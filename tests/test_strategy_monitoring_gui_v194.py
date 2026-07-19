"""
tests/test_strategy_monitoring_gui_v194.py
Tests for GUI panel v1.9.4 — Paper Strategy Monitoring & Drift Detection Lab.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only. No Real Orders. Not Investment Advice.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE,
    _TABS_V194_STRATEGY_MONITORING, _TABS,
    render_strategy_monitoring_tab, render_drift_detection_tab,
    render_rollback_alerts_tab, get_monitoring_tab_names,
    get_tab_names, get_panel_info, render_all_tabs,
)


# ── version ───────────────────────────────────────────────────────────────────

def test_panel_version_194():
    assert PANEL_VERSION in ("1.9.4", "1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10")


def test_panel_title_contains_194():
    assert "1.9.4" in PANEL_TITLE or "1.9.5" in PANEL_TITLE or "1.9.6" in PANEL_TITLE or "1.9.7" in PANEL_TITLE or "1.9.8" in PANEL_TITLE or "1.9.9" in PANEL_TITLE or "1.9.10" in PANEL_TITLE


def test_panel_title_contains_monitoring():
    assert "Monitoring" in PANEL_TITLE or "Drift" in PANEL_TITLE or "Review" in PANEL_TITLE or "Governance" in PANEL_TITLE or "Portfolio" in PANEL_TITLE


# ── monitoring tabs ───────────────────────────────────────────────────────────

def test_monitoring_tabs_count():
    assert len(_TABS_V194_STRATEGY_MONITORING) == 3


def test_monitoring_tab_strategy_monitoring():
    assert "strategy_monitoring" in _TABS_V194_STRATEGY_MONITORING


def test_monitoring_tab_drift_detection():
    assert "drift_detection" in _TABS_V194_STRATEGY_MONITORING


def test_monitoring_tab_rollback_alerts():
    assert "rollback_alerts" in _TABS_V194_STRATEGY_MONITORING


def test_monitoring_tabs_all_in_tabs():
    for tab in _TABS_V194_STRATEGY_MONITORING:
        assert tab in _TABS


def test_get_monitoring_tab_names_returns_list():
    assert isinstance(get_monitoring_tab_names(), list)


def test_get_monitoring_tab_names_count():
    assert len(get_monitoring_tab_names()) == 3


def test_get_monitoring_tab_names_strategy_monitoring():
    assert "strategy_monitoring" in get_monitoring_tab_names()


def test_get_monitoring_tab_names_drift_detection():
    assert "drift_detection" in get_monitoring_tab_names()


def test_get_monitoring_tab_names_rollback_alerts():
    assert "rollback_alerts" in get_monitoring_tab_names()


# ── render_strategy_monitoring_tab ────────────────────────────────────────────

def test_render_strategy_monitoring_tab_returns_dict():
    assert isinstance(render_strategy_monitoring_tab(), dict)


def test_render_strategy_monitoring_tab_tab_name():
    assert render_strategy_monitoring_tab()["tab"] == "strategy_monitoring"


def test_render_strategy_monitoring_tab_paper_only():
    assert render_strategy_monitoring_tab()["paper_only"] is True


def test_render_strategy_monitoring_tab_monitoring_only():
    assert render_strategy_monitoring_tab()["monitoring_only"] is True


def test_render_strategy_monitoring_tab_drift_detection_only():
    assert render_strategy_monitoring_tab()["drift_detection_only"] is True


def test_render_strategy_monitoring_tab_no_real_orders():
    assert render_strategy_monitoring_tab()["no_real_orders"] is True


def test_render_strategy_monitoring_tab_no_broker():
    assert render_strategy_monitoring_tab()["no_broker"] is True


def test_render_strategy_monitoring_tab_not_investment_advice():
    assert render_strategy_monitoring_tab()["not_investment_advice"] is True


def test_render_strategy_monitoring_tab_production_trading_blocked():
    assert render_strategy_monitoring_tab()["production_trading_blocked"] is True


def test_render_strategy_monitoring_tab_schema_version():
    assert render_strategy_monitoring_tab()["schema_version"] == "194"


def test_render_strategy_monitoring_tab_no_auto_rollback():
    tab = render_strategy_monitoring_tab()
    assert tab.get("auto_rollback", False) is False


# ── render_drift_detection_tab ────────────────────────────────────────────────

def test_render_drift_detection_tab_returns_dict():
    assert isinstance(render_drift_detection_tab(), dict)


def test_render_drift_detection_tab_tab_name():
    assert render_drift_detection_tab()["tab"] == "drift_detection"


def test_render_drift_detection_tab_paper_only():
    assert render_drift_detection_tab()["paper_only"] is True


def test_render_drift_detection_tab_monitoring_only():
    assert render_drift_detection_tab()["monitoring_only"] is True


def test_render_drift_detection_tab_drift_detection_only():
    assert render_drift_detection_tab()["drift_detection_only"] is True


def test_render_drift_detection_tab_no_real_orders():
    assert render_drift_detection_tab()["no_real_orders"] is True


def test_render_drift_detection_tab_not_investment_advice():
    assert render_drift_detection_tab()["not_investment_advice"] is True


def test_render_drift_detection_tab_schema_version():
    assert render_drift_detection_tab()["schema_version"] == "194"


# ── render_rollback_alerts_tab ────────────────────────────────────────────────

def test_render_rollback_alerts_tab_returns_dict():
    assert isinstance(render_rollback_alerts_tab(), dict)


def test_render_rollback_alerts_tab_tab_name():
    assert render_rollback_alerts_tab()["tab"] == "rollback_alerts"


def test_render_rollback_alerts_tab_paper_only():
    assert render_rollback_alerts_tab()["paper_only"] is True


def test_render_rollback_alerts_tab_monitoring_only():
    assert render_rollback_alerts_tab()["monitoring_only"] is True


def test_render_rollback_alerts_tab_rollback_trigger_only():
    assert render_rollback_alerts_tab()["rollback_trigger_only"] is True


def test_render_rollback_alerts_tab_auto_rollback_false():
    assert render_rollback_alerts_tab()["auto_rollback"] is False


def test_render_rollback_alerts_tab_requires_manual_review():
    assert render_rollback_alerts_tab()["requires_manual_review"] is True


def test_render_rollback_alerts_tab_no_real_orders():
    assert render_rollback_alerts_tab()["no_real_orders"] is True


def test_render_rollback_alerts_tab_not_investment_advice():
    assert render_rollback_alerts_tab()["not_investment_advice"] is True


def test_render_rollback_alerts_tab_schema_version():
    assert render_rollback_alerts_tab()["schema_version"] == "194"


def test_render_rollback_alerts_tab_production_trading_blocked():
    assert render_rollback_alerts_tab()["production_trading_blocked"] is True


# ── get_tab_names ─────────────────────────────────────────────────────────────

def test_get_tab_names_includes_strategy_monitoring():
    assert "strategy_monitoring" in get_tab_names()


def test_get_tab_names_includes_drift_detection():
    assert "drift_detection" in get_tab_names()


def test_get_tab_names_includes_rollback_alerts():
    assert "rollback_alerts" in get_tab_names()


def test_total_tabs_ge_151():
    assert len(_TABS) >= 151


# ── get_panel_info ────────────────────────────────────────────────────────────

def test_get_panel_info_panel_version():
    assert get_panel_info()["panel_version"] in ("1.9.4", "1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9", "1.9.10")


def test_get_panel_info_paper_only():
    assert get_panel_info()["paper_only"] is True


def test_get_panel_info_headless_safe():
    assert get_panel_info()["headless_safe"] is True


def test_get_panel_info_no_real_orders():
    assert get_panel_info()["no_real_orders"] is True


def test_get_panel_info_tab_count_includes_194():
    info = get_panel_info()
    assert info["tab_count"] >= 151


# ── render_all_tabs ───────────────────────────────────────────────────────────

def test_render_all_tabs_contains_strategy_monitoring():
    all_tabs = render_all_tabs()
    assert "strategy_monitoring" in all_tabs


def test_render_all_tabs_contains_drift_detection():
    all_tabs = render_all_tabs()
    assert "drift_detection" in all_tabs


def test_render_all_tabs_contains_rollback_alerts():
    all_tabs = render_all_tabs()
    assert "rollback_alerts" in all_tabs


def test_render_all_tabs_strategy_monitoring_paper_only():
    assert render_all_tabs()["strategy_monitoring"]["paper_only"] is True


def test_render_all_tabs_drift_detection_paper_only():
    assert render_all_tabs()["drift_detection"]["paper_only"] is True


def test_render_all_tabs_rollback_alerts_auto_rollback_false():
    assert render_all_tabs()["rollback_alerts"]["auto_rollback"] is False


def test_render_all_tabs_no_error_tabs():
    all_tabs = render_all_tabs()
    for v in all_tabs.values():
        if isinstance(v, dict):
            assert "error" not in v, f"Error found in tab: {v}"


# ── backward compat tabs still present ───────────────────────────────────────

def test_tabs_still_contains_strategy_promotion():
    assert "strategy_promotion" in _TABS


def test_tabs_still_contains_strategy_sandbox():
    assert "strategy_sandbox" in _TABS


def test_tabs_still_contains_strategy_rule_tuning():
    assert "strategy_rule_tuning" in _TABS


def test_tabs_still_contains_performance_review():
    assert "performance_review" in _TABS


def test_tabs_still_contains_decision_journal():
    assert "decision_journal" in _TABS
