"""
replay/timeframe_schema.py — Multi-Timeframe Replay Schema v1.2.5

Dataclass-based schema for multi-timeframe replay: timeframe definitions,
bar data, snapshots, alignment, and agreement results.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Multi-timeframe Replay Only. No Auto Decision. No Auto Execution.
[!] No broker execution. No paper orders. Not Investment Advice.
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
NO_AUTO_DECISION = True
NO_AUTO_EXECUTION = True

FORBIDDEN_MTF_FIELDS = [
    "outcome", "forward_return", "realized_pnl", "hindsight_score",
    "final_session_high", "final_session_low", "future_high", "future_low",
    "broker", "order_token", "api_key", "secret",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}{uuid.uuid4().hex[:12].upper()}"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Timeframe(str, Enum):
    D1  = "D1"
    M60 = "M60"
    M20 = "M20"
    M5  = "M5"
    M1  = "M1"


class AlignmentStatus(str, Enum):
    ALIGNED        = "ALIGNED"
    PARTIAL        = "PARTIAL"
    STALE          = "STALE"
    UNAVAILABLE    = "UNAVAILABLE"
    OUT_OF_SESSION = "OUT_OF_SESSION"
    BLOCKED        = "BLOCKED"


class AgreementStatus(str, Enum):
    STRONG_ALIGNMENT   = "STRONG_ALIGNMENT"
    MODERATE_ALIGNMENT = "MODERATE_ALIGNMENT"
    MIXED              = "MIXED"
    STRONG_CONFLICT    = "STRONG_CONFLICT"
    INSUFFICIENT       = "INSUFFICIENT"
    BLOCKED            = "BLOCKED"


# ---------------------------------------------------------------------------
# TimeframeDefinition
# ---------------------------------------------------------------------------

@dataclass
class TimeframeDefinition:
    """Defines a single timeframe and its position in the hierarchy."""
    timeframe_id: str               # e.g. "D1", "M60"
    label: str                      # e.g. "Daily", "60m"
    minutes: int                    # D1=390, M60=60, M20=20, M5=5, M1=1
    parent_timeframe: Optional[str] = None
    child_timeframe: Optional[str]  = None
    enabled: bool                   = True
    formal_supported: bool          = True
    partial_bar_supported: bool     = True
    indicator_supported: bool       = True
    strategy_supported: bool        = True
    source_priority: int            = 1
    research_only: bool             = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timeframe_id": self.timeframe_id,
            "label": self.label,
            "minutes": self.minutes,
            "parent_timeframe": self.parent_timeframe,
            "child_timeframe": self.child_timeframe,
            "enabled": self.enabled,
            "formal_supported": self.formal_supported,
            "partial_bar_supported": self.partial_bar_supported,
            "indicator_supported": self.indicator_supported,
            "strategy_supported": self.strategy_supported,
            "source_priority": self.source_priority,
            "research_only": self.research_only,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TimeframeDefinition":
        return cls(
            timeframe_id=d["timeframe_id"],
            label=d["label"],
            minutes=d["minutes"],
            parent_timeframe=d.get("parent_timeframe"),
            child_timeframe=d.get("child_timeframe"),
            enabled=d.get("enabled", True),
            formal_supported=d.get("formal_supported", True),
            partial_bar_supported=d.get("partial_bar_supported", True),
            indicator_supported=d.get("indicator_supported", True),
            strategy_supported=d.get("strategy_supported", True),
            source_priority=d.get("source_priority", 1),
            research_only=d.get("research_only", True),
        )


# ---------------------------------------------------------------------------
# TimeframeBar
# ---------------------------------------------------------------------------

@dataclass
class TimeframeBar:
    """A single OHLCV bar for a given symbol and timeframe."""
    symbol: str
    timeframe: str
    timestamp: str
    session_date: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    amount: float
    is_complete: bool
    is_partial: bool
    source: str
    source_timestamp: Optional[str] = None
    available_at: Optional[str]     = None
    point_in_time_verified: bool    = False
    qualification: str              = "UNVERIFIED"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "timestamp": self.timestamp,
            "session_date": self.session_date,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "amount": self.amount,
            "is_complete": self.is_complete,
            "is_partial": self.is_partial,
            "source": self.source,
            "source_timestamp": self.source_timestamp,
            "available_at": self.available_at,
            "point_in_time_verified": self.point_in_time_verified,
            "qualification": self.qualification,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TimeframeBar":
        return cls(
            symbol=d["symbol"],
            timeframe=d["timeframe"],
            timestamp=d["timestamp"],
            session_date=d["session_date"],
            open=float(d["open"]),
            high=float(d["high"]),
            low=float(d["low"]),
            close=float(d["close"]),
            volume=float(d["volume"]),
            amount=float(d.get("amount", 0.0)),
            is_complete=bool(d["is_complete"]),
            is_partial=bool(d["is_partial"]),
            source=d["source"],
            source_timestamp=d.get("source_timestamp"),
            available_at=d.get("available_at"),
            point_in_time_verified=bool(d.get("point_in_time_verified", False)),
            qualification=d.get("qualification", "UNVERIFIED"),
        )


# ---------------------------------------------------------------------------
# TimeframeSnapshot
# ---------------------------------------------------------------------------

@dataclass
class TimeframeSnapshot:
    """Snapshot of a single timeframe at a specific replay timestamp."""
    snapshot_id: str
    session_id: str
    symbol: str
    replay_timestamp: str
    timeframe: str
    current_bar: Optional[Dict[str, Any]]           = None
    latest_completed_bar: Optional[Dict[str, Any]]  = None
    indicators: Dict[str, Any]                      = field(default_factory=dict)
    support_resistance: Dict[str, Any]              = field(default_factory=dict)
    trend_state: str                                = "UNKNOWN"
    volume_state: str                               = "UNKNOWN"
    strategy_snapshot_id: Optional[str]             = None
    warnings: List[str]                             = field(default_factory=list)
    point_in_time_verified: bool                    = False
    qualification: str                              = "UNVERIFIED"
    generated_at: str                               = field(default_factory=_now_utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "session_id": self.session_id,
            "symbol": self.symbol,
            "replay_timestamp": self.replay_timestamp,
            "timeframe": self.timeframe,
            "current_bar": self.current_bar,
            "latest_completed_bar": self.latest_completed_bar,
            "indicators": self.indicators,
            "support_resistance": self.support_resistance,
            "trend_state": self.trend_state,
            "volume_state": self.volume_state,
            "strategy_snapshot_id": self.strategy_snapshot_id,
            "warnings": self.warnings,
            "point_in_time_verified": self.point_in_time_verified,
            "qualification": self.qualification,
            "generated_at": self.generated_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TimeframeSnapshot":
        return cls(
            snapshot_id=d["snapshot_id"],
            session_id=d["session_id"],
            symbol=d["symbol"],
            replay_timestamp=d["replay_timestamp"],
            timeframe=d["timeframe"],
            current_bar=d.get("current_bar"),
            latest_completed_bar=d.get("latest_completed_bar"),
            indicators=d.get("indicators", {}),
            support_resistance=d.get("support_resistance", {}),
            trend_state=d.get("trend_state", "UNKNOWN"),
            volume_state=d.get("volume_state", "UNKNOWN"),
            strategy_snapshot_id=d.get("strategy_snapshot_id"),
            warnings=d.get("warnings", []),
            point_in_time_verified=bool(d.get("point_in_time_verified", False)),
            qualification=d.get("qualification", "UNVERIFIED"),
            generated_at=d.get("generated_at", _now_utc()),
        )


# ---------------------------------------------------------------------------
# MultiTimeframeSnapshot
# ---------------------------------------------------------------------------

@dataclass
class MultiTimeframeSnapshot:
    """Snapshot across all timeframes at a specific replay timestamp."""
    multi_snapshot_id: str
    session_id: str
    symbol: str
    replay_timestamp: str
    snapshots: Dict[str, Any]                       = field(default_factory=dict)
    available_timeframes: List[str]                 = field(default_factory=list)
    unavailable_timeframes: List[str]               = field(default_factory=list)
    partial_timeframes: List[str]                   = field(default_factory=list)
    alignment_status: str                           = "UNKNOWN"
    agreement_score: float                          = 0.0
    conflict_score: float                           = 0.0
    dominant_timeframe: Optional[str]               = None
    trigger_timeframe: Optional[str]                = None
    warnings: List[str]                             = field(default_factory=list)
    point_in_time_verified: bool                    = False
    generated_at: str                               = field(default_factory=_now_utc)
    research_only: bool                             = True
    no_real_orders: bool                            = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "multi_snapshot_id": self.multi_snapshot_id,
            "session_id": self.session_id,
            "symbol": self.symbol,
            "replay_timestamp": self.replay_timestamp,
            "snapshots": self.snapshots,
            "available_timeframes": self.available_timeframes,
            "unavailable_timeframes": self.unavailable_timeframes,
            "partial_timeframes": self.partial_timeframes,
            "alignment_status": self.alignment_status,
            "agreement_score": self.agreement_score,
            "conflict_score": self.conflict_score,
            "dominant_timeframe": self.dominant_timeframe,
            "trigger_timeframe": self.trigger_timeframe,
            "warnings": self.warnings,
            "point_in_time_verified": self.point_in_time_verified,
            "generated_at": self.generated_at,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "MultiTimeframeSnapshot":
        return cls(
            multi_snapshot_id=d["multi_snapshot_id"],
            session_id=d["session_id"],
            symbol=d["symbol"],
            replay_timestamp=d["replay_timestamp"],
            snapshots=d.get("snapshots", {}),
            available_timeframes=d.get("available_timeframes", []),
            unavailable_timeframes=d.get("unavailable_timeframes", []),
            partial_timeframes=d.get("partial_timeframes", []),
            alignment_status=d.get("alignment_status", "UNKNOWN"),
            agreement_score=float(d.get("agreement_score", 0.0)),
            conflict_score=float(d.get("conflict_score", 0.0)),
            dominant_timeframe=d.get("dominant_timeframe"),
            trigger_timeframe=d.get("trigger_timeframe"),
            warnings=d.get("warnings", []),
            point_in_time_verified=bool(d.get("point_in_time_verified", False)),
            generated_at=d.get("generated_at", _now_utc()),
            research_only=bool(d.get("research_only", True)),
            no_real_orders=bool(d.get("no_real_orders", True)),
        )


# ---------------------------------------------------------------------------
# TimeframeAlignmentResult
# ---------------------------------------------------------------------------

@dataclass
class TimeframeAlignmentResult:
    """Result of alignment check for a single timeframe at a replay timestamp."""
    alignment_id: str
    session_id: str
    timeframe: str
    replay_timestamp: str
    status: str                         # AlignmentStatus value
    aligned_bar_timestamp: Optional[str] = None
    bar_age_minutes: Optional[float]     = None
    is_stale: bool                       = False
    stale_threshold_minutes: int         = 90
    warnings: List[str]                  = field(default_factory=list)
    point_in_time_verified: bool         = False
    generated_at: str                    = field(default_factory=_now_utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alignment_id": self.alignment_id,
            "session_id": self.session_id,
            "timeframe": self.timeframe,
            "replay_timestamp": self.replay_timestamp,
            "status": self.status,
            "aligned_bar_timestamp": self.aligned_bar_timestamp,
            "bar_age_minutes": self.bar_age_minutes,
            "is_stale": self.is_stale,
            "stale_threshold_minutes": self.stale_threshold_minutes,
            "warnings": self.warnings,
            "point_in_time_verified": self.point_in_time_verified,
            "generated_at": self.generated_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TimeframeAlignmentResult":
        return cls(
            alignment_id=d["alignment_id"],
            session_id=d["session_id"],
            timeframe=d["timeframe"],
            replay_timestamp=d["replay_timestamp"],
            status=d["status"],
            aligned_bar_timestamp=d.get("aligned_bar_timestamp"),
            bar_age_minutes=d.get("bar_age_minutes"),
            is_stale=bool(d.get("is_stale", False)),
            stale_threshold_minutes=int(d.get("stale_threshold_minutes", 90)),
            warnings=d.get("warnings", []),
            point_in_time_verified=bool(d.get("point_in_time_verified", False)),
            generated_at=d.get("generated_at", _now_utc()),
        )


# ---------------------------------------------------------------------------
# TimeframeAgreementResult
# ---------------------------------------------------------------------------

@dataclass
class TimeframeAgreementResult:
    """Result of cross-timeframe agreement analysis."""
    agreement_id: str
    session_id: str
    replay_timestamp: str
    status: str                             # AgreementStatus value
    agreement_score: float                  = 0.0
    conflict_score: float                   = 0.0
    bullish_timeframes: List[str]           = field(default_factory=list)
    bearish_timeframes: List[str]           = field(default_factory=list)
    neutral_timeframes: List[str]           = field(default_factory=list)
    unavailable_timeframes: List[str]       = field(default_factory=list)
    dominant_timeframe: Optional[str]       = None
    trigger_timeframe: Optional[str]        = None
    explanation: str                        = ""
    warnings: List[str]                     = field(default_factory=list)
    point_in_time_verified: bool            = False
    research_only: bool                     = True
    no_auto_trade: bool                     = True
    generated_at: str                       = field(default_factory=_now_utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agreement_id": self.agreement_id,
            "session_id": self.session_id,
            "replay_timestamp": self.replay_timestamp,
            "status": self.status,
            "agreement_score": self.agreement_score,
            "conflict_score": self.conflict_score,
            "bullish_timeframes": self.bullish_timeframes,
            "bearish_timeframes": self.bearish_timeframes,
            "neutral_timeframes": self.neutral_timeframes,
            "unavailable_timeframes": self.unavailable_timeframes,
            "dominant_timeframe": self.dominant_timeframe,
            "trigger_timeframe": self.trigger_timeframe,
            "explanation": self.explanation,
            "warnings": self.warnings,
            "point_in_time_verified": self.point_in_time_verified,
            "research_only": self.research_only,
            "no_auto_trade": self.no_auto_trade,
            "generated_at": self.generated_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TimeframeAgreementResult":
        return cls(
            agreement_id=d["agreement_id"],
            session_id=d["session_id"],
            replay_timestamp=d["replay_timestamp"],
            status=d["status"],
            agreement_score=float(d.get("agreement_score", 0.0)),
            conflict_score=float(d.get("conflict_score", 0.0)),
            bullish_timeframes=d.get("bullish_timeframes", []),
            bearish_timeframes=d.get("bearish_timeframes", []),
            neutral_timeframes=d.get("neutral_timeframes", []),
            unavailable_timeframes=d.get("unavailable_timeframes", []),
            dominant_timeframe=d.get("dominant_timeframe"),
            trigger_timeframe=d.get("trigger_timeframe"),
            explanation=d.get("explanation", ""),
            warnings=d.get("warnings", []),
            point_in_time_verified=bool(d.get("point_in_time_verified", False)),
            research_only=bool(d.get("research_only", True)),
            no_auto_trade=bool(d.get("no_auto_trade", True)),
            generated_at=d.get("generated_at", _now_utc()),
        )
