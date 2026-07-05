"""
tests/test_stable_rollup_component_matrix_v169.py
Tests for component_matrix_v169 module.
"""
import pytest
from paper_trading.stable_rollup.component_matrix_v169 import (
    COMPONENT_MATRIX, get_matrix, get_component, validate_matrix,
)


def test_matrix_is_list():
    assert isinstance(COMPONENT_MATRIX, list)


def test_component_count_32():
    assert len(COMPONENT_MATRIX) == 32


def test_get_matrix_returns_list():
    m = get_matrix()
    assert isinstance(m, list)
    assert len(m) == 32


def test_get_component_init():
    comp = get_component("__init__")
    assert comp is not None
    assert comp["module"] == "paper_trading.stable_rollup"


def test_get_component_health_v169():
    comp = get_component("health_v169")
    assert comp is not None
    assert comp["version"] == "1.6.9"


def test_get_component_nonexistent():
    comp = get_component("nonexistent_xyz")
    assert comp is None


def test_all_components_version_169():
    for comp in get_matrix():
        assert comp["version"] == "1.6.9", f"{comp['component_name']} version != 1.6.9"


def test_all_components_active():
    for comp in get_matrix():
        assert comp["status"] == "ACTIVE", f"{comp['component_name']} status={comp['status']}"


def test_all_components_have_module():
    for comp in get_matrix():
        assert comp.get("module"), f"{comp['component_name']} missing module"


def test_unique_component_names():
    names = [c["component_name"] for c in get_matrix()]
    assert len(set(names)) == len(names)


def test_validate_matrix_pass():
    result = validate_matrix()
    assert result["status"] == "PASS"
    assert result["issues"] == []


def test_validate_matrix_total():
    result = validate_matrix()
    assert result["total"] == 32


def test_health_v169_has_coverage():
    comp = get_component("health_v169")
    assert comp["health_coverage"] is True
    assert comp["gate_coverage"] is True


def test_version_v169_in_matrix():
    comp = get_component("version_v169")
    assert comp is not None


def test_enums_v169_in_matrix():
    comp = get_component("enums_v169")
    assert comp is not None


def test_models_v169_in_matrix():
    comp = get_component("models_v169")
    assert comp is not None


def test_safety_v169_in_matrix():
    comp = get_component("safety_v169")
    assert comp is not None
