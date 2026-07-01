"""
paper_trading/multi_session/lifecycle_coordinator_v166.py — Lifecycle Coordinator v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No real process start/stop. No auto restart. No auto failover.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.enums_v166 import SessionLifecycleState, DecisionType
from paper_trading.multi_session.models_v166 import SessionDescriptor, CoordinationDecision
from paper_trading.multi_session.state_machine_v166 import SessionStateMachine

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_AUTO_RESTART = True
NO_AUTO_FAILOVER = True
NO_AUTO_RESUME = True


FORBIDDEN_LIFECYCLE_ACTIONS = [
    "real_process_start",
    "real_process_stop",
    "subprocess_control",
    "service_control",
    "auto_restart",
    "auto_failover",
    "auto_resume",
]


class LifecycleCoordinator:
    """
    Manages lifecycle transitions for multiple sessions.
    All actions are logical. No real process control.
    """

    def __init__(self) -> None:
        self._machines: Dict[str, SessionStateMachine] = {}

    def register(self, session_id: str, initial: SessionLifecycleState = SessionLifecycleState.CREATED) -> None:
        self._machines[session_id] = SessionStateMachine(initial)

    def get_state(self, session_id: str) -> SessionLifecycleState:
        return self._machines[session_id].state

    def transition(
        self,
        session_id: str,
        to_state: SessionLifecycleState,
        actor: str = "lifecycle_coordinator",
        verified: bool = False,
    ) -> None:
        if session_id not in self._machines:
            raise KeyError(f"Session not registered: {session_id}")
        self._machines[session_id].transition(to_state, actor=actor, verified=verified)

    def admit(self, session_id: str) -> None:
        self.transition(session_id, SessionLifecycleState.REGISTERED)

    def mark_ready(self, session_id: str) -> None:
        self.transition(session_id, SessionLifecycleState.READY)

    def schedule(self, session_id: str) -> None:
        self.transition(session_id, SessionLifecycleState.SCHEDULED)

    def start_logical(self, session_id: str) -> None:
        self.transition(session_id, SessionLifecycleState.RUNNING, verified=True)

    def pause(self, session_id: str) -> None:
        self.transition(session_id, SessionLifecycleState.PAUSED)

    def degrade(self, session_id: str) -> None:
        self.transition(session_id, SessionLifecycleState.DEGRADED)

    def contain(self, session_id: str) -> None:
        self.transition(session_id, SessionLifecycleState.CONTAINED)

    def block(self, session_id: str) -> None:
        self.transition(session_id, SessionLifecycleState.BLOCKED)

    def mark_recovering(self, session_id: str) -> None:
        self.transition(session_id, SessionLifecycleState.RECOVERING)

    def mark_completed(self, session_id: str) -> None:
        self.transition(session_id, SessionLifecycleState.COMPLETED)

    def mark_failed(self, session_id: str) -> None:
        self.transition(session_id, SessionLifecycleState.FAILED)

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        return self._machines[session_id].get_history()

    def all_states(self) -> Dict[str, str]:
        return {sid: m.state.value for sid, m in self._machines.items()}
