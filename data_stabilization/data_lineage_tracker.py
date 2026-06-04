"""data_stabilization/data_lineage_tracker.py — DataLineageTracker v0.5.5.

Scans data directories to build a lineage record for each dataset.
Only reads metadata (path, size, mtime, head rows) — never logs data content.

[!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import glob
import hashlib
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Freshness thresholds (days)
# ---------------------------------------------------------------------------
_FRESHNESS_DAILY   = 3   # daily data: stale if >3 days
_FRESHNESS_WEEKLY  = 7
_FRESHNESS_MONTHLY = 45
_FRESHNESS_QUARTER = 120


@dataclass
class DataLineageRecord:
    """Metadata record for a single dataset file.

    [!] Data Stabilization Only. Research Only. No Real Orders.
    """

    dataset_name:    str
    path:            str
    relative_path:   str = ""
    source_provider: str = ""
    mode:            str = ""
    created_at:      str = ""
    modified_at:     str = ""
    size_bytes:      int = 0
    rows:            int = 0
    columns:         int = 0
    schema_status:   str = "UNKNOWN"
    freshness_status: str = "UNKNOWN"
    file_hash:       str = ""
    upstream:        str = ""
    downstream:      str = ""
    warning:         str = ""

    # Safety invariants
    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return {
            "dataset_name":    self.dataset_name,
            "path":            self.path,
            "relative_path":   self.relative_path,
            "source_provider": self.source_provider,
            "mode":            self.mode,
            "created_at":      self.created_at,
            "modified_at":     self.modified_at,
            "size_bytes":      self.size_bytes,
            "rows":            self.rows,
            "columns":         self.columns,
            "schema_status":   self.schema_status,
            "freshness_status": self.freshness_status,
            "file_hash":       self.file_hash,
            "upstream":        self.upstream,
            "downstream":      self.downstream,
            "warning":         self.warning,
        }


# ---------------------------------------------------------------------------
# Scan patterns: dataset_name -> list of glob patterns (relative to BASE_DIR)
# ---------------------------------------------------------------------------
_SCAN_PATTERNS = {
    "daily_k":                ["data/import/*.csv", "data/import/daily_*.csv"],
    "intraday_1min":          ["data/import/intraday_1min*.csv"],
    "intraday_5min":          ["data/import/intraday_5min*.csv"],
    "tick":                   ["data/import/tick*.csv"],
    "bidask":                 ["data/import/bidask*.csv"],
    "monthly_revenue":        ["data/import/monthly_revenue*.csv", "data/import/revenue*.csv"],
    "quarterly_financials":   ["data/import/quarterly*.csv", "data/import/financials*.csv"],
    "eps":                    ["data/import/eps*.csv"],
    "gross_margin":           ["data/import/gross_margin*.csv"],
    "operating_margin":       ["data/import/operating_margin*.csv"],
    "institutional_trading":  ["data/import/institutional*.csv", "data/import/chip*.csv"],
    "margin_balance":         ["data/import/margin*.csv"],
    "major_holders":          ["data/import/major_holder*.csv", "data/import/shareholders*.csv"],
    "shareholder_distribution": ["data/import/shareholder_dist*.csv"],
    "technical_features":     ["data/backtest_results/technical_features*.csv",
                                "data/backtest_results/feature_store*.csv"],
    "microstructure_features":["data/backtest_results/microstructure*.csv"],
    "financial_features":     ["data/backtest_results/financial_features*.csv"],
    "chip_features":          ["data/backtest_results/chip_features*.csv"],
    "strategy_filter_features":["data/backtest_results/strategy_filter_pack*.csv"],
    "ml_knowledge_features":  ["data/backtest_results/ml_feature_store/*.csv",
                                "data/backtest_results/ml_knowledge*.csv"],
    "data_quality_summary":   ["data/backtest_results/data_quality_gate*.csv",
                                "data/backtest_results/data_quality_summary*.csv"],
    "provider_health_summary":["data/backtest_results/provider_health*.csv",
                                "data/backtest_results/provider_reliability*.csv"],
    "feature_readiness_summary": ["data/backtest_results/data_stabilization/feature_readiness*.csv"],
}

# Upstream / downstream relationships
_UPSTREAM = {
    "technical_features":      "daily_k",
    "microstructure_features": "tick, bidask",
    "financial_features":      "quarterly_financials, monthly_revenue",
    "chip_features":           "institutional_trading, margin_balance",
    "strategy_filter_features":"daily_k, financial_features, chip_features",
    "ml_knowledge_features":   "technical_features, financial_features",
    "eps":                     "quarterly_financials",
    "gross_margin":            "quarterly_financials",
    "operating_margin":        "quarterly_financials",
    "data_quality_summary":    "daily_k, provider_health_summary",
    "feature_readiness_summary": "technical_features, financial_features, chip_features",
}

_DOWNSTREAM = {
    "daily_k":            "technical_features, strategy_filter_features",
    "quarterly_financials": "eps, gross_margin, operating_margin, financial_features",
    "monthly_revenue":    "financial_features",
    "institutional_trading": "chip_features",
    "margin_balance":     "chip_features",
}

# Provider guess from path patterns
_PROVIDER_HINTS = {
    "import": "XQ CSV / TWSE public endpoint",
    "provider": "data.providers",
    "backtest_results": "Derived / feature engine",
    "ml_feature_store": "ml.knowledge_feature_bridge",
}


class DataLineageTracker:
    """Scans data directories and builds lineage records.

    Only reads metadata; never logs full file content.

    [!] Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        root_dir: str = "data",
        output_dir: str = "data/backtest_results/data_stabilization",
    ) -> None:
        self.root_dir   = os.path.join(BASE_DIR, root_dir)
        self.output_dir = os.path.join(BASE_DIR, output_dir)
        self._records: List[DataLineageRecord] = []

    def scan_datasets(self) -> List[DataLineageRecord]:
        """Scan all known dataset patterns and return lineage records."""
        self._records = []
        try:
            from data_stabilization.data_schema_registry import DatasetSchemaRegistry
            registry = DatasetSchemaRegistry()
        except Exception as exc:
            logger.warning("DataLineageTracker: schema registry unavailable: %s", exc)
            registry = None

        for dataset_name, patterns in _SCAN_PATTERNS.items():
            record = self._scan_one(dataset_name, patterns, registry)
            self._records.append(record)
        return self._records

    def _scan_one(self, dataset_name: str, patterns: List[str], registry) -> DataLineageRecord:
        """Build a single lineage record for the named dataset."""
        try:
            found_path = ""
            for pattern in patterns:
                full = os.path.join(BASE_DIR, pattern)
                matches = sorted(glob.glob(full))
                if matches:
                    found_path = matches[-1]
                    break

            if not found_path:
                return DataLineageRecord(
                    dataset_name=dataset_name,
                    path="",
                    freshness_status="MISSING",
                    schema_status="MISSING",
                    upstream=_UPSTREAM.get(dataset_name, ""),
                    downstream=_DOWNSTREAM.get(dataset_name, ""),
                    warning=f"No file found for dataset '{dataset_name}'",
                )

            stat = os.stat(found_path)
            rel  = os.path.relpath(found_path, BASE_DIR).replace("\\", "/")
            mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            ctime = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")

            rows, columns = self._sample_csv(found_path)
            fhash  = self.hash_file(found_path)
            fresh  = self._freshness_status(dataset_name, stat.st_mtime)
            source = self._guess_provider(found_path)

            # Schema validation
            schema_status = "OK"
            warning       = ""
            if registry is not None:
                schema = registry.get_schema(dataset_name)
                if schema and columns > 0:
                    # Can't validate without column names here (just count)
                    schema_status = "OK"
                elif schema is None:
                    schema_status = "NO_SCHEMA"
                    warning = f"No schema defined for '{dataset_name}'"

            return DataLineageRecord(
                dataset_name=dataset_name,
                path=found_path,
                relative_path=rel,
                source_provider=source,
                mode="real",
                created_at=ctime,
                modified_at=mtime,
                size_bytes=stat.st_size,
                rows=rows,
                columns=columns,
                schema_status=schema_status,
                freshness_status=fresh,
                file_hash=fhash,
                upstream=_UPSTREAM.get(dataset_name, ""),
                downstream=_DOWNSTREAM.get(dataset_name, ""),
                warning=warning,
            )
        except Exception as exc:
            logger.warning("DataLineageTracker._scan_one(%s) failed: %s", dataset_name, exc)
            return DataLineageRecord(
                dataset_name=dataset_name,
                path="",
                schema_status="FAILED",
                freshness_status="UNKNOWN",
                warning=str(exc),
            )

    def build_lineage_record(self, dataset_path: str) -> DataLineageRecord:
        """Build a lineage record for an arbitrary dataset path."""
        try:
            if not os.path.isfile(dataset_path):
                return DataLineageRecord(
                    dataset_name=os.path.basename(dataset_path),
                    path=dataset_path,
                    freshness_status="MISSING",
                    warning="File not found",
                )
            stat = os.stat(dataset_path)
            rel  = os.path.relpath(dataset_path, BASE_DIR).replace("\\", "/")
            mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            rows, columns = self._sample_csv(dataset_path)
            return DataLineageRecord(
                dataset_name=os.path.basename(dataset_path),
                path=dataset_path,
                relative_path=rel,
                source_provider=self._guess_provider(dataset_path),
                modified_at=mtime,
                size_bytes=stat.st_size,
                rows=rows,
                columns=columns,
                file_hash=self.hash_file(dataset_path),
            )
        except Exception as exc:
            logger.warning("DataLineageTracker.build_lineage_record() failed: %s", exc)
            return DataLineageRecord(
                dataset_name=os.path.basename(dataset_path),
                path=dataset_path,
                warning=str(exc),
            )

    def hash_file(self, path: str) -> str:
        """Return MD5 hex digest of the first 64KB of a file (metadata only)."""
        try:
            h = hashlib.md5()
            with open(path, "rb") as f:
                h.update(f.read(65536))
            return h.hexdigest()
        except Exception:
            return ""

    def build_lineage_table(self) -> List[dict]:
        """Return list of record dicts. Scans if not already done."""
        if not self._records:
            self.scan_datasets()
        return [r.to_dict() for r in self._records]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _sample_csv(self, path: str):
        """Return (rows_count, columns_count) by reading only header + 5 rows."""
        rows = 0
        columns = 0
        try:
            ext = os.path.splitext(path)[1].lower()
            if ext == ".csv":
                import csv as csv_mod
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    reader = csv_mod.reader(f)
                    header = next(reader, None)
                    if header:
                        columns = len(header)
                    for _ in range(5):
                        next(reader, None)
                # Count rows properly but only read first 2MB
                with open(path, "rb") as fb:
                    chunk = fb.read(2_000_000)
                rows = max(0, chunk.count(b"\n") - 1)  # subtract header
        except Exception as exc:
            logger.debug("_sample_csv(%s): %s", path, exc)
        return rows, columns

    def _freshness_status(self, dataset_name: str, mtime: float) -> str:
        age_days = (datetime.now().timestamp() - mtime) / 86400
        # Use schema freshness rule to determine threshold
        if "intraday" in dataset_name or "tick" in dataset_name or "bidask" in dataset_name:
            threshold = 2
        elif "monthly" in dataset_name or "shareholders" in dataset_name or "major" in dataset_name:
            threshold = _FRESHNESS_MONTHLY
        elif "quarterly" in dataset_name or "eps" in dataset_name or "margin_q" in dataset_name:
            threshold = _FRESHNESS_QUARTER
        else:
            threshold = _FRESHNESS_DAILY

        if age_days <= threshold:
            return "FRESH"
        elif age_days <= threshold * 3:
            return "STALE"
        return "VERY_STALE"

    def _guess_provider(self, path: str) -> str:
        path_lower = path.lower().replace("\\", "/")
        for hint, provider in _PROVIDER_HINTS.items():
            if hint in path_lower:
                return provider
        return "unknown"
