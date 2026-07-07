"""
paper_trading/small_capital_strategy/technical_strength_filter_v171.py
Technical strength filter for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.watchlist_enums_v171 import TechnicalStrengthGrade
from paper_trading.small_capital_strategy.watchlist_models_v171 import TechnicalStrengthResult

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"


def grade_technical_strength(above_20ma: bool, above_60ma: bool, atr_pct: float) -> TechnicalStrengthGrade:
    """Grade technical strength from MA position and volatility."""
    if above_20ma and above_60ma and atr_pct <= 0.08:
        return TechnicalStrengthGrade.A
    if above_20ma and above_60ma:
        return TechnicalStrengthGrade.B
    if above_20ma and not above_60ma:
        return TechnicalStrengthGrade.C
    if not above_20ma and above_60ma and atr_pct <= 0.10:
        return TechnicalStrengthGrade.D
    if not above_20ma and not above_60ma:
        return TechnicalStrengthGrade.F
    return TechnicalStrengthGrade.D


def score_technical_grade(grade: TechnicalStrengthGrade) -> float:
    """Return 0-100 score from grade."""
    mapping = {
        TechnicalStrengthGrade.A:       90.0,
        TechnicalStrengthGrade.B:       75.0,
        TechnicalStrengthGrade.C:       55.0,
        TechnicalStrengthGrade.D:       40.0,
        TechnicalStrengthGrade.F:       20.0,
        TechnicalStrengthGrade.BLOCKED:  0.0,
    }
    return mapping[grade]


def apply_technical_strength_filter(
    symbol: str,
    above_20ma: bool,
    above_60ma: bool,
    atr_pct: float = 0.05,
) -> TechnicalStrengthResult:
    """Apply technical strength filter."""
    grade = grade_technical_strength(above_20ma, above_60ma, atr_pct)
    score = score_technical_grade(grade)
    passed = grade not in (TechnicalStrengthGrade.F, TechnicalStrengthGrade.BLOCKED)
    reason = ""
    if not passed:
        reason = f"weak technical structure: above_20ma={above_20ma}, above_60ma={above_60ma}"
    return TechnicalStrengthResult(
        symbol=symbol,
        above_20ma=above_20ma,
        above_60ma=above_60ma,
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


def get_technical_grade_scores() -> Dict[str, Any]:
    """Return technical grade scores. Deterministic."""
    return {
        "A": 90.0,
        "B": 75.0,
        "C": 55.0,
        "D": 40.0,
        "F": 20.0,
        "BLOCKED": 0.0,
    }
