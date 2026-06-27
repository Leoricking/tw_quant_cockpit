"""
paper_trading/failure_validation/scorecard_v165.py — Failure scorecard computation v1.6.5.
[!] Research Only. No Real Orders. No Real Failure Injection. Not Investment Advice.
[!] Scores are simulation-only. No production SLA claims. RTO/RPO labelled as insufficient if unknown.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional

from paper_trading.failure_validation.enums_v165 import (
    ScorecardDimension,
    SCORECARD_WEIGHTS,
)
from paper_trading.failure_validation.models_v165 import (
    FailureInjectionResult,
    FailureScorecard,
    RecoveryValidationResult,
)

PAPER_ONLY = True
RESEARCH_ONLY = True
NO_PRODUCTION_SLA_CLAIMS = True


def compute_scorecard(
    result: FailureInjectionResult,
    vr: RecoveryValidationResult,
    scenario_seed: int = 42,
) -> FailureScorecard:
    """Compute a FailureScorecard from injection result and validation result."""
    scorecard = FailureScorecard(
        scenario_id=result.scenario_id,
        validation_id=vr.validation_id,
    )

    # Detection (15 pts): did the failure get detected?
    if result.detection_confirmed:
        scorecard.dimension_scores[ScorecardDimension.DETECTION.value] = 100
        scorecard.dimension_notes[ScorecardDimension.DETECTION.value] = "Failure detected"
    else:
        scorecard.dimension_scores[ScorecardDimension.DETECTION.value] = 0
        scorecard.dimension_notes[ScorecardDimension.DETECTION.value] = "Failure NOT detected"

    # Alerting (10 pts): was an alert generated?
    if result.alert_generated:
        scorecard.dimension_scores[ScorecardDimension.ALERTING.value] = 100
        scorecard.dimension_notes[ScorecardDimension.ALERTING.value] = "Alert generated"
    elif result.detection_confirmed:
        scorecard.dimension_scores[ScorecardDimension.ALERTING.value] = 50
        scorecard.dimension_notes[ScorecardDimension.ALERTING.value] = "Detected but no alert"
    else:
        scorecard.dimension_scores[ScorecardDimension.ALERTING.value] = 0
        scorecard.dimension_notes[ScorecardDimension.ALERTING.value] = "No alert"

    # Containment (15 pts): was the failure contained?
    if result.containment_confirmed:
        scorecard.dimension_scores[ScorecardDimension.CONTAINMENT.value] = 100
        scorecard.dimension_notes[ScorecardDimension.CONTAINMENT.value] = "Failure contained"
    else:
        scorecard.dimension_scores[ScorecardDimension.CONTAINMENT.value] = 0
        scorecard.dimension_notes[ScorecardDimension.CONTAINMENT.value] = "Failure NOT contained"

    # Recovery (20 pts): did the recovery succeed?
    from paper_trading.failure_validation.enums_v165 import RecoveryState
    if vr.final_state == RecoveryState.RECOVERED:
        scorecard.dimension_scores[ScorecardDimension.RECOVERY.value] = 100
        scorecard.dimension_notes[ScorecardDimension.RECOVERY.value] = "Recovery succeeded"
    elif vr.final_state == RecoveryState.ROLLED_BACK:
        scorecard.dimension_scores[ScorecardDimension.RECOVERY.value] = 70
        scorecard.dimension_notes[ScorecardDimension.RECOVERY.value] = "Rolled back (partial credit)"
    elif vr.final_state in (RecoveryState.CONTAINED, RecoveryState.DEGRADED):
        scorecard.dimension_scores[ScorecardDimension.RECOVERY.value] = 40
        scorecard.dimension_notes[ScorecardDimension.RECOVERY.value] = "Contained/degraded (partial)"
    else:
        scorecard.dimension_scores[ScorecardDimension.RECOVERY.value] = 0
        scorecard.dimension_notes[ScorecardDimension.RECOVERY.value] = "Recovery failed"

    # Data Integrity (15 pts): did data reconcile?
    if vr.data_reconciled:
        scorecard.dimension_scores[ScorecardDimension.DATA_INTEGRITY.value] = 100
        scorecard.dimension_notes[ScorecardDimension.DATA_INTEGRITY.value] = "Data reconciled"
    elif result.hash_matches is True:
        scorecard.dimension_scores[ScorecardDimension.DATA_INTEGRITY.value] = 80
        scorecard.dimension_notes[ScorecardDimension.DATA_INTEGRITY.value] = "Hash matches (not fully reconciled)"
    else:
        scorecard.dimension_scores[ScorecardDimension.DATA_INTEGRITY.value] = 0
        scorecard.dimension_notes[ScorecardDimension.DATA_INTEGRITY.value] = "Data NOT reconciled"

    # State Integrity (10 pts): no invalid transitions detected
    invalid_real = [t for t in vr.invalid_transitions_detected if not t.startswith("CORRECTLY_BLOCKED")]
    if not invalid_real:
        scorecard.dimension_scores[ScorecardDimension.STATE_INTEGRITY.value] = 100
        scorecard.dimension_notes[ScorecardDimension.STATE_INTEGRITY.value] = "State machine integrity OK"
    else:
        scorecard.dimension_scores[ScorecardDimension.STATE_INTEGRITY.value] = 0
        scorecard.dimension_notes[ScorecardDimension.STATE_INTEGRITY.value] = (
            f"Invalid transitions: {invalid_real[:2]}"
        )

    # Replay Integrity (5 pts): was replay verified?
    if vr.replay_verified:
        scorecard.dimension_scores[ScorecardDimension.REPLAY_INTEGRITY.value] = 100
        scorecard.dimension_notes[ScorecardDimension.REPLAY_INTEGRITY.value] = "Replay verified"
    else:
        scorecard.dimension_scores[ScorecardDimension.REPLAY_INTEGRITY.value] = 0
        scorecard.dimension_notes[ScorecardDimension.REPLAY_INTEGRITY.value] = "Replay NOT verified"

    # Idempotency (5 pts): idempotency verified?
    if vr.idempotency_verified:
        scorecard.dimension_scores[ScorecardDimension.IDEMPOTENCY.value] = 100
        scorecard.dimension_notes[ScorecardDimension.IDEMPOTENCY.value] = "Idempotency verified"
    else:
        scorecard.dimension_scores[ScorecardDimension.IDEMPOTENCY.value] = 0
        scorecard.dimension_notes[ScorecardDimension.IDEMPOTENCY.value] = "Idempotency NOT verified"

    # RTO (3 pts): met or insufficient data
    if vr.rto_met is True:
        scorecard.dimension_scores[ScorecardDimension.RTO.value] = 100
        scorecard.dimension_notes[ScorecardDimension.RTO.value] = f"RTO met: {vr.rto_actual_ms}ms"
    elif vr.rto_met is False:
        scorecard.dimension_scores[ScorecardDimension.RTO.value] = 0
        scorecard.dimension_notes[ScorecardDimension.RTO.value] = f"RTO exceeded: {vr.rto_actual_ms}ms"
    else:
        scorecard.dimension_scores[ScorecardDimension.RTO.value] = None
        scorecard.dimension_notes[ScorecardDimension.RTO.value] = "RTO: INSUFFICIENT_DATA (not labelled as 0)"

    # RPO (2 pts): met or insufficient data
    if vr.rpo_met is True:
        scorecard.dimension_scores[ScorecardDimension.RPO.value] = 100
        scorecard.dimension_notes[ScorecardDimension.RPO.value] = f"RPO met: {vr.rpo_actual_ms}ms"
    elif vr.rpo_met is False:
        scorecard.dimension_scores[ScorecardDimension.RPO.value] = 0
        scorecard.dimension_notes[ScorecardDimension.RPO.value] = f"RPO exceeded: {vr.rpo_actual_ms}ms"
    else:
        scorecard.dimension_scores[ScorecardDimension.RPO.value] = None
        scorecard.dimension_notes[ScorecardDimension.RPO.value] = "RPO: INSUFFICIENT_DATA (not labelled as 0)"

    scorecard.compute()
    return scorecard
