"""
tests/test_decision_cockpit_cli_v186.py
Tests for decision cockpit CLI commands v1.8.6.
[!] Research Only. Paper Only. Decision Only. No Real Orders. Not Investment Advice.
"""
import pytest
from cli.command_registry import PROVIDER_COMMANDS


def _dc_commands():
    return [c for c in PROVIDER_COMMANDS if c.name.startswith("decision-cockpit")]


def test_dc_commands_count_ge_22():
    assert len(_dc_commands()) >= 22

def test_dc_version_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-version" in names

def test_dc_run_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-run" in names

def test_dc_config_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-config" in names

def test_dc_daily_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-daily" in names

def test_dc_weekly_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-weekly" in names

def test_dc_market_regime_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-market-regime" in names

def test_dc_watchlist_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-watchlist" in names

def test_dc_candidates_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-candidates" in names

def test_dc_buy_points_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-buy-points" in names

def test_dc_risk_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-risk" in names

def test_dc_position_sizing_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-position-sizing" in names

def test_dc_portfolio_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-portfolio" in names

def test_dc_monte_carlo_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-monte-carlo" in names

def test_dc_theme_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-theme" in names

def test_dc_blocks_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-blocks" in names

def test_dc_dashboard_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-dashboard" in names

def test_dc_report_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-report" in names

def test_dc_scenarios_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-scenarios" in names

def test_dc_fixtures_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-fixtures" in names

def test_dc_health_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-health" in names

def test_dc_gate_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-gate" in names

def test_dc_safety_audit_command_exists():
    names = [c.name for c in _dc_commands()]
    assert "decision-cockpit-safety-audit" in names

def test_dc_commands_unique_names():
    names = [c.name for c in _dc_commands()]
    assert len(names) == len(set(names))

def test_dc_commands_all_research_only():
    for c in _dc_commands():
        assert c.safety_classification == "RESEARCH_ONLY", f"{c.name} has wrong safety level"

def test_dc_commands_all_introduced_186():
    for c in _dc_commands():
        assert c.introduced_in == "1.8.6", f"{c.name} wrong introduced_in"

def test_dc_commands_all_decision_cockpit_group():
    for c in _dc_commands():
        assert c.group == "decision_cockpit", f"{c.name} wrong group"

def test_dc_commands_all_have_help():
    for c in _dc_commands():
        assert c.help, f"{c.name} missing help text"

def test_dc_commands_version_help_contains_research():
    cmd = next(c for c in _dc_commands() if c.name == "decision-cockpit-version")
    assert "Research" in cmd.help

def test_all_provider_commands_no_buy_command():
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "buy" not in " ".join(names).lower() or all("buy-point" in n or "buy_point" in n
                                                         for n in names if "buy" in n.lower())

def test_total_provider_commands_increased():
    assert len(PROVIDER_COMMANDS) >= 22
