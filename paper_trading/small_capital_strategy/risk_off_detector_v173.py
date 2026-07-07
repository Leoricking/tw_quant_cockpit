"""
paper_trading/small_capital_strategy/risk_off_detector_v173.py
Risk-off detector for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from paper_trading.small_capital_strategy.market_regime_enums_v173 import RiskOffSignal, BreadthSignal
from paper_trading.small_capital_strategy.market_regime_models_v173 import (
    MarketRegimeInput, RiskOffDetectionResult,
)

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.risk_off_detector_v173"

# Thresholds
VOLATILITY_SPIKE_THRESHOLD = 70.0   # volatility_score >= this = spike


def detect_risk_off(inp: MarketRegimeInput) -> RiskOffDetectionResult:
    """
    Detect risk-off condition from market inputs.
    EXTREME: index < MA240 AND volatility_spike AND risk_event_flag
    ACTIVE:  index < MA120 OR (volatility_spike AND risk_event_flag)
    WARNING: index < MA120 OR volatility_spike OR risk_event_flag OR breadth_very_weak
    NONE:    none of the above
    Paper only.
    """
    below_ma120 = inp.index_close < inp.index_ma120
    below_ma240 = inp.index_close < inp.index_ma240
    vol_spike   = inp.volatility_score >= VOLATILITY_SPIKE_THRESHOLD
    risk_event  = inp.risk_event_flag
    # breadth very weak via advance_decline_ratio < 0.5
    breadth_very_weak = inp.advance_decline_ratio < 0.5

    # Classify signal
    if below_ma240 and vol_spike and risk_event:
        signal = RiskOffSignal.EXTREME
    elif below_ma120 and (vol_spike or risk_event):
        signal = RiskOffSignal.ACTIVE
    elif below_ma120 or vol_spike or risk_event or breadth_very_weak:
        signal = RiskOffSignal.WARNING
    else:
        signal = RiskOffSignal.NONE

    parts = []
    if below_ma120:       parts.append("below_MA120")
    if below_ma240:       parts.append("below_MA240")
    if vol_spike:         parts.append("vol_spike")
    if risk_event:        parts.append("risk_event")
    if breadth_very_weak: parts.append("breadth_very_weak")
    detail = f"signal={signal.value} triggers=[{','.join(parts) or 'none'}]"

    return RiskOffDetectionResult(
        risk_off_signal=signal,
        index_below_ma120=below_ma120,
        index_below_ma240=below_ma240,
        volatility_spike=vol_spike,
        risk_event_active=risk_event,
        breadth_very_weak=breadth_very_weak,
        detail=detail,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )
