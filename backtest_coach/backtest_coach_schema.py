"""
backtest_coach/backtest_coach_schema.py — Backtest-to-Coach Loop Schema v0.7.3

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional

# ---------------------------------------------------------------------------
# Issue types
# ---------------------------------------------------------------------------
ISSUE_LOW_WIN_RATE           = "LOW_WIN_RATE"
ISSUE_HIGH_DRAWDOWN          = "HIGH_DRAWDOWN"
ISSUE_POOR_RISK_REWARD       = "POOR_RISK_REWARD"
ISSUE_OVERTRADING            = "OVERTRADING"
ISSUE_LATE_ENTRY             = "LATE_ENTRY"
ISSUE_LATE_EXIT              = "LATE_EXIT"
ISSUE_STOP_LOSS_DISCIPLINE   = "STOP_LOSS_DISCIPLINE"
ISSUE_FAKE_BREAKOUT          = "FAKE_BREAKOUT"
ISSUE_VWAP_LOSS              = "VWAP_LOSS"
ISSUE_OPENING_RANGE_FAILURE  = "OPENING_RANGE_FAILURE"
ISSUE_DATA_INSUFFICIENT      = "DATA_INSUFFICIENT"
ISSUE_SAMPLE_TOO_SMALL       = "SAMPLE_TOO_SMALL"
ISSUE_RULE_LOW_CONFIDENCE    = "RULE_LOW_CONFIDENCE"
ISSUE_JOURNAL_REPEAT_MISTAKE = "JOURNAL_REPEAT_MISTAKE"
ISSUE_REPLAY_SCORE_LOW       = "REPLAY_SCORE_LOW"

ALL_ISSUE_TYPES = [
    ISSUE_LOW_WIN_RATE, ISSUE_HIGH_DRAWDOWN, ISSUE_POOR_RISK_REWARD,
    ISSUE_OVERTRADING, ISSUE_LATE_ENTRY, ISSUE_LATE_EXIT,
    ISSUE_STOP_LOSS_DISCIPLINE, ISSUE_FAKE_BREAKOUT, ISSUE_VWAP_LOSS,
    ISSUE_OPENING_RANGE_FAILURE, ISSUE_DATA_INSUFFICIENT, ISSUE_SAMPLE_TOO_SMALL,
    ISSUE_RULE_LOW_CONFIDENCE, ISSUE_JOURNAL_REPEAT_MISTAKE, ISSUE_REPLAY_SCORE_LOW,
]

# ---------------------------------------------------------------------------
# Task types (ONLY these — no trading actions)
# ---------------------------------------------------------------------------
TASK_PRACTICE_REPLAY = "PRACTICE_REPLAY"
TASK_REVIEW_RULE     = "REVIEW_RULE"
TASK_REVIEW_JOURNAL  = "REVIEW_JOURNAL"
TASK_FIX_DATA        = "FIX_DATA"
TASK_BACKTEST_MORE   = "BACKTEST_MORE"
TASK_READ_REPORT     = "READ_REPORT"
TASK_UPDATE_MEMORY   = "UPDATE_MEMORY"
TASK_WAIT            = "WAIT"

ALL_TASK_TYPES = [
    TASK_PRACTICE_REPLAY, TASK_REVIEW_RULE, TASK_REVIEW_JOURNAL,
    TASK_FIX_DATA, TASK_BACKTEST_MORE, TASK_READ_REPORT,
    TASK_UPDATE_MEMORY, TASK_WAIT,
]

# ---------------------------------------------------------------------------
# Task statuses
# ---------------------------------------------------------------------------
STATUS_NEW         = "NEW"
STATUS_IN_PROGRESS = "IN_PROGRESS"
STATUS_DONE        = "DONE"
STATUS_SKIPPED     = "SKIPPED"
STATUS_ARCHIVED    = "ARCHIVED"

ALL_STATUSES = [STATUS_NEW, STATUS_IN_PROGRESS, STATUS_DONE, STATUS_SKIPPED, STATUS_ARCHIVED]

# ---------------------------------------------------------------------------
# Priorities
# ---------------------------------------------------------------------------
PRIORITY_P0 = "P0"
PRIORITY_P1 = "P1"
PRIORITY_P2 = "P2"
PRIORITY_P3 = "P3"

ALL_PRIORITIES = [PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3]

# ---------------------------------------------------------------------------
# Severities
# ---------------------------------------------------------------------------
SEV_CRITICAL = "CRITICAL"
SEV_HIGH     = "HIGH"
SEV_MEDIUM   = "MEDIUM"
SEV_LOW      = "LOW"

ALL_SEVERITIES = [SEV_CRITICAL, SEV_HIGH, SEV_MEDIUM, SEV_LOW]

# ---------------------------------------------------------------------------
# Source modules
# ---------------------------------------------------------------------------
SRC_BACKTEST              = "backtest"
SRC_STRATEGY_MEMORY       = "strategy_memory"
SRC_REPLAY_TRAINING       = "replay_training"
SRC_PORTFOLIO_JOURNAL     = "portfolio_journal"
SRC_RESEARCH_INTELLIGENCE = "research_intelligence"
SRC_RULE_GOVERNANCE       = "rule_governance"
SRC_DATA_COVERAGE         = "data_coverage"

ALL_SOURCES = [
    SRC_BACKTEST, SRC_STRATEGY_MEMORY, SRC_REPLAY_TRAINING,
    SRC_PORTFOLIO_JOURNAL, SRC_RESEARCH_INTELLIGENCE,
    SRC_RULE_GOVERNANCE, SRC_DATA_COVERAGE,
]

# ---------------------------------------------------------------------------
# Forbidden keyword guard
# ---------------------------------------------------------------------------
_FORBIDDEN = ["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE"]


def _guard(text: str) -> str:
    """Raise if text contains forbidden trading action keywords."""
    if text:
        upper = text.upper()
        for f in _FORBIDDEN:
            if f in upper:
                raise ValueError(
                    f"Forbidden keyword '{f}' in BacktestCoach output. "
                    "Coach Loop is Research Only — no trading actions allowed."
                )
    return text


# ---------------------------------------------------------------------------
# BacktestCoachSignal
# ---------------------------------------------------------------------------

@dataclass
class BacktestCoachSignal:
    """A single backtest weakness or research gap signal.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    signal_id:         str      = field(default_factory=lambda: f"SIG-{uuid.uuid4().hex[:8].upper()}")
    source_module:     str      = SRC_BACKTEST
    issue_type:        str      = ISSUE_LOW_WIN_RATE
    severity:          str      = SEV_MEDIUM
    priority:          str      = PRIORITY_P2
    strategy_name:     str      = ""
    symbol:            str      = ""
    metric_name:       str      = ""
    metric_value:      float    = 0.0
    threshold:         float    = 0.0
    description:       str      = ""
    evidence:          str      = ""
    suggested_action:  str      = ""
    suggested_command: str      = ""
    created_at:        str      = field(default_factory=lambda: datetime.now().isoformat())
    no_real_orders:    bool     = True
    production_blocked: bool    = True

    def __post_init__(self):
        _guard(self.description)
        _guard(self.evidence)
        _guard(self.suggested_action)
        _guard(self.suggested_command)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "BacktestCoachSignal":
        d = dict(d)
        for float_key in ["metric_value", "threshold"]:
            if isinstance(d.get(float_key), str):
                try:
                    d[float_key] = float(d[float_key])
                except (ValueError, TypeError):
                    d[float_key] = 0.0
        for bool_key in ["no_real_orders", "production_blocked"]:
            if isinstance(d.get(bool_key), str):
                d[bool_key] = d[bool_key].lower() in ("true", "1", "yes")
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


