"""
tests/test_market_regime_detector_v173.py
Tests for Market Regime Position Control market_regime_detector_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput
from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimeDetectionStatus, RegimeBlockReason,
)
from paper_trading.small_capital_strategy.market_regime_detector_v173 import detect_market_regime


def _bull_full():
    return MarketRegimeInput(
        index_close=20000.0, index_ma20=19500.0, index_ma60=18800.0,
        index_ma120=17500.0, index_ma240=16000.0, advance_decline_ratio=1.8,
        volatility_score=20.0, risk_event_flag=False, major_index_trend_score=1.0,
        institutional_market_bias=0.5,
    )


def _bear_full():
    return MarketRegimeInput(
        index_close=15000.0, index_ma20=16000.0, index_ma60=17000.0,
        index_ma120=18000.0, index_ma240=19000.0, advance_decline_ratio=0.4,
        volatility_score=60.0, risk_event_flag=False, major_index_trend_score=-1.0,
        institutional_market_bias=-0.5,
    )


def _risk_off_full():
    return MarketRegimeInput(
        index_close=14000.0, index_ma20=15000.0, index_ma60=16000.0,
        index_ma120=17000.0, index_ma240=18000.0, advance_decline_ratio=0.3,
        volatility_score=80.0, risk_event_flag=True, major_index_trend_score=-2.0,
        institutional_market_bias=-1.0,
    )


def _range_full():
    return MarketRegimeInput(
        index_close=18000.0, index_ma20=18200.0, index_ma60=18100.0,
        index_ma120=17000.0, index_ma240=15500.0, advance_decline_ratio=1.1,
        volatility_score=40.0, risk_event_flag=False, major_index_trend_score=0.0,
        institutional_market_bias=0.0,
    )


class TestDetectBull:
    def test_bull_regime_detected(self):
        result = detect_market_regime(_bull_full())
        assert result.regime == MarketRegime.BULL

    def test_bull_status_detected(self):
        result = detect_market_regime(_bull_full())
        assert result.status == RegimeDetectionStatus.DETECTED

    def test_bull_confidence_high(self):
        result = detect_market_regime(_bull_full())
        assert result.confidence >= 0.75

    def test_bull_no_block_reasons(self):
        result = detect_market_regime(_bull_full())
        assert result.block_reasons == []


class TestDetectBear:
    def test_bear_regime_detected(self):
        result = detect_market_regime(_bear_full())
        assert result.regime == MarketRegime.BEAR

    def test_bear_confidence_positive(self):
        result = detect_market_regime(_bear_full())
        assert result.confidence > 0


class TestDetectRiskOff:
    def test_risk_off_regime_detected(self):
        result = detect_market_regime(_risk_off_full())
        assert result.regime == MarketRegime.RISK_OFF

    def test_risk_off_status_detected(self):
        result = detect_market_regime(_risk_off_full())
        assert result.status == RegimeDetectionStatus.DETECTED


class TestDetectRange:
    def test_range_regime_detected(self):
        result = detect_market_regime(_range_full())
        assert result.regime in (MarketRegime.RANGE, MarketRegime.UNKNOWN)


class TestDetectUnknown:
    def test_zero_close_insufficient(self):
        result = detect_market_regime(MarketRegimeInput(index_close=0))
        assert result.status == RegimeDetectionStatus.INSUFFICIENT

    def test_zero_close_regime_unknown(self):
        result = detect_market_regime(MarketRegimeInput(index_close=0))
        assert result.regime == MarketRegime.UNKNOWN

    def test_zero_close_has_block_reason(self):
        result = detect_market_regime(MarketRegimeInput(index_close=0))
        assert RegimeBlockReason.INSUFFICIENT_DATA in result.block_reasons


class TestSubFilterResults:
    def test_contains_trend_result(self):
        result = detect_market_regime(_bull_full())
        assert result.trend is not None

    def test_contains_volatility_result(self):
        result = detect_market_regime(_bull_full())
        assert result.volatility is not None

    def test_contains_breadth_result(self):
        result = detect_market_regime(_bull_full())
        assert result.breadth is not None

    def test_contains_risk_off_result(self):
        result = detect_market_regime(_bull_full())
        assert result.risk_off is not None


class TestSafetyInvariants:
    def test_paper_only(self):
        result = detect_market_regime(_bull_full())
        assert result.paper_only is True

    def test_no_real_orders(self):
        result = detect_market_regime(_bull_full())
        assert result.no_real_orders is True

    def test_schema_version(self):
        result = detect_market_regime(_bull_full())
        assert result.schema_version == "173"

    def test_detection_note_not_empty(self):
        result = detect_market_regime(_bull_full())
        assert result.detection_note != ""
