"""
tests/test_paper_cockpit_gui_v204.py
v2.0.4 Paper Portfolio Review Loop & Weekly Improvement Pack — GUI Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

def test_panel_version_v204_exists():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V204
    assert PANEL_VERSION_V204 == "2.0.4"

def test_panel_version_unchanged():
    from gui.small_capital_strategy_panel import PANEL_VERSION
    assert PANEL_VERSION == "2.0.0"

def test_get_v204_tab_names_callable():
    from gui.small_capital_strategy_panel import get_v204_tab_names
    tabs = get_v204_tab_names()
    assert tabs is not None

def test_get_v204_tab_names_count():
    from gui.small_capital_strategy_panel import get_v204_tab_names
    tabs = get_v204_tab_names()
    assert len(tabs) == 3

def test_tab_weekly_review_v204_in_names():
    from gui.small_capital_strategy_panel import get_v204_tab_names
    tabs = get_v204_tab_names()
    assert "weekly_review_v204" in tabs

def test_tab_improvement_pack_v204_in_names():
    from gui.small_capital_strategy_panel import get_v204_tab_names
    tabs = get_v204_tab_names()
    assert "improvement_pack_v204" in tabs

def test_tab_review_metrics_v204_in_names():
    from gui.small_capital_strategy_panel import get_v204_tab_names
    tabs = get_v204_tab_names()
    assert "review_metrics_v204" in tabs

def test_get_tab_names_includes_v204_tabs():
    from gui.small_capital_strategy_panel import get_tab_names
    tabs = get_tab_names()
    assert "weekly_review_v204" in tabs
    assert "improvement_pack_v204" in tabs
    assert "review_metrics_v204" in tabs

def test_render_weekly_review_v204_callable():
    from gui.small_capital_strategy_panel import render_weekly_review_v204_tab
    result = render_weekly_review_v204_tab()
    assert result is not None

def test_render_weekly_review_v204_tab_name():
    from gui.small_capital_strategy_panel import render_weekly_review_v204_tab
    result = render_weekly_review_v204_tab()
    assert result["tab"] == "weekly_review_v204"

def test_render_weekly_review_v204_paper_only():
    from gui.small_capital_strategy_panel import render_weekly_review_v204_tab
    result = render_weekly_review_v204_tab()
    assert result["paper_only"] is True

def test_render_weekly_review_v204_no_real_orders():
    from gui.small_capital_strategy_panel import render_weekly_review_v204_tab
    result = render_weekly_review_v204_tab()
    assert result["no_real_orders"] is True

def test_render_weekly_review_v204_should_auto_apply_false():
    from gui.small_capital_strategy_panel import render_weekly_review_v204_tab
    result = render_weekly_review_v204_tab()
    assert result["should_auto_apply"] is False

def test_render_weekly_review_v204_human_review_required():
    from gui.small_capital_strategy_panel import render_weekly_review_v204_tab
    result = render_weekly_review_v204_tab()
    assert result["human_review_required"] is True

def test_render_weekly_review_v204_version():
    from gui.small_capital_strategy_panel import render_weekly_review_v204_tab
    result = render_weekly_review_v204_tab()
    assert result["version"] == "2.0.4"

def test_render_weekly_review_v204_no_error():
    from gui.small_capital_strategy_panel import render_weekly_review_v204_tab
    result = render_weekly_review_v204_tab()
    assert "error" not in result

def test_render_improvement_pack_v204_callable():
    from gui.small_capital_strategy_panel import render_improvement_pack_v204_tab
    result = render_improvement_pack_v204_tab()
    assert result is not None

def test_render_improvement_pack_v204_tab_name():
    from gui.small_capital_strategy_panel import render_improvement_pack_v204_tab
    result = render_improvement_pack_v204_tab()
    assert result["tab"] == "improvement_pack_v204"

def test_render_improvement_pack_v204_paper_only():
    from gui.small_capital_strategy_panel import render_improvement_pack_v204_tab
    result = render_improvement_pack_v204_tab()
    assert result["paper_only"] is True

def test_render_improvement_pack_v204_should_auto_apply_false():
    from gui.small_capital_strategy_panel import render_improvement_pack_v204_tab
    result = render_improvement_pack_v204_tab()
    assert result["should_auto_apply"] is False

def test_render_improvement_pack_v204_has_weekly_pack_fields():
    from gui.small_capital_strategy_panel import render_improvement_pack_v204_tab
    result = render_improvement_pack_v204_tab()
    assert "weekly_pack_fields" in result
    assert len(result["weekly_pack_fields"]) == 15

def test_render_improvement_pack_v204_no_error():
    from gui.small_capital_strategy_panel import render_improvement_pack_v204_tab
    result = render_improvement_pack_v204_tab()
    assert "error" not in result

def test_render_review_metrics_v204_callable():
    from gui.small_capital_strategy_panel import render_review_metrics_v204_tab
    result = render_review_metrics_v204_tab()
    assert result is not None

def test_render_review_metrics_v204_tab_name():
    from gui.small_capital_strategy_panel import render_review_metrics_v204_tab
    result = render_review_metrics_v204_tab()
    assert result["tab"] == "review_metrics_v204"

def test_render_review_metrics_v204_paper_only():
    from gui.small_capital_strategy_panel import render_review_metrics_v204_tab
    result = render_review_metrics_v204_tab()
    assert result["paper_only"] is True

def test_render_review_metrics_v204_has_fields():
    from gui.small_capital_strategy_panel import render_review_metrics_v204_tab
    result = render_review_metrics_v204_tab()
    assert "review_metrics_fields" in result
    assert len(result["review_metrics_fields"]) == 10

def test_render_review_metrics_v204_no_error():
    from gui.small_capital_strategy_panel import render_review_metrics_v204_tab
    result = render_review_metrics_v204_tab()
    assert "error" not in result

def test_render_all_tabs_no_error_weekly_review():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    assert "error" not in str(all_rendered.get("weekly_review_v204", {}))

def test_render_all_tabs_no_error_improvement_pack():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    assert "error" not in str(all_rendered.get("improvement_pack_v204", {}))

def test_render_all_tabs_no_error_review_metrics():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    assert "error" not in str(all_rendered.get("review_metrics_v204", {}))

def test_render_all_tabs_zero_error_tabs():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    error_tabs = [k for k, v in all_rendered.items() if isinstance(v, dict) and "error" in v]
    assert len(error_tabs) == 0, f"Error tabs found: {error_tabs}"

def test_render_all_tabs_v204_tabs_present():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    assert "weekly_review_v204" in all_rendered
    assert "improvement_pack_v204" in all_rendered
    assert "review_metrics_v204" in all_rendered

def test_tab_render_map_v204_exists():
    from gui.small_capital_strategy_panel import _TAB_RENDER_MAP_V204
    assert "weekly_review_v204" in _TAB_RENDER_MAP_V204
    assert "improvement_pack_v204" in _TAB_RENDER_MAP_V204
    assert "review_metrics_v204" in _TAB_RENDER_MAP_V204

def test_render_all_tabs_v203_tabs_still_present():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    assert "simulation_batch_v203" in all_rendered
    assert "scenario_replay_v203" in all_rendered
    assert "strategy_comparison_v203" in all_rendered

def test_render_all_tabs_v202_tabs_still_present():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    assert "report_export_v202" in all_rendered

def test_render_weekly_review_v204_schema_version():
    from gui.small_capital_strategy_panel import render_weekly_review_v204_tab
    result = render_weekly_review_v204_tab()
    assert result["schema_version"] == "204"
