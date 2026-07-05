"""
tests/test_stable_rollup_reconciler_v169.py
Tests for stable_reconciler_v169 module.
"""
import pytest
from paper_trading.stable_rollup.stable_reconciler_v169 import (
    StableReconciler, run_reconciliation,
    EXPECTED_RELEASES, EXPECTED_CAPABILITIES, EXPECTED_SAFETY_ITEMS,
    EXPECTED_TEST_BASELINE, EXPECTED_CLI_COMMANDS,
)
from paper_trading.stable_rollup.enums_v169 import RollupStatus, ConfidenceLevel


def test_expected_releases():
    assert EXPECTED_RELEASES == 13


def test_expected_capabilities_ge_19():
    assert EXPECTED_CAPABILITIES >= 19


def test_expected_safety_items():
    assert EXPECTED_SAFETY_ITEMS == 20


def test_expected_test_baseline():
    assert EXPECTED_TEST_BASELINE == 11465


def test_expected_cli_commands():
    assert EXPECTED_CLI_COMMANDS == 26


def test_reconciler_instantiable():
    r = StableReconciler()
    assert r is not None


def test_reconcile_releases_returns_obj():
    r = StableReconciler()
    result = r.reconcile_releases()
    assert hasattr(result, "domain")
    assert result.domain == "releases"


def test_reconcile_releases_ready():
    r = StableReconciler()
    result = r.reconcile_releases()
    assert result.status == RollupStatus.READY


def test_reconcile_releases_actual_ge_expected():
    r = StableReconciler()
    result = r.reconcile_releases()
    assert result.actual >= result.expected


def test_reconcile_capabilities_ready():
    r = StableReconciler()
    result = r.reconcile_capabilities()
    assert result.status == RollupStatus.READY


def test_reconcile_safety_ready():
    r = StableReconciler()
    result = r.reconcile_safety()
    assert result.status == RollupStatus.READY


def test_reconcile_tests_ready():
    r = StableReconciler()
    result = r.reconcile_tests()
    assert result.status == RollupStatus.READY


def test_reconcile_tests_baseline():
    r = StableReconciler()
    result = r.reconcile_tests()
    assert result.expected == 11465


def test_reconcile_all_returns_list():
    r = StableReconciler()
    results = r.reconcile_all()
    assert isinstance(results, list)
    assert len(results) == 5


def test_reconcile_all_all_ready():
    r = StableReconciler()
    results = r.reconcile_all()
    for result in results:
        assert result.status == RollupStatus.READY, f"{result.domain}: {result.actual} vs {result.expected}"


def test_run_reconciliation_returns_dict():
    result = run_reconciliation()
    assert isinstance(result, dict)


def test_run_reconciliation_all_pass():
    result = run_reconciliation()
    assert result["all_pass"] is True
    assert result["status"] == "PASS"


def test_run_reconciliation_paper_only():
    result = run_reconciliation()
    assert result.get("paper_only") is True
