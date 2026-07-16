"""
tests/test_decision_journal_version_v189.py
Tests for decision_journal_version_v189 — Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_journal_version_v189 import (
    VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
    INCLUDED_RELEASES, JOURNAL_ENTRY_STATES, REVIEW_DIMENSIONS,
    MISTAKE_TAGS, QUALITY_GRADES, FORBIDDEN_JOURNAL_ACTIONS,
    ALLOWED_JOURNAL_ACTIONS, HARD_BLOCK_CONDITIONS,
    get_version_info, verify_version, is_known_release, check_minimum_version,
    get_journal_entry_states, get_review_dimensions, get_mistake_tags,
    get_quality_grades, get_allowed_journal_actions, get_forbidden_journal_actions,
    get_hard_block_conditions,
)


def test_version_is_189():
    assert VERSION == "1.8.9"


def test_release_name_is_correct():
    assert RELEASE_NAME == "Paper Decision Journal & Review Loop"


def test_schema_version_is_189():
    assert SCHEMA_VERSION == "189"


def test_policy_version_contains_189():
    assert "1.8.9" in POLICY_VERSION


def test_verify_version_returns_true():
    assert verify_version() is True


def test_included_releases_contains_v189():
    assert "Paper Decision Journal & Review Loop v1.8.9" in INCLUDED_RELEASES


def test_included_releases_contains_v188():
    assert "Paper Decision Workflow Runner v1.8.8" in INCLUDED_RELEASES


def test_included_releases_contains_v170():
    assert "Small Capital Strategy v1.7.0" in INCLUDED_RELEASES


def test_journal_entry_states_count():
    assert len(JOURNAL_ENTRY_STATES) == 16


def test_journal_entry_states_contains_observe():
    assert "OBSERVE" in JOURNAL_ENTRY_STATES


def test_journal_entry_states_contains_wait():
    assert "WAIT" in JOURNAL_ENTRY_STATES


def test_journal_entry_states_contains_paper_plan_ready():
    assert "PAPER_PLAN_READY" in JOURNAL_ENTRY_STATES


def test_journal_entry_states_contains_paper_entry_allowed():
    assert "PAPER_ENTRY_ALLOWED" in JOURNAL_ENTRY_STATES


def test_journal_entry_states_contains_reduce_risk():
    assert "REDUCE_RISK" in JOURNAL_ENTRY_STATES


def test_journal_entry_states_contains_blocked():
    assert "BLOCKED" in JOURNAL_ENTRY_STATES


def test_journal_entry_states_contains_no_trade():
    assert "NO_TRADE" in JOURNAL_ENTRY_STATES


def test_journal_entry_states_contains_audit_only():
    assert "AUDIT_ONLY" in JOURNAL_ENTRY_STATES


def test_review_dimensions_count():
    assert len(REVIEW_DIMENSIONS) == 20


def test_review_dimensions_contains_market_regime():
    assert "market_regime_alignment" in REVIEW_DIMENSIONS


def test_review_dimensions_contains_audit_traceability():
    assert "audit_traceability" in REVIEW_DIMENSIONS


def test_review_dimensions_contains_evidence_completeness():
    assert "evidence_completeness" in REVIEW_DIMENSIONS


def test_review_dimensions_contains_journal_completeness():
    assert "journal_completeness" in REVIEW_DIMENSIONS


def test_mistake_tags_count():
    assert len(MISTAKE_TAGS) == 18


def test_mistake_tags_contains_chase_high():
    assert "CHASE_HIGH" in MISTAKE_TAGS


def test_mistake_tags_contains_no_mistake_found():
    assert "NO_MISTAKE_FOUND" in MISTAKE_TAGS


def test_mistake_tags_contains_oversize_position():
    assert "OVERSIZE_POSITION" in MISTAKE_TAGS


def test_mistake_tags_contains_missing_evidence():
    assert "MISSING_EVIDENCE" in MISTAKE_TAGS


def test_quality_grades_count():
    assert len(QUALITY_GRADES) == 6


def test_quality_grades_contains_excellent():
    assert "EXCELLENT" in QUALITY_GRADES


def test_quality_grades_contains_invalid():
    assert "INVALID" in QUALITY_GRADES


def test_quality_grades_contains_poor():
    assert "POOR" in QUALITY_GRADES


def test_forbidden_journal_actions_count():
    assert len(FORBIDDEN_JOURNAL_ACTIONS) == 9


def test_forbidden_contains_buy():
    assert "BUY" in FORBIDDEN_JOURNAL_ACTIONS


def test_forbidden_contains_sell():
    assert "SELL" in FORBIDDEN_JOURNAL_ACTIONS


def test_forbidden_contains_broker_order():
    assert "BROKER_ORDER" in FORBIDDEN_JOURNAL_ACTIONS


def test_forbidden_contains_submit_order():
    assert "SUBMIT_ORDER" in FORBIDDEN_JOURNAL_ACTIONS


def test_allowed_journal_actions_count():
    assert len(ALLOWED_JOURNAL_ACTIONS) == 16


def test_allowed_contains_observe():
    assert "OBSERVE" in ALLOWED_JOURNAL_ACTIONS


def test_allowed_contains_decision_only():
    assert "DECISION_ONLY" in ALLOWED_JOURNAL_ACTIONS


def test_allowed_does_not_contain_buy():
    assert "BUY" not in ALLOWED_JOURNAL_ACTIONS


def test_hard_block_conditions_count():
    assert len(HARD_BLOCK_CONDITIONS) == 18


def test_hard_block_contains_real_order():
    assert "real_order_requested" in HARD_BLOCK_CONDITIONS


def test_hard_block_contains_unsafe_export():
    assert "unsafe_export_path" in HARD_BLOCK_CONDITIONS


def test_hard_block_contains_missing_journal_audit_trail():
    assert "missing_journal_audit_trail" in HARD_BLOCK_CONDITIONS


def test_get_version_info_returns_dict():
    info = get_version_info()
    assert isinstance(info, dict)


def test_get_version_info_paper_only():
    assert get_version_info()["paper_only"] is True


def test_get_version_info_journal_only():
    assert get_version_info()["journal_only"] is True


def test_get_version_info_no_real_orders():
    assert get_version_info()["no_real_orders"] is True


def test_get_version_info_not_investment_advice():
    assert get_version_info()["not_investment_advice"] is True


def test_is_known_release_v189():
    assert is_known_release("Paper Decision Journal & Review Loop v1.8.9") is True


def test_is_known_release_v188():
    assert is_known_release("Paper Decision Workflow Runner v1.8.8") is True


def test_is_known_release_unknown_false():
    assert is_known_release("Unknown Release v99.9") is False


def test_check_minimum_version_170():
    assert check_minimum_version("1.7.0") is True


def test_check_minimum_version_189():
    assert check_minimum_version("1.8.9") is True


def test_check_minimum_version_higher_false():
    assert check_minimum_version("1.9.0") is False


def test_get_journal_entry_states_returns_list():
    assert isinstance(get_journal_entry_states(), list)


def test_get_journal_entry_states_count():
    assert len(get_journal_entry_states()) == 16


def test_get_review_dimensions_returns_list():
    assert isinstance(get_review_dimensions(), list)


def test_get_review_dimensions_count():
    assert len(get_review_dimensions()) == 20


def test_get_mistake_tags_returns_list():
    assert isinstance(get_mistake_tags(), list)


def test_get_mistake_tags_count():
    assert len(get_mistake_tags()) == 18


def test_get_quality_grades_returns_list():
    assert isinstance(get_quality_grades(), list)


def test_get_quality_grades_count():
    assert len(get_quality_grades()) == 6


def test_get_allowed_journal_actions_returns_list():
    assert isinstance(get_allowed_journal_actions(), list)


def test_get_allowed_journal_actions_count():
    assert len(get_allowed_journal_actions()) == 16


def test_get_forbidden_journal_actions_returns_list():
    assert isinstance(get_forbidden_journal_actions(), list)


def test_get_forbidden_journal_actions_count():
    assert len(get_forbidden_journal_actions()) == 9


def test_get_hard_block_conditions_returns_list():
    assert isinstance(get_hard_block_conditions(), list)


def test_get_hard_block_conditions_count():
    assert len(get_hard_block_conditions()) == 18
