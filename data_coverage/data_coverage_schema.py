"""
data_coverage/data_coverage_schema.py — DataCoverageItem and DataCoverageSummary schema.

[!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
STATUS_READY            = "READY"
STATUS_PARTIAL          = "PARTIAL"
STATUS_MISSING_REQUIRED = "MISSING_REQUIRED"
STATUS_MISSING_OPTIONAL = "MISSING_OPTIONAL"
STATUS_ENV_LIMITED      = "ENV_LIMITED"
STATUS_NOT_GENERATED    = "NOT_GENERATED"
STATUS_STALE            = "STALE"
STATUS_FAILED           = "FAILED"
STATUS_UNKNOWN          = "UNKNOWN"

# ---------------------------------------------------------------------------
# Domain constants
# ---------------------------------------------------------------------------
DOMAIN_PROVIDER         = "provider"
DOMAIN_DAILY_DATA       = "daily_data"
DOMAIN_INTRADAY         = "intraday"
DOMAIN_FINANCIAL        = "financial"
DOMAIN_CHIP             = "chip"
DOMAIN_FEATURE_STORE    = "feature_store"
DOMAIN_REPLAY           = "replay"
DOMAIN_EXPERIMENT       = "experiment"
DOMAIN_RULE_GOVERNANCE  = "rule_governance"
DOMAIN_REPORT_PACK      = "report_pack"
DOMAIN_REGRESSION       = "regression"
DOMAIN_STABLE_RELEASE   = "stable_release"

# Report type constant for report_pack integration
REPORT_DATA_COVERAGE    = "data_coverage"


class DataCoverageItem:
    """A single data coverage entry.

    [!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        item_id: str,
        domain: str,
        dataset_name: str,
        source_module: str = "",
        source_provider: str = "",
        expected_path: str = "",
        actual_path: str = "",
        status: str = STATUS_UNKNOWN,
        required: bool = True,
        environment_limited: bool = False,
        not_generated: bool = False,
        rows: Optional[int] = None,
        columns: Optional[int] = None,
        last_updated: str = "",
        freshness_status: str = "",
        coverage_score: float = 0.0,
        missing_reason: str = "",
        suggested_command: str = "",
        warning: str = "",
    ):
        self.item_id             = item_id
        self.domain              = domain
        self.dataset_name        = dataset_name
        self.source_module       = source_module
        self.source_provider     = source_provider
        self.expected_path       = expected_path
        self.actual_path         = actual_path
        self.status              = status
        self.required            = required
        self.environment_limited = environment_limited
        self.not_generated       = not_generated
        self.rows                = rows
        self.columns             = columns
        self.last_updated        = last_updated
        self.freshness_status    = freshness_status
        self.coverage_score      = coverage_score
        self.missing_reason      = missing_reason
        self.suggested_command   = suggested_command
        self.warning             = warning
        self.read_only           = True
        self.no_real_orders      = True
        self.production_blocked  = True

    def to_dict(self) -> dict:
        return {
            "item_id":             self.item_id,
            "domain":              self.domain,
            "dataset_name":        self.dataset_name,
            "source_module":       self.source_module,
            "source_provider":     self.source_provider,
            "expected_path":       self.expected_path,
            "actual_path":         self.actual_path,
            "status":              self.status,
            "required":            self.required,
            "environment_limited": self.environment_limited,
            "not_generated":       self.not_generated,
            "rows":                self.rows,
            "columns":             self.columns,
            "last_updated":        self.last_updated,
            "freshness_status":    self.freshness_status,
            "coverage_score":      self.coverage_score,
            "missing_reason":      self.missing_reason,
            "suggested_command":   self.suggested_command,
            "warning":             self.warning,
            "read_only":           self.read_only,
            "no_real_orders":      self.no_real_orders,
            "production_blocked":  self.production_blocked,
        }


class DataCoverageSummary:
    """Summary of a full data coverage scan.

    [!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        generated_at: str = "",
        mode: str = "real",
        total_items: int = 0,
        ready_count: int = 0,
        partial_count: int = 0,
        env_limited_count: int = 0,
        not_generated_count: int = 0,
        missing_required_count: int = 0,
        missing_optional_count: int = 0,
        stale_count: int = 0,
        failed_count: int = 0,
        coverage_score: float = 0.0,
        overall_status: str = STATUS_UNKNOWN,
        blockers: Optional[List[str]] = None,
        warnings: Optional[List[str]] = None,
    ):
        self.generated_at           = generated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mode                   = mode
        self.total_items            = total_items
        self.ready_count            = ready_count
        self.partial_count          = partial_count
        self.env_limited_count      = env_limited_count
        self.not_generated_count    = not_generated_count
        self.missing_required_count = missing_required_count
        self.missing_optional_count = missing_optional_count
        self.stale_count            = stale_count
        self.failed_count           = failed_count
        self.coverage_score         = coverage_score
        self.overall_status         = overall_status
        self.blockers               = blockers or []
        self.warnings               = warnings or []
        self.no_real_orders         = True
        self.production_blocked     = True

    def to_dict(self) -> dict:
        return {
            "generated_at":           self.generated_at,
            "mode":                   self.mode,
            "total_items":            self.total_items,
            "ready_count":            self.ready_count,
            "partial_count":          self.partial_count,
            "env_limited_count":      self.env_limited_count,
            "not_generated_count":    self.not_generated_count,
            "missing_required_count": self.missing_required_count,
            "missing_optional_count": self.missing_optional_count,
            "stale_count":            self.stale_count,
            "failed_count":           self.failed_count,
            "coverage_score":         self.coverage_score,
            "overall_status":         self.overall_status,
            "blockers":               self.blockers,
            "warnings":               self.warnings,
            "no_real_orders":         self.no_real_orders,
            "production_blocked":     self.production_blocked,
        }
