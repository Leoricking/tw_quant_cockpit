"""tests/test_strategy_promotion_cli_v193.py — v1.9.3 CLI registration tests."""
import pytest
from cli.command_registry import PROVIDER_COMMANDS


def _names():
    return [c.name for c in PROVIDER_COMMANDS]


# ── command presence ──────────────────────────────────────────────────────────
def test_cli_strategy_promotion_version(): assert "strategy-promotion-version" in _names()
def test_cli_strategy_promotion_build(): assert "strategy-promotion-build" in _names()
def test_cli_strategy_promotion_rollback(): assert "strategy-promotion-rollback" in _names()
def test_cli_strategy_promotion_gate(): assert "strategy-promotion-gate" in _names()
def test_cli_strategy_promotion_checklist(): assert "strategy-promotion-checklist" in _names()
def test_cli_strategy_promotion_recommendation(): assert "strategy-promotion-recommendation" in _names()
def test_cli_strategy_promotion_evidence(): assert "strategy-promotion-evidence" in _names()
def test_cli_strategy_promotion_audit_trail(): assert "strategy-promotion-audit-trail" in _names()
def test_cli_strategy_promotion_dashboard(): assert "strategy-promotion-dashboard" in _names()
def test_cli_strategy_promotion_export(): assert "strategy-promotion-export" in _names()
def test_cli_strategy_promotion_validate(): assert "strategy-promotion-validate" in _names()
def test_cli_strategy_promotion_report(): assert "strategy-promotion-report" in _names()
def test_cli_strategy_promotion_scenarios(): assert "strategy-promotion-scenarios" in _names()
def test_cli_strategy_promotion_fixtures(): assert "strategy-promotion-fixtures" in _names()
def test_cli_strategy_promotion_health(): assert "strategy-promotion-health" in _names()
def test_cli_strategy_promotion_rollback_validate(): assert "strategy-promotion-rollback-validate" in _names()
def test_cli_strategy_promotion_approval_state(): assert "strategy-promotion-approval-state" in _names()
def test_cli_strategy_promotion_safety_audit(): assert "strategy-promotion-safety-audit" in _names()

# ── count ─────────────────────────────────────────────────────────────────────
def test_cli_promotion_commands_count_18():
    promotion_cmds = [c for c in PROVIDER_COMMANDS if c.group == "strategy_promotion"]
    assert len(promotion_cmds) == 18

# ── metadata ─────────────────────────────────────────────────────────────────
def test_cli_promotion_version_introduced_in():
    cmd = next(c for c in PROVIDER_COMMANDS if c.name == "strategy-promotion-version")
    assert cmd.introduced_in == "1.9.3"

def test_cli_promotion_build_introduced_in():
    cmd = next(c for c in PROVIDER_COMMANDS if c.name == "strategy-promotion-build")
    assert cmd.introduced_in == "1.9.3"

def test_cli_promotion_gate_group():
    cmd = next(c for c in PROVIDER_COMMANDS if c.name == "strategy-promotion-gate")
    assert cmd.group == "strategy_promotion"

def test_cli_promotion_rollback_group():
    cmd = next(c for c in PROVIDER_COMMANDS if c.name == "strategy-promotion-rollback")
    assert cmd.group == "strategy_promotion"

def test_cli_promotion_safety_classification():
    cmd = next(c for c in PROVIDER_COMMANDS if c.name == "strategy-promotion-safety-audit")
    assert cmd.safety_classification == "RESEARCH_ONLY"

def test_cli_promotion_version_safety():
    cmd = next(c for c in PROVIDER_COMMANDS if c.name == "strategy-promotion-version")
    assert cmd.safety_classification == "RESEARCH_ONLY"

def test_cli_all_promotion_safety_research_only():
    promotion_cmds = [c for c in PROVIDER_COMMANDS if c.group == "strategy_promotion"]
    assert all(c.safety_classification == "RESEARCH_ONLY" for c in promotion_cmds)

def test_cli_all_promotion_introduced_193():
    promotion_cmds = [c for c in PROVIDER_COMMANDS if c.group == "strategy_promotion"]
    assert all(c.introduced_in == "1.9.3" for c in promotion_cmds)

def test_cli_provider_commands_is_list():
    assert isinstance(PROVIDER_COMMANDS, list)

def test_cli_no_duplicate_promotion_names():
    promotion_names = [c.name for c in PROVIDER_COMMANDS if c.group == "strategy_promotion"]
    assert len(promotion_names) == len(set(promotion_names))

def test_cli_promotion_health_handler():
    cmd = next(c for c in PROVIDER_COMMANDS if c.name == "strategy-promotion-health")
    assert cmd.handler_name == "cmd_strategy_promotion_health"

def test_cli_promotion_version_handler():
    cmd = next(c for c in PROVIDER_COMMANDS if c.name == "strategy-promotion-version")
    assert cmd.handler_name == "cmd_strategy_promotion_version"
