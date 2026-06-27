"""
paper_trading/failure_validation/state_machine_v165.py — Recovery state machine v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Set, Tuple
from paper_trading.failure_validation.enums_v165 import (
    INVALID_RECOVERY_TRANSITIONS, VERIFICATION_REQUIRED_TRANSITIONS,
    AUTO_RESUME_RUNNING_ENABLED, RecoveryState
)

PAPER_ONLY = True
RESEARCH_ONLY = True


# Valid transitions (all others default allowed unless explicitly forbidden)
ALLOWED_TRANSITIONS: Set[Tuple[RecoveryState, RecoveryState]] = {
    (RecoveryState.HEALTHY, RecoveryState.DEGRADED),
    (RecoveryState.DEGRADED, RecoveryState.CONTAINED),
    (RecoveryState.DEGRADED, RecoveryState.FAILED),
    (RecoveryState.CONTAINED, RecoveryState.RECOVERING),
    (RecoveryState.RECOVERING, RecoveryState.RECOVERED),
    (RecoveryState.RECOVERING, RecoveryState.ROLLED_BACK),
    (RecoveryState.RECOVERING, RecoveryState.FAILED),
    (RecoveryState.RECOVERED, RecoveryState.HEALTHY),
    (RecoveryState.ROLLED_BACK, RecoveryState.HEALTHY),
    (RecoveryState.FAILED, RecoveryState.BLOCKED),
    (RecoveryState.BLOCKED, RecoveryState.FAILED),
}


class RecoveryStateMachine:
    """Enforces valid recovery state transitions."""

    def __init__(self, initial: RecoveryState = RecoveryState.HEALTHY) -> None:
        self.state = initial
        self._history: List[Dict[str, Any]] = []

    def can_transition(self, to: RecoveryState, verification_passed: bool = False) -> Tuple[bool, str]:
        pair = (self.state, to)
        if pair in INVALID_RECOVERY_TRANSITIONS:
            return False, f"{self.state.value}→{to.value} is explicitly INVALID"
        if pair in VERIFICATION_REQUIRED_TRANSITIONS and not verification_passed:
            return False, f"{self.state.value}→{to.value} requires verification"
        if pair not in ALLOWED_TRANSITIONS:
            return False, f"{self.state.value}→{to.value} not in allowed transitions"
        return True, "OK"

    def transition(self, to: RecoveryState, verification_passed: bool = False) -> bool:
        allowed, reason = self.can_transition(to, verification_passed)
        self._history.append({
            "from": self.state.value, "to": to.value,
            "allowed": allowed, "reason": reason,
        })
        if allowed:
            self.state = to
        return allowed

    def history(self) -> List[Dict[str, Any]]:
        return list(self._history)
