"""
tests/test_strategy_registry_gate_v196.py
Tests for strategy_registry_release_gate_v196 — Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
import pytest
from release.strategy_registry_release_gate_v196 import (
    StrategyRegistryReleaseGate,
    run_release_gate,
    run_gate,
)


# ── gate class ────────────────────────────────────────────────────────────────

def test_gate_version():
    assert StrategyRegistryReleaseGate.GATE_VERSION == "1.9.6"

def test_gate_min_scenarios():
    assert StrategyRegistryReleaseGate.MIN_SCENARIOS == 75

def test_gate_min_fixtures():
    assert StrategyRegistryReleaseGate.MIN_FIXTURES == 75

def test_gate_min_cli():
    assert StrategyRegistryReleaseGate.MIN_CLI == 18

def test_gate_baseline_tests():
    assert StrategyRegistryReleaseGate.BASELINE_TESTS == 29358

def test_gate_min_new_tests():
    assert StrategyRegistryReleaseGate.MIN_NEW_TESTS == 400


# ── run_release_gate result shape ─────────────────────────────────────────────

def test_run_gate_returns_dict():
    assert isinstance(run_release_gate(), dict)

def test_run_gate_has_gate_passed():
    assert "gate_passed" in run_release_gate()

def test_run_gate_has_passed():
    assert "passed" in run_release_gate()

def test_run_gate_has_failed():
    assert "failed" in run_release_gate()

def test_run_gate_has_total():
    assert "total" in run_release_gate()

def test_run_gate_has_checks():
    assert "checks" in run_release_gate()


# ── safety flags in result ────────────────────────────────────────────────────

def test_gate_result_paper_only():
    assert run_release_gate()["paper_only"] is True

def test_gate_result_no_real_orders():
    assert run_release_gate()["no_real_orders"] is True

def test_gate_result_governance_only():
    assert run_release_gate()["governance_only"] is True

def test_gate_result_registry_only():
    assert run_release_gate()["registry_only"] is True

def test_gate_result_schema_version():
    assert run_release_gate()["schema_version"] == "196"


# ── pass criteria ─────────────────────────────────────────────────────────────

def test_gate_passed():
    result = run_release_gate()
    failed_checks = [c for c in result["checks"] if not c["passed"]]
    assert result["gate_passed"] is True, f"Gate failed: {[c['name'] for c in failed_checks]}"

def test_gate_failed_zero():
    assert run_release_gate()["failed"] == 0

def test_gate_total_ge_50():
    assert run_release_gate()["total"] >= 50


# ── run_gate alias ────────────────────────────────────────────────────────────

def test_run_gate_alias():
    assert run_gate is run_release_gate
