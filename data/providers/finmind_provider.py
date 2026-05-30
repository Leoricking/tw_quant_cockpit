"""
data/providers/finmind_provider.py - FinMind API provider.

Supports:
    - TaiwanStockMonthRevenue
    - TaiwanStockFinancialStatements
    - InstitutionalInvestorsBuySell
    - MarginPurchaseShortSaleBalance
    - TaiwanStockPrice

Token handling:
    - Optional: reads FINMIND_TOKEN from environment variable.
    - No token = limited / public access.
    - Never hardcodes or writes token to files.
    - If token not configured, shows warning but does not crash.

All output columns follow TW Quant Cockpit standard schema.
"""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from data.providers.base_provider import BaseMarketDataProvider
from data.api_cache import APICache

logger = logging.getLogger(__name__)

_FINMIND_API_URL = "https://api.finmindtrade.com/api/v4/data"
_REQUEST_DELAY = 1.0


def _get_token() -> Optional[str]:
    """
    Read FINMIND_TOKEN from environment or .env file.
    Returns None if not set. Never logs the full token.
    """
    # Try TokenSafeConfig first (reads .env without logging full value)
    try:
        from data.providers.token_safe_config import TokenSafeConfig
        cfg = TokenSafeConfig()
        cfg.load_env()
        token = cfg.get_token("FINMIND_TOKEN")
        if token:
            return token
    except Exception:
        pass
    # Fallback: read from os.environ directly
    token = os.environ.get("FINMIND_TOKEN", "").strip()
    return token if token else None


def _safe_fetch(dataset: str, stock_id: str, start_date: str = "", params_extra: dict = None, timeout: int = 30) -> Optional[list]:
    """Fetch data from FinMind API. Returns list of record dicts or None."""
    token = _get_token()
    params = {
        "dataset": dataset,
        "data_id": stock_id,
        "start_date": start_date,
        "token": token or "",
    }
    if params_extra:
        params.update(params_extra)

    try:
        import requests
        headers = {
            "User-Agent": "TW-Quant-Cockpit/0.3.9"
        }
        time.sleep(_REQUEST_DELAY)
        resp = requests.get(_FINMIND_API_URL, params=params, headers=headers, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == 200:
            return data.get("data", [])
        else:
            msg = data.get("msg", "unknown")
            logger.warning("FinMind API error dataset=%s stock=%s: %s", dataset, stock_id, msg)
            return None
    except Exception as exc:
        logger.warning("FinMind API request failed dataset=%s stock=%s: %s", dataset, stock_id, exc)
        return None


class FinMindProvider(BaseMarketDataProvider):
    """
    FinMind API provider.

    FINMIND_TOKEN env var is optional.  Basic public data may be accessible
    without a token.  Token-required datasets will fail gracefully.
    """

    name = "finmind"
    is_available = True
    is_planned = False

    def __init__(self, cache_ttl: int = 3600):
        self._cache = APICache(ttl_seconds=cache_ttl)
        token = _get_token()
        if token:
            logger.info("FinMindProvider: FINMIND_TOKEN configured")
        else:
            logger.info("FinMindProvider: FINMIND_TOKEN not set — limited public access")

    # ------------------------------------------------------------------
    # Monthly revenue
    # ------------------------------------------------------------------

    def get_monthly_revenue(
        self,
        symbol: str,
        months: int = 24,
    ) -> Optional[pd.DataFrame]:
        sym = str(symbol).strip()
        start_date = (datetime.today() - timedelta(days=months * 35)).strftime("%Y-%m-%d")
        key = self._cache.get_cache_key("fm_rev", sym, str(months))
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        data = _safe_fetch("TaiwanStockMonthRevenue", sym, start_date)
        if not data:
            return None

        fetched_at = datetime.utcnow().isoformat()
        rows = []
        for item in data:
            try:
                rev_raw = item.get("revenue", None)
                revenue = float(rev_raw) if rev_raw is not None else None
                mom_raw = item.get("revenue_growth_m/m")
                yoy_raw = item.get("revenue_growth_y/y")
                rows.append({
                    "month": str(item.get("date", ""))[:7],
                    "symbol": sym,
                    "name": item.get("company_name", ""),
                    "revenue": revenue,
                    "revenue_mom": float(mom_raw) / 100 if mom_raw is not None else None,
                    "revenue_yoy": float(yoy_raw) / 100 if yoy_raw is not None else None,
                    "accumulated_revenue": None,
                    "accumulated_yoy": None,
                    "source": "finmind",
                    "fetched_at": fetched_at,
                })
            except Exception as row_exc:
                logger.debug("FinMind revenue row error: %s", row_exc)

        if not rows:
            return None

        df = pd.DataFrame(rows)
        df = df.sort_values("month").reset_index(drop=True)
        if months and len(df) > months:
            df = df.tail(months).reset_index(drop=True)
        self._cache.write_cache(key, df.to_dict("records"))
        return df

    # ------------------------------------------------------------------
    # Financial statement
    # ------------------------------------------------------------------

    def get_financial_statement(
        self,
        symbol: str,
        years: int = 5,
    ) -> Optional[pd.DataFrame]:
        sym = str(symbol).strip()
        start_date = (datetime.today() - timedelta(days=years * 380)).strftime("%Y-%m-%d")
        key = self._cache.get_cache_key("fm_fin", sym, str(years))
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        data = _safe_fetch("TaiwanStockFinancialStatements", sym, start_date)
        if not data:
            return None

        fetched_at = datetime.utcnow().isoformat()
        rows = []
        # Group by date to build quarterly rows
        by_date: dict = {}
        for item in data:
            d = item.get("date", "")
            if d not in by_date:
                by_date[d] = {}
            by_date[d][item.get("type", "")] = item.get("value")

        for date_str, fields in by_date.items():
            try:
                gross_inc = fields.get("GrossProfit")
                revenue = fields.get("Revenue") or fields.get("OperatingRevenue")
                op_income = fields.get("OperatingIncome")
                net_income = fields.get("IncomeAfterTaxes") or fields.get("NetIncome") or fields.get("ProfitAttributeToParent")
                eps = fields.get("EPS")

                gross_margin = None
                if gross_inc is not None and revenue and float(revenue) != 0:
                    gross_margin = float(gross_inc) / float(revenue)

                op_margin = None
                if op_income is not None and revenue and float(revenue) != 0:
                    op_margin = float(op_income) / float(revenue)

                year_str = date_str[:4] if date_str else ""
                quarter_map = {"03": "Q1", "06": "Q2", "09": "Q3", "12": "Q4"}
                month_str = date_str[5:7] if len(date_str) >= 7 else ""
                quarter_str = quarter_map.get(month_str, "")

                rows.append({
                    "year": year_str,
                    "quarter": quarter_str,
                    "symbol": sym,
                    "eps": float(eps) if eps is not None else None,
                    "gross_margin": gross_margin,
                    "operating_margin": op_margin,
                    "operating_income": float(op_income) if op_income is not None else None,
                    "net_income": float(net_income) if net_income is not None else None,
                    "announcement_date": None,
                    "source": "finmind",
                    "fetched_at": fetched_at,
                })
            except Exception as row_exc:
                logger.debug("FinMind financial row error: %s", row_exc)

        if not rows:
            return None

        df = pd.DataFrame(rows).sort_values(["year", "quarter"]).reset_index(drop=True)
        self._cache.write_cache(key, df.to_dict("records"))
        return df

    # ------------------------------------------------------------------
    # Institutional detail
    # ------------------------------------------------------------------

    def get_institutional(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        sym = str(symbol).strip()
        start_date = start or (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
        key = self._cache.get_cache_key("fm_inst", sym, str(start_date), str(end))
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        data = _safe_fetch("InstitutionalInvestorsBuySell", sym, start_date)
        if not data:
            return None

        fetched_at = datetime.utcnow().isoformat()
        # FinMind returns one row per institution type per date — pivot to wide
        by_date: dict = {}
        for item in data:
            d = item.get("date", "")
            if d not in by_date:
                by_date[d] = {
                    "date": d, "symbol": sym,
                    "foreign_buy": 0, "foreign_sell": 0,
                    "trust_buy": 0, "trust_sell": 0,
                    "dealer_buy": 0, "dealer_sell": 0,
                    "source": "finmind", "fetched_at": fetched_at,
                }
            inst_type = item.get("name", "")
            buy = item.get("buy", 0) or 0
            sell = item.get("sell", 0) or 0
            if "外資" in inst_type or "Foreign" in inst_type:
                by_date[d]["foreign_buy"] += int(buy)
                by_date[d]["foreign_sell"] += int(sell)
            elif "投信" in inst_type or "Investment Trust" in inst_type:
                by_date[d]["trust_buy"] += int(buy)
                by_date[d]["trust_sell"] += int(sell)
            elif "自營" in inst_type or "Dealer" in inst_type:
                by_date[d]["dealer_buy"] += int(buy)
                by_date[d]["dealer_sell"] += int(sell)

        rows = []
        for d, row in by_date.items():
            row["foreign_net_buy"] = row["foreign_buy"] - row["foreign_sell"]
            row["trust_net_buy"] = row["trust_buy"] - row["trust_sell"]
            row["dealer_net_buy"] = row["dealer_buy"] - row["dealer_sell"]
            rows.append(row)

        if not rows:
            return None

        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        if end:
            df = df[df["date"] <= pd.to_datetime(end)]
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
        sym = str(symbol).strip()
        start_date = start or (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
        key = self._cache.get_cache_key("fm_margin", sym, str(start_date), str(end))
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        data = _safe_fetch("MarginPurchaseShortSaleBalance", sym, start_date)
        if not data:
            return None

        fetched_at = datetime.utcnow().isoformat()
        rows = []
        for item in data:
            try:
                rows.append({
                    "date": item.get("date", ""),
                    "symbol": sym,
                    "margin_balance": float(item.get("MarginPurchaseTodayBalance", 0) or 0),
                    "margin_change": float(item.get("MarginPurchaseChange", 0) or 0),
                    "short_balance": float(item.get("ShortSaleTodayBalance", 0) or 0),
                    "short_change": float(item.get("ShortSaleChange", 0) or 0),
                    "sbl_short_balance": None,
                    "source": "finmind",
                    "fetched_at": fetched_at,
                })
            except Exception as row_exc:
                logger.debug("FinMind margin row error: %s", row_exc)

        if not rows:
            return None

        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        if end:
            df = df[df["date"] <= pd.to_datetime(end)]
        df = df.sort_values("date").reset_index(drop=True)
        self._cache.write_cache(key, df.to_dict("records"))
        return df

    # ------------------------------------------------------------------
    # Historical daily price
    # ------------------------------------------------------------------

    def get_daily_price(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """Fetch historical daily OHLCV using TaiwanStockPrice dataset."""
        sym = str(symbol).strip()
        start_date = start or (datetime.today() - timedelta(days=365 * 3)).strftime("%Y-%m-%d")
        key = self._cache.get_cache_key("fm_daily", sym, str(start_date), str(end))
        cached = self._cache.read_cache(key)
        if cached is not None:
            try:
                return pd.DataFrame(cached)
            except Exception:
                pass

        data = _safe_fetch("TaiwanStockPrice", sym, start_date)
        if not data:
            return None

        rows = []
        for item in data:
            try:
                rows.append({
                    "date":   str(item.get("date", ""))[:10],
                    "symbol": sym,
                    "open":   float(item.get("open", 0) or 0),
                    "high":   float(item.get("max", 0) or 0),
                    "low":    float(item.get("min", 0) or 0),
                    "close":  float(item.get("close", 0) or 0),
                    "volume": float(item.get("Trading_Volume", 0) or 0),
                })
            except Exception as row_exc:
                logger.debug("FinMind daily price row error: %s", row_exc)

        if not rows:
            return None

        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        if end:
            df = df[df["date"] <= pd.to_datetime(end)]
        df = df.sort_values("date").reset_index(drop=True)
        self._cache.write_cache(key, df.to_dict("records"))
        return df

    # ------------------------------------------------------------------
    # Fundamental (EPS / margins) — v0.3.19 alias
    # ------------------------------------------------------------------

    def get_fundamental(
        self,
        symbol: str,
        months: int = 24,
    ) -> Optional[pd.DataFrame]:
        """
        Alias for get_financial_statement(), with month-based lookback.
        Returns DataFrame with eps, gross_margin, operating_margin, net_income,
        announcement_date, announcement_date_source, announcement_date_is_estimated.
        """
        years = max(1, months // 12)
        df = self.get_financial_statement(symbol, years=years)
        if df is None or df.empty:
            return None
        # Add v0.3.19 standard columns if missing
        if "announcement_date" not in df.columns:
            df["announcement_date"] = None
        if "announcement_date_source" not in df.columns:
            df["announcement_date_source"] = "estimated"
        if "announcement_date_is_estimated" not in df.columns:
            df["announcement_date_is_estimated"] = True
        # Synthesise date from year+quarter if missing
        if "date" not in df.columns:
            _qmap = {"Q1": "03", "Q2": "06", "Q3": "09", "Q4": "12"}
            df["date"] = df.apply(
                lambda r: f"{r.get('year', '2000')}-{_qmap.get(str(r.get('quarter', '')), '12')}-01",
                axis=1,
            )
        return df

    # ------------------------------------------------------------------
    # get_margin alias for v0.3.19 auto_fetcher compatibility
    # ------------------------------------------------------------------

    def get_margin(
        self,
        symbol: str,
        start: Optional[str] = None,
        end:   Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """Alias for get_margin_short()."""
        return self.get_margin_short(symbol, start=start, end=end)

    # ------------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------------

    def health_check(self) -> dict:
        token = _get_token()
        # Mask token for safe display — never log the full value
        try:
            from data.providers.token_safe_config import TokenSafeConfig
            _cfg = TokenSafeConfig()
            token_masked = _cfg.mask_token(token) if token else "(not configured)"
        except Exception:
            token_masked = "***" if token else "(not configured)"

        try:
            import requests
            resp = requests.head("https://api.finmindtrade.com/", timeout=5)
            ok = resp.status_code < 500
        except Exception:
            ok = False
        return {
            "ok": ok,
            "provider": self.name,
            "available": ok,
            "planned": False,
            "real_order": False,
            "supports_real_orders": False,
            "token_configured": token is not None,
            "token_masked": token_masked,
            "note": (
                "FinMind API provider — token configured" if token
                else "FinMind API provider — FINMIND_TOKEN not set (limited access)"
            ),
        }
