"""
tests/test_risk_dashboard_safety_v174.py
Tests for Small Account Risk Dashboard safety flags v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_safety_v174 import (
    SMALL_ACCOUNT_RISK_DASHBOARD_AVAILABLE,
    SMALL_ACCOUNT_RISK_DASHBOARD_RESEARCH_ONLY,
    SMALL_ACCOUNT_RISK_DASHBOARD_PAPER_ONLY,
    SMALL_ACCOUNT_RISK_DASHBOARD_READ_ONLY,
    SMALL_ACCOUNT_RISK_DASHBOARD_DETERMINISTIC,
    SMALL_ACCOUNT_RISK_DASHBOARD_NOT_INVESTMENT_ADVICE,
    SMALL_ACCOUNT_RISK_REAL_TRADING_ENABLED,
    SMALL_ACCOUNT_RISK_REAL_ACCOUNT_ENABLED,
    SMALL_ACCOUNT_RISK_REAL_ORDER_ENABLED,
    SMALL_ACCOUNT_RISK_BROKER_EXECUTION_ENABLED,
    SMALL_ACCOUNT_RISK_PRODUCTION_TRADING_ENABLED,
    SMALL_ACCOUNT_RISK_LIVE_EXECUTION_ENABLED,
    SMALL_ACCOUNT_RISK_AUTO_ORDER_ENABLED,
    SMALL_ACCOUNT_RISK_AUTO_STOP_LOSS_ENABLED,
    SMALL_ACCOUNT_RISK_AUTO_TAKE_PROFIT_ENABLED,
    SMALL_ACCOUNT_RISK_MARGIN_ENABLED,
    NO_REAL_ORDERS,
    BROKER_EXECUTION_ENABLED,
    PRODUCTION_TRADING_BLOCKED,
    get_risk_dashboard_safety_flags,
    audit_risk_dashboard_safety,
    assert_risk_dashboard_safe,
)


class TestPositiveSafetyFlags:
    def test_available_true(self):
        assert SMALL_ACCOUNT_RISK_DASHBOARD_AVAILABLE is True

    def test_research_only_true(self):
        assert SMALL_ACCOUNT_RISK_DASHBOARD_RESEARCH_ONLY is True

    def test_paper_only_true(self):
        assert SMALL_ACCOUNT_RISK_DASHBOARD_PAPER_ONLY is True

    def test_read_only_true(self):
        assert SMALL_ACCOUNT_RISK_DASHBOARD_READ_ONLY is True

    def test_deterministic_true(self):
        assert SMALL_ACCOUNT_RISK_DASHBOARD_DETERMINISTIC is True

    def test_not_investment_advice_true(self):
        assert SMALL_ACCOUNT_RISK_DASHBOARD_NOT_INVESTMENT_ADVICE is True

    def test_no_real_orders_alias_true(self):
        assert NO_REAL_ORDERS is True

    def test_production_trading_blocked_true(self):
        assert PRODUCTION_TRADING_BLOCKED is True


class TestNegativeSafetyFlags:
    def test_real_trading_false(self):
        assert SMALL_ACCOUNT_RISK_REAL_TRADING_ENABLED is False

    def test_real_account_false(self):
        assert SMALL_ACCOUNT_RISK_REAL_ACCOUNT_ENABLED is False

    def test_real_order_false(self):
        assert SMALL_ACCOUNT_RISK_REAL_ORDER_ENABLED is False

    def test_broker_execution_false(self):
        assert SMALL_ACCOUNT_RISK_BROKER_EXECUTION_ENABLED is False

    def test_production_trading_false(self):
        assert SMALL_ACCOUNT_RISK_PRODUCTION_TRADING_ENABLED is False

    def test_live_execution_false(self):
        assert SMALL_ACCOUNT_RISK_LIVE_EXECUTION_ENABLED is False

    def test_auto_order_false(self):
        assert SMALL_ACCOUNT_RISK_AUTO_ORDER_ENABLED is False

    def test_auto_stop_loss_false(self):
        assert SMALL_ACCOUNT_RISK_AUTO_STOP_LOSS_ENABLED is False

    def test_auto_take_profit_false(self):
        assert SMALL_ACCOUNT_RISK_AUTO_TAKE_PROFIT_ENABLED is False

    def test_margin_false(self):
        assert SMALL_ACCOUNT_RISK_MARGIN_ENABLED is False

    def test_broker_execution_alias_false(self):
        assert BROKER_EXECUTION_ENABLED is False


class TestSafetyAuditFunctions:
    def test_get_flags_returns_dict(self):
        flags = get_risk_dashboard_safety_flags()
        assert isinstance(flags, dict)

    def test_get_flags_not_empty(self):
        assert len(get_risk_dashboard_safety_flags()) > 0

    def test_audit_all_safe(self):
        result = audit_risk_dashboard_safety()
        assert result["all_safe"] is True

    def test_audit_zero_capabilities(self):
        assert audit_risk_dashboard_safety()["safety_capabilities"] == 0

    def test_audit_empty_issues(self):
        assert audit_risk_dashboard_safety()["issues"] == []

    def test_assert_safe_no_raise(self):
        assert_risk_dashboard_safe()  # Should not raise

    def test_audit_flags_key_exists(self):
        assert "flags" in audit_risk_dashboard_safety()
