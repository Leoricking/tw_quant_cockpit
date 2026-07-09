"""
paper_trading/small_capital_strategy/risk_dashboard_scorecard_v174.py
Scorecard for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskDashboardScorecardGrade,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskDashboard, RiskDashboardScorecard,
)

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"

# Scorecard weights (sum = 100)
WEIGHT_SINGLE_TRADE  = 20
WEIGHT_EXPOSURE      = 20
WEIGHT_CASH_RATIO    = 15
WEIGHT_DRAWDOWN      = 15
WEIGHT_STOP_LOSS     = 15
WEIGHT_CONCENTRATION = 10
WEIGHT_SAFETY        = 5
WEIGHTS_SUM          = 100

GRADE_A_MIN = 85.0
GRADE_B_MIN = 70.0
GRADE_C_MIN = 55.0
GRADE_D_MIN = 40.0


def _score_status(status: RiskStatus) -> float:
    """Convert RiskStatus to 0-1 score."""
    return {
        RiskStatus.PASS:     1.0,
        RiskStatus.WATCH:    0.75,
        RiskStatus.WARNING:  0.5,
        RiskStatus.DEGRADED: 0.25,
        RiskStatus.BLOCKED:  0.0,
    }.get(status, 0.0)


def compute_scorecard(dashboard: SmallAccountRiskDashboard) -> RiskDashboardScorecard:
    """Compute 0-100 risk dashboard scorecard. No A+."""
    # Hard block: any BLOCKED => grade BLOCKED
    if dashboard.overall_status == RiskStatus.BLOCKED:
        return RiskDashboardScorecard(
            total_score=0.0,
            grade=RiskDashboardScorecardGrade.BLOCKED,
            weights_sum=WEIGHTS_SUM,
        )

    single_trade_score  = _score_status(dashboard.single_trade.status) * WEIGHT_SINGLE_TRADE
    exposure_score      = _score_status(dashboard.exposure.status) * WEIGHT_EXPOSURE
    cash_ratio_score    = _score_status(dashboard.cash_ratio.status) * WEIGHT_CASH_RATIO
    drawdown_score      = _score_status(dashboard.drawdown.status) * WEIGHT_DRAWDOWN
    stop_loss_score     = _score_status(dashboard.stop_loss_coverage.status) * WEIGHT_STOP_LOSS
    concentration_score = _score_status(dashboard.concentration.status) * WEIGHT_CONCENTRATION
    safety_score        = WEIGHT_SAFETY  # Safety audit passes by construction

    total = (
        single_trade_score + exposure_score + cash_ratio_score +
        drawdown_score + stop_loss_score + concentration_score + safety_score
    )

    if total >= GRADE_A_MIN:
        grade = RiskDashboardScorecardGrade.A
    elif total >= GRADE_B_MIN:
        grade = RiskDashboardScorecardGrade.B
    elif total >= GRADE_C_MIN:
        grade = RiskDashboardScorecardGrade.C
    elif total >= GRADE_D_MIN:
        grade = RiskDashboardScorecardGrade.D
    else:
        grade = RiskDashboardScorecardGrade.F

    return RiskDashboardScorecard(
        total_score=round(total, 2),
        single_trade_score=single_trade_score,
        exposure_score=exposure_score,
        cash_ratio_score=cash_ratio_score,
        drawdown_score=drawdown_score,
        stop_loss_score=stop_loss_score,
        concentration_score=concentration_score,
        safety_score=safety_score,
        grade=grade,
        weights_sum=WEIGHTS_SUM,
    )


def get_weight_table() -> Dict[str, Any]:
    """Return scorecard weight table."""
    return {
        "single_trade_risk_compliance": WEIGHT_SINGLE_TRADE,
        "portfolio_exposure_compliance": WEIGHT_EXPOSURE,
        "cash_ratio_compliance": WEIGHT_CASH_RATIO,
        "drawdown_control": WEIGHT_DRAWDOWN,
        "stop_loss_coverage": WEIGHT_STOP_LOSS,
        "concentration_control": WEIGHT_CONCENTRATION,
        "safety_compliance": WEIGHT_SAFETY,
        "total": WEIGHTS_SUM,
    }
