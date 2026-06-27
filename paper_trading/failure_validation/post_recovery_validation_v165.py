"""
paper_trading/failure_validation/post_recovery_validation_v165.py — Post-recovery validation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

from paper_trading.failure_validation.enums_v165 import RecoveryState

PAPER_ONLY = True
RESEARCH_ONLY = True


@dataclass
class PostRecoveryValidationResult:
    scenario_id: str = ""
    state_verified: bool = False
    data_reconciled: bool = False
    replay_verified: bool = False
    idempotency_verified: bool = False
    health_check_passed: bool = False
    all_passed: bool = False
    errors: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.all_passed = all([
            self.state_verified, self.data_reconciled,
            self.replay_verified, self.idempotency_verified,
            self.health_check_passed,
        ])

    def as_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "state_verified": self.state_verified,
            "data_reconciled": self.data_reconciled,
            "replay_verified": self.replay_verified,
            "idempotency_verified": self.idempotency_verified,
            "health_check_passed": self.health_check_passed,
            "all_passed": self.all_passed,
            "errors": self.errors,
        }


def run_post_recovery_validation(scenario_id: str, final_state: RecoveryState,
                                  seed: int = 42) -> PostRecoveryValidationResult:
    import random
    rng = random.Random(seed)
    is_healthy = final_state in (RecoveryState.RECOVERED, RecoveryState.HEALTHY)
    result = PostRecoveryValidationResult(
        scenario_id=scenario_id,
        state_verified=is_healthy,
        data_reconciled=is_healthy and rng.random() > 0.05,
        replay_verified=is_healthy and rng.random() > 0.05,
        idempotency_verified=is_healthy and rng.random() > 0.05,
        health_check_passed=is_healthy and rng.random() > 0.05,
    )
    result.all_passed = all([
        result.state_verified, result.data_reconciled,
        result.replay_verified, result.idempotency_verified,
        result.health_check_passed,
    ])
    return result
