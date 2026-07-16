"""tests/test_decision_performance_safety_v190.py
Tests for decision performance safety module v1.9.0.
[!] Research Only. Paper Only.
"""
import pytest
from paper_trading.small_capital_strategy.decision_performance_safety_v190 import (
    SAFETY_FLAGS,
    run_safety_audit,
    is_forbidden_action,
    is_allowed_action,
    is_safe_output_path,
    validate_performance_action,
    FORBIDDEN_PERFORMANCE_ACTIONS,
    ALLOWED_PERFORMANCE_ACTIONS,
    HARD_BLOCK_CONDITIONS,
    get_safety_flags,
    get_hard_block_conditions,
)


def test_safety_flags_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True


def test_safety_flags_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True


def test_safety_flags_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True


def test_safety_flags_performance_review_only():
    assert SAFETY_FLAGS["performance_review_only"] is True


def test_safety_flags_strategy_improvement_only():
    assert SAFETY_FLAGS["strategy_improvement_only"] is True


def test_safety_flags_not_investment_advice():
    assert SAFETY_FLAGS["not_investment_advice"] is True


def test_safety_flags_broker_execution_false():
    assert SAFETY_FLAGS["broker_execution"] is False


def test_safety_flags_real_order_false():
    assert SAFETY_FLAGS["real_order"] is False


def test_run_safety_audit_all_safe():
    assert run_safety_audit()["all_safe"] is True


def test_run_safety_audit_paper_only():
    assert run_safety_audit()["paper_only"] is True


def test_run_safety_audit_performance_review_only():
    assert run_safety_audit()["performance_review_only"] is True


def test_is_forbidden_action_buy():
    assert is_forbidden_action("BUY") is True


def test_is_forbidden_action_sell():
    assert is_forbidden_action("SELL") is True


def test_is_forbidden_action_broker_order():
    assert is_forbidden_action("BROKER_ORDER") is True


def test_is_forbidden_action_review_false():
    assert is_forbidden_action("REVIEW") is False


def test_is_allowed_action_review():
    assert is_allowed_action("REVIEW") is True


def test_is_allowed_action_analyze():
    assert is_allowed_action("ANALYZE") is True


def test_is_allowed_action_performance_review():
    assert is_allowed_action("PERFORMANCE_REVIEW") is True


def test_is_allowed_action_strategy_improvement():
    assert is_allowed_action("STRATEGY_IMPROVEMENT") is True


def test_is_allowed_action_buy_false():
    assert is_allowed_action("BUY") is False


def test_is_safe_output_path_reports():
    assert is_safe_output_path("reports/") is True


def test_is_safe_output_path_production_db_false():
    assert is_safe_output_path("production_db/") is False


def test_is_safe_output_path_broker_false():
    assert is_safe_output_path("C:/broker/") is False


def test_forbidden_performance_actions_length():
    assert len(FORBIDDEN_PERFORMANCE_ACTIONS) == 9


def test_allowed_performance_actions_length():
    assert len(ALLOWED_PERFORMANCE_ACTIONS) == 16


def test_hard_block_conditions_length():
    assert len(HARD_BLOCK_CONDITIONS) == 14


def test_hard_block_conditions_contains_real_order_requested():
    assert "real_order_requested" in HARD_BLOCK_CONDITIONS


def test_hard_block_conditions_contains_unsafe_export_path():
    assert "unsafe_export_path" in HARD_BLOCK_CONDITIONS


def test_validate_performance_action_review_returns_dict():
    assert isinstance(validate_performance_action("REVIEW"), dict)


def test_validate_performance_action_review_has_valid_key():
    assert "valid" in validate_performance_action("REVIEW")


def test_validate_performance_action_review_valid_true():
    assert validate_performance_action("REVIEW")["valid"] is True


def test_validate_performance_action_buy_valid_false():
    assert validate_performance_action("BUY")["valid"] is False


def test_validate_performance_action_buy_blocked_true():
    assert validate_performance_action("BUY")["blocked"] is True


def test_get_safety_flags_paper_only():
    assert get_safety_flags()["paper_only"] is True


def test_get_safety_flags_performance_review_only():
    assert get_safety_flags()["performance_review_only"] is True


def test_get_hard_block_conditions_equals_constant():
    assert get_hard_block_conditions() == HARD_BLOCK_CONDITIONS


def test_safety_flags_research_only():
    assert SAFETY_FLAGS["research_only"] is True


def test_safety_flags_simulate_only():
    assert SAFETY_FLAGS["simulate_only"] is True


def test_safety_flags_review_only():
    assert SAFETY_FLAGS["review_only"] is True


def test_safety_flags_audit_only():
    assert SAFETY_FLAGS["audit_only"] is True


def test_safety_flags_no_margin():
    assert SAFETY_FLAGS["no_margin"] is True


def test_safety_flags_no_leverage():
    assert SAFETY_FLAGS["no_leverage"] is True


def test_safety_flags_demo_only():
    assert SAFETY_FLAGS["demo_only"] is True


def test_safety_flags_not_for_production():
    assert SAFETY_FLAGS["not_for_production"] is True


def test_safety_flags_production_trading_blocked():
    assert SAFETY_FLAGS["production_trading_blocked"] is True


def test_safety_flags_length_gte_20():
    assert len(SAFETY_FLAGS) >= 20


def test_is_safe_output_path_empty_false():
    assert is_safe_output_path("") is False


def test_is_safe_output_path_live_broker_false():
    assert is_safe_output_path("live_broker/") is False


def test_allowed_actions_contains_dashboard():
    assert "DASHBOARD" in ALLOWED_PERFORMANCE_ACTIONS


def test_allowed_actions_contains_health_check():
    assert "HEALTH_CHECK" in ALLOWED_PERFORMANCE_ACTIONS


def test_allowed_actions_contains_export():
    assert "EXPORT" in ALLOWED_PERFORMANCE_ACTIONS


def test_allowed_actions_contains_audit():
    assert "AUDIT" in ALLOWED_PERFORMANCE_ACTIONS


def test_forbidden_actions_contains_submit_order():
    assert "SUBMIT_ORDER" in FORBIDDEN_PERFORMANCE_ACTIONS


def test_forbidden_actions_contains_live_trade():
    assert "LIVE_TRADE" in FORBIDDEN_PERFORMANCE_ACTIONS


def test_run_safety_audit_no_broker():
    assert run_safety_audit()["no_broker"] is True


def test_run_safety_audit_not_investment_advice():
    assert run_safety_audit()["not_investment_advice"] is True


def test_run_safety_audit_strategy_improvement_only():
    assert run_safety_audit()["strategy_improvement_only"] is True


def test_run_safety_audit_returns_dict():
    assert isinstance(run_safety_audit(), dict)


def test_safety_flags_is_dict():
    assert isinstance(SAFETY_FLAGS, dict)


def test_forbidden_performance_actions_is_set_or_frozenset():
    assert isinstance(FORBIDDEN_PERFORMANCE_ACTIONS, (set, frozenset))


def test_allowed_performance_actions_is_set_or_frozenset():
    assert isinstance(ALLOWED_PERFORMANCE_ACTIONS, (set, frozenset))
