"""
tests/test_strategy_governance_dashboard_gate_v197.py
Tests for Paper Strategy Governance Dashboard Release Gate v1.9.7.
[!] Research Only. Paper Only. Governance Analytics Only. Dashboard Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest
from release.strategy_governance_dashboard_release_gate_v197 import (
    StrategyGovernanceDashboardReleaseGate,
    run_release_gate,
    run_gate,
    GATE_VERSION,
    MIN_CHECKS,
    BASELINE_TESTS,
    MIN_NEW_TESTS,
    MIN_SCENARIOS,
    MIN_FIXTURES,
    MIN_CLI,
)


# ── Constants ──────────────────────────────────────────────────────────────────

def test_gate_version_value():
    assert GATE_VERSION == "1.9.7"

def test_gate_min_checks_value():
    assert MIN_CHECKS >= 50

def test_gate_baseline_tests():
    assert BASELINE_TESTS == 29683

def test_gate_min_new_tests():
    assert MIN_NEW_TESTS >= 400

def test_gate_min_scenarios():
    assert MIN_SCENARIOS >= 75

def test_gate_min_fixtures():
    assert MIN_FIXTURES >= 75

def test_gate_min_cli():
    assert MIN_CLI >= 16


# ── Class attributes ───────────────────────────────────────────────────────────

def test_class_gate_version():
    assert StrategyGovernanceDashboardReleaseGate.GATE_VERSION == "1.9.7"

def test_class_min_scenarios():
    assert StrategyGovernanceDashboardReleaseGate.MIN_SCENARIOS >= 75

def test_class_min_fixtures():
    assert StrategyGovernanceDashboardReleaseGate.MIN_FIXTURES >= 75

def test_class_min_cli():
    assert StrategyGovernanceDashboardReleaseGate.MIN_CLI >= 16

def test_class_baseline_tests():
    assert StrategyGovernanceDashboardReleaseGate.BASELINE_TESTS == 29683

def test_class_min_new_tests():
    assert StrategyGovernanceDashboardReleaseGate.MIN_NEW_TESTS >= 400


# ── run() return shape ─────────────────────────────────────────────────────────

def test_run_returns_dict():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert isinstance(result, dict)

def test_run_has_gate_passed():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert "gate_passed" in result

def test_run_has_passed_count():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert "passed_count" in result

def test_run_has_failed_count():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert "failed_count" in result

def test_run_has_total():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert "total" in result

def test_run_has_gate_version():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert result["gate_version"] == "1.9.7"

def test_run_has_checks_list():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert isinstance(result["checks"], list)

def test_run_paper_only_true():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert result["paper_only"] is True

def test_run_no_real_orders_true():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert result["no_real_orders"] is True

def test_run_governance_analytics_only():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert result["governance_analytics_only"] is True

def test_run_dashboard_only():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert result["dashboard_only"] is True

def test_run_not_investment_advice():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert result["not_investment_advice"] is True

def test_run_schema_version_197():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert result["schema_version"] == "197"


# ── Gate PASS ─────────────────────────────────────────────────────────────────

def test_gate_passed_true():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert result["gate_passed"] is True

def test_gate_failed_count_zero():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert result["failed_count"] == 0

def test_gate_total_ge_min_checks():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert result["total"] >= MIN_CHECKS

def test_gate_passed_count_equals_total():
    result = StrategyGovernanceDashboardReleaseGate().run()
    assert result["passed_count"] == result["total"]


# ── All checks pass ────────────────────────────────────────────────────────────

def test_all_checks_pass_individually():
    result = StrategyGovernanceDashboardReleaseGate().run()
    failed = [c for c in result["checks"] if not c["passed"]]
    assert failed == [], f"Failed checks: {[c['name'] for c in failed]}"

def test_checks_have_name_field():
    result = StrategyGovernanceDashboardReleaseGate().run()
    for check in result["checks"]:
        assert "name" in check, f"Check missing 'name': {check}"

def test_checks_have_passed_field():
    result = StrategyGovernanceDashboardReleaseGate().run()
    for check in result["checks"]:
        assert "passed" in check, f"Check missing 'passed': {check}"

def test_checks_have_error_field():
    result = StrategyGovernanceDashboardReleaseGate().run()
    for check in result["checks"]:
        assert "error" in check, f"Check missing 'error': {check}"

def test_passed_checks_have_none_error():
    result = StrategyGovernanceDashboardReleaseGate().run()
    for check in result["checks"]:
        if check["passed"]:
            assert check["error"] is None, f"Passed check has non-None error: {check}"


# ── Specific check names present ───────────────────────────────────────────────

def test_health_all_passed_check_present():
    result = StrategyGovernanceDashboardReleaseGate().run()
    names = [c["name"] for c in result["checks"]]
    assert "health_all_passed" in names

def test_gate_version_check_present():
    result = StrategyGovernanceDashboardReleaseGate().run()
    names = [c["name"] for c in result["checks"]]
    assert "gate_version_1_9_7" in names

def test_safety_audit_check_present():
    result = StrategyGovernanceDashboardReleaseGate().run()
    names = [c["name"] for c in result["checks"]]
    assert "safety_audit_all_safe" in names

def test_model_count_check_present():
    result = StrategyGovernanceDashboardReleaseGate().run()
    names = [c["name"] for c in result["checks"]]
    assert "model_count_25" in names

def test_scenarios_count_check_present():
    result = StrategyGovernanceDashboardReleaseGate().run()
    names = [c["name"] for c in result["checks"]]
    assert "scenarios_count_75" in names

def test_fixtures_count_check_present():
    result = StrategyGovernanceDashboardReleaseGate().run()
    names = [c["name"] for c in result["checks"]]
    assert "fixtures_count_75" in names

def test_gui_panel_check_present():
    result = StrategyGovernanceDashboardReleaseGate().run()
    names = [c["name"] for c in result["checks"]]
    assert "gui_panel_version_197" in names

def test_baseline_tests_check_present():
    result = StrategyGovernanceDashboardReleaseGate().run()
    names = [c["name"] for c in result["checks"]]
    assert "baseline_tests_29683" in names

def test_backward_compat_v196_check_present():
    result = StrategyGovernanceDashboardReleaseGate().run()
    names = [c["name"] for c in result["checks"]]
    assert "backward_compat_v196" in names

def test_backward_compat_v190_check_present():
    result = StrategyGovernanceDashboardReleaseGate().run()
    names = [c["name"] for c in result["checks"]]
    assert "backward_compat_v190" in names


# ── run_release_gate() alias ───────────────────────────────────────────────────

def test_run_release_gate_function_returns_dict():
    result = run_release_gate()
    assert isinstance(result, dict)

def test_run_release_gate_gate_passed():
    result = run_release_gate()
    assert result["gate_passed"] is True

def test_run_release_gate_failed_count_zero():
    result = run_release_gate()
    assert result["failed_count"] == 0

def test_run_release_gate_paper_only():
    result = run_release_gate()
    assert result["paper_only"] is True


# ── run_gate() alias ───────────────────────────────────────────────────────────

def test_run_gate_alias_is_function():
    assert callable(run_gate)

def test_run_gate_returns_dict():
    result = run_gate()
    assert isinstance(result, dict)

def test_run_gate_gate_passed():
    result = run_gate()
    assert result["gate_passed"] is True

def test_run_gate_schema_version_197():
    result = run_gate()
    assert result["schema_version"] == "197"


# ── Idempotency ────────────────────────────────────────────────────────────────

def test_run_idempotent():
    gate = StrategyGovernanceDashboardReleaseGate()
    r1 = gate.run()
    r2 = gate.run()
    assert r1["gate_passed"] == r2["gate_passed"]
    assert r1["failed_count"] == r2["failed_count"]
    assert r1["total"] == r2["total"]
