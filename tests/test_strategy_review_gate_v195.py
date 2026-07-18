"""
tests/test_strategy_review_gate_v195.py
Tests for strategy review release gate v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only. No Real Orders. Not Investment Advice.
"""
import pytest
from release.strategy_review_release_gate_v195 import (
    StrategyReviewReleaseGate, run_release_gate,
)


@pytest.fixture(scope="module")
def gate_result():
    return run_release_gate()


# ── gate structure ────────────────────────────────────────────────────────────

def test_gate_returns_dict(gate_result):
    assert isinstance(gate_result, dict)


def test_gate_has_gate_passed(gate_result):
    assert "gate_passed" in gate_result


def test_gate_has_passed_count(gate_result):
    assert "passed_count" in gate_result


def test_gate_has_failed_count(gate_result):
    assert "failed_count" in gate_result


def test_gate_has_total(gate_result):
    assert "total" in gate_result


def test_gate_has_results(gate_result):
    assert "results" in gate_result


# ── gate safety flags ─────────────────────────────────────────────────────────

def test_gate_paper_only(gate_result):
    assert gate_result["paper_only"] is True


def test_gate_no_real_orders(gate_result):
    assert gate_result["no_real_orders"] is True


def test_gate_research_only(gate_result):
    assert gate_result["research_only"] is True


def test_gate_review_only(gate_result):
    assert gate_result["review_only"] is True


def test_gate_human_approval_only(gate_result):
    assert gate_result["human_approval_only"] is True


def test_gate_no_auto_approval(gate_result):
    assert gate_result["no_auto_approval"] is True


def test_gate_no_auto_rollback(gate_result):
    assert gate_result["no_auto_rollback"] is True


def test_gate_schema_version(gate_result):
    assert gate_result["schema_version"] == "195"


def test_gate_version(gate_result):
    assert gate_result["version"] == "1.9.5"


# ── gate pass/fail ────────────────────────────────────────────────────────────

def test_gate_passed(gate_result):
    assert gate_result["gate_passed"] is True


def test_gate_failed_count_zero(gate_result):
    assert gate_result["failed_count"] == 0


# ── individual gate checks ────────────────────────────────────────────────────

def test_gate_results_all_passed(gate_result):
    failed = [r for r in gate_result["results"] if not r["passed"]]
    assert failed == [], f"Failed gates: {[r['name'] for r in failed]}"


def test_gate_version_194_check(gate_result):
    names = [r["name"] for r in gate_result["results"]]
    assert "version_195" in names


def test_gate_safety_audit_check(gate_result):
    names = [r["name"] for r in gate_result["results"]]
    assert "safety_audit_all_safe" in names


def test_gate_model_auto_approval_false(gate_result):
    names = [r["name"] for r in gate_result["results"]]
    assert any("auto_approval" in n for n in names)


def test_gate_rollback_auto_rollback_false(gate_result):
    names = [r["name"] for r in gate_result["results"]]
    assert any("auto_rollback" in n for n in names)


def test_gate_fixtures_75(gate_result):
    names = [r["name"] for r in gate_result["results"]]
    assert any("fixtures_count" in n for n in names)


def test_gate_scenarios_75(gate_result):
    names = [r["name"] for r in gate_result["results"]]
    assert any("scenarios_count" in n for n in names)


def test_gate_gui_panel_version_check(gate_result):
    names = [r["name"] for r in gate_result["results"]]
    assert any("gui_panel_version" in n for n in names)


def test_gate_cli_commands_check(gate_result):
    names = [r["name"] for r in gate_result["results"]]
    assert any("cli_review_commands" in n for n in names)


def test_gate_health_all_passed_check(gate_result):
    names = [r["name"] for r in gate_result["results"]]
    assert "health_all_passed" in names


# ── class attributes ──────────────────────────────────────────────────────────

def test_gate_class_version():
    assert StrategyReviewReleaseGate.VERSION == "1.9.5"


def test_gate_class_baseline_tests():
    assert StrategyReviewReleaseGate.BASELINE_TESTS == 28947


def test_gate_class_min_new_tests():
    assert StrategyReviewReleaseGate.MIN_NEW_TESTS == 400


def test_gate_class_min_scenarios():
    assert StrategyReviewReleaseGate.MIN_SCENARIOS == 75


def test_gate_class_min_fixtures():
    assert StrategyReviewReleaseGate.MIN_FIXTURES == 75


def test_gate_class_min_cli():
    assert StrategyReviewReleaseGate.MIN_CLI == 18
