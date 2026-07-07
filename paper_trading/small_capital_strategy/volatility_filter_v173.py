"""
paper_trading/small_capital_strategy/volatility_filter_v173.py
Volatility filter for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from paper_trading.small_capital_strategy.market_regime_enums_v173 import VolatilityLevel
from paper_trading.small_capital_strategy.market_regime_models_v173 import (
    MarketRegimeInput, VolatilityFilterResult,
)

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.volatility_filter_v173"

# Thresholds (volatility_score 0–100)
LOW_MAX      = 25.0
MODERATE_MAX = 50.0
HIGH_MAX     = 75.0
# > HIGH_MAX => EXTREME

CONTROLLED_MAX = 50.0   # volatility_score <= this is "controlled"


def _classify_volatility(score: float) -> VolatilityLevel:
    if score <= LOW_MAX:
        return VolatilityLevel.LOW
    if score <= MODERATE_MAX:
        return VolatilityLevel.MODERATE
    if score <= HIGH_MAX:
        return VolatilityLevel.HIGH
    return VolatilityLevel.EXTREME


def evaluate_volatility_filter(inp: MarketRegimeInput) -> VolatilityFilterResult:
    """Evaluate volatility filter from MarketRegimeInput. Paper only."""
    score = inp.volatility_score
    level = _classify_volatility(score)
    controlled = score <= CONTROLLED_MAX

    detail = (
        f"volatility_score={score:.2f} "
        f"level={level.value} "
        f"controlled={controlled}"
    )

    return VolatilityFilterResult(
        volatility_level=level,
        volatility_score=score,
        volatility_controlled=controlled,
        detail=detail,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )
