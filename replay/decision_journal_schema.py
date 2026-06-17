"""
replay/decision_journal_schema.py — Decision Journal schemas for v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] Journal decisions are SIMULATION ONLY. No paper orders. No broker calls.
[!] No hindsight scoring. No future results. No realized PnL.
[!] Emotional state fields are self-reported only. NOT psychological diagnosis.
[!] Cognitive bias flags are self-reported or explicit rule-triggered only.
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
SIMULATION_ONLY = True

JOURNAL_ID_PREFIX = "DJR-"
REVISION_ID_PREFIX = "DREV-"

FORBIDDEN_JOURNAL_FIELDS = [
    "realized_return", "future_return", "hindsight_score",
    "final_result", "future_max_gain", "future_max_loss",
    "realized_pnl", "final_label", "outcome", "answer",
    "broker", "order_token", "api_key", "secret",
]

FORBIDDEN_SUMMARY_FIELDS = [
    "win_rate", "return_rate", "pnl", "accuracy", "alpha", "sharpe", "hindsight_score",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}{uuid.uuid4().hex[:12].upper()}"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SetupType(str, Enum):
    BREAKOUT = "BREAKOUT"
    PULLBACK = "PULLBACK"
    BOTTOM_REVERSAL = "BOTTOM_REVERSAL"
    TREND_FOLLOWING = "TREND_FOLLOWING"
    MOMENTUM = "MOMENTUM"
    SECTOR_ROTATION = "SECTOR_ROTATION"
    FUNDAMENTAL_TURNAROUND = "FUNDAMENTAL_TURNAROUND"
    RISK_REDUCTION = "RISK_REDUCTION"
    NO_CHASE = "NO_CHASE"
    NO_PANIC_SELL = "NO_PANIC_SELL"
    FREE_FORM = "FREE_FORM"
    OTHER = "OTHER"


class TimeHorizon(str, Enum):
    INTRADAY = "INTRADAY"
    SHORT = "SHORT"
    SWING = "SWING"
    MID = "MID"
    LONG = "LONG"
    UNDEFINED = "UNDEFINED"


class StopType(str, Enum):
    HARD_STOP = "HARD_STOP"
    CLOSE_CONFIRM = "CLOSE_CONFIRM"
    SUPPORT_BREAK = "SUPPORT_BREAK"
    MA_BREAK = "MA_BREAK"
    TIME_STOP = "TIME_STOP"
    VOLATILITY_STOP = "VOLATILITY_STOP"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    NONE = "NONE"


class TargetType(str, Enum):
    FIXED_PRICE = "FIXED_PRICE"
    RESISTANCE = "RESISTANCE"
    TRAILING = "TRAILING"
    SCALE_OUT = "SCALE_OUT"
    TIME_BASED = "TIME_BASED"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    NONE = "NONE"


class PrimaryEmotion(str, Enum):
    CALM = "CALM"
    CONFIDENT = "CONFIDENT"
    UNCERTAIN = "UNCERTAIN"
    ANXIOUS = "ANXIOUS"
    FEARFUL = "FEARFUL"
    GREEDY = "GREEDY"
    FRUSTRATED = "FRUSTRATED"
    IMPATIENT = "IMPATIENT"
    EXCITED = "EXCITED"
    FATIGUED = "FATIGUED"
    NEUTRAL = "NEUTRAL"
    OTHER = "OTHER"


class ChecklistCategory(str, Enum):
    DATA = "DATA"
    SETUP = "SETUP"
    ENTRY = "ENTRY"
    RISK = "RISK"
    POSITION = "POSITION"
    EMOTION = "EMOTION"
    DISCIPLINE = "DISCIPLINE"
    EXIT = "EXIT"
    REVIEW = "REVIEW"
    OTHER = "OTHER"


class JournalStatus(str, Enum):
    DRAFT = "DRAFT"
    RECORDED = "RECORDED"
    REVISED = "REVISED"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"
    BLOCKED = "BLOCKED"


class JournalReviewStatus(str, Enum):
    """v1.2.3: Scoring/review status for a journal entry."""
    NOT_REVIEWED = "NOT_REVIEWED"
    PROCESS_SCORED = "PROCESS_SCORED"
    OUTCOME_REVEALED = "OUTCOME_REVEALED"
    FULLY_REVIEWED = "FULLY_REVIEWED"
    BLOCKED = "BLOCKED"


class RelationType(str, Enum):
    ROOT = "ROOT"
    REVISION = "REVISION"
    FOLLOW_UP = "FOLLOW_UP"
    CONFIRMATION = "CONFIRMATION"
    INVALIDATION = "INVALIDATION"
    RISK_UPDATE = "RISK_UPDATE"
    EMOTION_UPDATE = "EMOTION_UPDATE"
    CHECKLIST_UPDATE = "CHECKLIST_UPDATE"
    SESSION_FORK_COPY = "SESSION_FORK_COPY"


# ---------------------------------------------------------------------------
# TradeThesis
# ---------------------------------------------------------------------------

@dataclass
class TradeThesis:
    """
    Trade thesis for a journal entry.
    [!] No future data. No hindsight. Simulation only.
    """
    thesis_id: str
    session_id: str
    decision_id: str
    setup_type: str = SetupType.FREE_FORM.value
    time_horizon: str = TimeHorizon.UNDEFINED.value
    title: str = ""
    thesis_text: str = ""
    summary: str = ""
    key_triggers: List[str] = field(default_factory=list)
    confirmation_conditions: List[str] = field(default_factory=list)
    invalidation_conditions: List[str] = field(default_factory=list)
    market_context: str = ""
    trend_context: str = ""
    sector_context: str = ""
    fundamental_context: str = ""
    technical_context: str = ""
    chip_context: str = ""
    catalyst_context: str = ""
    expected_scenario: str = ""
    alternative_scenario: str = ""
    assumptions: List[str] = field(default_factory=list)
    unknowns: List[str] = field(default_factory=list)
    notes: str = ""
    created_at: str = field(default_factory=_now_utc)
    updated_at: str = field(default_factory=_now_utc)
    simulation_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "thesis_id": self.thesis_id,
            "session_id": self.session_id,
            "decision_id": self.decision_id,
            "setup_type": self.setup_type,
            "time_horizon": self.time_horizon,
            "title": self.title,
            "thesis_text": self.thesis_text,
            "summary": self.summary,
            "key_triggers": self.key_triggers,
            "confirmation_conditions": self.confirmation_conditions,
            "invalidation_conditions": self.invalidation_conditions,
            "market_context": self.market_context,
            "trend_context": self.trend_context,
            "sector_context": self.sector_context,
            "fundamental_context": self.fundamental_context,
            "technical_context": self.technical_context,
            "chip_context": self.chip_context,
            "catalyst_context": self.catalyst_context,
            "expected_scenario": self.expected_scenario,
            "alternative_scenario": self.alternative_scenario,
            "assumptions": self.assumptions,
            "unknowns": self.unknowns,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TradeThesis":
        return cls(
            thesis_id=d.get("thesis_id", _new_id("THY-")),
            session_id=d.get("session_id", ""),
            decision_id=d.get("decision_id", ""),
            setup_type=d.get("setup_type", SetupType.FREE_FORM.value),
            time_horizon=d.get("time_horizon", TimeHorizon.UNDEFINED.value),
            title=d.get("title", ""),
            thesis_text=d.get("thesis_text", ""),
            summary=d.get("summary", ""),
            key_triggers=d.get("key_triggers", []),
            confirmation_conditions=d.get("confirmation_conditions", []),
            invalidation_conditions=d.get("invalidation_conditions", []),
            market_context=d.get("market_context", ""),
            trend_context=d.get("trend_context", ""),
            sector_context=d.get("sector_context", ""),
            fundamental_context=d.get("fundamental_context", ""),
            technical_context=d.get("technical_context", ""),
            chip_context=d.get("chip_context", ""),
            catalyst_context=d.get("catalyst_context", ""),
            expected_scenario=d.get("expected_scenario", ""),
            alternative_scenario=d.get("alternative_scenario", ""),
            assumptions=d.get("assumptions", []),
            unknowns=d.get("unknowns", []),
            notes=d.get("notes", ""),
            created_at=d.get("created_at", _now_utc()),
            updated_at=d.get("updated_at", _now_utc()),
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
        )


# ---------------------------------------------------------------------------
# RiskPlan
# ---------------------------------------------------------------------------

@dataclass
class RiskPlan:
    """
    Risk plan for a journal entry.
    [!] No future data. Simulation only.
    """
    risk_plan_id: str
    session_id: str
    decision_id: str
    stop_type: str = StopType.NONE.value
    stop_price_note: str = ""
    stop_price: Optional[float] = None
    target_type: str = TargetType.NONE.value
    target_price_note: str = ""
    target_price: Optional[float] = None
    max_risk_note: str = ""
    max_position_pct: Optional[float] = None
    initial_position_pct: Optional[float] = None
    add_position_pct: Optional[float] = None
    max_loss_pct: Optional[float] = None
    position_sizing_note: str = ""
    risk_reward_estimate: Optional[str] = None
    invalidation_price: Optional[float] = None
    support_reference: str = ""
    resistance_reference: str = ""
    gap_risk: str = ""
    event_risk: str = ""
    liquidity_risk: str = ""
    concentration_risk: str = ""
    notes: str = ""
    created_at: str = field(default_factory=_now_utc)
    updated_at: str = field(default_factory=_now_utc)
    simulation_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "risk_plan_id": self.risk_plan_id,
            "session_id": self.session_id,
            "decision_id": self.decision_id,
            "stop_type": self.stop_type,
            "stop_price_note": self.stop_price_note,
            "stop_price": self.stop_price,
            "target_type": self.target_type,
            "target_price_note": self.target_price_note,
            "target_price": self.target_price,
            "max_risk_note": self.max_risk_note,
            "max_position_pct": self.max_position_pct,
            "initial_position_pct": self.initial_position_pct,
            "add_position_pct": self.add_position_pct,
            "max_loss_pct": self.max_loss_pct,
            "position_sizing_note": self.position_sizing_note,
            "risk_reward_estimate": self.risk_reward_estimate,
            "invalidation_price": self.invalidation_price,
            "support_reference": self.support_reference,
            "resistance_reference": self.resistance_reference,
            "gap_risk": self.gap_risk,
            "event_risk": self.event_risk,
            "liquidity_risk": self.liquidity_risk,
            "concentration_risk": self.concentration_risk,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RiskPlan":
        return cls(
            risk_plan_id=d.get("risk_plan_id", _new_id("RSK-")),
            session_id=d.get("session_id", ""),
            decision_id=d.get("decision_id", ""),
            stop_type=d.get("stop_type", StopType.NONE.value),
            stop_price_note=d.get("stop_price_note", ""),
            stop_price=d.get("stop_price"),
            target_type=d.get("target_type", TargetType.NONE.value),
            target_price_note=d.get("target_price_note", ""),
            target_price=d.get("target_price"),
            max_risk_note=d.get("max_risk_note", ""),
            max_position_pct=d.get("max_position_pct"),
            initial_position_pct=d.get("initial_position_pct"),
            add_position_pct=d.get("add_position_pct"),
            max_loss_pct=d.get("max_loss_pct"),
            position_sizing_note=d.get("position_sizing_note", ""),
            risk_reward_estimate=d.get("risk_reward_estimate"),
            invalidation_price=d.get("invalidation_price"),
            support_reference=d.get("support_reference", ""),
            resistance_reference=d.get("resistance_reference", ""),
            gap_risk=d.get("gap_risk", ""),
            event_risk=d.get("event_risk", ""),
            liquidity_risk=d.get("liquidity_risk", ""),
            concentration_risk=d.get("concentration_risk", ""),
            notes=d.get("notes", ""),
            created_at=d.get("created_at", _now_utc()),
            updated_at=d.get("updated_at", _now_utc()),
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
        )


# ---------------------------------------------------------------------------
# EmotionalStateRecord
# ---------------------------------------------------------------------------

@dataclass
class EmotionalStateRecord:
    """
    Self-reported emotional state record.
    [!] Self-reported only. NOT a psychological diagnosis.
    [!] Values 0-100. No automated scoring.
    """
    emotional_state_id: str
    session_id: str
    decision_id: str
    primary_emotion: str = PrimaryEmotion.NEUTRAL.value
    # All 0-100, None = not provided
    confidence_level: Optional[int] = None
    anxiety_level: Optional[int] = None
    focus_level: Optional[int] = None
    intensity: Optional[int] = None
    stress_level: Optional[int] = None
    urgency_level: Optional[int] = None
    fear_level: Optional[int] = None
    greed_level: Optional[int] = None
    frustration_level: Optional[int] = None
    fatigue_level: Optional[int] = None
    fomo: bool = False
    revenge_trading_risk: bool = False
    loss_aversion_risk: bool = False
    cognitive_bias_flags: List[str] = field(default_factory=list)
    notes: str = ""
    self_reported: bool = True       # ALWAYS True — no automated diagnosis
    recorded_at: str = field(default_factory=_now_utc)
    created_at: str = field(default_factory=_now_utc)
    simulation_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True

    # NO_PSYCHOLOGICAL_DIAGNOSIS — this is self-reported training data only

    def to_dict(self) -> Dict[str, Any]:
        return {
            "emotional_state_id": self.emotional_state_id,
            "session_id": self.session_id,
            "decision_id": self.decision_id,
            "primary_emotion": self.primary_emotion,
            "confidence_level": self.confidence_level,
            "anxiety_level": self.anxiety_level,
            "focus_level": self.focus_level,
            "intensity": self.intensity,
            "stress_level": self.stress_level,
            "urgency_level": self.urgency_level,
            "fear_level": self.fear_level,
            "greed_level": self.greed_level,
            "frustration_level": self.frustration_level,
            "fatigue_level": self.fatigue_level,
            "fomo": self.fomo,
            "revenge_trading_risk": self.revenge_trading_risk,
            "loss_aversion_risk": self.loss_aversion_risk,
            "cognitive_bias_flags": self.cognitive_bias_flags,
            "notes": self.notes,
            "self_reported": True,
            "recorded_at": self.recorded_at,
            "created_at": self.created_at,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "EmotionalStateRecord":
        return cls(
            emotional_state_id=d.get("emotional_state_id", _new_id("EMO-")),
            session_id=d.get("session_id", ""),
            decision_id=d.get("decision_id", ""),
            primary_emotion=d.get("primary_emotion", PrimaryEmotion.NEUTRAL.value),
            confidence_level=d.get("confidence_level"),
            anxiety_level=d.get("anxiety_level"),
            focus_level=d.get("focus_level"),
            intensity=d.get("intensity"),
            stress_level=d.get("stress_level"),
            urgency_level=d.get("urgency_level"),
            fear_level=d.get("fear_level"),
            greed_level=d.get("greed_level"),
            frustration_level=d.get("frustration_level"),
            fatigue_level=d.get("fatigue_level"),
            fomo=bool(d.get("fomo", False)),
            revenge_trading_risk=bool(d.get("revenge_trading_risk", False)),
            loss_aversion_risk=bool(d.get("loss_aversion_risk", False)),
            cognitive_bias_flags=d.get("cognitive_bias_flags", []),
            notes=d.get("notes", ""),
            self_reported=True,
            recorded_at=d.get("recorded_at", _now_utc()),
            created_at=d.get("created_at", _now_utc()),
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
        )


# ---------------------------------------------------------------------------
# DisciplineChecklistResult
# ---------------------------------------------------------------------------

@dataclass
class DisciplineChecklistResult:
    """
    Result of running a discipline checklist.
    [!] Simulation only. No auto scoring. No trading trigger.
    """
    checklist_id: str
    session_id: str
    decision_id: str
    category: str = ChecklistCategory.OTHER.value
    checklist_name: str = ""
    template_id: str = ""
    items: List[Dict[str, Any]] = field(default_factory=list)
    passed_count: int = 0
    total_count: int = 0
    completed_count: int = 0
    all_required_passed: bool = False
    passed: bool = False
    warnings: List[str] = field(default_factory=list)
    blocked_items: List[str] = field(default_factory=list)
    notes: str = ""
    recorded_at: str = field(default_factory=_now_utc)
    created_at: str = field(default_factory=_now_utc)
    simulation_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "checklist_id": self.checklist_id,
            "session_id": self.session_id,
            "decision_id": self.decision_id,
            "category": self.category,
            "checklist_name": self.checklist_name,
            "template_id": self.template_id,
            "items": self.items,
            "passed_count": self.passed_count,
            "total_count": self.total_count,
            "completed_count": self.completed_count,
            "all_required_passed": self.all_required_passed,
            "passed": self.passed,
            "warnings": self.warnings,
            "blocked_items": self.blocked_items,
            "notes": self.notes,
            "recorded_at": self.recorded_at,
            "created_at": self.created_at,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DisciplineChecklistResult":
        return cls(
            checklist_id=d.get("checklist_id", _new_id("CHK-")),
            session_id=d.get("session_id", ""),
            decision_id=d.get("decision_id", ""),
            category=d.get("category", ChecklistCategory.OTHER.value),
            checklist_name=d.get("checklist_name", ""),
            template_id=d.get("template_id", ""),
            items=d.get("items", []),
            passed_count=int(d.get("passed_count", 0)),
            total_count=int(d.get("total_count", 0)),
            completed_count=int(d.get("completed_count", 0)),
            all_required_passed=bool(d.get("all_required_passed", False)),
            passed=bool(d.get("passed", False)),
            warnings=d.get("warnings", []),
            blocked_items=d.get("blocked_items", []),
            notes=d.get("notes", ""),
            recorded_at=d.get("recorded_at", _now_utc()),
            created_at=d.get("created_at", _now_utc()),
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
        )


# ---------------------------------------------------------------------------
# DecisionJournalEntry
# ---------------------------------------------------------------------------

@dataclass
class DecisionJournalEntry:
    """
    A decision journal entry (DJR- prefix).
    [!] SIMULATION_DECISION_ONLY. No paper orders. No broker calls.
    [!] No hindsight scoring. No future results. Append-only revisions.
    [!] Archived entries are immutable until restored.
    """
    journal_entry_id: str               # DJR- prefix
    decision_id: str
    session_id: str
    replay_date: str
    action: str = "WATCH"
    symbol: str = ""
    scenario_id: Optional[str] = None
    checkpoint_id: Optional[str] = None
    decision_revision: int = 0
    thesis_id: Optional[str] = None
    risk_plan_id: Optional[str] = None
    emotional_state_id: Optional[str] = None
    checklist_ids: List[str] = field(default_factory=list)
    confidence: int = 50
    confidence_reason: str = ""
    evidence_for: List[str] = field(default_factory=list)
    evidence_against: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    unknowns: List[str] = field(default_factory=list)
    confirmation_conditions: List[str] = field(default_factory=list)
    invalidation_conditions: List[str] = field(default_factory=list)
    planned_action: str = ""
    fallback_action: str = ""
    no_trade_conditions: List[str] = field(default_factory=list)
    decision_reason: str = ""
    pre_decision_notes: str = ""
    post_decision_notes: str = ""
    notes: str = ""
    tags: List[str] = field(default_factory=list)
    source_snapshot_id: Optional[str] = None
    point_in_time_verified: bool = False
    qualification: str = "OBSERVATIONAL_ONLY"
    status: str = JournalStatus.DRAFT.value
    revision_count: int = 0
    latest_revision_id: Optional[str] = None
    root_entry_id: Optional[str] = None
    parent_entry_id: Optional[str] = None
    hidden: bool = False
    archived: bool = False
    created_at: str = field(default_factory=_now_utc)
    updated_at: str = field(default_factory=_now_utc)
    simulation_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    # v1.2.3 Scoring fields — all with defaults for backward compat
    latest_process_score_id: Optional[str] = None
    latest_outcome_score_id: Optional[str] = None
    latest_composite_score_id: Optional[str] = None
    mistake_count: int = 0
    confirmed_mistake_count: int = 0
    outcome_revealed: bool = False
    review_status: str = "NOT_REVIEWED"   # JournalReviewStatus
    # v1.2.4 Strategy replay fields — all with defaults for backward compat
    strategy_snapshot_id: Optional[str] = None
    strategy_signals_at_decision: Optional[dict] = None
    strategy_warnings_at_decision: Optional[list] = None
    strategy_agreement_at_decision: Optional[float] = None
    strategy_conflicts_at_decision: Optional[list] = None
    strategy_rule_review_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "journal_entry_id": self.journal_entry_id,
            "decision_id": self.decision_id,
            "session_id": self.session_id,
            "replay_date": self.replay_date,
            "action": self.action,
            "symbol": self.symbol,
            "scenario_id": self.scenario_id,
            "checkpoint_id": self.checkpoint_id,
            "decision_revision": self.decision_revision,
            "thesis_id": self.thesis_id,
            "risk_plan_id": self.risk_plan_id,
            "emotional_state_id": self.emotional_state_id,
            "checklist_ids": self.checklist_ids,
            "confidence": self.confidence,
            "confidence_reason": self.confidence_reason,
            "evidence_for": self.evidence_for,
            "evidence_against": self.evidence_against,
            "assumptions": self.assumptions,
            "unknowns": self.unknowns,
            "confirmation_conditions": self.confirmation_conditions,
            "invalidation_conditions": self.invalidation_conditions,
            "planned_action": self.planned_action,
            "fallback_action": self.fallback_action,
            "no_trade_conditions": self.no_trade_conditions,
            "decision_reason": self.decision_reason,
            "pre_decision_notes": self.pre_decision_notes,
            "post_decision_notes": self.post_decision_notes,
            "notes": self.notes,
            "tags": self.tags,
            "source_snapshot_id": self.source_snapshot_id,
            "point_in_time_verified": self.point_in_time_verified,
            "qualification": self.qualification,
            "status": self.status,
            "revision_count": self.revision_count,
            "latest_revision_id": self.latest_revision_id,
            "root_entry_id": self.root_entry_id,
            "parent_entry_id": self.parent_entry_id,
            "hidden": self.hidden,
            "archived": self.archived,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
            # v1.2.3 scoring fields
            "latest_process_score_id": self.latest_process_score_id,
            "latest_outcome_score_id": self.latest_outcome_score_id,
            "latest_composite_score_id": self.latest_composite_score_id,
            "mistake_count": self.mistake_count,
            "confirmed_mistake_count": self.confirmed_mistake_count,
            "outcome_revealed": self.outcome_revealed,
            "review_status": self.review_status,
            # v1.2.4 strategy replay fields
            "strategy_snapshot_id": self.strategy_snapshot_id,
            "strategy_signals_at_decision": self.strategy_signals_at_decision,
            "strategy_warnings_at_decision": self.strategy_warnings_at_decision,
            "strategy_agreement_at_decision": self.strategy_agreement_at_decision,
            "strategy_conflicts_at_decision": self.strategy_conflicts_at_decision,
            "strategy_rule_review_ids": self.strategy_rule_review_ids,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DecisionJournalEntry":
        entry_id = d.get("journal_entry_id", _new_id(JOURNAL_ID_PREFIX))
        if not entry_id.startswith(JOURNAL_ID_PREFIX):
            entry_id = JOURNAL_ID_PREFIX + entry_id
        return cls(
            journal_entry_id=entry_id,
            decision_id=d.get("decision_id", ""),
            session_id=d.get("session_id", ""),
            replay_date=d.get("replay_date", ""),
            action=d.get("action", "WATCH"),
            symbol=d.get("symbol", ""),
            scenario_id=d.get("scenario_id"),
            checkpoint_id=d.get("checkpoint_id"),
            decision_revision=int(d.get("decision_revision", 0)),
            thesis_id=d.get("thesis_id"),
            risk_plan_id=d.get("risk_plan_id"),
            emotional_state_id=d.get("emotional_state_id"),
            checklist_ids=d.get("checklist_ids", []),
            confidence=int(d.get("confidence", 50)),
            confidence_reason=d.get("confidence_reason", ""),
            evidence_for=d.get("evidence_for", []),
            evidence_against=d.get("evidence_against", []),
            assumptions=d.get("assumptions", []),
            unknowns=d.get("unknowns", []),
            confirmation_conditions=d.get("confirmation_conditions", []),
            invalidation_conditions=d.get("invalidation_conditions", []),
            planned_action=d.get("planned_action", ""),
            fallback_action=d.get("fallback_action", ""),
            no_trade_conditions=d.get("no_trade_conditions", []),
            decision_reason=d.get("decision_reason", ""),
            pre_decision_notes=d.get("pre_decision_notes", ""),
            post_decision_notes=d.get("post_decision_notes", ""),
            notes=d.get("notes", ""),
            tags=d.get("tags", []),
            source_snapshot_id=d.get("source_snapshot_id"),
            point_in_time_verified=bool(d.get("point_in_time_verified", False)),
            qualification=d.get("qualification", "OBSERVATIONAL_ONLY"),
            status=d.get("status", JournalStatus.DRAFT.value),
            revision_count=int(d.get("revision_count", 0)),
            latest_revision_id=d.get("latest_revision_id"),
            root_entry_id=d.get("root_entry_id"),
            parent_entry_id=d.get("parent_entry_id"),
            hidden=bool(d.get("hidden", False)),
            archived=bool(d.get("archived", False)),
            created_at=d.get("created_at", _now_utc()),
            updated_at=d.get("updated_at", _now_utc()),
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
            # v1.2.3 scoring fields — graceful defaults for old entries
            latest_process_score_id=d.get("latest_process_score_id"),
            latest_outcome_score_id=d.get("latest_outcome_score_id"),
            latest_composite_score_id=d.get("latest_composite_score_id"),
            mistake_count=int(d.get("mistake_count", 0)),
            confirmed_mistake_count=int(d.get("confirmed_mistake_count", 0)),
            outcome_revealed=bool(d.get("outcome_revealed", False)),
            review_status=d.get("review_status", "NOT_REVIEWED"),
            # v1.2.4 strategy replay fields — graceful defaults for old entries
            strategy_snapshot_id=d.get("strategy_snapshot_id"),
            strategy_signals_at_decision=d.get("strategy_signals_at_decision"),
            strategy_warnings_at_decision=d.get("strategy_warnings_at_decision"),
            strategy_agreement_at_decision=d.get("strategy_agreement_at_decision"),
            strategy_conflicts_at_decision=d.get("strategy_conflicts_at_decision"),
            strategy_rule_review_ids=d.get("strategy_rule_review_ids", []),
        )


# ---------------------------------------------------------------------------
# DecisionRevisionRecord
# ---------------------------------------------------------------------------

@dataclass
class DecisionRevisionRecord:
    """
    Append-only revision record for a journal entry (DREV- prefix).
    [!] Never overwrites original entry. Append-only.
    [!] Simulation only. No real orders.
    """
    revision_id: str                    # DREV- prefix
    journal_entry_id: str
    original_entry_id: str
    decision_id: str
    session_id: str
    revision_number: int = 1
    previous_revision: int = 0
    new_revision: int = 1
    reason: str = ""
    change_reason: str = ""
    changed_fields: Dict[str, Any] = field(default_factory=dict)
    field_changes: Dict[str, Any] = field(default_factory=dict)
    new_snapshot: Dict[str, Any] = field(default_factory=dict)
    confidence_before: Optional[int] = None
    confidence_after: Optional[int] = None
    revised_by: str = "user"
    point_in_time_verified: bool = False
    created_at: str = field(default_factory=_now_utc)
    simulation_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "revision_id": self.revision_id,
            "journal_entry_id": self.journal_entry_id,
            "original_entry_id": self.original_entry_id,
            "decision_id": self.decision_id,
            "session_id": self.session_id,
            "revision_number": self.revision_number,
            "previous_revision": self.previous_revision,
            "new_revision": self.new_revision,
            "reason": self.reason,
            "change_reason": self.change_reason,
            "changed_fields": self.changed_fields,
            "field_changes": self.field_changes,
            "new_snapshot": self.new_snapshot,
            "confidence_before": self.confidence_before,
            "confidence_after": self.confidence_after,
            "revised_by": self.revised_by,
            "point_in_time_verified": self.point_in_time_verified,
            "created_at": self.created_at,
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DecisionRevisionRecord":
        rev_id = d.get("revision_id", _new_id(REVISION_ID_PREFIX))
        if not rev_id.startswith(REVISION_ID_PREFIX):
            rev_id = REVISION_ID_PREFIX + rev_id
        return cls(
            revision_id=rev_id,
            journal_entry_id=d.get("journal_entry_id", ""),
            original_entry_id=d.get("original_entry_id", d.get("journal_entry_id", "")),
            decision_id=d.get("decision_id", ""),
            session_id=d.get("session_id", ""),
            revision_number=int(d.get("revision_number", 1)),
            previous_revision=int(d.get("previous_revision", 0)),
            new_revision=int(d.get("new_revision", 1)),
            reason=d.get("reason", d.get("change_reason", "")),
            change_reason=d.get("change_reason", d.get("reason", "")),
            changed_fields=d.get("changed_fields", d.get("field_changes", {})),
            field_changes=d.get("field_changes", d.get("changed_fields", {})),
            new_snapshot=d.get("new_snapshot", {}),
            confidence_before=d.get("confidence_before"),
            confidence_after=d.get("confidence_after"),
            revised_by=d.get("revised_by", "user"),
            point_in_time_verified=bool(d.get("point_in_time_verified", False)),
            created_at=d.get("created_at", _now_utc()),
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
        )


# ---------------------------------------------------------------------------
# DecisionJournalLink
# ---------------------------------------------------------------------------

@dataclass
class DecisionJournalLink:
    """
    Link between journal entries or to session/scenario/checkpoint.
    """
    link_id: str
    source_entry_id: str
    target_entry_id: str
    relation_type: str = RelationType.FOLLOW_UP.value
    journal_entry_id: str = ""
    session_id: str = ""
    scenario_id: Optional[str] = None
    checkpoint_id: Optional[str] = None
    decision_id: str = ""
    parent_journal_entry_id: Optional[str] = None
    supersedes_entry_id: Optional[str] = None
    related_entry_ids: List[str] = field(default_factory=list)
    notes: str = ""
    created_at: str = field(default_factory=_now_utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "link_id": self.link_id,
            "source_entry_id": self.source_entry_id,
            "target_entry_id": self.target_entry_id,
            "relation_type": self.relation_type,
            "journal_entry_id": self.journal_entry_id,
            "session_id": self.session_id,
            "scenario_id": self.scenario_id,
            "checkpoint_id": self.checkpoint_id,
            "decision_id": self.decision_id,
            "parent_journal_entry_id": self.parent_journal_entry_id,
            "supersedes_entry_id": self.supersedes_entry_id,
            "related_entry_ids": self.related_entry_ids,
            "notes": self.notes,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DecisionJournalLink":
        return cls(
            link_id=d.get("link_id", _new_id("LNK-")),
            source_entry_id=d.get("source_entry_id", ""),
            target_entry_id=d.get("target_entry_id", ""),
            relation_type=d.get("relation_type", RelationType.FOLLOW_UP.value),
            journal_entry_id=d.get("journal_entry_id", ""),
            session_id=d.get("session_id", ""),
            scenario_id=d.get("scenario_id"),
            checkpoint_id=d.get("checkpoint_id"),
            decision_id=d.get("decision_id", ""),
            parent_journal_entry_id=d.get("parent_journal_entry_id"),
            supersedes_entry_id=d.get("supersedes_entry_id"),
            related_entry_ids=d.get("related_entry_ids", []),
            notes=d.get("notes", ""),
            created_at=d.get("created_at", _now_utc()),
        )
