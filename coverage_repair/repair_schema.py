"""
coverage_repair/repair_schema.py — Rich coverage issue and repair schema for v1.1.2.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] dry_run=True default. destructive=False default.
[!] INVALID OHLC: never auto-modify. CONFLICT: never auto-overwrite.
[!] Synthetic price repair: DISABLED. External data download: DISABLED.
"""
from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from datetime import datetime
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Issue type constants (18 types)
# ---------------------------------------------------------------------------
ISSUE_MISSING_SYMBOL_DATA    = "MISSING_SYMBOL_DATA"
ISSUE_INSUFFICIENT_HISTORY   = "INSUFFICIENT_HISTORY"
ISSUE_PARTIAL_OHLC           = "PARTIAL_OHLC"
ISSUE_MISSING_VOLUME         = "MISSING_VOLUME"
ISSUE_DUPLICATE_DATE         = "DUPLICATE_DATE"
ISSUE_CONFLICTING_ROW        = "CONFLICTING_ROW"
ISSUE_INVALID_OHLC           = "INVALID_OHLC"
ISSUE_INVALID_VOLUME         = "INVALID_VOLUME"
ISSUE_FUTURE_DATE            = "FUTURE_DATE"
ISSUE_STALE_DATA             = "STALE_DATA"
ISSUE_DATE_GAP               = "DATE_GAP"
ISSUE_MISSING_CHIPS          = "MISSING_CHIPS"
ISSUE_MISSING_REVENUE        = "MISSING_REVENUE"
ISSUE_MISSING_FUNDAMENTALS   = "MISSING_FUNDAMENTALS"
ISSUE_SCHEMA_MISMATCH        = "SCHEMA_MISMATCH"
ISSUE_SOURCE_UNKNOWN         = "SOURCE_UNKNOWN"
ISSUE_IMPORT_FAILED          = "IMPORT_FAILED"
ISSUE_LOW_MAPPING_CONFIDENCE = "LOW_MAPPING_CONFIDENCE"

ALL_ISSUE_TYPES = [
    ISSUE_MISSING_SYMBOL_DATA,
    ISSUE_INSUFFICIENT_HISTORY,
    ISSUE_PARTIAL_OHLC,
    ISSUE_MISSING_VOLUME,
    ISSUE_DUPLICATE_DATE,
    ISSUE_CONFLICTING_ROW,
    ISSUE_INVALID_OHLC,
    ISSUE_INVALID_VOLUME,
    ISSUE_FUTURE_DATE,
    ISSUE_STALE_DATA,
    ISSUE_DATE_GAP,
    ISSUE_MISSING_CHIPS,
    ISSUE_MISSING_REVENUE,
    ISSUE_MISSING_FUNDAMENTALS,
    ISSUE_SCHEMA_MISMATCH,
    ISSUE_SOURCE_UNKNOWN,
    ISSUE_IMPORT_FAILED,
    ISSUE_LOW_MAPPING_CONFIDENCE,
]

# ---------------------------------------------------------------------------
# Severity constants
# ---------------------------------------------------------------------------
SEVERITY_INFO     = "INFO"
SEVERITY_LOW      = "LOW"
SEVERITY_MEDIUM   = "MEDIUM"
SEVERITY_HIGH     = "HIGH"
SEVERITY_CRITICAL = "CRITICAL"

ALL_SEVERITIES = [SEVERITY_INFO, SEVERITY_LOW, SEVERITY_MEDIUM, SEVERITY_HIGH, SEVERITY_CRITICAL]

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
STATUS_OPEN              = "OPEN"
STATUS_PLANNED           = "PLANNED"
STATUS_IN_PROGRESS       = "IN_PROGRESS"
STATUS_REPAIRED          = "REPAIRED"
STATUS_PARTIAL           = "PARTIAL"
STATUS_BLOCKED           = "BLOCKED"
STATUS_NEEDS_SOURCE_DATA = "NEEDS_SOURCE_DATA"
STATUS_NEEDS_REVIEW      = "NEEDS_REVIEW"
STATUS_WONT_FIX          = "WONT_FIX"

ALL_STATUSES = [
    STATUS_OPEN, STATUS_PLANNED, STATUS_IN_PROGRESS, STATUS_REPAIRED,
    STATUS_PARTIAL, STATUS_BLOCKED, STATUS_NEEDS_SOURCE_DATA,
    STATUS_NEEDS_REVIEW, STATUS_WONT_FIX,
]

