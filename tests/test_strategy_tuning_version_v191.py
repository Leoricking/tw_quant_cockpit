"""tests/test_strategy_tuning_version_v191.py
Tests for strategy tuning version v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_tuning_version_v191 import (
    VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
    RULE_CATEGORIES, GUARDRAIL_TRIGGERS, TUNING_RECOMMENDATIONS,
    APPROVAL_STATES, GUARDRAIL_SEVERITIES, GUARDRAIL_ACTIONS,
    FORBIDDEN_TUNING_ACTIONS, ALLOWED_TUNING_ACTIONS, HARD_BLOCK_CONDITIONS,
    INCLUDED_RELEASES, KNOWN_RELEASE_NAMES,
    verify_version, is_known_release, check_minimum_version,
    get_version_info, get_rule_categories, get_guardrail_triggers,
    get_tuning_recommendations, get_approval_states,
    get_guardrail_severities, get_guardrail_actions,
    get_forbidden_tuning_actions, get_allowed_tuning_actions,
    get_hard_block_conditions,
)


# ── Version constants ─────────────────────────────────────────────────────────

def test_version_is_191():
    assert VERSION == "1.9.1"

def test_release_name_correct():
    assert RELEASE_NAME == "Paper Strategy Rule Tuning & Guardrail Lab"

def test_schema_version_191():
    assert SCHEMA_VERSION == "191"

def test_policy_version_contains_191():
    assert "1.9.1" in POLICY_VERSION

def test_verify_version_returns_true():
    assert verify_version() is True

def test_verify_version_type_bool():
    assert isinstance(verify_version(), bool)


# ── Rule categories ───────────────────────────────────────────────────────────

def test_rule_categories_count_14():
    assert len(RULE_CATEGORIES) == 14

def test_rule_categories_has_abc_buy_point():
    assert "ABC_BUY_POINT" in RULE_CATEGORIES

def test_rule_categories_has_second_wave_entry():
    assert "SECOND_WAVE_ENTRY" in RULE_CATEGORIES

def test_rule_categories_has_market_regime_filter():
    assert "MARKET_REGIME_FILTER" in RULE_CATEGORIES

def test_rule_categories_has_volume_confirmation():
    assert "VOLUME_CONFIRMATION" in RULE_CATEGORIES

def test_rule_categories_has_moving_average_filter():
    assert "MOVING_AVERAGE_FILTER" in RULE_CATEGORIES

def test_rule_categories_has_position_sizing():
    assert "POSITION_SIZING" in RULE_CATEGORIES

def test_rule_categories_has_cash_reserve():
    assert "CASH_RESERVE" in RULE_CATEGORIES

def test_rule_categories_has_concentration_limit():
    assert "CONCENTRATION_LIMIT" in RULE_CATEGORIES

def test_rule_categories_has_stop_loss():
    assert "STOP_LOSS" in RULE_CATEGORIES

def test_rule_categories_has_take_profit():
    assert "TAKE_PROFIT" in RULE_CATEGORIES

def test_rule_categories_has_reduce_risk():
    assert "REDUCE_RISK" in RULE_CATEGORIES

def test_rule_categories_has_blocked_condition():
    assert "BLOCKED_CONDITION" in RULE_CATEGORIES

def test_rule_categories_has_evidence_requirement():
    assert "EVIDENCE_REQUIREMENT" in RULE_CATEGORIES

def test_rule_categories_has_manual_review():
    assert "MANUAL_REVIEW" in RULE_CATEGORIES

def test_get_rule_categories_returns_list():
    assert isinstance(get_rule_categories(), list)

def test_get_rule_categories_length():
    assert len(get_rule_categories()) == 14

def test_get_rule_categories_not_same_object():
    assert get_rule_categories() is not RULE_CATEGORIES


# ── Guardrail triggers ────────────────────────────────────────────────────────

def test_guardrail_triggers_count_16():
    assert len(GUARDRAIL_TRIGGERS) == 16

def test_guardrail_triggers_has_expectancy_negative():
    assert "EXPECTANCY_NEGATIVE" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_win_rate_too_low():
    assert "WIN_RATE_TOO_LOW" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_average_loss_too_high():
    assert "AVERAGE_LOSS_TOO_HIGH" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_drawdown_budget_exceeded():
    assert "DRAWDOWN_BUDGET_EXCEEDED" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_mistake_rate_too_high():
    assert "MISTAKE_RATE_TOO_HIGH" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_chase_high_repeated():
    assert "CHASE_HIGH_REPEATED" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_early_entry_repeated():
    assert "EARLY_ENTRY_REPEATED" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_over_concentration():
    assert "OVER_CONCENTRATION_REPEATED" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_low_cash_reserve():
    assert "LOW_CASH_RESERVE_REPEATED" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_block_reason_ignored():
    assert "BLOCK_REASON_IGNORED" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_evidence_missing():
    assert "EVIDENCE_MISSING_REPEATED" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_market_regime_mismatch():
    assert "MARKET_REGIME_MISMATCH" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_volume_confirmation_missing():
    assert "VOLUME_CONFIRMATION_MISSING" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_ma_break_ignored():
    assert "MA_BREAK_IGNORED" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_no_clear_stop():
    assert "NO_CLEAR_STOP" in GUARDRAIL_TRIGGERS

def test_guardrail_triggers_has_no_clear_take_profit():
    assert "NO_CLEAR_TAKE_PROFIT" in GUARDRAIL_TRIGGERS

def test_get_guardrail_triggers_length():
    assert len(get_guardrail_triggers()) == 16

def test_get_guardrail_triggers_returns_list():
    assert isinstance(get_guardrail_triggers(), list)


# ── Tuning recommendations ────────────────────────────────────────────────────

def test_tuning_recommendations_count_15():
    assert len(TUNING_RECOMMENDATIONS) == 15

def test_tuning_recommendations_has_keep_rule():
    assert "KEEP_RULE" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_tighten_rule():
    assert "TIGHTEN_RULE" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_loosen_rule():
    assert "LOOSEN_RULE" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_disable_setup():
    assert "DISABLE_SETUP" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_lower_position_size():
    assert "LOWER_POSITION_SIZE" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_raise_cash_reserve():
    assert "RAISE_CASH_RESERVE" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_lower_concentration():
    assert "LOWER_CONCENTRATION_LIMIT" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_require_more_evidence():
    assert "REQUIRE_MORE_EVIDENCE" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_require_regime():
    assert "REQUIRE_MARKET_REGIME_CONFIRMATION" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_require_volume():
    assert "REQUIRE_VOLUME_CONFIRMATION" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_require_ma():
    assert "REQUIRE_MA_CONFIRMATION" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_require_manual_review():
    assert "REQUIRE_MANUAL_REVIEW" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_add_guardrail():
    assert "ADD_GUARDRAIL" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_escalate():
    assert "ESCALATE_TO_REVIEW" in TUNING_RECOMMENDATIONS

def test_tuning_recommendations_has_no_change():
    assert "NO_CHANGE" in TUNING_RECOMMENDATIONS

def test_get_tuning_recommendations_length():
    assert len(get_tuning_recommendations()) == 15


# ── Approval states ───────────────────────────────────────────────────────────

def test_approval_states_count_6():
    assert len(APPROVAL_STATES) == 6

def test_approval_states_has_proposed():
    assert "PROPOSED" in APPROVAL_STATES

def test_approval_states_has_review_required():
    assert "REVIEW_REQUIRED" in APPROVAL_STATES

def test_approval_states_has_paper_approved():
    assert "PAPER_APPROVED" in APPROVAL_STATES

def test_approval_states_has_paper_rejected():
    assert "PAPER_REJECTED" in APPROVAL_STATES

def test_approval_states_has_blocked():
    assert "BLOCKED" in APPROVAL_STATES

def test_approval_states_has_invalid():
    assert "INVALID" in APPROVAL_STATES

def test_get_approval_states_length():
    assert len(get_approval_states()) == 6


# ── Forbidden / allowed actions ───────────────────────────────────────────────

def test_forbidden_actions_count_9():
    assert len(FORBIDDEN_TUNING_ACTIONS) == 9

def test_forbidden_action_buy():
    assert "BUY" in FORBIDDEN_TUNING_ACTIONS

def test_forbidden_action_sell():
    assert "SELL" in FORBIDDEN_TUNING_ACTIONS

def test_forbidden_action_order():
    assert "ORDER" in FORBIDDEN_TUNING_ACTIONS

def test_forbidden_action_execute():
    assert "EXECUTE" in FORBIDDEN_TUNING_ACTIONS

def test_forbidden_action_submit_order():
    assert "SUBMIT_ORDER" in FORBIDDEN_TUNING_ACTIONS

def test_allowed_actions_count_16():
    assert len(ALLOWED_TUNING_ACTIONS) == 16

def test_allowed_action_tune():
    assert "TUNE" in ALLOWED_TUNING_ACTIONS

def test_allowed_action_review():
    assert "REVIEW" in ALLOWED_TUNING_ACTIONS

def test_allowed_action_guardrail_check():
    assert "GUARDRAIL_CHECK" in ALLOWED_TUNING_ACTIONS

def test_allowed_action_rule_tuning():
    assert "RULE_TUNING" in ALLOWED_TUNING_ACTIONS


# ── Hard block conditions ─────────────────────────────────────────────────────

def test_hard_block_conditions_count_17():
    assert len(HARD_BLOCK_CONDITIONS) == 17

def test_hard_block_has_real_order():
    assert "real_order_requested" in HARD_BLOCK_CONDITIONS

def test_hard_block_has_broker():
    assert "broker_requested" in HARD_BLOCK_CONDITIONS

def test_hard_block_has_production_mutation():
    assert "production_strategy_mutation_attempted" in HARD_BLOCK_CONDITIONS

def test_hard_block_has_guardrail_without_trigger():
    assert "guardrail_without_trigger" in HARD_BLOCK_CONDITIONS

def test_hard_block_has_rule_adjustment_without_evidence():
    assert "rule_adjustment_without_evidence" in HARD_BLOCK_CONDITIONS

def test_hard_block_has_missing_performance_source():
    assert "missing_performance_source" in HARD_BLOCK_CONDITIONS

def test_hard_block_has_forbidden_action_words():
    assert "forbidden_action_words" in HARD_BLOCK_CONDITIONS


# ── Version info dict ─────────────────────────────────────────────────────────

def test_get_version_info_returns_dict():
    assert isinstance(get_version_info(), dict)

def test_get_version_info_paper_only():
    assert get_version_info()["paper_only"] is True

def test_get_version_info_tuning_only():
    assert get_version_info()["tuning_only"] is True

def test_get_version_info_guardrail_only():
    assert get_version_info()["guardrail_only"] is True

def test_get_version_info_no_real_orders():
    assert get_version_info()["no_real_orders"] is True

def test_get_version_info_no_broker():
    assert get_version_info()["no_broker"] is True

def test_get_version_info_not_investment_advice():
    assert get_version_info()["not_investment_advice"] is True

def test_get_version_info_no_production_mutation():
    assert get_version_info()["no_production_strategy_mutation"] is True

def test_get_version_info_version_key():
    assert get_version_info()["version"] == "1.9.1"

def test_get_version_info_schema_version():
    assert get_version_info()["schema_version"] == "191"


# ── Known releases / backward compat ─────────────────────────────────────────

def test_is_known_release_v191():
    assert is_known_release("Paper Strategy Rule Tuning & Guardrail Lab v1.9.1") is True

def test_is_known_release_v190():
    assert is_known_release(
        "Paper Trading Performance Review & Strategy Improvement Lab v1.9.0") is True

def test_is_known_release_v189():
    assert is_known_release("Paper Decision Journal & Review Loop v1.8.9") is True

def test_is_known_release_v188():
    assert is_known_release("Paper Decision Workflow Runner v1.8.8") is True

def test_is_known_release_v170():
    assert is_known_release("Small Capital Strategy v1.7.0") is True

def test_is_known_release_unknown():
    assert is_known_release("Unknown Release v0.0.0") is False

def test_check_minimum_version_191():
    assert check_minimum_version("1.9.1") is True

def test_check_minimum_version_190():
    assert check_minimum_version("1.9.0") is True

def test_check_minimum_version_future():
    assert check_minimum_version("2.0.0") is False

def test_included_releases_contains_v191():
    assert "Paper Strategy Rule Tuning & Guardrail Lab v1.9.1" in INCLUDED_RELEASES

def test_included_releases_contains_v190():
    assert "Paper Trading Performance Review & Strategy Improvement Lab v1.9.0" in INCLUDED_RELEASES
