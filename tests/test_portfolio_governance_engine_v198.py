"""
tests/test_portfolio_governance_engine_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Engine Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_governance_engine_v198 import (
    validate_portfolio_input, validate_risk_grade, validate_risk_recommendation,
    validate_risk_limit_key, compute_risk_score, compute_risk_grade,
    evaluate_risk_limits, detect_concentration_risk, detect_correlation_risk,
    run_risk_overlay, generate_recommendations, build_exposure_summary,
    build_portfolio_dashboard, build_governance_report,
    build_audit_trail_entry, export_governance_pack,
    GRADE_THRESHOLDS,
)

_VALID_INPUT = {
    "paper_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "positions": [],
    "snapshot": {},
    "risk_limits": {},
}


class TestValidatePortfolioInput:
    def test_valid_input_not_blocked(self):
        assert validate_portfolio_input(_VALID_INPUT)["blocked"] is False

    def test_valid_input_valid_True(self):
        assert validate_portfolio_input(_VALID_INPUT)["valid"] is True

    def test_malformed_string_blocked(self):
        assert validate_portfolio_input("bad")["blocked"] is True

    def test_malformed_none_blocked(self):
        assert validate_portfolio_input(None)["blocked"] is True

    def test_malformed_list_blocked(self):
        assert validate_portfolio_input([])["blocked"] is True

    def test_missing_paper_only_blocked(self):
        inp = {"no_real_orders": True, "no_broker": True, "positions": [], "snapshot": {}, "risk_limits": {}}
        assert validate_portfolio_input(inp)["blocked"] is True

    def test_paper_only_False_blocked(self):
        inp = {**_VALID_INPUT, "paper_only": False}
        assert validate_portfolio_input(inp)["blocked"] is True

    def test_missing_no_broker_blocked(self):
        inp = {"paper_only": True, "no_real_orders": True, "positions": [], "snapshot": {}, "risk_limits": {}}
        assert validate_portfolio_input(inp)["blocked"] is True

    def test_missing_positions_blocked(self):
        inp = {"paper_only": True, "no_real_orders": True, "no_broker": True, "snapshot": {}, "risk_limits": {}}
        assert validate_portfolio_input(inp)["blocked"] is True

    def test_missing_snapshot_blocked(self):
        inp = {"paper_only": True, "no_real_orders": True, "no_broker": True, "positions": [], "risk_limits": {}}
        assert validate_portfolio_input(inp)["blocked"] is True

    def test_missing_risk_limits_blocked(self):
        inp = {"paper_only": True, "no_real_orders": True, "no_broker": True, "positions": [], "snapshot": {}}
        assert validate_portfolio_input(inp)["blocked"] is True

    def test_forbidden_word_BUY_blocked(self):
        inp = {**_VALID_INPUT, "note": "BUY"}
        assert validate_portfolio_input(inp)["blocked"] is True

    def test_forbidden_word_SELL_blocked(self):
        inp = {**_VALID_INPUT, "note": "SELL"}
        assert validate_portfolio_input(inp)["blocked"] is True

    def test_paper_only_True_in_result(self):
        r = validate_portfolio_input(_VALID_INPUT)
        assert r["paper_only"] is True

    def test_no_real_orders_True_in_result(self):
        r = validate_portfolio_input(_VALID_INPUT)
        assert r["no_real_orders"] is True


class TestValidateRiskGrade:
    def test_LOW_valid(self):
        assert validate_risk_grade("LOW")["valid"] is True

    def test_MODERATE_valid(self):
        assert validate_risk_grade("MODERATE")["valid"] is True

    def test_ELEVATED_valid(self):
        assert validate_risk_grade("ELEVATED")["valid"] is True

    def test_HIGH_valid(self):
        assert validate_risk_grade("HIGH")["valid"] is True

    def test_CRITICAL_valid(self):
        assert validate_risk_grade("CRITICAL")["valid"] is True

    def test_INVALID_valid(self):
        assert validate_risk_grade("INVALID")["valid"] is True

    def test_unknown_grade_invalid(self):
        assert validate_risk_grade("UNKNOWN")["valid"] is False

    def test_empty_string_invalid(self):
        assert validate_risk_grade("")["valid"] is False

    def test_lowercase_invalid(self):
        assert validate_risk_grade("low")["valid"] is False


class TestValidateRiskRecommendation:
    def test_NO_CHANGE_valid(self):
        assert validate_risk_recommendation("NO_CHANGE")["valid"] is True

    def test_RISK_OFF_MODE_valid(self):
        assert validate_risk_recommendation("RISK_OFF_MODE")["valid"] is True

    def test_REQUIRE_HUMAN_REVIEW_valid(self):
        assert validate_risk_recommendation("REQUIRE_HUMAN_REVIEW")["valid"] is True

    def test_KEEP_SHADOW_ONLY_valid(self):
        assert validate_risk_recommendation("KEEP_SHADOW_ONLY")["valid"] is True

    def test_unknown_rec_invalid(self):
        assert validate_risk_recommendation("DO_NOTHING")["valid"] is False


class TestValidateRiskLimitKey:
    def test_max_single_symbol_weight_valid(self):
        assert validate_risk_limit_key("max_single_symbol_weight")["valid"] is True

    def test_min_cash_buffer_valid(self):
        assert validate_risk_limit_key("min_cash_buffer")["valid"] is True

    def test_max_tsmc_sensitivity_valid(self):
        assert validate_risk_limit_key("max_tsmc_sensitivity")["valid"] is True

    def test_unknown_key_invalid(self):
        assert validate_risk_limit_key("unknown_key")["valid"] is False


class TestComputeRiskScore:
    def test_raw_0_returns_0(self):
        assert compute_risk_score({"raw_score": 0.0})["score"] == 0.0

    def test_raw_0_5_returns_0_5(self):
        assert compute_risk_score({"raw_score": 0.5})["score"] == 0.5

    def test_raw_1_0_returns_1_0(self):
        assert compute_risk_score({"raw_score": 1.0})["score"] == 1.0

    def test_raw_1_5_clamped_to_1_0(self):
        assert compute_risk_score({"raw_score": 1.5})["score"] == 1.0

    def test_raw_negative_clamped_to_0(self):
        assert compute_risk_score({"raw_score": -0.5})["score"] == 0.0

    def test_missing_raw_score_defaults_0(self):
        assert compute_risk_score({})["score"] == 0.0

    def test_malformed_blocked(self):
        assert compute_risk_score("bad")["blocked"] is True

    def test_not_blocked_for_valid(self):
        assert compute_risk_score({"raw_score": 0.3})["blocked"] is False


class TestComputeRiskGrade:
    def test_score_0_0_is_LOW(self):
        assert compute_risk_grade(0.0)["grade"] == "LOW"

    def test_score_0_1_is_LOW(self):
        assert compute_risk_grade(0.1)["grade"] == "LOW"

    def test_score_0_19_is_LOW(self):
        assert compute_risk_grade(0.19)["grade"] == "LOW"

    def test_score_0_3_is_MODERATE(self):
        assert compute_risk_grade(0.3)["grade"] == "MODERATE"

    def test_score_0_2_is_MODERATE(self):
        assert compute_risk_grade(0.2)["grade"] == "MODERATE"

    def test_score_0_5_is_ELEVATED(self):
        assert compute_risk_grade(0.5)["grade"] == "ELEVATED"

    def test_score_0_4_is_ELEVATED(self):
        assert compute_risk_grade(0.4)["grade"] == "ELEVATED"

    def test_score_0_7_is_HIGH(self):
        assert compute_risk_grade(0.7)["grade"] == "HIGH"

    def test_score_0_6_is_HIGH(self):
        assert compute_risk_grade(0.6)["grade"] == "HIGH"

    def test_score_0_9_is_CRITICAL(self):
        assert compute_risk_grade(0.9)["grade"] == "CRITICAL"

    def test_score_0_8_is_CRITICAL(self):
        assert compute_risk_grade(0.8)["grade"] == "CRITICAL"

    def test_score_0_95_is_CRITICAL(self):
        assert compute_risk_grade(0.95)["grade"] == "CRITICAL"

    def test_negative_score_is_INVALID(self):
        assert compute_risk_grade(-0.1)["grade"] == "INVALID"

    def test_score_gt_1_is_INVALID(self):
        assert compute_risk_grade(1.5)["grade"] == "INVALID"

    def test_paper_only_True_in_result(self):
        assert compute_risk_grade(0.5)["paper_only"] is True


class TestEvaluateRiskLimits:
    def test_returns_dict_for_valid(self):
        r = evaluate_risk_limits({}, {})
        assert isinstance(r, dict)

    def test_not_blocked_for_valid_input(self):
        assert evaluate_risk_limits({}, {})["blocked"] is False

    def test_blocked_for_malformed_portfolio(self):
        assert evaluate_risk_limits("bad", {})["blocked"] is True

    def test_blocked_for_malformed_limits(self):
        assert evaluate_risk_limits({}, "bad")["blocked"] is True

    def test_results_is_list(self):
        r = evaluate_risk_limits({}, {})
        assert isinstance(r["results"], list)

    def test_results_count_is_14(self):
        r = evaluate_risk_limits({}, {})
        assert len(r["results"]) == 14

    def test_breach_detected_when_current_exceeds_limit(self):
        portfolio = {"max_single_symbol_weight": 0.5}
        limits = {"max_single_symbol_weight": 0.2}
        r = evaluate_risk_limits(portfolio, limits)
        assert r["any_breach"] is True
        assert "max_single_symbol_weight" in r["breached"]


class TestDetectConcentrationRisk:
    def test_no_breach_when_all_below_max(self):
        weights = {"A": 0.1, "B": 0.15, "C": 0.2}
        r = detect_concentration_risk(weights, max_weight=0.3)
        assert r["any_breach"] is False

    def test_breach_when_one_exceeds_max(self):
        weights = {"A": 0.1, "B": 0.4}
        r = detect_concentration_risk(weights, max_weight=0.3)
        assert r["any_breach"] is True
        assert "B" in r["breaches"]

    def test_blocked_for_malformed(self):
        assert detect_concentration_risk("bad")["blocked"] is True

    def test_paper_only_True(self):
        assert detect_concentration_risk({})["paper_only"] is True


class TestDetectCorrelationRisk:
    def test_no_breach_low_cluster_weight(self):
        clusters = [{"id": "c1", "weight": 0.3}]
        r = detect_correlation_risk(clusters, max_cluster_weight=0.5)
        assert r["any_breach"] is False

    def test_breach_high_cluster_weight(self):
        clusters = [{"id": "c1", "weight": 0.6}]
        r = detect_correlation_risk(clusters, max_cluster_weight=0.5)
        assert r["any_breach"] is True

    def test_blocked_for_malformed(self):
        assert detect_correlation_risk("bad")["blocked"] is True

    def test_empty_clusters_no_breach(self):
        assert detect_correlation_risk([])["any_breach"] is False


class TestRunRiskOverlay:
    def test_blocked_for_malformed_portfolio(self):
        assert run_risk_overlay("cand", "bad")["blocked"] is True

    def test_blocked_missing_paper_only(self):
        assert run_risk_overlay("cand", {})["blocked"] is True

    def test_blocked_forbidden_word_BUY(self):
        r = run_risk_overlay("BUY_signal", {"paper_only": True})
        assert r["blocked"] is True

    def test_blocked_forbidden_word_EXECUTE(self):
        r = run_risk_overlay("EXECUTE_now", {"paper_only": True})
        assert r["blocked"] is True

    def test_overlay_passed_low_risk(self):
        r = run_risk_overlay("paper_cand_001", {"paper_only": True, "risk_score": 0.1})
        assert r["overlay_passed"] is True

    def test_overlay_not_passed_high_risk(self):
        r = run_risk_overlay("paper_cand_002", {"paper_only": True, "risk_score": 0.9})
        assert r["overlay_passed"] is False

    def test_blocked_rebalance_real_portfolio(self):
        r = run_risk_overlay("cand", {"paper_only": True, "overlay_tries_to_rebalance_real_portfolio": True})
        assert r["blocked"] is True

    def test_blocked_mutate_strategy(self):
        r = run_risk_overlay("cand", {"paper_only": True, "overlay_tries_to_mutate_strategy": True})
        assert r["blocked"] is True

    def test_paper_only_True_in_result(self):
        r = run_risk_overlay("cand", {"paper_only": True})
        assert r["paper_only"] is True


class TestGenerateRecommendations:
    def test_LOW_returns_NO_CHANGE(self):
        r = generate_recommendations("LOW", [])
        assert "NO_CHANGE" in r["recommendations"]

    def test_MODERATE_returns_REQUIRE_MORE_EVIDENCE(self):
        r = generate_recommendations("MODERATE", [])
        assert "REQUIRE_MORE_EVIDENCE" in r["recommendations"]

    def test_ELEVATED_returns_REDUCE_POSITION_SIZE(self):
        r = generate_recommendations("ELEVATED", [])
        assert "REDUCE_POSITION_SIZE" in r["recommendations"]

    def test_HIGH_returns_RISK_OFF_MODE(self):
        r = generate_recommendations("HIGH", [])
        assert "RISK_OFF_MODE" in r["recommendations"]

    def test_CRITICAL_returns_RISK_OFF_MODE(self):
        r = generate_recommendations("CRITICAL", [])
        assert "RISK_OFF_MODE" in r["recommendations"]

    def test_theme_breach_adds_REDUCE_THEME_EXPOSURE(self):
        r = generate_recommendations("LOW", ["max_single_theme_weight"])
        assert "REDUCE_THEME_EXPOSURE" in r["recommendations"]

    def test_industry_breach_adds_REDUCE_INDUSTRY_EXPOSURE(self):
        r = generate_recommendations("LOW", ["max_single_industry_weight"])
        assert "REDUCE_INDUSTRY_EXPOSURE" in r["recommendations"]

    def test_candidates_breach_adds_BLOCK_NEW_CANDIDATE(self):
        r = generate_recommendations("LOW", ["max_open_candidates"])
        assert "BLOCK_NEW_CANDIDATE" in r["recommendations"]

    def test_returns_dict(self):
        assert isinstance(generate_recommendations("LOW", []), dict)

    def test_count_in_result(self):
        r = generate_recommendations("LOW", [])
        assert "count" in r


class TestBuildExposureSummary:
    def test_empty_positions_returns_zeroes(self):
        r = build_exposure_summary([])
        assert r["symbol_count"] == 0
        assert r["theme_count"] == 0

    def test_blocked_for_malformed(self):
        assert build_exposure_summary("bad")["blocked"] is True

    def test_counts_unique_symbols(self):
        positions = [
            {"symbol": "A", "theme": "t1", "industry": "i1", "strategy_id": "s1"},
            {"symbol": "B", "theme": "t1", "industry": "i1", "strategy_id": "s1"},
        ]
        r = build_exposure_summary(positions)
        assert r["symbol_count"] == 2
        assert r["theme_count"] == 1

    def test_paper_only_True(self):
        assert build_exposure_summary([])["paper_only"] is True


class TestBuildPortfolioDashboard:
    def test_blocked_for_malformed_snapshot(self):
        assert build_portfolio_dashboard("bad", {}, "LOW", [])["blocked"] is True

    def test_panel_count_is_4(self):
        r = build_portfolio_dashboard({}, {}, "LOW", [])
        assert r["panel_count"] == 4

    def test_dashboard_mutates_strategy_False(self):
        r = build_portfolio_dashboard({}, {}, "LOW", [])
        assert r["dashboard_mutates_strategy"] is False

    def test_paper_only_True(self):
        r = build_portfolio_dashboard({}, {}, "LOW", [])
        assert r["paper_only"] is True


class TestBuildGovernanceReport:
    def test_blocked_for_malformed_dashboard(self):
        assert build_governance_report("bad", [])["blocked"] is True

    def test_section_count_5(self):
        r = build_governance_report({}, [])
        assert r["section_count"] == 5

    def test_report_triggers_rebalance_False(self):
        r = build_governance_report({}, [])
        assert r["report_triggers_rebalance"] is False

    def test_audit_entries_count(self):
        r = build_governance_report({}, [{"e": 1}, {"e": 2}])
        assert r["audit_entries"] == 2


class TestBuildAuditTrailEntry:
    def test_returns_dict(self):
        assert isinstance(build_audit_trail_entry("TEST", "detail"), dict)

    def test_event_type_present(self):
        r = build_audit_trail_entry("GOVERNANCE_RUN", "ran")
        assert r["event_type"] == "GOVERNANCE_RUN"

    def test_immutable_True(self):
        r = build_audit_trail_entry("TEST", "d")
        assert r["immutable"] is True

    def test_paper_only_True(self):
        r = build_audit_trail_entry("TEST", "d")
        assert r["paper_only"] is True


class TestExportGovernancePack:
    def test_safe_path_exported_True(self):
        r = export_governance_pack({}, "paper_export/test.json")
        assert r["exported"] is True

    def test_empty_path_uses_default(self):
        r = export_governance_pack({})
        assert "paper_export" in r["export_path"]

    def test_dotdot_path_blocked(self):
        assert export_governance_pack({}, "../bad/path")["blocked"] is True

    def test_production_path_blocked(self):
        assert export_governance_pack({}, "production/data.json")["blocked"] is True

    def test_live_path_blocked(self):
        assert export_governance_pack({}, "live/data.json")["blocked"] is True

    def test_paper_only_True(self):
        assert export_governance_pack({})["paper_only"] is True
