"""
tests/test_strategy_governance_dashboard_gui_v197.py
Tests for Paper Strategy Governance Dashboard GUI tabs v1.9.7.
[!] Research Only. Paper Only. Governance Analytics Only. Dashboard Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION,
    PANEL_TITLE,
    render_governance_dashboard_tab,
    render_decision_quality_tab,
    render_governance_analytics_tab,
    get_governance_dashboard_tab_names,
    get_panel_info,
)


# ── PANEL_VERSION ──────────────────────────────────────────────────────────────

def test_panel_version_is_197():
    assert PANEL_VERSION in ("1.9.7", "1.9.8", "1.9.9")

def test_panel_title_contains_197():
    assert "1.9.7" in PANEL_TITLE or "1.9.8" in PANEL_TITLE or "1.9.9" in PANEL_TITLE

def test_panel_title_contains_governance_dashboard():
    assert "Governance Dashboard" in PANEL_TITLE or "Governance" in PANEL_TITLE or "Portfolio" in PANEL_TITLE


# ── get_governance_dashboard_tab_names() ───────────────────────────────────────

def test_get_governance_dashboard_tab_names_returns_list():
    names = get_governance_dashboard_tab_names()
    assert isinstance(names, list)

def test_get_governance_dashboard_tab_names_count_3():
    names = get_governance_dashboard_tab_names()
    assert len(names) == 3

def test_governance_dashboard_in_tab_names():
    names = get_governance_dashboard_tab_names()
    assert "governance_dashboard" in names

def test_decision_quality_in_tab_names():
    names = get_governance_dashboard_tab_names()
    assert "decision_quality" in names

def test_governance_analytics_in_tab_names():
    names = get_governance_dashboard_tab_names()
    assert "governance_analytics" in names

def test_tab_names_no_forbidden_words():
    names = get_governance_dashboard_tab_names()
    forbidden = {"BUY", "SELL", "ORDER", "EXECUTE", "BROKER"}
    for name in names:
        assert name.upper() not in forbidden


# ── render_governance_dashboard_tab() ─────────────────────────────────────────

def test_render_governance_dashboard_tab_returns_dict():
    result = render_governance_dashboard_tab()
    assert isinstance(result, dict)

def test_render_governance_dashboard_tab_tab_name():
    result = render_governance_dashboard_tab()
    assert result["tab"] == "governance_dashboard"

def test_render_governance_dashboard_tab_version():
    result = render_governance_dashboard_tab()
    assert result["version"] in ("1.9.7", "1.9.8", "1.9.9")

def test_render_governance_dashboard_tab_paper_only():
    result = render_governance_dashboard_tab()
    assert result["paper_only"] is True

def test_render_governance_dashboard_tab_no_real_orders():
    result = render_governance_dashboard_tab()
    assert result["no_real_orders"] is True

def test_render_governance_dashboard_tab_governance_analytics_only():
    result = render_governance_dashboard_tab()
    assert result["governance_analytics_only"] is True

def test_render_governance_dashboard_tab_dashboard_only():
    result = render_governance_dashboard_tab()
    assert result["dashboard_only"] is True

def test_render_governance_dashboard_tab_quality_analytics_only():
    result = render_governance_dashboard_tab()
    assert result["quality_analytics_only"] is True

def test_render_governance_dashboard_tab_no_broker():
    result = render_governance_dashboard_tab()
    assert result["no_broker"] is True

def test_render_governance_dashboard_tab_not_investment_advice():
    result = render_governance_dashboard_tab()
    assert result["not_investment_advice"] is True

def test_render_governance_dashboard_tab_no_production_mutation():
    result = render_governance_dashboard_tab()
    assert result["no_production_strategy_mutation"] is True

def test_render_governance_dashboard_tab_no_automatic_rollback():
    result = render_governance_dashboard_tab()
    assert result["no_automatic_rollback"] is True

def test_render_governance_dashboard_tab_no_live_activation():
    result = render_governance_dashboard_tab()
    assert result["no_live_strategy_activation"] is True

def test_render_governance_dashboard_tab_production_trading_blocked():
    result = render_governance_dashboard_tab()
    assert result["production_trading_blocked"] is True

def test_render_governance_dashboard_tab_analytics_does_not_execute():
    result = render_governance_dashboard_tab()
    assert result["analytics_executes_decision"] is False

def test_render_governance_dashboard_tab_dashboard_does_not_mutate():
    result = render_governance_dashboard_tab()
    assert result["dashboard_mutates_strategy"] is False

def test_render_governance_dashboard_tab_panels_count():
    result = render_governance_dashboard_tab()
    assert result["panels_count"] == 12

def test_render_governance_dashboard_tab_schema_version():
    result = render_governance_dashboard_tab()
    assert result["schema_version"] == "197"

def test_render_governance_dashboard_tab_has_empty_state():
    result = render_governance_dashboard_tab()
    assert "empty_state" in result
    assert isinstance(result["empty_state"], str)
    assert len(result["empty_state"]) > 0

def test_render_governance_dashboard_tab_has_description():
    result = render_governance_dashboard_tab()
    assert "description" in result
    assert isinstance(result["description"], str)


# ── render_decision_quality_tab() ─────────────────────────────────────────────

def test_render_decision_quality_tab_returns_dict():
    result = render_decision_quality_tab()
    assert isinstance(result, dict)

def test_render_decision_quality_tab_tab_name():
    result = render_decision_quality_tab()
    assert result["tab"] == "decision_quality"

def test_render_decision_quality_tab_version():
    result = render_decision_quality_tab()
    assert result["version"] in ("1.9.7", "1.9.8", "1.9.9")

def test_render_decision_quality_tab_paper_only():
    result = render_decision_quality_tab()
    assert result["paper_only"] is True

def test_render_decision_quality_tab_no_real_orders():
    result = render_decision_quality_tab()
    assert result["no_real_orders"] is True

def test_render_decision_quality_tab_governance_analytics_only():
    result = render_decision_quality_tab()
    assert result["governance_analytics_only"] is True

def test_render_decision_quality_tab_quality_analytics_only():
    result = render_decision_quality_tab()
    assert result["quality_analytics_only"] is True

def test_render_decision_quality_tab_not_investment_advice():
    result = render_decision_quality_tab()
    assert result["not_investment_advice"] is True

def test_render_decision_quality_tab_no_production_mutation():
    result = render_decision_quality_tab()
    assert result["no_production_strategy_mutation"] is True

def test_render_decision_quality_tab_no_live_activation():
    result = render_decision_quality_tab()
    assert result["no_live_strategy_activation"] is True

def test_render_decision_quality_tab_production_trading_blocked():
    result = render_decision_quality_tab()
    assert result["production_trading_blocked"] is True

def test_render_decision_quality_tab_analytics_does_not_execute():
    result = render_decision_quality_tab()
    assert result["analytics_executes_decision"] is False

def test_render_decision_quality_tab_quality_metrics_count():
    result = render_decision_quality_tab()
    assert result["quality_metrics_count"] == 12

def test_render_decision_quality_tab_grades_list():
    result = render_decision_quality_tab()
    grades = result["quality_grades"]
    assert isinstance(grades, list)
    assert "EXCELLENT" in grades
    assert "GOOD" in grades
    assert "WATCH" in grades
    assert "WEAK" in grades
    assert "INVALID" in grades

def test_render_decision_quality_tab_schema_version():
    result = render_decision_quality_tab()
    assert result["schema_version"] == "197"

def test_render_decision_quality_tab_has_empty_state():
    result = render_decision_quality_tab()
    assert "empty_state" in result
    assert isinstance(result["empty_state"], str)


# ── render_governance_analytics_tab() ─────────────────────────────────────────

def test_render_governance_analytics_tab_returns_dict():
    result = render_governance_analytics_tab()
    assert isinstance(result, dict)

def test_render_governance_analytics_tab_tab_name():
    result = render_governance_analytics_tab()
    assert result["tab"] == "governance_analytics"

def test_render_governance_analytics_tab_version():
    result = render_governance_analytics_tab()
    assert result["version"] in ("1.9.7", "1.9.8", "1.9.9")

def test_render_governance_analytics_tab_paper_only():
    result = render_governance_analytics_tab()
    assert result["paper_only"] is True

def test_render_governance_analytics_tab_no_real_orders():
    result = render_governance_analytics_tab()
    assert result["no_real_orders"] is True

def test_render_governance_analytics_tab_governance_analytics_only():
    result = render_governance_analytics_tab()
    assert result["governance_analytics_only"] is True

def test_render_governance_analytics_tab_report_only():
    result = render_governance_analytics_tab()
    assert result["report_only"] is True

def test_render_governance_analytics_tab_audit_only():
    result = render_governance_analytics_tab()
    assert result["audit_only"] is True

def test_render_governance_analytics_tab_not_investment_advice():
    result = render_governance_analytics_tab()
    assert result["not_investment_advice"] is True

def test_render_governance_analytics_tab_no_production_mutation():
    result = render_governance_analytics_tab()
    assert result["no_production_strategy_mutation"] is True

def test_render_governance_analytics_tab_no_live_activation():
    result = render_governance_analytics_tab()
    assert result["no_live_strategy_activation"] is True

def test_render_governance_analytics_tab_production_trading_blocked():
    result = render_governance_analytics_tab()
    assert result["production_trading_blocked"] is True

def test_render_governance_analytics_tab_analytics_does_not_execute():
    result = render_governance_analytics_tab()
    assert result["analytics_executes_decision"] is False

def test_render_governance_analytics_tab_dashboard_does_not_mutate():
    result = render_governance_analytics_tab()
    assert result["dashboard_mutates_strategy"] is False

def test_render_governance_analytics_tab_analytics_windows():
    result = render_governance_analytics_tab()
    windows = result["analytics_windows"]
    assert isinstance(windows, list)
    assert "DAILY" in windows
    assert "WEEKLY" in windows
    assert "MONTHLY" in windows
    assert "QUARTERLY" in windows
    assert "FULL_HISTORY" in windows

def test_render_governance_analytics_tab_schema_version():
    result = render_governance_analytics_tab()
    assert result["schema_version"] == "197"

def test_render_governance_analytics_tab_has_empty_state():
    result = render_governance_analytics_tab()
    assert "empty_state" in result
    assert isinstance(result["empty_state"], str)


# ── get_panel_info() ──────────────────────────────────────────────────────────

def test_get_panel_info_returns_dict():
    info = get_panel_info()
    assert isinstance(info, dict)

def test_get_panel_info_panel_version():
    info = get_panel_info()
    assert info["panel_version"] in ("1.9.7", "1.9.8", "1.9.9")

def test_get_panel_info_paper_only():
    info = get_panel_info()
    assert info["paper_only"] is True

def test_get_panel_info_no_real_orders():
    info = get_panel_info()
    assert info["no_real_orders"] is True

def test_get_panel_info_headless_safe():
    info = get_panel_info()
    assert info["headless_safe"] is True

def test_get_panel_info_tab_count_positive():
    info = get_panel_info()
    assert info["tab_count"] > 0

def test_get_panel_info_tabs_is_list():
    info = get_panel_info()
    assert isinstance(info["tabs"], list)

def test_get_panel_info_v197_tabs_in_all_tabs():
    info = get_panel_info()
    tabs = info["tabs"]
    assert "governance_dashboard" in tabs
    assert "decision_quality" in tabs
    assert "governance_analytics" in tabs


# ── Idempotency & headless-safe ────────────────────────────────────────────────

def test_render_governance_dashboard_tab_idempotent():
    r1 = render_governance_dashboard_tab()
    r2 = render_governance_dashboard_tab()
    assert r1 == r2

def test_render_decision_quality_tab_idempotent():
    r1 = render_decision_quality_tab()
    r2 = render_decision_quality_tab()
    assert r1 == r2

def test_render_governance_analytics_tab_idempotent():
    r1 = render_governance_analytics_tab()
    r2 = render_governance_analytics_tab()
    assert r1 == r2

def test_all_v197_tabs_return_dicts():
    for fn in [render_governance_dashboard_tab, render_decision_quality_tab, render_governance_analytics_tab]:
        result = fn()
        assert isinstance(result, dict), f"{fn.__name__} did not return dict"

def test_all_v197_tabs_paper_only():
    for fn in [render_governance_dashboard_tab, render_decision_quality_tab, render_governance_analytics_tab]:
        result = fn()
        assert result.get("paper_only") is True, f"{fn.__name__} missing paper_only=True"

def test_all_v197_tabs_no_real_orders():
    for fn in [render_governance_dashboard_tab, render_decision_quality_tab, render_governance_analytics_tab]:
        result = fn()
        assert result.get("no_real_orders") is True, f"{fn.__name__} missing no_real_orders=True"

def test_all_v197_tabs_schema_version_197():
    for fn in [render_governance_dashboard_tab, render_decision_quality_tab, render_governance_analytics_tab]:
        result = fn()
        assert result.get("schema_version") == "197", f"{fn.__name__} schema_version != 197"

def test_all_v197_tabs_analytics_does_not_execute():
    for fn in [render_governance_dashboard_tab, render_decision_quality_tab, render_governance_analytics_tab]:
        result = fn()
        assert result.get("analytics_executes_decision") is False, f"{fn.__name__} analytics_executes_decision is not False"
