"""tests/test_paper_simulation_gui_v180.py — v1.8.0 Paper Simulation GUI tab tests"""
from __future__ import annotations
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE, _TABS, _TABS_V180_PAPER_SIM,
    render_paper_sim_lab_tab, render_paper_sim_equity_curve_tab,
    render_paper_sim_performance_tab, get_paper_sim_tab_names,
    render_all_tabs, get_panel_info,
)


# ---------------------------------------------------------------------------
# Panel version and title
# ---------------------------------------------------------------------------

def test_panel_version_is_180() -> None:
    assert PANEL_VERSION == "1.8.1"


def test_panel_title_contains_version_180() -> None:
    assert "1.8.1" in PANEL_TITLE


# ---------------------------------------------------------------------------
# _TABS includes the three new v1.8.0 tabs
# ---------------------------------------------------------------------------

def test_tabs_contains_paper_sim_lab() -> None:
    assert "paper_sim_lab" in _TABS


def test_tabs_contains_paper_sim_equity_curve() -> None:
    assert "paper_sim_equity_curve" in _TABS


def test_tabs_contains_paper_sim_performance() -> None:
    assert "paper_sim_performance" in _TABS


# ---------------------------------------------------------------------------
# _TABS_V180_PAPER_SIM contents
# ---------------------------------------------------------------------------

def test_tabs_v180_paper_sim_length_is_3() -> None:
    assert len(_TABS_V180_PAPER_SIM) == 3


def test_tabs_v180_paper_sim_contains_paper_sim_lab() -> None:
    assert "paper_sim_lab" in _TABS_V180_PAPER_SIM


def test_tabs_v180_paper_sim_contains_paper_sim_equity_curve() -> None:
    assert "paper_sim_equity_curve" in _TABS_V180_PAPER_SIM


def test_tabs_v180_paper_sim_contains_paper_sim_performance() -> None:
    assert "paper_sim_performance" in _TABS_V180_PAPER_SIM


# ---------------------------------------------------------------------------
# get_paper_sim_tab_names()
# ---------------------------------------------------------------------------

def test_get_paper_sim_tab_names_equals_tabs_v180() -> None:
    assert get_paper_sim_tab_names() == list(_TABS_V180_PAPER_SIM)


def test_get_paper_sim_tab_names_returns_list() -> None:
    result = get_paper_sim_tab_names()
    assert isinstance(result, list)


def test_get_paper_sim_tab_names_length_is_3() -> None:
    assert len(get_paper_sim_tab_names()) == 3


# ---------------------------------------------------------------------------
# render_paper_sim_lab_tab()
# ---------------------------------------------------------------------------

def test_render_paper_sim_lab_tab_returns_dict() -> None:
    result = render_paper_sim_lab_tab()
    assert isinstance(result, dict)


def test_render_paper_sim_lab_tab_tab_key() -> None:
    assert render_paper_sim_lab_tab()["tab"] == "paper_sim_lab"


def test_render_paper_sim_lab_tab_paper_only() -> None:
    assert render_paper_sim_lab_tab()["paper_only"] is True


def test_render_paper_sim_lab_tab_research_only() -> None:
    assert render_paper_sim_lab_tab()["research_only"] is True


def test_render_paper_sim_lab_tab_no_real_orders() -> None:
    assert render_paper_sim_lab_tab()["no_real_orders"] is True


def test_render_paper_sim_lab_tab_not_investment_advice() -> None:
    assert render_paper_sim_lab_tab()["not_investment_advice"] is True


def test_render_paper_sim_lab_tab_no_broker() -> None:
    assert render_paper_sim_lab_tab()["no_broker"] is True


# ---------------------------------------------------------------------------
# render_paper_sim_equity_curve_tab()
# ---------------------------------------------------------------------------

def test_render_paper_sim_equity_curve_tab_returns_dict() -> None:
    result = render_paper_sim_equity_curve_tab()
    assert isinstance(result, dict)


def test_render_paper_sim_equity_curve_tab_tab_key() -> None:
    assert render_paper_sim_equity_curve_tab()["tab"] == "paper_sim_equity_curve"


def test_render_paper_sim_equity_curve_tab_paper_only() -> None:
    assert render_paper_sim_equity_curve_tab()["paper_only"] is True


def test_render_paper_sim_equity_curve_tab_no_real_orders() -> None:
    assert render_paper_sim_equity_curve_tab()["no_real_orders"] is True


# ---------------------------------------------------------------------------
# render_paper_sim_performance_tab()
# ---------------------------------------------------------------------------

def test_render_paper_sim_performance_tab_returns_dict() -> None:
    result = render_paper_sim_performance_tab()
    assert isinstance(result, dict)


def test_render_paper_sim_performance_tab_tab_key() -> None:
    assert render_paper_sim_performance_tab()["tab"] == "paper_sim_performance"


def test_render_paper_sim_performance_tab_paper_only() -> None:
    assert render_paper_sim_performance_tab()["paper_only"] is True


def test_render_paper_sim_performance_tab_no_real_orders() -> None:
    assert render_paper_sim_performance_tab()["no_real_orders"] is True


# ---------------------------------------------------------------------------
# render_all_tabs()
# ---------------------------------------------------------------------------

def test_render_all_tabs_returns_dict() -> None:
    result = render_all_tabs()
    assert isinstance(result, dict)


def test_render_all_tabs_contains_paper_sim_lab() -> None:
    assert "paper_sim_lab" in render_all_tabs()


def test_render_all_tabs_contains_paper_sim_equity_curve() -> None:
    assert "paper_sim_equity_curve" in render_all_tabs()


def test_render_all_tabs_contains_paper_sim_performance() -> None:
    assert "paper_sim_performance" in render_all_tabs()


# ---------------------------------------------------------------------------
# get_panel_info()
# ---------------------------------------------------------------------------

def test_get_panel_info_panel_version_is_180() -> None:
    assert get_panel_info()["panel_version"] == "1.8.1"


def test_get_panel_info_tab_count_matches_tabs() -> None:
    assert get_panel_info()["tab_count"] == len(_TABS)


def test_get_panel_info_headless_safe() -> None:
    assert get_panel_info()["headless_safe"] is True


# ---------------------------------------------------------------------------
# Total tab count guard
# ---------------------------------------------------------------------------

def test_total_tab_count_at_least_123() -> None:
    assert len(_TABS) >= 123
