"""
paper_trading/multi_session/heartbeat_v166.py — Heartbeat v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Virtual clock only. No real sleep. No auto-restart.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.models_v166 import HeartbeatRecord
from paper_trading.multi_session.virtual_clock_v166 import VirtualClock

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_REAL_SLEEP = True
NO_AUTO_RESTART_ON_STALE = True


class HeartbeatManager:
    """Manages virtual heartbeats. No real network. No auto-restart."""

    def __init__(
        self,
        clock: Optional[VirtualClock] = None,
        expected_interval: float = 5.0,
        stale_threshold: float = 15.0,
    ) -> None:
        self._clock = clock or VirtualClock()
        self._records: Dict[str, HeartbeatRecord] = {}
        self._expected_interval = expected_interval
        self._stale_threshold = stale_threshold

    def register(self, session_id: str) -> HeartbeatRecord:
        now = self._clock.now
        rec = HeartbeatRecord(
            session_id=session_id,
            last_seen=now,
            expected_interval_seconds=self._expected_interval,
            stale_threshold_seconds=self._stale_threshold,
            missed_count=0,
            is_stale=False,
        )
        self._records[session_id] = rec
        return rec

    def beat(self, session_id: str) -> HeartbeatRecord:
        now = self._clock.now
        rec = self._records.get(session_id)
        if rec is None:
            return self.register(session_id)
        rec.last_seen = now
        rec.missed_count = 0
        rec.is_stale = False
        return rec

    def check_stale(self, session_id: str, now: Optional[datetime] = None) -> HeartbeatRecord:
        t = now or self._clock.now
        rec = self._records[session_id]
        elapsed = (t - rec.last_seen).total_seconds()
        if elapsed > rec.stale_threshold_seconds:
            rec.is_stale = True
            rec.missed_count = int(elapsed / rec.expected_interval_seconds)
        return rec

    def stale_sessions(self, now: Optional[datetime] = None) -> List[str]:
        t = now or self._clock.now
        return [
            sid for sid, rec in self._records.items()
            if (t - rec.last_seen).total_seconds() > rec.stale_threshold_seconds
        ]

    def get_record(self, session_id: str) -> Optional[HeartbeatRecord]:
        return self._records.get(session_id)
