"""
paper_trading/market_data/session_clock_v161.py — Session Clock v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Injectable clock for deterministic testing (no real sleep).
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, Callable

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


class MarketDataSessionClock:
    """
    Injectable clock for market data sessions.
    Supports real-time mode (uses datetime.now) and injected time for testing.
    No real sleep in test mode.
    """

    def __init__(self, time_provider: Optional[Callable[[], datetime]] = None) -> None:
        self._time_provider = time_provider or (lambda: datetime.now(timezone.utc))
        self._injected_time: Optional[datetime] = None

    def now(self) -> datetime:
        if self._injected_time is not None:
            return self._injected_time
        return self._time_provider()

    def now_utc_iso(self) -> str:
        return self.now().isoformat()

    def set_time(self, dt: datetime) -> None:
        """Inject a fixed time (for tests). No real sleep required."""
        self._injected_time = dt

    def advance(self, seconds: float) -> None:
        """Advance injected time by seconds (for reconnect tests). No real sleep."""
        if self._injected_time is None:
            self._injected_time = self.now()
        from datetime import timedelta
        self._injected_time = self._injected_time + timedelta(seconds=seconds)

    def reset(self) -> None:
        """Reset to real-time mode."""
        self._injected_time = None

    def elapsed_seconds(self, since_utc_iso: str) -> float:
        """Compute elapsed seconds from an ISO-8601 timestamp to now."""
        try:
            since = datetime.fromisoformat(since_utc_iso.replace("Z", "+00:00"))
            delta = self.now() - since
            return delta.total_seconds()
        except Exception:
            return 0.0
