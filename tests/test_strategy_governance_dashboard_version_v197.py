"""
tests/test_strategy_governance_dashboard_version_v197.py
Tests for strategy_governance_dashboard_version_v197 — Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7.
[!] Research Only. Paper Only. Governance Analytics Only. Dashboard Only.
[!] No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_governance_dashboard_version_v197 import (
    VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION, BASE_RELEASE,
    INCLUDED_RELEASES, DECISION_QUALITY_METRICS, DECISION_QUALITY_GRADES,
    ANALYTICS_WINDOWS, DASHBOARD_PANELS, HARD_BLOCK_CONDITIONS,
    FORBIDDEN_DASHBOARD_ACTIONS, ALLOWED_DASHBOARD_ACTIONS,
    MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH_CHECKS,
    verify_version, is_known_release, check_minimum_version,
    get_version_info, get_decision_quality_metrics, get_decision_quality_grades,
    get_analytics_windows, get_dashboard_panels, get_hard_block_conditions,
    get_forbidden_dashboard_actions, get_allowed_dashboard_actions,
)


# ── version constants ──────────────────────────────────────────────────────────
def test_version_is_197(): assert VERSION == "1.9.7"
def test_release_name_correct(): assert RELEASE_NAME == "Paper Strategy Governance Dashboard & Decision Quality Analytics Lab"
def test_schema_version_197(): assert SCHEMA_VERSION == "197"
def test_policy_version_contains_197(): assert "1.9.7" in POLICY_VERSION
def test_base_release_references_196(): assert "1.9.6" in BASE_RELEASE
def test_verify_version_true(): assert verify_version() is True
def test_min_scenarios_75(): assert MIN_SCENARIOS == 75
def test_min_fixtures_75(): assert MIN_FIXTURES == 75
def test_min_cli_16(): assert MIN_CLI >= 16
def test_min_health_checks_60(): assert MIN_HEALTH_CHECKS >= 60

# ── included releases ─────────────────────────────────────────────────────────
def test_included_releases_is_list(): assert isinstance(INCLUDED_RELEASES, list)
def test_included_releases_count_27(): assert len(INCLUDED_RELEASES) == 27
def test_included_releases_has_v197(): assert any("1.9.7" in r for r in INCLUDED_RELEASES)
def test_included_releases_has_v196(): assert any("1.9.6" in r for r in INCLUDED_RELEASES)
def test_included_releases_has_v190(): assert any("1.9.0" in r for r in INCLUDED_RELEASES)
def test_included_releases_has_v170(): assert any("1.7.0" in r for r in INCLUDED_RELEASES)
def test_is_known_release_v197(): assert is_known_release("Paper Strategy Governance Dashboard & Decision Quality Analytics Lab v1.9.7")
def test_is_known_release_v196(): assert is_known_release("Paper Strategy Decision Registry & Governance Lab v1.9.6")
def test_is_known_release_unknown_false(): assert is_known_release("Unknown Lab v9.9.9") is False
def test_check_minimum_version_196(): assert check_minimum_version("1.9.6") is True
def test_check_minimum_version_170(): assert check_minimum_version("1.7.0") is True

# ── quality metrics ────────────────────────────────────────────────────────────
def test_quality_metrics_count_12(): assert len(get_decision_quality_metrics()) == 12
def test_quality_metrics_has_evidence_coverage(): assert "evidence_coverage_score" in get_decision_quality_metrics()
def test_quality_metrics_has_rationale(): assert "rationale_completeness_score" in get_decision_quality_metrics()
def test_quality_metrics_has_registry_integrity(): assert "registry_integrity_score" in get_decision_quality_metrics()
def test_quality_metrics_has_paper_only_safety(): assert "paper_only_safety_score" in get_decision_quality_metrics()
def test_quality_metrics_returns_list(): assert isinstance(get_decision_quality_metrics(), list)

# ── quality grades ────────────────────────────────────────────────────────────
def test_quality_grades_count_5(): assert len(get_decision_quality_grades()) == 5
def test_quality_grades_has_excellent(): assert "EXCELLENT" in get_decision_quality_grades()
def test_quality_grades_has_good(): assert "GOOD" in get_decision_quality_grades()
def test_quality_grades_has_watch(): assert "WATCH" in get_decision_quality_grades()
def test_quality_grades_has_weak(): assert "WEAK" in get_decision_quality_grades()
def test_quality_grades_has_invalid(): assert "INVALID" in get_decision_quality_grades()

# ── analytics windows ─────────────────────────────────────────────────────────
def test_analytics_windows_count_5(): assert len(get_analytics_windows()) == 5
def test_analytics_windows_has_daily(): assert "DAILY" in get_analytics_windows()
def test_analytics_windows_has_full_history(): assert "FULL_HISTORY" in get_analytics_windows()
def test_analytics_windows_has_weekly(): assert "WEEKLY" in get_analytics_windows()
def test_analytics_windows_has_monthly(): assert "MONTHLY" in get_analytics_windows()
def test_analytics_windows_has_quarterly(): assert "QUARTERLY" in get_analytics_windows()

# ── dashboard panels ──────────────────────────────────────────────────────────
def test_dashboard_panels_count_12(): assert len(get_dashboard_panels()) == 12
def test_dashboard_panels_has_quality_overview(): assert "quality_overview" in get_dashboard_panels()
def test_dashboard_panels_has_evidence_coverage(): assert "evidence_coverage" in get_dashboard_panels()
def test_dashboard_panels_has_governance_violations(): assert "governance_violations" in get_dashboard_panels()
def test_dashboard_panels_has_export_manifest(): assert "export_manifest" in get_dashboard_panels()
def test_dashboard_panels_has_safety_summary(): assert "safety_summary" in get_dashboard_panels()

# ── hard block conditions ─────────────────────────────────────────────────────
def test_hard_block_conditions_count_17(): assert len(get_hard_block_conditions()) == 17
def test_hard_block_has_real_order(): assert "real_order_requested" in get_hard_block_conditions()
def test_hard_block_has_analytics_execute(): assert "analytics_tries_to_execute_decision" in get_hard_block_conditions()
def test_hard_block_has_dashboard_mutate(): assert "dashboard_tries_to_mutate_strategy" in get_hard_block_conditions()
def test_hard_block_has_missing_registry_source(): assert "missing_registry_source" in get_hard_block_conditions()

# ── forbidden / allowed actions ───────────────────────────────────────────────
def test_forbidden_actions_count_9(): assert len(get_forbidden_dashboard_actions()) == 9
def test_forbidden_has_buy(): assert "BUY" in get_forbidden_dashboard_actions()
def test_forbidden_has_broker_order(): assert "BROKER_ORDER" in get_forbidden_dashboard_actions()
def test_allowed_actions_count_18(): assert len(get_allowed_dashboard_actions()) == 18
def test_allowed_has_version(): assert "GOVERNANCE_DASHBOARD_VERSION" in get_allowed_dashboard_actions()
def test_allowed_has_health(): assert "GOVERNANCE_DASHBOARD_HEALTH" in get_allowed_dashboard_actions()
def test_allowed_has_quality_analytics(): assert "QUALITY_ANALYTICS" in get_allowed_dashboard_actions()

# ── version info dict ─────────────────────────────────────────────────────────
def test_version_info_returns_dict(): assert isinstance(get_version_info(), dict)
def test_version_info_paper_only(): assert get_version_info()["paper_only"] is True
def test_version_info_governance_analytics_only(): assert get_version_info()["governance_analytics_only"] is True
def test_version_info_dashboard_only(): assert get_version_info()["dashboard_only"] is True
def test_version_info_no_real_orders(): assert get_version_info()["no_real_orders"] is True
def test_version_info_not_investment_advice(): assert get_version_info()["not_investment_advice"] is True
def test_version_info_production_trading_blocked(): assert get_version_info()["production_trading_blocked"] is True
def test_version_info_no_production_mutation(): assert get_version_info()["no_production_strategy_mutation"] is True
def test_version_info_no_automatic_rollback(): assert get_version_info()["no_automatic_rollback"] is True
def test_version_info_no_live_activation(): assert get_version_info()["no_live_strategy_activation"] is True
