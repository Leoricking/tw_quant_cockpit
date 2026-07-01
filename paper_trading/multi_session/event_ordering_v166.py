"""
paper_trading/multi_session/event_ordering_v166.py — Event Ordering v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No future data. Monotonic ordering. Deterministic merge.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.models_v166 import EventRecord

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_FUTURE_DATA = True


class EventOrderingEngine:
    """
    Assigns global logical sequences to cross-session events.
    Enforces PIT correctness. Detects late/duplicate/out-of-order events.
    """

    def __init__(self, seed: int = 0) -> None:
        self._global_seq: int = 0
        self._seen_ids: set = set()
        self._last_by_session: Dict[str, int] = {}
        self._seed = seed

    def assign_global_sequence(self, events: List[EventRecord]) -> List[EventRecord]:
        # Sort: timestamp, then session_id (deterministic tie-break)
        sorted_events = sorted(events, key=lambda e: (e.timestamp, e.source_session_id, e.sequence))
        for e in sorted_events:
            self._global_seq += 1
            e.global_sequence = self._global_seq
        return sorted_events

    def detect_duplicates(self, events: List[EventRecord]) -> List[str]:
        dups = []
        seen = set()
        for e in events:
            if e.event_id in seen:
                dups.append(e.event_id)
            seen.add(e.event_id)
        return dups

    def detect_out_of_order(self, events: List[EventRecord]) -> List[str]:
        violations = []
        by_session: Dict[str, List[EventRecord]] = {}
        for e in events:
            by_session.setdefault(e.source_session_id, []).append(e)
        for sid, evs in by_session.items():
            sorted_evs = sorted(evs, key=lambda e: e.sequence)
            for i in range(1, len(sorted_evs)):
                if sorted_evs[i].timestamp < sorted_evs[i - 1].timestamp:
                    violations.append(sorted_evs[i].event_id)
        return violations

    def detect_late_events(self, events: List[EventRecord], now: datetime) -> List[str]:
        return [e.event_id for e in events if e.ingestion_time > e.timestamp and
                (e.ingestion_time - e.timestamp).total_seconds() > 60]

    def detect_sequence_gaps(self, events: List[EventRecord]) -> List[str]:
        gaps = []
        by_session: Dict[str, List[int]] = {}
        for e in events:
            by_session.setdefault(e.source_session_id, []).append(e.sequence)
        for sid, seqs in by_session.items():
            s_sorted = sorted(seqs)
            for i in range(1, len(s_sorted)):
                if s_sorted[i] - s_sorted[i - 1] > 1:
                    gaps.append(f"{sid}:{s_sorted[i-1]}-{s_sorted[i]}")
        return gaps

    def validate_pit(self, events: List[EventRecord], as_of: datetime) -> List[str]:
        violations = []
        for e in events:
            if e.available_from > as_of:
                violations.append(e.event_id)
        return violations
