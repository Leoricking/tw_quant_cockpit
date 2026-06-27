"""
paper_trading/failure_validation/recovery_failure_v165.py — Recovery failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

from paper_trading.failure_validation.enums_v165 import RecoveryState

PAPER_ONLY = True
RESEARCH_ONLY = True
AUTO_RECOVERY_EXECUTION_ENABLED = False


@dataclass
class RecoveryFailureResult:
    scenario_id: str = ""
    recovery_plan_id: str = ""
    steps_attempted: int = 0
    steps_succeeded: int = 0
    failure_at_step: int = 0
    final_state: RecoveryState = RecoveryState.FAILED
    rollback_attempted: bool = False
    rollback_succeeded: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "steps_attempted": self.steps_attempted,
            "steps_succeeded": self.steps_succeeded,
            "failure_at_step": self.failure_at_step,
            "final_state": self.final_state.value,
            "rollback_attempted": self.rollback_attempted,
            "rollback_succeeded": self.rollback_succeeded,
            "auto_recovery_enabled": AUTO_RECOVERY_EXECUTION_ENABLED,
        }


def simulate_recovery_failure(scenario_id: str, plan_id: str, total_steps: int = 5,
                               fail_at_step: int = 3, seed: int = 42) -> RecoveryFailureResult:
    assert not AUTO_RECOVERY_EXECUTION_ENABLED
    import random
    rng = random.Random(seed)
    result = RecoveryFailureResult(
        scenario_id=scenario_id,
        recovery_plan_id=plan_id,
        steps_attempted=fail_at_step,
        steps_succeeded=fail_at_step - 1,
        failure_at_step=fail_at_step,
        final_state=RecoveryState.FAILED,
    )
    result.rollback_attempted = True
    result.rollback_succeeded = rng.random() > 0.3
    if result.rollback_succeeded:
        result.final_state = RecoveryState.ROLLED_BACK
    return result
