"""
paper_trading/multi_session/session_discovery_v166.py — Session Discovery v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Local in-process discovery only. No network. No external service.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.enums_v166 import SessionType, SessionLifecycleState, SessionPriority
from paper_trading.multi_session.session_registry_v166 import SessionRegistry

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True


class SessionDiscovery:
    """Local session discovery — queries registry. No network calls."""

    def __init__(self, registry: SessionRegistry) -> None:
        self._registry = registry

    def discover_all(self) -> List[str]:
        return [d.session_id for d in self._registry.list_sessions()]

    def discover_by_type(self, session_type: SessionType) -> List[str]:
        return [d.session_id for d in self._registry.filter_by_type(session_type)]

    def discover_running(self) -> List[str]:
        return [d.session_id for d in self._registry.filter_by_state(SessionLifecycleState.RUNNING)]

    def discover_by_symbol(self, symbol: str) -> List[str]:
        return [d.session_id for d in self._registry.list_sessions() if symbol in d.symbols]

    def discover_by_strategy(self, strategy: str) -> List[str]:
        return [d.session_id for d in self._registry.list_sessions() if strategy in d.strategies]

    def discover_by_priority(self, priority: SessionPriority) -> List[str]:
        return [d.session_id for d in self._registry.list_sessions() if d.priority == priority]

    def count(self) -> int:
        return self._registry.count()

    def summary(self) -> Dict[str, Any]:
        sessions = self._registry.list_sessions()
        by_type: Dict[str, int] = {}
        by_state: Dict[str, int] = {}
        for d in sessions:
            by_type[d.session_type.value] = by_type.get(d.session_type.value, 0) + 1
            by_state[d.lifecycle_state.value] = by_state.get(d.lifecycle_state.value, 0) + 1
        return {"total": len(sessions), "by_type": by_type, "by_state": by_state}
