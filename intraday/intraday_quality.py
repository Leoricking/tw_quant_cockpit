"""
intraday/intraday_quality.py — Intraday data quality checker (v0.3.27).
[!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    import pandas as pd
    _PANDAS_OK = True
except ImportError:
    _PANDAS_OK = False
    logger.warning("pandas not available — IntradayQualityChecker will be limited")

try:
    import numpy as np
    _NUMPY_OK = True
except ImportError:
    _NUMPY_OK = False


class IntradayQualityChecker:
    """
    Intraday data quality checker for standardized intraday bar files.

    Scans standard_root/{freq}/{symbol}_{freq}.csv and computes quality metrics
    for each symbol/freq combination.

    [!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.

    Safety flags
    ------------
    read_only           : True
    no_real_orders      : True
    production_blocked  : True
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    # Taiwan market session (minutes from open to close)
    _SESSION_START = "09:00"
    _SESSION_END = "13:30"

    def __init__(
        self,
        standard_root: str = "data/import/intraday_standard",
        expected_start: str = "09:00",
        expected_end: str = "13:30",
    ):
        self.standard_root = (
            standard_root if os.path.isabs(standard_root)
            else os.path.join(BASE_DIR, standard_root)
        )
        self.expected_start = expected_start
        self.expected_end = expected_end

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Scan standard_root for all {freq}/{symbol}_{freq}.csv files and check each.

        Returns
        -------
        dict with keys:
            status               : "OK" | "NO_DATA"
            symbols              : list[str]
            results              : list[dict]
            overall_quality_score: float
            warnings             : list[str]
        """
        if not _PANDAS_OK:
            return {"status": "NO_DATA", "symbols": [], "results": [],
                    "overall_quality_score": 0.0, "warnings": ["pandas not available"]}

        warnings: List[str] = []
        results: List[dict] = []
        symbols: List[str] = []

        if not os.path.isdir(self.standard_root):
            return {
                "status": "NO_DATA",
                "symbols": [],
                "results": [],
                "overall_quality_score": 0.0,
                "warnings": [f"standard_root not found: {self.standard_root}"],
            }

        # Scan freq subdirectories
        for freq in ["1min", "5min"]:
            freq_dir = os.path.join(self.standard_root, freq)
            if not os.path.isdir(freq_dir):
                continue
            try:
                for fname in os.listdir(freq_dir):
                    if not fname.endswith(".csv"):
                        continue
                    # e.g. 2454_1min.csv
                    parts = fname.replace(".csv", "").split("_")
                    symbol = parts[0] if parts else fname.replace(".csv", "")
                    result = self.check_symbol(symbol, freq)
                    results.append(result)
                    if symbol not in symbols:
                        symbols.append(symbol)
            except Exception as exc:
                logger.warning("run: error scanning %s: %s", freq_dir, exc)
                warnings.extend([f"Scan error in {freq_dir}: {exc}"])

        if not results:
            return {
                "status": "NO_DATA",
                "symbols": [],
                "results": [],
                "overall_quality_score": 0.0,
                "warnings": warnings or ["No standardized files found"],
            }

        scores = [r.get("quality_score", 0.0) for r in results if r.get("quality_score") is not None]
        overall = round(sum(scores) / len(scores), 2) if scores else 0.0

        return {
            "status": "OK",
            "symbols": symbols,
            "results": results,
            "overall_quality_score": overall,
            "warnings": warnings,
        }

    # ------------------------------------------------------------------
    # Per-symbol check
    # ------------------------------------------------------------------

    def check_symbol(self, symbol: str, freq: str = "1min") -> dict:
        """
        Load the standard file for symbol/freq and run all quality checks.

        Returns
        -------
        dict with all output fields
        """
        base_result = {
            "symbol": symbol,
            "freq": freq,
            "rows": 0,
            "days": 0,
            "latest_date": None,
            "expected_bars_per_day": self._get_expected_bars(freq),
            "average_coverage_ratio": 0.0,
            "missing_minutes": 0,
            "duplicate_rows": 0,
            "anomaly_count": 0,
            "volume_anomaly_count": 0,
            "quality_score": 0.0,
            "quality_status": "MISSING",
            "warning": None,
            "recommended_action": "Import data for this symbol",
        }

        fpath = os.path.join(self.standard_root, freq, f"{symbol}_{freq}.csv")
        if not os.path.isfile(fpath):
            base_result["warning"] = f"File not found: {fpath}"
            base_result["recommended_action"] = f"Run pipeline to import {symbol} {freq} data"
            base_result["quality_status"] = "MISSING"
            base_result["quality_score"] = 0.0
            return base_result

        try:
            df = pd.read_csv(fpath, dtype=str, encoding="utf-8-sig")
        except Exception as exc:
            logger.warning("check_symbol: failed to load %s: %s", fpath, exc)
            base_result["warning"] = f"Load error: {exc}"
            base_result["quality_status"] = "MISSING"
            return base_result

        if df.empty:
            base_result["warning"] = "File is empty"
            base_result["quality_status"] = "MISSING"
            return base_result

        # Basic stats
        rows = len(df)
        days_count = 0
        latest_date = None

        if "date" in df.columns:
            dates = df["date"].dropna().astype(str).str.strip()
            dates = dates[dates != ""]
            unique_dates = sorted(dates.unique())
            days_count = len(unique_dates)
            latest_date = unique_dates[-1] if unique_dates else None

        # Coerce numeric columns for checks
        for col in ["open", "high", "low", "close", "volume"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Run checks
        session_cov = self.check_session_coverage(df)
        avg_coverage = session_cov.get("average_coverage_ratio", 0.0)
        missing_minutes = self.check_missing_minutes(df)
        duplicate_rows = self.check_duplicate_bars(df)
        anomaly_count = self.check_price_anomalies(df)
        volume_anomaly_count = self.check_volume_anomalies(df)

        result = {
            "symbol": symbol,
            "freq": freq,
            "rows": rows,
            "days": days_count,
            "latest_date": latest_date,
            "expected_bars_per_day": self._get_expected_bars(freq),
            "average_coverage_ratio": round(avg_coverage, 4),
            "missing_minutes": missing_minutes,
            "duplicate_rows": duplicate_rows,
            "anomaly_count": anomaly_count,
            "volume_anomaly_count": volume_anomaly_count,
            "quality_score": 0.0,
            "quality_status": "OK",
            "warning": None,
            "recommended_action": "None — data looks good",
        }

        result["quality_status"] = self.classify_quality(result)
        result["quality_score"] = self._compute_quality_score(result)

        # Set recommended action
        status = result["quality_status"]
        if status == "MISSING":
            result["recommended_action"] = "Import data"
        elif status == "STALE":
            result["recommended_action"] = "Refresh data — latest date is too old"
        elif status == "INSUFFICIENT":
            result["recommended_action"] = "Import more data (< 50 rows)"
        elif status == "DUPLICATED":
            result["recommended_action"] = "Deduplicate the data"
        elif status == "PRICE_ANOMALY":
            result["recommended_action"] = "Review price anomalies before use"
        elif status == "VOLUME_ANOMALY":
            result["recommended_action"] = "Review volume anomalies before use"
        elif status == "PARTIAL":
            result["recommended_action"] = "Coverage below 80% — import more complete data"
        else:
            result["recommended_action"] = "None — data quality OK"

        return result

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    def check_session_coverage(self, df) -> dict:
        """
        Per-day: compute expected bars (09:00–13:30 at freq) vs actual.

        Returns
        -------
        dict with average_coverage_ratio
        """
        if not _PANDAS_OK or df is None or df.empty:
            return {"average_coverage_ratio": 0.0}

        freq = "1min"
        if "freq" in df.columns:
            freqs = df["freq"].dropna().unique()
            if len(freqs) > 0:
                freq = str(freqs[0])

        expected = self._get_expected_bars(freq)
        if expected == 0:
            return {"average_coverage_ratio": 0.0}

        if "date" not in df.columns:
            return {"average_coverage_ratio": 0.0}

        try:
            date_groups = df.groupby("date")
            ratios = []
            for _date, group in date_groups:
                actual = len(group)
                ratio = min(actual / expected, 1.0)
                ratios.append(ratio)
            avg = sum(ratios) / len(ratios) if ratios else 0.0
            return {"average_coverage_ratio": avg}
        except Exception as exc:
            logger.warning("check_session_coverage: %s", exc)
            return {"average_coverage_ratio": 0.0}

    def check_missing_minutes(self, df) -> int:
        """
        Count gaps in the time series within each trading day.

        Returns
        -------
        int total missing minute-bars across all days
        """
        if not _PANDAS_OK or df is None or df.empty:
            return 0
        if "datetime" not in df.columns and ("date" not in df.columns or "time" not in df.columns):
            return 0

        try:
            if "datetime" in df.columns:
                dt_series = pd.to_datetime(df["datetime"], errors="coerce")
            else:
                dt_series = pd.to_datetime(
                    df["date"].astype(str) + " " + df["time"].astype(str),
                    errors="coerce"
                )

            df_copy = df.copy()
            df_copy["_dt"] = dt_series
            df_copy = df_copy.dropna(subset=["_dt"])

            if df_copy.empty:
                return 0

            total_missing = 0
            if "date" in df_copy.columns:
                for _date, group in df_copy.groupby("date"):
                    group_sorted = group.sort_values("_dt")
                    times = group_sorted["_dt"]
                    if len(times) < 2:
                        continue
                    diffs = times.diff().dropna()
                    expected_diff = pd.Timedelta(minutes=1)
                    for diff in diffs:
                        if diff > expected_diff * 1.5:
                            gaps = int(diff / expected_diff) - 1
                            total_missing += gaps
            else:
                times = df_copy.sort_values("_dt")["_dt"]
                diffs = times.diff().dropna()
                expected_diff = pd.Timedelta(minutes=1)
                for diff in diffs:
                    if diff > expected_diff * 1.5:
                        gaps = int(diff / expected_diff) - 1
                        total_missing += gaps

            return int(total_missing)
        except Exception as exc:
            logger.warning("check_missing_minutes: %s", exc)
            return 0

    def check_duplicate_bars(self, df) -> int:
        """
        Count duplicate (symbol, date, time) rows.

        Returns
        -------
        int count of duplicate rows
        """
        if not _PANDAS_OK or df is None or df.empty:
            return 0

        dup_cols = [c for c in ["symbol", "date", "time"] if c in df.columns]
        if not dup_cols:
            return 0

        try:
            duplicates = df.duplicated(subset=dup_cols)
            return int(duplicates.sum())
        except Exception as exc:
            logger.warning("check_duplicate_bars: %s", exc)
            return 0

    def check_price_anomalies(self, df) -> int:
        """
        Count rows where (high < low) or (close > high*1.1) or (close < low*0.9).

        Returns
        -------
        int anomaly count
        """
        if not _PANDAS_OK or df is None or df.empty:
            return 0
        required_cols = ["high", "low", "close"]
        if not all(c in df.columns for c in required_cols):
            return 0

        try:
            h = pd.to_numeric(df["high"], errors="coerce")
            l = pd.to_numeric(df["low"], errors="coerce")
            c = pd.to_numeric(df["close"], errors="coerce")

            mask = (
                (h < l) |
                (c > h * 1.1) |
                (c < l * 0.9)
            )
            return int(mask.sum())
        except Exception as exc:
            logger.warning("check_price_anomalies: %s", exc)
            return 0

    def check_volume_anomalies(self, df) -> int:
        """
        Count rows where volume == 0 or volume > median * 20.

        Returns
        -------
        int anomaly count
        """
        if not _PANDAS_OK or df is None or df.empty:
            return 0
        if "volume" not in df.columns:
            return 0

        try:
            vol = pd.to_numeric(df["volume"], errors="coerce").dropna()
            if vol.empty:
                return 0
            median_vol = float(vol.median())
            threshold = median_vol * 20 if median_vol > 0 else float("inf")

            vol_all = pd.to_numeric(df["volume"], errors="coerce")
            mask = (vol_all == 0) | (vol_all > threshold)
            return int(mask.sum())
        except Exception as exc:
            logger.warning("check_volume_anomalies: %s", exc)
            return 0

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    def classify_quality(self, result: dict) -> str:
        """
        Classify quality status based on result dict fields.

        Returns
        -------
        str: OK | PARTIAL | MISSING | STALE | DUPLICATED | PRICE_ANOMALY |
             VOLUME_ANOMALY | INSUFFICIENT
        """
        if result.get("rows", 0) == 0:
            return "MISSING"

        # STALE: latest_date > 5 trading days ago
        latest_date_str = result.get("latest_date")
        if latest_date_str:
            try:
                latest_dt = datetime.strptime(str(latest_date_str)[:10], "%Y-%m-%d")
                today = datetime.now()
                delta_days = (today - latest_dt).days
                # Approximate 5 trading days as 7 calendar days
                if delta_days > 7:
                    return "STALE"
            except Exception:
                pass

        if result.get("rows", 0) < 50:
            return "INSUFFICIENT"

        if result.get("duplicate_rows", 0) > 5:
            return "DUPLICATED"

        if result.get("anomaly_count", 0) > 0:
            return "PRICE_ANOMALY"

        if result.get("volume_anomaly_count", 0) > 10:
            return "VOLUME_ANOMALY"

        coverage = result.get("average_coverage_ratio", 1.0)
        if coverage < 0.8:
            return "PARTIAL"

        return "OK"

    def _compute_quality_score(self, result: dict) -> float:
        """
        Compute a 0–100 quality score from result fields.

        Deductions:
            coverage < 0.8   : -30 * (1 - coverage)
            missing > 10     : -10
            duplicates > 0   : -10
            anomalies > 0    : -20
        """
        score = 100.0

        status = result.get("quality_status", "OK")
        if status == "MISSING":
            return 0.0
        if status == "STALE":
            score -= 40.0
        if status == "INSUFFICIENT":
            score -= 50.0

        coverage = result.get("average_coverage_ratio", 1.0)
        if coverage < 0.8:
            deduct = 30.0 * (1.0 - coverage)
            score -= deduct

        if result.get("missing_minutes", 0) > 10:
            score -= 10.0

        if result.get("duplicate_rows", 0) > 0:
            score -= 10.0

        if result.get("anomaly_count", 0) > 0:
            score -= 20.0

        return max(0.0, round(score, 2))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_expected_bars(self, freq: str) -> int:
        """
        Return expected number of bars per trading day for the given frequency.

        1min: 270 bars (09:00–13:30 inclusive)
        5min: 54 bars
        """
        mapping = {
            "1min": 270,
            "5min": 54,
        }
        return mapping.get(freq, 270)
