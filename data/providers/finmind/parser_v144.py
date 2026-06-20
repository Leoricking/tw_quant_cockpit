"""
data/providers/finmind/parser_v144.py — FinMind response parser v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] HTTP 200 + empty data → EMPTY_RESULT (not success).
[!] payload status=402 + "limit" → QUOTA_EXCEEDED.
"""
from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class FinMindParser:
    """
    Parses raw FinMind API responses into a structured result dict.
    Handles JSON errors, missing keys, empty data, and payload status codes.
    """

    def parse_response(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse raw response dict (from FinMindClient.fetch).

        Returns dict with:
            status_code, payload_status, payload_msg, data,
            metadata, is_success, error_code, is_empty,
            is_quota_exceeded, is_rate_limited
        """
        http_status = raw.get("http_status", 0)
        body = raw.get("body")
        error = raw.get("error")
        content_type = raw.get("content_type", "")

        # Network/transport error
        if error and http_status == 0:
            return self._build(
                status_code=0,
                payload_status=None,
                payload_msg=error,
                data=[],
                metadata={},
                is_success=False,
                error_code="NETWORK_ERROR",
                is_empty=True,
                is_quota_exceeded=False,
                is_rate_limited=False,
            )

        # HTML response
        ct = (content_type or "").lower()
        if "text/html" in ct:
            return self._build(
                status_code=http_status,
                payload_status=None,
                payload_msg="HTML response",
                data=[],
                metadata={},
                is_success=False,
                error_code="SERVICE_UNAVAILABLE",
                is_empty=True,
                is_quota_exceeded=False,
                is_rate_limited=False,
            )

        # Rate limited
        if http_status == 429:
            return self._build(
                status_code=http_status,
                payload_status=None,
                payload_msg="Rate limited (HTTP 429)",
                data=[],
                metadata={},
                is_success=False,
                error_code="RATE_LIMITED",
                is_empty=True,
                is_quota_exceeded=False,
                is_rate_limited=True,
            )

        # Auth failure
        if http_status in (401, 403):
            return self._build(
                status_code=http_status,
                payload_status=None,
                payload_msg=f"Auth failure (HTTP {http_status})",
                data=[],
                metadata={},
                is_success=False,
                error_code="AUTH_INVALID",
                is_empty=True,
                is_quota_exceeded=False,
                is_rate_limited=False,
            )

        # Parse body
        if isinstance(body, str):
            if body.lstrip().startswith("<"):
                return self._build(
                    status_code=http_status,
                    payload_status=None,
                    payload_msg="HTML body",
                    data=[],
                    metadata={},
                    is_success=False,
                    error_code="SERVICE_UNAVAILABLE",
                    is_empty=True,
                    is_quota_exceeded=False,
                    is_rate_limited=False,
                )
            try:
                body = json.loads(body)
            except (json.JSONDecodeError, ValueError):
                return self._build(
                    status_code=http_status,
                    payload_status=None,
                    payload_msg="Malformed JSON",
                    data=[],
                    metadata={},
                    is_success=False,
                    error_code="MALFORMED_PAYLOAD",
                    is_empty=True,
                    is_quota_exceeded=False,
                    is_rate_limited=False,
                )

        if not isinstance(body, dict):
            return self._build(
                status_code=http_status,
                payload_status=None,
                payload_msg=f"Unexpected body type: {type(body).__name__}",
                data=[],
                metadata={},
                is_success=False,
                error_code="MALFORMED_PAYLOAD",
                is_empty=True,
                is_quota_exceeded=False,
                is_rate_limited=False,
            )

        payload_status = body.get("status", 200)
        payload_msg = str(body.get("msg", ""))
        data = body.get("data", [])
        metadata = {k: v for k, v in body.items() if k not in ("status", "msg", "data")}

        # Token/auth via payload
        msg_lower = payload_msg.lower()
        if "token" in msg_lower or "unauthorized" in msg_lower:
            return self._build(
                status_code=http_status,
                payload_status=payload_status,
                payload_msg=payload_msg,
                data=[],
                metadata=metadata,
                is_success=False,
                error_code="AUTH_INVALID",
                is_empty=True,
                is_quota_exceeded=False,
                is_rate_limited=False,
            )

        # Quota via payload
        is_quota = (payload_status == 402) or ("limit" in msg_lower and payload_status != 200)
        if is_quota:
            return self._build(
                status_code=http_status,
                payload_status=payload_status,
                payload_msg=payload_msg,
                data=[],
                metadata=metadata,
                is_success=False,
                error_code="QUOTA_EXCEEDED",
                is_empty=True,
                is_quota_exceeded=True,
                is_rate_limited=False,
            )

        # Non-200 payload status
        if isinstance(payload_status, int) and payload_status != 200:
            return self._build(
                status_code=http_status,
                payload_status=payload_status,
                payload_msg=payload_msg,
                data=[],
                metadata=metadata,
                is_success=False,
                error_code="INVALID_REQUEST",
                is_empty=True,
                is_quota_exceeded=False,
                is_rate_limited=False,
            )

        # Empty data
        if isinstance(data, list) and len(data) == 0:
            return self._build(
                status_code=http_status,
                payload_status=payload_status,
                payload_msg=payload_msg,
                data=[],
                metadata=metadata,
                is_success=False,
                error_code="EMPTY_RESULT",
                is_empty=True,
                is_quota_exceeded=False,
                is_rate_limited=False,
            )

        # Success
        return self._build(
            status_code=http_status,
            payload_status=payload_status,
            payload_msg=payload_msg,
            data=data if isinstance(data, list) else [data],
            metadata=metadata,
            is_success=True,
            error_code="SUCCESS",
            is_empty=False,
            is_quota_exceeded=False,
            is_rate_limited=False,
        )

    def _build(
        self,
        status_code: int,
        payload_status: Optional[int],
        payload_msg: str,
        data: List[Any],
        metadata: Dict[str, Any],
        is_success: bool,
        error_code: str,
        is_empty: bool,
        is_quota_exceeded: bool,
        is_rate_limited: bool,
    ) -> Dict[str, Any]:
        return {
            "status_code": status_code,
            "payload_status": payload_status,
            "payload_msg": payload_msg,
            "data": data,
            "metadata": metadata,
            "is_success": is_success,
            "error_code": error_code,
            "is_empty": is_empty,
            "is_quota_exceeded": is_quota_exceeded,
            "is_rate_limited": is_rate_limited,
        }
