"""paper_trading/event_bus_v160.py — Process-local Event Bus v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
No external message broker required.
"""
from __future__ import annotations
from typing import Callable, Dict, List, Optional

from .enums_v160 import PaperEventType
from .event_v160 import PaperEvent
from .event_journal_v160 import PaperEventJournal


class PaperEventBus:
    """Process-local, ordered event bus with journal and subscriber callbacks."""

    def __init__(self) -> None:
        self._journal = PaperEventJournal()
        self._subscribers: Dict[str, List[Callable[[PaperEvent], None]]] = {}
        self._sequence: int = 0

    def subscribe(self, event_type: PaperEventType, callback: Callable[[PaperEvent], None]) -> None:
        key = event_type.value
        if key not in self._subscribers:
            self._subscribers[key] = []
        self._subscribers[key].append(callback)

    def publish(self, event: PaperEvent) -> PaperEvent:
        stored = self._journal.append(event)
        self._sequence = stored.sequence + 1
        key = event.event_type.value
        for cb in self._subscribers.get(key, []):
            cb(stored)
        for cb in self._subscribers.get("*", []):
            cb(stored)
        return stored

    def next_sequence(self) -> int:
        return self._sequence

    def get_journal(self) -> PaperEventJournal:
        return self._journal

    def verify_chain(self) -> bool:
        return self._journal.verify_chain()

    def event_count(self) -> int:
        return self._journal.count()
