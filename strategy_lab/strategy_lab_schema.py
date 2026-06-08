"""
strategy_lab/strategy_lab_schema.py — Strategy Lab Stable schema v0.9.0

Dataclass schema for Strategy Lab Stable validation.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------
CAT_RESEARCH_INTELLIGENCE = "research_intelligence"
CAT_STRATEGY_MEMORY       = "strategy_memory"
CAT_BACKTEST_COACH        = "backtest_coach"
CAT_TRAINING_METRICS      = "training_metrics"
CAT_EVIDENCE_GRAPH        = "evidence_graph"
CAT_REPLAY_TRAINING       = "replay_training"
CAT_DATA_COVERAGE         = "data_coverage"
CAT_REPORT_PACK           = "report_pack"
CAT_REGRESSION            = "regression"
CAT_STABLE_RELEASE        = "stable_release"
CAT_SAFETY                = "safety"

# ---------------------------------------------------------------------------
# Stable statuses
# ---------------------------------------------------------------------------
STABLE_STATUS_STABLE  = "STABLE"
STABLE_STATUS_USABLE  = "USABLE"
STABLE_STATUS_PARTIAL = "PARTIAL"
STABLE_STATUS_WARNING = "WARNING"
STABLE_STATUS_BLOCKED = "BLOCKED"

# ---------------------------------------------------------------------------
# Check statuses
# ---------------------------------------------------------------------------
CHECK_PASS    = "PASS"
CHECK_WARN    = "WARN"
CHECK_FAIL    = "FAIL"
CHECK_BLOCKED = "BLOCKED"
CHECK_INFO    = "INFO"

# ---------------------------------------------------------------------------
# Severities
# ---------------------------------------------------------------------------
SEV_CRITICAL = "CRITICAL"
SEV_HIGH     = "HIGH"
SEV_MEDIUM   = "MEDIUM"
SEV_LOW      = "LOW"

# ---------------------------------------------------------------------------
# Safety guard — rejects forbidden trading action tokens
# ---------------------------------------------------------------------------
_FORBIDDEN_TOKENS = frozenset([
    "BUY", "SELL", "ORDER", "EXECUTE",
    "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE",
])
_SAFETY_DECL_TOKENS = frozenset([
    "NO REAL ORDERS", "NO_REAL_ORDERS", "RESEARCH ONLY",
    "PRODUCTION BLOCKED", "PRODUCTION_BLOCKED", "NOT INVESTMENT ADVICE",
])


def _guard(text: str, field_name: str = "field") -> str:
    """Reject forbidden trading action keywords in any field value."""
    if not text:
        return text
    upper = text.upper()
    for decl in _SAFETY_DECL_TOKENS:
        if decl in upper:
            return text  # safety declaration — not a trading action
    for token in _FORBIDDEN_TOKENS:
        pattern = r"\b" + re.escape(token) + r"\b"
        if re.search(pattern, upper):
            raise ValueError(
                f"[StrategyLabSchema] Forbidden token '{token}' detected in "
                f"{field_name}. Strategy Lab is Research Only — no trading actions. "
                f"No Real Orders. Production Trading BLOCKED."
            )
    return text


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class StrategyLabCapability:
    """A single capability in the Strategy Lab capability matrix.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    capability_id:     str
    name:              str
    category:          str
    source_module:     str       = ""
    version_added:     str       = "v0.9.0"
    stable_status:     str       = STABLE_STATUS_STABLE
    maturity:          str       = "STABLE"
    cli_commands:      List[str] = field(default_factory=list)
    gui_tabs:          List[str] = field(default_factory=list)
    reports:           List[str] = field(default_factory=list)
    regression_suites: List[str] = field(default_factory=list)
    dependencies:      List[str] = field(default_factory=list)
    safety_checks:     List[str] = field(default_factory=list)
    known_limitations: List[str] = field(default_factory=list)
    no_real_orders:    bool      = True
    production_blocked: bool     = True

    def to_dict(self) -> dict:
        return {
            "capability_id":    self.capability_id,
            "name":             self.name,
            "category":         self.category,
            "source_module":    self.source_module,
            "version_added":    self.version_added,
            "stable_status":    self.stable_status,
            "maturity":         self.maturity,
            "cli_commands":     "|".join(self.cli_commands),
            "gui_tabs":         "|".join(self.gui_tabs),
            "reports":          "|".join(self.reports),
            "regression_suites": "|".join(self.regression_suites),
            "dependencies":     "|".join(self.dependencies),
            "safety_checks":    "|".join(self.safety_checks),
            "known_limitations": "|".join(self.known_limitations),
            "no_real_orders":   self.no_real_orders,
            "production_blocked": self.production_blocked,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyLabCapability":
        def _split(v: str) -> List[str]:
            return [x for x in v.split("|") if x] if v else []
        return cls(
            capability_id=d.get("capability_id", ""),
            name=d.get("name", ""),
            category=d.get("category", ""),
            source_module=d.get("source_module", ""),
            version_added=d.get("version_added", "v0.9.0"),
            stable_status=d.get("stable_status", STABLE_STATUS_STABLE),
            maturity=d.get("maturity", "STABLE"),
            cli_commands=_split(d.get("cli_commands", "")),
            gui_tabs=_split(d.get("gui_tabs", "")),
            reports=_split(d.get("reports", "")),
            regression_suites=_split(d.get("regression_suites", "")),
            dependencies=_split(d.get("dependencies", "")),
            safety_checks=_split(d.get("safety_checks", "")),
            known_limitations=_split(d.get("known_limitations", "")),
            no_real_orders=str(d.get("no_real_orders", "True")).lower() != "false",
            production_blocked=str(d.get("production_blocked", "True")).lower() != "false",
        )


@dataclass
class StrategyLabCheck:
    """A single check result from the Strategy Lab checklist.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    check_id:       str
    category:       str
    name:           str
    status:         str  = CHECK_PASS
    severity:       str  = SEV_LOW
    message:        str  = ""
    suggested_fix:  str  = ""
    evidence:       str  = ""
    no_real_orders: bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return {
            "check_id":          self.check_id,
            "category":          self.category,
            "name":              self.name,
            "status":            self.status,
            "severity":          self.severity,
            "message":           self.message,
            "suggested_fix":     self.suggested_fix,
            "evidence":          self.evidence,
            "no_real_orders":    self.no_real_orders,
            "production_blocked": self.production_blocked,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyLabCheck":
        return cls(
            check_id=d.get("check_id", ""),
            category=d.get("category", ""),
            name=d.get("name", ""),
            status=d.get("status", CHECK_PASS),
            severity=d.get("severity", SEV_LOW),
            message=d.get("message", ""),
            suggested_fix=d.get("suggested_fix", ""),
            evidence=d.get("evidence", ""),
            no_real_orders=str(d.get("no_real_orders", "True")).lower() != "false",
            production_blocked=str(d.get("production_blocked", "True")).lower() != "false",
        )


@dataclass
class StrategyLabSummary:
    """Summary of the Strategy Lab Stable validation run.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    generated_at:          str  = field(default_factory=lambda: datetime.now().isoformat())
    version:               str  = "v0.9.0"
    release_name:          str  = "Strategy Lab Stable"
    mode:                  str  = "real"

    # Capabilities
    total_capabilities:    int  = 0
    stable_count:          int  = 0
    usable_count:          int  = 0
    partial_count:         int  = 0
    warning_count:         int  = 0
    blocked_count:         int  = 0

    # Checks
    total_checks:          int  = 0
    pass_count:            int  = 0
    warn_count:            int  = 0
    fail_count:            int  = 0
    blocked_check_count:   int  = 0

    # Safety
    recommendations_safe:  bool = True
    memories_safe:         bool = True
    coach_tasks_safe:      bool = True
    metrics_safe:          bool = True
    evidence_graph_safe:   bool = True
    forbidden_action_count: int = 0
    overall_status:        str  = STABLE_STATUS_STABLE

    no_real_orders:        bool = True
    production_blocked:    bool = True

    def to_dict(self) -> dict:
        return {
            "generated_at":           self.generated_at,
            "version":                self.version,
            "release_name":           self.release_name,
            "mode":                   self.mode,
            "total_capabilities":     self.total_capabilities,
            "stable_count":           self.stable_count,
            "usable_count":           self.usable_count,
            "partial_count":          self.partial_count,
            "warning_count":          self.warning_count,
            "blocked_count":          self.blocked_count,
            "total_checks":           self.total_checks,
            "pass_count":             self.pass_count,
            "warn_count":             self.warn_count,
            "fail_count":             self.fail_count,
            "blocked_check_count":    self.blocked_check_count,
            "recommendations_safe":   self.recommendations_safe,
            "memories_safe":          self.memories_safe,
            "coach_tasks_safe":       self.coach_tasks_safe,
            "metrics_safe":           self.metrics_safe,
            "evidence_graph_safe":    self.evidence_graph_safe,
            "forbidden_action_count": self.forbidden_action_count,
            "overall_status":         self.overall_status,
            "no_real_orders":         self.no_real_orders,
            "production_blocked":     self.production_blocked,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyLabSummary":
        def _bool(v) -> bool:
            return str(v).lower() not in ("false", "0", "no")
        return cls(
            generated_at=d.get("generated_at", ""),
            version=d.get("version", "v0.9.0"),
            release_name=d.get("release_name", "Strategy Lab Stable"),
            mode=d.get("mode", "real"),
            total_capabilities=int(d.get("total_capabilities", 0)),
            stable_count=int(d.get("stable_count", 0)),
            usable_count=int(d.get("usable_count", 0)),
            partial_count=int(d.get("partial_count", 0)),
            warning_count=int(d.get("warning_count", 0)),
            blocked_count=int(d.get("blocked_count", 0)),
            total_checks=int(d.get("total_checks", 0)),
            pass_count=int(d.get("pass_count", 0)),
            warn_count=int(d.get("warn_count", 0)),
            fail_count=int(d.get("fail_count", 0)),
            blocked_check_count=int(d.get("blocked_check_count", 0)),
            recommendations_safe=_bool(d.get("recommendations_safe", True)),
            memories_safe=_bool(d.get("memories_safe", True)),
            coach_tasks_safe=_bool(d.get("coach_tasks_safe", True)),
            metrics_safe=_bool(d.get("metrics_safe", True)),
            evidence_graph_safe=_bool(d.get("evidence_graph_safe", True)),
            forbidden_action_count=int(d.get("forbidden_action_count", 0)),
            overall_status=d.get("overall_status", STABLE_STATUS_STABLE),
            no_real_orders=_bool(d.get("no_real_orders", True)),
            production_blocked=_bool(d.get("production_blocked", True)),
        )
