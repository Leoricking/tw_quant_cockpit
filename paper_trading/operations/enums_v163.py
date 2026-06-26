"""
Session Operations & Observability Enums v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from enum import Enum


class ManagedSessionType(str, Enum):
    MARKET_DATA    = "MARKET_DATA"
    PAPER_TRADING  = "PAPER_TRADING"
    PAPER_STRATEGY = "PAPER_STRATEGY"
    COMPOSITE      = "COMPOSITE"


class OperationalStatus(str, Enum):
    UNINITIALIZED = "UNINITIALIZED"
    STARTING      = "STARTING"
    RUNNING       = "RUNNING"
    DEGRADED      = "DEGRADED"
    PAUSING       = "PAUSING"
    PAUSED        = "PAUSED"
    HALTING       = "HALTING"
    HALTED        = "HALTED"
    RECOVERING    = "RECOVERING"
    RECOVERED     = "RECOVERED"
    COMPLETING    = "COMPLETING"
    COMPLETED     = "COMPLETED"
    FAILED        = "FAILED"
    BLOCKED       = "BLOCKED"


class HealthStatus(str, Enum):
    UNKNOWN   = "UNKNOWN"
    HEALTHY   = "HEALTHY"
    WARNING   = "WARNING"
    DEGRADED  = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    CRITICAL  = "CRITICAL"
    BLOCKED   = "BLOCKED"

    @classmethod
    def severity_rank(cls, status: "HealthStatus") -> int:
        return {
            cls.BLOCKED:   6,
            cls.CRITICAL:  5,
            cls.UNHEALTHY: 4,
            cls.DEGRADED:  3,
            cls.WARNING:   2,
            cls.HEALTHY:   1,
            cls.UNKNOWN:   0,
        }.get(status, 0)

    @classmethod
    def worst(cls, statuses: list) -> "HealthStatus":
        if not statuses:
            return cls.UNKNOWN
        return max(statuses, key=lambda s: cls.severity_rank(s))


class AlertSeverity(str, Enum):
    INFO     = "INFO"
    WARNING  = "WARNING"
    ERROR    = "ERROR"
    CRITICAL = "CRITICAL"


class AlertStatus(str, Enum):
    OPEN         = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    SUPPRESSED   = "SUPPRESSED"
    RESOLVED     = "RESOLVED"
    EXPIRED      = "EXPIRED"


class IncidentStatus(str, Enum):
    OPEN          = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    MITIGATED     = "MITIGATED"
    RESOLVED      = "RESOLVED"
    CLOSED        = "CLOSED"


VALID_INCIDENT_TRANSITIONS = {
    IncidentStatus.OPEN:          {IncidentStatus.INVESTIGATING},
    IncidentStatus.INVESTIGATING: {IncidentStatus.MITIGATED, IncidentStatus.RESOLVED},
    IncidentStatus.MITIGATED:     {IncidentStatus.RESOLVED},
    IncidentStatus.RESOLVED:      {IncidentStatus.CLOSED},
    IncidentStatus.CLOSED:        set(),
}


class IncidentCategory(str, Enum):
    DATA_FRESHNESS       = "DATA_FRESHNESS"
    DATA_QUALITY         = "DATA_QUALITY"
    SEQUENCE_GAP         = "SEQUENCE_GAP"
    FEED_DISCONNECT      = "FEED_DISCONNECT"
    SESSION_STATE        = "SESSION_STATE"
    STRATEGY_FAILURE     = "STRATEGY_FAILURE"
    RISK_BLOCK           = "RISK_BLOCK"
    RATE_LIMIT           = "RATE_LIMIT"
    CHECKPOINT_FAILURE   = "CHECKPOINT_FAILURE"
    RECOVERY_FAILURE     = "RECOVERY_FAILURE"
    REPLAY_MISMATCH      = "REPLAY_MISMATCH"
    LINEAGE_FAILURE      = "LINEAGE_FAILURE"
    STORAGE_FAILURE      = "STORAGE_FAILURE"
    CLI_FAILURE          = "CLI_FAILURE"
    GUI_FAILURE          = "GUI_FAILURE"
    SAFETY_VIOLATION     = "SAFETY_VIOLATION"


class OperationType(str, Enum):
    START               = "START"
    PAUSE               = "PAUSE"
    RESUME              = "RESUME"
    HALT                = "HALT"
    COMPLETE            = "COMPLETE"
    RECOVER             = "RECOVER"
    CHECKPOINT          = "CHECKPOINT"
    SNAPSHOT            = "SNAPSHOT"
    REPLAY              = "REPLAY"
    ACKNOWLEDGE_ALERT   = "ACKNOWLEDGE_ALERT"
    RESOLVE_ALERT       = "RESOLVE_ALERT"
    OPEN_INCIDENT       = "OPEN_INCIDENT"
    MITIGATE_INCIDENT   = "MITIGATE_INCIDENT"
    CLOSE_INCIDENT      = "CLOSE_INCIDENT"


class AlertChannel(str, Enum):
    IN_APP           = "IN_APP"
    CLI              = "CLI"
    REPORT           = "REPORT"
    LOCAL_STORE      = "LOCAL_STORE"
    FIXTURE_CALLBACK = "FIXTURE_CALLBACK"


FORBIDDEN_ALERT_CHANNELS = {"EMAIL", "SMS", "SLACK", "TEAMS", "PAGERDUTY", "WEBHOOK", "BROKER_CHANNEL"}


class AggregationType(str, Enum):
    SUM   = "SUM"
    COUNT = "COUNT"
    MIN   = "MIN"
    MAX   = "MAX"
    AVG   = "AVG"
    LAST  = "LAST"
    RATE  = "RATE"
    RATIO = "RATIO"
    P50   = "P50"
    P95   = "P95"
    P99   = "P99"


class MetricType(str, Enum):
    COUNTER  = "COUNTER"
    GAUGE    = "GAUGE"
    DURATION = "DURATION"
    RATIO    = "RATIO"


class SLAStatus(str, Enum):
    PASS    = "PASS"
    WARNING = "WARNING"
    BREACHED = "BREACHED"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"


__all__ = [
    "ManagedSessionType", "OperationalStatus", "HealthStatus",
    "AlertSeverity", "AlertStatus", "IncidentStatus", "VALID_INCIDENT_TRANSITIONS",
    "IncidentCategory", "OperationType", "AlertChannel", "FORBIDDEN_ALERT_CHANNELS",
    "AggregationType", "MetricType", "SLAStatus",
]
