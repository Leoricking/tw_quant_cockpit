"""
tests/test_paper_cockpit_cli_v201.py
v2.0.1 Paper Cockpit — CLI Display Tests (30+ tests)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from paper_trading.small_capital_strategy.paper_cockpit_v201 import (
    CLI_COMMANDS_V201, CLIDisplayRow, CLIDisplayOutput,
    DailyWorkflowInput, DailyWorkflowResult,
    run_daily_workflow, build_cli_display,
)


# --- CLI_COMMANDS_V201 tests ---

def test_cli_commands_v201_count():
    assert len(CLI_COMMANDS_V201) == 10

def test_cli_commands_v201_daily_workflow():
    assert "paper-cockpit-daily-workflow" in CLI_COMMANDS_V201

def test_cli_commands_v201_no_entry_reason():
    assert "paper-cockpit-no-entry-reason" in CLI_COMMANDS_V201

def test_cli_commands_v201_final_action():
    assert "paper-cockpit-final-action" in CLI_COMMANDS_V201

def test_cli_commands_v201_candidate_rank():
    assert "paper-cockpit-candidate-rank" in CLI_COMMANDS_V201

def test_cli_commands_v201_risk_budget_status():
    assert "paper-cockpit-risk-budget-status" in CLI_COMMANDS_V201

def test_cli_commands_v201_cli_display():
    assert "paper-cockpit-cli-display" in CLI_COMMANDS_V201

def test_cli_commands_v201_version_201():
    assert "paper-cockpit-version-201" in CLI_COMMANDS_V201

def test_cli_commands_v201_health_201():
    assert "paper-cockpit-health-201" in CLI_COMMANDS_V201

def test_cli_commands_v201_gate_201():
    assert "paper-cockpit-gate-201" in CLI_COMMANDS_V201

def test_cli_commands_v201_safety_audit_201():
    assert "paper-cockpit-safety-audit-201" in CLI_COMMANDS_V201

def test_cli_commands_v201_all_strings():
    assert all(isinstance(c, str) for c in CLI_COMMANDS_V201)


# --- CLIDisplayRow tests ---

def test_cli_display_row_default_schema():
    r = CLIDisplayRow()
    assert r.schema_version == "201"

def test_cli_display_row_default_paper_only():
    r = CLIDisplayRow()
    assert r.paper_only is True

def test_cli_display_row_default_human_review_flag():
    r = CLIDisplayRow()
    assert r.human_review_flag is True

def test_cli_display_row_default_entry_allowed_false():
    r = CLIDisplayRow()
    assert r.entry_allowed is False

def test_cli_display_row_custom_symbol():
    r = CLIDisplayRow(symbol="2330", name="台積電", setup_type="A_PULLBACK_10MA")
    assert r.symbol == "2330"
    assert r.name == "台積電"
    assert r.setup_type == "A_PULLBACK_10MA"

def test_cli_display_row_entry_allowed_paper_buy_plan():
    r = CLIDisplayRow(suggested_paper_action="PAPER_BUY_PLAN", entry_allowed=True)
    assert r.entry_allowed is True
    assert r.suggested_paper_action == "PAPER_BUY_PLAN"

def test_cli_display_row_blocked_reason():
    r = CLIDisplayRow(blocked_reason="trend_broken")
    assert r.blocked_reason == "trend_broken"


# --- CLIDisplayOutput tests ---

def test_cli_display_output_default_schema():
    o = CLIDisplayOutput()
    assert o.schema_version == "201"

def test_cli_display_output_default_paper_only():
    o = CLIDisplayOutput()
    assert o.paper_only is True

def test_cli_display_output_default_no_real_orders():
    o = CLIDisplayOutput()
    assert o.no_real_orders is True

def test_cli_display_output_default_human_review():
    o = CLIDisplayOutput()
    assert o.human_review_required is True

def test_cli_display_output_default_empty():
    o = CLIDisplayOutput()
    assert o.total_candidates == 0
    assert o.top_candidates == []


# --- build_cli_display integration tests ---

def test_build_cli_display_empty_result():
    result = run_daily_workflow(DailyWorkflowInput(candidates=[]))
    display = build_cli_display(result)
    assert isinstance(display, CLIDisplayOutput)
    assert display.total_candidates == 0

def test_build_cli_display_single_candidate():
    inp = DailyWorkflowInput(candidates=["2330"])
    result = run_daily_workflow(inp)
    display = build_cli_display(result)
    assert display.total_candidates == 1
    assert len(display.top_candidates) == 1

def test_build_cli_display_action_counts_sum_to_total():
    inp = DailyWorkflowInput(candidates=["2330", "2454", "2317"])
    result = run_daily_workflow(inp)
    display = build_cli_display(result)
    total = (display.watch_count + display.wait_count + display.paper_buy_plan_count +
             display.paper_add_plan_count + display.paper_reduce_plan_count +
             display.paper_exit_plan_count + display.no_entry_count)
    assert total == display.total_candidates

def test_build_cli_display_paper_only():
    result = run_daily_workflow()
    display = build_cli_display(result)
    assert display.paper_only is True

def test_build_cli_display_human_review_required():
    result = run_daily_workflow()
    display = build_cli_display(result)
    assert display.human_review_required is True

def test_build_cli_display_rows_are_cli_display_rows():
    inp = DailyWorkflowInput(candidates=["2330"])
    result = run_daily_workflow(inp)
    display = build_cli_display(result)
    for row in display.top_candidates:
        assert isinstance(row, CLIDisplayRow)

def test_build_cli_display_row_human_review_flag_true():
    inp = DailyWorkflowInput(candidates=["2330"])
    result = run_daily_workflow(inp)
    display = build_cli_display(result)
    for row in display.top_candidates:
        assert row.human_review_flag is True

def test_cli_display_via_workflow_result():
    inp = DailyWorkflowInput(candidates=["2330"])
    result = run_daily_workflow(inp)
    assert result.cli_display is not None
    assert isinstance(result.cli_display, CLIDisplayOutput)

def test_cli_commands_registered_in_provider():
    from cli.command_registry import PROVIDER_COMMANDS
    command_names = {c.name for c in PROVIDER_COMMANDS}
    for cmd in CLI_COMMANDS_V201:
        assert cmd in command_names, f"CLI command '{cmd}' not registered in PROVIDER_COMMANDS"
