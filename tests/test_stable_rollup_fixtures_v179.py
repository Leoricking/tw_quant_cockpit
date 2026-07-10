"""
tests/test_stable_rollup_fixtures_v179.py
Tests for stable_rollup_fixture_registry_v179 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.stable_rollup_fixture_registry_v179 import (
    get_all_fixtures,
    count_fixtures,
    get_fixture_by_id,
    validate_registry,
)


def test_count_fixtures_is_50():
    assert count_fixtures() == 50


def test_get_all_fixtures_returns_list():
    fixtures = get_all_fixtures()
    assert isinstance(fixtures, list)


def test_get_all_fixtures_count_50():
    fixtures = get_all_fixtures()
    assert len(fixtures) == 50


def test_get_all_fixtures_returns_copy():
    f1 = get_all_fixtures()
    f2 = get_all_fixtures()
    assert f1 is not f2


def test_all_fixtures_have_fixture_id():
    for fx in get_all_fixtures():
        assert "fixture_id" in fx
        assert fx["fixture_id"].startswith("FX179-")


def test_all_fixtures_have_name():
    for fx in get_all_fixtures():
        assert "name" in fx
        assert len(fx["name"]) > 0


def test_all_fixtures_have_expected_action():
    for fx in get_all_fixtures():
        assert "expected_action" in fx


def test_all_fixtures_paper_only():
    for fx in get_all_fixtures():
        assert fx.get("paper_only") is True


def test_all_fixtures_research_only():
    for fx in get_all_fixtures():
        assert fx.get("research_only") is True


def test_all_fixtures_no_real_orders():
    for fx in get_all_fixtures():
        assert fx.get("no_real_orders") is True


def test_all_fixtures_no_broker():
    for fx in get_all_fixtures():
        assert fx.get("no_broker") is True


def test_all_fixtures_not_investment_advice():
    for fx in get_all_fixtures():
        assert fx.get("not_investment_advice") is True


def test_all_fixtures_demo_only():
    for fx in get_all_fixtures():
        assert fx.get("demo_only") is True


def test_all_fixtures_not_for_production():
    for fx in get_all_fixtures():
        assert fx.get("not_for_production") is True


def test_fixture_ids_are_unique():
    ids = [fx["fixture_id"] for fx in get_all_fixtures()]
    assert len(ids) == len(set(ids))


def test_get_fixture_by_id_fx179_001():
    fx = get_fixture_by_id("FX179-001")
    assert fx is not None
    assert fx["expected_action"] == "PAPER_ENTRY_ALLOWED"


def test_get_fixture_by_id_fx179_050():
    fx = get_fixture_by_id("FX179-050")
    assert fx is not None
    assert fx["expected_action"] == "NO_TRADE"


def test_get_fixture_by_id_nonexistent_returns_none():
    fx = get_fixture_by_id("FX179-999")
    assert fx is None


def test_get_fixture_by_id_fx179_011_safety():
    fx = get_fixture_by_id("FX179-011")
    assert fx is not None
    assert fx["expected_action"] == "PAPER_PLAN_READY"
    assert fx.get("safety_all_safe") is True


def test_get_fixture_by_id_fx179_046_blocked():
    fx = get_fixture_by_id("FX179-046")
    assert fx is not None
    assert fx["expected_action"] == "BLOCKED"
    assert fx.get("real_order") is True


def test_all_fixtures_have_schema_version():
    for fx in get_all_fixtures():
        assert fx.get("schema_version") == "179"


def test_all_fixtures_have_policy_version():
    for fx in get_all_fixtures():
        assert "1.7.9" in fx.get("policy_version", "")


def test_validate_registry_returns_true():
    assert validate_registry() is True


def test_paper_entry_allowed_fixtures_count():
    paper_entry = [fx for fx in get_all_fixtures() if fx["expected_action"] == "PAPER_ENTRY_ALLOWED"]
    assert len(paper_entry) == 10


def test_blocked_fixtures_count():
    blocked = [fx for fx in get_all_fixtures() if fx["expected_action"] == "BLOCKED"]
    assert len(blocked) == 4
