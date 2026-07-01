"""
paper_trading/multi_session/enums_v166.py — Multi-session Coordination enums v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from enum import Enum

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True


class SessionType(Enum):
    PAPER = "PAPER"
    REPLAY = "REPLAY"
    SIMULATION = "SIMULATION"
    TRAINING = "TRAINING"
    REVIEW = "REVIEW"


# Forbidden session types (never instantiated)
FORBIDDEN_SESSION_TYPES = {"LIVE", "REAL", "BROKER", "PRODUCTION_TRADING"}


class SessionLifecycleState(Enum):
    CREATED = "CREATED"
    REGISTERED = "REGISTERED"
    READY = "READY"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    DEGRADED = "DEGRADED"
    CONTAINED = "CONTAINED"
    RECOVERING = "RECOVERING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"


# Legal lifecycle transitions
VALID_LIFECYCLE_TRANSITIONS: dict[SessionLifecycleState, set[SessionLifecycleState]] = {
    SessionLifecycleState.CREATED:     {SessionLifecycleState.REGISTERED, SessionLifecycleState.CANCELLED},
    SessionLifecycleState.REGISTERED:  {SessionLifecycleState.READY, SessionLifecycleState.BLOCKED, SessionLifecycleState.CANCELLED},
    SessionLifecycleState.READY:       {SessionLifecycleState.SCHEDULED, SessionLifecycleState.BLOCKED, SessionLifecycleState.CANCELLED},
    SessionLifecycleState.SCHEDULED:   {SessionLifecycleState.RUNNING, SessionLifecycleState.BLOCKED, SessionLifecycleState.PAUSED, SessionLifecycleState.CANCELLED},
    SessionLifecycleState.RUNNING:     {SessionLifecycleState.PAUSED, SessionLifecycleState.DEGRADED, SessionLifecycleState.CONTAINED, SessionLifecycleState.RECOVERING, SessionLifecycleState.COMPLETED, SessionLifecycleState.FAILED, SessionLifecycleState.BLOCKED},
    SessionLifecycleState.PAUSED:      {SessionLifecycleState.READY, SessionLifecycleState.BLOCKED, SessionLifecycleState.CANCELLED, SessionLifecycleState.FAILED},
    SessionLifecycleState.DEGRADED:    {SessionLifecycleState.RECOVERING, SessionLifecycleState.CONTAINED, SessionLifecycleState.FAILED, SessionLifecycleState.BLOCKED},
    SessionLifecycleState.CONTAINED:   {SessionLifecycleState.RECOVERING, SessionLifecycleState.FAILED, SessionLifecycleState.BLOCKED},
    SessionLifecycleState.RECOVERING:  {SessionLifecycleState.READY, SessionLifecycleState.FAILED, SessionLifecycleState.BLOCKED},
    SessionLifecycleState.COMPLETED:   set(),
    SessionLifecycleState.FAILED:      set(),
    SessionLifecycleState.BLOCKED:     {SessionLifecycleState.READY, SessionLifecycleState.CANCELLED},
    SessionLifecycleState.CANCELLED:   set(),
}

# Transitions that require explicit verification before RUNNING
REQUIRES_VERIFICATION_BEFORE_RUNNING = {
    SessionLifecycleState.DEGRADED,
    SessionLifecycleState.RECOVERING,
    SessionLifecycleState.PAUSED,
    SessionLifecycleState.BLOCKED,
}


class CoordinationDomain(Enum):
    RESOURCE = "RESOURCE"
    SYMBOL = "SYMBOL"
    STRATEGY = "STRATEGY"
    CAPITAL = "CAPITAL"
    RISK = "RISK"
    MARKET_DATA = "MARKET_DATA"
    EVENT_ORDERING = "EVENT_ORDERING"
    LIFECYCLE = "LIFECYCLE"
    CHECKPOINT = "CHECKPOINT"
    RECOVERY = "RECOVERY"
    REPORTING = "REPORTING"


class ConflictType(Enum):
    RESOURCE_EXHAUSTION = "RESOURCE_EXHAUSTION"
    RESOURCE_DOUBLE_BOOKING = "RESOURCE_DOUBLE_BOOKING"
    SYMBOL_OVERLAP = "SYMBOL_OVERLAP"
    STRATEGY_CONFLICT = "STRATEGY_CONFLICT"
    CAPITAL_OVERALLOCATION = "CAPITAL_OVERALLOCATION"
    RISK_BUDGET_EXCEEDED = "RISK_BUDGET_EXCEEDED"
    EVENT_ORDER_VIOLATION = "EVENT_ORDER_VIOLATION"
    CHECKPOINT_CONFLICT = "CHECKPOINT_CONFLICT"
    SESSION_STATE_CONFLICT = "SESSION_STATE_CONFLICT"
    PRIORITY_INVERSION = "PRIORITY_INVERSION"
    STARVATION = "STARVATION"
    DEADLOCK = "DEADLOCK"
    STALE_HEARTBEAT = "STALE_HEARTBEAT"
    LEASE_EXPIRED = "LEASE_EXPIRED"
    RECOVERY_COLLISION = "RECOVERY_COLLISION"
    FAILURE_PROPAGATION = "FAILURE_PROPAGATION"


class ConflictSeverity(Enum):
    INFO = "INFO"
    WARN = "WARN"
    BLOCK = "BLOCK"
    CRITICAL = "CRITICAL"


class ResourceType(Enum):
    CPU_SLOT = "CPU_SLOT"
    MEMORY_BUDGET = "MEMORY_BUDGET"
    MARKET_DATA_CHANNEL = "MARKET_DATA_CHANNEL"
    SYMBOL_LOCK = "SYMBOL_LOCK"
    STRATEGY_SLOT = "STRATEGY_SLOT"
    EVENT_STREAM = "EVENT_STREAM"
    CHECKPOINT_SLOT = "CHECKPOINT_SLOT"
    REPORT_SLOT = "REPORT_SLOT"
    CAPITAL_BUDGET = "CAPITAL_BUDGET"
    RISK_BUDGET = "RISK_BUDGET"


class ReservationStatus(Enum):
    PENDING = "PENDING"
    GRANTED = "GRANTED"
    PARTIAL = "PARTIAL"
    DENIED = "DENIED"
    EXPIRED = "EXPIRED"
    RELEASED = "RELEASED"
    ROLLED_BACK = "ROLLED_BACK"


class SessionPriority(Enum):
    CRITICAL_RESEARCH = 100
    HIGH = 75
    NORMAL = 50
    LOW = 25
    BACKGROUND_REVIEW = 10


class DecisionType(Enum):
    ADMIT = "ADMIT"
    BLOCK = "BLOCK"
    PAUSE = "PAUSE"
    DEGRADE = "DEGRADE"
    CONTAIN = "CONTAIN"
    RESUME_ELIGIBLE = "RESUME_ELIGIBLE"
    RESUME_BLOCKED = "RESUME_BLOCKED"
    REQUIRE_REVIEW = "REQUIRE_REVIEW"
    WARN = "WARN"
    ALLOW = "ALLOW"


class CoordinationOutcome(Enum):
    PASS = "PASS"
    WARN = "WARN"
    BLOCK = "BLOCK"
    DEGRADE = "DEGRADE"
    REQUIRE_REVIEW = "REQUIRE_REVIEW"


class LockType(Enum):
    SHARED = "SHARED"
    EXCLUSIVE = "EXCLUSIVE"


class LockStatus(Enum):
    HELD = "HELD"
    RELEASED = "RELEASED"
    EXPIRED = "EXPIRED"
    WAITING = "WAITING"


class ElectionStatus(Enum):
    PENDING = "PENDING"
    ELECTED = "ELECTED"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"


class BarrierType(Enum):
    ALL_OF = "ALL_OF"
    QUORUM = "QUORUM"


class BarrierStatus(Enum):
    WAITING = "WAITING"
    RELEASED = "RELEASED"
    ABORTED = "ABORTED"
    TIMEOUT = "TIMEOUT"
