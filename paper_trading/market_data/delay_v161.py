"""
paper_trading/market_data/delay_v161.py — Delay Measurement v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Measures event-level and feed-level delivery delay in milliseconds.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, Dict, List
from collections import deque

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True

DEFAULT_WINDOW_SIZE: int = 100


class DelayMeasurement:
    """
    Measures delivery delay: received_at - event_timestamp.
    Maintains rolling statistics over a sliding window.
    """

    def __init__(self, window_size: int = DEFAULT_WINDOW_SIZE) -> None:
        self._window: deque = deque(maxlen=window_size)
        self._total_measured: int = 0

    def measure_ms(
        self,
        event_timestamp_utc: str,
        received_at_utc: Optional[str] = None,
        clock_now_utc: Optional[callable] = None,
    ) -> Optional[int]:
        """
        Compute delay in milliseconds between event_timestamp and received_at (or now).
        Returns None if timestamps cannot be parsed.
        """
        try:
            event_dt = datetime.fromisoformat(event_timestamp_utc.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None

        if received_at_utc:
            try:
                recv_dt = datetime.fromisoformat(received_at_utc.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                recv_dt = None
        else:
            recv_dt = None

        if recv_dt is None:
            if clock_now_utc:
                recv_dt = clock_now_utc()
            else:
                recv_dt = datetime.now(timezone.utc)

        if not event_dt.tzinfo:
            event_dt = event_dt.replace(tzinfo=timezone.utc)
        if not recv_dt.tzinfo:
            recv_dt = recv_dt.replace(tzinfo=timezone.utc)

        delay_ms = int((recv_dt - event_dt).total_seconds() * 1000)
        self._window.append(delay_ms)
        self._total_measured += 1
        return delay_ms

    def get_stats(self) -> Dict[str, Optional[float]]:
        if not self._window:
            return {"min_ms": None, "max_ms": None, "mean_ms": None, "count": 0}
        vals = list(self._window)
        return {
            "min_ms": min(vals),
            "max_ms": max(vals),
            "mean_ms": sum(vals) / len(vals),
            "count": len(vals),
        }

    def reset(self) -> None:
        self._window.clear()
        self._total_measured = 0
