"""
coverage_repair/issue_detector.py — CoverageIssueDetector for TW Quant Cockpit v1.1.2.

Detects: missing, insufficient, partial, stale, duplicate, conflict, invalid issues.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Read-only detection. No data modification in this module.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional, Dict

from coverage_repair.coverage_repair_schema import (
    CoverageIssue,
    ISSUE_MISSING, ISSUE_INSUFFICIENT, ISSUE_PARTIAL,
    ISSUE_STALE, ISSUE_DUPLICATE, ISSUE_CONFLICT, ISSUE_INVALID,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Coverage thresholds (aligned with UniverseCoverageAnalyzer)
MIN_ROWS_READY       = 240   # READY threshold
MIN_ROWS_PARTIAL     = 120   # PARTIAL threshold
MIN_ROWS_INSUFFICIENT = 1    # anything > 0 but < PARTIAL
STALE_DAYS_THRESHOLD = 30    # data older than this is STALE


class CoverageIssueDetector:
    """Detects coverage issues for symbols and datasets.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Read-only: does NOT modify any data.
    """

    research_only  = True
    no_real_orders = True

    DATASETS = ["daily", "margin", "institutional", "monthly_revenue", "trust_cost", "holder"]

    def detect_all(self, symbols: Optional[List[str]] = None) -> List[CoverageIssue]:
        """Detect all coverage issues for all symbols (or given subset)."""
        issues: List[CoverageIssue] = []
        if symbols is None:
            symbols = self._discover_symbols()
        for symbol in symbols:
            for dataset in self.DATASETS:
                detected = self._detect_symbol_dataset(symbol, dataset)
                issues.extend(detected)
        return issues

    def detect_symbol(self, symbol: str) -> List[CoverageIssue]:
        """Detect all issues for a single symbol across all datasets."""
        issues: List[CoverageIssue] = []
        for dataset in self.DATASETS:
            detected = self._detect_symbol_dataset(symbol, dataset)
            issues.extend(detected)
        return issues

    def _detect_symbol_dataset(self, symbol: str, dataset: str) -> List[CoverageIssue]:
        issues: List[CoverageIssue] = []
        data_path = self._data_path(symbol, dataset)
        ts = datetime.now().strftime("%Y%m%d%H%M%S%f")

        # 1. Check MISSING
        if not os.path.isfile(data_path):
            issues.append(CoverageIssue(
                issue_id=f"missing_{symbol}_{dataset}_{ts}",
                symbol=symbol,
                dataset=dataset,
                issue_type=ISSUE_MISSING,
                description=f"No data file found for {symbol}/{dataset}",
                row_count=0,
                expected_min_rows=MIN_ROWS_READY,
            ))
            return issues

        # Load data
        df = self._load_csv(data_path)
        if df is None:
            issues.append(CoverageIssue(
                issue_id=f"invalid_{symbol}_{dataset}_{ts}",
                symbol=symbol,
                dataset=dataset,
                issue_type=ISSUE_INVALID,
                description=f"Failed to load data file for {symbol}/{dataset}",
                row_count=0,
            ))
            return issues

        row_count = len(df)

        # 2. Check INSUFFICIENT / PARTIAL
        if row_count == 0:
            issues.append(CoverageIssue(
                issue_id=f"missing_{symbol}_{dataset}_{ts}a",
                symbol=symbol,
                dataset=dataset,
                issue_type=ISSUE_MISSING,
                description=f"Data file exists but is empty for {symbol}/{dataset}",
                row_count=0,
                expected_min_rows=MIN_ROWS_READY,
            ))
            return issues
        elif row_count < MIN_ROWS_PARTIAL:
            issues.append(CoverageIssue(
                issue_id=f"insufficient_{symbol}_{dataset}_{ts}",
                symbol=symbol,
                dataset=dataset,
                issue_type=ISSUE_INSUFFICIENT,
                description=f"{symbol}/{dataset} has only {row_count} rows (min={MIN_ROWS_PARTIAL})",
                row_count=row_count,
                expected_min_rows=MIN_ROWS_PARTIAL,
            ))
        elif row_count < MIN_ROWS_READY:
            issues.append(CoverageIssue(
                issue_id=f"partial_{symbol}_{dataset}_{ts}",
                symbol=symbol,
                dataset=dataset,
                issue_type=ISSUE_PARTIAL,
                description=f"{symbol}/{dataset} has {row_count} rows (READY needs {MIN_ROWS_READY})",
                row_count=row_count,
                expected_min_rows=MIN_ROWS_READY,
            ))

        # 3. Check STALE (only for daily dataset)
        if dataset == "daily":
            last_date = self._get_last_date(df)
            if last_date:
                try:
                    last_dt = datetime.strptime(last_date, "%Y-%m-%d")
                    age_days = (datetime.now() - last_dt).days
                    if age_days > STALE_DAYS_THRESHOLD:
                        issues.append(CoverageIssue(
                            issue_id=f"stale_{symbol}_{dataset}_{ts}",
                            symbol=symbol,
                            dataset=dataset,
                            issue_type=ISSUE_STALE,
                            description=f"{symbol}/{dataset} last date is {last_date} ({age_days} days ago)",
                            row_count=row_count,
                            last_date=last_date,
                        ))
                except Exception:
                    pass

        # 4. Check DUPLICATE and CONFLICT
        date_col = self._find_date_col(df)
        if date_col and date_col in df.columns:
            dup_issues = self._detect_duplicates(df, date_col, symbol, dataset, ts)
            issues.extend(dup_issues)

        # 5. Check INVALID OHLC (only for daily dataset)
        if dataset == "daily":
            invalid_issues = self._detect_invalid_ohlc(df, symbol, dataset, ts, row_count)
            issues.extend(invalid_issues)

        return issues

    def _detect_duplicates(self, df, date_col: str, symbol: str, dataset: str, ts: str) -> List[CoverageIssue]:
        issues: List[CoverageIssue] = []
        try:
            dup_mask = df.duplicated(subset=[date_col], keep=False)
            dup_df = df[dup_mask]
            if len(dup_df) == 0:
                return issues

            dup_dates = sorted(dup_df[date_col].astype(str).unique().tolist())

            # Check if duplicates are identical (same values) or conflicting (different values)
            value_cols = [c for c in df.columns if c != date_col]
            identical_dates = []
            conflict_dates = []
            for d in dup_dates:
                rows = df[df[date_col].astype(str) == str(d)]
                if len(rows) > 1:
                    if len(value_cols) > 0:
                        # All rows identical?
                        first = rows.iloc[0][value_cols].tolist()
                        all_identical = all(
                            rows.iloc[i][value_cols].tolist() == first
                            for i in range(1, len(rows))
                        )
                        if all_identical:
                            identical_dates.append(str(d))
                        else:
                            conflict_dates.append(str(d))
                    else:
                        identical_dates.append(str(d))

            if identical_dates:
                issues.append(CoverageIssue(
                    issue_id=f"duplicate_{symbol}_{dataset}_{ts}",
                    symbol=symbol,
                    dataset=dataset,
                    issue_type=ISSUE_DUPLICATE,
                    description=f"{symbol}/{dataset} has {len(identical_dates)} identical duplicate date(s)",
                    row_count=len(df),
                    affected_dates=identical_dates[:20],
                    details={"duplicate_count": len(identical_dates)},
                ))

            if conflict_dates:
                issues.append(CoverageIssue(
                    issue_id=f"conflict_{symbol}_{dataset}_{ts}",
                    symbol=symbol,
                    dataset=dataset,
                    issue_type=ISSUE_CONFLICT,
                    description=f"{symbol}/{dataset} has {len(conflict_dates)} conflicting date(s) with different values",
                    row_count=len(df),
                    affected_dates=conflict_dates[:20],
                    details={"conflict_count": len(conflict_dates)},
                ))
        except Exception as exc:
            logger.warning("_detect_duplicates %s/%s: %s", symbol, dataset, exc)
        return issues

    def _detect_invalid_ohlc(self, df, symbol: str, dataset: str, ts: str, row_count: int) -> List[CoverageIssue]:
        issues: List[CoverageIssue] = []
        try:
            has_open  = "open"  in df.columns
            has_high  = "high"  in df.columns
            has_low   = "low"   in df.columns
            has_close = "close" in df.columns
            has_vol   = "volume" in df.columns

            invalid_dates = []

            if has_high and has_low:
                bad = df[df["high"].apply(self._to_float) < df["low"].apply(self._to_float)]
                invalid_dates.extend(self._get_dates(bad, df))

            if has_close:
                bad = df[df["close"].apply(self._to_float) <= 0]
                invalid_dates.extend(self._get_dates(bad, df))

            if has_vol:
                bad = df[df["volume"].apply(self._to_float) < 0]
                invalid_dates.extend(self._get_dates(bad, df))

            invalid_dates = list(set(invalid_dates))[:20]

            if invalid_dates:
                issues.append(CoverageIssue(
                    issue_id=f"invalid_ohlc_{symbol}_{dataset}_{ts}",
                    symbol=symbol,
                    dataset=dataset,
                    issue_type=ISSUE_INVALID,
                    description=f"{symbol}/{dataset} has {len(invalid_dates)} invalid OHLCV row(s)",
                    row_count=row_count,
                    affected_dates=invalid_dates,
                    details={"invalid_count": len(invalid_dates)},
                ))
        except Exception as exc:
            logger.warning("_detect_invalid_ohlc %s/%s: %s", symbol, dataset, exc)
        return issues

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _data_path(self, symbol: str, dataset: str) -> str:
        return os.path.join(BASE_DIR, "data", "import", dataset, f"{symbol}.csv")

    def _load_csv(self, path: str):
        try:
            import pandas as pd
            for enc in ("utf-8-sig", "utf-8", "big5", "cp950"):
                try:
                    df = pd.read_csv(path, encoding=enc)
                    return df
                except Exception:
                    continue
        except ImportError:
            pass
        return None

    def _find_date_col(self, df) -> Optional[str]:
        DATE_CANDIDATES = ["date", "時間", "日期", "datetime"]
        for c in DATE_CANDIDATES:
            if c in df.columns:
                return c
        return None

    def _get_last_date(self, df) -> Optional[str]:
        date_col = self._find_date_col(df)
        if date_col and date_col in df.columns:
            try:
                return str(df[date_col].max())
            except Exception:
                pass
        return None

    def _discover_symbols(self) -> List[str]:
        """Discover symbols from data/import/daily/ directory."""
        daily_dir = os.path.join(BASE_DIR, "data", "import", "daily")
        if not os.path.isdir(daily_dir):
            return []
        symbols = []
        for fname in os.listdir(daily_dir):
            if fname.endswith(".csv"):
                sym = fname[:-4]
                if sym:
                    symbols.append(sym)
        return sorted(symbols)

    def _to_float(self, val) -> float:
        try:
            return float(val)
        except Exception:
            return 0.0

    def _get_dates(self, subset, df) -> List[str]:
        if len(subset) == 0:
            return []
        date_col = self._find_date_col(df)
        if date_col and date_col in subset.columns:
            return subset[date_col].astype(str).tolist()
        return []
