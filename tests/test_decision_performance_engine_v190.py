"""tests/test_decision_performance_engine_v190.py
Tests for decision performance engine v1.9.0.
[!] Research Only. Paper Only.
"""
import pytest
from paper_trading.small_capital_strategy.decision_performance_engine_v190 import (
    run_performance_review,
    build_strategy_summary,
    build_setup_summary,
    build_mistake_summary,
    build_r_multiple_summary,
    build_drawdown_summary,
    build_expectancy_summary,
    build_improvement_suggestion,
    build_dashboard,
    build_evidence_pack,
    build_audit_trail,
    build_export_manifest,
    get_engine_info,
    validate_setup_type,
    validate_improvement_suggestion,
    validate_quality_grade,
    validate_performance_dimension,
)


def test_run_performance_review_empty_entries_blocked():
    assert run_performance_review("r1", [])["blocked"] is True


def test_run_performance_review_empty_entries_paper_only():
    assert run_performance_review("r1", [])["paper_only"] is True


def test_run_performance_review_empty_entries_block_reason():
    assert run_performance_review("r1", [])["block_reason"] == "performance_review_without_journal_entries"


def test_run_performance_review_with_entries_not_blocked():
    assert run_performance_review("r2", ["e1"])["blocked"] is False


def test_run_performance_review_with_entries_paper_only():
    assert run_performance_review("r2", ["e1"])["paper_only"] is True


def test_run_performance_review_with_entries_performance_review_only():
    assert run_performance_review("r2", ["e1"])["performance_review_only"] is True


def test_run_performance_review_with_entries_no_real_orders():
    assert run_performance_review("r2", ["e1"])["no_real_orders"] is True


def test_build_strategy_summary_empty_paper_only():
    assert build_strategy_summary([])["paper_only"] is True


def test_build_strategy_summary_empty_performance_review_only():
    assert build_strategy_summary([])["performance_review_only"] is True


def test_build_strategy_summary_empty_no_real_orders():
    assert build_strategy_summary([])["no_real_orders"] is True


def test_build_strategy_summary_total_paper_decisions():
    assert build_strategy_summary([{"state": "PAPER_PLAN_READY"}, {"state": "NO_TRADE"}])["total_paper_decisions"] == 2


def test_build_setup_summary_paper_only():
    assert build_setup_summary("A_10MA_PULLBACK", [])["paper_only"] is True


def test_build_setup_summary_setup_type():
    assert build_setup_summary("A_10MA_PULLBACK", [])["setup_type"] == "A_10MA_PULLBACK"


def test_build_mistake_summary_empty_returns_list():
    assert isinstance(build_mistake_summary([]), list)


def test_build_mistake_summary_empty_is_empty():
    assert build_mistake_summary([]) == []


def test_build_r_multiple_summary_empty_total_trades():
    assert build_r_multiple_summary([])["total_trades"] == 0


def test_build_r_multiple_summary_empty_paper_only():
    assert build_r_multiple_summary([])["paper_only"] is True


def test_build_r_multiple_summary_empty_no_broker():
    assert build_r_multiple_summary([])["no_broker"] is True


def test_build_r_multiple_summary_with_trades_total():
    assert build_r_multiple_summary([1.5, 1.2, -1.0])["total_trades"] == 3


def test_build_r_multiple_summary_positive_r_healthy():
    assert build_r_multiple_summary([1.5, 1.2, -1.0])["r_multiple_healthy"] is True


def test_build_r_multiple_summary_negative_r_not_healthy():
    assert build_r_multiple_summary([-3.0, -2.0, -1.0])["r_multiple_healthy"] is False


def test_build_drawdown_summary_empty_paper_only():
    assert build_drawdown_summary([])["paper_only"] is True


def test_build_drawdown_summary_empty_production_trading_blocked():
    assert build_drawdown_summary([])["production_trading_blocked"] is True


def test_build_drawdown_summary_within_budget():
    assert build_drawdown_summary([1.0, -0.5, 0.8])["drawdown_within_budget"] is True


def test_build_drawdown_summary_paper_only_with_values():
    assert build_drawdown_summary([1.0, -0.5, 0.8])["paper_only"] is True


def test_build_expectancy_summary_positive():
    assert build_expectancy_summary(0.6, 1.5, 1.0)["expectancy_positive"] is True


def test_build_expectancy_summary_negative():
    assert build_expectancy_summary(0.3, 1.0, 2.0)["expectancy_positive"] is False


def test_build_expectancy_summary_paper_only():
    assert build_expectancy_summary(0.5, 1.5, 1.0)["paper_only"] is True


def test_build_expectancy_summary_strategy_improvement_only():
    assert build_expectancy_summary(0.5, 1.5, 1.0)["strategy_improvement_only"] is True


def test_build_improvement_suggestion_no_evidence_blocked():
    assert build_improvement_suggestion("s1", "TIGHTEN_RULE", "A_10MA_PULLBACK", "test", [])["blocked"] is True


def test_build_improvement_suggestion_no_evidence_block_reason():
    assert build_improvement_suggestion("s1", "TIGHTEN_RULE", "A_10MA_PULLBACK", "test", [])["block_reason"] == "improvement_suggestion_without_evidence"


