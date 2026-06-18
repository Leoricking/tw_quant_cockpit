"""
replay/challenge_schema.py — Replay Challenge Mode dataclasses v1.2.7

[!] Challenge Training Only. Simulation Only. No Real Orders. Not Investment Advice.
[!] Future data hidden. Outcome hidden until explicit reveal. Answer Key separate.
[!] Process weight always >= Outcome weight. No auto-decision. No auto-reveal.
[!] No Public Leaderboard. No Network Submission. Local personal records only.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


NO_REAL_ORDERS = True
RESEARCH_ONLY = True
CHALLENGE_TRAINING_ONLY = True
SIMULATION_ONLY = True
PUBLIC_LEADERBOARD_ENABLED = False
NETWORK_SUBMISSION_ENABLED = False
AUTO_DECISION_ENABLED = False
AUTO_REVEAL_ENABLED = False
AUTO_CONFIRM_ENABLED = False


def _new_id(prefix: str = "CHG-") -> str:
    return f"{prefix}{uuid.uuid4().hex[:10].upper()}"


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Enums (string constants)
# ---------------------------------------------------------------------------

class ChallengeType:
    FREE_DECISION          = "FREE_DECISION"
    TIMED_DECISION         = "TIMED_DECISION"
    NO_CHASE               = "NO_CHASE"
    NO_PANIC_SELL          = "NO_PANIC_SELL"
    DO_NOT_REBUY_YET       = "DO_NOT_REBUY_YET"
    BOTTOM_REVERSAL        = "BOTTOM_REVERSAL"
    BREAKOUT               = "BREAKOUT"
    PULLBACK               = "PULLBACK"
    RISK_CONTROL           = "RISK_CONTROL"
    JOURNAL_DISCIPLINE     = "JOURNAL_DISCIPLINE"
    STRATEGY_CONFLICT      = "STRATEGY_CONFLICT"
    TIMEFRAME_CONFLICT     = "TIMEFRAME_CONFLICT"
    POINT_IN_TIME          = "POINT_IN_TIME"
    DATA_INTEGRITY         = "DATA_INTEGRITY"
    MISTAKE_CORRECTION     = "MISTAKE_CORRECTION"
    CUSTOM                 = "CUSTOM"

    ALL = [
        FREE_DECISION, TIMED_DECISION, NO_CHASE, NO_PANIC_SELL,
        DO_NOT_REBUY_YET, BOTTOM_REVERSAL, BREAKOUT, PULLBACK,
        RISK_CONTROL, JOURNAL_DISCIPLINE, STRATEGY_CONFLICT,
        TIMEFRAME_CONFLICT, POINT_IN_TIME, DATA_INTEGRITY,
        MISTAKE_CORRECTION, CUSTOM,
    ]


class ChallengeDifficulty:
    BEGINNER     = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED     = "ADVANCED"
    EXPERT       = "EXPERT"
    CUSTOM       = "CUSTOM"

    ALL = [BEGINNER, INTERMEDIATE, ADVANCED, EXPERT, CUSTOM]


class AttemptStatus:
    NOT_STARTED   = "NOT_STARTED"
    RUNNING       = "RUNNING"
    PAUSED        = "PAUSED"
    COMPLETED     = "COMPLETED"
    TIMEOUT       = "TIMEOUT"
    CANCELLED     = "CANCELLED"
    BLOCKED       = "BLOCKED"
    INSUFFICIENT  = "INSUFFICIENT"


class ActionType:
    VIEW_CONTEXT               = "VIEW_CONTEXT"
    VIEW_TIMEFRAME             = "VIEW_TIMEFRAME"
    VIEW_STRATEGY              = "VIEW_STRATEGY"
    WRITE_THESIS               = "WRITE_THESIS"
    WRITE_RISK_PLAN            = "WRITE_RISK_PLAN"
    WRITE_CHECKLIST            = "WRITE_CHECKLIST"
    DECIDE_WAIT                = "DECIDE_WAIT"
    DECIDE_ENTER               = "DECIDE_ENTER"   # SIMULATION DECISION ONLY
    DECIDE_ADD                 = "DECIDE_ADD"     # SIMULATION DECISION ONLY
    DECIDE_REDUCE              = "DECIDE_REDUCE"  # SIMULATION DECISION ONLY
    DECIDE_EXIT                = "DECIDE_EXIT"    # SIMULATION DECISION ONLY
    DECIDE_SKIP                = "DECIDE_SKIP"
    REQUEST_HINT               = "REQUEST_HINT"
    PAUSE                      = "PAUSE"
    RESUME                     = "RESUME"
    COMPLETE                   = "COMPLETE"
    CANCEL                     = "CANCEL"

    ALL = [
        VIEW_CONTEXT, VIEW_TIMEFRAME, VIEW_STRATEGY,
        WRITE_THESIS, WRITE_RISK_PLAN, WRITE_CHECKLIST,
        DECIDE_WAIT, DECIDE_ENTER, DECIDE_ADD, DECIDE_REDUCE, DECIDE_EXIT, DECIDE_SKIP,
        REQUEST_HINT, PAUSE, RESUME, COMPLETE, CANCEL,
    ]

    SIMULATION_DECISION_ACTIONS = [DECIDE_ENTER, DECIDE_ADD, DECIDE_REDUCE, DECIDE_EXIT]


class ScoreClassification:
    EXCELLENT_PROCESS        = "EXCELLENT_PROCESS"
    GOOD_PROCESS             = "GOOD_PROCESS"
    MIXED_PROCESS            = "MIXED_PROCESS"
    WEAK_PROCESS             = "WEAK_PROCESS"
    PROCESS_ONLY             = "PROCESS_ONLY"
    GOOD_PROCESS_BAD_OUTCOME = "GOOD_PROCESS_BAD_OUTCOME"
    BAD_PROCESS_GOOD_OUTCOME = "BAD_PROCESS_GOOD_OUTCOME"
    INSUFFICIENT             = "INSUFFICIENT"
    BLOCKED                  = "BLOCKED"
    DEMO_ONLY                = "DEMO_ONLY"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ReplayChallengeDefinition:
    """
    Challenge definition dataclass.

    [!] Challenge Training Only. Simulation Only. No Real Orders.
    [!] Future data hidden. No auto-decision. No Public Leaderboard.
    """
    challenge_id:        str = field(default_factory=lambda: _new_id("CHG-"))
    title:               str = ""
    description:         str = ""
    challenge_type:      str = ChallengeType.FREE_DECISION
    difficulty:          str = ChallengeDifficulty.INTERMEDIATE
    scenario_id:         Optional[str] = None
    symbol:              Optional[str] = None
    hidden_symbol:       bool = False
    hidden_date:         bool = False
    hidden_outcome:      bool = True
    mode:                str = "mock"
    start_timestamp:     Optional[str] = None
    end_timestamp:       Optional[str] = None
    primary_timeframe:   str = "D1"
    enabled_timeframes:  List[str] = field(default_factory=lambda: ["D1"])
    objectives:          List[Dict[str, Any]] = field(default_factory=list)
    rules:               List[Dict[str, Any]] = field(default_factory=list)
    constraints:         Dict[str, Any] = field(default_factory=dict)
    max_duration_seconds: Optional[int] = None
    max_steps:           Optional[int] = None
    max_actions:         Optional[int] = None
    hint_limit:          int = 3
    hint_penalty:        float = 5.0
    completion_bonus:    float = 5.0
    process_weight:      float = 0.80
    outcome_weight:      float = 0.20
    seed:                Optional[str] = None
    qualification:       str = "TRAINING"
    created_at:          str = field(default_factory=_now_utc)
    archived:            bool = False
    research_only:       bool = True
    no_real_orders:      bool = True

    def __post_init__(self) -> None:
        # Safety invariants
        assert self.research_only is True, "research_only must be True"
        assert self.no_real_orders is True, "no_real_orders must be True"
        assert self.process_weight >= self.outcome_weight, (
            "process_weight must be >= outcome_weight"
        )
        assert self.outcome_weight <= 0.20, "outcome_weight max 20%"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "challenge_id":        self.challenge_id,
            "title":               self.title,
            "description":         self.description,
            "challenge_type":      self.challenge_type,
            "difficulty":          self.difficulty,
            "scenario_id":         self.scenario_id,
            "symbol":              self.symbol,
            "hidden_symbol":       self.hidden_symbol,
            "hidden_date":         self.hidden_date,
            "hidden_outcome":      self.hidden_outcome,
            "mode":                self.mode,
            "start_timestamp":     self.start_timestamp,
            "end_timestamp":       self.end_timestamp,
            "primary_timeframe":   self.primary_timeframe,
            "enabled_timeframes":  self.enabled_timeframes,
            "objectives":          self.objectives,
            "rules":               self.rules,
            "constraints":         self.constraints,
            "max_duration_seconds": self.max_duration_seconds,
            "max_steps":           self.max_steps,
            "max_actions":         self.max_actions,
            "hint_limit":          self.hint_limit,
            "hint_penalty":        self.hint_penalty,
            "completion_bonus":    self.completion_bonus,
            "process_weight":      self.process_weight,
            "outcome_weight":      self.outcome_weight,
            "seed":                self.seed,
            "qualification":       self.qualification,
            "created_at":          self.created_at,
            "archived":            self.archived,
            "research_only":       self.research_only,
            "no_real_orders":      self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayChallengeDefinition":
        return cls(
            challenge_id=d.get("challenge_id", _new_id("CHG-")),
            title=d.get("title", ""),
            description=d.get("description", ""),
            challenge_type=d.get("challenge_type", ChallengeType.FREE_DECISION),
            difficulty=d.get("difficulty", ChallengeDifficulty.INTERMEDIATE),
            scenario_id=d.get("scenario_id"),
            symbol=d.get("symbol"),
            hidden_symbol=d.get("hidden_symbol", False),
            hidden_date=d.get("hidden_date", False),
            hidden_outcome=d.get("hidden_outcome", True),
            mode=d.get("mode", "mock"),
            start_timestamp=d.get("start_timestamp"),
            end_timestamp=d.get("end_timestamp"),
            primary_timeframe=d.get("primary_timeframe", "D1"),
            enabled_timeframes=d.get("enabled_timeframes", ["D1"]),
            objectives=d.get("objectives", []),
            rules=d.get("rules", []),
            constraints=d.get("constraints", {}),
            max_duration_seconds=d.get("max_duration_seconds"),
            max_steps=d.get("max_steps"),
            max_actions=d.get("max_actions"),
            hint_limit=d.get("hint_limit", 3),
            hint_penalty=d.get("hint_penalty", 5.0),
            completion_bonus=d.get("completion_bonus", 5.0),
            process_weight=d.get("process_weight", 0.80),
            outcome_weight=d.get("outcome_weight", 0.20),
            seed=d.get("seed"),
            qualification=d.get("qualification", "TRAINING"),
            created_at=d.get("created_at", _now_utc()),
            archived=d.get("archived", False),
            research_only=True,
            no_real_orders=True,
        )


@dataclass
class ReplayChallengeAttempt:
    """
    Attempt record for a replay challenge.

    [!] Simulation Only. No Real Orders. Not Investment Advice.
    [!] All trading actions are SIMULATION DECISION ONLY.
    """
    attempt_id:              str = field(default_factory=lambda: _new_id("ATT-"))
    challenge_id:            str = ""
    session_id:              Optional[str] = None
    user_label:              str = ""
    attempt_number:          int = 1
    started_at:              Optional[str] = None
    finished_at:             Optional[str] = None
    active_elapsed_seconds:  float = 0.0
    paused_elapsed_seconds:  float = 0.0
    decision_elapsed_seconds: float = 0.0
    status:                  str = AttemptStatus.NOT_STARTED
    actions:                 List[Dict[str, Any]] = field(default_factory=list)
    hints_used:              int = 0
    steps_used:              int = 0
    final_decision:          Optional[str] = None
    journal_entry_id:        Optional[str] = None
    process_score_id:        Optional[str] = None
    outcome_score_id:        Optional[str] = None
    challenge_score_id:      Optional[str] = None
    result_id:               Optional[str] = None
    review_status:           str = "NOT_REVIEWED"
    seed:                    Optional[str] = None
    mode:                    str = "mock"
    research_only:           bool = True
    no_real_orders:          bool = True

    def __post_init__(self) -> None:
        assert self.research_only is True
        assert self.no_real_orders is True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "attempt_id":              self.attempt_id,
            "challenge_id":            self.challenge_id,
            "session_id":              self.session_id,
            "user_label":              self.user_label,
            "attempt_number":          self.attempt_number,
            "started_at":              self.started_at,
            "finished_at":             self.finished_at,
            "active_elapsed_seconds":  self.active_elapsed_seconds,
            "paused_elapsed_seconds":  self.paused_elapsed_seconds,
            "decision_elapsed_seconds": self.decision_elapsed_seconds,
            "status":                  self.status,
            "actions":                 self.actions,
            "hints_used":              self.hints_used,
            "steps_used":              self.steps_used,
            "final_decision":          self.final_decision,
            "journal_entry_id":        self.journal_entry_id,
            "process_score_id":        self.process_score_id,
            "outcome_score_id":        self.outcome_score_id,
            "challenge_score_id":      self.challenge_score_id,
            "result_id":               self.result_id,
            "review_status":           self.review_status,
            "seed":                    self.seed,
            "mode":                    self.mode,
            "research_only":           self.research_only,
            "no_real_orders":          self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayChallengeAttempt":
        return cls(
            attempt_id=d.get("attempt_id", _new_id("ATT-")),
            challenge_id=d.get("challenge_id", ""),
            session_id=d.get("session_id"),
            user_label=d.get("user_label", ""),
            attempt_number=d.get("attempt_number", 1),
            started_at=d.get("started_at"),
            finished_at=d.get("finished_at"),
            active_elapsed_seconds=d.get("active_elapsed_seconds", 0.0),
            paused_elapsed_seconds=d.get("paused_elapsed_seconds", 0.0),
            decision_elapsed_seconds=d.get("decision_elapsed_seconds", 0.0),
            status=d.get("status", AttemptStatus.NOT_STARTED),
            actions=d.get("actions", []),
            hints_used=d.get("hints_used", 0),
            steps_used=d.get("steps_used", 0),
            final_decision=d.get("final_decision"),
            journal_entry_id=d.get("journal_entry_id"),
            process_score_id=d.get("process_score_id"),
            outcome_score_id=d.get("outcome_score_id"),
            challenge_score_id=d.get("challenge_score_id"),
            result_id=d.get("result_id"),
            review_status=d.get("review_status", "NOT_REVIEWED"),
            seed=d.get("seed"),
            mode=d.get("mode", "mock"),
            research_only=True,
            no_real_orders=True,
        )


@dataclass
class ReplayChallengeScore:
    """
    Challenge scoring record.

    [!] Profit != high score. Loss != low score. Process weight >= Outcome weight.
    [!] Outcome max 20%. WAIT/SKIP not auto-penalized.
    [!] GOOD_PROCESS_BAD_OUTCOME / BAD_PROCESS_GOOD_OUTCOME both supported.
    """
    challenge_score_id:          str = field(default_factory=lambda: _new_id("CSC-"))
    attempt_id:                  str = ""
    process_score:               float = 0.0
    discipline_score:            float = 0.0
    risk_score:                  float = 0.0
    timing_score:                float = 0.0
    information_usage_score:     float = 0.0
    strategy_awareness_score:    float = 0.0
    timeframe_awareness_score:   float = 0.0
    journal_score:               float = 0.0
    mistake_penalty:             float = 0.0
    hint_penalty:                float = 0.0
    timeout_penalty:             float = 0.0
    completion_bonus:            float = 0.0
    outcome_score:               Optional[float] = None
    process_weight:              float = 0.80
    outcome_weight:              float = 0.20
    total_score:                 float = 0.0
    classification:              str = ScoreClassification.PROCESS_ONLY
    confidence:                  str = "LOW"
    qualification:               str = "TRAINING"
    reasons:                     List[str] = field(default_factory=list)
    warnings:                    List[str] = field(default_factory=list)
    calculated_at:               str = field(default_factory=_now_utc)
    research_only:               bool = True
    no_real_orders:              bool = True

    def __post_init__(self) -> None:
        assert self.research_only is True
        assert self.no_real_orders is True
        assert self.process_weight >= self.outcome_weight, "process_weight must be >= outcome_weight"
        assert self.outcome_weight <= 0.20, "outcome_weight max 20%"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "challenge_score_id":      self.challenge_score_id,
            "attempt_id":              self.attempt_id,
            "process_score":           self.process_score,
            "discipline_score":        self.discipline_score,
            "risk_score":              self.risk_score,
            "timing_score":            self.timing_score,
            "information_usage_score": self.information_usage_score,
            "strategy_awareness_score": self.strategy_awareness_score,
            "timeframe_awareness_score": self.timeframe_awareness_score,
            "journal_score":           self.journal_score,
            "mistake_penalty":         self.mistake_penalty,
            "hint_penalty":            self.hint_penalty,
            "timeout_penalty":         self.timeout_penalty,
            "completion_bonus":        self.completion_bonus,
            "outcome_score":           self.outcome_score,
            "process_weight":          self.process_weight,
            "outcome_weight":          self.outcome_weight,
            "total_score":             self.total_score,
            "classification":          self.classification,
            "confidence":              self.confidence,
            "qualification":           self.qualification,
            "reasons":                 self.reasons,
            "warnings":                self.warnings,
            "calculated_at":           self.calculated_at,
            "research_only":           self.research_only,
            "no_real_orders":          self.no_real_orders,
        }


@dataclass
class ReplayChallengeResult:
    """
    Challenge result record.

    [!] Research Only. Simulation Only. No Real Orders. Not Investment Advice.
    """
    result_id:           str = field(default_factory=lambda: _new_id("CRS-"))
    attempt_id:          str = ""
    challenge_id:        str = ""
    completed:           bool = False
    timed_out:           bool = False
    cancelled:           bool = False
    objectives_completed: List[str] = field(default_factory=list)
    objectives_failed:   List[str] = field(default_factory=list)
    rules_followed:      List[str] = field(default_factory=list)
    rules_violated:      List[str] = field(default_factory=list)
    hints_used:          int = 0
    mistakes_suggested:  List[str] = field(default_factory=list)
    process_score:       float = 0.0
    total_score:         float = 0.0
    personal_best:       bool = False
    badges_awarded:      List[str] = field(default_factory=list)
    review_required:     bool = True
    generated_at:        str = field(default_factory=_now_utc)
    research_only:       bool = True
    no_real_orders:      bool = True

    def __post_init__(self) -> None:
        assert self.research_only is True
        assert self.no_real_orders is True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id":             self.result_id,
            "attempt_id":            self.attempt_id,
            "challenge_id":          self.challenge_id,
            "completed":             self.completed,
            "timed_out":             self.timed_out,
            "cancelled":             self.cancelled,
            "objectives_completed":  self.objectives_completed,
            "objectives_failed":     self.objectives_failed,
            "rules_followed":        self.rules_followed,
            "rules_violated":        self.rules_violated,
            "hints_used":            self.hints_used,
            "mistakes_suggested":    self.mistakes_suggested,
            "process_score":         self.process_score,
            "total_score":           self.total_score,
            "personal_best":         self.personal_best,
            "badges_awarded":        self.badges_awarded,
            "review_required":       self.review_required,
            "generated_at":          self.generated_at,
            "research_only":         self.research_only,
            "no_real_orders":        self.no_real_orders,
        }


@dataclass
class ReplayChallengeAction:
    """
    Challenge action log entry. Append-only.

    [!] All trading actions (DECIDE_ENTER/ADD/REDUCE/EXIT) are SIMULATION DECISION ONLY.
    [!] No paper orders. No broker orders. No auto-execution.
    """
    action_id:                str = field(default_factory=lambda: _new_id("ACT-"))
    attempt_id:               str = ""
    replay_timestamp:         Optional[str] = None
    action_type:              str = ActionType.VIEW_CONTEXT
    payload:                  Dict[str, Any] = field(default_factory=dict)
    elapsed_since_start:      float = 0.0
    elapsed_since_previous_action: float = 0.0
    point_in_time_verified:   bool = False
    created_at:               str = field(default_factory=_now_utc)
    simulation_decision_only: bool = True
    no_paper_order:           bool = True
    no_broker_order:          bool = True

    def __post_init__(self) -> None:
        assert self.simulation_decision_only is True
        assert self.no_paper_order is True
        assert self.no_broker_order is True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id":                self.action_id,
            "attempt_id":               self.attempt_id,
            "replay_timestamp":         self.replay_timestamp,
            "action_type":              self.action_type,
            "payload":                  self.payload,
            "elapsed_since_start":      self.elapsed_since_start,
            "elapsed_since_previous_action": self.elapsed_since_previous_action,
            "point_in_time_verified":   self.point_in_time_verified,
            "created_at":               self.created_at,
            "simulation_decision_only": self.simulation_decision_only,
            "no_paper_order":           self.no_paper_order,
            "no_broker_order":          self.no_broker_order,
        }
