"""
paper_trading/strategy/rate_limit_v162.py — Rate limiter for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
import threading
from collections import deque
from datetime import datetime, timedelta, timezone
from typing import Any, Deque, Dict

logger = logging.getLogger(__name__)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class RateLimiter:
    """
    Sliding-window rate limiter for paper strategy signals.

    Limits the number of signals processed per rolling 60-second window.
    Thread-safe.
    """

    def __init__(self, max_per_minute: int = 10) -> None:
        assert max_per_minute > 0, "max_per_minute must be positive"
        self.max_per_minute = max_per_minute
        self._lock = threading.Lock()
        self._window: Deque[datetime] = deque()
        self._total_allowed: int = 0
        self._total_blocked: int = 0

    def _prune(self) -> None:
        """Remove entries older than 60 seconds. Must hold lock."""
        cutoff = _utcnow() - timedelta(seconds=60)
        while self._window and self._window[0] < cutoff:
            self._window.popleft()

    def is_limited(self) -> bool:
        """Return True if the rate limit is currently exceeded."""
        with self._lock:
            self._prune()
            return len(self._window) >= self.max_per_minute

    def try_acquire(self) -> bool:
        """
        Attempt to consume one rate-limit slot.
        Returns True if allowed, False if rate limited.
        """
        with self._lock:
            self._prune()
            if len(self._window) >= self.max_per_minute:
                self._total_blocked += 1
                logger.debug(
                    "[v1.6.2][rate_limit] Blocked (window=%d/%d)",
                    len(self._window), self.max_per_minute
                )
                return False
            self._window.append(_utcnow())
            self._total_allowed += 1
            return True

    def current_rate(self) -> int:
        """Return the number of signals in the current 60-second window."""
        with self._lock:
            self._prune()
            return len(self._window)

    def headroom(self) -> int:
        """Return remaining slots in the current window."""
        with self._lock:
            self._prune()
            return max(0, self.max_per_minute - len(self._window))

    def reset(self) -> None:
        with self._lock:
            self._window.clear()

    def snapshot(self) -> list:
        """Return list of ISO timestamps for checkpointing."""
        with self._lock:
            return [
                dt.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
                for dt in self._window
            ]

    def restore(self, snapshot: list) -> None:
        """Restore from a checkpoint snapshot."""
        with self._lock:
            self._window = deque()
            for iso in snapshot:
                try:
                    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
                    self._window.append(dt)
                except ValueError:
                    pass

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            self._prune()
            return {
                "max_per_minute": self.max_per_minute,
                "current_window_size": len(self._window),
                "total_allowed": self._total_allowed,
                "total_blocked": self._total_blocked,
                "headroom": max(0, self.max_per_minute - len(self._window)),
                "paper_only": True,
            }
