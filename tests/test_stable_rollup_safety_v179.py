"""
tests/test_stable_rollup_safety_v179.py
Tests for stable_rollup_safety_v179 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.stable_rollup_safety_v179 import (
    SAFETY_FLAGS,
    get_safety_flags,
    run_safety_audit,
    assert_safe,
)


def test_safety_flags_is_dict():
    assert isinstance(SAFETY_FLAGS, dict)


def test_paper_only_is_true():
    assert SAFETY_FLAGS["paper_only"] is True


def test_research_only_is_true():
    assert SAFETY_FLAGS["research_only"] is True


def test_no_real_orders_is_true():
    assert SAFETY_FLAGS["no_real_orders"] is True


def test_no_broker_is_true():
    assert SAFETY_FLAGS["no_broker"] is True


def test_not_investment_advice_is_true():
    assert SAFETY_FLAGS["not_investment_advice"] is True


def test_production_trading_blocked_is_true():
    assert SAFETY_FLAGS["production_trading_blocked"] is True


def test_real_trading_is_false():
    assert SAFETY_FLAGS["real_trading"] is False


def test_real_account_is_false():
    assert SAFETY_FLAGS["real_account"] is False


def test_real_order_is_false():
    assert SAFETY_FLAGS["real_order"] is False


def test_broker_execution_is_false():
    assert SAFETY_FLAGS["broker_execution"] is False


def test_no_margin_is_true():
    assert SAFETY_FLAGS["no_margin"] is True


def test_no_leverage_is_true():
    assert SAFETY_FLAGS["no_leverage"] is True


def test_no_production_db_writes_is_true():
    assert SAFETY_FLAGS["no_production_db_writes"] is True


def test_demo_only_is_true():
    assert SAFETY_FLAGS["demo_only"] is True


def test_not_for_production_is_true():
    assert SAFETY_FLAGS["not_for_production"] is True


def test_get_safety_flags_returns_dict():
    flags = get_safety_flags()
    assert isinstance(flags, dict)


def test_get_safety_flags_is_copy():
    flags1 = get_safety_flags()
    flags2 = get_safety_flags()
    assert flags1 is not flags2


def test_get_safety_flags_paper_only():
    flags = get_safety_flags()
    assert flags["paper_only"] is True


def test_get_safety_flags_real_order_false():
    flags = get_safety_flags()
    assert flags["real_order"] is False


def test_run_safety_audit_returns_dict():
    result = run_safety_audit()
    assert isinstance(result, dict)


def test_run_safety_audit_all_safe():
    result = run_safety_audit()
    assert result["all_safe"] is True


def test_run_safety_audit_no_issues():
    result = run_safety_audit()
    assert len(result["issues"]) == 0


def test_run_safety_audit_has_flags_key():
    result = run_safety_audit()
    assert "flags" in result


def test_run_safety_audit_flags_match_safety_flags():
    result = run_safety_audit()
    assert result["flags"]["paper_only"] is True
    assert result["flags"]["real_order"] is False


def test_assert_safe_does_not_raise():
    assert_safe()


def test_safety_flags_contains_all_required_true_keys():
    required_true = ["paper_only", "research_only", "no_real_orders", "no_broker", "not_investment_advice"]
    for key in required_true:
        assert SAFETY_FLAGS.get(key) is True, f"Expected {key} to be True"


def test_safety_flags_contains_all_required_false_keys():
    required_false = ["real_trading", "real_account", "real_order", "broker_execution"]
    for key in required_false:
        assert SAFETY_FLAGS.get(key) is False, f"Expected {key} to be False"
