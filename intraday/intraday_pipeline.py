"""
intraday/intraday_pipeline.py — Intraday Data Standardization Pipeline (v0.3.27).
[!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    import pandas as pd
    _PANDAS_OK = True
except ImportError:
    _PANDAS_OK = False
    logger.warning("pandas not available — IntradayDataPipeline will be limited")

from intraday.intraday_schema import IntradaySchema


class IntradayDataPipeline:
    """
    Intraday Data Standardization Pipeline.

    Discovers raw intraday files (CSV/XLSX), normalizes them to the standard
    schema, and writes outputs to intraday_standard/{freq}/.

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

    def __init__(
        self,
        mode: str = "real",
        input_root: str = "data/import/intraday",
        output_root: str = "data/import/intraday_standard",
        results_dir: str = "data/backtest_results",
        report_dir: str = "reports",
        freq: str = "1min",
        dry_run: bool = False,
    ):
        self.mode = mode
        self.freq = freq
        self.dry_run = dry_run

        # Resolve paths relative to BASE_DIR if not absolute
        self.input_root = input_root if os.path.isabs(input_root) else os.path.join(BASE_DIR, input_root)
        self.output_root = output_root if os.path.isabs(output_root) else os.path.join(BASE_DIR, output_root)
        self.results_dir = results_dir if os.path.isabs(results_dir) else os.path.join(BASE_DIR, results_dir)
        self.report_dir = report_dir if os.path.isabs(report_dir) else os.path.join(BASE_DIR, report_dir)

        self._schema = IntradaySchema()
        self._run_log: List[dict] = []

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Discover, load, standardize, and write all intraday files.

        Returns
        -------
        dict with keys:
            status              : "OK" | "NO_INPUT_FILES" | "PARTIAL"
            files_discovered    : int
            files_standardized  : int
            files_failed        : int
            symbols_covered     : list[str]
            warnings            : list[str]
            output_paths        : list[str]
        """
        self._run_log = []
        warnings: List[str] = []
        output_paths: List[str] = []
        files_standardized = 0
        files_failed = 0
        symbols_covered: List[str] = []

        paths = self.discover_files()
        files_discovered = len(paths)

        if files_discovered == 0:
            return {
                "status": "NO_INPUT_FILES",
                "files_discovered": 0,
                "files_standardized": 0,
                "files_failed": 0,
                "symbols_covered": [],
                "warnings": [f"No input files found in {self.input_root}"],
                "output_paths": [],
            }

        for path in paths:
            try:
                df = self.load_file(path)
                if df is None:
                    warnings.append(f"Failed to load: {path}")
                    files_failed += 1
                    continue

                result = self.standardize_dataframe(df, source_path=path)
                if result.get("warnings"):
                    warnings.extend(result["warnings"])

                if not result.get("ok") or result.get("df") is None:
                    warnings.append(f"Standardization failed for: {path}")
                    files_failed += 1
                    continue

                symbol = result.get("symbol") or self._extract_symbol_from_filename(path)
                freq = result.get("freq", self.freq)
                out_path = self.write_standard_output(result["df"], symbol, freq)
                if out_path:
                    output_paths.append(out_path)
                    files_standardized += 1
                    if symbol and symbol not in symbols_covered:
                        symbols_covered.append(symbol)
                else:
                    warnings.append(f"Write failed or skipped (dry_run) for symbol={symbol}")
                    if not self.dry_run:
                        files_failed += 1
                    else:
                        files_standardized += 1
                        if symbol and symbol not in symbols_covered:
                            symbols_covered.append(symbol)

            except Exception as exc:
                logger.exception("Pipeline error for %s: %s", path, exc)
                warnings.append(f"Unexpected error for {path}: {exc}")
                files_failed += 1

        if files_failed > 0 and files_standardized == 0:
            status = "PARTIAL"
        elif files_failed > 0:
            status = "PARTIAL"
        else:
            status = "OK"

        return {
            "status": status,
            "files_discovered": files_discovered,
            "files_standardized": files_standardized,
            "files_failed": files_failed,
            "symbols_covered": symbols_covered,
            "warnings": warnings,
            "output_paths": output_paths,
        }

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover_files(self) -> List[str]:
        """
        Find *.csv and *.xlsx files in input_root/freq/ and input_root/.

        Returns
        -------
        list of absolute file paths; empty list if no files found
        """
        found = []
        search_dirs = [
            os.path.join(self.input_root, self.freq),
            self.input_root,
        ]
        for directory in search_dirs:
            if not os.path.isdir(directory):
                continue
            try:
                for fname in os.listdir(directory):
                    if fname.lower().endswith(".csv") or fname.lower().endswith(".xlsx"):
                        full_path = os.path.join(directory, fname)
                        if full_path not in found:
                            found.append(full_path)
            except Exception as exc:
                logger.warning("discover_files: error scanning %s: %s", directory, exc)

        logger.info("discover_files: found %d files for freq=%s", len(found), self.freq)
        return found

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load_file(self, path: str):
        """
        Read a CSV or XLSX file into a DataFrame.

        Returns
        -------
        pd.DataFrame or None on failure
        """
        if not _PANDAS_OK:
            logger.error("pandas not available — cannot load file")
            return None
        try:
            ext = os.path.splitext(path)[1].lower()
            if ext == ".csv":
                df = pd.read_csv(path, dtype=str, encoding="utf-8-sig")
            elif ext in (".xlsx", ".xls"):
                df = pd.read_excel(path, dtype=str)
            else:
                logger.warning("load_file: unsupported extension %s for %s", ext, path)
                return None
            logger.info("load_file: loaded %s rows from %s", len(df), path)
            return df
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(path, dtype=str, encoding="big5")
                return df
            except Exception as exc2:
                logger.warning("load_file: encoding fallback failed for %s: %s", path, exc2)
                return None
        except Exception as exc:
            logger.warning("load_file: failed to load %s: %s", path, exc)
            return None

    # ------------------------------------------------------------------
    # Standardization
    # ------------------------------------------------------------------

    def standardize_dataframe(self, df, source_path: Optional[str] = None) -> dict:
        """
        Apply full schema normalization pipeline to a raw DataFrame.

        Returns
        -------
        dict with keys: df, symbol, freq, ok, warnings
        """
        warnings: List[str] = []
        symbol: Optional[str] = None

        if not _PANDAS_OK:
            return {"df": None, "symbol": None, "freq": self.freq,
                    "ok": False, "warnings": ["pandas not available"]}

        if df is None or (hasattr(df, "empty") and df.empty):
            return {"df": None, "symbol": None, "freq": self.freq,
                    "ok": False, "warnings": ["Input DataFrame is None or empty"]}

        try:
            # Extract symbol from filename
            if source_path:
                symbol = self._extract_symbol_from_filename(source_path)

            # Normalize columns
            df = self._schema.normalize_columns(df)

            # Inject symbol if missing
            if "symbol" not in df.columns or df["symbol"].astype(str).str.strip().eq("").all():
                if symbol:
                    df["symbol"] = symbol

            # Inject freq
            if "freq" not in df.columns or df["freq"].astype(str).str.strip().eq("").all():
                df["freq"] = self.freq

            # Build datetime
            df = self._schema.build_datetime(df)

            # Coerce dtypes
            df = self._schema.coerce_dtypes(df, freq=self.freq)

            # Fill missing optional columns
            df = self._schema.fill_missing_optional_columns(df, freq=self.freq)

            # Add source if missing
            if "source" not in df.columns or df["source"].astype(str).str.strip().eq("").all():
                src_name = os.path.basename(source_path) if source_path else "unknown"
                df["source"] = src_name

            # Validate
            validation = self._schema.validate(df, freq=self.freq)
            if validation.get("warnings"):
                warnings.extend(validation["warnings"])

            return {
                "df": df,
                "symbol": symbol,
                "freq": self.freq,
                "ok": validation.get("ok", False),
                "warnings": warnings,
            }

        except Exception as exc:
            logger.exception("standardize_dataframe error: %s", exc)
            warnings.append(f"standardize_dataframe exception: {exc}")
            return {"df": None, "symbol": symbol, "freq": self.freq,
                    "ok": False, "warnings": warnings}

    # ------------------------------------------------------------------
    # Writing
    # ------------------------------------------------------------------

    def write_standard_output(self, df, symbol: str, freq: str = "1min") -> Optional[str]:
        """
        Write standardized DataFrame to output_root/freq/{symbol}_{freq}.csv.

        Returns
        -------
        str path that was (or would be) written; None on failure
        """
        if not _PANDAS_OK:
            logger.error("pandas not available — cannot write output")
            return None

        out_dir = os.path.join(self.output_root, freq)
        fname = f"{symbol}_{freq}.csv"
        out_path = os.path.join(out_dir, fname)

        if self.dry_run:
            logger.info("dry_run: would write %s", out_path)
            return out_path

        try:
            os.makedirs(out_dir, exist_ok=True)
            df.to_csv(out_path, index=False, encoding="utf-8-sig")
            logger.info("write_standard_output: wrote %s rows to %s", len(df), out_path)
            return out_path
        except Exception as exc:
            logger.warning("write_standard_output: failed for %s: %s", out_path, exc)
            return None

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def build_pipeline_summary(self) -> dict:
        """Return summary of most recent run results."""
        return {
            "mode": self.mode,
            "freq": self.freq,
            "dry_run": self.dry_run,
            "input_root": self.input_root,
            "output_root": self.output_root,
            "run_log_entries": len(self._run_log),
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _extract_symbol_from_filename(self, path: str) -> str:
        """
        Extract symbol (4-5 digit stock code) from filename.

        Examples
        --------
        "2454_1min.csv"        → "2454"
        "2454 聯發科 1min.xlsx" → "2454"
        "2454_聯發科_1min.xlsx" → "2454"
        """
        basename = os.path.basename(path)
        name_no_ext = os.path.splitext(basename)[0]
        match = re.search(r"\b(\d{4,5})\b", name_no_ext)
        if match:
            return match.group(1)
        # Fallback: first digit sequence
        match2 = re.search(r"(\d{4,5})", name_no_ext)
        if match2:
            return match2.group(1)
        return name_no_ext.split("_")[0].split(" ")[0]
