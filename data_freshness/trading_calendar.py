"""
data_freshness/trading_calendar.py — Trading calendar for Taiwan stock market.
[!] No official TWSE holiday list included. Uses weekday heuristic + approximate=True.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone
from typing import List, Optional, Set

logger = logging.getLogger(__name__)

# Taiwan stock market approximate parameters
MARKET_TZ_OFFSET_HOURS  = 8     # UTC+8
MARKET_CLOSE_GRACE_HOURS = 2    # After 2pm, expect today's close available
MARKET_OPEN_HOUR_LOCAL   = 9
MARKET_CLOSE_HOUR_LOCAL  = 14   # conservative: data typically finalized by 2pm


class TradingCalendar:
    """
    Taiwan stock market trading calendar.

    Uses weekday heuristic (Mon-Fri) when no official holiday data is loaded.
    approximate=True when using heuristic — report clearly warns users.

    [!] Cannot account for Taiwan national holidays without an official list.
    [!] Does NOT auto-connect to external services to fetch holiday data.
    [!] When approximate=True: do NOT claim precise SLA compliance.
    """

    def __init__(self, holidays: Optional[Set[date]] = None):
        self._holidays: Set[date] = holidays or set()
        self._approximate: bool = len(self._holidays) == 0
        self._source: str = (
            "weekday_heuristic" if self._approximate else "provided_holiday_list"
        )

    def load_holidays(self, holiday_dates: List[date]) -> None:
        """Load a set of known holiday dates. Reduces approximation."""
        self._holidays = set(holiday_dates)
        if self._holidays:
            self._approximate = False
            self._source = "provided_holiday_list"

    def calendar_source(self) -> str:
        return self._source

    def is_approximate(self) -> bool:
        return self._approximate

    def is_trading_day(self, d: date) -> bool:
        """Return True if d is a trading day (Mon-Fri, not a holiday)."""
        if d.weekday() >= 5:   # Saturday=5, Sunday=6
            return False
        if d in self._holidays:
            return False
        return True

    def previous_trading_day(self, d: date) -> date:
        """Return the most recent trading day strictly before d."""
        candidate = d - timedelta(days=1)
        for _ in range(14):   # look back at most 2 weeks
            if self.is_trading_day(candidate):
                return candidate
            candidate -= timedelta(days=1)
        return candidate      # fallback

    def expected_latest_trading_day(self, now: Optional[datetime] = None) -> date:
        """
        Return the expected latest trading day for which data should be available.

        If market close grace period has not passed today, return previous trading day.
        [!] approximate=True when no holiday calendar is loaded.
        """
        if now is None:
            now = datetime.now(timezone.utc)
        # Convert UTC to Taiwan time (UTC+8)
        taiwan_now = now + timedelta(hours=MARKET_TZ_OFFSET_HOURS)
        today = taiwan_now.date()
        today_hour = taiwan_now.hour

        if (
            self.is_trading_day(today)
            and today_hour >= (MARKET_CLOSE_HOUR_LOCAL + MARKET_CLOSE_GRACE_HOURS)
        ):
            return today
        return self.previous_trading_day(today)

    def trading_days_between(self, start: date, end: date) -> int:
        """Count trading days in [start, end] inclusive."""
        if start > end:
            return 0
        count = 0
        current = start
        while current <= end:
            if self.is_trading_day(current):
                count += 1
            current += timedelta(days=1)
        return count

    def trading_day_lag(
        self, actual_date: Optional[date], expected_date: date
    ) -> Optional[int]:
        """
        Calculate trading-day lag between actual_date and expected_date.
        Returns None if actual_date is None.
        Returns negative if actual_date > expected_date (future date).
        """
        if actual_date is None:
            return None
        if actual_date > expected_date:
            return -self.trading_days_between(expected_date, actual_date)
        return self.trading_days_between(actual_date, expected_date) - 1
