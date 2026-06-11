"""
maintenance/data_report_hygiene_schema.py — Data & Report Hygiene Schema for v1.0.2.

Dataclasses for inventory items, report manifests, and hygiene summary.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Data Cleanup is Review Only. Archive Suggestions Only.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS      = True
PRODUCTION_BLOCKED  = True
REVIEW_ONLY         = True
DATA_CLEANUP_REVIEW_ONLY  = True
ARCHIVE_SUGGESTIONS_ONLY  = True

# Categories
CATEGORY_REPORT             = "REPORT"
CATEGORY_BACKTEST_RESULT    = "BACKTEST_RESULT"
CATEGORY_IMPORT_DATA        = "IMPORT_DATA"
CATEGORY_LOG                = "LOG"
CATEGORY_CACHE              = "CACHE"
CATEGORY_EXPERIMENT_OUTPUT  = "EXPERIMENT_OUTPUT"
CATEGORY_DATABASE           = "DATABASE"
CATEGORY_SPREADSHEET        = "SPREADSHEET"
CATEGORY_JSON_OUTPUT        = "JSON_OUTPUT"
CATEGORY_UNKNOWN            = "UNKNOWN"

# Action hints
ACTION_REVIEW           = "REVIEW"
ACTION_FIX_DATA         = "FIX_DATA"
ACTION_READ_REPORT      = "READ_REPORT"
ACTION_ARCHIVE_REVIEW   = "ARCHIVE_REVIEW"
ACTION_CLEANUP_REVIEW   = "CLEANUP_REVIEW"
ACTION_KEEP_OBSERVING   = "KEEP_OBSERVING"
ACTION_WAIT             = "WAIT"

# Severity levels
SEV_INFO    = "INFO"
SEV_LOW     = "LOW"
SEV_MEDIUM  = "MEDIUM"
SEV_HIGH    = "HIGH"
SEV_BLOCKED = "BLOCKED"


@dataclass
class HygieneInventoryItem:
    """One inventory item discovered during the hygiene scan.

    [!] Research Only. No Real Orders. Data Cleanup is Review Only.
    """
    item_id: str
    path: str
    category: str           # REPORT|BACKTEST_RESULT|IMPORT_DATA|LOG|CACHE|EXPERIMENT_OUTPUT|DATABASE|SPREADSHEET|JSON_OUTPUT|UNKNOWN
    file_type: str
    size_bytes: int
    modified_at: str
    age_days: float
    is_runtime_output: bool
    is_git_ignored: bool
    is_git_tracked: bool
    should_be_ignored: bool
    action_hint: str        # REVIEW|FIX_DATA|READ_REPORT|ARCHIVE_REVIEW|CLEANUP_REVIEW|KEEP_OBSERVING|WAIT
    severity: str           # INFO|LOW|MEDIUM|HIGH|BLOCKED
    reason: str
    no_real_orders: bool = True
    production_blocked: bool = True
    review_only: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "HygieneInventoryItem":
        return cls(
            item_id=d.get("item_id", ""),
            path=d.get("path", ""),
            category=d.get("category", CATEGORY_UNKNOWN),
            file_type=d.get("file_type", ""),
            size_bytes=int(d.get("size_bytes", 0)),
            modified_at=d.get("modified_at", ""),
            age_days=float(d.get("age_days", 0.0)),
            is_runtime_output=_to_bool(d.get("is_runtime_output", False)),
            is_git_ignored=_to_bool(d.get("is_git_ignored", False)),
            is_git_tracked=_to_bool(d.get("is_git_tracked", False)),
            should_be_ignored=_to_bool(d.get("should_be_ignored", False)),
            action_hint=d.get("action_hint", ACTION_REVIEW),
            severity=d.get("severity", SEV_INFO),
            reason=d.get("reason", ""),
            no_real_orders=_to_bool(d.get("no_real_orders", True)),
            production_blocked=_to_bool(d.get("production_blocked", True)),
            review_only=_to_bool(d.get("review_only", True)),
        )


@dataclass
class HygieneReportManifest:
    """Manifest entry for one discovered report file.

    [!] Research Only. No Real Orders. Data Cleanup is Review Only.
    """
    report_id: str
    report_path: str
    report_type: str
    generated_at: str
    module: str
    version: str
    is_latest: bool
    is_runtime_output: bool
    is_git_ignored: bool
    should_be_ignored: bool
    summary: str
    no_real_orders: bool = True
    review_only: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "HygieneReportManifest":
        return cls(
            report_id=d.get("report_id", ""),
            report_path=d.get("report_path", ""),
            report_type=d.get("report_type", ""),
            generated_at=d.get("generated_at", ""),
            module=d.get("module", ""),
            version=d.get("version", ""),
            is_latest=_to_bool(d.get("is_latest", False)),
            is_runtime_output=_to_bool(d.get("is_runtime_output", False)),
            is_git_ignored=_to_bool(d.get("is_git_ignored", False)),
            should_be_ignored=_to_bool(d.get("should_be_ignored", False)),
            summary=d.get("summary", ""),
            no_real_orders=_to_bool(d.get("no_real_orders", True)),
            review_only=_to_bool(d.get("review_only", True)),
        )


@dataclass
class HygieneSummary:
    """Aggregate summary from one hygiene scan run.

    [!] Research Only. No Real Orders. Data Cleanup is Review Only.
    """
    generated_at: str
    version: str
    total_items: int
    runtime_outputs: int
    git_tracked_runtime_outputs: int
    ignored_outputs: int
    missing_gitignore_rules: int
    stale_reports: int
    stale_csv_outputs: int
    stale_json_outputs: int
    large_files: int
    database_files: int
    spreadsheet_files: int
    blocked_count: int
    warning_count: int
    report_count: int
    latest_reports: int
    no_real_orders: bool = True
    production_blocked: bool = True
    review_only: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "HygieneSummary":
        return cls(
            generated_at=d.get("generated_at", ""),
            version=d.get("version", ""),
            total_items=int(d.get("total_items", 0)),
            runtime_outputs=int(d.get("runtime_outputs", 0)),
            git_tracked_runtime_outputs=int(d.get("git_tracked_runtime_outputs", 0)),
            ignored_outputs=int(d.get("ignored_outputs", 0)),
            missing_gitignore_rules=int(d.get("missing_gitignore_rules", 0)),
            stale_reports=int(d.get("stale_reports", 0)),
            stale_csv_outputs=int(d.get("stale_csv_outputs", 0)),
            stale_json_outputs=int(d.get("stale_json_outputs", 0)),
            large_files=int(d.get("large_files", 0)),
            database_files=int(d.get("database_files", 0)),
            spreadsheet_files=int(d.get("spreadsheet_files", 0)),
            blocked_count=int(d.get("blocked_count", 0)),
            warning_count=int(d.get("warning_count", 0)),
            report_count=int(d.get("report_count", 0)),
            latest_reports=int(d.get("latest_reports", 0)),
            no_real_orders=_to_bool(d.get("no_real_orders", True)),
            production_blocked=_to_bool(d.get("production_blocked", True)),
            review_only=_to_bool(d.get("review_only", True)),
        )


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _to_bool(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() in ("true", "1", "yes")
    return bool(v)
