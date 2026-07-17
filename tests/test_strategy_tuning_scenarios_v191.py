"""tests/test_strategy_tuning_scenarios_v191.py
Tests for strategy tuning scenarios v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_tuning_scenarios_v191 import (
    SCENARIOS, get_all_scenarios, get_scenarios_by_type, get_scenario_by_id,
)


def test_scenarios_count_75():
    assert len(get_all_scenarios()) == 75

def test_scenarios_all_paper_only():
    assert all(s["paper_only"] is True for s in get_all_scenarios())

def test_scenarios_all_no_real_orders():
    assert all(s["no_real_orders"] is True for s in get_all_scenarios())

def test_scenarios_all_no_broker():
    assert all(s["no_broker"] is True for s in get_all_scenarios())

def test_scenarios_all_tuning_only():
    assert all(s["tuning_only"] is True for s in get_all_scenarios())

def test_scenarios_all_guardrail_only():
    assert all(s["guardrail_only"] is True for s in get_all_scenarios())

def test_scenarios_all_no_production_mutation():
    assert all(s["no_production_strategy_mutation"] is True for s in get_all_scenarios())

def test_scenarios_all_not_investment_advice():
    assert all(s["not_investment_advice"] is True for s in get_all_scenarios())

def test_scenarios_all_production_trading_blocked():
    assert all(s["production_trading_blocked"] is True for s in get_all_scenarios())

def test_scenarios_all_have_scenario_id():
    assert all("scenario_id" in s for s in get_all_scenarios())

def test_scenarios_all_have_scenario_type():
    assert all("scenario_type" in s for s in get_all_scenarios())

def test_scenarios_all_have_description():
    assert all("description" in s for s in get_all_scenarios())

def test_scenarios_schema_191():
    assert all(s["schema_version"] == "191" for s in get_all_scenarios())

def test_scenarios_no_forbidden_words_in_description():
    forbidden = ["SUBMIT_ORDER", "BROKER_ORDER", "AUTO_TRADE", "LIVE_TRADE"]
    for s in get_all_scenarios():
        desc = s.get("description", "").upper()
        assert not any(w in desc for w in forbidden)

def test_get_scenarios_by_type_complete_review():
    scenarios = get_scenarios_by_type("complete_rule_tuning_review")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_empty_source_blocked():
    scenarios = get_scenarios_by_type("empty_performance_source_blocked")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_malformed_input():
    scenarios = get_scenarios_by_type("malformed_tuning_input")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_keep_abc():
    scenarios = get_scenarios_by_type("keep_a_buy_point_rule")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_tighten_abc():
    scenarios = get_scenarios_by_type("tighten_a_buy_point_rule")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_tighten_breakout():
    scenarios = get_scenarios_by_type("tighten_b_breakout_rule")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_disable_setup():
    scenarios = get_scenarios_by_type("disable_weak_setup")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_add_guardrail():
    scenarios = get_scenarios_by_type("add_chase_high_guardrail")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_lower_position_size():
    scenarios = get_scenarios_by_type("lower_position_size")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_raise_cash_reserve():
    scenarios = get_scenarios_by_type("raise_cash_reserve")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_production_blocked():
    scenarios = get_scenarios_by_type("production_mutation_blocked")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_forbidden_word_blocked():
    scenarios = get_scenarios_by_type("forbidden_action_word_blocked")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_evidence_pack():
    scenarios = get_scenarios_by_type("complete_tuning_evidence_pack")
    assert len(scenarios) >= 1

def test_get_scenario_by_id_first():
    s = get_scenario_by_id("ST191-001")
    assert s["scenario_id"] == "ST191-001"

def test_get_scenario_by_id_last():
    s = get_scenario_by_id("ST191-075")
    assert s["scenario_id"] == "ST191-075"

def test_get_scenario_by_id_not_found():
    s = get_scenario_by_id("ST191-999")
    assert s == {}

def test_scenarios_unique_ids():
    ids = [s["scenario_id"] for s in get_all_scenarios()]
    assert len(ids) == len(set(ids))

def test_scenarios_blocked_scenarios_have_block_reason():
    for s in get_all_scenarios():
        if s.get("blocked", False):
            assert "block_reason" in s

def test_scenarios_complete_review_not_blocked():
    for s in get_scenarios_by_type("complete_rule_tuning_review"):
        assert s.get("blocked", False) is False

def test_scenarios_safety_audit_type_exists():
    scenarios = get_scenarios_by_type("safety_audit_all_safe")
    assert len(scenarios) >= 1
