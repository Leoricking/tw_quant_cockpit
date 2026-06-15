"""
gate_enforcement.run_snapshot — RunGateSnapshotBuilder v1.1.5

Captures and saves run-level gate snapshots.
Research Only. No Real Orders.
Must NOT contain secrets, tokens, credentials, or .env content.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from gate_enforcement.enforcement_schema import (
    GateEnforcementRequest, GateEnforcementResult, RunGateSnapshot,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


class RunGateSnapshotBuilder:
    """
    Builds and saves RunGateSnapshot objects.
    Does NOT capture secrets, tokens, credentials, or .env content.
    """

    def capture(
        self,
        request: GateEnforcementRequest,
        enforcement_result: GateEnforcementResult,
        decisions: dict,
        output_dir: str = "data/quality_gate_enforcement",
    ) -> RunGateSnapshot:
        """Build and save a snapshot from request + result."""
        snapshot = self.build_snapshot(request, enforcement_result, decisions)
        self.save_snapshot(snapshot, output_dir=output_dir)
        return snapshot

    def capture_coverage(self, symbols: List[str]) -> dict:
        """Capture coverage state for symbols (reads from coverage store if available)."""
        state = {}
        for sym in symbols:
            try:
                from coverage_repair.repair_store import CoverageRepairStore
                store = CoverageRepairStore()
                issues = store.list_issues(symbol=sym)
                open_count = len([i for i in issues if i.get("status") == "OPEN"])
                state[sym] = {"open_issues": open_count}
            except Exception:
                state[sym] = {"open_issues": 0}
        return state

    def capture_freshness(self, symbols: List[str]) -> dict:
        """Capture freshness state for symbols."""
        state = {}
        for sym in symbols:
            try:
                from data_freshness.freshness_store import FreshnessStore
                store = FreshnessStore()
                record = store.get_latest(sym)
                if record:
                    state[sym] = {
                        "freshness_status": record.get("freshness_status", "UNKNOWN"),
                        "trading_day_lag": record.get("trading_day_lag", -1),
                    }
                else:
                    state[sym] = {"freshness_status": "UNKNOWN", "trading_day_lag": -1}
            except Exception:
                state[sym] = {"freshness_status": "UNKNOWN", "trading_day_lag": -1}
        return state

    def capture_repairs(self, symbols: List[str]) -> dict:
        """Capture open repair issue counts for symbols."""
        state = {}
        for sym in symbols:
            try:
                from coverage_repair.repair_store import CoverageRepairStore
                store = CoverageRepairStore()
                issues = store.list_issues(symbol=sym)
                critical = len([i for i in issues if i.get("severity") == "CRITICAL" and i.get("status") == "OPEN"])
                total = len([i for i in issues if i.get("status") == "OPEN"])
                state[sym] = {"critical_open": critical, "total_open": total}
            except Exception:
                state[sym] = {"critical_open": 0, "total_open": 0}
        return state

    def capture_onboarding(self, symbols: List[str]) -> dict:
        """Capture onboarding/import status for symbols."""
        state = {}
        for sym in symbols:
            state[sym] = {"onboarding_status": "UNKNOWN"}
        return state

    def capture_sources(self, symbols: List[str]) -> dict:
        """Capture source/version identifiers for symbols (no secrets)."""
        state = {}
        try:
            from release.version_info import VERSION
            state["code_version"] = VERSION
        except Exception:
            state["code_version"] = "unknown"
        state["symbols"] = symbols
        return state

    def capture_confidence(self, decisions: dict) -> Optional[float]:
        """Compute average confidence proxy from decisions."""
        if not decisions:
            return None
        level_scores = {
            "ELIGIBLE_FORMAL": 1.0,
            "ELIGIBLE_OBSERVATIONAL": 0.6,
            "DEMO_ONLY": 0.3,
        }
        scores = [level_scores.get(v, 0.0) for v in decisions.values()]
        if not scores:
            return None
        return round(sum(scores) / len(scores), 4)

    def build_snapshot(
        self,
        request: GateEnforcementRequest,
        enforcement_result: GateEnforcementResult,
        decisions: dict,
    ) -> RunGateSnapshot:
        """Build a RunGateSnapshot from enforcement request and result."""
        symbols_all = request.requested_symbols or []
        coverage_state = self.capture_coverage(symbols_all)
        freshness_state = self.capture_freshness(symbols_all)
        repair_state = self.capture_repairs(symbols_all)
        onboarding_state = self.capture_onboarding(symbols_all)
        source_versions = self.capture_sources(symbols_all)
        confidence = self.capture_confidence(decisions)

        # Build payload hash
        from gate_enforcement.reproducibility import RunReproducibilityHasher
        hasher = RunReproducibilityHasher()
        payload_hash = hasher.build_run_hash(
            code_version=source_versions.get("code_version", "unknown"),
            command_name=request.command_name,
            arguments=request.arguments,
            gate_name=request.gate_name,
            gate_policy_version=enforcement_result.policy_version,
            included_symbols=enforcement_result.included_symbols,
            excluded_symbols=enforcement_result.excluded_symbols,
            decisions=decisions,
            coverage_state=coverage_state,
            freshness_state=freshness_state,
            statistical_confidence=confidence,
        )

        return RunGateSnapshot(
            snapshot_id=_new_uuid(),
            run_id=request.run_id,
            command_name=request.command_name,
            gate_name=request.gate_name,
            gate_policy_version=enforcement_result.policy_version,
            requested_level=request.requested_level,
            applied_level=enforcement_result.applied_level,
            symbols_requested=request.requested_symbols,
            symbols_evaluated=enforcement_result.evaluated_symbols,
            symbols_included=enforcement_result.included_symbols,
            symbols_excluded=enforcement_result.excluded_symbols,
            decision_ids=[],
            source_versions=source_versions,
            coverage_state=coverage_state,
            freshness_state=freshness_state,
            repair_state=repair_state,
            onboarding_state=onboarding_state,
            statistical_confidence=confidence,
            generated_at=_now_utc(),
            payload_hash=payload_hash,
        )

    def save_snapshot(
        self, snapshot: RunGateSnapshot,
        output_dir: str = "data/quality_gate_enforcement",
    ) -> str:
        """Save snapshot to JSONL file. Returns file path."""
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "run_snapshots.jsonl")
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(snapshot.to_dict(), ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.error("Failed to save snapshot: %s", exc)
        return path

    def verify_snapshot(self, snapshot_id: str, output_dir: str = "data/quality_gate_enforcement") -> bool:
        """Verify a snapshot exists in the JSONL store by snapshot_id."""
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        path = os.path.join(output_dir, "run_snapshots.jsonl")
        if not os.path.isfile(path):
            return False
        try:
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        if d.get("snapshot_id") == snapshot_id:
                            return True
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass
        return False
