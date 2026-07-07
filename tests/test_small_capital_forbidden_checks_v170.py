"""tests/test_small_capital_forbidden_checks_v170.py — forbidden trade rule tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.forbidden_trade_rules_v170 import (
    check_margin, check_day_trading_primary,
    check_financing_overheated, check_insufficient_cash,
    check_no_stop_loss, check_position_risk_vs_budget,
    check_real_order, check_total_holdings, check_weak_theme,
    check_below_20ma, check_below_60ma, check_broker_execution,
    run_all_forbidden_checks, get_permission_status,
    TradePermissionStatus,
)
from paper_trading.small_capital_strategy.enums_v170 import ForbiddenTradeReason, ThemeStrength


def _all_clear_context():
    return {
        "margin_requested": False,
        "is_day_trading_primary": False,
        "financing_overheated": False,
        "real_order_requested": False,
        "broker_requested": False,
        "stop_loss_price": 470.0,
        "current_holdings": 2,
        "max_holdings": 4,
        "theme_strength": ThemeStrength.STRONG.value,
        "close_gt_ma20": True,
        "close_gt_ma60": True,
        "current_cash_pct": 0.30,
        "required_cash_min_pct": 0.20,
        "position_risk_twd": 2500.0,
        "risk_budget_twd": 3000.0,
    }


def test_check_margin_use_margin_forbidden():
    result = check_margin("2330", margin_requested=True)
    assert result.blocked is True
    assert result.reason == ForbiddenTradeReason.MARGIN_NOT_ALLOWED


def test_check_margin_no_margin_ok():
    result = check_margin("2330", margin_requested=False)
    assert result.blocked is False


def test_check_day_trading_primary_forbidden():
    result = check_day_trading_primary("2330", is_day_trading_primary=True)
    assert result.blocked is True


def test_check_day_trading_not_primary_ok():
    result = check_day_trading_primary("2330", is_day_trading_primary=False)
    assert result.blocked is False


def test_check_real_order_forbidden():
    result = check_real_order("2330", real_order_requested=True)
    assert result.blocked is True


def test_check_real_order_ok():
    result = check_real_order("2330", real_order_requested=False)
    assert result.blocked is False


def test_check_total_holdings_over_limit():
    result = check_total_holdings("2330", current_holdings=5, max_holdings=4)
    assert result.blocked is True


def test_check_total_holdings_ok():
    result = check_total_holdings("2330", current_holdings=3, max_holdings=4)
    assert result.blocked is False


def test_check_position_risk_vs_budget_exceeded():
    result = check_position_risk_vs_budget("2330", position_risk_twd=5000.0, risk_budget_twd=3000.0)
    assert result.blocked is True


def test_check_position_risk_vs_budget_ok():
    result = check_position_risk_vs_budget("2330", position_risk_twd=2500.0, risk_budget_twd=3000.0)
    assert result.blocked is False


def test_check_no_stop_loss_forbidden():
    result = check_no_stop_loss("2330", stop_loss_price=0.0)
    assert result.blocked is True


def test_check_no_stop_loss_ok():
    result = check_no_stop_loss("2330", stop_loss_price=470.0)
    assert result.blocked is False


def test_check_financing_overheated():
    result = check_financing_overheated("2330", financing_overheated=True)
    assert result.blocked is True


def test_check_financing_ok():
    result = check_financing_overheated("2330", financing_overheated=False)
    assert result.blocked is False


def test_check_weak_theme_forbidden():
    result = check_weak_theme("2330", theme_strength=ThemeStrength.WEAK.value)
    assert result.blocked is True


def test_check_weak_theme_strong_ok():
    result = check_weak_theme("2330", theme_strength=ThemeStrength.STRONG.value)
    assert result.blocked is False


def test_check_below_20ma_forbidden():
    result = check_below_20ma("2330", close_gt_ma20=False)
    assert result.blocked is True


def test_check_below_20ma_ok():
    result = check_below_20ma("2330", close_gt_ma20=True)
    assert result.blocked is False


def test_check_broker_execution_forbidden():
    result = check_broker_execution("2330", broker_requested=True)
    assert result.blocked is True


def test_check_broker_execution_ok():
    result = check_broker_execution("2330", broker_requested=False)
    assert result.blocked is False


def test_check_insufficient_cash_forbidden():
    result = check_insufficient_cash("2330", current_cash_pct=0.10, required_cash_min_pct=0.20)
    assert result.blocked is True


def test_check_insufficient_cash_ok():
    result = check_insufficient_cash("2330", current_cash_pct=0.30, required_cash_min_pct=0.20)
    assert result.blocked is False


def test_run_all_forbidden_checks_all_clear():
    checks = run_all_forbidden_checks("2330", _all_clear_context())
    assert not any(c.blocked for c in checks)


def test_run_all_forbidden_checks_returns_list():
    checks = run_all_forbidden_checks("2330", _all_clear_context())
    assert isinstance(checks, list)


def test_get_permission_status_allowed():
    checks = run_all_forbidden_checks("2330", _all_clear_context())
    status = get_permission_status(checks)
    assert status == TradePermissionStatus.ALLOWED


def test_get_permission_status_blocked_on_margin():
    ctx = _all_clear_context()
    ctx["margin_requested"] = True
    checks = run_all_forbidden_checks("2330", ctx)
    status = get_permission_status(checks)
    assert status == TradePermissionStatus.BLOCKED
