"""
tests/test_stable_rollup_scenarios_v179.py
Tests for stable_rollup_scenarios_v179 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.stable_rollup_scenarios_v179 import (
    get_scenarios,
    count_scenarios,
    get_scenario_by_id,
    get_scenarios_by_action,
)


def test_count_scenarios_is_50():
    assert count_scenarios() == 50


def test_get_scenarios_returns_list():
    scenarios = get_scenarios()
    assert isinstance(scenarios, list)


def test_get_scenarios_count_50():
    scenarios = get_scenarios()
    assert len(scenarios) == 50


def test_get_scenarios_returns_copy():
    s1 = get_scenarios()
    s2 = get_scenarios()
    assert s1 is not s2


def test_all_scenarios_have_id():
    for sc in get_scenarios():
        assert "id" in sc
        assert sc["id"].startswith("SC179-")


def test_all_scenarios_have_name():
    for sc in get_scenarios():
        assert "name" in sc
        assert len(sc["name"]) > 0


def test_all_scenarios_have_expected_action():
    for sc in get_scenarios():
        assert "expected_action" in sc


def test_all_scenarios_paper_only():
    for sc in get_scenarios():
        assert sc.get("paper_only") is True


def test_all_scenarios_research_only():
    for sc in get_scenarios():
        assert sc.get("research_only") is True


def test_all_scenarios_no_real_orders():
    for sc in get_scenarios():
        assert sc.get("no_real_orders") is True


def test_all_scenarios_no_broker():
    for sc in get_scenarios():
        assert sc.get("no_broker") is True


def test_all_scenarios_not_investment_advice():
    for sc in get_scenarios():
        assert sc.get("not_investment_advice") is True


def test_all_scenarios_demo_only():
    for sc in get_scenarios():
        assert sc.get("demo_only") is True


def test_all_scenarios_not_for_production():
    for sc in get_scenarios():
        assert sc.get("not_for_production") is True


def test_scenario_ids_are_unique():
    ids = [sc["id"] for sc in get_scenarios()]
    assert len(ids) == len(set(ids))


def test_get_scenario_by_id_sc179_001():
    sc = get_scenario_by_id("SC179-001")
    assert sc is not None
    assert sc["expected_action"] == "PAPER_ENTRY_ALLOWED"


def test_get_scenario_by_id_sc179_050():
    sc = get_scenario_by_id("SC179-050")
    assert sc is not None
    assert sc["expected_action"] == "NO_TRADE"


def test_get_scenario_by_id_nonexistent_returns_none():
    sc = get_scenario_by_id("SC179-999")
    assert sc is None


def test_get_scenarios_by_action_paper_entry_allowed():
    scenarios = get_scenarios_by_action("PAPER_ENTRY_ALLOWED")
    assert len(scenarios) == 10
    for sc in scenarios:
        assert sc["expected_action"] == "PAPER_ENTRY_ALLOWED"


def test_get_scenarios_by_action_blocked():
    scenarios = get_scenarios_by_action("BLOCKED")
    assert len(scenarios) == 5
    for sc in scenarios:
        assert sc["expected_action"] == "BLOCKED"


def test_get_scenarios_by_action_no_trade():
    scenarios = get_scenarios_by_action("NO_TRADE")
    assert len(scenarios) == 2
    for sc in scenarios:
        assert sc["expected_action"] == "NO_TRADE"


def test_get_scenarios_by_action_wait():
    scenarios = get_scenarios_by_action("WAIT")
    assert len(scenarios) == 8


def test_get_scenarios_by_action_reduce_risk():
    scenarios = get_scenarios_by_action("REDUCE_RISK")
    assert len(scenarios) == 5


def test_scenario_sc179_044_blocked_real_order():
    sc = get_scenario_by_id("SC179-044")
    assert sc is not None
    assert sc["expected_action"] == "BLOCKED"
    assert sc.get("real_order_requested") is True


def test_scenario_sc179_011_paper_plan_ready():
    sc = get_scenario_by_id("SC179-011")
    assert sc is not None
    assert sc["expected_action"] == "PAPER_PLAN_READY"


def test_no_scenario_has_forbidden_expected_action():
    forbidden = {"BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE"}
    for sc in get_scenarios():
        assert sc["expected_action"] not in forbidden
