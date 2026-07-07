"""
paper_trading/small_capital_strategy/exit_plan_v170.py
Exit plan for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
Paper plan / research plan only. No auto order.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.enums_v170 import ExitPlanStatus
from paper_trading.small_capital_strategy.models_v170 import ExitPlan

# Short-term exit rules
SHORT_TERM_EXIT = {
    "reduce_trigger": "break 5MA",
    "full_exit_trigger": "break 10MA",
    "staged_take_profit": [
        {"stage": 1, "trigger": "gain 10%", "action": "take half"},
        {"stage": 2, "trigger": "long upper shadow with volume", "action": "reduce"},
        {"stage": 3, "trigger": "break 10MA", "action": "full exit"},
    ],
}

# Swing exit rules
SWING_EXIT = {
    "reduce_trigger": "break 10MA",
    "full_exit_trigger": "break 20MA",
    "staged_take_profit": [
        {"stage": 1, "trigger": "gain 25%", "action": "staged take profit"},
        {"stage": 2, "trigger": "gain 40%", "action": "staged take profit"},
        {"stage": 3, "trigger": "break prior swing low", "action": "stop"},
    ],
}

# Core exit rules
CORE_EXIT = {
    "reduce_trigger": "break 60MA",
    "full_exit_trigger": "fundamental deterioration",
    "staged_take_profit": [
        {"stage": 1, "trigger": "break 60MA", "action": "reduce"},
        {"stage": 2, "trigger": "market below long-term trend", "action": "lower exposure"},
        {"stage": 3, "trigger": "fundamental deterioration", "action": "exit"},
    ],
}


def build_exit_plan(symbol: str, holding_type: str) -> ExitPlan:
    """
    Build an ExitPlan based on holding type.
    holding_type: 'short_term', 'swing', or 'core'
    Paper plan only — no auto order.
    """
    if holding_type == "short_term":
        rules = SHORT_TERM_EXIT
    elif holding_type == "core":
        rules = CORE_EXIT
    else:
        rules = SWING_EXIT  # default to swing

    return ExitPlan(
        symbol=symbol,
        holding_type=holding_type,
        reduce_trigger=rules["reduce_trigger"],
        full_exit_trigger=rules["full_exit_trigger"],
        staged_take_profit=list(rules["staged_take_profit"]),
        status=ExitPlanStatus.ACTIVE,
    )


def get_exit_rules_summary(holding_type: str) -> Dict[str, Any]:
    """Return exit rules summary for a holding type."""
    if holding_type == "short_term":
        rules = SHORT_TERM_EXIT
    elif holding_type == "core":
        rules = CORE_EXIT
    else:
        rules = SWING_EXIT
    return {
        "holding_type": holding_type,
        **rules,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def validate_exit_plan(plan: ExitPlan) -> Dict[str, Any]:
    """Validate an ExitPlan. Returns {valid, issues}."""
    issues = []
    if not plan.symbol:
        issues.append("symbol must be non-empty")
    if not plan.reduce_trigger:
        issues.append("reduce_trigger must be non-empty")
    if not plan.full_exit_trigger:
        issues.append("full_exit_trigger must be non-empty")
    if not plan.paper_only:
        issues.append("paper_only must be True")
    if not plan.no_real_orders:
        issues.append("no_real_orders must be True")
    return {"valid": len(issues) == 0, "issues": issues}
