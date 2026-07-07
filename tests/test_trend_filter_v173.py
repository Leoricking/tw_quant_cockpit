"""
tests/test_trend_filter_v173.py
Tests for Market Regime Position Control trend_filter_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput
from paper_trading.small_capital_strategy.market_regime_enums_v173 import TrendSignal
from paper_trading.small_capital_strategy.trend_filter_v173 import (
    evaluate_trend_filter, _compute_trend_score, _classify_trend,
    STRONG_UP_MIN_SCORE, MILD_UP_MIN_SCORE,
)


def _bull_input():
    return MarketRegimeInput(
        index_close=20000.0, index_ma20=19500.0, index_ma60=18800.0,
        index_ma120=17500.0, index_ma240=16000.0, major_index_trend_score=1.0,
        institutional_market_bias=0.5,
    )


def _bear_input():
    return MarketRegimeInput(
        index_close=15000.0, index_ma20=16000.0, index_ma60=17000.0,
        index_ma120=18000.0, index_ma240=19000.0, major_index_trend_score=-1.0,
        institutional_market_bias=-0.5,
    )


class TestEvaluateTrendFilter:
    def test_bull_strong_up_signal(self):
        result = evaluate_trend_filter(_bull_input())
        assert result.trend_signal in (TrendSignal.STRONG_UP, TrendSignal.MILD_UP)

    def test_bull_above_ma20(self):
        result = evaluate_trend_filter(_bull_input())
        assert result.index_above_ma20 is True

    def test_bull_above_ma60(self):
        result = evaluate_trend_filter(_bull_input())
        assert result.index_above_ma60 is True

    def test_bull_ma20_above_ma60(self):
        result = evaluate_trend_filter(_bull_input())
        assert result.ma20_above_ma60 is True

    def test_bull_ma60_rising(self):
        result = evaluate_trend_filter(_bull_input())
        assert result.ma60_rising is True

    def test_bull_positive_score(self):
        result = evaluate_trend_filter(_bull_input())
        assert result.trend_score > 0

    def test_bear_not_above_ma20(self):
        result = evaluate_trend_filter(_bear_input())
        assert result.index_above_ma20 is False

    def test_bear_not_above_ma60(self):
        result = evaluate_trend_filter(_bear_input())
        assert result.index_above_ma60 is False

    def test_bear_negative_score(self):
        result = evaluate_trend_filter(_bear_input())
        assert result.trend_score < 0

    def test_result_paper_only(self):
        result = evaluate_trend_filter(_bull_input())
        assert result.paper_only is True

    def test_result_no_real_orders(self):
        result = evaluate_trend_filter(_bull_input())
        assert result.no_real_orders is True

    def test_detail_not_empty(self):
        result = evaluate_trend_filter(_bull_input())
        assert result.detail != ""

    def test_schema_version(self):
        result = evaluate_trend_filter(_bull_input())
        assert result.schema_version == "173"

    def test_sideways_input(self):
        inp = MarketRegimeInput(
            index_close=18000.0, index_ma20=18200.0, index_ma60=18100.0,
            major_index_trend_score=0.0,
        )
        result = evaluate_trend_filter(inp)
        assert result.trend_signal in (TrendSignal.SIDEWAYS, TrendSignal.MILD_DOWN, TrendSignal.MILD_UP)


class TestComputeTrendScore:
    def test_bull_score_positive(self):
        score = _compute_trend_score(_bull_input())
        assert score > 0

    def test_bear_score_negative(self):
        score = _compute_trend_score(_bear_input())
        assert score < 0

    def test_score_is_float(self):
        score = _compute_trend_score(_bull_input())
        assert isinstance(score, float)


class TestClassifyTrend:
    def test_strong_up_threshold(self):
        assert _classify_trend(float(STRONG_UP_MIN_SCORE)) == TrendSignal.STRONG_UP

    def test_mild_up_threshold(self):
        assert _classify_trend(float(MILD_UP_MIN_SCORE)) == TrendSignal.MILD_UP

    def test_strong_down_negative(self):
        assert _classify_trend(-3.0) == TrendSignal.STRONG_DOWN

    def test_sideways_zero(self):
        assert _classify_trend(0.0) == TrendSignal.SIDEWAYS
