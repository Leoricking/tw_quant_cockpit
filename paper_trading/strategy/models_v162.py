"""
paper_trading/strategy/models_v162.py — Data models for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from paper_trading.strategy.enums_v162 import (
    ApprovalMode,
    CheckpointReason,
    ConflictPolicy,
    DecisionOutcome,
    EligibilityResult,
    JournalEventType,
    ProposalStatus,
    RecoveryMode,
    SignalStrength,
    SignalType,
    StrategyStatus,
    TriggerType,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


def _new_id() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Strategy config / metadata
# ---------------------------------------------------------------------------

@dataclass
class StrategyConfig:
    """Immutable configuration for a paper strategy instance."""
    strategy_id: str                    = field(default_factory=_new_id)
    strategy_name: str                  = "unnamed_strategy"
    strategy_version: str               = "0.0.1"
    description: str                    = ""
    author: str                         = "research"
    approval_mode: ApprovalMode         = ApprovalMode.MANUAL_REQUIRED
    conflict_policy: ConflictPolicy     = ConflictPolicy.MOST_CONSERVATIVE
    max_signals_per_minute: int         = 10
    cooldown_seconds: int               = 60
    max_open_proposals: int             = 5
    allowed_signal_types: List[str]     = field(default_factory=lambda: [
        SignalType.ENTRY_LONG.value,
        SignalType.EXIT_LONG.value,
        SignalType.HOLD.value,
        SignalType.REDUCE_RESEARCH.value,
        SignalType.BLOCK.value,
        SignalType.ALERT.value,
    ])
    tags: List[str]                     = field(default_factory=list)
    extra: Dict[str, Any]               = field(default_factory=dict)

    # Safety — all must remain True/False as shown
    paper_only: bool                    = True
    research_only: bool                 = True
    simulation_only: bool               = True
    not_a_real_order: bool              = True
    no_broker_call: bool                = True
    no_real_account: bool               = True
    no_formal_portfolio_ledger_write: bool = True

    def __post_init__(self) -> None:
        assert self.paper_only is True, "paper_only must be True"
        assert self.research_only is True, "research_only must be True"
        assert self.simulation_only is True, "simulation_only must be True"
        assert self.not_a_real_order is True, "not_a_real_order must be True"
        assert self.no_broker_call is True, "no_broker_call must be True"
        assert self.no_real_account is True, "no_real_account must be True"
        assert self.no_formal_portfolio_ledger_write is True


@dataclass
class StrategyMetadata:
    """Runtime metadata for a strategy instance."""
    strategy_id: str
    registered_at: str          = field(default_factory=_now_iso)
    started_at: Optional[str]   = None
    paused_at: Optional[str]    = None
    halted_at: Optional[str]    = None
    completed_at: Optional[str] = None
    status: StrategyStatus      = StrategyStatus.REGISTERED
    signal_count: int           = 0
    decision_count: int         = 0
    proposal_count: int         = 0
    approved_count: int         = 0
    rejected_count: int         = 0
    error_count: int            = 0
    last_signal_at: Optional[str] = None
    last_decision_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------

@dataclass
class PaperSignal:
    """A research-only trading signal from a paper strategy."""
    signal_id: str                  = field(default_factory=_new_id)
    strategy_id: str                = ""
    ticker: str                     = ""
    signal_type: str                = SignalType.HOLD.value
    strength: str                   = SignalStrength.NEUTRAL.value
    confidence: float               = 0.0          # [0.0, 1.0]
    raw_value: Optional[float]      = None
    normalized_value: Optional[float] = None
    generated_at: str               = field(default_factory=_now_iso)
    trigger_type: str               = TriggerType.MANUAL.value
    metadata: Dict[str, Any]        = field(default_factory=dict)
    is_duplicate: bool              = False
    dedup_key: str                  = ""

    # Safety labels
    paper_only: bool                = True
    research_only: bool             = True
    not_a_real_order: bool          = True

    def __post_init__(self) -> None:
        assert self.paper_only is True
        assert self.research_only is True
        assert self.not_a_real_order is True
        assert 0.0 <= self.confidence <= 1.0, f"confidence must be in [0,1]: {self.confidence}"
        allowed = {st.value for st in SignalType}
        assert self.signal_type in allowed, f"Forbidden signal_type: {self.signal_type}"


# ---------------------------------------------------------------------------
# Decision context / result
# ---------------------------------------------------------------------------

@dataclass
class DecisionContext:
    """Context passed through the 19-step decision pipeline."""
    context_id: str                     = field(default_factory=_new_id)
    signal: Optional[PaperSignal]       = None
    strategy_config: Optional[StrategyConfig] = None
    market_open: bool                   = False
    data_quality_ok: bool               = False
    pit_valid: bool                     = False
    eligibility: str                    = EligibilityResult.UNCERTAIN.value
    suggested_size: Optional[float]     = None
    correlation_breach: bool            = False
    risk_blocked: bool                  = False
    conflict_tickers: List[str]         = field(default_factory=list)
    approval_mode: str                  = ApprovalMode.MANUAL_REQUIRED.value
    pipeline_step: int                  = 0
    pipeline_log: List[str]             = field(default_factory=list)
    created_at: str                     = field(default_factory=_now_iso)
    extra: Dict[str, Any]               = field(default_factory=dict)


@dataclass
class DecisionResult:
    """Output of the 19-step decision pipeline."""
    decision_id: str                    = field(default_factory=_new_id)
    context_id: str                     = ""
    strategy_id: str                    = ""
    ticker: str                         = ""
    signal_id: str                      = ""
    outcome: str                        = DecisionOutcome.REJECTED.value
    reason: str                         = ""
    pipeline_steps_completed: int       = 0
    decided_at: str                     = field(default_factory=_now_iso)
    proposal_id: Optional[str]          = None
    extra: Dict[str, Any]               = field(default_factory=dict)

    # Safety labels
    paper_only: bool                    = True
    research_only: bool                 = True
    simulation_only: bool               = True
    not_a_real_order: bool              = True
    no_broker_call: bool                = True

    def __post_init__(self) -> None:
        assert self.paper_only is True
        assert self.not_a_real_order is True
        assert self.no_broker_call is True


# ---------------------------------------------------------------------------
# Paper order proposal
# ---------------------------------------------------------------------------

@dataclass
class PaperOrderProposal:
    """A research-only paper order proposal (never submitted to any broker)."""
    proposal_id: str                = field(default_factory=_new_id)
    decision_id: str                = ""
    strategy_id: str                = ""
    ticker: str                     = ""
    signal_type: str                = SignalType.HOLD.value
    proposed_size: float            = 0.0
    proposed_price: Optional[float] = None
    status: str                     = ProposalStatus.PENDING.value
    created_at: str                 = field(default_factory=_now_iso)
    submitted_at: Optional[str]     = None
    accepted_at: Optional[str]      = None
    rejected_at: Optional[str]      = None
    rejection_reason: str           = ""
    metadata: Dict[str, Any]        = field(default_factory=dict)

    # Safety labels — all permanently set
    paper_only: bool                = True
    research_only: bool             = True
    simulation_only: bool           = True
    not_a_real_order: bool          = True
    no_broker_call: bool            = True
    no_real_account: bool           = True
    no_formal_portfolio_ledger_write: bool = True

    def __post_init__(self) -> None:
        assert self.paper_only is True
        assert self.research_only is True
        assert self.simulation_only is True
        assert self.not_a_real_order is True
        assert self.no_broker_call is True
        assert self.no_real_account is True
        assert self.no_formal_portfolio_ledger_write is True
        allowed = {st.value for st in SignalType}
        assert self.signal_type in allowed


# ---------------------------------------------------------------------------
# Journal entry
# ---------------------------------------------------------------------------

@dataclass
class JournalEntry:
    """Single entry in the strategy journal."""
    entry_id: str                   = field(default_factory=_new_id)
    strategy_id: str                = ""
    event_type: str                 = JournalEventType.SIGNAL_RECEIVED.value
    timestamp: str                  = field(default_factory=_now_iso)
    summary: str                    = ""
    detail: Dict[str, Any]          = field(default_factory=dict)
    related_ids: List[str]          = field(default_factory=list)


# ---------------------------------------------------------------------------
# Checkpoint
# ---------------------------------------------------------------------------

@dataclass
class StrategyCheckpoint:
    """Serializable checkpoint for strategy state recovery."""
    checkpoint_id: str              = field(default_factory=_new_id)
    strategy_id: str                = ""
    reason: str                     = CheckpointReason.PERIODIC.value
    saved_at: str                   = field(default_factory=_now_iso)
    signal_count: int               = 0
    decision_count: int             = 0
    proposal_count: int             = 0
    cooldown_map: Dict[str, str]    = field(default_factory=dict)
    rate_window: List[str]          = field(default_factory=list)
    open_proposals: List[str]       = field(default_factory=list)
    extra_state: Dict[str, Any]     = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Lineage record
# ---------------------------------------------------------------------------

@dataclass
class LineageRecord:
    """Lineage tracing a decision back to its originating signal and trigger."""
    lineage_id: str                 = field(default_factory=_new_id)
    proposal_id: str                = ""
    decision_id: str                = ""
    signal_id: str                  = ""
    strategy_id: str                = ""
    trigger_type: str               = TriggerType.MANUAL.value
    ticker: str                     = ""
    signal_type: str                = SignalType.HOLD.value
    recorded_at: str                = field(default_factory=_now_iso)
    reproducibility_hash: str       = ""
    pipeline_steps: int             = 0
    outcome: str                    = DecisionOutcome.REJECTED.value
    extra: Dict[str, Any]           = field(default_factory=dict)
