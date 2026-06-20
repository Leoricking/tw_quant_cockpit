"""
data/providers/tpex/client_v141.py — TPEx HTTP client v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
"""
from __future__ import annotations

import json
import time
import uuid
from typing import Any, Callable, Dict, Optional, Tuple

from data.providers.tpex.models_v141 import TPExFetchStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_DEFAULT_USER_AGENT = "TW-Quant-Cockpit/1.4.1 (Research Only; No Real Orders; Not Investment Advice; TPEx Provider)"
_MAX_RESPONSE_BYTES = 50 * 1024 * 1024  # 50 MB


class TPExHttpClient:
    """
    HTTP client for TPEx OpenAPI endpoints.

    Transport is injectable: when transport=None, uses real requests library.
    Transport callable: (url, params) -> (status_code, content_bytes).
    NEVER falls back to mock on error.
    """

    def __init__(
        self,
        transport: Optional[Callable] = None,
        connect_timeout: float = 10.0,
        read_timeout: float = 30.0,
        max_retries: int = 3,
        rate_limit_delay: float = 1.0,
    ) -> None:
        self._transport = transport
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.max_retries = max_retries
        self.rate_limit_delay = rate_limit_delay

    def get(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[TPExFetchStatus, Any, Dict[str, Any]]:
        """
        Perform a GET request and return (status, data, provenance_partial).
        data is a Python object (parsed JSON) or None.
        provenance_partial is a dict with partial provenance fields.
        NEVER falls back to mock.
        """
        request_id = str(uuid.uuid4())
        params = params or {}
        attempts = 0
        last_status = TPExFetchStatus.NETWORK_ERROR
        last_data = None
        last_prov: Dict[str, Any] = {"request_id": request_id, "warnings": []}

        while attempts <= self.max_retries:
            attempts += 1
            try:
                status_code, content_bytes = self._do_request(url, params)
            except TimeoutError:
                last_status = TPExFetchStatus.TIMEOUT
                last_prov["warnings"].append(f"Timeout on attempt {attempts}")
                if attempts <= self.max_retries:
                    continue
                break
            except (ConnectionError, OSError, Exception) as exc:
                last_status = TPExFetchStatus.NETWORK_ERROR
                last_prov["warnings"].append(f"Network error on attempt {attempts}: {exc}")
                if attempts <= self.max_retries:
                    continue
                break

            # Handle HTTP status codes
            if status_code == 200:
                if not content_bytes:
                    last_status = TPExFetchStatus.EMPTY_RESPONSE
                    break
                if len(content_bytes) > _MAX_RESPONSE_BYTES:
                    last_status = TPExFetchStatus.MALFORMED
                    last_prov["warnings"].append("Response too large")
                    break
                # Check if HTML error page
                stripped = content_bytes.lstrip()
                if stripped.startswith(b"<!") or stripped.startswith(b"<html") or stripped.startswith(b"<HTML"):
                    last_status = TPExFetchStatus.MALFORMED
                    last_prov["warnings"].append("HTML error page returned instead of JSON")
                    break
                try:
                    data = json.loads(content_bytes.decode("utf-8", errors="replace"))
                    last_status = TPExFetchStatus.SUCCESS
                    last_data = data
                    break
                except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                    last_status = TPExFetchStatus.MALFORMED
                    last_prov["warnings"].append(f"JSON parse error: {exc}")
                    break

            elif status_code == 429:
                last_status = TPExFetchStatus.RATE_LIMITED
                last_prov["warnings"].append("Rate limited (429). No mock fallback.")
                break  # Do not retry on rate limit

            elif status_code in (500, 502, 503, 504):
                last_status = TPExFetchStatus.UNAVAILABLE
                last_prov["warnings"].append(f"Server error {status_code} on attempt {attempts}")
                if attempts <= self.max_retries:
                    time.sleep(min(2 ** (attempts - 1), 8))
                    continue
                break

            else:
                last_status = TPExFetchStatus.UNAVAILABLE
                last_prov["warnings"].append(f"Unexpected HTTP status {status_code}")
                break

        last_prov["request_id"] = request_id
        return last_status, last_data, last_prov

    def _do_request(self, url: str, params: Dict[str, Any]) -> Tuple[int, bytes]:
        """Perform the actual HTTP request via transport or requests library."""
        if self._transport is not None:
            return self._transport(url, params)
        # Real HTTP via requests
        try:
            import requests
            resp = requests.get(
                url,
                params=params if params else None,
                timeout=(self.connect_timeout, self.read_timeout),
                headers={"User-Agent": _DEFAULT_USER_AGENT},
            )
            return resp.status_code, resp.content
        except Exception:
            raise
