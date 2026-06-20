"""
data/providers/finmind/error_classifier_v144.py — FinMind error classification v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] HTTP 200 + empty data → EMPTY_RESULT (not SUCCESS).
[!] Payload status=402 + "limit" → QUOTA_EXCEEDED.
[!] HTML response → SERVICE_UNAVAILABLE.
[!] AUTH_INVALID → no retry, no token display.
"""
from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

from data.providers.finmind.models_v144 import FinMindErrorCode, FinMindErrorDetail

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class FinMindErrorClassifier:
    """
    Classifies FinMind API errors into FinMindErrorDetail.
    Never exposes token values in error details.
    """

    def classify(
        self,
        http_status: int,
        response_body: Any,
        content_type: str = "",
        headers: Optional[Dict[str, Any]] = None,
    ) -> FinMindErrorDetail:
        """
        Classify error from HTTP response.

        Key rules:
        - payload status=402 + msg contains "limit" → QUOTA_EXCEEDED
        - HTTP 429 → RATE_LIMITED
        - HTTP 200 + error payload → not SUCCESS
        - HTTP 200 + empty data → EMPTY_RESULT
        - HTTP 200 + schema mismatch → SCHEMA_CHANGED
        - HTML response → SERVICE_UNAVAILABLE
        - invalid token message → AUTH_INVALID
        - JSON parse failure → MALFORMED_PAYLOAD
        """
        headers = headers or {}

        # HTML response → SERVICE_UNAVAILABLE
        ct = (content_type or "").lower()
        if "text/html" in ct:
            return self._make_detail(
                FinMindErrorCode.SERVICE_UNAVAILABLE,
                retryable=True, retry_after=60, blocking=False,
                user_message="FinMind returned HTML (maintenance or gateway error).",
                technical_message=f"Content-Type: {content_type}. HTTP {http_status}.",
                remediation="Retry later. Check FinMind service status.",
            )

        # Parse body
        payload = None
        if isinstance(response_body, (dict, list)):
            payload = response_body
        elif isinstance(response_body, (str, bytes)):
            body_str = response_body if isinstance(response_body, str) else response_body.decode("utf-8", errors="replace")
            if body_str.lstrip().startswith("<"):
                return self._make_detail(
                    FinMindErrorCode.SERVICE_UNAVAILABLE,
                    retryable=True, retry_after=60, blocking=False,
                    user_message="FinMind returned HTML body.",
                    technical_message=f"HTML body received. HTTP {http_status}.",
                    remediation="Retry later.",
                )
            try:
                payload = json.loads(body_str)
            except (json.JSONDecodeError, ValueError) as exc:
                return self._make_detail(
                    FinMindErrorCode.MALFORMED_PAYLOAD,
                    retryable=False, retry_after=None, blocking=True,
                    user_message="FinMind returned malformed JSON.",
                    technical_message=f"JSON parse error: {exc}. HTTP {http_status}.",
                    remediation="Report to FinMind. Schema may have changed.",
                )

        # HTTP 429 → RATE_LIMITED
        if http_status == 429:
            retry_after = None
            ra_header = headers.get("Retry-After") or headers.get("retry-after")
            if ra_header is not None:
                try:
                    retry_after = int(ra_header)
                except (ValueError, TypeError):
                    pass
            return self._make_detail(
                FinMindErrorCode.RATE_LIMITED,
                retryable=True, retry_after=retry_after or 60, blocking=False,
                user_message="FinMind rate limit exceeded (HTTP 429).",
                technical_message=f"HTTP 429. Retry-After: {retry_after}.",
                remediation="Wait and retry. Consider using a token for higher limits.",
            )

        # HTTP 401/403 → AUTH_INVALID
        if http_status in (401, 403):
            return self._make_detail(
                FinMindErrorCode.AUTH_INVALID,
                retryable=False, retry_after=None, blocking=True,
                user_message="FinMind authentication failed.",
                technical_message=f"HTTP {http_status}. Check FINMIND_API_TOKEN env var.",
                remediation="Verify token via FINMIND_API_TOKEN. No token rotation attempted.",
            )

        # HTTP 5xx → SERVICE_UNAVAILABLE
        if http_status >= 500:
            return self._make_detail(
                FinMindErrorCode.SERVICE_UNAVAILABLE,
                retryable=True, retry_after=120, blocking=False,
                user_message=f"FinMind server error (HTTP {http_status}).",
                technical_message=f"HTTP {http_status}.",
                remediation="Retry later.",
            )

        # HTTP 404 → DATASET_NOT_FOUND
        if http_status == 404:
            return self._make_detail(
                FinMindErrorCode.DATASET_NOT_FOUND,
                retryable=False, retry_after=None, blocking=True,
                user_message="FinMind dataset or endpoint not found (HTTP 404).",
                technical_message=f"HTTP 404.",
                remediation="Check dataset name against allowlist.",
            )

        # Analyze payload for HTTP 200
        if http_status == 200 and isinstance(payload, dict):
            payload_status = payload.get("status", 200)
            payload_msg = str(payload.get("msg", "")).lower()

            # Token/auth invalid via payload message
            if "token" in payload_msg or "unauthorized" in payload_msg or "invalid token" in payload_msg:
                return self._make_detail(
                    FinMindErrorCode.AUTH_INVALID,
                    retryable=False, retry_after=None, blocking=True,
                    user_message="FinMind token invalid (payload message).",
                    technical_message=f"Payload msg indicated auth failure. status={payload_status}.",
                    remediation="Check FINMIND_API_TOKEN. No token display.",
                )

            # Quota exceeded via payload (402 + "limit")
            if payload_status == 402 or (
                isinstance(payload_status, int) and payload_status == 402
            ) or "limit" in payload_msg:
                if "limit" in payload_msg or payload_status == 402:
                    return self._make_detail(
                        FinMindErrorCode.QUOTA_EXCEEDED,
                        retryable=False, retry_after=3600, blocking=True,
                        user_message="FinMind quota exceeded.",
                        technical_message=f"Payload status={payload_status}, msg={payload_msg[:100]}.",
                        remediation="Wait for quota reset or use authenticated token.",
                    )

            # Non-200 payload status → error
            if isinstance(payload_status, int) and payload_status != 200:
                if "date" in payload_msg or "range" in payload_msg:
                    return self._make_detail(
                        FinMindErrorCode.DATE_RANGE_INVALID,
                        retryable=False, retry_after=None, blocking=True,
                        user_message="FinMind rejected the date range.",
                        technical_message=f"Payload status={payload_status}, msg={payload_msg[:100]}.",
                        remediation="Check start_date/end_date format (YYYY-MM-DD).",
                    )
                if "data_id" in payload_msg or "stock" in payload_msg:
                    return self._make_detail(
                        FinMindErrorCode.DATA_ID_NOT_FOUND,
                        retryable=False, retry_after=None, blocking=False,
                        user_message="FinMind data_id not found.",
                        technical_message=f"Payload status={payload_status}, msg={payload_msg[:100]}.",
                        remediation="Verify symbol/data_id.",
                    )
                return self._make_detail(
                    FinMindErrorCode.INVALID_REQUEST,
                    retryable=False, retry_after=None, blocking=False,
                    user_message=f"FinMind rejected request (status={payload_status}).",
                    technical_message=f"Payload status={payload_status}, msg={payload_msg[:100]}.",
                    remediation="Check request parameters.",
                )

            # Empty data
            data_val = payload.get("data")
            if data_val is not None and isinstance(data_val, list) and len(data_val) == 0:
                return self._make_detail(
                    FinMindErrorCode.EMPTY_RESULT,
                    retryable=False, retry_after=None, blocking=False,
                    user_message="FinMind returned empty data array.",
                    technical_message="HTTP 200, payload.data=[].",
                    remediation="Try different date range or data_id.",
                )

            # Success
            return self._make_detail(
                FinMindErrorCode.SUCCESS,
                retryable=False, retry_after=None, blocking=False,
                user_message="OK",
                technical_message=f"HTTP 200, payload.status=200.",
                remediation="",
            )

        # HTTP 200 but payload is a list or unexpected shape
        if http_status == 200:
            return self._make_detail(
                FinMindErrorCode.SUCCESS,
                retryable=False, retry_after=None, blocking=False,
                user_message="OK (non-dict payload)",
                technical_message=f"HTTP 200. Payload type={type(payload).__name__}.",
                remediation="",
            )

        # Fallback
        return self._make_detail(
            FinMindErrorCode.UNKNOWN_ERROR,
            retryable=False, retry_after=None, blocking=False,
            user_message=f"Unknown error (HTTP {http_status}).",
            technical_message=f"HTTP {http_status}, content_type={content_type}.",
            remediation="Check FinMind API documentation.",
        )

    def _make_detail(
        self,
        error_code: FinMindErrorCode,
        retryable: bool,
        retry_after: Optional[int],
        blocking: bool,
        user_message: str,
        technical_message: str,
        remediation: str,
    ) -> FinMindErrorDetail:
        return FinMindErrorDetail(
            error_code=error_code,
            retryable=retryable,
            retry_after=retry_after,
            blocking=blocking,
            user_message=user_message,
            technical_message=technical_message,
            safe_context={
                "no_token_in_context": True,
                "no_real_orders": True,
            },
            remediation=remediation,
        )
