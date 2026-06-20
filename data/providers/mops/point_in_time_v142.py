"""
data/providers/mops/point_in_time_v142.py — MOPS point-in-time availability service v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
Clock is injectable for deterministic tests.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# MOPS disclosure schedule (approximate deadlines in CE calendar)
# Monthly revenue: disclosed by 10th of next month
# Q1 (Jan-Mar): deadline May 15
# Q2 (Apr-Jun): deadline Aug 14
# Q3 (Jul-Sep): deadline Nov 14
# Annual (Jan-Dec): deadline Mar 31 of next year

_MONTHLY_REVENUE_DAY = 10  # day of following month

_QUARTERLY_DEADLINES = {
    "Q1": (5, 15),   # May 15
    "Q2": (8, 14),   # Aug 14
    "Q3": (11, 14),  # Nov 14
    "Q4": (3, 31),   # Mar 31 next year (annual is Q4 equivalent)
    "ANNUAL": (3, 31),
}


def _default_clock() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class MOPSPointInTimeService:
    """
    Determines MOPS data availability at a given point in time.
    Clock is injectable: pass clock=lambda: your_datetime for deterministic tests.
    """

    def __init__(self, clock: Optional[Callable[[], datetime.datetime]] = None) -> None:
        self._clock = clock or _default_clock

    def now(self) -> datetime.datetime:
        return self._clock()

    def is_monthly_revenue_available(
        self, year: int, month: int, asof: Optional[datetime.datetime] = None
    ) -> Dict[str, Any]:
        """
        Check if monthly revenue for year/month is available as of asof date.
        Available after the 10th of the following month.
        """
        if asof is None:
            asof = self.now()

        # Availability: next month's 10th
        if month == 12:
            avail_year = year + 1
            avail_month = 1
        else:
            avail_year = year
            avail_month = month + 1

        avail_date = datetime.datetime(avail_year, avail_month, _MONTHLY_REVENUE_DAY, 0, 0, 0, tzinfo=datetime.timezone.utc)
        available = asof >= avail_date

        return {
            "year": year,
            "month": month,
            "available": available,
            "available_from": avail_date.date().isoformat(),
            "asof": asof.date().isoformat(),
            "data_type": "monthly_revenue",
        }

    def is_financial_report_available(
        self,
        fiscal_year: int,
        fiscal_period: str,
        asof: Optional[datetime.datetime] = None,
    ) -> Dict[str, Any]:
        """
        Check if financial report for fiscal_year/period is available as of asof date.
        """
        if asof is None:
            asof = self.now()

        deadline = _QUARTERLY_DEADLINES.get(fiscal_period)
        if deadline is None:
            return {
                "fiscal_year": fiscal_year,
                "fiscal_period": fiscal_period,
                "available": False,
                "available_from": None,
                "asof": asof.date().isoformat(),
                "data_type": "financial_report",
                "error": f"Unknown fiscal period: {fiscal_period}",
            }

        avail_month, avail_day = deadline
        if fiscal_period in ("Q4", "ANNUAL"):
            avail_year = fiscal_year + 1
        else:
            avail_year = fiscal_year

        try:
            avail_date = datetime.datetime(avail_year, avail_month, avail_day, 0, 0, 0, tzinfo=datetime.timezone.utc)
        except ValueError:
            avail_date = datetime.datetime(avail_year, avail_month, 28, 0, 0, 0, tzinfo=datetime.timezone.utc)

        available = asof >= avail_date

        return {
            "fiscal_year": fiscal_year,
            "fiscal_period": fiscal_period,
            "available": available,
            "available_from": avail_date.date().isoformat(),
            "asof": asof.date().isoformat(),
            "data_type": "financial_report",
        }

    def get_available_periods_as_of(
        self, fiscal_year: int, asof: Optional[datetime.datetime] = None
    ) -> Dict[str, Any]:
        """Return which periods are available for a fiscal year as of asof date."""
        if asof is None:
            asof = self.now()
        result = {}
        for period in ("Q1", "Q2", "Q3", "Q4", "ANNUAL"):
            info = self.is_financial_report_available(fiscal_year, period, asof)
            result[period] = info["available"]
        return {
            "fiscal_year": fiscal_year,
            "asof": asof.date().isoformat(),
            "available_periods": result,
        }