# ---------------------------------------------------------------------------
# Repairability constants
# ---------------------------------------------------------------------------
REPAIRABILITY_AUTO_SAFE       = "AUTO_SAFE"
REPAIRABILITY_SEMI_AUTO       = "SEMI_AUTO"
REPAIRABILITY_MANUAL          = "MANUAL"
REPAIRABILITY_SOURCE_REQUIRED = "SOURCE_REQUIRED"
REPAIRABILITY_NOT_REPAIRABLE  = "NOT_REPAIRABLE"

ALL_REPAIRABILITIES = [
    REPAIRABILITY_AUTO_SAFE, REPAIRABILITY_SEMI_AUTO, REPAIRABILITY_MANUAL,
    REPAIRABILITY_SOURCE_REQUIRED, REPAIRABILITY_NOT_REPAIRABLE,
]

# ---------------------------------------------------------------------------
# Action constants
# ---------------------------------------------------------------------------
ACTION_REVIEW               = "REVIEW"
ACTION_FIX_DATA             = "FIX_DATA"
ACTION_REIMPORT             = "REIMPORT"
ACTION_MERGE_SAFE           = "MERGE_SAFE"
ACTION_DEDUPLICATE_SAFE     = "DEDUPLICATE_SAFE"
ACTION_NORMALIZE_SCHEMA     = "NORMALIZE_SCHEMA"
ACTION_NORMALIZE_DATE       = "NORMALIZE_DATE"
ACTION_REFRESH_COVERAGE     = "REFRESH_COVERAGE"
ACTION_PROVIDE_SOURCE_DATA  = "PROVIDE_SOURCE_DATA"
ACTION_KEEP_OBSERVING       = "KEEP_OBSERVING"
ACTION_WAIT                 = "WAIT"

# ---------------------------------------------------------------------------
# Repair mode constants
# ---------------------------------------------------------------------------
REPAIR_MODE_DRY_RUN              = "DRY_RUN"
REPAIR_MODE_METADATA_ONLY        = "METADATA_ONLY"
REPAIR_MODE_DEDUPLICATE_IDENTICAL = "DEDUPLICATE_IDENTICAL"
REPAIR_MODE_NORMALIZE_SAFE       = "NORMALIZE_SAFE"
REPAIR_MODE_REIMPORT_SAFE        = "REIMPORT_SAFE"
REPAIR_MODE_MERGE_SAFE           = "MERGE_SAFE"
REPAIR_MODE_MANUAL_REVIEW        = "MANUAL_REVIEW"
REPAIR_MODE_BLOCKED              = "BLOCKED"

# ---------------------------------------------------------------------------
# Priority constants
# ---------------------------------------------------------------------------
PRIORITY_P0 = "P0"
PRIORITY_P1 = "P1"
PRIORITY_P2 = "P2"
PRIORITY_P3 = "P3"

