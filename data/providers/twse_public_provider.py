"""
data/providers/twse_public_provider.py - TWSE / data.gov.tw public data provider.

Supports:
    - Listed company monthly revenue (TWSE OpenAPI)
    - Listed company institutional detail (TWSE OpenAPI)
    - Listed company margin/short data (TWSE OpenAPI)
    - Listed company basic info (TWSE OpenAPI)

All output columns follow the TW Quant Cockpit standard schema.
Missing data returns None — never crashes.
Rate limiting and TTL cache are applied via APICache.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from data.providers.base_provider import BaseMarketDataProvider
from data.api_cache import APICache

logger = logging.getLogger(__name__)

_TWSE_API_BASE = "https://openapi.twse.com.tw/v1"
_REQUEST_DELAY = 1.5  # seconds between requests (be polite)


def _safe_get(url: str, params: dict = None, timeout: int = 15) -> Optional[list]:
    """GET JSON from URL, return parsed list/dict or None on any error."""
    try:
        import requests
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (compatible; TW-Quant-Cockpit/0.3.9; "
                "+https://github.com/trading-master)"
            )
        }
        resp = requests.get(url, params=params, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        logger.warning("TWSE API request failed url=%s: %s", url, exc)
        return None


class TWPublicProvider(BaseMarketDataProvider):
    """
    TWSE public data provider.

    Does NOT require API keys.  Uses TWSE OpenAPI endpoints.
    """

    name = "twse_public"
    is_available = True
    is_planned = False

    def __init__(self, cache_ttl: int = 3600):
        self._cache = APICache(ttl_seconds=cache_ttl)

    # ------------------------------------------------------------------
    # Monthly revenue
    # ------------------------------------------------------------------

    def get_monthly_revenue(
        self,
        symbol: str,
        months: int = 24,
    ) -> Optional[pd.DataFrame]:
        """
        Fetch monthly revenue for a listed company.

        Returns DataFrame with standard columns or None.
        """
        sym = str(symbol).strip()
        key = self._cache.get_cache_key("twse_rev", sym, str(months))
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        rows = []
        fetched_at = datetime.utcnow().isoformat()

        # TWSE OpenAPI: monthly revenue endpoint
        url = f"{_TWSE_API_BASE}/exchangeReport/BWIBBU_d"
        # Fallback: use revenue history endpoint
        rev_url = "https://openapi.twse.com.tw/v1/opendata/t187ap05_L"
        time.sleep(_REQUEST_DELAY)
        data = _safe_get(rev_url)
        if data:
            for item in data:
                stock_id = item.get("公司代號", "").strip()
                if stock_id != sym:
                    continue
                try:
                    month_str = str(item.get("資料年月", "")).strip()
                    revenue_raw = str(item.get("當月營收", "0")).replace(",", "")
                    revenue = float(revenue_raw) if revenue_raw else None
                    rows.append({
                        "month": month_str,
                        "symbol": sym,
                        "name": item.get("公司名稱", ""),
                        "revenue": revenue,
                        "revenue_mom": None,
                        "revenue_yoy": None,
                        "accumulated_revenue": None,
                        "accumulated_yoy": None,
                        "source": "twse_openapi",
                        "fetched_at": fetched_at,
                    })
                except Exception as row_exc:
                    logger.debug("TWPublicProvider rev row error: %s", row_exc)

        if not rows:
            logger.info("TWPublicProvider: no revenue data found for %s", sym)
            return None

        df = pd.DataFrame(rows)
        if months and len(df) > months:
            df = df.tail(months)
        self._cache.write_cache(key, df.to_dict("records"))
        return df.reset_index(drop=True)

    # ------------------------------------------------------------------
    # Institutional detail
    # ------------------------------------------------------------------

    def get_institutional(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """Fetch institutional buy/sell detail from TWSE OpenAPI."""
        sym = str(symbol).strip()
        key = self._cache.get_cache_key("twse_inst", sym, str(start), str(end))
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        url = "https://openapi.twse.com.tw/v1/fund/TWT44U"
        time.sleep(_REQUEST_DELAY)
        data = _safe_get(url)
        if not data:
            return None

        fetched_at = datetime.utcnow().isoformat()
        rows = []
        for item in data:
            stock_id = item.get("Code", "").strip()
            if stock_id != sym:
                continue
            try:
                def _parse_int(v):
                    try:
                        return int(str(v).replace(",", ""))
                    except Exception:
                        return None

                rows.append({
                    "date": item.get("Date", ""),
                    "symbol": sym,
                    "foreign_net_buy": _parse_int(item.get("ForeignInvestorsBuy", 0)) - _parse_int(item.get("ForeignInvestorsSell", 0) or 0),
                    "trust_net_buy": _parse_int(item.get("InvestmentTrustBuy", 0)) - _parse_int(item.get("InvestmentTrustSell", 0) or 0),
                    "dealer_net_buy": _parse_int(item.get("DealersBuy", 0)) - _parse_int(item.get("DealersSell", 0) or 0),
                    "foreign_buy": _parse_int(item.get("ForeignInvestorsBuy", 0)),
                    "foreign_sell": _parse_int(item.get("ForeignInvestorsSell", 0)),
                    "trust_buy": _parse_int(item.get("InvestmentTrustBuy", 0)),
                    "trust_sell": _parse_int(item.get("InvestmentTrustSell", 0)),
                    "dealer_buy": _parse_int(item.get("DealersBuy", 0)),
                    "dealer_sell": _parse_int(item.get("DealersSell", 0)),
                    "source": "twse_openapi",
                    "fetched_at": fetched_at,
                })
            except Exception as row_exc:
                logger.debug("TWPublicProvider inst row error: %s", row_exc)

        if not rows:
            return None

        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        if start:
            df = df[df["date"] >= pd.to_datetime(start)]
        if end:
            df = df[df["date"] <= pd.to_datetime(end)]
        if df.empty:
            return None
        df = df.sort_values("date").reset_index(drop=True)
        self._cache.write_cache(key, df.to_dict("records"))
        return df

    # ------------------------------------------------------------------
    # Margin / short
    # ------------------------------------------------------------------

    def get_margin_short(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """Fetch margin/short balance from TWSE OpenAPI."""
        sym = str(symbol).strip()
        key = self._cache.get_cache_key("twse_margin", sym, str(start), str(end))
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        url = "https://openapi.twse.com.tw/v1/fund/MI_MARGRATIO"
        time.sleep(_REQUEST_DELAY)
        data = _safe_get(url)
        if not data:
            return None

        fetched_at = datetime.utcnow().isoformat()
        rows = []
        for item in data:
            stock_id = item.get("StockNo", "").strip()
            if stock_id != sym:
                continue
            try:
                def _parse_num(v):
                    try:
                        return float(str(v).replace(",", ""))
                    except Exception:
                        return None

                rows.append({
                    "date": item.get("Date", ""),
                    "symbol": sym,
                    "margin_balance": _parse_num(item.get("MarginPurchaseBalance")),
                    "margin_change": _parse_num(item.get("MarginPurchaseChange")),
                    "short_balance": _parse_num(item.get("ShortSaleBalance")),
                    "short_change": _parse_num(item.get("ShortSaleChange")),
                    "sbl_short_balance": None,
                    "source": "twse_openapi",
                    "fetched_at": fetched_at,
                })
            except Exception as row_exc:
                logger.debug("TWPublicProvider margin row error: %s", row_exc)

        if not rows:
            return None

        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        if start:
            df = df[df["date"] >= pd.to_datetime(start)]
        if end:
            df = df[df["date"] <= pd.to_datetime(end)]
        if df.empty:
            return None
        df = df.sort_values("date").reset_index(drop=True)
        self._cache.write_cache(key, df.to_dict("records"))
        return df

    # ------------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------------

    def health_check(self) -> dict:
        try:
            import requests
            resp = requests.head(
                "https://openapi.twse.com.tw/", timeout=5
            )
            ok = resp.status_code < 500
        except Exception:
            ok = False
        return {
            "ok": ok,
            "provider": self.name,
            "available": ok,
            "planned": False,
            "real_order": False,
            "note": "TWSE OpenAPI public provider",
        }
