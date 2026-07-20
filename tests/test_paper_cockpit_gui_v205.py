"""
tests/test_paper_cockpit_gui_v205.py
v2.0.5 GUI Compatibility Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest


def test_panel_importable():
    import gui.small_capital_strategy_panel

def test_panel_version_v205():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V205
    assert PANEL_VERSION_V205 == "2.0.5"

def test_tabs_v205_watchlist_count_3():
    from gui.small_capital_strategy_panel import _TABS_V205_WATCHLIST
    assert len(_TABS_V205_WATCHLIST) == 3

def test_tab_watchlist_rotation_v205_in_list():
    from gui.small_capital_strategy_panel import _TABS_V205_WATCHLIST
    assert "watchlist_rotation_v205" in _TABS_V205_WATCHLIST

def test_tab_promotion_queue_v205_in_list():
    from gui.small_capital_strategy_panel import _TABS_V205_WATCHLIST
    assert "promotion_queue_v205" in _TABS_V205_WATCHLIST

def test_tab_human_review_queue_v205_in_list():
    from gui.small_capital_strategy_panel import _TABS_V205_WATCHLIST
    assert "human_review_queue_v205" in _TABS_V205_WATCHLIST

def test_tabs_v205_in_get_tab_names():
    from gui.small_capital_strategy_panel import get_tab_names
    tab_names = get_tab_names()
    assert "watchlist_rotation_v205" in tab_names
    assert "promotion_queue_v205" in tab_names
    assert "human_review_queue_v205" in tab_names

def test_get_v205_tab_names_returns_3():
    from gui.small_capital_strategy_panel import get_v205_tab_names
    assert len(get_v205_tab_names()) == 3

def test_render_watchlist_rotation_v205_tab_callable():
    from gui.small_capital_strategy_panel import render_watchlist_rotation_v205_tab
    result = render_watchlist_rotation_v205_tab()
    assert result is not None

def test_render_watchlist_rotation_v205_tab_paper_only():
    from gui.small_capital_strategy_panel import render_watchlist_rotation_v205_tab
    result = render_watchlist_rotation_v205_tab()
    assert result["paper_only"] is True

def test_render_watchlist_rotation_v205_tab_no_real_orders():
    from gui.small_capital_strategy_panel import render_watchlist_rotation_v205_tab
    result = render_watchlist_rotation_v205_tab()
    assert result["no_real_orders"] is True

def test_render_watchlist_rotation_v205_tab_should_auto_apply_false():
    from gui.small_capital_strategy_panel import render_watchlist_rotation_v205_tab
    result = render_watchlist_rotation_v205_tab()
    assert result["should_auto_apply"] is False

def test_render_watchlist_rotation_v205_tab_version():
    from gui.small_capital_strategy_panel import render_watchlist_rotation_v205_tab
    result = render_watchlist_rotation_v205_tab()
    assert result["version"] == "2.0.5"

def test_render_watchlist_rotation_v205_tab_schema_version():
    from gui.small_capital_strategy_panel import render_watchlist_rotation_v205_tab
    result = render_watchlist_rotation_v205_tab()
    assert result["schema_version"] == "205"

def test_render_promotion_queue_v205_tab_callable():
    from gui.small_capital_strategy_panel import render_promotion_queue_v205_tab
    result = render_promotion_queue_v205_tab()
    assert result is not None

def test_render_promotion_queue_v205_tab_paper_only():
    from gui.small_capital_strategy_panel import render_promotion_queue_v205_tab
    result = render_promotion_queue_v205_tab()
    assert result["paper_only"] is True

def test_render_promotion_queue_v205_tab_should_auto_apply_false():
    from gui.small_capital_strategy_panel import render_promotion_queue_v205_tab
    result = render_promotion_queue_v205_tab()
    assert result["should_auto_apply"] is False

def test_render_promotion_queue_v205_tab_version():
    from gui.small_capital_strategy_panel import render_promotion_queue_v205_tab
    result = render_promotion_queue_v205_tab()
    assert result["version"] == "2.0.5"

def test_render_human_review_queue_v205_tab_callable():
    from gui.small_capital_strategy_panel import render_human_review_queue_v205_tab
    result = render_human_review_queue_v205_tab()
    assert result is not None

def test_render_human_review_queue_v205_tab_paper_only():
    from gui.small_capital_strategy_panel import render_human_review_queue_v205_tab
    result = render_human_review_queue_v205_tab()
    assert result["paper_only"] is True

def test_render_human_review_queue_v205_tab_should_auto_apply_false():
    from gui.small_capital_strategy_panel import render_human_review_queue_v205_tab
    result = render_human_review_queue_v205_tab()
    assert result["should_auto_apply"] is False

def test_render_human_review_queue_v205_tab_human_review_required():
    from gui.small_capital_strategy_panel import render_human_review_queue_v205_tab
    result = render_human_review_queue_v205_tab()
    assert result["human_review_required"] is True

def test_tab_render_map_v205_has_3_entries():
    from gui.small_capital_strategy_panel import _TAB_RENDER_MAP_V205
    assert len(_TAB_RENDER_MAP_V205) == 3

def test_render_all_tabs_watchlist_rotation_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("watchlist_rotation_v205", {})

def test_render_all_tabs_promotion_queue_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("promotion_queue_v205", {})

def test_render_all_tabs_human_review_queue_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("human_review_queue_v205", {})

def test_render_all_tabs_no_error_tabs():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    error_tabs = [k for k, v in result.items() if "error" in v]
    assert error_tabs == [], f"Error tabs: {error_tabs}"

def test_v205_tabs_present_in_all_tabs():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "watchlist_rotation_v205" in result
    assert "promotion_queue_v205" in result
    assert "human_review_queue_v205" in result

def test_v204_tabs_still_present():
    from gui.small_capital_strategy_panel import get_tab_names
    tab_names = get_tab_names()
    assert "weekly_review_v204" in tab_names
    assert "improvement_pack_v204" in tab_names
    assert "review_metrics_v204" in tab_names
