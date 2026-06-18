"""
replay/timeframe_clock.py — ReplayTimeframeClock v1.2.5

Single authoritative clock for all timeframes in multi-timeframe replay.
No individual timeframe sneaks ahead. Out-of-session → OUT_OF_SESSION.
Backward movement never below session start. Forward never above session end.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Single clock for all timeframes. No individual TF advance. Not Investment Advice.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

OUT_OF_SESSION = "OUT_OF_SESSION"
IN_SESSION     = "IN_SESSION"
PRE_SESSION    = "PRE_SESSION"
POST_SESSION   = "POST_SESSION"


class ReplayTimeframeClock:
    """
    Single authoritative clock for all timeframes in a replay session.

    Rules:
    - One clock governs all timeframes — no individual TF sneaking ahead.
    - out-of-session movement → status = OUT_OF_SESSION.
    - backward: never below session_start.
    - forward: never above session_end.
    - before Outcome Reveal: never crosses allowed boundary.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(
        self,
        session_start: Optional[str] = None,
        session_end: Optional[str] = None,
        initial_timestamp: Optional[str] = None,
        timezone: str = "Asia/Taipei",
    ) -> None:
        self._timezone = timezone
        self._session_start = session_start or "2023-01-06T09:00:00"
        self._session_end   = session_end   or "2023-01-06T13:30:00"
        self._current: str  = initial_timestamp or self._session_start
        self._history: List[str] = [self._current]
        self._paused: bool = False
        self._outcome_reveal_allowed: bool = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def current_timestamp(self) -> str:
        """Return current replay timestamp."""
        return self._current

    def set_timestamp(self, timestamp: str) -> Dict[str, Any]:
        """
        Set clock to specific timestamp.
        Clamps to [session_start, session_end].
        Returns status dict.
        """
        clamped = self._clamp(timestamp)
        status = self._session_status(clamped)
        self._current = clamped
        self._history.append(clamped)
        return {"timestamp": clamped, "status": status, "clamped": clamped != timestamp}

    def next_bar(self, timeframe: Optional[str] = None) -> Dict[str, Any]:
        """Advance clock to next bar boundary for given timeframe."""
        minutes = self._timeframe_minutes(timeframe or "M1")
        dt = self._parse(self._current)
        if dt is None:
            return {"timestamp": self._current, "status": "ERROR"}
        new_dt = dt + timedelta(minutes=minutes)
        new_ts = new_dt.isoformat()
        return self.set_timestamp(new_ts)

    def previous_bar(self, timeframe: Optional[str] = None) -> Dict[str, Any]:
        """Move clock back by one bar boundary for given timeframe."""
        minutes = self._timeframe_minutes(timeframe or "M1")
        dt = self._parse(self._current)
        if dt is None:
            return {"timestamp": self._current, "status": "ERROR"}
        new_dt = dt - timedelta(minutes=minutes)
        new_ts = new_dt.isoformat()
        return self.set_timestamp(new_ts)

    def jump(self, timestamp: str) -> Dict[str, Any]:
        """Jump to specific timestamp (clamped to session bounds)."""
        return self.set_timestamp(timestamp)

    def step(self, minutes: Optional[int] = None, timeframe: Optional[str] = None) -> Dict[str, Any]:
        """Step forward by given minutes or timeframe bar size."""
        if timeframe and not minutes:
            minutes = self._timeframe_minutes(timeframe)
        if not minutes:
            minutes = 1
        dt = self._parse(self._current)
        if dt is None:
            return {"timestamp": self._current, "status": "ERROR"}
        new_ts = (dt + timedelta(minutes=minutes)).isoformat()
        return self.set_timestamp(new_ts)

    def synchronize(self, reference_timestamp: str) -> Dict[str, Any]:
        """Synchronize all timeframes to reference timestamp."""
        return self.set_timestamp(reference_timestamp)

    def is_market_open(self) -> bool:
        """Return True if current timestamp is within market hours."""
        try:
            from replay.timeframe_calendar import TaiwanReplayTradingCalendar
            cal = TaiwanReplayTradingCalendar()
            return cal.is_market_time(self._current)
        except Exception:
            return False

    def progress(self) -> float:
        """Return session progress as fraction 0.0–1.0."""
        try:
            start = self._parse(self._session_start)
            end   = self._parse(self._session_end)
            curr  = self._parse(self._current)
            if start is None or end is None or curr is None:
                return 0.0
            total = (end - start).total_seconds()
            elapsed = (curr - start).total_seconds()
            if total <= 0:
                return 1.0
            return max(0.0, min(1.0, elapsed / total))
        except Exception:
            return 0.0

    def summary(self) -> Dict[str, Any]:
        """Return clock state summary."""
        return {
            "current_timestamp": self._current,
            "session_start": self._session_start,
            "session_end": self._session_end,
            "timezone": self._timezone,
            "status": self._session_status(self._current),
            "progress": self.progress(),
            "is_market_open": self.is_market_open(),
            "paused": self._paused,
            "history_count": len(self._history),
            "research_only": self.RESEARCH_ONLY,
            "no_real_orders": self.NO_REAL_ORDERS,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _parse(self, ts: str) -> Optional[datetime]:
        """Parse ISO timestamp string to datetime."""
        if not ts:
            return None
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(ts[:19], fmt[:19])
            except ValueError:
                continue
        return None

    def _clamp(self, timestamp: str) -> str:
        """Clamp timestamp to [session_start, session_end]."""
        try:
            dt    = self._parse(timestamp)
            start = self._parse(self._session_start)
            end   = self._parse(self._session_end)
            if dt is None:
                return self._current
            if start and dt < start:
                return self._session_start
            if end and dt > end:
                return self._session_end
            return timestamp
        except Exception:
            return self._current

    def _session_status(self, timestamp: str) -> str:
        """Return session status for timestamp."""
        try:
            dt    = self._parse(timestamp)
            start = self._parse(self._session_start)
            end   = self._parse(self._session_end)
            if dt is None:
                return OUT_OF_SESSION
            if start and dt < start:
                return PRE_SESSION
            if end and dt > end:
                return POST_SESSION
            return IN_SESSION
        except Exception:
            return OUT_OF_SESSION

    def _timeframe_minutes(self, timeframe: str) -> int:
        """Return bar size in minutes for timeframe."""
        tf_map = {"D1": 390, "M60": 60, "M20": 20, "M5": 5, "M1": 1}
        return tf_map.get(timeframe.upper(), 1)
