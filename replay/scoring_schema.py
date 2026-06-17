"""
replay/scoring_schema.py — Scoring schemas for v1.2.3 Replay Scoring & Mistake Taxonomy

[!] Research Only. No Real Orders. Replay Training Only.
[!] Scoring NEVER triggers paper orders or broker execution.
[!] Process scores use NO future data, NO outcome, NO PnL.
[!] Outcome reveal is EXPLICIT ONLY — default BLOCKED.
[!] Mistake detection is SUGGESTED only — never auto-confirmed.
[!] Emotional/bias fields: self-reported or rule-triggered only. NOT psychological diagnosis.
[!] Not Investment Advice.
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
SCORING_TRIGGERS_NO_ORDERS = True
AUTO_OUTCOME_REVEAL_ENABLED = False
AUTO_MISTAKE_CONFIRMATION_ENABLED = False
AUTO_SCORE_TO_TRADE_ENABLED = False

SCORE_ID_PREFIX = "PSC-"
OUTCOME_SCORE_ID_PREFIX = "OSC-"
COMPOSITE_SCORE_ID_PREFIX = "CSC-"
MISTAKE_ID_PREFIX = "MIS-"
REVIEW_ID_PREFIX = "MRV-"
REVEAL_ID_PREFIX = "REV-"

PROCESS_SCORE_WEIGHTS = {
    "thesis_quality": 15,
    "risk_planning": 15,
    "discipline_checklist": 15,
    "evidence_quality": 10,
    "confirmation_invalidation": 10,
    "point_in_time_integrity": 10,
    "emotional_awareness": 5,
    "revision_quality": 5,
    "data_sufficiency": 5,
    "scenario_objective": 5,
    "session_completion": 5,
}

FORBIDDEN_SCORE_FIELDS = [
    "realized_return", "future_return", "hindsight_score",
    "final_result", "future_max_gain", "future_max_loss",
    "realized_pnl", "final_label", "outcome", "answer",
    "broker", "order_token", "api_key", "secret",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}{uuid.uuid4().hex[:12].upper()}"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ScoreConfidenceLevel(str, Enum):
    DEMO_ONLY = "DEMO_ONLY"
    INSUFFICIENT = "INSUFFICIENT"
    OBSERVATIONAL = "OBSERVATIONAL"
    RELIABLE = "RELIABLE"


class ProcessScoreStatus(str, Enum):
    NOT_SCORED = "NOT_SCORED"
    SCORED = "SCORED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    BLOCKED = "BLOCKED"


class OutcomeRevealStatus(str, Enum):
    BLOCKED = "BLOCKED"
    PENDING_REVEAL = "PENDING_REVEAL"
    REVEALED = "REVEALED"
    PARTIAL = "PARTIAL"


class CompositeScoreStatus(str, Enum):
    NOT_SCORED = "NOT_SCORED"
    PROCESS_ONLY = "PROCESS_ONLY"
    COMPOSITE = "COMPOSITE"
    INSUFFICIENT = "INSUFFICIENT"
    BLOCKED = "BLOCKED"


class CompositeClassification(str, Enum):
    GOOD_PROCESS_GOOD_OUTCOME = "GOOD_PROCESS_GOOD_OUTCOME"
    GOOD_PROCESS_BAD_OUTCOME = "GOOD_PROCESS_BAD_OUTCOME"
    BAD_PROCESS_GOOD_OUTCOME = "BAD_PROCESS_GOOD_OUTCOME"
    BAD_PROCESS_BAD_OUTCOME = "BAD_PROCESS_BAD_OUTCOME"
    PROCESS_ONLY = "PROCESS_ONLY"
    INSUFFICIENT = "INSUFFICIENT"
    BLOCKED = "BLOCKED"


class MistakeStatus(str, Enum):
    SUGGESTED = "SUGGESTED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    CONFIRMED = "CONFIRMED"
    DISMISSED = "DISMISSED"
    OVERRIDDEN = "OVERRIDDEN"
    REOPENED = "REOPENED"


class MistakeSource(str, Enum):
    SYSTEM_SUGGESTED = "SYSTEM_SUGGESTED"
    SELF_REPORTED = "SELF_REPORTED"
    RULE_SUGGESTED = "RULE_SUGGESTED"
    USER_CONFIRMED = "USER_CONFIRMED"


class MistakeSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ReviewerRole(str, Enum):
    USER = "USER"
    SYSTEM_REVIEW = "SYSTEM_REVIEW"


class JournalReviewStatus(str, Enum):
    NOT_REVIEWED = "NOT_REVIEWED"
    PROCESS_SCORED = "PROCESS_SCORED"
    OUTCOME_REVEALED = "OUTCOME_REVEALED"
    FULLY_REVIEWED = "FULLY_REVIEWED"
    BLOCKED = "BLOCKED"


class MistakeReviewStatus(str, Enum):
    NOT_REVIEWED = "NOT_REVIEWED"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEWED = "REVIEWED"
    DISMISSED = "DISMISSED"


# ---------------------------------------------------------------------------
# ScoreComponent
# ---------------------------------------------------------------------------

@dataclass
class ScoreComponent:
    """
    One dimension of a process or outcome score.
    [!] No future data. Simulation only.
    """
    dimension: str
    raw_score: float                         # 0.0 - 1.0
    weight: int                              # integer weight (sums to 100)
    weighted_score: float                    # raw_score * weight
    rationale: str = ""
    evidence_items: List[str] = field(default_factory=list)
    missing_items: List[str] = field(default_factory=list)
    flags: List[str] = field(default_factory=list)
    simulation_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dimension": self.dimension,
            "raw_score": self.raw_score,
            "weight": self.weight,
            "weighted_score": self.weighted_score,
            "rationale": self.rationale,
            "evidence_items": self.evidence_items,
            "missing_items": self.missing_items,
            "flags": self.flags,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ScoreComponent":
        return cls(
            dimension=d.get("dimension", ""),
            raw_score=float(d.get("raw_score", 0.0)),
            weight=int(d.get("weight", 0)),
            weighted_score=float(d.get("weighted_score", 0.0)),
            rationale=d.get("rationale", ""),
            evidence_items=d.get("evidence_items", []),
            missing_items=d.get("missing_items", []),
            flags=d.get("flags", []),
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
        )


# ---------------------------------------------------------------------------
# ReplayProcessScore
# ---------------------------------------------------------------------------

@dataclass
class ReplayProcessScore:
    """
    Process quality score for a replay session.
    [!] NO future data. NO outcome. NO PnL. Simulation only.
    [!] Scoring NEVER triggers paper orders or broker execution.
    """
    score_id: str
    session_id: str
    journal_entry_id: Optional[str] = None
    decision_id: Optional[str] = None
    symbol: str = ""
    replay_date: str = ""
    total_score: float = 0.0             # 0 - 100
    max_score: float = 100.0
    components: List[ScoreComponent] = field(default_factory=list)
    status: str = ProcessScoreStatus.NOT_SCORED.value
    confidence_level: str = ScoreConfidenceLevel.OBSERVATIONAL.value
    confidence_note: str = ""
    scoring_notes: str = ""
    flags: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    scored_by: str = "USER"
    scored_at: str = field(default_factory=_now_utc)
    created_at: str = field(default_factory=_now_utc)
    simulation_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    scoring_triggers_no_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score_id": self.score_id,
            "session_id": self.session_id,
            "journal_entry_id": self.journal_entry_id,
            "decision_id": self.decision_id,
            "symbol": self.symbol,
            "replay_date": self.replay_date,
            "total_score": self.total_score,
            "max_score": self.max_score,
            "components": [c.to_dict() for c in self.components],
            "status": self.status,
            "confidence_level": self.confidence_level,
            "confidence_note": self.confidence_note,
            "scoring_notes": self.scoring_notes,
            "flags": self.flags,
            "warnings": self.warnings,
            "scored_by": self.scored_by,
            "scored_at": self.scored_at,
            "created_at": self.created_at,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
            "scoring_triggers_no_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayProcessScore":
        return cls(
            score_id=d.get("score_id", _new_id(SCORE_ID_PREFIX)),
            session_id=d.get("session_id", ""),
            journal_entry_id=d.get("journal_entry_id"),
            decision_id=d.get("decision_id"),
            symbol=d.get("symbol", ""),
            replay_date=d.get("replay_date", ""),
            total_score=float(d.get("total_score", 0.0)),
            max_score=float(d.get("max_score", 100.0)),
            components=[ScoreComponent.from_dict(c) for c in d.get("components", [])],
            status=d.get("status", ProcessScoreStatus.NOT_SCORED.value),
            confidence_level=d.get("confidence_level", ScoreConfidenceLevel.OBSERVATIONAL.value),
            confidence_note=d.get("confidence_note", ""),
            scoring_notes=d.get("scoring_notes", ""),
            flags=d.get("flags", []),
            warnings=d.get("warnings", []),
            scored_by=d.get("scored_by", "USER"),
            scored_at=d.get("scored_at", _now_utc()),
            created_at=d.get("created_at", _now_utc()),
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
            scoring_triggers_no_orders=True,
        )


# ---------------------------------------------------------------------------
# ReplayOutcomeScore
# ---------------------------------------------------------------------------

@dataclass
class ReplayOutcomeScore:
    """
    Outcome score — only available AFTER explicit outcome reveal.
    [!] Default: BLOCKED. Requires explicit --reveal AND --confirm-review flags.
    [!] Does NOT modify original session snapshot or journal entry.
    [!] Writes only to review store (data/replay_scoring/).
    [!] Scoring NEVER triggers paper orders or broker execution.
    """
    score_id: str
    session_id: str
    reveal_id: str
    journal_entry_id: Optional[str] = None
    decision_id: Optional[str] = None
    symbol: str = ""
    reveal_window_bars: int = 0
    outcome_score: float = 0.0           # 0 - 100
    outcome_label: str = ""
    outcome_notes: str = ""
    status: str = OutcomeRevealStatus.BLOCKED.value
    confidence_level: str = ScoreConfidenceLevel.INSUFFICIENT.value
    confidence_note: str = ""
    flags: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    scored_by: str = "USER"
    scored_at: str = field(default_factory=_now_utc)
    created_at: str = field(default_factory=_now_utc)
    simulation_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    scoring_triggers_no_orders: bool = True
    auto_outcome_reveal_enabled: bool = False    # ALWAYS False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score_id": self.score_id,
            "session_id": self.session_id,
            "reveal_id": self.reveal_id,
            "journal_entry_id": self.journal_entry_id,
            "decision_id": self.decision_id,
            "symbol": self.symbol,
            "reveal_window_bars": self.reveal_window_bars,
            "outcome_score": self.outcome_score,
            "outcome_label": self.outcome_label,
            "outcome_notes": self.outcome_notes,
            "status": self.status,
            "confidence_level": self.confidence_level,
            "confidence_note": self.confidence_note,
            "flags": self.flags,
            "warnings": self.warnings,
            "scored_by": self.scored_by,
            "scored_at": self.scored_at,
            "created_at": self.created_at,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
            "scoring_triggers_no_orders": True,
            "auto_outcome_reveal_enabled": False,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayOutcomeScore":
        return cls(
            score_id=d.get("score_id", _new_id(OUTCOME_SCORE_ID_PREFIX)),
            session_id=d.get("session_id", ""),
            reveal_id=d.get("reveal_id", ""),
            journal_entry_id=d.get("journal_entry_id"),
            decision_id=d.get("decision_id"),
            symbol=d.get("symbol", ""),
            reveal_window_bars=int(d.get("reveal_window_bars", 0)),
            outcome_score=float(d.get("outcome_score", 0.0)),
            outcome_label=d.get("outcome_label", ""),
            outcome_notes=d.get("outcome_notes", ""),
            status=d.get("status", OutcomeRevealStatus.BLOCKED.value),
            confidence_level=d.get("confidence_level", ScoreConfidenceLevel.INSUFFICIENT.value),
            confidence_note=d.get("confidence_note", ""),
            flags=d.get("flags", []),
            warnings=d.get("warnings", []),
            scored_by=d.get("scored_by", "USER"),
            scored_at=d.get("scored_at", _now_utc()),
            created_at=d.get("created_at", _now_utc()),
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
            scoring_triggers_no_orders=True,
            auto_outcome_reveal_enabled=False,
        )


# ---------------------------------------------------------------------------
# ReplayCompositeScore
# ---------------------------------------------------------------------------

@dataclass
class ReplayCompositeScore:
    """
    Composite score combining process and (optional) outcome.
    [!] Before outcome reveal: PROCESS_ONLY (not COMPOSITE).
    [!] outcome_weight > 0.5 shows warning.
    [!] Scoring NEVER triggers paper orders or broker execution.
    """
    score_id: str
    session_id: str
    process_score_id: Optional[str] = None
    outcome_score_id: Optional[str] = None
    journal_entry_id: Optional[str] = None
    decision_id: Optional[str] = None
    symbol: str = ""
    process_score: Optional[float] = None
    outcome_score: Optional[float] = None
    process_weight: float = 0.70
    outcome_weight: float = 0.30
    composite_score: Optional[float] = None
    classification: str = CompositeClassification.BLOCKED.value
    status: str = CompositeScoreStatus.BLOCKED.value
    confidence_level: str = ScoreConfidenceLevel.INSUFFICIENT.value
    confidence_note: str = ""
    notes: str = ""
    flags: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    scored_by: str = "USER"
    scored_at: str = field(default_factory=_now_utc)
    created_at: str = field(default_factory=_now_utc)
    simulation_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    scoring_triggers_no_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score_id": self.score_id,
            "session_id": self.session_id,
            "process_score_id": self.process_score_id,
            "outcome_score_id": self.outcome_score_id,
            "journal_entry_id": self.journal_entry_id,
            "decision_id": self.decision_id,
            "symbol": self.symbol,
            "process_score": self.process_score,
            "outcome_score": self.outcome_score,
            "process_weight": self.process_weight,
            "outcome_weight": self.outcome_weight,
            "composite_score": self.composite_score,
            "classification": self.classification,
            "status": self.status,
            "confidence_level": self.confidence_level,
            "confidence_note": self.confidence_note,
            "notes": self.notes,
            "flags": self.flags,
            "warnings": self.warnings,
            "scored_by": self.scored_by,
            "scored_at": self.scored_at,
            "created_at": self.created_at,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
            "scoring_triggers_no_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayCompositeScore":
        return cls(
            score_id=d.get("score_id", _new_id(COMPOSITE_SCORE_ID_PREFIX)),
            session_id=d.get("session_id", ""),
            process_score_id=d.get("process_score_id"),
            outcome_score_id=d.get("outcome_score_id"),
            journal_entry_id=d.get("journal_entry_id"),
            decision_id=d.get("decision_id"),
            symbol=d.get("symbol", ""),
            process_score=d.get("process_score"),
            outcome_score=d.get("outcome_score"),
            process_weight=float(d.get("process_weight", 0.70)),
            outcome_weight=float(d.get("outcome_weight", 0.30)),
            composite_score=d.get("composite_score"),
            classification=d.get("classification", CompositeClassification.BLOCKED.value),
            status=d.get("status", CompositeScoreStatus.BLOCKED.value),
            confidence_level=d.get("confidence_level", ScoreConfidenceLevel.INSUFFICIENT.value),
            confidence_note=d.get("confidence_note", ""),
            notes=d.get("notes", ""),
            flags=d.get("flags", []),
            warnings=d.get("warnings", []),
            scored_by=d.get("scored_by", "USER"),
            scored_at=d.get("scored_at", _now_utc()),
            created_at=d.get("created_at", _now_utc()),
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
            scoring_triggers_no_orders=True,
        )


# ---------------------------------------------------------------------------
# MistakeRecord
# ---------------------------------------------------------------------------

@dataclass
class MistakeRecord:
    """
    A single suggested or confirmed mistake record.
    [!] System-detected: status=SUGGESTED (never auto-CONFIRMED).
    [!] Must have evidence field. Must have confidence field.
    [!] WAIT/SKIP not misclassified as mistakes.
    [!] Single loss != mistake. Single profit != good decision.
    [!] Emotional/bias: SELF_REPORTED, RULE_SUGGESTED, USER_CONFIRMED only.
    [!] No psychological diagnosis.
    """
    mistake_id: str
    session_id: str
    journal_entry_id: Optional[str] = None
    decision_id: Optional[str] = None
    symbol: str = ""
    replay_date: str = ""
    mistake_type: str = ""
    category: str = ""
    description: str = ""
    evidence: List[str] = field(default_factory=list)
    confidence: int = 50                   # 0-100
    severity: str = MistakeSeverity.LOW.value
    status: str = MistakeStatus.SUGGESTED.value
    source: str = MistakeSource.SYSTEM_SUGGESTED.value
    action: str = ""                       # The decision action
    is_wait_or_skip: bool = False          # WAIT/SKIP flag — never misclassify
    is_planned_stop: bool = False          # Planned stop — never misclassify
    is_planned_reduce: bool = False        # Planned reduce — never misclassify
    requires_review: bool = True
    auto_confirmed: bool = False           # ALWAYS False — system cannot auto-confirm
    notes: str = ""
    tags: List[str] = field(default_factory=list)
    detected_at: str = field(default_factory=_now_utc)
    created_at: str = field(default_factory=_now_utc)
    simulation_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mistake_id": self.mistake_id,
            "session_id": self.session_id,
            "journal_entry_id": self.journal_entry_id,
            "decision_id": self.decision_id,
            "symbol": self.symbol,
            "replay_date": self.replay_date,
            "mistake_type": self.mistake_type,
            "category": self.category,
            "description": self.description,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "severity": self.severity,
            "status": self.status,
            "source": self.source,
            "action": self.action,
            "is_wait_or_skip": self.is_wait_or_skip,
            "is_planned_stop": self.is_planned_stop,
            "is_planned_reduce": self.is_planned_reduce,
            "requires_review": self.requires_review,
            "auto_confirmed": False,
            "notes": self.notes,
            "tags": self.tags,
            "detected_at": self.detected_at,
            "created_at": self.created_at,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MistakeRecord":
        return cls(
            mistake_id=d.get("mistake_id", _new_id(MISTAKE_ID_PREFIX)),
            session_id=d.get("session_id", ""),
            journal_entry_id=d.get("journal_entry_id"),
            decision_id=d.get("decision_id"),
            symbol=d.get("symbol", ""),
            replay_date=d.get("replay_date", ""),
            mistake_type=d.get("mistake_type", ""),
            category=d.get("category", ""),
            description=d.get("description", ""),
            evidence=d.get("evidence", []),
            confidence=int(d.get("confidence", 50)),
            severity=d.get("severity", MistakeSeverity.LOW.value),
            status=d.get("status", MistakeStatus.SUGGESTED.value),
            source=d.get("source", MistakeSource.SYSTEM_SUGGESTED.value),
            action=d.get("action", ""),
            is_wait_or_skip=bool(d.get("is_wait_or_skip", False)),
            is_planned_stop=bool(d.get("is_planned_stop", False)),
            is_planned_reduce=bool(d.get("is_planned_reduce", False)),
            requires_review=bool(d.get("requires_review", True)),
            auto_confirmed=False,
            notes=d.get("notes", ""),
            tags=d.get("tags", []),
            detected_at=d.get("detected_at", _now_utc()),
            created_at=d.get("created_at", _now_utc()),
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
        )


# ---------------------------------------------------------------------------
# MistakeReviewRecord
# ---------------------------------------------------------------------------

@dataclass
class MistakeReviewRecord:
    """
    Append-only review record for a mistake.
    [!] dismiss preserves original suggestion.
    [!] override preserves original type/severity.
    [!] reopen preserves history.
    [!] SYSTEM cannot auto-CONFIRM.
    """
    review_id: str
    mistake_id: str
    session_id: str
    action: str = ""                       # confirm / dismiss / override / reopen
    new_status: str = MistakeStatus.NEEDS_REVIEW.value
    reviewer: str = ReviewerRole.USER.value
    rationale: str = ""
    override_type: Optional[str] = None
    override_severity: Optional[str] = None
    preserve_original: bool = True        # Always True — append-only
    auto_confirmed: bool = False          # ALWAYS False
    notes: str = ""
    reviewed_at: str = field(default_factory=_now_utc)
    created_at: str = field(default_factory=_now_utc)
    simulation_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "review_id": self.review_id,
            "mistake_id": self.mistake_id,
            "session_id": self.session_id,
            "action": self.action,
            "new_status": self.new_status,
            "reviewer": self.reviewer,
            "rationale": self.rationale,
            "override_type": self.override_type,
            "override_severity": self.override_severity,
            "preserve_original": True,
            "auto_confirmed": False,
            "notes": self.notes,
            "reviewed_at": self.reviewed_at,
            "created_at": self.created_at,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MistakeReviewRecord":
        return cls(
            review_id=d.get("review_id", _new_id(REVIEW_ID_PREFIX)),
            mistake_id=d.get("mistake_id", ""),
            session_id=d.get("session_id", ""),
            action=d.get("action", ""),
            new_status=d.get("new_status", MistakeStatus.NEEDS_REVIEW.value),
            reviewer=d.get("reviewer", ReviewerRole.USER.value),
            rationale=d.get("rationale", ""),
            override_type=d.get("override_type"),
            override_severity=d.get("override_severity"),
            preserve_original=True,
            auto_confirmed=False,
            notes=d.get("notes", ""),
            reviewed_at=d.get("reviewed_at", _now_utc()),
            created_at=d.get("created_at", _now_utc()),
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
        )


# ---------------------------------------------------------------------------
# OutcomeRevealRecord
# ---------------------------------------------------------------------------

@dataclass
class OutcomeRevealRecord:
    """
    Record of an explicit outcome reveal.
    [!] Default: BLOCKED. Only explicit --reveal AND --confirm-review creates this.
    [!] Does NOT modify original session snapshot or journal entry.
    [!] Writes only to review store (data/replay_scoring/).
    [!] AUTO_OUTCOME_REVEAL_ENABLED = False (invariant).
    """
    reveal_id: str
    session_id: str
    journal_entry_id: Optional[str] = None
    decision_id: Optional[str] = None
    symbol: str = ""
    session_end_date: str = ""
    reveal_window_bars: int = 0
    reveal_confirmed: bool = False         # Must be explicitly set True
    confirm_review_flag: bool = False      # --confirm-review flag
    status: str = OutcomeRevealStatus.BLOCKED.value
    outcome_data_summary: str = ""
    original_snapshot_unchanged: bool = True   # Invariant
    original_journal_unchanged: bool = True    # Invariant
    notes: str = ""
    revealed_by: str = "USER"
    revealed_at: str = field(default_factory=_now_utc)
    created_at: str = field(default_factory=_now_utc)
    simulation_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    auto_outcome_reveal_enabled: bool = False   # ALWAYS False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reveal_id": self.reveal_id,
            "session_id": self.session_id,
            "journal_entry_id": self.journal_entry_id,
            "decision_id": self.decision_id,
            "symbol": self.symbol,
            "session_end_date": self.session_end_date,
            "reveal_window_bars": self.reveal_window_bars,
            "reveal_confirmed": self.reveal_confirmed,
            "confirm_review_flag": self.confirm_review_flag,
            "status": self.status,
            "outcome_data_summary": self.outcome_data_summary,
            "original_snapshot_unchanged": True,
            "original_journal_unchanged": True,
            "notes": self.notes,
            "revealed_by": self.revealed_by,
            "revealed_at": self.revealed_at,
            "created_at": self.created_at,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
            "auto_outcome_reveal_enabled": False,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "OutcomeRevealRecord":
        return cls(
            reveal_id=d.get("reveal_id", _new_id(REVEAL_ID_PREFIX)),
            session_id=d.get("session_id", ""),
            journal_entry_id=d.get("journal_entry_id"),
            decision_id=d.get("decision_id"),
            symbol=d.get("symbol", ""),
            session_end_date=d.get("session_end_date", ""),
            reveal_window_bars=int(d.get("reveal_window_bars", 0)),
            reveal_confirmed=bool(d.get("reveal_confirmed", False)),
            confirm_review_flag=bool(d.get("confirm_review_flag", False)),
            status=d.get("status", OutcomeRevealStatus.BLOCKED.value),
            outcome_data_summary=d.get("outcome_data_summary", ""),
            original_snapshot_unchanged=True,
            original_journal_unchanged=True,
            notes=d.get("notes", ""),
            revealed_by=d.get("revealed_by", "USER"),
            revealed_at=d.get("revealed_at", _now_utc()),
            created_at=d.get("created_at", _now_utc()),
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
            auto_outcome_reveal_enabled=False,
        )
