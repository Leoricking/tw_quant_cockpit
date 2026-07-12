"""
tests/test_optimization_gui_v182.py
Tests for optimization GUI tabs v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE, _TABS, _TABS_V182_OPTIMIZATION,
    render_param_optimization_tab, render_walk_forward_validation_tab,
    render_overfitting_risk_tab, get_optimization_tab_names,
    render_all_tabs, get_tab_names, get_panel_info,
)


# --- PANEL_VERSION ---
def test_panel_version_182():
    assert PANEL_VERSION == "1.8.3"

def test_panel_title_182():
    assert "1.8.3" in PANEL_TITLE

def test_panel_title_optimization():
    assert "Optimization" in PANEL_TITLE


# --- _TABS_V182_OPTIMIZATION ---
def test_optimization_tabs_count_3():
    assert len(_TABS_V182_OPTIMIZATION) == 3

def test_optimization_tabs_param():
    assert "param_optimization" in _TABS_V182_OPTIMIZATION

def test_optimization_tabs_walk_forward():
    assert "walk_forward_validation" in _TABS_V182_OPTIMIZATION

def test_optimization_tabs_overfitting():
    assert "overfitting_risk" in _TABS_V182_OPTIMIZATION


# --- _TABS total ---
def test_tabs_total_129():
    assert len(_TABS) == 132

def test_tabs_includes_optimization():
    for tab in _TABS_V182_OPTIMIZATION:
        assert tab in _TABS


# --- get_optimization_tab_names ---
def test_get_optimization_tab_names_count():
    assert len(get_optimization_tab_names()) == 3

def test_get_optimization_tab_names_list():
    assert isinstance(get_optimization_tab_names(), list)

def test_get_optimization_tab_names_content():
    names = get_optimization_tab_names()
    assert "param_optimization" in names
    assert "walk_forward_validation" in names
    assert "overfitting_risk" in names


# --- render_param_optimization_tab ---
def test_param_opt_tab_returns_dict():
    result = render_param_optimization_tab()
    assert isinstance(result, dict)

def test_param_opt_tab_name():
    result = render_param_optimization_tab()
    assert result["tab"] == "param_optimization"

def test_param_opt_tab_version():
    result = render_param_optimization_tab()
    assert result["version"] == "1.8.2"

def test_param_opt_tab_paper_only():
    result = render_param_optimization_tab()
    assert result["paper_only"] is True

def test_param_opt_tab_research_only():
    result = render_param_optimization_tab()
    assert result["research_only"] is True

def test_param_opt_tab_validation_only():
    result = render_param_optimization_tab()
    assert result["validation_only"] is True

def test_param_opt_tab_no_real_orders():
    result = render_param_optimization_tab()
    assert result["no_real_orders"] is True

def test_param_opt_tab_headless_safe():
    result = render_param_optimization_tab()
    assert result["headless_safe"] is True

def test_param_opt_tab_dimensions():
    result = render_param_optimization_tab()
    assert result["parameter_dimensions"] == 12

def test_param_opt_tab_actions_count():
    result = render_param_optimization_tab()
    assert result["allowed_actions_count"] == 14


# --- render_walk_forward_validation_tab ---
def test_wf_tab_returns_dict():
    result = render_walk_forward_validation_tab()
    assert isinstance(result, dict)

def test_wf_tab_name():
    result = render_walk_forward_validation_tab()
    assert result["tab"] == "walk_forward_validation"

def test_wf_tab_version():
    result = render_walk_forward_validation_tab()
    assert result["version"] == "1.8.2"

def test_wf_tab_paper_only():
    result = render_walk_forward_validation_tab()
    assert result["paper_only"] is True

def test_wf_tab_headless_safe():
    result = render_walk_forward_validation_tab()
    assert result["headless_safe"] is True

def test_wf_tab_types_count():
    result = render_walk_forward_validation_tab()
    assert result["walk_forward_types_count"] == 10


# --- render_overfitting_risk_tab ---
def test_overfitting_tab_returns_dict():
    result = render_overfitting_risk_tab()
    assert isinstance(result, dict)

def test_overfitting_tab_name():
    result = render_overfitting_risk_tab()
    assert result["tab"] == "overfitting_risk"

def test_overfitting_tab_version():
    result = render_overfitting_risk_tab()
    assert result["version"] == "1.8.2"

def test_overfitting_tab_paper_only():
    result = render_overfitting_risk_tab()
    assert result["paper_only"] is True

def test_overfitting_tab_headless_safe():
    result = render_overfitting_risk_tab()
    assert result["headless_safe"] is True

def test_overfitting_tab_has_grade():
    result = render_overfitting_risk_tab()
    assert "final_grade" in result

def test_overfitting_tab_has_risk_score():
    result = render_overfitting_risk_tab()
    assert "overfitting_risk_score" in result

def test_overfitting_tab_has_pass_rate():
    result = render_overfitting_risk_tab()
    assert "walk_forward_pass_rate_pct" in result


# --- render_all_tabs ---
def test_render_all_tabs_count():
    result = render_all_tabs()
    assert len(result) >= 129

def test_render_all_tabs_includes_optimization():
    result = render_all_tabs()
    assert "param_optimization" in result
    assert "walk_forward_validation" in result
    assert "overfitting_risk" in result


# --- get_tab_names ---
def test_get_tab_names_count():
    assert len(get_tab_names()) == 132


# --- get_panel_info ---
def test_panel_info_version():
    assert get_panel_info()["panel_version"] == "1.8.3"

def test_panel_info_tab_count():
    assert get_panel_info()["tab_count"] == 132
