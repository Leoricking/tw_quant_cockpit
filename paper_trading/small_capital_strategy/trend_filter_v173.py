"""
paper_trading/small_capital_strategy/trend_filter_v173.py
Trend filter for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from paper_trading.small_capital_strategy.market_regime_enums_v173 import TrendSignal
from paper_trading.small_capital_strategy.market_regime_models_v173 import (
    MarketRegimeInput, TrendFilterResult,
)

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.trend_filter_v173"

# Thresholds
STRONG_UP_MIN_SCORE   = 3
MILD_UP_MIN_SCORE     = 2
SIDEWAYS_MIN_SCORE    = 0
MILD_DOWN_MAX_SCORE   = -1
STRONG_DOWN_MAX_SCORE = -2


def _compute_trend_score(inp: MarketRegimeInput) -> float:
    """
    Score trend from -4 to +4 based on MA relationships.
    +1 per condition: above MA20, above MA60, MA20>MA60, MA60 rising (via major_index_trend_score>0)
    Positive institutional bias adds 0.5.
    """
    score = 0.0
    if inp.index_close > inp.index_ma20:
        score += 1.0
    if inp.index_close > inp.index_ma60:
        score += 1.0
    if inp.index_ma20 > inp.index_ma60:
        score += 1.0
    if inp.major_index_trend_score > 0:
        score += 1.0
    if inp.institutional_market_bias > 0:
        score += 0.5
    if inp.index_close < inp.index_ma20:
        score -= 0.5
    if inp.index_close < inp.index_ma60:
        score -= 0.5
    if inp.index_ma20 < inp.index_ma60:
        score -= 0.5
    if inp.major_index_trend_score < 0:
        score -= 0.5
    return round(score, 2)


def _classify_trend(score: float) -> TrendSignal:
    if score >= STRONG_UP_MIN_SCORE:
        return TrendSignal.STRONG_UP
    if score >= MILD_UP_MIN_SCORE:
        return TrendSignal.MILD_UP
    if score > MILD_DOWN_MAX_SCORE:
        return TrendSignal.SIDEWAYS
    if score > STRONG_DOWN_MAX_SCORE:
        return TrendSignal.MILD_DOWN
    return TrendSignal.STRONG_DOWN


def evaluate_trend_filter(inp: MarketRegimeInput) -> TrendFilterResult:
    """Evaluate trend filter from MarketRegimeInput. Paper only."""
    score   = _compute_trend_score(inp)
    signal  = _classify_trend(score)
    above20 = inp.index_close > inp.index_ma20
    above60 = inp.index_close > inp.index_ma60
    ma20_above_ma60 = inp.index_ma20 > inp.index_ma60
    ma60_rising = inp.major_index_trend_score > 0

    detail_parts = []
    if above20:
        detail_parts.append("above_MA20")
    if above60:
        detail_parts.append("above_MA60")
    if ma20_above_ma60:
        detail_parts.append("MA20>MA60")
    if ma60_rising:
        detail_parts.append("MA60_rising")
    detail = f"trend_score={score:.2f} signals=[{','.join(detail_parts)}]"

    return TrendFilterResult(
        trend_signal=signal,
        index_above_ma20=above20,
        index_above_ma60=above60,
        ma20_above_ma60=ma20_above_ma60,
        ma60_rising=ma60_rising,
        trend_score=score,
        detail=detail,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )
