"""
tests/test_decision_report_health_v187.py
Tests for decision_report_health_v187 — v1.8.7 Decision Report Export & Evidence Pack.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_report_health_v187 import (
    DecisionReportHealthCheck, run_health_check,
)
from paper_trading.small_capital_strategy.decision_report_models_v187 import ReportHealthSummary


def test_run_health_check_returns_health_summary():
    result = run_health_check()
    assert isinstance(result, ReportHealthSummary)


def test_run_health_check_status_pass():
    result = run_health_check()
    assert result.status == "PASS"


def test_run_health_check_all_passed():
    result = run_health_check()
    assert result.all_passed is True


def test_run_health_check_failed_zero():
    result = run_health_check()
    assert result.failed == 0


def test_run_health_check_total_ge_60():
    result = run_health_check()
    assert result.total >= 60


def test_run_health_check_passed_equals_total():
    result = run_health_check()
    assert result.passed == result.total


def test_run_health_check_paper_only():
    result = run_health_check()
    assert result.paper_only is True


def test_run_health_check_no_real_orders():
    result = run_health_check()
    assert result.no_real_orders is True


def test_run_health_check_schema_version():
    result = run_health_check()
    assert result.schema_version == "187"


def test_decision_report_health_check_class_instantiates():
    checker = DecisionReportHealthCheck()
    assert checker is not None


def test_decision_report_health_check_run_returns_summary():
    checker = DecisionReportHealthCheck()
    result = checker.run()
    assert isinstance(result, ReportHealthSummary)


def test_health_check_version_check_passes():
    checker = DecisionReportHealthCheck()
    result = checker.run()
    # version_is_187 check should be in the checks
    version_checks = [c for c in checker._checks if "version" in c["name"].lower()]
    assert len(version_checks) >= 1
    for vc in version_checks:
        assert vc["passed"] is True


def test_health_check_safety_checks_pass():
    checker = DecisionReportHealthCheck()
    result = checker.run()
    safety_checks = [c for c in checker._checks if "safety" in c["name"].lower()]
    assert len(safety_checks) >= 1
    for sc in safety_checks:
        assert sc["passed"] is True, f"Safety check failed: {sc['name']}: {sc['error']}"


def test_health_check_model_checks_pass():
    checker = DecisionReportHealthCheck()
    result = checker.run()
    model_checks = [c for c in checker._checks if "model_" in c["name"].lower()]
    assert len(model_checks) >= 22
    for mc in model_checks:
        assert mc["passed"] is True, f"Model check failed: {mc['name']}: {mc['error']}"


def test_health_check_engine_checks_pass():
    checker = DecisionReportHealthCheck()
    result = checker.run()
    engine_checks = [c for c in checker._checks if "engine_" in c["name"].lower()]
    assert len(engine_checks) >= 6
    for ec in engine_checks:
        assert ec["passed"] is True, f"Engine check failed: {ec['name']}: {ec['error']}"


def test_health_check_export_checks_pass():
    checker = DecisionReportHealthCheck()
    result = checker.run()
    export_checks = [c for c in checker._checks if "export_" in c["name"].lower()]
    assert len(export_checks) >= 5
    for ec in export_checks:
        assert ec["passed"] is True, f"Export check failed: {ec['name']}: {ec['error']}"


def test_health_check_scenario_checks_pass():
    checker = DecisionReportHealthCheck()
    result = checker.run()
    scenario_checks = [c for c in checker._checks if "scenario" in c["name"].lower()]
    assert len(scenario_checks) >= 3
    for sc in scenario_checks:
        assert sc["passed"] is True, f"Scenario check failed: {sc['name']}: {sc['error']}"


def test_health_check_fixture_checks_pass():
    checker = DecisionReportHealthCheck()
    result = checker.run()
    fixture_checks = [c for c in checker._checks if "fixture" in c["name"].lower()]
    assert len(fixture_checks) >= 3
    for fc in fixture_checks:
        assert fc["passed"] is True, f"Fixture check failed: {fc['name']}: {fc['error']}"


def test_health_check_all_checks_have_name():
    checker = DecisionReportHealthCheck()
    checker.run()
    for c in checker._checks:
        assert "name" in c and len(c["name"]) > 0


def test_health_check_all_checks_have_passed_field():
    checker = DecisionReportHealthCheck()
    checker.run()
    for c in checker._checks:
        assert "passed" in c
        assert isinstance(c["passed"], bool)


def test_health_check_all_checks_have_error_field():
    checker = DecisionReportHealthCheck()
    checker.run()
    for c in checker._checks:
        assert "error" in c
        # error should be None if passed
        if c["passed"]:
            assert c["error"] is None


def test_health_check_consecutive_runs_consistent():
    result1 = run_health_check()
    result2 = run_health_check()
    assert result1.status == result2.status
    assert result1.total == result2.total
    assert result1.passed == result2.passed


def test_health_check_version_is_187_present():
    checker = DecisionReportHealthCheck()
    checker.run()
    names = [c["name"] for c in checker._checks]
    assert "version_is_187" in names


def test_health_check_safety_audit_present():
    checker = DecisionReportHealthCheck()
    checker.run()
    names = [c["name"] for c in checker._checks]
    assert "safety_audit_all_safe" in names


def test_health_check_scenarios_count_75_present():
    checker = DecisionReportHealthCheck()
    checker.run()
    names = [c["name"] for c in checker._checks]
    assert "scenarios_count_75" in names


def test_health_check_fixtures_count_75_present():
    checker = DecisionReportHealthCheck()
    checker.run()
    names = [c["name"] for c in checker._checks]
    assert "fixtures_count_75" in names


def test_health_check_no_duplicate_check_names():
    checker = DecisionReportHealthCheck()
    checker.run()
    names = [c["name"] for c in checker._checks]
    assert len(names) == len(set(names)), "Duplicate check names found"
