"""
In-Process Event Bus v1.6.3 — Synchronous, deterministic, no network.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple

from paper_trading.operations.models_v163 import _new_id, _now_utc


@dataclass
class BusEvent:
    event_id:    str
    topic:       str
    payload:     Any
    published_at: datetime
    publisher:   str = ""
    sequence:    int = 0


class EventBus:
    """
    In-process synchronous event bus.
    - No background threads by default
    - No network transport
    - Subscriber failure isolated (doesn't crash others)
    - Duplicate event IDs blocked
    - Append-only journal
    - Ordered dispatch
    """

    def __init__(self, clock: Optional[Callable[[], datetime]] = None):
        self._clock        = clock or _now_utc
        self._subscribers: Dict[str, List[Callable]] = {}
        self._journal:     List[BusEvent]             = []
        self._seen_ids:    set                         = set()
        self._sequence:    int                         = 0

    def subscribe(self, topic: str, callback: Callable) -> None:
        self._subscribers.setdefault(topic, []).append(callback)

    def unsubscribe(self, topic: str, callback: Callable) -> bool:
        subs = self._subscribers.get(topic, [])
        if callback in subs:
            subs.remove(callback)
            return True
        return False

    def publish(
        self,
        topic:     str,
        payload:   Any,
        event_id:  Optional[str]   = None,
        publisher: str             = "",
    ) -> Tuple[bool, object]:
        eid = event_id or _new_id("evt_")

        if eid in self._seen_ids:
            return False, f"Duplicate event ID blocked: {eid}"

        event = BusEvent(
            event_id=eid,
            topic=topic,
            payload=payload,
            published_at=self._clock(),
            publisher=publisher,
            sequence=self._sequence,
        )
        self._sequence   += 1
        self._seen_ids.add(eid)
        self._journal.append(event)

        errors = []
        for cb in self._subscribers.get(topic, []):
            try:
                cb(event)
            except Exception as exc:
                errors.append(str(exc))   # Isolated

        return True, event

    def replay(self, topic: str, handler: Callable) -> int:
        count = 0
        for ev in self._journal:
            if ev.topic == topic:
                try:
                    handler(ev)
                    count += 1
                except Exception:
                    pass
        return count

    def journal(self, topic: Optional[str] = None) -> List[BusEvent]:
        if topic is None:
            return list(self._journal)
        return [e for e in self._journal if e.topic == topic]

    def count(self) -> int:
        return len(self._journal)


__all__ = ["BusEvent", "EventBus"]
