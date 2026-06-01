"""
data/providers/retry_policy.py - API retry / timeout / backoff shared policy (v0.4.1).

Used for read-only GET / safe fetch operations ONLY.
Never used for order submission or destructive operations.

[!] Read Only. No Real Orders.
[!] Retry is only applied to safe read/fetch operations.
"""
from __future__ import annotations

import logging
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Error classification constants
_RETRYABLE_STATUS   = {429, 500, 502, 503, 504}
_AUTH_STATUS        = {401, 403}
_CLIENT_ERROR       = {400, 404, 422}

ERR_TIMEOUT         = "TIMEOUT"
ERR_NETWORK         = "NETWORK"
ERR_RATE_LIMIT      = "RATE_LIMIT"
ERR_SERVER          = "SERVER_ERROR"
ERR_AUTH            = "AUTH_ERROR"
ERR_SCHEMA_CHANGED  = "SCHEMA_CHANGED"
ERR_CLIENT          = "CLIENT_ERROR"
ERR_UNKNOWN         = "UNKNOWN"


class RetryPolicy:
    """
    API retry / timeout / backoff shared policy.

    Parameters
    ----------
    max_retries      : Maximum retry attempts (default: 3)
    timeout_seconds  : Request timeout in seconds (default: 15)
    backoff_seconds  : Base backoff between retries (default: 1.5)
    retry_on_status  : HTTP status codes that trigger retry (default: 429, 500, 502, 503)

    Safety:
        - Only retries read-only GET / safe fetch operations.
        - Never retries order submission.
        - SCHEMA_CHANGED errors are flagged, not blindly retried.
    """

    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        max_retries:     int = 3,
        timeout_seconds: int = 15,
        backoff_seconds: float = 1.5,
        retry_on_status: Optional[List[int]] = None,
    ):
        self.max_retries      = max(0, max_retries)
        self.timeout_seconds  = max(1, timeout_seconds)
        self.backoff_seconds  = max(0.0, backoff_seconds)
        self._retry_on_status = set(retry_on_status) if retry_on_status else _RETRYABLE_STATUS.copy()

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run(self, func: Callable, *args: Any, **kwargs: Any) -> Tuple[Any, dict]:
        """
        Execute func(*args, **kwargs) with retry/backoff.

        Returns
        -------
        (result, diagnostics)
            result      : return value of func, or None on final failure
            diagnostics : dict with attempts, elapsed_seconds, final_status, error_type, retryable
        """
        start     = time.monotonic()
        attempt   = 0
        last_error: Optional[str] = None
        last_error_type: str = ERR_UNKNOWN
        last_status: Optional[int] = None

        while attempt <= self.max_retries:
            attempt += 1
            try:
                result = func(*args, **kwargs)
                elapsed = time.monotonic() - start
                return result, self._diag(attempt, elapsed, "OK", None, None, False)
            except Exception as exc:
                last_error = str(exc)
                last_error_type, last_status = self.classify_error(exc)
                elapsed = time.monotonic() - start

                retryable = self.should_retry(exc)

                if attempt > self.max_retries or not retryable:
                    break

                wait = self.backoff_seconds * (2 ** (attempt - 1))
                logger.debug(
                    "RetryPolicy: attempt %d/%d failed (%s) — retry in %.1fs",
                    attempt, self.max_retries + 1, last_error_type, wait,
                )
                time.sleep(wait)

        elapsed = time.monotonic() - start
        return None, self._diag(
            attempt, elapsed, "FAILED", last_error_type, last_error, False
        )

    def should_retry(self, error_or_status: Any) -> bool:
        """Return True if the error is retryable."""
        if isinstance(error_or_status, (int, float)):
            return int(error_or_status) in self._retry_on_status

        err_type, status = self.classify_error(error_or_status)

        if err_type == ERR_SCHEMA_CHANGED:
            return False  # never blindly retry schema errors
        if err_type in (ERR_AUTH, ERR_CLIENT):
            return False  # auth / bad request — no point retrying
        if err_type in (ERR_TIMEOUT, ERR_NETWORK, ERR_RATE_LIMIT, ERR_SERVER):
            return True

        if status is not None:
            return status in self._retry_on_status

        return False

    def classify_error(self, error: Any) -> Tuple[str, Optional[int]]:
        """
        Classify an exception as one of the ERR_* constants.

        Returns (error_type, http_status_or_None).
        """
        if error is None:
            return ERR_UNKNOWN, None

        err_str = str(error).lower()

        # HTTP status code extraction
        status: Optional[int] = None
        for candidate in [429, 500, 502, 503, 504, 401, 403, 400, 404, 422]:
            if str(candidate) in err_str:
                status = candidate
                break

        # Try to get status from requests.HTTPError
        try:
            resp = getattr(error, "response", None)
            if resp is not None and hasattr(resp, "status_code"):
                status = int(resp.status_code)
        except Exception:
            pass

        if status is not None:
            if status == 429:
                return ERR_RATE_LIMIT, status
            if status in _AUTH_STATUS:
                return ERR_AUTH, status
            if status in _CLIENT_ERROR:
                return ERR_CLIENT, status
            if status >= 500:
                return ERR_SERVER, status

        # Schema / structural errors
        for kw in ("schema", "keyerror", "column", "unexpected field", "missingkey", "missing column"):
            if kw in err_str:
                return ERR_SCHEMA_CHANGED, None

        # Timeout / connection
        for kw in ("timeout", "timed out", "read timeout", "connect timeout"):
            if kw in err_str:
                return ERR_TIMEOUT, None
        for kw in ("connection", "network", "connectionerror", "remotedisconnected", "ssl"):
            if kw in err_str:
                return ERR_NETWORK, None

        return ERR_UNKNOWN, None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _diag(
        attempts:       int,
        elapsed:        float,
        final_status:   str,
        error_type:     Optional[str],
        error_message:  Optional[str],
        retryable:      bool,
    ) -> dict:
        return {
            "attempts":        attempts,
            "elapsed_seconds": round(elapsed, 3),
            "final_status":    final_status,
            "error_type":      error_type,
            "error_message":   error_message,
            "retryable":       retryable,
        }
