"""
data/intraday_data_importer.py - Intraday data importer for XQ 1min / 5min data.

Imports per-minute / 5-minute bar data from XQ exports or other sources.
Stores to: data/import/intraday/1min/ and data/import/intraday/5min/

Standard columns:
    symbol, date, time, datetime, open, high, low, close, volume, source
Optional columns:
    vwap, big_buy_sell_power, retail_buy_sell_power,
    bid_volume, ask_volume, buy_sell_pressure

Cleaning rules:
    - Only keep 09:00:00 ~ 13:30:00 (Taiwan trading hours)
    - Remove blank rows
    - Remove duplicate datetime rows
    - Convert prices to float
    - Convert volumes to float
    - Auto-fill symbol from filename
    - Auto-derive date, time, datetime from source columns
    - Convert Chinese column headers to standard English
    - Never mix intraday data into daily CSV
"""

from __future__ import annotations

import logging
import os
import re
from datetime import datetime, time as dt_time
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_INTRADAY_BASE = os.path.join(_BASE_DIR, "data", "import", "intraday")
_1MIN_DIR = os.path.join(_INTRADAY_BASE, "1min")
_5MIN_DIR = os.path.join(_INTRADAY_BASE, "5min")

_STANDARD_COLS = [
    "symbol", "date", "time", "datetime", "open", "high", "low", "close", "volume", "source"
]
_OPTIONAL_COLS = [
    "vwap", "big_buy_sell_power", "retail_buy_sell_power",
    "bid_volume", "ask_volume", "buy_sell_pressure",
]

# Taiwan trading hours (inclusive)
_MARKET_OPEN = dt_time(9, 0, 0)
_MARKET_CLOSE = dt_time(13, 30, 0)

# Chinese → English column map
_COL_MAP = {
    "時間": "time",
    "日期": "date",
    "開盤": "open",
    "開盤價": "open",
    "最高": "high",
    "最高價": "high",
    "最低": "low",
    "最低價": "low",
    "收盤": "close",
    "收盤價": "close",
    "成交量": "volume",
    "成交額": "amount",
    "買量": "bid_volume",
    "賣量": "ask_volume",
    "均價": "vwap",
    "日期時間": "datetime",
    "股票代碼": "symbol",
    "代碼": "symbol",
}

_TAIWAN_MARKET_OPEN = "09:00:00"
_TAIWAN_MARKET_CLOSE = "13:30:00"


