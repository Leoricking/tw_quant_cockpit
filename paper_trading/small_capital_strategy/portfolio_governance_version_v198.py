"""
paper_trading/small_capital_strategy/portfolio_governance_version_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Version Registry
[!] Paper Only. Research Only. Simulation Only. Validation Only.
[!] Portfolio Governance Only. Risk Overlay Only. Dashboard Only.
[!] No Real Orders. No Broker. No Margin. No Leverage.
[!] Not Investment Advice.
"""
VERSION = "1.9.8"
RELEASE_NAME = "Paper Portfolio Governance & Risk Overlay Lab"
SCHEMA_VERSION = "198"

PORTFOLIO_EXPOSURE_DIMENSIONS = [
    "symbol_exposure",
    "strategy_exposure",
    "theme_exposure",
    "industry_exposure",
    "sector_exposure",
    "market_cap_exposure",
    "direction_exposure",
    "ai_supply_chain_exposure",
    "semiconductor_exposure",
    "pcb_exposure",
    "cooling_exposure",
    "power_exposure",
    "asic_exposure",
    "server_supply_chain_exposure",
    "taiwan_index_beta",
    "tsmc_sensitivity",
    "etf_overlap",
    "foreign_futures_risk",
    "liquidity_risk",
    "drawdown_risk",
]

RISK_GRADES = ["LOW", "MODERATE", "ELEVATED", "HIGH", "CRITICAL", "INVALID"]

RISK_RECOMMENDATIONS = [
    "KEEP_PORTFOLIO",
    "REDUCE_POSITION_SIZE",
    "REDUCE_THEME_EXPOSURE",
    "REDUCE_INDUSTRY_EXPOSURE",
    "KEEP_CASH_BUFFER",
    "BLOCK_NEW_CANDIDATE",
    "REQUIRE_MORE_EVIDENCE",
    "REQUIRE_HUMAN_REVIEW",
    "KEEP_SHADOW_ONLY",
    "SUSPEND_PORTFOLIO_EXPANSION",
    "RISK_OFF_MODE",
    "NO_CHANGE",
]

RISK_LIMIT_KEYS = [
    "max_single_symbol_weight",
    "max_single_theme_weight",
    "max_single_industry_weight",
    "max_single_strategy_weight",
    "max_ai_supply_chain_weight",
    "max_semiconductor_weight",
    "max_correlation_cluster_weight",
    "max_high_risk_positions",
    "max_open_candidates",
    "min_cash_buffer",
    "max_drawdown_budget",
    "max_market_beta",
    "max_tsmc_sensitivity",
    "max_etf_overlap",
]

DASHBOARD_PANELS = [
    "portfolio_snapshot",
    "exposure_summary",
    "theme_risk",
    "industry_risk",
    "strategy_risk",
    "concentration_risk",
    "correlation_risk",
    "risk_limits",
    "risk_score",
    "risk_grade",
    "recommendations",
    "audit_trail",
]

HARD_BLOCK_CONDITIONS = [
    "real_order_requested",
    "broker_requested",
    "margin_or_leverage_requested",
    "production_db_write_attempted",
    "production_strategy_mutation_attempted",
    "automatic_rollback_attempted",
    "live_strategy_activation_attempted",
    "missing_paper_only_flags",
    "missing_no_broker_flags",
    "missing_not_investment_advice_flags",
    "missing_portfolio_snapshot",
    "missing_position_list",
    "missing_exposure_summary",
    "missing_risk_limits",
    "malformed_portfolio_input",
    "unsafe_export_path",
    "forbidden_action_words",
    "overlay_tries_to_execute_decision",
    "overlay_tries_to_mutate_strategy",
    "overlay_tries_to_rebalance_real_portfolio",
]

FORBIDDEN_OUTPUT_WORDS = [
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
    "REBALANCE_REAL_PORTFOLIO",
]

_PAPER_HEADER = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "portfolio_governance_only": True,
    "risk_overlay_only": True,
    "dashboard_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_db_writes": True,
    "no_automatic_production_strategy_mutation": True,
    "no_automatic_rollback": True,
    "no_live_strategy_activation": True,
    "not_investment_advice": True,
    "analytics_executes_decision": False,
    "dashboard_mutates_strategy": False,
    "overlay_places_real_order": False,
    "report_triggers_rebalance": False,
}


def get_version_info() -> dict:
    return {
        "version": VERSION,
        "release_name": RELEASE_NAME,
        "schema_version": SCHEMA_VERSION,
        "exposure_dimensions": len(PORTFOLIO_EXPOSURE_DIMENSIONS),
        "risk_grades": len(RISK_GRADES),
        "risk_recommendations": len(RISK_RECOMMENDATIONS),
        "risk_limit_keys": len(RISK_LIMIT_KEYS),
        "dashboard_panels": len(DASHBOARD_PANELS),
        "hard_block_conditions": len(HARD_BLOCK_CONDITIONS),
        "forbidden_output_words": len(FORBIDDEN_OUTPUT_WORDS),
        **_PAPER_HEADER,
    }


def verify_version() -> bool:
    assert VERSION == "1.9.8"
    assert SCHEMA_VERSION == "198"
    assert len(PORTFOLIO_EXPOSURE_DIMENSIONS) >= 20
    assert len(RISK_GRADES) >= 6
    assert len(RISK_RECOMMENDATIONS) >= 12
    assert len(RISK_LIMIT_KEYS) >= 14
    assert len(HARD_BLOCK_CONDITIONS) >= 17
    assert len(FORBIDDEN_OUTPUT_WORDS) >= 10
    return True


def get_exposure_dimensions() -> list:
    return list(PORTFOLIO_EXPOSURE_DIMENSIONS)


def get_risk_grades() -> list:
    return list(RISK_GRADES)


def get_risk_recommendations() -> list:
    return list(RISK_RECOMMENDATIONS)


def get_risk_limit_keys() -> list:
    return list(RISK_LIMIT_KEYS)


def get_dashboard_panels() -> list:
    return list(DASHBOARD_PANELS)


def get_hard_block_conditions() -> list:
    return list(HARD_BLOCK_CONDITIONS)


def get_forbidden_output_words() -> list:
    return list(FORBIDDEN_OUTPUT_WORDS)


assert verify_version()
