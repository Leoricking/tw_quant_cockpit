"""tests/test_small_capital_stop_loss_v170.py — stop loss plan tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.enums_v170 import BuyPointType, StopLossType
from paper_trading.small_capital_strategy.stop_loss_plan_v170 import build_stop_loss_plan


def test_build_stop_loss_plan_a_buy_point():
    plan = build_stop_loss_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0, ma10=480.0)
    assert plan is not None
    assert plan.stop_loss_type == StopLossType.MA_BASED


def test_build_stop_loss_plan_b_buy_point():
    plan = build_stop_loss_plan("2330", BuyPointType.B_PLATFORM_BREAKOUT, entry_price=500.0, swing_low=470.0)
    assert plan is not None


def test_build_stop_loss_plan_c_buy_point():
    plan = build_stop_loss_plan("2330", BuyPointType.C_20MA_RECLAIM, entry_price=500.0, ma20=475.0)
    assert plan is not None


def test_build_stop_loss_plan_fixed_pct():
    plan = build_stop_loss_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0, fixed_stop_pct=0.07)
    assert plan is not None


def test_stop_loss_plan_paper_only():
    plan = build_stop_loss_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0, ma10=480.0)
    assert plan.paper_only is True


def test_stop_loss_plan_no_real_orders():
    plan = build_stop_loss_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0, ma10=480.0)
    assert plan.no_real_orders is True


def test_stop_loss_plan_stop_price_below_entry():
    plan = build_stop_loss_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0, ma10=480.0)
    assert plan.stop_loss_price <= 500.0


def test_stop_loss_plan_fixed_pct_stop_price():
    plan = build_stop_loss_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0, fixed_stop_pct=0.07)
    assert plan.stop_loss_price < 500.0


def test_stop_loss_plan_symbol():
    plan = build_stop_loss_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0, ma10=480.0)
    assert plan.symbol == "2330"
