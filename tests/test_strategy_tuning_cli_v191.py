"""tests/test_strategy_tuning_cli_v191.py
Tests for strategy tuning CLI commands v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
"""
import pytest
from cli.command_registry import (
    get_all_commands, get_commands_by_group, get_command,
)

_ST_COMMANDS = [c for c in get_commands_by_group("strategy_tuning") if c.introduced_in == "1.9.1"]


def test_strategy_tuning_commands_count_18():
    assert len(_ST_COMMANDS) >= 18

def test_command_strategy_tuning_version_exists():
    assert get_command("strategy-tuning-version") is not None

def test_command_strategy_tuning_review_exists():
    assert get_command("strategy-tuning-review") is not None

def test_command_strategy_tuning_rules_exists():
    assert get_command("strategy-tuning-rules") is not None

def test_command_strategy_tuning_guardrails_exists():
    assert get_command("strategy-tuning-guardrails") is not None

def test_command_strategy_tuning_recommend_exists():
    assert get_command("strategy-tuning-recommend") is not None

def test_command_strategy_tuning_abc_exists():
    assert get_command("strategy-tuning-abc") is not None

def test_command_strategy_tuning_position_sizing_exists():
    assert get_command("strategy-tuning-position-sizing") is not None

def test_command_strategy_tuning_cash_reserve_exists():
    assert get_command("strategy-tuning-cash-reserve") is not None

def test_command_strategy_tuning_concentration_exists():
    assert get_command("strategy-tuning-concentration") is not None

def test_command_strategy_tuning_evidence_exists():
    assert get_command("strategy-tuning-evidence") is not None

def test_command_strategy_tuning_dashboard_exists():
    assert get_command("strategy-tuning-dashboard") is not None

def test_command_strategy_tuning_export_exists():
    assert get_command("strategy-tuning-export") is not None

def test_command_strategy_tuning_audit_exists():
    assert get_command("strategy-tuning-audit") is not None

def test_command_strategy_tuning_health_exists():
    assert get_command("strategy-tuning-health") is not None

def test_command_strategy_tuning_gate_exists():
    assert get_command("strategy-tuning-gate") is not None

def test_command_strategy_tuning_scenarios_exists():
    assert get_command("strategy-tuning-scenarios") is not None

def test_command_strategy_tuning_fixtures_exists():
    assert get_command("strategy-tuning-fixtures") is not None

def test_command_strategy_tuning_safety_audit_exists():
    assert get_command("strategy-tuning-safety-audit") is not None

def test_all_st_commands_introduced_in_191():
    assert all(c.introduced_in == "1.9.1" for c in _ST_COMMANDS)

def test_all_st_commands_group_strategy_tuning():
    assert all(c.group == "strategy_tuning" for c in _ST_COMMANDS)

def test_all_st_commands_safety_level_research_only():
    assert all(c.safety_classification == "RESEARCH_ONLY" for c in _ST_COMMANDS)

def test_all_st_commands_read_only():
    assert all(c.research_only is True for c in _ST_COMMANDS)

def test_all_st_commands_handler_names_not_empty():
    assert all(c.handler_name != "" for c in _ST_COMMANDS)

def test_strategy_tuning_version_handler_name():
    cmd = get_command("strategy-tuning-version")
    assert cmd.handler_name == "cmd_strategy_tuning_version"

def test_strategy_tuning_health_handler_name():
    cmd = get_command("strategy-tuning-health")
    assert cmd.handler_name == "cmd_strategy_tuning_health"
