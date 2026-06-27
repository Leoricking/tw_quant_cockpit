"""
paper_trading/failure_validation/enums_v165.py — Failure Injection & Recovery enumerations v1.6.5.
[!] Research Only. No Real Orders. No Real Failure Injection. Not Investment Advice.
[!] REAL_FAILURE_INJECTION_ENABLED = False. PRODUCTION_CHAOS_ENABLED = False.
[!] Simulation/fixture only. No broker. No real account. No real network.
"""
from __future__ import annotations

from enum import Enum, auto

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
REAL_FAILURE_INJECTION_ENABLED = False
PRODUCTION_CHAOS_ENABLED = False
PAPER_ONLY = True
RESEARCH_ONLY = True


class FailureDomain(str, Enum):
    """Domains in which controlled failure injection is permitted (paper/simulation only)."""
    MARKET_DATA         = "MARKET_DATA"
    SESSION_STATE       = "SESSION_STATE"
    STRATEGY_SIGNAL     = "STRATEGY_SIGNAL"
    PAPER_ORDER         = "PAPER_ORDER"
    PAPER_FILL          = "PAPER_FILL"
    EVENT_STREAM        = "EVENT_STREAM"
    CHECKPOINT          = "CHECKPOINT"
    STORE               = "STORE"
    QUERY               = "QUERY"
    ALERT               = "ALERT"
    INCIDENT            = "INCIDENT"
    RECOVERY            = "RECOVERY"
    ANALYTICS           = "ANALYTICS"
    REPORT              = "REPORT"
    DEPENDENCY          = "DEPENDENCY"
    TIME                = "TIME"
    CONFIGURATION       = "CONFIGURATION"

    # Forbidden domains — these must NEVER be injected
    # BROKER             = "BROKER"           # FORBIDDEN
    # REAL_ACCOUNT       = "REAL_ACCOUNT"     # FORBIDDEN
    # REAL_ORDER         = "REAL_ORDER"       # FORBIDDEN
    # PRODUCTION_SERVICE = "PRODUCTION_SERVICE" # FORBIDDEN
    # OPERATING_SYSTEM   = "OPERATING_SYSTEM" # FORBIDDEN
    # FIREWALL           = "FIREWALL"         # FORBIDDEN
    # REAL_NETWORK       = "REAL_NETWORK"     # FORBIDDEN


FORBIDDEN_DOMAINS = frozenset({
    "BROKER", "REAL_ACCOUNT", "REAL_ORDER",
    "PRODUCTION_SERVICE", "OPERATING_SYSTEM", "FIREWALL", "REAL_NETWORK",
})

PERMITTED_DOMAINS = frozenset(d.value for d in FailureDomain)


class FailureType(str, Enum):
    """Types of failure that can be injected in controlled simulation."""
    TIMEOUT                     = "TIMEOUT"
    DELAY                       = "DELAY"
    STALE_DATA                  = "STALE_DATA"
    MISSING_DATA                = "MISSING_DATA"
    DUPLICATE_EVENT             = "DUPLICATE_EVENT"
    OUT_OF_ORDER_EVENT          = "OUT_OF_ORDER_EVENT"
    INVALID_PAYLOAD             = "INVALID_PAYLOAD"
    PARTIAL_WRITE               = "PARTIAL_WRITE"
    READ_FAILURE                = "READ_FAILURE"
    WRITE_FAILURE               = "WRITE_FAILURE"
    CHECKPOINT_CORRUPTION       = "CHECKPOINT_CORRUPTION"
    SNAPSHOT_MISMATCH           = "SNAPSHOT_MISMATCH"
    HASH_MISMATCH               = "HASH_MISMATCH"
    REPLAY_MISMATCH             = "REPLAY_MISMATCH"
    STATE_DIVERGENCE            = "STATE_DIVERGENCE"
    EVENT_LOSS                  = "EVENT_LOSS"
    EVENT_STORM                 = "EVENT_STORM"
    ALERT_LOSS                  = "ALERT_LOSS"
    ALERT_DUPLICATION           = "ALERT_DUPLICATION"
    INCIDENT_CREATION_FAILURE   = "INCIDENT_CREATION_FAILURE"
    RECOVERY_FAILURE            = "RECOVERY_FAILURE"
    ROLLBACK_FAILURE            = "ROLLBACK_FAILURE"
    RETRY_EXHAUSTION            = "RETRY_EXHAUSTION"
    CIRCUIT_OPEN                = "CIRCUIT_OPEN"
    DEPENDENCY_UNAVAILABLE      = "DEPENDENCY_UNAVAILABLE"
    DEGRADED_MODE               = "DEGRADED_MODE"
    CONFIG_DRIFT                = "CONFIG_DRIFT"
    CLOCK_SKEW                  = "CLOCK_SKEW"


