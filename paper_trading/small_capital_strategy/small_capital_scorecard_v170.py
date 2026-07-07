"""
paper_trading/small_capital_strategy/small_capital_scorecard_v170.py
Scorecard for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
Score range: 0-100. Grade A=85-100, B=70-84, C=55-69, D=40-54, F=0-39, BLOCKED=safety failure.
No A+ grade.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.enums_v170 import SmallCapitalGrade
from paper_trading.small_capital_strategy.models_v170 import SmallCapitalScorecard

# Scoring weights (must sum to 100)
SCORE_WEIGHTS = {
    "risk_budget_compliance": 25,
    "position_sizing_correctness": 20,
    "buy_point_quality": 15,
    "market_regime_alignment": 15,
    "watchlist_quality": 10,
    "exit_plan_completeness": 10,
    "safety_compliance": 5,
}

assert sum(SCORE_WEIGHTS.values()) == 100, f"Weights must sum to 100, got {sum(SCORE_WEIGHTS.values())}"


def _score_to_grade(score: float, safety_blocked: bool) -> SmallCapitalGrade:
    if safety_blocked:
        return SmallCapitalGrade.BLOCKED
    if score >= 85:
        return SmallCapitalGrade.A
    if score >= 70:
        return SmallCapitalGrade.B
    if score >= 55:
        return SmallCapitalGrade.C
    if score >= 40:
        return SmallCapitalGrade.D
    return SmallCapitalGrade.F


def compute_scorecard(
    template_id: str,
    component_scores: Dict[str, float],
    safety_blocked: bool = False,
) -> SmallCapitalScorecard:
    """
    Compute scorecard from component scores (each 0.0-1.0).
    Safety failure directly sets BLOCKED.
    """
    if safety_blocked:
        return SmallCapitalScorecard(
            template_id=template_id,
            score=0.0,
            grade=SmallCapitalGrade.BLOCKED,
            risk_budget_compliance=0.0,
            position_sizing_correctness=0.0,
            buy_point_quality=0.0,
            market_regime_alignment=0.0,
            watchlist_quality=0.0,
            exit_plan_completeness=0.0,
            safety_compliance=0.0,
            safety_blocked=True,
        )

    def _get(key: str) -> float:
        v = component_scores.get(key, 0.0)
        return max(0.0, min(1.0, float(v)))

    rbc = _get("risk_budget_compliance")
    psc = _get("position_sizing_correctness")
    bpq = _get("buy_point_quality")
    mra = _get("market_regime_alignment")
    wq = _get("watchlist_quality")
    epc = _get("exit_plan_completeness")
    sc = _get("safety_compliance")

    total_score = (
        rbc * SCORE_WEIGHTS["risk_budget_compliance"]
        + psc * SCORE_WEIGHTS["position_sizing_correctness"]
        + bpq * SCORE_WEIGHTS["buy_point_quality"]
        + mra * SCORE_WEIGHTS["market_regime_alignment"]
        + wq * SCORE_WEIGHTS["watchlist_quality"]
        + epc * SCORE_WEIGHTS["exit_plan_completeness"]
        + sc * SCORE_WEIGHTS["safety_compliance"]
    )

    total_score = round(min(100.0, max(0.0, total_score)), 2)
    grade = _score_to_grade(total_score, safety_blocked=False)

    return SmallCapitalScorecard(
        template_id=template_id,
        score=total_score,
        grade=grade,
        risk_budget_compliance=round(rbc, 4),
        position_sizing_correctness=round(psc, 4),
        buy_point_quality=round(bpq, 4),
        market_regime_alignment=round(mra, 4),
        watchlist_quality=round(wq, 4),
        exit_plan_completeness=round(epc, 4),
        safety_compliance=round(sc, 4),
        safety_blocked=False,
    )


def get_scorecard_weights() -> Dict[str, int]:
    """Return a copy of the score weights."""
    return dict(SCORE_WEIGHTS)


def validate_scorecard(scorecard: SmallCapitalScorecard) -> Dict[str, Any]:
    """Validate a SmallCapitalScorecard. Returns {valid, issues}."""
    issues = []
    if not (0.0 <= scorecard.score <= 100.0):
        issues.append(f"score {scorecard.score} not in [0, 100]")
    if scorecard.grade == SmallCapitalGrade.A and scorecard.score < 85:
        issues.append(f"grade A requires score >= 85, got {scorecard.score}")
    if not scorecard.paper_only:
        issues.append("paper_only must be True")
    if not scorecard.no_real_orders:
        issues.append("no_real_orders must be True")
    return {"valid": len(issues) == 0, "issues": issues}
