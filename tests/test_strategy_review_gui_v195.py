"""
tests/test_strategy_review_gui_v195.py
Tests for GUI panel v1.9.5 — Paper Strategy Review Alert & Human Approval Lab.
[!] Research Only. Paper Only. Review Only. Human Approval Only. No Real Orders. Not Investment Advice.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE,
    _TABS_V195_STRATEGY_REVIEW, _TABS,
    render_review_alerts_tab, render_human_approval_tab,
    render_rollback_review_tab, get_review_tab_names,
    get_tab_names, get_panel_info, render_all_tabs,
)


# ── version ───────────────────────────────────────────────────────────────────

def test_panel_version_195():
    assert PANEL_VERSION in ("1.9.5", "1.9.6", "1.9.7")


def test_panel_title_contains_195():
    assert "1.9.5" in PANEL_TITLE or "1.9.6" in PANEL_TITLE or "1.9.7" in PANEL_TITLE


def test_panel_title_contains_review_or_approval():
    assert "Review" in PANEL_TITLE or "Approval" in PANEL_TITLE or "Governance" in PANEL_TITLE or "Dashboard" in PANEL_TITLE


# ── review tabs ───────────────────────────────────────────────────────────────

def test_review_tabs_count():
    assert len(_TABS_V195_STRATEGY_REVIEW) == 3


def test_review_tab_review_alerts():
    assert "review_alerts" in _TABS_V195_STRATEGY_REVIEW


def test_review_tab_human_approval():
    assert "human_approval" in _TABS_V195_STRATEGY_REVIEW


def test_review_tab_rollback_review():
    assert "rollback_review" in _TABS_V195_STRATEGY_REVIEW


def test_review_tabs_all_in_tabs():
    for tab in _TABS_V195_STRATEGY_REVIEW:
        assert tab in _TABS


def test_get_review_tab_names_returns_list():
    assert isinstance(get_review_tab_names(), list)


def test_get_review_tab_names_count():
    assert len(get_review_tab_names()) == 3


def test_get_review_tab_names_review_alerts():
    assert "review_alerts" in get_review_tab_names()


def test_get_review_tab_names_human_approval():
    assert "human_approval" in get_review_tab_names()


def test_get_review_tab_names_rollback_review():
    assert "rollback_review" in get_review_tab_names()


# ── render_review_alerts_tab ──────────────────────────────────────────────────

def test_render_review_alerts_tab_returns_dict():
    assert isinstance(render_review_alerts_tab(), dict)


def test_render_review_alerts_tab_tab_name():
    assert render_review_alerts_tab()["tab"] == "review_alerts"


def test_render_review_alerts_tab_paper_only():
    assert render_review_alerts_tab()["paper_only"] is True


def test_render_review_alerts_tab_review_only():
    assert render_review_alerts_tab()["review_only"] is True


def test_render_review_alerts_tab_auto_approval_false():
    assert render_review_alerts_tab()["auto_approval"] is False


def test_render_review_alerts_tab_requires_human_review():
    assert render_review_alerts_tab()["requires_human_review"] is True


def test_render_review_alerts_tab_no_real_orders():
    assert render_review_alerts_tab()["no_real_orders"] is True


def test_render_review_alerts_tab_not_investment_advice():
    assert render_review_alerts_tab()["not_investment_advice"] is True


def test_render_review_alerts_tab_schema_version():
    assert render_review_alerts_tab()["schema_version"] == "195"


# ── render_human_approval_tab ─────────────────────────────────────────────────

def test_render_human_approval_tab_returns_dict():
    assert isinstance(render_human_approval_tab(), dict)


def test_render_human_approval_tab_tab_name():
    assert render_human_approval_tab()["tab"] == "human_approval"


def test_render_human_approval_tab_paper_only():
    assert render_human_approval_tab()["paper_only"] is True


def test_render_human_approval_tab_human_approval_only():
    assert render_human_approval_tab()["human_approval_only"] is True


def test_render_human_approval_tab_auto_approval_false():
    assert render_human_approval_tab()["auto_approval"] is False


def test_render_human_approval_tab_auto_execute_false():
    assert render_human_approval_tab()["auto_execute"] is False


def test_render_human_approval_tab_requires_manual_review():
    assert render_human_approval_tab()["requires_manual_review"] is True


def test_render_human_approval_tab_no_real_orders():
    assert render_human_approval_tab()["no_real_orders"] is True


def test_render_human_approval_tab_not_investment_advice():
    assert render_human_approval_tab()["not_investment_advice"] is True


def test_render_human_approval_tab_schema_version():
    assert render_human_approval_tab()["schema_version"] == "195"


# ── render_rollback_review_tab ────────────────────────────────────────────────

def test_render_rollback_review_tab_returns_dict():
    assert isinstance(render_rollback_review_tab(), dict)


def test_render_rollback_review_tab_tab_name():
    assert render_rollback_review_tab()["tab"] == "rollback_review"


def test_render_rollback_review_tab_paper_only():
    assert render_rollback_review_tab()["paper_only"] is True


def test_render_rollback_review_tab_rollback_review_only():
    assert render_rollback_review_tab()["rollback_review_only"] is True


def test_render_rollback_review_tab_auto_rollback_false():
    assert render_rollback_review_tab()["auto_rollback"] is False


def test_render_rollback_review_tab_requires_manual_review():
    assert render_rollback_review_tab()["requires_manual_review"] is True


def test_render_rollback_review_tab_no_real_orders():
    assert render_rollback_review_tab()["no_real_orders"] is True


def test_render_rollback_review_tab_not_investment_advice():
    assert render_rollback_review_tab()["not_investment_advice"] is True


def test_render_rollback_review_tab_schema_version():
    assert render_rollback_review_tab()["schema_version"] == "195"


# ── get_tab_names ─────────────────────────────────────────────────────────────

def test_get_tab_names_includes_review_alerts():
    assert "review_alerts" in get_tab_names()


def test_get_tab_names_includes_human_approval():
    assert "human_approval" in get_tab_names()


def test_get_tab_names_includes_rollback_review():
    assert "rollback_review" in get_tab_names()


def test_total_tabs_ge_157():
    assert len(_TABS) >= 157


# ── get_panel_info ────────────────────────────────────────────────────────────

def test_get_panel_info_panel_version():
    assert get_panel_info()["panel_version"] in ("1.9.5", "1.9.6", "1.9.7")


def test_get_panel_info_paper_only():
    assert get_panel_info()["paper_only"] is True


def test_get_panel_info_headless_safe():
    assert get_panel_info()["headless_safe"] is True


def test_get_panel_info_no_real_orders():
    assert get_panel_info()["no_real_orders"] is True


def test_get_panel_info_tab_count_ge_157():
    assert get_panel_info()["tab_count"] >= 157


# ── render_all_tabs ───────────────────────────────────────────────────────────

def test_render_all_tabs_contains_review_alerts():
    assert "review_alerts" in render_all_tabs()


def test_render_all_tabs_contains_human_approval():
    assert "human_approval" in render_all_tabs()


def test_render_all_tabs_contains_rollback_review():
    assert "rollback_review" in render_all_tabs()


def test_render_all_tabs_review_alerts_paper_only():
    assert render_all_tabs()["review_alerts"]["paper_only"] is True


def test_render_all_tabs_human_approval_auto_approval_false():
    assert render_all_tabs()["human_approval"]["auto_approval"] is False


def test_render_all_tabs_rollback_review_auto_rollback_false():
    assert render_all_tabs()["rollback_review"]["auto_rollback"] is False


def test_render_all_tabs_no_error_tabs():
    all_tabs = render_all_tabs()
    for v in all_tabs.values():
        if isinstance(v, dict):
            assert "error" not in v, f"Error found in tab: {v}"


# ── backward compat tabs still present ───────────────────────────────────────

def test_tabs_still_contains_strategy_monitoring():
    assert "strategy_monitoring" in _TABS


def test_tabs_still_contains_strategy_promotion():
    assert "strategy_promotion" in _TABS


def test_tabs_still_contains_strategy_sandbox():
    assert "strategy_sandbox" in _TABS


def test_tabs_still_contains_drift_detection():
    assert "drift_detection" in _TABS


def test_tabs_still_contains_rollback_alerts():
    assert "rollback_alerts" in _TABS


def test_tabs_still_contains_performance_review():
    assert "performance_review" in _TABS
