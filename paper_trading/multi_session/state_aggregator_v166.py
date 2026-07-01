"""
paper_trading/multi_session/state_aggregator_v166.py — State Aggregator v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List
from paper_trading.multi_session.models_v166 import SessionDescriptor

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True


class StateAggregator:
    """Aggregates state across multiple sessions. Local only."""

    def aggregate(self, sessions: List[SessionDescriptor]) -> Dict[str, Any]:
        by_state: Dict[str, int] = {}
        by_type: Dict[str, int] = {}
        for s in sessions:
            by_state[s.lifecycle_state.value] = by_state.get(s.lifecycle_state.value, 0) + 1
            by_type[s.session_type.value] = by_type.get(s.session_type.value, 0) + 1
        return {
            "total": len(sessions),
            "by_state": by_state,
            "by_type": by_type,
            "running_count": by_state.get("RUNNING", 0),
            "blocked_count": by_state.get("BLOCKED", 0),
            "failed_count": by_state.get("FAILED", 0),
        }
