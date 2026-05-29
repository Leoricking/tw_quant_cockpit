"""
data/providers/tpex_public_provider.py - TPEx / OTC OpenAPI public data provider.

Supports:
    - OTC / emerging listed monthly revenue
    - OTC institutional buy/sell
    - OTC margin/short data
    - OTC company info

Column formats match TWPublicProvider (twse_public_provider) exactly.
Missing data returns None — never crashes.
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

_TPEX_API_BASE = "https://www.tpex.org.tw"
_REQUEST_DELAY = 1.5


def _safe_get(url: str, params: dict = None, timeout: int = 15) -> Optional[object]:
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
        logger.warning("TPEx API request failed url=%s: %s", url, exc)
        return None


class TPExPublicProvider(BaseMarketDataProvider):
    """
    TPEx (OTC / emerging) public data provider.

    Does NOT require API keys.  Uses TPEx public endpoints.
    """

    name = "tpex_public"
    is_available = True
    is_planned = False

    def __init__(self, cache_ttl: int = 3600):
        self._cache = APICache(ttl_seconds=cache_ttl)

    def get_monthly_revenue(
        self,
        symbol: str,
        months: int = 24,
    ) -> Optional[pd.DataFrame]:
        """Fetch monthly revenue for an OTC-listed company."""
        sym = str(symbol).strip()
        key = self._cache.get_cache_key("tpex_rev", sym, str(months))
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        # TPEx monthly revenue endpoint
        url = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap05_O"
        time.sleep(_REQUEST_DELAY)
        data = _safe_get(url)
        if not data:
            return None

        fetched_at = datetime.utcnow().isoformat()
        rows = []
        for item in data:
            stock_id = item.get("公司代號", "").strip()
            if stock_id != sym:
                continue
            try:
                revenue_raw = str(item.get("當月營收", "0")).replace(",", "")
                revenue = float(revenue_raw) if revenue_raw else None
                rows.append({
                    "month": str(item.get("資料年月", "")).strip(),
                    "symbol": sym,
                    "name": item.get("公司名稱", ""),
                    "revenue": revenue,
                    "revenue_mom": None,
                    "revenue_yoy": None,
                    "accumulated_revenue": None,
                    "accumulated_yoy": None,
                    "source": "tpex_openapi",
                    "fetched_at": fetched_at,
                })
            except Exception as row_exc:
                logger.debug("TPExPublicProvider rev row error: %s", row_exc)

        if not rows:
            return None

        df = pd.DataFrame(rows)
        if months and len(df) > months:
            df = df.tail(months)
        self._cache.write_cache(key, df.to_dict("records"))
        return df.reset_index(drop=True)

    def get_institutional(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """Fetch institutional detail for an OTC-listed company."""
        sym = str(symbol).strip()
        key = self._cache.get_cache_key("tpex_inst", sym, str(start), str(end))
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        url = "https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes"
        time.sleep(_REQUEST_DELAY)
        data = _safe_get(url)
        if not data:
            return None

        fetched_at = datetime.utcnow().isoformat()
        rows = []
        for item in data:
            stock_id = item.get("SecuritiesCompanyCode", "").strip()
            if stock_id != sym:
                continue
            try:
                def _parse_int(v):
                    try:
                        return int(str(v).replace(",", ""))
                    except Exception:
                        return None

                fb = _parse_int(item.get("ForeignInvestorsBuyShares", 0)) or 0
                fs = _parse_int(item.get("ForeignInvestorsSellShares", 0)) or 0
                tb = _parse_int(item.get("InvestmentTrustBuyShares", 0)) or 0
                ts = _parse_int(item.get("InvestmentTrustSellShares", 0)) or 0
                db = _parse_int(item.get("DealersBuyShares", 0)) or 0
                ds = _parse_int(item.get("DealersSellShares", 0)) or 0
                rows.append({
                    "date": item.get("Date", ""),
                    "symbol": sym,
                    "foreign_net_buy": fb - fs,
                    "trust_net_buy": tb - ts,
                    "dealer_net_buy": db - ds,
                    "foreign_buy": fb,
                    "foreign_sell": fs,
                    "trust_buy": tb,
                    "trust_sell": ts,
                    "dealer_buy": db,
                    "dealer_sell": ds,
                    "source": "tpex_openapi",
                    "fetched_at": fetched_at,
                })
            except Exception as row_exc:
                logger.debug("TPExPublicProvider inst row error: %s", row_exc)

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

    def get_margin_short(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """Fetch margin/short balance for an OTC-listed company."""
        sym = str(symbol).strip()
        key = self._cache.get_cache_key("tpex_margin", sym, str(start), str(end))
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        url = "https://www.tpex.org.tw/openapi/v1/tpex_margin_purchase_short_sale"
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
                    "source": "tpex_openapi",
                    "fetched_at": fetched_at,
                })
            except Exception as row_exc:
                logger.debug("TPExPublicProvider margin row error: %s", row_exc)

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

    def health_check(self) -> dict:
        try:
            import requests
            resp = requests.head("https://www.tpex.org.tw/", timeout=5)
            ok = resp.status_code < 500
        except Exception:
            ok = False
        return {
            "ok": ok,
            "provider": self.name,
            "available": ok,
            "planned": False,
            "real_order": False,
            "note": "TPEx OTC public data provider",
        }
