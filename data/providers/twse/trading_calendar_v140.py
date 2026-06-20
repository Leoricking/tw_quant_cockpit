"""
data/providers/twse/trading_calendar_v140.py — TWSE trading calendar v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Calendar uses heuristic. Always approximate=True unless official data loaded.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Known Taiwan public holidays (approximate list; heuristic always returns approximate=True)
# Format: (month, day) tuples for recurring holidays, "YYYY-MM-DD" for specific dates
_RECURRING_HOLIDAYS = {
    (1, 1),   # New Year's Day
    (2, 28),  # Peace Memorial Day
    (4, 4),   # Children's Day
    (4, 5),   # Qingming Festival (approximate; can vary)
    (6, 18),  # Dragon Boat Festival (approximate; lunar)
    (9, 28),  # Confucius Day / Teacher's Day (not always public holiday)
    (10, 10), # National Day
    (12, 25), # Constitution Day (not a trading holiday; kept for reference)
}

# Known non-trading dates for specific years (month/day)
_SPECIFIC_HOLIDAYS: Dict[str, str] = {
    "2024-01-01": "元旦",
    "2024-02-08": "農曆除夕",
    "2024-02-09": "春節",
    "2024-02-10": "春節",
    "2024-02-11": "春節",
    "2024-02-12": "春節",
    "2024-02-13": "春節",
    "2024-02-14": "春節",
    "2024-02-28": "和平紀念日",
    "2024-04-04": "兒童節",
    "2024-04-05": "清明節",
    "2024-06-10": "端午節",
    "2024-09-17": "中秋節",
    "2024-10-10": "國慶日",
    "2025-01-01": "元旦",
    "2025-01-27": "農曆除夕",
    "2025-01-28": "春節",
    "2025-01-29": "春節",
    "2025-01-30": "春節",
    "2025-01-31": "春節",
    "2025-02-03": "春節補假",
    "2025-02-28": "和平紀念日",
    "2025-04-03": "兒童節補假",
    "2025-04-04": "兒童節",
    "2025-05-30": "端午節補假",
    "2025-10-10": "國慶日",
}


class TWSETradingCalendar:
    """
    TWSE trading calendar based on heuristic rules.

    Always returns approximate=True because we use heuristic (weekend + known holidays).
    Official data must be loaded separately to achieve non-approximate status.
    Timezone: Asia/Taipei (UTC+8 fixed offset).
    """

    _UTC8 = datetime.timezone(datetime.timedelta(hours=8))

    def __init__(self) -> None:
        self._clock_fn: Optional[Callable] = None
        self._official_loaded = False

    def inject_clock(self, clock_fn: Callable[[], datetime.datetime]) -> None:
        """Inject a clock function for testing."""
        self._clock_fn = clock_fn

    def _now(self) -> datetime.datetime:
        if self._clock_fn is not None:
            return self._clock_fn()
        return datetime.datetime.now(self._UTC8)

    def _parse_date(self, date_str: str) -> datetime.date:
        return datetime.date.fromisoformat(date_str)

    def is_trading_day(self, date: str) -> Dict[str, Any]:
        """
        Return dict with keys: is_trading_day, source, approximate, holiday_name.
        """
        d = self._parse_date(date)
        # Weekend check
        if d.weekday() >= 5:  # Saturday=5, Sunday=6
            return {
                "is_trading_day": False,
                "source": "heuristic",
                "approximate": True,
                "holiday_name": "Weekend",
            }
        # Specific holiday check
        holiday_name = _SPECIFIC_HOLIDAYS.get(date)
        if holiday_name:
            return {
                "is_trading_day": False,
                "source": "heuristic",
                "approximate": True,
                "holiday_name": holiday_name,
            }
        return {
            "is_trading_day": True,
            "source": "heuristic",
            "approximate": True,
            "holiday_name": None,
        }

    def previous_trading_day(self, date: str) -> str:
        """Return the previous trading day before the given date."""
        d = self._parse_date(date) - datetime.timedelta(days=1)
        for _ in range(30):
            result = self.is_trading_day(d.isoformat())
            if result["is_trading_day"]:
                return d.isoformat()
            d -= datetime.timedelta(days=1)
        # fallback
        return (self._parse_date(date) - datetime.timedelta(days=1)).isoformat()

    def next_trading_day(self, date: str) -> str:
        """Return the next trading day after the given date."""
        d = self._parse_date(date) + datetime.timedelta(days=1)
        for _ in range(30):
            result = self.is_trading_day(d.isoformat())
            if result["is_trading_day"]:
                return d.isoformat()
            d += datetime.timedelta(days=1)
        # fallback
        return (self._parse_date(date) + datetime.timedelta(days=1)).isoformat()

    def count_trading_days(self, start: str, end: str) -> int:
        """Count trading days between start and end (inclusive)."""
        d = self._parse_date(start)
        end_d = self._parse_date(end)
        count = 0
        while d <= end_d:
            if self.is_trading_day(d.isoformat())["is_trading_day"]:
                count += 1
            d += datetime.timedelta(days=1)
        return count

    def official_holiday_name(self, date: str) -> Optional[str]:
        """Return official holiday name if known, else None."""
        return _SPECIFIC_HOLIDAYS.get(date)

    def calendar_source(self) -> str:
        """Return description of calendar source."""
        return "heuristic (Asia/Taipei UTC+8; weekend + known Taiwan holidays)"

    def approximate(self) -> bool:
        """Returns True when using heuristic calendar (always for now)."""
        return not self._official_loaded
