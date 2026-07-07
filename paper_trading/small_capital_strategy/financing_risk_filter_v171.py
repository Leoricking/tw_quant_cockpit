"""
paper_trading/small_capital_strategy/financing_risk_filter_v171.py
Financing risk filter for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.watchlist_enums_v171 import FinancingRiskGrade
from paper_trading.small_capital_strategy.watchlist_models_v171 import FinancingRiskResult

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"

# Financing ratio = financing shares / total shares
FINANCING_HEALTHY_MAX    = 0.10   # <= 10%: HEALTHY
FINANCING_MODERATE_MAX   = 0.20   # <= 20%: MODERATE
FINANCING_ELEVATED_MAX   = 0.30   # <= 30%: ELEVATED
# > 30%: OVERHEATED (triggers exclusion)
FINANCING_OVERHEATED_THRESHOLD = 0.30


def grade_financing_risk(financing_ratio: float) -> FinancingRiskGrade:
    """Grade financing risk from financing ratio."""
    if financing_ratio <= FINANCING_HEALTHY_MAX:
        return FinancingRiskGrade.HEALTHY
    if financing_ratio <= FINANCING_MODERATE_MAX:
        return FinancingRiskGrade.MODERATE
    if financing_ratio <= FINANCING_ELEVATED_MAX:
        return FinancingRiskGrade.ELEVATED
    return FinancingRiskGrade.OVERHEATED


def score_financing_grade(grade: FinancingRiskGrade) -> float:
    """Return 0-100 score from grade."""
    mapping = {
        FinancingRiskGrade.HEALTHY:    95.0,
        FinancingRiskGrade.MODERATE:   70.0,
        FinancingRiskGrade.ELEVATED:   40.0,
        FinancingRiskGrade.OVERHEATED:  0.0,
    }
    return mapping[grade]


def apply_financing_risk_filter(symbol: str, financing_ratio: float) -> FinancingRiskResult:
    """Apply financing risk filter. Blocked if overheated (> 30%)."""
    grade = grade_financing_risk(financing_ratio)
    score = score_financing_grade(grade)
    passed = grade != FinancingRiskGrade.OVERHEATED
    reason = "" if passed else f"financing overheated: ratio={financing_ratio:.1%} > {FINANCING_OVERHEATED_THRESHOLD:.0%}"
    return FinancingRiskResult(
        symbol=symbol,
        financing_ratio=financing_ratio,
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


def get_financing_thresholds() -> Dict[str, Any]:
    """Return financing thresholds. Deterministic."""
    return {
        "healthy_max": FINANCING_HEALTHY_MAX,
        "moderate_max": FINANCING_MODERATE_MAX,
        "elevated_max": FINANCING_ELEVATED_MAX,
        "overheated_above": FINANCING_OVERHEATED_THRESHOLD,
    }
