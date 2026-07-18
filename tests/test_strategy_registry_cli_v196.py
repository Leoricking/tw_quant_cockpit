"""
tests/test_strategy_registry_cli_v196.py
Tests for CLI commands for strategy registry v1.9.6 — Paper Strategy Decision Registry & Governance Lab.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
import pytest
from cli.command_registry import PROVIDER_COMMANDS, get_commands_by_group


# ── command group ─────────────────────────────────────────────────────────────

def test_strategy_registry_group_commands_count_18():
    cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("strategy-registry-")]
    assert len(cmds) >= 18

def test_get_commands_by_group_returns_registry():
    cmds = get_commands_by_group("strategy_registry")
    assert len(cmds) >= 18


# ── specific commands exist ───────────────────────────────────────────────────

def test_cli_strategy_registry_version():
    assert any(c.name == "strategy-registry-version" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_register():
    assert any(c.name == "strategy-registry-register" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_list():
    assert any(c.name == "strategy-registry-list" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_get():
    assert any(c.name == "strategy-registry-get" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_governance_check():
    assert any(c.name == "strategy-registry-governance-check" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_governance_report():
    assert any(c.name == "strategy-registry-governance-report" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_lineage():
    assert any(c.name == "strategy-registry-lineage" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_evidence():
    assert any(c.name == "strategy-registry-evidence" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_audit_trail():
    assert any(c.name == "strategy-registry-audit-trail" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_dashboard():
    assert any(c.name == "strategy-registry-dashboard" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_export():
    assert any(c.name == "strategy-registry-export" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_validate():
    assert any(c.name == "strategy-registry-validate" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_queue():
    assert any(c.name == "strategy-registry-queue" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_violation_report():
    assert any(c.name == "strategy-registry-violation-report" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_retention_policy():
    assert any(c.name == "strategy-registry-retention-policy" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_full_pack():
    assert any(c.name == "strategy-registry-full-pack" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_gate():
    assert any(c.name == "strategy-registry-gate" for c in PROVIDER_COMMANDS)

def test_cli_strategy_registry_safety_audit():
    assert any(c.name == "strategy-registry-safety-audit" for c in PROVIDER_COMMANDS)


# ── command metadata ──────────────────────────────────────────────────────────

def test_registry_commands_introduced_in_196():
    cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("strategy-registry-")]
    assert all(c.introduced_in == "1.9.6" for c in cmds)

def test_registry_commands_group_is_strategy_registry():
    cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("strategy-registry-")]
    assert all(c.group == "strategy_registry" for c in cmds)
