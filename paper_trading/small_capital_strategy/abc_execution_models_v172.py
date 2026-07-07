"""
paper_trading/small_capital_strategy/abc_execution_models_v172.py
Dataclass models for A/B/C Buy Point Execution Plan v1.7.2.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCExecutionStatus, ABCConditionStatus,
    ABCEntryMode, ABCAddMode, ABCStopLossMode, ABCTakeProfitMode,
    ABCInvalidationReason, ABCExecutionGrade, ABCRiskPermission,
    ABCPaperOrderIntentType, ABCExecutionBlockReason, ABCExecutionWarningReason,
    ABCMarketCompatibility, ABCWatchlistCompatibility,
)

_SCHEMA  = "172"
_POLICY  = "1.7.2-abc-buy-point-execution-plan"
_LINEAGE = "paper_trading.small_capital_strategy.abc_execution_models_v172"


def _now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class ABCSignalInput:
    """Raw market signal input for ABC buy-point evaluation."""
    symbol: str
    buy_point_type: ABCBuyPointType
    close: float
    ma5: float
    ma10: float
    ma20: float
    ma60: float
    volume: float
    avg_volume_20d: float
    volume_ratio: float
    atr_pct: float
    kd_k: float
    kd_d: float
    kd_dead_cross: bool
    financing_ratio: float
    institutional_net_buy_days: int
    theme_strength: str
    consolidation_weeks: int
    prior_platform_high: float
    had_first_wave: bool
    pullback_completed: bool
    volume_dry_up_before_reclaim: bool
    kd_golden_cross: bool
    institutional_reaccumulation: bool
    tier: str = "EXCLUDED"
    market_regime: str = "UNKNOWN"
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCNormalizedSignal:
    """Normalized signal after pre-processing."""
    symbol: str
    buy_point_type: ABCBuyPointType
    above_ma10: bool
    above_ma20: bool
    above_ma60: bool
    low_touched_ma10: bool
    volume_contracting: bool
    volume_confirmed: bool
    financing_safe: bool
    institutional_not_selling: bool
    consolidation_valid: bool
    first_wave_present: bool
    pullback_complete: bool
    ma20_reclaim_valid: bool
    kd_not_dead_cross: bool
    kd_improving: bool
    raw: Optional[ABCSignalInput] = None
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCConditionCheck:
    """Result of checking one buy-point condition."""
    condition_name: str
    buy_point_type: ABCBuyPointType
    status: ABCConditionStatus
    detail: str = ""
    is_blocking: bool = False
    block_reason: Optional[ABCExecutionBlockReason] = None
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCEntryPricePlan:
    """Entry price plan for an ABC buy point."""
    symbol: str
    buy_point_type: ABCBuyPointType
    entry_mode: ABCEntryMode
    entry_price: float
    entry_price_note: str = ""
    status: ABCExecutionStatus = ABCExecutionStatus.WAITING_CONFIRMATION
    block_reasons: List[ABCExecutionBlockReason] = field(default_factory=list)
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCAddPricePlan:
    """Add price plan after initial entry."""
    symbol: str
    buy_point_type: ABCBuyPointType
    add_mode: ABCAddMode
    add_price: float
    add_price_note: str = ""
    max_add_units: int = 1
    status: ABCExecutionStatus = ABCExecutionStatus.WAITING_CONFIRMATION
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCStopLossExecutionPlan:
    """Stop loss plan for ABC execution."""
    symbol: str
    buy_point_type: ABCBuyPointType
    stop_loss_mode: ABCStopLossMode
    stop_loss_price: float
    stop_loss_note: str = ""
    stop_loss_pct_from_entry: float = 0.0
    status: ABCExecutionStatus = ABCExecutionStatus.WAITING_CONFIRMATION
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCTakeProfitExecutionPlan:
    """Take profit plan for ABC execution."""
    symbol: str
    buy_point_type: ABCBuyPointType
    take_profit_mode: ABCTakeProfitMode
    take_profit_references: List[float] = field(default_factory=list)
    partial_pct_first: float = 0.0
    swing_pct_target: float = 0.0
    take_profit_note: str = ""
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCInvalidationPlan:
    """Conditions that invalidate an ABC execution plan."""
    symbol: str
    buy_point_type: ABCBuyPointType
    invalidation_reasons: List[ABCInvalidationReason] = field(default_factory=list)
    invalidation_notes: List[str] = field(default_factory=list)
    bars_to_confirm: int = 3
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCPositionSizingBridgeResult:
    """Position sizing result bridged from v1.7.0 capital profile."""
    symbol: str
    capital_twd: float
    max_holdings: int
    position_amount: float
    quantity_estimate: int
    max_loss_amount: float
    risk_pct: float
    training_cap_applied: bool
    risk_permission: ABCRiskPermission
    block_reasons: List[ABCExecutionBlockReason] = field(default_factory=list)
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCWatchlistBridgeResult:
    """Watchlist tier compatibility result."""
    symbol: str
    tier: str
    compatibility: ABCWatchlistCompatibility
    allowed_buy_points: List[ABCBuyPointType] = field(default_factory=list)
    preferred_buy_points: List[ABCBuyPointType] = field(default_factory=list)
    block_reasons: List[ABCExecutionBlockReason] = field(default_factory=list)
    training_cap: float = 0.0
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCMarketRegimeBridgeResult:
    """Market regime compatibility result."""
    market_regime: str
    buy_point_type: ABCBuyPointType
    tier: str
    compatibility: ABCMarketCompatibility
    block_reasons: List[ABCExecutionBlockReason] = field(default_factory=list)
    warnings: List[ABCExecutionWarningReason] = field(default_factory=list)
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCForbiddenRuleBridgeResult:
    """Forbidden trade rule check result."""
    symbol: str
    rule_name: str
    passed: bool
    detail: str = ""
    block_reasons: List[ABCExecutionBlockReason] = field(default_factory=list)
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCPaperOrderIntent:
    """Paper order intent — no real order, no broker execution."""
    intent_id: str
    symbol: str
    buy_point_type: ABCBuyPointType
    tier: str
    action: ABCPaperOrderIntentType
    reference_price: float
    quantity_estimate: int
    position_size_amount: float
    max_loss_amount: float
    stop_loss_price: float
    take_profit_references: List[float] = field(default_factory=list)
    invalidation_conditions: List[str] = field(default_factory=list)
    block_reasons: List[ABCExecutionBlockReason] = field(default_factory=list)
    warnings: List[ABCExecutionWarningReason] = field(default_factory=list)
    real_order_requested: bool = False
    broker_execution_requested: bool = False
    paper_only: bool = True
    no_real_orders: bool = True
    broker_execution_enabled: bool = False
    production_trading_enabled: bool = False
    not_investment_advice: bool = True
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    research_only: bool = True


@dataclass
class ABCExecutionScorecard:
    """Scorecard for ABC execution plan (0-100)."""
    symbol: str
    buy_point_type: ABCBuyPointType
    total_score: float
    buy_point_condition_score: float
    risk_sizing_score: float
    watchlist_tier_score: float
    market_regime_score: float
    stop_loss_score: float
    take_profit_score: float
    safety_score: float
    grade: ABCExecutionGrade
    weights_sum: int = 100
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCExecutionPlan:
    """Complete ABC execution plan for a candidate."""
    symbol: str
    buy_point_type: ABCBuyPointType
    tier: str
    status: ABCExecutionStatus
    conditions_checked: List[ABCConditionCheck] = field(default_factory=list)
    entry_plan: Optional[ABCEntryPricePlan] = None
    add_plan: Optional[ABCAddPricePlan] = None
    stop_loss_plan: Optional[ABCStopLossExecutionPlan] = None
    take_profit_plan: Optional[ABCTakeProfitExecutionPlan] = None
    invalidation_plan: Optional[ABCInvalidationPlan] = None
    position_sizing: Optional[ABCPositionSizingBridgeResult] = None
    watchlist_bridge: Optional[ABCWatchlistBridgeResult] = None
    regime_bridge: Optional[ABCMarketRegimeBridgeResult] = None
    forbidden_checks: List[ABCForbiddenRuleBridgeResult] = field(default_factory=list)
    paper_intent: Optional[ABCPaperOrderIntent] = None
    scorecard: Optional[ABCExecutionScorecard] = None
    block_reasons: List[ABCExecutionBlockReason] = field(default_factory=list)
    warnings: List[ABCExecutionWarningReason] = field(default_factory=list)
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCExecutionReport:
    """Full ABC execution report (16 sections)."""
    symbol: str
    buy_point_type: ABCBuyPointType
    plan: Optional[ABCExecutionPlan] = None
    sections: Dict[str, Any] = field(default_factory=dict)
    report_format: str = "JSON"
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ABCExecutionHealthSummary:
    """Summary of execution health check."""
    version: str
    release_name: str
    all_passed: bool
    passed: int
    failed: int
    total: int
    status: str
    details: List[Dict[str, Any]] = field(default_factory=list)
    schema_version: str = _SCHEMA
    policy_version: str = _POLICY
    source_lineage: str = _LINEAGE
    created_at: str = field(default_factory=_now)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
