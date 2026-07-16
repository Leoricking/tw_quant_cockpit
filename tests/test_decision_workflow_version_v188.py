"""
tests/test_decision_workflow_version_v188.py
Tests for decision_workflow_version_v188 — Paper Decision Workflow Runner v1.8.8.
[!] Research Only. Paper Only. Workflow Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_workflow_version_v188 import (
    VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
    INCLUDED_RELEASES, WORKFLOW_TYPES, WORKFLOW_STEPS,
    FINAL_WORKFLOW_GRADES, ALLOWED_WORKFLOW_ACTIONS, FORBIDDEN_WORKFLOW_ACTIONS,
    MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH_CHECKS, KNOWN_RELEASE_NAMES,
    get_version_info, verify_version, is_known_release, check_minimum_version,
    get_workflow_types, get_workflow_steps, get_final_workflow_grades,
    get_allowed_workflow_actions, get_forbidden_workflow_actions,
)


def test_version_is_188():
    assert VERSION == "1.8.8"


def test_release_name_is_paper_decision_workflow_runner():
    assert RELEASE_NAME == "Paper Decision Workflow Runner"


def test_schema_version_is_188():
    assert SCHEMA_VERSION == "188"


def test_policy_version_contains_188():
    assert "1.8.8" in POLICY_VERSION


def test_policy_version_contains_workflow():
    assert "workflow" in POLICY_VERSION


def test_included_releases_has_v188():
    assert "Paper Decision Workflow Runner v1.8.8" in INCLUDED_RELEASES


def test_included_releases_has_v187():
    assert "Decision Report Export & Evidence Pack v1.8.7" in INCLUDED_RELEASES


def test_included_releases_has_v186():
    assert "End-to-End Small Capital Decision Cockpit v1.8.6" in INCLUDED_RELEASES


def test_included_releases_has_v170():
    assert "Small Capital Strategy v1.7.0" in INCLUDED_RELEASES


def test_included_releases_count_ge_18():
    assert len(INCLUDED_RELEASES) >= 18


def test_workflow_types_count_12():
    assert len(WORKFLOW_TYPES) == 12


def test_workflow_types_contains_daily():
    assert "daily_workflow" in WORKFLOW_TYPES


def test_workflow_types_contains_weekly():
    assert "weekly_workflow" in WORKFLOW_TYPES


def test_workflow_types_contains_pre_market():
    assert "pre_market_workflow" in WORKFLOW_TYPES


def test_workflow_types_contains_post_market():
    assert "post_market_workflow" in WORKFLOW_TYPES


def test_workflow_types_contains_watchlist():
    assert "watchlist_workflow" in WORKFLOW_TYPES


def test_workflow_types_contains_candidate_review():
    assert "candidate_review_workflow" in WORKFLOW_TYPES


def test_workflow_types_contains_risk_review():
    assert "risk_review_workflow" in WORKFLOW_TYPES


def test_workflow_types_contains_portfolio_review():
    assert "portfolio_review_workflow" in WORKFLOW_TYPES


def test_workflow_types_contains_blocked_market():
    assert "blocked_market_workflow" in WORKFLOW_TYPES


def test_workflow_types_contains_report_generation():
    assert "report_generation_workflow" in WORKFLOW_TYPES


def test_workflow_types_contains_evidence_pack():
    assert "evidence_pack_workflow" in WORKFLOW_TYPES


def test_workflow_types_contains_audit_trail():
    assert "audit_trail_workflow" in WORKFLOW_TYPES


def test_workflow_steps_count_20():
    assert len(WORKFLOW_STEPS) == 20


def test_workflow_steps_contains_load_config():
    assert "load_config" in WORKFLOW_STEPS


def test_workflow_steps_contains_validate_safety():
    assert "validate_safety_flags" in WORKFLOW_STEPS


def test_workflow_steps_contains_load_watchlist():
    assert "load_watchlist" in WORKFLOW_STEPS


def test_workflow_steps_contains_evaluate_market_regime():
    assert "evaluate_market_regime" in WORKFLOW_STEPS


def test_workflow_steps_contains_run_decision_cockpit():
    assert "run_decision_cockpit" in WORKFLOW_STEPS


def test_workflow_steps_contains_final_workflow_grade():
    assert "final_workflow_grade" in WORKFLOW_STEPS


def test_final_workflow_grades_count_5():
    assert len(FINAL_WORKFLOW_GRADES) == 5


def test_final_workflow_grades_contains_complete():
    assert "COMPLETE" in FINAL_WORKFLOW_GRADES


def test_final_workflow_grades_contains_blocked():
    assert "BLOCKED" in FINAL_WORKFLOW_GRADES


def test_final_workflow_grades_contains_invalid():
    assert "INVALID" in FINAL_WORKFLOW_GRADES


def test_allowed_actions_count_20():
    assert len(ALLOWED_WORKFLOW_ACTIONS) == 20


def test_allowed_actions_contains_observe():
    assert "OBSERVE" in ALLOWED_WORKFLOW_ACTIONS


def test_allowed_actions_contains_workflow_only():
    assert "WORKFLOW_ONLY" in ALLOWED_WORKFLOW_ACTIONS


def test_allowed_actions_not_buy():
    assert "BUY" not in ALLOWED_WORKFLOW_ACTIONS


def test_allowed_actions_not_sell():
    assert "SELL" not in ALLOWED_WORKFLOW_ACTIONS


def test_forbidden_actions_contains_buy():
    assert "BUY" in FORBIDDEN_WORKFLOW_ACTIONS


def test_forbidden_actions_contains_broker_order():
    assert "BROKER_ORDER" in FORBIDDEN_WORKFLOW_ACTIONS


def test_min_scenarios_75():
    assert MIN_SCENARIOS == 75


def test_min_fixtures_75():
    assert MIN_FIXTURES == 75


def test_min_cli_21():
    assert MIN_CLI == 21


def test_get_version_info_returns_dict():
    info = get_version_info()
    assert isinstance(info, dict)


def test_get_version_info_paper_only():
    info = get_version_info()
    assert info["paper_only"] is True


def test_get_version_info_no_real_orders():
    info = get_version_info()
    assert info["no_real_orders"] is True


def test_get_version_info_workflow_only():
    info = get_version_info()
    assert info["workflow_only"] is True


def test_get_version_info_version_188():
    info = get_version_info()
    assert info["version"] == "1.8.8"


def test_verify_version_true():
    assert verify_version() is True


def test_is_known_release_v188():
    assert is_known_release("Paper Decision Workflow Runner v1.8.8") is True


def test_is_known_release_v187():
    assert is_known_release("Decision Report Export & Evidence Pack v1.8.7") is True


def test_is_known_release_unknown_false():
    assert is_known_release("Unknown Release v9.9.9") is False


def test_check_minimum_version_100():
    assert check_minimum_version("1.0.0") is True


def test_check_minimum_version_188():
    assert check_minimum_version("1.8.8") is True


def test_get_workflow_types_returns_list():
    wt = get_workflow_types()
    assert isinstance(wt, list)
    assert len(wt) == 12


def test_get_workflow_steps_returns_list():
    ws = get_workflow_steps()
    assert isinstance(ws, list)
    assert len(ws) == 20


def test_get_final_workflow_grades_returns_list():
    grades = get_final_workflow_grades()
    assert isinstance(grades, list)
    assert "COMPLETE" in grades


def test_get_allowed_workflow_actions_returns_list():
    actions = get_allowed_workflow_actions()
    assert isinstance(actions, list)
    assert "DECISION_ONLY" in actions


def test_get_forbidden_workflow_actions_returns_list():
    forbidden = get_forbidden_workflow_actions()
    assert isinstance(forbidden, list)
    assert "BUY" in forbidden
