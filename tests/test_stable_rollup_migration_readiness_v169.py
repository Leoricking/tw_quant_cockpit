"""
tests/test_stable_rollup_migration_readiness_v169.py
Tests for migration_readiness_v169 module.
"""
import pytest
from paper_trading.stable_rollup.migration_readiness_v169 import (
    MigrationReadinessAssessor, assess_migration_readiness,
)
from paper_trading.stable_rollup.enums_v169 import MigrationReadiness
from paper_trading.stable_rollup.models_v169 import MigrationReadinessSummary


def test_assessor_instantiable():
    a = MigrationReadinessAssessor()
    assert a is not None


def test_assess_returns_summary():
    a = MigrationReadinessAssessor()
    result = a.assess()
    assert isinstance(result, MigrationReadinessSummary)


def test_assess_not_blocked():
    a = MigrationReadinessAssessor()
    result = a.assess()
    assert result.readiness != MigrationReadiness.BLOCKED


def test_assess_has_passed_checks():
    a = MigrationReadinessAssessor()
    result = a.assess()
    assert isinstance(result.passed_checks, list)
    assert len(result.passed_checks) > 0


def test_assess_has_blocking_issues():
    a = MigrationReadinessAssessor()
    result = a.assess()
    assert isinstance(result.blocking_issues, list)


def test_assess_has_conditional_issues():
    a = MigrationReadinessAssessor()
    result = a.assess()
    assert isinstance(result.conditional_issues, list)


def test_stable_identity_check_passes():
    a = MigrationReadinessAssessor()
    _, ok, _ = a._check("stable_identity", a._check_stable_identity)
    assert ok is True


def test_api_stability_check_passes():
    a = MigrationReadinessAssessor()
    _, ok, _ = a._check("api_stability", a._check_api_stability)
    assert ok is True


def test_safety_boundaries_check_passes():
    a = MigrationReadinessAssessor()
    _, ok, _ = a._check("safety_boundaries", a._check_safety_boundaries)
    assert ok is True


def test_deterministic_replay_check_passes():
    a = MigrationReadinessAssessor()
    _, ok, _ = a._check("deterministic_replay", a._check_deterministic_replay)
    assert ok is True


def test_rollback_traceability_check_passes():
    a = MigrationReadinessAssessor()
    _, ok, _ = a._check("rollback_traceability", a._check_rollback_traceability)
    assert ok is True


def test_get_readiness_returns_enum():
    a = MigrationReadinessAssessor()
    r = a.get_readiness()
    assert isinstance(r, MigrationReadiness)


def test_get_readiness_not_blocked():
    a = MigrationReadinessAssessor()
    r = a.get_readiness()
    assert r != MigrationReadiness.BLOCKED


def test_assess_migration_readiness_returns_dict():
    result = assess_migration_readiness()
    assert isinstance(result, dict)
    assert "readiness" in result


def test_assess_migration_readiness_paper_only():
    result = assess_migration_readiness()
    assert result.get("paper_only") is True


def test_assess_migration_readiness_no_real_orders():
    result = assess_migration_readiness()
    assert result.get("no_real_orders") is True
