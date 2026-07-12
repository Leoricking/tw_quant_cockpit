"""
tests/test_position_sizing_report_v184.py
Tests for position_sizing_report_v184 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.position_sizing_report_v184 import (
    REPORT_SECTIONS, get_report_sections, build_report,
)
from paper_trading.small_capital_strategy.position_sizing_models_v184 import (
    PositionSizingDashboard, PositionSizingInput,
)
from paper_trading.small_capital_strategy.position_sizing_engine_v184 import (
    build_position_sizing_dashboard,
)


def _make_dashboard():
    inp = PositionSizingInput(capital=300000.0, per_trade_risk_pct=1.0,
                              stop_loss_distance_pct=7.0, has_stop_loss=True)
    return build_position_sizing_dashboard(inp)


def test_report_sections_is_list():
    assert isinstance(REPORT_SECTIONS, list)

def test_report_sections_count_12():
    assert len(REPORT_SECTIONS) == 12

def test_report_sections_contains_version():
    assert "version" in REPORT_SECTIONS

def test_report_sections_contains_safety():
    assert "safety" in REPORT_SECTIONS

def test_report_sections_contains_capital_profile():
    assert "capital_profile" in REPORT_SECTIONS

def test_report_sections_contains_risk_budget():
    assert "risk_budget" in REPORT_SECTIONS

def test_report_sections_contains_engine():
    assert "position_sizing_engine" in REPORT_SECTIONS

def test_report_sections_contains_abc():
    assert "abc_staged_sizing" in REPORT_SECTIONS

def test_report_sections_contains_exposure():
    assert "exposure_limits" in REPORT_SECTIONS

def test_report_sections_contains_concentration():
    assert "concentration_risk" in REPORT_SECTIONS

def test_report_sections_contains_drawdown():
    assert "drawdown_budget" in REPORT_SECTIONS

def test_report_sections_contains_cash():
    assert "cash_reserve" in REPORT_SECTIONS

def test_report_sections_contains_capital_stage():
    assert "capital_stage_plan" in REPORT_SECTIONS

def test_report_sections_contains_summary():
    assert "summary" in REPORT_SECTIONS

def test_get_report_sections_returns_list():
    assert isinstance(get_report_sections(), list)

def test_get_report_sections_count_12():
    assert len(get_report_sections()) == 12

def test_build_report_returns_report():
    from paper_trading.small_capital_strategy.position_sizing_models_v184 import PositionSizingReport
    rpt = build_report(_make_dashboard())
    assert isinstance(rpt, PositionSizingReport)

def test_build_report_paper_only():
    assert build_report(_make_dashboard()).paper_only is True

def test_build_report_allocation_only():
    assert build_report(_make_dashboard()).allocation_only is True

def test_build_report_no_real_orders():
    assert build_report(_make_dashboard()).no_real_orders is True

def test_build_report_version():
    assert build_report(_make_dashboard()).version == "1.8.4"

def test_build_report_sections_count():
    rpt = build_report(_make_dashboard())
    assert len(rpt.sections) == 12

def test_build_report_all_checks_pass():
    assert build_report(_make_dashboard()).all_checks_pass is True

def test_build_report_release_name():
    rpt = build_report(_make_dashboard())
    assert rpt.release_name == "Position Sizing & Capital Allocation Lab"

def test_build_report_not_investment_advice():
    assert build_report(_make_dashboard()).not_investment_advice is True

def test_build_report_no_broker():
    assert build_report(_make_dashboard()).no_broker is True

def test_build_report_no_margin():
    assert build_report(_make_dashboard()).no_margin is True

def test_build_report_no_leverage():
    assert build_report(_make_dashboard()).no_leverage is True
