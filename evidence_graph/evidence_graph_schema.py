"""
evidence_graph/evidence_graph_schema.py — Evidence Graph Schema v0.8.3

Defines EvidenceNode, EvidenceEdge, EvidenceGraphSummary dataclasses.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] No BUY / SELL / ORDER / EXECUTE / SUBMIT_ORDER / AUTO_TRADE / REAL_TRADE output.
"""

from __future__ import annotations

import dataclasses
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Node type constants
# ---------------------------------------------------------------------------
NODE_RESEARCH_RECOMMENDATION = "RESEARCH_RECOMMENDATION"
NODE_STRATEGY_MEMORY         = "STRATEGY_MEMORY"
NODE_BACKTEST_COACH_TASK     = "BACKTEST_COACH_TASK"
NODE_TRAINING_METRIC         = "TRAINING_METRIC"
NODE_REPLAY_MISTAKE          = "REPLAY_MISTAKE"
NODE_JOURNAL_PATTERN         = "JOURNAL_PATTERN"
NODE_DATA_GAP                = "DATA_GAP"
NODE_REPORT_RESULT           = "REPORT_RESULT"
NODE_REGRESSION_RESULT       = "REGRESSION_RESULT"
NODE_RULE_CANDIDATE          = "RULE_CANDIDATE"
NODE_STRATEGY_HYPOTHESIS     = "STRATEGY_HYPOTHESIS"
NODE_PROVIDER_LIMITATION     = "PROVIDER_LIMITATION"
NODE_STABLE_CHECK            = "STABLE_CHECK"
NODE_MANUAL_NOTE             = "MANUAL_NOTE"

ALL_NODE_TYPES = [
    NODE_RESEARCH_RECOMMENDATION, NODE_STRATEGY_MEMORY, NODE_BACKTEST_COACH_TASK,
    NODE_TRAINING_METRIC, NODE_REPLAY_MISTAKE, NODE_JOURNAL_PATTERN,
    NODE_DATA_GAP, NODE_REPORT_RESULT, NODE_REGRESSION_RESULT,
    NODE_RULE_CANDIDATE, NODE_STRATEGY_HYPOTHESIS, NODE_PROVIDER_LIMITATION,
    NODE_STABLE_CHECK, NODE_MANUAL_NOTE,
]

# ---------------------------------------------------------------------------
# Edge relation type constants
# ---------------------------------------------------------------------------
EDGE_SUPPORTS               = "SUPPORTS"
EDGE_CONTRADICTS            = "CONTRADICTS"
EDGE_DUPLICATES             = "DUPLICATES"
EDGE_REFINES                = "REFINES"
EDGE_REQUIRES_DATA          = "REQUIRES_DATA"
EDGE_REQUIRES_BACKTEST      = "REQUIRES_BACKTEST"
EDGE_REQUIRES_REPLAY        = "REQUIRES_REPLAY"
EDGE_REQUIRES_JOURNAL_REVIEW = "REQUIRES_JOURNAL_REVIEW"
EDGE_GENERATED_FROM         = "GENERATED_FROM"
EDGE_VALIDATED_BY           = "VALIDATED_BY"
EDGE_WEAKENED_BY            = "WEAKENED_BY"
EDGE_RELATED_TO             = "RELATED_TO"

ALL_EDGE_TYPES = [
    EDGE_SUPPORTS, EDGE_CONTRADICTS, EDGE_DUPLICATES, EDGE_REFINES,
    EDGE_REQUIRES_DATA, EDGE_REQUIRES_BACKTEST, EDGE_REQUIRES_REPLAY,
    EDGE_REQUIRES_JOURNAL_REVIEW, EDGE_GENERATED_FROM, EDGE_VALIDATED_BY,
    EDGE_WEAKENED_BY, EDGE_RELATED_TO,
]

# ---------------------------------------------------------------------------
# v0.9.1 Thread quality labels
# ---------------------------------------------------------------------------
THREAD_STRONG_EVIDENCE = "STRONG_EVIDENCE"
THREAD_PARTIAL_EVIDENCE = "PARTIAL_EVIDENCE"
THREAD_NEEDS_DATA = "NEEDS_DATA"
THREAD_NEEDS_BACKTEST = "NEEDS_BACKTEST"
THREAD_CONFLICTED = "CONFLICTED"
THREAD_ORPHANED = "ORPHANED"

# v0.9.1 Gap types
GAP_ORPHAN_NODE = "ORPHAN_NODE"
GAP_REQUIRES_DATA = "REQUIRES_DATA"
GAP_REQUIRES_BACKTEST = "REQUIRES_BACKTEST"
GAP_REQUIRES_REPLAY = "REQUIRES_REPLAY"
GAP_CONTRADICTION = "CONTRADICTION"
GAP_LOW_CONFIDENCE_EDGE = "LOW_CONFIDENCE_EDGE"
GAP_DUPLICATE_CLUSTER = "DUPLICATE_CLUSTER"

