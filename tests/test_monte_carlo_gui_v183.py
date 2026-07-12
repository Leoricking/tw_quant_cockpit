"""
tests/test_monte_carlo_gui_v183.py
Tests for Monte Carlo GUI panel tabs v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from gui.small_capital_strategy_panel import (
    PANEL_VERSION,
    _TABS_V183_MONTE_CARLO,
    get_tab_names,
    get_monte_carlo_tab_names,
    render_monte_carlo_tab,
    render_risk_of_ruin_tab,
    render_robustness_probability_tab,
    get_panel_info,
)


# ---------------------------------------------------------------------------
# Panel version
# ---------------------------------------------------------------------------

def test_panel_version_is_183():
    assert PANEL_VERSION == "1.8.3"


# ---------------------------------------------------------------------------
# _TABS_V183_MONTE_CARLO constant
# ---------------------------------------------------------------------------

def test_tabs_v183_monte_carlo_is_list():
    assert isinstance(_TABS_V183_MONTE_CARLO, list)


def test_tabs_v183_monte_carlo_count_3():
    assert len(_TABS_V183_MONTE_CARLO) == 3


def test_tabs_v183_monte_carlo_contains_monte_carlo():
    assert "monte_carlo" in _TABS_V183_MONTE_CARLO


def test_tabs_v183_monte_carlo_contains_risk_of_ruin():
    assert "risk_of_ruin" in _TABS_V183_MONTE_CARLO


def test_tabs_v183_monte_carlo_contains_robustness_probability():
    assert "robustness_probability" in _TABS_V183_MONTE_CARLO


# ---------------------------------------------------------------------------
# get_tab_names()
# ---------------------------------------------------------------------------

def test_get_tab_names_returns_list():
    assert isinstance(get_tab_names(), list)


def test_get_tab_names_contains_monte_carlo():
    assert "monte_carlo" in get_tab_names()


def test_get_tab_names_contains_risk_of_ruin():
    assert "risk_of_ruin" in get_tab_names()


def test_get_tab_names_contains_robustness_probability():
    assert "robustness_probability" in get_tab_names()


# ---------------------------------------------------------------------------
# get_monte_carlo_tab_names()
# ---------------------------------------------------------------------------

def test_get_monte_carlo_tab_names_returns_list():
    assert isinstance(get_monte_carlo_tab_names(), list)


def test_get_monte_carlo_tab_names_exact():
    assert get_monte_carlo_tab_names() == ["monte_carlo", "risk_of_ruin", "robustness_probability"]


# ---------------------------------------------------------------------------
# render_monte_carlo_tab()
# ---------------------------------------------------------------------------

def test_render_monte_carlo_tab_returns_dict():
    assert isinstance(render_monte_carlo_tab(), dict)


def test_render_monte_carlo_tab_paper_only():
    assert render_monte_carlo_tab()["paper_only"] is True


def test_render_monte_carlo_tab_monte_carlo_only():
    assert render_monte_carlo_tab()["monte_carlo_only"] is True


def test_render_monte_carlo_tab_headless_safe():
    assert render_monte_carlo_tab()["headless_safe"] is True


def test_render_monte_carlo_tab_version():
    assert render_monte_carlo_tab()["version"] == "1.8.3"


# ---------------------------------------------------------------------------
# render_risk_of_ruin_tab()
# ---------------------------------------------------------------------------

def test_render_risk_of_ruin_tab_returns_dict():
    assert isinstance(render_risk_of_ruin_tab(), dict)


def test_render_risk_of_ruin_tab_paper_only():
    assert render_risk_of_ruin_tab()["paper_only"] is True


def test_render_risk_of_ruin_tab_headless_safe():
    assert render_risk_of_ruin_tab()["headless_safe"] is True


# ---------------------------------------------------------------------------
# render_robustness_probability_tab()
# ---------------------------------------------------------------------------

def test_render_robustness_probability_tab_returns_dict():
    assert isinstance(render_robustness_probability_tab(), dict)


def test_render_robustness_probability_tab_paper_only():
    assert render_robustness_probability_tab()["paper_only"] is True


def test_render_robustness_probability_tab_headless_safe():
    assert render_robustness_probability_tab()["headless_safe"] is True


# ---------------------------------------------------------------------------
# get_panel_info()
# ---------------------------------------------------------------------------

def test_get_panel_info_panel_version():
    assert get_panel_info()["panel_version"] == "1.8.3"


def test_get_panel_info_paper_only():
    assert get_panel_info()["paper_only"] is True
