"""
data/providers/forum/ptt/client_v147.py — PTTClient v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] NO login, NO proxy, NO CAPTCHA bypass. Adult cookie only for normal public access.
[!] No credentials stored. Rate limit via governance layer.
[!] timeout/retry/Retry-After handled. Encoding detection (Big5/UTF-8).
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
LOGIN_BYPASS_ENABLED = False      # ALWAYS FALSE
CAPTCHA_BYPASS_ENABLED = False    # ALWAYS FALSE
PROXY_ROTATION_ENABLED = False    # ALWAYS FALSE
CREDENTIAL_STORAGE_ENABLED = False  # ALWAYS FALSE
FULL_IP_STORED = False            # ALWAYS FALSE


class PTTClient:
    """
    HTTP client for PTT public board.
    [!] NO login. NO proxy. NO CAPTCHA bypass. NO credentials stored.
    [!] Adult cookie: only set for pages that normally require over-18 confirmation.
    [!] Rate limit via governance layer. Retry-After respected.
    [!] Encoding detection: Big5/UTF-8 fallback.
    [!] dry_run=True by default (no real HTTP in dry_run mode).
    """

    def __init__(
        self,
        dry_run: bool = True,
        timeout: int = 10,
        max_retries: int = 3,
        rate_limit_sec: float = 2.0,
        governance=None,
    ) -> None:
        self._dry_run = dry_run
        self._timeout = timeout
        self._max_retries = max_retries
        self._rate_limit_sec = rate_limit_sec
        self._governance = governance
        self._last_request_time: float = 0.0

    def fetch_board_index(self, page: int = 1) -> Dict[str, Any]:
        """
        Fetch PTT board index page.
        [!] dry_run=True returns fixture-like empty response.
        """
        url = f"https://www.ptt.cc/bbs/Stock/index{page}.html"
        return self._fetch(url, content_type="board_index")

    def fetch_article(self, article_path: str) -> Dict[str, Any]:
        """
        Fetch a single PTT article.
        [!] dry_run=True returns fixture-like empty response.
        """
        url = f"https://www.ptt.cc{article_path}"
        return self._fetch(url, content_type="article")

    def _fetch(self, url: str, content_type: str = "article") -> Dict[str, Any]:
        """
        Internal fetch with rate limit, retry, and encoding detection.
        [!] dry_run=True: no real HTTP call.
        """
        if self._dry_run:
            return {
                "url": url,
                "status": "DRY_RUN",
                "html": "",
                "encoding": "utf-8",
                "dry_run": True,
            }

        # Rate limit enforcement
        elapsed = time.time() - self._last_request_time
        if elapsed < self._rate_limit_sec:
            time.sleep(self._rate_limit_sec - elapsed)

        # Governance rate limit check
        if self._governance is not None:
            allowed = self._governance.check_rate_limit("ptt_stock", url)
            if not allowed:
                return {
                    "url": url,
                    "status": "RATE_LIMITED",
                    "html": "",
                    "error": "Rate limit exceeded per governance policy",
                }

        import urllib.request
        import urllib.error

        headers = {
            "User-Agent": "Mozilla/5.0 TW-Quant-Cockpit/1.4.7 (research only; no commercial use)",
            "Cookie": "over18=1",  # Public over-18 confirmation only
            # NO: login tokens, session cookies, proxy headers, credentials
        }

        last_error = None
        for attempt in range(self._max_retries):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                    raw = resp.read()
                    self._last_request_time = time.time()
                    # Encoding detection
                    html, encoding = self._detect_encoding(raw)
                    return {
                        "url": url,
                        "status": "OK",
                        "html": html,
                        "encoding": encoding,
                        "dry_run": False,
                    }
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    # Retry-After
                    retry_after = int(e.headers.get("Retry-After", 60))
                    logger.warning("PTTClient: 429 rate limited, Retry-After=%ds", retry_after)
                    time.sleep(min(retry_after, 120))
                    last_error = str(e)
                    continue
                last_error = str(e)
                break
            except Exception as exc:
                last_error = str(exc)
                if attempt < self._max_retries - 1:
                    time.sleep(2 ** attempt)

        return {
            "url": url,
            "status": "ERROR",
            "html": "",
            "error": last_error,
        }

    def _detect_encoding(self, raw: bytes) -> tuple:
        """Try UTF-8 first, then Big5/CP950."""
        for enc in ("utf-8", "big5", "cp950"):
            try:
                return raw.decode(enc), enc
            except (UnicodeDecodeError, LookupError):
                continue
        return raw.decode("utf-8", errors="replace"), "utf-8_replace"
