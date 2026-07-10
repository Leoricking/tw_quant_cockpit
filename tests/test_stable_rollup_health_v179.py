"""
tests/test_stable_rollup_health_v179.py
Tests for stable_rollup_health_v179 module (30+ tests).
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.stable_rollup_health_v179 import (
    run_health_check,
    MIN_HEALTH_CHECKS,
)
from paper_trading.small_capital_strategy.stable_rollup_models_v179 import StableRollupHealthSummary


def test_min_health_checks_ge_50():
    assert MIN_HEALTH_CHECKS >= 50


def test_run_health_check_returns_health_summary():
    result = run_health_check()
    assert isinstance(result, StableRollupHealthSummary)


def test_run_health_check_status_pass():
    result = run_health_check()
    assert result.status == "PASS"


def test_run_health_check_all_passed():
    result = run_health_check()
    assert result.all_passed is True


def test_run_health_check_failed_zero():
    result = run_health_check()
    assert result.failed == 0


def test_run_health_check_total_ge_50():
    result = run_health_check()
    assert result.total >= 50


def test_run_health_check_passed_ge_50():
    result = run_health_check()
    assert result.passed >= 50


def test_run_health_check_paper_only():
    result = run_health_check()
    assert result.paper_only is True


def test_run_health_check_research_only():
    result = run_health_check()
    assert result.research_only is True


def test_run_health_check_no_real_orders():
    result = run_health_check()
    assert result.no_real_orders is True


def test_run_health_check_no_broker():
    result = run_health_check()
    assert result.no_broker is True


def test_run_health_check_not_investment_advice():
    result = run_health_check()
    assert result.not_investment_advice is True


def test_run_health_check_demo_only():
    result = run_health_check()
    assert result.demo_only is True


def test_run_health_check_not_for_production():
    result = run_health_check()
    assert result.not_for_production is True


def test_run_health_check_schema_version():
    result = run_health_check()
    assert result.schema_version == "179"


def test_run_health_check_policy_version():
    result = run_health_check()
    assert "1.7.9" in result.policy_version


def test_run_health_check_checks_is_list():
    result = run_health_check()
    assert isinstance(result.checks, list)


def test_run_health_check_checks_not_empty():
    result = run_health_check()
    assert len(result.checks) > 0


def test_run_health_check_checks_have_name():
    result = run_health_check()
    for check in result.checks:
        assert "name" in check


def test_run_health_check_checks_have_passed():
    result = run_health_check()
    for check in result.checks:
        assert "passed" in check


def test_run_health_check_all_checks_passed():
    result = run_health_check()
    failed = [c for c in result.checks if not c["passed"]]
    assert len(failed) == 0, f"Failed checks: {[c['name'] for c in failed]}"


def test_run_health_check_version_check_passes():
    result = run_health_check()
    version_checks = [c for c in result.checks if c["name"] == "version_179"]
    assert len(version_checks) == 1
    assert version_checks[0]["passed"] is True


def test_run_health_check_safety_audit_check_passes():
    result = run_health_check()
    safety_checks = [c for c in result.checks if c["name"] == "safety_audit_all_safe"]
    assert len(safety_checks) == 1
    assert safety_checks[0]["passed"] is True


def test_run_health_check_manifest_check_passes():
    result = run_health_check()
    manifest_checks = [c for c in result.checks if c["name"] == "manifest_valid"]
    assert len(manifest_checks) == 1
    assert manifest_checks[0]["passed"] is True


def test_run_health_check_cli_check_passes():
    result = run_health_check()
    cli_checks = [c for c in result.checks if c["name"] == "cli_all_registered"]
    assert len(cli_checks) == 1
    assert cli_checks[0]["passed"] is True


def test_run_health_check_gui_check_passes():
    result = run_health_check()
    gui_checks = [c for c in result.checks if c["name"] == "gui_stable_tabs_present"]
    assert len(gui_checks) == 1
    assert gui_checks[0]["passed"] is True


def test_run_health_check_compat_all_pass():
    result = run_health_check()
    compat_checks = [c for c in result.checks if c["name"] == "compat_all_9_pass"]
    assert len(compat_checks) == 1
    assert compat_checks[0]["passed"] is True


def test_run_health_check_fixture_check_passes():
    result = run_health_check()
    fixture_checks = [c for c in result.checks if c["name"] == "fixture_audit_all_safe"]
    assert len(fixture_checks) == 1
    assert fixture_checks[0]["passed"] is True


def test_run_health_check_scenario_check_passes():
    result = run_health_check()
    scenario_checks = [c for c in result.checks if c["name"] == "scenario_audit_all_clean"]
    assert len(scenario_checks) == 1
    assert scenario_checks[0]["passed"] is True


def test_run_health_check_passed_equals_total():
    result = run_health_check()
    assert result.passed == result.total
