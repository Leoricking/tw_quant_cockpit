"""
coverage_repair/coverage_repair_schema.py — Coverage Repair dataclasses for TW Quant Cockpit v1.1.2.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] dry_run=True by default. Destructive repair disabled.
[!] Synthetic OHLC repair DISABLED. Invalid OHLC not auto-modified.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# ---------------------------------------------------------------------------
# Issue type constants
# ---------------------------------------------------------------------------
ISSUE_MISSING      = "MISSING"       # No data at all for symbol/dataset
ISSUE_INSUFFICIENT = "INSUFFICIENT"  # Too few rows (below minimum threshold)
ISSUE_PARTIAL      = "PARTIAL"       # Some rows but below READY threshold
ISSUE_STALE        = "STALE"         # Data exists but not recent enough
ISSUE_DUPLICATE    = "DUPLICATE"     # Identical duplicate date rows
ISSUE_CONFLICT     = "CONFLICT"      # Same date, different OHLCV values
ISSUE_INVALID      = "INVALID"       # Invalid OHLC (e.g. high < low, close <= 0)

VALID_ISSUE_TYPES = [
    ISSUE_MISSING,
    ISSUE_INSUFFICIENT,
    ISSUE_PARTIAL,
    ISSUE_STALE,
    ISSUE_DUPLICATE,
    ISSUE_CONFLICT,
    ISSUE_INVALID,
]

# ---------------------------------------------------------------------------
# Repair action constants
# ---------------------------------------------------------------------------
ACTION_AUTO_SAFE       = "AUTO_SAFE"       # Safe to execute automatically
ACTION_MANUAL_REVIEW   = "MANUAL_REVIEW"   # Requires human review before repair
ACTION_SOURCE_REQUIRED = "SOURCE_REQUIRED" # External source data needed
ACTION_BLOCKED         = "BLOCKED"         # Cannot repair; must not auto-modify

VALID_REPAIR_ACTIONS = [
    ACTION_AUTO_SAFE,
    ACTION_MANUAL_REVIEW,
    ACTION_SOURCE_REQUIRED,
    ACTION_BLOCKED,
]

# ---------------------------------------------------------------------------
# Priority constants
# ---------------------------------------------------------------------------
PRIORITY_P0 = "P0"   # Critical: no data / full outage
PRIORITY_P1 = "P1"   # High: conflicts, invalid
PRIORITY_P2 = "P2"   # Medium: insufficient, partial, stale
PRIORITY_P3 = "P3"   # Low: identical duplicates

VALID_PRIORITIES = [PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3]

# ---------------------------------------------------------------------------
# Repair result status constants
# ---------------------------------------------------------------------------
REPAIR_STATUS_OK          = "OK"
REPAIR_STATUS_DRY_RUN     = "DRY_RUN"
REPAIR_STATUS_SKIPPED     = "SKIPPED"
REPAIR_STATUS_BLOCKED     = "BLOCKED"
REPAIR_STATUS_MANUAL      = "MANUAL"
REPAIR_STATUS_FAILED      = "FAILED"
REPAIR_STATUS_PARTIAL     = "PARTIAL"

# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------
NO_REAL_ORDERS                    = True
BROKER_DISABLED                   = True
DRY_RUN_DEFAULT                   = True
DESTRUCTIVE_REPAIR_DISABLED       = True
SYNTHETIC_OHLC_REPAIR_DISABLED    = True
INVALID_OHLC_AUTO_MODIFY_DISABLED = True


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class CoverageIssue:
    """A single coverage problem detected for a symbol/dataset."""
    issue_id: str
    symbol: str
    dataset: str
    issue_type: str          # MISSING / INSUFFICIENT / PARTIAL / STALE / DUPLICATE / CONFLICT / INVALID
    description: str
    row_count: int
    affected_dates: List[str] = field(default_factory=list)
    expected_min_rows: int = 0
    last_date: Optional[str] = None
    details: Dict[str, object] = field(default_factory=dict)
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "issue_id":         self.issue_id,
            "symbol":           self.symbol,
            "dataset":          self.dataset,
            "issue_type":       self.issue_type,
            "description":      self.description,
            "row_count":        self.row_count,
            "affected_dates":   self.affected_dates,
            "expected_min_rows": self.expected_min_rows,
            "last_date":        self.last_date,
            "details":          self.details,
            "research_only":    self.research_only,
            "no_real_orders":   self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CoverageIssue":
        return cls(
            issue_id=d.get("issue_id", ""),
            symbol=d.get("symbol", ""),
            dataset=d.get("dataset", "daily"),
            issue_type=d.get("issue_type", ISSUE_MISSING),
            description=d.get("description", ""),
            row_count=d.get("row_count", 0),
            affected_dates=d.get("affected_dates", []),
            expected_min_rows=d.get("expected_min_rows", 0),
            last_date=d.get("last_date"),
            details=d.get("details", {}),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class CoverageRepairTask:
    """A single repair task derived from a CoverageIssue."""
    task_id: str
    issue_id: str
    symbol: str
    dataset: str
    issue_type: str
    action: str          # AUTO_SAFE / MANUAL_REVIEW / SOURCE_REQUIRED / BLOCKED
    priority: str        # P0 / P1 / P2 / P3
    description: str
    dry_run: bool = True
    destructive: bool = False
    blocked_reason: Optional[str] = None
    affected_dates: List[str] = field(default_factory=list)
    before_row_count: int = 0
    estimated_after_row_count: int = 0
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "task_id":                   self.task_id,
            "issue_id":                  self.issue_id,
            "symbol":                    self.symbol,
            "dataset":                   self.dataset,
            "issue_type":                self.issue_type,
            "action":                    self.action,
            "priority":                  self.priority,
            "description":               self.description,
            "dry_run":                   self.dry_run,
            "destructive":               self.destructive,
            "blocked_reason":            self.blocked_reason,
            "affected_dates":            self.affected_dates,
            "before_row_count":          self.before_row_count,
            "estimated_after_row_count": self.estimated_after_row_count,
            "research_only":             self.research_only,
            "no_real_orders":            self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CoverageRepairTask":
        return cls(
            task_id=d.get("task_id", ""),
            issue_id=d.get("issue_id", ""),
            symbol=d.get("symbol", ""),
            dataset=d.get("dataset", "daily"),
            issue_type=d.get("issue_type", ISSUE_MISSING),
            action=d.get("action", ACTION_BLOCKED),
            priority=d.get("priority", PRIORITY_P2),
            description=d.get("description", ""),
            dry_run=d.get("dry_run", True),
            destructive=d.get("destructive", False),
            blocked_reason=d.get("blocked_reason"),
            affected_dates=d.get("affected_dates", []),
            before_row_count=d.get("before_row_count", 0),
            estimated_after_row_count=d.get("estimated_after_row_count", 0),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class RepairPlan:
    """Full repair plan for a batch of coverage issues."""
    plan_id: str
    created_at: str
    total_issues: int
    total_tasks: int
    p0_count: int
    p1_count: int
    p2_count: int
    p3_count: int
    auto_safe_count: int
    manual_review_count: int
    source_required_count: int
    blocked_count: int
    tasks: List[CoverageRepairTask] = field(default_factory=list)
    dry_run: bool = True
    destructive_disabled: bool = True
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "plan_id":               self.plan_id,
            "created_at":            self.created_at,
            "total_issues":          self.total_issues,
            "total_tasks":           self.total_tasks,
            "p0_count":              self.p0_count,
            "p1_count":              self.p1_count,
            "p2_count":              self.p2_count,
            "p3_count":              self.p3_count,
            "auto_safe_count":       self.auto_safe_count,
            "manual_review_count":   self.manual_review_count,
            "source_required_count": self.source_required_count,
            "blocked_count":         self.blocked_count,
            "tasks":                 [t.to_dict() for t in self.tasks],
            "dry_run":               self.dry_run,
            "destructive_disabled":  self.destructive_disabled,
            "research_only":         self.research_only,
            "no_real_orders":        self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RepairPlan":
        tasks = [CoverageRepairTask.from_dict(t) for t in d.get("tasks", [])]
        return cls(
            plan_id=d.get("plan_id", ""),
            created_at=d.get("created_at", ""),
            total_issues=d.get("total_issues", 0),
            total_tasks=d.get("total_tasks", 0),
            p0_count=d.get("p0_count", 0),
            p1_count=d.get("p1_count", 0),
            p2_count=d.get("p2_count", 0),
            p3_count=d.get("p3_count", 0),
            auto_safe_count=d.get("auto_safe_count", 0),
            manual_review_count=d.get("manual_review_count", 0),
            source_required_count=d.get("source_required_count", 0),
            blocked_count=d.get("blocked_count", 0),
            tasks=tasks,
            dry_run=d.get("dry_run", True),
            destructive_disabled=d.get("destructive_disabled", True),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class RepairResult:
    """Result of executing a single CoverageRepairTask."""
    result_id: str
    task_id: str
    plan_id: str
    symbol: str
    dataset: str
    issue_type: str
    action: str
    status: str          # OK / DRY_RUN / SKIPPED / BLOCKED / MANUAL / FAILED / PARTIAL
    rows_before: int
    rows_after: int
    rows_removed: int
    dry_run: bool = True
    blocked_reason: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    executed_at: Optional[str] = None
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "result_id":      self.result_id,
            "task_id":        self.task_id,
            "plan_id":        self.plan_id,
            "symbol":         self.symbol,
            "dataset":        self.dataset,
            "issue_type":     self.issue_type,
            "action":         self.action,
            "status":         self.status,
            "rows_before":    self.rows_before,
            "rows_after":     self.rows_after,
            "rows_removed":   self.rows_removed,
            "dry_run":        self.dry_run,
            "blocked_reason": self.blocked_reason,
            "warnings":       self.warnings,
            "errors":         self.errors,
            "executed_at":    self.executed_at,
            "research_only":  self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RepairResult":
        return cls(
            result_id=d.get("result_id", ""),
            task_id=d.get("task_id", ""),
            plan_id=d.get("plan_id", ""),
            symbol=d.get("symbol", ""),
            dataset=d.get("dataset", "daily"),
            issue_type=d.get("issue_type", ISSUE_MISSING),
            action=d.get("action", ACTION_BLOCKED),
            status=d.get("status", REPAIR_STATUS_FAILED),
            rows_before=d.get("rows_before", 0),
            rows_after=d.get("rows_after", 0),
            rows_removed=d.get("rows_removed", 0),
            dry_run=d.get("dry_run", True),
            blocked_reason=d.get("blocked_reason"),
            warnings=d.get("warnings", []),
            errors=d.get("errors", []),
            executed_at=d.get("executed_at"),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class RepairSummary:
    """Summary of a batch repair session."""
    summary_id: str
    plan_id: str
    created_at: str
    total_tasks: int
    succeeded: int
    partial: int
    failed: int
    skipped: int
    blocked: int
    manual_review: int
    dry_run: bool = True
    results: List[RepairResult] = field(default_factory=list)
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "summary_id":    self.summary_id,
            "plan_id":       self.plan_id,
            "created_at":    self.created_at,
            "total_tasks":   self.total_tasks,
            "succeeded":     self.succeeded,
            "partial":       self.partial,
            "failed":        self.failed,
            "skipped":       self.skipped,
            "blocked":       self.blocked,
            "manual_review": self.manual_review,
            "dry_run":       self.dry_run,
            "results":       [r.to_dict() for r in self.results],
            "research_only":  self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RepairSummary":
        results = [RepairResult.from_dict(r) for r in d.get("results", [])]
        return cls(
            summary_id=d.get("summary_id", ""),
            plan_id=d.get("plan_id", ""),
            created_at=d.get("created_at", ""),
            total_tasks=d.get("total_tasks", 0),
            succeeded=d.get("succeeded", 0),
            partial=d.get("partial", 0),
            failed=d.get("failed", 0),
            skipped=d.get("skipped", 0),
            blocked=d.get("blocked", 0),
            manual_review=d.get("manual_review", 0),
            dry_run=d.get("dry_run", True),
            results=results,
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )


@dataclass
class RepairRetryManifest:
    """Manifest of repair tasks that failed and need retry."""
    manifest_id: str
    created_at: str
    plan_id: str
    failed_tasks: List[str] = field(default_factory=list)
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
            "plan_id":        self.plan_id,
            "failed_tasks":   self.failed_tasks,
            "failed_symbols": self.failed_symbols,
            "retry_count":    self.retry_count,
            "last_retry_at":  self.last_retry_at,
            "resolved":       self.resolved,
            "research_only":  self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RepairRetryManifest":
        return cls(
            manifest_id=d.get("manifest_id", ""),
            created_at=d.get("created_at", ""),
            plan_id=d.get("plan_id", ""),
            failed_tasks=d.get("failed_tasks", []),
            failed_symbols=d.get("failed_symbols", []),
            retry_count=d.get("retry_count", 0),
            last_retry_at=d.get("last_retry_at"),
            resolved=d.get("resolved", False),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
        )
