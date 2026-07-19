"""
paper_trading/small_capital_strategy/portfolio_risk_report_version_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Version Module
[!] Paper Only. Research Only. Position Sizing Policy Only. Portfolio Risk Report Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.9.9"
SCHEMA_VERSION = "199"
RELEASE_NAME = "Paper Portfolio Risk Report & Position Sizing Policy Lab"
BASELINE_TESTS = 31044
MIN_NEW_TESTS = 400

ENTRY_TYPES = [
    "A_PULLBACK_10MA",
    "B_BREAKOUT_BASE",
    "C_RECLAIM_20MA",
    "TEST_POSITION",
    "ADD_POSITION",
    "REDUCE_POSITION",
    "NO_ENTRY",
]

POSITION_SIZING_POLICIES = [
    "fixed_fractional_risk",
    "stop_distance_based_sizing",
    "max_single_trade_loss",
    "max_symbol_weight",
    "max_theme_weight",
    "max_industry_weight",
    "max_strategy_weight",
    "min_cash_buffer",
    "risk_off_position_cut",
    "high_correlation_sizing_cut",
    "no_entry_when_risk_exceeded",
]

RISK_GRADES = ["LOW", "MODERATE", "ELEVATED", "HIGH", "CRITICAL", "INVALID"]

RECOMMENDATIONS = [
    "ALLOW_NORMAL_SIZE",
    "ALLOW_REDUCED_SIZE",
    "TEST_POSITION_ONLY",
    "KEEP_CASH",
    "BLOCK_NEW_ENTRY",
    "REDUCE_EXISTING_EXPOSURE",
    "REQUIRE_TIGHTER_STOP",
    "REQUIRE_MORE_EVIDENCE",
    "RISK_OFF_MODE",
    "NO_CHANGE",
]

PAPER_ACTIONS = [
    "PAPER_ALLOW_NORMAL_SIZE",
    "PAPER_ALLOW_REDUCED_SIZE",
    "PAPER_TEST_POSITION_ONLY",
    "PAPER_BLOCK_NEW_ENTRY",
    "PAPER_KEEP_CASH",
    "PAPER_REQUIRE_HUMAN_REVIEW",
    "PAPER_RISK_OFF_MODE",
]

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

ENTRY_SIZE_MULTIPLIERS = {
    "A_PULLBACK_10MA": 1.0,
    "B_BREAKOUT_BASE": 0.7,
    "C_RECLAIM_20MA": 0.5,
    "TEST_POSITION": 0.3,
    "ADD_POSITION": 0.5,
    "REDUCE_POSITION": 0.0,
    "NO_ENTRY": 0.0,
}

CLI_COMMANDS = [
    "portfolio-risk-report-version",
    "portfolio-risk-report-run",
    "portfolio-risk-report-capital-profile",
    "portfolio-risk-report-risk-budget",
    "portfolio-risk-report-position-size",
    "portfolio-risk-report-entry-rule",
    "portfolio-risk-report-stop-distance",
    "portfolio-risk-report-cash-buffer",
    "portfolio-risk-report-exposure-limits",
    "portfolio-risk-report-no-entry",
    "portfolio-risk-report-risk-off",
    "portfolio-risk-report-dashboard",
    "portfolio-risk-report-export",
    "portfolio-risk-report-health",
    "portfolio-risk-report-gate",
    "portfolio-risk-report-scenarios",
    "portfolio-risk-report-fixtures",
    "portfolio-risk-report-safety-audit",
]

GUI_TABS = [
    "portfolio_risk_report",
    "position_sizing_policy",
    "risk_budget_dashboard",
]

CAPITAL_PROFILE_300K = {
    "capital_base": 300_000,
    "normal_single_trade_risk_pct_min": 0.008,
    "normal_single_trade_risk_pct_max": 0.015,
    "normal_single_trade_loss_min": 2_400,
    "normal_single_trade_loss_max": 4_500,
    "aggressive_single_trade_risk_pct_max": 0.02,
    "risk_off_single_trade_risk_pct_max": 0.005,
    "min_cash_buffer_pct": 0.05,
    "weak_market_cash_buffer_pct": 0.50,
    "max_single_symbol_weight": 0.20,
    "max_single_theme_weight": 0.35,
    "max_single_industry_weight": 0.40,
    "max_high_correlation_cluster_weight": 0.45,
}


def get_version_info() -> dict:
    return {
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "release_name": RELEASE_NAME,
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
        "entry_types": list(ENTRY_TYPES),
        "position_sizing_policies": list(POSITION_SIZING_POLICIES),
        "risk_grades": list(RISK_GRADES),
        "recommendations": list(RECOMMENDATIONS),
        "paper_actions": list(PAPER_ACTIONS),
        "cli_commands": list(CLI_COMMANDS),
        "gui_tabs": list(GUI_TABS),
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "validation_only": True,
        "portfolio_risk_report_only": True,
        "position_sizing_policy_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "no_margin": True,
        "no_leverage": True,
        "no_production_db_writes": True,
        "no_automatic_rollback": True,
        "no_live_strategy_activation": True,
        "no_real_portfolio_rebalancing": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
    }


def verify_version() -> bool:
    info = get_version_info()
    assert info["version"] == VERSION
    assert info["schema_version"] == SCHEMA_VERSION
    assert len(ENTRY_TYPES) == 7
    assert len(POSITION_SIZING_POLICIES) == 11
    assert len(RISK_GRADES) == 6
    assert len(RECOMMENDATIONS) == 10
    assert len(PAPER_ACTIONS) == 7
    assert len(CLI_COMMANDS) == 18
    assert len(GUI_TABS) == 3
    assert len(HARD_BLOCK_CONDITIONS) == 22
    assert len(FORBIDDEN_ACTIONS) == 10
    assert info["paper_only"] is True
    assert info["no_real_orders"] is True
    assert info["production_trading_blocked"] is True
    return True


assert verify_version(), "v1.9.9 version verification failed"
