"""
tests/test_portfolio_construction_report_v185.py
Tests for portfolio_construction_report_v185 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_construction_report_v185 import (
    REPORT_SECTIONS, get_report_sections, build_report,
)
from paper_trading.small_capital_strategy.portfolio_construction_engine_v185 import (
    build_portfolio_dashboard,
)
from paper_trading.small_capital_strategy.portfolio_construction_models_v185 import (
    PortfolioConstructionInput, PortfolioDashboard,
)


def test_report_sections_count():
    assert len(REPORT_SECTIONS) == 15

def test_get_report_sections_list():
    assert isinstance(get_report_sections(), list)

def test_get_report_sections_count():
    assert len(get_report_sections()) == 15

def test_report_sections_has_version():
    assert "version" in REPORT_SECTIONS

def test_report_sections_has_safety():
    assert "safety" in REPORT_SECTIONS

def test_report_sections_has_portfolio_profile():
    assert "portfolio_profile" in REPORT_SECTIONS

def test_report_sections_has_portfolio_construction():
    assert "portfolio_construction" in REPORT_SECTIONS

def test_report_sections_has_exposure_control():
    assert "exposure_control" in REPORT_SECTIONS

def test_report_sections_has_sector_risk():
    assert "sector_risk" in REPORT_SECTIONS

def test_report_sections_has_theme_risk():
    assert "theme_risk" in REPORT_SECTIONS

def test_report_sections_has_correlation_risk():
    assert "correlation_risk" in REPORT_SECTIONS

def test_report_sections_has_diversification():
    assert "diversification_score" in REPORT_SECTIONS

def test_report_sections_has_rebalance_plan():
    assert "rebalance_plan" in REPORT_SECTIONS

def test_report_sections_has_summary():
    assert "summary" in REPORT_SECTIONS

def test_build_report_paper_only():
    dash = build_portfolio_dashboard(PortfolioConstructionInput(capital=300000.0))
    rpt = build_report(dash)
    assert rpt.paper_only is True

def test_build_report_portfolio_only():
    dash = build_portfolio_dashboard(PortfolioConstructionInput(capital=300000.0))
    rpt = build_report(dash)
    assert rpt.portfolio_only is True

def test_build_report_no_real_orders():
    dash = build_portfolio_dashboard(PortfolioConstructionInput(capital=300000.0))
    rpt = build_report(dash)
    assert rpt.no_real_orders is True

def test_build_report_version():
    dash = build_portfolio_dashboard(PortfolioConstructionInput(capital=300000.0))
    rpt = build_report(dash)
    assert rpt.version == "1.8.5"

def test_build_report_release_name():
    dash = build_portfolio_dashboard(PortfolioConstructionInput(capital=300000.0))
    rpt = build_report(dash)
    assert rpt.release_name == "Portfolio Construction & Rebalancing Lab"

def test_build_report_sections_present():
    dash = build_portfolio_dashboard(PortfolioConstructionInput(capital=300000.0))
    rpt = build_report(dash)
    assert len(rpt.sections) == 15

def test_build_report_all_checks_pass():
    dash = build_portfolio_dashboard(PortfolioConstructionInput(capital=300000.0))
    rpt = build_report(dash)
    assert rpt.all_checks_pass is True

def test_build_report_schema_version():
    dash = build_portfolio_dashboard(PortfolioConstructionInput(capital=300000.0))
    rpt = build_report(dash)
    assert rpt.schema_version == "185"

def test_build_report_from_none_dashboard():
    rpt = build_report(None)
    assert rpt.paper_only is True

def test_build_report_no_margin():
    dash = build_portfolio_dashboard(PortfolioConstructionInput(capital=500000.0))
    rpt = build_report(dash)
    assert rpt.no_margin is True

def test_build_report_no_leverage():
    dash = build_portfolio_dashboard(PortfolioConstructionInput(capital=1000000.0))
    rpt = build_report(dash)
    assert rpt.no_leverage is True