# ---------------------------------------------------------------------------
# CoachTrainingTask
# ---------------------------------------------------------------------------

@dataclass
class CoachTrainingTask:
    """A single coach training task derived from backtest signals.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    Task types are limited to PRACTICE_REPLAY, REVIEW_RULE, REVIEW_JOURNAL,
    FIX_DATA, BACKTEST_MORE, READ_REPORT, UPDATE_MEMORY, WAIT only.
    """

    task_id:             str        = field(default_factory=lambda: f"TASK-{uuid.uuid4().hex[:8].upper()}")
    task_type:           str        = TASK_REVIEW_RULE
    title:               str        = ""
    description:         str        = ""
    training_goal:       str        = ""
    practice_method:     str        = ""
    success_criteria:    str        = ""
    priority:            str        = PRIORITY_P2
    status:              str        = STATUS_NEW
    source_module:       str        = SRC_BACKTEST
    source_signal_ids:   List[str]  = field(default_factory=list)
    strategy_name:       str        = ""
    symbol:              str        = ""
    suggested_commands:  List[str]  = field(default_factory=list)
    estimated_minutes:   int        = 30
    created_at:          str        = field(default_factory=lambda: datetime.now().isoformat())
    no_real_orders:      bool       = True
    production_blocked:  bool       = True

    def __post_init__(self):
        _guard(self.title)
        _guard(self.description)
        _guard(self.training_goal)
        _guard(self.practice_method)
        for cmd in self.suggested_commands:
            _guard(cmd)

    def to_dict(self) -> dict:
        d = asdict(self)
        for lst_key in ["source_signal_ids", "suggested_commands"]:
            if isinstance(d[lst_key], list):
                d[lst_key] = "|".join(str(x) for x in d[lst_key])
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "CoachTrainingTask":
        d = dict(d)
        for lst_key in ["source_signal_ids", "suggested_commands"]:
            val = d.get(lst_key, "")
            if isinstance(val, str):
                d[lst_key] = [x for x in val.split("|") if x]
            elif val is None:
                d[lst_key] = []
        for bool_key in ["no_real_orders", "production_blocked"]:
            if isinstance(d.get(bool_key), str):
                d[bool_key] = d[bool_key].lower() in ("true", "1", "yes")
        for int_key in ["estimated_minutes"]:
            if isinstance(d.get(int_key), str):
                try:
                    d[int_key] = int(d[int_key])
                except (ValueError, TypeError):
                    d[int_key] = 30
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


