"""report_pack/report_pack_schema.py — ReportPackItem / ReportPack schema.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
STATUS_READY   = "READY"
STATUS_PARTIAL = "PARTIAL"
STATUS_MISSING = "MISSING"
STATUS_FAILED  = "FAILED"
STATUS_SKIPPED = "SKIPPED"

# ---------------------------------------------------------------------------
# Pack type constants
# ---------------------------------------------------------------------------
PACK_DAILY   = "daily"
PACK_WEEKLY  = "weekly"
PACK_FULL    = "full"
PACK_CUSTOM  = "custom"

# ---------------------------------------------------------------------------
# Report type constants (20 types)
# ---------------------------------------------------------------------------
REPORT_DAILY_MARKET      = "daily_market"
REPORT_AUTO_REPORT       = "auto_report"
REPORT_DATA_QUALITY      = "data_quality"
REPORT_PROVIDER          = "provider"
REPORT_STRATEGY_FILTER   = "strategy_filter"
REPORT_SIGNAL_QUALITY    = "signal_quality"
REPORT_RULE_GOVERNANCE   = "rule_governance"
REPORT_PORTFOLIO_JOURNAL = "portfolio_journal"
REPORT_RESEARCH_REVIEW   = "research_review"
REPORT_RESEARCH_COACH    = "research_coach"
REPORT_RESEARCH_WORKFLOW = "research_workflow"
REPORT_RESEARCH_OS       = "research_os"
REPORT_REGRESSION        = "regression"
REPORT_CLI_UX            = "cli_ux"
REPORT_GUI_NAVIGATION    = "gui_navigation"
REPORT_NOTIFICATION      = "notification"
REPORT_INTRADAY_REPLAY   = "intraday_replay"
REPORT_EXPERIMENT        = "experiment"
REPORT_RELEASE           = "release"
REPORT_SAFETY            = "safety"

ALL_REPORT_TYPES = [
    REPORT_DAILY_MARKET, REPORT_AUTO_REPORT, REPORT_DATA_QUALITY,
    REPORT_PROVIDER, REPORT_STRATEGY_FILTER, REPORT_SIGNAL_QUALITY,
    REPORT_RULE_GOVERNANCE, REPORT_PORTFOLIO_JOURNAL, REPORT_RESEARCH_REVIEW,
    REPORT_RESEARCH_COACH, REPORT_RESEARCH_WORKFLOW, REPORT_RESEARCH_OS,
    REPORT_REGRESSION, REPORT_CLI_UX, REPORT_GUI_NAVIGATION,
    REPORT_NOTIFICATION, REPORT_INTRADAY_REPLAY, REPORT_EXPERIMENT,
    REPORT_RELEASE, REPORT_SAFETY,
]


@dataclass
class ReportPackItem:
    """A single report entry in a ReportPack manifest.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    report_type:   str
    status:        str = STATUS_MISSING
    path:          str = ""
    report_date:   str = ""
    size_bytes:    int = 0
    error:         str = ""
    generated_at:  str = ""
    link:          str = ""
    notes:         str = ""

    # Safety invariants — always True, never modified
    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return {
            "report_type":      self.report_type,
            "status":           self.status,
            "path":             self.path,
            "report_date":      self.report_date,
            "size_bytes":       self.size_bytes,
            "error":            self.error,
            "generated_at":     self.generated_at,
            "link":             self.link,
            "notes":            self.notes,
            "read_only":        self.read_only,
            "no_real_orders":   self.no_real_orders,
            "production_blocked": self.production_blocked,
        }


@dataclass
class ReportPack:
    """A consolidated report pack for a given date and pack type.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    pack_type:    str
    report_date:  str
    status:       str = STATUS_MISSING
    items:        List[ReportPackItem] = field(default_factory=list)
    output_dir:   str = ""
    index_path:   str = ""
    manifest_path: str = ""
    health_score: float = 0.0
    generated_at: str = ""
    notes:        str = ""

    # Safety invariants — always True, never modified
    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return {
            "pack_type":      self.pack_type,
            "report_date":    self.report_date,
            "status":         self.status,
            "items":          [i.to_dict() for i in self.items],
            "output_dir":     self.output_dir,
            "index_path":     self.index_path,
            "manifest_path":  self.manifest_path,
            "health_score":   self.health_score,
            "ready_count":    self.ready_count,
            "missing_count":  self.missing_count,
            "failed_count":   self.failed_count,
            "generated_at":   self.generated_at,
            "notes":          self.notes,
            "read_only":      self.read_only,
            "no_real_orders": self.no_real_orders,
            "production_blocked": self.production_blocked,
        }

    @property
    def ready_count(self) -> int:
        return sum(1 for i in self.items if i.status == STATUS_READY)

    @property
    def missing_count(self) -> int:
        return sum(1 for i in self.items if i.status == STATUS_MISSING)

    @property
    def failed_count(self) -> int:
        return sum(1 for i in self.items if i.status == STATUS_FAILED)
