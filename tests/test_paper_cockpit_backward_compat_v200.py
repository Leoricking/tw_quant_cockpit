"""
tests/test_paper_cockpit_backward_compat_v200.py
v2.0.0 Paper Cockpit — Backward Compatibility Tests (v1.7.0~v1.9.10)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from gui.small_capital_strategy_panel import PANEL_VERSION, PANEL_TITLE, get_tab_names


def test_panel_version_is_200():
    assert PANEL_VERSION == "2.0.0"

def test_panel_title_contains_version():
    assert "2.0.0" in PANEL_TITLE or "Cockpit" in PANEL_TITLE or "Console" in PANEL_TITLE

# v1.7.0 core tabs still present
def test_v170_tab_overview_present():
    assert "overview" in get_tab_names()

def test_v170_tab_safety_present():
    assert "safety" in get_tab_names()

def test_v170_tab_capital_profile_present():
    assert "capital_profile" in get_tab_names()

def test_v170_tab_market_regime_present():
    assert "market_regime" in get_tab_names()

def test_v170_tab_watchlist_present():
    assert "watchlist" in get_tab_names()

def test_v170_tab_position_sizing_present():
    assert "position_sizing" in get_tab_names()

# v1.7.1 watchlist tabs
def test_v171_watchlist_overview_present():
    assert "watchlist_overview" in get_tab_names()

def test_v171_watchlist_ranking_present():
    assert "watchlist_ranking" in get_tab_names()

# v1.7.2 ABC tabs
def test_v172_abc_execution_overview_present():
    assert "abc_execution_overview" in get_tab_names()

def test_v172_abc_a_10ma_pullback_present():
    assert "abc_a_10ma_pullback" in get_tab_names()

# v1.7.3 regime tabs
def test_v173_regime_overview_present():
    assert "regime_overview" in get_tab_names()

# v1.7.5 trade journal tabs
def test_v175_trade_journal_overview_present():
    assert "trade_journal_overview" in get_tab_names()

# v1.7.6 mistake taxonomy tabs
def test_v176_mistake_taxonomy_present():
    assert "mistake_review_overview" in get_tab_names()

# v1.7.7 theme rotation tabs
def test_v177_theme_rotation_present():
    assert "theme_rotation" in get_tab_names()

# v1.7.8 integrated strategy tabs
def test_v178_integrated_strategy_present():
    assert "integrated_strategy" in get_tab_names()

# v1.7.9 stable rollup tabs
def test_v179_stable_rollup_present():
    assert "stable_rollup" in get_tab_names()

# v1.8.0 paper sim tabs
def test_v180_paper_sim_present():
    assert "paper_sim_lab" in get_tab_names()

# v1.8.6 decision cockpit tabs
def test_v186_daily_decision_cockpit_present():
    assert "daily_decision_cockpit" in get_tab_names()

# v1.8.7 decision report tabs
def test_v187_decision_report_present():
    assert "decision_report" in get_tab_names()

# v1.8.8 decision workflow tabs
def test_v188_decision_workflow_present():
    assert "decision_workflow" in get_tab_names()

# v1.8.9 decision journal tabs
def test_v189_decision_journal_present():
    assert "decision_journal" in get_tab_names()

# v1.9.0 performance review tabs
def test_v190_performance_review_present():
    assert "performance_review" in get_tab_names()

# v1.9.1 strategy tuning tabs
def test_v191_strategy_rule_tuning_present():
    assert "strategy_rule_tuning" in get_tab_names()

# v1.9.2 sandbox tabs
def test_v192_strategy_sandbox_present():
    assert "strategy_sandbox" in get_tab_names()

# v1.9.3 promotion tabs
def test_v193_strategy_promotion_present():
    assert "strategy_promotion" in get_tab_names()

# v1.9.4 monitoring tabs
def test_v194_strategy_monitoring_present():
    assert "strategy_monitoring" in get_tab_names()

def test_v194_drift_detection_present():
    assert "drift_detection" in get_tab_names()

# v1.9.5 review alert tabs
def test_v195_review_alerts_present():
    assert "review_alerts" in get_tab_names()

def test_v195_human_approval_present():
    assert "human_approval" in get_tab_names()

# v1.9.6 decision registry tabs
def test_v196_decision_registry_present():
    assert "decision_registry" in get_tab_names()

def test_v196_governance_review_present():
    assert "governance_review" in get_tab_names()

# v1.9.7 governance dashboard tabs
def test_v197_governance_dashboard_present():
    assert "governance_dashboard" in get_tab_names()

def test_v197_decision_quality_present():
    assert "decision_quality" in get_tab_names()

# v1.9.8 portfolio governance tabs
def test_v198_portfolio_governance_present():
    assert "portfolio_governance" in get_tab_names()

def test_v198_risk_overlay_present():
    assert "risk_overlay" in get_tab_names()

def test_v198_exposure_dashboard_present():
    assert "exposure_dashboard" in get_tab_names()

# v1.9.9 risk report tabs
def test_v199_portfolio_risk_report_present():
    assert "portfolio_risk_report" in get_tab_names()

def test_v199_position_sizing_policy_present():
    assert "position_sizing_policy" in get_tab_names()

def test_v199_risk_budget_dashboard_present():
    assert "risk_budget_dashboard" in get_tab_names()

# v1.9.10 governance stack tabs
def test_v1910_governance_stack_audit_present():
    assert "governance_stack_audit" in get_tab_names()

def test_v1910_release_audit_present():
    assert "release_audit" in get_tab_names()

def test_v1910_compatibility_summary_present():
    assert "compatibility_summary" in get_tab_names()

# v2.0.0 cockpit tabs
def test_v200_paper_cockpit_present():
    assert "paper_cockpit" in get_tab_names()

def test_v200_strategy_decision_console_present():
    assert "strategy_decision_console" in get_tab_names()

def test_v200_decision_ticket_present():
    assert "decision_ticket" in get_tab_names()

# v1.9.9 modules still importable
def test_v199_portfolio_risk_report_version_importable():
    from paper_trading.small_capital_strategy.portfolio_risk_report_version_v199 import VERSION
    assert VERSION == "1.9.9"

def test_v199_portfolio_risk_report_models_importable():
    from paper_trading.small_capital_strategy.portfolio_risk_report_models_v199 import _ALL_MODEL_NAMES
    assert len(_ALL_MODEL_NAMES) == 25

# v1.9.4 still importable
def test_v194_strategy_monitoring_importable():
    from paper_trading.small_capital_strategy.strategy_monitoring_version_v194 import VERSION
    assert VERSION == "1.9.4"

# v1.9.10 still importable
def test_v1910_governance_stack_importable():
    from paper_trading.small_capital_strategy.governance_stack_audit_v1910 import VERSION
    assert VERSION == "1.9.10"

# v2.0.0 new tabs coexist with all old tabs
def test_all_v200_tabs_coexist_with_all_old_tabs():
    tabs = get_tab_names()
    assert "paper_cockpit" in tabs
    assert "governance_stack_audit" in tabs
    assert "portfolio_risk_report" in tabs
    assert "portfolio_governance" in tabs
    assert "governance_dashboard" in tabs
    assert "decision_registry" in tabs
    assert "strategy_monitoring" in tabs
    assert "performance_review" in tabs
    assert "daily_decision_cockpit" in tabs
    assert "paper_sim_lab" in tabs
    assert "overview" in tabs

# v2.0.0 module backward compat check
def test_v200_covered_versions_includes_v170():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import COVERED_VERSIONS
    assert "1.7.0" in COVERED_VERSIONS

def test_v200_covered_versions_includes_v1910():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import COVERED_VERSIONS
    assert "1.9.10" in COVERED_VERSIONS

def test_v200_covered_versions_all_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import COVERED_VERSIONS
    for v in ["1.7.0", "1.7.1", "1.7.2", "1.7.3", "1.7.5", "1.8.0", "1.9.0", "1.9.10"]:
        assert v in COVERED_VERSIONS, f"Version {v} missing from COVERED_VERSIONS"
