"""
replay/timeframe_timeline.py — MultiTimeframeReplayTimeline v1.2.5

Timeline of events across all timeframes during a replay session.
Never includes future outcomes.

Timeline events: BAR_OPENED, BAR_UPDATED_PARTIAL, BAR_COMPLETED, SIGNAL_APPEARED,
SIGNAL_CLEARED, WARNING_APPEARED, WARNING_CLEARED, ALIGNMENT_CHANGED,
CONFLICT_APPEARED, CONFLICT_CLEARED, TIMEFRAME_UNAVAILABLE, TIMEFRAME_AVAILABLE,
MARKET_OPEN, MARKET_CLOSE.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
[!] Timeline never includes future outcomes.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

TIMELINE_EVENTS = [
    "BAR_OPENED", "BAR_UPDATED_PARTIAL", "BAR_COMPLETED",
    "SIGNAL_APPEARED", "SIGNAL_CLEARED",
    "WARNING_APPEARED", "WARNING_CLEARED",
    "ALIGNMENT_CHANGED",
    "CONFLICT_APPEARED", "CONFLICT_CLEARED",
    "TIMEFRAME_UNAVAILABLE", "TIMEFRAME_AVAILABLE",
    "MARKET_OPEN", "MARKET_CLOSE",
]

FORBIDDEN_TIMELINE_FIELDS = [
    "outcome", "forward_return", "realized_pnl", "hindsight_score",
    "final_session_high", "final_session_low",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_event_id() -> str:
    return f"EVT-{uuid.uuid4().hex[:12].upper()}"


class MultiTimeframeReplayTimeline:
    """
    Multi-timeframe replay timeline.

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] Never includes future outcomes.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    TIMEFRAME_ORDER = ["D1", "M60", "M20", "M5", "M1"]

    def __init__(self) -> None:
        self._events: List[Dict[str, Any]] = []

    def build(
        self,
        session_id: str,
        bars_by_tf: Optional[Dict[str, List[Dict[str, Any]]]] = None,
        session_start: str = "",
        session_end: str = "",
    ) -> List[Dict[str, Any]]:
        """Build timeline events from bar data."""
        bars_by_tf = bars_by_tf or {}
        events: List[Dict[str, Any]] = []

        # Market open/close events
        if session_start:
            events.append(self._make_event(
                "MARKET_OPEN", session_start, None, "Market session opened",
                session_id=session_id
            ))
        if session_end:
            events.append(self._make_event(
                "MARKET_CLOSE", session_end, None, "Market session closed",
                session_id=session_id
            ))

        # Bar events per timeframe
        for tf in self.TIMEFRAME_ORDER:
            tf_bars = bars_by_tf.get(tf, [])
            for bar in sorted(tf_bars, key=lambda b: b.get("timestamp", "")):
                bar_ts = bar.get("timestamp", "")
                is_complete = bar.get("is_complete", False)
                is_partial  = bar.get("is_partial", False)

                # Bar opened
                events.append(self._make_event(
                    "BAR_OPENED", bar_ts, tf,
                    f"{tf} bar opened at {bar_ts}",
                    bar=bar, session_id=session_id
                ))

                # Partial update
                if is_partial and not is_complete:
                    events.append(self._make_event(
                        "BAR_UPDATED_PARTIAL", bar_ts, tf,
                        f"{tf} bar partial at {bar_ts}",
                        bar=bar, session_id=session_id
                    ))

                # Bar completed
                if is_complete:
                    events.append(self._make_event(
                        "BAR_COMPLETED", bar_ts, tf,
                        f"{tf} bar completed at {bar_ts}",
                        bar=bar, session_id=session_id
                    ))

        self._events = sorted(events, key=lambda e: e.get("event_timestamp", ""))
        return self._events

    def get_timestamp(self, timestamp: str) -> List[Dict[str, Any]]:
        """Return events at or before timestamp."""
        return [e for e in self._events if e.get("event_timestamp", "") <= timestamp]

    def get_range(self, start: str, end: str) -> List[Dict[str, Any]]:
        """Return events within timestamp range."""
        return [
            e for e in self._events
            if start <= e.get("event_timestamp", "") <= end
        ]

    def next_event(self, timestamp: str) -> Optional[Dict[str, Any]]:
        """Return next event after timestamp."""
        future = [e for e in self._events if e.get("event_timestamp", "") > timestamp]
        return future[0] if future else None

    def previous_event(self, timestamp: str) -> Optional[Dict[str, Any]]:
        """Return most recent event before or at timestamp."""
        past = [e for e in self._events if e.get("event_timestamp", "") <= timestamp]
        return past[-1] if past else None

    def signal_changes(self, timeframe: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return signal change events."""
        events = [e for e in self._events if e["event_type"] in ("SIGNAL_APPEARED", "SIGNAL_CLEARED")]
        if timeframe:
            events = [e for e in events if e.get("timeframe") == timeframe]
        return events

    def agreement_changes(self) -> List[Dict[str, Any]]:
        """Return alignment/agreement change events."""
        return [e for e in self._events if e["event_type"] == "ALIGNMENT_CHANGED"]

    def conflict_changes(self) -> List[Dict[str, Any]]:
        """Return conflict events."""
        return [
            e for e in self._events
            if e["event_type"] in ("CONFLICT_APPEARED", "CONFLICT_CLEARED")
        ]

    def partial_to_complete_changes(self) -> List[Dict[str, Any]]:
        """Return bar completion events."""
        return [e for e in self._events if e["event_type"] == "BAR_COMPLETED"]

    def availability_changes(self) -> List[Dict[str, Any]]:
        """Return timeframe availability change events."""
        return [
            e for e in self._events
            if e["event_type"] in ("TIMEFRAME_UNAVAILABLE", "TIMEFRAME_AVAILABLE")
        ]

    def summary(self) -> Dict[str, Any]:
        return {
            "total_events": len(self._events),
            "event_types": list({e["event_type"] for e in self._events}),
            "first_event": self._events[0].get("event_timestamp") if self._events else None,
            "last_event": self._events[-1].get("event_timestamp") if self._events else None,
            "no_future_outcomes": True,
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _make_event(
        self,
        event_type: str,
        event_timestamp: str,
        timeframe: Optional[str],
        description: str,
        bar: Optional[Dict[str, Any]] = None,
        session_id: str = "",
    ) -> Dict[str, Any]:
        """Create a timeline event dict."""
        # Strip forbidden fields from bar data
        safe_bar = None
        if bar:
            safe_bar = {k: v for k, v in bar.items() if k not in FORBIDDEN_TIMELINE_FIELDS}

        return {
            "event_id": _new_event_id(),
            "event_type": event_type,
            "event_timestamp": event_timestamp,
            "timeframe": timeframe,
            "description": description,
            "bar": safe_bar,
            "session_id": session_id,
            "generated_at": _now_utc(),
            "has_future_outcome": False,
            "research_only": True,
        }
