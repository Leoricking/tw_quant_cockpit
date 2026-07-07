"""tests/test_small_capital_take_profit_v170.py — take profit plan tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.enums_v170 import TakeProfitType, BuyPointType
from paper_trading.small_capital_strategy.take_profit_plan_v170 import (
    build_take_profit_plan, validate_take_profit_plan,
)


def test_build_take_profit_a_buy_point():
    plan = build_take_profit_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0)
    assert plan is not None


def test_build_take_profit_b_buy_point():
    plan = build_take_profit_plan("2330", BuyPointType.B_PLATFORM_BREAKOUT, entry_price=500.0)
    assert plan is not None


def test_build_take_profit_c_buy_point():
    plan = build_take_profit_plan("2330", BuyPointType.C_20MA_RECLAIM, entry_price=500.0)
    assert plan is not None


def test_build_take_profit_paper_only():
    plan = build_take_profit_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0)
    assert plan.paper_only is True


def test_build_take_profit_no_real_orders():
    plan = build_take_profit_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0)
    assert plan.no_real_orders is True


def test_build_take_profit_symbol():
    plan = build_take_profit_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0)
    assert plan.symbol == "2330"


def test_build_take_profit_has_stages():
    plan = build_take_profit_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0)
    assert isinstance(plan.stages, list)
    assert len(plan.stages) >= 1


def test_build_take_profit_entry_price_stage_target():
    plan = build_take_profit_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0)
    for stage in plan.stages:
        if stage.get("target_price") is not None:
            assert stage["target_price"] > 500.0


def test_build_take_profit_gain_target_type():
    plan = build_take_profit_plan("2330", TakeProfitType.GAIN_TARGET)
    assert plan.take_profit_type == TakeProfitType.GAIN_TARGET


def test_validate_take_profit_plan_returns_dict():
    plan = build_take_profit_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0)
    result = validate_take_profit_plan(plan)
    assert isinstance(result, dict)


def test_validate_take_profit_plan_pass():
    plan = build_take_profit_plan("2330", BuyPointType.A_10MA_PULLBACK, entry_price=500.0)
    result = validate_take_profit_plan(plan)
    assert result["valid"] is True
