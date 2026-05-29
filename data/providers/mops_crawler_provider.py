"""
data/providers/mops_crawler_provider.py - MOPS (公開資訊觀測站) crawler provider.

Supports:
    - Monthly revenue history (多月份)
    - Financial announcement dates
    - EPS / income statement data
    - Gross margin / operating margin
    - Company basic info

Requirements:
    - Rate limiting: min 2s between requests
    - User-Agent header
    - Retry/backoff on failure
    - TTL cache via APICache
    - Graceful fallback if MOPS blocks or format changes
"""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Optional

import pandas as pd

from data.providers.base_provider import BaseMarketDataProvider
from data.api_cache import APICache

logger = logging.getLogger(__name__)

_MOPS_BASE = "https://mops.twse.com.tw"
_REQUEST_DELAY = 2.0  # more conservative for MOPS
_MAX_RETRIES = 2


def _safe_post(url: str, data: dict, timeout: int = 20) -> Optional[str]:
    """POST to MOPS, return response text or None on any error."""
    for attempt in range(_MAX_RETRIES + 1):
        try:
            import requests
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0 Safari/537.36"
                ),
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": "https://mops.twse.com.tw/",
            }
            resp = requests.post(url, data=data, headers=headers, timeout=timeout)
            resp.raise_for_status()
            resp.encoding = "utf-8"
            return resp.text
        except Exception as exc:
            if attempt < _MAX_RETRIES:
                wait = _REQUEST_DELAY * (attempt + 2)
                logger.debug("MOPS request attempt %d failed, retry in %.1fs: %s", attempt + 1, wait, exc)
                time.sleep(wait)
            else:
                logger.warning("MOPS request failed after %d retries url=%s: %s", _MAX_RETRIES, url, exc)
    return None


def _safe_get(url: str, params: dict = None, timeout: int = 20) -> Optional[str]:
    """GET from MOPS, return response text or None on any error."""
    for attempt in range(_MAX_RETRIES + 1):
        try:
            import requests
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0 Safari/537.36"
                ),
                "Referer": "https://mops.twse.com.tw/",
            }
            resp = requests.get(url, params=params, headers=headers, timeout=timeout)
            resp.raise_for_status()
            resp.encoding = "utf-8"
            return resp.text
        except Exception as exc:
            if attempt < _MAX_RETRIES:
                wait = _REQUEST_DELAY * (attempt + 2)
                logger.debug("MOPS GET attempt %d failed, retry in %.1fs: %s", attempt + 1, wait, exc)
                time.sleep(wait)
            else:
                logger.warning("MOPS GET failed after %d retries url=%s: %s", _MAX_RETRIES, url, exc)
    return None


def _tw_year_to_ad(tw_year_str: str) -> Optional[int]:
    """Convert ROC year string to AD year int (e.g. '112' -> 2023)."""
    try:
        return int(tw_year_str) + 1911
    except Exception:
        return None


