"""
portfolio/walk_forward/calendar_v154.py — Walk-forward Calendar v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
Timezone: Asia/Taipei (UTC+8). Weekday-only trading calendar for fixtures.
"""
from __future__ import annotations
import datetime
from typing import Optional

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
CALENDAR_VERSION = "1.5.4"
TIMEZONE = "Asia/Taipei"
UTC_OFFSET_HOURS = 8


def _parse(date_str: str) -> datetime.date:
    return datetime.date.fromisoformat(date_str)


def _fmt(d: datetime.date) -> str:
    return d.isoformat()


class WalkForwardCalendar:
    """Simple walk-forward calendar. Fixtures use weekday-only (Mon-Fri)."""

    def __init__(self, timezone: str = "Asia/Taipei"):
        self.timezone = timezone
        self.calendar_version = CALENDAR_VERSION

    def is_trading_day(self, date_str: str) -> bool:
        """Return True if the date is a trading day (Mon-Fri, no specific holidays in fixture mode)."""
        d = _parse(date_str)
        return d.weekday() < 5  # Monday=0 ... Friday=4

    def next_trading_day(self, date_str: str) -> str:
        """Return the next trading day after date_str."""
        d = _parse(date_str) + datetime.timedelta(days=1)
        while d.weekday() >= 5:
            d += datetime.timedelta(days=1)
        return _fmt(d)

    def prev_trading_day(self, date_str: str) -> str:
        """Return the previous trading day before date_str."""
        d = _parse(date_str) - datetime.timedelta(days=1)
        while d.weekday() >= 5:
            d -= datetime.timedelta(days=1)
        return _fmt(d)

    def trading_days_between(self, start: str, end: str) -> int:
        """Return count of trading days in [start, end) (start inclusive, end exclusive)."""
        s = _parse(start)
        e = _parse(end)
        if s >= e:
            return 0
        count = 0
        cur = s
        while cur < e:
            if cur.weekday() < 5:
                count += 1
            cur += datetime.timedelta(days=1)
        return count

    def add_calendar_days(self, date_str: str, days: int) -> str:
        """Add calendar days to a date."""
        d = _parse(date_str) + datetime.timedelta(days=days)
        return _fmt(d)

    def add_trading_days(self, date_str: str, trading_days: int) -> str:
        """Add N trading days to a date."""
        d = _parse(date_str)
        added = 0
        while added < trading_days:
            d += datetime.timedelta(days=1)
            if d.weekday() < 5:
                added += 1
        return _fmt(d)
