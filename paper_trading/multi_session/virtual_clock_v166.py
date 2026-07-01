"""
paper_trading/multi_session/virtual_clock_v166.py — Virtual Clock v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No real sleep. No real time.time() dependency for coordination decisions.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Optional

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_REAL_SLEEP = True


class VirtualClock:
    """
    Deterministic virtual clock for simulation.
    Advancing never sleeps. Time is driven by explicit tick() calls.
    """

    def __init__(self, start: Optional[datetime] = None) -> None:
        self._now = start or datetime(2024, 1, 2, 9, 30, 0, tzinfo=timezone.utc)

    @property
    def now(self) -> datetime:
        return self._now

    def tick(self, seconds: float = 1.0) -> datetime:
        self._now = self._now + timedelta(seconds=seconds)
        return self._now

    def advance_to(self, dt: datetime) -> None:
        if dt < self._now:
            raise ValueError(f"Cannot advance clock backwards: {dt} < {self._now}")
        self._now = dt

    def is_expired(self, expires_at: datetime) -> bool:
        return self._now >= expires_at

    def seconds_until(self, dt: datetime) -> float:
        return (dt - self._now).total_seconds()

    def elapsed_since(self, dt: datetime) -> float:
        return (self._now - dt).total_seconds()

    def snapshot(self) -> str:
        return self._now.isoformat()
