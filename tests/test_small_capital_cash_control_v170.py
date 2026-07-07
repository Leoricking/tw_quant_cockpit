"""tests/test_small_capital_cash_control_v170.py — cash control tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.enums_v170 import MarketRegime
from paper_trading.small_capital_strategy.cash_control_v170 import (
    get_cash_control_plan, validate_cash_control,
)


def test_get_cash_control_bull():
    plan = get_cash_control_plan(MarketRegime.BULL, 300000.0)
    assert plan is not None


def test_get_cash_control_bear_cash_high():
    plan = get_cash_control_plan(MarketRegime.BEAR, 300000.0)
    assert plan.min_cash_pct >= 0.49


def test_get_cash_control_bull_cash_low():
    plan = get_cash_control_plan(MarketRegime.BULL, 300000.0)
    assert plan.min_cash_pct <= 0.06


def test_get_cash_control_range():
    plan = get_cash_control_plan(MarketRegime.RANGE, 300000.0)
    assert plan.min_cash_pct >= 0.24


def test_get_cash_control_paper_only():
    plan = get_cash_control_plan(MarketRegime.BULL, 300000.0)
    assert plan.paper_only is True


def test_get_cash_control_no_real_orders():
    plan = get_cash_control_plan(MarketRegime.BULL, 300000.0)
    assert plan.no_real_orders is True


def test_validate_cash_control_bull_pass():
    plan = get_cash_control_plan(MarketRegime.BULL, 300000.0)
    result = validate_cash_control(plan, plan.min_cash_pct + 0.01)
    assert result["valid"] is True


def test_validate_cash_control_bear_pass():
    plan = get_cash_control_plan(MarketRegime.BEAR, 300000.0)
    result = validate_cash_control(plan, plan.min_cash_pct + 0.01)
    assert result["valid"] is True


def test_cash_control_regime_set():
    plan = get_cash_control_plan(MarketRegime.BULL, 300000.0)
    assert plan.regime == MarketRegime.BULL


def test_cash_control_mode_bull():
    from paper_trading.small_capital_strategy.enums_v170 import CashControlMode
    plan = get_cash_control_plan(MarketRegime.BULL, 300000.0)
    assert plan.mode == CashControlMode.BULL
