"""
paper_trading/small_capital_strategy/revenue_growth_filter_v171.py
Revenue growth filter for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.watchlist_enums_v171 import RevenueGrowthGrade
from paper_trading.small_capital_strategy.watchlist_models_v171 import RevenueGrowthFilterResult

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"

# Thresholds as decimal fractions
REVENUE_STRONG_THRESHOLD   = 0.15   # >= 15% YoY: STRONG
REVENUE_MODERATE_THRESHOLD = 0.05   # >= 5% YoY: MODERATE
REVENUE_WEAK_THRESHOLD     = 0.0    # >= 0%: WEAK
# < 0%: NEGATIVE


def grade_revenue_growth(revenue_growth_pct: float) -> RevenueGrowthGrade:
    """Return revenue growth grade."""
    if revenue_growth_pct >= REVENUE_STRONG_THRESHOLD:
        return RevenueGrowthGrade.STRONG
    if revenue_growth_pct >= REVENUE_MODERATE_THRESHOLD:
        return RevenueGrowthGrade.MODERATE
    if revenue_growth_pct >= REVENUE_WEAK_THRESHOLD:
        return RevenueGrowthGrade.WEAK
    return RevenueGrowthGrade.NEGATIVE


def score_revenue_grade(grade: RevenueGrowthGrade) -> float:
    """Return 0-100 score from grade."""
    mapping = {
        RevenueGrowthGrade.STRONG:   90.0,
        RevenueGrowthGrade.MODERATE: 65.0,
        RevenueGrowthGrade.WEAK:     40.0,
        RevenueGrowthGrade.NEGATIVE: 15.0,
        RevenueGrowthGrade.UNKNOWN:  30.0,
    }
    return mapping[grade]


def apply_revenue_growth_filter(symbol: str, revenue_growth_pct: float) -> RevenueGrowthFilterResult:
    """Apply revenue growth filter."""
    grade = grade_revenue_growth(revenue_growth_pct)
    score = score_revenue_grade(grade)
    passed = grade not in (RevenueGrowthGrade.NEGATIVE,)
    reason = "" if passed else f"negative revenue growth: {revenue_growth_pct:.1%}"
    return RevenueGrowthFilterResult(
        symbol=symbol,
        revenue_growth_pct=revenue_growth_pct,
        grade=grade,
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


def get_revenue_thresholds() -> Dict[str, Any]:
    """Return revenue growth thresholds. Deterministic."""
    return {
        "strong": REVENUE_STRONG_THRESHOLD,
        "moderate": REVENUE_MODERATE_THRESHOLD,
        "weak": REVENUE_WEAK_THRESHOLD,
    }
