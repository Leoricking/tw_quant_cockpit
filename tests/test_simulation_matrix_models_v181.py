"""
tests/test_simulation_matrix_models_v181.py
Tests for simulation_matrix_models_v181 — dataclass models.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import (
    SimulationMatrixInput, SimulationMatrixConfig, SimulationMatrixAxis,
    SimulationMatrixCell, SimulationMatrixResult,
    StressTestScenario, StressTestResult, StressDrawdownShock,
    StressLosingStreakShock, StressRegimeShiftShock, StressThemeCollapseShock,
    StressMistakeInjection, RobustnessScore,
    ScenarioMatrixDashboard, ScenarioMatrixReport, ScenarioMatrixHealthSummary,
    get_all_model_names,
)


# ── get_all_model_names() ──────────────────────────────────────────────────────

def test_model_names_is_list():
    assert isinstance(get_all_model_names(), list)

def test_model_names_count_16():
    assert len(get_all_model_names()) == 16

def test_model_names_contains_input():
    assert "SimulationMatrixInput" in get_all_model_names()

def test_model_names_contains_config():
    assert "SimulationMatrixConfig" in get_all_model_names()

def test_model_names_contains_cell():
    assert "SimulationMatrixCell" in get_all_model_names()

def test_model_names_contains_result():
    assert "SimulationMatrixResult" in get_all_model_names()

def test_model_names_contains_stress_result():
    assert "StressTestResult" in get_all_model_names()

def test_model_names_contains_robustness():
    assert "RobustnessScore" in get_all_model_names()

def test_model_names_contains_dashboard():
    assert "ScenarioMatrixDashboard" in get_all_model_names()

def test_model_names_contains_health_summary():
    assert "ScenarioMatrixHealthSummary" in get_all_model_names()


# ── SimulationMatrixInput ──────────────────────────────────────────────────────

def test_matrix_input_defaults():
    inp = SimulationMatrixInput()
    assert inp.initial_capital == 300000.0

def test_matrix_input_paper_only():
    assert SimulationMatrixInput().paper_only is True

def test_matrix_input_research_only():
    assert SimulationMatrixInput().research_only is True

def test_matrix_input_simulate_only():
    assert SimulationMatrixInput().simulate_only is True

def test_matrix_input_no_real_orders():
    assert SimulationMatrixInput().no_real_orders is True

def test_matrix_input_no_broker():
    assert SimulationMatrixInput().no_broker is True

def test_matrix_input_not_investment_advice():
    assert SimulationMatrixInput().not_investment_advice is True

def test_matrix_input_default_market_regime():
    assert SimulationMatrixInput().market_regime == "BULL"

def test_matrix_input_default_theme_rank():
    assert SimulationMatrixInput().theme_rank == "LEADER"

def test_matrix_input_default_watchlist_rank():
    assert SimulationMatrixInput().watchlist_rank == "CORE"

def test_matrix_input_default_abc_signal():
    assert SimulationMatrixInput().abc_signal == "A"

def test_matrix_input_default_behavior_risk():
    assert SimulationMatrixInput().behavior_risk == "PASS"

def test_matrix_input_default_risk_dashboard():
    assert SimulationMatrixInput().risk_dashboard == "PASS"

def test_matrix_input_default_mistake_injection():
    assert SimulationMatrixInput().mistake_injection == "NONE"

def test_matrix_input_schema_version():
    assert SimulationMatrixInput().schema_version == "181"

def test_matrix_input_custom_capital():
    inp = SimulationMatrixInput(initial_capital=500000.0)
    assert inp.initial_capital == 500000.0

def test_matrix_input_custom_regime():
    inp = SimulationMatrixInput(market_regime="BEAR")
    assert inp.market_regime == "BEAR"


# ── SimulationMatrixConfig ─────────────────────────────────────────────────────

def test_matrix_config_defaults():
    cfg = SimulationMatrixConfig()
    assert cfg.paper_only is True

def test_matrix_config_market_regimes():
    cfg = SimulationMatrixConfig()
    assert "BULL" in cfg.market_regimes
    assert "RISK_OFF" in cfg.market_regimes

def test_matrix_config_theme_ranks():
    cfg = SimulationMatrixConfig()
    assert "LEADER" in cfg.theme_ranks
    assert "EXCLUDED" in cfg.theme_ranks

def test_matrix_config_abc_signals():
    cfg = SimulationMatrixConfig()
    assert "A" in cfg.abc_signals
    assert "BLOCKED" in cfg.abc_signals

def test_matrix_config_mistake_injections():
    cfg = SimulationMatrixConfig()
    assert "NO_STOP_LOSS" in cfg.mistake_injections

def test_matrix_config_initial_capitals():
    cfg = SimulationMatrixConfig()
    assert 300000.0 in cfg.initial_capitals

def test_matrix_config_schema_version():
    assert SimulationMatrixConfig().schema_version == "181"

def test_matrix_config_no_real_orders():
    assert SimulationMatrixConfig().no_real_orders is True


# ── SimulationMatrixAxis ───────────────────────────────────────────────────────

def test_matrix_axis_defaults():
    axis = SimulationMatrixAxis()
    assert axis.paper_only is True

def test_matrix_axis_empty_values():
    axis = SimulationMatrixAxis()
    assert isinstance(axis.values, list)

def test_matrix_axis_custom_name():
    axis = SimulationMatrixAxis(name="market_regime", values=["BULL","BEAR"])
    assert axis.name == "market_regime"
    assert len(axis.values) == 2


# ── SimulationMatrixCell ───────────────────────────────────────────────────────

def test_matrix_cell_defaults():
    cell = SimulationMatrixCell()
    assert cell.paper_only is True

def test_matrix_cell_default_action():
    assert SimulationMatrixCell().action == "WAIT"

def test_matrix_cell_default_not_blocked():
    assert SimulationMatrixCell().is_blocked is False

def test_matrix_cell_schema_version():
    assert SimulationMatrixCell().schema_version == "181"

def test_matrix_cell_no_real_orders():
    assert SimulationMatrixCell().no_real_orders is True


# ── SimulationMatrixResult ─────────────────────────────────────────────────────

def test_matrix_result_defaults():
    r = SimulationMatrixResult()
    assert r.paper_only is True

def test_matrix_result_default_grade():
    assert SimulationMatrixResult().final_grade == "FRAGILE"

def test_matrix_result_cells_empty_list():
    assert SimulationMatrixResult().cells == []

def test_matrix_result_no_real_orders():
    assert SimulationMatrixResult().no_real_orders is True


# ── StressTestScenario ─────────────────────────────────────────────────────────

def test_stress_scenario_paper_only():
    assert StressTestScenario().paper_only is True

def test_stress_scenario_stress_test_only():
    assert StressTestScenario().stress_test_only is True

def test_stress_scenario_no_real_orders():
    assert StressTestScenario().no_real_orders is True

def test_stress_scenario_severity_default():
    assert StressTestScenario().severity == "MEDIUM"


# ── StressTestResult ───────────────────────────────────────────────────────────

def test_stress_result_paper_only():
    assert StressTestResult().paper_only is True

def test_stress_result_stress_test_only():
    assert StressTestResult().stress_test_only is True

def test_stress_result_default_survived():
    assert StressTestResult().survived is True

def test_stress_result_default_capital():
    assert StressTestResult().final_capital == 300000.0

def test_stress_result_no_real_orders():
    assert StressTestResult().no_real_orders is True


# ── StressDrawdownShock ────────────────────────────────────────────────────────

def test_drawdown_shock_paper_only():
    assert StressDrawdownShock().paper_only is True

def test_drawdown_shock_stress_test_only():
    assert StressDrawdownShock().stress_test_only is True

def test_drawdown_shock_default_drawdown():
    assert StressDrawdownShock().drawdown_pct == 20.0


# ── StressLosingStreakShock ────────────────────────────────────────────────────

def test_losing_streak_paper_only():
    assert StressLosingStreakShock().paper_only is True

def test_losing_streak_stress_test_only():
    assert StressLosingStreakShock().stress_test_only is True

def test_losing_streak_default_length():
    assert StressLosingStreakShock().streak_length == 3

def test_losing_streak_total_loss_auto_computed():
    shock = StressLosingStreakShock(streak_length=5, loss_per_trade_pct=1.0)
    assert shock.total_loss_pct == 5.0

def test_losing_streak_total_loss_override():
    shock = StressLosingStreakShock(streak_length=3, loss_per_trade_pct=1.0, total_loss_pct=10.0)
    assert shock.total_loss_pct == 10.0


# ── StressRegimeShiftShock ─────────────────────────────────────────────────────

def test_regime_shift_paper_only():
    assert StressRegimeShiftShock().paper_only is True

def test_regime_shift_stress_test_only():
    assert StressRegimeShiftShock().stress_test_only is True

def test_regime_shift_default_from():
    assert StressRegimeShiftShock().from_regime == "BULL"

def test_regime_shift_default_to():
    assert StressRegimeShiftShock().to_regime == "RISK_OFF"


# ── StressThemeCollapseShock ───────────────────────────────────────────────────

def test_theme_collapse_paper_only():
    assert StressThemeCollapseShock().paper_only is True

def test_theme_collapse_stress_test_only():
    assert StressThemeCollapseShock().stress_test_only is True

def test_theme_collapse_default_from():
    assert StressThemeCollapseShock().from_theme == "LEADER"

def test_theme_collapse_default_to():
    assert StressThemeCollapseShock().to_theme == "EXCLUDED"


# ── StressMistakeInjection ─────────────────────────────────────────────────────

def test_mistake_injection_paper_only():
    assert StressMistakeInjection().paper_only is True

def test_mistake_injection_stress_test_only():
    assert StressMistakeInjection().stress_test_only is True

def test_mistake_injection_default_type():
    assert StressMistakeInjection().mistake_type == "NONE"


# ── RobustnessScore ────────────────────────────────────────────────────────────

def test_robustness_score_paper_only():
    assert RobustnessScore().paper_only is True

def test_robustness_score_stress_test_only():
    assert RobustnessScore().stress_test_only is True

def test_robustness_score_default_grade():
    assert RobustnessScore().final_grade == "FRAGILE"

def test_robustness_score_default_score():
    assert RobustnessScore().score == 0.0

def test_robustness_score_no_real_orders():
    assert RobustnessScore().no_real_orders is True


# ── ScenarioMatrixDashboard ────────────────────────────────────────────────────

def test_dashboard_paper_only():
    assert ScenarioMatrixDashboard().paper_only is True

def test_dashboard_stress_test_only():
    assert ScenarioMatrixDashboard().stress_test_only is True

def test_dashboard_version():
    assert ScenarioMatrixDashboard().version == "1.8.1"

def test_dashboard_default_grade():
    assert ScenarioMatrixDashboard().final_grade == "FRAGILE"

def test_dashboard_no_real_orders():
    assert ScenarioMatrixDashboard().no_real_orders is True


# ── ScenarioMatrixReport ───────────────────────────────────────────────────────

def test_matrix_report_paper_only():
    assert ScenarioMatrixReport().paper_only is True

def test_matrix_report_stress_test_only():
    assert ScenarioMatrixReport().stress_test_only is True

def test_matrix_report_version():
    assert ScenarioMatrixReport().version == "1.8.1"

def test_matrix_report_sections_empty():
    assert ScenarioMatrixReport().sections == []


# ── ScenarioMatrixHealthSummary ────────────────────────────────────────────────

def test_health_summary_status():
    assert ScenarioMatrixHealthSummary().status == "PASS"

def test_health_summary_all_passed():
    assert ScenarioMatrixHealthSummary().all_passed is True

def test_health_summary_paper_only():
    assert ScenarioMatrixHealthSummary().paper_only is True

def test_health_summary_no_real_orders():
    assert ScenarioMatrixHealthSummary().no_real_orders is True

def test_health_summary_checks_empty():
    assert ScenarioMatrixHealthSummary().checks == []
