"""tests/test_integrated_strategy_fixtures_v178.py — v1.7.8 integrated strategy fixture registry tests."""
import pytest
from paper_trading.small_capital_strategy.integrated_strategy_fixture_registry_v178 import (
    get_fixtures,
    count_fixtures,
    get_fixture_by_id,
    validate_registry,
)

_FORBIDDEN_ACTIONS = {"BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER"}


class TestGetFixtures:
    def test_returns_list(self):
        result = get_fixtures()
        assert isinstance(result, list)

    def test_count_ge_70(self):
        result = get_fixtures()
        assert len(result) >= 70

    def test_all_paper_only(self):
        for f in get_fixtures():
            assert f["paper_only"] is True, f"Fixture {f.get('fixture_id')} missing paper_only"

    def test_all_research_only(self):
        for f in get_fixtures():
            assert f["research_only"] is True, f"Fixture {f.get('fixture_id')} missing research_only"

    def test_all_no_real_orders(self):
        for f in get_fixtures():
            assert f["no_real_orders"] is True, f"Fixture {f.get('fixture_id')} missing no_real_orders"

    def test_all_no_broker(self):
        for f in get_fixtures():
            assert f["no_broker"] is True, f"Fixture {f.get('fixture_id')} missing no_broker"

    def test_all_not_investment_advice(self):
        for f in get_fixtures():
            assert f["not_investment_advice"] is True, f"Fixture {f.get('fixture_id')} missing not_investment_advice"

    def test_all_demo_only(self):
        for f in get_fixtures():
            assert f["demo_only"] is True, f"Fixture {f.get('fixture_id')} missing demo_only"

    def test_all_not_for_production(self):
        for f in get_fixtures():
            assert f["not_for_production"] is True, f"Fixture {f.get('fixture_id')} missing not_for_production"

    def test_all_have_fixture_id(self):
        for f in get_fixtures():
            assert "fixture_id" in f, f"Fixture missing fixture_id: {f}"

    def test_all_fixture_ids_unique(self):
        ids = [f["fixture_id"] for f in get_fixtures()]
        assert len(ids) == len(set(ids)), "Duplicate fixture_ids found"

    def test_all_have_expected_action(self):
        for f in get_fixtures():
            assert "expected_action" in f, f"Fixture {f.get('fixture_id')} missing expected_action"

    def test_all_have_name(self):
        for f in get_fixtures():
            assert "name" in f, f"Fixture {f.get('fixture_id')} missing name field"
            assert len(f["name"]) > 0

    def test_all_have_schema_version_178(self):
        for f in get_fixtures():
            assert f.get("schema_version") == "178", (
                f"Fixture {f.get('fixture_id')} has wrong schema_version: {f.get('schema_version')}"
            )

    def test_all_have_correct_policy_version(self):
        expected = "1.7.8-small-capital-strategy-integration"
        for f in get_fixtures():
            assert f.get("policy_version") == expected, (
                f"Fixture {f.get('fixture_id')} has wrong policy_version: {f.get('policy_version')}"
            )

    def test_no_forbidden_expected_actions(self):
        for f in get_fixtures():
            assert f["expected_action"] not in _FORBIDDEN_ACTIONS, (
                f"Fixture {f.get('fixture_id')} has forbidden action: {f['expected_action']}"
            )

    def test_covers_at_least_7_action_values(self):
        actions = {f["expected_action"] for f in get_fixtures()}
        assert len(actions) >= 7, f"Only {len(actions)} action types covered"

    def test_at_least_10_blocked_fixtures(self):
        blocked = [f for f in get_fixtures() if f["expected_action"] == "BLOCKED"]
        assert len(blocked) >= 10

    def test_at_least_5_paper_entry_allowed_fixtures(self):
        matches = [f for f in get_fixtures() if f["expected_action"] == "PAPER_ENTRY_ALLOWED"]
        assert len(matches) >= 5

    def test_at_least_5_paper_plan_ready_fixtures(self):
        matches = [f for f in get_fixtures() if f["expected_action"] == "PAPER_PLAN_READY"]
        assert len(matches) >= 5

    def test_at_least_5_no_trade_fixtures(self):
        matches = [f for f in get_fixtures() if f["expected_action"] == "NO_TRADE"]
        assert len(matches) >= 5

    def test_at_least_3_wait_fixtures(self):
        matches = [f for f in get_fixtures() if f["expected_action"] == "WAIT"]
        assert len(matches) >= 3

    def test_at_least_3_observe_fixtures(self):
        matches = [f for f in get_fixtures() if f["expected_action"] == "OBSERVE"]
        assert len(matches) >= 3

    def test_at_least_3_reduce_risk_fixtures(self):
        matches = [f for f in get_fixtures() if f["expected_action"] == "REDUCE_RISK"]
        assert len(matches) >= 3

    def test_at_least_3_review_required_fixtures(self):
        matches = [f for f in get_fixtures() if f["expected_action"] == "REVIEW_REQUIRED"]
        assert len(matches) >= 3

    def test_at_least_3_paper_add_allowed_fixtures(self):
        matches = [f for f in get_fixtures() if f["expected_action"] == "PAPER_ADD_ALLOWED"]
        assert len(matches) >= 3


class TestCountFixtures:
    def test_count_ge_70(self):
        assert count_fixtures() >= 70

    def test_count_matches_list_length(self):
        assert count_fixtures() == len(get_fixtures())

    def test_count_is_deterministic(self):
        first = count_fixtures()
        second = count_fixtures()
        assert first == second


class TestGetFixtureById:
    def test_fx178_001_not_none(self):
        result = get_fixture_by_id("FX178-001")
        assert result is not None

    def test_fx178_021_action_blocked(self):
        result = get_fixture_by_id("FX178-021")
        assert result["expected_action"] == "BLOCKED"

    def test_fx178_021_no_stop_loss(self):
        result = get_fixture_by_id("FX178-021")
        assert result["has_stop_loss"] is False

    def test_nonexistent_returns_none(self):
        result = get_fixture_by_id("NONEXISTENT")
        assert result is None

    def test_empty_string_returns_none(self):
        result = get_fixture_by_id("")
        assert result is None

    def test_returns_correct_fixture_id(self):
        result = get_fixture_by_id("FX178-001")
        assert result["fixture_id"] == "FX178-001"


class TestValidateRegistry:
    def test_returns_dict(self):
        result = validate_registry()
        assert isinstance(result, dict)

    def test_valid_is_true(self):
        result = validate_registry()
        assert result["valid"] is True

    def test_issues_empty(self):
        result = validate_registry()
        assert result["issues"] == []

    def test_count_ge_70(self):
        result = validate_registry()
        assert result["count"] >= 70

    def test_paper_only_true(self):
        result = validate_registry()
        assert result["paper_only"] is True

    def test_research_only_true(self):
        result = validate_registry()
        assert result["research_only"] is True
