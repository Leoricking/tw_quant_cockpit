"""tests/test_abc_fixtures_v172.py — Fixture registry tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_fixture_registry_v172 import (
    ABC_FIXTURE_REGISTRY, get_fixture_count, get_fixture_by_id, validate_registry,
)
from paper_trading.small_capital_strategy.abc_fixture_schema_v172 import (
    REQUIRED_MARKERS, validate_fixture,
)


def test_fixture_count_at_least_70():
    assert get_fixture_count() >= 70


def test_fixture_registry_nonempty():
    assert len(ABC_FIXTURE_REGISTRY) > 0


def test_all_fixtures_have_fixture_id():
    for f in ABC_FIXTURE_REGISTRY:
        assert "fixture_id" in f
        assert f["fixture_id"]


def test_all_fixture_ids_unique():
    ids = [f["fixture_id"] for f in ABC_FIXTURE_REGISTRY]
    assert len(ids) == len(set(ids))


def test_all_fixtures_have_abc_execution_only():
    for f in ABC_FIXTURE_REGISTRY:
        assert f.get("abc_execution_only") is True


def test_all_fixtures_have_paper_only():
    for f in ABC_FIXTURE_REGISTRY:
        assert f.get("paper_only") is True


def test_all_fixtures_have_no_real_orders():
    for f in ABC_FIXTURE_REGISTRY:
        assert f.get("no_real_orders") is True


def test_all_fixtures_have_required_markers():
    for f in ABC_FIXTURE_REGISTRY:
        for marker in REQUIRED_MARKERS:
            assert marker in f, f"Fixture {f.get('fixture_id')} missing marker {marker}"


def test_get_fixture_by_id_abc_001():
    f = get_fixture_by_id("abc_001")
    assert f is not None
    assert f["fixture_id"] == "abc_001"


def test_get_fixture_by_id_missing_returns_empty():
    f = get_fixture_by_id("abc_NONEXISTENT")
    assert not f  # returns {} for missing


def test_validate_registry_passes():
    result = validate_registry()
    assert result["valid"] is True


def test_validate_registry_errors_empty():
    result = validate_registry()
    assert result["errors"] == []


def test_all_fixtures_pass_validate():
    for f in ABC_FIXTURE_REGISTRY:
        result = validate_fixture(f)
        assert result["valid"] is True, f"Fixture {f.get('fixture_id')} failed validation: {result}"


def test_fixture_has_scenario_id():
    for f in ABC_FIXTURE_REGISTRY:
        assert "scenario_id" in f
