"""
tests/test_integrated_strategy_report_v178.py
Tests for build_report() and get_report_sections() — v1.7.8.
[!] Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
    IntegratedDecisionAction,
    IntegratedRegimeStatus,
    IntegratedWatchlistStatus,
    IntegratedABCStatus,
    IntegratedThemeStatus,
    IntegratedRiskLevel,
    IntegratedBehaviorStatus,
    IntegratedScoreGrade,
)
from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
    IntegratedStrategyInput,
    IntegratedDashboard,
    IntegratedStrategyReport,
)
from paper_trading.small_capital_strategy.integrated_strategy_engine_v178 import (
    build_integrated_dashboard,
)
from paper_trading.small_capital_strategy.integrated_strategy_report_v178 import (
    build_report,
    get_report_sections,
)

# ---------------------------------------------------------------------------
# Safety invariants
# ---------------------------------------------------------------------------
paper_only = True
no_real_orders = True
no_broker = True
not_investment_advice = True


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _good_dashboard() -> IntegratedDashboard:
    inp = IntegratedStrategyInput(
        symbol="2330",
        date="2026-07-10",
        has_stop_loss=True,
        regime_status=IntegratedRegimeStatus.BULL,
        theme_status=IntegratedThemeStatus.LEADER,
        watchlist_status=IntegratedWatchlistStatus.FOCUS,
        abc_status=IntegratedABCStatus.A_READY,
        risk_level=IntegratedRiskLevel.SAFE,
        behavior_status=IntegratedBehaviorStatus.CLEAN,
        theme_score=90.0,
        watchlist_score=90.0,
        abc_score=90.0,
        regime_score=90.0,
        risk_score=90.0,
        behavior_score=90.0,
        journal_quality_score=80.0,
    )
    return build_integrated_dashboard(inp)


def _section_by_name(report: IntegratedStrategyReport, name: str) -> dict:
    """Find a section dict by its name field."""
    for s in report.sections:
        if s.get("name") == name:
            return s
    raise KeyError(f"Section '{name}' not found in report.sections")


# ===========================================================================
# get_report_sections() — 7 tests
# ===========================================================================

def test_get_report_sections_returns_list_with_6_items():
    sections = get_report_sections()
    assert len(sections) == 6


def test_get_report_sections_contains_executive_summary():
    assert "executive_summary" in get_report_sections()


def test_get_report_sections_contains_scorecard_detail():
    assert "scorecard_detail" in get_report_sections()


def test_get_report_sections_contains_subsystem_status():
    assert "subsystem_status" in get_report_sections()


def test_get_report_sections_contains_no_trade_reasons():
    assert "no_trade_reasons" in get_report_sections()


def test_get_report_sections_contains_paper_plan_summary():
    assert "paper_plan_summary" in get_report_sections()


def test_get_report_sections_contains_safety_disclaimer():
    assert "safety_disclaimer" in get_report_sections()


# ===========================================================================
# build_report() — return type and top-level flags — 8 tests
# ===========================================================================

def test_build_report_returns_integrated_strategy_report():
    report = build_report(_good_dashboard())
    assert isinstance(report, IntegratedStrategyReport)


def test_build_report_paper_only_is_true():
    report = build_report(_good_dashboard())
    assert report.paper_only is True


def test_build_report_no_real_orders_is_true():
    report = build_report(_good_dashboard())
    assert report.no_real_orders is True


def test_build_report_no_broker_is_true():
    report = build_report(_good_dashboard())
    assert report.no_broker is True


def test_build_report_not_investment_advice_is_true():
    report = build_report(_good_dashboard())
    assert report.not_investment_advice is True


def test_build_report_demo_only_is_true():
    report = build_report(_good_dashboard())
    assert report.demo_only is True


def test_build_report_not_for_production_is_true():
    report = build_report(_good_dashboard())
    assert report.not_for_production is True


def test_build_report_report_format_is_text():
    report = build_report(_good_dashboard())
    assert report.report_format == "text"


# ===========================================================================
# build_report() — content and structure — 8 tests
# ===========================================================================

def test_build_report_sections_has_at_least_6_items():
    report = build_report(_good_dashboard())
    assert len(report.sections) >= 6


def test_build_report_first_section_name_is_executive_summary():
    report = build_report(_good_dashboard())
    assert report.sections[0]["name"] == "executive_summary"


def test_build_report_second_section_name_is_scorecard_detail():
    report = build_report(_good_dashboard())
    assert report.sections[1]["name"] == "scorecard_detail"


def test_build_report_last_section_name_is_safety_disclaimer():
    report = build_report(_good_dashboard())
    assert report.sections[-1]["name"] == "safety_disclaimer"


def test_build_report_action_is_valid_decision_action_member():
    report = build_report(_good_dashboard())
    assert report.action in list(IntegratedDecisionAction)


def test_build_report_summary_is_string():
    report = build_report(_good_dashboard())
    assert isinstance(report.summary, str)


def test_build_report_final_score_in_valid_range():
    report = build_report(_good_dashboard())
    assert 0.0 <= report.final_score <= 100.0


def test_build_report_grade_is_not_none():
    report = build_report(_good_dashboard())
    assert report.grade is not None


# ===========================================================================
# Section-level flag tests — 5 tests
# ===========================================================================

def test_build_report_executive_summary_section_paper_only_is_true():
    report = build_report(_good_dashboard())
    s = _section_by_name(report, "executive_summary")
    assert s["paper_only"] is True


def test_build_report_safety_disclaimer_section_no_real_orders_is_true():
    report = build_report(_good_dashboard())
    s = _section_by_name(report, "safety_disclaimer")
    assert s["no_real_orders"] is True


def test_build_report_safety_disclaimer_section_demo_only_is_true():
    report = build_report(_good_dashboard())
    s = _section_by_name(report, "safety_disclaimer")
    assert s["demo_only"] is True


def test_build_report_safety_disclaimer_section_not_for_production_is_true():
    report = build_report(_good_dashboard())
    s = _section_by_name(report, "safety_disclaimer")
    assert s["not_for_production"] is True


def test_build_report_safety_disclaimer_section_disclaimer_contains_paper_only():
    report = build_report(_good_dashboard())
    s = _section_by_name(report, "safety_disclaimer")
    assert "PAPER ONLY" in s["disclaimer"]


# ===========================================================================
# paper_plan_summary section — 2 tests
# ===========================================================================

def test_build_report_paper_plan_summary_broker_execution_enabled_is_false():
    report = build_report(_good_dashboard())
    s = _section_by_name(report, "paper_plan_summary")
    assert s["broker_execution_enabled"] is False


def test_build_report_paper_plan_summary_no_real_orders_is_true():
    report = build_report(_good_dashboard())
    s = _section_by_name(report, "paper_plan_summary")
    assert s["no_real_orders"] is True


# ===========================================================================
# Empty dashboard graceful handling — 1 test
# ===========================================================================

def test_build_report_empty_dashboard_does_not_crash():
    """
    An IntegratedDashboard with all None fields should not raise an exception.
    """
    dashboard = IntegratedDashboard()
    report = build_report(dashboard)
    assert isinstance(report, IntegratedStrategyReport)
