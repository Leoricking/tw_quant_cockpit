"""
portfolio/walk_forward/models_v154.py — Walk-forward Backtest Models v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
"""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from portfolio.walk_forward.enums_v154 import (
    WindowType, WindowStatus, RebalanceFrequency,
    SimulatedTransactionType, WalkForwardResultStatus, RegimeType,
    SlippageModelType
)

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
MODELS_VERSION = "1.5.4"


def _compute_hash(data: dict) -> str:
    raw = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


@dataclass
class WalkForwardConfiguration:
    config_id: str
    name: str
    version: str
    portfolio_id: str
    start_date: str
    end_date: str
    window_type: WindowType
    training_length: int
    validation_length: int
    step_length: int
    purge_length: int
    embargo_length: int
    rebalance_frequency: RebalanceFrequency
    benchmark_symbol: str
    initial_cash: float
    cost_policy_id: str
    slippage_policy_id: str
    liquidity_policy_id: str
    sizing_policy_id: str
    risk_policy_id: str
    correlation_policy_id: str
    minimum_windows: int
    minimum_observations: int
    research_only: bool = True
    auto_apply_enabled: bool = False
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class WalkForwardWindow:
    window_id: str
    sequence: int
    training_start: str
    training_end: str
    purge_start: str
    purge_end: str
    validation_start: str
    validation_end: str
    embargo_end: str
    window_type: WindowType
    status: WindowStatus
    warnings: Optional[List[str]] = None
    blockers: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class HistoricalDecisionContext:
    decision_id: str
    portfolio_id: str
    as_of: str
    available_from: str
    portfolio_snapshot_id: str
    sizing_context: Optional[Dict[str, Any]] = None
    correlation_context: Optional[Dict[str, Any]] = None
    risk_control_context: Optional[Dict[str, Any]] = None
    eligible_universe: Optional[List[str]] = None
    market_regime: Optional[str] = None
    source_lineage_ids: Optional[List[str]] = None
    content_hash: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SimulatedPortfolioTransaction:
    transaction_id: str
    window_id: str
    decision_id: str
    transaction_type: SimulatedTransactionType
    symbol: str
    decision_date: str
    simulated_execution_date: str
    quantity: float
    decision_price: float
    simulated_price: float
    gross_amount: float
    fee: float
    tax: float
    slippage: float
    net_amount: float
    currency: str
    reason: str
    research_only: bool = True
    executable: bool = False
    real_order_created: bool = False
    formal_ledger_persisted: bool = False
    source_lineage_ids: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class WalkForwardWindowMetrics:
    window_id: str
    period_return: float
    annualized_return: float
    volatility: float
    max_drawdown: float
    turnover: float
    total_fees: float
    total_slippage: float
    benchmark_return: float
    excess_return: float
    positive_periods: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class WalkForwardWindowResult:
    window_id: str
    training_metrics: Optional[WalkForwardWindowMetrics]
    validation_metrics: Optional[WalkForwardWindowMetrics]
    benchmark_metrics: Optional[WalkForwardWindowMetrics] = None
    simulated_transactions: Optional[List[SimulatedPortfolioTransaction]] = None
    ending_positions: Optional[Dict[str, Any]] = None
    ending_cash: float = 0.0
    turnover: float = 0.0
    costs: float = 0.0
    slippage: float = 0.0
    maximum_drawdown: float = 0.0
    volatility: float = 0.0
    risk_budget_utilization: Optional[float] = None
    correlation_exposure: Optional[Dict[str, Any]] = None
    eligibility: Optional[Dict[str, Any]] = None
    status: Optional[WalkForwardResultStatus] = None
    source_lineage_ids: Optional[List[str]] = None
    content_hash: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class WalkForwardSummary:
    run_id: str
    config_id: str
    total_windows: int
    valid_windows: int
    partial_windows: int
    blocked_windows: int
    in_sample_return: float
    out_of_sample_return: float
    benchmark_return: float
    excess_return: float
    annualized_return: float
    annualized_volatility: float
    sharpe_like_ratio: Optional[float] = None
    maximum_drawdown: float = 0.0
    turnover: float = 0.0
    total_fees: float = 0.0
    total_taxes: float = 0.0
    total_slippage: float = 0.0
    stability_score: Optional[float] = None
    parameter_sensitivity_score: Optional[float] = None
    regime_results: Optional[List[Any]] = None
    warnings: Optional[List[str]] = None
    blockers: Optional[List[str]] = None
    status: Optional[WalkForwardResultStatus] = None
    calculation_version: str = "1.5.4"
    content_hash: Optional[str] = None
    generated_at: Optional[str] = None
    research_only: bool = True
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class StabilityResult:
    window_metric_name: str
    window_values: List[float]
    mean: float
    median: float
    standard_deviation: float
    positive_window_ratio: float
    worst_window: float
    best_window: float
    dispersion: float
    trend: Optional[str] = None
    status: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ParameterSensitivityResult:
    parameter_name: str
    tested_values: List[Any]
    results_by_value: Dict[str, Any]
    local_stability: Optional[float] = None
    cliff_effect: bool = False
    selected_value: Optional[Any] = None
    selection_applied: bool = False
    status: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class RegimeResult:
    regime_type: RegimeType
    window_count: int
    mean_return: float
    median_return: float
    max_drawdown: float
    mean_turnover: float
    mean_risk_status: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class CostPolicy:
    policy_id: str
    buy_fee_rate: float
    sell_fee_rate: float
    tax_rate: float
    minimum_fee: float
    effective_from: str
    version: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SlippagePolicy:
    policy_id: str
    model_type: SlippageModelType
    fixed_bps: Optional[float] = None
    participation_rate: Optional[float] = None
    effective_from: Optional[str] = None
    version: str = "1.5.4"
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ReproducibilityManifest:
    run_id: str
    config_hash: str
    window_hashes: Optional[List[str]] = None
    decision_hashes: Optional[List[str]] = None
    dataset_hashes: Optional[Dict[str, str]] = None
    result_hashes: Optional[List[str]] = None
    python_version: Optional[str] = None
    dependencies: Optional[Dict[str, str]] = None
    timezone: str = "Asia/Taipei"
    calendar_version: str = "1.5.4"
    seed: Optional[int] = None
    code_commit: Optional[str] = None
    fixture_hashes: Optional[Dict[str, str]] = None
    metadata: Optional[Dict[str, Any]] = None
