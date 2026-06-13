"""
data_onboarding/onboarding_schema.py — Onboarding dataclasses for TW Quant Cockpit v1.1.1.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] dry_run=True by default. No write without explicit allow_write=True.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# ---------------------------------------------------------------------------
# Import mode constants
# ---------------------------------------------------------------------------
IMPORT_MODE_MERGE_SAFE     = "MERGE_SAFE"       # Safe: add new rows only, no overwrite
IMPORT_MODE_APPEND_SAFE    = "APPEND_SAFE"       # Safe: append only, skip duplicates
IMPORT_MODE_REPLACE_EXPLICIT = "REPLACE_EXPLICIT"  # Destructive: replace all; disabled by default
IMPORT_MODE_DRY_RUN        = "DRY_RUN"          # No write at all

VALID_IMPORT_MODES = [
    IMPORT_MODE_MERGE_SAFE,
    IMPORT_MODE_APPEND_SAFE,
    IMPORT_MODE_REPLACE_EXPLICIT,
    IMPORT_MODE_DRY_RUN,
]

# ---------------------------------------------------------------------------
# File type constants
# ---------------------------------------------------------------------------
FILE_TYPE_XQ_EXCEL     = "XQ_EXCEL"
FILE_TYPE_XQ_CSV       = "XQ_CSV"
FILE_TYPE_STANDARD_CSV = "STANDARD_CSV"
FILE_TYPE_EXCEL        = "EXCEL"
FILE_TYPE_UNKNOWN      = "UNKNOWN"

# ---------------------------------------------------------------------------
# Validation status constants
# ---------------------------------------------------------------------------
VALIDATION_OK      = "OK"
VALIDATION_WARNING = "WARNING"
VALIDATION_FAIL    = "FAIL"
VALIDATION_BLOCKED = "BLOCKED"

# ---------------------------------------------------------------------------
# Plan action constants
# ---------------------------------------------------------------------------
PLAN_ACTION_MERGE_SAFE      = "MERGE_SAFE"
PLAN_ACTION_APPEND_SAFE     = "APPEND_SAFE"
PLAN_ACTION_REPLACE_EXPLICIT = "REPLACE_EXPLICIT"
PLAN_ACTION_SKIP            = "SKIP"
PLAN_ACTION_REVIEW          = "REVIEW"
PLAN_ACTION_BLOCKED         = "BLOCKED"

# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------
NO_REAL_ORDERS              = True
BROKER_DISABLED             = True
DRY_RUN_DEFAULT             = True
DESTRUCTIVE_IMPORT_DISABLED = True


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class DiscoveredFile:
    """Metadata about a discovered importable file."""
    file_path: str
    file_name: str
    file_type: str
    size_bytes: int
    detected_symbol: Optional[str]
    detected_dataset: Optional[str]
    sheet_count: int
    encoding_hint: str
    mapping_confidence: float   # 0.0 - 1.0
    columns_raw: List[str] = field(default_factory=list)
    columns_mapped: Dict[str, str] = field(default_factory=dict)
    preview_rows: int = 0
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "file_path":          self.file_path,
            "file_name":          self.file_name,
            "file_type":          self.file_type,
            "size_bytes":         self.size_bytes,
            "detected_symbol":    self.detected_symbol,
            "detected_dataset":   self.detected_dataset,
            "sheet_count":        self.sheet_count,
            "encoding_hint":      self.encoding_hint,
            "mapping_confidence": self.mapping_confidence,
            "columns_raw":        self.columns_raw,
            "columns_mapped":     self.columns_mapped,
            "preview_rows":       self.preview_rows,
            "warnings":           self.warnings,
            "errors":             self.errors,
            "research_only":      self.research_only,
            "no_real_orders":     self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "DiscoveredFile":
        return cls(
            file_path=d.get("file_path", ""),
            file_name=d.get("file_name", ""),
            file_type=d.get("file_type", FILE_TYPE_UNKNOWN),
            size_bytes=d.get("size_bytes", 0),
            detected_symbol=d.get("detected_symbol"),
            detected_dataset=d.get("detected_dataset"),
            sheet_count=d.get("sheet_count", 0),
            encoding_hint=d.get("encoding_hint", "utf-8"),
            mapping_confidence=d.get("mapping_confidence", 0.0),
            columns_raw=d.get("columns_raw", []),
            columns_mapped=d.get("columns_mapped", {}),
            preview_rows=d.get("preview_rows", 0),
            warnings=d.get("warnings", []),
            errors=d.get("errors", []),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class FileValidationResult:
    """Result of validating a single importable file."""
    file_path: str
    symbol: Optional[str]
    dataset: str
    status: str          # OK / WARNING / FAIL / BLOCKED
    row_count: int
    valid_rows: int
    invalid_rows: int
    duplicate_count: int
    conflict_count: int
    missing_required_cols: List[str] = field(default_factory=list)
    missing_optional_cols: List[str] = field(default_factory=list)
    date_range_start: Optional[str] = None
    date_range_end: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "file_path":             self.file_path,
            "symbol":                self.symbol,
            "dataset":               self.dataset,
            "status":                self.status,
            "row_count":             self.row_count,
            "valid_rows":            self.valid_rows,
            "invalid_rows":          self.invalid_rows,
            "duplicate_count":       self.duplicate_count,
            "conflict_count":        self.conflict_count,
            "missing_required_cols": self.missing_required_cols,
            "missing_optional_cols": self.missing_optional_cols,
            "date_range_start":      self.date_range_start,
            "date_range_end":        self.date_range_end,
            "warnings":              self.warnings,
            "errors":                self.errors,
            "research_only":         self.research_only,
            "no_real_orders":        self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "FileValidationResult":
        return cls(
            file_path=d.get("file_path", ""),
            symbol=d.get("symbol"),
            dataset=d.get("dataset", "daily"),
            status=d.get("status", VALIDATION_FAIL),
            row_count=d.get("row_count", 0),
            valid_rows=d.get("valid_rows", 0),
            invalid_rows=d.get("invalid_rows", 0),
            duplicate_count=d.get("duplicate_count", 0),
            conflict_count=d.get("conflict_count", 0),
            missing_required_cols=d.get("missing_required_cols", []),
            missing_optional_cols=d.get("missing_optional_cols", []),
            date_range_start=d.get("date_range_start"),
            date_range_end=d.get("date_range_end"),
            warnings=d.get("warnings", []),
            errors=d.get("errors", []),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class ImportPlanItem:
    """Plan for importing a single file."""
    file_path: str
    symbol: Optional[str]
    dataset: str
    file_type: str
    action: str         # MERGE_SAFE / APPEND_SAFE / REPLACE_EXPLICIT / SKIP / REVIEW / BLOCKED
    import_mode: str
    dry_run: bool = True
    destructive: bool = False
    blocked_reason: Optional[str] = None
    expected_new_rows: int = 0
    expected_skip_rows: int = 0
    expected_conflict_rows: int = 0
    requires_review: bool = False
    validation_status: str = VALIDATION_OK
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "file_path":              self.file_path,
            "symbol":                 self.symbol,
            "dataset":                self.dataset,
            "file_type":              self.file_type,
            "action":                 self.action,
            "import_mode":            self.import_mode,
            "dry_run":                self.dry_run,
            "destructive":            self.destructive,
            "blocked_reason":         self.blocked_reason,
            "expected_new_rows":      self.expected_new_rows,
            "expected_skip_rows":     self.expected_skip_rows,
            "expected_conflict_rows": self.expected_conflict_rows,
            "requires_review":        self.requires_review,
            "validation_status":      self.validation_status,
            "research_only":          self.research_only,
            "no_real_orders":         self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ImportPlanItem":
        return cls(
            file_path=d.get("file_path", ""),
            symbol=d.get("symbol"),
            dataset=d.get("dataset", "daily"),
            file_type=d.get("file_type", FILE_TYPE_UNKNOWN),
            action=d.get("action", PLAN_ACTION_SKIP),
            import_mode=d.get("import_mode", IMPORT_MODE_DRY_RUN),
            dry_run=d.get("dry_run", True),
            destructive=d.get("destructive", False),
            blocked_reason=d.get("blocked_reason"),
            expected_new_rows=d.get("expected_new_rows", 0),
            expected_skip_rows=d.get("expected_skip_rows", 0),
            expected_conflict_rows=d.get("expected_conflict_rows", 0),
            requires_review=d.get("requires_review", False),
            validation_status=d.get("validation_status", VALIDATION_OK),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class ImportPlan:
    """Full import plan for a batch of files."""
    plan_id: str
    created_at: str
    source_path: str
    total_files: int
    merge_safe_count: int
    append_safe_count: int
    replace_explicit_count: int
    blocked_count: int
    review_count: int
    skip_count: int
    items: List[ImportPlanItem] = field(default_factory=list)
    dry_run: bool = True
    destructive_disabled: bool = True
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "plan_id":               self.plan_id,
            "created_at":            self.created_at,
            "source_path":           self.source_path,
            "total_files":           self.total_files,
            "merge_safe_count":      self.merge_safe_count,
            "append_safe_count":     self.append_safe_count,
            "replace_explicit_count": self.replace_explicit_count,
            "blocked_count":         self.blocked_count,
            "review_count":          self.review_count,
            "skip_count":            self.skip_count,
            "items":                 [i.to_dict() for i in self.items],
            "dry_run":               self.dry_run,
            "destructive_disabled":  self.destructive_disabled,
            "research_only":         self.research_only,
            "no_real_orders":        self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ImportPlan":
        items = [ImportPlanItem.from_dict(i) for i in d.get("items", [])]
        return cls(
            plan_id=d.get("plan_id", ""),
            created_at=d.get("created_at", ""),
            source_path=d.get("source_path", ""),
            total_files=d.get("total_files", 0),
            merge_safe_count=d.get("merge_safe_count", 0),
            append_safe_count=d.get("append_safe_count", 0),
            replace_explicit_count=d.get("replace_explicit_count", 0),
            blocked_count=d.get("blocked_count", 0),
            review_count=d.get("review_count", 0),
            skip_count=d.get("skip_count", 0),
            items=items,
            dry_run=d.get("dry_run", True),
            destructive_disabled=d.get("destructive_disabled", True),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class ImportResult:
    """Result of importing a single file."""
    result_id: str
    plan_id: str
    file_path: str
    symbol: Optional[str]
    dataset: str
    status: str         # OK / PARTIAL / FAILED / SKIPPED / BLOCKED / DRY_RUN
    rows_imported: int
    rows_skipped: int
    rows_failed: int
    conflicts_detected: int
    conflicts_kept: int
    dry_run: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    executed_at: Optional[str] = None
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "result_id":          self.result_id,
            "plan_id":            self.plan_id,
            "file_path":          self.file_path,
            "symbol":             self.symbol,
            "dataset":            self.dataset,
            "status":             self.status,
            "rows_imported":      self.rows_imported,
            "rows_skipped":       self.rows_skipped,
            "rows_failed":        self.rows_failed,
            "conflicts_detected": self.conflicts_detected,
            "conflicts_kept":     self.conflicts_kept,
            "dry_run":            self.dry_run,
            "warnings":           self.warnings,
            "errors":             self.errors,
            "executed_at":        self.executed_at,
            "research_only":      self.research_only,
            "no_real_orders":     self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ImportResult":
        return cls(
            result_id=d.get("result_id", ""),
            plan_id=d.get("plan_id", ""),
            file_path=d.get("file_path", ""),
            symbol=d.get("symbol"),
            dataset=d.get("dataset", "daily"),
            status=d.get("status", "FAILED"),
            rows_imported=d.get("rows_imported", 0),
            rows_skipped=d.get("rows_skipped", 0),
            rows_failed=d.get("rows_failed", 0),
            conflicts_detected=d.get("conflicts_detected", 0),
            conflicts_kept=d.get("conflicts_kept", 0),
            dry_run=d.get("dry_run", True),
            warnings=d.get("warnings", []),
            errors=d.get("errors", []),
            executed_at=d.get("executed_at"),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class BatchImportSummary:
    """Summary of a batch import session."""
    batch_id: str
    created_at: str
    source_path: str
    total_files: int
    succeeded: int
    partial: int
    failed: int
    skipped: int
    blocked: int
    dry_run: bool = True
    results: List[ImportResult] = field(default_factory=list)
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "batch_id":    self.batch_id,
            "created_at":  self.created_at,
            "source_path": self.source_path,
            "total_files": self.total_files,
            "succeeded":   self.succeeded,
            "partial":     self.partial,
            "failed":      self.failed,
            "skipped":     self.skipped,
            "blocked":     self.blocked,
            "dry_run":     self.dry_run,
            "results":     [r.to_dict() for r in self.results],
            "research_only":  self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "BatchImportSummary":
        results = [ImportResult.from_dict(r) for r in d.get("results", [])]
        return cls(
            batch_id=d.get("batch_id", ""),
            created_at=d.get("created_at", ""),
            source_path=d.get("source_path", ""),
            total_files=d.get("total_files", 0),
            succeeded=d.get("succeeded", 0),
            partial=d.get("partial", 0),
            failed=d.get("failed", 0),
            skipped=d.get("skipped", 0),
            blocked=d.get("blocked", 0),
            dry_run=d.get("dry_run", True),
            results=results,
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class RetryManifest:
    """Manifest of files that failed and need retry."""
    manifest_id: str
    created_at: str
    source_path: str
    failed_files: List[str] = field(default_factory=list)
    failed_symbols: List[str] = field(default_factory=list)
    retry_count: int = 0
    last_retry_at: Optional[str] = None
    resolved: bool = False
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "manifest_id":    self.manifest_id,
            "created_at":     self.created_at,
            "source_path":    self.source_path,
            "failed_files":   self.failed_files,
            "failed_symbols": self.failed_symbols,
            "retry_count":    self.retry_count,
            "last_retry_at":  self.last_retry_at,
            "resolved":       self.resolved,
            "research_only":  self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RetryManifest":
        return cls(
            manifest_id=d.get("manifest_id", ""),
            created_at=d.get("created_at", ""),
            source_path=d.get("source_path", ""),
            failed_files=d.get("failed_files", []),
            failed_symbols=d.get("failed_symbols", []),
            retry_count=d.get("retry_count", 0),
            last_retry_at=d.get("last_retry_at"),
            resolved=d.get("resolved", False),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )
