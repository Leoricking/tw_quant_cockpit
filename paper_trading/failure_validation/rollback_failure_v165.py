"""
paper_trading/failure_validation/rollback_failure_v165.py — Rollback failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict

from paper_trading.failure_validation.enums_v165 import RecoveryState

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class RollbackFailureResult:
    scenario_id: str = ""
    rollback_step_failed: int = 0
    total_steps: int = 0
    detected: bool = False
    alerted: bool = False
    final_state: RecoveryState = RecoveryState.FAILED

    def as_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "rollback_step_failed": self.rollback_step_failed,
            "total_steps": self.total_steps,
            "detected": self.detected,
            "alerted": self.alerted,
            "final_state": self.final_state.value,
        }


def simulate_rollback_failure(scenario_id: str, total_steps: int = 3,
                               fail_at: int = 2, seed: int = 42) -> RollbackFailureResult:
    import random
    rng = random.Random(seed)
    result = RollbackFailureResult(
        scenario_id=scenario_id,
        rollback_step_failed=fail_at,
        total_steps=total_steps,
        final_state=RecoveryState.FAILED,
    )
    result.detected = rng.random() > 0.05
    result.alerted = result.detected and rng.random() > 0.1
    return result
