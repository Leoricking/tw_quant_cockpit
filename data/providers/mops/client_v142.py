"""
data/providers/mops/client_v142.py — MOPS HTTP client v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
"""
from __future__ import annotations

import time
import uuid
from typing import Any, Callable, Dict, Optional, Tuple

from data.providers.mops.models_v142 import MOPSFetchStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
MOPS_MOCK_FALLBACK_ENABLED = False

_DEFAULT_USER_AGENT = "TW-Quant-Cockpit/1.4.2 (Research Only; No Real Orders; Not Investment Advice; MOPS Provider)"
_MAX_RESPONSE_BYTES = 50 * 1024 * 1024  # 50 MB

_MAINTENANCE_MARKERS = [
    b"\xe7\xb3\xbb\xe7\xb5\xb1\xe7\xb6\xad\xe8\xad\xb7",  # 系統維護
    b"maintenance",
    b"Maintenance",
    b"\xe4\xb8\xad\xe6\x96\xad\xe7\xb6\xad\xe8\xad\xb7",  # 中斷維護
]


def _is_maintenance_page(content: bytes) -> bool:
    """Detect MOPS maintenance pages."""
    for marker in _MAINTENANCE_MARKERS:
        if marker in content:
            return True
    return False


class MOPSHttpClient:
    """
    HTTP client for MOPS endpoints.

    Supports GET and POST (form submission) methods.
    Transport is injectable for offline testing.
    Transport callable: (url, method, params, form_data) -> (status_code, content_bytes).
    NEVER falls back to mock on error.
    MOPS uses POST form submissions for most endpoints.
    """

    def __init__(
        self,
        transport: Optional[Callable] = None,
        connect_timeout: float = 10.0,
        read_timeout: float = 30.0,
        max_retries: int = 2,
        rate_limit_delay: float = 1.5,
        session_cookie: Optional[str] = None,
    ) -> None:
        self._transport = transport
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.max_retries = max_retries
        self.rate_limit_delay = rate_limit_delay
        self.session_cookie = session_cookie

    def get(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[MOPSFetchStatus, Any, Dict[str, Any]]:
        """Perform a GET request."""
        return self._request(url, "GET", params=params or {}, form_data=None)

    def post_form(
        self, url: str, form_data: Dict[str, Any]
    ) -> Tuple[MOPSFetchStatus, bytes, Dict[str, Any]]:
        """Perform a POST form submission. Returns raw bytes for HTML parsing."""
        return self._request(url, "POST", params=None, form_data=form_data)

    def _request(
        self,
        url: str,
        method: str,
        params: Optional[Dict[str, Any]],
        form_data: Optional[Dict[str, Any]],
    ) -> Tuple[MOPSFetchStatus, Any, Dict[str, Any]]:
        """Internal request method."""
        request_id = str(uuid.uuid4())
        attempts = 0
        last_status = MOPSFetchStatus.NETWORK_ERROR
        last_data: Any = None
        last_prov: Dict[str, Any] = {"request_id": request_id, "warnings": []}

        while attempts <= self.max_retries:
            attempts += 1
            try:
                status_code, content_bytes = self._do_request(url, method, params, form_data)
            except TimeoutError:
                last_status = MOPSFetchStatus.TIMEOUT
                last_prov["warnings"].append(f"Timeout on attempt {attempts}")
                if attempts <= self.max_retries:
                    continue
                break
            except (ConnectionError, OSError, Exception) as exc:
                last_status = MOPSFetchStatus.NETWORK_ERROR
                last_prov["warnings"].append(f"Network error on attempt {attempts}: {exc}")
                if attempts <= self.max_retries:
                    continue
                break

            if status_code == 200:
                if not content_bytes:
                    last_status = MOPSFetchStatus.EMPTY_RESPONSE
                    break
                if len(content_bytes) > _MAX_RESPONSE_BYTES:
                    last_status = MOPSFetchStatus.MALFORMED
                    last_prov["warnings"].append("Response too large")
                    break
                if _is_maintenance_page(content_bytes):
                    last_status = MOPSFetchStatus.MAINTENANCE
                    last_prov["warnings"].append("MOPS maintenance page detected")
                    break
                last_status = MOPSFetchStatus.SUCCESS
                last_data = content_bytes
                break

            elif status_code == 429:
                last_status = MOPSFetchStatus.RATE_LIMITED
                last_prov["warnings"].append("Rate limited (429). No mock fallback.")
                break

            elif status_code in (500, 502, 503, 504):
                last_status = MOPSFetchStatus.UNAVAILABLE
                last_prov["warnings"].append(f"Server error {status_code} on attempt {attempts}")
                if attempts <= self.max_retries:
                    time.sleep(min(2 ** (attempts - 1), 8))
                    continue
                break

            else:
                last_status = MOPSFetchStatus.UNAVAILABLE
                last_prov["warnings"].append(f"Unexpected HTTP status {status_code}")
                break

        last_prov["request_id"] = request_id
        return last_status, last_data, last_prov

    def _do_request(
        self,
        url: str,
        method: str,
        params: Optional[Dict[str, Any]],
        form_data: Optional[Dict[str, Any]],
    ) -> Tuple[int, bytes]:
        """Perform the actual HTTP request via transport or requests library."""
        if self._transport is not None:
            return self._transport(url, method, params, form_data)
        try:
            import requests
            headers = {"User-Agent": _DEFAULT_USER_AGENT}
            if self.session_cookie:
                headers["Cookie"] = self.session_cookie
            if method == "POST" and form_data:
                resp = requests.post(
                    url,
                    data=form_data,
                    timeout=(self.connect_timeout, self.read_timeout),
                    headers=headers,
                )
            else:
                resp = requests.get(
                    url,
                    params=params if params else None,
                    timeout=(self.connect_timeout, self.read_timeout),
                    headers=headers,
                )
            return resp.status_code, resp.content
        except Exception:
            raise
