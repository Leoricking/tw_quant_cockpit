"""
paper_trading/multi_session/state_machine_v166.py — Session State Machine v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.enums_v166 import SessionLifecycleState, VALID_LIFECYCLE_TRANSITIONS
from paper_trading.multi_session.validation_v166 import validate_lifecycle_transition

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
AUTO_RESUME_DISABLED = True


class SessionStateMachine:
    """Enforces valid lifecycle transitions. No auto-resume."""

    def __init__(self, initial: SessionLifecycleState = SessionLifecycleState.CREATED) -> None:
        self._state = initial
        self._history: List[Dict[str, Any]] = []

    @property
    def state(self) -> SessionLifecycleState:
        return self._state

    def transition(
        self,
        to_state: SessionLifecycleState,
        actor: str = "system",
        verified: bool = False,
    ) -> None:
        result = validate_lifecycle_transition(self._state, to_state, verified)
        if not result.valid:
            raise ValueError(f"Invalid transition: {result.violations}")
        old = self._state
        self._state = to_state
        self._history.append({
            "from": old.value,
            "to": to_state.value,
            "actor": actor,
            "verified": verified,
        })

    def can_transition(self, to_state: SessionLifecycleState) -> bool:
        return to_state in VALID_LIFECYCLE_TRANSITIONS.get(self._state, set())

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self._history)

    def is_terminal(self) -> bool:
        return self._state in (
            SessionLifecycleState.COMPLETED,
            SessionLifecycleState.FAILED,
            SessionLifecycleState.CANCELLED,
        )
