"""tests/test_paper_simulation_models_v180.py — v1.8.0 Paper Simulation model tests"""
from __future__ import annotations
import pytest
from paper_trading.small_capital_strategy.paper_simulation_models_v180 import (
    PaperSimulationInput, PaperSimulationConfig, PaperSimulationScenario,
    PaperSimulationTrade, PaperSimulationPosition, PaperSimulationPortfolio,
    PaperSimulationResult, PaperPerformanceMetrics, PaperEquityCurve,
    PaperDrawdownReport, PaperRiskReport, PaperRegimePerformance,
    PaperThemePerformance, PaperABCPerformance, PaperMistakeImpactReport,
    PaperSimulationDashboard, PaperSimulationHealthSummary, get_all_model_names,
)

_ALL_MODEL_NAMES = [
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


# ---------------------------------------------------------------------------
# get_all_model_names()
# ---------------------------------------------------------------------------

def test_get_all_model_names_returns_list():
    names = get_all_model_names()
    assert isinstance(names, list)


def test_get_all_model_names_length_is_17():
    assert len(get_all_model_names()) == 17


@pytest.mark.parametrize("name", _ALL_MODEL_NAMES)
def test_get_all_model_names_contains_each(name):
    assert name in get_all_model_names()


# ---------------------------------------------------------------------------
# PaperSimulationInput
# ---------------------------------------------------------------------------

def test_paper_simulation_input_instantiates():
    obj = PaperSimulationInput()
    assert obj is not None


def test_paper_simulation_input_paper_only():
    assert PaperSimulationInput().paper_only is True


def test_paper_simulation_input_no_real_orders():
    assert PaperSimulationInput().no_real_orders is True


def test_paper_simulation_input_schema_version():
    assert PaperSimulationInput().schema_version == "180"


def test_paper_simulation_input_default_capital():
    assert PaperSimulationInput().initial_capital == 300000.0


def test_paper_simulation_input_default_regime():
    assert PaperSimulationInput().market_regime == "BULL"


def test_paper_simulation_input_default_decision():
    assert PaperSimulationInput().integrated_decision == "PAPER_ENTRY_ALLOWED"


def test_paper_simulation_input_research_only():
    assert PaperSimulationInput().research_only is True


# ---------------------------------------------------------------------------
# PaperSimulationConfig
# ---------------------------------------------------------------------------

def test_paper_simulation_config_instantiates():
    obj = PaperSimulationConfig()
    assert obj is not None


def test_paper_simulation_config_paper_only():
    assert PaperSimulationConfig().paper_only is True


def test_paper_simulation_config_no_real_orders():
    assert PaperSimulationConfig().no_real_orders is True


def test_paper_simulation_config_schema_version():
    assert PaperSimulationConfig().schema_version == "180"


def test_paper_simulation_config_initial_capital():
    assert PaperSimulationConfig().initial_capital == 300000.0


def test_paper_simulation_config_risk_per_trade_pcts_values():
    cfg = PaperSimulationConfig()
    assert cfg.risk_per_trade_pcts == [0.8, 1.0, 1.5]


def test_paper_simulation_config_risk_per_trade_pcts_length():
    cfg = PaperSimulationConfig()
    assert len(cfg.risk_per_trade_pcts) == 3


def test_paper_simulation_config_max_holdings_options():
    cfg = PaperSimulationConfig()
    assert isinstance(cfg.max_holdings_options, list)
    assert len(cfg.max_holdings_options) == 3


def test_paper_simulation_config_simulation_days():
    assert PaperSimulationConfig().simulation_days == 252


# ---------------------------------------------------------------------------
# PaperSimulationScenario
# ---------------------------------------------------------------------------

def test_paper_simulation_scenario_instantiates():
    obj = PaperSimulationScenario()
    assert obj is not None


def test_paper_simulation_scenario_paper_only():
    assert PaperSimulationScenario().paper_only is True


def test_paper_simulation_scenario_no_real_orders():
    assert PaperSimulationScenario().no_real_orders is True


def test_paper_simulation_scenario_schema_version():
    assert PaperSimulationScenario().schema_version == "180"


def test_paper_simulation_scenario_expected_action_default():
    assert PaperSimulationScenario().expected_action == "PAPER_ENTRY_ALLOWED"


# ---------------------------------------------------------------------------
# PaperSimulationTrade
# ---------------------------------------------------------------------------

def test_paper_simulation_trade_instantiates():
    obj = PaperSimulationTrade()
    assert obj is not None


def test_paper_simulation_trade_paper_only():
    assert PaperSimulationTrade().paper_only is True


def test_paper_simulation_trade_no_real_orders():
    assert PaperSimulationTrade().no_real_orders is True


def test_paper_simulation_trade_schema_version():
    assert PaperSimulationTrade().schema_version == "180"


def test_paper_simulation_trade_default_abc_type():
    assert PaperSimulationTrade().abc_type == "A"


def test_paper_simulation_trade_default_mistake_type():
    assert PaperSimulationTrade().mistake_type == "none"


# ---------------------------------------------------------------------------
# PaperSimulationPosition
# ---------------------------------------------------------------------------

def test_paper_simulation_position_instantiates():
    obj = PaperSimulationPosition()
    assert obj is not None


def test_paper_simulation_position_paper_only():
    assert PaperSimulationPosition().paper_only is True


def test_paper_simulation_position_no_real_orders():
    assert PaperSimulationPosition().no_real_orders is True


def test_paper_simulation_position_schema_version():
    assert PaperSimulationPosition().schema_version == "180"


# ---------------------------------------------------------------------------
# PaperSimulationPortfolio
# ---------------------------------------------------------------------------

def test_paper_simulation_portfolio_instantiates():
    obj = PaperSimulationPortfolio()
    assert obj is not None


def test_paper_simulation_portfolio_paper_only():
    assert PaperSimulationPortfolio().paper_only is True


def test_paper_simulation_portfolio_no_real_orders():
    assert PaperSimulationPortfolio().no_real_orders is True


def test_paper_simulation_portfolio_schema_version():
    assert PaperSimulationPortfolio().schema_version == "180"


def test_paper_simulation_portfolio_default_cash():
    assert PaperSimulationPortfolio().cash == 300000.0


def test_paper_simulation_portfolio_positions_is_list():
    assert isinstance(PaperSimulationPortfolio().positions, list)


# ---------------------------------------------------------------------------
# PaperSimulationResult
# ---------------------------------------------------------------------------

def test_paper_simulation_result_instantiates():
    obj = PaperSimulationResult()
    assert obj is not None


def test_paper_simulation_result_paper_only():
    assert PaperSimulationResult().paper_only is True


def test_paper_simulation_result_no_real_orders():
    assert PaperSimulationResult().no_real_orders is True


def test_paper_simulation_result_schema_version():
    assert PaperSimulationResult().schema_version == "180"


def test_paper_simulation_result_default_trade_count():
    assert PaperSimulationResult().trade_count == 0


def test_paper_simulation_result_trades_is_list():
    assert isinstance(PaperSimulationResult().trades, list)


# ---------------------------------------------------------------------------
# PaperPerformanceMetrics
# ---------------------------------------------------------------------------

def test_paper_performance_metrics_instantiates():
    obj = PaperPerformanceMetrics()
    assert obj is not None


def test_paper_performance_metrics_paper_only():
    assert PaperPerformanceMetrics().paper_only is True


def test_paper_performance_metrics_no_real_orders():
    assert PaperPerformanceMetrics().no_real_orders is True


def test_paper_performance_metrics_schema_version():
    assert PaperPerformanceMetrics().schema_version == "180"


def test_paper_performance_metrics_final_grade_default():
    assert PaperPerformanceMetrics().final_grade == "B"


# ---------------------------------------------------------------------------
# PaperEquityCurve
# ---------------------------------------------------------------------------

def test_paper_equity_curve_instantiates():
    obj = PaperEquityCurve()
    assert obj is not None


def test_paper_equity_curve_paper_only():
    assert PaperEquityCurve().paper_only is True


def test_paper_equity_curve_no_real_orders():
    assert PaperEquityCurve().no_real_orders is True


def test_paper_equity_curve_schema_version():
    assert PaperEquityCurve().schema_version == "180"


def test_paper_equity_curve_dates_is_list():
    assert isinstance(PaperEquityCurve().dates, list)


def test_paper_equity_curve_values_is_list():
    assert isinstance(PaperEquityCurve().values, list)


def test_paper_equity_curve_drawdowns_is_list():
    assert isinstance(PaperEquityCurve().drawdowns, list)


# ---------------------------------------------------------------------------
# PaperDrawdownReport
# ---------------------------------------------------------------------------

def test_paper_drawdown_report_instantiates():
    obj = PaperDrawdownReport()
    assert obj is not None


def test_paper_drawdown_report_paper_only():
    assert PaperDrawdownReport().paper_only is True


def test_paper_drawdown_report_no_real_orders():
    assert PaperDrawdownReport().no_real_orders is True


def test_paper_drawdown_report_schema_version():
    assert PaperDrawdownReport().schema_version == "180"


def test_paper_drawdown_report_drawdown_periods_is_list():
    assert isinstance(PaperDrawdownReport().drawdown_periods, list)


# ---------------------------------------------------------------------------
# PaperRiskReport
# ---------------------------------------------------------------------------

def test_paper_risk_report_instantiates():
    obj = PaperRiskReport()
    assert obj is not None


def test_paper_risk_report_paper_only():
    assert PaperRiskReport().paper_only is True


def test_paper_risk_report_no_real_orders():
    assert PaperRiskReport().no_real_orders is True


def test_paper_risk_report_schema_version():
    assert PaperRiskReport().schema_version == "180"


def test_paper_risk_report_default_risk_status():
    assert PaperRiskReport().risk_status == "PASS"


def test_paper_risk_report_stop_loss_coverage():
    assert PaperRiskReport().stop_loss_coverage is True


# ---------------------------------------------------------------------------
# PaperRegimePerformance
# ---------------------------------------------------------------------------

def test_paper_regime_performance_instantiates():
    obj = PaperRegimePerformance()
    assert obj is not None


def test_paper_regime_performance_paper_only():
    assert PaperRegimePerformance().paper_only is True


def test_paper_regime_performance_no_real_orders():
    assert PaperRegimePerformance().no_real_orders is True


def test_paper_regime_performance_schema_version():
    assert PaperRegimePerformance().schema_version == "180"


def test_paper_regime_performance_default_regime():
    assert PaperRegimePerformance().regime == "BULL"


# ---------------------------------------------------------------------------
# PaperThemePerformance
# ---------------------------------------------------------------------------

def test_paper_theme_performance_instantiates():
    obj = PaperThemePerformance()
    assert obj is not None


def test_paper_theme_performance_paper_only():
    assert PaperThemePerformance().paper_only is True


def test_paper_theme_performance_no_real_orders():
    assert PaperThemePerformance().no_real_orders is True


def test_paper_theme_performance_schema_version():
    assert PaperThemePerformance().schema_version == "180"


# ---------------------------------------------------------------------------
# PaperABCPerformance
# ---------------------------------------------------------------------------

def test_paper_abc_performance_instantiates():
    obj = PaperABCPerformance()
    assert obj is not None


def test_paper_abc_performance_paper_only():
    assert PaperABCPerformance().paper_only is True


def test_paper_abc_performance_no_real_orders():
    assert PaperABCPerformance().no_real_orders is True


def test_paper_abc_performance_schema_version():
    assert PaperABCPerformance().schema_version == "180"


def test_paper_abc_performance_default_abc_type():
    assert PaperABCPerformance().abc_type == "A"


# ---------------------------------------------------------------------------
# PaperMistakeImpactReport
# ---------------------------------------------------------------------------

def test_paper_mistake_impact_report_instantiates():
    obj = PaperMistakeImpactReport()
    assert obj is not None


def test_paper_mistake_impact_report_paper_only():
    assert PaperMistakeImpactReport().paper_only is True


def test_paper_mistake_impact_report_no_real_orders():
    assert PaperMistakeImpactReport().no_real_orders is True


def test_paper_mistake_impact_report_schema_version():
    assert PaperMistakeImpactReport().schema_version == "180"


def test_paper_mistake_impact_report_default_mistake_type():
    assert PaperMistakeImpactReport().mistake_type == "none"


# ---------------------------------------------------------------------------
# PaperSimulationDashboard
# ---------------------------------------------------------------------------

def test_paper_simulation_dashboard_instantiates():
    obj = PaperSimulationDashboard()
    assert obj is not None


def test_paper_simulation_dashboard_paper_only():
    assert PaperSimulationDashboard().paper_only is True


def test_paper_simulation_dashboard_no_real_orders():
    assert PaperSimulationDashboard().no_real_orders is True


def test_paper_simulation_dashboard_schema_version():
    assert PaperSimulationDashboard().schema_version == "180"


def test_paper_simulation_dashboard_version():
    assert PaperSimulationDashboard().version == "1.8.0"


def test_paper_simulation_dashboard_final_grade_default():
    assert PaperSimulationDashboard().final_grade == "B"


def test_paper_simulation_dashboard_metrics_default_none():
    assert PaperSimulationDashboard().metrics is None


# ---------------------------------------------------------------------------
# PaperSimulationHealthSummary
# ---------------------------------------------------------------------------

def test_paper_simulation_health_summary_instantiates():
    obj = PaperSimulationHealthSummary()
    assert obj is not None


def test_paper_simulation_health_summary_paper_only():
    assert PaperSimulationHealthSummary().paper_only is True


def test_paper_simulation_health_summary_no_real_orders():
    assert PaperSimulationHealthSummary().no_real_orders is True


def test_paper_simulation_health_summary_schema_version():
    assert PaperSimulationHealthSummary().schema_version == "180"


def test_paper_simulation_health_summary_status():
    assert PaperSimulationHealthSummary().status == "PASS"


def test_paper_simulation_health_summary_all_passed():
    assert PaperSimulationHealthSummary().all_passed is True


def test_paper_simulation_health_summary_checks_is_list():
    assert isinstance(PaperSimulationHealthSummary().checks, list)