# v0.9.1 Crash stages
CRASH_STAGE_CRASH_CAUSE = "CRASH_CAUSE"
CRASH_STAGE_STABILIZATION = "STABILIZATION"
CRASH_STAGE_RELATIVE_STRENGTH = "RELATIVE_STRENGTH"
CRASH_STAGE_EPS_DIP_FILTER = "EPS_DIP_FILTER"
CRASH_STAGE_MA_PROFIT_DISCIPLINE = "MA_PROFIT_DISCIPLINE"
CRASH_STAGE_HIGH_RISK_GUARD = "HIGH_RISK_GUARD"

# v0.9.1 Safe next steps
SAFE_NEXT_STEPS = frozenset([
    "REVIEW", "TRACE_EVIDENCE", "VALIDATE", "BACKTEST_MORE",
    "PRACTICE_REPLAY", "REVIEW_JOURNAL", "FIX_DATA", "READ_REPORT",
    "WAIT", "REVIEW_RISK", "REVIEW_EARNINGS", "REVIEW_CHIPS",
    "BUILD_WATCHLIST", "DO_NOT_CHASE"
])

# ---------------------------------------------------------------------------
# Safety guard — forbidden trading actions
# ---------------------------------------------------------------------------
_FORBIDDEN_ACTION_TOKENS = frozenset([
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE"
])
_SAFETY_DECLARATION_TOKENS = frozenset([
    "NO REAL ORDERS", "NO_REAL_ORDERS", "RESEARCH ONLY", "PRODUCTION BLOCKED",
    "PRODUCTION_BLOCKED", "NOT INVESTMENT ADVICE",
])

def _guard(text: str, field_name: str = "field") -> str:
    """Raise ValueError if a forbidden trading action token appears in an action field."""
    if not text:
        return text
    upper = text.upper()
    for token in _FORBIDDEN_ACTION_TOKENS:
        pattern = r'\b' + re.escape(token) + r'\b'
        if re.search(pattern, upper):
            # Allow if it's part of a safety declaration phrase
            is_safety = any(decl in upper for decl in _SAFETY_DECLARATION_TOKENS)
            if not is_safety:
                raise ValueError(
                    f"[EvidenceGraph] SAFETY GUARD: forbidden action '{token}' "
                    f"detected in {field_name}. No trading actions allowed."
                )
    return text


# ---------------------------------------------------------------------------
# EvidenceNode
# ---------------------------------------------------------------------------
@dataclass
class EvidenceNode:
    """A single node in the Research Intelligence Evidence Graph.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """
    node_id:            str
    node_type:          str
    title:              str
    summary:            str
    source_module:      str
    source_ref:         str        = ""
    status:             str        = "ACTIVE"
    confidence:         float      = 0.5
    priority:           str        = "MEDIUM"
    related_symbols:    List[str]  = field(default_factory=list)
    related_strategies: List[str]  = field(default_factory=list)
    related_rules:      List[str]  = field(default_factory=list)
    related_reports:    List[str]  = field(default_factory=list)
    related_memories:   List[str]  = field(default_factory=list)
    related_tasks:      List[str]  = field(default_factory=list)
    evidence_text:      str        = ""
    created_at:         str        = field(default_factory=lambda: datetime.now().isoformat())
    updated_at:         str        = field(default_factory=lambda: datetime.now().isoformat())
    # v0.9.1 UX optional fields
    display_title:           str        = ""
    node_group:              str        = ""
    crash_stage:             str        = ""
    evidence_quality:        str        = ""
    is_crash_reversal_node:  bool       = False
    is_orphan:               bool       = False
    neighbor_count:          int        = 0
    path_count:              int        = 0
    gap_tags:                List[str]  = field(default_factory=list)
    safe_next_step:          str        = ""
    read_only:          bool       = True
    no_real_orders:     bool       = True
    production_blocked: bool       = True

    def __post_init__(self) -> None:
        # Guard action fields for forbidden tokens
        _guard(self.summary, "summary")
        _guard(self.evidence_text, "evidence_text")

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        for lst_key in ("related_symbols", "related_strategies", "related_rules",
                        "related_reports", "related_memories", "related_tasks",
                        "gap_tags"):
            if isinstance(d[lst_key], list):
                d[lst_key] = "|".join(d[lst_key])
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "EvidenceNode":
        d2 = dict(d)
        for lst_key in ("related_symbols", "related_strategies", "related_rules",
                        "related_reports", "related_memories", "related_tasks",
                        "gap_tags"):
            v = d2.get(lst_key, "")
            if isinstance(v, str):
                d2[lst_key] = [x for x in v.split("|") if x]
            elif not isinstance(v, list):
                d2[lst_key] = []
        for bool_key in ("read_only", "no_real_orders", "production_blocked",
                         "is_crash_reversal_node", "is_orphan"):
            v = d2.get(bool_key, True)
            if isinstance(v, str):
                d2[bool_key] = v.lower() not in ("false", "0", "")
        try:
            d2["confidence"] = float(d2.get("confidence", 0.5))
        except (TypeError, ValueError):
            d2["confidence"] = 0.5
        for int_key in ("neighbor_count", "path_count"):
            try:
                d2[int_key] = int(d2.get(int_key, 0))
            except (TypeError, ValueError):
                d2[int_key] = 0
        return cls(**{k: v for k, v in d2.items() if k in cls.__dataclass_fields__})


