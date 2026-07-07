"""
paper_trading/small_capital_strategy/liquidity_filter_v171.py
Liquidity filter for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.watchlist_enums_v171 import LiquidityGrade
from paper_trading.small_capital_strategy.watchlist_models_v171 import LiquidityFilterResult

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"

# Thresholds in TWD daily volume
LIQUIDITY_HIGH_THRESHOLD   = 20_000_000   # >= 20M TWD: HIGH
LIQUIDITY_MEDIUM_THRESHOLD =  5_000_000   # >= 5M TWD: MEDIUM
LIQUIDITY_LOW_THRESHOLD    =  1_000_000   # >= 1M TWD: LOW
# < 1M TWD: BLOCKED


def grade_liquidity(avg_daily_volume: float) -> LiquidityGrade:
    """Return liquidity grade from avg daily volume."""
    if avg_daily_volume >= LIQUIDITY_HIGH_THRESHOLD:
        return LiquidityGrade.HIGH
    if avg_daily_volume >= LIQUIDITY_MEDIUM_THRESHOLD:
        return LiquidityGrade.MEDIUM
    if avg_daily_volume >= LIQUIDITY_LOW_THRESHOLD:
        return LiquidityGrade.LOW
    return LiquidityGrade.BLOCKED


def score_liquidity_grade(grade: LiquidityGrade) -> float:
    """Return 0-100 score from grade."""
    mapping = {
        LiquidityGrade.HIGH:    90.0,
        LiquidityGrade.MEDIUM:  65.0,
        LiquidityGrade.LOW:     35.0,
        LiquidityGrade.BLOCKED:  0.0,
    }
    return mapping[grade]


def apply_liquidity_filter(symbol: str, avg_daily_volume: float) -> LiquidityFilterResult:
    """Apply liquidity filter. Blocked if below 1M TWD daily volume."""
    grade = grade_liquidity(avg_daily_volume)
    score = score_liquidity_grade(grade)
    passed = grade != LiquidityGrade.BLOCKED
    reason = "" if passed else f"liquidity too low: avg_vol={avg_daily_volume:.0f} < {LIQUIDITY_LOW_THRESHOLD}"
    return LiquidityFilterResult(
        symbol=symbol,
        avg_daily_volume=avg_daily_volume,
        liquidity_grade=grade,
        score=score,
        passed=passed,
        reason=reason,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def get_liquidity_thresholds() -> Dict[str, Any]:
    """Return liquidity thresholds. Deterministic."""
    return {
        "high": LIQUIDITY_HIGH_THRESHOLD,
        "medium": LIQUIDITY_MEDIUM_THRESHOLD,
        "low": LIQUIDITY_LOW_THRESHOLD,
        "blocked_below": LIQUIDITY_LOW_THRESHOLD,
    }
