"""
tests/test_stable_rollup_query_v169.py
Tests for stable_query_v169 module.
"""
import pytest
from paper_trading.stable_rollup.stable_query_v169 import StableQuery
from paper_trading.stable_rollup.models_v169 import StableRollupQuery


def test_query_instantiable():
    q = StableQuery()
    assert q is not None


def test_query_releases_returns_query():
    q = StableQuery()
    result = q.query_releases()
    assert isinstance(result, StableRollupQuery)


def test_query_releases_result_count():
    q = StableQuery()
    result = q.query_releases()
    assert result.result_count == 13


def test_query_releases_filtered():
    q = StableQuery()
    result = q.query_releases(filters={"version": "1.6.9"})
    assert result.result_count == 1
    assert result.results[0]["version"] == "1.6.9"


def test_query_capabilities_returns_query():
    q = StableQuery()
    result = q.query_capabilities()
    assert isinstance(result, StableRollupQuery)


def test_query_capabilities_count_ge_19():
    q = StableQuery()
    result = q.query_capabilities()
    assert result.result_count >= 19


def test_query_capabilities_filtered():
    q = StableQuery()
    result = q.query_capabilities(filters={"capability": "paper_trading"})
    assert result.result_count == 1


def test_query_capabilities_no_production_ready():
    q = StableQuery()
    result = q.query_capabilities(filters={"production_ready": False})
    # All should match since all are production_ready=False
    assert result.result_count >= 19


def test_query_safety_returns_query():
    q = StableQuery()
    result = q.query_safety()
    assert isinstance(result, StableRollupQuery)


def test_query_safety_count_ge_20():
    q = StableQuery()
    result = q.query_safety()
    assert result.result_count >= 20


def test_query_safety_filtered():
    q = StableQuery()
    result = q.query_safety(filters={"status": "SAFE"})
    assert result.result_count >= 20


def test_query_health_returns_query():
    q = StableQuery()
    result = q.query_health()
    assert isinstance(result, StableRollupQuery)


def test_query_results_paper_only():
    q = StableQuery()
    result = q.query_releases()
    assert result.paper_only is True


def test_query_results_no_real_orders():
    q = StableQuery()
    result = q.query_releases()
    assert result.no_real_orders is True


def test_query_id_unique():
    q = StableQuery()
    r1 = q.query_releases()
    r2 = q.query_releases()
    assert r1.query_id != r2.query_id
