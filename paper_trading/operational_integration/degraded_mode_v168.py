"""
paper_trading/operational_integration/degraded_mode_v168.py
Degraded Mode Handler for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List

from .models_v168 import DegradedState
from .enums_v168 import DegradedReason, FailureSeverity, ConfidenceLevel

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class DegradedModeHandler:
    """Handles degraded mode detection and propagation. Research only."""

    def check_stale_market_data(self, data: Dict[str, Any]) -> DegradedState:
        """Check if market data is stale enough to trigger degraded mode."""
        max_age = data.get("max_age_seconds", 3600)
        last_update = data.get("last_update", "")
        is_stale = False
        if last_update:
            now = datetime.now(timezone.utc)
            try:
                ts = datetime.fromisoformat(last_update.replace("Z", "+00:00"))
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                age = (now - ts).total_seconds()
                is_stale = age > max_age
            except Exception:
                is_stale = True
        return DegradedState(
            component_id=data.get("component_id", "market_data"),
            reasons=[DegradedReason.STALE_MARKET_DATA] if is_stale else [],
            severity=FailureSeverity.HIGH if is_stale else FailureSeverity.INFO,
            confidence=ConfidenceLevel.HIGH,
            blocking=False,
        )

    def check_missing_benchmark(self, attrs: Dict[str, Any]) -> DegradedState:
        """Check if benchmark is missing."""
        has_benchmark = "benchmark_return" in attrs and attrs["benchmark_return"] is not None
        return DegradedState(
            component_id=attrs.get("component_id", "attribution"),
            reasons=[DegradedReason.MISSING_BENCHMARK] if not has_benchmark else [],
            severity=FailureSeverity.MEDIUM if not has_benchmark else FailureSeverity.INFO,
            confidence=ConfidenceLevel.HIGH,
            blocking=False,
        )

    def check_partial_execution(self, executions: List[Dict[str, Any]]) -> DegradedState:
        """Check if any executions are partial/incomplete."""
        partial = [e for e in executions if e.get("status") == "PARTIAL_FILL"]
        has_partial = len(partial) > 0
        return DegradedState(
            component_id="execution",
            reasons=[DegradedReason.PARTIAL_EXECUTION] if has_partial else [],
            severity=FailureSeverity.MEDIUM if has_partial else FailureSeverity.INFO,
            confidence=ConfidenceLevel.HIGH,
            blocking=False,
        )

    def check_unknown_cost(self, costs: Dict[str, Any]) -> DegradedState:
        """Check if any costs are unknown/estimated."""
        has_unknown = any(
            costs.get(k, "KNOWN") in ("UNKNOWN", "ESTIMATED")
            for k in costs
        )
        return DegradedState(
            component_id=costs.get("component_id", "cost"),
            reasons=[DegradedReason.UNKNOWN_COST] if has_unknown else [],
            severity=FailureSeverity.LOW if has_unknown else FailureSeverity.INFO,
            confidence=ConfidenceLevel.MEDIUM,
            blocking=False,
        )

    def check_incomplete_lineage(self, lineage: Dict[str, Any]) -> DegradedState:
        """Check if lineage chain is incomplete."""
        is_complete = lineage.get("chain_complete", True) and not lineage.get("broken", False)
        return DegradedState(
            component_id=lineage.get("component_id", "lineage"),
            reasons=[DegradedReason.INCOMPLETE_LINEAGE] if not is_complete else [],
            severity=FailureSeverity.MEDIUM if not is_complete else FailureSeverity.INFO,
            confidence=ConfidenceLevel.HIGH,
            blocking=False,
        )

    def propagate(
        self, upstream_state: DegradedState, downstream_component: str
    ) -> DegradedState:
        """Propagate degraded state from upstream to downstream component."""
        if not upstream_state.reasons:
            return DegradedState(component_id=downstream_component)
        return DegradedState(
            component_id=downstream_component,
            reasons=upstream_state.reasons + [DegradedReason.FAILED_CHILD],
            severity=upstream_state.severity,
            confidence=ConfidenceLevel.MEDIUM,
            downstream_affected=upstream_state.downstream_affected + [downstream_component],
            blocking=upstream_state.blocking,
        )

    def can_upgrade_to_complete(self, state: DegradedState) -> bool:
        """
        Return True only if degraded state is fully resolved.
        Returns False unless all degraded reasons are cleared.
        """
        if not state.reasons:
            return True
        return False

    def summarize(self, states: List[DegradedState]) -> Dict[str, Any]:
        """Return summary of degraded states."""
        total = len(states)
        degraded = sum(1 for s in states if len(s.reasons) > 0)
        blocking = sum(1 for s in states if s.blocking)
        all_reasons = []
        for s in states:
            all_reasons.extend([r.value for r in s.reasons])
        return {
            "total_components": total,
            "degraded_count": degraded,
            "blocking_count": blocking,
            "reason_distribution": {r: all_reasons.count(r) for r in set(all_reasons)},
            "paper_only": True,
        }
