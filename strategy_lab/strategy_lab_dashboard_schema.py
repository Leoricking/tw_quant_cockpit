"""
strategy_lab/strategy_lab_dashboard_schema.py — Strategy Lab Dashboard Schema v0.9.3

Dataclasses for the Strategy Lab Dashboard.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

# ---------------------------------------------------------------------------
# Forbidden keyword guard
# ---------------------------------------------------------------------------

_FORBIDDEN_TOKENS = frozenset([
    "BUY", "SELL", "ORDER", "EXECUTE",
    "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE",
])

# Phrases that contain a forbidden-looking substring but are legitimate safety disclaimers.
# These are never blocked by _guard().
_SAFE_PHRASES = frozenset([
    "NO REAL ORDERS",
    "NO_REAL_ORDERS",
    "NO BUY/SELL/ORDER",
    "PRODUCTION TRADING BLOCKED",
    "NOT INVESTMENT ADVICE",
])


def _guard(text: str, field_name: str = "") -> None:
    """Raise ValueError if text contains forbidden trading tokens as whole words.

    Safety-declaration phrases (e.g. 'No Real Orders') are never blocked.
    Uses word-boundary matching to avoid false positives on compound names
    like 'eps_backed_dip_buy_filter' or 'no_real_orders'.
    """
    import re
    upper = text.upper()
    # Strip known safe phrases first
    for safe in _SAFE_PHRASES:
        upper = upper.replace(safe, "")
    for token in _FORBIDDEN_TOKENS:
        if re.search(r'\b' + token + r'\b', upper):
            raise ValueError(
                f"[SAFETY] Forbidden token '{token}' found in field '{field_name}'. "
                f"No BUY/SELL/ORDER allowed. Research Only."
            )


# ---------------------------------------------------------------------------
# Status / Severity constants
# ---------------------------------------------------------------------------

STATUS_GOOD    = "GOOD"
STATUS_WATCH   = "WATCH"
STATUS_WARNING = "WARNING"
STATUS_BLOCKED = "BLOCKED"
STATUS_UNKNOWN = "UNKNOWN"

SEV_INFO    = "INFO"
SEV_LOW     = "LOW"
SEV_MEDIUM  = "MEDIUM"
SEV_HIGH    = "HIGH"
SEV_EXTREME = "EXTREME"

# ---------------------------------------------------------------------------
# Action type constants
# ---------------------------------------------------------------------------

ACTION_REVIEW           = "REVIEW"
ACTION_BACKTEST_MORE    = "BACKTEST_MORE"
ACTION_PRACTICE_REPLAY  = "PRACTICE_REPLAY"
ACTION_REVIEW_JOURNAL   = "REVIEW_JOURNAL"
ACTION_FIX_DATA         = "FIX_DATA"
ACTION_READ_REPORT      = "READ_REPORT"
ACTION_WAIT             = "WAIT"
ACTION_REVIEW_RISK      = "REVIEW_RISK"
ACTION_REVIEW_EARNINGS  = "REVIEW_EARNINGS"
ACTION_REVIEW_CHIPS     = "REVIEW_CHIPS"
ACTION_BUILD_WATCHLIST  = "BUILD_WATCHLIST"
ACTION_DO_NOT_CHASE     = "DO_NOT_CHASE"
ACTION_KEEP_OBSERVING   = "KEEP_OBSERVING"

ALLOWED_ACTION_TYPES = frozenset([
    ACTION_REVIEW, ACTION_BACKTEST_MORE, ACTION_PRACTICE_REPLAY,
    ACTION_REVIEW_JOURNAL, ACTION_FIX_DATA, ACTION_READ_REPORT,
    ACTION_WAIT, ACTION_REVIEW_RISK, ACTION_REVIEW_EARNINGS,
    ACTION_REVIEW_CHIPS, ACTION_BUILD_WATCHLIST, ACTION_DO_NOT_CHASE,
    ACTION_KEEP_OBSERVING,
])


# ---------------------------------------------------------------------------
# StrategyLabDashboardCard
# ---------------------------------------------------------------------------

@dataclass
class StrategyLabDashboardCard:
    """A single summary card on the Strategy Lab Dashboard.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """
    card_id:           str = ""
    title:             str = ""
    value:             str = ""
    subtitle:          str = ""
    status:            str = STATUS_UNKNOWN   # GOOD/WATCH/WARNING/BLOCKED/UNKNOWN
    severity:          str = SEV_INFO         # INFO/LOW/MEDIUM/HIGH/EXTREME
    source_module:     str = ""
    safe_next_step:    str = ""
    no_real_orders:    bool = True
    production_blocked: bool = True

    def __post_init__(self):
        _guard(self.title,          "title")
        _guard(self.value,          "value")
        _guard(self.subtitle,       "subtitle")
        _guard(self.safe_next_step, "safe_next_step")

    def to_dict(self) -> dict:
        return {
            "card_id":           self.card_id,
            "title":             self.title,
            "value":             self.value,
            "subtitle":          self.subtitle,
            "status":            self.status,
            "severity":          self.severity,
            "source_module":     self.source_module,
            "safe_next_step":    self.safe_next_step,
            "no_real_orders":    self.no_real_orders,
            "production_blocked": self.production_blocked,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyLabDashboardCard":
        return cls(
            card_id=d.get("card_id", ""),
            title=d.get("title", ""),
            value=d.get("value", ""),
            subtitle=d.get("subtitle", ""),
            status=d.get("status", STATUS_UNKNOWN),
            severity=d.get("severity", SEV_INFO),
            source_module=d.get("source_module", ""),
            safe_next_step=d.get("safe_next_step", ""),
            no_real_orders=bool(d.get("no_real_orders", True)),
            production_blocked=bool(d.get("production_blocked", True)),
        )


# ---------------------------------------------------------------------------
# StrategyLabDashboardRow
# ---------------------------------------------------------------------------

@dataclass
class StrategyLabDashboardRow:
    """A single row in the Strategy Lab Dashboard validation board.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """
    row_id:            str = ""
    category:          str = ""
    title:             str = ""
    status:            str = STATUS_UNKNOWN
    priority:          str = "P2"
    score:             float = 0.0
    grade:             str = ""
    source_module:     str = ""
    evidence:          str = ""
    limitation:        str = ""
    safe_next_step:    str = ""
    no_real_orders:    bool = True
    production_blocked: bool = True

    def __post_init__(self):
        _guard(self.title,          "title")
        _guard(self.evidence,       "evidence")
        _guard(self.safe_next_step, "safe_next_step")

    def to_dict(self) -> dict:
        return {
            "row_id":            self.row_id,
            "category":          self.category,
            "title":             self.title,
            "status":            self.status,
            "priority":          self.priority,
            "score":             self.score,
            "grade":             self.grade,
            "source_module":     self.source_module,
            "evidence":          self.evidence,
            "limitation":        self.limitation,
            "safe_next_step":    self.safe_next_step,
            "no_real_orders":    self.no_real_orders,
            "production_blocked": self.production_blocked,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyLabDashboardRow":
        return cls(
            row_id=d.get("row_id", ""),
            category=d.get("category", ""),
            title=d.get("title", ""),
            status=d.get("status", STATUS_UNKNOWN),
            priority=d.get("priority", "P2"),
            score=float(d.get("score", 0.0)),
            grade=d.get("grade", ""),
            source_module=d.get("source_module", ""),
            evidence=d.get("evidence", ""),
            limitation=d.get("limitation", ""),
            safe_next_step=d.get("safe_next_step", ""),
            no_real_orders=bool(d.get("no_real_orders", True)),
            production_blocked=bool(d.get("production_blocked", True)),
        )


# ---------------------------------------------------------------------------
# StrategyLabActionItem
# ---------------------------------------------------------------------------

@dataclass
class StrategyLabActionItem:
    """An action item on the Strategy Lab Dashboard.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    action_type must be one of ALLOWED_ACTION_TYPES.
    """
    action_id:          str = ""
    title:              str = ""
    action_type:        str = ACTION_REVIEW    # must be in ALLOWED_ACTION_TYPES
    priority:           str = "P2"
    source_module:      str = ""
    related_strategy_id: str = ""
    related_thread_id:  str = ""
    related_memory_id:  str = ""
    related_task_id:    str = ""
    reason:             str = ""
    safe_command:       str = ""
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __post_init__(self):
        if self.action_type not in ALLOWED_ACTION_TYPES:
            raise ValueError(
                f"action_type '{self.action_type}' not in ALLOWED_ACTION_TYPES. "
                f"Only research actions allowed."
            )
        _guard(self.title,        "title")
        _guard(self.reason,       "reason")
        _guard(self.safe_command, "safe_command")

    def to_dict(self) -> dict:
        return {
            "action_id":           self.action_id,
            "title":               self.title,
            "action_type":         self.action_type,
            "priority":            self.priority,
            "source_module":       self.source_module,
            "related_strategy_id": self.related_strategy_id,
            "related_thread_id":   self.related_thread_id,
            "related_memory_id":   self.related_memory_id,
            "related_task_id":     self.related_task_id,
            "reason":              self.reason,
            "safe_command":        self.safe_command,
            "no_real_orders":      self.no_real_orders,
            "production_blocked":  self.production_blocked,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyLabActionItem":
        return cls(
            action_id=d.get("action_id", ""),
            title=d.get("title", ""),
            action_type=d.get("action_type", ACTION_REVIEW),
            priority=d.get("priority", "P2"),
            source_module=d.get("source_module", ""),
            related_strategy_id=d.get("related_strategy_id", ""),
            related_thread_id=d.get("related_thread_id", ""),
            related_memory_id=d.get("related_memory_id", ""),
            related_task_id=d.get("related_task_id", ""),
            reason=d.get("reason", ""),
            safe_command=d.get("safe_command", ""),
            no_real_orders=bool(d.get("no_real_orders", True)),
            production_blocked=bool(d.get("production_blocked", True)),
        )


# ---------------------------------------------------------------------------
# StrategyLabDashboardSummary
# ---------------------------------------------------------------------------

@dataclass
class StrategyLabDashboardSummary:
    """Aggregate summary of the Strategy Lab Dashboard run.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """
    generated_at:             str = ""
    mode:                     str = "real"
    overall_status:           str = "UNKNOWN"   # STABLE/WATCH/WARNING/CRITICAL
    overall_health_score:     float = 0.0
    strategy_count:           int = 0
    validated_count:          int = 0
    validating_count:         int = 0
    observational_count:      int = 0
    insufficient_count:       int = 0
    conflicted_count:         int = 0
    rejected_count:           int = 0
    evidence_thread_count:    int = 0
    graph_gap_count:          int = 0
    crash_reversal_warning_count: int = 0
    training_metric_count:    int = 0
    coach_task_count:         int = 0
    memory_active_count:      int = 0
    needs_backtest_count:     int = 0
    needs_replay_count:       int = 0
    needs_data_count:         int = 0
    forbidden_action_count:   int = 0
    no_real_orders:           bool = True
    production_blocked:       bool = True

    def to_dict(self) -> dict:
        return {
            "generated_at":               self.generated_at,
            "mode":                       self.mode,
            "overall_status":             self.overall_status,
            "overall_health_score":       self.overall_health_score,
            "strategy_count":             self.strategy_count,
            "validated_count":            self.validated_count,
            "validating_count":           self.validating_count,
            "observational_count":        self.observational_count,
            "insufficient_count":         self.insufficient_count,
            "conflicted_count":           self.conflicted_count,
            "rejected_count":             self.rejected_count,
            "evidence_thread_count":      self.evidence_thread_count,
            "graph_gap_count":            self.graph_gap_count,
            "crash_reversal_warning_count": self.crash_reversal_warning_count,
            "training_metric_count":      self.training_metric_count,
            "coach_task_count":           self.coach_task_count,
            "memory_active_count":        self.memory_active_count,
            "needs_backtest_count":       self.needs_backtest_count,
            "needs_replay_count":         self.needs_replay_count,
            "needs_data_count":           self.needs_data_count,
            "forbidden_action_count":     self.forbidden_action_count,
            "no_real_orders":             self.no_real_orders,
            "production_blocked":         self.production_blocked,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyLabDashboardSummary":
        return cls(
            generated_at=d.get("generated_at", ""),
            mode=d.get("mode", "real"),
            overall_status=d.get("overall_status", "UNKNOWN"),
            overall_health_score=float(d.get("overall_health_score", 0.0)),
            strategy_count=int(d.get("strategy_count", 0)),
            validated_count=int(d.get("validated_count", 0)),
            validating_count=int(d.get("validating_count", 0)),
            observational_count=int(d.get("observational_count", 0)),
            insufficient_count=int(d.get("insufficient_count", 0)),
            conflicted_count=int(d.get("conflicted_count", 0)),
            rejected_count=int(d.get("rejected_count", 0)),
            evidence_thread_count=int(d.get("evidence_thread_count", 0)),
            graph_gap_count=int(d.get("graph_gap_count", 0)),
            crash_reversal_warning_count=int(d.get("crash_reversal_warning_count", 0)),
            training_metric_count=int(d.get("training_metric_count", 0)),
            coach_task_count=int(d.get("coach_task_count", 0)),
            memory_active_count=int(d.get("memory_active_count", 0)),
            needs_backtest_count=int(d.get("needs_backtest_count", 0)),
            needs_replay_count=int(d.get("needs_replay_count", 0)),
            needs_data_count=int(d.get("needs_data_count", 0)),
            forbidden_action_count=int(d.get("forbidden_action_count", 0)),
            no_real_orders=bool(d.get("no_real_orders", True)),
            production_blocked=bool(d.get("production_blocked", True)),
        )
