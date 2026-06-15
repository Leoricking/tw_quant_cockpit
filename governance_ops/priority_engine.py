"""
governance_ops.priority_engine — GovernancePriorityEngine v1.1.6

Assigns priority scores to governance action items.
Does NOT consider: expected return, stock movement, popularity, trading signals, profit.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Dict, List

from governance_ops.governance_schema import GovernanceActionItem

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Priority score thresholds
_P0_SCORE = 1000
_P1_SCORE = 500
_P2_SCORE = 200
_P3_SCORE = 0

# P0 action types — critical, must be addressed
_P0_ACTION_TYPES = {
    "REVIEW_INVALID_DATA",
    "REVIEW_CONFLICT",
    "VERIFY_REPRODUCIBILITY",
    "REVIEW_AUDIT_FAILURE",
    "REVIEW_GATE_BLOCK",
}

# P0 reason codes
_P0_REASON_CODES = {
    "AUDIT_CHAIN_INVALID",
    "FUTURE_DATE",
    "DATE_REGRESSION",
    "CONFLICTING_PRICE_DATA",
    "INVALID_OHLC",
    "FORMAL_GATE_BYPASS",
    "WIDESPREAD_SOURCE_INTERRUPTION",
}

# P1 reason codes
_P1_REASON_CODES = {
    "CORE_10_STALE",
    "CORE_10_MISSING",
    "IMPORT_FAILURE_BLOCKING_FORMAL",
    "CRITICAL_REPAIR_OPEN",
    "MANUAL_REVIEW_BLOCKING_FORMAL",
}

# P2 reason codes
_P2_REASON_CODES = {
    "RESEARCH_30_PARTIAL",
    "CHIPS_DATA_DELAYED",
    "REVENUE_DATA_DELAYED",
    "OBSERVATIONAL_ONLY_QUALIFICATION",
    "REPORT_QUALIFICATION_WARNING",
}


class GovernancePriorityEngine:
    """
    Assigns priority scores to governance action items.

    Priority rules:
    - P0: audit chain invalid, future date, date regression, conflicting price data,
          invalid OHLC, formal gate bypass, widespread source interruption
    - P1: CORE_10 stale/missing, import failure blocking formal, critical repair open,
          manual review blocking formal
    - P2: RESEARCH_30 partial, chips/revenue delayed, observational-only qualification,
          report qualification warning
    - P3: optional metadata, broad100 incomplete, documentation/minor warning

    [!] Research Only. No Real Orders.
    """

    def score(self, action: GovernanceActionItem) -> int:
        """Return integer priority score (higher = more urgent)."""
        base = 0

        # P0 action types
        if action.action_type in _P0_ACTION_TYPES:
            base = max(base, _P0_SCORE)

        # P0 reason codes
        for rc in (action.reason_codes or []):
            if rc in _P0_REASON_CODES:
                base = max(base, _P0_SCORE)
            elif rc in _P1_REASON_CODES:
                base = max(base, _P1_SCORE)
            elif rc in _P2_REASON_CODES:
                base = max(base, _P2_SCORE)

        # Boost for blocked actions
        if action.blocked:
            base = max(base, _P1_SCORE)

        # Boost for CORE tier
        if action.dataset and "CORE" in action.dataset.upper():
            base = max(base, _P1_SCORE)

        # Boost for source data required
        if action.requires_source_data:
            base = max(base, _P1_SCORE)

        # Known P0 action types by keyword
        title_lower = (action.title or "").lower()
        if any(kw in title_lower for kw in ["audit chain", "future date", "date regression", "conflicting price", "invalid ohlc", "gate bypass"]):
            base = max(base, _P0_SCORE)

        return base

    def assign_priority(self, action: GovernanceActionItem) -> str:
        """Return priority string (P0/P1/P2/P3)."""
        s = self.score(action)
        if s >= _P0_SCORE:
            return "P0"
        if s >= _P1_SCORE:
            return "P1"
        if s >= _P2_SCORE:
            return "P2"
        return "P3"

    def explain_priority(self, action: GovernanceActionItem) -> str:
        """Return human-readable explanation of the priority assignment."""
        s = self.score(action)
        p = self.assign_priority(action)
        reasons = []

        if action.action_type in _P0_ACTION_TYPES:
            reasons.append(f"action_type={action.action_type} is P0")
        for rc in (action.reason_codes or []):
            if rc in _P0_REASON_CODES:
                reasons.append(f"reason_code={rc} is P0")
            elif rc in _P1_REASON_CODES:
                reasons.append(f"reason_code={rc} is P1")
        if action.blocked:
            reasons.append("action is BLOCKED")
        if action.requires_source_data:
            reasons.append("requires_source_data=True")

        reason_str = "; ".join(reasons) if reasons else "no special escalation"
        return f"Priority={p} (score={s}): {reason_str}"

    def group_by_priority(self, actions: List[GovernanceActionItem]) -> Dict[str, List[GovernanceActionItem]]:
        """Group action items by their priority."""
        groups: Dict[str, List[GovernanceActionItem]] = {
            "P0": [], "P1": [], "P2": [], "P3": [],
        }
        for action in actions:
            p = action.priority or self.assign_priority(action)
            if p in groups:
                groups[p].append(action)
            else:
                groups["P3"].append(action)
        return groups

    def top_actions(self, actions: List[GovernanceActionItem], limit: int = 10) -> List[GovernanceActionItem]:
        """Return top N actions sorted by priority (P0 first) then score."""
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        sorted_actions = sorted(
            actions,
            key=lambda a: (priority_order.get(a.priority, 4), -self.score(a)),
        )
        return sorted_actions[:limit]
