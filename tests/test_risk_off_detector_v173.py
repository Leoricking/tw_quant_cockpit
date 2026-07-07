"""
tests/test_risk_off_detector_v173.py
Tests for Market Regime Position Control risk_off_detector_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput
from paper_trading.small_capital_strategy.market_regime_enums_v173 import RiskOffSignal
from paper_trading.small_capital_strategy.risk_off_detector_v173 import (
    detect_risk_off, VOLATILITY_SPIKE_THRESHOLD,
)


def _safe_input():
    return MarketRegimeInput(
        index_close=20000.0, index_ma120=17000.0, index_ma240=16000.0,
        volatility_score=10.0, risk_event_flag=False, advance_decline_ratio=1.8,
    )


def _risk_off_input():
    return MarketRegimeInput(
        index_close=14000.0, index_ma120=17000.0, index_ma240=18000.0,
        volatility_score=80.0, risk_event_flag=True, advance_decline_ratio=0.3,
    )


class TestDetectRiskOff:
    def test_safe_input_is_none(self):
        result = detect_risk_off(_safe_input())
        assert result.risk_off_signal == RiskOffSignal.NONE

    def test_extreme_all_triggers(self):
        result = detect_risk_off(_risk_off_input())
        assert result.risk_off_signal == RiskOffSignal.EXTREME

    def test_active_below_ma120_plus_spike(self):
        inp = MarketRegimeInput(
            index_close=14000.0, index_ma120=17000.0, index_ma240=18000.0,
            volatility_score=80.0, risk_event_flag=False, advance_decline_ratio=1.0,
        )
        result = detect_risk_off(inp)
        assert result.risk_off_signal in (RiskOffSignal.ACTIVE, RiskOffSignal.EXTREME)

    def test_warning_just_below_ma120(self):
        inp = MarketRegimeInput(
            index_close=14000.0, index_ma120=17000.0, index_ma240=19000.0,
            volatility_score=20.0, risk_event_flag=False, advance_decline_ratio=1.2,
        )
        result = detect_risk_off(inp)
        assert result.risk_off_signal == RiskOffSignal.WARNING

    def test_vol_spike_detected(self):
        result = detect_risk_off(_risk_off_input())
        assert result.volatility_spike is True

    def test_no_spike_when_safe(self):
        result = detect_risk_off(_safe_input())
        assert result.volatility_spike is False

    def test_risk_event_detected(self):
        result = detect_risk_off(_risk_off_input())
        assert result.risk_event_active is True

    def test_no_risk_event_when_safe(self):
        result = detect_risk_off(_safe_input())
        assert result.risk_event_active is False

    def test_below_ma120_detected(self):
        result = detect_risk_off(_risk_off_input())
        assert result.index_below_ma120 is True

    def test_not_below_ma120_when_safe(self):
        result = detect_risk_off(_safe_input())
        assert result.index_below_ma120 is False

    def test_breadth_very_weak(self):
        result = detect_risk_off(_risk_off_input())
        assert result.breadth_very_weak is True

    def test_paper_only(self):
        result = detect_risk_off(_safe_input())
        assert result.paper_only is True

    def test_no_real_orders(self):
        result = detect_risk_off(_safe_input())
        assert result.no_real_orders is True

    def test_schema_version(self):
        result = detect_risk_off(_safe_input())
        assert result.schema_version == "173"

    def test_detail_not_empty(self):
        result = detect_risk_off(_safe_input())
        assert result.detail != ""


class TestThresholds:
    def test_volatility_spike_threshold_70(self):
        assert VOLATILITY_SPIKE_THRESHOLD == 70.0
