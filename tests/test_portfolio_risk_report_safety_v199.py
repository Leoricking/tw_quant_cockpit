"""
tests/test_portfolio_risk_report_safety_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Safety Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_risk_report_safety_v199 import (
    SAFETY_FLAGS,
    FORBIDDEN_ACTIONS,
    ALLOWED_ACTIONS,
    HARD_BLOCK_CONDITIONS,
    run_safety_audit,
    assert_safe,
    is_safe_export_path,
)


def test_safety_flags_is_dict():
    assert isinstance(SAFETY_FLAGS, dict)


def test_safety_flags_paper_only_True():
    assert SAFETY_FLAGS["paper_only"] is True


def test_safety_flags_no_real_orders_True():
    assert SAFETY_FLAGS["no_real_orders"] is True


def test_safety_flags_not_investment_advice_True():
    assert SAFETY_FLAGS["not_investment_advice"] is True


def test_safety_flags_no_broker_True():
    assert SAFETY_FLAGS["no_broker"] is True


def test_safety_flags_no_margin_True():
    assert SAFETY_FLAGS["no_margin"] is True


def test_safety_flags_no_leverage_True():
    assert SAFETY_FLAGS["no_leverage"] is True


def test_safety_flags_sizing_executes_order_False():
    assert SAFETY_FLAGS["sizing_executes_order"] is False


def test_safety_flags_dashboard_mutates_strategy_False():
    assert SAFETY_FLAGS["dashboard_mutates_strategy"] is False


def test_safety_flags_export_triggers_real_order_False():
    assert SAFETY_FLAGS.get("export_triggers_real_order") is False


def test_forbidden_actions_is_list():
    assert isinstance(FORBIDDEN_ACTIONS, list)


def test_forbidden_actions_has_BUY():
    assert "BUY" in FORBIDDEN_ACTIONS


def test_forbidden_actions_has_SELL():
    assert "SELL" in FORBIDDEN_ACTIONS


def test_forbidden_actions_has_ORDER():
    assert "ORDER" in FORBIDDEN_ACTIONS


def test_forbidden_actions_has_EXECUTE():
    assert "EXECUTE" in FORBIDDEN_ACTIONS


def test_allowed_actions_is_list():
    assert isinstance(ALLOWED_ACTIONS, list)


def test_allowed_actions_has_paper_actions():
    paper_count = sum(1 for a in ALLOWED_ACTIONS if a.startswith("PAPER_"))
    assert paper_count > 0


def test_forbidden_actions_no_overlap_with_allowed_actions():
    assert not any(fa in ALLOWED_ACTIONS for fa in FORBIDDEN_ACTIONS)


def test_allowed_actions_no_overlap_with_forbidden_actions():
    assert not any(aa in FORBIDDEN_ACTIONS for aa in ALLOWED_ACTIONS)


def test_hard_block_conditions_is_list():
    assert isinstance(HARD_BLOCK_CONDITIONS, list)


def test_hard_block_conditions_has_real_order_requested():
    assert "real_order_requested" in HARD_BLOCK_CONDITIONS


def test_hard_block_conditions_has_missing_paper_only_flags():
    assert "missing_paper_only_flags" in HARD_BLOCK_CONDITIONS


def test_hard_block_conditions_has_broker_requested():
    assert "broker_requested" in HARD_BLOCK_CONDITIONS


def test_hard_block_conditions_has_unsafe_export_path():
    assert "unsafe_export_path" in HARD_BLOCK_CONDITIONS


def test_hard_block_conditions_has_forbidden_action_words():
    assert "forbidden_action_words" in HARD_BLOCK_CONDITIONS


def test_run_safety_audit_returns_dict():
    assert isinstance(run_safety_audit(), dict)


def test_run_safety_audit_all_safe_True():
    assert run_safety_audit()["all_safe"] is True


def test_run_safety_audit_paper_only_True():
    assert run_safety_audit()["paper_only"] is True


def test_run_safety_audit_no_real_orders_True():
    assert run_safety_audit()["no_real_orders"] is True


def test_run_safety_audit_errors_is_empty_list():
    assert run_safety_audit()["errors"] == []


def test_run_safety_audit_safety_flags_count_gt_0():
    assert run_safety_audit()["safety_flags_count"] > 0


def test_assert_safe_BUY_raises_ValueError():
    with pytest.raises(ValueError):
        assert_safe("BUY")


def test_assert_safe_SELL_raises_ValueError():
    with pytest.raises(ValueError):
        assert_safe("SELL")


def test_assert_safe_ORDER_raises_ValueError():
    with pytest.raises(ValueError):
        assert_safe("ORDER")


def test_assert_safe_PAPER_ALLOW_NORMAL_SIZE_does_not_raise():
    raised = False
    try:
        assert_safe("PAPER_ALLOW_NORMAL_SIZE")
    except ValueError:
        raised = True
    assert raised is False


def test_is_safe_export_path_empty_string_returns_False():
    assert is_safe_export_path("") is False


def test_is_safe_export_path_production_data_returns_False():
    assert is_safe_export_path("production/data") is False


def test_is_safe_export_path_paper_data_report_returns_True():
    assert is_safe_export_path("paper_data/report") is True


def test_is_safe_export_path_live_path_returns_False():
    assert is_safe_export_path("live/export") is False


def test_is_safe_export_path_paper_export_returns_True():
    assert is_safe_export_path("paper_export/risk_report.json") is True


def test_run_safety_audit_production_trading_blocked_True():
    assert run_safety_audit()["production_trading_blocked"] is True
