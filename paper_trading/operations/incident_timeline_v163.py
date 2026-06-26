"""
Incident Timeline v1.6.3 — Append-only, immutable, hash-chained.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from paper_trading.operations.models_v163 import _now_utc


TIMELINE_EVENTS = [
    "alert_opened", "alert_acknowledged", "incident_opened",
    "session_degraded", "session_paused", "session_halted",
    "checkpoint_created", "recovery_started", "recovery_completed",
    "session_resumed", "alert_resolved", "incident_mitigated",
    "incident_resolved", "incident_closed",
]


@dataclass
class TimelineEntry:
    sequence:     int
    event_type:   str
    session_id:   str
    actor:        str
    reason:       str
    occurred_at:  datetime
    entity_id:    str   = ""
    prev_hash:    str   = ""
    entry_hash:   str   = ""

    def __post_init__(self):
        if not self.entry_hash:
            self.entry_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        data = f"{self.sequence}:{self.event_type}:{self.session_id}:{self.actor}:{self.reason}:{self.occurred_at.isoformat()}:{self.prev_hash}"
        return "sha256:" + hashlib.sha256(data.encode()).hexdigest()


class IncidentTimeline:
    """
    Append-only, immutable, deterministic sequence.
    - No timestamp regression
    - No future events
    - No missing actor
    - No missing reason
    - Content hash chain
    """

    def __init__(self, clock=None):
        self._entries: List[TimelineEntry] = []
        self._clock = clock or _now_utc

    def append(
        self,
        event_type:  str,
        session_id:  str,
        actor:       str,
        reason:      str,
        entity_id:   str = "",
        occurred_at: Optional[datetime] = None,
    ) -> Tuple[bool, object]:
        if not actor:
            return False, "Missing actor — BLOCKED"
        if not reason:
            return False, "Missing reason — BLOCKED"

        now = self._clock()
        ts = occurred_at or now

        # Ensure timezone-aware
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)

        # No future events
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        if ts > now:
            return False, f"Future event blocked: {ts}"

        # No timestamp regression
        if self._entries:
            last_ts = self._entries[-1].occurred_at
            if last_ts.tzinfo is None:
                last_ts = last_ts.replace(tzinfo=timezone.utc)
            if ts < last_ts:
                return False, f"Timestamp regression blocked: {ts} < {last_ts}"

        seq = len(self._entries)
        prev_hash = self._entries[-1].entry_hash if self._entries else ""

        entry = TimelineEntry(
            sequence=seq,
            event_type=event_type,
            session_id=session_id,
            actor=actor,
            reason=reason,
            occurred_at=ts,
            entity_id=entity_id,
            prev_hash=prev_hash,
        )
        self._entries.append(entry)
        return True, entry

    def verify_chain(self) -> Tuple[bool, str]:
        for i in range(1, len(self._entries)):
            expected_prev = self._entries[i - 1].entry_hash
            if self._entries[i].prev_hash != expected_prev:
                return False, f"Chain broken at sequence {i}"
        return True, "Chain intact"

    def tail(self, n: int = 10) -> List[TimelineEntry]:
        return self._entries[-n:]

    def all(self) -> List[TimelineEntry]:
        return list(self._entries)

    def count(self) -> int:
        return len(self._entries)


__all__ = ["TimelineEntry", "IncidentTimeline", "TIMELINE_EVENTS"]
