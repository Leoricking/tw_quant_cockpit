"""
replay/challenge_rules.py — Challenge rule types v1.2.7

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class RuleType:
    REQUIRE_THESIS                  = "REQUIRE_THESIS"
    REQUIRE_RISK_PLAN               = "REQUIRE_RISK_PLAN"
    REQUIRE_STOP_PLAN               = "REQUIRE_STOP_PLAN"
    REQUIRE_INVALIDATION            = "REQUIRE_INVALIDATION"
    REQUIRE_CONFIRMATION            = "REQUIRE_CONFIRMATION"
    REQUIRE_CHECKLIST               = "REQUIRE_CHECKLIST"
    REQUIRE_HIGHER_TIMEFRAME_CONTEXT = "REQUIRE_HIGHER_TIMEFRAME_CONTEXT"
    REQUIRE_TRIGGER_TIMEFRAME       = "REQUIRE_TRIGGER_TIMEFRAME"
    REQUIRE_STRATEGY_CONFLICT_REVIEW = "REQUIRE_STRATEGY_CONFLICT_REVIEW"
    REQUIRE_POINT_IN_TIME_PASS      = "REQUIRE_POINT_IN_TIME_PASS"
    PROHIBIT_OUTCOME_REVEAL         = "PROHIBIT_OUTCOME_REVEAL"
    PROHIBIT_FUTURE_DATA            = "PROHIBIT_FUTURE_DATA"
    PROHIBIT_UNPLANNED_ADD          = "PROHIBIT_UNPLANNED_ADD"
    PROHIBIT_EXCESSIVE_ACTIONS      = "PROHIBIT_EXCESSIVE_ACTIONS"
    PROHIBIT_EMPTY_DECISION_REASON  = "PROHIBIT_EMPTY_DECISION_REASON"

    ALL = [
        REQUIRE_THESIS, REQUIRE_RISK_PLAN, REQUIRE_STOP_PLAN,
        REQUIRE_INVALIDATION, REQUIRE_CONFIRMATION, REQUIRE_CHECKLIST,
        REQUIRE_HIGHER_TIMEFRAME_CONTEXT, REQUIRE_TRIGGER_TIMEFRAME,
        REQUIRE_STRATEGY_CONFLICT_REVIEW, REQUIRE_POINT_IN_TIME_PASS,
        PROHIBIT_OUTCOME_REVEAL, PROHIBIT_FUTURE_DATA,
        PROHIBIT_UNPLANNED_ADD, PROHIBIT_EXCESSIVE_ACTIONS,
        PROHIBIT_EMPTY_DECISION_REASON,
    ]


def build_rule(rule_type: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Build a rule definition dict."""
    return {
        "rule_type": rule_type,
        "params": params or {},
        "required": True,
        "research_only": True,
        "no_real_orders": True,
    }


def check_rule(
    rule: Dict[str, Any],
    attempt_actions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Check if a rule is satisfied by the attempt actions."""
    rule_type = rule.get("rule_type", "")
    action_types = [a.get("action_type", "") for a in attempt_actions]
    passed = False
    reason = ""

    if rule_type == RuleType.REQUIRE_THESIS:
        passed = "WRITE_THESIS" in action_types
        reason = "Thesis written" if passed else "Thesis not written"
    elif rule_type == RuleType.REQUIRE_RISK_PLAN:
        passed = "WRITE_RISK_PLAN" in action_types
        reason = "Risk plan written" if passed else "Risk plan not written"
    elif rule_type == RuleType.REQUIRE_CHECKLIST:
        passed = "WRITE_CHECKLIST" in action_types
        reason = "Checklist completed" if passed else "Checklist not completed"
    elif rule_type == RuleType.PROHIBIT_FUTURE_DATA:
        passed = True  # firewall enforced at data layer
        reason = "Future Firewall active — no future data accessible"
    elif rule_type == RuleType.PROHIBIT_EMPTY_DECISION_REASON:
        decision_actions = [a for a in attempt_actions if a.get("action_type", "").startswith("DECIDE_")]
        if decision_actions:
            passed = all(a.get("payload", {}).get("reason", "") for a in decision_actions)
            reason = "All decisions have reasons" if passed else "Decision without reason found"
        else:
            passed = True
            reason = "No decision action yet"
    else:
        passed = True
        reason = f"Rule {rule_type}: not evaluated (informational)"

    return {
        "rule_type": rule_type,
        "passed": passed,
        "reason": reason,
        "research_only": True,
    }