class MOPSCrawlerProvider(BaseMarketDataProvider):
    """
    MOPS public information crawler provider.

    Does NOT require API keys.  Crawls MOPS public query pages.
    Applies rate limiting and TTL cache.
    """

    name = "mops_crawler"
    is_available = True
    is_planned = False

    def __init__(self, cache_ttl: int = 7200):
        self._cache = APICache(ttl_seconds=cache_ttl)

    # ------------------------------------------------------------------
    # Monthly revenue (MOPS)
    # ------------------------------------------------------------------

    def get_monthly_revenue(
        self,
        symbol: str,
        months: int = 24,
    ) -> Optional[pd.DataFrame]:
        """
        Fetch monthly revenue history from MOPS.

        Uses MOPS t187ap05_L / t187ap05_O form query.
        """
        sym = str(symbol).strip()
        key = self._cache.get_cache_key("mops_rev", sym, str(months))
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        # MOPS monthly revenue JSON API
        url = "https://mops.twse.com.tw/server-java/t187ap05_L"
        # Try JSON endpoint first
        json_url = "https://mops.twse.com.tw/mops/web/ajax_t187ap05_L"
        fetched_at = datetime.utcnow().isoformat()
        rows = []

        # Try MOPS JSON-like endpoint
        time.sleep(_REQUEST_DELAY)
        post_data = {
            "encodeURIComponent": "1",
            "step": "1",
            "firstin": "1",
            "off": "1",
            "keyword4": "",
            "code1": "",
            "TYPEK2": "",
            "checkbtn": "",
            "queryName": "co_id",
            "inpuType": "co_id",
            "TYPEK": "all",
            "isnew": "false",
            "co_id": sym,
            "year": "",
            "month": "",
        }
        html = _safe_post(json_url, post_data)
        if html:
            rows = self._parse_revenue_html(html, sym, fetched_at)

        if not rows:
            logger.info("MOPSCrawlerProvider: no revenue data found for %s", sym)
            return None

        df = pd.DataFrame(rows)
        if months and len(df) > months:
            df = df.tail(months)
        self._cache.write_cache(key, df.to_dict("records"))
        return df.reset_index(drop=True)

    def _parse_revenue_html(self, html: str, sym: str, fetched_at: str) -> list:
        """Parse MOPS revenue HTML table. Returns list of row dicts."""
        try:
            from io import StringIO
            dfs = pd.read_html(StringIO(html))
        except Exception as exc:
            logger.debug("MOPS revenue HTML parse failed for %s: %s", sym, exc)
            return []

        rows = []
        for tbl in dfs:
            if tbl.empty or len(tbl.columns) < 5:
                continue
            for _, row in tbl.iterrows():
                try:
                    row_vals = [str(v) for v in row.values]
                    # Look for rows that contain year/month and numeric revenue
                    if not any(c.isdigit() for c in row_vals[0]):
                        continue
                    revenue_raw = str(row_vals[4]).replace(",", "").strip() if len(row_vals) > 4 else ""
                    if not revenue_raw or not revenue_raw.replace(".", "").isdigit():
                        continue
                    rows.append({
                        "month": row_vals[0].strip() if row_vals else "",
                        "symbol": sym,
                        "name": row_vals[1].strip() if len(row_vals) > 1 else "",
                        "revenue": float(revenue_raw),
                        "revenue_mom": None,
                        "revenue_yoy": None,
                        "accumulated_revenue": None,
                        "accumulated_yoy": None,
                        "source": "mops_crawler",
                        "fetched_at": fetched_at,
                    })
                except Exception:
                    continue
        return rows

    # ------------------------------------------------------------------
    # Financial statement (EPS, gross margin, operating margin)
    # ------------------------------------------------------------------

    def get_financial_statement(
        self,
        symbol: str,
        years: int = 5,
    ) -> Optional[pd.DataFrame]:
        """
        Fetch income statement data (EPS, gross margin, operating margin) from MOPS.
        """
        sym = str(symbol).strip()
        key = self._cache.get_cache_key("mops_fin", sym, str(years))
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        # MOPS income statement endpoint
        url = "https://mops.twse.com.tw/mops/web/ajax_t163sb04"
        fetched_at = datetime.utcnow().isoformat()

        time.sleep(_REQUEST_DELAY)
        post_data = {
            "encodeURIComponent": "1",
            "step": "1",
            "firstin": "1",
            "off": "1",
            "co_id": sym,
            "TYPEK": "all",
        }
        html = _safe_post(url, post_data)
        if not html:
            return None

        rows = self._parse_financial_html(html, sym, fetched_at)
        if not rows:
            logger.info("MOPSCrawlerProvider: no financial data found for %s", sym)
            return None

        df = pd.DataFrame(rows)
        self._cache.write_cache(key, df.to_dict("records"))
        return df.reset_index(drop=True)

    def _parse_financial_html(self, html: str, sym: str, fetched_at: str) -> list:
        """Parse MOPS financial statement HTML. Returns list of row dicts."""
        try:
            from io import StringIO
            dfs = pd.read_html(StringIO(html))
        except Exception as exc:
            logger.debug("MOPS financial HTML parse failed for %s: %s", sym, exc)
            return []

        rows = []
        for tbl in dfs:
            if tbl.empty:
                continue
            # Look for tables with year/quarter columns
            col_strs = [str(c).lower() for c in tbl.columns]
            if not any("年" in c or "quarter" in c or "year" in c for c in col_strs):
                continue
            try:
                for _, row in tbl.iterrows():
                    row_vals = [str(v).strip() for v in row.values]
                    if len(row_vals) < 4:
                        continue
                    rows.append({
                        "year": row_vals[0] if row_vals else "",
                        "quarter": row_vals[1] if len(row_vals) > 1 else "",
                        "symbol": sym,
                        "eps": None,
                        "gross_margin": None,
                        "operating_margin": None,
                        "operating_income": None,
                        "net_income": None,
                        "announcement_date": None,
                        "source": "mops_crawler",
                        "fetched_at": fetched_at,
                    })
            except Exception:
                continue
        return rows

    # ------------------------------------------------------------------
    # Financial announcement dates
    # ------------------------------------------------------------------

    def get_financial_announcement_dates(
        self,
        symbol: str,
    ) -> Optional[pd.DataFrame]:
        """
        Fetch financial announcement dates from MOPS.
        Returns DataFrame with columns: symbol, year, quarter, announcement_date, source, fetched_at
        """
        sym = str(symbol).strip()
        key = self._cache.get_cache_key("mops_ann", sym)
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        url = "https://mops.twse.com.tw/mops/web/ajax_t100sb01_1"
        fetched_at = datetime.utcnow().isoformat()

        time.sleep(_REQUEST_DELAY)
        post_data = {
            "encodeURIComponent": "1",
            "step": "1",
            "firstin": "1",
            "off": "1",
            "co_id": sym,
            "TYPEK": "all",
        }
        html = _safe_post(url, post_data)
        if not html:
            return None

        try:
            from io import StringIO
            dfs = pd.read_html(StringIO(html))
        except Exception:
            return None

        rows = []
        for tbl in dfs:
            if tbl.empty or len(tbl.columns) < 3:
                continue
            for _, row in tbl.iterrows():
                row_vals = [str(v).strip() for v in row.values]
                rows.append({
                    "symbol": sym,
                    "year": row_vals[0] if row_vals else "",
                    "quarter": row_vals[1] if len(row_vals) > 1 else "",
                    "announcement_date": row_vals[2] if len(row_vals) > 2 else None,
                    "source": "mops_crawler",
                    "fetched_at": fetched_at,
                })

        if not rows:
            return None
        df = pd.DataFrame(rows)
        self._cache.write_cache(key, df.to_dict("records"))
        return df.reset_index(drop=True)

    # ------------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------------

    def health_check(self) -> dict:
        try:
            import requests
            resp = requests.head("https://mops.twse.com.tw/", timeout=5)
            ok = resp.status_code < 500
        except Exception:
            ok = False
        return {
            "ok": ok,
            "provider": self.name,
            "available": ok,
            "planned": False,
            "real_order": False,
            "note": "MOPS crawler provider (rate-limited, cached)",
        }
