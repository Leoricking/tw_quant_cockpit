"""
paper_trading/failure_validation/session_state_failure_v165.py — Session state failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

from paper_trading.failure_validation.enums_v165 import FailureType, RecoveryState

PAPER_ONLY = True
RESEARCH_ONLY = True
AUTO_RESUME_RUNNING_ENABLED = False


@dataclass
class SessionStateFailureResult:
    session_id: str = ""
    failure_type: FailureType = FailureType.STATE_DIVERGENCE
    initial_state: RecoveryState = RecoveryState.HEALTHY
    final_state: RecoveryState = RecoveryState.DEGRADED
    detected: bool = False
    alerted: bool = False
    auto_resume_blocked: bool = True  # Always True — auto resume is disabled

    def as_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "failure_type": self.failure_type.value,
            "initial_state": self.initial_state.value,
            "final_state": self.final_state.value,
            "detected": self.detected,
            "alerted": self.alerted,
            "auto_resume_blocked": self.auto_resume_blocked,
            "AUTO_RESUME_RUNNING_ENABLED": AUTO_RESUME_RUNNING_ENABLED,
        }


def simulate_session_state_failure(session_id: str, failure_type: FailureType,
                                    seed: int = 42) -> SessionStateFailureResult:
    import random
    rng = random.Random(seed)
    result = SessionStateFailureResult(session_id=session_id, failure_type=failure_type)
    result.detected = rng.random() > 0.05
    result.alerted = result.detected and rng.random() > 0.1
    assert not AUTO_RESUME_RUNNING_ENABLED, "Auto resume running must never be enabled"
    return result
