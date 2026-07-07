"""tests/test_small_capital_market_regime_v170.py — market regime filter tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.enums_v170 import MarketRegime
from paper_trading.small_capital_strategy.market_regime_filter_v170 import (
    get_regime_control, is_trade_allowed_in_regime, REGIME_CONTROL,
)


def test_regime_control_has_bull():
    assert MarketRegime.BULL in REGIME_CONTROL


def test_regime_control_has_bear():
    assert MarketRegime.BEAR in REGIME_CONTROL


def test_regime_control_has_range():
    assert MarketRegime.RANGE in REGIME_CONTROL


def test_regime_control_has_risk_off():
    assert MarketRegime.RISK_OFF in REGIME_CONTROL


def test_regime_control_has_unknown():
    assert MarketRegime.UNKNOWN in REGIME_CONTROL


def test_bull_max_invested_95pct():
    result = get_regime_control(MarketRegime.BULL)
    assert result.max_invested_pct >= 0.94


def test_bull_cash_min_5pct():
    result = get_regime_control(MarketRegime.BULL)
    assert result.cash_min_pct <= 0.06


def test_bull_short_term_allowed():
    result = get_regime_control(MarketRegime.BULL)
    assert result.short_term_training_allowed is True


def test_bear_max_invested_50pct():
    result = get_regime_control(MarketRegime.BEAR)
    assert result.max_invested_pct <= 0.51


def test_bear_cash_min_50pct():
    result = get_regime_control(MarketRegime.BEAR)
    assert result.cash_min_pct >= 0.49


def test_bear_short_term_not_allowed():
    result = get_regime_control(MarketRegime.BEAR)
    assert result.short_term_training_allowed is False


def test_range_max_invested_75pct():
    result = get_regime_control(MarketRegime.RANGE)
    assert result.max_invested_pct <= 0.76


def test_range_cash_min_25pct():
    result = get_regime_control(MarketRegime.RANGE)
    assert result.cash_min_pct >= 0.24


def test_range_short_term_allowed():
    result = get_regime_control(MarketRegime.RANGE)
    assert result.short_term_training_allowed is True


def test_risk_off_same_as_bear():
    result = get_regime_control(MarketRegime.RISK_OFF)
    assert result.cash_min_pct >= 0.49
    assert result.short_term_training_allowed is False


def test_unknown_max_invested_60pct():
    result = get_regime_control(MarketRegime.UNKNOWN)
    assert result.max_invested_pct <= 0.61


def test_unknown_short_term_not_allowed():
    result = get_regime_control(MarketRegime.UNKNOWN)
    assert result.short_term_training_allowed is False


def test_trade_allowed_in_bull():
    assert is_trade_allowed_in_regime(MarketRegime.BULL) is True


def test_trade_allowed_in_range():
    assert is_trade_allowed_in_regime(MarketRegime.RANGE) is True


def test_trade_allowed_in_bear():
    result = is_trade_allowed_in_regime(MarketRegime.BEAR, is_short_term=False)
    assert isinstance(result, bool)


def test_short_term_not_allowed_in_bear():
    result = is_trade_allowed_in_regime(MarketRegime.BEAR, is_short_term=True)
    assert result is False


def test_regime_result_paper_only():
    result = get_regime_control(MarketRegime.BULL)
    assert result.paper_only is True
