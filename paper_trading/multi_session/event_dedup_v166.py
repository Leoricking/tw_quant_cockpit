"""
paper_trading/multi_session/event_dedup_v166.py — Event Deduplication v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Set
from paper_trading.multi_session.models_v166 import EventRecord

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True


class EventDedup:
    """Deduplicates events by event_id. Deterministic."""

    def __init__(self) -> None:
        self._seen: Set[str] = set()

    def deduplicate(self, events: List[EventRecord]) -> List[EventRecord]:
        result = []
        for e in events:
            if e.event_id not in self._seen:
                self._seen.add(e.event_id)
                result.append(e)
        return result

    def is_duplicate(self, event_id: str) -> bool:
        return event_id in self._seen

    def seen_count(self) -> int:
        return len(self._seen)

    def reset(self) -> None:
        self._seen = set()
