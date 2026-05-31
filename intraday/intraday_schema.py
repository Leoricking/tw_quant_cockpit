"""
intraday/intraday_schema.py — Intraday standard schema and column normalization (v0.3.27).
[!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    import pandas as pd
    _PANDAS_OK = True
except ImportError:
    _PANDAS_OK = False
    logger.warning("pandas not available — IntradaySchema will be limited")

try:
    import numpy as np
    _NUMPY_OK = True
except ImportError:
    _NUMPY_OK = False


class IntradaySchema:
    """
    Intraday standard schema, column normalization, and validation.

    [!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.

    Safety flags
    ------------
    read_only           : True  — never writes to broker or order system
    no_real_orders      : True  — no order generation
    production_blocked  : True  — must not be used in live trading
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    STANDARD_COLUMNS: List[str] = [
        "symbol", "name", "date", "time", "datetime", "freq",
        "open", "high", "low", "close", "volume", "amount",
        "vwap", "source", "fetched_at", "imported_at",
    ]

    REQUIRED_BY_FREQ: Dict[str, List[str]] = {
        "1min": ["symbol", "date", "time", "datetime", "freq",
                 "open", "high", "low", "close", "volume", "source"],
        "5min": ["symbol", "date", "time", "datetime", "freq",
                 "open", "high", "low", "close", "volume", "source"],
        "tick": ["symbol", "date", "time", "datetime",
                 "price", "volume", "source"],
        "bidask": ["symbol", "date", "time", "datetime",
                   "bid_price_1", "bid_volume_1",
                   "ask_price_1", "ask_volume_1", "source"],
    }

    OPTIONAL_BY_FREQ: Dict[str, List[str]] = {
        "1min": ["name", "amount", "vwap", "fetched_at", "imported_at"],
        "5min": ["name", "amount", "vwap", "fetched_at", "imported_at"],
        "tick": ["amount", "side", "is_large_trade"],
        "bidask": [
            "bid_price_2", "bid_price_3", "bid_price_4", "bid_price_5",
            "bid_volume_2", "bid_volume_3", "bid_volume_4", "bid_volume_5",
            "ask_price_2", "ask_price_3", "ask_price_4", "ask_price_5",
            "ask_volume_2", "ask_volume_3", "ask_volume_4", "ask_volume_5",
            "spread", "order_imbalance",
        ],
    }

    XQ_COLUMN_MAP: Dict[str, str] = {
        "開盤價": "open",
        "最高價": "high",
        "最低價": "low",
        "收盤價": "close",
        "成交量": "volume",
        "成交金額": "amount",
        "日期": "date",
        "時間": "time",
        "商品代號": "symbol",
        "股票代號": "symbol",
        "名稱": "name",
        "代碼": "symbol",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
        "Amount": "amount",
        "Date": "date",
        "Time": "time",
    }

    def standard_columns(self) -> List[str]:
        """Return the list of standard schema columns."""
        return list(self.STANDARD_COLUMNS)

    def required_columns(self, freq: str = "1min") -> List[str]:
        """Return required columns for the given frequency."""
        return list(self.REQUIRED_BY_FREQ.get(freq, self.REQUIRED_BY_FREQ["1min"]))

    def optional_columns(self, freq: str = "1min") -> List[str]:
        """Return optional columns for the given frequency."""
        return list(self.OPTIONAL_BY_FREQ.get(freq, self.OPTIONAL_BY_FREQ["1min"]))

    def normalize_columns(self, df):
        """
        Apply XQ_COLUMN_MAP renaming then lowercase any remaining columns.

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        pd.DataFrame
        """
        if not _PANDAS_OK:
            raise RuntimeError("pandas is required for normalize_columns")
        df = df.copy()
        rename_map = {}
        for col in df.columns:
            if col in self.XQ_COLUMN_MAP:
                rename_map[col] = self.XQ_COLUMN_MAP[col]
        if rename_map:
            df = df.rename(columns=rename_map)
        # Lowercase remaining columns (skip already-mapped ones)
        df.columns = [c.lower() if c == c else c for c in df.columns]
        return df

    def validate(self, df, freq: str = "1min") -> dict:
        """
        Validate a DataFrame against the schema for the given frequency.

        Returns
        -------
        dict with keys: ok, missing_required, extra_columns, row_count, warnings
        """
        if not _PANDAS_OK:
            return {"ok": False, "missing_required": [], "extra_columns": [],
                    "row_count": 0, "warnings": ["pandas not available"]}
        if df is None or df.empty:
            return {"ok": False, "missing_required": self.required_columns(freq),
                    "extra_columns": [], "row_count": 0,
                    "warnings": ["DataFrame is None or empty"]}

        required = self.required_columns(freq)
        optional = self.optional_columns(freq)
        all_known = required + optional

        cols = list(df.columns)
        missing_required = [c for c in required if c not in cols]
        extra_columns = [c for c in cols if c not in all_known]

        warnings = []
        if missing_required:
            warnings.append(f"Missing required columns: {missing_required}")
        if extra_columns:
            warnings.append(f"Extra/unknown columns: {extra_columns}")

        ok = len(missing_required) == 0
        return {
            "ok": ok,
            "missing_required": missing_required,
            "extra_columns": extra_columns,
            "row_count": len(df),
            "warnings": warnings,
        }

    def fill_missing_optional_columns(self, df, freq: str = "1min"):
        """
        Add missing optional columns as NaN columns.

        Returns
        -------
        pd.DataFrame
        """
        if not _PANDAS_OK:
            raise RuntimeError("pandas is required")
        df = df.copy()
        optional = self.optional_columns(freq)
        for col in optional:
            if col not in df.columns:
                df[col] = float("nan")
        return df

    def coerce_dtypes(self, df, freq: str = "1min"):
        """
        Coerce numeric columns to float, date/time to str, volume to int64 if possible.

        Returns
        -------
        pd.DataFrame
        """
        if not _PANDAS_OK:
            raise RuntimeError("pandas is required")
        df = df.copy()
        numeric_cols = ["open", "high", "low", "close", "amount", "vwap",
                        "price", "bid_price_1", "ask_price_1", "spread",
                        "order_imbalance"]
        volume_cols = ["volume", "bid_volume_1", "ask_volume_1"]
        str_cols = ["date", "time", "datetime", "symbol", "name", "source",
                    "freq", "fetched_at", "imported_at"]

        for col in numeric_cols:
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                except Exception as exc:
                    logger.warning("coerce_dtypes: %s → float failed: %s", col, exc)

        for col in volume_cols:
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                    df[col] = df[col].astype("Int64")
                except Exception as exc:
                    logger.warning("coerce_dtypes: %s → Int64 failed: %s", col, exc)

        for col in str_cols:
            if col in df.columns:
                try:
                    df[col] = df[col].astype(str)
                    df[col] = df[col].replace("nan", "").replace("<NA>", "")
                except Exception as exc:
                    logger.warning("coerce_dtypes: %s → str failed: %s", col, exc)

        return df

    def build_datetime(self, df):
        """
        Create 'datetime' column from 'date' + 'time' if missing or all-empty.

        Format: 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DD HH:MM'

        Returns
        -------
        pd.DataFrame
        """
        if not _PANDAS_OK:
            raise RuntimeError("pandas is required")
        df = df.copy()

        # If datetime column already present and populated, skip
        if "datetime" in df.columns:
            non_empty = df["datetime"].astype(str).replace("", None).replace("nan", None).dropna()
            if len(non_empty) > 0:
                return df

        if "date" not in df.columns or "time" not in df.columns:
            logger.warning("build_datetime: 'date' and/or 'time' columns missing")
            if "datetime" not in df.columns:
                df["datetime"] = ""
            return df

        try:
            date_str = df["date"].astype(str).str.strip()
            time_str = df["time"].astype(str).str.strip()
            combined = date_str + " " + time_str
            # Attempt to parse and reformat
            parsed = pd.to_datetime(combined, errors="coerce")
            # Format as YYYY-MM-DD HH:MM:SS (or HH:MM where seconds not present)
            df["datetime"] = parsed.dt.strftime("%Y-%m-%d %H:%M:%S")
            # Where parse failed, keep raw concatenation
            mask_failed = parsed.isna()
            if mask_failed.any():
                df.loc[mask_failed, "datetime"] = combined[mask_failed]
        except Exception as exc:
            logger.warning("build_datetime failed: %s", exc)
            df["datetime"] = df.get("date", "") + " " + df.get("time", "")

        return df
