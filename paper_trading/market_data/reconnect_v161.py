"""
paper_trading/market_data/reconnect_v161.py — Reconnect Policy v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
NO_RECONNECT / FIXED_INTERVAL / BOUNDED_EXPONENTIAL_BACKOFF.
Injectable clock — no real sleep in tests.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from paper_trading.market_data.enums_v161 import ReconnectPolicy

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True

DEFAULT_BASE_INTERVAL_S: int = 5
DEFAULT_MAX_INTERVAL_S: int = 120
DEFAULT_MAX_ATTEMPTS: int = 5
DEFAULT_BACKOFF_FACTOR: float = 2.0


class ReconnectState:
    def __init__(self) -> None:
        self.attempt_count: int = 0
        self.last_attempt_utc: Optional[str] = None
        self.next_attempt_interval_s: float = DEFAULT_BASE_INTERVAL_S
        self.exhausted: bool = False


class ReconnectManager:
    """
    Manages reconnect schedule according to policy.
    Injectable clock — no real sleep. Tests can advance time.
    """

    def __init__(
        self,
        policy: ReconnectPolicy,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        base_interval_s: float = DEFAULT_BASE_INTERVAL_S,
        max_interval_s: float = DEFAULT_MAX_INTERVAL_S,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
        clock_now_utc: Optional[callable] = None,
    ) -> None:
        self._policy = policy
        self._max_attempts = max_attempts
        self._base_interval = base_interval_s
        self._max_interval = max_interval_s
        self._backoff_factor = backoff_factor
        self._clock = clock_now_utc or (lambda: datetime.now(timezone.utc))
        self._state = ReconnectState()

    @property
    def policy(self) -> ReconnectPolicy:
        return self._policy

    def should_reconnect(self) -> bool:
        if self._policy == ReconnectPolicy.NO_RECONNECT:
            return False
        if self._state.exhausted:
            return False
        return self._state.attempt_count < self._max_attempts

    def record_attempt(self) -> None:
        self._state.attempt_count += 1
        self._state.last_attempt_utc = self._clock().isoformat()

        if self._policy == ReconnectPolicy.BOUNDED_EXPONENTIAL_BACKOFF:
            new_interval = min(
                self._state.next_attempt_interval_s * self._backoff_factor,
                self._max_interval,
            )
            self._state.next_attempt_interval_s = new_interval
        else:
            self._state.next_attempt_interval_s = self._base_interval

        if self._state.attempt_count >= self._max_attempts:
            self._state.exhausted = True

    def get_next_interval_s(self) -> float:
        if self._policy == ReconnectPolicy.NO_RECONNECT:
            return 0.0
        if self._policy == ReconnectPolicy.FIXED_INTERVAL:
            return self._base_interval
        return self._state.next_attempt_interval_s

    def reset(self) -> None:
        self._state = ReconnectState()

    def get_status(self) -> Dict[str, Any]:
        return {
            "policy": self._policy.value,
            "attempt_count": self._state.attempt_count,
            "max_attempts": self._max_attempts,
            "exhausted": self._state.exhausted,
            "next_interval_s": self.get_next_interval_s(),
            "should_reconnect": self.should_reconnect(),
        }
