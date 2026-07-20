"""
tests/test_paper_cockpit_backward_compat_v203.py
v2.0.3 Backward Compatibility Tests (v2.0.0, v2.0.1, v2.0.2 still intact)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# v2.0.0 backward compat
# ---------------------------------------------------------------------------

def test_v200_import():
    import paper_trading.small_capital_strategy.paper_cockpit_v200

def test_v200_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import VERSION
    assert VERSION == "2.0.0"

def test_v200_safety_flags():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import SAFETY_FLAGS
    assert SAFETY_FLAGS.get("paper_only") is True

def test_v200_safety_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import SAFETY_FLAGS
    assert SAFETY_FLAGS.get("no_real_orders") is True

def test_v200_safety_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import SAFETY_FLAGS
    assert SAFETY_FLAGS.get("no_broker") is True

def test_v200_run_cockpit_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v200 import run_cockpit
    result = run_cockpit()
    assert result.paper_only is True

def test_v200_scenarios_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v200 import SCENARIOS
    assert len(SCENARIOS) == 80

def test_v200_fixtures_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v200 import FIXTURES
    assert len(FIXTURES) == 80

# ---------------------------------------------------------------------------
# v2.0.1 backward compat
# ---------------------------------------------------------------------------

def test_v201_import():
    import paper_trading.small_capital_strategy.paper_cockpit_v201

def test_v201_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import VERSION
    assert VERSION == "2.0.1"

def test_v201_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_v201_run_daily_workflow_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import run_daily_workflow
    result = run_daily_workflow()
    assert result.paper_only is True

def test_v201_no_entry_reasons_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import NO_ENTRY_REASONS
    assert len(NO_ENTRY_REASONS) == 13

def test_v201_daily_final_actions_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import DAILY_FINAL_ACTIONS
    assert len(DAILY_FINAL_ACTIONS) == 7

def test_v201_scenarios_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v201 import SCENARIOS
    assert len(SCENARIOS) == 80

def test_v201_fixtures_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v201 import FIXTURES
    assert len(FIXTURES) == 80

def test_v201_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v201 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "201"

# ---------------------------------------------------------------------------
# v2.0.2 backward compat
# ---------------------------------------------------------------------------

def test_v202_import():
    import paper_trading.small_capital_strategy.paper_cockpit_v202

def test_v202_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import VERSION
    assert VERSION == "2.0.2"

def test_v202_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_v202_export_json_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_json
    result = export_json()
    assert result.is_valid is True

def test_v202_export_markdown_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_markdown
    result = export_markdown()
    assert result.paper_only is True

def test_v202_export_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import export_csv
    result = export_csv()
    assert result.export_ok is True

def test_v202_build_audit_pack_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.reproducibility_hash

def test_v202_export_formats_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import EXPORT_FORMATS
    assert len(EXPORT_FORMATS) == 4

def test_v202_audit_pack_fields_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AUDIT_PACK_FIELDS
    assert len(AUDIT_PACK_FIELDS) == 11

def test_v202_scenarios_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v202 import SCENARIOS
    assert len(SCENARIOS) == 80

def test_v202_fixtures_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v202 import FIXTURES
    assert len(FIXTURES) == 80

def test_v202_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "202"

def test_v202_safety_flags_intact():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import SAFETY_FLAGS_V202
    assert SAFETY_FLAGS_V202.get("paper_only") is True

# ---------------------------------------------------------------------------
# GUI panel backward compat
# ---------------------------------------------------------------------------

def test_panel_version_still_200():
    from gui.small_capital_strategy_panel import PANEL_VERSION
    assert PANEL_VERSION == "2.0.0"

def test_panel_v201_still_201():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V201
    assert PANEL_VERSION_V201 == "2.0.1"

def test_panel_v202_still_202():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V202
    assert PANEL_VERSION_V202 == "2.0.2"

def test_v200_tabs_still_present():
    from gui.small_capital_strategy_panel import get_tab_names
    tab_names = get_tab_names()
    for tab in ["paper_cockpit", "strategy_decision_console", "decision_ticket"]:
        assert tab in tab_names

def test_v201_tabs_still_present():
    from gui.small_capital_strategy_panel import get_tab_names
    tab_names = get_tab_names()
    for tab in ["daily_workflow_v201", "no_entry_reason_detail", "decision_ticket_v201"]:
        assert tab in tab_names

def test_v202_tabs_still_present():
    from gui.small_capital_strategy_panel import get_tab_names
    tab_names = get_tab_names()
    for tab in ["report_export_v202", "audit_pack_v202", "export_status_v202"]:
        assert tab in tab_names

def test_render_all_tabs_zero_error_tabs():
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    error_tabs = [k for k, v in all_rendered.items() if isinstance(v, dict) and "error" in v]
    assert error_tabs == [], f"Error tabs found: {error_tabs}"

def test_v200_render_functions_still_work():
    from gui.small_capital_strategy_panel import render_all_tabs
    rendered = render_all_tabs()
    for tab in ["paper_cockpit", "strategy_decision_console", "decision_ticket"]:
        assert "error" not in str(rendered.get(tab, {}))

def test_v201_render_functions_still_work():
    from gui.small_capital_strategy_panel import render_all_tabs
    rendered = render_all_tabs()
    for tab in ["daily_workflow_v201", "no_entry_reason_detail", "decision_ticket_v201"]:
        assert "error" not in str(rendered.get(tab, {}))

def test_v202_render_functions_still_work():
    from gui.small_capital_strategy_panel import render_all_tabs
    rendered = render_all_tabs()
    for tab in ["report_export_v202", "audit_pack_v202", "export_status_v202"]:
        assert "error" not in str(rendered.get(tab, {}))

# ---------------------------------------------------------------------------
# CLI backward compat
# ---------------------------------------------------------------------------

def test_v200_cli_commands_still_present():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    for cmd in [
        "paper-cockpit-version", "paper-cockpit-run", "paper-cockpit-watchlist",
        "paper-cockpit-score", "paper-cockpit-abc-check",
    ]:
        assert cmd in names

def test_v201_cli_commands_still_present():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-daily-workflow" in names

def test_v202_cli_commands_still_present():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v202-report-json" in names
