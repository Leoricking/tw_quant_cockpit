"""
replay/timeframe_calendar.py — TaiwanReplayTradingCalendar v1.2.5

Taiwan stock market trading calendar for multi-timeframe replay.
Trading hours: 09:00–13:30 Asia/Taipei (Mon-Fri, excluding TW holidays).

Not Supported in v1.2.5: pre-market, after-hours, odd-lots, night session.
Not Investment Advice. Research Only.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
from datetime import date, datetime, time, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

TIMEZONE = "Asia/Taipei"
MARKET_OPEN_TIME  = time(9, 0, 0)
MARKET_CLOSE_TIME = time(13, 30, 0)

NOT_SUPPORTED_V1_2_5 = [
    "pre_market", "after_hours", "odd_lots", "night_session",
]

# Taiwan public holidays (simplified — major holidays only)
_TW_HOLIDAYS = {
    # 2023
    "2023-01-01", "2023-01-02", "2023-01-20", "2023-01-23",
    "2023-01-24", "2023-01-25", "2023-01-26", "2023-01-27",
    "2023-02-27", "2023-02-28", "2023-04-05",
    "2023-05-01", "2023-06-22", "2023-06-23",
    "2023-10-09", "2023-10-10",
    # 2024
    "2024-01-01", "2024-02-08", "2024-02-09", "2024-02-12",
    "2024-02-13", "2024-02-14",
    "2024-04-04", "2024-04-05",
    "2024-05-01", "2024-06-10",
    "2024-09-17", "2024-10-10",
    # 2025
    "2025-01-01", "2025-01-27", "2025-01-28", "2025-01-29",
    "2025-01-30", "2025-01-31",
    "2025-04-03", "2025-04-04",
    "2025-05-01", "2025-05-30",
    "2025-10-10",
}


class TaiwanReplayTradingCalendar:
    """
    Taiwan stock market trading calendar for replay.
    Trading hours: 09:00–13:30 Asia/Taipei, Mon-Fri (excluding holidays).

    Not Supported in v1.2.5: pre-market, after-hours, odd-lots, night session.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    NOT_SUPPORTED_V1_2_5 = NOT_SUPPORTED_V1_2_5

    def is_trading_day(self, d: Any) -> bool:
        """Return True if given date is a Taiwan trading day."""
        if isinstance(d, str):
            try:
                d = date.fromisoformat(d[:10])
            except ValueError:
                return False
        if isinstance(d, datetime):
            d = d.date()
        # Weekends
        if d.weekday() >= 5:
            return False
        # Holidays
        if d.isoformat() in _TW_HOLIDAYS:
            return False
        return True

    def is_market_time(self, timestamp: Any) -> bool:
        """Return True if timestamp falls within Taiwan market hours (09:00-13:30)."""
        dt = self._parse_dt(timestamp)
        if dt is None:
            return False
        if not self.is_trading_day(dt.date()):
            return False
        t = dt.time().replace(second=0, microsecond=0)
        return MARKET_OPEN_TIME <= t <= MARKET_CLOSE_TIME

    def session_date(self, timestamp: Any) -> Optional[str]:
        """Return session date string for timestamp, or None if out of session."""
        dt = self._parse_dt(timestamp)
        if dt is None:
            return None
        d = dt.date()
        if not self.is_trading_day(d):
            return None
        return d.isoformat()

    def market_open(self, d: Any) -> Optional[str]:
        """Return market open timestamp for date, or None if not a trading day."""
        if isinstance(d, str):
            try:
                d = date.fromisoformat(d[:10])
            except ValueError:
                return None
        if not self.is_trading_day(d):
            return None
        dt = datetime.combine(d, MARKET_OPEN_TIME)
        return dt.isoformat()

    def market_close(self, d: Any) -> Optional[str]:
        """Return market close timestamp for date, or None if not a trading day."""
        if isinstance(d, str):
            try:
                d = date.fromisoformat(d[:10])
            except ValueError:
                return None
        if not self.is_trading_day(d):
            return None
        dt = datetime.combine(d, MARKET_CLOSE_TIME)
        return dt.isoformat()

    def expected_bars(self, d: Any, timeframe: str) -> int:
        """Return expected number of bars for a full trading day and timeframe."""
        if not self.is_trading_day(d):
            return 0
        # TW market: 09:00–13:30 = 270 minutes
        session_minutes = 270
        tf_upper = timeframe.upper()
        minutes_map = {"D1": 270, "M60": 60, "M20": 20, "M5": 5, "M1": 1}
        minutes = minutes_map.get(tf_upper, 1)
        if tf_upper == "D1":
            return 1
        return session_minutes // minutes

    def previous_bar_time(self, timestamp: Any, timeframe: str) -> Optional[str]:
        """Return start of previous completed bar for given timeframe."""
        dt = self._parse_dt(timestamp)
        if dt is None:
            return None
        tf_upper = timeframe.upper()
        minutes_map = {"M60": 60, "M20": 20, "M5": 5, "M1": 1}
        minutes = minutes_map.get(tf_upper)
        if not minutes:
            return None
        aligned = self._align_to_bar_start(dt, minutes)
        prev = aligned - timedelta(minutes=minutes)
        return prev.isoformat()

    def next_bar_time(self, timestamp: Any, timeframe: str) -> Optional[str]:
        """Return start of next bar for given timeframe."""
        dt = self._parse_dt(timestamp)
        if dt is None:
            return None
        tf_upper = timeframe.upper()
        minutes_map = {"M60": 60, "M20": 20, "M5": 5, "M1": 1}
        minutes = minutes_map.get(tf_upper)
        if not minutes:
            return None
        aligned = self._align_to_bar_start(dt, minutes)
        nxt = aligned + timedelta(minutes=minutes)
        return nxt.isoformat()

    def align_to_bar_close(self, timestamp: Any, timeframe: str) -> Optional[str]:
        """Return close timestamp for bar containing given timestamp."""
        dt = self._parse_dt(timestamp)
        if dt is None:
            return None
        tf_upper = timeframe.upper()
        minutes_map = {"M60": 60, "M20": 20, "M5": 5, "M1": 1}
        minutes = minutes_map.get(tf_upper)
        if not minutes:
            return None
        aligned = self._align_to_bar_start(dt, minutes)
        close_dt = aligned + timedelta(minutes=minutes)
        return close_dt.isoformat()

    def is_bar_complete(
        self, timestamp: Any, replay_timestamp: Any, timeframe: str
    ) -> bool:
        """
        Return True if bar at 'timestamp' is completed as of 'replay_timestamp'.
        Bar is complete if its close time < replay_timestamp.
        """
        close_str = self.align_to_bar_close(timestamp, timeframe)
        if not close_str:
            return False
        replay_dt = self._parse_dt(replay_timestamp)
        close_dt = self._parse_dt(close_str)
        if replay_dt is None or close_dt is None:
            return False
        return close_dt <= replay_dt

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _parse_dt(self, timestamp: Any) -> Optional[datetime]:
        """Parse timestamp to naive datetime (treating as Asia/Taipei local time)."""
        if isinstance(timestamp, datetime):
            return timestamp.replace(tzinfo=None)
        if isinstance(timestamp, str):
            ts = timestamp.strip()
            # Remove timezone suffix for simple comparison
            for fmt in (
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d",
            ):
                try:
                    dt = datetime.strptime(ts[:19], fmt[:19])
                    return dt
                except ValueError:
                    continue
        return None

    def _align_to_bar_start(self, dt: datetime, minutes: int) -> datetime:
        """Align datetime to start of bar period."""
        total_minutes = dt.hour * 60 + dt.minute
        bar_start_minutes = (total_minutes // minutes) * minutes
        start_hour = bar_start_minutes // 60
        start_minute = bar_start_minutes % 60
        return dt.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
