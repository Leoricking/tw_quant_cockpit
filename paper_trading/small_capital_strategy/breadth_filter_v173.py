"""
paper_trading/small_capital_strategy/breadth_filter_v173.py
Market breadth filter for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from paper_trading.small_capital_strategy.market_regime_enums_v173 import BreadthSignal
from paper_trading.small_capital_strategy.market_regime_models_v173 import (
    MarketRegimeInput, BreadthFilterResult,
)

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.breadth_filter_v173"

# Advance/decline ratio thresholds
HEALTHY_MIN   = 1.5   # ratio >= 1.5 => HEALTHY
MIXED_MIN     = 0.9   # ratio >= 0.9 => MIXED
WEAK_MIN      = 0.5   # ratio >= 0.5 => WEAK
# ratio < 0.5 => VERY_WEAK

HEALTHY_THRESHOLD = 1.2   # breadth_healthy when ratio >= this


def _classify_breadth(ratio: float) -> BreadthSignal:
    if ratio >= HEALTHY_MIN:
        return BreadthSignal.HEALTHY
    if ratio >= MIXED_MIN:
        return BreadthSignal.MIXED
    if ratio >= WEAK_MIN:
        return BreadthSignal.WEAK
    return BreadthSignal.VERY_WEAK


def evaluate_breadth_filter(inp: MarketRegimeInput) -> BreadthFilterResult:
    """Evaluate breadth filter from MarketRegimeInput. Paper only."""
    ratio   = inp.advance_decline_ratio
    signal  = _classify_breadth(ratio)
    healthy = ratio >= HEALTHY_THRESHOLD

    detail = (
        f"advance_decline_ratio={ratio:.3f} "
        f"signal={signal.value} "
        f"healthy={healthy}"
    )

    return BreadthFilterResult(
        breadth_signal=signal,
        advance_decline_ratio=ratio,
        breadth_healthy=healthy,
        detail=detail,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )
