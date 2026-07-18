"""tests/test_decision_performance_gui_v190.py
Tests for GUI panel v1.9.0 — Paper Trading Performance Review & Strategy Improvement Lab.
[!] Research Only. Paper Only. Headless-safe.
"""
import pytest
from gui.small_capital_strategy_panel import (
    PANEL_VERSION,
    PANEL_TITLE,
    _TABS_V190_PERFORMANCE_REVIEW,
    _TABS,
    get_tab_names,
    get_panel_info,
    get_performance_review_tab_names,
    render_performance_review_tab,
    render_strategy_improvement_tab,
    render_setup_analytics_tab,
    render_all_tabs,
)


def test_panel_version_is_190():
    assert PANEL_VERSION in ("1.9.0", "1.9.1", "1.9.2")


def test_panel_title_contains_190():
    assert "1.9.0" in PANEL_TITLE or "1.9.1" in PANEL_TITLE or "1.9.2" in PANEL_TITLE


def test_panel_title_contains_performance_or_review():
    assert "Performance" in PANEL_TITLE or "Review" in PANEL_TITLE or "Tuning" in PANEL_TITLE or "Sandbox" in PANEL_TITLE


def test_tabs_v190_performance_review_count():
    assert len(_TABS_V190_PERFORMANCE_REVIEW) == 3


def test_tabs_v190_contains_performance_review():
    assert "performance_review" in _TABS_V190_PERFORMANCE_REVIEW


def test_tabs_v190_contains_strategy_improvement():
    assert "strategy_improvement" in _TABS_V190_PERFORMANCE_REVIEW


def test_tabs_v190_contains_setup_analytics():
    assert "setup_analytics" in _TABS_V190_PERFORMANCE_REVIEW


def test_tabs_includes_performance_review():
    assert "performance_review" in _TABS


def test_tabs_includes_strategy_improvement():
    assert "strategy_improvement" in _TABS


def test_tabs_includes_setup_analytics():
    assert "setup_analytics" in _TABS


def test_get_performance_review_tab_names_equals_v190_list():
    assert get_performance_review_tab_names() == list(_TABS_V190_PERFORMANCE_REVIEW)


def test_get_performance_review_tab_names_count():
    assert len(get_performance_review_tab_names()) == 3


def test_get_performance_review_tab_names_is_list():
    assert isinstance(get_performance_review_tab_names(), list)


def test_render_performance_review_tab_tab_name():
    assert render_performance_review_tab()["tab"] == "performance_review"


def test_render_performance_review_tab_paper_only():
    assert render_performance_review_tab()["paper_only"] is True


def test_render_performance_review_tab_performance_review_only():
    assert render_performance_review_tab()["performance_review_only"] is True


def test_render_performance_review_tab_strategy_improvement_only():
    assert render_performance_review_tab()["strategy_improvement_only"] is True


def test_render_performance_review_tab_no_real_orders():
    assert render_performance_review_tab()["no_real_orders"] is True


def test_render_performance_review_tab_no_broker():
    assert render_performance_review_tab()["no_broker"] is True


def test_render_performance_review_tab_not_investment_advice():
    assert render_performance_review_tab()["not_investment_advice"] is True


def test_render_performance_review_tab_production_trading_blocked():
    assert render_performance_review_tab()["production_trading_blocked"] is True


def test_render_performance_review_tab_schema_version():
    assert render_performance_review_tab()["schema_version"] == "190"


def test_render_performance_review_tab_empty_state():
    assert "empty_state" in render_performance_review_tab()


def test_render_strategy_improvement_tab_tab_name():
    assert render_strategy_improvement_tab()["tab"] == "strategy_improvement"


def test_render_strategy_improvement_tab_paper_only():
    assert render_strategy_improvement_tab()["paper_only"] is True


def test_render_strategy_improvement_tab_strategy_improvement_only():
    assert render_strategy_improvement_tab()["strategy_improvement_only"] is True


def test_render_strategy_improvement_tab_performance_review_only():
    assert render_strategy_improvement_tab()["performance_review_only"] is True


def test_render_strategy_improvement_tab_schema_version():
    assert render_strategy_improvement_tab()["schema_version"] == "190"


def test_render_strategy_improvement_tab_empty_state():
    assert "empty_state" in render_strategy_improvement_tab()


def test_render_setup_analytics_tab_tab_name():
    assert render_setup_analytics_tab()["tab"] == "setup_analytics"


def test_render_setup_analytics_tab_paper_only():
    assert render_setup_analytics_tab()["paper_only"] is True


def test_render_setup_analytics_tab_performance_review_only():
    assert render_setup_analytics_tab()["performance_review_only"] is True


def test_render_setup_analytics_tab_schema_version():
    assert render_setup_analytics_tab()["schema_version"] == "190"


def test_render_setup_analytics_tab_empty_state():
    assert "empty_state" in render_setup_analytics_tab()


def test_get_panel_info_panel_version():
    assert get_panel_info()["panel_version"] in ("1.9.0", "1.9.1", "1.9.2")


def test_get_panel_info_paper_only():
    assert get_panel_info()["paper_only"] is True


def test_get_panel_info_headless_safe():
    assert get_panel_info()["headless_safe"] is True


def test_get_panel_info_no_real_orders():
    assert get_panel_info()["no_real_orders"] is True


def test_get_panel_info_is_dict():
    assert isinstance(get_panel_info(), dict)


def test_get_tab_names_includes_performance_review():
    assert "performance_review" in get_tab_names()


def test_render_all_tabs_contains_all_tab_keys():
    all_tabs = render_all_tabs()
    for tab_key in _TABS:
        assert tab_key in all_tabs, f"Tab key missing from render_all_tabs(): {tab_key}"


def test_render_all_tabs_performance_review_paper_only():
    assert render_all_tabs()["performance_review"]["paper_only"] is True


def test_render_all_tabs_strategy_improvement_paper_only():
    assert render_all_tabs()["strategy_improvement"]["paper_only"] is True


def test_render_all_tabs_setup_analytics_paper_only():
    assert render_all_tabs()["setup_analytics"]["paper_only"] is True


def test_render_all_tabs_no_error_tabs():
    all_tabs = render_all_tabs()
    for v in all_tabs.values():
        if isinstance(v, dict):
            assert "error" not in v, f"Error found in tab: {v}"


def test_tabs_still_contains_decision_journal():
    assert "decision_journal" in _TABS


def test_tabs_still_contains_decision_workflow():
    assert "decision_workflow" in _TABS


def test_tabs_cumulative_count():
    assert len(_TABS) >= 148


def test_render_performance_review_tab_research_only():
    assert render_performance_review_tab()["research_only"] is True


def test_render_strategy_improvement_tab_no_broker():
    assert render_strategy_improvement_tab()["no_broker"] is True


def test_render_setup_analytics_tab_strategy_improvement_only():
    assert render_setup_analytics_tab()["strategy_improvement_only"] is True
