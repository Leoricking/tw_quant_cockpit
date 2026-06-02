"""
review/review_schema.py — Research Review Dashboard Schema (v0.4.7).

Defines ReviewItem dataclass for the Research Review Dashboard.

[!] Review Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No broker IDs. No real-order execution. No token storage.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

# ---------------------------------------------------------------------------
# review_type constants
# ---------------------------------------------------------------------------
REVIEW_TYPE_DAILY            = "daily_review"
REVIEW_TYPE_WEEKLY           = "weekly_review"
REVIEW_TYPE_MISTAKE          = "mistake_review"
REVIEW_TYPE_WEAK_RULE        = "weak_rule_review"
REVIEW_TYPE_DATA_BLOCKER     = "data_blocker_review"
REVIEW_TYPE_PROVIDER         = "provider_review"
REVIEW_TYPE_MODEL_MONITORING = "model_monitoring_review"
REVIEW_TYPE_REPLAY_TRAINING  = "replay_training_review"
REVIEW_TYPE_SIGNAL_QUALITY   = "signal_quality_review"
REVIEW_TYPE_JOURNAL          = "journal_review"
REVIEW_TYPE_EXPERIMENT       = "experiment_review"
REVIEW_TYPE_SAFETY           = "safety_review"

ALL_REVIEW_TYPES = [
    REVIEW_TYPE_DAILY,
    REVIEW_TYPE_WEEKLY,
    REVIEW_TYPE_MISTAKE,
    REVIEW_TYPE_WEAK_RULE,
    REVIEW_TYPE_DATA_BLOCKER,
    REVIEW_TYPE_PROVIDER,
    REVIEW_TYPE_MODEL_MONITORING,
    REVIEW_TYPE_REPLAY_TRAINING,
    REVIEW_TYPE_SIGNAL_QUALITY,
    REVIEW_TYPE_JOURNAL,
    REVIEW_TYPE_EXPERIMENT,
    REVIEW_TYPE_SAFETY,
]

# ---------------------------------------------------------------------------
# severity constants
# ---------------------------------------------------------------------------
SEV_INFO     = "INFO"
SEV_NOTICE   = "NOTICE"
SEV_WARNING  = "WARNING"
SEV_ERROR    = "ERROR"
SEV_CRITICAL = "CRITICAL"
SEV_BLOCKED  = "BLOCKED"

ALL_SEVERITIES = [SEV_INFO, SEV_NOTICE, SEV_WARNING, SEV_ERROR, SEV_CRITICAL, SEV_BLOCKED]

_SEV_RANK = {s: i for i, s in enumerate(ALL_SEVERITIES)}


def severity_gte(a: str, b: str) -> bool:
    """Return True if severity a >= b."""
    return _SEV_RANK.get(a, 0) >= _SEV_RANK.get(b, 0)


# ---------------------------------------------------------------------------
# category constants
# ---------------------------------------------------------------------------
CAT_MISTAKE      = "mistake"
CAT_RULE         = "rule"
CAT_DATA         = "data"
CAT_PROVIDER     = "provider"
CAT_MODEL        = "model"
CAT_REPLAY       = "replay"
CAT_JOURNAL      = "journal"
CAT_NOTIFICATION = "notification"
CAT_EXPERIMENT   = "experiment"
CAT_SAFETY       = "safety"
CAT_WORKFLOW     = "workflow"
CAT_REPORT       = "report"

ALL_CATEGORIES = [
    CAT_MISTAKE, CAT_RULE, CAT_DATA, CAT_PROVIDER, CAT_MODEL,
    CAT_REPLAY, CAT_JOURNAL, CAT_NOTIFICATION, CAT_EXPERIMENT,
    CAT_SAFETY, CAT_WORKFLOW, CAT_REPORT,
]

# ---------------------------------------------------------------------------
# status constants
# ---------------------------------------------------------------------------
STATUS_OPEN        = "OPEN"
STATUS_IN_PROGRESS = "IN_PROGRESS"
STATUS_REVIEWED    = "REVIEWED"
STATUS_DISMISSED   = "DISMISSED"
STATUS_ARCHIVED    = "ARCHIVED"

ALL_STATUSES = [STATUS_OPEN, STATUS_IN_PROGRESS, STATUS_REVIEWED, STATUS_DISMISSED, STATUS_ARCHIVED]


# ---------------------------------------------------------------------------
# ReviewItem
# ---------------------------------------------------------------------------

@dataclass
class ReviewItem:
    """
    A single research review item produced by the ResearchReviewAggregator.

    Safety invariants (always True):
      read_only          = True
      no_real_orders     = True
      production_blocked = True
    """

    # Identity
    review_id:   str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    created_at:  str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    # Classification
    review_type: str = REVIEW_TYPE_DAILY
    severity:    str = SEV_INFO
    category:    str = CAT_WORKFLOW

    # Description
    title:             str = ""
    summary:           str = ""
    source:            str = ""
    source_module:     str = ""

    # Related objects (all optional)
    related_symbol:            Optional[str] = None
    related_rule_id:           Optional[str] = None
    related_experiment_id:     Optional[str] = None
    related_journal_id:        Optional[str] = None
    related_notification_id:   Optional[str] = None
    related_replay_session_id: Optional[str] = None
    related_report:            Optional[str] = None

    # Action
    action_required:    bool = False
    recommended_action: str  = ""

    # State
    status:   str  = STATUS_OPEN
    priority: int  = 3

    # Metadata
    tags: List[str] = field(default_factory=list)

    # Safety flags — always True, never override
    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        """Serialize to plain dict (JSON-safe)."""
        return {
            "review_id":                self.review_id,
            "created_at":               self.created_at,
            "review_type":              self.review_type,
            "severity":                 self.severity,
            "category":                 self.category,
            "title":                    self.title,
            "summary":                  self.summary,
            "source":                   self.source,
            "source_module":            self.source_module,
            "related_symbol":           self.related_symbol,
            "related_rule_id":          self.related_rule_id,
            "related_experiment_id":    self.related_experiment_id,
            "related_journal_id":       self.related_journal_id,
            "related_notification_id":  self.related_notification_id,
            "related_replay_session_id": self.related_replay_session_id,
            "related_report":           self.related_report,
            "action_required":          self.action_required,
            "recommended_action":       self.recommended_action,
            "status":                   self.status,
            "priority":                 self.priority,
            "tags":                     "|".join(self.tags) if self.tags else "",
            "read_only":                self.read_only,
            "no_real_orders":           self.no_real_orders,
            "production_blocked":       self.production_blocked,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ReviewItem":
        """Deserialize from dict."""
        tags_raw = d.get("tags", "")
        tags = [t for t in tags_raw.split("|") if t] if isinstance(tags_raw, str) else list(tags_raw)
        return cls(
            review_id=d.get("review_id", str(uuid.uuid4())[:12]),
            created_at=d.get("created_at", datetime.now().isoformat(timespec="seconds")),
            review_type=d.get("review_type", REVIEW_TYPE_DAILY),
            severity=d.get("severity", SEV_INFO),
            category=d.get("category", CAT_WORKFLOW),
            title=d.get("title", ""),
            summary=d.get("summary", ""),
            source=d.get("source", ""),
            source_module=d.get("source_module", ""),
            related_symbol=d.get("related_symbol"),
            related_rule_id=d.get("related_rule_id"),
            related_experiment_id=d.get("related_experiment_id"),
            related_journal_id=d.get("related_journal_id"),
            related_notification_id=d.get("related_notification_id"),
            related_replay_session_id=d.get("related_replay_session_id"),
            related_report=d.get("related_report"),
            action_required=bool(d.get("action_required", False)),
            recommended_action=d.get("recommended_action", ""),
            status=d.get("status", STATUS_OPEN),
            priority=int(d.get("priority", 3)),
            tags=tags,
            read_only=True,
            no_real_orders=True,
            production_blocked=True,
        )
