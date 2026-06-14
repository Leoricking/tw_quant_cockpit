"""
data_freshness/freshness_store.py — Persistence layer for freshness reports v1.1.3.
[!] Research Only. No Real Orders.
[!] Output files go in data/freshness_reports/ — NOT committed to git.
[!] No broker connection, no trading, no automatic repair.
"""
from __future__ import annotations

import csv
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from data_freshness.freshness_schema import (
    DatasetFreshnessRecord, FreshnessAlert, FreshnessSummary,
    SourceFreshnessStatus,
)

logger = logging.getLogger(__name__)

# Safety invariants
NO_REAL_ORDERS                 = True
RESEARCH_ONLY                  = True
AUTO_EXTERNAL_REFRESH_ENABLED  = False
STALE_DATA_AUTO_REPAIR_ENABLED = False

# Output filenames
_FILE_RECORDS       = "freshness_records.csv"
_FILE_ALERTS        = "freshness_alerts.csv"
_FILE_SOURCE_HEALTH = "freshness_source_health.csv"
_FILE_SUMMARY       = "freshness_summary.csv"
_FILE_HISTORY       = "freshness_history.csv"
_FILE_REPAIR        = "freshness_repair_handoff.csv"
_FILE_UNRESOLVED    = "freshness_unresolved.csv"


