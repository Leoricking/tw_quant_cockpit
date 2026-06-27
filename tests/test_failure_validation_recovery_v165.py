"""
tests/test_failure_validation_recovery_v165.py — Recovery Validator tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
from decimal import Decimal

import pytest

from paper_trading.failure_validation.enums_v165 import (
    INVALID_RECOVERY_TRANSITIONS,
    VERIFICATION_REQUIRED_TRANSITIONS,
    ExpectedOutcome,
    FailureDomain,
    FailureSeverity,
    FailureType,
    RecoveryState,
)
from paper_trading.failure_validation.models_v165 import (
    FailureInjectionRequest,
    FailureInjectionResult,
    FailureScenario,
    RecoveryPlan,
)
from paper_trading.failure_validation.recovery_validator_v165 import (
    AUTO_FAILOVER_ENABLED,
    AUTO_RECOVERY_EXECUTION_ENABLED,
    AUTO_RESTART_ENABLED,
    RecoveryValidator,
)


def _make_result(detection=True, containment=True, recovery=True):
    from paper_trading.failure_validation.enums_v165 import InjectionStatus
    result = FailureInjectionResult()
    result.detection_confirmed = detection
    result.containment_confirmed = containment
    result.recovery_triggered = recovery
    result.status = InjectionStatus.CONTAINED if containment else InjectionStatus.DETECTED
    return result


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestRecoveryValidatorSafetyFlags:
    def test_auto_recovery_execution_disabled(self):
        assert AUTO_RECOVERY_EXECUTION_ENABLED is False

    def test_auto_failover_disabled(self):
        assert AUTO_FAILOVER_ENABLED is False

    def test_auto_restart_disabled(self):
        assert AUTO_RESTART_ENABLED is False

    def test_validator_instantiates(self):
        rv = RecoveryValidator()
        assert rv is not None


# ---------------------------------------------------------------------------
# validate_transition
# ---------------------------------------------------------------------------

class TestValidateTransition:
    def test_degraded_to_containing_allowed(self):
        rv = RecoveryValidator()
        allowed, reason = rv.validate_transition(RecoveryState.DEGRADED, RecoveryState.CONTAINED)
        assert allowed is True

    def test_failed_to_healthy_blocked(self):
        rv = RecoveryValidator()
        allowed, reason = rv.validate_transition(RecoveryState.FAILED, RecoveryState.HEALTHY)
        assert allowed is False
        assert "INVALID" in reason or "FAILED" in reason

    def test_blocked_to_recovered_blocked(self):
        rv = RecoveryValidator()
        allowed, reason = rv.validate_transition(RecoveryState.BLOCKED, RecoveryState.RECOVERED)
        assert allowed is False

    def test_recovering_to_recovered_without_verification_blocked(self):
        rv = RecoveryValidator()
        allowed, reason = rv.validate_transition(
            RecoveryState.RECOVERING, RecoveryState.RECOVERED,
            verification_passed=False,
        )
        assert allowed is False
        assert "verification" in reason.lower()

    def test_recovering_to_recovered_with_verification_allowed(self):
        rv = RecoveryValidator()
        allowed, reason = rv.validate_transition(
            RecoveryState.RECOVERING, RecoveryState.RECOVERED,
            verification_passed=True,
        )
        assert allowed is True

    def test_all_invalid_transitions_rejected(self):
        rv = RecoveryValidator()
        for (f, t) in INVALID_RECOVERY_TRANSITIONS:
            allowed, _ = rv.validate_transition(f, t)
            assert allowed is False, f"Expected {f.value}→{t.value} to be invalid"


# ---------------------------------------------------------------------------
# build_recovery_plan
# ---------------------------------------------------------------------------

class TestBuildRecoveryPlan:
    def test_plan_has_auto_execution_false(self):
        rv = RecoveryValidator()
        result = _make_result()
        plan = rv.build_recovery_plan(result)
        assert plan.auto_execution_enabled is False

    def test_plan_has_requires_verification_true(self):
        rv = RecoveryValidator()
        result = _make_result()
        plan = rv.build_recovery_plan(result)
        assert plan.requires_verification is True

    def test_plan_steps_when_contained(self):
        rv = RecoveryValidator()
        result = _make_result(detection=True, containment=True)
        plan = rv.build_recovery_plan(result)
        assert len(plan.steps) >= 4  # verify, initiate, verify_state, reconcile, replay

    def test_plan_has_rollback_steps(self):
        rv = RecoveryValidator()
        result = _make_result()
        plan = rv.build_recovery_plan(result)
        assert len(plan.rollback_steps) >= 2

    def test_plan_rollback_steps_include_halt(self):
        rv = RecoveryValidator()
        result = _make_result()
        plan = rv.build_recovery_plan(result)
        actions = [s["action"] for s in plan.rollback_steps]
        assert "halt_recovery" in actions

    def test_plan_rollback_steps_include_restore_baseline(self):
        rv = RecoveryValidator()
        result = _make_result()
        plan = rv.build_recovery_plan(result)
        actions = [s["action"] for s in plan.rollback_steps]
        assert "restore_baseline" in actions

    def test_plan_with_rto_budget(self):
        rv = RecoveryValidator()
        result = _make_result()
        plan = rv.build_recovery_plan(result, rto_budget_ms=Decimal("5000"))
        assert plan.rto_budget_ms == Decimal("5000")

    def test_plan_with_rpo_budget(self):
        rv = RecoveryValidator()
        result = _make_result()
        plan = rv.build_recovery_plan(result, rpo_budget_ms=Decimal("1000"))
        assert plan.rpo_budget_ms == Decimal("1000")

    def test_plan_scenario_id_matches_result(self):
        rv = RecoveryValidator()
        result = _make_result()
        result.scenario_id = "test_scenario_123"
        plan = rv.build_recovery_plan(result)
        assert plan.scenario_id == "test_scenario_123"


# ---------------------------------------------------------------------------
# execute_validation
# ---------------------------------------------------------------------------

class TestExecuteValidation:
    def test_validation_has_final_state(self):
        rv = RecoveryValidator()
        result = _make_result()
        plan = rv.build_recovery_plan(result)
        vr = rv.execute_validation(plan, result, seed=42)
        assert vr.final_state is not None

    def test_validation_detects_invalid_transitions(self):
        rv = RecoveryValidator()
        result = _make_result()
        plan = rv.build_recovery_plan(result)
        vr = rv.execute_validation(plan, result, seed=42)
        # The validator always tests invalid transitions
        assert len(vr.invalid_transitions_detected) >= 2

    def test_validation_invalid_transitions_have_correctly_blocked_prefix(self):
        rv = RecoveryValidator()
        result = _make_result()
        plan = rv.build_recovery_plan(result)
        vr = rv.execute_validation(plan, result, seed=42)
        for item in vr.invalid_transitions_detected:
            assert "CORRECTLY_BLOCKED" in item or "FAILED" in item or "BLOCKED" in item

    def test_validation_has_state_transitions(self):
        rv = RecoveryValidator()
        result = _make_result(detection=True, containment=True, recovery=True)
        plan = rv.build_recovery_plan(result)
        vr = rv.execute_validation(plan, result, seed=42)
        assert len(vr.state_transitions) >= 1

    def test_rto_measured_when_budget_set(self):
        rv = RecoveryValidator()
        result = _make_result()
        plan = rv.build_recovery_plan(result, rto_budget_ms=Decimal("5000"))
        vr = rv.execute_validation(plan, result, seed=42)
        assert vr.rto_actual_ms is not None

    def test_rpo_measured_when_budget_set(self):
        rv = RecoveryValidator()
        result = _make_result()
        plan = rv.build_recovery_plan(result, rpo_budget_ms=Decimal("500"))
        vr = rv.execute_validation(plan, result, seed=42)
        assert vr.rpo_actual_ms is not None

    def test_rto_not_measured_when_budget_not_set(self):
        rv = RecoveryValidator()
        result = _make_result()
        plan = rv.build_recovery_plan(result)
        vr = rv.execute_validation(plan, result, seed=42)
        assert vr.rto_actual_ms is None

    def test_validation_deterministic_same_seed(self):
        rv = RecoveryValidator()
        result1 = _make_result()
        result1.scenario_id = "same_scenario"
        result2 = _make_result()
        result2.scenario_id = "same_scenario"
        plan1 = rv.build_recovery_plan(result1)
        plan2 = rv.build_recovery_plan(result2)
        vr1 = rv.execute_validation(plan1, result1, seed=100)
        vr2 = rv.execute_validation(plan2, result2, seed=100)
        assert vr1.final_state == vr2.final_state
