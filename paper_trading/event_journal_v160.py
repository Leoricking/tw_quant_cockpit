"""paper_trading/event_journal_v160.py — Append-only Event Journal v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
"""
from __future__ import annotations
from typing import List, Optional

from .event_v160 import PaperEvent
from .idempotency_v160 import IdempotencyRegistry


class PaperEventJournal:
    """Append-only, hash-chained event journal. Replayable, recoverable."""

    def __init__(self) -> None:
        self._events: List[PaperEvent] = []
        self._idempotency = IdempotencyRegistry()
        self._last_hash: str = ""

    def append(self, event: PaperEvent) -> PaperEvent:
        if self._idempotency.is_duplicate(event.idempotency_key):
            existing_seq = self._idempotency.get_sequence(event.idempotency_key)
            # Return existing event (idempotent)
            for e in self._events:
                if e.idempotency_key == event.idempotency_key:
                    return e
            return event

        expected_seq = len(self._events)
        if event.sequence != expected_seq:
            raise ValueError(f"Out-of-order event: expected seq {expected_seq}, got {event.sequence}")

        event.previous_hash = self._last_hash
        event.content_hash = event._compute_hash()

        self._idempotency.register(event.idempotency_key, event.sequence)
        self._events.append(event)
        self._last_hash = event.content_hash
        return event

    def get_events(self) -> List[PaperEvent]:
        return list(self._events)

    def get_event(self, sequence: int) -> Optional[PaperEvent]:
        if 0 <= sequence < len(self._events):
            return self._events[sequence]
        return None

    def verify_chain(self) -> bool:
        prev_hash = ""
        for event in self._events:
            if event.previous_hash != prev_hash:
                return False
            if not event.verify_hash():
                return False
            prev_hash = event.content_hash
        return True

    def count(self) -> int:
        return len(self._events)

    def last_hash(self) -> str:
        return self._last_hash

    def replay(self) -> List[PaperEvent]:
        """Return all events in order for replay."""
        return list(self._events)