# ---------------------------------------------------------------------------
# BacktestCoachSummary
# ---------------------------------------------------------------------------

@dataclass
class BacktestCoachSummary:
    """Aggregate summary of backtest coach loop run.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    generated_at:         str   = field(default_factory=lambda: datetime.now().isoformat())
    mode:                 str   = "real"
    total_signals:        int   = 0
    total_tasks:          int   = 0
    p0_count:             int   = 0
    p1_count:             int   = 0
    p2_count:             int   = 0
    p3_count:             int   = 0
    replay_tasks:         int   = 0
    rule_review_tasks:    int   = 0
    journal_tasks:        int   = 0
    backtest_tasks:       int   = 0
    fix_data_tasks:       int   = 0
    read_report_tasks:    int   = 0
    update_memory_tasks:  int   = 0
    wait_tasks:           int   = 0
    daily_tasks_count:    int   = 0
    weekly_tasks_count:   int   = 0
    top_task:             str   = ""
    top_signal:           str   = ""
    overall_status:       str   = "OK"
    no_real_orders:       bool  = True
    production_blocked:   bool  = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "BacktestCoachSummary":
        d = dict(d)
        for bool_key in ["no_real_orders", "production_blocked"]:
            if isinstance(d.get(bool_key), str):
                d[bool_key] = d[bool_key].lower() in ("true", "1", "yes")
        for int_key in [
            "total_signals", "total_tasks", "p0_count", "p1_count",
            "p2_count", "p3_count", "replay_tasks", "rule_review_tasks",
            "journal_tasks", "backtest_tasks", "fix_data_tasks",
            "read_report_tasks", "update_memory_tasks", "wait_tasks",
            "daily_tasks_count", "weekly_tasks_count",
        ]:
            if isinstance(d.get(int_key), str):
                try:
                    d[int_key] = int(d[int_key])
                except (ValueError, TypeError):
                    d[int_key] = 0
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
