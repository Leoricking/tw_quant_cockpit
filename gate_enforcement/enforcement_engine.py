"""
gate_enforcement.enforcement_engine — QualityGateEnforcementEngine v1.1.5

Main enforcement engine that orchestrates the full gate enforcement flow.
Research Only. No Real Orders. No broker. No orders.

Flow:
1. Create GateEnforcementRequest
2. Resolve gate
3. Get v1.1.4 decisions (from quality_gates package)
4. Filter symbols by requested level
5. Build exclusion records
6. Validate override
7. Build snapshot
8. Build reproducibility hash
9. Write audit
10. Return included symbols + enforcement context

Rules:
- Gate engine failure => MUST NOT fallback allow-all => formal run BLOCKED
- audit-only mode: preserve original symbols but show WARNING
- off mode: label non-qualified
- No auto-override, no broker, no orders

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from gate_enforcement.enforcement_schema import (
    GateEnforcementRequest,
    GateEnforcementResult,
    EnforcementAuditEvent,
)
from gate_enforcement.enforcement_policy import QualityGateEnforcementPolicy
from gate_enforcement.run_gate_resolver import RunGateResolver
from gate_enforcement.symbol_filter import QualityGateSymbolFilter
from gate_enforcement.run_snapshot import RunGateSnapshotBuilder
from gate_enforcement.reproducibility import RunReproducibilityHasher
from gate_enforcement.audit_log import QualityGateAuditLog

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


class QualityGateEnforcementEngine:
    """
    Orchestrates quality gate enforcement for research runs.
    No broker. No orders. Research only.
    """

    def __init__(
        self,
        output_dir: str = "data/quality_gate_enforcement",
        audit_dir: str = "data/quality_gate_audit",
    ):
        self._policy = QualityGateEnforcementPolicy()
        self._resolver = RunGateResolver()
        self._symbol_filter = QualityGateSymbolFilter()
        self._snapshot_builder = RunGateSnapshotBuilder()
        self._hasher = RunReproducibilityHasher()
        self._output_dir = output_dir if os.path.isabs(output_dir) else os.path.join(BASE_DIR, output_dir)
        self._audit_dir = audit_dir if os.path.isabs(audit_dir) else os.path.join(BASE_DIR, audit_dir)
        self._audit_log = QualityGateAuditLog(audit_dir=self._audit_dir)

    def enforce(
        self,
        command_name: str,
        args,
        symbols: List[str],
        mode: str = "real",
    ) -> Tuple[List[str], GateEnforcementResult]:
        """
        Main enforcement entry point. Returns (included_symbols, result).
        Gate engine failure => formal run BLOCKED (never fallback allow-all).
        """
        try:
            request = self._resolver.resolve_request(command_name, args, mode)
            request.requested_symbols = symbols or request.requested_symbols
        except Exception as exc:
            logger.error("Failed to resolve enforcement request: %s", exc)
            return [], self.fail_run(
                run_id=_new_uuid(),
                gate_name="UNKNOWN",
                requested_level="FORMAL",
                reason=f"Request resolution failed: {exc}",
            )

        # Check for unknown gate
        if request.gate_name == "UNKNOWN_GATE":
            return [], self.fail_run(
                run_id=request.run_id,
                gate_name=request.gate_name,
                requested_level=request.requested_level,
                reason=f"Unknown gate for command '{command_name}'",
            )

        return self.enforce_symbol_run(request)

    def enforce_symbol_run(
        self, request: GateEnforcementRequest
    ) -> Tuple[List[str], GateEnforcementResult]:
        """Run enforcement for a set of symbols."""
        try:
            decisions = self.evaluate_decisions(request.requested_symbols)
        except Exception as exc:
            logger.error("Failed to evaluate gate decisions: %s", exc)
            # gate engine failure => BLOCKED, not allow-all
            return [], self.fail_run(
                run_id=request.run_id,
                gate_name=request.gate_name,
                requested_level=request.requested_level,
                reason=f"Decision evaluation failed: {exc}",
            )

        quality_gate_mode = request.quality_gate_mode
        requested_level = request.requested_level

        # audit-only mode: preserve symbols but warn
        if quality_gate_mode == "AUDIT_ONLY":
            filter_result = {
                "included": list(request.requested_symbols),
                "excluded": [],
                "formal": [],
                "observational": [],
                "demo": [],
                "blocked": [],
                "exclusion_records": [],
                "status": "PASSED_WITH_WARNINGS",
                "warnings": [
                    "AUDIT_ONLY mode: original symbols preserved. "
                    "Results are NOT formally qualified."
                ],
            }
        elif quality_gate_mode == "OFF":
            filter_result = {
                "included": list(request.requested_symbols),
                "excluded": [],
                "formal": [],
                "observational": [],
                "demo": [],
                "blocked": [],
                "exclusion_records": [],
                "status": "PASSED_WITH_WARNINGS",
                "warnings": [self._policy.off_mode_label()],
            }
        else:
            try:
                filter_result = self.apply_filter(
                    request.requested_symbols, decisions, requested_level
                )
            except Exception as exc:
                logger.error("Symbol filter failed: %s", exc)
                return [], self.fail_run(
                    run_id=request.run_id,
                    gate_name=request.gate_name,
                    requested_level=requested_level,
                    reason=f"Symbol filter failed: {exc}",
                )

        included = filter_result.get("included", [])
        applied_level = requested_level if included else "BLOCKED"

        result = self.finalize(request, filter_result, decisions, applied_level)

        try:
            snapshot = self.build_snapshot(request, result, decisions)
            result.decision_snapshot_id = snapshot.snapshot_id
        except Exception as exc:
            logger.warning("Snapshot build failed (non-fatal): %s", exc)

        try:
            self.write_audit(request, result, filter_result)
        except Exception as exc:
            logger.warning("Audit write failed (non-fatal): %s", exc)

        try:
            self._save_result(request, result)
        except Exception as exc:
            logger.warning("Result store failed (non-fatal): %s", exc)

        return included, result

    def enforce_universe_run(
        self, command_name: str, tier: str, args, mode: str = "real"
    ) -> Tuple[List[str], GateEnforcementResult]:
        """Run enforcement for a universe tier."""
        symbols = []
        try:
            from universe.universe_store import UniverseStore
            store = UniverseStore()
            symbols = store.get_symbols(tier=tier)
        except Exception as exc:
            logger.warning("Could not load universe tier '%s': %s", tier, exc)
        return self.enforce(command_name, args, symbols, mode)

    def enforce_module_run(
        self, command_name: str, module_name: str, args, mode: str = "real"
    ) -> Tuple[List[str], GateEnforcementResult]:
        """Run enforcement for a specific module."""
        return self.enforce(command_name, args, [], mode)

    def evaluate_decisions(self, symbols: List[str]) -> Dict[str, str]:
        """
        Get quality gate decisions for symbols from v1.1.4 quality_gates package.
        Returns dict: symbol -> decision string.
        """
        decisions = {}
        try:
            from quality_gates.gate_decision_engine import CoverageQualityGateEngine
            engine = CoverageQualityGateEngine()
            for symbol in symbols:
                try:
                    decision_obj = engine.evaluate_symbol(symbol, "price_backtest", mode="real")
                    if hasattr(decision_obj, "decision"):
                        decisions[symbol] = decision_obj.decision
                    elif isinstance(decision_obj, dict):
                        decisions[symbol] = decision_obj.get("decision", "BLOCKED_DATA_QUALITY")
                    else:
                        decisions[symbol] = "BLOCKED_DATA_QUALITY"
                except Exception as exc:
                    logger.warning("Decision failed for symbol '%s': %s", symbol, exc)
                    decisions[symbol] = "BLOCKED_DATA_QUALITY"
        except ImportError:
            logger.warning("quality_gates package not available; defaulting all symbols to BLOCKED")
            for symbol in symbols:
                decisions[symbol] = "BLOCKED_DATA_QUALITY"
        return decisions

    def apply_filter(
        self, symbols: List[str], decisions: Dict[str, str], required_level: str
    ) -> dict:
        return self._symbol_filter.filter_symbols(symbols, decisions, required_level)

    def build_snapshot(
        self, request: GateEnforcementRequest, result: GateEnforcementResult, decisions: dict
    ):
        return self._snapshot_builder.capture(
            request, result, decisions, output_dir=self._output_dir
        )

    def write_audit(
        self, request: GateEnforcementRequest, result: GateEnforcementResult, filter_result: dict
    ) -> None:
        """Write audit events for the run."""
        try:
            # Request created event
            event = EnforcementAuditEvent(
                event_id=_new_uuid(),
                run_id=request.run_id,
                event_type="REQUEST_CREATED",
                actor="researcher",
                timestamp=_now_utc(),
                command_name=request.command_name,
                symbol=None,
                gate_name=request.gate_name,
                previous_state=None,
                new_state=request.requested_level,
                reason="Enforcement request created",
                metadata={"mode": request.mode, "tier": request.tier},
                immutable_hash="",
            )
            self._audit_log.append(event)

            # Gate evaluated event
            gate_event = EnforcementAuditEvent(
                event_id=_new_uuid(),
                run_id=request.run_id,
                event_type="GATE_EVALUATED",
                actor="system",
                timestamp=_now_utc(),
                command_name=request.command_name,
                symbol=None,
                gate_name=request.gate_name,
                previous_state=None,
                new_state=result.status,
                reason=f"Gate evaluated: {result.status}",
                metadata={
                    "included": len(result.included_symbols),
                    "excluded": len(result.excluded_symbols),
                },
                immutable_hash="",
            )
            self._audit_log.append(gate_event)

            # Completion event
            self._audit_log.record_completion(
                run_id=request.run_id,
                status=result.status,
                reproducibility_hash=result.reproducibility_hash or "",
            )
        except Exception as exc:
            logger.warning("write_audit non-fatal error: %s", exc)

    def finalize(
        self,
        request: GateEnforcementRequest,
        filter_result: dict,
        decisions: dict,
        applied_level: str,
    ) -> GateEnforcementResult:
        """Build the final GateEnforcementResult."""
        included = filter_result.get("included", [])
        excluded = filter_result.get("excluded", [])
        formal = filter_result.get("formal", [])
        observational = filter_result.get("observational", [])
        demo = filter_result.get("demo", [])
        blocked = filter_result.get("blocked", [])
        warnings = filter_result.get("warnings", [])
        status = filter_result.get("status", "PASSED")
        exclusion_records = filter_result.get("exclusion_records", [])

        exclusion_reasons = {}
        for rec in exclusion_records:
            sym = rec.symbol if hasattr(rec, "symbol") else rec.get("symbol", "")
            reasons = rec.reasons if hasattr(rec, "reasons") else rec.get("reasons", [])
            exclusion_reasons[sym] = reasons

        # Build reproducibility hash
        try:
            repro_hash = self._hasher.build_run_hash(
                code_version="1.1.5",
                command_name=request.command_name,
                arguments=request.arguments,
                gate_name=request.gate_name,
                gate_policy_version=self._policy.POLICY_VERSION,
                included_symbols=included,
                excluded_symbols=excluded,
                decisions=decisions,
            )
        except Exception:
            repro_hash = ""

        return GateEnforcementResult(
            run_id=request.run_id,
            gate_name=request.gate_name,
            requested_level=request.requested_level,
            applied_level=applied_level,
            requested_symbols=request.requested_symbols,
            evaluated_symbols=list(decisions.keys()),
            included_symbols=included,
            formal_symbols=formal,
            observational_symbols=observational,
            demo_symbols=demo,
            blocked_symbols=blocked,
            excluded_symbols=excluded,
            exclusion_reasons=exclusion_reasons,
            warnings=warnings,
            override_used=bool(request.override_id),
            override_id=request.override_id,
            policy_version=self._policy.POLICY_VERSION,
            decision_snapshot_id=None,
            freshness_snapshot_id=None,
            coverage_snapshot_id=None,
            reproducibility_hash=repro_hash,
            status=status,
            created_at=_now_utc(),
        )

    def fail_run(
        self,
        run_id: str,
        gate_name: str,
        requested_level: str,
        reason: str = "",
    ) -> GateEnforcementResult:
        """Return a FAILED enforcement result. Does NOT allow-all."""
        logger.error("Gate enforcement FAILED for run_id=%s: %s", run_id, reason)
        return GateEnforcementResult(
            run_id=run_id,
            gate_name=gate_name,
            requested_level=requested_level,
            applied_level="BLOCKED",
            requested_symbols=[],
            evaluated_symbols=[],
            included_symbols=[],
            formal_symbols=[],
            observational_symbols=[],
            demo_symbols=[],
            blocked_symbols=[],
            excluded_symbols=[],
            exclusion_reasons={},
            warnings=[f"Run FAILED: {reason}"],
            override_used=False,
            override_id=None,
            policy_version=self._policy.POLICY_VERSION,
            decision_snapshot_id=None,
            freshness_snapshot_id=None,
            coverage_snapshot_id=None,
            reproducibility_hash=None,
            status="FAILED",
            created_at=_now_utc(),
        )

    def _save_result(self, request: GateEnforcementRequest, result: GateEnforcementResult) -> None:
        """Save result to enforcement store (non-fatal)."""
        try:
            from gate_enforcement.enforcement_store import EnforcementStore
            store = EnforcementStore(output_dir=self._output_dir)
            store.save_request(request)
            store.save_result(result)
        except Exception as exc:
            logger.warning("_save_result failed (non-fatal): %s", exc)
