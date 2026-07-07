"""tests/test_watchlist_gui_v171.py — GUI panel tests for v1.7.1 watchlist tabs (headless)."""
import pytest
from gui.small_capital_strategy_panel import (
    get_tab_names,
    get_watchlist_tab_names,
    render_watchlist_overview_tab,
    render_watchlist_candidate_pool_tab,
    render_watchlist_theme_rotation_tab,
    render_watchlist_score_weights_tab,
    render_watchlist_ranking_tab,
    render_watchlist_top_10_focus_tab,
    render_watchlist_top_5_tradable_tab,
    render_watchlist_tier_classification_tab,
    render_watchlist_excluded_tab,
    render_watchlist_overdiversification_tab,
    render_watchlist_allocation_mapping_tab,
    render_watchlist_safety_tab,
    render_watchlist_report_tab,
    render_watchlist_health_tab,
    render_watchlist_gate_tab,
    PANEL_VERSION,
)


def test_panel_version_171():
    # Panel updated to v1.7.2 to include ABC execution tabs
    assert PANEL_VERSION == "1.7.3"


def test_total_tab_count():
    tabs = get_tab_names()
    assert len(tabs) == 69  # 22 v1.7.0 + 15 v1.7.1 + 18 v1.7.2


def test_watchlist_tab_count():
    tabs = get_watchlist_tab_names()
    assert len(tabs) == 15


def test_watchlist_tabs_not_empty():
    tabs = get_watchlist_tab_names()
    assert all(len(t) > 0 for t in tabs)


def test_render_overview_dict():
    result = render_watchlist_overview_tab()
    assert isinstance(result, dict)


def test_render_overview_paper_only():
    result = render_watchlist_overview_tab()
    assert result.get("paper_only") is True


def test_render_candidate_pool_dict():
    result = render_watchlist_candidate_pool_tab()
    assert isinstance(result, dict)


def test_render_candidate_pool_paper_only():
    result = render_watchlist_candidate_pool_tab()
    assert result.get("paper_only") is True


def test_render_theme_rotation_dict():
    result = render_watchlist_theme_rotation_tab()
    assert isinstance(result, dict)


def test_render_score_weights_dict():
    result = render_watchlist_score_weights_tab()
    assert isinstance(result, dict)


def test_render_ranking_dict():
    result = render_watchlist_ranking_tab()
    assert isinstance(result, dict)


def test_render_top_10_focus_dict():
    result = render_watchlist_top_10_focus_tab()
    assert isinstance(result, dict)


def test_render_top_5_tradable_dict():
    result = render_watchlist_top_5_tradable_tab()
    assert isinstance(result, dict)


def test_render_tier_classification_dict():
    result = render_watchlist_tier_classification_tab()
    assert isinstance(result, dict)


def test_render_excluded_dict():
    result = render_watchlist_excluded_tab()
    assert isinstance(result, dict)


def test_render_overdiversification_dict():
    result = render_watchlist_overdiversification_tab()
    assert isinstance(result, dict)


def test_render_allocation_mapping_dict():
    result = render_watchlist_allocation_mapping_tab()
    assert isinstance(result, dict)


def test_render_safety_tab_dict():
    result = render_watchlist_safety_tab()
    assert isinstance(result, dict)


def test_render_safety_tab_has_flags():
    result = render_watchlist_safety_tab()
    assert "flags" in result


def test_render_report_tab_dict():
    result = render_watchlist_report_tab()
    assert isinstance(result, dict)


def test_render_health_tab_dict():
    result = render_watchlist_health_tab()
    assert isinstance(result, dict)


def test_render_gate_tab_dict():
    result = render_watchlist_gate_tab()
    assert isinstance(result, dict)


def test_all_watchlist_renders_paper_only():
    # safety/health/gate tabs return status structures without top-level paper_only
    renderers_with_paper_only = [
        render_watchlist_overview_tab,
        render_watchlist_candidate_pool_tab,
        render_watchlist_theme_rotation_tab,
        render_watchlist_score_weights_tab,
        render_watchlist_ranking_tab,
        render_watchlist_top_10_focus_tab,
        render_watchlist_top_5_tradable_tab,
        render_watchlist_tier_classification_tab,
        render_watchlist_excluded_tab,
        render_watchlist_overdiversification_tab,
        render_watchlist_allocation_mapping_tab,
        render_watchlist_report_tab,
    ]
    for fn in renderers_with_paper_only:
        result = fn()
        assert result.get("paper_only") is True, f"{fn.__name__} missing paper_only=True"
