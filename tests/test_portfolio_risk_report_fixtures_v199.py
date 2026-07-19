"""
tests/test_portfolio_risk_report_fixtures_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Fixtures Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.portfolio_risk_report_fixtures_v199 import (
    get_fixtures,
    get_fixture_by_id,
)


def test_get_fixtures_returns_list():
    assert isinstance(get_fixtures(), list)


def test_get_fixtures_length_is_75():
    assert len(get_fixtures()) == 75


def test_all_fixtures_have_id():
    for f in get_fixtures():
        assert "id" in f and f["id"]


def test_all_fixtures_have_fixture_id():
    for f in get_fixtures():
        assert "fixture_id" in f and f["fixture_id"]


def test_all_fixtures_schema_version_is_199():
    for f in get_fixtures():
        assert f["schema_version"] == "199"


def test_all_fixtures_paper_only_True():
    for f in get_fixtures():
        assert f["paper_only"] is True


def test_all_fixtures_no_real_orders_True():
    for f in get_fixtures():
        assert f["no_real_orders"] is True


def test_all_fixtures_no_broker_True():
    for f in get_fixtures():
        assert f["no_broker"] is True


def test_all_fixtures_no_margin_True():
    for f in get_fixtures():
        assert f["no_margin"] is True


def test_all_fixtures_no_leverage_True():
    for f in get_fixtures():
        assert f["no_leverage"] is True


def test_all_fixtures_not_investment_advice_True():
    for f in get_fixtures():
        assert f["not_investment_advice"] is True


def test_all_fixtures_demo_only_True():
    for f in get_fixtures():
        assert f["demo_only"] is True


def test_all_fixtures_not_for_production_True():
    for f in get_fixtures():
        assert f["not_for_production"] is True


def test_all_fixtures_production_trading_blocked_True():
    for f in get_fixtures():
        assert f["production_trading_blocked"] is True


def test_all_fixture_ids_are_unique():
    ids = [f["id"] for f in get_fixtures()]
    assert len(ids) == len(set(ids))


def test_get_fixture_by_id_PRRF199_001_returns_correct():
    result = get_fixture_by_id("PRRF199-001")
    assert isinstance(result, dict)
    assert result["id"] == "PRRF199-001"


def test_get_fixture_by_id_nonexistent_returns_empty():
    result = get_fixture_by_id("NONEXISTENT")
    assert result == {}


def test_all_fixtures_have_capital_base():
    for f in get_fixtures():
        assert "capital_base" in f


def test_all_fixtures_have_entry_type():
    for f in get_fixtures():
        assert "entry_type" in f


def test_all_fixtures_have_expected_recommendation():
    for f in get_fixtures():
        assert "expected_recommendation" in f


def test_all_fixtures_have_expected_blocked():
    for f in get_fixtures():
        assert "expected_blocked" in f
        assert isinstance(f["expected_blocked"], bool)


def test_get_fixture_by_id_returns_dict():
    result = get_fixture_by_id("PRRF199-001")
    assert isinstance(result, dict)


def test_fixtures_capital_base_is_numeric():
    for f in get_fixtures():
        assert isinstance(f["capital_base"], (int, float))


def test_fixtures_entry_type_is_string():
    for f in get_fixtures():
        assert isinstance(f["entry_type"], str)


def test_fixtures_expected_recommendation_is_string():
    for f in get_fixtures():
        assert isinstance(f["expected_recommendation"], str)


def test_fixtures_cover_multiple_entry_types():
    entry_types = {f["entry_type"] for f in get_fixtures()}
    assert len(entry_types) >= 3


def test_some_fixtures_expected_blocked_True():
    blocked = [f for f in get_fixtures() if f["expected_blocked"] is True]
    assert len(blocked) > 0


def test_some_fixtures_expected_blocked_False():
    not_blocked = [f for f in get_fixtures() if f["expected_blocked"] is False]
    assert len(not_blocked) > 0
