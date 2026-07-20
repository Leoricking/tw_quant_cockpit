"""
tests/test_paper_cockpit_cli_v203.py
v2.0.3 CLI Command Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# PROVIDER_COMMANDS registration
# ---------------------------------------------------------------------------

def test_provider_commands_has_simulate_one():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v203-simulate-one" in names

def test_provider_commands_has_simulate_batch():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v203-simulate-batch" in names

def test_provider_commands_has_replay_scenario():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v203-replay-scenario" in names

def test_provider_commands_has_compare_profiles():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v203-compare-profiles" in names

def test_provider_commands_has_rank_results():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v203-rank-results" in names

def test_provider_commands_has_export_json():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v203-export-json" in names

def test_provider_commands_has_export_md():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v203-export-md" in names

def test_provider_commands_has_export_csv():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v203-export-csv" in names

def test_provider_commands_has_health():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v203-health" in names

def test_provider_commands_has_gate():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v203-gate" in names

# ---------------------------------------------------------------------------
# command group
# ---------------------------------------------------------------------------

def test_v203_commands_group():
    from cli.command_registry import PROVIDER_COMMANDS
    v203_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("paper-cockpit-v203")]
    for cmd in v203_cmds:
        assert cmd.group == "paper_cockpit_v203"

def test_v203_commands_count():
    from cli.command_registry import PROVIDER_COMMANDS
    v203_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("paper-cockpit-v203")]
    assert len(v203_cmds) == 10

def test_v203_commands_safety_classification():
    from cli.command_registry import PROVIDER_COMMANDS
    v203_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("paper-cockpit-v203")]
    for cmd in v203_cmds:
        assert cmd.safety_classification == "RESEARCH_ONLY"

def test_v203_commands_introduced_in():
    from cli.command_registry import PROVIDER_COMMANDS
    v203_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("paper-cockpit-v203")]
    for cmd in v203_cmds:
        assert cmd.introduced_in == "2.0.3"

# ---------------------------------------------------------------------------
# v2.0.2 commands backward compat
# ---------------------------------------------------------------------------

def test_v202_commands_still_present():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    for cmd in [
        "paper-cockpit-v202-report-json",
        "paper-cockpit-v202-report-md",
        "paper-cockpit-v202-report-csv",
        "paper-cockpit-v202-audit-pack",
        "paper-cockpit-v202-export-all",
        "paper-cockpit-v202-health",
        "paper-cockpit-v202-gate",
    ]:
        assert cmd in names, f"v2.0.2 command {cmd} missing"

# ---------------------------------------------------------------------------
# v2.0.1 commands backward compat
# ---------------------------------------------------------------------------

def test_v201_commands_still_present():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    for cmd in [
        "paper-cockpit-daily-workflow",
        "paper-cockpit-no-entry-reason",
        "paper-cockpit-final-action",
        "paper-cockpit-candidate-rank",
        "paper-cockpit-risk-budget-status",
        "paper-cockpit-cli-display",
        "paper-cockpit-version-201",
        "paper-cockpit-health-201",
        "paper-cockpit-gate-201",
        "paper-cockpit-safety-audit-201",
    ]:
        assert cmd in names, f"v2.0.1 command {cmd} missing"

# ---------------------------------------------------------------------------
# main.py handlers
# ---------------------------------------------------------------------------

def test_main_handler_simulate_one():
    from main import cmd_paper_cockpit_v203_simulate_one
    assert callable(cmd_paper_cockpit_v203_simulate_one)

def test_main_handler_simulate_batch():
    from main import cmd_paper_cockpit_v203_simulate_batch
    assert callable(cmd_paper_cockpit_v203_simulate_batch)

def test_main_handler_replay_scenario():
    from main import cmd_paper_cockpit_v203_replay_scenario
    assert callable(cmd_paper_cockpit_v203_replay_scenario)

def test_main_handler_compare_profiles():
    from main import cmd_paper_cockpit_v203_compare_profiles
    assert callable(cmd_paper_cockpit_v203_compare_profiles)

def test_main_handler_rank_results():
    from main import cmd_paper_cockpit_v203_rank_results
    assert callable(cmd_paper_cockpit_v203_rank_results)

def test_main_handler_export_json():
    from main import cmd_paper_cockpit_v203_export_json
    assert callable(cmd_paper_cockpit_v203_export_json)

def test_main_handler_export_md():
    from main import cmd_paper_cockpit_v203_export_md
    assert callable(cmd_paper_cockpit_v203_export_md)

def test_main_handler_export_csv():
    from main import cmd_paper_cockpit_v203_export_csv
    assert callable(cmd_paper_cockpit_v203_export_csv)

def test_main_handler_health():
    from main import cmd_paper_cockpit_v203_health
    assert callable(cmd_paper_cockpit_v203_health)

def test_main_handler_gate():
    from main import cmd_paper_cockpit_v203_gate
    assert callable(cmd_paper_cockpit_v203_gate)

# ---------------------------------------------------------------------------
# CLI_COMMANDS_V203 in module
# ---------------------------------------------------------------------------

def test_cli_commands_v203_in_module():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    assert len(CLI_COMMANDS_V203) == 10

def test_cli_commands_v203_all_in_registry():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import CLI_COMMANDS_V203
    from cli.command_registry import PROVIDER_COMMANDS
    registry_names = {c.name for c in PROVIDER_COMMANDS}
    for cmd in CLI_COMMANDS_V203:
        assert cmd in registry_names, f"CLI command '{cmd}' not in PROVIDER_COMMANDS"