class FailureSeverity(str, Enum):
    """Severity levels for failure scenarios."""
    INFO        = "INFO"
    LOW         = "LOW"
    MEDIUM      = "MEDIUM"
    HIGH        = "HIGH"
    CRITICAL    = "CRITICAL"


class ExpectedOutcome(str, Enum):
    """Expected outcome after a controlled failure injection."""
    DETECTED        = "DETECTED"
    ALERTED         = "ALERTED"
    CONTAINED       = "CONTAINED"
    DEGRADED        = "DEGRADED"
    HALTED          = "HALTED"
    RECOVERED       = "RECOVERED"
    ROLLED_BACK     = "ROLLED_BACK"
    BLOCKED         = "BLOCKED"
    NO_EFFECT       = "NO_EFFECT"


class RecoveryState(str, Enum):
    """States in the recovery state machine."""
    HEALTHY     = "HEALTHY"
    DEGRADED    = "DEGRADED"
    CONTAINED   = "CONTAINED"
    RECOVERING  = "RECOVERING"
    RECOVERED   = "RECOVERED"
    ROLLED_BACK = "ROLLED_BACK"
    FAILED      = "FAILED"
    BLOCKED     = "BLOCKED"


# Invalid recovery state transitions — these must be detected and rejected
INVALID_RECOVERY_TRANSITIONS = frozenset({
    (RecoveryState.FAILED, RecoveryState.HEALTHY),
    (RecoveryState.BLOCKED, RecoveryState.RECOVERED),
})

# Transitions that require explicit verification before completion
VERIFICATION_REQUIRED_TRANSITIONS = frozenset({
    (RecoveryState.RECOVERING, RecoveryState.RECOVERED),
})

# Auto-resume from DEGRADED to RUNNING is blocked
AUTO_RESUME_RUNNING_ENABLED = False


class CircuitBreakerState(str, Enum):
    """Circuit breaker states."""
    CLOSED      = "CLOSED"
    OPEN        = "OPEN"
    HALF_OPEN   = "HALF_OPEN"


class InjectionStatus(str, Enum):
    """Status of a failure injection operation."""
    PENDING             = "PENDING"
    BLOCKED_BY_SAFETY   = "BLOCKED_BY_SAFETY"
    INJECTED            = "INJECTED"
    DETECTED            = "DETECTED"
    CONTAINED           = "CONTAINED"
    REVERTED            = "REVERTED"
    EXPIRED             = "EXPIRED"
    ERROR               = "ERROR"


class ValidationPhase(str, Enum):
    """Phases of the failure injection validation chain."""
    BASELINE_SNAPSHOT           = "BASELINE_SNAPSHOT"
    SCENARIO_DEFINITION         = "SCENARIO_DEFINITION"
    SAFETY_PRECHECK             = "SAFETY_PRECHECK"
    CONTROLLED_INJECTION        = "CONTROLLED_INJECTION"
    DETECTION                   = "DETECTION"
    ALERT                       = "ALERT"
    INCIDENT                    = "INCIDENT"
    CONTAINMENT                 = "CONTAINMENT"
    RECOVERY_PLAN               = "RECOVERY_PLAN"
    RECOVERY_EXECUTION          = "RECOVERY_EXECUTION"
    STATE_VERIFICATION          = "STATE_VERIFICATION"
    DATA_RECONCILIATION         = "DATA_RECONCILIATION"
    POST_RECOVERY_VALIDATION    = "POST_RECOVERY_VALIDATION"
    REPLAY                      = "REPLAY"
    REPORT                      = "REPORT"


class ScorecardDimension(str, Enum):
    """Scorecard dimensions for failure/recovery evaluation."""
    DETECTION           = "DETECTION"
    ALERTING            = "ALERTING"
    CONTAINMENT         = "CONTAINMENT"
    RECOVERY            = "RECOVERY"
    DATA_INTEGRITY      = "DATA_INTEGRITY"
    STATE_INTEGRITY     = "STATE_INTEGRITY"
    REPLAY_INTEGRITY    = "REPLAY_INTEGRITY"
    IDEMPOTENCY         = "IDEMPOTENCY"
    RTO                 = "RTO"
    RPO                 = "RPO"


SCORECARD_WEIGHTS: dict[str, int] = {
    ScorecardDimension.DETECTION.value:         15,
    ScorecardDimension.ALERTING.value:          10,
    ScorecardDimension.CONTAINMENT.value:       15,
    ScorecardDimension.RECOVERY.value:          20,
    ScorecardDimension.DATA_INTEGRITY.value:    15,
    ScorecardDimension.STATE_INTEGRITY.value:   10,
    ScorecardDimension.REPLAY_INTEGRITY.value:   5,
    ScorecardDimension.IDEMPOTENCY.value:        5,
    ScorecardDimension.RTO.value:                3,
    ScorecardDimension.RPO.value:                2,
}

assert sum(SCORECARD_WEIGHTS.values()) == 100, "Scorecard weights must sum to 100"
