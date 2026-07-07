"""tests/test_abc_safety_v172.py — Safety flag tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_execution_safety_v172 import (
    ABC_EXECUTION_PLAN_AVAILABLE, ABC_EXECUTION_PLAN_RESEARCH_ONLY,
    ABC_EXECUTION_PLAN_PAPER_ONLY, ABC_EXECUTION_PLAN_NOT_INVESTMENT_ADVICE,
    ABC_REAL_TRADING_ENABLED, ABC_REAL_ACCOUNT_ENABLED,
    ABC_REAL_ORDER_ENABLED, ABC_BROKER_EXECUTION_ENABLED,
    ABC_PRODUCTION_TRADING_ENABLED, ABC_LIVE_EXECUTION_ENABLED,
    ABC_AUTO_ORDER_ENABLED, ABC_AUTO_STOP_LOSS_ENABLED,
    ABC_AUTO_TAKE_PROFIT_ENABLED, ABC_MARGIN_ENABLED,
    ABC_DAY_TRADING_PRIMARY_ENABLED,
    NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    get_abc_safety_flags, audit_abc_safety, assert_abc_safe,
)


def test_available_true():
    assert ABC_EXECUTION_PLAN_AVAILABLE is True


def test_research_only_true():
    assert ABC_EXECUTION_PLAN_RESEARCH_ONLY is True


def test_paper_only_true():
    assert ABC_EXECUTION_PLAN_PAPER_ONLY is True


def test_not_investment_advice_true():
    assert ABC_EXECUTION_PLAN_NOT_INVESTMENT_ADVICE is True


def test_real_trading_false():
    assert ABC_REAL_TRADING_ENABLED is False


def test_real_account_false():
    assert ABC_REAL_ACCOUNT_ENABLED is False


def test_real_order_false():
    assert ABC_REAL_ORDER_ENABLED is False


def test_broker_execution_false():
    assert ABC_BROKER_EXECUTION_ENABLED is False


def test_production_trading_false():
    assert ABC_PRODUCTION_TRADING_ENABLED is False


def test_live_execution_false():
    assert ABC_LIVE_EXECUTION_ENABLED is False


def test_auto_order_false():
    assert ABC_AUTO_ORDER_ENABLED is False


def test_auto_stop_loss_false():
    assert ABC_AUTO_STOP_LOSS_ENABLED is False


def test_auto_take_profit_false():
    assert ABC_AUTO_TAKE_PROFIT_ENABLED is False


def test_margin_false():
    assert ABC_MARGIN_ENABLED is False


def test_day_trading_primary_false():
    assert ABC_DAY_TRADING_PRIMARY_ENABLED is False


def test_no_real_orders_true():
    assert NO_REAL_ORDERS is True


def test_broker_execution_enabled_false():
    assert BROKER_EXECUTION_ENABLED is False


def test_production_trading_blocked_true():
    assert PRODUCTION_TRADING_BLOCKED is True


def test_get_abc_safety_flags_returns_dict():
    flags = get_abc_safety_flags()
    assert isinstance(flags, dict)


def test_get_abc_safety_flags_contains_available():
    assert "ABC_EXECUTION_PLAN_AVAILABLE" in get_abc_safety_flags()


def test_audit_abc_safety_all_safe():
    result = audit_abc_safety()
    assert result["all_safe"] is True


def test_audit_abc_safety_capabilities_zero():
    result = audit_abc_safety()
    assert result["safety_capabilities"] == 0


def test_audit_abc_safety_no_issues():
    result = audit_abc_safety()
    assert result["issues"] == []


def test_audit_abc_safety_has_flags():
    result = audit_abc_safety()
    assert isinstance(result["flags"], dict)


def test_assert_abc_safe_does_not_raise():
    assert_abc_safe()  # must not raise
