"""
governance_rollup/rollup_schema.py — DataClasses for Data Governance Stable Rollup v1.1.9

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] All dry_run defaults=True. No auto repair / migration / execution.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

# ---------------------------------------------------------------------------
# Store type constants
# ---------------------------------------------------------------------------
STORE_TYPE_JSON      = "JSON"
STORE_TYPE_JSONL     = "JSONL"
STORE_TYPE_CSV       = "CSV"
STORE_TYPE_SQLITE    = "SQLITE"
STORE_TYPE_DIRECTORY = "DIRECTORY"
STORE_TYPE_MARKDOWN  = "MARKDOWN"
STORE_TYPE_OTHER     = "OTHER"

# ---------------------------------------------------------------------------
# Issue type constants
# ---------------------------------------------------------------------------
ISSUE_MISSING_INDEX           = "MISSING_INDEX"
ISSUE_STALE_INDEX             = "STALE_INDEX"
ISSUE_CORRUPTED_TAIL          = "CORRUPTED_TAIL"
ISSUE_MALFORMED_JSON          = "MALFORMED_JSON"
ISSUE_MALFORMED_JSONL_LINE    = "MALFORMED_JSONL_LINE"
ISSUE_MISSING_STATE_FILE      = "MISSING_STATE_FILE"
ISSUE_MISSING_DIRECTORY       = "MISSING_DIRECTORY"
ISSUE_PATH_NOT_PORTABLE       = "PATH_NOT_PORTABLE"
ISSUE_ABSOLUTE_PATH_STALE     = "ABSOLUTE_PATH_STALE"
ISSUE_SCHEMA_VERSION_MISMATCH = "SCHEMA_VERSION_MISMATCH"
ISSUE_DUPLICATE_INDEX_ENTRY   = "DUPLICATE_INDEX_ENTRY"
ISSUE_ORPHAN_ARTIFACT_REFERENCE = "ORPHAN_ARTIFACT_REFERENCE"
ISSUE_MISSING_ARTIFACT        = "MISSING_ARTIFACT"
ISSUE_UNKNOWN                 = "UNKNOWN"

# ---------------------------------------------------------------------------
# Proposed action constants
# ---------------------------------------------------------------------------
ACTION_REBUILD_INDEX               = "REBUILD_INDEX"
ACTION_REBUILD_STATE               = "REBUILD_STATE"
ACTION_TRUNCATE_CORRUPTED_TAIL_COPY = "TRUNCATE_CORRUPTED_TAIL_COPY"
ACTION_RESTORE_BACKUP              = "RESTORE_BACKUP"
ACTION_NORMALIZE_PATH              = "NORMALIZE_PATH"
ACTION_MIGRATE_SCHEMA              = "MIGRATE_SCHEMA"
ACTION_MARK_MISSING                = "MARK_MISSING"
ACTION_MANUAL_REVIEW               = "MANUAL_REVIEW"
ACTION_NO_ACTION                   = "NO_ACTION"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# ModuleConsistencyResult
# ---------------------------------------------------------------------------

@dataclass
class ModuleConsistencyResult:
    """Result of a consistency check for one governance module."""

    module_name:           str
    available:             bool
    schema_version:        str        = ""
    expected_version:      str        = ""
    import_status:         str        = "UNKNOWN"
    health_status:         str        = "UNKNOWN"
    store_status:          str        = "UNKNOWN"
    index_status:          str        = "UNKNOWN"
    audit_status:          str        = "UNKNOWN"
    path_status:           str        = "UNKNOWN"
    qualification_status:  str        = "UNKNOWN"
    safety_status:         str        = "UNKNOWN"
    warnings:              List[str]  = field(default_factory=list)
    errors:                List[str]  = field(default_factory=list)
    checked_at:            str        = field(default_factory=_now_iso)
    research_only:         bool       = True
    no_real_orders:        bool       = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module_name":          self.module_name,
            "available":            self.available,
            "schema_version":       self.schema_version,
            "expected_version":     self.expected_version,
            "import_status":        self.import_status,
            "health_status":        self.health_status,
            "store_status":         self.store_status,
            "index_status":         self.index_status,
            "audit_status":         self.audit_status,
            "path_status":          self.path_status,
            "qualification_status": self.qualification_status,
            "safety_status":        self.safety_status,
            "warnings":             list(self.warnings),
            "errors":               list(self.errors),
            "checked_at":           self.checked_at,
            "research_only":        self.research_only,
            "no_real_orders":       self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ModuleConsistencyResult":
        return cls(
            module_name=d.get("module_name", ""),
            available=bool(d.get("available", False)),
            schema_version=d.get("schema_version", ""),
            expected_version=d.get("expected_version", ""),
            import_status=d.get("import_status", "UNKNOWN"),
            health_status=d.get("health_status", "UNKNOWN"),
            store_status=d.get("store_status", "UNKNOWN"),
            index_status=d.get("index_status", "UNKNOWN"),
            audit_status=d.get("audit_status", "UNKNOWN"),
            path_status=d.get("path_status", "UNKNOWN"),
            qualification_status=d.get("qualification_status", "UNKNOWN"),
            safety_status=d.get("safety_status", "UNKNOWN"),
            warnings=list(d.get("warnings", [])),
            errors=list(d.get("errors", [])),
            checked_at=d.get("checked_at", _now_iso()),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


# ---------------------------------------------------------------------------
# StoreInventoryRecord
# ---------------------------------------------------------------------------

@dataclass
class StoreInventoryRecord:
    """Inventory record for one governance store file/directory."""

    store_id:             str
    module_name:          str
    store_type:           str       = STORE_TYPE_OTHER
    path:                 str       = ""
    relative_path:        str       = ""
    exists:               bool      = False
    readable:             bool      = False
    writable:             bool      = False
    size_bytes:           int       = 0
    record_count:         int       = 0
    last_modified:        str       = ""
    append_only:          bool      = False
    index_available:      bool      = False
    backup_available:     bool      = False
    corruption_detected:  bool      = False
    corrupted_tail_detected: bool   = False
    checksum:             str       = ""
    status:               str       = "UNKNOWN"
    reason:               str       = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "store_id":               self.store_id,
            "module_name":            self.module_name,
            "store_type":             self.store_type,
            "path":                   self.path,
            "relative_path":          self.relative_path,
            "exists":                 self.exists,
            "readable":               self.readable,
            "writable":               self.writable,
            "size_bytes":             self.size_bytes,
            "record_count":           self.record_count,
            "last_modified":          self.last_modified,
            "append_only":            self.append_only,
            "index_available":        self.index_available,
            "backup_available":       self.backup_available,
            "corruption_detected":    self.corruption_detected,
            "corrupted_tail_detected": self.corrupted_tail_detected,
            "checksum":               self.checksum,
            "status":                 self.status,
            "reason":                 self.reason,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "StoreInventoryRecord":
        return cls(
            store_id=d.get("store_id", ""),
            module_name=d.get("module_name", ""),
            store_type=d.get("store_type", STORE_TYPE_OTHER),
            path=d.get("path", ""),
            relative_path=d.get("relative_path", ""),
            exists=bool(d.get("exists", False)),
            readable=bool(d.get("readable", False)),
            writable=bool(d.get("writable", False)),
            size_bytes=int(d.get("size_bytes", 0)),
            record_count=int(d.get("record_count", 0)),
            last_modified=d.get("last_modified", ""),
            append_only=bool(d.get("append_only", False)),
            index_available=bool(d.get("index_available", False)),
            backup_available=bool(d.get("backup_available", False)),
            corruption_detected=bool(d.get("corruption_detected", False)),
            corrupted_tail_detected=bool(d.get("corrupted_tail_detected", False)),
            checksum=d.get("checksum", ""),
            status=d.get("status", "UNKNOWN"),
            reason=d.get("reason", ""),
        )


# ---------------------------------------------------------------------------
# RecoveryPlan
# ---------------------------------------------------------------------------

@dataclass
class RecoveryPlan:
    """Recovery plan for a problematic governance store."""

    plan_id:               str
    store_id:              str
    module_name:           str
    issue_type:            str       = ISSUE_UNKNOWN
    current_path:          str       = ""
    backup_path:           str       = ""
    proposed_action:       str       = ACTION_MANUAL_REVIEW
    destructive:           bool      = False
    dry_run:               bool      = True
    requires_allow_write:  bool      = True
    estimated_record_loss: int       = 0
    safe:                  bool      = True
    status:                str       = "PENDING"
    reason:                str       = ""
    created_at:            str       = field(default_factory=_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id":               self.plan_id,
            "store_id":              self.store_id,
            "module_name":           self.module_name,
            "issue_type":            self.issue_type,
            "current_path":          self.current_path,
            "backup_path":           self.backup_path,
            "proposed_action":       self.proposed_action,
            "destructive":           self.destructive,
            "dry_run":               self.dry_run,
            "requires_allow_write":  self.requires_allow_write,
            "estimated_record_loss": self.estimated_record_loss,
            "safe":                  self.safe,
            "status":                self.status,
            "reason":                self.reason,
            "created_at":            self.created_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RecoveryPlan":
        return cls(
            plan_id=d.get("plan_id", ""),
            store_id=d.get("store_id", ""),
            module_name=d.get("module_name", ""),
            issue_type=d.get("issue_type", ISSUE_UNKNOWN),
            current_path=d.get("current_path", ""),
            backup_path=d.get("backup_path", ""),
            proposed_action=d.get("proposed_action", ACTION_MANUAL_REVIEW),
            destructive=bool(d.get("destructive", False)),
            dry_run=bool(d.get("dry_run", True)),
            requires_allow_write=bool(d.get("requires_allow_write", True)),
            estimated_record_loss=int(d.get("estimated_record_loss", 0)),
            safe=bool(d.get("safe", True)),
            status=d.get("status", "PENDING"),
            reason=d.get("reason", ""),
            created_at=d.get("created_at", _now_iso()),
        )


# ---------------------------------------------------------------------------
# CrossModuleConsistencySummary
# ---------------------------------------------------------------------------

@dataclass
class CrossModuleConsistencySummary:
    """Summary of cross-module consistency check results."""

    generated_at:             str       = field(default_factory=_now_iso)
    modules_checked:          int       = 0
    modules_pass:             int       = 0
    modules_warn:             int       = 0
    modules_fail:             int       = 0
    stores_checked:           int       = 0
    stores_valid:             int       = 0
    stores_warn:              int       = 0
    stores_fail:              int       = 0
    audit_chains_valid:       int       = 0
    audit_chains_failed:      int       = 0
    indexes_valid:            int       = 0
    indexes_stale:            int       = 0
    path_issues:              int       = 0
    schema_mismatches:        int       = 0
    qualification_mismatches: int       = 0
    safety_mismatches:        int       = 0
    overall_status:           str       = "UNKNOWN"
    research_only:            bool      = True
    no_real_orders:           bool      = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "generated_at":             self.generated_at,
            "modules_checked":          self.modules_checked,
            "modules_pass":             self.modules_pass,
            "modules_warn":             self.modules_warn,
            "modules_fail":             self.modules_fail,
            "stores_checked":           self.stores_checked,
            "stores_valid":             self.stores_valid,
            "stores_warn":              self.stores_warn,
            "stores_fail":              self.stores_fail,
            "audit_chains_valid":       self.audit_chains_valid,
            "audit_chains_failed":      self.audit_chains_failed,
            "indexes_valid":            self.indexes_valid,
            "indexes_stale":            self.indexes_stale,
            "path_issues":              self.path_issues,
            "schema_mismatches":        self.schema_mismatches,
            "qualification_mismatches": self.qualification_mismatches,
            "safety_mismatches":        self.safety_mismatches,
            "overall_status":           self.overall_status,
            "research_only":            self.research_only,
            "no_real_orders":           self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CrossModuleConsistencySummary":
        return cls(
            generated_at=d.get("generated_at", _now_iso()),
            modules_checked=int(d.get("modules_checked", 0)),
            modules_pass=int(d.get("modules_pass", 0)),
            modules_warn=int(d.get("modules_warn", 0)),
            modules_fail=int(d.get("modules_fail", 0)),
            stores_checked=int(d.get("stores_checked", 0)),
            stores_valid=int(d.get("stores_valid", 0)),
            stores_warn=int(d.get("stores_warn", 0)),
            stores_fail=int(d.get("stores_fail", 0)),
            audit_chains_valid=int(d.get("audit_chains_valid", 0)),
            audit_chains_failed=int(d.get("audit_chains_failed", 0)),
            indexes_valid=int(d.get("indexes_valid", 0)),
            indexes_stale=int(d.get("indexes_stale", 0)),
            path_issues=int(d.get("path_issues", 0)),
            schema_mismatches=int(d.get("schema_mismatches", 0)),
            qualification_mismatches=int(d.get("qualification_mismatches", 0)),
            safety_mismatches=int(d.get("safety_mismatches", 0)),
            overall_status=d.get("overall_status", "UNKNOWN"),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


# ---------------------------------------------------------------------------
# StableRollupSummary
# ---------------------------------------------------------------------------

@dataclass
class StableRollupSummary:
    """Top-level summary for the Data Governance Stable Rollup."""

    version:             str        = "1.1.9"
    release_name:        str        = "Data Governance Stable Rollup"
    generated_at:        str        = field(default_factory=_now_iso)
    overall_status:      str        = "UNKNOWN"
    health_summary:      Dict[str, Any] = field(default_factory=dict)
    consistency_summary: Dict[str, Any] = field(default_factory=dict)
    migration_summary:   Dict[str, Any] = field(default_factory=dict)
    recovery_summary:    Dict[str, Any] = field(default_factory=dict)
    regression_summary:  Dict[str, Any] = field(default_factory=dict)
    gui_summary:         Dict[str, Any] = field(default_factory=dict)
    cli_summary:         Dict[str, Any] = field(default_factory=dict)
    docs_summary:        Dict[str, Any] = field(default_factory=dict)
    safety_summary:      Dict[str, Any] = field(default_factory=dict)
    known_warnings:      List[str]   = field(default_factory=list)
    blocking_issues:     List[str]   = field(default_factory=list)
    stable_ready:        bool        = False
    research_only:       bool        = True
    no_real_orders:      bool        = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version":             self.version,
            "release_name":        self.release_name,
            "generated_at":        self.generated_at,
            "overall_status":      self.overall_status,
            "health_summary":      dict(self.health_summary),
            "consistency_summary": dict(self.consistency_summary),
            "migration_summary":   dict(self.migration_summary),
            "recovery_summary":    dict(self.recovery_summary),
            "regression_summary":  dict(self.regression_summary),
            "gui_summary":         dict(self.gui_summary),
            "cli_summary":         dict(self.cli_summary),
            "docs_summary":        dict(self.docs_summary),
            "safety_summary":      dict(self.safety_summary),
            "known_warnings":      list(self.known_warnings),
            "blocking_issues":     list(self.blocking_issues),
            "stable_ready":        self.stable_ready,
            "research_only":       self.research_only,
            "no_real_orders":      self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "StableRollupSummary":
        return cls(
            version=d.get("version", "1.1.9"),
            release_name=d.get("release_name", "Data Governance Stable Rollup"),
            generated_at=d.get("generated_at", _now_iso()),
            overall_status=d.get("overall_status", "UNKNOWN"),
            health_summary=dict(d.get("health_summary", {})),
            consistency_summary=dict(d.get("consistency_summary", {})),
            migration_summary=dict(d.get("migration_summary", {})),
            recovery_summary=dict(d.get("recovery_summary", {})),
            regression_summary=dict(d.get("regression_summary", {})),
            gui_summary=dict(d.get("gui_summary", {})),
            cli_summary=dict(d.get("cli_summary", {})),
            docs_summary=dict(d.get("docs_summary", {})),
            safety_summary=dict(d.get("safety_summary", {})),
            known_warnings=list(d.get("known_warnings", [])),
            blocking_issues=list(d.get("blocking_issues", [])),
            stable_ready=bool(d.get("stable_ready", False)),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )
