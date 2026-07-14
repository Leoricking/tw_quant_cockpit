"""
tests/test_decision_report_gate_v187.py
Tests for decision_report_release_gate_v187 — v1.8.7 Decision Report Export & Evidence Pack.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
import pytest
from release.decision_report_release_gate_v187 import (
    DecisionReportReleaseGate, run_gate, GATE_VERSION, MIN_CHECKS,
)


def test_run_gate_returns_dict():
    result = run_gate()
    assert isinstance(result, dict)


def test_run_gate_gate_passed():
    result = run_gate()
    assert result["gate_passed"] is True


def test_run_gate_status_pass():
    result = run_gate()
    assert result["status"] == "PASS"


def test_run_gate_failed_zero():
    result = run_gate()
    assert result["failed"] == 0


def test_run_gate_total_ge_60():
    result = run_gate()
    assert result["total"] >= 60


def test_run_gate_passed_equals_total():
    result = run_gate()
    assert result["passed"] == result["total"]


def test_run_gate_gate_version():
    result = run_gate()
    assert result["gate_version"] == "1.8.7"


def test_run_gate_paper_only():
    result = run_gate()
    assert result["paper_only"] is True


def test_run_gate_report_only():
    result = run_gate()
    assert result["report_only"] is True


def test_run_gate_audit_only():
    result = run_gate()
    assert result["audit_only"] is True


def test_run_gate_no_real_orders():
    result = run_gate()
    assert result["no_real_orders"] is True


def test_run_gate_schema_version():
    result = run_gate()
    assert result["schema_version"] == "187"


def test_run_gate_has_checks_list():
    result = run_gate()
    assert "checks" in result
    assert isinstance(result["checks"], list)


def test_run_gate_checks_count_ge_60():
    result = run_gate()
    assert len(result["checks"]) >= 60


def test_gate_version_constant():
    assert GATE_VERSION == "1.8.7"


def test_min_checks_constant():
    assert MIN_CHECKS == 60


def test_decision_report_release_gate_class_instantiates():
    gate = DecisionReportReleaseGate()
    assert gate is not None


def test_decision_report_release_gate_run_returns_dict():
    gate = DecisionReportReleaseGate()
    result = gate.run()
    assert isinstance(result, dict)


def test_gate_checks_all_passed():
    result = run_gate()
    for check in result["checks"]:
        assert check["passed"] is True, f"Gate check failed: {check['name']}: {check.get('error')}"


def test_gate_health_all_passed_check_present():
    result = run_gate()
    names = [c["name"] for c in result["checks"]]
    assert "health_all_passed" in names


def test_gate_health_status_pass_check_present():
    result = run_gate()
    names = [c["name"] for c in result["checks"]]
    assert "health_status_pass" in names


def test_gate_version_187_check_present():
    result = run_gate()
    names = [c["name"] for c in result["checks"]]
    assert "gate_version_187" in names


def test_gate_safety_all_safe_check_present():
    result = run_gate()
    names = [c["name"] for c in result["checks"]]
    assert "safety_all_safe" in names


def test_gate_scenarios_count_eq_75_check_present():
    result = run_gate()
    names = [c["name"] for c in result["checks"]]
    assert "scenarios_count_eq_75" in names


def test_gate_cli_decision_report_group_check_present():
    result = run_gate()
    names = [c["name"] for c in result["checks"]]
    assert "cli_decision_report_group_exists" in names


def test_gate_gui_panel_version_check_present():
    result = run_gate()
    names = [c["name"] for c in result["checks"]]
    assert "gui_panel_version_187" in names


def test_gate_no_forbidden_buy_check_present():
    result = run_gate()
    names = [c["name"] for c in result["checks"]]
    assert "no_forbidden_buy_in_engine" in names


def test_gate_checks_have_name_field():
    result = run_gate()
    for c in result["checks"]:
        assert "name" in c
        assert len(c["name"]) > 0


def test_gate_checks_have_passed_field():
    result = run_gate()
    for c in result["checks"]:
        assert "passed" in c
        assert isinstance(c["passed"], bool)


def test_gate_checks_no_duplicates():
    result = run_gate()
    names = [c["name"] for c in result["checks"]]
    assert len(names) == len(set(names)), "Duplicate check names in gate"


def test_gate_consecutive_runs_consistent():
    r1 = run_gate()
    r2 = run_gate()
    assert r1["gate_passed"] == r2["gate_passed"]
    assert r1["total"] == r2["total"]
