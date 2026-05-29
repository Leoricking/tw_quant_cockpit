"""
data/providers/csv_provider.py - CSV-based market data provider.

Wraps the existing RealDataLoader and DataSourceRouter so that all
downstream modules (features, reports, backtest) can consume data through
the BaseMarketDataProvider interface without knowing the underlying CSV
file structure.

This is the primary active provider in v0.3.x.  XQ export is a separate
transition provider (xq_export_provider.py).
"""

from __future__ import annotations

import logging
import os
from typing import Optional

import pandas as pd

from data.providers.base_provider import BaseMarketDataProvider

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CSVProvider(BaseMarketDataProvider):
    """
    Provider backed by standard CSV files in data/import/.

    File layout (managed by import-csv / batch-import / import-xq-export):
        data/import/profile/stock_profile.csv          (or *_sample.csv)
        data/import/daily/daily_k.csv                  (or *_sample.csv)
        data/import/institutional/institutional.csv    (or *_sample.csv)
        data/import/margin/margin.csv                  (or *_sample.csv)
        data/import/monthly_revenue/monthly_revenue.csv (or *_sample.csv)
        data/import/holder/holder.csv                  (or *_sample.csv)
        data/import/trust_cost/trust_cost.csv          (or *_sample.csv)
    """

    name = "csv"
    is_available = True
    is_planned = False

    def __init__(self):
        try:
            from data.real_data_loader import RealDataLoader
            self._loader = RealDataLoader()
            self._loader_ok = True
        except Exception as exc:
            logger.warning("CSVProvider: RealDataLoader init failed — %s", exc)
            self._loader = None
            self._loader_ok = False

    # ------------------------------------------------------------------
    # Core daily OHLCV
    # ------------------------------------------------------------------

    def get_daily(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """Return daily OHLCV as DataFrame, or None if unavailable."""
        if not self._loader_ok:
            return None
        try:
            result = self._loader.load_daily_k(symbol, n_bars=5000)
            if not result or not result.get("bars"):
                return None
            rows = result["bars"]
            df = pd.DataFrame(rows)
            df["date"] = pd.to_datetime(df["date"])
            df["symbol"] = symbol
            if start:
                df = df[df["date"] >= pd.to_datetime(start)]
            if end:
                df = df[df["date"] <= pd.to_datetime(end)]
            return df.sort_values("date").reset_index(drop=True) if not df.empty else None
        except Exception as exc:
            logger.warning("CSVProvider.get_daily(%s): %s", symbol, exc)
            return None

    # ------------------------------------------------------------------
    # Chip / institutional data
    # ------------------------------------------------------------------

    def get_institutional(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        if not self._loader_ok:
            return None
        try:
            result = self._loader.load_institutional(symbol)
            if not result:
                return None
            rows = result.get("rows") or []
            if not rows:
                return None
            df = pd.DataFrame(rows)
            df["date"] = pd.to_datetime(df["date"])
            if start:
                df = df[df["date"] >= pd.to_datetime(start)]
            if end:
                df = df[df["date"] <= pd.to_datetime(end)]
            return df.sort_values("date").reset_index(drop=True) if not df.empty else None
        except Exception as exc:
            logger.warning("CSVProvider.get_institutional(%s): %s", symbol, exc)
            return None

    def get_margin(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        if not self._loader_ok:
            return None
        try:
            result = self._loader.load_margin(symbol)
            if not result:
                return None
            rows = result.get("rows") or []
            if not rows:
                return None
            df = pd.DataFrame(rows)
            df["date"] = pd.to_datetime(df["date"])
            if start:
                df = df[df["date"] >= pd.to_datetime(start)]
            if end:
                df = df[df["date"] <= pd.to_datetime(end)]
            return df.sort_values("date").reset_index(drop=True) if not df.empty else None
        except Exception as exc:
            logger.warning("CSVProvider.get_margin(%s): %s", symbol, exc)
            return None

    # ------------------------------------------------------------------
    # Fundamentals
    # ------------------------------------------------------------------

    def get_monthly_revenue(
        self, symbol: str, months: int = 24
    ) -> Optional[pd.DataFrame]:
        if not self._loader_ok:
            return None
        try:
            result = self._loader.load_monthly_revenue(symbol)
            if not result:
                return None
            rows = result.get("rows") or []
            if not rows:
                return None
            df = pd.DataFrame(rows)
            if months:
                df = df.tail(months)
            return df.reset_index(drop=True)
        except Exception as exc:
            logger.warning("CSVProvider.get_monthly_revenue(%s): %s", symbol, exc)
            return None

    def get_holder(self, symbol: str) -> Optional[pd.DataFrame]:
        if not self._loader_ok:
            return None
        try:
            result = self._loader.load_holder(symbol)
            if not result:
                return None
            rows = result.get("rows") or []
            if not rows:
                return None
            return pd.DataFrame(rows)
        except Exception as exc:
            logger.warning("CSVProvider.get_holder(%s): %s", symbol, exc)
            return None

    def get_trust_cost(self, symbol: str) -> Optional[pd.DataFrame]:
        if not self._loader_ok:
            return None
        try:
            result = self._loader.load_trust_cost(symbol)
            if not result:
                return None
            rows = result.get("rows") or []
            if not rows:
                return None
            return pd.DataFrame(rows)
        except Exception as exc:
            logger.warning("CSVProvider.get_trust_cost(%s): %s", symbol, exc)
            return None

    def get_profile(self, symbol: str) -> Optional[dict]:
        if not self._loader_ok:
            return None
        try:
            return self._loader.load_profile(symbol)
        except Exception as exc:
            logger.warning("CSVProvider.get_profile(%s): %s", symbol, exc)
            return None

    # ------------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------------

    def health_check(self) -> dict:
        import_dir = os.path.join(_BASE_DIR, "data", "import")
        daily_dir = os.path.join(import_dir, "daily")
        has_data = os.path.isdir(daily_dir) and bool(os.listdir(daily_dir))
        return {
            "ok": self._loader_ok and has_data,
            "provider": self.name,
            "available": self._loader_ok,
            "planned": False,
            "real_order": False,
            "data_dir": import_dir,
            "has_data_files": has_data,
            "note": "CSV files in data/import/ (primary active provider)",
        }


# Safe backward-compatibility alias (v0.3.6 Phase 2)
CSVDataProvider = CSVProvider
