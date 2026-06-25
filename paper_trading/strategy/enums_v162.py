"""
paper_trading/strategy/enums_v162.py — Enumerations for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

from enum import Enum


class StrategyStatus(Enum):
    """Lifecycle status of a registered paper strategy."""
    REGISTERED   = "REGISTERED"
    INITIALIZING = "INITIALIZING"
    READY        = "READY"
    RUNNING      = "RUNNING"
    PAUSED       = "PAUSED"
    HALTED       = "HALTED"
    COMPLETED    = "COMPLETED"
    FAILED       = "FAILED"
    RETIRED      = "RETIRED"


class SignalType(Enum):
    """
    Permitted signal types. SHORT/MARGIN permanently excluded.
    [!] ENTRY_SHORT and SELL_SHORT are intentionally absent — not supported.
    """
    ENTRY_LONG      = "ENTRY_LONG"
    EXIT_LONG       = "EXIT_LONG"
    HOLD            = "HOLD"
    REDUCE_RESEARCH = "REDUCE_RESEARCH"
    BLOCK           = "BLOCK"
    ALERT           = "ALERT"


class SignalStrength(Enum):
    """Normalized signal strength levels."""
    STRONG    = "STRONG"
    MODERATE  = "MODERATE"
    WEAK      = "WEAK"
    NEUTRAL   = "NEUTRAL"


class DecisionOutcome(Enum):
    """Final outcome of the 19-step decision pipeline."""
    APPROVED        = "APPROVED"
    REJECTED        = "REJECTED"
    BLOCKED         = "BLOCKED"
    DEFERRED        = "DEFERRED"
    COOLDOWN        = "COOLDOWN"
    RATE_LIMITED    = "RATE_LIMITED"
    DUPLICATE       = "DUPLICATE"
    CONFLICT        = "CONFLICT"
    INELIGIBLE      = "INELIGIBLE"
    DATA_STALE      = "DATA_STALE"
    RISK_BLOCKED    = "RISK_BLOCKED"
    SIZING_ZERO     = "SIZING_ZERO"
    PIPELINE_ERROR  = "PIPELINE_ERROR"


class ApprovalMode(Enum):
    """Approval policy for paper order proposals."""
    MANUAL_REQUIRED = "MANUAL_REQUIRED"   # default — explicit approval needed
    AUTO_PAPER_ONLY = "AUTO_PAPER_ONLY"   # auto approve only when all safety conditions met


class ConflictPolicy(Enum):
    """Conflict resolution policy when multiple signals compete."""
    MOST_CONSERVATIVE = "MOST_CONSERVATIVE"   # default
    FIRST_WINS        = "FIRST_WINS"
    HIGHEST_STRENGTH  = "HIGHEST_STRENGTH"
    LATEST_WINS       = "LATEST_WINS"
    BLOCK_ALL         = "BLOCK_ALL"


class TriggerType(Enum):
    """Types of strategy trigger sources."""
    TIMER        = "TIMER"
    MARKET_EVENT = "MARKET_EVENT"
    PRICE_ALERT  = "PRICE_ALERT"
    MANUAL       = "MANUAL"
    REPLAY       = "REPLAY"
    CHECKPOINT   = "CHECKPOINT"


class ProposalStatus(Enum):
    """Status of a paper order proposal."""
    PENDING    = "PENDING"
    SUBMITTED  = "SUBMITTED"
    ACCEPTED   = "ACCEPTED"
    REJECTED   = "REJECTED"
    CANCELLED  = "CANCELLED"
    EXPIRED    = "EXPIRED"


class JournalEventType(Enum):
    """Types of events recorded in the strategy journal."""
    STRATEGY_REGISTERED   = "STRATEGY_REGISTERED"
    STRATEGY_STARTED      = "STRATEGY_STARTED"
    STRATEGY_PAUSED       = "STRATEGY_PAUSED"
    STRATEGY_HALTED       = "STRATEGY_HALTED"
    STRATEGY_COMPLETED    = "STRATEGY_COMPLETED"
    SIGNAL_RECEIVED       = "SIGNAL_RECEIVED"
    SIGNAL_NORMALIZED     = "SIGNAL_NORMALIZED"
    SIGNAL_DEDUPLICATED   = "SIGNAL_DEDUPLICATED"
    DECISION_STARTED      = "DECISION_STARTED"
    DECISION_COMPLETED    = "DECISION_COMPLETED"
    PROPOSAL_CREATED      = "PROPOSAL_CREATED"
    PROPOSAL_SUBMITTED    = "PROPOSAL_SUBMITTED"
    PROPOSAL_REJECTED     = "PROPOSAL_REJECTED"
    COOLDOWN_APPLIED      = "COOLDOWN_APPLIED"
    RATE_LIMIT_APPLIED    = "RATE_LIMIT_APPLIED"
    CONFLICT_RESOLVED     = "CONFLICT_RESOLVED"
    APPROVAL_GRANTED      = "APPROVAL_GRANTED"
    APPROVAL_DENIED       = "APPROVAL_DENIED"
    CHECKPOINT_SAVED      = "CHECKPOINT_SAVED"
    RECOVERY_ATTEMPTED    = "RECOVERY_ATTEMPTED"
    LINEAGE_RECORDED      = "LINEAGE_RECORDED"


class CheckpointReason(Enum):
    """Why a checkpoint was saved."""
    PERIODIC    = "PERIODIC"
    PRE_HALT    = "PRE_HALT"
    PRE_PAUSE   = "PRE_PAUSE"
    MANUAL      = "MANUAL"
    SIGNAL_GATE = "SIGNAL_GATE"


class RecoveryMode(Enum):
    """How a strategy recovers from a checkpoint."""
    FULL_REPLAY     = "FULL_REPLAY"
    STATE_RESTORE   = "STATE_RESTORE"
    COLD_START      = "COLD_START"


class EligibilityResult(Enum):
    """Result from the eligibility adapter."""
    ELIGIBLE   = "ELIGIBLE"
    INELIGIBLE = "INELIGIBLE"
    UNCERTAIN  = "UNCERTAIN"
