"""
tests/test_failure_validation_models_v165.py — Models & Enums tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import hashlib
import json
from decimal import Decimal

import pytest

from paper_trading.failure_validation.enums_v165 import (
    AUTO_RESUME_RUNNING_ENABLED,
    FORBIDDEN_DOMAINS,
    INVALID_RECOVERY_TRANSITIONS,
    PERMITTED_DOMAINS,
    SCORECARD_WEIGHTS,
    VERIFICATION_REQUIRED_TRANSITIONS,
    CircuitBreakerState,
    ExpectedOutcome,
    FailureDomain,
    FailureSeverity,
    FailureType,
    InjectionStatus,
    PRODUCTION_CHAOS_ENABLED,
    REAL_FAILURE_INJECTION_ENABLED,
    RecoveryState,
    ScorecardDimension,
    ValidationPhase,
)
from paper_trading.failure_validation.models_v165 import (
    BaselineSnapshot,
    CircuitBreakerModel,
    FailureInjectionRequest,
    FailureInjectionResult,
    FailureScenario,
    FailureScorecard,
    RecoveryPlan,
    RecoveryValidationResult,
    RetryRecord,
)


# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------

class TestSafetyConstants:
    def test_real_failure_injection_disabled(self):
        assert REAL_FAILURE_INJECTION_ENABLED is False

    def test_production_chaos_disabled(self):
        assert PRODUCTION_CHAOS_ENABLED is False

    def test_auto_resume_running_disabled(self):
        assert AUTO_RESUME_RUNNING_ENABLED is False

    def test_models_safety_flags(self):
        from paper_trading.failure_validation.models_v165 import (
            REAL_FAILURE_INJECTION_ENABLED as M_RFI,
            PRODUCTION_CHAOS_ENABLED as M_PC,
            PAPER_ONLY,
            RESEARCH_ONLY,
        )
        assert M_RFI is False
        assert M_PC is False
        assert PAPER_ONLY is True
        assert RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# FailureDomain enum
# ---------------------------------------------------------------------------

class TestFailureDomainEnum:
    def test_permitted_domains_non_empty(self):
        assert len(PERMITTED_DOMAINS) >= 17

    def test_market_data_domain_permitted(self):
        assert "MARKET_DATA" in PERMITTED_DOMAINS

    def test_broker_forbidden(self):
        assert "BROKER" in FORBIDDEN_DOMAINS

    def test_real_account_forbidden(self):
        assert "REAL_ACCOUNT" in FORBIDDEN_DOMAINS

    def test_real_order_forbidden(self):
        assert "REAL_ORDER" in FORBIDDEN_DOMAINS

    def test_production_service_forbidden(self):
        assert "PRODUCTION_SERVICE" in FORBIDDEN_DOMAINS

    def test_firewall_forbidden(self):
        assert "FIREWALL" in FORBIDDEN_DOMAINS

    def test_permitted_and_forbidden_disjoint(self):
        assert PERMITTED_DOMAINS.isdisjoint(FORBIDDEN_DOMAINS)

    def test_domain_str_value(self):
        assert FailureDomain.SESSION_STATE.value == "SESSION_STATE"

    def test_domain_is_str_subclass(self):
        assert isinstance(FailureDomain.MARKET_DATA, str)

    def test_all_17_domains_present(self):
        expected = {
            "MARKET_DATA", "SESSION_STATE", "STRATEGY_SIGNAL", "PAPER_ORDER",
            "PAPER_FILL", "EVENT_STREAM", "CHECKPOINT", "STORE", "QUERY",
            "ALERT", "INCIDENT", "RECOVERY", "ANALYTICS", "REPORT",
            "DEPENDENCY", "TIME", "CONFIGURATION",
        }
        assert expected == {d.value for d in FailureDomain}


# ---------------------------------------------------------------------------
# FailureType enum
# ---------------------------------------------------------------------------

class TestFailureTypeEnum:
    def test_failure_type_count(self):
        assert len(FailureType) >= 27

    def test_timeout_value(self):
        assert FailureType.TIMEOUT.value == "TIMEOUT"

    def test_cascading_types_present(self):
        types = {ft.value for ft in FailureType}
        assert "CIRCUIT_OPEN" in types
        assert "DEPENDENCY_UNAVAILABLE" in types
        assert "DEGRADED_MODE" in types
        assert "CONFIG_DRIFT" in types
        assert "CLOCK_SKEW" in types

    def test_integrity_types_present(self):
        types = {ft.value for ft in FailureType}
        assert "CHECKPOINT_CORRUPTION" in types
        assert "HASH_MISMATCH" in types
        assert "REPLAY_MISMATCH" in types
        assert "STATE_DIVERGENCE" in types

    def test_alert_incident_types_present(self):
        types = {ft.value for ft in FailureType}
        assert "ALERT_LOSS" in types
        assert "ALERT_DUPLICATION" in types
        assert "INCIDENT_CREATION_FAILURE" in types

    def test_failure_type_is_str_subclass(self):
        assert isinstance(FailureType.STALE_DATA, str)


# ---------------------------------------------------------------------------
# RecoveryState enum & transitions
# ---------------------------------------------------------------------------

class TestRecoveryStateEnum:
    def test_healthy_state_value(self):
        assert RecoveryState.HEALTHY.value == "HEALTHY"

    def test_blocked_state_value(self):
        assert RecoveryState.BLOCKED.value == "BLOCKED"

    def test_failed_to_healthy_is_invalid(self):
        assert (RecoveryState.FAILED, RecoveryState.HEALTHY) in INVALID_RECOVERY_TRANSITIONS

    def test_blocked_to_recovered_is_invalid(self):
        assert (RecoveryState.BLOCKED, RecoveryState.RECOVERED) in INVALID_RECOVERY_TRANSITIONS

    def test_recovering_to_recovered_requires_verification(self):
        assert (RecoveryState.RECOVERING, RecoveryState.RECOVERED) in VERIFICATION_REQUIRED_TRANSITIONS

    def test_at_least_8_states(self):
        assert len(RecoveryState) >= 8


# ---------------------------------------------------------------------------
# Scorecard weights
# ---------------------------------------------------------------------------

class TestScorecardWeights:
    def test_weights_sum_to_100(self):
        assert sum(SCORECARD_WEIGHTS.values()) == 100

    def test_all_10_dimensions_weighted(self):
        assert len(SCORECARD_WEIGHTS) == 10

    def test_recovery_has_highest_weight(self):
        assert SCORECARD_WEIGHTS[ScorecardDimension.RECOVERY.value] == 20

    def test_rpo_weight(self):
        assert SCORECARD_WEIGHTS[ScorecardDimension.RPO.value] == 2

    def test_rto_weight(self):
        assert SCORECARD_WEIGHTS[ScorecardDimension.RTO.value] == 3


# ---------------------------------------------------------------------------
# FailureScenario model
# ---------------------------------------------------------------------------

class TestFailureScenario:
    def _make_scenario(self, **kwargs):
        defaults = dict(
            name="test_scenario",
            description="test",
            domain=FailureDomain.MARKET_DATA,
            failure_type=FailureType.STALE_DATA,
            severity=FailureSeverity.LOW,
            expected_outcomes=[ExpectedOutcome.DETECTED],
        )
        defaults.update(kwargs)
        return FailureScenario(**defaults)

    def test_scenario_has_uuid_id(self):
        s = self._make_scenario()
        assert len(s.scenario_id) == 36

    def test_scenario_default_safety_flags_all_true(self):
        s = self._make_scenario()
        assert s.all_safety_markers_set() is True

    def test_safety_markers_has_10_keys(self):
        s = self._make_scenario()
        markers = s.safety_markers()
        assert len(markers) == 10

    def test_fixture_only_default_true(self):
        s = self._make_scenario()
        assert s.fixture_only is True

    def test_no_broker_default_true(self):
        s = self._make_scenario()
        assert s.no_broker is True

    def test_no_real_order_default_true(self):
        s = self._make_scenario()
        assert s.no_real_order is True

    def test_not_for_production_default_true(self):
        s = self._make_scenario()
        assert s.not_for_production is True

    def test_failure_injection_only_default_true(self):
        s = self._make_scenario()
        assert s.failure_injection_only is True

    def test_reversible_default_true(self):
        s = self._make_scenario()
        assert s.reversible is True

    def test_bounded_default_true(self):
        s = self._make_scenario()
        assert s.bounded is True

    def test_two_scenarios_get_different_ids(self):
        s1 = self._make_scenario()
        s2 = self._make_scenario()
        assert s1.scenario_id != s2.scenario_id

    def test_cascading_targets_defaults_empty(self):
        s = self._make_scenario()
        assert s.cascading_targets == []

    def test_scenario_with_cascading_targets(self):
        s = self._make_scenario(cascading_targets=["SESSION_STATE", "ALERT"])
        assert len(s.cascading_targets) == 2


# ---------------------------------------------------------------------------
# FailureInjectionRequest model
# ---------------------------------------------------------------------------

class TestFailureInjectionRequest:
    def test_request_default_safety_flags(self):
        r = FailureInjectionRequest()
        assert r.fixture_only is True
        assert r.research_only is True
        assert r.paper_only is True
        assert r.no_broker is True
        assert r.no_real_order is True
        assert r.not_for_production is True

    def test_request_has_idempotency_key(self):
        r = FailureInjectionRequest()
        assert len(r.idempotency_key) == 36

    def test_two_requests_different_idempotency_keys(self):
        r1 = FailureInjectionRequest()
        r2 = FailureInjectionRequest()
        assert r1.idempotency_key != r2.idempotency_key


# ---------------------------------------------------------------------------
# FailureInjectionResult model
# ---------------------------------------------------------------------------

class TestFailureInjectionResult:
    def test_default_status_pending(self):
        r = FailureInjectionResult()
        assert r.status == InjectionStatus.PENDING

    def test_detection_not_confirmed_by_default(self):
        r = FailureInjectionResult()
        assert r.detection_confirmed is False

    def test_log_phase_appends_entry(self):
        r = FailureInjectionResult()
        r.log_phase(ValidationPhase.DETECTION, "PASS", "detected stale data")
        assert len(r.phase_log) == 1
        assert r.phase_log[0]["phase"] == "DETECTION"
        assert r.phase_log[0]["outcome"] == "PASS"

    def test_log_phase_multiple_entries(self):
        r = FailureInjectionResult()
        r.log_phase(ValidationPhase.SAFETY_PRECHECK, "PASS")
        r.log_phase(ValidationPhase.DETECTION, "PASS")
        r.log_phase(ValidationPhase.ALERT, "PASS")
        assert len(r.phase_log) == 3


# ---------------------------------------------------------------------------
# RecoveryPlan model
# ---------------------------------------------------------------------------

class TestRecoveryPlan:
    def test_auto_execution_always_false(self):
        plan = RecoveryPlan()
        assert plan.auto_execution_enabled is False

    def test_requires_verification_default_true(self):
        plan = RecoveryPlan()
        assert plan.requires_verification is True

    def test_plan_has_uuid_id(self):
        plan = RecoveryPlan()
        assert len(plan.plan_id) == 36


# ---------------------------------------------------------------------------
# RecoveryValidationResult model
# ---------------------------------------------------------------------------

class TestRecoveryValidationResult:
    def test_add_allowed_transition(self):
        r = RecoveryValidationResult()
        r.add_transition(RecoveryState.DEGRADED, RecoveryState.RECOVERING, allowed=True)
        assert len(r.state_transitions) == 1
        assert r.state_transitions[0]["allowed"] is True
        assert len(r.invalid_transitions_detected) == 0

    def test_add_invalid_transition_records_it(self):
        r = RecoveryValidationResult()
        r.add_transition(RecoveryState.FAILED, RecoveryState.HEALTHY,
                         allowed=False, reason="blocked by safety")
        assert len(r.invalid_transitions_detected) == 1
        assert "FAILED->HEALTHY" in r.invalid_transitions_detected[0]


# ---------------------------------------------------------------------------
# FailureScorecard model
# ---------------------------------------------------------------------------

class TestFailureScorecard:
    def test_compute_all_100_scores(self):
        sc = FailureScorecard()
        for dim in SCORECARD_WEIGHTS:
            sc.dimension_scores[dim] = 100
        total = sc.compute()
        assert total == 100

    def test_compute_all_zero_scores(self):
        sc = FailureScorecard()
        for dim in SCORECARD_WEIGHTS:
            sc.dimension_scores[dim] = 0
        total = sc.compute()
        assert total == 0

    def test_compute_partial_scores(self):
        sc = FailureScorecard()
        sc.dimension_scores[ScorecardDimension.RECOVERY.value] = 100  # weight 20
        total = sc.compute()
        assert total == 20

    def test_summary_has_required_keys(self):
        sc = FailureScorecard()
        sc.compute()
        summary = sc.summary()
        assert "total_score" in summary
        assert "dimensions" in summary
        assert "max_score" in summary

    def test_summary_max_score_is_100(self):
        sc = FailureScorecard()
        assert sc.summary()["max_score"] == 100


# ---------------------------------------------------------------------------
# BaselineSnapshot model
# ---------------------------------------------------------------------------

class TestBaselineSnapshot:
    def test_snapshot_computes_hash_on_init(self):
        snap = BaselineSnapshot(state_data={"price": 100, "volume": 500})
        assert len(snap.content_hash) == 64  # sha256 hex

    def test_verify_integrity_passes_fresh(self):
        snap = BaselineSnapshot(state_data={"price": 100})
        assert snap.verify_integrity() is True

    def test_verify_integrity_fails_after_mutation(self):
        snap = BaselineSnapshot(state_data={"price": 100})
        snap.state_data["price"] = 999  # mutate after init
        assert snap.verify_integrity() is False

    def test_same_data_same_hash_deterministic(self):
        s1 = BaselineSnapshot(state_data={"a": 1, "b": 2})
        s2 = BaselineSnapshot(state_data={"a": 1, "b": 2})
        assert s1.content_hash == s2.content_hash

    def test_different_data_different_hash(self):
        s1 = BaselineSnapshot(state_data={"a": 1})
        s2 = BaselineSnapshot(state_data={"a": 2})
        assert s1.content_hash != s2.content_hash


# ---------------------------------------------------------------------------
# CircuitBreakerModel
# ---------------------------------------------------------------------------

class TestCircuitBreakerModel:
    def test_initial_state_closed(self):
        cb = CircuitBreakerModel(name="test_cb")
        assert cb.state == CircuitBreakerState.CLOSED

    def test_trips_to_open_after_threshold(self):
        cb = CircuitBreakerModel(name="test_cb", failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitBreakerState.CLOSED
        cb.record_failure()
        assert cb.state == CircuitBreakerState.OPEN

    def test_open_to_half_open_after_cooldown(self):
        cb = CircuitBreakerModel(name="test_cb", failure_threshold=2, cooldown_ms=1000)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == CircuitBreakerState.OPEN
        cb.advance_clock(1000)
        assert cb.state == CircuitBreakerState.HALF_OPEN

    def test_half_open_to_closed_after_successes(self):
        cb = CircuitBreakerModel(name="test_cb", failure_threshold=2,
                                  cooldown_ms=1000, success_threshold=2)
        cb.record_failure()
        cb.record_failure()
        cb.advance_clock(1000)
        assert cb.state == CircuitBreakerState.HALF_OPEN
        cb.record_success()
        assert cb.state == CircuitBreakerState.HALF_OPEN
        cb.record_success()
        assert cb.state == CircuitBreakerState.CLOSED

    def test_transitions_logged(self):
        cb = CircuitBreakerModel(name="test_cb", failure_threshold=2)
        cb.record_failure()
        cb.record_failure()
        assert len(cb.transitions) == 1
        assert cb.transitions[0]["from"] == "CLOSED"
        assert cb.transitions[0]["to"] == "OPEN"

    def test_cooldown_not_met_stays_open(self):
        cb = CircuitBreakerModel(name="test_cb", failure_threshold=2, cooldown_ms=5000)
        cb.record_failure()
        cb.record_failure()
        cb.advance_clock(1000)
        assert cb.state == CircuitBreakerState.OPEN


# ---------------------------------------------------------------------------
# RetryRecord model
# ---------------------------------------------------------------------------

class TestRetryRecord:
    def test_initial_not_succeeded_not_exhausted(self):
        r = RetryRecord(max_attempts=3, backoff_ms=100)
        assert r.succeeded is False
        assert r.exhausted is False

    def test_success_on_first_attempt(self):
        r = RetryRecord(max_attempts=3)
        r.record_attempt(success=True)
        assert r.succeeded is True
        assert r.exhausted is False

    def test_exhaustion_after_max_attempts(self):
        r = RetryRecord(max_attempts=3, backoff_ms=100)
        r.record_attempt(success=False)
        r.record_attempt(success=False)
        r.record_attempt(success=False)
        assert r.exhausted is True
        assert r.succeeded is False

    def test_backoff_increases_clock(self):
        r = RetryRecord(max_attempts=3, backoff_ms=100)
        r.record_attempt(success=False)  # attempt 1; clock += 100 * 2^0 = 100
        assert r.virtual_clock_ms == 100

    def test_attempt_log_records_entries(self):
        r = RetryRecord(max_attempts=3)
        r.record_attempt(success=False, detail="timeout")
        assert len(r.attempts) == 1
        assert r.attempts[0]["success"] is False
        assert r.attempts[0]["detail"] == "timeout"

    def test_exponential_backoff_pattern(self):
        r = RetryRecord(max_attempts=4, backoff_ms=100)
        r.record_attempt(success=False)  # clock after: 100
        r.record_attempt(success=False)  # clock after: 100 + 200 = 300
        assert r.virtual_clock_ms == 300
