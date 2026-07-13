"""
paper_trading/small_capital_strategy/decision_cockpit_models_v186.py
Data models for End-to-End Small Capital Decision Cockpit v1.8.6.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Decision Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class DecisionCockpitInput:
    capital: float = 300000.0
    capital_stage: str = "300K"
    market_regime: str = "BULL"
    decision_cycle: str = "daily_check"
    date_label: str = ""
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    portfolio_holding_count: int = 0
    monte_carlo_ruin_risk_pct: float = 0.0
    max_drawdown_budget_pct: float = 20.0
    drawdown_used_pct: float = 0.0
    concentration_risk_score: float = 0.0
    behavior_risk_blocked: bool = False
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "186"


@dataclass
class DecisionCockpitResult:
    cockpit_version: str = "1.8.6"
    release_name: str = "End-to-End Small Capital Decision Cockpit"
    capital_stage: str = "300K"
    market_regime: str = "BULL"
    daily_action: str = "DECISION_ONLY"
    weekly_action: str = "DECISION_ONLY"
    candidate_count: int = 0
    ready_candidate_count: int = 0
    watch_candidate_count: int = 0
    blocked_candidate_count: int = 0
    portfolio_holding_count: int = 0
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    theme_exposure_summary: Dict[str, float] = field(default_factory=dict)
    sector_exposure_summary: Dict[str, float] = field(default_factory=dict)
    concentration_risk_score: float = 0.0
    diversification_score: float = 100.0
    monte_carlo_ruin_risk: float = 0.0
    max_drawdown_budget_usage_pct: float = 0.0
    position_sizing_summary: str = ""
    portfolio_rebalance_summary: str = ""
    top_watch_candidates: List[str] = field(default_factory=list)
    paper_plan_ready_candidates: List[str] = field(default_factory=list)
    reduce_risk_candidates: List[str] = field(default_factory=list)
    blocked_candidates: List[str] = field(default_factory=list)
    block_reasons: List[str] = field(default_factory=list)
    final_cockpit_grade: str = "WAIT"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "186"


@dataclass
class DailyDecisionContext:
    date_label: str = ""
    market_open: bool = True
    pre_market_checked: bool = False
    watchlist_reviewed: bool = False
    candidate_count: int = 0
    daily_action: str = "DECISION_ONLY"
    notes: str = ""
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class WeeklyDecisionContext:
    week_label: str = ""
    portfolio_reviewed: bool = False
    risk_reviewed: bool = False
    regime_reviewed: bool = False
    weekly_action: str = "DECISION_ONLY"
    reduce_exposure_required: bool = False
    rebalance_required: bool = False
    notes: str = ""
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class MarketDecisionState:
    market_regime: str = "BULL"
    regime_blocked: bool = False
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    drawdown_used_pct: float = 0.0
    max_drawdown_budget_pct: float = 20.0
    entry_allowed: bool = True
    add_allowed: bool = True
    action: str = "DECISION_ONLY"
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class CandidateDecisionInput:
    ticker: str = ""
    name: str = ""
    sector: str = ""
    theme: str = ""
    theme_strength: str = "NEUTRAL"
    revenue_growth_pct: float = 0.0
    above_10ma: bool = True
    above_20ma: bool = True
    volume_breakout: bool = False
    volume_contracting: bool = True
    kd_below_50: bool = False
    kd_recovering: bool = False
    rsi: float = 50.0
    macd_positive: bool = False
    institutional_flow_positive: bool = True
    institutional_consecutive_negative_days: int = 0
    margin_balance_risk: float = 0.0
    big_holder_crowding: bool = False
    abc_buy_point: str = "A_10MA_PULLBACK"
    market_regime: str = "BULL"
    stop_loss_distance_pct: float = 7.0
    stop_loss_defined: bool = True
    liquidity_ok: bool = True
    position_sizing_pct: float = 10.0
    portfolio_concentration_ok: bool = True
    monte_carlo_ruin_risk_pct: float = 0.0
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class CandidateDecisionResult:
    ticker: str = ""
    theme_strength_ok: bool = True
    revenue_growth_ok: bool = True
    ma_structure_ok: bool = True
    volume_ok: bool = True
    oscillator_ok: bool = True
    institutional_flow_ok: bool = True
    margin_risk_ok: bool = True
    crowding_risk_ok: bool = True
    abc_buy_point_ok: bool = False
    regime_ok: bool = True
    position_sizing_ok: bool = True
    concentration_ok: bool = True
    monte_carlo_ok: bool = True
    final_action: str = "WAIT"
    block_reasons: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class BuyPointDecision:
    ticker: str = ""
    buy_point_type: str = "A_10MA_PULLBACK"
    condition_met: bool = False
    action: str = "WAIT"
    block_reasons: List[str] = field(default_factory=list)
    notes: str = ""
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class RiskDecision:
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    monte_carlo_ruin_risk_pct: float = 0.0
    drawdown_budget_usage_pct: float = 0.0
    stop_loss_coverage_ok: bool = True
    exposure_ok: bool = True
    cash_ok: bool = True
    ruin_risk_ok: bool = True
    drawdown_ok: bool = True
    action: str = "DECISION_ONLY"
    block_reasons: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class PositionSizingDecision:
    ticker: str = ""
    capital: float = 300000.0
    suggested_position_pct: float = 10.0
    suggested_position_amount: float = 30000.0
    position_ok: bool = True
    action: str = "DECISION_ONLY"
    block_reasons: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class PortfolioDecision:
    holding_count: int = 0
    total_exposure_pct: float = 0.0
    cash_reserve_pct: float = 100.0
    concentration_risk_score: float = 0.0
    diversification_score: float = 100.0
    overexposed_sectors: List[str] = field(default_factory=list)
    overexposed_themes: List[str] = field(default_factory=list)
    rebalance_needed: bool = False
    portfolio_ok: bool = True
    action: str = "DECISION_ONLY"
    block_reasons: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class MonteCarloDecision:
    ruin_probability_pct: float = 0.0
    ruin_risk_level: str = "LOW"
    entry_allowed: bool = True
    add_allowed: bool = True
    action: str = "DECISION_ONLY"
    block_reasons: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class ThemeDecision:
    top_themes: List[str] = field(default_factory=list)
    weak_themes: List[str] = field(default_factory=list)
    overcrowded_themes: List[str] = field(default_factory=list)
    theme_rotation_active: bool = False
    action: str = "DECISION_ONLY"
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class RegimeDecision:
    market_regime: str = "BULL"
    regime_blocked: bool = False
    entry_permitted: bool = True
    add_permitted: bool = True
    max_exposure_pct: float = 60.0
    action: str = "DECISION_ONLY"
    block_reasons: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class EntryReadinessScore:
    score: float = 0.0
    max_score: float = 100.0
    regime_ok: bool = False
    candidate_ready: bool = False
    risk_ok: bool = False
    portfolio_ok: bool = False
    mc_ok: bool = False
    action: str = "WAIT"
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class AddReadinessScore:
    score: float = 0.0
    max_score: float = 100.0
    regime_ok: bool = False
    cash_reserve_ok: bool = False
    ruin_risk_ok: bool = False
    concentration_ok: bool = False
    action: str = "WAIT"
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class ReduceRiskDecision:
    reduce_required: bool = False
    reduce_candidates: List[str] = field(default_factory=list)
    reason: str = ""
    target_exposure_pct: float = 60.0
    action: str = "OBSERVE"
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class BlockReason:
    code: str = ""
    description: str = ""
    severity: str = "HIGH"
    affected_tickers: List[str] = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class DecisionChecklist:
    market_regime_checked: bool = False
    watchlist_reviewed: bool = False
    candidates_evaluated: bool = False
    buy_points_assessed: bool = False
    risk_reviewed: bool = False
    position_sizing_checked: bool = False
    portfolio_checked: bool = False
    monte_carlo_checked: bool = False
    theme_checked: bool = False
    all_checked: bool = False
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


@dataclass
class DecisionDashboard:
    regime_decision: Optional[RegimeDecision] = None
    theme_decision: Optional[ThemeDecision] = None
    risk_decision: Optional[RiskDecision] = None
    portfolio_decision: Optional[PortfolioDecision] = None
    monte_carlo_decision: Optional[MonteCarloDecision] = None
    entry_readiness: Optional[EntryReadinessScore] = None
    add_readiness: Optional[AddReadinessScore] = None
    reduce_risk_decision: Optional[ReduceRiskDecision] = None
    checklist: Optional[DecisionChecklist] = None
    final_cockpit_grade: str = "WAIT"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    schema_version: str = "186"


@dataclass
class DecisionReport:
    version: str = "1.8.6"
    release_name: str = "End-to-End Small Capital Decision Cockpit"
    sections: List[str] = field(default_factory=list)
    cockpit_result: Optional[DecisionCockpitResult] = None
    all_checks_pass: bool = True
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    demo_only: bool = True
    not_for_production: bool = True
    production_trading_blocked: bool = True
    schema_version: str = "186"


@dataclass
class DecisionHealthSummary:
    total: int = 0
    passed: int = 0
    failed: int = 0
    all_passed: bool = False
    status: str = "FAIL"
    paper_only: bool = True
    research_only: bool = True
    decision_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "186"


_ALL_MODELS = [
    "DecisionCockpitInput",
    "DecisionCockpitResult",
    "DailyDecisionContext",
    "WeeklyDecisionContext",
    "MarketDecisionState",
    "CandidateDecisionInput",
    "CandidateDecisionResult",
    "BuyPointDecision",
    "RiskDecision",
    "PositionSizingDecision",
    "PortfolioDecision",
    "MonteCarloDecision",
    "ThemeDecision",
    "RegimeDecision",
    "EntryReadinessScore",
    "AddReadinessScore",
    "ReduceRiskDecision",
    "BlockReason",
    "DecisionChecklist",
    "DecisionDashboard",
    "DecisionReport",
    "DecisionHealthSummary",
]


def get_all_model_names() -> list:
    """Return list of all model names."""
    return list(_ALL_MODELS)
