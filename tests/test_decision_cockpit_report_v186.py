"""
tests/test_decision_cockpit_report_v186.py
Tests for decision_cockpit_report_v186 module.
[!] Research Only. Paper Only. Decision Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_cockpit_report_v186 import (
    REPORT_SECTIONS, get_report_sections, build_report,
)
from paper_trading.small_capital_strategy.decision_cockpit_engine_v186 import (
    build_decision_dashboard,
)
from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import (
    DecisionCockpitInput,
)


def test_report_sections_count():
    assert len(REPORT_SECTIONS) == 20

def test_report_sections_has_version():
    assert "version" in REPORT_SECTIONS

def test_report_sections_has_safety():
    assert "safety" in REPORT_SECTIONS

def test_report_sections_has_daily_decision():
    assert "daily_decision" in REPORT_SECTIONS

def test_report_sections_has_weekly_decision():
    assert "weekly_decision" in REPORT_SECTIONS

def test_report_sections_has_buy_point():
    assert "buy_point_assessment" in REPORT_SECTIONS

def test_report_sections_has_risk():
    assert "risk_decision" in REPORT_SECTIONS

def test_report_sections_has_monte_carlo():
    assert "monte_carlo_decision" in REPORT_SECTIONS

def test_report_sections_has_block_reasons():
    assert "block_reasons" in REPORT_SECTIONS

def test_report_sections_has_cockpit_grade():
    assert "cockpit_grade" in REPORT_SECTIONS

def test_report_sections_has_summary():
    assert "summary" in REPORT_SECTIONS

def test_get_report_sections_returns_list():
    assert isinstance(get_report_sections(), list)

def test_get_report_sections_count():
    assert len(get_report_sections()) == 20

def test_get_report_sections_matches_constant():
    assert get_report_sections() == list(REPORT_SECTIONS)

def test_build_report_callable():
    inp = DecisionCockpitInput()
    dash = build_decision_dashboard(inp)
    report = build_report(dash)
    assert report is not None

def test_build_report_paper_only():
    inp = DecisionCockpitInput()
    dash = build_decision_dashboard(inp)
    report = build_report(dash)
    assert report.paper_only is True

def test_build_report_decision_only():
    inp = DecisionCockpitInput()
    dash = build_decision_dashboard(inp)
    report = build_report(dash)
    assert report.decision_only is True

def test_build_report_no_real_orders():
    inp = DecisionCockpitInput()
    dash = build_decision_dashboard(inp)
    report = build_report(dash)
    assert report.no_real_orders is True

def test_build_report_no_broker():
    inp = DecisionCockpitInput()
    dash = build_decision_dashboard(inp)
    report = build_report(dash)
    assert report.no_broker is True

def test_build_report_version():
    inp = DecisionCockpitInput()
    dash = build_decision_dashboard(inp)
    report = build_report(dash)
    assert report.version == "1.8.6"

def test_build_report_release_name():
    inp = DecisionCockpitInput()
    dash = build_decision_dashboard(inp)
    report = build_report(dash)
    assert report.release_name == "End-to-End Small Capital Decision Cockpit"

def test_build_report_sections_count():
    inp = DecisionCockpitInput()
    dash = build_decision_dashboard(inp)
    report = build_report(dash)
    assert len(report.sections) == 20

def test_build_report_production_blocked():
    inp = DecisionCockpitInput()
    dash = build_decision_dashboard(inp)
    report = build_report(dash)
    assert report.production_trading_blocked is True

def test_build_report_not_investment_advice():
    inp = DecisionCockpitInput()
    dash = build_decision_dashboard(inp)
    report = build_report(dash)
    assert report.not_investment_advice is True

def test_build_report_demo_only():
    inp = DecisionCockpitInput()
    dash = build_decision_dashboard(inp)
    report = build_report(dash)
    assert report.demo_only is True
