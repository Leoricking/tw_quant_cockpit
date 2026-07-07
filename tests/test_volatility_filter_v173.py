"""
tests/test_volatility_filter_v173.py
Tests for Market Regime Position Control volatility_filter_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput
from paper_trading.small_capital_strategy.market_regime_enums_v173 import VolatilityLevel
from paper_trading.small_capital_strategy.volatility_filter_v173 import (
    evaluate_volatility_filter, LOW_MAX, MODERATE_MAX, HIGH_MAX, CONTROLLED_MAX,
)


class TestEvaluateVolatilityFilter:
    def test_low_volatility_controlled(self):
        inp = MarketRegimeInput(volatility_score=10.0)
        result = evaluate_volatility_filter(inp)
        assert result.volatility_controlled is True

    def test_low_volatility_level(self):
        inp = MarketRegimeInput(volatility_score=10.0)
        result = evaluate_volatility_filter(inp)
        assert result.volatility_level == VolatilityLevel.LOW

    def test_moderate_volatility_controlled(self):
        inp = MarketRegimeInput(volatility_score=40.0)
        result = evaluate_volatility_filter(inp)
        assert result.volatility_controlled is True
        assert result.volatility_level == VolatilityLevel.MODERATE

    def test_high_volatility_not_controlled(self):
        inp = MarketRegimeInput(volatility_score=60.0)
        result = evaluate_volatility_filter(inp)
        assert result.volatility_controlled is False
        assert result.volatility_level == VolatilityLevel.HIGH

    def test_extreme_volatility(self):
        inp = MarketRegimeInput(volatility_score=80.0)
        result = evaluate_volatility_filter(inp)
        assert result.volatility_level == VolatilityLevel.EXTREME
        assert result.volatility_controlled is False

    def test_boundary_low_max(self):
        inp = MarketRegimeInput(volatility_score=LOW_MAX)
        result = evaluate_volatility_filter(inp)
        assert result.volatility_level == VolatilityLevel.LOW

    def test_boundary_controlled_max(self):
        inp = MarketRegimeInput(volatility_score=CONTROLLED_MAX)
        result = evaluate_volatility_filter(inp)
        assert result.volatility_controlled is True

    def test_paper_only(self):
        result = evaluate_volatility_filter(MarketRegimeInput(volatility_score=20.0))
        assert result.paper_only is True

    def test_no_real_orders(self):
        result = evaluate_volatility_filter(MarketRegimeInput(volatility_score=20.0))
        assert result.no_real_orders is True

    def test_detail_not_empty(self):
        result = evaluate_volatility_filter(MarketRegimeInput(volatility_score=30.0))
        assert result.detail != ""

    def test_schema_version(self):
        result = evaluate_volatility_filter(MarketRegimeInput(volatility_score=10.0))
        assert result.schema_version == "173"

    def test_score_stored_correctly(self):
        inp = MarketRegimeInput(volatility_score=42.5)
        result = evaluate_volatility_filter(inp)
        assert result.volatility_score == 42.5


class TestThresholds:
    def test_low_max_is_25(self):
        assert LOW_MAX == 25.0

    def test_moderate_max_is_50(self):
        assert MODERATE_MAX == 50.0

    def test_high_max_is_75(self):
        assert HIGH_MAX == 75.0

    def test_controlled_max_is_50(self):
        assert CONTROLLED_MAX == 50.0
