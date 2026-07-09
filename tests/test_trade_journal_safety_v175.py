"""
tests/test_trade_journal_safety_v175.py
Tests for Trade Journal safety v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_safety_v175 import (
    SAFETY_FLAGS, get_safety_flags, run_safety_audit, assert_safe,
    real_trading, real_account, real_order, broker_execution, production_trading_blocked,
    TRADE_JOURNAL_AVAILABLE, TRADE_JOURNAL_RESEARCH_ONLY, TRADE_JOURNAL_PAPER_ONLY,
)


class TestSafetyFlags:
    def test_paper_only_true(self):
        assert SAFETY_FLAGS["paper_only"] is True

    def test_research_only_true(self):
        assert SAFETY_FLAGS["research_only"] is True

    def test_no_real_orders_true(self):
        assert SAFETY_FLAGS["no_real_orders"] is True

    def test_no_broker_true(self):
        assert SAFETY_FLAGS["no_broker"] is True

    def test_not_investment_advice_true(self):
        assert SAFETY_FLAGS["not_investment_advice"] is True

    def test_production_trading_blocked_true(self):
        assert SAFETY_FLAGS["production_trading_blocked"] is True

    def test_real_trading_false(self):
        assert SAFETY_FLAGS["real_trading"] is False

    def test_real_account_false(self):
        assert SAFETY_FLAGS["real_account"] is False

    def test_real_order_false(self):
        assert SAFETY_FLAGS["real_order"] is False

    def test_broker_execution_false(self):
        assert SAFETY_FLAGS["broker_execution"] is False


class TestModuleConstants:
    def test_trade_journal_available(self):
        assert TRADE_JOURNAL_AVAILABLE is True

    def test_trade_journal_research_only(self):
        assert TRADE_JOURNAL_RESEARCH_ONLY is True

    def test_trade_journal_paper_only(self):
        assert TRADE_JOURNAL_PAPER_ONLY is True

    def test_real_trading_false(self):
        assert real_trading is False

    def test_real_account_false(self):
        assert real_account is False

    def test_real_order_false(self):
        assert real_order is False

    def test_broker_execution_false(self):
        assert broker_execution is False

    def test_production_trading_blocked_true(self):
        assert production_trading_blocked is True


class TestGetSafetyFlags:
    def test_returns_dict(self):
        assert isinstance(get_safety_flags(), dict)

    def test_paper_only_in_result(self):
        flags = get_safety_flags()
        assert flags["paper_only"] is True

    def test_real_order_false_in_result(self):
        flags = get_safety_flags()
        assert flags["real_order"] is False


class TestRunSafetyAudit:
    def test_all_safe_true(self):
        result = run_safety_audit()
        assert result["all_safe"] is True

    def test_issues_empty(self):
        result = run_safety_audit()
        assert result["issues"] == []

    def test_flags_in_result(self):
        result = run_safety_audit()
        assert "flags" in result

    def test_returns_dict(self):
        assert isinstance(run_safety_audit(), dict)


class TestAssertSafe:
    def test_assert_safe_no_raise(self):
        # Should not raise
        assert_safe()

    def test_assert_safe_returns_none(self):
        result = assert_safe()
        assert result is None
