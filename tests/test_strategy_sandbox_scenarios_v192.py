"""tests/test_strategy_sandbox_scenarios_v192.py
Tests for strategy sandbox scenarios v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_sandbox_scenarios_v192 import (
    SCENARIOS, get_all_scenarios, get_scenarios_by_type, get_scenario_by_id,
)


# ── Count and universal fields ────────────────────────────────────────────────

def test_get_all_scenarios_count_75():
    assert len(get_all_scenarios()) == 75

def test_scenarios_all_paper_only():
    assert all(s["paper_only"] is True for s in get_all_scenarios())

def test_scenarios_all_sandbox_only():
    assert all(s["sandbox_only"] is True for s in get_all_scenarios())

def test_scenarios_all_shadow_only():
    assert all(s["shadow_only"] is True for s in get_all_scenarios())

def test_scenarios_all_no_real_orders():
    assert all(s["no_real_orders"] is True for s in get_all_scenarios())

def test_scenarios_all_no_broker():
    assert all(s["no_broker"] is True for s in get_all_scenarios())

def test_scenarios_all_production_trading_blocked():
    assert all(s["production_trading_blocked"] is True for s in get_all_scenarios())

def test_scenarios_all_schema_version_192():
    assert all(s["schema_version"] == "192" for s in get_all_scenarios())

def test_scenarios_all_have_scenario_id():
    assert all("scenario_id" in s for s in get_all_scenarios())

def test_scenarios_all_have_scenario_type():
    assert all("scenario_type" in s for s in get_all_scenarios())

def test_scenarios_all_have_description():
    assert all("description" in s for s in get_all_scenarios())

def test_scenarios_not_investment_advice():
    assert all(s["not_investment_advice"] is True for s in get_all_scenarios())

def test_scenarios_no_margin():
    assert all(s["no_margin"] is True for s in get_all_scenarios())

def test_scenarios_no_leverage():
    assert all(s["no_leverage"] is True for s in get_all_scenarios())


# ── get_scenarios_by_type ─────────────────────────────────────────────────────

def test_get_scenarios_by_type_complete_sandbox_validation():
    scenarios = get_scenarios_by_type("complete_sandbox_validation")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_shadow_compare_baseline_vs_candidate():
    scenarios = get_scenarios_by_type("shadow_compare_baseline_vs_candidate")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_candidate_strategy_paper_approved():
    scenarios = get_scenarios_by_type("candidate_strategy_paper_approved")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_candidate_strategy_regression_detected():
    scenarios = get_scenarios_by_type("candidate_strategy_regression_detected")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_empty_baseline_blocked():
    scenarios = get_scenarios_by_type("empty_baseline_blocked")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_empty_candidate_blocked():
    scenarios = get_scenarios_by_type("empty_candidate_blocked")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_malformed_sandbox_input():
    scenarios = get_scenarios_by_type("malformed_sandbox_input")
    assert len(scenarios) >= 1

def test_get_scenarios_by_type_unknown_returns_empty():
    scenarios = get_scenarios_by_type("not_a_real_type_xyz")
    assert len(scenarios) == 0


# ── get_scenario_by_id ────────────────────────────────────────────────────────

def test_get_scenario_by_id_001_not_none():
    assert get_scenario_by_id("SS192-001") is not None

def test_get_scenario_by_id_075_not_none():
    assert get_scenario_by_id("SS192-075") is not None

def test_get_scenario_by_id_nonexistent_is_none():
    assert get_scenario_by_id("SS192-999") is None

def test_get_scenario_by_id_empty_string_is_none():
    assert get_scenario_by_id("") is None

def test_get_scenario_by_id_001_is_dict():
    result = get_scenario_by_id("SS192-001")
    assert isinstance(result, dict)

def test_get_scenario_by_id_001_paper_only():
    result = get_scenario_by_id("SS192-001")
    assert result["paper_only"] is True


# ── Blocked scenarios have block_reason ───────────────────────────────────────

def test_blocked_scenarios_have_block_reason():
    blocked = [s for s in get_all_scenarios() if s.get("blocked") is True]
    assert len(blocked) > 0
    for s in blocked:
        assert "block_reason" in s
        assert s["block_reason"] != ""

def test_non_blocked_scenarios_exist():
    non_blocked = [s for s in get_all_scenarios() if s.get("blocked") is not True]
    assert len(non_blocked) > 0


# ── Unique scenario IDs ───────────────────────────────────────────────────────

def test_all_scenario_ids_unique():
    ids = [s["scenario_id"] for s in get_all_scenarios()]
    assert len(ids) == len(set(ids))

def test_scenario_ids_follow_ss192_pattern():
    ids = [s["scenario_id"] for s in get_all_scenarios()]
    assert all(sid.startswith("SS192-") for sid in ids)


# ── Scenario types coverage ───────────────────────────────────────────────────

def test_scenario_types_includes_a_rule_tightening():
    types = {s["scenario_type"] for s in get_all_scenarios()}
    assert "a_rule_tightening_improves_risk" in types

def test_scenario_types_includes_candidate_strategy_blocked():
    types = {s["scenario_type"] for s in get_all_scenarios()}
    assert "candidate_strategy_blocked" in types

def test_scenario_types_includes_complete_sandbox_evidence_pack():
    types = {s["scenario_type"] for s in get_all_scenarios()}
    assert "complete_sandbox_evidence_pack" in types

def test_at_least_15_distinct_scenario_types():
    types = {s["scenario_type"] for s in get_all_scenarios()}
    assert len(types) >= 15
