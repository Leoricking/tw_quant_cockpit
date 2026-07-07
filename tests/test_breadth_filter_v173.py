"""
tests/test_breadth_filter_v173.py
Tests for Market Regime Position Control breadth_filter_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput
from paper_trading.small_capital_strategy.market_regime_enums_v173 import BreadthSignal
from paper_trading.small_capital_strategy.breadth_filter_v173 import (
    evaluate_breadth_filter, HEALTHY_MIN, MIXED_MIN, WEAK_MIN, HEALTHY_THRESHOLD,
)


class TestEvaluateBreadthFilter:
    def test_healthy_breadth_above_threshold(self):
        inp = MarketRegimeInput(advance_decline_ratio=1.8)
        result = evaluate_breadth_filter(inp)
        assert result.breadth_signal == BreadthSignal.HEALTHY

    def test_healthy_breadth_flag(self):
        inp = MarketRegimeInput(advance_decline_ratio=1.8)
        result = evaluate_breadth_filter(inp)
        assert result.breadth_healthy is True

    def test_mixed_breadth(self):
        inp = MarketRegimeInput(advance_decline_ratio=1.1)
        result = evaluate_breadth_filter(inp)
        assert result.breadth_signal in (BreadthSignal.MIXED, BreadthSignal.HEALTHY)

    def test_weak_breadth(self):
        inp = MarketRegimeInput(advance_decline_ratio=0.6)
        result = evaluate_breadth_filter(inp)
        assert result.breadth_signal == BreadthSignal.WEAK

    def test_very_weak_breadth(self):
        inp = MarketRegimeInput(advance_decline_ratio=0.3)
        result = evaluate_breadth_filter(inp)
        assert result.breadth_signal == BreadthSignal.VERY_WEAK

    def test_very_weak_not_healthy(self):
        inp = MarketRegimeInput(advance_decline_ratio=0.3)
        result = evaluate_breadth_filter(inp)
        assert result.breadth_healthy is False

    def test_adr_stored(self):
        inp = MarketRegimeInput(advance_decline_ratio=1.5)
        result = evaluate_breadth_filter(inp)
        assert result.advance_decline_ratio == 1.5

    def test_paper_only(self):
        result = evaluate_breadth_filter(MarketRegimeInput(advance_decline_ratio=1.8))
        assert result.paper_only is True

    def test_no_real_orders(self):
        result = evaluate_breadth_filter(MarketRegimeInput(advance_decline_ratio=1.8))
        assert result.no_real_orders is True

    def test_detail_not_empty(self):
        result = evaluate_breadth_filter(MarketRegimeInput(advance_decline_ratio=1.2))
        assert result.detail != ""

    def test_schema_version(self):
        result = evaluate_breadth_filter(MarketRegimeInput(advance_decline_ratio=1.0))
        assert result.schema_version == "173"


class TestThresholds:
    def test_healthy_min_is_1_5(self):
        assert HEALTHY_MIN == 1.5

    def test_mixed_min_is_0_9(self):
        assert MIXED_MIN == 0.9

    def test_weak_min_is_0_5(self):
        assert WEAK_MIN == 0.5

    def test_healthy_threshold_is_1_2(self):
        assert HEALTHY_THRESHOLD == 1.2
