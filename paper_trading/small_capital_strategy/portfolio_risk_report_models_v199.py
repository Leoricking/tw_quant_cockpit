"""
paper_trading/small_capital_strategy/portfolio_risk_report_models_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Models
[!] Paper Only. Research Only. Position Sizing Policy Only. Portfolio Risk Report Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class PaperPortfolioRiskReportInput:
    schema_version: str = "199"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    portfolio_risk_report_only: bool = True
    position_sizing_policy_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    capital_base: float = 300_000.0
    portfolio_risk_score: float = 0.0
    portfolio_risk_grade: str = "LOW"
    current_cash_pct: float = 1.0
    entry_type: str = "A_PULLBACK_10MA"
    stop_distance_pct: float = 0.05
    theme_exposures: Dict[str, float] = field(default_factory=dict)
    industry_exposures: Dict[str, float] = field(default_factory=dict)
    symbol_weights: Dict[str, float] = field(default_factory=dict)
    high_correlation_cluster_weight: float = 0.0
    market_risk_off: bool = False
    existing_positions_count: int = 0
    candidate_symbol: str = ""
    candidate_theme: str = ""
    candidate_industry: str = ""


@dataclass
class PaperPortfolioRiskReportResult:
    schema_version: str = "199"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    portfolio_risk_report_only: bool = True
    position_sizing_policy_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    no_margin: bool = True
    no_leverage: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    allowed: bool = False
    recommendation: str = "BLOCK_NEW_ENTRY"
    paper_action: str = "PAPER_BLOCK_NEW_ENTRY"
    position_size_shares: int = 0
    position_size_amount: float = 0.0
    position_size_pct: float = 0.0
    max_loss_amount: float = 0.0
    risk_grade: str = "LOW"
    block_reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    sizing_executes_order: bool = False
    sizing_mutates_strategy: bool = False
    sizing_rebalances_real_portfolio: bool = False


@dataclass
class PaperCapitalProfile:
    schema_version: str = "199"
    paper_only: bool = True
    capital_base: float = 300_000.0
    normal_single_trade_risk_pct_min: float = 0.008
    normal_single_trade_risk_pct_max: float = 0.015
    normal_single_trade_loss_min: float = 2_400.0
    normal_single_trade_loss_max: float = 4_500.0
    aggressive_single_trade_risk_pct_max: float = 0.02
    risk_off_single_trade_risk_pct_max: float = 0.005
    min_cash_buffer_pct: float = 0.05
    weak_market_cash_buffer_pct: float = 0.50
    max_single_symbol_weight: float = 0.20
    max_single_theme_weight: float = 0.35
    max_single_industry_weight: float = 0.40
    max_high_correlation_cluster_weight: float = 0.45
    not_investment_advice: bool = True
    production_trading_blocked: bool = True


@dataclass
class PaperRiskBudget:
    schema_version: str = "199"
    paper_only: bool = True
    capital_base: float = 300_000.0
    total_risk_budget: float = 0.0
    used_risk_budget: float = 0.0
    remaining_risk_budget: float = 0.0
    risk_budget_pct_used: float = 0.0
    max_portfolio_risk_pct: float = 0.20
    current_portfolio_risk_pct: float = 0.0
    risk_budget_exceeded: bool = False
    not_investment_advice: bool = True
    production_trading_blocked: bool = True


@dataclass
class PaperTradeRiskBudget:
    schema_version: str = "199"
    paper_only: bool = True
    capital_base: float = 300_000.0
    entry_type: str = "A_PULLBACK_10MA"
    risk_pct: float = 0.01
    max_loss_amount: float = 0.0
    position_size_amount: float = 0.0
    stop_distance_pct: float = 0.05
    size_multiplier: float = 1.0
    risk_off_mode: bool = False
    blocked: bool = False
    block_reason: str = ""
    not_investment_advice: bool = True
    production_trading_blocked: bool = True


@dataclass
class PaperPositionSizingPolicy:
    schema_version: str = "199"
    paper_only: bool = True
    policy_name: str = "fixed_fractional_risk"
    enabled: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    sizing_executes_order: bool = False


@dataclass
class PaperPositionSizingResult:
    schema_version: str = "199"
    paper_only: bool = True
    entry_type: str = "A_PULLBACK_10MA"
    capital_base: float = 300_000.0
    risk_pct: float = 0.01
    stop_distance_pct: float = 0.05
    size_multiplier: float = 1.0
    raw_position_amount: float = 0.0
    adjusted_position_amount: float = 0.0
    position_pct_of_capital: float = 0.0
    max_loss_amount: float = 0.0
    policy_applied: str = "fixed_fractional_risk"
    blocked: bool = False
    block_reason: str = ""
    warnings: List[str] = field(default_factory=list)
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    sizing_executes_order: bool = False
    sizing_mutates_strategy: bool = False


@dataclass
class PaperEntryType:
    schema_version: str = "199"
    paper_only: bool = True
    entry_type: str = "A_PULLBACK_10MA"
    size_multiplier: float = 1.0
    description: str = ""
    requirements: List[str] = field(default_factory=list)
    invalidation_conditions: List[str] = field(default_factory=list)
    not_investment_advice: bool = True
    production_trading_blocked: bool = True


@dataclass
class PaperEntrySizingRule:
    schema_version: str = "199"
    paper_only: bool = True
    entry_type: str = "A_PULLBACK_10MA"
    size_multiplier: float = 1.0
    min_risk_pct: float = 0.008
    max_risk_pct: float = 0.015
    requires_gain_buffer: bool = False
    allow_add_position: bool = False
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    sizing_executes_order: bool = False


@dataclass
class PaperStopDistanceRule:
    schema_version: str = "199"
    paper_only: bool = True
    stop_distance_pct: float = 0.05
    size_adjustment_factor: float = 1.0
    blocked: bool = False
    block_reason: str = ""
    description: str = ""
    not_investment_advice: bool = True
    production_trading_blocked: bool = True


@dataclass
class PaperCashBufferPolicy:
    schema_version: str = "199"
    paper_only: bool = True
    min_cash_buffer_pct: float = 0.05
    weak_market_cash_buffer_pct: float = 0.50
    current_cash_pct: float = 1.0
    cash_buffer_ok: bool = True
    weak_market_mode: bool = False
    block_new_entry: bool = False
    not_investment_advice: bool = True
    production_trading_blocked: bool = True


@dataclass
class PaperExposureLimitPolicy:
    schema_version: str = "199"
    paper_only: bool = True
    max_single_symbol_weight: float = 0.20
    max_single_theme_weight: float = 0.35
    max_single_industry_weight: float = 0.40
    max_high_correlation_cluster_weight: float = 0.45
    symbol_limit_exceeded: bool = False
    theme_limit_exceeded: bool = False
    industry_limit_exceeded: bool = False
    correlation_limit_exceeded: bool = False
    not_investment_advice: bool = True
    production_trading_blocked: bool = True


@dataclass
class PaperThemeSizingLimit:
    schema_version: str = "199"
    paper_only: bool = True
    theme_name: str = ""
    current_weight: float = 0.0
    max_weight: float = 0.35
    limit_exceeded: bool = False
    block_new_entry: bool = False
    reduce_size: bool = False
    not_investment_advice: bool = True
    production_trading_blocked: bool = True


@dataclass
class PaperIndustrySizingLimit:
    schema_version: str = "199"
    paper_only: bool = True
    industry_name: str = ""
    current_weight: float = 0.0
    max_weight: float = 0.40
    limit_exceeded: bool = False
    block_new_entry: bool = False
    reduce_size: bool = False
    not_investment_advice: bool = True
    production_trading_blocked: bool = True


@dataclass
class PaperStrategySizingLimit:
    schema_version: str = "199"
    paper_only: bool = True
    strategy_name: str = ""
    current_weight: float = 0.0
    max_weight: float = 0.50
    limit_exceeded: bool = False
    block_new_entry: bool = False
    not_investment_advice: bool = True
    production_trading_blocked: bool = True


@dataclass
class PaperRiskOffSizingPolicy:
    schema_version: str = "199"
    paper_only: bool = True
    risk_off_active: bool = False
    risk_off_position_cut_pct: float = 0.50
    risk_off_max_risk_pct: float = 0.005
    risk_off_cash_buffer_pct: float = 0.50
    block_new_entry_without_edge: bool = True
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    sizing_executes_order: bool = False


@dataclass
class PaperNoEntryCondition:
    schema_version: str = "199"
    paper_only: bool = True
    condition_name: str = ""
    triggered: bool = False
    reason: str = ""
    paper_action: str = "PAPER_BLOCK_NEW_ENTRY"
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    executes_real_order: bool = False


@dataclass
class PaperAddPositionRule:
    schema_version: str = "199"
    paper_only: bool = True
    allowed: bool = False
    requires_unrealized_gain: bool = True
    block_if_portfolio_risk_exceeded: bool = True
    block_if_cash_buffer_below_min: bool = True
    block_reason: str = ""
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    executes_real_order: bool = False


@dataclass
class PaperReducePositionRule:
    schema_version: str = "199"
    paper_only: bool = True
    triggered: bool = False
    reason: str = ""
    reduce_by_pct: float = 0.0
    paper_action: str = "PAPER_ALLOW_REDUCED_SIZE"
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    executes_real_order: bool = False


@dataclass
class PaperPositionSizingAuditTrail:
    schema_version: str = "199"
    paper_only: bool = True
    audit_id: str = ""
    entry_type: str = ""
    capital_base: float = 0.0
    risk_pct: float = 0.0
    stop_distance_pct: float = 0.0
    size_multiplier: float = 0.0
    position_amount: float = 0.0
    max_loss_amount: float = 0.0
    policy_applied: str = ""
    recommendation: str = ""
    paper_action: str = ""
    blocked: bool = False
    block_reasons: List[str] = field(default_factory=list)
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    sizing_executes_order: bool = False
    sizing_mutates_strategy: bool = False


@dataclass
class PaperRiskReportDashboard:
    schema_version: str = "199"
    paper_only: bool = True
    dashboard_only: bool = True
    report_only: bool = True
    portfolio_risk_grade: str = "LOW"
    portfolio_risk_score: float = 0.0
    cash_pct: float = 1.0
    cash_buffer_ok: bool = True
    theme_limits_ok: bool = True
    industry_limits_ok: bool = True
    symbol_limits_ok: bool = True
    correlation_ok: bool = True
    risk_off_active: bool = False
    recommendation: str = "NO_CHANGE"
    paper_action: str = "PAPER_KEEP_CASH"
    panels_count: int = 12
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    dashboard_mutates_strategy: bool = False
    dashboard_places_real_order: bool = False


@dataclass
class PaperRiskReportExport:
    schema_version: str = "199"
    paper_only: bool = True
    export_format: str = "json"
    export_path: str = ""
    export_safe: bool = True
    blocked: bool = False
    block_reason: str = ""
    sections: List[str] = field(default_factory=list)
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    export_triggers_real_order: bool = False
    export_mutates_production: bool = False


@dataclass
class PaperRiskReportHealthSummary:
    schema_version: str = "199"
    paper_only: bool = True
    all_passed: bool = False
    status: str = "UNKNOWN"
    passed: int = 0
    failed: int = 0
    total: int = 0
    checks: List[Dict[str, Any]] = field(default_factory=list)
    not_investment_advice: bool = True
    production_trading_blocked: bool = True


@dataclass
class PaperRiskReportValidationResult:
    schema_version: str = "199"
    paper_only: bool = True
    valid: bool = False
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    checked_fields: List[str] = field(default_factory=list)
    not_investment_advice: bool = True
    production_trading_blocked: bool = True


@dataclass
class PaperRiskReportRecommendation:
    schema_version: str = "199"
    paper_only: bool = True
    recommendation: str = "NO_CHANGE"
    paper_action: str = "PAPER_KEEP_CASH"
    rationale: str = ""
    priority: int = 0
    applies_to_entry_types: List[str] = field(default_factory=list)
    not_investment_advice: bool = True
    production_trading_blocked: bool = True
    recommendation_executes_order: bool = False
    recommendation_mutates_strategy: bool = False


_ALL_MODEL_NAMES = [
    "PaperPortfolioRiskReportInput",
    "PaperPortfolioRiskReportResult",
    "PaperCapitalProfile",
    "PaperRiskBudget",
    "PaperTradeRiskBudget",
    "PaperPositionSizingPolicy",
    "PaperPositionSizingResult",
    "PaperEntryType",
    "PaperEntrySizingRule",
    "PaperStopDistanceRule",
    "PaperCashBufferPolicy",
    "PaperExposureLimitPolicy",
    "PaperThemeSizingLimit",
    "PaperIndustrySizingLimit",
    "PaperStrategySizingLimit",
    "PaperRiskOffSizingPolicy",
    "PaperNoEntryCondition",
    "PaperAddPositionRule",
    "PaperReducePositionRule",
    "PaperPositionSizingAuditTrail",
    "PaperRiskReportDashboard",
    "PaperRiskReportExport",
    "PaperRiskReportHealthSummary",
    "PaperRiskReportValidationResult",
    "PaperRiskReportRecommendation",
]
assert len(_ALL_MODEL_NAMES) == 25, f"Expected 25 models, got {len(_ALL_MODEL_NAMES)}"
