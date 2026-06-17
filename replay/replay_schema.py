"""
replay/replay_schema.py — Data schemas for Replay Training UX Foundation v1.2.0

[!] Research Only. No Real Orders. Replay Training Only.
[!] All decisions are SIMULATION_DECISION_ONLY. No paper orders. No broker calls.
[!] Not Investment Advice.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
REPLAY_TRAINING_ONLY = True

# ---------------------------------------------------------------------------
# Status / Action / Event type constants
# ---------------------------------------------------------------------------

SESSION_STATUSES = [
    "CREATED", "READY", "PLAYING", "PAUSED", "COMPLETED",
    "BLOCKED", "ERROR", "ARCHIVED",
]

DECISION_ACTIONS = [
    "WATCH", "WAIT", "ENTER", "ADD", "HOLD", "REDUCE", "EXIT", "STOP", "SKIP",
]

EVENT_TYPES = [
    "SESSION_CREATED", "SESSION_LOADED", "SESSION_RESUMED", "DATE_CHANGED",
    "PLAY_STARTED", "PLAY_PAUSED", "DECISION_RECORDED", "DECISION_UPDATED",
    "ANNOTATION_ADDED", "WARNING_RAISED", "SESSION_COMPLETED", "SESSION_ARCHIVED",
]

ANNOTATION_TYPES = [
    "NOTE", "SUPPORT", "RESISTANCE", "TREND", "VOLUME",
    "KD", "MACD", "CHIP", "FUNDAMENTAL", "RISK", "MISTAKE", "OTHER",
]

QUALIFICATION_VALUES = [
    "OBSERVATIONAL_ONLY", "DEMO_ONLY", "BLOCKED", "UNKNOWN",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# ReplaySessionConfig
# ---------------------------------------------------------------------------

@dataclass
class ReplaySessionConfig:
    """
    Configuration for a replay training session.
    [!] research_only=True and no_real_orders=True are invariants.
    """
    session_id: str
    session_name: str
    symbol: str
    start_date: str                          # YYYY-MM-DD
    end_date: str                            # YYYY-MM-DD
    initial_date: Optional[str] = None       # YYYY-MM-DD
    mode: str = "real"                       # "real" / "mock"
    tier: str = ""
    timeframe: str = "DAILY"
    visible_history_days: int = 120
    playback_speed: int = 1
    strict_future_firewall: bool = True
    include_strategy_knowledge: bool = True
    include_quality_gate: bool = True
    include_freshness: bool = True
    include_fundamental: bool = True
    include_chips: bool = True
    created_at: str = field(default_factory=_now_utc)
    research_only: bool = True
    no_real_orders: bool = True
    # v1.2.1 new fields (all with defaults for backward compat)
    scenario_id: Optional[str] = None
    scenario_instance_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    folder_name: Optional[str] = None
    root_session_id: Optional[str] = None
    parent_session_id: Optional[str] = None
    source_checkpoint_id: Optional[str] = None
    portable_metadata_version: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "session_name": self.session_name,
            "symbol": self.symbol,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "initial_date": self.initial_date,
            "mode": self.mode,
            "tier": self.tier,
            "timeframe": self.timeframe,
            "visible_history_days": self.visible_history_days,
            "playback_speed": self.playback_speed,
            "strict_future_firewall": self.strict_future_firewall,
            "include_strategy_knowledge": self.include_strategy_knowledge,
            "include_quality_gate": self.include_quality_gate,
            "include_freshness": self.include_freshness,
            "include_fundamental": self.include_fundamental,
            "include_chips": self.include_chips,
            "created_at": self.created_at,
            "research_only": True,
            "no_real_orders": True,
            # v1.2.1
            "scenario_id": self.scenario_id,
            "scenario_instance_id": self.scenario_instance_id,
            "tags": self.tags,
            "folder_name": self.folder_name,
            "root_session_id": self.root_session_id,
            "parent_session_id": self.parent_session_id,
            "source_checkpoint_id": self.source_checkpoint_id,
            "portable_metadata_version": self.portable_metadata_version,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplaySessionConfig":
        return cls(
            session_id=d.get("session_id", ""),
            session_name=d.get("session_name", ""),
            symbol=d.get("symbol", ""),
            start_date=d.get("start_date", ""),
            end_date=d.get("end_date", ""),
            initial_date=d.get("initial_date"),
            mode=d.get("mode", "real"),
            tier=d.get("tier", ""),
            timeframe=d.get("timeframe", "DAILY"),
            visible_history_days=int(d.get("visible_history_days", 120)),
            playback_speed=int(d.get("playback_speed", 1)),
            strict_future_firewall=bool(d.get("strict_future_firewall", True)),
            include_strategy_knowledge=bool(d.get("include_strategy_knowledge", True)),
            include_quality_gate=bool(d.get("include_quality_gate", True)),
            include_freshness=bool(d.get("include_freshness", True)),
            include_fundamental=bool(d.get("include_fundamental", True)),
            include_chips=bool(d.get("include_chips", True)),
            created_at=d.get("created_at", _now_utc()),
            research_only=True,
            no_real_orders=True,
            # v1.2.1 fields — graceful defaults for old sessions
            scenario_id=d.get("scenario_id"),
            scenario_instance_id=d.get("scenario_instance_id"),
            tags=d.get("tags", []),
            folder_name=d.get("folder_name"),
            root_session_id=d.get("root_session_id"),
            parent_session_id=d.get("parent_session_id"),
            source_checkpoint_id=d.get("source_checkpoint_id"),
            portable_metadata_version=int(d.get("portable_metadata_version", 1)),
        )


# ---------------------------------------------------------------------------
# ReplaySessionState
# ---------------------------------------------------------------------------

@dataclass
class ReplaySessionState:
    """
    Mutable state for a replay training session.
    [!] research_only and no_real_orders are invariants.
    """
    session_id: str
    current_date: str
    current_index: int
    total_steps: int
    status: str                          # see SESSION_STATUSES
    playback_speed: int = 1
    last_action: Optional[str] = None
    last_decision_id: Optional[str] = None
    completed: bool = False
    paused: bool = False
    updated_at: str = field(default_factory=_now_utc)
    visible_from: str = ""
    visible_to: str = ""
    available_records: int = 0
    qualification: str = "UNKNOWN"
    warnings: List[str] = field(default_factory=list)
    research_only: bool = True
    no_real_orders: bool = True
    # v1.2.1 new fields (all with defaults for backward compat)
    checkpoint_count: int = 0
    fork_count: int = 0
    child_session_count: int = 0
    hidden: bool = False
    archived_at: Optional[str] = None
    restored_at: Optional[str] = None
    last_checkpoint_id: Optional[str] = None
    # v1.2.3 scoring fields (all with defaults for backward compat)
    process_score_status: str = "NOT_SCORED"
    outcome_reveal_status: str = "BLOCKED"
    composite_score_status: str = "NOT_SCORED"
    mistake_review_status: str = "NOT_REVIEWED"
    latest_process_score_id: Optional[str] = None
    latest_composite_score_id: Optional[str] = None
    suggested_mistake_count: int = 0
    confirmed_mistake_count: int = 0
    dismissed_mistake_count: int = 0
    # v1.2.4 strategy replay fields (all with defaults for backward compat)
    strategy_snapshot_count: int = 0
    latest_strategy_snapshot_id: Optional[str] = None
    strategy_review_status: str = "NOT_REVIEWED"
    strategy_rule_review_count: int = 0
    strategy_conflict_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "current_date": self.current_date,
            "current_index": self.current_index,
            "total_steps": self.total_steps,
            "status": self.status,
            "playback_speed": self.playback_speed,
            "last_action": self.last_action,
            "last_decision_id": self.last_decision_id,
            "completed": self.completed,
            "paused": self.paused,
            "updated_at": self.updated_at,
            "visible_from": self.visible_from,
            "visible_to": self.visible_to,
            "available_records": self.available_records,
            "qualification": self.qualification,
            "warnings": self.warnings,
            "research_only": True,
            "no_real_orders": True,
            # v1.2.1
            "checkpoint_count": self.checkpoint_count,
            "fork_count": self.fork_count,
            "child_session_count": self.child_session_count,
            "hidden": self.hidden,
            "archived_at": self.archived_at,
            "restored_at": self.restored_at,
            "last_checkpoint_id": self.last_checkpoint_id,
            # v1.2.3 scoring fields
            "process_score_status": self.process_score_status,
            "outcome_reveal_status": self.outcome_reveal_status,
            "composite_score_status": self.composite_score_status,
            "mistake_review_status": self.mistake_review_status,
            "latest_process_score_id": self.latest_process_score_id,
            "latest_composite_score_id": self.latest_composite_score_id,
            "suggested_mistake_count": self.suggested_mistake_count,
            "confirmed_mistake_count": self.confirmed_mistake_count,
            "dismissed_mistake_count": self.dismissed_mistake_count,
            # v1.2.4 strategy replay fields
            "strategy_snapshot_count": self.strategy_snapshot_count,
            "latest_strategy_snapshot_id": self.latest_strategy_snapshot_id,
            "strategy_review_status": self.strategy_review_status,
            "strategy_rule_review_count": self.strategy_rule_review_count,
            "strategy_conflict_count": self.strategy_conflict_count,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplaySessionState":
        return cls(
            session_id=d.get("session_id", ""),
            current_date=d.get("current_date", ""),
            current_index=int(d.get("current_index", 0)),
            total_steps=int(d.get("total_steps", 0)),
            status=d.get("status", "CREATED"),
            playback_speed=int(d.get("playback_speed", 1)),
            last_action=d.get("last_action"),
            last_decision_id=d.get("last_decision_id"),
            completed=bool(d.get("completed", False)),
            paused=bool(d.get("paused", False)),
            updated_at=d.get("updated_at", _now_utc()),
            visible_from=d.get("visible_from", ""),
            visible_to=d.get("visible_to", ""),
            available_records=int(d.get("available_records", 0)),
            qualification=d.get("qualification", "UNKNOWN"),
            warnings=d.get("warnings", []),
            research_only=True,
            no_real_orders=True,
            # v1.2.1 fields — graceful defaults for old sessions
            checkpoint_count=int(d.get("checkpoint_count", 0)),
            fork_count=int(d.get("fork_count", 0)),
            child_session_count=int(d.get("child_session_count", 0)),
            hidden=bool(d.get("hidden", False)),
            archived_at=d.get("archived_at"),
            restored_at=d.get("restored_at"),
            last_checkpoint_id=d.get("last_checkpoint_id"),
            # v1.2.3 scoring fields — graceful defaults
            process_score_status=d.get("process_score_status", "NOT_SCORED"),
            outcome_reveal_status=d.get("outcome_reveal_status", "BLOCKED"),
            composite_score_status=d.get("composite_score_status", "NOT_SCORED"),
            mistake_review_status=d.get("mistake_review_status", "NOT_REVIEWED"),
            latest_process_score_id=d.get("latest_process_score_id"),
            latest_composite_score_id=d.get("latest_composite_score_id"),
            suggested_mistake_count=int(d.get("suggested_mistake_count", 0)),
            confirmed_mistake_count=int(d.get("confirmed_mistake_count", 0)),
            dismissed_mistake_count=int(d.get("dismissed_mistake_count", 0)),
            # v1.2.4 strategy replay fields — graceful defaults for old sessions
            strategy_snapshot_count=int(d.get("strategy_snapshot_count", 0)),
            latest_strategy_snapshot_id=d.get("latest_strategy_snapshot_id"),
            strategy_review_status=d.get("strategy_review_status", "NOT_REVIEWED"),
            strategy_rule_review_count=int(d.get("strategy_rule_review_count", 0)),
            strategy_conflict_count=int(d.get("strategy_conflict_count", 0)),
        )


# ---------------------------------------------------------------------------
# ReplayMarketSnapshot
# ---------------------------------------------------------------------------

@dataclass
class ReplayMarketSnapshot:
    """
    Point-in-time market snapshot for replay_date.
    [!] No future data. Firewall enforced. research_only invariant.
    """
    session_id: str
    symbol: str
    replay_date: str
    price_data: Dict[str, Any] = field(default_factory=dict)
    indicator_data: Dict[str, Any] = field(default_factory=dict)
    chips_data: Dict[str, Any] = field(default_factory=dict)
    fundamental_data: Dict[str, Any] = field(default_factory=dict)
    quality_gate: Dict[str, Any] = field(default_factory=dict)
    freshness: Dict[str, Any] = field(default_factory=dict)
    strategy_knowledge: Dict[str, Any] = field(default_factory=dict)
    available_sections: List[str] = field(default_factory=list)
    unavailable_sections: List[str] = field(default_factory=list)
    timing_warnings: List[str] = field(default_factory=list)
    source_metadata: Dict[str, Any] = field(default_factory=dict)
    point_in_time_verified: bool = False
    future_data_blocked_count: int = 0
    generated_at: str = field(default_factory=_now_utc)
    research_only: bool = True
    no_real_orders: bool = True
    # v1.2.4 strategy replay fields (all with defaults for backward compat)
    strategy_replay_snapshot_id: Optional[str] = None
    strategy_agreement_score: Optional[float] = None
    strategy_conflict_score: Optional[float] = None
    strategy_module_availability: Optional[dict] = None
    strategy_warning_count: int = 0
    strategy_conflict_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "symbol": self.symbol,
            "replay_date": self.replay_date,
            "price_data": self.price_data,
            "indicator_data": self.indicator_data,
            "chips_data": self.chips_data,
            "fundamental_data": self.fundamental_data,
            "quality_gate": self.quality_gate,
            "freshness": self.freshness,
            "strategy_knowledge": self.strategy_knowledge,
            "available_sections": self.available_sections,
            "unavailable_sections": self.unavailable_sections,
            "timing_warnings": self.timing_warnings,
            "source_metadata": self.source_metadata,
            "point_in_time_verified": self.point_in_time_verified,
            "future_data_blocked_count": self.future_data_blocked_count,
            "generated_at": self.generated_at,
            "research_only": True,
            "no_real_orders": True,
            # v1.2.4
            "strategy_replay_snapshot_id": self.strategy_replay_snapshot_id,
            "strategy_agreement_score": self.strategy_agreement_score,
            "strategy_conflict_score": self.strategy_conflict_score,
            "strategy_module_availability": self.strategy_module_availability,
            "strategy_warning_count": self.strategy_warning_count,
            "strategy_conflict_count": self.strategy_conflict_count,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayMarketSnapshot":
        return cls(
            session_id=d.get("session_id", ""),
            symbol=d.get("symbol", ""),
            replay_date=d.get("replay_date", ""),
            price_data=d.get("price_data", {}),
            indicator_data=d.get("indicator_data", {}),
            chips_data=d.get("chips_data", {}),
            fundamental_data=d.get("fundamental_data", {}),
            quality_gate=d.get("quality_gate", {}),
            freshness=d.get("freshness", {}),
            strategy_knowledge=d.get("strategy_knowledge", {}),
            available_sections=d.get("available_sections", []),
            unavailable_sections=d.get("unavailable_sections", []),
            timing_warnings=d.get("timing_warnings", []),
            source_metadata=d.get("source_metadata", {}),
            point_in_time_verified=bool(d.get("point_in_time_verified", False)),
            future_data_blocked_count=int(d.get("future_data_blocked_count", 0)),
            generated_at=d.get("generated_at", _now_utc()),
            research_only=True,
            no_real_orders=True,
            # v1.2.4 — graceful defaults for old sessions
            strategy_replay_snapshot_id=d.get("strategy_replay_snapshot_id"),
            strategy_agreement_score=d.get("strategy_agreement_score"),
            strategy_conflict_score=d.get("strategy_conflict_score"),
            strategy_module_availability=d.get("strategy_module_availability"),
            strategy_warning_count=int(d.get("strategy_warning_count", 0)),
            strategy_conflict_count=int(d.get("strategy_conflict_count", 0)),
        )


# ---------------------------------------------------------------------------
# ReplayDecision
# ---------------------------------------------------------------------------

@dataclass
class ReplayDecision:
    """
    A simulated trading decision in a replay session.
    [!] SIMULATION_DECISION_ONLY. No paper orders. No broker calls.
    [!] simulation_decision_only = True is an invariant.
    """
    decision_id: str
    session_id: str
    symbol: str
    replay_date: str
    action: str                                  # see DECISION_ACTIONS
    planned_price: Optional[float] = None
    planned_quantity: Optional[int] = None
    planned_position_pct: Optional[float] = None
    stop_price: Optional[float] = None
    target_price: Optional[float] = None
    confidence: int = 50                         # 0-100
    reasons: List[str] = field(default_factory=list)
    notes: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=_now_utc)
    updated_at: str = field(default_factory=_now_utc)
    research_only: bool = True
    no_real_orders: bool = True
    simulation_decision_only: bool = True
    # v1.2.2 journal fields — all with defaults for backward compat
    journal_entry_id: Optional[str] = None
    thesis_id: Optional[str] = None
    risk_plan_id: Optional[str] = None
    emotional_state_id: Optional[str] = None
    checklist_ids: List[str] = field(default_factory=list)
    revision_count: int = 0
    latest_revision_id: Optional[str] = None
    simulation_only: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "session_id": self.session_id,
            "symbol": self.symbol,
            "replay_date": self.replay_date,
            "action": self.action,
            "planned_price": self.planned_price,
            "planned_quantity": self.planned_quantity,
            "planned_position_pct": self.planned_position_pct,
            "stop_price": self.stop_price,
            "target_price": self.target_price,
            "confidence": self.confidence,
            "reasons": self.reasons,
            "notes": self.notes,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "research_only": True,
            "no_real_orders": True,
            "simulation_decision_only": True,
            # v1.2.2 fields
            "journal_entry_id": self.journal_entry_id,
            "thesis_id": self.thesis_id,
            "risk_plan_id": self.risk_plan_id,
            "emotional_state_id": self.emotional_state_id,
            "checklist_ids": self.checklist_ids,
            "revision_count": self.revision_count,
            "latest_revision_id": self.latest_revision_id,
            "simulation_only": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayDecision":
        return cls(
            decision_id=d.get("decision_id", _new_uuid()),
            session_id=d.get("session_id", ""),
            symbol=d.get("symbol", ""),
            replay_date=d.get("replay_date", ""),
            action=d.get("action", "WATCH"),
            planned_price=d.get("planned_price"),
            planned_quantity=d.get("planned_quantity"),
            planned_position_pct=d.get("planned_position_pct"),
            stop_price=d.get("stop_price"),
            target_price=d.get("target_price"),
            confidence=int(d.get("confidence", 50)),
            reasons=d.get("reasons", []),
            notes=d.get("notes", ""),
            tags=d.get("tags", []),
            created_at=d.get("created_at", _now_utc()),
            updated_at=d.get("updated_at", _now_utc()),
            research_only=True,
            no_real_orders=True,
            simulation_decision_only=True,
            # v1.2.2 fields — graceful defaults for old decisions
            journal_entry_id=d.get("journal_entry_id"),
            thesis_id=d.get("thesis_id"),
            risk_plan_id=d.get("risk_plan_id"),
            emotional_state_id=d.get("emotional_state_id"),
            checklist_ids=d.get("checklist_ids", []),
            revision_count=int(d.get("revision_count", 0)),
            latest_revision_id=d.get("latest_revision_id"),
            simulation_only=True,
        )


# ---------------------------------------------------------------------------
# ReplayEvent
# ---------------------------------------------------------------------------

@dataclass
class ReplayEvent:
    """
    An event in the lifecycle of a replay session.
    [!] Research Only. No Real Orders.
    """
    event_id: str
    session_id: str
    replay_date: str
    event_type: str                  # see EVENT_TYPES
    payload: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_now_utc)
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "session_id": self.session_id,
            "replay_date": self.replay_date,
            "event_type": self.event_type,
            "payload": self.payload,
            "created_at": self.created_at,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayEvent":
        return cls(
            event_id=d.get("event_id", _new_uuid()),
            session_id=d.get("session_id", ""),
            replay_date=d.get("replay_date", ""),
            event_type=d.get("event_type", "SESSION_CREATED"),
            payload=d.get("payload", {}),
            created_at=d.get("created_at", _now_utc()),
            research_only=True,
            no_real_orders=True,
        )


# ---------------------------------------------------------------------------
# ReplayAnnotation
# ---------------------------------------------------------------------------

@dataclass
class ReplayAnnotation:
    """
    An annotation attached to a replay session date.
    remove_from_view: sets hidden=True, does NOT delete from audit history.
    """
    annotation_id: str
    session_id: str
    replay_date: str
    annotation_type: str             # see ANNOTATION_TYPES
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    price_level: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    style_metadata: Dict[str, Any] = field(default_factory=dict)
    hidden: bool = False
    created_at: str = field(default_factory=_now_utc)
    updated_at: str = field(default_factory=_now_utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "annotation_id": self.annotation_id,
            "session_id": self.session_id,
            "replay_date": self.replay_date,
            "annotation_type": self.annotation_type,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "price_level": self.price_level,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "style_metadata": self.style_metadata,
            "hidden": self.hidden,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayAnnotation":
        return cls(
            annotation_id=d.get("annotation_id", _new_uuid()),
            session_id=d.get("session_id", ""),
            replay_date=d.get("replay_date", ""),
            annotation_type=d.get("annotation_type", "NOTE"),
            title=d.get("title", ""),
            content=d.get("content", ""),
            tags=d.get("tags", []),
            price_level=d.get("price_level"),
            start_date=d.get("start_date"),
            end_date=d.get("end_date"),
            style_metadata=d.get("style_metadata", {}),
            hidden=bool(d.get("hidden", False)),
            created_at=d.get("created_at", _now_utc()),
            updated_at=d.get("updated_at", _now_utc()),
        )
