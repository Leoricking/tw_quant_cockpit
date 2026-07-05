"""
tests/test_stable_rollup_compatibility_matrix_v169.py
Tests for compatibility_matrix_v169 module.
"""
import pytest
from paper_trading.stable_rollup.compatibility_matrix_v169 import (
    COMPATIBILITY_EDGES, get_edges, get_edge, validate_matrix,
)


def test_edges_is_list():
    assert isinstance(COMPATIBILITY_EDGES, list)


def test_edge_count_11():
    assert len(COMPATIBILITY_EDGES) == 11


def test_get_edges_returns_list():
    edges = get_edges()
    assert isinstance(edges, list)
    assert len(edges) == 11


def test_get_edges_returns_copy():
    e1 = get_edges()
    e2 = get_edges()
    assert e1 is not e2


def test_edge_160_to_161():
    e = get_edge("1.6.0", "1.6.1")
    assert e is not None
    assert e["overall_status"] == "COMPATIBLE"


def test_edge_168_to_169():
    e = get_edge("1.6.8", "1.6.9")
    assert e is not None
    assert e["overall_status"] == "COMPATIBLE"


def test_edge_nonexistent():
    e = get_edge("1.6.0", "1.6.9")
    assert e is None


def test_all_edges_compatible():
    for edge in get_edges():
        assert edge["overall_status"] == "COMPATIBLE", \
            f"Edge {edge['from_version']}->{edge['to_version']} is not COMPATIBLE"


def test_all_edges_safety_compatible():
    for edge in get_edges():
        assert edge["safety_compatibility"] == "COMPATIBLE", \
            f"Edge {edge['from_version']}->{edge['to_version']} safety_compat not COMPATIBLE"


def test_validate_matrix_pass():
    result = validate_matrix()
    assert result["status"] == "PASS"
    assert result["issues"] == []


def test_validate_matrix_unique():
    result = validate_matrix()
    assert result["unique"] == 11


def test_no_duplicate_edges():
    edges = get_edges()
    pairs = [(e["from_version"], e["to_version"]) for e in edges]
    assert len(set(pairs)) == len(pairs)


def test_each_edge_has_schema_fields():
    required_fields = [
        "from_version", "to_version", "version_identity", "schema_compatibility",
        "overall_status",
    ]
    for edge in get_edges():
        for field in required_fields:
            assert field in edge, f"Edge missing field {field!r}"


def test_edge_666_to_6661():
    e = get_edge("1.6.6", "1.6.6.1")
    assert e is not None
    assert e["overall_status"] == "COMPATIBLE"


def test_edge_6661_to_6662():
    e = get_edge("1.6.6.1", "1.6.6.2")
    assert e is not None


def test_deterministic_order():
    e1 = [f"{e['from_version']}->{e['to_version']}" for e in get_edges()]
    e2 = [f"{e['from_version']}->{e['to_version']}" for e in get_edges()]
    assert e1 == e2
