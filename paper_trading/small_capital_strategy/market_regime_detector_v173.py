"""
paper_trading/small_capital_strategy/market_regime_detector_v173.py
Market regime detector for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimeDetectionStatus, RiskOffSignal, TrendSignal,
    VolatilityLevel, BreadthSignal, RegimeBlockReason, RegimeWarningReason,
)
from paper_trading.small_capital_strategy.market_regime_models_v173 import (
    MarketRegimeInput, MarketRegimeDetectionResult,
)
from paper_trading.small_capital_strategy.trend_filter_v173 import evaluate_trend_filter
from paper_trading.small_capital_strategy.volatility_filter_v173 import evaluate_volatility_filter
from paper_trading.small_capital_strategy.breadth_filter_v173 import evaluate_breadth_filter
from paper_trading.small_capital_strategy.risk_off_detector_v173 import detect_risk_off

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.market_regime_detector_v173"


def _detect_regime(
    inp: MarketRegimeInput,
    trend_signal: TrendSignal,
    vol_level: VolatilityLevel,
    breadth_signal: BreadthSignal,
    risk_off_signal: RiskOffSignal,
) -> tuple:
    """
    Determine regime from sub-filter results.
    Returns (regime, confidence, note).
    """
    # RISK_OFF: active or extreme risk-off signal
    if risk_off_signal in (RiskOffSignal.ACTIVE, RiskOffSignal.EXTREME):
        return MarketRegime.RISK_OFF, 0.90, "risk_off_active"

    # BEAR: strong down trend + weak breadth
    if trend_signal in (TrendSignal.STRONG_DOWN, TrendSignal.MILD_DOWN) and \
       breadth_signal in (BreadthSignal.WEAK, BreadthSignal.VERY_WEAK):
        return MarketRegime.BEAR, 0.85, "bear_trend_and_weak_breadth"

    # BULL: strong up or mild up + healthy breadth + controlled volatility
    if trend_signal in (TrendSignal.STRONG_UP, TrendSignal.MILD_UP) and \
       breadth_signal in (BreadthSignal.HEALTHY, BreadthSignal.MIXED) and \
       vol_level in (VolatilityLevel.LOW, VolatilityLevel.MODERATE):
        conf = 0.90 if trend_signal == TrendSignal.STRONG_UP and breadth_signal == BreadthSignal.HEALTHY else 0.75
        return MarketRegime.BULL, conf, "bull_up_trend_healthy_breadth"

    # RANGE: sideways trend or mixed breadth
    if trend_signal == TrendSignal.SIDEWAYS or breadth_signal == BreadthSignal.MIXED:
        return MarketRegime.RANGE, 0.70, "range_sideways_or_mixed"

    # Conflicting signals fall to UNKNOWN
    return MarketRegime.UNKNOWN, 0.40, "insufficient_or_conflicting"


def detect_market_regime(inp: MarketRegimeInput) -> MarketRegimeDetectionResult:
    """
    Full market regime detection pipeline. Paper only.
    Runs trend, volatility, breadth, risk_off filters then classifies regime.
    """
    trend       = evaluate_trend_filter(inp)
    volatility  = evaluate_volatility_filter(inp)
    breadth     = evaluate_breadth_filter(inp)
    risk_off    = detect_risk_off(inp)

    block_reasons: List[RegimeBlockReason] = []
    warnings: List[RegimeWarningReason]    = []

    # Insufficient data guard
    if inp.index_close <= 0:
        block_reasons.append(RegimeBlockReason.INSUFFICIENT_DATA)
        return MarketRegimeDetectionResult(
            regime=MarketRegime.UNKNOWN,
            status=RegimeDetectionStatus.INSUFFICIENT,
            confidence=0.0,
            trend=trend,
            volatility=volatility,
            breadth=breadth,
            risk_off=risk_off,
            block_reasons=block_reasons,
            warnings=warnings,
            detection_note="insufficient_data: index_close <= 0",
            schema_version=_SCHEMA,
            policy_version=_POLICY,
            source_lineage=_LINEAGE,
        )

    regime, confidence, note = _detect_regime(
        inp, trend.trend_signal, volatility.volatility_level,
        breadth.breadth_signal, risk_off.risk_off_signal,
    )

    # Warnings
    if risk_off.risk_off_signal == RiskOffSignal.WARNING:
        warnings.append(RegimeWarningReason.CONFIRMATION_NEEDED)
    if regime == MarketRegime.UNKNOWN:
        warnings.append(RegimeWarningReason.DATA_PARTIAL)
    if volatility.volatility_level == VolatilityLevel.HIGH:
        warnings.append(RegimeWarningReason.REGIME_DEGRADED)

    # Status
    if block_reasons:
        status = RegimeDetectionStatus.BLOCKED
    elif regime == MarketRegime.UNKNOWN:
        status = RegimeDetectionStatus.CONFLICTED
    elif confidence >= 0.75:
        status = RegimeDetectionStatus.DETECTED
    else:
        status = RegimeDetectionStatus.CONFLICTED

    return MarketRegimeDetectionResult(
        regime=regime,
        status=status,
        confidence=confidence,
        trend=trend,
        volatility=volatility,
        breadth=breadth,
        risk_off=risk_off,
        block_reasons=block_reasons,
        warnings=warnings,
        detection_note=note,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )
