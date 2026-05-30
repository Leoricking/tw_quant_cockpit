"""
data/providers/public_data_provider.py - Unified public data provider.

Aggregates all public API / crawler providers with a fallback chain:
    FinMind → TWSE/TPEx OpenAPI → MOPS crawler → existing CSV

Design:
    - Missing data returns None / empty DataFrame, never crashes.
    - Each source failure is logged as a warning; next source is tried.
    - Real mode never falls back to mock data.
    - No API key required for basic public data.
    - FINMIND_TOKEN optional (env var only).

Usage:
    from data.providers.public_data_provider import PublicDataProvider
    p = PublicDataProvider()
    df = p.get_monthly_revenue('2454', months=24)
    status = p.health_check()
"""

from __future__ import annotations

import logging
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


class PublicDataProvider:
    """
    Unified public data provider with source fallback chain.

    Fallback order per method:
        1. FinMind (if FINMIND_TOKEN or public access available)
        2. TWSE OpenAPI
        3. TPEx OpenAPI (for OTC stocks)
        4. MOPS crawler
    """

    def __init__(self, source: Optional[str] = None):
        """
        Parameters
        ----------
        source : str, optional
            Force a specific source: 'finmind', 'twse', 'tpex', 'mops', 'auto'.
            Default 'auto' tries all in fallback order.
        """
        self._forced_source = source or "auto"
        self._finmind = self._init_provider("finmind")
        self._twse = self._init_provider("twse")
        self._tpex = self._init_provider("tpex")
        self._mops = self._init_provider("mops")

    def _init_provider(self, name: str):
        try:
            if name == "finmind":
                from data.providers.finmind_provider import FinMindProvider
                return FinMindProvider()
            elif name == "twse":
                from data.providers.twse_public_provider import TWPublicProvider
                return TWPublicProvider()
            elif name == "tpex":
                from data.providers.tpex_public_provider import TPExPublicProvider
                return TPExPublicProvider()
            elif name == "mops":
                from data.providers.mops_crawler_provider import MOPSCrawlerProvider
                return MOPSCrawlerProvider()
        except Exception as exc:
            logger.warning("PublicDataProvider: cannot init %s: %s", name, exc)
        return None

    def _get_sources(self) -> list:
        """Return list of (name, provider) to try in order."""
        if self._forced_source == "finmind":
            return [("finmind", self._finmind)]
        elif self._forced_source == "twse":
            return [("twse", self._twse)]
        elif self._forced_source == "tpex":
            return [("tpex", self._tpex)]
        elif self._forced_source == "mops":
            return [("mops", self._mops)]
        # auto: try all in fallback order
        return [
            ("finmind", self._finmind),
            ("twse", self._twse),
            ("tpex", self._tpex),
            ("mops", self._mops),
        ]

    def _try_sources(self, method_name: str, *args, **kwargs) -> Optional[pd.DataFrame]:
        """Try each source in order; return first successful result."""
        for src_name, provider in self._get_sources():
            if provider is None:
                continue
            method = getattr(provider, method_name, None)
            if method is None:
                continue
            try:
                result = method(*args, **kwargs)
                if result is not None and (not isinstance(result, pd.DataFrame) or not result.empty):
                    logger.info("PublicDataProvider: %s via %s OK", method_name, src_name)
                    return result
            except Exception as exc:
                logger.warning(
                    "PublicDataProvider: %s via %s failed: %s",
                    method_name, src_name, exc
                )
        return None

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def get_monthly_revenue(
        self, symbol: str, months: int = 24
    ) -> Optional[pd.DataFrame]:
        """Fetch monthly revenue. Fallback chain: FinMind → TWSE → TPEx → MOPS."""
        return self._try_sources("get_monthly_revenue", symbol, months=months)

    def get_financial_statement(
        self, symbol: str, years: int = 5
    ) -> Optional[pd.DataFrame]:
        """Fetch financial statement (EPS, margins). Fallback: FinMind → MOPS."""
        for src_name, provider in self._get_sources():
            if provider is None:
                continue
            method = getattr(provider, "get_financial_statement", None)
            if method is None:
                continue
            try:
                result = method(symbol, years=years)
                if result is not None and not result.empty:
                    logger.info("PublicDataProvider: get_financial_statement via %s OK", src_name)
                    return result
            except Exception as exc:
                logger.warning("PublicDataProvider: get_financial_statement via %s failed: %s", src_name, exc)
        return None

    def get_eps(
        self, symbol: str, years: int = 5
    ) -> Optional[pd.DataFrame]:
        """Fetch EPS data. Subset of financial_statement."""
        df = self.get_financial_statement(symbol, years=years)
        if df is None or df.empty:
            return None
        cols = ["year", "quarter", "symbol", "eps", "announcement_date", "source", "fetched_at"]
        available_cols = [c for c in cols if c in df.columns]
        result = df[available_cols].copy()
        return result[result["eps"].notna()] if "eps" in result.columns else None

    def get_profitability(
        self, symbol: str, years: int = 5
    ) -> Optional[pd.DataFrame]:
        """Fetch gross_margin / operating_margin. Subset of financial_statement."""
        df = self.get_financial_statement(symbol, years=years)
        if df is None or df.empty:
            return None
        cols = ["year", "quarter", "symbol", "gross_margin", "operating_margin",
                "announcement_date", "source", "fetched_at"]
        available_cols = [c for c in cols if c in df.columns]
        return df[available_cols].copy()

    def get_financial_announcement_dates(
        self, symbol: str
    ) -> Optional[pd.DataFrame]:
        """Fetch financial announcement dates. Fallback: MOPS → FinMind."""
        # Try MOPS first (most reliable for announcement dates)
        if self._mops is not None:
            method = getattr(self._mops, "get_financial_announcement_dates", None)
            if method is not None:
                try:
                    result = method(symbol)
                    if result is not None and not result.empty:
                        return result
                except Exception as exc:
                    logger.warning("PublicDataProvider: announcement_dates via mops failed: %s", exc)
        return None

    def get_daily_price(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """Fetch historical daily OHLCV. Fallback chain: FinMind → TWSE → TPEx."""
        return self._try_sources("get_daily_price", symbol, start=start, end=end)

    def get_institutional_detail(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """Fetch institutional buy/sell detail. Fallback chain: FinMind → TWSE → TPEx."""
        return self._try_sources("get_institutional", symbol, start=start, end=end)

    def get_margin_short(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """Fetch margin/short balance. Fallback chain: FinMind → TWSE → TPEx."""
        return self._try_sources("get_margin_short", symbol, start=start, end=end)

    def health_check(self) -> dict:
        """Return health status of all sub-providers."""
        statuses = {}
        for name, provider in [
            ("finmind", self._finmind),
            ("twse", self._twse),
            ("tpex", self._tpex),
            ("mops", self._mops),
        ]:
            if provider is None:
                statuses[name] = {"ok": False, "note": "provider init failed"}
            else:
                try:
                    statuses[name] = provider.health_check()
                except Exception as exc:
                    statuses[name] = {"ok": False, "note": str(exc)}

        any_ok = any(v.get("ok") for v in statuses.values())
        return {
            "ok": any_ok,
            "provider": "public_data",
            "available": any_ok,
            "planned": False,
            "real_order": False,
            "sources": statuses,
            "note": "Unified public data provider (FinMind + TWSE + TPEx + MOPS)",
        }
