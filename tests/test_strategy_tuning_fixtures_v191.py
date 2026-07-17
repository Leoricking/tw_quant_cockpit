"""tests/test_strategy_tuning_fixtures_v191.py
Tests for strategy tuning fixtures v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_tuning_fixtures_v191 import (
    FIXTURES, get_all_fixtures, get_fixture_by_id,
    get_fixtures_by_recommendation, get_fixtures_by_rule_category,
    get_fixtures_by_approval_state,
)


def test_fixtures_count_75():
    assert len(get_all_fixtures()) == 75

def test_fixtures_all_paper_only():
    assert all(f["paper_only"] is True for f in get_all_fixtures())

def test_fixtures_all_no_real_orders():
    assert all(f["no_real_orders"] is True for f in get_all_fixtures())

def test_fixtures_all_no_broker():
    assert all(f["no_broker"] is True for f in get_all_fixtures())

def test_fixtures_all_tuning_only():
    assert all(f["tuning_only"] is True for f in get_all_fixtures())

def test_fixtures_all_guardrail_only():
    assert all(f["guardrail_only"] is True for f in get_all_fixtures())

def test_fixtures_all_no_production_mutation():
    assert all(f["no_production_strategy_mutation"] is True for f in get_all_fixtures())

def test_fixtures_all_not_investment_advice():
    assert all(f["not_investment_advice"] is True for f in get_all_fixtures())

def test_fixtures_all_production_trading_blocked():
    assert all(f["production_trading_blocked"] is True for f in get_all_fixtures())

def test_fixtures_all_demo_only():
    assert all(f["demo_only"] is True for f in get_all_fixtures())

def test_fixtures_all_not_for_production():
    assert all(f["not_for_production"] is True for f in get_all_fixtures())

def test_fixtures_all_auto_approve_blocked():
    assert all(f["auto_approve_blocked"] is True for f in get_all_fixtures())

def test_fixtures_all_schema_191():
    assert all(f["schema_version"] == "191" for f in get_all_fixtures())

def test_fixtures_all_have_fixture_id():
    assert all("fixture_id" in f for f in get_all_fixtures())

def test_fixtures_all_have_tuning_id():
    assert all("tuning_id" in f for f in get_all_fixtures())

def test_fixtures_all_have_rule_category():
    assert all("rule_category" in f for f in get_all_fixtures())

def test_fixtures_all_have_guardrail_trigger():
    assert all("guardrail_trigger" in f for f in get_all_fixtures())

def test_fixtures_all_have_recommendation():
    assert all("recommendation" in f for f in get_all_fixtures())

def test_fixtures_all_have_approval_state():
    assert all("approval_state" in f for f in get_all_fixtures())

def test_fixtures_unique_ids():
    ids = [f["fixture_id"] for f in get_all_fixtures()]
    assert len(ids) == len(set(ids))

def test_get_fixture_by_id_first():
    f = get_fixture_by_id("STF191-001")
    assert f["fixture_id"] == "STF191-001"

def test_get_fixture_by_id_last():
    f = get_fixture_by_id("STF191-075")
    assert f["fixture_id"] == "STF191-075"

def test_get_fixture_by_id_not_found():
    f = get_fixture_by_id("STF191-999")
    assert f == {}

def test_get_fixtures_by_recommendation_keep_rule():
    fixtures = get_fixtures_by_recommendation("KEEP_RULE")
    assert len(fixtures) >= 1

def test_get_fixtures_by_recommendation_all_correct():
    fixtures = get_fixtures_by_recommendation("TIGHTEN_RULE")
    assert all(f["recommendation"] == "TIGHTEN_RULE" for f in fixtures)

def test_get_fixtures_by_rule_category_abc():
    fixtures = get_fixtures_by_rule_category("ABC_BUY_POINT")
    assert len(fixtures) >= 1

def test_get_fixtures_by_rule_category_all_correct():
    fixtures = get_fixtures_by_rule_category("POSITION_SIZING")
    assert all(f["rule_category"] == "POSITION_SIZING" for f in fixtures)

def test_get_fixtures_by_approval_state_proposed():
    fixtures = get_fixtures_by_approval_state("PROPOSED")
    assert len(fixtures) >= 1

def test_get_fixtures_win_rate_range():
    for f in get_all_fixtures():
        assert 0.0 <= f["win_rate"] <= 1.0

def test_get_fixtures_drawdown_usage_range():
    for f in get_all_fixtures():
        assert f["drawdown_budget_usage_pct"] >= 0.0

def test_get_fixtures_evidence_count_positive():
    for f in get_all_fixtures():
        assert f["evidence_count"] >= 0
