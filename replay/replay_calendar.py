"""
replay/replay_calendar.py — ReplayTradingCalendar v1.2.0

Builds trading calendar from actual daily price data.
Does NOT assume Mon-Fri are trading days.
Does NOT use future network APIs.
Clamps out-of-range dates with explicit warning.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayTradingCalendar:
    """
    Builds trading calendar from actual daily price data.
    Does NOT assume Mon-Fri are trading days.
    Does NOT use future network APIs.
    Clamps out-of-range dates with explicit warning.
    """

    def __init__(self, repo_root=None):
        self.repo_root = Path(repo_root) if repo_root else Path(".")
        self._dates: List[str] = []          # sorted list of date strings for current symbol
        self._symbol: Optional[str] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def available_dates(self, symbol: str, start: Optional[str] = None, end: Optional[str] = None) -> List[str]:
        """Returns sorted list of available trading date strings for symbol."""
        self._ensure_loaded(symbol)
        dates = list(self._dates)
        if start:
            dates = [d for d in dates if d >= start]
        if end:
            dates = [d for d in dates if d <= end]
        return dates

    def normalize_date(self, date: str) -> str:
        """Returns date string as YYYY-MM-DD (strips time portion if present)."""
        if not date:
            return date
        return str(date)[:10]

    def nearest_previous_trading_day(self, date: str) -> Optional[str]:
        """Returns nearest trading day <= date from loaded calendar."""
        date = self.normalize_date(date)
        candidates = [d for d in self._dates if d <= date]
        return candidates[-1] if candidates else None

    def nearest_next_trading_day(self, date: str) -> Optional[str]:
        """Returns nearest trading day >= date from loaded calendar."""
        date = self.normalize_date(date)
        candidates = [d for d in self._dates if d >= date]
        return candidates[0] if candidates else None

    def first_available_date(self, symbol: str) -> Optional[str]:
        """Return first available trading date for symbol."""
        self._ensure_loaded(symbol)
        return self._dates[0] if self._dates else None

    def last_available_date(self, symbol: str) -> Optional[str]:
        """Return last available trading date for symbol."""
        self._ensure_loaded(symbol)
        return self._dates[-1] if self._dates else None

    def build_timeline(self, symbol: str, start: str, end: str) -> List[str]:
        """Returns sorted list of trading date strings between start and end (inclusive), from actual data."""
        self._ensure_loaded(symbol)
        return [d for d in self._dates if start <= d <= end]

    def index_of(self, date: str) -> int:
        """Returns index of date in loaded calendar, or -1 if not found."""
        date = self.normalize_date(date)
        try:
            return self._dates.index(date)
        except ValueError:
            return -1

    def date_at(self, index: int) -> Optional[str]:
        """Returns date string at index, or None if out of range."""
        if 0 <= index < len(self._dates):
            return self._dates[index]
        return None

    def is_trading_day(self, date: str) -> bool:
        """Returns True if date is a trading day in the loaded calendar."""
        return self.normalize_date(date) in self._dates

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_loaded(self, symbol: str) -> None:
        """Load price dates for symbol if not already loaded."""
        if self._symbol == symbol and self._dates:
            return
        self._symbol = symbol
        self._dates = self._load_price_dates(symbol)

    def _load_price_dates(self, symbol: str) -> List[str]:
        """
        Load dates from existing data store. Returns sorted list of date strings.
        Tries multiple common paths. Returns empty list with warning if not found.
        """
        try:
            import pandas as pd
        except ImportError:
            logger.warning("[ReplayTradingCalendar] pandas not available — empty calendar returned")
            return []

        search_paths = [
            self.repo_root / "data" / f"{symbol}.csv",
            self.repo_root / "data" / f"{symbol}_daily.csv",
            self.repo_root / "data" / "market" / f"{symbol}.csv",
            self.repo_root / "data" / "market" / f"{symbol}_daily.csv",
            self.repo_root / "data" / "price" / f"{symbol}.csv",
            self.repo_root / "data" / "price" / f"{symbol}_daily.csv",
            self.repo_root / "data" / "daily" / f"{symbol}.csv",
        ]

        # Also try glob pattern
        import glob
        glob_patterns = [
            str(self.repo_root / "data" / f"{symbol}*.csv"),
            str(self.repo_root / "data" / "market" / f"{symbol}*.csv"),
            str(self.repo_root / "data" / "price" / f"{symbol}*.csv"),
        ]

        found_files = []
        for p in search_paths:
            if p.exists():
                found_files.append(str(p))
                break

        if not found_files:
            for pattern in glob_patterns:
                matches = glob.glob(pattern)
                if matches:
                    found_files.extend(matches[:1])
                    break

        if not found_files:
            logger.warning(
                "[ReplayTradingCalendar] No price data found for symbol=%s under %s — empty calendar",
                symbol, self.repo_root / "data",
            )
            return []

        all_dates = set()
        for fpath in found_files:
            try:
                df = pd.read_csv(fpath, usecols=lambda c: c.lower() in ("date",), nrows=None)
                # find date column
                date_cols = [c for c in df.columns if c.lower() == "date"]
                if not date_cols:
                    # try first column
                    df2 = pd.read_csv(fpath, nrows=None)
                    if df2.empty:
                        continue
                    date_col = df2.columns[0]
                    date_series = pd.to_datetime(df2[date_col], errors="coerce")
                else:
                    date_series = pd.to_datetime(df[date_cols[0]], errors="coerce")
                valid = date_series.dropna()
                for d in valid:
                    all_dates.add(d.strftime("%Y-%m-%d"))
            except Exception as exc:
                logger.warning("[ReplayTradingCalendar] Failed reading %s: %s", fpath, exc)

        sorted_dates = sorted(all_dates)
        logger.debug("[ReplayTradingCalendar] Loaded %d trading dates for %s", len(sorted_dates), symbol)
        return sorted_dates
