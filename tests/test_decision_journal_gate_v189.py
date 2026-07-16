"""
tests/test_decision_journal_gate_v189.py
Tests for decision_journal_release_gate_v189 — Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. No Real Orders. Not Investment Advice.
"""
import pytest
from release.decision_journal_release_gate_v189 import (
    DecisionJournalReleaseGate, run_release_gate,
)


def test_run_release_gate_returns_dict():
    result = run_release_gate()
    assert isinstance(result, dict)


def test_release_gate_passed():
    result = run_release_gate()
    assert result["gate_passed"] is True


def test_release_gate_status_pass():
    result = run_release_gate()
    assert result["status"] == "PASS"


def test_release_gate_zero_failures():
    result = run_release_gate()
    assert result["failed"] == 0


def test_release_gate_total_at_least_50():
    result = run_release_gate()
    assert result["total"] >= 50


def test_release_gate_passed_equals_total():
    result = run_release_gate()
    assert result["passed"] == result["total"]


def test_release_gate_version():
    result = run_release_gate()
    assert result["version"] == "1.8.9"


def test_release_gate_release_name():
    result = run_release_gate()
    assert result["release_name"] == "Paper Decision Journal & Review Loop"


def test_release_gate_paper_only():
    result = run_release_gate()
    assert result["paper_only"] is True


def test_release_gate_no_real_orders():
    result = run_release_gate()
    assert result["no_real_orders"] is True


def test_release_gate_no_broker():
    result = run_release_gate()
    assert result["no_broker"] is True


def test_release_gate_journal_only():
    result = run_release_gate()
    assert result["journal_only"] is True


def test_release_gate_review_only():
    result = run_release_gate()
    assert result["review_only"] is True


def test_release_gate_audit_only():
    result = run_release_gate()
    assert result["audit_only"] is True


def test_release_gate_not_investment_advice():
    result = run_release_gate()
    assert result["not_investment_advice"] is True


def test_release_gate_production_trading_blocked():
    result = run_release_gate()
    assert result["production_trading_blocked"] is True


def test_release_gate_min_scenarios():
    result = run_release_gate()
    assert result["min_scenarios"] == 75


def test_release_gate_min_fixtures():
    result = run_release_gate()
    assert result["min_fixtures"] == 75


def test_release_gate_min_cli():
    result = run_release_gate()
    assert result["min_cli"] == 18


def test_release_gate_baseline_tests():
    result = run_release_gate()
    assert result["baseline_tests"] == 25641


def test_release_gate_min_new_tests():
    result = run_release_gate()
    assert result["min_new_tests"] == 400


def test_release_gate_results_list():
    result = run_release_gate()
    assert isinstance(result["results"], list)


def test_release_gate_all_results_passed():
    result = run_release_gate()
    for r in result["results"]:
        assert r["passed"] is True, f"Gate check failed: {r['name']} — {r.get('error', '')}"


def test_release_gate_instance_run():
    gate = DecisionJournalReleaseGate()
    result = gate.run()
    assert isinstance(result, dict)


def test_release_gate_instance_passed():
    gate = DecisionJournalReleaseGate()
    result = gate.run()
    assert result["gate_passed"] is True


def test_release_gate_version_constant():
    gate = DecisionJournalReleaseGate()
    assert gate.VERSION == "1.8.9"


def test_release_gate_release_name_constant():
    gate = DecisionJournalReleaseGate()
    assert gate.RELEASE_NAME == "Paper Decision Journal & Review Loop"


def test_release_gate_min_scenarios_constant():
    gate = DecisionJournalReleaseGate()
    assert gate.MIN_SCENARIOS == 75


def test_release_gate_min_fixtures_constant():
    gate = DecisionJournalReleaseGate()
    assert gate.MIN_FIXTURES == 75


def test_release_gate_multiple_runs_consistent():
    r1 = run_release_gate()
    r2 = run_release_gate()
    assert r1["passed"] == r2["passed"]
    assert r1["status"] == r2["status"]
