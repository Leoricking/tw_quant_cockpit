"""
coach/coach_schema.py — Research Assistant / Coach Schema (v0.4.8).

Defines CoachRecommendation dataclass.

[!] Coaching Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] suggested_command must be research-only. No buy/sell/order.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

# ---------------------------------------------------------------------------
# recommendation_type constants
# ---------------------------------------------------------------------------
REC_DAILY_CHECKLIST        = "daily_checklist"
REC_WEEKLY_CHECKLIST       = "weekly_checklist"
REC_REPLAY_TRAINING        = "replay_training"
REC_RULE_REVIEW            = "rule_review"
REC_DATA_REPAIR            = "data_repair"
REC_JOURNAL_REVIEW         = "journal_review"
REC_EXPERIMENT_REVIEW      = "experiment_review"
REC_MODEL_MONITORING_REVIEW = "model_monitoring_review"
REC_SIGNAL_QUALITY_REVIEW  = "signal_quality_review"
REC_SAFETY_CHECK           = "safety_check"
REC_LEARNING_NOTE          = "learning_note"

ALL_REC_TYPES = [
    REC_DAILY_CHECKLIST, REC_WEEKLY_CHECKLIST, REC_REPLAY_TRAINING,
    REC_RULE_REVIEW, REC_DATA_REPAIR, REC_JOURNAL_REVIEW,
    REC_EXPERIMENT_REVIEW, REC_MODEL_MONITORING_REVIEW,
    REC_SIGNAL_QUALITY_REVIEW, REC_SAFETY_CHECK, REC_LEARNING_NOTE,
]

# ---------------------------------------------------------------------------
# priority constants
# ---------------------------------------------------------------------------
PRIORITY_P0 = "P0"
PRIORITY_P1 = "P1"
PRIORITY_P2 = "P2"
PRIORITY_P3 = "P3"

ALL_PRIORITIES = [PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3]

# ---------------------------------------------------------------------------
# category constants
# ---------------------------------------------------------------------------
CAT_PROCESS    = "process"
CAT_DATA       = "data"
CAT_PROVIDER   = "provider"
CAT_RULE       = "rule"
CAT_MODEL      = "model"
CAT_REPLAY     = "replay"
CAT_JOURNAL    = "journal"
CAT_EXPERIMENT = "experiment"
CAT_SAFETY     = "safety"
CAT_WORKFLOW   = "workflow"
CAT_LEARNING   = "learning"

ALL_CATEGORIES = [
    CAT_PROCESS, CAT_DATA, CAT_PROVIDER, CAT_RULE, CAT_MODEL,
    CAT_REPLAY, CAT_JOURNAL, CAT_EXPERIMENT, CAT_SAFETY,
    CAT_WORKFLOW, CAT_LEARNING,
]

# ---------------------------------------------------------------------------
# status constants
# ---------------------------------------------------------------------------
STATUS_OPEN        = "OPEN"
STATUS_IN_PROGRESS = "IN_PROGRESS"
STATUS_DONE        = "DONE"
STATUS_DISMISSED   = "DISMISSED"
STATUS_ARCHIVED    = "ARCHIVED"

ALL_STATUSES = [STATUS_OPEN, STATUS_IN_PROGRESS, STATUS_DONE, STATUS_DISMISSED, STATUS_ARCHIVED]

# ---------------------------------------------------------------------------
# effort_level constants
# ---------------------------------------------------------------------------
EFFORT_QUICK  = "quick"
EFFORT_MEDIUM = "medium"
EFFORT_DEEP   = "deep"

# ---------------------------------------------------------------------------
# due_type constants
# ---------------------------------------------------------------------------
DUE_TODAY      = "today"
DUE_THIS_WEEK  = "this_week"
DUE_BACKLOG    = "backlog"

# ---------------------------------------------------------------------------
# Forbidden keywords in suggested commands
# ---------------------------------------------------------------------------
_FORBIDDEN_KEYWORDS = [
    "buy", "sell", "order", "submit_order", "place_order",
    "broker", "shioaji order", "live trade", "auto trade",
    "execute trade",
]


def _safe_command(cmd: str) -> str:
    """Block any forbidden trading command."""
    low = cmd.lower()
    for kw in _FORBIDDEN_KEYWORDS:
        if kw in low:
            return "# BLOCKED: no trading commands allowed"
    return cmd


# ---------------------------------------------------------------------------
# CoachRecommendation
# ---------------------------------------------------------------------------

@dataclass
class CoachRecommendation:
    """
    A single Research Coach recommendation.

    Safety invariants (always True):
      read_only          = True
      no_real_orders     = True
      production_blocked = True
      suggested_command  = research-only (validated in __post_init__)
    """

    # Identity
    coach_id:   str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    # Classification
    recommendation_type: str = REC_DAILY_CHECKLIST
    priority:            str = PRIORITY_P3
    category:            str = CAT_WORKFLOW

    # Description
    title:            str = ""
    summary:          str = ""
    rationale:        str = ""
    source:           str = ""

    # Related objects (all optional)
    related_review_id:         Optional[str] = None
    related_journal_id:        Optional[str] = None
    related_rule_id:           Optional[str] = None
    related_experiment_id:     Optional[str] = None
    related_replay_session_id: Optional[str] = None
    related_report:            Optional[str] = None

    # Action
    suggested_action:  str = ""
    suggested_command: str = ""
    expected_benefit:  str = ""
    risk_if_ignored:   str = ""
    effort_level:      str = EFFORT_QUICK
    due_type:          str = DUE_TODAY

    # State
    status: str = STATUS_OPEN

    # Metadata
    tags: List[str] = field(default_factory=list)

    # Safety flags — always True
    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __post_init__(self):
        # Safety: block forbidden commands
        self.suggested_command = _safe_command(self.suggested_command)

    def to_dict(self) -> dict:
        """Serialize to plain dict (JSON-safe)."""
        return {
            "coach_id":                 self.coach_id,
            "created_at":               self.created_at,
            "recommendation_type":      self.recommendation_type,
            "priority":                 self.priority,
            "category":                 self.category,
            "title":                    self.title,
            "summary":                  self.summary,
            "rationale":                self.rationale,
            "source":                   self.source,
            "related_review_id":        self.related_review_id,
            "related_journal_id":       self.related_journal_id,
            "related_rule_id":          self.related_rule_id,
            "related_experiment_id":    self.related_experiment_id,
            "related_replay_session_id": self.related_replay_session_id,
            "related_report":           self.related_report,
            "suggested_action":         self.suggested_action,
            "suggested_command":        self.suggested_command,
            "expected_benefit":         self.expected_benefit,
            "risk_if_ignored":          self.risk_if_ignored,
            "effort_level":             self.effort_level,
            "due_type":                 self.due_type,
            "status":                   self.status,
            "tags":                     "|".join(self.tags) if self.tags else "",
            "read_only":                self.read_only,
            "no_real_orders":           self.no_real_orders,
            "production_blocked":       self.production_blocked,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CoachRecommendation":
        tags_raw = d.get("tags", "")
        tags = [t for t in tags_raw.split("|") if t] if isinstance(tags_raw, str) else list(tags_raw)
        return cls(
            coach_id=d.get("coach_id", str(uuid.uuid4())[:12]),
            created_at=d.get("created_at", datetime.now().isoformat(timespec="seconds")),
            recommendation_type=d.get("recommendation_type", REC_DAILY_CHECKLIST),
            priority=d.get("priority", PRIORITY_P3),
            category=d.get("category", CAT_WORKFLOW),
            title=d.get("title", ""),
            summary=d.get("summary", ""),
            rationale=d.get("rationale", ""),
            source=d.get("source", ""),
            related_review_id=d.get("related_review_id"),
            related_journal_id=d.get("related_journal_id"),
            related_rule_id=d.get("related_rule_id"),
            related_experiment_id=d.get("related_experiment_id"),
            related_replay_session_id=d.get("related_replay_session_id"),
            related_report=d.get("related_report"),
            suggested_action=d.get("suggested_action", ""),
            suggested_command=d.get("suggested_command", ""),
            expected_benefit=d.get("expected_benefit", ""),
            risk_if_ignored=d.get("risk_if_ignored", ""),
            effort_level=d.get("effort_level", EFFORT_QUICK),
            due_type=d.get("due_type", DUE_TODAY),
            status=d.get("status", STATUS_OPEN),
            tags=tags,
            read_only=True,
            no_real_orders=True,
            production_blocked=True,
        )
