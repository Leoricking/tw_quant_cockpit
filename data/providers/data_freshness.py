"""
data/providers/data_freshness.py - Data freshness & coverage checker (v0.3.19).

Checks how up-to-date each standard import CSV is and reports coverage
across the universe of symbols.

[!] Read Only. No Real Orders.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Freshness status constants
FRESH                = "FRESH"
STALE                = "STALE"
OLD                  = "OLD"
MISSING              = "MISSING"
PARTIAL              = "PARTIAL"
UNKNOWN              = "UNKNOWN"
HISTORICAL_INTRADAY  = "HISTORICAL_INTRADAY"
TIMING_ESTIMATED     = "TIMING_ESTIMATED"

# Standard dataset definitions
_DATASETS: Dict[str, dict] = {
    "daily_k": {
        "path":        "data/import/daily/daily_k.csv",
        "date_col":    "date",
        "symbol_col":  "symbol",
        "fresh_days":  3,
        "stale_days":  7,
        "label":       "Daily Price (K-line)",
    },
    "monthly_revenue": {
        "path":        "data/import/monthly_revenue/monthly_revenue.csv",
        "date_col":    "date",
        "symbol_col":  "symbol",
        "fresh_days":  45,
        "stale_days":  90,
        "label":       "Monthly Revenue",
    },
    "institutional": {
        "path":        "data/import/institutional/institutional.csv",
        "date_col":    "date",
        "symbol_col":  "symbol",
        "fresh_days":  3,
        "stale_days":  7,
        "label":       "Institutional Flows",
    },
    "margin": {
        "path":        "data/import/margin/margin.csv",
        "date_col":    "date",
        "symbol_col":  "symbol",
        "fresh_days":  3,
        "stale_days":  7,
        "label":       "Margin / Short Balance",
    },
    "fundamental": {
        "path":        "data/import/fundamental/fundamental.csv",
        "date_col":    "date",
        "symbol_col":  "symbol",
        "fresh_days":  100,   # ~1 quarter
        "stale_days":  200,
        "label":       "Fundamental (EPS/Margins)",
    },
    "intraday": {
        "path":        "data/import/intraday",   # directory
        "date_col":    "date",
        "symbol_col":  "symbol",
        "fresh_days":  1,
        "stale_days":  3,
        "label":       "Intraday (per-minute)",
        "is_dir":      True,
    },
    "intraday_1min": {
        "path":        "data/import/intraday_standard/1min",   # standardized 1min directory (v0.3.27)
        "date_col":    "date",
        "symbol_col":  "symbol",
        "fresh_days":  1,
        "stale_days":  3,
        "label":       "Intraday 1min Standardized",
        "is_dir":      True,
        "standard_pipeline": True,
    },
    "intraday_5min": {
        "path":        "data/import/intraday_standard/5min",   # standardized 5min directory (v0.3.27)
        "date_col":    "date",
        "symbol_col":  "symbol",
        "fresh_days":  1,
        "stale_days":  3,
        "label":       "Intraday 5min Standardized",
        "is_dir":      True,
        "standard_pipeline": True,
    },
}


class DataFreshnessChecker:
    """
    Checks freshness and coverage of standard import datasets.

    Parameters
    ----------
    import_root : Root folder for data/import (default: project root)
    """

    def __init__(self, import_root: Optional[str] = None):
        self._import_root = import_root or _BASE_DIR

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run_all(self) -> dict:
        """
        Check all datasets and return a freshness summary dict.
        """
        checked_at = datetime.now().isoformat()
        results    = {}
        for name in _DATASETS:
            results[name] = self.check_dataset(name)

        # Overall summary
        statuses = [r["status"] for r in results.values()]
        n_fresh   = sum(1 for s in statuses if s == FRESH)
        n_stale   = sum(1 for s in statuses if s in (STALE, OLD))
        n_missing = sum(1 for s in statuses if s == MISSING)

        return {
            "checked_at":   checked_at,
            "datasets":     results,
            "summary": {
                "fresh":   n_fresh,
                "stale":   n_stale,
                "missing": n_missing,
                "partial": sum(1 for s in statuses if s == PARTIAL),
            },
            "read_only":      True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Per-dataset check
    # ------------------------------------------------------------------

    def check_dataset(self, dataset_name: str) -> dict:
        """Check freshness of a single named dataset."""
        defn = _DATASETS.get(dataset_name)
        if defn is None:
            return self._make_result(
                dataset_name, UNKNOWN,
                warning=f"Unknown dataset '{dataset_name}'",
            )

        # Intraday: special handling
        if defn.get("is_dir", False):
            return self._check_intraday(dataset_name, defn)

        abs_path = os.path.join(self._import_root, defn["path"])
        if not os.path.isfile(abs_path):
            return self._make_result(
                dataset_name, MISSING,
                warning=f"File not found: {defn['path']}",
                recommended_action=f"Run: python main.py provider-auto-fetch --dataset {dataset_name}",
            )

        try:
            import pandas as pd
            df = pd.read_csv(abs_path, low_memory=False)
        except Exception as exc:
            return self._make_result(
                dataset_name, UNKNOWN,
                warning=f"Cannot read {defn['path']}: {exc}",
            )

        if df.empty:
            return self._make_result(
                dataset_name, MISSING,
                warning="File exists but is empty",
                recommended_action=f"Run: python main.py provider-auto-fetch --dataset {dataset_name}",
            )

        rows    = len(df)
        symbols = []
        if defn.get("symbol_col") and defn["symbol_col"] in df.columns:
            symbols = sorted(df[defn["symbol_col"]].dropna().unique().tolist())

        latest_date = self.check_latest_date(dataset_name, df=df)
        status      = self.classify_freshness(dataset_name, latest_date)

        # Check for timing_estimated flag in fundamental
        warning = ""
        if dataset_name == "fundamental":
            if "announcement_date_is_estimated" in df.columns:
                n_est = df["announcement_date_is_estimated"].sum()
                if n_est > 0:
                    warning = f"TIMING_ESTIMATED: {n_est} rows have estimated announcement dates"
                    if status == FRESH:
                        status = PARTIAL  # partial because timing may be off

        return self._make_result(
            dataset_name, status,
            latest_date=latest_date,
            rows=rows,
            symbols=symbols,
            warning=warning,
        )

    def _check_intraday(self, dataset_name: str, defn: dict) -> dict:
        """Intraday is directory-based; report HISTORICAL if files exist."""
        abs_dir = os.path.join(self._import_root, defn["path"])
        is_standard = defn.get("standard_pipeline", False)
        import_cmd = "python main.py intraday-pipeline" if is_standard else "python main.py import-intraday"
        missing_msg = (
            "Standardized intraday directory not found. Run intraday-pipeline first."
            if is_standard
            else "Intraday directory not found. Use import-intraday to import."
        )
        no_files_msg = (
            "No standardized intraday CSV files found. Run intraday-pipeline first."
            if is_standard
            else "No intraday CSV files found."
        )

        if not os.path.isdir(abs_dir):
            return self._make_result(
                dataset_name, MISSING,
                warning=missing_msg,
                recommended_action=import_cmd,
            )
        try:
            files = [f for f in os.listdir(abs_dir) if f.endswith(".csv")]
        except Exception:
            files = []

        if not files:
            return self._make_result(
                dataset_name, MISSING,
                warning=no_files_msg,
                recommended_action=import_cmd,
            )

        return self._make_result(
            dataset_name, HISTORICAL_INTRADAY,
            rows=len(files),
            warning=f"Intraday source: {'standardized pipeline' if is_standard else 'XQ import / CSV'} ({len(files)} files). API provider planned for v0.4+.",
        )

    # ------------------------------------------------------------------
    # Symbol coverage
    # ------------------------------------------------------------------

    def check_symbol_coverage(
        self,
        dataset_name: str,
        symbols: List[str],
    ) -> dict:
        """Return coverage ratio and missing symbols for the given universe."""
        defn = _DATASETS.get(dataset_name)
        if defn is None or defn.get("is_dir"):
            return {"coverage_ratio": 0.0, "missing": symbols, "present": []}

        abs_path = os.path.join(self._import_root, defn["path"])
        if not os.path.isfile(abs_path):
            return {"coverage_ratio": 0.0, "missing": symbols, "present": []}

        try:
            import pandas as pd
            df = pd.read_csv(abs_path, low_memory=False, usecols=[defn["symbol_col"]])
            present = set(df[defn["symbol_col"]].dropna().astype(str).unique())
            universe = set(str(s) for s in symbols)
            missing  = sorted(universe - present)
            covered  = sorted(universe & present)
            ratio    = len(covered) / len(universe) if universe else 0.0
            return {"coverage_ratio": ratio, "missing": missing, "present": covered}
        except Exception as exc:
            logger.debug("check_symbol_coverage %s: %s", dataset_name, exc)
            return {"coverage_ratio": 0.0, "missing": symbols, "present": []}

    # ------------------------------------------------------------------
    # Date helpers
    # ------------------------------------------------------------------

    def check_latest_date(
        self,
        dataset_name: str,
        df=None,
    ) -> Optional[str]:
        """Return the latest date string in the dataset, or None."""
        defn = _DATASETS.get(dataset_name)
        if defn is None or defn.get("is_dir"):
            return None

        if df is None:
            abs_path = os.path.join(self._import_root, defn["path"])
            if not os.path.isfile(abs_path):
                return None
            try:
                import pandas as pd
                df = pd.read_csv(abs_path, low_memory=False)
            except Exception:
                return None

        date_col = defn.get("date_col", "date")
        if date_col not in df.columns:
            return None
        try:
            import pandas as pd
            dates = pd.to_datetime(df[date_col], errors="coerce").dropna()
            if dates.empty:
                return None
            return dates.max().strftime("%Y-%m-%d")
        except Exception:
            return None

    def classify_freshness(
        self,
        dataset_name: str,
        latest_date: Optional[str],
    ) -> str:
        """Classify freshness based on age of latest_date."""
        if latest_date is None:
            return MISSING

        defn = _DATASETS.get(dataset_name)
        if defn is None:
            return UNKNOWN

        try:
            dt = datetime.strptime(latest_date, "%Y-%m-%d")
        except ValueError:
            return UNKNOWN

        age_days = (datetime.now() - dt).days
        fresh_days = defn.get("fresh_days", 3)
        stale_days = defn.get("stale_days", 7)

        if age_days <= fresh_days:
            return FRESH
        if age_days <= stale_days:
            return STALE
        return OLD

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------

    @staticmethod
    def _make_result(
        dataset:    str,
        status:     str,
        latest_date: Optional[str] = None,
        rows:        int = 0,
        symbols:     Optional[list] = None,
        warning:     str = "",
        recommended_action: str = "",
    ) -> dict:
        defn = _DATASETS.get(dataset, {})
        syms = symbols or []

        # v0.3.24: compute stale_reason
        stale_reason = ""
        if status == "MISSING":
            stale_reason = "file_not_found"
        elif status == "OLD":
            stale_reason = "data_too_old"
        elif status == "STALE":
            stale_reason = "data_stale"
        elif status == TIMING_ESTIMATED:
            stale_reason = "timing_estimated"
        elif status == HISTORICAL_INTRADAY:
            stale_reason = "historical_intraday_only"

        return {
            "dataset":              dataset,
            "label":                defn.get("label", dataset),
            "status":               status,
            "latest_date":          latest_date or "",
            "rows":                 rows,
            "symbols":              len(syms),
            "coverage_ratio":       1.0 if syms else 0.0,
            "missing_symbols":      [],
            "missing_symbol_count": 0,
            "warning":              warning,
            "recommended_action":   recommended_action,
            # v0.3.24 fields for dataset_confidence_input
            "stale_reason":         stale_reason,
            "dataset_confidence_input": {
                "freshness_status":      status,
                "latest_date":           latest_date or "",
                "rows":                  rows,
                "coverage_ratio":        1.0 if syms else 0.0,
                "missing_symbol_count":  0,
                "stale_reason":          stale_reason,
            },
        }
