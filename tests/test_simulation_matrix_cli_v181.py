"""
tests/test_simulation_matrix_cli_v181.py
Tests for v1.8.1 CLI commands registered in command_registry.py.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
import pytest
from cli.command_registry import (
    get_formal_command_names, get_commands_by_group, PROVIDER_COMMANDS,
)


# ── Core CLI commands present ──────────────────────────────────────────────────

def test_cli_simulation_matrix_version():
    assert "simulation-matrix-version" in get_formal_command_names()

def test_cli_simulation_matrix_run():
    assert "simulation-matrix-run" in get_formal_command_names()

def test_cli_simulation_matrix_config():
    assert "simulation-matrix-config" in get_formal_command_names()

def test_cli_simulation_matrix_axis():
    assert "simulation-matrix-axis" in get_formal_command_names()

def test_cli_simulation_matrix_cell():
    assert "simulation-matrix-cell" in get_formal_command_names()

def test_cli_simulation_matrix_result():
    assert "simulation-matrix-result" in get_formal_command_names()

def test_cli_simulation_stress_test():
    assert "simulation-stress-test" in get_formal_command_names()

def test_cli_simulation_stress_drawdown():
    assert "simulation-stress-drawdown" in get_formal_command_names()

def test_cli_simulation_stress_losing_streak():
    assert "simulation-stress-losing-streak" in get_formal_command_names()

def test_cli_simulation_stress_regime_shift():
    assert "simulation-stress-regime-shift" in get_formal_command_names()

def test_cli_simulation_stress_theme_collapse():
    assert "simulation-stress-theme-collapse" in get_formal_command_names()

def test_cli_simulation_stress_mistake_impact():
    assert "simulation-stress-mistake-impact" in get_formal_command_names()

def test_cli_simulation_robustness_score():
    assert "simulation-robustness-score" in get_formal_command_names()

def test_cli_simulation_matrix_dashboard():
    assert "simulation-matrix-dashboard" in get_formal_command_names()

def test_cli_simulation_matrix_report():
    assert "simulation-matrix-report" in get_formal_command_names()

def test_cli_simulation_matrix_scenarios():
    assert "simulation-matrix-scenarios" in get_formal_command_names()

def test_cli_simulation_matrix_fixtures():
    assert "simulation-matrix-fixtures" in get_formal_command_names()

def test_cli_simulation_matrix_health():
    assert "simulation-matrix-health" in get_formal_command_names()

def test_cli_simulation_matrix_gate():
    assert "simulation-matrix-gate" in get_formal_command_names()

def test_cli_simulation_matrix_safety_audit():
    assert "simulation-matrix-safety-audit" in get_formal_command_names()


# ── Group membership ───────────────────────────────────────────────────────────

def test_cli_group_simulation_matrix_count_ge_20():
    group = get_commands_by_group("simulation_matrix")
    assert len(group) >= 20

def test_cli_group_simulation_matrix_all_research_only():
    group = get_commands_by_group("simulation_matrix")
    assert all(c.safety_classification == "RESEARCH_ONLY" for c in group)

def test_cli_group_simulation_matrix_all_introduced_181():
    group = get_commands_by_group("simulation_matrix")
    assert all(c.introduced_in == "1.8.1" for c in group)


# ── Safety enforcement: no real trade commands ─────────────────────────────────

def test_no_real_buy_command():
    names = get_formal_command_names()
    assert not any("real-buy" in n or "execute-buy" in n for n in names)

def test_no_live_order_command():
    names = get_formal_command_names()
    assert not any("live-order" in n for n in names)

def test_simulation_commands_no_forbidden_words():
    group = get_commands_by_group("simulation_matrix")
    forbidden = {"BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER"}
    for cmd in group:
        for word in forbidden:
            assert word.lower() not in cmd.name, f"Forbidden word in cmd: {cmd.name}"


# ── Handler names ──────────────────────────────────────────────────────────────

def test_handler_name_version():
    group = get_commands_by_group("simulation_matrix")
    cmd = next((c for c in group if c.name == "simulation-matrix-version"), None)
    assert cmd is not None
    assert cmd.handler_name == "cmd_simulation_matrix_version"

def test_handler_name_stress_test():
    group = get_commands_by_group("simulation_matrix")
    cmd = next((c for c in group if c.name == "simulation-stress-test"), None)
    assert cmd is not None
    assert cmd.handler_name == "cmd_simulation_stress_test"

def test_handler_name_health():
    group = get_commands_by_group("simulation_matrix")
    cmd = next((c for c in group if c.name == "simulation-matrix-health"), None)
    assert cmd is not None
    assert cmd.handler_name == "cmd_simulation_matrix_health"
