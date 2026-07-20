"""
tests/test_paper_cockpit_gui_v203.py
v2.0.3 GUI Panel Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# panel version
# ---------------------------------------------------------------------------

def test_panel_version_v203():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V203
    assert PANEL_VERSION_V203 == "2.0.3"

def test_panel_version_unchanged():
    from gui.small_capital_strategy_panel import PANEL_VERSION
    assert PANEL_VERSION == "2.0.0"

def test_panel_version_v202_unchanged():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V202
    assert PANEL_VERSION_V202 == "2.0.2"

def test_panel_version_v201_unchanged():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V201
    assert PANEL_VERSION_V201 == "2.0.1"

def test_panel_title_unchanged():
    from gui.small_capital_strategy_panel import PANEL_TITLE
    assert "2.0.0" in PANEL_TITLE

# ---------------------------------------------------------------------------
# tab registration
# ---------------------------------------------------------------------------

def test_simulation_batch_v203_in_tab_names():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "simulation_batch_v203" in get_tab_names()

def test_scenario_replay_v203_in_tab_names():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "scenario_replay_v203" in get_tab_names()

def test_strategy_comparison_v203_in_tab_names():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "strategy_comparison_v203" in get_tab_names()

def test_get_v203_tab_names():
    from gui.small_capital_strategy_panel import get_v203_tab_names
    names = get_v203_tab_names()
    assert len(names) == 3

def test_get_v203_tab_names_has_simulation_batch():
    from gui.small_capital_strategy_panel import get_v203_tab_names
    assert "simulation_batch_v203" in get_v203_tab_names()

def test_get_v203_tab_names_has_scenario_replay():
    from gui.small_capital_strategy_panel import get_v203_tab_names
    assert "scenario_replay_v203" in get_v203_tab_names()

def test_get_v203_tab_names_has_strategy_comparison():
    from gui.small_capital_strategy_panel import get_v203_tab_names
    assert "strategy_comparison_v203" in get_v203_tab_names()

# ---------------------------------------------------------------------------
# v2.0.2 tabs still present (backward compat)
# ---------------------------------------------------------------------------

def test_report_export_v202_still_in_tab_names():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "report_export_v202" in get_tab_names()

def test_audit_pack_v202_still_in_tab_names():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "audit_pack_v202" in get_tab_names()

def test_export_status_v202_still_in_tab_names():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "export_status_v202" in get_tab_names()

def test_get_v202_tab_names_still_3():
    from gui.small_capital_strategy_panel import get_v202_tab_names
    assert len(get_v202_tab_names()) == 3

# ---------------------------------------------------------------------------
# v2.0.1 tabs still present (backward compat)
# ---------------------------------------------------------------------------

def test_daily_workflow_v201_still_in_tab_names():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "daily_workflow_v201" in get_tab_names()

def test_get_v201_tab_names_still_3():
    from gui.small_capital_strategy_panel import get_v201_tab_names
    assert len(get_v201_tab_names()) == 3

# ---------------------------------------------------------------------------
# render functions
# ---------------------------------------------------------------------------

def test_render_simulation_batch_v203_tab():
    from gui.small_capital_strategy_panel import render_simulation_batch_v203_tab
    result = render_simulation_batch_v203_tab()
    assert result is not None

def test_render_simulation_batch_tab_key():
    from gui.small_capital_strategy_panel import render_simulation_batch_v203_tab
    result = render_simulation_batch_v203_tab()
    assert result["tab"] == "simulation_batch_v203"

def test_render_simulation_batch_paper_only():
    from gui.small_capital_strategy_panel import render_simulation_batch_v203_tab
    result = render_simulation_batch_v203_tab()
    assert result["paper_only"] is True

def test_render_simulation_batch_no_real_orders():
    from gui.small_capital_strategy_panel import render_simulation_batch_v203_tab
    result = render_simulation_batch_v203_tab()
    assert result["no_real_orders"] is True

def test_render_simulation_batch_version():
    from gui.small_capital_strategy_panel import render_simulation_batch_v203_tab
    result = render_simulation_batch_v203_tab()
    assert result["version"] == "2.0.3"

def test_render_simulation_batch_schema_version():
    from gui.small_capital_strategy_panel import render_simulation_batch_v203_tab
    result = render_simulation_batch_v203_tab()
    assert result["schema_version"] == "203"

def test_render_scenario_replay_v203_tab():
    from gui.small_capital_strategy_panel import render_scenario_replay_v203_tab
    result = render_scenario_replay_v203_tab()
    assert result is not None

def test_render_scenario_replay_tab_key():
    from gui.small_capital_strategy_panel import render_scenario_replay_v203_tab
    result = render_scenario_replay_v203_tab()
    assert result["tab"] == "scenario_replay_v203"

def test_render_scenario_replay_paper_only():
    from gui.small_capital_strategy_panel import render_scenario_replay_v203_tab
    result = render_scenario_replay_v203_tab()
    assert result["paper_only"] is True

def test_render_scenario_replay_no_real_orders():
    from gui.small_capital_strategy_panel import render_scenario_replay_v203_tab
    result = render_scenario_replay_v203_tab()
    assert result["no_real_orders"] is True

def test_render_scenario_replay_version():
    from gui.small_capital_strategy_panel import render_scenario_replay_v203_tab
    result = render_scenario_replay_v203_tab()
    assert result["version"] == "2.0.3"

def test_render_scenario_replay_has_fields():
    from gui.small_capital_strategy_panel import render_scenario_replay_v203_tab
    result = render_scenario_replay_v203_tab()
    assert len(result["scenario_replay_fields"]) == 12

def test_render_strategy_comparison_v203_tab():
    from gui.small_capital_strategy_panel import render_strategy_comparison_v203_tab
    result = render_strategy_comparison_v203_tab()
    assert result is not None

def test_render_strategy_comparison_tab_key():
    from gui.small_capital_strategy_panel import render_strategy_comparison_v203_tab
    result = render_strategy_comparison_v203_tab()
    assert result["tab"] == "strategy_comparison_v203"

def test_render_strategy_comparison_paper_only():
    from gui.small_capital_strategy_panel import render_strategy_comparison_v203_tab
    result = render_strategy_comparison_v203_tab()
    assert result["paper_only"] is True

def test_render_strategy_comparison_no_real_orders():
    from gui.small_capital_strategy_panel import render_strategy_comparison_v203_tab
    result = render_strategy_comparison_v203_tab()
    assert result["no_real_orders"] is True

def test_render_strategy_comparison_version():
    from gui.small_capital_strategy_panel import render_strategy_comparison_v203_tab
    result = render_strategy_comparison_v203_tab()
    assert result["version"] == "2.0.3"

def test_render_strategy_comparison_batch_fields():
    from gui.small_capital_strategy_panel import render_strategy_comparison_v203_tab
    result = render_strategy_comparison_v203_tab()
    assert len(result["batch_comparison_fields"]) == 15

def test_render_strategy_comparison_ranking_fields():
    from gui.small_capital_strategy_panel import render_strategy_comparison_v203_tab
    result = render_strategy_comparison_v203_tab()
    assert len(result["ranking_fields"]) == 10

# ---------------------------------------------------------------------------
# render_all_tabs — critical regression check
# ---------------------------------------------------------------------------

def test_render_all_tabs_no_error_simulation_batch():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    tab = all_rendered.get("simulation_batch_v203", {})
    assert "error" not in str(tab)

def test_render_all_tabs_no_error_scenario_replay():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    tab = all_rendered.get("scenario_replay_v203", {})
    assert "error" not in str(tab)

def test_render_all_tabs_no_error_strategy_comparison():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    tab = all_rendered.get("strategy_comparison_v203", {})
    assert "error" not in str(tab)

def test_render_all_tabs_zero_error_tabs():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    error_tabs = [k for k, v in all_rendered.items() if isinstance(v, dict) and "error" in v]
    assert error_tabs == [], f"Error tabs: {error_tabs}"

def test_render_all_tabs_v202_still_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    for tab in ["report_export_v202", "audit_pack_v202", "export_status_v202"]:
        assert "error" not in str(all_rendered.get(tab, {})), f"{tab} has error"

def test_render_all_tabs_v201_still_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    for tab in ["daily_workflow_v201", "no_entry_reason_detail", "decision_ticket_v201"]:
        assert "error" not in str(all_rendered.get(tab, {})), f"{tab} has error"

def test_render_all_tabs_v200_still_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    for tab in ["paper_cockpit", "strategy_decision_console", "decision_ticket"]:
        assert "error" not in str(all_rendered.get(tab, {})), f"{tab} has error"
