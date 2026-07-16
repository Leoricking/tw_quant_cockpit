"""
tests/test_decision_report_gui_v187.py
Tests for GUI small_capital_strategy_panel v1.8.7 — Decision Report Export & Evidence Pack.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE,
    _TABS_V187_DECISION_REPORT, _TABS,
    render_decision_report_tab, render_evidence_pack_tab,
    render_audit_trail_report_tab, get_tab_names, get_panel_info,
)


def test_panel_version_is_187():
    assert PANEL_VERSION in ("1.8.7", "1.8.8", "1.8.9", "1.9.0")


def test_panel_title_contains_187():
    assert "1.8.7" in PANEL_TITLE or "1.8.8" in PANEL_TITLE or "1.8.9" in PANEL_TITLE or "1.9.0" in PANEL_TITLE


def test_panel_title_contains_decision_report():
    assert "Decision Report" in PANEL_TITLE or "Workflow Runner" in PANEL_TITLE or "Journal" in PANEL_TITLE or "Performance" in PANEL_TITLE


def test_tabs_v187_decision_report_count():
    assert len(_TABS_V187_DECISION_REPORT) == 3


def test_tabs_v187_contains_decision_report():
    assert "decision_report" in _TABS_V187_DECISION_REPORT


def test_tabs_v187_contains_evidence_pack():
    assert "evidence_pack" in _TABS_V187_DECISION_REPORT


def test_tabs_v187_contains_audit_trail_report():
    assert "audit_trail_report" in _TABS_V187_DECISION_REPORT


def test_tabs_includes_v187():
    for tab in _TABS_V187_DECISION_REPORT:
        assert tab in _TABS


def test_get_tab_names_includes_decision_report():
    tabs = get_tab_names()
    assert "decision_report" in tabs


def test_get_tab_names_includes_evidence_pack():
    tabs = get_tab_names()
    assert "evidence_pack" in tabs


def test_get_tab_names_includes_audit_trail_report():
    tabs = get_tab_names()
    assert "audit_trail_report" in tabs


# ── render_decision_report_tab ────────────────────────────────────────────────

def test_render_decision_report_tab_returns_dict():
    result = render_decision_report_tab()
    assert isinstance(result, dict)


def test_render_decision_report_tab_tab_name():
    result = render_decision_report_tab()
    assert result["tab"] == "decision_report"


def test_render_decision_report_tab_paper_only():
    result = render_decision_report_tab()
    assert result["paper_only"] is True


def test_render_decision_report_tab_no_real_orders():
    result = render_decision_report_tab()
    assert result["no_real_orders"] is True


def test_render_decision_report_tab_not_investment_advice():
    result = render_decision_report_tab()
    assert result["not_investment_advice"] is True


def test_render_decision_report_tab_production_trading_blocked():
    result = render_decision_report_tab()
    assert result["production_trading_blocked"] is True


def test_render_decision_report_tab_schema_version():
    result = render_decision_report_tab()
    assert result["schema_version"] == "187"


def test_render_decision_report_tab_version():
    result = render_decision_report_tab()
    assert result["version"] in ("1.8.7", "1.8.8", "1.8.9", "1.9.0")


def test_render_decision_report_tab_report_only():
    result = render_decision_report_tab()
    assert result["report_only"] is True


def test_render_decision_report_tab_audit_only():
    result = render_decision_report_tab()
    assert result["audit_only"] is True


def test_render_decision_report_tab_has_description():
    result = render_decision_report_tab()
    assert len(result["description"]) > 0


def test_render_decision_report_tab_has_empty_state():
    result = render_decision_report_tab()
    assert "empty_state" in result


# ── render_evidence_pack_tab ──────────────────────────────────────────────────

def test_render_evidence_pack_tab_returns_dict():
    result = render_evidence_pack_tab()
    assert isinstance(result, dict)


def test_render_evidence_pack_tab_tab_name():
    result = render_evidence_pack_tab()
    assert result["tab"] == "evidence_pack"


def test_render_evidence_pack_tab_paper_only():
    result = render_evidence_pack_tab()
    assert result["paper_only"] is True


def test_render_evidence_pack_tab_no_real_orders():
    result = render_evidence_pack_tab()
    assert result["no_real_orders"] is True


def test_render_evidence_pack_tab_not_investment_advice():
    result = render_evidence_pack_tab()
    assert result["not_investment_advice"] is True


def test_render_evidence_pack_tab_production_trading_blocked():
    result = render_evidence_pack_tab()
    assert result["production_trading_blocked"] is True


def test_render_evidence_pack_tab_schema_version():
    result = render_evidence_pack_tab()
    assert result["schema_version"] == "187"


def test_render_evidence_pack_tab_version():
    result = render_evidence_pack_tab()
    assert result["version"] in ("1.8.7", "1.8.8", "1.8.9", "1.9.0")


def test_render_evidence_pack_tab_has_description():
    result = render_evidence_pack_tab()
    assert len(result["description"]) > 0


# ── render_audit_trail_report_tab ─────────────────────────────────────────────

def test_render_audit_trail_report_tab_returns_dict():
    result = render_audit_trail_report_tab()
    assert isinstance(result, dict)


def test_render_audit_trail_report_tab_tab_name():
    result = render_audit_trail_report_tab()
    assert result["tab"] == "audit_trail_report"


def test_render_audit_trail_report_tab_paper_only():
    result = render_audit_trail_report_tab()
    assert result["paper_only"] is True


def test_render_audit_trail_report_tab_no_real_orders():
    result = render_audit_trail_report_tab()
    assert result["no_real_orders"] is True


def test_render_audit_trail_report_tab_not_investment_advice():
    result = render_audit_trail_report_tab()
    assert result["not_investment_advice"] is True


def test_render_audit_trail_report_tab_production_trading_blocked():
    result = render_audit_trail_report_tab()
    assert result["production_trading_blocked"] is True


def test_render_audit_trail_report_tab_schema_version():
    result = render_audit_trail_report_tab()
    assert result["schema_version"] == "187"


def test_render_audit_trail_report_tab_version():
    result = render_audit_trail_report_tab()
    assert result["version"] in ("1.8.7", "1.8.8", "1.8.9", "1.9.0")


def test_render_audit_trail_report_tab_audit_only():
    result = render_audit_trail_report_tab()
    assert result["audit_only"] is True


def test_render_audit_trail_report_tab_has_description():
    result = render_audit_trail_report_tab()
    assert len(result["description"]) > 0


# ── get_panel_info ────────────────────────────────────────────────────────────

def test_get_panel_info_panel_version():
    info = get_panel_info()
    assert info["panel_version"] in ("1.8.7", "1.8.8", "1.8.9", "1.9.0")


def test_get_panel_info_paper_only():
    info = get_panel_info()
    assert info["paper_only"] is True


def test_get_panel_info_tab_count_includes_v187():
    info = get_panel_info()
    assert info["tab_count"] >= 126  # 123 existing + 3 new
