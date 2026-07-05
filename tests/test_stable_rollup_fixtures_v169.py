"""
tests/test_stable_rollup_fixtures_v169.py
Tests for fixture schema validation.
"""
import os
import json
import pytest
from paper_trading.stable_rollup.fixture_schema_v169 import (
    REQUIRED_MARKERS, REQUIRED_FIELDS, validate_fixture, load_and_validate_fixture,
)
from paper_trading.stable_rollup.fixture_registry_v169 import (
    FIXTURE_REGISTRY, get_registry, get_fixture, validate_registry, count_fixtures,
)


FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "stable_rollup")


def test_required_markers_count():
    assert len(REQUIRED_MARKERS) == 10


def test_required_markers_all_true():
    for marker, val in REQUIRED_MARKERS.items():
        assert val is True, f"Marker {marker!r} should be True"


def test_required_fields_count():
    assert len(REQUIRED_FIELDS) >= 10


def test_validate_fixture_valid():
    fixture = {m: True for m in REQUIRED_MARKERS}
    fixture.update({
        "fixture_id": "sr_001",
        "scenario_id": "test_scenario",
        "purpose": "test",
        "usage_type": "test",
        "deterministic_seed": 42,
        "schema_version": "169",
        "policy_version": "1.6.9-live-paper-stable-rollup",
        "source_lineage": "v1.6.9",
        "expected_status": "PASS",
    })
    result = validate_fixture(fixture)
    assert result["valid"] is True
    assert result["issues"] == []


def test_validate_fixture_missing_marker():
    fixture = {}
    result = validate_fixture(fixture)
    assert result["valid"] is False
    assert len(result["issues"]) > 0


def test_validate_fixture_wrong_marker():
    fixture = {m: True for m in REQUIRED_MARKERS}
    fixture["test_fixture"] = False
    result = validate_fixture(fixture)
    assert result["valid"] is False


def test_validate_fixture_wrong_schema_version():
    fixture = {m: True for m in REQUIRED_MARKERS}
    fixture.update({
        "fixture_id": "sr_001", "scenario_id": "x", "purpose": "x",
        "usage_type": "test", "deterministic_seed": 42,
        "schema_version": "168",  # wrong
        "policy_version": "1.6.9-live-paper-stable-rollup",
        "source_lineage": "v1.6.9", "expected_status": "PASS",
    })
    result = validate_fixture(fixture)
    assert result["valid"] is False


def test_load_and_validate_sr_001():
    path = os.path.join(FIXTURE_DIR, "sr_001.json")
    result = load_and_validate_fixture(path)
    assert result["valid"] is True


def test_load_and_validate_missing_file():
    result = load_and_validate_fixture("/nonexistent/file.json")
    assert result["valid"] is False


def test_fixture_registry_count_80():
    assert count_fixtures() == 80


def test_fixture_registry_is_dict():
    assert isinstance(FIXTURE_REGISTRY, dict)


def test_get_fixture_sr_001():
    entry = get_fixture("sr_001")
    assert entry is not None
    assert entry["fixture_id"] == "sr_001"


def test_get_fixture_nonexistent():
    entry = get_fixture("nonexistent_xyz")
    assert entry is None


def test_validate_registry_pass():
    result = validate_registry()
    assert result["status"] == "PASS"


def test_validate_registry_total_80():
    result = validate_registry()
    assert result["total"] == 80


def test_all_fixture_files_valid():
    passed = 0
    for i in range(1, 81):
        path = os.path.join(FIXTURE_DIR, f"sr_{str(i).zfill(3)}.json")
        result = load_and_validate_fixture(path)
        if result["valid"]:
            passed += 1
    assert passed == 80
