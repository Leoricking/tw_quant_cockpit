"""tests/test_small_capital_trade_plan_validator_v170.py — trade plan validator tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.trade_plan_validator_v170 import (
    validate_trade_plan_dict,
)
from paper_trading.small_capital_strategy.enums_v170 import BuyPointType, MarketRegime


def _valid_plan_dict(**kwargs):
    base = {
        "symbol": "2330",
        "buy_point_type": BuyPointType.A_10MA_PULLBACK.value,
        "entry_price": 500.0,
        "stop_loss_pct": 0.06,
        "position_size_twd": 50000.0,
        "regime": MarketRegime.BULL.value,
        "capital_twd": 300000.0,
        "paper_only": True,
        "no_real_orders": True,
    }
    base.update(kwargs)
    return base


def test_validate_trade_plan_dict_valid():
    result = validate_trade_plan_dict(_valid_plan_dict())
    assert result["valid"] is True


def test_validate_trade_plan_dict_returns_dict():
    result = validate_trade_plan_dict(_valid_plan_dict())
    assert isinstance(result, dict)
    assert "valid" in result
    assert "issues" in result


def test_validate_trade_plan_dict_missing_symbol():
    plan = _valid_plan_dict()
    del plan["symbol"]
    result = validate_trade_plan_dict(plan)
    assert result["valid"] is False


def test_validate_trade_plan_dict_paper_only_false_fails():
    result = validate_trade_plan_dict(_valid_plan_dict(paper_only=False))
    assert result["valid"] is False


def test_validate_trade_plan_dict_no_real_orders_false_fails():
    result = validate_trade_plan_dict(_valid_plan_dict(no_real_orders=False))
    assert result["valid"] is False


def test_validate_trade_plan_dict_issues_list_empty_on_valid():
    result = validate_trade_plan_dict(_valid_plan_dict())
    assert result["issues"] == []


def test_validate_trade_plan_dict_issues_list_non_empty_on_invalid():
    plan = _valid_plan_dict()
    del plan["symbol"]
    result = validate_trade_plan_dict(plan)
    assert len(result["issues"]) >= 1


def test_validate_trade_plan_dict_empty_symbol_fails():
    result = validate_trade_plan_dict(_valid_plan_dict(symbol=""))
    assert result["valid"] is False


def test_validate_trade_plan_dict_entry_price_present():
    result = validate_trade_plan_dict(_valid_plan_dict(entry_price=500.0))
    assert result["valid"] is True
