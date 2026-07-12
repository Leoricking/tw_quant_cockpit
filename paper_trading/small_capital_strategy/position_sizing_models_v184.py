"""
paper_trading/small_capital_strategy/position_sizing_models_v184.py
Data models for Position Sizing & Capital Allocation Lab v1.8.4.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Allocation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CapitalProfile:
    capital: float = 300000.0
    capital_stage: str = "300K"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    allocation_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    schema_version: str = "184"


@dataclass
class RiskBudget:
    per_trade_risk_pct: float = 1.0
    max_single_position_pct: float = 20.0
    max_total_equity_exposure_pct: float = 60.0
    cash_reserve_pct: float = 20.0
    max_sector_exposure_pct: float = 35.0
    max_theme_exposure_pct: float = 40.0
    max_concurrent_positions: int = 4
    max_drawdown_budget_pct: float = 20.0
    stop_loss_distance_pct: float = 7.0
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    schema_version: str = "184"


@dataclass
class PositionSizingInput:
    capital: float = 300000.0
    per_trade_risk_pct: float = 1.0
    stop_loss_distance_pct: float = 7.0
    max_single_position_pct: float = 20.0
    max_total_equity_exposure_pct: float = 60.0
    cash_reserve_pct: float = 20.0
    max_concurrent_positions: int = 4
    max_drawdown_budget_pct: float = 20.0
    current_drawdown_pct: float = 0.0
    current_positions: int = 0
    current_exposure_pct: float = 0.0
    ruin_risk_pct: float = 0.0
    volatility_pct: float = 15.0
    abc_buy_point: str = "A_10MA_PULLBACK"
    market_regime: str = "BULL"
    has_stop_loss: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    allocation_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    schema_version: str = "184"


@dataclass
class PositionSizingRule:
    rule_name: str = "fixed_risk"
    description: str = ""
    per_trade_risk_pct: float = 1.0
    stop_loss_distance_pct: float = 7.0
    max_position_pct: float = 20.0
    enabled: bool = True
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "184"


@dataclass
class PositionSizingResult:
    capital: float = 300000.0
    per_trade_risk_amount: float = 0.0
    max_loss_allowed: float = 0.0
    stop_loss_distance_pct: float = 7.0
    suggested_position_value: float = 0.0
    suggested_position_pct: float = 0.0
    max_shares_estimate: float = 0.0
    initial_entry_value: float = 0.0
    add_position_value: float = 0.0
    reduce_position_trigger: str = "REVIEW_REQUIRED"
    stop_loss_trigger: str = "REVIEW_REQUIRED"
    cash_after_entry: float = 0.0
    cash_reserve_pct: float = 20.0
    total_exposure_pct: float = 0.0
    concentration_risk_score: float = 0.0
    drawdown_budget_usage_pct: float = 0.0
    ruin_risk_adjustment: float = 1.0
    final_position_grade: str = "SAFE"
    action: str = "PAPER_PLAN_READY"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    allocation_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    schema_version: str = "184"


@dataclass
class PortfolioAllocationInput:
    capital: float = 300000.0
    max_concurrent_positions: int = 4
    max_total_equity_exposure_pct: float = 60.0
    cash_reserve_pct: float = 20.0
    max_sector_exposure_pct: float = 35.0
    max_theme_exposure_pct: float = 40.0
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    schema_version: str = "184"


@dataclass
class PortfolioAllocationResult:
    capital: float = 300000.0
    max_deployable_capital: float = 0.0
    per_position_budget: float = 0.0
    cash_reserve_amount: float = 0.0
    total_exposure_pct: float = 0.0
    positions_capacity: int = 4
    action: str = "ALLOCATION_ONLY"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    schema_version: str = "184"


@dataclass
class ScalingPlan:
    initial_entry_pct: float = 40.0
    add1_pct: float = 30.0
    add2_pct: float = 30.0
    abc_buy_point: str = "A_10MA_PULLBACK"
    add_trigger: str = "PAPER_ADD_ALLOWED"
    reduce_trigger: str = "REDUCE_RISK"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "184"


@dataclass
class AddPositionPlan:
    add_value: float = 0.0
    add_pct_of_planned: float = 0.0
    trigger_condition: str = ""
    action: str = "PAPER_ADD_ALLOWED"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "184"


@dataclass
class ReducePositionPlan:
    reduce_trigger_pct: float = 0.0
    reduce_reason: str = ""
    action: str = "REDUCE_RISK"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "184"


@dataclass
class StopLossBudget:
    stop_loss_distance_pct: float = 7.0
    max_loss_per_trade: float = 0.0
    total_stop_loss_budget: float = 0.0
    stop_loss_trigger: str = "REVIEW_REQUIRED"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "184"


@dataclass
class DrawdownBudget:
    max_drawdown_budget_pct: float = 20.0
    current_drawdown_pct: float = 0.0
    remaining_drawdown_pct: float = 20.0
    drawdown_budget_usage_pct: float = 0.0
    budget_exhausted: bool = False
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "184"


@dataclass
class ConcentrationRiskReport:
    single_position_pct: float = 0.0
    max_allowed_single_pct: float = 20.0
    sector_exposure_pct: float = 0.0
    max_allowed_sector_pct: float = 35.0
    theme_exposure_pct: float = 0.0
    max_allowed_theme_pct: float = 40.0
    concentration_risk_score: float = 0.0
    risk_level: str = "SAFE"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "184"


@dataclass
class ExposureLimitReport:
    total_exposure_pct: float = 0.0
    max_total_exposure_pct: float = 60.0
    cash_reserve_pct: float = 20.0
    cash_reserve_amount: float = 0.0
    exposure_ok: bool = True
    cash_reserve_ok: bool = True
    action: str = "PAPER_PLAN_READY"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "184"


@dataclass
class CashReservePlan:
    capital: float = 300000.0
    cash_reserve_pct: float = 20.0
    cash_reserve_amount: float = 0.0
    deployable_capital: float = 0.0
    action: str = "ALLOCATION_ONLY"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "184"


@dataclass
class CapitalStagePlan:
    capital: float = 300000.0
    stage_label: str = "300K"
    max_per_trade_risk_amount: float = 0.0
    max_position_value: float = 0.0
    suggested_max_positions: int = 3
    recommended_risk_pct: float = 1.0
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "184"


@dataclass
class PositionSizingDashboard:
    capital_profile: Optional[CapitalProfile] = None
    risk_budget: Optional[RiskBudget] = None
    sizing_result: Optional[PositionSizingResult] = None
    drawdown_budget: Optional[DrawdownBudget] = None
    concentration_report: Optional[ConcentrationRiskReport] = None
    exposure_report: Optional[ExposureLimitReport] = None
    cash_reserve_plan: Optional[CashReservePlan] = None
    capital_stage_plan: Optional[CapitalStagePlan] = None
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    schema_version: str = "184"


@dataclass
class PositionSizingReport:
    version: str = "1.8.4"
    release_name: str = "Position Sizing & Capital Allocation Lab"
    sections: List[str] = field(default_factory=list)
    all_checks_pass: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    allocation_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    schema_version: str = "184"


@dataclass
class PositionSizingHealthSummary:
    total: int = 0
    passed: int = 0
    failed: int = 0
    all_passed: bool = False
    status: str = "FAIL"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "184"


_ALL_MODELS = [
    "CapitalProfile", "RiskBudget", "PositionSizingInput", "PositionSizingRule",
    "PositionSizingResult", "PortfolioAllocationInput", "PortfolioAllocationResult",
    "ScalingPlan", "AddPositionPlan", "ReducePositionPlan", "StopLossBudget",
    "DrawdownBudget", "ConcentrationRiskReport", "ExposureLimitReport",
    "CashReservePlan", "CapitalStagePlan", "PositionSizingDashboard",
    "PositionSizingReport", "PositionSizingHealthSummary",
]


def get_all_model_names() -> list:
    """Return list of all model names."""
    return list(_ALL_MODELS)
