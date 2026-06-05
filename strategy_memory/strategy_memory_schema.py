"""
strategy_memory_schema.py — Strategy Research Memory Schema v0.7.2

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime

# --- Memory Types ---
MEMORY_TYPE_STRATEGY_HYPOTHESIS   = "STRATEGY_HYPOTHESIS"
MEMORY_TYPE_RULE_CANDIDATE         = "RULE_CANDIDATE"
MEMORY_TYPE_REPLAY_MISTAKE_PATTERN = "REPLAY_MISTAKE_PATTERN"
MEMORY_TYPE_JOURNAL_PATTERN        = "JOURNAL_PATTERN"
MEMORY_TYPE_DATA_GAP               = "DATA_GAP"
MEMORY_TYPE_REPORT_GAP             = "REPORT_GAP"
MEMORY_TYPE_REGRESSION_RISK        = "REGRESSION_RISK"
MEMORY_TYPE_PROVIDER_LIMITATION    = "PROVIDER_LIMITATION"
MEMORY_TYPE_RESEARCH_CONCLUSION    = "RESEARCH_CONCLUSION"
MEMORY_TYPE_FOLLOW_UP_TASK         = "FOLLOW_UP_TASK"

ALL_MEMORY_TYPES = [
    MEMORY_TYPE_STRATEGY_HYPOTHESIS, MEMORY_TYPE_RULE_CANDIDATE,
    MEMORY_TYPE_REPLAY_MISTAKE_PATTERN, MEMORY_TYPE_JOURNAL_PATTERN,
    MEMORY_TYPE_DATA_GAP, MEMORY_TYPE_REPORT_GAP,
    MEMORY_TYPE_REGRESSION_RISK, MEMORY_TYPE_PROVIDER_LIMITATION,
    MEMORY_TYPE_RESEARCH_CONCLUSION, MEMORY_TYPE_FOLLOW_UP_TASK,
]

# --- Statuses ---
STATUS_NEW                = "NEW"
STATUS_REVIEWING          = "REVIEWING"
STATUS_VALIDATING         = "VALIDATING"
STATUS_ACCEPTED           = "ACCEPTED"
STATUS_REJECTED           = "REJECTED"
STATUS_ARCHIVED           = "ARCHIVED"
STATUS_NEEDS_MORE_EVIDENCE = "NEEDS_MORE_EVIDENCE"

ALL_STATUSES = [
    STATUS_NEW, STATUS_REVIEWING, STATUS_VALIDATING,
    STATUS_ACCEPTED, STATUS_REJECTED, STATUS_ARCHIVED,
    STATUS_NEEDS_MORE_EVIDENCE,
]

# --- Priorities ---
PRIORITY_P0 = "P0"
PRIORITY_P1 = "P1"
PRIORITY_P2 = "P2"
PRIORITY_P3 = "P3"

ALL_PRIORITIES = [PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3]

# --- Source Modules ---
SOURCE_RESEARCH_INTELLIGENCE = "research_intelligence"
SOURCE_STRATEGY_KNOWLEDGE    = "strategy_knowledge"
SOURCE_RULE_GOVERNANCE       = "rule_governance"
SOURCE_REPLAY_TRAINING       = "replay_training"
SOURCE_PORTFOLIO_JOURNAL     = "portfolio_journal"
SOURCE_DATA_COVERAGE         = "data_coverage"
SOURCE_REPORT_PACK           = "report_pack"
SOURCE_REGRESSION            = "regression"
SOURCE_STABLE_RELEASE        = "stable_release"
SOURCE_RESEARCH_COACH        = "research_coach"
SOURCE_MANUAL                = "manual"

ALL_SOURCE_MODULES = [
    SOURCE_RESEARCH_INTELLIGENCE, SOURCE_STRATEGY_KNOWLEDGE,
    SOURCE_RULE_GOVERNANCE, SOURCE_REPLAY_TRAINING,
    SOURCE_PORTFOLIO_JOURNAL, SOURCE_DATA_COVERAGE,
    SOURCE_REPORT_PACK, SOURCE_REGRESSION,
    SOURCE_STABLE_RELEASE, SOURCE_RESEARCH_COACH, SOURCE_MANUAL,
]

# --- Relation Types ---
RELATION_SUPPORTS         = "SUPPORTS"
RELATION_CONTRADICTS      = "CONTRADICTS"
RELATION_DUPLICATES       = "DUPLICATES"
RELATION_REFINES          = "REFINES"
RELATION_REQUIRES_DATA    = "REQUIRES_DATA"
RELATION_REQUIRES_BACKTEST = "REQUIRES_BACKTEST"
RELATION_REQUIRES_REPLAY  = "REQUIRES_REPLAY"
RELATION_RELATED_TO       = "RELATED_TO"

ALL_RELATION_TYPES = [
    RELATION_SUPPORTS, RELATION_CONTRADICTS, RELATION_DUPLICATES,
    RELATION_REFINES, RELATION_REQUIRES_DATA, RELATION_REQUIRES_BACKTEST,
    RELATION_REQUIRES_REPLAY, RELATION_RELATED_TO,
]

# --- Forbidden strings (safety guard) ---
_FORBIDDEN = ["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE"]

def _guard(text: str) -> str:
    """Raise if text contains forbidden trading action keywords."""
    if text:
        upper = text.upper()
        for f in _FORBIDDEN:
            if f in upper:
                raise ValueError(
                    f"Forbidden keyword '{f}' detected. "
                    "Strategy Memory is Research Only — no trading actions allowed."
                )
    return text


@dataclass
class StrategyMemoryItem:
    """A single research memory item. Research Only. No Real Orders."""

    memory_id:                  str       = field(default_factory=lambda: str(uuid.uuid4())[:12])
    memory_type:                str       = STATUS_NEW
    title:                      str       = ""
    summary:                    str       = ""
    status:                     str       = STATUS_NEW
    confidence:                 float     = 0.5
    priority:                   str       = PRIORITY_P2
    source_module:              str       = SOURCE_MANUAL
    source_ref:                 str       = ""
    related_symbols:            List[str] = field(default_factory=list)
    related_strategies:         List[str] = field(default_factory=list)
    related_rules:              List[str] = field(default_factory=list)
    related_replay_sessions:    List[str] = field(default_factory=list)
    related_reports:            List[str] = field(default_factory=list)
    related_data_gaps:          List[str] = field(default_factory=list)
    evidence:                   str       = ""
    hypothesis:                 str       = ""
    validation_plan:            str       = ""
    suggested_commands:         List[str] = field(default_factory=list)
    risk_notes:                 str       = ""
    created_at:                 str       = field(default_factory=lambda: datetime.now().isoformat())
    updated_at:                 str       = field(default_factory=lambda: datetime.now().isoformat())
    last_seen_at:               str       = field(default_factory=lambda: datetime.now().isoformat())
    seen_count:                 int       = 1
    archived:                   bool      = False
    read_only:                  bool      = True
    no_real_orders:             bool      = True
    production_blocked:         bool      = True

    def __post_init__(self):
        _guard(self.title)
        _guard(self.summary)
        _guard(self.hypothesis)
        _guard(self.evidence)
        for cmd in self.suggested_commands:
            _guard(cmd)

    def to_dict(self) -> dict:
        d = asdict(self)
        for lst_key in ["related_symbols", "related_strategies", "related_rules",
                        "related_replay_sessions", "related_reports",
                        "related_data_gaps", "suggested_commands"]:
            if isinstance(d[lst_key], list):
                d[lst_key] = "|".join(d[lst_key])
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyMemoryItem":
        d = dict(d)
        for lst_key in ["related_symbols", "related_strategies", "related_rules",
                        "related_replay_sessions", "related_reports",
                        "related_data_gaps", "suggested_commands"]:
            val = d.get(lst_key, "")
            if isinstance(val, str):
                d[lst_key] = [x for x in val.split("|") if x]
            elif val is None:
                d[lst_key] = []
        for bool_key in ["archived", "read_only", "no_real_orders", "production_blocked"]:
            if isinstance(d.get(bool_key), str):
                d[bool_key] = d[bool_key].lower() in ("true", "1", "yes")
        for float_key in ["confidence"]:
            if isinstance(d.get(float_key), str):
                try:
                    d[float_key] = float(d[float_key])
                except (ValueError, TypeError):
                    d[float_key] = 0.5
        for int_key in ["seen_count"]:
            if isinstance(d.get(int_key), str):
                try:
                    d[int_key] = int(d[int_key])
                except (ValueError, TypeError):
                    d[int_key] = 1
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class StrategyMemoryLink:
    """Link between two memory items or a memory item and an external resource."""

    link_id:          str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    source_memory_id: str = ""
    target_type:      str = ""
    target_id:        str = ""
    relation_type:    str = RELATION_RELATED_TO
    description:      str = ""
    created_at:       str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyMemoryLink":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class StrategyMemorySummary:
    """Aggregate summary of the strategy memory store."""

    generated_at:              str   = field(default_factory=lambda: datetime.now().isoformat())
    total_memories:            int   = 0
    active_count:              int   = 0
    archived_count:            int   = 0
    new_count:                 int   = 0
    reviewing_count:           int   = 0
    validating_count:          int   = 0
    accepted_count:            int   = 0
    rejected_count:            int   = 0
    needs_more_evidence_count: int   = 0
    p0_count:                  int   = 0
    p1_count:                  int   = 0
    duplicate_count:           int   = 0
    top_memory:                str   = ""
    overall_status:            str   = "OK"
    no_real_orders:            bool  = True
    production_blocked:        bool  = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyMemorySummary":
        d = dict(d)
        for bool_key in ["no_real_orders", "production_blocked"]:
            if isinstance(d.get(bool_key), str):
                d[bool_key] = d[bool_key].lower() in ("true", "1", "yes")
        for int_key in ["total_memories", "active_count", "archived_count", "new_count",
                        "reviewing_count", "validating_count", "accepted_count",
                        "rejected_count", "needs_more_evidence_count",
                        "p0_count", "p1_count", "duplicate_count"]:
            if isinstance(d.get(int_key), str):
                try:
                    d[int_key] = int(d[int_key])
                except (ValueError, TypeError):
                    d[int_key] = 0
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
