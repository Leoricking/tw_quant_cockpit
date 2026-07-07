"""tests/test_small_capital_fixtures_v170.py — fixture schema/registry tests for v1.7.0."""
import json
import os
import pytest
from paper_trading.small_capital_strategy.fixture_schema_v170 import (
    REQUIRED_MARKERS, REQUIRED_FIELDS, validate_fixture,
    get_required_markers, get_required_fields,
)
from paper_trading.small_capital_strategy.fixture_registry_v170 import (
    FIXTURE_REGISTRY, count_fixtures, get_fixtures_by_category,
    get_all_categories, list_fixtures,
)

FIXTURE_DIR = os.path.join(
    os.path.dirname(__file__), "fixtures", "small_capital_strategy"
)


def test_required_markers_count_10():
    assert len(REQUIRED_MARKERS) == 10


def test_required_markers_all_true():
    assert all(v is True for v in REQUIRED_MARKERS.values())


def test_required_markers_has_small_capital_only():
    assert "small_capital_strategy_only" in REQUIRED_MARKERS


def test_required_markers_has_paper_only():
    assert "paper_only" in REQUIRED_MARKERS


def test_required_markers_has_no_live_data():
    assert "no_live_data" in REQUIRED_MARKERS


def test_required_fields_at_least_18():
    assert len(REQUIRED_FIELDS) >= 18


def test_required_fields_has_fixture_id():
    assert "fixture_id" in REQUIRED_FIELDS


def test_required_fields_has_schema_version():
    assert "schema_version" in REQUIRED_FIELDS


def test_validate_fixture_valid():
    fixture = {f: None for f in REQUIRED_FIELDS}
    fixture.update(REQUIRED_MARKERS)
    fixture["schema_version"] = "170"
    fixture["fixture_id"] = "sc_001"
    fixture["scenario_id"] = "test"
    fixture["template_id"] = "small_capital_300k_v170"
    fixture["category"] = "test"
    fixture["description"] = "test"
    fixture["created_at"] = "2026-07-06T00:00:00Z"
    fixture["input"] = {}
    fixture["expected"] = {}
    result = validate_fixture(fixture)
    assert result["valid"] is True


def test_validate_fixture_missing_marker_fails():
    fixture = {f: None for f in REQUIRED_FIELDS}
    fixture.update(REQUIRED_MARKERS)
    fixture["schema_version"] = "170"
    fixture.pop("small_capital_strategy_only")
    result = validate_fixture(fixture)
    assert result["valid"] is False


def test_get_required_markers_returns_copy():
    markers = get_required_markers()
    assert isinstance(markers, dict)
    assert markers == REQUIRED_MARKERS


def test_get_required_fields_returns_copy():
    fields = get_required_fields()
    assert isinstance(fields, list)
    assert set(fields) == set(REQUIRED_FIELDS)


def test_fixture_registry_count_80():
    assert count_fixtures() == 80


def test_fixture_registry_has_sc_001():
    assert "sc_001" in FIXTURE_REGISTRY


def test_fixture_registry_has_sc_080():
    assert "sc_080" in FIXTURE_REGISTRY


def test_fixture_registry_all_have_category():
    for fid, meta in FIXTURE_REGISTRY.items():
        assert "category" in meta, f"Missing category: {fid}"


def test_fixture_registry_all_have_description():
    for fid, meta in FIXTURE_REGISTRY.items():
        assert "description" in meta, f"Missing description: {fid}"


def test_get_fixtures_by_category_capital_profile():
    fixtures = get_fixtures_by_category("capital_profile")
    assert len(fixtures) == 10


def test_get_all_categories_returns_list():
    cats = get_all_categories()
    assert isinstance(cats, list)
    assert len(cats) >= 8


def test_list_fixtures_returns_list():
    fixtures = list_fixtures()
    assert isinstance(fixtures, list)
    assert len(fixtures) == 80


def test_fixture_files_exist_80():
    if not os.path.isdir(FIXTURE_DIR):
        pytest.skip("Fixture directory not found")
    files = [f for f in os.listdir(FIXTURE_DIR) if f.endswith(".json")]
    assert len(files) == 80


@pytest.mark.parametrize("fixture_id", [f"sc_{i:03d}" for i in range(1, 81)])
def test_fixture_file_valid(fixture_id):
    path = os.path.join(FIXTURE_DIR, f"{fixture_id}.json")
    if not os.path.isfile(path):
        pytest.skip(f"Fixture file not found: {path}")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    result = validate_fixture(data)
    assert result["valid"] is True, f"{fixture_id}: {result['issues']}"
