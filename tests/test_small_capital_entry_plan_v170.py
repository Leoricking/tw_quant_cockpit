"""tests/test_small_capital_entry_plan_v170.py — entry plan tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.enums_v170 import BuyPointType
from paper_trading.small_capital_strategy.entry_plan_v170 import (
    build_entry_plan, validate_entry_plan, EntryPlanStatus,
)


def _default_input(**kwargs):
    defaults = {
        "symbol": "2330",
        "buy_point_type": BuyPointType.A_10MA_PULLBACK,
        "entry_price": 500.0,
        "add_price": None,
        "stop_loss_price": 470.0,
        "position_size_twd": 50000.0,
        "status": EntryPlanStatus.VALID,
    }
    defaults.update(kwargs)
    return defaults


def test_build_entry_plan_returns_plan():
    plan = build_entry_plan(**_default_input())
    assert plan is not None


def test_build_entry_plan_symbol():
    plan = build_entry_plan(**_default_input())
    assert plan.symbol == "2330"


def test_build_entry_plan_buy_point_type():
    plan = build_entry_plan(**_default_input())
    assert plan.buy_point_type == BuyPointType.A_10MA_PULLBACK


def test_build_entry_plan_paper_only():
    plan = build_entry_plan(**_default_input())
    assert plan.paper_only is True


def test_build_entry_plan_no_real_orders():
    plan = build_entry_plan(**_default_input())
    assert plan.no_real_orders is True


def test_build_entry_plan_entry_price():
    plan = build_entry_plan(**_default_input())
    assert plan.entry_price == 500.0


def test_build_entry_plan_position_size():
    plan = build_entry_plan(**_default_input())
    assert plan.position_size_twd == 50000.0


def test_validate_entry_plan_pass():
    plan = build_entry_plan(**_default_input())
    result = validate_entry_plan(plan)
    assert result["valid"] is True


def test_validate_entry_plan_returns_dict():
    plan = build_entry_plan(**_default_input())
    result = validate_entry_plan(plan)
    assert isinstance(result, dict)


def test_build_entry_plan_b_type():
    plan = build_entry_plan(**_default_input(buy_point_type=BuyPointType.B_PLATFORM_BREAKOUT))
    assert plan.buy_point_type == BuyPointType.B_PLATFORM_BREAKOUT


def test_build_entry_plan_c_type():
    plan = build_entry_plan(**_default_input(buy_point_type=BuyPointType.C_20MA_RECLAIM))
    assert plan.buy_point_type == BuyPointType.C_20MA_RECLAIM
