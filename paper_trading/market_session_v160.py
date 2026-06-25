"""paper_trading/market_session_v160.py — Taiwan Market Session Calendar v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
Market timezone: Asia/Taipei
"""
from __future__ import annotations
import datetime
from typing import Optional, Protocol

from .enums_v160 import MarketSessionStatus

# TWSE trading hours (Asia/Taipei)
_PRE_OPEN_START = datetime.time(8, 30)
_REGULAR_OPEN = datetime.time(9, 0)
_REGULAR_CLOSE = datetime.time(13, 30)
_BREAK_START = None  # No mid-day break for TWSE regular session

# Taiwan weekdays: Mon=0 ... Fri=4, Sat=5, Sun=6
_TRADING_WEEKDAYS = {0, 1, 2, 3, 4}


class MarketCalendarProvider(Protocol):
    def is_trading_day(self, date: datetime.date) -> bool: ...
    def get_status(self, dt: datetime.datetime) -> MarketSessionStatus: ...


class TWFixtureCalendar:
    """Fixture calendar for tests — all weekdays are trading days."""

    def is_trading_day(self, date: datetime.date) -> bool:
        return date.weekday() in _TRADING_WEEKDAYS

    def get_status(self, dt: datetime.datetime) -> MarketSessionStatus:
        if not self.is_trading_day(dt.date()):
            return MarketSessionStatus.NON_TRADING_DAY
        t = dt.time()
        if t < _PRE_OPEN_START:
            return MarketSessionStatus.CLOSED
        if _PRE_OPEN_START <= t < _REGULAR_OPEN:
            return MarketSessionStatus.PRE_OPEN
        if _REGULAR_OPEN <= t <= _REGULAR_CLOSE:
            return MarketSessionStatus.OPEN
        return MarketSessionStatus.CLOSED


class TWMarketSessionState:
    """
    Taiwan stock market session state.
    Calendar provider is replaceable; fixture calendar used for offline tests.
    """

    def __init__(self, calendar: Optional[MarketCalendarProvider] = None) -> None:
        self._calendar: MarketCalendarProvider = calendar or TWFixtureCalendar()
        self._current_status: MarketSessionStatus = MarketSessionStatus.UNKNOWN

    def update(self, dt: Optional[datetime.datetime] = None) -> MarketSessionStatus:
        if dt is None:
            self._current_status = MarketSessionStatus.UNKNOWN
            return self._current_status
        self._current_status = self._calendar.get_status(dt)
        return self._current_status

    def get_status(self) -> MarketSessionStatus:
        return self._current_status

    def is_trading_open(self) -> bool:
        return self._current_status == MarketSessionStatus.OPEN

    def can_simulate_fill(self, dt: Optional[datetime.datetime] = None) -> bool:
        """Only OPEN session can simulate fills."""
        if dt is not None:
            status = self._calendar.get_status(dt)
        else:
            status = self._current_status
        return status == MarketSessionStatus.OPEN

    def is_trading_day(self, date: datetime.date) -> bool:
        return self._calendar.is_trading_day(date)
