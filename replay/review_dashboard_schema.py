"""
replay/review_dashboard_schema.py — Replay Review Dashboard Schema v1.2.6

Dataclass-based schema for the replay review dashboard: snapshots, session rows,
queue items, progress records, and checklist items.

[!] Research Only. No Real Orders. Replay Training Only.
[!] No Auto Review Complete. No Auto Outcome Reveal. No Auto Confirm.
[!] No Auto Decision. No Auto Execution. No Score-to-Trade. Not Investment Advice.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
REPLAY_TRAINING_ONLY = True
NO_AUTO_REVIEW_COMPLETE = True
NO_AUTO_OUTCOME_REVEAL = True
NO_AUTO_CONFIRM = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}{uuid.uuid4().hex[:12].upper()}"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class QueueItemType(str, Enum):
    OUTCOME_REVEAL_PENDING       = "OUTCOME_REVEAL_PENDING"
    MISTAKE_REVIEW_PENDING       = "MISTAKE_REVIEW_PENDING"
    STRATEGY_RULE_REVIEW_PENDING = "STRATEGY_RULE_REVIEW_PENDING"
    TIMEFRAME_CONFLICT_REVIEW    = "TIMEFRAME_CONFLICT_REVIEW"
    LOW_CONFIDENCE_REVIEW        = "LOW_CONFIDENCE_REVIEW"
    INSUFFICIENT_DATA_REVIEW     = "INSUFFICIENT_DATA_REVIEW"
    POINT_IN_TIME_REVIEW         = "POINT_IN_TIME_REVIEW"
    REPORT_MISSING               = "REPORT_MISSING"
    SESSION_INCOMPLETE           = "SESSION_INCOMPLETE"
    OTHER                        = "OTHER"


class QueueItemPriority(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class QueueItemStatus(str, Enum):
    OPEN         = "OPEN"
    IN_REVIEW    = "IN_REVIEW"
    COMPLETED    = "COMPLETED"
    DISMISSED    = "DISMISSED"
    BLOCKED      = "BLOCKED"
    INSUFFICIENT = "INSUFFICIENT"


class ReviewProgressStatus(str, Enum):
    NOT_STARTED      = "NOT_STARTED"
    IN_PROGRESS      = "IN_PROGRESS"
    REVIEW_COMPLETE  = "REVIEW_COMPLETE"
    BLOCKED          = "BLOCKED"
    INSUFFICIENT     = "INSUFFICIENT"


# ---------------------------------------------------------------------------
# ReplayReviewQueueItem
# ---------------------------------------------------------------------------

@dataclass
class ReplayReviewQueueItem:
    """A single item in the replay review queue.

    [!] complete() does NOT auto-confirm mistakes or auto-reveal outcome.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """
    queue_item_id: str
    session_id: str
    queue_type: str                      # QueueItemType value
    priority: str                        # QueueItemPriority value
    status: str                          # QueueItemStatus value
    title: str                           = ""
    description: str                     = ""
    source_ref: Optional[str]            = None
    symbol: Optional[str]                = None
    scenario_id: Optional[str]           = None
    created_at: str                      = field(default_factory=_now_utc)
    started_at: Optional[str]            = None
    completed_at: Optional[str]          = None
    dismissed_at: Optional[str]          = None
    blocked_at: Optional[str]            = None
    note: str                            = ""
    dismiss_reason: str                  = ""
    block_reason: str                    = ""
    reopen_reason: str                   = ""
    history: List[Dict[str, Any]]        = field(default_factory=list)
    warnings: List[str]                  = field(default_factory=list)
    research_only: bool                  = True
    no_real_orders: bool                 = True
    auto_confirm_on_complete: bool       = False
    auto_reveal_on_complete: bool        = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "queue_item_id":            self.queue_item_id,
            "session_id":               self.session_id,
            "queue_type":               self.queue_type,
            "priority":                 self.priority,
            "status":                   self.status,
            "title":                    self.title,
            "description":              self.description,
            "source_ref":               self.source_ref,
            "symbol":                   self.symbol,
            "scenario_id":              self.scenario_id,
            "created_at":               self.created_at,
            "started_at":               self.started_at,
            "completed_at":             self.completed_at,
            "dismissed_at":             self.dismissed_at,
            "blocked_at":               self.blocked_at,
            "note":                     self.note,
            "dismiss_reason":           self.dismiss_reason,
            "block_reason":             self.block_reason,
            "reopen_reason":            self.reopen_reason,
            "history":                  self.history,
            "warnings":                 self.warnings,
            "research_only":            self.research_only,
            "no_real_orders":           self.no_real_orders,
            "auto_confirm_on_complete": self.auto_confirm_on_complete,
            "auto_reveal_on_complete":  self.auto_reveal_on_complete,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayReviewQueueItem":
        return cls(
            queue_item_id=d["queue_item_id"],
            session_id=d["session_id"],
            queue_type=d["queue_type"],
            priority=d["priority"],
            status=d["status"],
            title=d.get("title", ""),
            description=d.get("description", ""),
            source_ref=d.get("source_ref"),
            symbol=d.get("symbol"),
            scenario_id=d.get("scenario_id"),
            created_at=d.get("created_at", _now_utc()),
            started_at=d.get("started_at"),
            completed_at=d.get("completed_at"),
            dismissed_at=d.get("dismissed_at"),
            blocked_at=d.get("blocked_at"),
            note=d.get("note", ""),
            dismiss_reason=d.get("dismiss_reason", ""),
            block_reason=d.get("block_reason", ""),
            reopen_reason=d.get("reopen_reason", ""),
            history=d.get("history", []),
            warnings=d.get("warnings", []),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
            auto_confirm_on_complete=bool(d.get("auto_confirm_on_complete", False)),
            auto_reveal_on_complete=bool(d.get("auto_reveal_on_complete", False)),
        )


# ---------------------------------------------------------------------------
# ReplayReviewProgress
# ---------------------------------------------------------------------------

@dataclass
class ReplayReviewProgress:
    """Progress record for a single session review.

    [!] PROCESS_REVIEW_COMPLETE != FULL_REVIEW_COMPLETE.
    [!] Outcome Reveal is NOT required for PROCESS_REVIEW_COMPLETE.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """
    progress_id: str
    session_id: str
    status: str                              # ReviewProgressStatus value
    # Required steps
    session_completed: bool                  = False
    journal_exists: bool                     = False
    process_score_calculated: bool           = False
    suggested_mistakes_reviewed: bool        = False
    strategy_conflicts_reviewed: bool        = False
    timeframe_conflicts_reviewed: bool       = False
    point_in_time_verified: bool             = False
    review_note_added: bool                  = False
    # Optional steps
    outcome_revealed: bool                   = False
    outcome_score_calculated: bool           = False
    composite_score_calculated: bool         = False
    final_report_generated: bool             = False
    # Computed
    required_steps_complete: int             = 0
    required_steps_total: int                = 8
    optional_steps_complete: int             = 0
    optional_steps_total: int                = 4
    progress_percent: float                  = 0.0
    blocked_steps: List[str]                 = field(default_factory=list)
    missing_items: List[str]                 = field(default_factory=list)
    explanation: str                         = ""
    process_review_complete: bool            = False
    full_review_complete: bool               = False
    outcome_reveal_required: bool            = False
    calculated_at: str                       = field(default_factory=_now_utc)
    research_only: bool                      = True
    no_real_orders: bool                     = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "progress_id":                 self.progress_id,
            "session_id":                  self.session_id,
            "status":                      self.status,
            "session_completed":           self.session_completed,
            "journal_exists":              self.journal_exists,
            "process_score_calculated":    self.process_score_calculated,
            "suggested_mistakes_reviewed": self.suggested_mistakes_reviewed,
            "strategy_conflicts_reviewed": self.strategy_conflicts_reviewed,
            "timeframe_conflicts_reviewed": self.timeframe_conflicts_reviewed,
            "point_in_time_verified":      self.point_in_time_verified,
            "review_note_added":           self.review_note_added,
            "outcome_revealed":            self.outcome_revealed,
            "outcome_score_calculated":    self.outcome_score_calculated,
            "composite_score_calculated":  self.composite_score_calculated,
            "final_report_generated":      self.final_report_generated,
            "required_steps_complete":     self.required_steps_complete,
            "required_steps_total":        self.required_steps_total,
            "optional_steps_complete":     self.optional_steps_complete,
            "optional_steps_total":        self.optional_steps_total,
            "progress_percent":            self.progress_percent,
            "blocked_steps":               self.blocked_steps,
            "missing_items":               self.missing_items,
            "explanation":                 self.explanation,
            "process_review_complete":     self.process_review_complete,
            "full_review_complete":        self.full_review_complete,
            "outcome_reveal_required":     self.outcome_reveal_required,
            "calculated_at":               self.calculated_at,
            "research_only":               self.research_only,
            "no_real_orders":              self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayReviewProgress":
        return cls(
            progress_id=d["progress_id"],
            session_id=d["session_id"],
            status=d["status"],
            session_completed=bool(d.get("session_completed", False)),
            journal_exists=bool(d.get("journal_exists", False)),
            process_score_calculated=bool(d.get("process_score_calculated", False)),
            suggested_mistakes_reviewed=bool(d.get("suggested_mistakes_reviewed", False)),
            strategy_conflicts_reviewed=bool(d.get("strategy_conflicts_reviewed", False)),
            timeframe_conflicts_reviewed=bool(d.get("timeframe_conflicts_reviewed", False)),
            point_in_time_verified=bool(d.get("point_in_time_verified", False)),
            review_note_added=bool(d.get("review_note_added", False)),
            outcome_revealed=bool(d.get("outcome_revealed", False)),
            outcome_score_calculated=bool(d.get("outcome_score_calculated", False)),
            composite_score_calculated=bool(d.get("composite_score_calculated", False)),
            final_report_generated=bool(d.get("final_report_generated", False)),
            required_steps_complete=int(d.get("required_steps_complete", 0)),
            required_steps_total=int(d.get("required_steps_total", 8)),
            optional_steps_complete=int(d.get("optional_steps_complete", 0)),
            optional_steps_total=int(d.get("optional_steps_total", 4)),
            progress_percent=float(d.get("progress_percent", 0.0)),
            blocked_steps=d.get("blocked_steps", []),
            missing_items=d.get("missing_items", []),
            explanation=d.get("explanation", ""),
            process_review_complete=bool(d.get("process_review_complete", False)),
            full_review_complete=bool(d.get("full_review_complete", False)),
            outcome_reveal_required=bool(d.get("outcome_reveal_required", False)),
            calculated_at=d.get("calculated_at", _now_utc()),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


# ---------------------------------------------------------------------------
# ReplayReviewChecklistItem
# ---------------------------------------------------------------------------

@dataclass
class ReplayReviewChecklistItem:
    """A single item in the replay review checklist.

    [!] NOT auto-complete for Mistake Confirm / Outcome Reveal / Strategy Review Confirm.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """
    item_id: str
    session_id: str
    category: str
    label: str
    required: bool                           = True
    completed: bool                          = False
    blocked: bool                            = False
    blocked_reason: str                      = ""
    evidence_link: str                       = ""
    user_note: str                           = ""
    completed_at: Optional[str]              = None
    completion_history: List[Dict[str, Any]] = field(default_factory=list)
    auto_complete: bool                      = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id":            self.item_id,
            "session_id":         self.session_id,
            "category":           self.category,
            "label":              self.label,
            "required":           self.required,
            "completed":          self.completed,
            "blocked":            self.blocked,
            "blocked_reason":     self.blocked_reason,
            "evidence_link":      self.evidence_link,
            "user_note":          self.user_note,
            "completed_at":       self.completed_at,
            "completion_history": self.completion_history,
            "auto_complete":      self.auto_complete,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayReviewChecklistItem":
        return cls(
            item_id=d["item_id"],
            session_id=d["session_id"],
            category=d["category"],
            label=d["label"],
            required=bool(d.get("required", True)),
            completed=bool(d.get("completed", False)),
            blocked=bool(d.get("blocked", False)),
            blocked_reason=d.get("blocked_reason", ""),
            evidence_link=d.get("evidence_link", ""),
            user_note=d.get("user_note", ""),
            completed_at=d.get("completed_at"),
            completion_history=d.get("completion_history", []),
            auto_complete=bool(d.get("auto_complete", False)),
        )


# ---------------------------------------------------------------------------
# ReplayReviewSessionRow
# ---------------------------------------------------------------------------

@dataclass
class ReplayReviewSessionRow:
    """Summary row for a session in the review dashboard table.

    [!] outcome_score and composite_score hidden until outcome_revealed=True.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """
    session_id: str
    symbol: str
    scenario_id: Optional[str]       = None
    status: str                       = "UNKNOWN"
    review_progress: str              = "NOT_STARTED"
    process_score: Optional[float]    = None
    outcome_score: Optional[float]    = None
    composite_score: Optional[float]  = None
    classification: str               = "UNCLASSIFIED"
    mistake_count: int                = 0
    confirmed_mistake_count: int      = 0
    strategy_conflicts: int           = 0
    mtf_conflicts: int                = 0
    outcome_revealed: bool            = False
    pit_verified: bool                = False
    elapsed_seconds: float            = 0.0
    confidence: str                   = "INSUFFICIENT"
    warnings: List[str]               = field(default_factory=list)
    review_complete: bool             = False
    mode: str                         = "real"
    created_at: str                   = field(default_factory=_now_utc)
    updated_at: str                   = field(default_factory=_now_utc)
    research_only: bool               = True
    no_real_orders: bool              = True

    def to_dict(self) -> Dict[str, Any]:
        os_val = self.outcome_score if self.outcome_revealed else None
        cs_val = self.composite_score if self.outcome_revealed else None
        return {
            "session_id":              self.session_id,
            "symbol":                  self.symbol,
            "scenario_id":             self.scenario_id,
            "status":                  self.status,
            "review_progress":         self.review_progress,
            "process_score":           self.process_score,
            "outcome_score":           os_val,
            "outcome_score_hidden":    not self.outcome_revealed,
            "composite_score":         cs_val,
            "composite_score_hidden":  not self.outcome_revealed,
            "classification":          self.classification,
            "mistake_count":           self.mistake_count,
            "confirmed_mistake_count": self.confirmed_mistake_count,
            "strategy_conflicts":      self.strategy_conflicts,
            "mtf_conflicts":           self.mtf_conflicts,
            "outcome_revealed":        self.outcome_revealed,
            "pit_verified":            self.pit_verified,
            "elapsed_seconds":         self.elapsed_seconds,
            "confidence":              self.confidence,
            "warnings":                self.warnings,
            "review_complete":         self.review_complete,
            "mode":                    self.mode,
            "created_at":              self.created_at,
            "updated_at":              self.updated_at,
            "research_only":           self.research_only,
            "no_real_orders":          self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayReviewSessionRow":
        return cls(
            session_id=d["session_id"],
            symbol=d["symbol"],
            scenario_id=d.get("scenario_id"),
            status=d.get("status", "UNKNOWN"),
            review_progress=d.get("review_progress", "NOT_STARTED"),
            process_score=d.get("process_score"),
            outcome_score=d.get("outcome_score"),
            composite_score=d.get("composite_score"),
            classification=d.get("classification", "UNCLASSIFIED"),
            mistake_count=int(d.get("mistake_count", 0)),
            confirmed_mistake_count=int(d.get("confirmed_mistake_count", 0)),
            strategy_conflicts=int(d.get("strategy_conflicts", 0)),
            mtf_conflicts=int(d.get("mtf_conflicts", 0)),
            outcome_revealed=bool(d.get("outcome_revealed", False)),
            pit_verified=bool(d.get("pit_verified", False)),
            elapsed_seconds=float(d.get("elapsed_seconds", 0.0)),
            confidence=d.get("confidence", "INSUFFICIENT"),
            warnings=d.get("warnings", []),
            review_complete=bool(d.get("review_complete", False)),
            mode=d.get("mode", "real"),
            created_at=d.get("created_at", _now_utc()),
            updated_at=d.get("updated_at", _now_utc()),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


# ---------------------------------------------------------------------------
# ReplayReviewDashboardSnapshot
# ---------------------------------------------------------------------------

@dataclass
class ReplayReviewDashboardSnapshot:
    """Top-level snapshot of the replay review dashboard at a point in time.

    [!] Research Only. No Real Orders. No Auto Review Complete.
    [!] No Auto Outcome Reveal. No Auto Confirm. Not Investment Advice.
    """
    snapshot_id: str
    mode: str                                        # real / mock
    generated_at: str                                = field(default_factory=_now_utc)
    total_sessions: int                              = 0
    active_sessions: int                             = 0
    completed_sessions: int                          = 0
    archived_sessions: int                           = 0
    review_complete_sessions: int                    = 0
    review_incomplete_sessions: int                  = 0
    pending_outcome_reveal: int                      = 0
    pending_mistake_review: int                      = 0
    pending_strategy_review: int                     = 0
    pending_timeframe_review: int                    = 0
    low_confidence_count: int                        = 0
    insufficient_data_count: int                     = 0
    total_pending_queue: int                         = 0
    avg_process_score: Optional[float]               = None
    avg_outcome_score: Optional[float]               = None
    avg_composite_score: Optional[float]             = None
    suggested_mistakes: int                          = 0
    confirmed_mistakes: int                          = 0
    dismissed_mistakes: int                          = 0
    strategy_conflicts: int                          = 0
    strategy_warnings: int                           = 0
    timeframe_conflicts: int                         = 0
    pit_failures: int                                = 0
    firewall_blocks: int                             = 0
    total_review_elapsed_seconds: float              = 0.0
    avg_review_elapsed_seconds: float                = 0.0
    confidence: str                                  = "INSUFFICIENT"
    warnings: List[str]                              = field(default_factory=list)
    session_rows: List[Dict[str, Any]]               = field(default_factory=list)
    research_only: bool                              = True
    no_real_orders: bool                             = True
    auto_review_complete_enabled: bool               = False
    auto_outcome_reveal_enabled: bool                = False
    auto_mistake_confirmation_enabled: bool          = False
    auto_decision_creation_enabled: bool             = False
    auto_score_to_trade_enabled: bool                = False
    replay_trade_execution_enabled: bool             = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id":                   self.snapshot_id,
            "mode":                          self.mode,
            "generated_at":                  self.generated_at,
            "total_sessions":                self.total_sessions,
            "active_sessions":               self.active_sessions,
            "completed_sessions":            self.completed_sessions,
            "archived_sessions":             self.archived_sessions,
            "review_complete_sessions":      self.review_complete_sessions,
            "review_incomplete_sessions":    self.review_incomplete_sessions,
            "pending_outcome_reveal":        self.pending_outcome_reveal,
            "pending_mistake_review":        self.pending_mistake_review,
            "pending_strategy_review":       self.pending_strategy_review,
            "pending_timeframe_review":      self.pending_timeframe_review,
            "low_confidence_count":          self.low_confidence_count,
            "insufficient_data_count":       self.insufficient_data_count,
            "total_pending_queue":           self.total_pending_queue,
            "avg_process_score":             self.avg_process_score,
            "avg_outcome_score":             self.avg_outcome_score,
            "avg_composite_score":           self.avg_composite_score,
            "suggested_mistakes":            self.suggested_mistakes,
            "confirmed_mistakes":            self.confirmed_mistakes,
            "dismissed_mistakes":            self.dismissed_mistakes,
            "strategy_conflicts":            self.strategy_conflicts,
            "strategy_warnings":             self.strategy_warnings,
            "timeframe_conflicts":           self.timeframe_conflicts,
            "pit_failures":                  self.pit_failures,
            "firewall_blocks":               self.firewall_blocks,
            "total_review_elapsed_seconds":  self.total_review_elapsed_seconds,
            "avg_review_elapsed_seconds":    self.avg_review_elapsed_seconds,
            "confidence":                    self.confidence,
            "warnings":                      self.warnings,
            "session_rows":                  self.session_rows,
            "research_only":                 self.research_only,
            "no_real_orders":                self.no_real_orders,
            "auto_review_complete_enabled":        self.auto_review_complete_enabled,
            "auto_outcome_reveal_enabled":          self.auto_outcome_reveal_enabled,
            "auto_mistake_confirmation_enabled":    self.auto_mistake_confirmation_enabled,
            "auto_decision_creation_enabled":       self.auto_decision_creation_enabled,
            "auto_score_to_trade_enabled":          self.auto_score_to_trade_enabled,
            "replay_trade_execution_enabled":       self.replay_trade_execution_enabled,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayReviewDashboardSnapshot":
        return cls(
            snapshot_id=d["snapshot_id"],
            mode=d.get("mode", "real"),
            generated_at=d.get("generated_at", _now_utc()),
            total_sessions=int(d.get("total_sessions", 0)),
            active_sessions=int(d.get("active_sessions", 0)),
            completed_sessions=int(d.get("completed_sessions", 0)),
            archived_sessions=int(d.get("archived_sessions", 0)),
            review_complete_sessions=int(d.get("review_complete_sessions", 0)),
            review_incomplete_sessions=int(d.get("review_incomplete_sessions", 0)),
            pending_outcome_reveal=int(d.get("pending_outcome_reveal", 0)),
            pending_mistake_review=int(d.get("pending_mistake_review", 0)),
            pending_strategy_review=int(d.get("pending_strategy_review", 0)),
            pending_timeframe_review=int(d.get("pending_timeframe_review", 0)),
            low_confidence_count=int(d.get("low_confidence_count", 0)),
            insufficient_data_count=int(d.get("insufficient_data_count", 0)),
            total_pending_queue=int(d.get("total_pending_queue", 0)),
            avg_process_score=d.get("avg_process_score"),
            avg_outcome_score=d.get("avg_outcome_score"),
            avg_composite_score=d.get("avg_composite_score"),
            suggested_mistakes=int(d.get("suggested_mistakes", 0)),
            confirmed_mistakes=int(d.get("confirmed_mistakes", 0)),
            dismissed_mistakes=int(d.get("dismissed_mistakes", 0)),
            strategy_conflicts=int(d.get("strategy_conflicts", 0)),
            strategy_warnings=int(d.get("strategy_warnings", 0)),
            timeframe_conflicts=int(d.get("timeframe_conflicts", 0)),
            pit_failures=int(d.get("pit_failures", 0)),
            firewall_blocks=int(d.get("firewall_blocks", 0)),
            total_review_elapsed_seconds=float(d.get("total_review_elapsed_seconds", 0.0)),
            avg_review_elapsed_seconds=float(d.get("avg_review_elapsed_seconds", 0.0)),
            confidence=d.get("confidence", "INSUFFICIENT"),
            warnings=d.get("warnings", []),
            session_rows=d.get("session_rows", []),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
            auto_review_complete_enabled=bool(d.get("auto_review_complete_enabled", False)),
            auto_outcome_reveal_enabled=bool(d.get("auto_outcome_reveal_enabled", False)),
            auto_mistake_confirmation_enabled=bool(d.get("auto_mistake_confirmation_enabled", False)),
            auto_decision_creation_enabled=bool(d.get("auto_decision_creation_enabled", False)),
            auto_score_to_trade_enabled=bool(d.get("auto_score_to_trade_enabled", False)),
            replay_trade_execution_enabled=bool(d.get("replay_trade_execution_enabled", False)),
        )
