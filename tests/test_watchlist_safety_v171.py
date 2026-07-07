"""tests/test_watchlist_safety_v171.py — safety flag tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_safety_v171 import (
    WATCHLIST_STRATEGY_AVAILABLE, WATCHLIST_STRATEGY_RESEARCH_ONLY,
    WATCHLIST_STRATEGY_PAPER_ONLY, WATCHLIST_STRATEGY_READ_ONLY,
    WATCHLIST_STRATEGY_DETERMINISTIC, WATCHLIST_STRATEGY_NOT_INVESTMENT_ADVICE,
    WATCHLIST_REAL_TRADING_ENABLED, WATCHLIST_REAL_ACCOUNT_ENABLED,
    WATCHLIST_REAL_ORDER_ENABLED, WATCHLIST_BROKER_EXECUTION_ENABLED,
    WATCHLIST_PRODUCTION_TRADING_ENABLED, WATCHLIST_LIVE_EXECUTION_ENABLED,
    WATCHLIST_AUTO_ORDER_ENABLED, WATCHLIST_MARGIN_ENABLED,
    NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    get_watchlist_safety_flags, audit_watchlist_safety, assert_watchlist_safe,
)


def test_available_true():
    assert WATCHLIST_STRATEGY_AVAILABLE is True


def test_research_only_true():
    assert WATCHLIST_STRATEGY_RESEARCH_ONLY is True


def test_paper_only_true():
    assert WATCHLIST_STRATEGY_PAPER_ONLY is True


def test_read_only_true():
    assert WATCHLIST_STRATEGY_READ_ONLY is True


def test_deterministic_true():
    assert WATCHLIST_STRATEGY_DETERMINISTIC is True


def test_not_investment_advice_true():
    assert WATCHLIST_STRATEGY_NOT_INVESTMENT_ADVICE is True


def test_real_trading_disabled():
    assert WATCHLIST_REAL_TRADING_ENABLED is False


def test_real_account_disabled():
    assert WATCHLIST_REAL_ACCOUNT_ENABLED is False


def test_real_order_disabled():
    assert WATCHLIST_REAL_ORDER_ENABLED is False


def test_broker_execution_disabled():
    assert WATCHLIST_BROKER_EXECUTION_ENABLED is False


def test_production_trading_disabled():
    assert WATCHLIST_PRODUCTION_TRADING_ENABLED is False


def test_live_execution_disabled():
    assert WATCHLIST_LIVE_EXECUTION_ENABLED is False


def test_auto_order_disabled():
    assert WATCHLIST_AUTO_ORDER_ENABLED is False


def test_margin_disabled():
    assert WATCHLIST_MARGIN_ENABLED is False


def test_no_real_orders_true():
    assert NO_REAL_ORDERS is True


def test_broker_execution_enabled_false():
    assert BROKER_EXECUTION_ENABLED is False


def test_production_trading_blocked():
    assert PRODUCTION_TRADING_BLOCKED is True


def test_get_flags_returns_dict():
    assert isinstance(get_watchlist_safety_flags(), dict)


def test_get_flags_has_available():
    assert "WATCHLIST_STRATEGY_AVAILABLE" in get_watchlist_safety_flags()


def test_get_flags_all_disabled_correct():
    flags = get_watchlist_safety_flags()
    for key in [
        "WATCHLIST_REAL_TRADING_ENABLED",
        "WATCHLIST_BROKER_EXECUTION_ENABLED",
        "WATCHLIST_MARGIN_ENABLED",
    ]:
        assert flags[key] is False


def test_audit_all_safe():
    result = audit_watchlist_safety()
    assert result["all_safe"] is True


def test_audit_safety_capabilities_zero():
    result = audit_watchlist_safety()
    assert result["safety_capabilities"] == 0


def test_audit_no_issues():
    result = audit_watchlist_safety()
    assert result["issues"] == []


def test_assert_safe_no_raise():
    assert_watchlist_safe()  # should not raise
