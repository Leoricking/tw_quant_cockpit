"""
paper_trading/multi_session/priority_engine_v166.py — Priority Engine v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Logical priority only. Not OS scheduler control.
"""
from __future__ import annotations
from typing import Any, Dict, List
from paper_trading.multi_session.enums_v166 import SessionPriority
from paper_trading.multi_session.models_v166 import SessionDescriptor

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_OS_SCHEDULER_CONTROL = True


class PriorityEngine:
    """
    Orders sessions by priority (weighted, with deterministic tie-break).
    No OS scheduler access. No auto-production priority override.
    """

    def order_sessions(
        self,
        sessions: List[SessionDescriptor],
        seed: int = 0,
        aging_state: Dict[str, int] = None,
    ) -> List[SessionDescriptor]:
        if aging_state is None:
            aging_state = {}
        # Sort by: priority value desc, then aging rounds desc, then session_id (deterministic)
        def sort_key(s: SessionDescriptor):
            aging = aging_state.get(s.session_id, 0)
            return (-(s.priority.value + aging * 5), s.session_id)
        return sorted(sessions, key=sort_key)

    def compute_priority_score(
        self,
        session: SessionDescriptor,
        aging_rounds: int = 0,
        aging_factor: float = 0.1,
    ) -> float:
        return session.priority.value + aging_rounds * aging_factor * session.priority.value

    def detect_priority_inversion(
        self,
        waiting_session: SessionDescriptor,
        holding_session: SessionDescriptor,
    ) -> bool:
        return waiting_session.priority.value > holding_session.priority.value

    def select_victim_for_deadlock(
        self,
        candidates: List[SessionDescriptor],
        seed: int = 0,
    ) -> SessionDescriptor:
        # Deterministic victim: lowest priority, then alphabetical by session_id
        return sorted(candidates, key=lambda s: (s.priority.value, s.session_id))[0]