def _remap_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename Chinese column headers to standard English names."""
    rename = {}
    for col in df.columns:
        col_str = str(col).strip()
        if col_str in _COL_MAP:
            rename[col] = _COL_MAP[col_str]
        elif col_str.lower() in [v.lower() for v in _COL_MAP.values()]:
            rename[col] = col_str.lower()
    if rename:
        df = df.rename(columns=rename)
    return df


def _infer_symbol_from_path(path: str) -> str:
    """Infer stock symbol from file name, e.g. '2454_1min.csv' -> '2454'."""
    fname = os.path.splitext(os.path.basename(path))[0]
    match = re.match(r"^(\d{4,6})", fname)
    return match.group(1) if match else ""


def _clean_intraday(df: pd.DataFrame, symbol: str, freq: str) -> pd.DataFrame:
    """
    Apply standard cleaning rules to intraday DataFrame.

    Parameters
    ----------
    df : raw DataFrame from CSV/Excel
    symbol : stock symbol string
    freq : '1min' or '5min'

    Returns
    -------
    Cleaned DataFrame with standard columns.
    """
    if df.empty:
        return pd.DataFrame(columns=_STANDARD_COLS)

    df = _remap_columns(df)
    df = df.copy()

    # Fill symbol
    if "symbol" not in df.columns or df["symbol"].isna().all():
        df["symbol"] = symbol

    # Build datetime column
    if "datetime" not in df.columns:
        if "date" in df.columns and "time" in df.columns:
            df["datetime"] = pd.to_datetime(
                df["date"].astype(str) + " " + df["time"].astype(str),
                errors="coerce",
            )
        elif "date" in df.columns:
            df["datetime"] = pd.to_datetime(df["date"], errors="coerce")
        else:
            # Try parsing first column as datetime
            first_col = df.columns[0]
            df["datetime"] = pd.to_datetime(df[first_col], errors="coerce")

    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df = df.dropna(subset=["datetime"])

    # Derive date and time columns from datetime
    df["date"] = df["datetime"].dt.strftime("%Y-%m-%d")
    df["time"] = df["datetime"].dt.strftime("%H:%M:%S")

    # Filter Taiwan trading hours: 09:00:00 ~ 13:30:00
    t_open = pd.to_datetime(_TAIWAN_MARKET_OPEN, format="%H:%M:%S").time()
    t_close = pd.to_datetime(_TAIWAN_MARKET_CLOSE, format="%H:%M:%S").time()
    df["_time"] = df["datetime"].dt.time
    df = df[(df["_time"] >= t_open) & (df["_time"] <= t_close)].copy()
    df = df.drop(columns=["_time"], errors="ignore")

    # Drop blank rows
    df = df.dropna(how="all")

    # Deduplicate by datetime + symbol
    df = df.drop_duplicates(subset=["datetime", "symbol"])

    # Convert OHLCV to numeric
    for col in ["open", "high", "low", "close"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "volume" in df.columns:
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

    # Add source
    df["source"] = f"xq_intraday_{freq}"

    # Ensure all standard cols exist
    for col in _STANDARD_COLS:
        if col not in df.columns:
            df[col] = None

    # Optional cols if present
    final_cols = _STANDARD_COLS + [c for c in _OPTIONAL_COLS if c in df.columns]
    df = df[final_cols]

    return df.sort_values("datetime").reset_index(drop=True)


def _output_path(symbol: str, freq: str) -> str:
    """Return output CSV path for a given symbol and frequency."""
    out_dir = _1MIN_DIR if freq == "1min" else _5MIN_DIR
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, f"{symbol}_{freq}.csv")


def _merge_write(path: str, df_new: pd.DataFrame, replace: bool = False) -> int:
    """Merge new intraday data with existing, write to CSV. Returns rows written."""
    if replace or not os.path.isfile(path):
        df_new.to_csv(path, index=False, encoding="utf-8-sig")
        return len(df_new)
    try:
        existing = pd.read_csv(path, parse_dates=["datetime"])
    except Exception:
        existing = pd.DataFrame()

    combined = pd.concat([existing, df_new], ignore_index=True)
    if "datetime" in combined.columns and "symbol" in combined.columns:
        combined = combined.drop_duplicates(subset=["datetime", "symbol"])
    if "datetime" in combined.columns:
        combined = combined.sort_values("datetime")
    combined.to_csv(path, index=False, encoding="utf-8-sig")
    return len(combined)


class IntradayDataImporter:
    """
    Importer for XQ intraday 1min / 5min bar data.

    Supports:
        - Single file import
        - Folder scan import
        - dry-run mode
    """

    def __init__(self, dry_run: bool = False, replace: bool = False):
        self.dry_run = dry_run
        self.replace = replace

    def import_file(
        self,
        file_path: str,
        symbol: Optional[str] = None,
        freq: str = "1min",
    ) -> dict:
        """
        Import a single intraday CSV or Excel file.

        Returns result dict: symbol, freq, rows_imported, output_path, warnings.
        """
        result = {
            "file": file_path,
            "symbol": symbol or _infer_symbol_from_path(file_path),
            "freq": freq,
            "rows_imported": 0,
            "output_path": None,
            "warnings": [],
            "dry_run": self.dry_run,
        }
        sym = result["symbol"]

        if not os.path.isfile(file_path):
            result["warnings"].append(f"File not found: {file_path}")
            return result

        # Read file
        try:
            ext = os.path.splitext(file_path)[1].lower()
            if ext in (".xlsx", ".xls"):
                df_raw = pd.read_excel(file_path, dtype=str)
            else:
                try:
                    df_raw = pd.read_csv(file_path, dtype=str, encoding="utf-8-sig")
                except UnicodeDecodeError:
                    df_raw = pd.read_csv(file_path, dtype=str, encoding="cp950")
        except Exception as exc:
            result["warnings"].append(f"Cannot read file {file_path}: {exc}")
            return result

        if df_raw.empty:
            result["warnings"].append(f"File is empty: {file_path}")
            return result

        # Clean
        df_clean = _clean_intraday(df_raw, sym, freq)

        if df_clean.empty:
            result["warnings"].append(
                f"{sym}: no bars in Taiwan trading hours after cleaning"
            )
            return result

        out_path = _output_path(sym, freq)
        result["output_path"] = out_path
        result["rows_imported"] = len(df_clean)

        if self.dry_run:
            logger.info(
                "IntradayDataImporter DRY-RUN: %s %s — %d bars would be written to %s",
                sym, freq, len(df_clean), out_path,
            )
        else:
            written = _merge_write(out_path, df_clean, replace=self.replace)
            result["rows_imported"] = written
            logger.info(
                "IntradayDataImporter: wrote %d bars for %s %s to %s",
                written, sym, freq, out_path,
            )

        return result

    def import_folder(
        self,
        folder: str,
        freq: str = "1min",
    ) -> list:
        """
        Scan a folder for intraday CSV/Excel files and import all.

        Returns list of result dicts (one per file found).
        """
        if not os.path.isdir(folder):
            logger.warning("IntradayDataImporter: folder not found: %s", folder)
            return [{"folder": folder, "warnings": [f"Folder not found: {folder}"], "files_found": 0}]

        results = []
        for fname in sorted(os.listdir(folder)):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in (".csv", ".xlsx", ".xls"):
                continue
            # Only import files that look like intraday (freq in name or just symbol)
            fpath = os.path.join(folder, fname)
            sym = _infer_symbol_from_path(fpath)
            if not sym:
                logger.debug("IntradayDataImporter: skipping %s (cannot infer symbol)", fname)
                continue
            result = self.import_file(fpath, symbol=sym, freq=freq)
            results.append(result)

        if not results:
            logger.info("IntradayDataImporter: no importable files found in %s", folder)

        return results

    def status(self) -> dict:
        """Return current intraday data status (count of files per freq)."""
        def _count_files(d):
            if not os.path.isdir(d):
                return 0
            return len([f for f in os.listdir(d) if f.endswith(".csv")])

        return {
            "intraday_1min_files": _count_files(_1MIN_DIR),
            "intraday_5min_files": _count_files(_5MIN_DIR),
            "1min_dir": _1MIN_DIR,
            "5min_dir": _5MIN_DIR,
        }

    def load_intraday(
        self,
        symbol: str,
        freq: str = "1min",
        date: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """
        Load intraday data for a symbol.

        Parameters
        ----------
        symbol : str
        freq : '1min' or '5min'
        date : optional date string 'YYYY-MM-DD' to filter a single day

        Returns
        -------
        pd.DataFrame or None if not available
        """
        path = _output_path(symbol, freq)
        if not os.path.isfile(path):
            return None
        try:
            df = pd.read_csv(path, parse_dates=["datetime"])
            if date:
                df = df[df["date"] == date]
            return df if not df.empty else None
        except Exception as exc:
            logger.warning("IntradayDataImporter.load_intraday(%s, %s): %s", symbol, freq, exc)
            return None

    def load_intraday_standard(
        self,
        symbol: str,
        freq: str = "1min",
        date: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """
        Load standardized intraday data for a symbol from intraday_standard/.

        The standardized path is data/import/intraday_standard/{freq}/{symbol}_{freq}.csv,
        written by IntradayDataPipeline (v0.3.27).

        Returns pd.DataFrame or None if not available.
        """
        std_dir = os.path.join(_BASE_DIR, "data", "import", "intraday_standard", freq)
        path = os.path.join(std_dir, f"{symbol}_{freq}.csv")
        if not os.path.isfile(path):
            # Fall back to legacy path
            return self.load_intraday(symbol, freq=freq, date=date)
        try:
            df = pd.read_csv(path, parse_dates=["datetime"])
            if date:
                df = df[df["date"] == date]
            return df if not df.empty else None
        except Exception as exc:
            logger.warning("load_intraday_standard(%s, %s): %s", symbol, freq, exc)
            return self.load_intraday(symbol, freq=freq, date=date)
