"""tests/test_integrated_strategy_scenarios_v178.py — v1.7.8 integrated strategy scenarios tests."""
import pytest
from paper_trading.small_capital_strategy.integrated_strategy_scenarios_v178 import (
    get_scenarios,
    count_scenarios,
    get_scenario_by_id,
    get_scenarios_by_action,
)

_VALID_ACTIONS = {
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED",
    "PAPER_ADD_ALLOWED", "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE",
}
_FORBIDDEN_ACTIONS = {
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
}


class TestGetScenarios:
    def test_returns_list(self):
        result = get_scenarios()
        assert isinstance(result, list)

    def test_count_ge_70(self):
        result = get_scenarios()
        assert len(result) >= 70

    def test_all_paper_only(self):
        for s in get_scenarios():
            assert s["paper_only"] is True, f"Scenario {s.get('id')} missing paper_only"

    def test_all_research_only(self):
        for s in get_scenarios():
            assert s["research_only"] is True, f"Scenario {s.get('id')} missing research_only"

    def test_all_no_real_orders(self):
        for s in get_scenarios():
            assert s["no_real_orders"] is True, f"Scenario {s.get('id')} missing no_real_orders"

    def test_all_no_broker(self):
        for s in get_scenarios():
            assert s["no_broker"] is True, f"Scenario {s.get('id')} missing no_broker"

    def test_all_not_investment_advice(self):
        for s in get_scenarios():
            assert s["not_investment_advice"] is True, f"Scenario {s.get('id')} missing not_investment_advice"

    def test_all_demo_only(self):
        for s in get_scenarios():
            assert s["demo_only"] is True, f"Scenario {s.get('id')} missing demo_only"

    def test_all_not_for_production(self):
        for s in get_scenarios():
            assert s["not_for_production"] is True, f"Scenario {s.get('id')} missing not_for_production"

    def test_all_have_id_field(self):
        for s in get_scenarios():
            assert "id" in s, f"Scenario missing id field: {s}"

    def test_all_ids_unique(self):
        ids = [s["id"] for s in get_scenarios()]
        assert len(ids) == len(set(ids)), "Duplicate scenario ids found"

    def test_all_have_expected_action(self):
        for s in get_scenarios():
            assert "expected_action" in s, f"Scenario {s.get('id')} missing expected_action"

    def test_all_expected_action_valid(self):
        for s in get_scenarios():
            assert s["expected_action"] in _VALID_ACTIONS, (
                f"Scenario {s.get('id')} has invalid action: {s['expected_action']}"
            )

    def test_no_forbidden_expected_actions(self):
        for s in get_scenarios():
            assert s["expected_action"] not in _FORBIDDEN_ACTIONS, (
                f"Scenario {s.get('id')} has forbidden action: {s['expected_action']}"
            )

    def test_covers_at_least_6_action_values(self):
        actions = {s["expected_action"] for s in get_scenarios()}
        assert len(actions) >= 6, f"Only {len(actions)} action types covered"

    def test_at_least_one_blocked_no_stop_loss(self):
        matches = [
            s for s in get_scenarios()
            if not s.get("has_stop_loss", True) and s["expected_action"] == "BLOCKED"
        ]
        assert len(matches) >= 1, "No BLOCKED scenario found for has_stop_loss=False"

    def test_at_least_one_blocked_real_order_requested(self):
        matches = [
            s for s in get_scenarios()
            if s.get("real_order_requested") is True and s["expected_action"] == "BLOCKED"
        ]
        assert len(matches) >= 1, "No BLOCKED scenario found for real_order_requested=True"

    def test_at_least_one_blocked_broker_requested(self):
        matches = [
            s for s in get_scenarios()
            if s.get("broker_requested") is True and s["expected_action"] == "BLOCKED"
        ]
        assert len(matches) >= 1, "No BLOCKED scenario found for broker_requested=True"

    def test_at_least_one_blocked_margin_requested(self):
        matches = [
            s for s in get_scenarios()
            if s.get("margin_requested") is True and s["expected_action"] == "BLOCKED"
        ]
        assert len(matches) >= 1, "No BLOCKED scenario found for margin_requested=True"


class TestCountScenarios:
    def test_count_ge_70(self):
        assert count_scenarios() >= 70

    def test_count_matches_list_length(self):
        assert count_scenarios() == len(get_scenarios())

    def test_count_is_deterministic(self):
        first = count_scenarios()
        second = count_scenarios()
        assert first == second


class TestGetScenarioById:
    def test_sc178_001_not_none(self):
        result = get_scenario_by_id("SC178-001")
        assert result is not None

    def test_sc178_001_action_paper_entry_allowed(self):
        result = get_scenario_by_id("SC178-001")
        assert result["expected_action"] == "PAPER_ENTRY_ALLOWED"

    def test_sc178_021_action_blocked(self):
        result = get_scenario_by_id("SC178-021")
        assert result["expected_action"] == "BLOCKED"

    def test_sc178_021_no_stop_loss(self):
        result = get_scenario_by_id("SC178-021")
        assert result["has_stop_loss"] is False

    def test_nonexistent_returns_none(self):
        result = get_scenario_by_id("NONEXISTENT")
        assert result is None

    def test_empty_string_returns_none(self):
        result = get_scenario_by_id("")
        assert result is None

    def test_returns_correct_id(self):
        result = get_scenario_by_id("SC178-001")
        assert result["id"] == "SC178-001"


class TestGetScenariosByAction:
    def test_blocked_ge_10(self):
        result = get_scenarios_by_action("BLOCKED")
        assert len(result) >= 10

    def test_paper_entry_allowed_ge_5(self):
        result = get_scenarios_by_action("PAPER_ENTRY_ALLOWED")
        assert len(result) >= 5

    def test_no_trade_ge_5(self):
        result = get_scenarios_by_action("NO_TRADE")
        assert len(result) >= 5

    def test_wait_ge_3(self):
        result = get_scenarios_by_action("WAIT")
        assert len(result) >= 3

    def test_observe_ge_3(self):
        result = get_scenarios_by_action("OBSERVE")
        assert len(result) >= 3

    def test_reduce_risk_ge_3(self):
        result = get_scenarios_by_action("REDUCE_RISK")
        assert len(result) >= 3

    def test_review_required_ge_3(self):
        result = get_scenarios_by_action("REVIEW_REQUIRED")
        assert len(result) >= 3

    def test_paper_plan_ready_ge_5(self):
        result = get_scenarios_by_action("PAPER_PLAN_READY")
        assert len(result) >= 5

    def test_all_returned_match_action(self):
        for action in _VALID_ACTIONS:
            for s in get_scenarios_by_action(action):
                assert s["expected_action"] == action

    def test_unknown_action_returns_empty_or_list(self):
        result = get_scenarios_by_action("NONEXISTENT_ACTION")
        assert isinstance(result, list)
        assert len(result) == 0
