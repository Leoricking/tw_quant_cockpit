"""
tests/test_optimization_report_v182.py
Tests for optimization report builder v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.optimization_report_v182 import (
    REPORT_SECTIONS, build_optimization_report, build_dashboard_report,
    get_report_info,
)
from paper_trading.small_capital_strategy.optimization_models_v182 import (
    OptimizationDashboard, OptimizationReport, ParameterGrid, OptimizationConfig,
    ParameterSearchResult,
)
from paper_trading.small_capital_strategy.optimization_engine_v182 import (
    run_parameter_search, VALID_FINAL_GRADES,
)


# --- REPORT_SECTIONS ---
def test_report_sections_count_12():
    assert len(REPORT_SECTIONS) == 12

def test_report_sections_type():
    assert isinstance(REPORT_SECTIONS, list)

def test_report_sections_version():
    assert "version" in REPORT_SECTIONS

def test_report_sections_safety():
    assert "safety" in REPORT_SECTIONS

def test_report_sections_parameter_grid():
    assert "parameter_grid" in REPORT_SECTIONS

def test_report_sections_parameter_search():
    assert "parameter_search" in REPORT_SECTIONS

def test_report_sections_parameter_ranking():
    assert "parameter_ranking" in REPORT_SECTIONS

def test_report_sections_walk_forward():
    assert "walk_forward" in REPORT_SECTIONS

def test_report_sections_stability():
    assert "stability_score" in REPORT_SECTIONS

def test_report_sections_sensitivity():
    assert "sensitivity_report" in REPORT_SECTIONS

def test_report_sections_overfitting():
    assert "overfitting_risk" in REPORT_SECTIONS

def test_report_sections_dashboard():
    assert "dashboard" in REPORT_SECTIONS

def test_report_sections_backward_compat():
    assert "backward_compat" in REPORT_SECTIONS

def test_report_sections_summary():
    assert "summary" in REPORT_SECTIONS


# --- build_optimization_report ---
def test_build_report_returns_model():
    dashboard = OptimizationDashboard()
    report = build_optimization_report(dashboard)
    assert isinstance(report, OptimizationReport)

def test_build_report_sections_12():
    dashboard = OptimizationDashboard()
    report = build_optimization_report(dashboard)
    assert len(report.sections) == 12

def test_build_report_paper_only():
    dashboard = OptimizationDashboard()
    report = build_optimization_report(dashboard)
    assert report.paper_only is True

def test_build_report_research_only():
    dashboard = OptimizationDashboard()
    report = build_optimization_report(dashboard)
    assert report.research_only is True

def test_build_report_version():
    dashboard = OptimizationDashboard()
    report = build_optimization_report(dashboard)
    assert report.version == "1.8.2"

def test_build_report_schema_version():
    dashboard = OptimizationDashboard()
    report = build_optimization_report(dashboard)
    assert report.schema_version == "182"

def test_build_report_all_sections_have_paper_only():
    dashboard = OptimizationDashboard()
    report = build_optimization_report(dashboard)
    for section in report.sections:
        assert section["paper_only"] is True

def test_build_report_blocked_dashboard():
    dashboard = OptimizationDashboard(final_grade="BLOCKED")
    report = build_optimization_report(dashboard)
    assert report.all_audits_pass is False


# --- build_dashboard_report ---
def test_dashboard_returns_model():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    dashboard = build_dashboard_report(result)
    assert isinstance(dashboard, OptimizationDashboard)

def test_dashboard_paper_only():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    dashboard = build_dashboard_report(result)
    assert dashboard.paper_only is True

def test_dashboard_version():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    dashboard = build_dashboard_report(result)
    assert dashboard.version == "1.8.2"

def test_dashboard_schema_version():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    dashboard = build_dashboard_report(result)
    assert dashboard.schema_version == "182"

def test_dashboard_grade_valid():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    dashboard = build_dashboard_report(result)
    assert dashboard.final_grade in VALID_FINAL_GRADES

def test_dashboard_valid_count_gt_0():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    dashboard = build_dashboard_report(result)
    assert dashboard.valid_parameter_count > 0

def test_dashboard_parameter_count_gt_0():
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    dashboard = build_dashboard_report(result)
    assert dashboard.parameter_count > 0

def test_dashboard_empty_result():
    result = ParameterSearchResult()
    dashboard = build_dashboard_report(result)
    assert dashboard.final_grade == "BLOCKED"


# --- get_report_info ---
def test_report_info_returns_dict():
    assert isinstance(get_report_info(), dict)

def test_report_info_version():
    assert get_report_info()["version"] == "1.8.2"

def test_report_info_count_12():
    assert get_report_info()["count"] == 12

def test_report_info_paper_only():
    assert get_report_info()["paper_only"] is True

def test_report_info_validation_only():
    assert get_report_info()["validation_only"] is True

def test_report_info_schema_version():
    assert get_report_info()["schema_version"] == "182"

def test_report_info_sections_list():
    info = get_report_info()
    assert isinstance(info["sections"], list)
    assert len(info["sections"]) == 12
