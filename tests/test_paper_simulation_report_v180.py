"""tests/test_paper_simulation_report_v180.py — v1.8.0 Paper Simulation report tests"""
from __future__ import annotations

import pytest

from paper_trading.small_capital_strategy.paper_simulation_report_v180 import (
    build_simulation_report,
    build_dashboard_report,
    get_report_section_names,
    get_report_info,
    REPORT_SECTIONS,
    _DISCLAIMER,
)
from paper_trading.small_capital_strategy.paper_simulation_models_v180 import (
    PaperSimulationInput,
    PaperSimulationResult,
    PaperPerformanceMetrics,
    PaperEquityCurve,
    PaperDrawdownReport,
    PaperRiskReport,
)


# ---------------------------------------------------------------------------
# REPORT_SECTIONS constant
# ---------------------------------------------------------------------------

def test_report_sections_is_list() -> None:
    assert isinstance(REPORT_SECTIONS, list)


def test_report_sections_length_at_least_10() -> None:
    assert len(REPORT_SECTIONS) >= 10


def test_performance_metrics_in_report_sections() -> None:
    assert "performance_metrics" in REPORT_SECTIONS


def test_equity_curve_in_report_sections() -> None:
    assert "equity_curve" in REPORT_SECTIONS


def test_drawdown_report_in_report_sections() -> None:
    assert "drawdown_report" in REPORT_SECTIONS


def test_risk_report_in_report_sections() -> None:
    assert "risk_report" in REPORT_SECTIONS


def test_version_in_report_sections() -> None:
    assert "version" in REPORT_SECTIONS


# ---------------------------------------------------------------------------
# _DISCLAIMER constant
# ---------------------------------------------------------------------------

def test_disclaimer_contains_research_only() -> None:
    assert "Research Only" in _DISCLAIMER


def test_disclaimer_contains_paper_only() -> None:
    assert "Paper Only" in _DISCLAIMER


def test_disclaimer_contains_no_real_orders() -> None:
    assert "No Real Orders" in _DISCLAIMER


# ---------------------------------------------------------------------------
# get_report_info
# ---------------------------------------------------------------------------

def test_get_report_info_returns_dict() -> None:
    assert isinstance(get_report_info(), dict)


def test_get_report_info_paper_only_true() -> None:
    assert get_report_info()["paper_only"] is True


def test_get_report_info_section_count_at_least_10() -> None:
    assert get_report_info()["section_count"] >= 10


def test_get_report_info_no_real_orders_true() -> None:
    assert get_report_info()["no_real_orders"] is True


def test_get_report_info_sections_key_present() -> None:
    assert "sections" in get_report_info()


# ---------------------------------------------------------------------------
# get_report_section_names
# ---------------------------------------------------------------------------

def test_get_report_section_names_equals_report_sections() -> None:
    assert get_report_section_names() == REPORT_SECTIONS


def test_get_report_section_names_returns_list() -> None:
    assert isinstance(get_report_section_names(), list)


# ---------------------------------------------------------------------------
# build_dashboard_report
# ---------------------------------------------------------------------------

def test_build_dashboard_report_returns_dict() -> None:
    result = build_dashboard_report(scenario_count=5, total_trades=10, final_grade="B")
    assert isinstance(result, dict)


def test_build_dashboard_report_paper_only_true() -> None:
    result = build_dashboard_report()
    assert result["paper_only"] is True


def test_build_dashboard_report_no_real_orders_true() -> None:
    result = build_dashboard_report()
    assert result["no_real_orders"] is True


def test_build_dashboard_report_production_trading_blocked_true() -> None:
    result = build_dashboard_report()
    assert result["production_trading_blocked"] is True


def test_build_dashboard_report_grade_a_reflected() -> None:
    result = build_dashboard_report(final_grade="A")
    assert result["final_grade"] == "A"


def test_build_dashboard_report_scenario_count_reflected() -> None:
    result = build_dashboard_report(scenario_count=70)
    assert result["scenario_count"] == 70


def test_build_dashboard_report_total_trades_reflected() -> None:
    result = build_dashboard_report(total_trades=42)
    assert result["total_trades"] == 42


def test_build_dashboard_report_default_grade_b() -> None:
    result = build_dashboard_report()
    assert result["final_grade"] == "B"


# ---------------------------------------------------------------------------
# build_simulation_report
# ---------------------------------------------------------------------------

def _default_report() -> dict:
    result = PaperSimulationResult()
    metrics = PaperPerformanceMetrics()
    equity_curve = PaperEquityCurve(values=[300000.0], drawdowns=[0.0], dates=["D000"])
    drawdown = PaperDrawdownReport()
    risk_report = PaperRiskReport()
    return build_simulation_report(result, metrics, equity_curve, drawdown, risk_report)


def test_build_simulation_report_returns_dict() -> None:
    assert isinstance(_default_report(), dict)


def test_build_simulation_report_paper_only_true() -> None:
    assert _default_report()["paper_only"] is True


def test_build_simulation_report_has_simulation_summary() -> None:
    assert "simulation_summary" in _default_report()


def test_build_simulation_report_has_performance_metrics() -> None:
    assert "performance_metrics" in _default_report()


def test_build_simulation_report_has_disclaimer() -> None:
    assert "disclaimer" in _default_report()


def test_build_simulation_report_disclaimer_contains_research_only() -> None:
    assert "Research Only" in _default_report()["disclaimer"]


def test_build_simulation_report_regime_performance_empty_by_default() -> None:
    assert _default_report()["regime_performance"] == []


def test_build_simulation_report_no_real_orders_true() -> None:
    assert _default_report()["no_real_orders"] is True


def test_build_simulation_report_not_investment_advice_true() -> None:
    assert _default_report()["not_investment_advice"] is True


def test_build_simulation_report_sections_key_present() -> None:
    assert "sections" in _default_report()


def test_build_simulation_report_theme_performance_empty_by_default() -> None:
    assert _default_report()["theme_performance"] == []


def test_build_simulation_report_abc_performance_empty_by_default() -> None:
    assert _default_report()["abc_performance"] == []
