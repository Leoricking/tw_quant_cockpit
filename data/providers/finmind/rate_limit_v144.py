"""
data/providers/finmind/rate_limit_v144.py — FinMind rate limit handling v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Injectable clock/sleeper for tests — no actual sleep in tests.
[!] Respects Retry-After header on 429. Exponential backoff with jitter.
"""
from __future__ import annotations

import logging
import random
import time
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_DEFAULT_MAX_RETRIES = 3
_DEFAULT_BASE_DELAY = 2.0  # seconds
_DEFAULT_MAX_DELAY = 120.0  # seconds
_DEFAULT_JITTER_FACTOR = 0.25


class FinMindRateLimitHandler:
    """
    Handles rate limiting and exponential backoff for FinMind API requests.
    Injectable clock and sleeper for deterministic testing.
    """

    def __init__(
        self,
        max_retries: int = _DEFAULT_MAX_RETRIES,
        base_delay: float = _DEFAULT_BASE_DELAY,
        max_delay: float = _DEFAULT_MAX_DELAY,
        jitter_factor: float = _DEFAULT_JITTER_FACTOR,
        clock: Optional[Callable[[], float]] = None,
        sleeper: Optional[Callable[[float], None]] = None,
    ) -> None:
        self._max_retries = max_retries
        self._base_delay = base_delay
        self._max_delay = max_delay
        self._jitter_factor = jitter_factor
        self._clock = clock or time.monotonic
        self._sleeper = sleeper or time.sleep
        self._attempt_count: int = 0
        self._last_retry_after: Optional[int] = None

    def should_retry(self, attempt: int, error_code: str) -> bool:
        """Return True if another attempt should be made."""
        retryable_codes = {"RATE_LIMITED", "SERVICE_UNAVAILABLE", "TIMEOUT", "NETWORK_ERROR"}
        if error_code not in retryable_codes:
            return False
        return attempt < self._max_retries

    def compute_delay(self, attempt: int, retry_after: Optional[int] = None) -> float:
        """
        Compute delay in seconds for given attempt.
        Respects Retry-After header if provided.
        Uses exponential backoff with jitter otherwise.
        """
        if retry_after is not None and retry_after > 0:
            return float(min(retry_after, self._max_delay))
        delay = self._base_delay * (2 ** attempt)
        jitter = random.uniform(0, delay * self._jitter_factor)
        return min(delay + jitter, self._max_delay)

    def wait(self, attempt: int, retry_after: Optional[int] = None) -> float:
        """Wait appropriate time and return the delay applied."""
        delay = self.compute_delay(attempt, retry_after)
        logger.debug("FinMind rate limit: attempt=%d delay=%.1fs", attempt, delay)
        self._sleeper(delay)
        self._attempt_count += 1
        self._last_retry_after = retry_after
        return delay

    def extract_retry_after(self, headers: Dict[str, Any]) -> Optional[int]:
        """Extract Retry-After header value in seconds."""
        raw = headers.get("Retry-After") or headers.get("retry-after")
        if raw is None:
            return None
        try:
            return int(raw)
        except (ValueError, TypeError):
            return None

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_waits": self._attempt_count,
            "max_retries": self._max_retries,
            "base_delay": self._base_delay,
            "max_delay": self._max_delay,
            "last_retry_after": self._last_retry_after,
        }