# ---------------------------------------------------------------------------
# EvidenceEdge
# ---------------------------------------------------------------------------
@dataclass
class EvidenceEdge:
    """A directed relationship between two EvidenceNodes.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """
    edge_id:            str
    source_node_id:     str
    target_node_id:     str
    relation_type:      str
    confidence:         float  = 0.5
    description:        str    = ""
    evidence:           str    = ""
    suggested_next_step: str   = ""
    created_at:         str    = field(default_factory=lambda: datetime.now().isoformat())
    # v0.9.1 UX optional fields
    edge_group:           str   = ""
    path_role:            str   = ""
    is_low_confidence:    bool  = False
    is_contradiction:     bool  = False
    is_duplicate_link:    bool  = False
    safety_label:         str   = ""
    read_only:          bool   = True
    no_real_orders:     bool   = True
    production_blocked: bool   = True

    def __post_init__(self) -> None:
        _guard(self.suggested_next_step, "suggested_next_step")
        _guard(self.description, "description")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "EvidenceEdge":
        d2 = dict(d)
        for bool_key in ("read_only", "no_real_orders", "production_blocked",
                         "is_low_confidence", "is_contradiction", "is_duplicate_link"):
            v = d2.get(bool_key, True)
            if isinstance(v, str):
                d2[bool_key] = v.lower() not in ("false", "0", "")
        try:
            d2["confidence"] = float(d2.get("confidence", 0.5))
        except (TypeError, ValueError):
            d2["confidence"] = 0.5
        return cls(**{k: v for k, v in d2.items() if k in cls.__dataclass_fields__})


# ---------------------------------------------------------------------------
# EvidenceGraphSummary
# ---------------------------------------------------------------------------
@dataclass
class EvidenceGraphSummary:
    """Top-level summary of the Evidence Graph.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """
    generated_at:           str   = field(default_factory=lambda: datetime.now().isoformat())
    mode:                   str   = "real"
    total_nodes:            int   = 0
    total_edges:            int   = 0
    recommendation_nodes:   int   = 0
    memory_nodes:           int   = 0
    coach_task_nodes:       int   = 0
    metric_nodes:           int   = 0
    data_gap_nodes:         int   = 0
    report_nodes:           int   = 0
    contradiction_count:    int   = 0
    requires_data_count:    int   = 0
    requires_backtest_count: int  = 0
    requires_replay_count:  int   = 0
    orphan_node_count:      int   = 0
    high_confidence_links:  int   = 0
    low_confidence_links:   int   = 0
    overall_status:         str   = "INSUFFICIENT_EVIDENCE"
    top_evidence_thread:    str   = ""
    no_real_orders:         bool  = True
    production_blocked:     bool  = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "EvidenceGraphSummary":
        d2 = dict(d)
        for bool_key in ("no_real_orders", "production_blocked"):
            v = d2.get(bool_key, True)
            if isinstance(v, str):
                d2[bool_key] = v.lower() not in ("false", "0", "")
        for int_key in ("total_nodes", "total_edges", "recommendation_nodes",
                        "memory_nodes", "coach_task_nodes", "metric_nodes",
                        "data_gap_nodes", "report_nodes", "contradiction_count",
                        "requires_data_count", "requires_backtest_count",
                        "requires_replay_count", "orphan_node_count",
                        "high_confidence_links", "low_confidence_links"):
            try:
                d2[int_key] = int(d2.get(int_key, 0))
            except (TypeError, ValueError):
                d2[int_key] = 0
        return cls(**{k: v for k, v in d2.items() if k in cls.__dataclass_fields__})


