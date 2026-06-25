"""
paper_trading/market_data/calendar_v161.py — Taiwan Market Calendar v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
TWSE/TPEX session windows. No auto-trading. Research only.
"""
from __future__ import annotations
from datetime import datetime, time, timezone
from typing import Optional, Tuple

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True

# Taiwan Standard Time offset: UTC+8
TW_UTC_OFFSET_HOURS: int = 8

# TWSE/TPEX regular session: 09:00–13:30 TST
TWSE_OPEN_TST: time = time(9, 0, 0)
TWSE_CLOSE_TST: time = time(13, 30, 0)

# Pre-market auction: 08:30–09:00 TST
PREMARKET_OPEN_TST: time = time(8, 30, 0)

# After-hours: 14:00–14:30 TST
AFTERHOURS_OPEN_TST: time = time(14, 0, 0)
AFTERHOURS_CLOSE_TST: time = time(14, 30, 0)


class TaiwanMarketCalendar:
    """
    Taiwan market session calendar.
    Determines session windows for TWSE/TPEX.
    No trading execution — research only.
    """

    def is_trading_day(self, dt: datetime) -> bool:
        """Returns True if dt is a weekday (Mon-Fri). Does not account for holidays."""
        return dt.weekday() < 5

    def is_regular_session(self, dt_utc: datetime) -> bool:
        """True if dt_utc is within TWSE regular session (09:00-13:30 TST)."""
        from datetime import timedelta
        tst = dt_utc + timedelta(hours=TW_UTC_OFFSET_HOURS)
        if not self.is_trading_day(tst):
            return False
        t = tst.time()
        return TWSE_OPEN_TST <= t < TWSE_CLOSE_TST

    def is_premarket_session(self, dt_utc: datetime) -> bool:
        """True if dt_utc is within pre-market auction (08:30-09:00 TST)."""
        from datetime import timedelta
        tst = dt_utc + timedelta(hours=TW_UTC_OFFSET_HOURS)
        if not self.is_trading_day(tst):
            return False
        t = tst.time()
        return PREMARKET_OPEN_TST <= t < TWSE_OPEN_TST

    def is_afterhours_session(self, dt_utc: datetime) -> bool:
        """True if dt_utc is within after-hours session (14:00-14:30 TST)."""
        from datetime import timedelta
        tst = dt_utc + timedelta(hours=TW_UTC_OFFSET_HOURS)
        if not self.is_trading_day(tst):
            return False
        t = tst.time()
        return AFTERHOURS_OPEN_TST <= t <= AFTERHOURS_CLOSE_TST

    def get_session_label(self, dt_utc: datetime) -> str:
        if self.is_regular_session(dt_utc):
            return "REGULAR"
        if self.is_premarket_session(dt_utc):
            return "PREMARKET"
        if self.is_afterhours_session(dt_utc):
            return "AFTERHOURS"
        if self.is_trading_day(dt_utc):
            return "CLOSED"
        return "WEEKEND"

    def utc_to_tst_iso(self, dt_utc: datetime) -> str:
        from datetime import timedelta
        tst = dt_utc + timedelta(hours=TW_UTC_OFFSET_HOURS)
        return tst.isoformat()
