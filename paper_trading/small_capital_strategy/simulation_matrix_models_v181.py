"""
paper_trading/small_capital_strategy/simulation_matrix_models_v181.py
Dataclass models for Simulation Scenario Matrix & Stress Test Lab v1.8.1.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

_SCHEMA = "181"

_SAFETY = dict(
    paper_only=True, research_only=True, simulate_only=True,
    no_real_orders=True, no_broker=True, not_investment_advice=True,
    stress_test_only=True,
)


@dataclass
class SimulationMatrixInput:
    """Single-cell input for a scenario matrix run."""
    initial_capital: float = 300000.0
    single_trade_risk_pct: float = 1.0
    max_positions: int = 4
    market_regime: str = "BULL"
    theme_rank: str = "LEADER"
    watchlist_rank: str = "CORE"
    abc_signal: str = "A"
    behavior_risk: str = "PASS"
    risk_dashboard: str = "PASS"
    mistake_injection: str = "NONE"
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class SimulationMatrixConfig:
    """Full configuration defining all axes of the scenario matrix."""
    initial_capitals: List[float] = field(default_factory=lambda: [300000.0, 500000.0, 1000000.0])
    risk_pcts: List[float] = field(default_factory=lambda: [0.8, 1.0, 1.5])
    max_positions_list: List[int] = field(default_factory=lambda: [3, 4, 5])
    market_regimes: List[str] = field(default_factory=lambda: ["BULL", "RANGE", "BEAR", "RISK_OFF", "UNKNOWN"])
    theme_ranks: List[str] = field(default_factory=lambda: ["LEADER", "STRONG", "WATCH", "WEAK", "EXCLUDED"])
    watchlist_ranks: List[str] = field(default_factory=lambda: ["CORE", "MAIN_THEME_SWING", "SECOND_WAVE", "TRAINING", "EXCLUDED"])
    abc_signals: List[str] = field(default_factory=lambda: ["A", "B", "C", "BLOCKED", "NOT_READY"])
    behavior_risks: List[str] = field(default_factory=lambda: ["PASS", "WATCH", "WARNING", "BLOCKED"])
    risk_dashboards: List[str] = field(default_factory=lambda: ["PASS", "WARNING", "BLOCKED"])
    mistake_injections: List[str] = field(default_factory=lambda: [
        "NONE", "NO_STOP_LOSS", "OVERSIZED_POSITION", "OVERTRADING", "REVENGE_TRADE", "MOVED_STOP_LOSS"
    ])
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class SimulationMatrixAxis:
    """Definition of one matrix axis / dimension."""
    name: str = ""
    values: List[Any] = field(default_factory=list)
    description: str = ""
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class SimulationMatrixCell:
    """Result for a single cell in the scenario matrix."""
    cell_id: str = ""
    input_params: Dict[str, Any] = field(default_factory=dict)
    action: str = "WAIT"
    is_blocked: bool = False
    total_return_pct: float = 0.0
    max_drawdown_pct: float = 0.0
    win_rate_pct: float = 0.0
    expectancy_r: float = 0.0
    final_grade: str = "D"
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class SimulationMatrixResult:
    """Aggregated result across all scenario matrix cells."""
    scenario_count: int = 0
    pass_count: int = 0
    blocked_count: int = 0
    average_return_pct: float = 0.0
    median_return_pct: float = 0.0
    worst_case_return_pct: float = 0.0
    best_case_return_pct: float = 0.0
    average_max_drawdown_pct: float = 0.0
    worst_max_drawdown_pct: float = 0.0
    average_win_rate_pct: float = 0.0
    average_profit_factor: float = 0.0
    average_expectancy_r: float = 0.0
    risk_of_ruin_score: float = 0.0
    robustness_score: float = 0.0
    stress_survival_rate_pct: float = 0.0
    blocked_reason_distribution: Dict[str, int] = field(default_factory=dict)
    final_grade: str = "FRAGILE"
    cells: List[SimulationMatrixCell] = field(default_factory=list)
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StressTestScenario:
    """Definition of one stress test scenario."""
    scenario_id: str = ""
    name: str = ""
    shock_type: str = ""
    severity: str = "MEDIUM"
    description: str = ""
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    stress_test_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StressTestResult:
    """Result of a single stress test run."""
    scenario_id: str = ""
    shock_type: str = ""
    survived: bool = True
    total_return_pct: float = 0.0
    max_drawdown_pct: float = 0.0
    final_capital: float = 300000.0
    action: str = "BLOCKED"
    notes: str = ""
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    stress_test_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StressDrawdownShock:
    """A sudden drawdown shock event applied to the portfolio."""
    shock_id: str = ""
    drawdown_pct: float = 20.0
    duration_days: int = 5
    recovery_pct: float = 10.0
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    stress_test_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StressLosingStreakShock:
    """A consecutive losing streak shock injection."""
    streak_length: int = 3
    loss_per_trade_pct: float = 1.0
    total_loss_pct: float = 0.0
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    stress_test_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True

    def __post_init__(self) -> None:
        if self.total_loss_pct == 0.0:
            self.total_loss_pct = round(self.streak_length * self.loss_per_trade_pct, 4)


@dataclass
class StressRegimeShiftShock:
    """A sudden market regime shift shock."""
    from_regime: str = "BULL"
    to_regime: str = "RISK_OFF"
    shift_day: int = 10
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    stress_test_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StressThemeCollapseShock:
    """A theme collapse shock (theme rank drops to EXCLUDED)."""
    from_theme: str = "LEADER"
    to_theme: str = "EXCLUDED"
    collapse_day: int = 5
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    stress_test_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class StressMistakeInjection:
    """An injected behavioral mistake into the simulation."""
    mistake_type: str = "NONE"
    injection_day: int = 1
    frequency: int = 1
    severity: str = "HIGH"
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    stress_test_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class RobustnessScore:
    """Overall robustness evaluation across all matrix cells and stress tests."""
    score: float = 0.0
    stress_survival_rate_pct: float = 0.0
    scenario_pass_rate_pct: float = 0.0
    average_max_drawdown_pct: float = 0.0
    worst_case_return_pct: float = 0.0
    behavior_resilience_score: float = 0.0
    final_grade: str = "FRAGILE"
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    stress_test_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ScenarioMatrixDashboard:
    """Top-level dashboard aggregating matrix and stress test results."""
    version: str = "1.8.1"
    total_scenarios: int = 0
    pass_count: int = 0
    blocked_count: int = 0
    stress_tests_run: int = 0
    stress_survived: int = 0
    robustness_score: float = 0.0
    final_grade: str = "FRAGILE"
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    stress_test_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ScenarioMatrixReport:
    """Full report from scenario matrix and stress test run."""
    version: str = "1.8.1"
    scenario_count: int = 0
    stress_test_count: int = 0
    robustness_score: float = 0.0
    final_grade: str = "FRAGILE"
    sections: List[str] = field(default_factory=list)
    schema_version: str = _SCHEMA
    paper_only: bool = True
    research_only: bool = True
    simulate_only: bool = True
    stress_test_only: bool = True
    no_real_orders: bool = True
    not_investment_advice: bool = True


@dataclass
class ScenarioMatrixHealthSummary:
    """Health check summary for Simulation Scenario Matrix v1.8.1."""
    status: str = "PASS"
    passed: int = 0
    failed: int = 0
    total: int = 0
    all_passed: bool = True
    checks: List[Dict[str, Any]] = field(default_factory=list)
    schema_version: str = _SCHEMA
    paper_only: bool = True
    not_investment_advice: bool = True
    no_real_orders: bool = True


def get_all_model_names() -> List[str]:
    """Return list of all 16 model class names in this module."""
    return [
        "SimulationMatrixInput",
        "SimulationMatrixConfig",
        "SimulationMatrixAxis",
        "SimulationMatrixCell",
        "SimulationMatrixResult",
        "StressTestScenario",
        "StressTestResult",
        "StressDrawdownShock",
        "StressLosingStreakShock",
        "StressRegimeShiftShock",
        "StressThemeCollapseShock",
        "StressMistakeInjection",
        "RobustnessScore",
        "ScenarioMatrixDashboard",
        "ScenarioMatrixReport",
        "ScenarioMatrixHealthSummary",
    ]
