"""
paper_trading/failure_validation/event_stream_v165.py — Event stream failure simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

PAPER_ONLY = True
RESEARCH_ONLY = True


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class SimulatedEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    sequence_no: int = 0
    payload: Dict[str, Any] = field(default_factory=dict)
    emitted_at: datetime = field(default_factory=_utcnow)


class EventStreamSimulator:
    """Simulates an event stream with controlled failure injection."""

    def __init__(self, seed: int = 42) -> None:
        import random
        self._rng = random.Random(seed)
        self._events: List[SimulatedEvent] = []
        self._dropped: int = 0
        self._duplicated: int = 0
        self._out_of_order: int = 0

    def emit(self, event_type: str, payload: Dict[str, Any],
             drop_prob: float = 0.0, dup_prob: float = 0.0,
             out_of_order_prob: float = 0.0) -> List[SimulatedEvent]:
        seq = len(self._events) + 1
        evt = SimulatedEvent(event_type=event_type, sequence_no=seq, payload=payload)

        if self._rng.random() < drop_prob:
            self._dropped += 1
            return []

        emitted = [evt]
        if self._rng.random() < dup_prob:
            dup = SimulatedEvent(event_id=evt.event_id, event_type=event_type,
                                 sequence_no=seq, payload=payload)
            emitted.append(dup)
            self._duplicated += 1

        if self._rng.random() < out_of_order_prob and len(self._events) > 0:
            emitted.reverse()
            self._out_of_order += 1

        self._events.extend(emitted)
        return emitted

    def stats(self) -> Dict[str, int]:
        return {
            "total_emitted": len(self._events),
            "dropped": self._dropped,
            "duplicated": self._duplicated,
            "out_of_order": self._out_of_order,
        }
