"""
paper_trading/multi_session/conflict_resolver_v166.py — Conflict Resolver v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List
from paper_trading.multi_session.enums_v166 import ConflictType, ConflictSeverity, CoordinationOutcome
from paper_trading.multi_session.models_v166 import SessionConflict

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True


class ConflictResolver:
    """Resolves detected conflicts using policy rules. No auto-action on production."""

    def resolve(
        self,
        conflict: SessionConflict,
        policy_rules: Dict[str, Any],
    ) -> Dict[str, Any]:
        resolution: Dict[str, Any] = {
            "conflict_id": conflict.conflict_id,
            "conflict_type": conflict.conflict_type.value,
            "outcome": CoordinationOutcome.PASS.value,
            "action": "none",
            "affected_sessions": [],
            "warnings": [],
        }

        if conflict.conflict_type == ConflictType.SYMBOL_OVERLAP:
            overlap_action = policy_rules.get("symbol_overlap_rules", {}).get("same_direction_over_concentration", "WARN")
            if overlap_action == "BLOCK":
                resolution["outcome"] = CoordinationOutcome.BLOCK.value
                resolution["action"] = "block_lower_priority"
                resolution["affected_sessions"] = conflict.session_ids[1:]
            else:
                resolution["outcome"] = CoordinationOutcome.WARN.value
                resolution["action"] = "warn_overlap"
                resolution["warnings"] = [f"Symbol overlap: {conflict.symbol}"]

        elif conflict.conflict_type == ConflictType.STRATEGY_CONFLICT:
            resolution["outcome"] = CoordinationOutcome.WARN.value
            resolution["action"] = "warn_strategy"
            resolution["warnings"] = [f"Duplicate strategy: {conflict.strategy}"]

        elif conflict.conflict_type == ConflictType.CAPITAL_OVERALLOCATION:
            resolution["outcome"] = CoordinationOutcome.BLOCK.value
            resolution["action"] = "block_lowest_priority"
            resolution["affected_sessions"] = conflict.session_ids

        elif conflict.conflict_type == ConflictType.RISK_BUDGET_EXCEEDED:
            resolution["outcome"] = CoordinationOutcome.BLOCK.value
            resolution["action"] = "block_lowest_priority"

        elif conflict.conflict_type == ConflictType.DEADLOCK:
            resolution["outcome"] = CoordinationOutcome.BLOCK.value
            resolution["action"] = "mark_blocked_recommend_release"
            resolution["warnings"] = ["Deadlock detected — manual resolution required"]

        elif conflict.conflict_type == ConflictType.STARVATION:
            resolution["outcome"] = CoordinationOutcome.WARN.value
            resolution["action"] = "recommend_escalation"
            resolution["warnings"] = ["Starvation detected — recommend priority adjustment"]

        elif conflict.conflict_type in (ConflictType.STALE_HEARTBEAT, ConflictType.LEASE_EXPIRED):
            resolution["outcome"] = CoordinationOutcome.WARN.value
            resolution["action"] = "mark_stale_require_review"

        else:
            if conflict.blocking:
                resolution["outcome"] = CoordinationOutcome.BLOCK.value
                resolution["action"] = "block"
            else:
                resolution["outcome"] = CoordinationOutcome.WARN.value
                resolution["action"] = "warn"

        return resolution

    def resolve_all(
        self,
        conflicts: List[SessionConflict],
        policy_rules: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        return [self.resolve(c, policy_rules) for c in conflicts]
