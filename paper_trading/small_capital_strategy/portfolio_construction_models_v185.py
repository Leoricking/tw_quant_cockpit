"""
paper_trading/small_capital_strategy/portfolio_construction_models_v185.py
Data models for Portfolio Construction & Rebalancing Lab v1.8.5.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Portfolio Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class PortfolioProfile:
    capital: float = 300000.0
    capital_stage: str = "300K"
    max_positions: int = 3
    core_position_pct: float = 30.0
    satellite_position_pct: float = 15.0
    max_single_position_pct: float = 25.0
    max_total_exposure_pct: float = 60.0
    min_cash_reserve_pct: float = 20.0
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    portfolio_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    schema_version: str = "185"


@dataclass
class PortfolioHolding:
    ticker: str = ""
    name: str = ""
    sector: str = ""
    theme: str = ""
    weight_pct: float = 0.0
    value: float = 0.0
    cost_basis: float = 0.0
    current_price: float = 0.0
    unrealized_pnl_pct: float = 0.0
    above_10ma: bool = True
    above_20ma: bool = True
    abc_buy_point: str = "A_10MA_PULLBACK"
    stop_loss_distance_pct: float = 7.0
    conviction_score: float = 5.0
    volatility_pct: float = 15.0
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


@dataclass
class PortfolioCandidate:
    ticker: str = ""
    name: str = ""
    sector: str = ""
    theme: str = ""
    conviction_score: float = 5.0
    volatility_pct: float = 15.0
    abc_buy_point: str = "A_10MA_PULLBACK"
    stop_loss_distance_pct: float = 7.0
    above_10ma: bool = True
    above_20ma: bool = True
    market_regime_compatible: bool = True
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


@dataclass
class PortfolioConstructionInput:
    capital: float = 300000.0
    market_regime: str = "BULL"
    max_positions: int = 3
    max_single_position_pct: float = 25.0
    max_total_exposure_pct: float = 60.0
    max_sector_exposure_pct: float = 35.0
    max_theme_exposure_pct: float = 40.0
    min_cash_reserve_pct: float = 20.0
    max_correlation_bucket_pct: float = 40.0
    max_drawdown_budget_pct: float = 20.0
    rebalance_threshold_pct: float = 10.0
    monte_carlo_ruin_risk_pct: float = 0.0
    weighting_method: str = "equal_weight"
    holdings: List[PortfolioHolding] = field(default_factory=list)
    candidates: List[PortfolioCandidate] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    portfolio_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    schema_version: str = "185"


@dataclass
class PortfolioConstructionResult:
    capital: float = 300000.0
    holding_count: int = 0
    max_positions: int = 3
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 0.0
    cash_reserve_amount: float = 0.0
    single_position_max_pct: float = 0.0
    concentration_risk_score: float = 0.0
    diversification_score: float = 0.0
    correlation_risk_score: float = 0.0
    drawdown_budget_usage_pct: float = 0.0
    monte_carlo_ruin_risk_adjustment: float = 1.0
    suggested_keep_list: List[str] = field(default_factory=list)
    suggested_reduce_list: List[str] = field(default_factory=list)
    suggested_replace_list: List[str] = field(default_factory=list)
    suggested_watch_list: List[str] = field(default_factory=list)
    blocked_candidates: List[str] = field(default_factory=list)
    rebalance_actions: List[str] = field(default_factory=list)
    final_portfolio_grade: str = "BALANCED"
    action: str = "PORTFOLIO_ONLY"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    portfolio_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    schema_version: str = "185"


@dataclass
class RebalanceInput:
    capital: float = 300000.0
    holdings: List[PortfolioHolding] = field(default_factory=list)
    target_weights: Dict[str, float] = field(default_factory=dict)
    rebalance_threshold_pct: float = 10.0
    market_regime: str = "BULL"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    schema_version: str = "185"


@dataclass
class RebalancePlan:
    actions: List["RebalanceAction"] = field(default_factory=list)
    total_drift_pct: float = 0.0
    rebalance_needed: bool = False
    action: str = "PORTFOLIO_ONLY"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


@dataclass
class RebalanceAction:
    ticker: str = ""
    current_weight_pct: float = 0.0
    target_weight_pct: float = 0.0
    drift_pct: float = 0.0
    action_type: str = "OBSERVE"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


@dataclass
class PortfolioExposureReport:
    total_exposure_pct: float = 0.0
    max_total_exposure_pct: float = 60.0
    cash_reserve_pct: float = 0.0
    single_position_max_pct: float = 0.0
    exposure_ok: bool = True
    action: str = "PORTFOLIO_ONLY"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


@dataclass
class SectorExposureReport:
    sector_weights: Dict[str, float] = field(default_factory=dict)
    max_sector_exposure_pct: float = 35.0
    overexposed_sectors: List[str] = field(default_factory=list)
    sector_ok: bool = True
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


@dataclass
class ThemeExposureReport:
    theme_weights: Dict[str, float] = field(default_factory=dict)
    max_theme_exposure_pct: float = 40.0
    overexposed_themes: List[str] = field(default_factory=list)
    theme_ok: bool = True
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


@dataclass
class CorrelationRiskReport:
    correlation_buckets: Dict[str, float] = field(default_factory=dict)
    max_correlation_bucket_pct: float = 40.0
    high_correlation_pairs: List[str] = field(default_factory=list)
    correlation_risk_score: float = 0.0
    correlation_ok: bool = True
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


@dataclass
class ConcentrationLimit:
    max_single_position_pct: float = 25.0
    max_sector_pct: float = 35.0
    max_theme_pct: float = 40.0
    max_correlation_bucket_pct: float = 40.0
    min_cash_reserve_pct: float = 20.0
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


@dataclass
class DiversificationScore:
    score: float = 0.0
    sector_count: int = 0
    theme_count: int = 0
    position_count: int = 0
    herfindahl_index: float = 0.0
    grade: str = "ACCEPTABLE"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


@dataclass
class RotationCandidate:
    ticker: str = ""
    theme: str = ""
    sector: str = ""
    rotation_score: float = 0.0
    momentum_score: float = 0.0
    conviction_score: float = 0.0
    suggested_action: str = "OBSERVE"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


@dataclass
class KeepOrReplaceDecision:
    ticker: str = ""
    decision: str = "OBSERVE"
    reason: str = ""
    above_10ma: bool = True
    above_20ma: bool = True
    theme_strength: str = "STRONG"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


@dataclass
class PortfolioRiskBudget:
    capital: float = 300000.0
    max_total_exposure_pct: float = 60.0
    max_single_position_pct: float = 25.0
    max_sector_exposure_pct: float = 35.0
    max_theme_exposure_pct: float = 40.0
    max_drawdown_budget_pct: float = 20.0
    min_cash_reserve_pct: float = 20.0
    max_correlation_bucket_pct: float = 40.0
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


@dataclass
class PortfolioDashboard:
    profile: Optional[PortfolioProfile] = None
    construction_result: Optional[PortfolioConstructionResult] = None
    exposure_report: Optional[PortfolioExposureReport] = None
    sector_report: Optional[SectorExposureReport] = None
    theme_report: Optional[ThemeExposureReport] = None
    correlation_report: Optional[CorrelationRiskReport] = None
    diversification_score: Optional[DiversificationScore] = None
    rebalance_plan: Optional[RebalancePlan] = None
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    schema_version: str = "185"


@dataclass
class PortfolioRebalanceReport:
    version: str = "1.8.5"
    release_name: str = "Portfolio Construction & Rebalancing Lab"
    sections: List[str] = field(default_factory=list)
    rebalance_plan: Optional[RebalancePlan] = None
    all_checks_pass: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    portfolio_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    schema_version: str = "185"


@dataclass
class PortfolioHealthSummary:
    total: int = 0
    passed: int = 0
    failed: int = 0
    all_passed: bool = False
    status: str = "FAIL"
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "185"


_ALL_MODELS = [
    "PortfolioProfile",
    "PortfolioHolding",
    "PortfolioCandidate",
    "PortfolioConstructionInput",
    "PortfolioConstructionResult",
    "RebalanceInput",
    "RebalancePlan",
    "RebalanceAction",
    "PortfolioExposureReport",
    "SectorExposureReport",
    "ThemeExposureReport",
    "CorrelationRiskReport",
    "ConcentrationLimit",
    "DiversificationScore",
    "RotationCandidate",
    "KeepOrReplaceDecision",
    "PortfolioRiskBudget",
    "PortfolioDashboard",
    "PortfolioRebalanceReport",
    "PortfolioHealthSummary",
]


def get_all_model_names() -> list:
    """Return list of all model names."""
    return list(_ALL_MODELS)
