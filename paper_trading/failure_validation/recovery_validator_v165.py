"""
paper_trading/failure_validation/recovery_validator_v165.py — Recovery validation v1.6.5.
[!] Research Only. No Real Orders. No Real Failure Injection. Not Investment Advice.
[!] No auto-recovery execution. No auto-failover. No auto-restart. Simulation only.
[!] INVALID_RECOVERY_TRANSITIONS enforced. Verification required before RECOVERED.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

from paper_trading.failure_validation.enums_v165 import (
    INVALID_RECOVERY_TRANSITIONS,
    VERIFICATION_REQUIRED_TRANSITIONS,
    AUTO_RESUME_RUNNING_ENABLED,
    RecoveryState,
    ValidationPhase,
)
from paper_trading.failure_validation.models_v165 import (
    FailureInjectionResult,
    RecoveryPlan,
    RecoveryValidationResult,
)

AUTO_RECOVERY_EXECUTION_ENABLED = False
AUTO_FAILOVER_ENABLED = False
AUTO_RESTART_ENABLED = False


class RecoveryValidator:
    """Validates recovery state transitions and reconciliation (simulation only)."""

    def __init__(self) -> None:
        assert not AUTO_RECOVERY_EXECUTION_ENABLED, "Auto recovery must never be enabled"
        assert not AUTO_FAILOVER_ENABLED, "Auto failover must never be enabled"
        assert not AUTO_RESTART_ENABLED, "Auto restart must never be enabled"
        assert not AUTO_RESUME_RUNNING_ENABLED, "Auto resume running must never be enabled"

    def validate_transition(
        self,
        from_state: RecoveryState,
        to_state: RecoveryState,
        verification_passed: bool = False,
    ) -> Tuple[bool, str]:
        """
        Validate a state transition.
        Returns (allowed, reason).
        """
        pair = (from_state, to_state)

        if pair in INVALID_RECOVERY_TRANSITIONS:
            return False, f"Transition {from_state.value}→{to_state.value} is INVALID (explicit prohibition)"

        if pair in VERIFICATION_REQUIRED_TRANSITIONS and not verification_passed:
            return False, (
                f"Transition {from_state.value}→{to_state.value} requires verification_passed=True "
                "(RECOVERING→RECOVERED without verification is blocked)"
            )

        return True, "OK"

    def build_recovery_plan(
        self,
        result: FailureInjectionResult,
        rto_budget_ms: Optional[Decimal] = None,
        rpo_budget_ms: Optional[Decimal] = None,
    ) -> RecoveryPlan:
        """Build a simulated recovery plan for an injection result."""
        plan = RecoveryPlan(
            scenario_id=result.scenario_id,
            result_id=result.result_id,
            rto_budget_ms=rto_budget_ms,
            rpo_budget_ms=rpo_budget_ms,
            requires_verification=True,
            auto_execution_enabled=False,
        )

        # Build simulated steps based on detection state
        if result.detection_confirmed:
            plan.steps.append({
                "step": 1,
                "action": "verify_containment",
                "description": "Verify failure is contained before recovery",
            })
        if result.containment_confirmed:
            plan.steps.append({
                "step": 2,
                "action": "initiate_recovery",
                "description": "Begin simulated recovery sequence",
            })
            plan.steps.append({
                "step": 3,
                "action": "verify_state",
                "description": "Verify state after recovery",
            })
            plan.steps.append({
                "step": 4,
                "action": "reconcile_data",
                "description": "Reconcile data integrity after recovery",
            })
            plan.steps.append({
                "step": 5,
                "action": "verify_replay",
                "description": "Verify replay produces same result",
            })

        plan.rollback_steps = [
            {"step": 1, "action": "halt_recovery", "description": "Halt recovery if verification fails"},
            {"step": 2, "action": "restore_baseline", "description": "Restore from baseline snapshot"},
        ]
        return plan

    def execute_validation(
        self,
        plan: RecoveryPlan,
        result: FailureInjectionResult,
        initial_state: RecoveryState = RecoveryState.DEGRADED,
        seed: int = 42,
    ) -> RecoveryValidationResult:
        """
        Simulate the full recovery validation sequence (no real execution).
        Enforces state machine rules.
        """
        import random
        rng = random.Random(seed)

        vr = RecoveryValidationResult(
            plan_id=plan.plan_id,
            result_id=result.result_id,
            initial_state=initial_state,
        )

        current_state = initial_state

        # Step 1: DEGRADED → CONTAINED
        if result.containment_confirmed:
            allowed, reason = self.validate_transition(current_state, RecoveryState.CONTAINED)
            vr.add_transition(current_state, RecoveryState.CONTAINED, allowed, reason)
            if allowed:
                current_state = RecoveryState.CONTAINED

        # Step 2: CONTAINED → RECOVERING
        if current_state == RecoveryState.CONTAINED and result.recovery_triggered:
            allowed, reason = self.validate_transition(current_state, RecoveryState.RECOVERING)
            vr.add_transition(current_state, RecoveryState.RECOVERING, allowed, reason)
            if allowed:
                current_state = RecoveryState.RECOVERING

        # Step 3: RECOVERING → RECOVERED (requires verification)
        if current_state == RecoveryState.RECOVERING:
            verification_passed = rng.random() > 0.1
            vr.idempotency_verified = rng.random() > 0.05
            vr.data_reconciled = rng.random() > 0.05
            vr.replay_verified = rng.random() > 0.05
            vr.verification_passed = verification_passed and vr.data_reconciled and vr.replay_verified

            allowed, reason = self.validate_transition(
                current_state, RecoveryState.RECOVERED,
                verification_passed=vr.verification_passed,
            )
            vr.add_transition(current_state, RecoveryState.RECOVERED, allowed, reason)
            if allowed:
                current_state = RecoveryState.RECOVERED
            else:
                # Cannot recover without verification — test BLOCKED or FAILED
                allowed2, reason2 = self.validate_transition(current_state, RecoveryState.FAILED)
                vr.add_transition(current_state, RecoveryState.FAILED, allowed2, reason2)
                if allowed2:
                    current_state = RecoveryState.FAILED
                vr.errors.append(f"Recovery blocked: {reason}")

        # Test the INVALID transitions to confirm they are detected
        blocked_test_pairs = [
            (RecoveryState.FAILED, RecoveryState.HEALTHY),
            (RecoveryState.BLOCKED, RecoveryState.RECOVERED),
        ]
        for f, t in blocked_test_pairs:
            allowed_inv, reason_inv = self.validate_transition(f, t)
            if not allowed_inv:
                vr.invalid_transitions_detected.append(
                    f"CORRECTLY_BLOCKED: {f.value}→{t.value}: {reason_inv}"
                )

        # RTO/RPO simulation (virtual clock, Decimal ms)
        vr.rto_actual_ms = Decimal(str(rng.randint(100, 2000))) if plan.rto_budget_ms is not None else None
        vr.rpo_actual_ms = Decimal(str(rng.randint(0, 500))) if plan.rpo_budget_ms is not None else None
        if plan.rto_budget_ms is not None and vr.rto_actual_ms is not None:
            vr.rto_met = vr.rto_actual_ms <= plan.rto_budget_ms
        if plan.rpo_budget_ms is not None and vr.rpo_actual_ms is not None:
            vr.rpo_met = vr.rpo_actual_ms <= plan.rpo_budget_ms

        vr.final_state = current_state
        return vr
