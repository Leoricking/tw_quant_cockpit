"""
tests/test_portfolio_governance_version_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Version Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_governance_version_v198 import (
    VERSION, SCHEMA_VERSION, RELEASE_NAME,
    PORTFOLIO_EXPOSURE_DIMENSIONS, RISK_GRADES, RISK_RECOMMENDATIONS,
    RISK_LIMIT_KEYS, DASHBOARD_PANELS, HARD_BLOCK_CONDITIONS,
    FORBIDDEN_OUTPUT_WORDS, _PAPER_HEADER,
    get_version_info, verify_version, get_exposure_dimensions,
    get_risk_grades, get_risk_recommendations, get_risk_limit_keys,
    get_dashboard_panels, get_hard_block_conditions, get_forbidden_output_words,
)


class TestVersionConstants:
    def test_version_is_1_9_8(self):
        assert VERSION == "1.9.8"

    def test_schema_version_is_198(self):
        assert SCHEMA_VERSION == "198"

    def test_release_name_contains_portfolio_governance(self):
        assert "Portfolio Governance" in RELEASE_NAME

    def test_release_name_contains_risk_overlay(self):
        assert "Risk Overlay" in RELEASE_NAME

    def test_release_name_contains_lab(self):
        assert "Lab" in RELEASE_NAME

    def test_release_name_is_string(self):
        assert isinstance(RELEASE_NAME, str)

    def test_version_is_string(self):
        assert isinstance(VERSION, str)

    def test_schema_version_is_string(self):
        assert isinstance(SCHEMA_VERSION, str)


class TestExposureDimensions:
    def test_count_is_20(self):
        assert len(PORTFOLIO_EXPOSURE_DIMENSIONS) == 20

    def test_is_list(self):
        assert isinstance(PORTFOLIO_EXPOSURE_DIMENSIONS, list)

    def test_has_symbol_exposure(self):
        assert "symbol_exposure" in PORTFOLIO_EXPOSURE_DIMENSIONS

    def test_has_strategy_exposure(self):
        assert "strategy_exposure" in PORTFOLIO_EXPOSURE_DIMENSIONS

    def test_has_theme_exposure(self):
        assert "theme_exposure" in PORTFOLIO_EXPOSURE_DIMENSIONS

    def test_has_ai_supply_chain_exposure(self):
        assert "ai_supply_chain_exposure" in PORTFOLIO_EXPOSURE_DIMENSIONS

    def test_has_semiconductor_exposure(self):
        assert "semiconductor_exposure" in PORTFOLIO_EXPOSURE_DIMENSIONS

    def test_has_tsmc_sensitivity(self):
        assert "tsmc_sensitivity" in PORTFOLIO_EXPOSURE_DIMENSIONS

    def test_has_etf_overlap(self):
        assert "etf_overlap" in PORTFOLIO_EXPOSURE_DIMENSIONS

    def test_has_drawdown_risk(self):
        assert "drawdown_risk" in PORTFOLIO_EXPOSURE_DIMENSIONS

    def test_all_strings(self):
        assert all(isinstance(d, str) for d in PORTFOLIO_EXPOSURE_DIMENSIONS)


class TestRiskGrades:
    def test_count_is_6(self):
        assert len(RISK_GRADES) == 6

    def test_is_list(self):
        assert isinstance(RISK_GRADES, list)

    def test_has_LOW(self):
        assert "LOW" in RISK_GRADES

    def test_has_MODERATE(self):
        assert "MODERATE" in RISK_GRADES

    def test_has_ELEVATED(self):
        assert "ELEVATED" in RISK_GRADES

    def test_has_HIGH(self):
        assert "HIGH" in RISK_GRADES

    def test_has_CRITICAL(self):
        assert "CRITICAL" in RISK_GRADES

    def test_has_INVALID(self):
        assert "INVALID" in RISK_GRADES

    def test_all_strings(self):
        assert all(isinstance(g, str) for g in RISK_GRADES)


class TestRiskRecommendations:
    def test_count_is_12(self):
        assert len(RISK_RECOMMENDATIONS) == 12

    def test_is_list(self):
        assert isinstance(RISK_RECOMMENDATIONS, list)

    def test_has_NO_CHANGE(self):
        assert "NO_CHANGE" in RISK_RECOMMENDATIONS

    def test_has_RISK_OFF_MODE(self):
        assert "RISK_OFF_MODE" in RISK_RECOMMENDATIONS

    def test_has_REQUIRE_HUMAN_REVIEW(self):
        assert "REQUIRE_HUMAN_REVIEW" in RISK_RECOMMENDATIONS

    def test_has_KEEP_SHADOW_ONLY(self):
        assert "KEEP_SHADOW_ONLY" in RISK_RECOMMENDATIONS

    def test_has_BLOCK_NEW_CANDIDATE(self):
        assert "BLOCK_NEW_CANDIDATE" in RISK_RECOMMENDATIONS

    def test_has_REDUCE_POSITION_SIZE(self):
        assert "REDUCE_POSITION_SIZE" in RISK_RECOMMENDATIONS

    def test_all_strings(self):
        assert all(isinstance(r, str) for r in RISK_RECOMMENDATIONS)


class TestRiskLimitKeys:
    def test_count_is_14(self):
        assert len(RISK_LIMIT_KEYS) == 14

    def test_is_list(self):
        assert isinstance(RISK_LIMIT_KEYS, list)

    def test_has_max_single_symbol_weight(self):
        assert "max_single_symbol_weight" in RISK_LIMIT_KEYS

    def test_has_max_single_theme_weight(self):
        assert "max_single_theme_weight" in RISK_LIMIT_KEYS

    def test_has_max_ai_supply_chain_weight(self):
        assert "max_ai_supply_chain_weight" in RISK_LIMIT_KEYS

    def test_has_min_cash_buffer(self):
        assert "min_cash_buffer" in RISK_LIMIT_KEYS

    def test_has_max_drawdown_budget(self):
        assert "max_drawdown_budget" in RISK_LIMIT_KEYS

    def test_has_max_tsmc_sensitivity(self):
        assert "max_tsmc_sensitivity" in RISK_LIMIT_KEYS

    def test_all_strings(self):
        assert all(isinstance(k, str) for k in RISK_LIMIT_KEYS)


class TestDashboardPanels:
    def test_count_is_12(self):
        assert len(DASHBOARD_PANELS) == 12

    def test_has_portfolio_snapshot(self):
        assert "portfolio_snapshot" in DASHBOARD_PANELS

    def test_has_audit_trail(self):
        assert "audit_trail" in DASHBOARD_PANELS

    def test_has_risk_grade(self):
        assert "risk_grade" in DASHBOARD_PANELS

    def test_is_list(self):
        assert isinstance(DASHBOARD_PANELS, list)


class TestHardBlockConditions:
    def test_count_gte_17(self):
        assert len(HARD_BLOCK_CONDITIONS) >= 17

    def test_count_is_20(self):
        assert len(HARD_BLOCK_CONDITIONS) == 20

    def test_has_real_order_requested(self):
        assert "real_order_requested" in HARD_BLOCK_CONDITIONS

    def test_has_missing_paper_only_flags(self):
        assert "missing_paper_only_flags" in HARD_BLOCK_CONDITIONS

    def test_has_malformed_portfolio_input(self):
        assert "malformed_portfolio_input" in HARD_BLOCK_CONDITIONS

    def test_has_unsafe_export_path(self):
        assert "unsafe_export_path" in HARD_BLOCK_CONDITIONS

    def test_is_list(self):
        assert isinstance(HARD_BLOCK_CONDITIONS, list)


class TestForbiddenOutputWords:
    def test_count_gte_10(self):
        assert len(FORBIDDEN_OUTPUT_WORDS) >= 10

    def test_count_is_10(self):
        assert len(FORBIDDEN_OUTPUT_WORDS) == 10

    def test_has_BUY(self):
        assert "BUY" in FORBIDDEN_OUTPUT_WORDS

    def test_has_SELL(self):
        assert "SELL" in FORBIDDEN_OUTPUT_WORDS

    def test_has_ORDER(self):
        assert "ORDER" in FORBIDDEN_OUTPUT_WORDS

    def test_has_EXECUTE(self):
        assert "EXECUTE" in FORBIDDEN_OUTPUT_WORDS

    def test_has_BROKER_ORDER(self):
        assert "BROKER_ORDER" in FORBIDDEN_OUTPUT_WORDS

    def test_is_list(self):
        assert isinstance(FORBIDDEN_OUTPUT_WORDS, list)


class TestGetVersionInfo:
    def test_returns_dict(self):
        assert isinstance(get_version_info(), dict)

    def test_version_field(self):
        assert get_version_info()["version"] == "1.9.8"

    def test_schema_version_field(self):
        assert get_version_info()["schema_version"] == "198"

    def test_paper_only_True(self):
        assert get_version_info()["paper_only"] is True

    def test_no_real_orders_True(self):
        assert get_version_info()["no_real_orders"] is True

    def test_no_broker_True(self):
        assert get_version_info()["no_broker"] is True

    def test_not_investment_advice_True(self):
        assert get_version_info()["not_investment_advice"] is True

    def test_analytics_executes_decision_False(self):
        assert get_version_info()["analytics_executes_decision"] is False

    def test_dashboard_mutates_strategy_False(self):
        assert get_version_info()["dashboard_mutates_strategy"] is False

    def test_overlay_places_real_order_False(self):
        assert get_version_info()["overlay_places_real_order"] is False

    def test_report_triggers_rebalance_False(self):
        assert get_version_info()["report_triggers_rebalance"] is False

    def test_exposure_dimensions_count(self):
        assert get_version_info()["exposure_dimensions"] == 20

    def test_risk_grades_count(self):
        assert get_version_info()["risk_grades"] == 6


class TestVerifyVersion:
    def test_returns_True(self):
        assert verify_version() is True


class TestAccessors:
    def test_get_exposure_dimensions_returns_list(self):
        assert isinstance(get_exposure_dimensions(), list)

    def test_get_exposure_dimensions_count(self):
        assert len(get_exposure_dimensions()) == 20

    def test_get_risk_grades_returns_list(self):
        assert isinstance(get_risk_grades(), list)

    def test_get_risk_grades_count(self):
        assert len(get_risk_grades()) == 6

    def test_get_risk_recommendations_returns_list(self):
        assert isinstance(get_risk_recommendations(), list)

    def test_get_risk_recommendations_count(self):
        assert len(get_risk_recommendations()) == 12

    def test_get_risk_limit_keys_returns_list(self):
        assert isinstance(get_risk_limit_keys(), list)

    def test_get_risk_limit_keys_count(self):
        assert len(get_risk_limit_keys()) == 14

    def test_get_dashboard_panels_returns_list(self):
        assert isinstance(get_dashboard_panels(), list)

    def test_get_hard_block_conditions_returns_list(self):
        assert isinstance(get_hard_block_conditions(), list)

    def test_get_forbidden_output_words_returns_list(self):
        assert isinstance(get_forbidden_output_words(), list)


class TestPaperHeader:
    def test_paper_only_True(self):
        assert _PAPER_HEADER["paper_only"] is True

    def test_no_real_orders_True(self):
        assert _PAPER_HEADER["no_real_orders"] is True

    def test_no_broker_True(self):
        assert _PAPER_HEADER["no_broker"] is True

    def test_not_investment_advice_True(self):
        assert _PAPER_HEADER["not_investment_advice"] is True

    def test_analytics_executes_decision_False(self):
        assert _PAPER_HEADER["analytics_executes_decision"] is False

    def test_dashboard_mutates_strategy_False(self):
        assert _PAPER_HEADER["dashboard_mutates_strategy"] is False

    def test_overlay_places_real_order_False(self):
        assert _PAPER_HEADER["overlay_places_real_order"] is False

    def test_report_triggers_rebalance_False(self):
        assert _PAPER_HEADER["report_triggers_rebalance"] is False
