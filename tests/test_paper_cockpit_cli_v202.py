"""
tests/test_paper_cockpit_cli_v202.py
v2.0.2 Paper Cockpit — CLI Tests (30+)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest


# ---------------------------------------------------------------------------
# CLI command list tests
# ---------------------------------------------------------------------------

def test_cli_commands_v202_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert isinstance(CLI_COMMANDS_V202, list)


def test_cli_commands_v202_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert len(CLI_COMMANDS_V202) == 7


def test_cli_all_v202_prefixed():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert all("v202" in cmd for cmd in CLI_COMMANDS_V202)


def test_cli_all_paper_cockpit_prefixed():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert all("paper-cockpit" in cmd for cmd in CLI_COMMANDS_V202)


def test_cli_command_report_json_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-report-json" in CLI_COMMANDS_V202


def test_cli_command_report_md_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-report-md" in CLI_COMMANDS_V202


def test_cli_command_report_csv_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-report-csv" in CLI_COMMANDS_V202


def test_cli_command_audit_pack_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-audit-pack" in CLI_COMMANDS_V202


def test_cli_command_export_all_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-export-all" in CLI_COMMANDS_V202


def test_cli_command_health_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-health" in CLI_COMMANDS_V202


def test_cli_command_gate_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import CLI_COMMANDS_V202
    assert "paper-cockpit-v202-gate" in CLI_COMMANDS_V202


# ---------------------------------------------------------------------------
# CLI handler function tests (via main.py)
# ---------------------------------------------------------------------------

def test_cmd_v202_report_json_callable():
    from main import cmd_paper_cockpit_v202_report_json
    cmd_paper_cockpit_v202_report_json()


def test_cmd_v202_report_md_callable():
    from main import cmd_paper_cockpit_v202_report_md
    cmd_paper_cockpit_v202_report_md()


def test_cmd_v202_report_csv_callable():
    from main import cmd_paper_cockpit_v202_report_csv
    cmd_paper_cockpit_v202_report_csv()


def test_cmd_v202_audit_pack_callable():
    from main import cmd_paper_cockpit_v202_audit_pack
    cmd_paper_cockpit_v202_audit_pack()


def test_cmd_v202_export_all_callable():
    from main import cmd_paper_cockpit_v202_export_all
    cmd_paper_cockpit_v202_export_all()


def test_cmd_v202_health_callable():
    from main import cmd_paper_cockpit_v202_health
    cmd_paper_cockpit_v202_health()


def test_cmd_v202_gate_callable():
    from main import cmd_paper_cockpit_v202_gate
    cmd_paper_cockpit_v202_gate()


# ---------------------------------------------------------------------------
# CLI registry tests (command_registry.py)
# ---------------------------------------------------------------------------

def test_registry_has_v202_report_json():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v202-report-json" in names


def test_registry_has_v202_report_md():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v202-report-md" in names


def test_registry_has_v202_report_csv():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v202-report-csv" in names


def test_registry_has_v202_audit_pack():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v202-audit-pack" in names


def test_registry_has_v202_export_all():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v202-export-all" in names


def test_registry_has_v202_health():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v202-health" in names


def test_registry_has_v202_gate():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v202-gate" in names


def test_registry_v202_commands_group():
    from cli.command_registry import PROVIDER_COMMANDS
    v202_cmds = [cmd for cmd in PROVIDER_COMMANDS if "v202" in cmd.name]
    assert len(v202_cmds) == 7
    for cmd in v202_cmds:
        assert cmd.group == "paper_cockpit_v202"


def test_registry_v202_introduced_in():
    from cli.command_registry import PROVIDER_COMMANDS
    v202_cmds = [cmd for cmd in PROVIDER_COMMANDS if "v202" in cmd.name]
    for cmd in v202_cmds:
        assert cmd.introduced_in == "2.0.2"
