"""
tests/test_strategy_review_cli_v195.py
Tests for strategy review CLI commands v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only. No Real Orders. Not Investment Advice.
"""
import pytest
from cli.command_registry import PROVIDER_COMMANDS


@pytest.fixture(scope="module")
def review_commands():
    return [c for c in PROVIDER_COMMANDS if c.name.startswith("strategy-review-")]


# ── command count ─────────────────────────────────────────────────────────────

def test_review_commands_count_18(review_commands):
    assert len(review_commands) >= 18


# ── specific commands exist ───────────────────────────────────────────────────

def test_strategy_review_version_command(review_commands):
    assert any(c.name == "strategy-review-version" for c in review_commands)


def test_strategy_review_run_command(review_commands):
    assert any(c.name == "strategy-review-run" for c in review_commands)


def test_strategy_review_alerts_command(review_commands):
    assert any(c.name == "strategy-review-alerts" for c in review_commands)


def test_strategy_review_queue_command(review_commands):
    assert any(c.name == "strategy-review-queue" for c in review_commands)


def test_strategy_review_approval_command(review_commands):
    assert any(c.name == "strategy-review-approval" for c in review_commands)


def test_strategy_review_decision_command(review_commands):
    assert any(c.name == "strategy-review-decision" for c in review_commands)


def test_strategy_review_rollback_ticket_command(review_commands):
    assert any(c.name == "strategy-review-rollback-ticket" for c in review_commands)


def test_strategy_review_escalation_command(review_commands):
    assert any(c.name == "strategy-review-escalation" for c in review_commands)


def test_strategy_review_report_command(review_commands):
    assert any(c.name == "strategy-review-report" for c in review_commands)


def test_strategy_review_dashboard_command(review_commands):
    assert any(c.name == "strategy-review-dashboard" for c in review_commands)


def test_strategy_review_export_command(review_commands):
    assert any(c.name == "strategy-review-export" for c in review_commands)


def test_strategy_review_evidence_command(review_commands):
    assert any(c.name == "strategy-review-evidence" for c in review_commands)


def test_strategy_review_audit_command(review_commands):
    assert any(c.name == "strategy-review-audit" for c in review_commands)


def test_strategy_review_health_command(review_commands):
    assert any(c.name == "strategy-review-health" for c in review_commands)


def test_strategy_review_gate_command(review_commands):
    assert any(c.name == "strategy-review-gate" for c in review_commands)


def test_strategy_review_scenarios_command(review_commands):
    assert any(c.name == "strategy-review-scenarios" for c in review_commands)


def test_strategy_review_fixtures_command(review_commands):
    assert any(c.name == "strategy-review-fixtures" for c in review_commands)


def test_strategy_review_safety_audit_command(review_commands):
    assert any(c.name == "strategy-review-safety-audit" for c in review_commands)


# ── command attributes ────────────────────────────────────────────────────────

def test_review_commands_all_research_only(review_commands):
    assert all(c.research_only is True for c in review_commands)


def test_review_commands_all_safety_classification(review_commands):
    assert all(c.safety_classification == "RESEARCH_ONLY" for c in review_commands)


def test_review_commands_all_group_strategy_review(review_commands):
    assert all(c.group == "strategy_review" for c in review_commands)


def test_review_commands_all_introduced_in_195(review_commands):
    assert all(c.introduced_in == "1.9.5" for c in review_commands)


def test_review_commands_all_have_help(review_commands):
    assert all(c.help for c in review_commands)


def test_review_commands_all_have_handler_name(review_commands):
    assert all(c.handler_name for c in review_commands)
