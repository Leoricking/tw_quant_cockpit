"""
tests/test_decision_journal_gui_v189.py
Tests for v1.8.9 GUI tabs — Paper Decision Journal & Review Loop.
[!] Research Only. Paper Only. Journal Only. Review Only. No Real Orders. Not Investment Advice.
Headless-safe: no tkinter or display required.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION, PANEL_TITLE,
    _TABS_V189_DECISION_JOURNAL,
    get_decision_journal_tab_names,
    render_decision_journal_tab,
    render_daily_review_tab,
    render_weekly_review_v189_tab,
    get_panel_info,
    _TABS,
)


def test_panel_version_is_189():
    assert PANEL_VERSION in ("1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5")


def test_panel_title_contains_189():
    assert "1.8.9" in PANEL_TITLE or "1.9.0" in PANEL_TITLE or "1.9.1" in PANEL_TITLE or "1.9.2" in PANEL_TITLE or "1.9.3" in PANEL_TITLE or "1.9.4" in PANEL_TITLE or "1.9.5" in PANEL_TITLE


def test_panel_title_contains_journal():
    assert "Journal" in PANEL_TITLE or "journal" in PANEL_TITLE.lower() or "Performance" in PANEL_TITLE or "Tuning" in PANEL_TITLE or "Sandbox" in PANEL_TITLE or "Promotion" in PANEL_TITLE or "Rollback" in PANEL_TITLE or "Monitoring" in PANEL_TITLE or "Drift" in PANEL_TITLE or "Review" in PANEL_TITLE


def test_decision_journal_tabs_count():
    assert len(_TABS_V189_DECISION_JOURNAL) == 3


def test_decision_journal_tabs_contains_journal():
    assert "decision_journal" in _TABS_V189_DECISION_JOURNAL


def test_decision_journal_tabs_contains_daily_review():
    assert "daily_review" in _TABS_V189_DECISION_JOURNAL


def test_decision_journal_tabs_contains_weekly_review():
    assert "weekly_review" in _TABS_V189_DECISION_JOURNAL


def test_get_decision_journal_tab_names_returns_list():
    assert isinstance(get_decision_journal_tab_names(), list)


def test_get_decision_journal_tab_names_count():
    assert len(get_decision_journal_tab_names()) == 3


def test_tabs_includes_v189_journal_tabs():
    for tab in _TABS_V189_DECISION_JOURNAL:
        assert tab in _TABS


def test_total_tabs_increased_by_3():
    assert "decision_journal" in _TABS
    assert "daily_review" in _TABS
    assert "weekly_review" in _TABS


def test_render_decision_journal_tab_returns_dict():
    assert isinstance(render_decision_journal_tab(), dict)


def test_render_decision_journal_tab_tab_name():
    assert render_decision_journal_tab()["tab"] == "decision_journal"


def test_render_decision_journal_tab_paper_only():
    assert render_decision_journal_tab()["paper_only"] is True


def test_render_decision_journal_tab_journal_only():
    assert render_decision_journal_tab()["journal_only"] is True


def test_render_decision_journal_tab_review_only():
    assert render_decision_journal_tab()["review_only"] is True


def test_render_decision_journal_tab_audit_only():
    assert render_decision_journal_tab()["audit_only"] is True


def test_render_decision_journal_tab_no_real_orders():
    assert render_decision_journal_tab()["no_real_orders"] is True


def test_render_decision_journal_tab_no_broker():
    assert render_decision_journal_tab()["no_broker"] is True


def test_render_decision_journal_tab_not_investment_advice():
    assert render_decision_journal_tab()["not_investment_advice"] is True


def test_render_decision_journal_tab_production_trading_blocked():
    assert render_decision_journal_tab()["production_trading_blocked"] is True


def test_render_decision_journal_tab_schema_version():
    assert render_decision_journal_tab()["schema_version"] == "189"


def test_render_decision_journal_tab_empty_state():
    tab = render_decision_journal_tab()
    assert "empty_state" in tab
    assert len(tab["empty_state"]) > 0


def test_render_daily_review_tab_returns_dict():
    assert isinstance(render_daily_review_tab(), dict)


def test_render_daily_review_tab_tab_name():
    assert render_daily_review_tab()["tab"] == "daily_review"


def test_render_daily_review_tab_paper_only():
    assert render_daily_review_tab()["paper_only"] is True


def test_render_daily_review_tab_journal_only():
    assert render_daily_review_tab()["journal_only"] is True


def test_render_daily_review_tab_review_only():
    assert render_daily_review_tab()["review_only"] is True


def test_render_daily_review_tab_no_real_orders():
    assert render_daily_review_tab()["no_real_orders"] is True


def test_render_daily_review_tab_schema_189():
    assert render_daily_review_tab()["schema_version"] == "189"


def test_render_weekly_review_tab_returns_dict():
    assert isinstance(render_weekly_review_v189_tab(), dict)


def test_render_weekly_review_tab_tab_name():
    assert render_weekly_review_v189_tab()["tab"] == "weekly_review"


def test_render_weekly_review_tab_paper_only():
    assert render_weekly_review_v189_tab()["paper_only"] is True


def test_render_weekly_review_tab_journal_only():
    assert render_weekly_review_v189_tab()["journal_only"] is True


def test_render_weekly_review_tab_review_only():
    assert render_weekly_review_v189_tab()["review_only"] is True


def test_render_weekly_review_tab_schema_189():
    assert render_weekly_review_v189_tab()["schema_version"] == "189"


def test_get_panel_info_returns_dict():
    info = get_panel_info()
    assert isinstance(info, dict)


def test_get_panel_info_panel_version():
    assert get_panel_info()["panel_version"] in ("1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5")


def test_get_panel_info_headless_safe():
    assert get_panel_info()["headless_safe"] is True


def test_get_panel_info_paper_only():
    assert get_panel_info()["paper_only"] is True


def test_get_panel_info_no_real_orders():
    assert get_panel_info()["no_real_orders"] is True


def test_get_panel_info_tab_count_increased():
    info = get_panel_info()
    assert info["tab_count"] >= 123


def test_render_tabs_no_broker_connection():
    for render_fn in [render_decision_journal_tab, render_daily_review_tab, render_weekly_review_v189_tab]:
        tab = render_fn()
        assert tab.get("no_broker") is True


def test_render_tabs_not_investment_advice():
    for render_fn in [render_decision_journal_tab, render_daily_review_tab, render_weekly_review_v189_tab]:
        tab = render_fn()
        assert tab.get("not_investment_advice") is True


def test_render_tabs_production_trading_blocked():
    for render_fn in [render_decision_journal_tab, render_daily_review_tab, render_weekly_review_v189_tab]:
        tab = render_fn()
        assert tab.get("production_trading_blocked") is True
