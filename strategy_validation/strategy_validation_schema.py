"""
strategy_validation/strategy_validation_schema.py
TW Quant Cockpit — Strategy Validation Score Schema
v0.9.2 — Research Only / No Real Orders / VALIDATED does not enable trading

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] VALIDATED grade means research-validated ONLY. Does NOT enable trading.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

VERSION = "v0.9.2"

# ---------------------------------------------------------------------------
# Validation grades
# ---------------------------------------------------------------------------
GRADE_INSUFFICIENT  = "INSUFFICIENT"
GRADE_OBSERVATIONAL = "OBSERVATIONAL"
GRADE_VALIDATING    = "VALIDATING"
GRADE_VALIDATED     = "VALIDATED"
GRADE_CONFLICTED    = "CONFLICTED"
GRADE_REJECTED      = "REJECTED"
ALL_GRADES = [
    GRADE_INSUFFICIENT, GRADE_OBSERVATIONAL, GRADE_VALIDATING,
    GRADE_VALIDATED, GRADE_CONFLICTED, GRADE_REJECTED,
]

# ---------------------------------------------------------------------------
# Strategy types
# ---------------------------------------------------------------------------
STYPE_RULE_CANDIDATE        = "RULE_CANDIDATE"
STYPE_STRATEGY_HYPOTHESIS   = "STRATEGY_HYPOTHESIS"
STYPE_CRASH_REVERSAL_RULE   = "CRASH_REVERSAL_RULE"
STYPE_MEMORY_RULE           = "MEMORY_RULE"
STYPE_BACKTEST_RULE         = "BACKTEST_RULE"
STYPE_REPLAY_PATTERN        = "REPLAY_PATTERN"
STYPE_JOURNAL_PATTERN       = "JOURNAL_PATTERN"
STYPE_RISK_GUARD            = "RISK_GUARD"
STYPE_DATA_DEPENDENT        = "DATA_DEPENDENT_RULE"
STYPE_UNKNOWN               = "UNKNOWN"

# ---------------------------------------------------------------------------
# Status values
# ---------------------------------------------------------------------------
STATUS_ACTIVE_RESEARCH      = "ACTIVE_RESEARCH"
STATUS_NEEDS_DATA           = "NEEDS_MORE_DATA"
STATUS_NEEDS_BACKTEST       = "NEEDS_BACKTEST"
STATUS_NEEDS_REPLAY         = "NEEDS_REPLAY"
STATUS_NEEDS_JOURNAL        = "NEEDS_JOURNAL_REVIEW"
STATUS_CONFLICTED           = "CONFLICTED_EVIDENCE"
STATUS_RESEARCH_VALIDATED   = "RESEARCH_VALIDATED"
STATUS_RESEARCH_REJECTED    = "RESEARCH_REJECTED"
STATUS_UNKNOWN              = "UNKNOWN"

# ---------------------------------------------------------------------------
# Component types
# ---------------------------------------------------------------------------
COMP_BACKTEST         = "BACKTEST"
COMP_REPLAY           = "REPLAY"
COMP_JOURNAL          = "JOURNAL"
COMP_TRAINING_METRICS = "TRAINING_METRICS"
COMP_EVIDENCE_GRAPH   = "EVIDENCE_GRAPH"
COMP_DATA_COVERAGE    = "DATA_COVERAGE"
COMP_RISK_GUARD       = "RISK_GUARD"
COMP_FUNDAMENTAL      = "FUNDAMENTAL_SUPPORT"
COMP_CHIP             = "CHIP_SUPPORT"
COMP_TECHNICAL        = "TECHNICAL_SUPPORT"
COMP_CONTRADICTION    = "CONTRADICTION_PENALTY"
COMP_SAMPLE_PENALTY   = "SAMPLE_SIZE_PENALTY"

# ---------------------------------------------------------------------------
# Safe next steps / forbidden actions
# ---------------------------------------------------------------------------
SAFE_NEXT_STEPS = frozenset([
    "REVIEW", "VALIDATE", "BACKTEST_MORE", "PRACTICE_REPLAY", "REVIEW_JOURNAL",
    "FIX_DATA", "READ_REPORT", "WAIT", "REVIEW_RISK", "REVIEW_EARNINGS",
    "REVIEW_CHIPS", "BUILD_WATCHLIST", "DO_NOT_CHASE", "KEEP_OBSERVING",
    "MARK_RESEARCH_ONLY",
])
FORBIDDEN_ACTIONS = frozenset([
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE",
])

read_only                         = True
no_real_orders                    = True
production_blocked                = True
validated_does_not_enable_trading = True


def _guard_next_step(value: str) -> str:
    """Ensure suggested_next_step is never a forbidden action."""
    if value in FORBIDDEN_ACTIONS:
        return "REVIEW"
    if value not in SAFE_NEXT_STEPS:
        return "REVIEW"
    return value


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class StrategyValidationScore:
    """
    Research-only validation score for a strategy candidate.
    VALIDATED grade does NOT enable trading.
    """
    validation_id:                    str   = ""
    strategy_id:                      str   = ""
    strategy_name:                    str   = ""
    strategy_type:                    str   = "UNKNOWN"
    source_module:                    str   = ""
    source_ref:                       str   = ""
    validation_grade:                 str   = "INSUFFICIENT"
    validation_score:                 float = 0.0
    confidence:                       float = 0.0
    sample_count:                     int   = 0
    symbol_count:                     int   = 0
    evidence_thread_count:            int   = 0
    support_count:                    int   = 0
    contradiction_count:              int   = 0
    backtest_score:                   float = 0.0
    replay_score:                     float = 0.0
    journal_score:                    float = 0.0
    training_metric_score:            float = 0.0
    evidence_graph_score:             float = 0.0
    data_coverage_score:              float = 0.0
    risk_penalty:                     float = 0.0
    final_score:                      float = 0.0
    status:                           str   = "UNKNOWN"
    suggested_next_step:              str   = "REVIEW"
    reason:                           str   = ""
    limitations:                      str   = ""
    created_at:                       str   = ""
    updated_at:                       str   = ""
    read_only:                        bool  = True
    no_real_orders:                   bool  = True
    production_blocked:               bool  = True
    validated_does_not_enable_trading: bool = True

    def __post_init__(self) -> None:
        now = datetime.now().isoformat()
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now
        self.suggested_next_step = _guard_next_step(self.suggested_next_step)
        # Safety hard-locks
        self.read_only                         = True
        self.no_real_orders                    = True
        self.production_blocked                = True
        self.validated_does_not_enable_trading = True

    def to_dict(self) -> dict:
        return {
            "validation_id":                    self.validation_id,
            "strategy_id":                      self.strategy_id,
            "strategy_name":                    self.strategy_name,
            "strategy_type":                    self.strategy_type,
            "source_module":                    self.source_module,
            "source_ref":                       self.source_ref,
            "validation_grade":                 self.validation_grade,
            "validation_score":                 self.validation_score,
            "confidence":                       self.confidence,
            "sample_count":                     self.sample_count,
            "symbol_count":                     self.symbol_count,
            "evidence_thread_count":            self.evidence_thread_count,
            "support_count":                    self.support_count,
            "contradiction_count":              self.contradiction_count,
            "backtest_score":                   self.backtest_score,
            "replay_score":                     self.replay_score,
            "journal_score":                    self.journal_score,
            "training_metric_score":            self.training_metric_score,
            "evidence_graph_score":             self.evidence_graph_score,
            "data_coverage_score":              self.data_coverage_score,
            "risk_penalty":                     self.risk_penalty,
            "final_score":                      self.final_score,
            "status":                           self.status,
            "suggested_next_step":              self.suggested_next_step,
            "reason":                           self.reason,
            "limitations":                      self.limitations,
            "created_at":                       self.created_at,
            "updated_at":                       self.updated_at,
            "read_only":                        self.read_only,
            "no_real_orders":                   self.no_real_orders,
            "production_blocked":               self.production_blocked,
            "validated_does_not_enable_trading": self.validated_does_not_enable_trading,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyValidationScore":
        def _f(key, default=0.0):
            try:
                return float(d.get(key, default))
            except (TypeError, ValueError):
                return default

        def _i(key, default=0):
            try:
                return int(d.get(key, default))
            except (TypeError, ValueError):
                return default

        def _b(key, default=True):
            v = d.get(key, default)
            if isinstance(v, bool):
                return v
            if isinstance(v, str):
                return v.strip().lower() not in ("false", "0", "no", "")
            return bool(v)

        return cls(
            validation_id=str(d.get("validation_id", "")),
            strategy_id=str(d.get("strategy_id", "")),
            strategy_name=str(d.get("strategy_name", "")),
            strategy_type=str(d.get("strategy_type", "UNKNOWN")),
            source_module=str(d.get("source_module", "")),
            source_ref=str(d.get("source_ref", "")),
            validation_grade=str(d.get("validation_grade", GRADE_INSUFFICIENT)),
            validation_score=_f("validation_score"),
            confidence=_f("confidence"),
            sample_count=_i("sample_count"),
            symbol_count=_i("symbol_count"),
            evidence_thread_count=_i("evidence_thread_count"),
            support_count=_i("support_count"),
            contradiction_count=_i("contradiction_count"),
            backtest_score=_f("backtest_score"),
            replay_score=_f("replay_score"),
            journal_score=_f("journal_score"),
            training_metric_score=_f("training_metric_score"),
            evidence_graph_score=_f("evidence_graph_score"),
            data_coverage_score=_f("data_coverage_score"),
            risk_penalty=_f("risk_penalty"),
            final_score=_f("final_score"),
            status=str(d.get("status", STATUS_UNKNOWN)),
            suggested_next_step=str(d.get("suggested_next_step", "REVIEW")),
            reason=str(d.get("reason", "")),
            limitations=str(d.get("limitations", "")),
            created_at=str(d.get("created_at", "")),
            updated_at=str(d.get("updated_at", "")),
            read_only=True,
            no_real_orders=True,
            production_blocked=True,
            validated_does_not_enable_trading=True,
        )


@dataclass
class StrategyValidationComponent:
    """
    A single evidence component contributing to a validation score.
    Research Only. No Real Orders.
    """
    component_id:  str   = ""
    strategy_id:   str   = ""
    component_type: str  = ""
    score:         float = 0.0
    weight:        float = 0.0
    weighted_score: float = 0.0
    evidence:      str   = ""
    status:        str   = ""
    limitation:    str   = ""
    source_module: str   = ""

    def to_dict(self) -> dict:
        return {
            "component_id":   self.component_id,
            "strategy_id":    self.strategy_id,
            "component_type": self.component_type,
            "score":          self.score,
            "weight":         self.weight,
            "weighted_score": self.weighted_score,
            "evidence":       self.evidence,
            "status":         self.status,
            "limitation":     self.limitation,
            "source_module":  self.source_module,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyValidationComponent":
        def _f(key, default=0.0):
            try:
                return float(d.get(key, default))
            except (TypeError, ValueError):
                return default

        return cls(
            component_id=str(d.get("component_id", "")),
            strategy_id=str(d.get("strategy_id", "")),
            component_type=str(d.get("component_type", "")),
            score=_f("score"),
            weight=_f("weight"),
            weighted_score=_f("weighted_score"),
            evidence=str(d.get("evidence", "")),
            status=str(d.get("status", "")),
            limitation=str(d.get("limitation", "")),
            source_module=str(d.get("source_module", "")),
        )


@dataclass
class StrategyValidationSummary:
    """
    Aggregate summary of all strategy validation scores.
    Research Only. No Real Orders. VALIDATED does not enable trading.
    """
    generated_at:                      str   = ""
    mode:                              str   = "real"
    total_strategies:                  int   = 0
    insufficient_count:                int   = 0
    observational_count:               int   = 0
    validating_count:                  int   = 0
    validated_count:                   int   = 0
    conflicted_count:                  int   = 0
    rejected_count:                    int   = 0
    avg_score:                         float = 0.0
    top_validated:                     str   = ""
    top_needs_backtest:                str   = ""
    top_conflicted:                    str   = ""
    forbidden_action_count:            int   = 0
    no_real_orders:                    bool  = True
    production_blocked:                bool  = True
    validated_does_not_enable_trading: bool  = True

    def __post_init__(self) -> None:
        if not self.generated_at:
            self.generated_at = datetime.now().isoformat()
        self.no_real_orders                    = True
        self.production_blocked                = True
        self.validated_does_not_enable_trading = True

    def to_dict(self) -> dict:
        return {
            "generated_at":                      self.generated_at,
            "mode":                              self.mode,
            "total_strategies":                  self.total_strategies,
            "insufficient_count":                self.insufficient_count,
            "observational_count":               self.observational_count,
            "validating_count":                  self.validating_count,
            "validated_count":                   self.validated_count,
            "conflicted_count":                  self.conflicted_count,
            "rejected_count":                    self.rejected_count,
            "avg_score":                         self.avg_score,
            "top_validated":                     self.top_validated,
            "top_needs_backtest":                self.top_needs_backtest,
            "top_conflicted":                    self.top_conflicted,
            "forbidden_action_count":            self.forbidden_action_count,
            "no_real_orders":                    self.no_real_orders,
            "production_blocked":                self.production_blocked,
            "validated_does_not_enable_trading": self.validated_does_not_enable_trading,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StrategyValidationSummary":
        def _i(key, default=0):
            try:
                return int(d.get(key, default))
            except (TypeError, ValueError):
                return default

        def _f(key, default=0.0):
            try:
                return float(d.get(key, default))
            except (TypeError, ValueError):
                return default

        return cls(
            generated_at=str(d.get("generated_at", "")),
            mode=str(d.get("mode", "real")),
            total_strategies=_i("total_strategies"),
            insufficient_count=_i("insufficient_count"),
            observational_count=_i("observational_count"),
            validating_count=_i("validating_count"),
            validated_count=_i("validated_count"),
            conflicted_count=_i("conflicted_count"),
            rejected_count=_i("rejected_count"),
            avg_score=_f("avg_score"),
            top_validated=str(d.get("top_validated", "")),
            top_needs_backtest=str(d.get("top_needs_backtest", "")),
            top_conflicted=str(d.get("top_conflicted", "")),
            forbidden_action_count=_i("forbidden_action_count"),
            no_real_orders=True,
            production_blocked=True,
            validated_does_not_enable_trading=True,
        )
