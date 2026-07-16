"""tests/test_decision_performance_version_v190.py
Tests for decision performance version module v1.9.0.
[!] Research Only. Paper Only.
"""
import pytest
from paper_trading.small_capital_strategy.decision_performance_version_v190 import (
    VERSION,
    RELEASE_NAME,
    SCHEMA_VERSION,
    verify_version,
    is_known_release,
    get_version_info,
    get_setup_types,
    get_improvement_suggestions,
    get_quality_grades,
    get_performance_dimensions,
    get_forbidden_performance_actions,
    get_allowed_performance_actions,
    get_hard_block_conditions,
)


def test_version_value():
    assert VERSION == "1.9.0"


def test_release_name_value():
    assert RELEASE_NAME == "Paper Trading Performance Review & Strategy Improvement Lab"


def test_schema_version_value():
    assert SCHEMA_VERSION == "190"


def test_verify_version_returns_true():
    assert verify_version() is True


def test_get_setup_types_length():
    assert len(get_setup_types()) == 11


def test_setup_types_contains_a_10ma_pullback():
    assert "A_10MA_PULLBACK" in get_setup_types()


def test_setup_types_contains_b_base_breakout():
    assert "B_BASE_BREAKOUT" in get_setup_types()


def test_setup_types_contains_c_20ma_reclaim():
    assert "C_20MA_RECLAIM" in get_setup_types()


def test_setup_types_contains_second_wave():
    assert "SECOND_WAVE" in get_setup_types()


def test_setup_types_contains_unknown_setup():
    assert "UNKNOWN_SETUP" in get_setup_types()


def test_get_improvement_suggestions_length():
    assert len(get_improvement_suggestions()) == 13


def test_improvement_suggestions_contains_keep_rule():
    assert "KEEP_RULE" in get_improvement_suggestions()


def test_improvement_suggestions_contains_tighten_rule():
    assert "TIGHTEN_RULE" in get_improvement_suggestions()


def test_improvement_suggestions_contains_block_setup():
    assert "BLOCK_SETUP" in get_improvement_suggestions()


def test_improvement_suggestions_contains_no_change():
    assert "NO_CHANGE" in get_improvement_suggestions()


def test_get_quality_grades_length():
    assert len(get_quality_grades()) == 6


def test_quality_grades_contains_excellent():
    assert "EXCELLENT" in get_quality_grades()


def test_quality_grades_contains_good():
    assert "GOOD" in get_quality_grades()


def test_quality_grades_contains_invalid():
    assert "INVALID" in get_quality_grades()


def test_get_performance_dimensions_length():
    assert len(get_performance_dimensions()) == 26


def test_performance_dimensions_contains_win_rate():
    assert "win_rate" in get_performance_dimensions()


def test_performance_dimensions_contains_expectancy_r():
    assert "expectancy_r" in get_performance_dimensions()


def test_performance_dimensions_contains_total_paper_decisions():
    assert "total_paper_decisions" in get_performance_dimensions()


def test_get_forbidden_performance_actions_length():
    assert len(get_forbidden_performance_actions()) == 9


def test_forbidden_actions_contains_buy():
    assert "BUY" in get_forbidden_performance_actions()


def test_forbidden_actions_contains_sell():
    assert "SELL" in get_forbidden_performance_actions()


def test_forbidden_actions_contains_broker_order():
    assert "BROKER_ORDER" in get_forbidden_performance_actions()


def test_get_allowed_performance_actions_length():
    assert len(get_allowed_performance_actions()) == 16


def test_allowed_actions_contains_review():
    assert "REVIEW" in get_allowed_performance_actions()


def test_allowed_actions_contains_analyze():
    assert "ANALYZE" in get_allowed_performance_actions()


def test_allowed_actions_contains_performance_review():
    assert "PERFORMANCE_REVIEW" in get_allowed_performance_actions()


def test_allowed_actions_contains_strategy_improvement():
    assert "STRATEGY_IMPROVEMENT" in get_allowed_performance_actions()


def test_get_hard_block_conditions_length():
    assert len(get_hard_block_conditions()) == 14


def test_hard_block_conditions_contains_real_order_requested():
    assert "real_order_requested" in get_hard_block_conditions()


def test_hard_block_conditions_contains_unsafe_export_path():
    assert "unsafe_export_path" in get_hard_block_conditions()


def test_version_info_paper_only():
    assert get_version_info()["paper_only"] is True


def test_version_info_performance_review_only():
    assert get_version_info()["performance_review_only"] is True


def test_version_info_strategy_improvement_only():
    assert get_version_info()["strategy_improvement_only"] is True


def test_version_info_no_real_orders():
    assert get_version_info()["no_real_orders"] is True


def test_version_info_no_broker():
    assert get_version_info()["no_broker"] is True


def test_version_info_schema_version():
    assert get_version_info()["schema_version"] == "190"


def test_is_known_release_v190():
    assert is_known_release("Paper Trading Performance Review & Strategy Improvement Lab v1.9.0") is True


def test_is_known_release_v189():
    assert is_known_release("Paper Decision Journal & Review Loop v1.8.9") is True


def test_is_known_release_v188():
    assert is_known_release("Paper Decision Workflow Runner v1.8.8") is True


def test_is_known_release_unknown():
    assert is_known_release("UNKNOWN") is False


def test_all_setup_types_are_strings():
    assert all(isinstance(s, str) for s in get_setup_types())


def test_all_improvement_suggestions_are_strings():
    assert all(isinstance(s, str) for s in get_improvement_suggestions())


def test_all_quality_grades_are_strings():
    assert all(isinstance(s, str) for s in get_quality_grades())


def test_all_performance_dimensions_are_strings():
    assert all(isinstance(s, str) for s in get_performance_dimensions())


def test_no_forbidden_actions_contain_review():
    assert not any("REVIEW" in a for a in get_forbidden_performance_actions())


def test_no_forbidden_actions_contain_analyze():
    assert not any("ANALYZE" in a for a in get_forbidden_performance_actions())


def test_get_quality_grades_returns_list():
    assert isinstance(get_quality_grades(), list)


def test_get_setup_types_returns_list():
    assert isinstance(get_setup_types(), list)


def test_get_improvement_suggestions_returns_list():
    assert isinstance(get_improvement_suggestions(), list)


def test_get_performance_dimensions_returns_list():
    assert isinstance(get_performance_dimensions(), list)


def test_get_hard_block_conditions_returns_list():
    assert isinstance(get_hard_block_conditions(), list)


def test_improvement_suggestions_contains_require_more_evidence():
    assert "REQUIRE_MORE_EVIDENCE" in get_improvement_suggestions()


def test_improvement_suggestions_contains_require_risk_review():
    assert "REQUIRE_RISK_REVIEW" in get_improvement_suggestions()


def test_get_setup_types_length_gte_10():
    assert len(get_setup_types()) >= 10


def test_get_quality_grades_length_gte_5():
    assert len(get_quality_grades()) >= 5
