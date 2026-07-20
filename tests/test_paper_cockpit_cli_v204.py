"""
tests/test_paper_cockpit_cli_v204.py
v2.0.4 Paper Portfolio Review Loop & Weekly Improvement Pack — CLI Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

def test_v204_cli_commands_in_provider_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v204-review-weekly" in names

def test_cli_review_portfolio_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v204-review-portfolio" in names

def test_cli_review_strategy_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v204-review-strategy" in names

def test_cli_review_blocked_reasons_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v204-review-blocked-reasons" in names

def test_cli_review_risk_usage_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v204-review-risk-usage" in names

def test_cli_generate_improvement_pack_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v204-generate-improvement-pack" in names

def test_cli_export_json_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v204-export-json" in names

def test_cli_export_md_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v204-export-md" in names

def test_cli_export_csv_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v204-export-csv" in names

def test_cli_health_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v204-health" in names

def test_cli_gate_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v204-gate" in names

def test_all_v204_cli_commands_in_registry():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    from cli.command_registry import PROVIDER_COMMANDS
    registry_names = {c.name for c in PROVIDER_COMMANDS}
    for cmd in CLI_COMMANDS_V204:
        assert cmd in registry_names, f"CLI command '{cmd}' missing from PROVIDER_COMMANDS"

def test_v204_commands_research_only():
    from cli.command_registry import PROVIDER_COMMANDS
    v204_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("paper-cockpit-v204")]
    assert len(v204_cmds) == 11
    for cmd in v204_cmds:
        assert cmd.safety_classification == "RESEARCH_ONLY"

def test_v204_commands_introduced_in_204():
    from cli.command_registry import PROVIDER_COMMANDS
    v204_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("paper-cockpit-v204")]
    for cmd in v204_cmds:
        assert cmd.introduced_in == "2.0.4"

def test_v204_commands_group():
    from cli.command_registry import PROVIDER_COMMANDS
    v204_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("paper-cockpit-v204")]
    for cmd in v204_cmds:
        assert cmd.group == "paper_cockpit_v204"

def test_v203_commands_still_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v203-simulate-one" in names
    assert "paper-cockpit-v203-simulate-batch" in names

def test_v202_commands_still_in_registry():
    from cli.command_registry import PROVIDER_COMMANDS
    names = {c.name for c in PROVIDER_COMMANDS}
    assert "paper-cockpit-v202-report-json" in names

def test_no_duplicate_command_names():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert len(names) == len(set(names)), "Duplicate CLI command names found"
