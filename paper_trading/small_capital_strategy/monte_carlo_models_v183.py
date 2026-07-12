"""
paper_trading/small_capital_strategy/monte_carlo_models_v183.py
Data models for Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class MonteCarloInput:
    initial_capital: float = 300000.0
    trial_count: int = 1000
    random_seed: int = 42
    single_trade_risk_pct: float = 1.0
    max_positions: int = 4
    stop_loss_pct: float = 7.0
    take_profit_pct: float = 15.0
    win_rate_pct: float = 50.0
    avg_win_pct: float = 10.0
    avg_loss_pct: float = 7.0
    trade_count_per_trial: int = 100
    capital_floor_pct: float = 70.0
    max_drawdown_limit_pct: float = 20.0
    losing_streak_threshold: int = 5
    slippage_pct: float = 0.1
    transaction_cost_pct: float = 0.2
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    monte_carlo_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    no_broker: bool = True
    schema_version: str = "183"


@dataclass
class MonteCarloConfig:
    trial_count: int = 1000
    random_seed: int = 42
    enable_trade_shuffle: bool = True
    enable_bootstrap: bool = True
    enable_return_perturbation: bool = True
    enable_streak_randomization: bool = True
    enable_slippage_shock: bool = True
    enable_cost_shock: bool = True
    enable_stop_loss_gap_shock: bool = True
    enable_regime_transition: bool = True
    enable_theme_collapse: bool = True
    enable_mistake_injection: bool = True
    theme_collapse_probability: float = 0.05
    mistake_injection_probability: float = 0.08
    slippage_shock_multiplier: float = 2.0
    cost_shock_multiplier: float = 1.5
    stop_loss_gap_shock_pct: float = 3.0
    paper_only: bool = True
    research_only: bool = True
    monte_carlo_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "183"


@dataclass
class MonteCarloTrial:
    trial_id: int = 0
    seed_used: int = 0
    terminal_equity: float = 0.0
    terminal_return_pct: float = 0.0
    max_drawdown_pct: float = 0.0
    max_consecutive_losses: int = 0
    trade_count: int = 0
    win_count: int = 0
    loss_count: int = 0
    ruined: bool = False
    ruin_reason: str = ""
    paper_only: bool = True
    monte_carlo_only: bool = True
    schema_version: str = "183"


@dataclass
class MonteCarloResult:
    trial_count: int = 0
    survival_rate_pct: float = 0.0
    ruin_probability_pct: float = 0.0
    median_return_pct: float = 0.0
    average_return_pct: float = 0.0
    worst_5pct_return_pct: float = 0.0
    best_5pct_return_pct: float = 0.0
    median_max_drawdown_pct: float = 0.0
    average_max_drawdown_pct: float = 0.0
    worst_5pct_max_drawdown_pct: float = 0.0
    max_consecutive_loss_distribution: dict = field(default_factory=dict)
    risk_of_ruin_score: float = 0.0
    sequence_risk_score: float = 0.0
    tail_risk_score: float = 0.0
    robustness_probability_pct: float = 0.0
    cost_sensitivity_score: float = 0.0
    slippage_sensitivity_score: float = 0.0
    final_grade: str = "BLOCKED"
    trials: list = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    monte_carlo_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "183"


@dataclass
class BootstrapSample:
    sample_id: int = 0
    sample_size: int = 0
    resampled_return_pct: float = 0.0
    resampled_max_drawdown_pct: float = 0.0
    resampled_win_rate_pct: float = 0.0
    with_replacement: bool = True
    paper_only: bool = True
    monte_carlo_only: bool = True
    schema_version: str = "183"


@dataclass
class BootstrapResult:
    sample_count: int = 0
    mean_return_pct: float = 0.0
    std_return_pct: float = 0.0
    ci_lower_5pct: float = 0.0
    ci_upper_95pct: float = 0.0
    mean_max_drawdown_pct: float = 0.0
    worst_5pct_drawdown_pct: float = 0.0
    bootstrap_passed: bool = False
    samples: list = field(default_factory=list)
    paper_only: bool = True
    research_only: bool = True
    monte_carlo_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "183"


@dataclass
class RiskOfRuinInput:
    initial_capital: float = 300000.0
    capital_floor_pct: float = 70.0
    max_drawdown_limit_pct: float = 20.0
    losing_streak_threshold: int = 5
    single_trade_risk_pct: float = 1.0
    win_rate_pct: float = 50.0
    avg_win_pct: float = 10.0
    avg_loss_pct: float = 7.0
    paper_only: bool = True
    monte_carlo_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "183"


@dataclass
class RiskOfRuinResult:
    capital_floor_pct: float = 70.0
    max_drawdown_limit_pct: float = 20.0
    losing_streak_threshold: int = 5
    ruin_probability_pct: float = 0.0
    survival_probability_pct: float = 0.0
    expected_max_drawdown_pct: float = 0.0
    worst_5pct_drawdown_pct: float = 0.0
    median_terminal_equity: float = 0.0
    worst_5pct_terminal_equity: float = 0.0
    best_5pct_terminal_equity: float = 0.0
    risk_of_ruin_score: float = 0.0
    is_ruined: bool = False
    paper_only: bool = True
    research_only: bool = True
    monte_carlo_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "183"


@dataclass
class DrawdownDistribution:
    trial_count: int = 0
    min_drawdown_pct: float = 0.0
    max_drawdown_pct: float = 0.0
    median_drawdown_pct: float = 0.0
    mean_drawdown_pct: float = 0.0
    p5_drawdown_pct: float = 0.0
    p25_drawdown_pct: float = 0.0
    p75_drawdown_pct: float = 0.0
    p95_drawdown_pct: float = 0.0
    drawdown_exceeds_limit_pct: float = 0.0
    paper_only: bool = True
    monte_carlo_only: bool = True
    schema_version: str = "183"


@dataclass
class ReturnDistribution:
    trial_count: int = 0
    min_return_pct: float = 0.0
    max_return_pct: float = 0.0
    median_return_pct: float = 0.0
    mean_return_pct: float = 0.0
    p5_return_pct: float = 0.0
    p25_return_pct: float = 0.0
    p75_return_pct: float = 0.0
    p95_return_pct: float = 0.0
    positive_return_rate_pct: float = 0.0
    paper_only: bool = True
    monte_carlo_only: bool = True
    schema_version: str = "183"


@dataclass
class SequenceRiskReport:
    max_consecutive_losses_observed: int = 0
    mean_consecutive_losses: float = 0.0
    worst_5pct_consecutive_losses: float = 0.0
    streak_ruin_probability_pct: float = 0.0
    sequence_risk_score: float = 0.0
    losing_streak_threshold: int = 5
    exceeds_threshold_rate_pct: float = 0.0
    paper_only: bool = True
    monte_carlo_only: bool = True
    schema_version: str = "183"


@dataclass
class SlippageCostShock:
    base_slippage_pct: float = 0.1
    shocked_slippage_pct: float = 0.2
    base_cost_pct: float = 0.2
    shocked_cost_pct: float = 0.3
    slippage_shock_multiplier: float = 2.0
    cost_shock_multiplier: float = 1.5
    return_degradation_pct: float = 0.0
    drawdown_increase_pct: float = 0.0
    slippage_sensitivity_score: float = 0.0
    cost_sensitivity_score: float = 0.0
    still_viable: bool = True
    paper_only: bool = True
    monte_carlo_only: bool = True
    schema_version: str = "183"


@dataclass
class TailRiskReport:
    tail_5pct_return_pct: float = 0.0
    tail_1pct_return_pct: float = 0.0
    tail_5pct_drawdown_pct: float = 0.0
    tail_1pct_drawdown_pct: float = 0.0
    expected_shortfall_pct: float = 0.0
    tail_risk_score: float = 0.0
    tail_risk_grade: str = "BLOCKED"
    paper_only: bool = True
    monte_carlo_only: bool = True
    schema_version: str = "183"


@dataclass
class RobustnessProbability:
    robustness_probability_pct: float = 0.0
    survives_shuffled_order_pct: float = 0.0
    survives_bootstrap_pct: float = 0.0
    survives_slippage_shock_pct: float = 0.0
    survives_cost_shock_pct: float = 0.0
    survives_regime_transition_pct: float = 0.0
    survives_theme_collapse_pct: float = 0.0
    survives_mistake_injection_pct: float = 0.0
    robustness_grade: str = "BLOCKED"
    paper_only: bool = True
    research_only: bool = True
    monte_carlo_only: bool = True
    schema_version: str = "183"


@dataclass
class MonteCarloDashboard:
    version: str = "1.8.3"
    trial_count: int = 0
    survival_rate_pct: float = 0.0
    ruin_probability_pct: float = 0.0
    median_return_pct: float = 0.0
    average_return_pct: float = 0.0
    worst_5pct_return_pct: float = 0.0
    best_5pct_return_pct: float = 0.0
    median_max_drawdown_pct: float = 0.0
    average_max_drawdown_pct: float = 0.0
    worst_5pct_max_drawdown_pct: float = 0.0
    risk_of_ruin_score: float = 0.0
    sequence_risk_score: float = 0.0
    tail_risk_score: float = 0.0
    robustness_probability_pct: float = 0.0
    cost_sensitivity_score: float = 0.0
    slippage_sensitivity_score: float = 0.0
    final_grade: str = "BLOCKED"
    paper_only: bool = True
    research_only: bool = True
    monte_carlo_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True
    schema_version: str = "183"


@dataclass
class MonteCarloReport:
    version: str = "1.8.3"
    sections: list = field(default_factory=list)
    all_audits_pass: bool = False
    paper_only: bool = True
    research_only: bool = True
    monte_carlo_only: bool = True
    no_real_orders: bool = True
    schema_version: str = "183"


@dataclass
class MonteCarloHealthSummary:
    total: int = 0
    passed: int = 0
    failed: int = 0
    all_passed: bool = False
    status: str = "FAIL"
    checks: list = field(default_factory=list)
    paper_only: bool = True
    monte_carlo_only: bool = True
    schema_version: str = "183"


def get_all_model_names() -> list:
    """Return list of all model class names."""
    return [
        "MonteCarloInput", "MonteCarloConfig", "MonteCarloTrial", "MonteCarloResult",
        "BootstrapSample", "BootstrapResult", "RiskOfRuinInput", "RiskOfRuinResult",
        "DrawdownDistribution", "ReturnDistribution", "SequenceRiskReport", "SlippageCostShock",
        "TailRiskReport", "RobustnessProbability", "MonteCarloDashboard", "MonteCarloReport",
        "MonteCarloHealthSummary",
    ]
