"""
tests/test_portfolio_risk_report_scenarios_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Scenarios Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.portfolio_risk_report_scenarios_v199 import (
    get_scenarios,
    get_scenario_by_id,
)

_EXPECTED_ENTRY_TYPES = [
    "A_PULLBACK_10MA", "B_BREAKOUT_BASE", "C_RECLAIM_20MA",
    "TEST_POSITION", "ADD_POSITION", "REDUCE_POSITION", "NO_ENTRY",
]

_EXPECTED_RECOMMENDATIONS = [
    "ALLOW_NORMAL_SIZE", "ALLOW_REDUCED_SIZE", "TEST_POSITION_ONLY",
    "NO_ENTRY", "BLOCK",
]


def test_get_scenarios_returns_list():
    assert isinstance(get_scenarios(), list)


def test_get_scenarios_length_is_75():
    assert len(get_scenarios()) == 75


def test_all_scenarios_have_id():
    for s in get_scenarios():
        assert "id" in s and s["id"]


def test_all_scenarios_have_scenario_id():
    for s in get_scenarios():
        assert "scenario_id" in s and s["scenario_id"]


def test_all_scenarios_schema_version_is_199():
    for s in get_scenarios():
        assert s["schema_version"] == "199"


def test_all_scenarios_paper_only_True():
    for s in get_scenarios():
        assert s["paper_only"] is True


def test_all_scenarios_no_real_orders_True():
    for s in get_scenarios():
        assert s["no_real_orders"] is True


def test_all_scenarios_no_broker_True():
    for s in get_scenarios():
        assert s["no_broker"] is True


def test_all_scenarios_no_margin_True():
    for s in get_scenarios():
        assert s["no_margin"] is True


def test_all_scenarios_no_leverage_True():
    for s in get_scenarios():
        assert s["no_leverage"] is True


def test_all_scenarios_no_production_strategy_mutation_True():
    for s in get_scenarios():
        assert s["no_production_strategy_mutation"] is True


def test_all_scenarios_no_automatic_rollback_True():
    for s in get_scenarios():
        assert s["no_automatic_rollback"] is True


def test_all_scenarios_no_live_strategy_activation_True():
    for s in get_scenarios():
        assert s["no_live_strategy_activation"] is True


def test_all_scenarios_no_real_portfolio_rebalancing_True():
    for s in get_scenarios():
        assert s["no_real_portfolio_rebalancing"] is True


def test_all_scenarios_not_investment_advice_True():
    for s in get_scenarios():
        assert s["not_investment_advice"] is True


def test_all_scenarios_demo_only_True():
    for s in get_scenarios():
        assert s["demo_only"] is True


def test_all_scenarios_not_for_production_True():
    for s in get_scenarios():
        assert s["not_for_production"] is True


def test_all_scenarios_production_trading_blocked_True():
    for s in get_scenarios():
        assert s["production_trading_blocked"] is True


def test_all_scenarios_have_entry_type():
    for s in get_scenarios():
        assert "entry_type" in s


def test_all_scenarios_have_expected_recommendation():
    for s in get_scenarios():
        assert "expected_recommendation" in s


def test_all_scenario_ids_are_unique():
    ids = [s["id"] for s in get_scenarios()]
    assert len(ids) == len(set(ids))


def test_get_scenario_by_id_PRR199_001_returns_correct():
    result = get_scenario_by_id("PRR199-001")
    assert isinstance(result, dict)
    assert result["id"] == "PRR199-001"


def test_get_scenario_by_id_nonexistent_returns_empty():
    result = get_scenario_by_id("NONEXISTENT")
    assert result == {}


def test_scenarios_include_A_entry_type():
    entry_types = {s["entry_type"] for s in get_scenarios()}
    assert "A_PULLBACK_10MA" in entry_types


def test_scenarios_include_B_entry_type():
    entry_types = {s["entry_type"] for s in get_scenarios()}
    assert "B_BREAKOUT_BASE" in entry_types


def test_scenarios_include_C_entry_type():
    entry_types = {s["entry_type"] for s in get_scenarios()}
    assert "C_RECLAIM_20MA" in entry_types


def test_scenarios_include_NO_ENTRY_entry_type():
    entry_types = {s["entry_type"] for s in get_scenarios()}
    assert "NO_ENTRY" in entry_types


def test_scenarios_cover_multiple_recommendations():
    recs = {s["expected_recommendation"] for s in get_scenarios()}
    assert len(recs) >= 3


def test_all_scenarios_entry_type_is_string():
    for s in get_scenarios():
        assert isinstance(s["entry_type"], str)


def test_all_scenarios_expected_recommendation_is_string():
    for s in get_scenarios():
        assert isinstance(s["expected_recommendation"], str)


def test_get_scenario_by_id_returns_dict():
    result = get_scenario_by_id("PRR199-001")
    assert isinstance(result, dict)


def test_scenarios_have_TEST_POSITION_entry_type():
    entry_types = {s["entry_type"] for s in get_scenarios()}
    assert "TEST_POSITION" in entry_types
