"""
data/providers/finmind/client_v144.py — FinMind HTTP client v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Injectable transport for offline tests. Never logs token.
[!] API v4 base URL: https://api.finmindtrade.com/api/v4/data
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FINMIND_API_V4_BASE_URL = "https://api.finmindtrade.com/api/v4/data"


class FinMindClient:
    """
    HTTP client for FinMind API v4.
    Accepts injectable transport for offline/test use.
    Never logs token values.
    """

    def __init__(self, transport: Optional[Callable] = None) -> None:
        """
        transport: callable(url, params) → dict with keys:
            http_status (int), body (dict|str), headers (dict), content_type (str)
        If None, uses requests library.
        """
        self._transport = transport

    def fetch(
        self,
        dataset: str,
        data_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        token: Optional[str] = None,
        extra_params: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """
        Fetch data from FinMind API v4.
        Returns dict: {http_status, body, headers, content_type, url, params_safe}
        Never logs the token.
        """
        params: Dict[str, Any] = {"dataset": dataset}
        if data_id is not None:
            params["data_id"] = data_id
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if token is not None:
            params["token"] = token  # included in request, never logged
        if extra_params:
            params.update(extra_params)

        # Safe params for logging (no token)
        params_safe = {k: v for k, v in params.items() if k != "token"}
        logger.debug("FinMind fetch: dataset=%s params_safe=%s", dataset, params_safe)

        if self._transport is not None:
            try:
                result = self._transport(FINMIND_API_V4_BASE_URL, params)
                result["url"] = FINMIND_API_V4_BASE_URL
                result["params_safe"] = params_safe
                return result
            except Exception as exc:
                return {
                    "http_status": 0,
                    "body": None,
                    "headers": {},
                    "content_type": "",
                    "url": FINMIND_API_V4_BASE_URL,
                    "params_safe": params_safe,
                    "error": str(exc),
                }

        # Real network request
        try:
            import requests  # type: ignore
            resp = requests.get(FINMIND_API_V4_BASE_URL, params=params, timeout=timeout)
            content_type = resp.headers.get("Content-Type", "")
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            return {
                "http_status": resp.status_code,
                "body": body,
                "headers": dict(resp.headers),
                "content_type": content_type,
                "url": FINMIND_API_V4_BASE_URL,
                "params_safe": params_safe,
            }
        except ImportError:
            return {
                "http_status": 0,
                "body": None,
                "headers": {},
                "content_type": "",
                "url": FINMIND_API_V4_BASE_URL,
                "params_safe": params_safe,
                "error": "requests library not available",
            }
        except Exception as exc:
            return {
                "http_status": 0,
                "body": None,
                "headers": {},
                "content_type": "",
                "url": FINMIND_API_V4_BASE_URL,
                "params_safe": params_safe,
                "error": str(exc),
            }
