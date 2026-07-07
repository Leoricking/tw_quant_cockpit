"""
paper_trading/small_capital_strategy/market_regime_scorecard_v173.py
Scorecard for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, Any

from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimeDetectionStatus, RegimeScorecardGrade, RegimeBlockReason,
)
from paper_trading.small_capital_strategy.market_regime_models_v173 import (
    MarketRegimeDetectionResult, CashRatioPlan, ExposureControlPlan,
    CandidateRegimePermission, ABCRegimePermission, MarketRegimeScorecard,
)

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.market_regime_scorecard_v173"

# Scorecard weights (sum = 100)
WEIGHT_REGIME_DETECTION   = 25
WEIGHT_CASH_RATIO         = 20
WEIGHT_EXPOSURE_CONTROL   = 20
WEIGHT_CANDIDATE_PERM     = 15
WEIGHT_ABC_COMPATIBILITY  = 10
WEIGHT_SAFETY             = 10

WEIGHTS_SUM = (
    WEIGHT_REGIME_DETECTION + WEIGHT_CASH_RATIO + WEIGHT_EXPOSURE_CONTROL
    + WEIGHT_CANDIDATE_PERM + WEIGHT_ABC_COMPATIBILITY + WEIGHT_SAFETY
)  # = 100

# Grade thresholds (no A+)
GRADE_A_MIN = 85.0
GRADE_B_MIN = 70.0
GRADE_C_MIN = 55.0
GRADE_D_MIN = 40.0
# < 40 => F, BLOCKED is special


def _grade_score(score: float, blocked: bool) -> RegimeScorecardGrade:
    if blocked:
        return RegimeScorecardGrade.BLOCKED
    if score >= GRADE_A_MIN:
        return RegimeScorecardGrade.A
    if score >= GRADE_B_MIN:
        return RegimeScorecardGrade.B
    if score >= GRADE_C_MIN:
        return RegimeScorecardGrade.C
    if score >= GRADE_D_MIN:
        return RegimeScorecardGrade.D
    return RegimeScorecardGrade.F


def _score_regime_detection(detection: MarketRegimeDetectionResult) -> float:
    """Score regime detection quality 0–100."""
    if detection.status == RegimeDetectionStatus.BLOCKED:
        return 0.0
    if detection.status == RegimeDetectionStatus.INSUFFICIENT:
        return 20.0
    if detection.status == RegimeDetectionStatus.CONFLICTED:
        return 50.0
    # DETECTED — scale by confidence
    return min(100.0, detection.confidence * 100)


def _score_cash_ratio(cash_plan: CashRatioPlan) -> float:
    """Score cash ratio compliance 0–100."""
    if not cash_plan.allocation_valid:
        return 0.0
    if cash_plan.block_reasons:
        return 20.0
    if cash_plan.total_pct == 100:
        return 100.0
    return 50.0


def _score_exposure_control(exposure_plan: ExposureControlPlan) -> float:
    """Score exposure control 0–100."""
    if exposure_plan.margin_allowed or exposure_plan.leverage_allowed:
        return 0.0
    if exposure_plan.block_reasons:
        return 30.0
    return 100.0


def _score_candidate_permission(candidate_perm: CandidateRegimePermission) -> float:
    """Score candidate permission 0–100."""
    from paper_trading.small_capital_strategy.market_regime_enums_v173 import RegimePermissionStatus
    p = candidate_perm.permission
    if p == RegimePermissionStatus.BLOCKED:
        return 0.0
    if p == RegimePermissionStatus.DEGRADED:
        return 30.0
    if p == RegimePermissionStatus.LIMITED:
        return 50.0
    if p == RegimePermissionStatus.SELECTIVE:
        return 75.0
    return 100.0  # ALLOWED


def _score_abc_compatibility(abc_perm: ABCRegimePermission) -> float:
    """Score ABC execution compatibility 0–100."""
    allowed_count = sum([abc_perm.a_allowed, abc_perm.b_allowed, abc_perm.c_allowed])
    return round(allowed_count / 3.0 * 100, 1)


def _score_safety(regime: MarketRegime, detection: MarketRegimeDetectionResult) -> float:
    """Score safety 0–100. Always returns 100 for paper-only system."""
    return 100.0


def build_regime_scorecard(
    regime: MarketRegime,
    detection: MarketRegimeDetectionResult,
    cash_plan: CashRatioPlan,
    exposure_plan: ExposureControlPlan,
    candidate_perm: CandidateRegimePermission,
    abc_perm: ABCRegimePermission,
) -> MarketRegimeScorecard:
    """
    Build full regime scorecard from all component results. Paper only.
    Weights sum to 100. Grade: A(85+), B(70+), C(55+), D(40+), F(<40), BLOCKED.
    """
    s_detect  = _score_regime_detection(detection)
    s_cash    = _score_cash_ratio(cash_plan)
    s_exposure = _score_exposure_control(exposure_plan)
    s_cand    = _score_candidate_permission(candidate_perm)
    s_abc     = _score_abc_compatibility(abc_perm)
    s_safety  = _score_safety(regime, detection)

    total = (
        s_detect  * WEIGHT_REGIME_DETECTION / 100
        + s_cash    * WEIGHT_CASH_RATIO / 100
        + s_exposure * WEIGHT_EXPOSURE_CONTROL / 100
        + s_cand   * WEIGHT_CANDIDATE_PERM / 100
        + s_abc    * WEIGHT_ABC_COMPATIBILITY / 100
        + s_safety * WEIGHT_SAFETY / 100
    )
    total = round(total, 2)

    blocked = detection.status == RegimeDetectionStatus.BLOCKED
    grade   = _grade_score(total, blocked)

    return MarketRegimeScorecard(
        regime=regime,
        total_score=total,
        regime_detection_score=round(s_detect, 2),
        cash_ratio_score=round(s_cash, 2),
        exposure_control_score=round(s_exposure, 2),
        candidate_permission_score=round(s_cand, 2),
        abc_compatibility_score=round(s_abc, 2),
        safety_score=round(s_safety, 2),
        grade=grade,
        weights_sum=WEIGHTS_SUM,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
    )


def get_weight_table() -> Dict[str, int]:
    """Return scorecard weight table."""
    return {
        "regime_detection": WEIGHT_REGIME_DETECTION,
        "cash_ratio": WEIGHT_CASH_RATIO,
        "exposure_control": WEIGHT_EXPOSURE_CONTROL,
        "candidate_permission": WEIGHT_CANDIDATE_PERM,
        "abc_compatibility": WEIGHT_ABC_COMPATIBILITY,
        "safety": WEIGHT_SAFETY,
        "total": WEIGHTS_SUM,
    }
