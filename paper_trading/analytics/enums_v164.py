"""
paper_trading/analytics/enums_v164.py — Operational Analytics Enums v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from enum import Enum


class ReviewStatus(str, Enum):
    PENDING     = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED   = "COMPLETED"
    REOPENED    = "REOPENED"
    BLOCKED     = "BLOCKED"


VALID_REVIEW_TRANSITIONS = {
    ReviewStatus.PENDING:     {ReviewStatus.IN_PROGRESS, ReviewStatus.BLOCKED},
    ReviewStatus.IN_PROGRESS: {ReviewStatus.COMPLETED, ReviewStatus.BLOCKED},
    ReviewStatus.COMPLETED:   {ReviewStatus.REOPENED},
    ReviewStatus.REOPENED:    {ReviewStatus.IN_PROGRESS, ReviewStatus.BLOCKED},
    ReviewStatus.BLOCKED:     {ReviewStatus.IN_PROGRESS},
}


class ReviewScope(str, Enum):
    MARKET_DATA       = "MARKET_DATA"
    PAPER_TRADING     = "PAPER_TRADING"
    PAPER_STRATEGY    = "PAPER_STRATEGY"
    SESSION_OPERATIONS= "SESSION_OPERATIONS"
    COMPOSITE         = "COMPOSITE"


class MetricQuality(str, Enum):
    VALID             = "VALID"
    PARTIAL           = "PARTIAL"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    INVALID           = "INVALID"
    UNKNOWN           = "UNKNOWN"


class AttributionType(str, Enum):
    MARKET    = "MARKET"
    SIGNAL    = "SIGNAL"
    STRATEGY  = "STRATEGY"
    EXECUTION = "EXECUTION"
    SLIPPAGE  = "SLIPPAGE"
    LATENCY   = "LATENCY"
    COST      = "COST"
    INCIDENT  = "INCIDENT"
    ALERT     = "ALERT"
    RECOVERY  = "RECOVERY"
    DOWNTIME  = "DOWNTIME"


class RootCauseCategory(str, Enum):
    DATA_QUALITY         = "DATA_QUALITY"
    SIGNAL_QUALITY       = "SIGNAL_QUALITY"
    STRATEGY_LOGIC       = "STRATEGY_LOGIC"
    EXECUTION_SIMULATION = "EXECUTION_SIMULATION"
    LATENCY              = "LATENCY"
    CONFIGURATION        = "CONFIGURATION"
    OPERATIONAL_PROCESS  = "OPERATIONAL_PROCESS"
    INCIDENT             = "INCIDENT"
    UNKNOWN              = "UNKNOWN"


class ActionItemStatus(str, Enum):
    OPEN        = "OPEN"
    ACCEPTED    = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED   = "COMPLETED"
    REJECTED    = "REJECTED"
    DEFERRED    = "DEFERRED"


VALID_ACTION_ITEM_TRANSITIONS = {
    ActionItemStatus.OPEN:        {ActionItemStatus.ACCEPTED, ActionItemStatus.REJECTED, ActionItemStatus.DEFERRED},
    ActionItemStatus.ACCEPTED:    {ActionItemStatus.IN_PROGRESS, ActionItemStatus.DEFERRED},
    ActionItemStatus.IN_PROGRESS: {ActionItemStatus.COMPLETED, ActionItemStatus.DEFERRED},
    ActionItemStatus.COMPLETED:   set(),
    ActionItemStatus.REJECTED:    set(),
    ActionItemStatus.DEFERRED:    {ActionItemStatus.ACCEPTED, ActionItemStatus.REJECTED},
}


class AnomalySeverity(str, Enum):
    LOW      = "LOW"
    MEDIUM   = "MEDIUM"
    HIGH     = "HIGH"
    CRITICAL = "CRITICAL"


class MistakeCategory(str, Enum):
    STALE_DATA_DECISION      = "STALE_DATA_DECISION"
    MISSING_DATA_ASSUMPTION  = "MISSING_DATA_ASSUMPTION"
    DUPLICATE_SIGNAL         = "DUPLICATE_SIGNAL"
    CONFLICTING_SIGNAL       = "CONFLICTING_SIGNAL"
    LATE_SIGNAL              = "LATE_SIGNAL"
    OVERTRADING              = "OVERTRADING"
    UNDERTRADING             = "UNDERTRADING"
    EXCESSIVE_REJECTION      = "EXCESSIVE_REJECTION"
    POOR_SIMULATED_EXECUTION = "POOR_SIMULATED_EXECUTION"
    HIGH_SLIPPAGE            = "HIGH_SLIPPAGE"
    LATENCY_SENSITIVITY      = "LATENCY_SENSITIVITY"
    IGNORED_ALERT            = "IGNORED_ALERT"
    DELAYED_ACKNOWLEDGEMENT  = "DELAYED_ACKNOWLEDGEMENT"
    PREMATURE_RESUME_ATTEMPT = "PREMATURE_RESUME_ATTEMPT"
    FAILED_RECOVERY          = "FAILED_RECOVERY"
    INCOMPLETE_LINEAGE       = "INCOMPLETE_LINEAGE"
    IRREPRODUCIBLE_RESULT    = "IRREPRODUCIBLE_RESULT"
    UNSUPPORTED_CONCLUSION   = "UNSUPPORTED_CONCLUSION"


class ReproducibilityStatus(str, Enum):
    MATCH      = "MATCH"
    MISMATCH   = "MISMATCH"
    UNKNOWN    = "UNKNOWN"
    INCOMPLETE = "INCOMPLETE"


class LessonStatus(str, Enum):
    PROPOSED  = "PROPOSED"
    ACCEPTED  = "ACCEPTED"
    REJECTED  = "REJECTED"
    ARCHIVED  = "ARCHIVED"


class ScorecardDimension(str, Enum):
    DATA_QUALITY       = "DATA_QUALITY"
    SIGNAL_QUALITY     = "SIGNAL_QUALITY"
    STRATEGY_QUALITY   = "STRATEGY_QUALITY"
    EXECUTION_QUALITY  = "EXECUTION_QUALITY"
    OPERATIONAL_QUALITY= "OPERATIONAL_QUALITY"
    RISK_DISCIPLINE    = "RISK_DISCIPLINE"
    RECOVERY_QUALITY   = "RECOVERY_QUALITY"


SCORECARD_WEIGHTS: dict = {
    ScorecardDimension.DATA_QUALITY:        15,
    ScorecardDimension.SIGNAL_QUALITY:      15,
    ScorecardDimension.STRATEGY_QUALITY:    20,
    ScorecardDimension.EXECUTION_QUALITY:   15,
    ScorecardDimension.OPERATIONAL_QUALITY: 15,
    ScorecardDimension.RISK_DISCIPLINE:     10,
    ScorecardDimension.RECOVERY_QUALITY:    10,
}

SCORECARD_WEIGHT_VERSION = "1.6.4"


__all__ = [
    "ReviewStatus", "VALID_REVIEW_TRANSITIONS",
    "ReviewScope", "MetricQuality", "AttributionType",
    "RootCauseCategory", "ActionItemStatus", "VALID_ACTION_ITEM_TRANSITIONS",
    "AnomalySeverity", "MistakeCategory",
    "ReproducibilityStatus", "LessonStatus",
    "ScorecardDimension", "SCORECARD_WEIGHTS", "SCORECARD_WEIGHT_VERSION",
]
