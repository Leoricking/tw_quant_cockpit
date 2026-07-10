"""tests/test_theme_rotation_safety_v177.py — v1.7.7 safety tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_safety_v177 import (
    run_safety_audit, assert_safe, get_safety_flags, SAFETY_FLAGS,
    THEME_ROTATION_AVAILABLE, THEME_ROTATION_RESEARCH_ONLY, THEME_ROTATION_PAPER_ONLY,
    real_trading, real_account, real_order, broker_execution, production_trading_blocked,
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

    def test_no_margin_true(self):
        assert SAFETY_FLAGS["no_margin"] is True


class TestModuleVariables:
    def test_theme_rotation_available(self):
        assert THEME_ROTATION_AVAILABLE is True

    def test_research_only(self):
        assert THEME_ROTATION_RESEARCH_ONLY is True

    def test_paper_only(self):
        assert THEME_ROTATION_PAPER_ONLY is True

    def test_real_trading_false(self):
        assert real_trading is False

    def test_real_account_false(self):
        assert real_account is False

    def test_real_order_false(self):
        assert real_order is False

    def test_broker_execution_false(self):
        assert broker_execution is False

    def test_production_trading_blocked(self):
        assert production_trading_blocked is True


class TestRunSafetyAudit:
    def test_returns_dict(self):
        result = run_safety_audit()
        assert isinstance(result, dict)

    def test_all_safe_true(self):
        result = run_safety_audit()
        assert result["all_safe"] is True

    def test_issues_empty(self):
        result = run_safety_audit()
        assert result["issues"] == []

    def test_flags_in_result(self):
        result = run_safety_audit()
        assert "flags" in result

    def test_flags_is_dict(self):
        result = run_safety_audit()
        assert isinstance(result["flags"], dict)


class TestGetSafetyFlags:
    def test_returns_dict(self):
        result = get_safety_flags()
        assert isinstance(result, dict)

    def test_paper_only_in_flags(self):
        result = get_safety_flags()
        assert result["paper_only"] is True

    def test_is_copy(self):
        result = get_safety_flags()
        result["paper_only"] = False
        assert SAFETY_FLAGS["paper_only"] is True


class TestAssertSafe:
    def test_assert_safe_does_not_raise(self):
        # Should not raise
        assert_safe()
        assert True
