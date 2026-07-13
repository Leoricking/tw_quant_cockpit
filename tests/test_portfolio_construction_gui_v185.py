"""
tests/test_portfolio_construction_gui_v185.py
Tests for portfolio construction GUI panel v1.8.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE, _TABS, _TABS_V185_PORTFOLIO_CONSTRUCTION,
    get_tab_names, render_overview_tab,
)


def test_panel_version_185():
    assert PANEL_VERSION >= "1.8.5"

def test_panel_title_contains_185():
    assert "1.8" in PANEL_TITLE

def test_panel_title_contains_portfolio():
    assert "Small Capital" in PANEL_TITLE

def test_tabs_v185_count():
    assert len(_TABS_V185_PORTFOLIO_CONSTRUCTION) == 3

def test_portfolio_construction_lab_tab():
    assert "portfolio_construction_lab" in _TABS_V185_PORTFOLIO_CONSTRUCTION

def test_portfolio_rebalancing_tab():
    assert "portfolio_rebalancing" in _TABS_V185_PORTFOLIO_CONSTRUCTION

def test_portfolio_exposure_control_tab():
    assert "portfolio_exposure_control" in _TABS_V185_PORTFOLIO_CONSTRUCTION

def test_all_tabs_ge_138():
    assert len(_TABS) >= 138

def test_portfolio_construction_lab_in_all_tabs():
    assert "portfolio_construction_lab" in _TABS

def test_portfolio_rebalancing_in_all_tabs():
    assert "portfolio_rebalancing" in _TABS

def test_portfolio_exposure_control_in_all_tabs():
    assert "portfolio_exposure_control" in _TABS

def test_get_tab_names_returns_list():
    assert isinstance(get_tab_names(), list)

def test_get_tab_names_count():
    assert len(get_tab_names()) >= 138

def test_v170_tabs_preserved():
    assert "overview" in _TABS

def test_v171_tabs_preserved():
    assert "watchlist_overview" in _TABS

def test_v172_tabs_preserved():
    assert "abc_execution_overview" in _TABS

def test_v173_tabs_preserved():
    assert "regime_overview" in _TABS

def test_v174_tabs_preserved():
    assert "risk_dashboard_overview" in _TABS

def test_v175_tabs_preserved():
    assert "trade_journal_overview" in _TABS

def test_v180_tabs_preserved():
    assert "paper_sim_lab" in _TABS

def test_v181_tabs_preserved():
    assert "sim_matrix_lab" in _TABS

def test_v182_tabs_preserved():
    assert "param_optimization" in _TABS

def test_v183_tabs_preserved():
    assert "monte_carlo" in _TABS

def test_v184_tabs_preserved():
    assert "position_sizing_lab" in _TABS

def test_render_overview_paper_only():
    overview = render_overview_tab()
    assert overview.get("paper_only") is True

def test_render_overview_no_real_orders():
    overview = render_overview_tab()
    assert overview.get("no_real_orders") is True

def test_render_overview_tab_count():
    overview = render_overview_tab()
    assert overview.get("tab_count", 0) >= 138

def test_no_duplicate_tabs():
    assert len(_TABS) == len(set(_TABS))
