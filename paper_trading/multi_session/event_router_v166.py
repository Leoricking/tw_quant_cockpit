"""
paper_trading/multi_session/event_router_v166.py — Event Router v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from paper_trading.multi_session.models_v166 import EventRecord

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True
NO_EXTERNAL_MESSAGE_BUS = True


class EventRouter:
    """Routes events to subscribed sessions. Local in-process only."""

    def __init__(self) -> None:
        self._subscriptions: Dict[str, List[str]] = {}  # event_type -> [session_ids]

    def subscribe(self, session_id: str, event_type: str) -> None:
        self._subscriptions.setdefault(event_type, []).append(session_id)

    def unsubscribe(self, session_id: str, event_type: str) -> None:
        subs = self._subscriptions.get(event_type, [])
        self._subscriptions[event_type] = [s for s in subs if s != session_id]

    def route(self, event: EventRecord) -> List[str]:
        return list(self._subscriptions.get(event.event_type, []))

    def route_all(self, events: List[EventRecord]) -> Dict[str, List[str]]:
        result: Dict[str, List[str]] = {}
        for e in events:
            result[e.event_id] = self.route(e)
        return result