# ---------------------------------------------------------------------------
# Result status constants
# ---------------------------------------------------------------------------
RESULT_STATUS_REPAIRED        = "REPAIRED"
RESULT_STATUS_DRY_RUN         = "DRY_RUN"
RESULT_STATUS_PARTIAL         = "PARTIAL"
RESULT_STATUS_BLOCKED         = "BLOCKED"
RESULT_STATUS_SKIPPED         = "SKIPPED"
RESULT_STATUS_FAILED          = "FAILED"
RESULT_STATUS_MANUAL          = "MANUAL_REVIEW"
RESULT_STATUS_SOURCE_REQUIRED = "SOURCE_REQUIRED"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class CoverageIssue:
    """Represents a single detected coverage issue for a symbol/dataset.

    [!] Research Only. No Real Orders.
    """
    issue_id:        str
    symbol:          str
    issue_type:      str
    dataset:         str                   = "daily"
    tier:            Optional[str]         = None
    severity:        str                   = SEVERITY_MEDIUM
    field:           Optional[str]         = None
    first_date:      Optional[str]         = None
    last_date:       Optional[str]         = None
    affected_rows:   int                   = 0
    affected_ratio:  float                 = 0.0
    detected_at:     str                   = dc_field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    source:          Optional[str]         = None
    status:          str                   = STATUS_OPEN
    repairability:   str                   = REPAIRABILITY_MANUAL
    reason:          Optional[str]         = None
    evidence:        Optional[Dict[str, Any]] = None
    research_only:   bool                  = True
    no_real_orders:  bool                  = True

    def to_dict(self) -> dict:
        return {
            "issue_id":       self.issue_id,
            "symbol":         self.symbol,
            "issue_type":     self.issue_type,
            "dataset":        self.dataset,
            "tier":           self.tier,
            "severity":       self.severity,
            "field":          self.field,
            "first_date":     self.first_date,
            "last_date":      self.last_date,
            "affected_rows":  self.affected_rows,
            "affected_ratio": self.affected_ratio,
            "detected_at":    self.detected_at,
            "source":         self.source,
            "status":         self.status,
            "repairability":  self.repairability,
            "reason":         self.reason,
            "evidence":       self.evidence,
            "research_only":  self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CoverageIssue":
        return cls(
            issue_id=d["issue_id"],
            symbol=d["symbol"],
            issue_type=d["issue_type"],
            dataset=d.get("dataset", "daily"),
            tier=d.get("tier"),
            severity=d.get("severity", SEVERITY_MEDIUM),
            field=d.get("field"),
            first_date=d.get("first_date"),
            last_date=d.get("last_date"),
            affected_rows=d.get("affected_rows", 0),
            affected_ratio=d.get("affected_ratio", 0.0),
            detected_at=d.get("detected_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            source=d.get("source"),
            status=d.get("status", STATUS_OPEN),
            repairability=d.get("repairability", REPAIRABILITY_MANUAL),
            reason=d.get("reason"),
            evidence=d.get("evidence"),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class CoverageRepairTask:
    """Represents a repair task derived from a CoverageIssue.

    [!] Research Only. No Real Orders.
    [!] dry_run=True default. destructive=False default.
    """
    task_id:          str
    issue_id:         str
    symbol:           str
    title:            str                   = ""
    action:           str                   = ACTION_REVIEW
    priority:         str                   = PRIORITY_P2
    dataset:          str                   = "daily"
    repair_mode:      str                   = REPAIR_MODE_DRY_RUN
    source_path:      Optional[str]         = None
    required_input:   Optional[str]         = None
    dry_run:          bool                  = True
    destructive:      bool                  = False
    status:           str                   = STATUS_OPEN
    blocked_reason:   Optional[str]         = None
    expected_effect:  Optional[str]         = None
    created_at:       str                   = dc_field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at:       str                   = dc_field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    research_only:    bool                  = True
    no_real_orders:   bool                  = True

    def to_dict(self) -> dict:
        return {
            "task_id":        self.task_id,
            "issue_id":       self.issue_id,
            "symbol":         self.symbol,
            "title":          self.title,
            "action":         self.action,
            "priority":       self.priority,
            "dataset":        self.dataset,
            "repair_mode":    self.repair_mode,
            "source_path":    self.source_path,
            "required_input": self.required_input,
            "dry_run":        self.dry_run,
            "destructive":    self.destructive,
            "status":         self.status,
            "blocked_reason": self.blocked_reason,
            "expected_effect": self.expected_effect,
            "created_at":     self.created_at,
            "updated_at":     self.updated_at,
            "research_only":  self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CoverageRepairTask":
        return cls(
            task_id=d["task_id"],
            issue_id=d["issue_id"],
            symbol=d["symbol"],
            title=d.get("title", ""),
            action=d.get("action", ACTION_REVIEW),
            priority=d.get("priority", PRIORITY_P2),
            dataset=d.get("dataset", "daily"),
            repair_mode=d.get("repair_mode", REPAIR_MODE_DRY_RUN),
            source_path=d.get("source_path"),
            required_input=d.get("required_input"),
            dry_run=d.get("dry_run", True),
            destructive=d.get("destructive", False),
            status=d.get("status", STATUS_OPEN),
            blocked_reason=d.get("blocked_reason"),
            expected_effect=d.get("expected_effect"),
            created_at=d.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            updated_at=d.get("updated_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class CoverageRepairPlan:
    """A complete repair plan across a set of symbols.

    [!] Research Only. No Real Orders.
    [!] dry_run=True default.
    """
    plan_id:                  str
    created_at:               str
    tasks:                    List[CoverageRepairTask] = dc_field(default_factory=list)
    tier:                     Optional[str]            = None
    symbols:                  List[str]               = dc_field(default_factory=list)
    open_count:               int                     = 0
    auto_safe_count:          int                     = 0
    manual_count:             int                     = 0
    blocked_count:            int                     = 0
    source_required_count:    int                     = 0
    destructive_count:        int                     = 0
    dry_run:                  bool                    = True
    expected_ready_gain:      int                     = 0
    expected_partial_reduction: int                   = 0
    research_only:            bool                    = True
    no_real_orders:           bool                    = True

    def to_dict(self) -> dict:
        return {
            "plan_id":                  self.plan_id,
            "created_at":               self.created_at,
            "tasks":                    [t.to_dict() for t in self.tasks],
            "tier":                     self.tier,
            "symbols":                  self.symbols,
            "open_count":               self.open_count,
            "auto_safe_count":          self.auto_safe_count,
            "manual_count":             self.manual_count,
            "blocked_count":            self.blocked_count,
            "source_required_count":    self.source_required_count,
            "destructive_count":        self.destructive_count,
            "dry_run":                  self.dry_run,
            "expected_ready_gain":      self.expected_ready_gain,
            "expected_partial_reduction": self.expected_partial_reduction,
            "research_only":            self.research_only,
            "no_real_orders":           self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CoverageRepairPlan":
        return cls(
            plan_id=d["plan_id"],
            created_at=d["created_at"],
            tasks=[CoverageRepairTask.from_dict(t) for t in d.get("tasks", [])],
            tier=d.get("tier"),
            symbols=d.get("symbols", []),
            open_count=d.get("open_count", 0),
            auto_safe_count=d.get("auto_safe_count", 0),
            manual_count=d.get("manual_count", 0),
            blocked_count=d.get("blocked_count", 0),
            source_required_count=d.get("source_required_count", 0),
            destructive_count=d.get("destructive_count", 0),
            dry_run=d.get("dry_run", True),
            expected_ready_gain=d.get("expected_ready_gain", 0),
            expected_partial_reduction=d.get("expected_partial_reduction", 0),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class CoverageRepairResult:
    """Result of executing a single repair task.

    [!] Research Only. No Real Orders.
    """
    result_id:            str
    plan_id:              str
    task_id:              str
    symbol:               str
    issue_type:           str                   = ""
    status:               str                   = RESULT_STATUS_DRY_RUN
    rows_before:          int                   = 0
    rows_after:           int                   = 0
    duplicates_removed:   int                   = 0
    metadata_normalized:  bool                  = False
    conflicts_remaining:  int                   = 0
    coverage_before:      Optional[str]         = None
    coverage_after:       Optional[str]         = None
    quality_before:       Optional[str]         = None
    quality_after:        Optional[str]         = None
    warning:              Optional[str]         = None
    error:                Optional[str]         = None
    executed_at:          str                   = dc_field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    dry_run:              bool                  = True

    def to_dict(self) -> dict:
        return {
            "result_id":           self.result_id,
            "plan_id":             self.plan_id,
            "task_id":             self.task_id,
            "symbol":              self.symbol,
            "issue_type":          self.issue_type,
            "status":              self.status,
            "rows_before":         self.rows_before,
            "rows_after":          self.rows_after,
            "duplicates_removed":  self.duplicates_removed,
            "metadata_normalized": self.metadata_normalized,
            "conflicts_remaining": self.conflicts_remaining,
            "coverage_before":     self.coverage_before,
            "coverage_after":      self.coverage_after,
            "quality_before":      self.quality_before,
            "quality_after":       self.quality_after,
            "warning":             self.warning,
            "error":               self.error,
            "executed_at":         self.executed_at,
            "dry_run":             self.dry_run,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CoverageRepairResult":
        return cls(
            result_id=d["result_id"],
            plan_id=d["plan_id"],
            task_id=d["task_id"],
            symbol=d["symbol"],
            issue_type=d.get("issue_type", ""),
            status=d.get("status", RESULT_STATUS_DRY_RUN),
            rows_before=d.get("rows_before", 0),
            rows_after=d.get("rows_after", 0),
            duplicates_removed=d.get("duplicates_removed", 0),
            metadata_normalized=d.get("metadata_normalized", False),
            conflicts_remaining=d.get("conflicts_remaining", 0),
            coverage_before=d.get("coverage_before"),
            coverage_after=d.get("coverage_after"),
            quality_before=d.get("quality_before"),
            quality_after=d.get("quality_after"),
            warning=d.get("warning"),
            error=d.get("error"),
            executed_at=d.get("executed_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            dry_run=d.get("dry_run", True),
        )


# ---------------------------------------------------------------------------
# Module-level safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS                   = True
DRY_RUN_DEFAULT                  = True
DESTRUCTIVE_REPAIR_DISABLED      = True
SYNTHETIC_PRICE_REPAIR_ENABLED   = False
EXTERNAL_DATA_DOWNLOAD_ENABLED   = False
CONFLICT_AUTO_OVERWRITE_ENABLED  = False
MOCK_DATA_FORMAL_CONCLUSION_ALLOWED = False
