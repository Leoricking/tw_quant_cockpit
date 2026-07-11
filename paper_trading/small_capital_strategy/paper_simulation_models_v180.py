"""
paper_trading/small_capital_strategy/paper_simulation_models_v180.py
Dataclass models for Paper Simulation & Performance Lab v1.8.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

_SCHEMA_VERSION = "180"


@dataclass
class PaperSimulationInput:
    """Input parameters for a single paper simulation run."""
    initial_capital: float = 300000.0
    risk_per_trade_pct: float = 1.0
    max_holdings: int = 4
    market_regime: str = "BULL"
    theme_rank: str = "LEADER"
    watchlist_rank: str = "CORE"
    abc_buy_point: str = "A"
    mistake_taxonomy_effect: str = "none"
    risk_dashboard_status: str = "PASS"
    integrated_decision: str = "PAPER_ENTRY_ALLOWED"
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperSimulationConfig:
    """Configuration for running multiple paper simulation scenarios."""
    initial_capital: float = 300000.0
    risk_per_trade_pcts: List[float] = field(default_factory=lambda: [0.8, 1.0, 1.5])
    max_holdings_options: List[int] = field(default_factory=lambda: [3, 4, 5])
    simulation_days: int = 252
    regime_weights: Dict[str, float] = field(default_factory=dict)
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperSimulationScenario:
    """A single scenario definition for paper simulation."""
    scenario_id: str = ""
    name: str = ""
    market_regime: str = "BULL"
    theme_rank: str = "LEADER"
    watchlist_rank: str = "CORE"
    abc_buy_point: str = "A"
    expected_action: str = "PAPER_ENTRY_ALLOWED"
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperSimulationTrade:
    """A single simulated paper trade record."""
    trade_id: str = ""
    symbol: str = ""
    entry_price: float = 0.0
    exit_price: float = 0.0
    stop_loss: float = 0.0
    position_size: float = 0.0
    pnl: float = 0.0
    pnl_pct: float = 0.0
    r_multiple: float = 0.0
    abc_type: str = "A"
    theme: str = ""
    regime: str = "BULL"
    mistake_type: str = "none"
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperSimulationPosition:
    """An open simulated paper position."""
    symbol: str = ""
    entry_price: float = 0.0
    current_price: float = 0.0
    stop_loss: float = 0.0
    position_size: float = 0.0
    unrealized_pnl: float = 0.0
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperSimulationPortfolio:
    """Portfolio state during a paper simulation run."""
    cash: float = 300000.0
    positions: List[PaperSimulationPosition] = field(default_factory=list)
    total_value: float = 300000.0
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperSimulationResult:
    """Result of a completed paper simulation run."""
    scenario_id: str = ""
    total_return_pct: float = 0.0
    final_capital: float = 300000.0
    trade_count: int = 0
    trades: List[PaperSimulationTrade] = field(default_factory=list)
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperPerformanceMetrics:
    """Computed performance metrics from a paper simulation run."""
    total_return_pct: float = 0.0
    annualized_return_pct: float = 0.0
    max_drawdown_pct: float = 0.0
    win_rate_pct: float = 0.0
    average_win_pct: float = 0.0
    average_loss_pct: float = 0.0
    profit_factor: float = 0.0
    expectancy_r: float = 0.0
    average_r: float = 0.0
    max_consecutive_losses: int = 0
    max_consecutive_wins: int = 0
    trade_count: int = 0
    exposure_pct: float = 0.0
    cash_drag_pct: float = 0.0
    turnover: float = 0.0
    risk_of_ruin_score: float = 0.0
    behavior_penalty_score: float = 0.0
    final_grade: str = "B"
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperEquityCurve:
    """Equity curve data from a paper simulation run."""
    dates: List[str] = field(default_factory=list)
    values: List[float] = field(default_factory=list)
    drawdowns: List[float] = field(default_factory=list)
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperDrawdownReport:
    """Drawdown analysis from a paper simulation equity curve."""
    max_drawdown_pct: float = 0.0
    max_drawdown_duration_days: int = 0
    recovery_days: int = 0
    drawdown_periods: List[Dict[str, Any]] = field(default_factory=list)
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperRiskReport:
    """Risk metrics report from a paper simulation run."""
    risk_per_trade_pct: float = 1.0
    max_holdings: int = 4
    current_exposure_pct: float = 0.0
    risk_budget_used_pct: float = 0.0
    stop_loss_coverage: bool = True
    risk_status: str = "PASS"
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperRegimePerformance:
    """Per-regime performance breakdown from paper simulation trades."""
    regime: str = "BULL"
    trade_count: int = 0
    win_rate_pct: float = 0.0
    avg_return_pct: float = 0.0
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperThemePerformance:
    """Per-theme performance breakdown from paper simulation trades."""
    theme: str = ""
    trade_count: int = 0
    win_rate_pct: float = 0.0
    avg_return_pct: float = 0.0
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperABCPerformance:
    """Per-ABC-type performance breakdown from paper simulation trades."""
    abc_type: str = "A"
    trade_count: int = 0
    win_rate_pct: float = 0.0
    avg_return_pct: float = 0.0
    avg_r: float = 0.0
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperMistakeImpactReport:
    """Impact report for a specific mistake type in paper simulation."""
    mistake_type: str = "none"
    trade_count: int = 0
    avg_loss_pct: float = 0.0
    behavior_penalty: float = 0.0
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperSimulationDashboard:
    """Top-level dashboard aggregating all paper simulation results."""
    version: str = "1.8.0"
    scenario_count: int = 0
    total_trades: int = 0
    final_grade: str = "B"
    metrics: Optional[PaperPerformanceMetrics] = None
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    research_only: bool = True
    no_real_orders: bool = True
    no_broker: bool = True
    not_investment_advice: bool = True


@dataclass
class PaperSimulationHealthSummary:
    """Health check summary for Paper Simulation & Performance Lab v1.8.0."""
    status: str = "PASS"
    passed: int = 0
    failed: int = 0
    total: int = 0
    all_passed: bool = True
    checks: List[Dict[str, Any]] = field(default_factory=list)
    schema_version: str = _SCHEMA_VERSION
    paper_only: bool = True
    not_investment_advice: bool = True
    no_real_orders: bool = True


def get_all_model_names() -> List[str]:
    """Return list of all 17 model class names in this module."""
    return [
        "PaperSimulationInput",
        "PaperSimulationConfig",
        "PaperSimulationScenario",
        "PaperSimulationTrade",
        "PaperSimulationPosition",
        "PaperSimulationPortfolio",
        "PaperSimulationResult",
        "PaperPerformanceMetrics",
        "PaperEquityCurve",
        "PaperDrawdownReport",
        "PaperRiskReport",
        "PaperRegimePerformance",
        "PaperThemePerformance",
        "PaperABCPerformance",
        "PaperMistakeImpactReport",
        "PaperSimulationDashboard",
        "PaperSimulationHealthSummary",
    ]
