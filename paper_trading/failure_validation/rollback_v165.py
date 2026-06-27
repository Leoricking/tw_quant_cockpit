"""
paper_trading/failure_validation/rollback_v165.py — Rollback simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

from paper_trading.failure_validation.enums_v165 import RecoveryState

PAPER_ONLY = True
RESEARCH_ONLY = True
AUTO_ROLLBACK_ENABLED = False


@dataclass
class RollbackResult:
    scenario_id: str = ""
    plan_id: str = ""
    rollback_succeeded: bool = False
    steps_completed: int = 0
    steps_total: int = 0
    final_state: RecoveryState = RecoveryState.FAILED
    errors: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "rollback_succeeded": self.rollback_succeeded,
            "steps_completed": self.steps_completed,
            "steps_total": self.steps_total,
            "final_state": self.final_state.value,
            "auto_rollback_enabled": AUTO_ROLLBACK_ENABLED,
        }


def simulate_rollback(scenario_id: str, plan_id: str, rollback_steps: List[Dict],
                      seed: int = 42) -> RollbackResult:
    assert not AUTO_ROLLBACK_ENABLED
    import random
    rng = random.Random(seed)
    result = RollbackResult(
        scenario_id=scenario_id,
        plan_id=plan_id,
        steps_total=len(rollback_steps),
    )
    for _ in rollback_steps:
        if rng.random() > 0.05:
            result.steps_completed += 1
        else:
            result.errors.append("Step failed")
            break
    result.rollback_succeeded = result.steps_completed == result.steps_total
    result.final_state = RecoveryState.ROLLED_BACK if result.rollback_succeeded else RecoveryState.FAILED
    return result
