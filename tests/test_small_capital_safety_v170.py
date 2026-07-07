"""tests/test_small_capital_safety_v170.py — safety flag tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.safety_v170 import (
    LIVE_FALLBACK_ENABLED, BROKER_ENABLED, REAL_ACCOUNT_ENABLED,
    REAL_ORDER_ENABLED, PRODUCTION_TRADING_ENABLED, AUTO_ORDER_ENABLED,
    AUTO_STOP_LOSS_ENABLED, AUTO_TAKE_PROFIT_ENABLED, MARGIN_ENABLED,
    DAY_TRADING_PRIMARY_ENABLED, SHIOAJI_ENABLED, EXTERNAL_HTTP_ENABLED,
    PRODUCTION_WRITE_ENABLED, REAL_CAPITAL_MUTATION_ENABLED,
    REAL_TRADING_ENABLED,
    RESEARCH_ONLY, PAPER_ONLY, NO_REAL_ORDERS, NOT_INVESTMENT_ADVICE,
    DETERMINISTIC, READ_ONLY,
    get_safety_flags, audit_safety, assert_safe,
)


def test_live_fallback_disabled():
    assert LIVE_FALLBACK_ENABLED is False


def test_broker_disabled():
    assert BROKER_ENABLED is False


def test_real_account_disabled():
    assert REAL_ACCOUNT_ENABLED is False


def test_real_order_disabled():
    assert REAL_ORDER_ENABLED is False


def test_production_trading_disabled():
    assert PRODUCTION_TRADING_ENABLED is False


def test_auto_order_disabled():
    assert AUTO_ORDER_ENABLED is False


def test_auto_stop_loss_disabled():
    assert AUTO_STOP_LOSS_ENABLED is False


def test_auto_take_profit_disabled():
    assert AUTO_TAKE_PROFIT_ENABLED is False


def test_margin_disabled():
    assert MARGIN_ENABLED is False


def test_day_trading_primary_disabled():
    assert DAY_TRADING_PRIMARY_ENABLED is False


def test_shioaji_disabled():
    assert SHIOAJI_ENABLED is False


def test_external_http_disabled():
    assert EXTERNAL_HTTP_ENABLED is False


def test_production_write_disabled():
    assert PRODUCTION_WRITE_ENABLED is False


def test_real_capital_mutation_disabled():
    assert REAL_CAPITAL_MUTATION_ENABLED is False


def test_real_trading_disabled():
    assert REAL_TRADING_ENABLED is False


def test_research_only_true():
    assert RESEARCH_ONLY is True


def test_paper_only_true():
    assert PAPER_ONLY is True


def test_no_real_orders_true():
    assert NO_REAL_ORDERS is True


def test_not_investment_advice_true():
    assert NOT_INVESTMENT_ADVICE is True


def test_deterministic_true():
    assert DETERMINISTIC is True


def test_read_only_true():
    assert READ_ONLY is True


def test_get_safety_flags_returns_dict():
    flags = get_safety_flags()
    assert isinstance(flags, dict)


def test_get_safety_flags_live_fallback_false():
    flags = get_safety_flags()
    assert flags["LIVE_FALLBACK_ENABLED"] is False


def test_get_safety_flags_research_only_true():
    flags = get_safety_flags()
    assert flags["RESEARCH_ONLY"] is True


def test_get_safety_flags_broker_false():
    flags = get_safety_flags()
    assert flags["BROKER_ENABLED"] is False


def test_audit_safety_returns_dict():
    result = audit_safety()
    assert isinstance(result, dict)


def test_audit_safety_all_safe():
    result = audit_safety()
    assert result["all_safe"] is True


def test_audit_safety_no_issues():
    result = audit_safety()
    assert len(result["issues"]) == 0


def test_audit_safety_has_flags():
    result = audit_safety()
    assert "flags" in result


def test_assert_safe_does_not_raise():
    assert_safe()


def test_audit_safety_capabilities():
    result = audit_safety()
    assert "safety_capabilities" in result
