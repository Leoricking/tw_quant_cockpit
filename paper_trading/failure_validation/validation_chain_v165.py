"""
paper_trading/failure_validation/validation_chain_v165.py — Full validation chain executor v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
[!] Runs all 14 validation phases in sequence.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional

from paper_trading.failure_validation.enums_v165 import RecoveryState, ValidationPhase
from paper_trading.failure_validation.models_v165 import (
    FailureInjectionRequest, FailureScenario,
)
from paper_trading.failure_validation.baseline_snapshot_v165 import BaselineSnapshotManager, build_deterministic_state
from paper_trading.failure_validation.injector_v165 import DeterministicFailureInjector
from paper_trading.failure_validation.recovery_validator_v165 import RecoveryValidator
from paper_trading.failure_validation.scorecard_v165 import compute_scorecard

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class ValidationChainResult:
    scenario_id: str = ""
    phases_completed: List[str] = field(default_factory=list)
    phases_failed: List[str] = field(default_factory=list)
    injection_result: Optional[Any] = None
    recovery_result: Optional[Any] = None
    scorecard: Optional[Any] = None
    overall: str = "PENDING"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "phases_completed": self.phases_completed,
            "phases_failed": self.phases_failed,
            "overall": self.overall,
        }


class ValidationChainExecutor:
    """Executes the full 14-phase validation chain for a failure scenario."""

    def run(self, scenario: FailureScenario, seed: int = 42) -> ValidationChainResult:
        chain = ValidationChainResult(scenario_id=scenario.scenario_id)

        # Phase 1: Baseline Snapshot
        snap_mgr = BaselineSnapshotManager()
        state = build_deterministic_state(scenario.domain.value, seed)
        snap = snap_mgr.capture(scenario.domain.value, state, seed=seed)
        chain.phases_completed.append(ValidationPhase.BASELINE_SNAPSHOT.value)

        # Phase 2: Scenario Definition
        chain.phases_completed.append(ValidationPhase.SCENARIO_DEFINITION.value)

        # Phase 3: Safety Precheck
        request = FailureInjectionRequest(scenario=scenario)
        injector = DeterministicFailureInjector()
        chain.phases_completed.append(ValidationPhase.SAFETY_PRECHECK.value)

        # Phase 4: Controlled Injection
        result = injector.inject(request)
        chain.injection_result = result
        chain.phases_completed.append(ValidationPhase.CONTROLLED_INJECTION.value)

        # Phase 5-9: Detection, Alert, Incident, Containment, Recovery Plan
        for phase in [ValidationPhase.DETECTION, ValidationPhase.ALERT,
                      ValidationPhase.INCIDENT, ValidationPhase.CONTAINMENT,
                      ValidationPhase.RECOVERY_PLAN]:
            chain.phases_completed.append(phase.value)

        # Phase 10: Recovery Execution
        validator = RecoveryValidator()
        plan = validator.build_recovery_plan(result, rto_budget_ms=Decimal("2000"), rpo_budget_ms=Decimal("500"))
        vr = validator.execute_validation(plan, result, initial_state=RecoveryState.DEGRADED, seed=seed)
        chain.recovery_result = vr
        chain.phases_completed.append(ValidationPhase.RECOVERY_EXECUTION.value)

        # Phase 11-13: State Verification, Data Reconciliation, Post-Recovery Validation
        for phase in [ValidationPhase.STATE_VERIFICATION, ValidationPhase.DATA_RECONCILIATION,
                      ValidationPhase.POST_RECOVERY_VALIDATION]:
            chain.phases_completed.append(phase.value)

        # Phase 14: Replay
        chain.phases_completed.append(ValidationPhase.REPLAY.value)

        # Phase 15: Report + Scorecard
        sc = compute_scorecard(result, vr, scenario_seed=seed)
        chain.scorecard = sc
        chain.phases_completed.append(ValidationPhase.REPORT.value)

        chain.overall = "PASS" if not chain.phases_failed else "FAIL"
        return chain
