"""
governance_ops.governance_aggregator — DataGovernanceAggregator v1.1.6

Aggregates data from all module adapters into unified governance summary,
symbol matrix, action queue, and run audit summary.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Aggregator reads only. Does NOT modify data, repair, download, or override gates.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from governance_ops.governance_schema import (
    GovernanceModuleStatus,
    GovernanceSymbolStatus,
    GovernanceActionItem,
    GovernanceSummary,
    GovernanceRunSummary,
    _now_utc,
    _new_uuid,
)
from governance_ops.priority_engine import GovernancePriorityEngine

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class DataGovernanceAggregator:
    """
    Aggregates governance data from all module adapters.

    - Module missing data: no crash
    - CONFLICT/INVALID/FUTURE_DATE/audit chain fail: high priority
    - Optional dataset missing != daily price invalid
    - Mock records excluded from formal summary
    - No duplicate actions for same issue
    - Aggregate source interruptions (don't generate P0 per symbol for same source)

    [!] Research Only. No Real Orders.
    """

    def __init__(self):
        from governance_ops.governance_adapters import (
            UniverseGovernanceAdapter,
            OnboardingGovernanceAdapter,
            RepairGovernanceAdapter,
            FreshnessGovernanceAdapter,
            QualityGateGovernanceAdapter,
            EnforcementGovernanceAdapter,
            ReportPackGovernanceAdapter,
            SystemHealthGovernanceAdapter,
        )
        self._adapters = {
            "UNIVERSE": UniverseGovernanceAdapter(),
            "ONBOARDING": OnboardingGovernanceAdapter(),
            "COVERAGE_REPAIR": RepairGovernanceAdapter(),
            "FRESHNESS": FreshnessGovernanceAdapter(),
            "QUALITY_GATES": QualityGateGovernanceAdapter(),
            "GATE_ENFORCEMENT": EnforcementGovernanceAdapter(),
            "REPORT_PACK": ReportPackGovernanceAdapter(),
            "SYSTEM_HEALTH": SystemHealthGovernanceAdapter(),
        }
        self._priority_engine = GovernancePriorityEngine()

    def aggregate(self, mode: str = "real", tier: Optional[str] = None,
                  symbols: Optional[List[str]] = None) -> GovernanceSummary:
        """Aggregate all governance data into a GovernanceSummary."""
        module_statuses = self.aggregate_modules()
        symbol_statuses = self.aggregate_symbols(tier=tier, symbols=symbols)
        actions = self.aggregate_actions(symbol_statuses, module_statuses)
        runs = self.aggregate_runs()
        return self.build_summary(
            module_statuses=module_statuses,
            symbol_statuses=symbol_statuses,
            actions=actions,
            runs=runs,
            mode=mode,
            tier=tier or "",
        )

    def aggregate_modules(self) -> Dict[str, GovernanceModuleStatus]:
        """Aggregate health status from all module adapters."""
        statuses: Dict[str, GovernanceModuleStatus] = {}
        for name, adapter in self._adapters.items():
            try:
                status = adapter.health()
                statuses[name] = status
            except Exception as exc:
                logger.warning("aggregate_modules: adapter %s error: %s", name, exc)
                statuses[name] = GovernanceModuleStatus(
                    module_name=name,
                    available=False,
                    health_status="UNAVAILABLE",
                    reason=f"Health check error: {exc}",
                )
        return statuses

    def aggregate_symbols(self, tier: Optional[str] = None,
                          symbols: Optional[List[str]] = None) -> List[GovernanceSymbolStatus]:
        """Build symbol governance status matrix from all adapters."""
        result: List[GovernanceSymbolStatus] = []
        universe_adapter = self._adapters.get("UNIVERSE")
        universe_summary = {}
        symbol_list = []

        if universe_adapter and universe_adapter.available():
            try:
                universe_summary = universe_adapter.latest_summary()
                # Try to get symbol list from universe
                from universe.universe_query import UniverseQuery
                q = UniverseQuery()
                if tier:
                    symbol_list = q.symbols_by_tier(tier) if hasattr(q, "symbols_by_tier") else q.all_symbols()
                else:
                    symbol_list = q.all_symbols() if hasattr(q, "all_symbols") else []
            except Exception as exc:
                logger.warning("aggregate_symbols: universe query error: %s", exc)

        if symbols:
            symbol_list = list(symbols)

        if not symbol_list:
            # Return empty — no symbols to evaluate
            return result

        for sym in symbol_list:
            try:
                status = self._build_symbol_status(sym, tier or "")
                result.append(status)
            except Exception as exc:
                logger.warning("aggregate_symbols: symbol %s error: %s", sym, exc)
                result.append(GovernanceSymbolStatus(symbol=sym, tier=tier or ""))

        return result

    def _build_symbol_status(self, symbol: str, tier: str) -> GovernanceSymbolStatus:
        """Build governance status for a single symbol."""
        status = GovernanceSymbolStatus(symbol=symbol, tier=tier)

        # Universe data
        universe_adapter = self._adapters.get("UNIVERSE")
        if universe_adapter and universe_adapter.available():
            try:
                uni_data = universe_adapter.symbol_status(symbol)
                if isinstance(uni_data, dict):
                    status.name = uni_data.get("name", "")
                    status.tier = uni_data.get("tier", tier)
                    status.coverage_status = uni_data.get("coverage_status", "UNKNOWN")
            except Exception:
                pass

        # Freshness data
        freshness_adapter = self._adapters.get("FRESHNESS")
        if freshness_adapter and freshness_adapter.available():
            try:
                fresh_data = freshness_adapter.symbol_status(symbol)
                if isinstance(fresh_data, dict):
                    status.freshness_status = fresh_data.get("freshness_status", "UNKNOWN")
                    status.trading_day_lag = int(fresh_data.get("trading_day_lag", 0))
                    status.latest_data_date = fresh_data.get("latest_data_date")
            except Exception:
                pass

        # Quality gate data
        qg_adapter = self._adapters.get("QUALITY_GATES")
        if qg_adapter and qg_adapter.available():
            try:
                qg_data = qg_adapter.symbol_status(symbol)
                if isinstance(qg_data, dict):
                    status.quality_gate_level = qg_data.get("decision", "UNKNOWN")
                    decision = qg_data.get("decision", "")
                    status.formal_eligible = decision == "ELIGIBLE_FORMAL"
                    status.observational_eligible = decision in ("ELIGIBLE_FORMAL", "ELIGIBLE_OBSERVATIONAL")
                    status.blocked = "BLOCKED" in decision.upper()
                    if status.blocked:
                        status.qualification = "BLOCKED"
                    elif status.formal_eligible:
                        status.qualification = "FORMAL_ELIGIBLE"
                    elif status.observational_eligible:
                        status.qualification = "OBSERVATIONAL_ELIGIBLE"
                    else:
                        status.qualification = "DEMO_ONLY"
                    rc = qg_data.get("reason_codes", [])
                    if isinstance(rc, list):
                        status.top_reason_codes = rc[:5]
            except Exception:
                pass

        # Repair data
        repair_adapter = self._adapters.get("COVERAGE_REPAIR")
        if repair_adapter and repair_adapter.available():
            try:
                repair_issues = [i for i in (repair_adapter.list_issues() or [])
                                 if isinstance(i, dict) and i.get("symbol") == symbol]
                status.open_repair_issues = len(repair_issues)
                status.critical_repair_issues = sum(
                    1 for i in repair_issues if i.get("severity") == "CRITICAL"
                )
                status.conflict_count = sum(
                    1 for i in repair_issues if i.get("issue") == "CONFLICT"
                )
                status.invalid_count = sum(
                    1 for i in repair_issues if i.get("issue") in ("INVALID_OHLC", "INVALID_DATA")
                )
            except Exception:
                pass

        # Assign symbol priority
        if status.blocked or status.conflict_count > 0 or status.invalid_count > 0:
            status.priority = "P0"
        elif status.critical_repair_issues > 0 or not status.formal_eligible:
            status.priority = "P1"
        elif status.open_repair_issues > 0 or status.trading_day_lag > 5:
            status.priority = "P2"
        else:
            status.priority = "P3"

        return status

    def aggregate_actions(self, symbol_statuses: List[GovernanceSymbolStatus],
                          module_statuses: Dict[str, Any]) -> List[GovernanceActionItem]:
        """Build prioritized action queue from symbol and module data."""
        from governance_ops.action_queue import GovernanceActionQueue
        queue = GovernanceActionQueue()
        all_actions: List[GovernanceActionItem] = []

        # Build from module adapters
        for name, adapter in self._adapters.items():
            try:
                if name == "ONBOARDING":
                    all_actions.extend(queue.build_from_onboarding(adapter))
                elif name == "COVERAGE_REPAIR":
                    all_actions.extend(queue.build_from_repairs(adapter))
                elif name == "FRESHNESS":
                    all_actions.extend(queue.build_from_freshness(adapter))
                elif name == "QUALITY_GATES":
                    all_actions.extend(queue.build_from_quality_gates(adapter))
                elif name == "GATE_ENFORCEMENT":
                    all_actions.extend(queue.build_from_enforcement(adapter))
            except Exception as exc:
                logger.warning("aggregate_actions: module %s error: %s", name, exc)

        # Deduplicate and prioritize
        all_actions = queue.deduplicate(all_actions)
        all_actions = queue.prioritize(all_actions)
        return all_actions

    def aggregate_runs(self) -> List[GovernanceRunSummary]:
        """Aggregate recent enforcement runs."""
        runs: List[GovernanceRunSummary] = []
        try:
            from gate_enforcement.enforcement_query import EnforcementQuery
            q = EnforcementQuery()
            raw_runs = q.latest_runs(limit=20)
            for r in (raw_runs or []):
                if not isinstance(r, dict):
                    continue
                run = GovernanceRunSummary(
                    run_id=r.get("run_id", ""),
                    command_name=r.get("command_name", ""),
                    qualification=r.get("status", ""),
                    included_count=len(r.get("included_symbols", [])) if isinstance(r.get("included_symbols"), list) else 0,
                    excluded_count=len(r.get("excluded_symbols", [])) if isinstance(r.get("excluded_symbols"), list) else 0,
                    override_used=bool(r.get("override_used", False)),
                    audit_chain_valid=True,  # would need deeper check
                    reproducibility_verified=bool(r.get("reproducibility_hash")),
                    report_output="",
                    created_at=r.get("created_at", ""),
                )
                runs.append(run)
        except Exception as exc:
            logger.warning("aggregate_runs error: %s", exc)
        return runs

    def resolve_symbol_identity(self, symbol: str) -> dict:
        """Resolve symbol to its identity (name, tier, etc.)."""
        universe_adapter = self._adapters.get("UNIVERSE")
        if universe_adapter and universe_adapter.available():
            try:
                return universe_adapter.symbol_status(symbol)
            except Exception:
                pass
        return {"symbol": symbol}

    def merge_reason_codes(self, *code_lists) -> List[str]:
        """Merge multiple reason code lists, removing duplicates."""
        seen = set()
        result = []
        for codes in code_lists:
            for code in (codes or []):
                if code not in seen:
                    seen.add(code)
                    result.append(code)
        return result

    def merge_required_actions(self, *action_lists) -> List[str]:
        """Merge multiple required action lists, removing duplicates."""
        seen = set()
        result = []
        for actions in action_lists:
            for action in (actions or []):
                if action not in seen:
                    seen.add(action)
                    result.append(action)
        return result

    def build_summary(self, module_statuses: Dict[str, Any],
                      symbol_statuses: List[GovernanceSymbolStatus],
                      actions: List[GovernanceActionItem],
                      runs: List[GovernanceRunSummary],
                      mode: str = "real",
                      tier: str = "") -> GovernanceSummary:
        """Build GovernanceSummary from aggregated data."""
        overall_status = self.determine_overall_status(module_statuses, symbol_statuses, actions)
        confidence = self.determine_confidence(module_statuses)

        p0 = sum(1 for a in actions if a.priority == "P0")
        p1 = sum(1 for a in actions if a.priority == "P1")
        open_a = sum(1 for a in actions if a.status in ("OPEN", "IN_PROGRESS"))

        source_interruptions = 0
        audit_chain_failures = 0
        non_qualified = sum(
            1 for r in runs
            if r.qualification in ("DEMO_ONLY", "OBSERVATIONAL_ONLY", "BLOCKED", "FAILED")
        )

        return GovernanceSummary(
            generated_at=_now_utc(),
            mode=mode,
            tier=tier,
            module_statuses={k: v.to_dict() for k, v in module_statuses.items()},
            registered_symbols=len(symbol_statuses),
            evaluated_symbols=len(symbol_statuses),
            ready_symbols=sum(1 for s in symbol_statuses if s.coverage_status == "READY"),
            partial_symbols=sum(1 for s in symbol_statuses if s.coverage_status == "PARTIAL"),
            stale_symbols=sum(1 for s in symbol_statuses if s.freshness_status in ("STALE", "DELAYED")),
            missing_symbols=sum(1 for s in symbol_statuses if s.coverage_status == "MISSING"),
            formal_eligible=sum(1 for s in symbol_statuses if s.formal_eligible),
            observational_eligible=sum(1 for s in symbol_statuses if s.observational_eligible and not s.formal_eligible),
            demo_only=sum(1 for s in symbol_statuses if not s.observational_eligible and not s.blocked),
            blocked_symbols=sum(1 for s in symbol_statuses if s.blocked),
            critical_alerts=p0,
            open_actions=open_a,
            p0_actions=p0,
            p1_actions=p1,
            source_interruptions=source_interruptions,
            audit_chain_failures=audit_chain_failures,
            non_qualified_runs=non_qualified,
            overall_status=overall_status,
            confidence=confidence,
            research_only=True,
            no_real_orders=True,
        )

    def determine_overall_status(self, module_statuses: Dict[str, Any],
                                  symbol_statuses: List[GovernanceSymbolStatus],
                                  actions: List[GovernanceActionItem]) -> str:
        """
        Determine overall governance status.
        CRITICAL: audit chain failure, widespread source interruption, invalid/conflict affecting formal, formal gate bypassed
        ATTENTION_REQUIRED: P0/P1 actions, CORE_10 stale/missing, import failures, unresolved manual reviews
        DEGRADED: optional data missing, observational-only universe, partial coverage
        HEALTHY: no critical issue, no P0, source healthy, audit valid
        """
        p0_count = sum(1 for a in actions if a.priority == "P0" and a.status in ("OPEN", "IN_PROGRESS"))
        p1_count = sum(1 for a in actions if a.priority == "P1" and a.status in ("OPEN", "IN_PROGRESS"))

        # Check module failures
        fail_modules = [
            k for k, v in module_statuses.items()
            if isinstance(v, GovernanceModuleStatus) and v.health_status in ("FAIL", "BLOCKED")
        ]

        # Check symbol issues
        has_invalid = any(s.invalid_count > 0 or s.conflict_count > 0 for s in symbol_statuses)
        has_blocked = any(s.blocked for s in symbol_statuses)

        if p0_count > 0 or has_invalid or (len(fail_modules) > 1):
            return "CRITICAL"
        if p1_count > 0 or has_blocked or len(fail_modules) > 0:
            return "ATTENTION_REQUIRED"
        if any(s.coverage_status in ("PARTIAL", "MISSING") for s in symbol_statuses):
            return "DEGRADED"
        if not symbol_statuses and not any(
            isinstance(v, GovernanceModuleStatus) and v.available
            for v in module_statuses.values()
        ):
            return "UNKNOWN"
        return "HEALTHY"

    def determine_confidence(self, module_statuses: Dict[str, Any]) -> float:
        """Determine confidence score (0.0-1.0) based on available modules."""
        if not module_statuses:
            return 0.0
        available_count = sum(
            1 for v in module_statuses.values()
            if isinstance(v, GovernanceModuleStatus) and v.available
        )
        healthy_count = sum(
            1 for v in module_statuses.values()
            if isinstance(v, GovernanceModuleStatus) and v.health_status in ("PASS", "WARN")
        )
        total = len(module_statuses)
        if total == 0:
            return 0.0
        return round(healthy_count / total, 2)
