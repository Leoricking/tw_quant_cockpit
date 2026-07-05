"""
tests/test_stable_rollup_models_v169.py
Tests for models_v169 module.
"""
import pytest
from paper_trading.stable_rollup.models_v169 import (
    ReleaseDescriptor, ReleaseIdentity, ReleaseCapability, ReleaseSafetyBoundary,
    ReleaseHealthSummary, ReleaseGateSummary, ReleaseCLISummary, ReleaseGUISummary,
    ReleaseFixtureSummary, ReleaseScenarioSummary, ReleaseLineageSummary,
    ReleaseContractSummary, ReleaseRegressionSummary, StableRollupManifest,
    StableRollupSnapshot, StableRollupValidationResult, StableRollupReconciliation,
    StableRollupScore, StableRollupReport, StableRollupQuery,
    MigrationReadinessSummary, StableRollupHealthSummary,
)
from paper_trading.stable_rollup.enums_v169 import (
    RollupStatus, SealStatus, MigrationReadiness, ConfidenceLevel, ValidationSeverity,
)


def test_release_descriptor_defaults():
    r = ReleaseDescriptor()
    assert r.paper_only is True
    assert r.no_real_orders is True
    assert r.not_for_production is True
    assert r.schema_version == "169"


def test_release_identity_defaults():
    r = ReleaseIdentity()
    assert r.paper_only is True
    assert r.research_only is True
    assert r.schema_version == "169"


def test_release_capability_defaults():
    r = ReleaseCapability()
    assert r.production_ready is False
    assert r.paper_only is True
    assert isinstance(r.dependencies, list)


def test_release_capability_production_ready_false():
    r = ReleaseCapability(capability_name="test", introduced_in="1.6.0")
    assert r.production_ready is False


def test_release_safety_boundary_defaults():
    r = ReleaseSafetyBoundary()
    assert r.paper_only is True
    assert r.no_real_orders is True


def test_release_health_summary_defaults():
    r = ReleaseHealthSummary()
    assert r.passed == 0
    assert r.failed == 0
    assert r.total == 0


def test_release_gate_summary_defaults():
    r = ReleaseGateSummary()
    assert r.gate_passed is False
    assert r.paper_only is True


def test_release_cli_summary_defaults():
    r = ReleaseCLISummary()
    assert r.unresolved == 0
    assert r.callable_count == 0


def test_release_gui_summary_defaults():
    r = ReleaseGUISummary()
    assert r.headless_safe is True
    assert r.empty_state_ok is True


def test_release_fixture_summary_defaults():
    r = ReleaseFixtureSummary()
    assert r.total == 0
    assert r.valid == 0


def test_release_scenario_summary_defaults():
    r = ReleaseScenarioSummary()
    assert r.passed == 0
    assert r.skipped == 0


def test_release_lineage_summary_defaults():
    r = ReleaseLineageSummary()
    assert r.parent_chain_intact is False
    assert isinstance(r.broken_links, list)


def test_release_contract_summary_defaults():
    r = ReleaseContractSummary()
    assert r.contract_valid is False


def test_release_regression_summary_defaults():
    r = ReleaseRegressionSummary()
    assert r.regression_found is False
    assert r.delta == 0


def test_stable_rollup_manifest_defaults():
    m = StableRollupManifest()
    assert m.rollup_version == "1.6.9"
    assert m.sealed is True
    assert m.paper_only is True


def test_stable_rollup_snapshot_defaults():
    s = StableRollupSnapshot()
    assert s.rollup_status == RollupStatus.READY
    assert s.paper_only is True
    assert s.no_real_orders is True


def test_stable_rollup_validation_result_defaults():
    r = StableRollupValidationResult()
    assert r.passed is False
    assert isinstance(r.issues, list)


def test_stable_rollup_reconciliation_defaults():
    r = StableRollupReconciliation()
    assert r.expected == 0
    assert r.actual == 0
    assert r.status == RollupStatus.READY


def test_stable_rollup_score_defaults():
    s = StableRollupScore()
    assert s.total_score == 0.0
    assert s.not_for_real_trading is True
    assert s.paper_only is True
    assert isinstance(s.component_scores, dict)
    assert isinstance(s.blocking_issues, list)


def test_stable_rollup_report_defaults():
    r = StableRollupReport()
    assert r.paper_only is True
    assert r.no_real_orders is True
    assert r.migration_readiness == MigrationReadiness.NOT_READY


def test_stable_rollup_query_defaults():
    q = StableRollupQuery()
    assert q.result_count == 0
    assert isinstance(q.results, list)
    assert isinstance(q.filters, dict)


def test_migration_readiness_summary_defaults():
    m = MigrationReadinessSummary()
    assert m.readiness == MigrationReadiness.NOT_READY
    assert isinstance(m.blocking_issues, list)
    assert isinstance(m.passed_checks, list)


def test_stable_rollup_health_summary_defaults():
    h = StableRollupHealthSummary()
    assert h.all_pass is False
    assert h.any_blocking is False
    assert isinstance(h.health_summaries, list)


def test_all_models_have_policy_version():
    models = [
        ReleaseDescriptor(), ReleaseIdentity(), StableRollupScore(),
        StableRollupManifest(), StableRollupSnapshot(),
    ]
    for m in models:
        assert hasattr(m, "policy_version"), f"{type(m).__name__} missing policy_version"
        assert m.policy_version == "1.6.9-live-paper-stable-rollup"
