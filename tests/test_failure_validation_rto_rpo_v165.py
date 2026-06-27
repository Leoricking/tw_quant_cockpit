"""
tests/test_failure_validation_rto_rpo_v165.py — RTO/RPO & Scorecard tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
from decimal import Decimal

import pytest

from paper_trading.failure_validation.enums_v165 import (
    RecoveryState,
    ScorecardDimension,
    SCORECARD_WEIGHTS,
)
from paper_trading.failure_validation.models_v165 import (
    FailureInjectionResult,
    FailureScorecard,
    RecoveryValidationResult,
)
from paper_trading.failure_validation.rto_rpo_v165 import (
    NO_PRODUCTION_SLA_CLAIMS,
    PAPER_ONLY,
    RESEARCH_ONLY,
    RTORPOMeasurement,
    UNKNOWN_IS_NOT_ZERO,
    simulate_rto_rpo,
)
from paper_trading.failure_validation.scorecard_v165 import (
    NO_PRODUCTION_SLA_CLAIMS as SC_NO_PROD,
    PAPER_ONLY as SC_PAPER_ONLY,
    RESEARCH_ONLY as SC_RESEARCH_ONLY,
    compute_scorecard,
)


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestRTORPOSafetyFlags:
    def test_paper_only_true(self):
        assert PAPER_ONLY is True

    def test_research_only_true(self):
        assert RESEARCH_ONLY is True

    def test_no_production_sla_claims(self):
        assert NO_PRODUCTION_SLA_CLAIMS is True

    def test_unknown_is_not_zero(self):
        assert UNKNOWN_IS_NOT_ZERO is True

    def test_scorecard_paper_only(self):
        assert SC_PAPER_ONLY is True

    def test_scorecard_research_only(self):
        assert SC_RESEARCH_ONLY is True

    def test_scorecard_no_production_sla_claims(self):
        assert SC_NO_PROD is True


# ---------------------------------------------------------------------------
# RTORPOMeasurement
# ---------------------------------------------------------------------------

class TestRTORPOMeasurement:
    def test_no_data_labels_insufficient(self):
        m = RTORPOMeasurement(scenario_id="s1")
        assert m.rto_label == "INSUFFICIENT_DATA"
        assert m.rpo_label == "INSUFFICIENT_DATA"

    def test_actual_set_no_budget_label(self):
        m = RTORPOMeasurement(
            scenario_id="s1",
            rto_actual_ms=Decimal("1000"),
        )
        assert m.rto_label == "NO_BUDGET_SET"

    def test_rto_met_label(self):
        m = RTORPOMeasurement(
            scenario_id="s1",
            rto_budget_ms=Decimal("5000"),
            rto_actual_ms=Decimal("3000"),
        )
        assert m.rto_label == "MET"

    def test_rto_exceeded_label(self):
        m = RTORPOMeasurement(
            scenario_id="s1",
            rto_budget_ms=Decimal("5000"),
            rto_actual_ms=Decimal("7000"),
        )
        assert m.rto_label == "EXCEEDED"

    def test_rpo_met_label(self):
        m = RTORPOMeasurement(
            scenario_id="s1",
            rpo_budget_ms=Decimal("500"),
            rpo_actual_ms=Decimal("200"),
        )
        assert m.rpo_label == "MET"

    def test_rpo_exceeded_label(self):
        m = RTORPOMeasurement(
            scenario_id="s1",
            rpo_budget_ms=Decimal("200"),
            rpo_actual_ms=Decimal("400"),
        )
        assert m.rpo_label == "EXCEEDED"

    def test_as_dict_has_required_keys(self):
        m = RTORPOMeasurement(scenario_id="s1")
        d = m.as_dict()
        assert "measurement_id" in d
        assert "scenario_id" in d
        assert "rto_label" in d
        assert "rpo_label" in d
        assert "no_production_sla_claims" in d

    def test_as_dict_no_production_sla_claims_true(self):
        m = RTORPOMeasurement(scenario_id="s1")
        assert m.as_dict()["no_production_sla_claims"] is True

    def test_measurement_has_uuid_id(self):
        m = RTORPOMeasurement(scenario_id="s1")
        assert len(m.measurement_id) == 36


# ---------------------------------------------------------------------------
# simulate_rto_rpo
# ---------------------------------------------------------------------------

class TestSimulateRTORPO:
    def test_returns_measurement(self):
        m = simulate_rto_rpo("s1", Decimal("5000"), Decimal("1000"), seed=42)
        assert isinstance(m, RTORPOMeasurement)

    def test_actual_rto_set(self):
        m = simulate_rto_rpo("s1", Decimal("5000"), Decimal("1000"), seed=42)
        assert m.rto_actual_ms is not None

    def test_actual_rpo_set(self):
        m = simulate_rto_rpo("s1", Decimal("5000"), Decimal("1000"), seed=42)
        assert m.rpo_actual_ms is not None

    def test_label_is_met_or_exceeded(self):
        m = simulate_rto_rpo("s1", Decimal("5000"), Decimal("1000"), seed=42)
        assert m.rto_label in {"MET", "EXCEEDED"}
        assert m.rpo_label in {"MET", "EXCEEDED"}

    def test_scenario_id_preserved(self):
        m = simulate_rto_rpo("my_scenario", Decimal("3000"), Decimal("500"), seed=1)
        assert m.scenario_id == "my_scenario"

    def test_deterministic_same_seed(self):
        m1 = simulate_rto_rpo("s", Decimal("5000"), Decimal("1000"), seed=42)
        m2 = simulate_rto_rpo("s", Decimal("5000"), Decimal("1000"), seed=42)
        assert m1.rto_actual_ms == m2.rto_actual_ms
        assert m1.rpo_actual_ms == m2.rpo_actual_ms


# ---------------------------------------------------------------------------
# compute_scorecard
# ---------------------------------------------------------------------------

def _full_result(detected=True, alert=True, contained=True, hash_matches=False):
    from paper_trading.failure_validation.enums_v165 import InjectionStatus
    r = FailureInjectionResult()
    r.detection_confirmed = detected
    r.alert_generated = alert
    r.containment_confirmed = contained
    r.hash_matches = hash_matches
    r.status = InjectionStatus.CONTAINED if contained else InjectionStatus.DETECTED
    return r


def _full_vr(final_state=RecoveryState.RECOVERED, data_reconciled=True,
             replay_verified=True, idempotency_verified=True,
             rto_met=True, rpo_met=True):
    vr = RecoveryValidationResult()
    vr.final_state = final_state
    vr.data_reconciled = data_reconciled
    vr.replay_verified = replay_verified
    vr.idempotency_verified = idempotency_verified
    vr.rto_met = rto_met
    vr.rpo_met = rpo_met
    return vr


class TestComputeScorecard:
    def test_perfect_score_all_100(self):
        result = _full_result()
        vr = _full_vr()
        sc = compute_scorecard(result, vr)
        assert sc.total_score == 100

    def test_no_detection_reduces_score(self):
        result = _full_result(detected=False, alert=False, contained=False)
        vr = _full_vr(final_state=RecoveryState.FAILED, data_reconciled=False,
                      replay_verified=False, idempotency_verified=False,
                      rto_met=None, rpo_met=None)
        sc = compute_scorecard(result, vr)
        assert sc.total_score < 100

    def test_detection_score_set(self):
        result = _full_result(detected=True)
        vr = _full_vr()
        sc = compute_scorecard(result, vr)
        assert sc.dimension_scores[ScorecardDimension.DETECTION.value] == 100

    def test_no_detection_score_zero(self):
        result = _full_result(detected=False, alert=False, contained=False)
        vr = _full_vr(final_state=RecoveryState.FAILED, data_reconciled=False,
                      replay_verified=False, idempotency_verified=False)
        sc = compute_scorecard(result, vr)
        assert sc.dimension_scores[ScorecardDimension.DETECTION.value] == 0

    def test_recovery_score_100_when_recovered(self):
        result = _full_result()
        vr = _full_vr(final_state=RecoveryState.RECOVERED)
        sc = compute_scorecard(result, vr)
        assert sc.dimension_scores[ScorecardDimension.RECOVERY.value] == 100

    def test_recovery_score_70_when_rolled_back(self):
        result = _full_result()
        vr = _full_vr(final_state=RecoveryState.ROLLED_BACK)
        sc = compute_scorecard(result, vr)
        assert sc.dimension_scores[ScorecardDimension.RECOVERY.value] == 70

    def test_recovery_score_40_when_degraded(self):
        result = _full_result()
        vr = _full_vr(final_state=RecoveryState.DEGRADED)
        sc = compute_scorecard(result, vr)
        assert sc.dimension_scores[ScorecardDimension.RECOVERY.value] == 40

    def test_scorecard_compute_called_sets_total(self):
        result = _full_result()
        vr = _full_vr()
        sc = compute_scorecard(result, vr)
        assert sc.total_score is not None

    def test_rto_none_gets_none_score(self):
        result = _full_result()
        vr = _full_vr(rto_met=None)
        sc = compute_scorecard(result, vr)
        assert sc.dimension_scores[ScorecardDimension.RTO.value] is None

    def test_state_integrity_100_no_invalid_transitions(self):
        result = _full_result()
        vr = _full_vr()
        vr.invalid_transitions_detected = []
        sc = compute_scorecard(result, vr)
        assert sc.dimension_scores[ScorecardDimension.STATE_INTEGRITY.value] == 100

    def test_state_integrity_0_with_invalid_transitions(self):
        result = _full_result()
        vr = _full_vr()
        vr.invalid_transitions_detected = ["FAILED->HEALTHY: blocked"]  # not "CORRECTLY_BLOCKED"
        sc = compute_scorecard(result, vr)
        assert sc.dimension_scores[ScorecardDimension.STATE_INTEGRITY.value] == 0

    def test_correctly_blocked_transitions_do_not_reduce_state_integrity(self):
        result = _full_result()
        vr = _full_vr()
        vr.invalid_transitions_detected = ["CORRECTLY_BLOCKED: FAILED->HEALTHY: reason"]
        sc = compute_scorecard(result, vr)
        assert sc.dimension_scores[ScorecardDimension.STATE_INTEGRITY.value] == 100
