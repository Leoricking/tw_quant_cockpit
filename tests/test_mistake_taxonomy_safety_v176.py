"""tests/test_mistake_taxonomy_safety_v176.py — v1.7.6 safety flag tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_safety_v176 import (
    SAFETY_FLAGS, get_safety_flags, run_safety_audit, assert_safe,
    real_trading, real_account, real_order, broker_execution, production_trading_blocked,
)


class TestSafetyFlags:
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

    def test_safety_flags_paper_only(self):
        assert SAFETY_FLAGS["paper_only"] is True

    def test_safety_flags_research_only(self):
        assert SAFETY_FLAGS["research_only"] is True

    def test_safety_flags_no_real_orders(self):
        assert SAFETY_FLAGS["no_real_orders"] is True

    def test_safety_flags_no_broker(self):
        assert SAFETY_FLAGS["no_broker"] is True

    def test_safety_flags_no_margin(self):
        assert SAFETY_FLAGS["no_margin"] is True

    def test_safety_flags_no_leverage(self):
        assert SAFETY_FLAGS["no_leverage"] is True

    def test_safety_flags_no_production_db(self):
        assert SAFETY_FLAGS["no_production_db_writes"] is True

    def test_safety_flags_real_order_false(self):
        assert SAFETY_FLAGS["real_order"] is False

    def test_safety_flags_broker_exec_false(self):
        assert SAFETY_FLAGS["broker_execution"] is False


class TestGetSafetyFlags:
    def test_returns_dict(self):
        assert isinstance(get_safety_flags(), dict)

    def test_returns_copy(self):
        flags = get_safety_flags()
        flags["paper_only"] = False
        assert SAFETY_FLAGS["paper_only"] is True


class TestSafetyAudit:
    def test_audit_all_safe(self):
        assert run_safety_audit()["all_safe"] is True

    def test_audit_no_issues(self):
        assert run_safety_audit()["issues"] == []

    def test_audit_returns_flags(self):
        assert isinstance(run_safety_audit()["flags"], dict)

    def test_assert_safe_no_raise(self):
        assert_safe()  # must not raise
