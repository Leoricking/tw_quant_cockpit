"""
data/providers/finmind/quota_v144.py — FinMind quota tracking v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] EXHAUSTED → stop non-essential prefetch, no retry, no token rotation, no mock fallback.
[!] plan_unknown=True by default (FinMind does not expose plan tier in response).
"""
from __future__ import annotations

import datetime
import logging
from typing import Any, Dict, Optional

from data.providers.finmind.models_v144 import FinMindQuotaState, FinMindQuotaStatus

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

ANONYMOUS_DEFAULT_LIMIT_PER_HOUR = 300
AUTHENTICATED_DEFAULT_LIMIT_PER_HOUR = 600


class FinMindQuotaManager:
    """
    Tracks FinMind API quota usage.
    Defaults are conservative estimates — actual plan limits may differ.
    plan_unknown=True means we cannot assert actual limits.
    """

    def __init__(
        self,
        anonymous_limit: int = ANONYMOUS_DEFAULT_LIMIT_PER_HOUR,
        authenticated_limit: int = AUTHENTICATED_DEFAULT_LIMIT_PER_HOUR,
        authenticated: bool = False,
    ) -> None:
        self._anonymous_limit = anonymous_limit
        self._authenticated_limit = authenticated_limit
        self._authenticated = authenticated
        self._used: int = 0
        self._limit: Optional[int] = None  # updated from API response if available
        self._quota_reset_at: Optional[str] = None
        self._quota_source: str = "DEFAULT_ESTIMATE"
        self._last_checked_at: Optional[str] = None
        self._last_quota_error: Optional[str] = None
        self._plan_unknown: bool = True

    def _now_iso(self) -> str:
        return datetime.datetime.now(datetime.timezone.utc).isoformat()

    @property
    def _effective_limit(self) -> int:
        if self._limit is not None:
            return self._limit
        return self._authenticated_limit if self._authenticated else self._anonymous_limit

    def record_request(self) -> None:
        """Record a single API request."""
        self._used += 1
        self._last_checked_at = self._now_iso()

    def record_quota_error(self, message: str = "") -> None:
        """Record a quota-exceeded error."""
        self._last_quota_error = message or "QUOTA_EXCEEDED"
        self._last_checked_at = self._now_iso()
        logger.warning("FinMind quota error recorded: %s", message)

    def get_status(self) -> FinMindQuotaState:
        """Return current quota state."""
        remaining = max(0, self._effective_limit - self._used)
        if self._last_quota_error:
            status = FinMindQuotaStatus.EXHAUSTED
        elif remaining == 0:
            status = FinMindQuotaStatus.EXHAUSTED
        elif remaining < self._effective_limit * 0.1:
            status = FinMindQuotaStatus.LOW
        elif self._plan_unknown:
            status = FinMindQuotaStatus.UNKNOWN
        else:
            status = FinMindQuotaStatus.AVAILABLE

        return FinMindQuotaState(
            quota_limit=self._effective_limit,
            quota_used=self._used,
            quota_remaining=remaining,
            quota_reset_at=self._quota_reset_at,
            quota_source=self._quota_source,
            plan_unknown=self._plan_unknown,
            last_checked_at=self._last_checked_at,
            last_quota_error=self._last_quota_error,
            status=status,
        )

    def update_from_response(self, response_headers: Dict[str, Any]) -> None:
        """
        Update quota state from API response headers if present.
        FinMind v4 may return X-RateLimit-* headers.
        """
        if not response_headers:
            return
        limit_str = (
            response_headers.get("X-RateLimit-Limit")
            or response_headers.get("x-ratelimit-limit")
        )
        remaining_str = (
            response_headers.get("X-RateLimit-Remaining")
            or response_headers.get("x-ratelimit-remaining")
        )
        reset_str = (
            response_headers.get("X-RateLimit-Reset")
            or response_headers.get("x-ratelimit-reset")
        )
        if limit_str is not None:
            try:
                self._limit = int(limit_str)
                self._quota_source = "API_RESPONSE_HEADER"
                self._plan_unknown = False
            except (ValueError, TypeError):
                pass
        if remaining_str is not None:
            try:
                remaining = int(remaining_str)
                self._used = max(0, (self._limit or self._effective_limit) - remaining)
            except (ValueError, TypeError):
                pass
        if reset_str is not None:
            self._quota_reset_at = str(reset_str)
        self._last_checked_at = self._now_iso()

    def is_exhausted(self) -> bool:
        return self.get_status().status == FinMindQuotaStatus.EXHAUSTED
