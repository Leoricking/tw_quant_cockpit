"""
tests/test_optimization_models_v182.py
Tests for all 16 optimization data models v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.optimization_models_v182 import (
    OptimizationInput, OptimizationConfig, ParameterGrid, ParameterSet,
    ParameterSearchResult, ParameterRanking, WalkForwardWindow, WalkForwardConfig,
    WalkForwardResult, RobustParameterSet, OverfittingRiskReport, StabilityScore,
    ParameterSensitivityReport, OptimizationDashboard, OptimizationReport,
    OptimizationHealthSummary, get_all_model_names,
)


# --- get_all_model_names ---
def test_model_names_count_16():
    assert len(get_all_model_names()) == 16

def test_model_names_type():
    assert isinstance(get_all_model_names(), list)

def test_model_names_all_strings():
    assert all(isinstance(n, str) for n in get_all_model_names())

def test_model_names_contains_optimization_input():
    assert "OptimizationInput" in get_all_model_names()

def test_model_names_contains_parameter_grid():
    assert "ParameterGrid" in get_all_model_names()

def test_model_names_contains_walk_forward_result():
    assert "WalkForwardResult" in get_all_model_names()

def test_model_names_contains_optimization_dashboard():
    assert "OptimizationDashboard" in get_all_model_names()


# --- OptimizationInput ---
def test_optimization_input_defaults():
    m = OptimizationInput()
    assert m.initial_capital == 300000.0
    assert m.single_trade_risk_pct == 1.0
    assert m.max_positions == 4
    assert m.stop_loss_pct == 7.0
    assert m.take_profit_pct == 15.0

def test_optimization_input_paper_only():
    assert OptimizationInput().paper_only is True

def test_optimization_input_research_only():
    assert OptimizationInput().research_only is True

def test_optimization_input_validation_only():
    assert OptimizationInput().validation_only is True

def test_optimization_input_no_real_orders():
    assert OptimizationInput().no_real_orders is True

def test_optimization_input_not_investment_advice():
    assert OptimizationInput().not_investment_advice is True

def test_optimization_input_no_broker():
    assert OptimizationInput().no_broker is True

def test_optimization_input_schema_version():
    assert OptimizationInput().schema_version == "182"

def test_optimization_input_trailing_stop():
    assert OptimizationInput().trailing_stop_pct == 8.0

def test_optimization_input_max_drawdown():
    assert OptimizationInput().max_drawdown_limit_pct == 12.0

def test_optimization_input_thresholds():
    m = OptimizationInput()
    assert m.theme_score_threshold == 65.0
    assert m.watchlist_score_threshold == 65.0
    assert m.abc_score_threshold == 65.0


# --- OptimizationConfig ---
def test_optimization_config_defaults():
    m = OptimizationConfig()
    assert m.optimization_mode == "GRID_SEARCH"
    assert m.walk_forward_type == "ROLLING"
    assert m.in_sample_periods == 6
    assert m.out_of_sample_periods == 3

def test_optimization_config_paper_only():
    assert OptimizationConfig().paper_only is True

def test_optimization_config_research_only():
    assert OptimizationConfig().research_only is True

def test_optimization_config_validation_only():
    assert OptimizationConfig().validation_only is True

def test_optimization_config_no_real_orders():
    assert OptimizationConfig().no_real_orders is True

def test_optimization_config_schema_version():
    assert OptimizationConfig().schema_version == "182"

def test_optimization_config_min_parameter_sets():
    assert OptimizationConfig().min_parameter_sets == 10

def test_optimization_config_max_overfitting():
    assert OptimizationConfig().max_overfitting_risk_score == 70.0

def test_optimization_config_min_wf_pass_rate():
    assert OptimizationConfig().min_walk_forward_pass_rate_pct == 60.0

def test_optimization_config_max_degradation():
    assert OptimizationConfig().max_degradation_pct == 30.0


# --- ParameterGrid ---
def test_parameter_grid_paper_only():
    assert ParameterGrid().paper_only is True

def test_parameter_grid_schema_version():
    assert ParameterGrid().schema_version == "182"

def test_parameter_grid_initial_capital_values():
    assert len(ParameterGrid().initial_capital_values) == 3

def test_parameter_grid_risk_pct_values():
    assert len(ParameterGrid().single_trade_risk_pct_values) == 3

def test_parameter_grid_max_positions_values():
    assert len(ParameterGrid().max_positions_values) == 3

def test_parameter_grid_stop_loss_values():
    assert len(ParameterGrid().stop_loss_pct_values) == 3

def test_parameter_grid_take_profit_values():
    assert len(ParameterGrid().take_profit_pct_values) == 4

def test_parameter_grid_trailing_stop_values():
    assert len(ParameterGrid().trailing_stop_pct_values) == 3

def test_parameter_grid_drawdown_values():
    assert len(ParameterGrid().max_drawdown_limit_pct_values) == 4

def test_parameter_grid_theme_values():
    assert len(ParameterGrid().theme_score_threshold_values) == 3

def test_parameter_grid_watchlist_values():
    assert len(ParameterGrid().watchlist_score_threshold_values) == 3

def test_parameter_grid_abc_values():
    assert len(ParameterGrid().abc_score_threshold_values) == 3

def test_parameter_grid_behavior_values():
    assert len(ParameterGrid().behavior_risk_limit_values) == 3

def test_parameter_grid_risk_dashboard_values():
    assert len(ParameterGrid().risk_dashboard_limit_values) == 2


# --- ParameterSet ---
def test_parameter_set_defaults():
    m = ParameterSet()
    assert m.parameter_set_id == ""
    assert m.initial_capital == 300000.0
    assert m.is_blocked is False
    assert m.block_reason == ""

def test_parameter_set_paper_only():
    assert ParameterSet().paper_only is True

def test_parameter_set_research_only():
    assert ParameterSet().research_only is True

def test_parameter_set_validation_only():
    assert ParameterSet().validation_only is True

def test_parameter_set_no_real_orders():
    assert ParameterSet().no_real_orders is True

def test_parameter_set_schema_version():
    assert ParameterSet().schema_version == "182"

def test_parameter_set_performance_defaults():
    m = ParameterSet()
    assert m.in_sample_return_pct == 0.0
    assert m.out_of_sample_return_pct == 0.0
    assert m.win_rate_pct == 0.0
    assert m.profit_factor == 0.0
    assert m.expectancy_r == 0.0


# --- ParameterSearchResult ---
def test_search_result_defaults():
    m = ParameterSearchResult()
    assert m.total_parameter_sets == 0
    assert m.valid_parameter_sets == 0

def test_search_result_paper_only():
    assert ParameterSearchResult().paper_only is True

def test_search_result_schema_version():
    assert ParameterSearchResult().schema_version == "182"

def test_search_result_search_mode():
    assert ParameterSearchResult().search_mode == "GRID_SEARCH"

def test_search_result_parameter_sets_list():
    assert isinstance(ParameterSearchResult().parameter_sets, list)


# --- ParameterRanking ---
def test_ranking_defaults():
    m = ParameterRanking()
    assert m.rank == 0
    assert m.final_grade == "BLOCKED"

def test_ranking_paper_only():
    assert ParameterRanking().paper_only is True

def test_ranking_validation_only():
    assert ParameterRanking().validation_only is True

def test_ranking_schema_version():
    assert ParameterRanking().schema_version == "182"


# --- WalkForwardWindow ---
def test_wf_window_defaults():
    m = WalkForwardWindow()
    assert m.window_id == ""
    assert m.window_type == "ROLLING"
    assert m.market_regime == "BULL"
    assert m.passed is False

def test_wf_window_paper_only():
    assert WalkForwardWindow().paper_only is True

def test_wf_window_schema_version():
    assert WalkForwardWindow().schema_version == "182"


# --- WalkForwardConfig ---
def test_wf_config_defaults():
    m = WalkForwardConfig()
    assert m.walk_forward_type == "ROLLING"
    assert m.num_windows == 5
    assert m.in_sample_size == 6
    assert m.out_of_sample_size == 3

def test_wf_config_paper_only():
    assert WalkForwardConfig().paper_only is True

def test_wf_config_validation_only():
    assert WalkForwardConfig().validation_only is True

def test_wf_config_schema_version():
    assert WalkForwardConfig().schema_version == "182"

def test_wf_config_min_pass_rate():
    assert WalkForwardConfig().min_pass_rate_pct == 60.0


# --- WalkForwardResult ---
def test_wf_result_defaults():
    m = WalkForwardResult()
    assert m.walk_forward_type == "ROLLING"
    assert m.total_windows == 0
    assert m.walk_forward_passed is False

def test_wf_result_paper_only():
    assert WalkForwardResult().paper_only is True

def test_wf_result_validation_only():
    assert WalkForwardResult().validation_only is True

def test_wf_result_no_real_orders():
    assert WalkForwardResult().no_real_orders is True

def test_wf_result_schema_version():
    assert WalkForwardResult().schema_version == "182"

def test_wf_result_windows_list():
    assert isinstance(WalkForwardResult().windows, list)


# --- RobustParameterSet ---
def test_robust_ps_defaults():
    m = RobustParameterSet()
    assert m.parameter_set_id == ""
    assert m.final_grade == "BLOCKED"
    assert m.is_robust is False

def test_robust_ps_paper_only():
    assert RobustParameterSet().paper_only is True

def test_robust_ps_validation_only():
    assert RobustParameterSet().validation_only is True

def test_robust_ps_schema_version():
    assert RobustParameterSet().schema_version == "182"

def test_robust_ps_regime_flags():
    m = RobustParameterSet()
    assert m.works_in_bull is False
    assert m.works_in_bear is False
    assert m.works_in_range is False
    assert m.works_in_risk_off is False


# --- OverfittingRiskReport ---
def test_overfitting_defaults():
    m = OverfittingRiskReport()
    assert m.overfitting_risk_score == 0.0
    assert m.overfitting_detected is False
    assert m.overfitting_risk_level == "LOW"

def test_overfitting_paper_only():
    assert OverfittingRiskReport().paper_only is True

def test_overfitting_validation_only():
    assert OverfittingRiskReport().validation_only is True

def test_overfitting_schema_version():
    assert OverfittingRiskReport().schema_version == "182"

def test_overfitting_recommendations_list():
    assert isinstance(OverfittingRiskReport().recommendations, list)


# --- StabilityScore ---
def test_stability_defaults():
    m = StabilityScore()
    assert m.score == 0.0
    assert m.is_stable is False
    assert m.stability_grade == "UNSTABLE"

def test_stability_paper_only():
    assert StabilityScore().paper_only is True

def test_stability_schema_version():
    assert StabilityScore().schema_version == "182"


# --- ParameterSensitivityReport ---
def test_sensitivity_defaults():
    m = ParameterSensitivityReport()
    assert m.most_sensitive_parameter == ""
    assert m.overall_sensitivity == 0.0

def test_sensitivity_paper_only():
    assert ParameterSensitivityReport().paper_only is True

def test_sensitivity_validation_only():
    assert ParameterSensitivityReport().validation_only is True

def test_sensitivity_schema_version():
    assert ParameterSensitivityReport().schema_version == "182"

def test_sensitivity_scores_dict():
    assert isinstance(ParameterSensitivityReport().sensitivity_scores, dict)


# --- OptimizationDashboard ---
def test_dashboard_defaults():
    m = OptimizationDashboard()
    assert m.version == "1.8.2"
    assert m.final_grade == "BLOCKED"

def test_dashboard_paper_only():
    assert OptimizationDashboard().paper_only is True

def test_dashboard_research_only():
    assert OptimizationDashboard().research_only is True

def test_dashboard_validation_only():
    assert OptimizationDashboard().validation_only is True

def test_dashboard_no_real_orders():
    assert OptimizationDashboard().no_real_orders is True

def test_dashboard_not_investment_advice():
    assert OptimizationDashboard().not_investment_advice is True

def test_dashboard_schema_version():
    assert OptimizationDashboard().schema_version == "182"


# --- OptimizationReport ---
def test_report_defaults():
    m = OptimizationReport()
    assert m.version == "1.8.2"
    assert m.all_audits_pass is False

def test_report_paper_only():
    assert OptimizationReport().paper_only is True

def test_report_research_only():
    assert OptimizationReport().research_only is True

def test_report_schema_version():
    assert OptimizationReport().schema_version == "182"

def test_report_sections_list():
    assert isinstance(OptimizationReport().sections, list)


# --- OptimizationHealthSummary ---
def test_health_summary_defaults():
    m = OptimizationHealthSummary()
    assert m.total == 0
    assert m.passed == 0
    assert m.failed == 0
    assert m.all_passed is False
    assert m.status == "FAIL"

def test_health_summary_paper_only():
    assert OptimizationHealthSummary().paper_only is True

def test_health_summary_schema_version():
    assert OptimizationHealthSummary().schema_version == "182"

def test_health_summary_checks_list():
    assert isinstance(OptimizationHealthSummary().checks, list)
