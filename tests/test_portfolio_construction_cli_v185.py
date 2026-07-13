"""
tests/test_portfolio_construction_cli_v185.py
Tests for portfolio construction CLI commands v1.8.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from cli.command_registry import PROVIDER_COMMANDS, get_commands_by_group


def _pc_commands():
    return [c for c in PROVIDER_COMMANDS if c.name.startswith("portfolio-construction")]


def test_pc_commands_count_ge_22():
    assert len(_pc_commands()) >= 22

def test_pc_commands_count_exact():
    assert len(_pc_commands()) == 22

def test_pc_version_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-version" in names

def test_pc_run_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-run" in names

def test_pc_config_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-config" in names

def test_pc_profile_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-profile" in names

def test_pc_holdings_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-holdings" in names

def test_pc_candidates_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-candidates" in names

def test_pc_build_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-build" in names

def test_pc_rebalance_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-rebalance" in names

def test_pc_exposure_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-exposure" in names

def test_pc_sector_risk_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-sector-risk" in names

def test_pc_theme_risk_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-theme-risk" in names

def test_pc_correlation_risk_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-correlation-risk" in names

def test_pc_diversification_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-diversification" in names

def test_pc_rotation_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-rotation" in names

def test_pc_keep_replace_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-keep-replace" in names

def test_pc_dashboard_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-dashboard" in names

def test_pc_report_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-report" in names

def test_pc_scenarios_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-scenarios" in names

def test_pc_fixtures_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-fixtures" in names

def test_pc_health_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-health" in names

def test_pc_gate_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-gate" in names

def test_pc_safety_audit_command_exists():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-construction-safety-audit" in names

def test_pc_commands_group():
    cmds = _pc_commands()
    assert all(c.group == "portfolio_construction" for c in cmds)

def test_pc_commands_introduced_in_185():
    cmds = _pc_commands()
    assert all(c.introduced_in == "1.8.5" for c in cmds)

def test_pc_commands_research_only():
    cmds = _pc_commands()
    assert all(c.safety_classification == "RESEARCH_ONLY" for c in cmds)

def test_pc_commands_have_handler():
    cmds = _pc_commands()
    assert all(len(c.handler_name) > 0 for c in cmds)

def test_pc_commands_have_help():
    cmds = _pc_commands()
    assert all(len(c.help) > 0 for c in cmds)

def test_pc_group_commands():
    grp = get_commands_by_group("portfolio_construction")
    assert len(grp) >= 22

def test_pc_commands_no_duplicates():
    names = [c.name for c in _pc_commands()]
    assert len(names) == len(set(names))

def test_pc_commands_research_prefix_in_help():
    cmds = _pc_commands()
    assert all("[Research]" in c.help for c in cmds)
