"""
tests/test_stable_rollup_integration_v169.py
Integration tests for stable rollup v1.6.9.
"""
import pytest
import paper_trading.stable_rollup as sr_pkg


def test_package_importable():
    assert sr_pkg.VERSION == "1.6.9"


def test_all_core_modules_importable():
    import paper_trading.stable_rollup.version_v169
    import paper_trading.stable_rollup.enums_v169
    import paper_trading.stable_rollup.models_v169
    import paper_trading.stable_rollup.safety_v169
    import paper_trading.stable_rollup.release_manifest_v169
    import paper_trading.stable_rollup.release_registry_v169
    assert True


def test_all_matrix_modules_importable():
    import paper_trading.stable_rollup.capability_matrix_v169
    import paper_trading.stable_rollup.safety_matrix_v169
    import paper_trading.stable_rollup.compatibility_matrix_v169
    import paper_trading.stable_rollup.component_matrix_v169
    assert True


def test_all_aggregator_modules_importable():
    import paper_trading.stable_rollup.health_aggregator_v169
    import paper_trading.stable_rollup.gate_aggregator_v169
    import paper_trading.stable_rollup.cli_aggregator_v169
    import paper_trading.stable_rollup.gui_aggregator_v169
    import paper_trading.stable_rollup.fixture_aggregator_v169
    import paper_trading.stable_rollup.scenario_aggregator_v169
    import paper_trading.stable_rollup.lineage_aggregator_v169
    import paper_trading.stable_rollup.contract_aggregator_v169
    assert True


def test_all_stable_modules_importable():
    import paper_trading.stable_rollup.stable_contract_v169
    import paper_trading.stable_rollup.stable_snapshot_v169
    import paper_trading.stable_rollup.stable_validator_v169
    import paper_trading.stable_rollup.stable_reconciler_v169
    import paper_trading.stable_rollup.stable_scorecard_v169
    import paper_trading.stable_rollup.stable_query_v169
    import paper_trading.stable_rollup.stable_report_v169
    assert True


def test_all_support_modules_importable():
    import paper_trading.stable_rollup.migration_readiness_v169
    import paper_trading.stable_rollup.regression_matrix_v169
    import paper_trading.stable_rollup.scenario_registry_v169
    import paper_trading.stable_rollup.fixture_schema_v169
    import paper_trading.stable_rollup.fixture_registry_v169
    import paper_trading.stable_rollup.health_v169
    assert True


def test_safety_contract_passes():
    from paper_trading.stable_rollup.stable_contract_v169 import StableContract
    result = StableContract().validate_safety()
    assert result["passed"] is True


def test_release_manifest_has_169():
    from paper_trading.stable_rollup.release_manifest_v169 import get_release
    entry = get_release("1.6.9")
    assert entry is not None


def test_lineage_is_intact():
    from paper_trading.stable_rollup.lineage_aggregator_v169 import run
    result = run()
    assert result["intact"] is True


def test_full_health_run():
    from paper_trading.stable_rollup.health_v169 import StableRollupHealthCheck
    result = StableRollupHealthCheck().run()
    assert result["status"] == "PASS"


def test_full_gate_run():
    from release.live_paper_trading_stable_rollup_release_gate_v169 import StableRollupReleaseGate
    result = StableRollupReleaseGate().run()
    assert result["gate_passed"] is True


def test_scorecard_not_zero():
    from paper_trading.stable_rollup.stable_scorecard_v169 import compute_scorecard
    score = compute_scorecard()
    assert score.total_score > 0


def test_migration_not_blocked():
    from paper_trading.stable_rollup.migration_readiness_v169 import MigrationReadinessAssessor
    from paper_trading.stable_rollup.enums_v169 import MigrationReadiness
    assessor = MigrationReadinessAssessor()
    r = assessor.get_readiness()
    assert r != MigrationReadiness.BLOCKED


def test_reconcile_all_ready():
    from paper_trading.stable_rollup.stable_reconciler_v169 import StableReconciler
    from paper_trading.stable_rollup.enums_v169 import RollupStatus
    reconciler = StableReconciler()
    results = reconciler.reconcile_all()
    for r in results:
        assert r.status == RollupStatus.READY, f"Domain {r.domain!r} not READY"


def test_cli_has_26_stable_rollup_commands():
    from paper_trading.stable_rollup.cli_aggregator_v169 import run
    result = run()
    assert result["stable_rollup_commands"] >= 26