def test_build_improvement_suggestion_with_evidence_not_blocked():
    assert build_improvement_suggestion("s2", "TIGHTEN_RULE", "A_10MA_PULLBACK", "test", ["e1"])["blocked"] is False


def test_build_improvement_suggestion_with_evidence_strategy_improvement_only():
    assert build_improvement_suggestion("s2", "TIGHTEN_RULE", "A_10MA_PULLBACK", "test", ["e1"])["strategy_improvement_only"] is True


def test_build_improvement_suggestion_no_change_paper_only():
    assert build_improvement_suggestion("s2", "NO_CHANGE", "A_10MA_PULLBACK", "test", ["e1"])["paper_only"] is True


def test_build_dashboard_empty_paper_only():
    assert build_dashboard("d1", "period")["paper_only"] is True


def test_build_dashboard_empty_no_leverage():
    assert build_dashboard("d1", "period")["no_leverage"] is True


def test_build_dashboard_empty_no_margin():
    assert build_dashboard("d1", "period")["no_margin"] is True


def test_build_evidence_pack_empty_paper_only():
    assert build_evidence_pack("p1", "r1")["paper_only"] is True


def test_build_evidence_pack_empty_validation_only():
    assert build_evidence_pack("p1", "r1")["validation_only"] is True


def test_build_audit_trail_empty_paper_only():
    assert build_audit_trail("t1", "r1")["paper_only"] is True


def test_build_audit_trail_empty_audit_only():
    assert build_audit_trail("t1", "r1")["audit_only"] is True


def test_build_export_manifest_default_safe_path():
    assert build_export_manifest("m1", "period")["safe_path"] is True


def test_build_export_manifest_unsafe_path_redirected():
    assert build_export_manifest("m2", "period", "production_db/")["export_path"] == "reports/"


def test_build_export_manifest_safe_path_reports():
    assert build_export_manifest("m1", "period", "reports/")["safe_path"] is True


def test_get_engine_info_paper_only():
    assert get_engine_info()["paper_only"] is True


def test_get_engine_info_performance_review_only():
    assert get_engine_info()["performance_review_only"] is True


def test_validate_setup_type_a_10ma_pullback():
    assert validate_setup_type("A_10MA_PULLBACK") is True


def test_validate_setup_type_b_base_breakout():
    assert validate_setup_type("B_BASE_BREAKOUT") is True


def test_validate_setup_type_real_trade_false():
    assert validate_setup_type("REAL_TRADE") is False


def test_validate_setup_type_unknown_setup():
    assert validate_setup_type("UNKNOWN_SETUP") is True


def test_validate_improvement_suggestion_keep_rule():
    assert validate_improvement_suggestion("KEEP_RULE") is True


def test_validate_improvement_suggestion_tighten_rule():
    assert validate_improvement_suggestion("TIGHTEN_RULE") is True


def test_validate_improvement_suggestion_buy_more_false():
    assert validate_improvement_suggestion("BUY_MORE") is False


def test_validate_quality_grade_excellent():
    assert validate_quality_grade("EXCELLENT") is True


def test_validate_quality_grade_good():
    assert validate_quality_grade("GOOD") is True


def test_validate_quality_grade_unknown_false():
    assert validate_quality_grade("UNKNOWN") is False


def test_validate_performance_dimension_win_rate():
    assert validate_performance_dimension("win_rate") is True


def test_validate_performance_dimension_expectancy_r():
    assert validate_performance_dimension("expectancy_r") is True


def test_validate_performance_dimension_fake_dim_false():
    assert validate_performance_dimension("fake_dim") is False


def test_run_performance_review_returns_dict():
    assert isinstance(run_performance_review("r3", ["e1"]), dict)


def test_build_strategy_summary_returns_dict():
    assert isinstance(build_strategy_summary([]), dict)


def test_build_r_multiple_summary_returns_dict():
    assert isinstance(build_r_multiple_summary([]), dict)


def test_build_dashboard_returns_dict():
    assert isinstance(build_dashboard("d1", "period"), dict)


def test_build_r_multiple_summary_two_trades_performance_review_only():
    assert build_r_multiple_summary([2.0, -1.0])["performance_review_only"] is True


def test_build_drawdown_summary_two_values_strategy_improvement_only():
    assert build_drawdown_summary([1.0, -0.5])["strategy_improvement_only"] is True


def test_build_strategy_summary_empty_strategy_improvement_only():
    assert build_strategy_summary([])["strategy_improvement_only"] is True


def test_build_setup_summary_b_base_breakout_performance_review_only():
    assert build_setup_summary("B_BASE_BREAKOUT", [])["performance_review_only"] is True


def test_get_engine_info_strategy_improvement_only():
    assert get_engine_info()["strategy_improvement_only"] is True


def test_build_export_manifest_paper_only():
    assert build_export_manifest("m3", "p2")["paper_only"] is True


def test_build_evidence_pack_with_data_performance_review_only():
    assert build_evidence_pack("p2", "r2", [{"test": 1}])["performance_review_only"] is True


def test_build_audit_trail_with_data_performance_review_only():
    assert build_audit_trail("t2", "r2", [{"test": 1}])["performance_review_only"] is True
