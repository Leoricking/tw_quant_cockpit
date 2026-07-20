"""
tests/test_paper_cockpit_backward_compat_v204.py
v2.0.4 Backward Compatibility Tests — v2.0.3, v2.0.2, v2.0.1, v2.0.0
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# v2.0.3 backward compatibility
# ---------------------------------------------------------------------------

def test_v203_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v203

def test_v203_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import VERSION
    assert VERSION == "2.0.3"

def test_v203_simulate_one_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.all_passed is True

def test_v203_simulate_one_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one
    result = simulate_one()
    assert result.paper_only is True

def test_v203_simulate_batch_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_batch
    result = simulate_batch()
    assert result.all_passed is True

def test_v203_replay_scenario_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import replay_scenario
    result = replay_scenario()
    assert result is not None

def test_v203_export_json_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_json
    result = export_simulation_json(simulate_one())
    assert result.is_valid is True

def test_v203_safety_flags_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SAFETY_FLAGS_V203
    assert len(SAFETY_FLAGS_V203) == 20
    assert SAFETY_FLAGS_V203["paper_only"] is True
    assert SAFETY_FLAGS_V203["no_real_orders"] is True

def test_v203_no_real_orders_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_v203_broker_disabled_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_v203_scenarios_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v203 import SCENARIOS
    assert len(SCENARIOS) == 80

def test_v203_fixtures_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v203 import FIXTURES
    assert len(FIXTURES) == 80

# ---------------------------------------------------------------------------
# v2.0.2 backward compatibility
# ---------------------------------------------------------------------------

def test_v202_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v202

def test_v202_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import VERSION
    assert VERSION == "2.0.2"

def test_v202_export_json_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    assert result.is_valid is True

# ---------------------------------------------------------------------------
# v2.0.1 backward compatibility
# ---------------------------------------------------------------------------

def test_v201_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v201

def test_v201_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import VERSION
    assert VERSION == "2.0.1"

def test_v201_run_daily_workflow_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import run_daily_workflow
    result = run_daily_workflow()
    assert result.paper_only is True

# ---------------------------------------------------------------------------
# v2.0.0 backward compatibility
# ---------------------------------------------------------------------------

def test_v200_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v200

def test_v200_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION
    assert VERSION == "2.0.0"

# ---------------------------------------------------------------------------
# GUI backward compatibility
# ---------------------------------------------------------------------------

def test_gui_v203_tabs_still_registered():
    from gui.small_capital_strategy_panel import get_tab_names
    tabs = get_tab_names()
    assert "simulation_batch_v203" in tabs
    assert "scenario_replay_v203" in tabs
    assert "strategy_comparison_v203" in tabs

def test_gui_v202_tabs_still_registered():
    from gui.small_capital_strategy_panel import get_tab_names
    tabs = get_tab_names()
    assert "report_export_v202" in tabs
    assert "audit_pack_v202" in tabs

def test_gui_v201_tabs_still_registered():
    from gui.small_capital_strategy_panel import get_tab_names
    tabs = get_tab_names()
    assert "daily_workflow_v201" in tabs

def test_gui_v200_tabs_still_registered():
    from gui.small_capital_strategy_panel import get_tab_names
    tabs = get_tab_names()
    assert "paper_cockpit" in tabs

def test_gui_v203_render_functions_callable():
    from gui.small_capital_strategy_panel import (
        render_simulation_batch_v203_tab, render_scenario_replay_v203_tab,
        render_strategy_comparison_v203_tab,
    )
    r1 = render_simulation_batch_v203_tab()
    r2 = render_scenario_replay_v203_tab()
    r3 = render_strategy_comparison_v203_tab()
    assert r1["tab"] == "simulation_batch_v203"
    assert r2["tab"] == "scenario_replay_v203"
    assert r3["tab"] == "strategy_comparison_v203"

def test_panel_version_v203_unchanged():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V203
    assert PANEL_VERSION_V203 == "2.0.3"

def test_panel_version_v202_unchanged():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V202
    assert PANEL_VERSION_V202 == "2.0.2"

def test_panel_version_v201_unchanged():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V201
    assert PANEL_VERSION_V201 == "2.0.1"

# ---------------------------------------------------------------------------
# CLI backward compatibility
# ---------------------------------------------------------------------------

def test_v203_cli_commands_still_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    v203_cmds = [
        "paper-cockpit-v203-simulate-one", "paper-cockpit-v203-simulate-batch",
        "paper-cockpit-v203-export-json", "paper-cockpit-v203-health",
    ]
    for cmd in v203_cmds:
        assert cmd in names, f"v2.0.3 CLI command '{cmd}' missing"

def test_v202_cli_commands_still_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v202-report-json" in names
    assert "paper-cockpit-v202-health" in names

def test_v201_cli_commands_still_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-daily-workflow" in names
