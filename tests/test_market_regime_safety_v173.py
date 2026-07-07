"""
tests/test_market_regime_safety_v173.py
Tests for Market Regime Position Control safety_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_safety_v173 import (
    MARKET_REGIME_CONTROL_AVAILABLE, MARKET_REGIME_CONTROL_RESEARCH_ONLY,
    MARKET_REGIME_CONTROL_PAPER_ONLY, MARKET_REGIME_CONTROL_READ_ONLY,
    MARKET_REGIME_CONTROL_DETERMINISTIC, MARKET_REGIME_CONTROL_NOT_INVESTMENT_ADVICE,
    MARKET_REGIME_REAL_TRADING_ENABLED, MARKET_REGIME_REAL_ACCOUNT_ENABLED,
    MARKET_REGIME_REAL_ORDER_ENABLED, MARKET_REGIME_BROKER_EXECUTION_ENABLED,
    MARKET_REGIME_PRODUCTION_TRADING_ENABLED, MARKET_REGIME_LIVE_EXECUTION_ENABLED,
    MARKET_REGIME_AUTO_ORDER_ENABLED, MARKET_REGIME_AUTO_STOP_LOSS_ENABLED,
    MARKET_REGIME_AUTO_TAKE_PROFIT_ENABLED, MARKET_REGIME_MARGIN_ENABLED,
    NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    get_market_regime_safety_flags, audit_market_regime_safety, assert_market_regime_safe,
)


class TestPositiveSafetyFlags:
    def test_available_true(self):
        assert MARKET_REGIME_CONTROL_AVAILABLE is True

    def test_research_only_true(self):
        assert MARKET_REGIME_CONTROL_RESEARCH_ONLY is True

    def test_paper_only_true(self):
        assert MARKET_REGIME_CONTROL_PAPER_ONLY is True

    def test_read_only_true(self):
        assert MARKET_REGIME_CONTROL_READ_ONLY is True

    def test_deterministic_true(self):
        assert MARKET_REGIME_CONTROL_DETERMINISTIC is True

    def test_not_investment_advice_true(self):
        assert MARKET_REGIME_CONTROL_NOT_INVESTMENT_ADVICE is True


class TestNegativeSafetyFlags:
    def test_real_trading_false(self):
        assert MARKET_REGIME_REAL_TRADING_ENABLED is False

    def test_real_account_false(self):
        assert MARKET_REGIME_REAL_ACCOUNT_ENABLED is False

    def test_real_order_false(self):
        assert MARKET_REGIME_REAL_ORDER_ENABLED is False

    def test_broker_false(self):
        assert MARKET_REGIME_BROKER_EXECUTION_ENABLED is False

    def test_production_false(self):
        assert MARKET_REGIME_PRODUCTION_TRADING_ENABLED is False

    def test_live_execution_false(self):
        assert MARKET_REGIME_LIVE_EXECUTION_ENABLED is False

    def test_auto_order_false(self):
        assert MARKET_REGIME_AUTO_ORDER_ENABLED is False

    def test_auto_stop_loss_false(self):
        assert MARKET_REGIME_AUTO_STOP_LOSS_ENABLED is False

    def test_auto_take_profit_false(self):
        assert MARKET_REGIME_AUTO_TAKE_PROFIT_ENABLED is False

    def test_margin_false(self):
        assert MARKET_REGIME_MARGIN_ENABLED is False


class TestAliases:
    def test_no_real_orders_true(self):
        assert NO_REAL_ORDERS is True

    def test_broker_execution_enabled_false(self):
        assert BROKER_EXECUTION_ENABLED is False

    def test_production_blocked_true(self):
        assert PRODUCTION_TRADING_BLOCKED is True


class TestGetFlags:
    def test_returns_dict(self):
        flags = get_market_regime_safety_flags()
        assert isinstance(flags, dict)

    def test_margin_false_in_dict(self):
        flags = get_market_regime_safety_flags()
        assert flags["MARKET_REGIME_MARGIN_ENABLED"] is False

    def test_no_real_orders_in_dict(self):
        flags = get_market_regime_safety_flags()
        assert flags["NO_REAL_ORDERS"] is True


class TestAudit:
    def test_all_safe_true(self):
        result = audit_market_regime_safety()
        assert result["all_safe"] is True

    def test_zero_dangerous_capabilities(self):
        result = audit_market_regime_safety()
        assert result["safety_capabilities"] == 0

    def test_no_issues(self):
        result = audit_market_regime_safety()
        assert result["issues"] == []

    def test_flags_in_result(self):
        result = audit_market_regime_safety()
        assert "flags" in result


class TestAssertSafe:
    def test_does_not_raise(self):
        assert_market_regime_safe()  # should not raise
