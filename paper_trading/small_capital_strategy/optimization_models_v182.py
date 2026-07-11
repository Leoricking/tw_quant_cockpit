"""
paper_trading/small_capital_strategy/optimization_models_v182.py
Data models for Parameter Optimization & Walk-Forward Validation Lab v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class OptimizationInput:
    initial_capital: float = 300000.0
    single_trade_risk_pct: float = 1.0
    max_positions: int = 4
    stop_loss_pct: float = 7.0
    take_profit_pct: float = 15.0
    trailing_stop_pct: float = 8.0
    max_drawdown_limit_pct: float = 12.0
    theme_score_threshold: float = 65.0
    watchlist_score_threshold: float = 65.0
    abc_score_threshold: float = 65.0
    behavior_risk_limit: str = "PASS"
    risk_dashboard_limit: str = "PASS"
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    validation_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    no_broker: bool = True
    schema_version: str = "182"


@dataclass
class OptimizationConfig:
    optimization_mode: str = "GRID_SEARCH"
    walk_forward_type: str = "ROLLING"
    in_sample_periods: int = 6
    out_of_sample_periods: int = 3
    min_parameter_sets: int = 10
    max_overfitting_risk_score: float = 70.0
    min_walk_forward_pass_rate_pct: float = 60.0
    max_degradation_pct: float = 30.0
    paper_only: bool = True
    research_only: bool = True
    validation_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "182"


@dataclass
class ParameterGrid:
    initial_capital_values: list = field(default_factory=lambda: [300000.0, 500000.0, 1000000.0])
    single_trade_risk_pct_values: list = field(default_factory=lambda: [0.8, 1.0, 1.5])
    max_positions_values: list = field(default_factory=lambda: [3, 4, 5])
    stop_loss_pct_values: list = field(default_factory=lambda: [5.0, 7.0, 10.0])
    take_profit_pct_values: list = field(default_factory=lambda: [10.0, 15.0, 20.0, 30.0])
    trailing_stop_pct_values: list = field(default_factory=lambda: [5.0, 8.0, 12.0])
    max_drawdown_limit_pct_values: list = field(default_factory=lambda: [8.0, 12.0, 15.0, 20.0])
    theme_score_threshold_values: list = field(default_factory=lambda: [50.0, 65.0, 80.0])
    watchlist_score_threshold_values: list = field(default_factory=lambda: [50.0, 65.0, 80.0])
    abc_score_threshold_values: list = field(default_factory=lambda: [50.0, 65.0, 80.0])
    behavior_risk_limit_values: list = field(default_factory=lambda: ["PASS", "WATCH", "WARNING"])
    risk_dashboard_limit_values: list = field(default_factory=lambda: ["PASS", "WARNING"])
    paper_only: bool = True
    schema_version: str = "182"


@dataclass
class ParameterSet:
    parameter_set_id: str = ""
    initial_capital: float = 300000.0
    single_trade_risk_pct: float = 1.0
    max_positions: int = 4
    stop_loss_pct: float = 7.0
    take_profit_pct: float = 15.0
    trailing_stop_pct: float = 8.0
    max_drawdown_limit_pct: float = 12.0
    theme_score_threshold: float = 65.0
    watchlist_score_threshold: float = 65.0
    abc_score_threshold: float = 65.0
    behavior_risk_limit: str = "PASS"
    risk_dashboard_limit: str = "PASS"
    in_sample_return_pct: float = 0.0
    out_of_sample_return_pct: float = 0.0
    max_drawdown_pct: float = 0.0
    win_rate_pct: float = 0.0
    profit_factor: float = 0.0
    expectancy_r: float = 0.0
    is_blocked: bool = False
    block_reason: str = ""
    paper_only: bool = True
    research_only: bool = True
    validation_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "182"


@dataclass
class ParameterSearchResult:
    total_parameter_sets: int = 0
    valid_parameter_sets: int = 0
    blocked_parameter_sets: int = 0
    best_in_sample_return_pct: float = 0.0
    best_out_of_sample_return_pct: float = 0.0
    average_out_of_sample_return_pct: float = 0.0
    best_parameter_set_id: str = ""
    parameter_sets: list = field(default_factory=list)
    search_mode: str = "GRID_SEARCH"
    paper_only: bool = True
    research_only: bool = True
    validation_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "182"


@dataclass
class ParameterRanking:
    rank: int = 0
    parameter_set_id: str = ""
    composite_score: float = 0.0
    out_of_sample_return_pct: float = 0.0
    stability_score: float = 0.0
    robustness_score: float = 0.0
    overfitting_risk_score: float = 0.0
    final_grade: str = "BLOCKED"
    paper_only: bool = True
    validation_only: bool = True
    schema_version: str = "182"


@dataclass
class WalkForwardWindow:
    window_id: str = ""
    window_type: str = "ROLLING"
    in_sample_start: int = 0
    in_sample_end: int = 0
    out_of_sample_start: int = 0
    out_of_sample_end: int = 0
    market_regime: str = "BULL"
    in_sample_return_pct: float = 0.0
    out_of_sample_return_pct: float = 0.0
    passed: bool = False
    paper_only: bool = True
    schema_version: str = "182"


@dataclass
class WalkForwardConfig:
    walk_forward_type: str = "ROLLING"
    num_windows: int = 5
    in_sample_size: int = 6
    out_of_sample_size: int = 3
    min_pass_rate_pct: float = 60.0
    paper_only: bool = True
    validation_only: bool = True
    schema_version: str = "182"


@dataclass
class WalkForwardResult:
    walk_forward_type: str = "ROLLING"
    total_windows: int = 0
    passed_windows: int = 0
    failed_windows: int = 0
    pass_rate_pct: float = 0.0
    average_out_of_sample_return_pct: float = 0.0
    worst_out_of_sample_return_pct: float = 0.0
    degradation_pct: float = 0.0
    walk_forward_passed: bool = False
    windows: list = field(default_factory=list)
    paper_only: bool = True
    validation_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "182"


@dataclass
class RobustParameterSet:
    parameter_set_id: str = ""
    stability_score: float = 0.0
    robustness_score: float = 0.0
    overfitting_risk_score: float = 0.0
    walk_forward_pass_rate_pct: float = 0.0
    degradation_pct: float = 0.0
    final_grade: str = "BLOCKED"
    works_in_bull: bool = False
    works_in_bear: bool = False
    works_in_range: bool = False
    works_in_risk_off: bool = False
    is_robust: bool = False
    paper_only: bool = True
    validation_only: bool = True
    schema_version: str = "182"


@dataclass
class OverfittingRiskReport:
    overfitting_risk_score: float = 0.0
    in_sample_return_pct: float = 0.0
    out_of_sample_return_pct: float = 0.0
    degradation_pct: float = 0.0
    parameter_count_used: int = 0
    overfitting_detected: bool = False
    overfitting_risk_level: str = "LOW"
    recommendations: list = field(default_factory=list)
    paper_only: bool = True
    validation_only: bool = True
    schema_version: str = "182"


@dataclass
class StabilityScore:
    score: float = 0.0
    regime_consistency: float = 0.0
    parameter_sensitivity: float = 0.0
    walk_forward_consistency: float = 0.0
    drawdown_consistency: float = 0.0
    is_stable: bool = False
    stability_grade: str = "UNSTABLE"
    paper_only: bool = True
    schema_version: str = "182"


@dataclass
class ParameterSensitivityReport:
    most_sensitive_parameter: str = ""
    least_sensitive_parameter: str = ""
    sensitivity_scores: dict = field(default_factory=dict)
    high_sensitivity_parameters: list = field(default_factory=list)
    low_sensitivity_parameters: list = field(default_factory=list)
    overall_sensitivity: float = 0.0
    paper_only: bool = True
    validation_only: bool = True
    schema_version: str = "182"


@dataclass
class OptimizationDashboard:
    version: str = "1.8.2"
    parameter_count: int = 0
    valid_parameter_count: int = 0
    blocked_parameter_count: int = 0
    best_in_sample_return_pct: float = 0.0
    best_out_of_sample_return_pct: float = 0.0
    average_out_of_sample_return_pct: float = 0.0
    max_drawdown_pct: float = 0.0
    worst_drawdown_pct: float = 0.0
    win_rate_pct: float = 0.0
    profit_factor: float = 0.0
    expectancy_r: float = 0.0
    stability_score: float = 0.0
    robustness_score: float = 0.0
    overfitting_risk_score: float = 0.0
    degradation_pct: float = 0.0
    walk_forward_pass_rate_pct: float = 0.0
    final_grade: str = "BLOCKED"
    paper_only: bool = True
    research_only: bool = True
    validation_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "182"


@dataclass
class OptimizationReport:
    version: str = "1.8.2"
    sections: list = field(default_factory=list)
    all_audits_pass: bool = False
    paper_only: bool = True
    research_only: bool = True
    validation_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "182"


@dataclass
class OptimizationHealthSummary:
    total: int = 0
    passed: int = 0
    failed: int = 0
    all_passed: bool = False
    status: str = "FAIL"
    checks: list = field(default_factory=list)
    paper_only: bool = True
    schema_version: str = "182"


def get_all_model_names() -> list:
    """Return list of all model class names."""
    return [
        "OptimizationInput", "OptimizationConfig", "ParameterGrid", "ParameterSet",
        "ParameterSearchResult", "ParameterRanking", "WalkForwardWindow", "WalkForwardConfig",
        "WalkForwardResult", "RobustParameterSet", "OverfittingRiskReport", "StabilityScore",
        "ParameterSensitivityReport", "OptimizationDashboard", "OptimizationReport",
        "OptimizationHealthSummary",
    ]
