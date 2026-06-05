"""research_intelligence/research_intelligence_schema.py — Schema for Research Intelligence v0.7.1.

[!] Research Intelligence Only. Research Only. No Real Orders.
[!] Production Trading: BLOCKED. Not investment advice.
[!] All action_type outputs are research-only. BUY/SELL/ORDER are forbidden.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Source module constants
# ---------------------------------------------------------------------------
SRC_DATA_COVERAGE       = "data_coverage"
SRC_DATA_STABILIZATION  = "data_stabilization"
SRC_REPORT_PACK         = "report_pack"
SRC_REPLAY_TRAINING     = "replay_training"
SRC_PORTFOLIO_JOURNAL   = "portfolio_journal"
SRC_RESEARCH_COACH      = "research_coach"
SRC_RESEARCH_REVIEW     = "research_review"
SRC_RESEARCH_WORKFLOW   = "research_workflow"
SRC_STRATEGY_KNOWLEDGE  = "strategy_knowledge"
SRC_STRATEGY_FILTER     = "strategy_filter"
SRC_RULE_GOVERNANCE     = "rule_governance"
SRC_REGRESSION          = "regression"
SRC_STABLE_RELEASE      = "stable_release"
SRC_PROVIDER_HEALTH     = "provider_health"
SRC_NOTIFICATION_CENTER = "notification_center"

ALL_SOURCE_MODULES = [
    SRC_DATA_COVERAGE, SRC_DATA_STABILIZATION, SRC_REPORT_PACK,
    SRC_REPLAY_TRAINING, SRC_PORTFOLIO_JOURNAL, SRC_RESEARCH_COACH,
    SRC_RESEARCH_REVIEW, SRC_RESEARCH_WORKFLOW, SRC_STRATEGY_KNOWLEDGE,
    SRC_STRATEGY_FILTER, SRC_RULE_GOVERNANCE, SRC_REGRESSION,
    SRC_STABLE_RELEASE, SRC_PROVIDER_HEALTH, SRC_NOTIFICATION_CENTER,
]

# ---------------------------------------------------------------------------
# Category constants
# ---------------------------------------------------------------------------
CAT_DATA_GAP           = "DATA_GAP"
CAT_REPORT_GAP         = "REPORT_GAP"
CAT_REPLAY_MISTAKE     = "REPLAY_MISTAKE"
CAT_JOURNAL_PATTERN    = "JOURNAL_PATTERN"
CAT_RULE_REVIEW        = "RULE_REVIEW"
CAT_STRATEGY_RESEARCH  = "STRATEGY_RESEARCH"
CAT_SYSTEM_RISK        = "SYSTEM_RISK"
CAT_TRAINING_TASK      = "TRAINING_TASK"
CAT_PROVIDER_LIMIT     = "PROVIDER_LIMITATION"
CAT_REGRESSION_WARN    = "REGRESSION_WARNING"
CAT_STABLE_NOTE        = "STABLE_RELEASE_NOTE"

ALL_CATEGORIES = [
    CAT_DATA_GAP, CAT_REPORT_GAP, CAT_REPLAY_MISTAKE, CAT_JOURNAL_PATTERN,
    CAT_RULE_REVIEW, CAT_STRATEGY_RESEARCH, CAT_SYSTEM_RISK, CAT_TRAINING_TASK,
    CAT_PROVIDER_LIMIT, CAT_REGRESSION_WARN, CAT_STABLE_NOTE,
]

# ---------------------------------------------------------------------------
# Priority constants
# ---------------------------------------------------------------------------
PRI_P0 = "P0"
PRI_P1 = "P1"
PRI_P2 = "P2"
PRI_P3 = "P3"

# ---------------------------------------------------------------------------
# Severity constants
# ---------------------------------------------------------------------------
SEV_CRITICAL = "CRITICAL"
SEV_HIGH     = "HIGH"
SEV_MEDIUM   = "MEDIUM"
SEV_LOW      = "LOW"
SEV_INFO     = "INFO"

# ---------------------------------------------------------------------------
# Action type constants — RESEARCH ONLY, NO TRADING ACTIONS
# ---------------------------------------------------------------------------
ACT_FIX_DATA        = "FIX_DATA"
ACT_GENERATE_REPORT = "GENERATE_REPORT"
ACT_REVIEW_RULE     = "REVIEW_RULE"
ACT_PRACTICE_REPLAY = "PRACTICE_REPLAY"
ACT_REVIEW_JOURNAL  = "REVIEW_JOURNAL"
ACT_RUN_BACKTEST    = "RUN_BACKTEST"
ACT_RUN_REGRESSION  = "RUN_REGRESSION"
ACT_READ_REPORT     = "READ_REPORT"
ACT_WAIT            = "WAIT"
ACT_WATCH           = "WATCH"
ACT_DO_NOT_TRADE    = "DO_NOT_TRADE"

SAFE_ACTION_TYPES = {
    ACT_FIX_DATA, ACT_GENERATE_REPORT, ACT_REVIEW_RULE, ACT_PRACTICE_REPLAY,
    ACT_REVIEW_JOURNAL, ACT_RUN_BACKTEST, ACT_RUN_REGRESSION, ACT_READ_REPORT,
    ACT_WAIT, ACT_WATCH, ACT_DO_NOT_TRADE,
}

# Forbidden action types — must never appear in output
FORBIDDEN_ACTION_TYPES = {
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE",
    "PLACE_ORDER", "BROKER_ORDER", "REAL_TRADE",
}

# ---------------------------------------------------------------------------
# Command safety classification constants
# ---------------------------------------------------------------------------
CMD_SAFE_READ_ONLY    = "SAFE_READ_ONLY"
CMD_SAFE_REPORT       = "SAFE_REPORT"
CMD_SAFE_REGRESSION   = "SAFE_REGRESSION"
CMD_SAFE_REPLAY       = "SAFE_REPLAY"
CMD_SAFE_DATA_CHECK   = "SAFE_DATA_CHECK"
CMD_BLOCKED_TRADING   = "BLOCKED_FOR_TRADING"

_FORBIDDEN_CMD_KEYWORDS = {
    "buy", "sell", "order", "execute", "submit_order", "auto_trade",
    "place_order", "broker_order", "real_trade",
}


def classify_command_safety(command: str) -> str:
    """Return command safety classification. Returns BLOCKED_FOR_TRADING if any forbidden keyword found."""
    if not command:
        return CMD_SAFE_READ_ONLY
    cmd_lower = command.lower()
    for kw in _FORBIDDEN_CMD_KEYWORDS:
        if kw in cmd_lower:
            return CMD_BLOCKED_TRADING
    if any(x in cmd_lower for x in ["report", "generate-report", "auto-report"]):
        return CMD_SAFE_REPORT
    if any(x in cmd_lower for x in ["regression", "stable-v060", "compileall"]):
        return CMD_SAFE_REGRESSION
    if any(x in cmd_lower for x in ["replay", "replay-training"]):
        return CMD_SAFE_REPLAY
    if any(x in cmd_lower for x in ["coverage", "data-quality", "data-freshness", "feature"]):
        return CMD_SAFE_DATA_CHECK
    return CMD_SAFE_READ_ONLY

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
STATUS_NEW       = "NEW"
STATUS_REVIEWED  = "REVIEWED"
STATUS_RESOLVED  = "RESOLVED"
STATUS_DEFERRED  = "DEFERRED"


def _validate_action(action_type: str) -> str:
    """Raise ValueError if action_type is forbidden. Returns the safe action."""
    if action_type and action_type.upper() in FORBIDDEN_ACTION_TYPES:
        raise ValueError(
            f"[!] FORBIDDEN action_type '{action_type}' — "
            f"Research Intelligence must not produce BUY/SELL/ORDER actions. "
            f"No real orders. Production Trading: BLOCKED."
        )
    return action_type


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ResearchSignal:
    """A single research signal collected from a source module.

    [!] Research Intelligence Only. Research Only. No Real Orders.
    """

    signal_id:                 str
    source_module:             str
    source_type:               str = ""
    category:                  str = CAT_DATA_GAP
    title:                     str = ""
    description:               str = ""
    severity:                  str = SEV_INFO
    confidence:                float = 0.5
    priority:                  str = PRI_P3
    status:                    str = STATUS_NEW
    suggested_action:          str = ACT_READ_REPORT
    suggested_command:         str = ""
    related_symbols:           List[str] = field(default_factory=list)
    related_strategies:        List[str] = field(default_factory=list)
    related_reports:           List[str] = field(default_factory=list)
    related_rules:             List[str] = field(default_factory=list)
    related_replay_sessions:   List[str] = field(default_factory=list)
    evidence:                  str = ""
    warning:                   str = ""
    created_at:                str = ""
    display_label:             str = ""
    user_friendly_reason:      str = ""
    safe_action_hint:          str = ""
    read_only:                 bool = True
    no_real_orders:            bool = True
    production_blocked:        bool = True

    def __post_init__(self):
        _validate_action(self.suggested_action)
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "signal_id":              self.signal_id,
            "source_module":          self.source_module,
            "source_type":            self.source_type,
            "category":               self.category,
            "title":                  self.title,
            "description":            self.description,
            "severity":               self.severity,
            "confidence":             self.confidence,
            "priority":               self.priority,
            "status":                 self.status,
            "suggested_action":       self.suggested_action,
            "suggested_command":      self.suggested_command,
            "related_symbols":        "|".join(self.related_symbols),
            "related_strategies":     "|".join(self.related_strategies),
            "related_reports":        "|".join(self.related_reports),
            "related_rules":          "|".join(self.related_rules),
            "related_replay_sessions": "|".join(self.related_replay_sessions),
            "evidence":               self.evidence,
            "warning":                self.warning,
            "created_at":             self.created_at,
            "display_label":          self.display_label,
            "user_friendly_reason":   self.user_friendly_reason,
            "safe_action_hint":       self.safe_action_hint,
            "read_only":              self.read_only,
            "no_real_orders":         self.no_real_orders,
            "production_blocked":     self.production_blocked,
        }


@dataclass
class ResearchRecommendation:
    """A ranked research action recommendation.

    [!] Research Intelligence Only. Research Only. No Real Orders.
    """

    recommendation_id:  str
    title:              str
    category:           str = CAT_DATA_GAP
    priority:           str = PRI_P3
    action_type:        str = ACT_READ_REPORT
    rationale:          str = ""
    expected_benefit:   str = ""
    required_inputs:    List[str] = field(default_factory=list)
    suggested_commands: List[str] = field(default_factory=list)
    blockers:           List[str] = field(default_factory=list)
    related_signals:    List[str] = field(default_factory=list)
    related_modules:    List[str] = field(default_factory=list)
    due_hint:           str = ""
    status:             str = STATUS_NEW
    why_now:            str = ""
    risk_if_ignored:    str = ""
    command_safety:     str = CMD_SAFE_READ_ONLY
    safe_command_label: str = ""
    display_order:      int = 0
    optional:           bool = False
    dismissible:        bool = False
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __post_init__(self):
        _validate_action(self.action_type)

    def to_dict(self) -> dict:
        return {
            "recommendation_id":  self.recommendation_id,
            "title":              self.title,
            "category":           self.category,
            "priority":           self.priority,
            "action_type":        self.action_type,
            "rationale":          self.rationale,
            "expected_benefit":   self.expected_benefit,
            "required_inputs":    "|".join(self.required_inputs),
            "suggested_commands": "|".join(self.suggested_commands),
            "blockers":           "|".join(self.blockers),
            "related_signals":    "|".join(self.related_signals),
            "related_modules":    "|".join(self.related_modules),
            "due_hint":           self.due_hint,
            "status":             self.status,
            "why_now":            self.why_now,
            "risk_if_ignored":    self.risk_if_ignored,
            "command_safety":     self.command_safety,
            "safe_command_label": self.safe_command_label,
            "display_order":      self.display_order,
            "optional":           self.optional,
            "dismissible":        self.dismissible,
            "no_real_orders":     self.no_real_orders,
            "production_blocked": self.production_blocked,
        }


@dataclass
class ResearchIntelligenceSummary:
    """Top-level summary of a Research Intelligence run.

    [!] Research Intelligence Only. Research Only. No Real Orders.
    """

    generated_at:           str
    mode:                   str = "real"
    total_signals:          int = 0
    high_priority_count:    int = 0
    medium_priority_count:  int = 0
    low_priority_count:     int = 0
    data_gap_count:         int = 0
    replay_issue_count:     int = 0
    rule_review_count:      int = 0
    report_gap_count:       int = 0
    system_risk_count:      int = 0
    recommendations_count:          int = 0
    top_priority:                   str = ""
    overall_status:                 str = "OK"
    today_focus:                    str = ""
    top_p0_title:                   str = ""
    top_p1_title:                   str = ""
    safe_command_count:             int = 0
    blocked_trading_action_count:   int = 0
    optional_recommendation_count:  int = 0
    no_real_orders:                 bool = True
    production_blocked:             bool = True

    def to_dict(self) -> dict:
        return {
            "generated_at":          self.generated_at,
            "mode":                  self.mode,
            "total_signals":         self.total_signals,
            "high_priority_count":   self.high_priority_count,
            "medium_priority_count": self.medium_priority_count,
            "low_priority_count":    self.low_priority_count,
            "data_gap_count":        self.data_gap_count,
            "replay_issue_count":    self.replay_issue_count,
            "rule_review_count":     self.rule_review_count,
            "report_gap_count":      self.report_gap_count,
            "system_risk_count":     self.system_risk_count,
            "recommendations_count": self.recommendations_count,
            "top_priority":                  self.top_priority,
            "overall_status":                self.overall_status,
            "today_focus":                   self.today_focus,
            "top_p0_title":                  self.top_p0_title,
            "top_p1_title":                  self.top_p1_title,
            "safe_command_count":            self.safe_command_count,
            "blocked_trading_action_count":  self.blocked_trading_action_count,
            "optional_recommendation_count": self.optional_recommendation_count,
            "no_real_orders":                self.no_real_orders,
            "production_blocked":            self.production_blocked,
        }
