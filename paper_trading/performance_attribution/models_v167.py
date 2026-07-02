"""
paper_trading/performance_attribution/models_v167.py
Data models for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No broker session, real account token, API secret, password, credential,
    real order handle, production DB connection, bank account, or real capital control.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from .enums_v167 import (
    AttributionLevel, AttributionDimension, ReturnBasis, ReconciliationStatus,
    AttributionStatus, ConfidenceLevel, DataQualityStatus, PeriodType,
    TradeDirection, PositionState, RegimeType, BenchmarkMode, CostType,
    CostQuality, ExecutionQuality, ExecutionReference, FixtureUsageType, AttributionPurpose,
)

SCHEMA_VERSION  = "167"
POLICY_VERSION  = "1.6.7-paper-attribution"
RESEARCH_ONLY   = True
PAPER_ONLY      = True
NO_REAL_ORDERS  = True


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ─────────────────────────────────────────────────────────────────────────────
# Core period and snapshot models
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class AttributionPeriod:
    period_start: str           # ISO8601 date
    period_end: str             # ISO8601 date
    period_type: PeriodType = PeriodType.ARBITRARY
    timezone: str = "Asia/Taipei"
    trading_days: int = 0
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True

    def __post_init__(self) -> None:
        if self.period_start > self.period_end:
            raise ValueError(f"Reversed period: {self.period_start} > {self.period_end}")


@dataclass
class BenchmarkSnapshot:
    benchmark_id: str
    benchmark_mode: BenchmarkMode
    period_start: str
    period_end: str
    weights: Dict[str, float] = field(default_factory=dict)
    returns: Dict[str, float] = field(default_factory=dict)
    total_return: Optional[float] = None
    source_lineage: str = ""
    stale: bool = False
    missing: bool = False
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True


@dataclass
class PortfolioSnapshot:
    portfolio_id: str
    period_start: str
    period_end: str
    initial_equity: float
    ending_equity: float
    cash: float = 0.0
    gross_exposure: float = 0.0
    net_exposure: float = 0.0
    source_lineage: str = ""
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class PositionSnapshot:
    position_id: str
    symbol: str
    strategy_id: str
    session_id: str
    open_date: str
    close_date: Optional[str]
    average_cost: float
    quantity: float
    current_price: float
    state: PositionState
    direction: TradeDirection
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    total_pnl: float = 0.0
    cost_basis: float = 0.0
    source_lineage: str = ""
    schema_version: str = SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True


@dataclass
class TradeSnapshot:
    trade_id: str
    symbol: str
    strategy_id: str
    session_id: str
    direction: TradeDirection
    quantity: float
    signal_price: Optional[float]
    decision_price: Optional[float]
    fill_price: float
    exit_price: Optional[float]
    timestamp: str
    gross_pnl: float = 0.0
    net_pnl: float = 0.0
    cost: float = 0.0
    slippage: float = 0.0
    source_lineage: str = ""
    schema_version: str = SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    simulated: bool = True


@dataclass
class ExecutionSnapshot:
    execution_id: str
    trade_id: str
    symbol: str
    fill_price: float
    fill_quantity: float
    order_price: float
    signal_price: Optional[float]
    decision_price: Optional[float]
    vwap: Optional[float]
    twap: Optional[float]
    close_price: Optional[float]
    timestamp: str
    simulated: bool = True
    model_version: str = ""
    slippage_policy: str = ""
    liquidity_assumption: str = ""
    price_reference: str = ""
    implementation_shortfall: float = 0.0
    source_lineage: str = ""
    schema_version: str = SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True


@dataclass
class CostSnapshot:
    run_id: str
    period_start: str
    period_end: str
    commission: float = 0.0
    transaction_tax: float = 0.0
    exchange_fee: float = 0.0
    borrow_cost: float = 0.0
    financing_cost: float = 0.0
    spread_cost: float = 0.0
    slippage: float = 0.0
    impact_proxy: float = 0.0
    turnover_drag: float = 0.0
    other: float = 0.0
    quality: CostQuality = CostQuality.KNOWN
    unknown_cost_amount: float = 0.0
    estimated_cost_amount: float = 0.0
    source_lineage: str = ""
    schema_version: str = SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True

    @property
    def total_known(self) -> float:
        return (self.commission + self.transaction_tax + self.exchange_fee
                + self.borrow_cost + self.financing_cost + self.spread_cost
                + self.slippage + self.impact_proxy + self.turnover_drag + self.other)

    @property
    def total(self) -> float:
        return self.total_known + self.unknown_cost_amount + self.estimated_cost_amount


@dataclass
class MarketSnapshot:
    symbol: str
    period_start: str
    period_end: str
    prices: Dict[str, float] = field(default_factory=dict)  # date -> close
    volumes: Dict[str, float] = field(default_factory=dict)
    returns: Dict[str, float] = field(default_factory=dict)
    source_lineage: str = ""
    schema_version: str = SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True


@dataclass
class RegimeSnapshot:
    period_start: str
    period_end: str
    regimes: Dict[str, RegimeType] = field(default_factory=dict)  # date -> regime
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    source_lineage: str = ""
    schema_version: str = SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True


@dataclass
class FactorSnapshot:
    symbol: str
    period_start: str
    period_end: str
    factor_exposures: Dict[str, float] = field(default_factory=dict)  # factor -> exposure
    factor_returns: Dict[str, float] = field(default_factory=dict)
    is_proxy: bool = True
    proxy_method: str = ""
    confidence: ConfidenceLevel = ConfidenceLevel.LOW
    source_lineage: str = ""
    schema_version: str = SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True


# ─────────────────────────────────────────────────────────────────────────────
# Contribution models
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ReturnContribution:
    entity_id: str
    level: AttributionLevel
    gross_return: float
    net_return: float
    realized_return: float
    unrealized_return: float
    active_return: float
    cost_return: float
    execution_return: float
    residual_return: float
    cumulative_return: Optional[float] = None
    twr: Optional[float] = None
    mwr: Optional[float] = None
    mwr_available: bool = False
    basis_points_active: float = 0.0
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class PnLContribution:
    entity_id: str
    level: AttributionLevel
    realized_pnl: float
    unrealized_pnl: float
    gross_pnl: float
    net_pnl: float
    commission: float = 0.0
    transaction_tax: float = 0.0
    exchange_fee: float = 0.0
    borrow_cost: float = 0.0
    financing_cost: float = 0.0
    spread_cost: float = 0.0
    slippage: float = 0.0
    impact_proxy: float = 0.0
    turnover_drag: float = 0.0
    dividend: float = 0.0
    distribution: float = 0.0
    cash_carry: float = 0.0
    residual: float = 0.0
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class SelectionContribution:
    entity_id: str
    level: AttributionLevel
    selection_return: float
    selection_alpha: float
    hit_rate: float
    win_rate: float
    average_winner: float
    average_loser: float
    top_contributors: List[str] = field(default_factory=list)
    bottom_contributors: List[str] = field(default_factory=list)
    benchmark_mode: BenchmarkMode = BenchmarkMode.NONE
    look_ahead_checked: bool = True
    no_look_ahead: bool = True
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class AllocationContribution:
    entity_id: str
    level: AttributionLevel
    allocation_return: float
    overweight_effect: float
    underweight_effect: float
    cash_allocation_effect: float
    leverage_effect: float
    idle_cash_drag: float
    capital_utilization_effect: float
    weight_sum_drift: float = 0.0
    benchmark_mode: BenchmarkMode = BenchmarkMode.NONE
    double_count_checked: bool = True
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class TimingContribution:
    entity_id: str
    level: AttributionLevel
    timing_return: float
    entry_timing: float
    exit_timing: float
    add_on_timing: float
    trim_timing: float
    delayed_entry: float
    early_exit: float
    missed_move: float
    avoided_drawdown: float
    signal_execution_delay: float
    stale_signal_drag: float
    reference_used: ExecutionReference
    insufficient_data: bool = False
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ExecutionContribution:
    entity_id: str
    level: AttributionLevel
    implementation_shortfall: float
    delay_cost: float
    spread_cost: float
    slippage: float
    adverse_selection_proxy: float
    partial_fill_impact: float
    unfilled_opportunity_cost: float
    fill_ratio: float
    simulated: bool = True
    model_version: str = ""
    slippage_policy: str = ""
    liquidity_assumption: str = ""
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class CostContribution:
    entity_id: str
    level: AttributionLevel
    commission: float
    transaction_tax: float
    exchange_fee: float
    borrow_fee: float
    financing_cost: float
    slippage: float
    spread: float
    impact_proxy: float
    turnover_cost: float
    other_modeled: float
    unknown_cost: float
    estimated_cost: float
    known_cost: float
    total_cost: float
    cost_bps: float = 0.0
    cost_pct_gross_pnl: float = 0.0
    cost_pct_net_pnl: float = 0.0
    cost_pct_equity: float = 0.0
    cost_quality: CostQuality = CostQuality.KNOWN
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class SlippageContribution:
    entity_id: str
    level: AttributionLevel
    total_slippage: float
    positive_slippage: float
    negative_slippage: float
    slippage_bps: float
    per_trade_slippage: float
    slippage_vs_vwap: Optional[float] = None
    slippage_vs_close: Optional[float] = None
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class TurnoverContribution:
    entity_id: str
    level: AttributionLevel
    turnover_rate: float
    turnover_cost: float
    turnover_drag_bps: float
    trade_count: int
    avg_trade_size: float
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ExposureContribution:
    entity_id: str
    level: AttributionLevel
    market_exposure: float
    beta_exposure: float
    gross_exposure: float
    net_exposure: float
    long_exposure: float
    short_exposure: float
    concentration: float
    leverage: float
    sector_exposures: Dict[str, float] = field(default_factory=dict)
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class RiskContribution:
    entity_id: str
    level: AttributionLevel
    volatility_contribution: float
    downside_volatility_contribution: float
    drawdown_contribution: float
    correlation_cluster_contribution: float
    leverage_contribution: float
    liquidity_risk_proxy: float
    gap_risk: float
    overnight_risk: float
    turnover_risk: float
    tail_loss_contribution: float
    marginal_contribution: float
    component_contribution: float
    normalized_contribution: float
    fallback_method: str = ""
    data_complete: bool = True
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class DrawdownContribution:
    entity_id: str
    level: AttributionLevel
    max_drawdown: float
    peak_timestamp: str
    trough_timestamp: str
    recovery_timestamp: Optional[str]
    peak_to_trough_duration: int
    recovery_duration: Optional[int]
    no_recovery: bool
    symbol_contribution: float
    strategy_contribution: float
    session_contribution: float
    allocation_contribution: float
    concentration_contribution: float
    leverage_contribution: float
    execution_contribution: float
    cost_contribution: float
    residual_contribution: float
    reconciled: bool = False
    incomplete_period: bool = False
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class RegimeContribution:
    entity_id: str
    level: AttributionLevel
    regime: RegimeType
    return_in_regime: float
    net_return_in_regime: float
    hit_rate_in_regime: float
    drawdown_in_regime: float
    cost_in_regime: float
    selection_effect_in_regime: float
    allocation_effect_in_regime: float
    timing_effect_in_regime: float
    unknown_forced: bool = False
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class BenchmarkContribution:
    entity_id: str
    level: AttributionLevel
    benchmark_id: str
    benchmark_mode: BenchmarkMode
    benchmark_return: float
    active_return: float
    source_lineage: str = ""
    stale_detected: bool = False
    missing_detected: bool = False
    equal_weight_fallback: bool = False
    look_ahead_checked: bool = True
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class FactorContribution:
    entity_id: str
    level: AttributionLevel
    factor_name: str
    factor_exposure: float
    factor_return: float
    factor_contribution: float
    is_proxy: bool
    proxy_method: str = ""
    unavailable: bool = False
    residual_alpha: float = 0.0
    confidence: ConfidenceLevel = ConfidenceLevel.LOW
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class ResidualContribution:
    entity_id: str
    level: AttributionLevel
    residual: float
    rounding_residual: float
    model_residual: float
    threshold: float
    exceeds_threshold: bool
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    source_lineage: str = ""
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


# ─────────────────────────────────────────────────────────────────────────────
# Aggregation models
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class AttributionBreakdown:
    entity_id: str
    level: AttributionLevel
    period_start: str
    period_end: str
    selection: float = 0.0
    allocation: float = 0.0
    timing: float = 0.0
    exposure: float = 0.0
    execution: float = 0.0
    cost: float = 0.0
    risk: float = 0.0
    regime: float = 0.0
    benchmark: float = 0.0
    factor: float = 0.0
    residual: float = 0.0
    active_return: float = 0.0
    sum_of_components: float = 0.0
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    source_lineage: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class AttributionReconciliation:
    entity_id: str
    expected_total: float
    actual_component_sum: float
    residual: float
    rounding_residual: float
    model_residual: float
    tolerance: float
    status: ReconciliationStatus
    failing_dimensions: List[str] = field(default_factory=list)
    source_lineage: str = ""
    precision: int = 8
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class AttributionScore:
    entity_id: str
    total_score: float          # 0–100
    grade: str                  # A, B, C, D, F
    reconciliation_score: float
    data_completeness_score: float
    execution_quality_score: float
    cost_completeness_score: float
    benchmark_quality_score: float
    risk_model_quality_score: float
    lineage_quality_score: float
    determinism_score: float
    component_scores: Dict[str, float] = field(default_factory=dict)
    failed_dimensions: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    blocking_issues: List[str] = field(default_factory=list)
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    usable_for_research: bool = True
    usable_for_paper_review: bool = True
    not_for_real_trading: bool = True
    period_start: str = ""
    period_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class AttributionReport:
    run_id: str
    portfolio_id: str
    period_start: str
    period_end: str
    sections: Dict[str, Any] = field(default_factory=dict)
    score: Optional[AttributionScore] = None
    reconciliation: Optional[AttributionReconciliation] = None
    residual_visible: bool = True
    unknown_cost_visible: bool = True
    estimated_cost_visible: bool = True
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    status: AttributionStatus = AttributionStatus.COMPLETE
    formats_available: List[str] = field(default_factory=lambda: ["markdown", "json", "csv", "console"])
    limitations: List[str] = field(default_factory=list)
    not_for_real_trading: bool = True
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    source_lineage: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class AttributionRun:
    run_id: str
    portfolio_id: str
    strategy_id: str
    session_id: str
    period: AttributionPeriod
    status: AttributionStatus = AttributionStatus.COMPLETE
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    deterministic_seed: int = 0
    residual_tolerance: float = 0.0001
    rounding_tolerance: float = 1e-8
    data_quality: DataQualityStatus = DataQualityStatus.COMPLETE
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    policy_version: str = POLICY_VERSION
    source_lineage: str = ""
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class AttributionQuery:
    query_id: str
    portfolio_id: Optional[str] = None
    strategy_id: Optional[str] = None
    session_id: Optional[str] = None
    symbol: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    regime: Optional[RegimeType] = None
    status: Optional[AttributionStatus] = None
    level: Optional[AttributionLevel] = None
    limit: int = 100
    offset: int = 0
    read_only: bool = True
    paper_only: bool = True
    research_only: bool = True


@dataclass
class AttributionSummary:
    total_runs: int
    complete_runs: int
    degraded_runs: int
    failed_runs: int
    portfolios: List[str] = field(default_factory=list)
    strategies: List[str] = field(default_factory=list)
    sessions: List[str] = field(default_factory=list)
    date_start: str = ""
    date_end: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True


@dataclass
class AttributionComparison:
    comparison_id: str
    entity_ids: List[str]
    dimension: AttributionDimension
    values: Dict[str, float] = field(default_factory=dict)
    ranked: List[str] = field(default_factory=list)
    period_start: str = ""
    period_end: str = ""
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class AttributionValidationResult:
    run_id: str
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    blocked: bool = False
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True


@dataclass
class AttributionHealthSummary:
    version: str
    release_name: str
    total_checks: int
    passed: int
    failed: int
    status: str
    checks: List[Dict[str, Any]] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    not_for_production: bool = True
    created_at: str = field(default_factory=_utcnow_iso)
    schema_version: str = SCHEMA_VERSION