# ---------------------------------------------------------------------------
# EvidenceThread (v0.9.1)
# ---------------------------------------------------------------------------
@dataclass
class EvidenceThread:
    """v0.9.1 — Evidence Thread with quality scoring. Research Only."""
    thread_id: str = ""
    title: str = ""
    summary: str = ""
    node_ids: List[str] = field(default_factory=list)
    edge_ids: List[str] = field(default_factory=list)
    node_count: int = 0
    edge_count: int = 0
    support_count: int = 0
    contradiction_count: int = 0
    requires_data_count: int = 0
    requires_backtest_count: int = 0
    requires_replay_count: int = 0
    quality_score: float = 0.0
    quality_label: str = "UNKNOWN"  # STRONG_EVIDENCE, PARTIAL_EVIDENCE, NEEDS_DATA, NEEDS_BACKTEST, CONFLICTED, ORPHANED
    suggested_next_step: str = "REVIEW"
    evidence_path: List[str] = field(default_factory=list)
    related_symbols: List[str] = field(default_factory=list)
    related_strategies: List[str] = field(default_factory=list)
    related_rules: List[str] = field(default_factory=list)
    source_modules: List[str] = field(default_factory=list)
    no_real_orders: bool = True
    production_blocked: bool = True

    _FORBIDDEN = frozenset(["BUY","SELL","ORDER","EXECUTE","SUBMIT_ORDER","AUTO_TRADE","REAL_TRADE"])

    def to_dict(self) -> dict:
        d = {}
        for f in dataclasses.fields(self):
            if f.name.startswith('_'):
                continue
            val = getattr(self, f.name)
            if isinstance(val, list):
                val = "|".join(str(v) for v in val)
            d[f.name] = val
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "EvidenceThread":
        init_fields = {f.name for f in dataclasses.fields(cls) if not f.name.startswith('_')}
        kwargs = {}
        for f in dataclasses.fields(cls):
            if f.name.startswith('_'):
                continue
            if f.name not in d:
                continue
            val = d[f.name]
            if f.name in ("node_ids","edge_ids","evidence_path","related_symbols","related_strategies","related_rules","source_modules","gap_tags"):
                if isinstance(val, str):
                    val = [v for v in val.split("|") if v] if val else []
            elif f.name in ("node_count","edge_count","support_count","contradiction_count","requires_data_count","requires_backtest_count","requires_replay_count"):
                try:
                    val = int(val)
                except (ValueError, TypeError):
                    val = 0
            elif f.name in ("quality_score",):
                try:
                    val = float(val)
                except (ValueError, TypeError):
                    val = 0.0
            elif f.name in ("no_real_orders","production_blocked"):
                val = str(val).lower() not in ("false","0","")
            kwargs[f.name] = val
        return cls(**{k: v for k, v in kwargs.items() if k in init_fields})


# ---------------------------------------------------------------------------
# EvidenceGraphGap (v0.9.1)
# ---------------------------------------------------------------------------
@dataclass
class EvidenceGraphGap:
    """v0.9.1 — Graph gap / weakness analysis result. Research Only."""
    gap_id: str = ""
    gap_type: str = ""  # ORPHAN_NODE, REQUIRES_DATA, REQUIRES_BACKTEST, REQUIRES_REPLAY, CONTRADICTION, LOW_CONFIDENCE_EDGE, DUPLICATE_CLUSTER
    title: str = ""
    description: str = ""
    affected_node_ids: List[str] = field(default_factory=list)
    affected_edge_ids: List[str] = field(default_factory=list)
    severity: str = "MEDIUM"  # LOW, MEDIUM, HIGH
    suggested_next_step: str = "REVIEW"
    source_module: str = ""
    no_real_orders: bool = True
    production_blocked: bool = True

    _FORBIDDEN = frozenset(["BUY","SELL","ORDER","EXECUTE","SUBMIT_ORDER","AUTO_TRADE","REAL_TRADE"])

    def to_dict(self) -> dict:
        d = {}
        for f in dataclasses.fields(self):
            if f.name.startswith('_'):
                continue
            val = getattr(self, f.name)
            if isinstance(val, list):
                val = "|".join(str(v) for v in val)
            d[f.name] = val
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "EvidenceGraphGap":
        init_fields = {f.name for f in dataclasses.fields(cls) if not f.name.startswith('_')}
        kwargs = {}
        for f in dataclasses.fields(cls):
            if f.name.startswith('_'):
                continue
            if f.name not in d:
                continue
            val = d[f.name]
            if f.name in ("affected_node_ids","affected_edge_ids"):
                if isinstance(val, str):
                    val = [v for v in val.split("|") if v] if val else []
            elif f.name in ("no_real_orders","production_blocked"):
                val = str(val).lower() not in ("false","0","")
            kwargs[f.name] = val
        return cls(**{k: v for k, v in kwargs.items() if k in init_fields})
