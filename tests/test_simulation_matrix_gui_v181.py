"""
tests/test_simulation_matrix_gui_v181.py
Tests for v1.8.1 GUI tabs in small_capital_strategy_panel.py.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE, _TABS, _TABS_V181_SIM_MATRIX,
    render_sim_matrix_lab_tab, render_sim_stress_test_tab, render_sim_robustness_score_tab,
    get_sim_matrix_tab_names, render_all_tabs,
)


# ── Panel version ──────────────────────────────────────────────────────────────

def test_panel_version_181():
    assert PANEL_VERSION == "1.8.1"

def test_panel_title_contains_181():
    assert "1.8.1" in PANEL_TITLE

def test_panel_title_contains_simulation():
    assert "Simulation" in PANEL_TITLE


# ── _TABS_V181_SIM_MATRIX ─────────────────────────────────────────────────────

def test_sim_matrix_tabs_is_list():
    assert isinstance(_TABS_V181_SIM_MATRIX, list)

def test_sim_matrix_tabs_count_3():
    assert len(_TABS_V181_SIM_MATRIX) == 3

def test_sim_matrix_lab_in_tabs():
    assert "sim_matrix_lab" in _TABS_V181_SIM_MATRIX

def test_sim_stress_test_in_tabs():
    assert "sim_stress_test" in _TABS_V181_SIM_MATRIX

def test_sim_robustness_score_in_tabs():
    assert "sim_robustness_score" in _TABS_V181_SIM_MATRIX

def test_all_v181_tabs_in_global_tabs():
    for tab in _TABS_V181_SIM_MATRIX:
        assert tab in _TABS


# ── get_sim_matrix_tab_names() ────────────────────────────────────────────────

def test_get_sim_matrix_tab_names_is_list():
    assert isinstance(get_sim_matrix_tab_names(), list)

def test_get_sim_matrix_tab_names_count():
    assert len(get_sim_matrix_tab_names()) == 3

def test_get_sim_matrix_tab_names_content():
    names = get_sim_matrix_tab_names()
    assert "sim_matrix_lab" in names
    assert "sim_stress_test" in names
    assert "sim_robustness_score" in names


# ── render_sim_matrix_lab_tab() ───────────────────────────────────────────────

def test_render_sim_matrix_lab_is_dict():
    assert isinstance(render_sim_matrix_lab_tab(), dict)

def test_render_sim_matrix_lab_tab_key():
    assert render_sim_matrix_lab_tab()["tab"] == "sim_matrix_lab"

def test_render_sim_matrix_lab_paper_only():
    assert render_sim_matrix_lab_tab()["paper_only"] is True

def test_render_sim_matrix_lab_research_only():
    assert render_sim_matrix_lab_tab()["research_only"] is True

def test_render_sim_matrix_lab_stress_test_only():
    assert render_sim_matrix_lab_tab()["stress_test_only"] is True

def test_render_sim_matrix_lab_no_real_orders():
    assert render_sim_matrix_lab_tab()["no_real_orders"] is True

def test_render_sim_matrix_lab_not_investment_advice():
    assert render_sim_matrix_lab_tab()["not_investment_advice"] is True

def test_render_sim_matrix_lab_no_broker():
    assert render_sim_matrix_lab_tab()["no_broker"] is True

def test_render_sim_matrix_lab_version():
    result = render_sim_matrix_lab_tab()
    assert result.get("version") == "1.8.1"

def test_render_sim_matrix_lab_scenario_count_ge_75():
    result = render_sim_matrix_lab_tab()
    assert result.get("scenario_count", 0) >= 75

def test_render_sim_matrix_lab_title_not_empty():
    assert render_sim_matrix_lab_tab()["title"] != ""


# ── render_sim_stress_test_tab() ──────────────────────────────────────────────

def test_render_sim_stress_test_is_dict():
    assert isinstance(render_sim_stress_test_tab(), dict)

def test_render_sim_stress_test_tab_key():
    assert render_sim_stress_test_tab()["tab"] == "sim_stress_test"

def test_render_sim_stress_test_paper_only():
    assert render_sim_stress_test_tab()["paper_only"] is True

def test_render_sim_stress_test_stress_test_only():
    assert render_sim_stress_test_tab()["stress_test_only"] is True

def test_render_sim_stress_test_no_real_orders():
    assert render_sim_stress_test_tab()["no_real_orders"] is True

def test_render_sim_stress_test_not_investment_advice():
    assert render_sim_stress_test_tab()["not_investment_advice"] is True

def test_render_sim_stress_test_count_ge_10():
    result = render_sim_stress_test_tab()
    assert result.get("stress_test_count", 0) >= 10

def test_render_sim_stress_test_survived_count_nonneg():
    result = render_sim_stress_test_tab()
    assert result.get("survived_count", 0) >= 0

def test_render_sim_stress_test_title_not_empty():
    assert render_sim_stress_test_tab()["title"] != ""


# ── render_sim_robustness_score_tab() ────────────────────────────────────────

def test_render_sim_robustness_score_is_dict():
    assert isinstance(render_sim_robustness_score_tab(), dict)

def test_render_sim_robustness_score_tab_key():
    assert render_sim_robustness_score_tab()["tab"] == "sim_robustness_score"

def test_render_sim_robustness_score_paper_only():
    assert render_sim_robustness_score_tab()["paper_only"] is True

def test_render_sim_robustness_score_stress_test_only():
    assert render_sim_robustness_score_tab()["stress_test_only"] is True

def test_render_sim_robustness_score_no_real_orders():
    assert render_sim_robustness_score_tab()["no_real_orders"] is True

def test_render_sim_robustness_score_not_investment_advice():
    assert render_sim_robustness_score_tab()["not_investment_advice"] is True

def test_render_sim_robustness_score_grade_in_valid():
    result = render_sim_robustness_score_tab()
    valid_grades = {"ROBUST", "ACCEPTABLE", "FRAGILE", "DANGEROUS", "BLOCKED"}
    assert result.get("final_grade") in valid_grades

def test_render_sim_robustness_score_in_range():
    result = render_sim_robustness_score_tab()
    assert 0.0 <= result.get("score", 0.0) <= 100.0

def test_render_sim_robustness_score_title_not_empty():
    assert render_sim_robustness_score_tab()["title"] != ""


# ── render_all_tabs() includes v1.8.1 tabs ────────────────────────────────────

def test_render_all_tabs_contains_sim_matrix_lab():
    result = render_all_tabs()
    assert "sim_matrix_lab" in result

def test_render_all_tabs_contains_sim_stress_test():
    result = render_all_tabs()
    assert "sim_stress_test" in result

def test_render_all_tabs_contains_sim_robustness_score():
    result = render_all_tabs()
    assert "sim_robustness_score" in result

def test_render_all_tabs_sim_matrix_lab_paper_only():
    result = render_all_tabs()
    assert result["sim_matrix_lab"]["paper_only"] is True

def test_render_all_tabs_sim_stress_test_no_real_orders():
    result = render_all_tabs()
    assert result["sim_stress_test"]["no_real_orders"] is True

def test_render_all_tabs_sim_robustness_score_stress_test_only():
    result = render_all_tabs()
    assert result["sim_robustness_score"]["stress_test_only"] is True
