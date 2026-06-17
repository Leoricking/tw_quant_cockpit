"""
replay/strategy_replay_schema.py — Strategy Knowledge Replay schemas for v1.2.4

[!] Research Only. No Real Orders. Replay Training Only.
[!] Strategy Knowledge Replay NEVER triggers paper orders or broker execution.
[!] All snapshots are point-in-time verified. No forward return. No outcome.
[!] Auto Strategy Decision DISABLED. Auto Strategy Execution DISABLED.
[!] Auto Strategy Weight Change DISABLED. Not Investment Advice.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
REPLAY_TRAINING_ONLY = True
AUTO_STRATEGY_DECISION_ENABLED = False
AUTO_STRATEGY_EXECUTION_ENABLED = False
AUTO_STRATEGY_WEIGHT_CHANGE_ENABLED = False
AUTO_STRATEGY_MISTAKE_CONFIRMATION_ENABLED = False
REPLAY_TRADE_EXECUTION_ENABLED = False

SNAPSHOT_ID_PREFIX = "SSN-"
MODULE_RESULT_ID_PREFIX = "SMR-"
TIMELINE_RECORD_ID_PREFIX = "STL-"
AGREEMENT_ID_PREFIX = "SAG-"
RULE_REVIEW_ID_PREFIX = "SRR-"

MODULE_NAMES = [
    "KD_ADVANCED",
    "SHORT_INTEREST",
    "BOTTOM_REVERSAL",
    "SECTOR_ROTATION",
    "FUNDAMENTAL_QUALITY",
    "NO_CHASE",
    "NO_PANIC_SELL",
    "DO_NOT_REBUY_YET",
    "ABC_BUY_POINT",
]

FORBIDDEN_SNAPSHOT_FIELDS = [
    "forward_return", "future_return", "hindsight_score",
    "final_result", "future_max_gain", "future_max_loss",
    "realized_pnl", "final_label", "outcome", "answer",
    "broker", "order_token", "api_key", "secret",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}{uuid.uuid4().hex[:12].upper()}"


# ---------------------------------------------------------------------------
# StrategyModuleReplayResult
# ---------------------------------------------------------------------------

@dataclass
class StrategyModuleReplayResult:
    """
    Result for a single strategy module in replay context.
    [!] No forward_return. No outcome. Point-in-time only.
    """
    module_name: str
    replay_date: str
    available: bool
    signal: str
    score: Optional[float]
    warning: str
    reason: str
    evidence: List[str]
    source_fields: List[str]
    source_dates: List[str]
    timing_warning: str
    point_in_time_verified: bool
    confidence: str
    qualification: str
    limitations: List[str]
    generated_at: str = field(default_factory=_now_utc)
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module_name": self.module_name,
            "replay_date": self.replay_date,
            "available": self.available,
            "signal": self.signal,
            "score": self.score,
            "warning": self.warning,
            "reason": self.reason,
            "evidence": self.evidence,
            "source_fields": self.source_fields,
            "source_dates": self.source_dates,
            "timing_warning": self.timing_warning,
            "point_in_time_verified": self.point_in_time_verified,
            "confidence": self.confidence,
            "qualification": self.qualification,
            "limitations": self.limitations,
            "generated_at": self.generated_at,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "StrategyModuleReplayResult":
        return cls(
            module_name=d.get("module_name", ""),
            replay_date=d.get("replay_date", ""),
            available=bool(d.get("available", False)),
            signal=d.get("signal", "UNAVAILABLE"),
            score=d.get("score"),
            warning=d.get("warning", ""),
            reason=d.get("reason", ""),
            evidence=d.get("evidence", []),
            source_fields=d.get("source_fields", []),
            source_dates=d.get("source_dates", []),
            timing_warning=d.get("timing_warning", ""),
            point_in_time_verified=bool(d.get("point_in_time_verified", False)),
            confidence=d.get("confidence", "INSUFFICIENT"),
            qualification=d.get("qualification", "UNAVAILABLE"),
            limitations=d.get("limitations", []),
            generated_at=d.get("generated_at", _now_utc()),
            research_only=True,
            no_real_orders=True,
        )


# ---------------------------------------------------------------------------
# StrategyReplaySnapshot
# ---------------------------------------------------------------------------

@dataclass
class StrategyReplaySnapshot:
    """
    Full strategy knowledge snapshot at a given replay date.
    [!] NO forward_return. NO outcome. NO hindsight. Point-in-time only.
    [!] Not Investment Advice.
    """
    strategy_snapshot_id: str
    session_id: str
    symbol: str
    replay_date: str
    modules: List[dict]
    agreement_score: float
    conflict_score: float
    bullish_modules: List[str]
    bearish_modules: List[str]
    warning_modules: List[str]
    unavailable_modules: List[str]
    point_in_time_verified: bool
    future_fields_blocked: List[str]
    qualification: str
    warnings: List[str]
    source_metadata: dict
    generated_at: str = field(default_factory=_now_utc)
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy_snapshot_id": self.strategy_snapshot_id,
            "session_id": self.session_id,
            "symbol": self.symbol,
            "replay_date": self.replay_date,
            "modules": self.modules,
            "agreement_score": self.agreement_score,
            "conflict_score": self.conflict_score,
            "bullish_modules": self.bullish_modules,
            "bearish_modules": self.bearish_modules,
            "warning_modules": self.warning_modules,
            "unavailable_modules": self.unavailable_modules,
            "point_in_time_verified": self.point_in_time_verified,
            "future_fields_blocked": self.future_fields_blocked,
            "qualification": self.qualification,
            "warnings": self.warnings,
            "source_metadata": self.source_metadata,
            "generated_at": self.generated_at,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "StrategyReplaySnapshot":
        return cls(
            strategy_snapshot_id=d.get("strategy_snapshot_id", _new_id(SNAPSHOT_ID_PREFIX)),
            session_id=d.get("session_id", ""),
            symbol=d.get("symbol", ""),
            replay_date=d.get("replay_date", ""),
            modules=d.get("modules", []),
            agreement_score=float(d.get("agreement_score", 0.0)),
            conflict_score=float(d.get("conflict_score", 0.0)),
            bullish_modules=d.get("bullish_modules", []),
            bearish_modules=d.get("bearish_modules", []),
            warning_modules=d.get("warning_modules", []),
            unavailable_modules=d.get("unavailable_modules", []),
            point_in_time_verified=bool(d.get("point_in_time_verified", False)),
            future_fields_blocked=d.get("future_fields_blocked", []),
            qualification=d.get("qualification", "UNAVAILABLE"),
            warnings=d.get("warnings", []),
            source_metadata=d.get("source_metadata", {}),
            generated_at=d.get("generated_at", _now_utc()),
            research_only=True,
            no_real_orders=True,
        )


# ---------------------------------------------------------------------------
# StrategySignalTimelineRecord
# ---------------------------------------------------------------------------

@dataclass
class StrategySignalTimelineRecord:
    """
    Single signal timeline record for one module at one date.
    """
    timeline_record_id: str
    session_id: str
    symbol: str
    replay_date: str
    module_name: str
    signal_name: str
    signal_value: str
    score: Optional[float]
    warning: str
    reason: str
    confidence: str
    qualification: str
    point_in_time_verified: bool
    created_at: str = field(default_factory=_now_utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timeline_record_id": self.timeline_record_id,
            "session_id": self.session_id,
            "symbol": self.symbol,
            "replay_date": self.replay_date,
            "module_name": self.module_name,
            "signal_name": self.signal_name,
            "signal_value": self.signal_value,
            "score": self.score,
            "warning": self.warning,
            "reason": self.reason,
            "confidence": self.confidence,
            "qualification": self.qualification,
            "point_in_time_verified": self.point_in_time_verified,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "StrategySignalTimelineRecord":
        return cls(
            timeline_record_id=d.get("timeline_record_id", _new_id(TIMELINE_RECORD_ID_PREFIX)),
            session_id=d.get("session_id", ""),
            symbol=d.get("symbol", ""),
            replay_date=d.get("replay_date", ""),
            module_name=d.get("module_name", ""),
            signal_name=d.get("signal_name", ""),
            signal_value=d.get("signal_value", ""),
            score=d.get("score"),
            warning=d.get("warning", ""),
            reason=d.get("reason", ""),
            confidence=d.get("confidence", "INSUFFICIENT"),
            qualification=d.get("qualification", "UNAVAILABLE"),
            point_in_time_verified=bool(d.get("point_in_time_verified", False)),
            created_at=d.get("created_at", _now_utc()),
        )


# ---------------------------------------------------------------------------
# StrategyAgreementResult
# ---------------------------------------------------------------------------

@dataclass
class StrategyAgreementResult:
    """
    Agreement/conflict analysis result for a strategy snapshot.
    [!] UNAVAILABLE modules are NOT counted as bearish.
    [!] Confidence INSUFFICIENT if < 3 modules available.
    """
    agreement_id: str
    session_id: str
    replay_date: str
    bullish_count: int
    bearish_count: int
    neutral_count: int
    warning_count: int
    unavailable_count: int
    agreement_score: float
    conflict_score: float
    aligned_modules: List[str]
    conflicting_modules: List[str]
    reasons: List[str]
    confidence: str
    status: str  # STRONG_ALIGNMENT, MODERATE_ALIGNMENT, MIXED, STRONG_CONFLICT, INSUFFICIENT, BLOCKED
    created_at: str = field(default_factory=_now_utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agreement_id": self.agreement_id,
            "session_id": self.session_id,
            "replay_date": self.replay_date,
            "bullish_count": self.bullish_count,
            "bearish_count": self.bearish_count,
            "neutral_count": self.neutral_count,
            "warning_count": self.warning_count,
            "unavailable_count": self.unavailable_count,
            "agreement_score": self.agreement_score,
            "conflict_score": self.conflict_score,
            "aligned_modules": self.aligned_modules,
            "conflicting_modules": self.conflicting_modules,
            "reasons": self.reasons,
            "confidence": self.confidence,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "StrategyAgreementResult":
        return cls(
            agreement_id=d.get("agreement_id", _new_id(AGREEMENT_ID_PREFIX)),
            session_id=d.get("session_id", ""),
            replay_date=d.get("replay_date", ""),
            bullish_count=int(d.get("bullish_count", 0)),
            bearish_count=int(d.get("bearish_count", 0)),
            neutral_count=int(d.get("neutral_count", 0)),
            warning_count=int(d.get("warning_count", 0)),
            unavailable_count=int(d.get("unavailable_count", 0)),
            agreement_score=float(d.get("agreement_score", 0.0)),
            conflict_score=float(d.get("conflict_score", 0.0)),
            aligned_modules=d.get("aligned_modules", []),
            conflicting_modules=d.get("conflicting_modules", []),
            reasons=d.get("reasons", []),
            confidence=d.get("confidence", "INSUFFICIENT"),
            status=d.get("status", "INSUFFICIENT"),
            created_at=d.get("created_at", _now_utc()),
        )


# ---------------------------------------------------------------------------
# StrategyRuleReviewRecord
# ---------------------------------------------------------------------------

@dataclass
class StrategyRuleReviewRecord:
    """
    Review record comparing a strategy rule signal to a decision action.
    [!] All reviews start as SUGGESTED. System cannot auto-CONFIRM.
    [!] Planned stop not auto-CONTRADICTED for No Panic Sell.
    [!] Planned breakout not auto-chasing for No Chase.
    """
    review_id: str
    session_id: str
    journal_entry_id: Optional[str]
    decision_id: Optional[str]
    replay_date: str
    module_name: str
    rule_signal: str
    decision_action: str
    relationship: str  # FOLLOWED, IGNORED, CONTRADICTED, NOT_APPLICABLE, INSUFFICIENT
    system_suggested: bool
    user_confirmed: bool
    evidence: List[str]
    counter_evidence: List[str]
    confidence: str
    status: str  # SUGGESTED, CONFIRMED, DISMISSED, OVERRIDDEN, NEEDS_REVIEW, INSUFFICIENT, BLOCKED
    note: str
    created_at: str = field(default_factory=_now_utc)
    updated_at: str = field(default_factory=_now_utc)
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "review_id": self.review_id,
            "session_id": self.session_id,
            "journal_entry_id": self.journal_entry_id,
            "decision_id": self.decision_id,
            "replay_date": self.replay_date,
            "module_name": self.module_name,
            "rule_signal": self.rule_signal,
            "decision_action": self.decision_action,
            "relationship": self.relationship,
            "system_suggested": self.system_suggested,
            "user_confirmed": self.user_confirmed,
            "evidence": self.evidence,
            "counter_evidence": self.counter_evidence,
            "confidence": self.confidence,
            "status": self.status,
            "note": self.note,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "StrategyRuleReviewRecord":
        return cls(
            review_id=d.get("review_id", _new_id(RULE_REVIEW_ID_PREFIX)),
            session_id=d.get("session_id", ""),
            journal_entry_id=d.get("journal_entry_id"),
            decision_id=d.get("decision_id"),
            replay_date=d.get("replay_date", ""),
            module_name=d.get("module_name", ""),
            rule_signal=d.get("rule_signal", ""),
            decision_action=d.get("decision_action", ""),
            relationship=d.get("relationship", "INSUFFICIENT"),
            system_suggested=bool(d.get("system_suggested", True)),
            user_confirmed=bool(d.get("user_confirmed", False)),
            evidence=d.get("evidence", []),
            counter_evidence=d.get("counter_evidence", []),
            confidence=d.get("confidence", "INSUFFICIENT"),
            status=d.get("status", "SUGGESTED"),
            note=d.get("note", ""),
            created_at=d.get("created_at", _now_utc()),
            updated_at=d.get("updated_at", _now_utc()),
            research_only=True,
            no_real_orders=True,
        )
