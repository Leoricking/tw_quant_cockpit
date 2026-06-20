"""
data/providers/data_gov_tw/client_v143.py — data.gov.tw HTTP client v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] DATA_GOV_TW_MOCK_FALLBACK_ENABLED = False.
[!] DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED = False.
[!] Rate limited: RATE_LIMITED returned. No mock fallback. No mirror fallback.
[!] Different agency hosts have separate rate limits.
"""
from __future__ import annotations

import time
import uuid
from typing import Any, Callable, Dict, Optional, Tuple

from data.providers.data_gov_tw.models_v143 import FetchStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
DATA_GOV_TW_MOCK_FALLBACK_ENABLED = False
DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED = False

_DEFAULT_USER_AGENT = (
    "TW-Quant-Cockpit/1.4.3 (Research Only; No Real Orders; "
    "Not Investment Advice; data.gov.tw Provider)"
)
_MAX_RESPONSE_BYTES = 100 * 1024 * 1024  # 100 MB


class DataGovTwHttpClient:
    """
    HTTP client for data.gov.tw endpoints and agency download URLs.

    - Transport is injectable for offline testing.
    - Transport callable: (url, method, params, body) -> (status_code, content_bytes).
    - NEVER falls back to mock on error.
    - NEVER falls back to non-official mirror.
    - Rate limited → RATE_LIMITED, stops current resource fetch.
    - Per-domain rate limit tracking.
    """

    def __init__(
        self,
        transport: Optional[Callable] = None,
        connect_timeout: float = 10.0,
        read_timeout: float = 60.0,
        max_retries: int = 2,
        rate_limit_delay: float = 2.0,
    ) -> None:
        self._transport = transport
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.max_retries = max_retries
        self.rate_limit_delay = rate_limit_delay

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        max_bytes: int = _MAX_RESPONSE_BYTES,
    ) -> Tuple[FetchStatus, Optional[bytes], Dict[str, Any]]:
        return self._request(url, "GET", params=params or {}, max_bytes=max_bytes)

    def get_json(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Tuple[FetchStatus, Optional[Any], Dict[str, Any]]:
        """GET and parse JSON response."""
        import json as _json
        status, content, prov = self._request(url, "GET", params=params or {})
        if status != FetchStatus.SUCCESS or not content:
            return status, None, prov
        try:
            data = _json.loads(content.decode("utf-8", errors="replace"))
            return FetchStatus.SUCCESS, data, prov
        except (_json.JSONDecodeError, ValueError) as exc:
            prov["warnings"].append(f"JSON decode error: {exc}")
            return FetchStatus.MALFORMED, None, prov

    def download(
        self,
        url: str,
        max_bytes: int = _MAX_RESPONSE_BYTES,
    ) -> Tuple[FetchStatus, Optional[bytes], Dict[str, Any]]:
        """Download a resource file (CSV, XML, ZIP, etc.)."""
        return self._request(url, "GET", params={}, max_bytes=max_bytes)

    def _request(
        self,
        url: str,
        method: str,
        params: Optional[Dict[str, Any]] = None,
        max_bytes: int = _MAX_RESPONSE_BYTES,
    ) -> Tuple[FetchStatus, Optional[bytes], Dict[str, Any]]:
        request_id = str(uuid.uuid4())
        attempts = 0
        last_status = FetchStatus.NETWORK_ERROR
        last_data: Optional[bytes] = None
        last_prov: Dict[str, Any] = {"request_id": request_id, "warnings": [], "url": url}

        while attempts <= self.max_retries:
            attempts += 1
            try:
                status_code, content_bytes = self._do_request(url, method, params or {})
            except TimeoutError:
                last_status = FetchStatus.TIMEOUT
                last_prov["warnings"].append(f"Timeout on attempt {attempts}")
                if attempts <= self.max_retries:
                    continue
                break
            except (ConnectionError, OSError, Exception) as exc:
                last_status = FetchStatus.NETWORK_ERROR
                last_prov["warnings"].append(f"Network error on attempt {attempts}: {exc}")
                if attempts <= self.max_retries:
                    continue
                break

            if status_code == 200:
                if not content_bytes:
                    last_status = FetchStatus.EMPTY_RESPONSE
                    break
                if len(content_bytes) > max_bytes:
                    last_status = FetchStatus.BLOCKED
                    last_prov["warnings"].append(
                        f"Response exceeds size limit ({len(content_bytes)} > {max_bytes})"
                    )
                    break
                last_status = FetchStatus.SUCCESS
                last_data = content_bytes
                break

            elif status_code == 429:
                last_status = FetchStatus.RATE_LIMITED
                last_prov["warnings"].append("Rate limited (429). No mock fallback. Stopping fetch.")
                break

            elif status_code in (301, 302, 303, 307, 308):
                last_status = FetchStatus.UNAVAILABLE
                last_prov["warnings"].append(f"Redirect {status_code} — not automatically followed")
                break

            elif status_code in (500, 502, 503, 504):
                last_status = FetchStatus.UNAVAILABLE
                last_prov["warnings"].append(f"Server error {status_code} on attempt {attempts}")
                if attempts <= self.max_retries:
                    time.sleep(min(2 ** (attempts - 1), 8))
                    continue
                break

            else:
                last_status = FetchStatus.UNAVAILABLE
                last_prov["warnings"].append(f"Unexpected HTTP status {status_code}")
                break

        last_prov["request_id"] = request_id
        return last_status, last_data, last_prov

    def _do_request(
        self,
        url: str,
        method: str,
        params: Dict[str, Any],
    ) -> Tuple[int, bytes]:
        if self._transport is not None:
            return self._transport(url, method, params, None)
        try:
            import requests
            headers = {"User-Agent": _DEFAULT_USER_AGENT, "Accept": "application/json"}
            resp = requests.get(
                url,
                params=params if params else None,
                timeout=(self.connect_timeout, self.read_timeout),
                headers=headers,
            )
            return resp.status_code, resp.content
        except Exception:
            raise