def _auto_output_dir() -> str:
    """Infer default output dir as <repo_root>/data/freshness_reports/."""
    here = os.path.abspath(__file__)
    repo_root = os.path.dirname(os.path.dirname(here))
    return os.path.join(repo_root, "data", "freshness_reports")


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _write_csv(path: str, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    """Write rows to a CSV file, creating/overwriting."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _append_csv(path: str, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    """Append rows to a CSV file, writing header only if file is new/empty."""
    write_header = not os.path.isfile(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _read_csv(path: str) -> List[Dict[str, str]]:
    """Read all rows from a CSV file. Returns empty list if file missing."""
    if not os.path.isfile(path):
        return []
    try:
        with open(path, newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as exc:
        logger.warning("Could not read CSV %s: %s", path, exc)
        return []


def _bool_from_str(val: Any) -> bool:
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() in ("true", "1", "yes")


def _int_or_none(val: Any) -> Optional[int]:
    if val is None or val == "":
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


# Column definitions
_RECORD_FIELDS = [
    "record_id", "symbol", "tier", "dataset", "source",
    "expected_latest_date", "actual_latest_date", "previous_latest_date",
    "calendar_age_days", "trading_day_lag", "row_count", "latest_row_valid",
    "future_date_detected", "date_regression_detected",
    "status", "severity", "sla_name", "sla_limit",
    "detected_at", "reason", "research_only", "no_real_orders",
]

_ALERT_FIELDS = [
    "alert_id", "symbol", "dataset", "source", "alert_type", "severity",
    "status", "message", "first_detected_at", "last_detected_at",
    "occurrence_count", "repair_issue_id", "acknowledged",
    "research_only", "no_real_orders",
]

_SOURCE_HEALTH_FIELDS = [
    "source_id", "source_name", "dataset", "symbols_expected",
    "symbols_fresh", "symbols_delayed", "symbols_stale", "symbols_missing",
    "latest_seen_at", "interruption_suspected", "interruption_started_at",
    "status", "severity", "reason",
]

_SUMMARY_FIELDS = [
    "generated_at", "tier",
    "fresh_count", "acceptable_count", "delayed_count", "stale_count",
    "interrupted_count", "missing_count", "critical_count",
    "overall_status", "confidence", "research_only", "no_real_orders",
    "symbols", "datasets",
]

_REPAIR_FIELDS = [
    "issue_id", "alert_id", "symbol", "dataset", "source",
    "issue_type", "repairability", "action", "auto_safe",
    "priority", "message", "research_only", "no_real_orders",
]


class FreshnessStore:
    """
    Persistence layer for all freshness monitor outputs.

    Writes to data/freshness_reports/ (runtime directory, not committed to git).
    Uses csv module only — no pandas dependency.
    """

    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir: str = output_dir or _auto_output_dir()
        _ensure_dir(self.output_dir)

    def _path(self, filename: str) -> str:
        return os.path.join(self.output_dir, filename)

    # ------------------------------------------------------------------
    # Save methods
    # ------------------------------------------------------------------

    def save_records(self, records: List[DatasetFreshnessRecord]) -> str:
        """Save freshness records to CSV. Returns file path."""
        path = self._path(_FILE_RECORDS)
        rows = [r.to_dict() for r in records]
        _write_csv(path, rows, _RECORD_FIELDS)
        logger.info("Saved %d freshness records to %s", len(records), path)
        return path

    def save_alerts(self, alerts: List[FreshnessAlert]) -> str:
        """Save alerts to CSV. Returns file path."""
        path = self._path(_FILE_ALERTS)
        rows = [a.to_dict() for a in alerts]
        _write_csv(path, rows, _ALERT_FIELDS)
        logger.info("Saved %d alerts to %s", len(alerts), path)
        return path

    def save_source_health(self, statuses: List[SourceFreshnessStatus]) -> str:
        """Save source health statuses to CSV. Returns file path."""
        path = self._path(_FILE_SOURCE_HEALTH)
        rows = [s.to_dict() for s in statuses]
        _write_csv(path, rows, _SOURCE_HEALTH_FIELDS)
        logger.info("Saved %d source health records to %s", len(statuses), path)
        return path

    def save_summary(self, summary: FreshnessSummary) -> str:
        """Save summary to CSV (single row). Returns file path."""
        path = self._path(_FILE_SUMMARY)
        d = summary.to_dict()
        # Flatten list fields to JSON strings for CSV
        d["symbols"] = json.dumps(d.get("symbols", []))
        d["datasets"] = json.dumps(d.get("datasets", []))
        # Drop nested source_health dict (too complex for flat CSV)
        d.pop("source_health", None)
        _write_csv(path, [d], _SUMMARY_FIELDS)
        logger.info("Saved summary to %s", path)
        return path

    def append_history(self, records: List[DatasetFreshnessRecord]) -> str:
        """Append records to the history file. Returns file path."""
        path = self._path(_FILE_HISTORY)
        rows = [r.to_dict() for r in records]
        _append_csv(path, rows, _RECORD_FIELDS)
        logger.info("Appended %d records to history at %s", len(records), path)
        return path

    def save_repair_handoff(self, handoff: List[Dict[str, Any]]) -> str:
        """Save repair handoff dicts to CSV. Returns file path."""
        path = self._path(_FILE_REPAIR)
        _write_csv(path, handoff, _REPAIR_FIELDS)
        logger.info("Saved %d repair handoff items to %s", len(handoff), path)
        return path

    def save_unresolved(self, alerts: List[FreshnessAlert]) -> str:
        """Save unresolved alerts to CSV. Returns file path."""
        path = self._path(_FILE_UNRESOLVED)
        rows = [a.to_dict() for a in alerts]
        _write_csv(path, rows, _ALERT_FIELDS)
        logger.info("Saved %d unresolved alerts to %s", len(alerts), path)
        return path

    # ------------------------------------------------------------------
    # Load methods
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> Optional[FreshnessSummary]:
        """Load the latest freshness summary from CSV. Returns None if missing."""
        path = self._path(_FILE_SUMMARY)
        rows = _read_csv(path)
        if not rows:
            return None
        try:
            row = rows[-1]  # Latest row
            # Parse JSON-encoded list fields
            symbols_raw = row.get("symbols", "[]")
            datasets_raw = row.get("datasets", "[]")
            try:
                symbols = json.loads(symbols_raw) if symbols_raw else []
            except Exception:
                symbols = []
            try:
                datasets = json.loads(datasets_raw) if datasets_raw else []
            except Exception:
                datasets = []

            summary = FreshnessSummary(
                generated_at=row.get("generated_at", ""),
                tier=row.get("tier", ""),
            )
            summary.symbols = symbols
            summary.datasets = datasets
            summary.fresh_count       = _int_or_none(row.get("fresh_count")) or 0
            summary.acceptable_count  = _int_or_none(row.get("acceptable_count")) or 0
            summary.delayed_count     = _int_or_none(row.get("delayed_count")) or 0
            summary.stale_count       = _int_or_none(row.get("stale_count")) or 0
            summary.interrupted_count = _int_or_none(row.get("interrupted_count")) or 0
            summary.missing_count     = _int_or_none(row.get("missing_count")) or 0
            summary.critical_count    = _int_or_none(row.get("critical_count")) or 0
            summary.source_health     = {}
            summary.overall_status    = row.get("overall_status", "UNKNOWN")
            summary.confidence        = row.get("confidence", "LOW")
            summary.research_only     = _bool_from_str(row.get("research_only", "True"))
            summary.no_real_orders    = _bool_from_str(row.get("no_real_orders", "True"))
            return summary
        except Exception as exc:
            logger.warning("Could not parse summary from %s: %s", path, exc)
            return None

    def load_latest_records(self) -> List[DatasetFreshnessRecord]:
        """Load latest freshness records from CSV."""
        path = self._path(_FILE_RECORDS)
        rows = _read_csv(path)
        records: List[DatasetFreshnessRecord] = []
        for row in rows:
            try:
                # Convert types
                d: Dict[str, Any] = dict(row)
                d["calendar_age_days"] = _int_or_none(d.get("calendar_age_days"))
                d["trading_day_lag"]   = _int_or_none(d.get("trading_day_lag"))
                d["row_count"]         = _int_or_none(d.get("row_count")) or 0
                d["sla_limit"]         = _int_or_none(d.get("sla_limit"))
                d["latest_row_valid"]         = _bool_from_str(d.get("latest_row_valid", "True"))
                d["future_date_detected"]     = _bool_from_str(d.get("future_date_detected", "False"))
                d["date_regression_detected"] = _bool_from_str(d.get("date_regression_detected", "False"))
                d["research_only"]   = _bool_from_str(d.get("research_only", "True"))
                d["no_real_orders"]  = _bool_from_str(d.get("no_real_orders", "True"))
                records.append(DatasetFreshnessRecord.from_dict(d))
            except Exception as exc:
                logger.warning("Could not parse record row: %s", exc)
        return records

    def load_alerts(self) -> List[FreshnessAlert]:
        """Load alerts from CSV."""
        path = self._path(_FILE_ALERTS)
        rows = _read_csv(path)
        alerts: List[FreshnessAlert] = []
        for row in rows:
            try:
                d: Dict[str, Any] = dict(row)
                d["occurrence_count"] = _int_or_none(d.get("occurrence_count")) or 1
                d["acknowledged"]     = _bool_from_str(d.get("acknowledged", "False"))
                d["research_only"]    = _bool_from_str(d.get("research_only", "True"))
                d["no_real_orders"]   = _bool_from_str(d.get("no_real_orders", "True"))
                d["repair_issue_id"]  = d.get("repair_issue_id") or None
                alerts.append(FreshnessAlert.from_dict(d))
            except Exception as exc:
                logger.warning("Could not parse alert row: %s", exc)
        return alerts
