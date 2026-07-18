"""tests/test_strategy_sandbox_gate_v192.py
Tests for strategy sandbox release gate v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
"""
import pytest
from release.strategy_sandbox_release_gate_v192 import (
    StrategySandboxReleaseGate, run_release_gate,
)


# ── run_release_gate return structure ─────────────────────────────────────────

def test_run_release_gate_returns_dict():
    result = run_release_gate()
    assert isinstance(result, dict)

def test_run_release_gate_gate_passed_key_exists():
    result = run_release_gate()
    assert "gate_passed" in result

def test_run_release_gate_status_key_exists():
    result = run_release_gate()
    assert "status" in result

def test_run_release_gate_failed_key_exists():
    result = run_release_gate()
    assert "failed" in result

def test_run_release_gate_passed_ge_80():
    result = run_release_gate()
    assert result["passed"] >= 80

def test_run_release_gate_total_ge_80():
    result = run_release_gate()
    assert result["total"] >= 80

def test_run_release_gate_version_192():
    result = run_release_gate()
    assert result["version"] == "1.9.2"

def test_run_release_gate_release_name():
    result = run_release_gate()
    assert result["release_name"] == "Paper Strategy Rule Sandbox & Shadow Validation Lab"

def test_run_release_gate_paper_only():
    result = run_release_gate()
    assert result["paper_only"] is True

def test_run_release_gate_no_real_orders():
    result = run_release_gate()
    assert result["no_real_orders"] is True

def test_run_release_gate_sandbox_only():
    result = run_release_gate()
    assert result["sandbox_only"] is True

def test_run_release_gate_shadow_only():
    result = run_release_gate()
    assert result["shadow_only"] is True

def test_run_release_gate_not_investment_advice():
    result = run_release_gate()
    assert result["not_investment_advice"] is True

def test_run_release_gate_production_trading_blocked():
    result = run_release_gate()
    assert result["production_trading_blocked"] is True

def test_run_release_gate_schema_version_192():
    result = run_release_gate()
    assert result["schema_version"] == "192"

def test_run_release_gate_results_is_list():
    result = run_release_gate()
    assert isinstance(result["results"], list)

def test_run_release_gate_all_results_have_name():
    result = run_release_gate()
    assert all("name" in r for r in result["results"])

def test_run_release_gate_all_results_have_passed():
    result = run_release_gate()
    assert all("passed" in r for r in result["results"])

def test_run_release_gate_most_results_passed():
    result = run_release_gate()
    passed_count = sum(1 for r in result["results"] if r["passed"] is True)
    assert passed_count >= 80

def test_run_release_gate_no_broker():
    result = run_release_gate()
    assert result["no_broker"] is True

def test_run_release_gate_no_production_mutation():
    result = run_release_gate()
    assert result["no_production_strategy_mutation"] is True


# ── StrategySandboxReleaseGate class attributes ───────────────────────────────

def test_release_gate_class_version():
    assert StrategySandboxReleaseGate.VERSION == "1.9.2"

def test_release_gate_class_release_name():
    assert StrategySandboxReleaseGate.RELEASE_NAME == "Paper Strategy Rule Sandbox & Shadow Validation Lab"

def test_release_gate_class_min_scenarios():
    assert StrategySandboxReleaseGate.MIN_SCENARIOS == 75

def test_release_gate_class_min_fixtures():
    assert StrategySandboxReleaseGate.MIN_FIXTURES == 75

def test_release_gate_class_min_cli():
    assert StrategySandboxReleaseGate.MIN_CLI == 20

def test_release_gate_class_min_health_checks():
    assert StrategySandboxReleaseGate.MIN_HEALTH_CHECKS == 60


# ── Release gate min counts in result ────────────────────────────────────────

def test_run_release_gate_min_scenarios():
    result = run_release_gate()
    assert result["min_scenarios"] == 75

def test_run_release_gate_min_fixtures():
    result = run_release_gate()
    assert result["min_fixtures"] == 75

def test_run_release_gate_min_cli():
    result = run_release_gate()
    assert result["min_cli"] == 20

def test_run_release_gate_min_new_tests():
    result = run_release_gate()
    assert result["min_new_tests"] == 400

def test_run_release_gate_research_only():
    result = run_release_gate()
    assert result["research_only"] is True
