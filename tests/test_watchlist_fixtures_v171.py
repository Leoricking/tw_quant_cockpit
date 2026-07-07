"""tests/test_watchlist_fixtures_v171.py — fixture registry tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_fixture_registry_v171 import (
    WATCHLIST_FIXTURE_REGISTRY,
    get_fixture_count,
    get_fixture_ids,
    validate_all_fixtures,
)
from paper_trading.small_capital_strategy.watchlist_fixture_schema_v171 import (
    validate_watchlist_fixture,
    get_required_markers,
    get_required_fields,
    SCHEMA_VERSION, REQUIRED_MARKERS, REQUIRED_FIELDS,
)


def test_fixture_count_ge_70():
    assert get_fixture_count() >= 70


def test_fixture_registry_is_list():
    assert isinstance(WATCHLIST_FIXTURE_REGISTRY, list)


def test_fixture_count_matches_registry():
    assert get_fixture_count() == len(WATCHLIST_FIXTURE_REGISTRY)


def test_fixture_ids_is_list():
    assert isinstance(get_fixture_ids(), list)


def test_fixture_ids_count():
    assert len(get_fixture_ids()) == get_fixture_count()


def test_fixture_ids_start_with_wl():
    for fid in get_fixture_ids():
        assert fid.startswith("wl_"), f"Bad fixture_id: {fid}"


def test_fixture_ids_unique():
    ids = get_fixture_ids()
    assert len(ids) == len(set(ids)), "Duplicate fixture IDs found"


def test_validate_all_fixtures_valid():
    result = validate_all_fixtures()
    assert result["valid"] is True, f"Fixture validation failed: {result['issues']}"


def test_validate_all_fixtures_dict():
    result = validate_all_fixtures()
    assert isinstance(result, dict)
    assert "valid" in result
    assert "total" in result


def test_validate_all_fixtures_total_matches():
    result = validate_all_fixtures()
    assert result["total"] == get_fixture_count()


def test_all_fixtures_paper_only():
    for f in WATCHLIST_FIXTURE_REGISTRY:
        assert f.get("paper_only") is True, f"paper_only not True in {f.get('fixture_id')}"


def test_all_fixtures_not_investment_advice():
    for f in WATCHLIST_FIXTURE_REGISTRY:
        assert f.get("not_investment_advice") is True, (
            f"not_investment_advice not True in {f.get('fixture_id')}"
        )


def test_all_fixtures_no_real_orders():
    for f in WATCHLIST_FIXTURE_REGISTRY:
        assert f.get("no_real_orders") is True, (
            f"no_real_orders not True in {f.get('fixture_id')}"
        )


def test_all_fixtures_watchlist_strategy_only():
    for f in WATCHLIST_FIXTURE_REGISTRY:
        assert f.get("watchlist_strategy_only") is True, (
            f"watchlist_strategy_only not True in {f.get('fixture_id')}"
        )


def test_all_fixtures_schema_version_171():
    for f in WATCHLIST_FIXTURE_REGISTRY:
        assert f.get("schema_version") == "171", (
            f"Wrong schema_version in {f.get('fixture_id')}"
        )


def test_schema_version_constant():
    assert SCHEMA_VERSION == "171"


def test_required_markers_dict():
    assert isinstance(REQUIRED_MARKERS, dict)
    assert len(REQUIRED_MARKERS) == 11


def test_required_fields_list():
    assert isinstance(REQUIRED_FIELDS, list)


def test_get_required_markers_returns_copy():
    m1 = get_required_markers()
    m1["extra"] = True
    m2 = get_required_markers()
    assert "extra" not in m2


def test_get_required_fields_returns_copy():
    f1 = get_required_fields()
    f1.append("EXTRA")
    f2 = get_required_fields()
    assert "EXTRA" not in f2


def test_validate_fixture_valid():
    f = WATCHLIST_FIXTURE_REGISTRY[0]
    result = validate_watchlist_fixture(f)
    assert result["valid"] is True


def test_validate_fixture_missing_field():
    result = validate_watchlist_fixture({"fixture_id": "test", "paper_only": True})
    assert result["valid"] is False
    assert len(result["issues"]) > 0


def test_validate_fixture_wrong_marker():
    from copy import deepcopy
    f = deepcopy(WATCHLIST_FIXTURE_REGISTRY[0])
    f["paper_only"] = False
    result = validate_watchlist_fixture(f)
    assert result["valid"] is False
