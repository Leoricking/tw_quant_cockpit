"""
evidence_graph/evidence_graph_schema.py — Evidence Graph Schema v0.8.3

Defines EvidenceNode, EvidenceEdge, EvidenceGraphSummary dataclasses.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] No BUY / SELL / ORDER / EXECUTE / SUBMIT_ORDER / AUTO_TRADE / REAL_TRADE output.
"""

from __future__ import annotations

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
                        "related_reports", "related_memories", "related_tasks"):
            if isinstance(d[lst_key], list):
                d[lst_key] = "|".join(d[lst_key])
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "EvidenceNode":
        d2 = dict(d)
        for lst_key in ("related_symbols", "related_strategies", "related_rules",
                        "related_reports", "related_memories", "related_tasks"):
            v = d2.get(lst_key, "")
            if isinstance(v, str):
                d2[lst_key] = [x for x in v.split("|") if x]
            elif not isinstance(v, list):
                d2[lst_key] = []
        for bool_key in ("read_only", "no_real_orders", "production_blocked"):
            v = d2.get(bool_key, True)
            if isinstance(v, str):
                d2[bool_key] = v.lower() not in ("false", "0", "")
        try:
            d2["confidence"] = float(d2.get("confidence", 0.5))
        except (TypeError, ValueError):
            d2["confidence"] = 0.5
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
        for bool_key in ("read_only", "no_real_orders", "production_blocked"):
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
