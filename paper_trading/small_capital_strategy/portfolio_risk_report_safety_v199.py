"""
paper_trading/small_capital_strategy/portfolio_risk_report_safety_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Safety Module
[!] Paper Only. Research Only. Position Sizing Policy Only. Portfolio Risk Report Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

SAFETY_FLAGS = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "portfolio_risk_report_only": True,
    "position_sizing_policy_only": True,
    "dashboard_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_writes": True,
    "no_automatic_rollback": True,
    "no_live_strategy_activation": True,
    "no_real_portfolio_rebalancing": True,
    "no_production_strategy_mutation": True,
    "not_investment_advice": True,
    "production_trading_blocked": True,
    "demo_only": True,
    "not_for_production": True,
    "sizing_executes_order": False,
    "sizing_mutates_strategy": False,
    "sizing_rebalances_real_portfolio": False,
    "dashboard_mutates_strategy": False,
    "dashboard_places_real_order": False,
    "export_triggers_real_order": False,
}

FORBIDDEN_ACTIONS = [
    "BUY",
    "SELL",
    "ORDER",
    "EXECUTE",
    "SUBMIT_ORDER",
    "AUTO_TRADE",
    "REAL_TRADE",
    "LIVE_TRADE",
    "BROKER_ORDER",
    "REBALANCE_REAL_PORTFOLIO",
    "REAL_ORDER",
    "BROKER_CONNECT",
    "LIVE_ACTIVATE",
    "PRODUCTION_WRITE",
    "AUTO_REBALANCE",
]

ALLOWED_ACTIONS = [
    "PAPER_ALLOW_NORMAL_SIZE",
    "PAPER_ALLOW_REDUCED_SIZE",
    "PAPER_TEST_POSITION_ONLY",
    "PAPER_BLOCK_NEW_ENTRY",
    "PAPER_KEEP_CASH",
    "PAPER_REQUIRE_HUMAN_REVIEW",
    "PAPER_RISK_OFF_MODE",
    "PAPER_REPORT",
    "PAPER_DASHBOARD",
    "PAPER_AUDIT",
    "PAPER_EXPORT",
    "PAPER_VALIDATE",
    "PAPER_SIMULATE",
    "PAPER_RESEARCH",
    "PAPER_NO_CHANGE",
    "PAPER_REDUCE_EXISTING_EXPOSURE",
    "PAPER_REQUIRE_TIGHTER_STOP",
    "PAPER_REQUIRE_MORE_EVIDENCE",
    "PAPER_TEST_POSITION",
    "PAPER_NORMAL_SIZE",
]

HARD_BLOCK_CONDITIONS = [
    "real_order_requested",
    "broker_requested",
    "margin_leverage_requested",
    "production_db_write_attempted",
    "production_strategy_mutation_attempted",
    "automatic_rollback_attempted",
    "live_strategy_activation_attempted",
    "real_portfolio_rebalancing_attempted",
    "missing_paper_only_flags",
    "missing_no_broker_flags",
    "missing_not_investment_advice_flags",
    "missing_capital_profile",
    "missing_risk_budget",
    "missing_stop_distance",
    "missing_entry_type",
    "missing_exposure_limits",
    "malformed_sizing_input",
    "unsafe_export_path",
    "forbidden_action_words",
    "sizing_tries_to_execute_order",
    "sizing_tries_to_mutate_strategy",
    "sizing_tries_to_rebalance_real_portfolio",
]


def run_safety_audit() -> dict:
    errors = []
    for flag, expected in SAFETY_FLAGS.items():
        if SAFETY_FLAGS.get(flag) != expected:
            errors.append(f"Safety flag mismatch: {flag}")
    for action in FORBIDDEN_ACTIONS:
        if action in ALLOWED_ACTIONS:
            errors.append(f"Forbidden action in allowed list: {action}")
    for action in ALLOWED_ACTIONS:
        if action in FORBIDDEN_ACTIONS:
            errors.append(f"Allowed action in forbidden list: {action}")
    return {
        "all_safe": len(errors) == 0,
        "errors": errors,
        "safety_flags_count": len(SAFETY_FLAGS),
        "forbidden_actions_count": len(FORBIDDEN_ACTIONS),
        "allowed_actions_count": len(ALLOWED_ACTIONS),
        "hard_block_conditions_count": len(HARD_BLOCK_CONDITIONS),
        "paper_only": True,
        "no_real_orders": True,
        "production_trading_blocked": True,
    }


def assert_safe(action: str) -> None:
    if action in FORBIDDEN_ACTIONS:
        raise ValueError(f"Forbidden action blocked: {action}. Use paper-only actions.")


def is_safe_export_path(path: str) -> bool:
    if not path:
        return False
    forbidden_paths = [
        "production", "prod", "live", "broker", "real_trade",
        "C:/Program Files", "C:/Windows",
    ]
    path_lower = path.lower()
    for fp in forbidden_paths:
        if fp.lower() in path_lower:
            return False
    return True
