"""tests/test_strategy_sandbox_version_v192.py
Tests for strategy sandbox version metadata v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_sandbox_version_v192 import (
    VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
    SANDBOX_MODES, VALIDATION_DIMENSIONS,
    SANDBOX_APPROVAL_STATES, SANDBOX_RECOMMENDATIONS,
    FORBIDDEN_SANDBOX_ACTIONS, ALLOWED_SANDBOX_ACTIONS,
    HARD_BLOCK_CONDITIONS, INCLUDED_RELEASES, KNOWN_RELEASE_NAMES,
    verify_version, is_known_release, check_minimum_version,
    get_version_info, get_sandbox_modes, get_validation_dimensions,
    get_sandbox_approval_states, get_sandbox_recommendations,
    get_forbidden_sandbox_actions, get_allowed_sandbox_actions,
    get_hard_block_conditions,
)


# ── Version constants ─────────────────────────────────────────────────────────

def test_version_is_192():
    assert VERSION == "1.9.2"

def test_release_name_correct():
    assert RELEASE_NAME == "Paper Strategy Rule Sandbox & Shadow Validation Lab"

def test_schema_version_192():
    assert SCHEMA_VERSION == "192"

def test_policy_version_contains_192():
    assert "1.9.2" in POLICY_VERSION

def test_verify_version_returns_true():
    assert verify_version() is True

def test_verify_version_type_bool():
    assert isinstance(verify_version(), bool)


# ── Known releases / backward compat ─────────────────────────────────────────

def test_is_known_release_v192():
    assert is_known_release("Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2") is True

def test_is_known_release_v191():
    assert is_known_release("Paper Strategy Rule Tuning & Guardrail Lab v1.9.1") is True

def test_is_known_release_v170():
    assert is_known_release("Small Capital Strategy v1.7.0") is True

def test_is_known_release_unknown():
    assert is_known_release("Unknown Release v0.0.0") is False

def test_check_minimum_version_192():
    assert check_minimum_version("1.9.2") is True

def test_check_minimum_version_191():
    assert check_minimum_version("1.9.1") is True

def test_check_minimum_version_future():
    assert check_minimum_version("2.0.0") is False

def test_included_releases_contains_v192():
    assert "Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2" in INCLUDED_RELEASES

def test_included_releases_contains_v191():
    assert "Paper Strategy Rule Tuning & Guardrail Lab v1.9.1" in INCLUDED_RELEASES


# ── Sandbox modes ─────────────────────────────────────────────────────────────

def test_get_sandbox_modes_returns_list():
    assert isinstance(get_sandbox_modes(), list)

def test_get_sandbox_modes_count_11():
    assert len(get_sandbox_modes()) == 11

def test_sandbox_modes_has_shadow_compare():
    assert "SHADOW_COMPARE" in get_sandbox_modes()

def test_sandbox_modes_has_baseline_only():
    assert "BASELINE_ONLY" in get_sandbox_modes()

def test_sandbox_modes_has_full_ruleset_compare():
    assert "FULL_RULESET_COMPARE" in get_sandbox_modes()

def test_sandbox_modes_has_regression_only():
    assert "REGRESSION_ONLY" in get_sandbox_modes()

def test_sandbox_modes_has_a_b_rule_compare():
    assert "A_B_RULE_COMPARE" in get_sandbox_modes()


# ── Validation dimensions ─────────────────────────────────────────────────────

def test_get_validation_dimensions_count_20():
    assert len(get_validation_dimensions()) == 20

def test_get_validation_dimensions_returns_list():
    assert isinstance(get_validation_dimensions(), list)

def test_validation_dimensions_has_win_rate_delta():
    assert "win_rate_delta" in get_validation_dimensions()

def test_validation_dimensions_has_expectancy_delta_r():
    assert "expectancy_delta_r" in get_validation_dimensions()

def test_validation_dimensions_has_shadow_validation_score():
    assert "shadow_validation_score" in get_validation_dimensions()

def test_validation_dimensions_has_risk_reduction_score():
    assert "risk_reduction_score" in get_validation_dimensions()

def test_validation_dimensions_has_max_drawdown_delta_r():
    assert "max_drawdown_delta_r" in get_validation_dimensions()


# ── Sandbox approval states ───────────────────────────────────────────────────

def test_get_sandbox_approval_states_count_6():
    assert len(get_sandbox_approval_states()) == 6

def test_approval_states_has_shadow_only():
    assert "SHADOW_ONLY" in get_sandbox_approval_states()

def test_approval_states_has_paper_approved():
    assert "PAPER_APPROVED" in get_sandbox_approval_states()

def test_approval_states_has_blocked():
    assert "BLOCKED" in get_sandbox_approval_states()

def test_approval_states_has_regression_detected():
    assert "REGRESSION_DETECTED" in get_sandbox_approval_states()


# ── Sandbox recommendations ───────────────────────────────────────────────────

def test_get_sandbox_recommendations_count_13():
    assert len(get_sandbox_recommendations()) == 13

def test_recommendations_has_keep_baseline():
    assert "KEEP_BASELINE" in get_sandbox_recommendations()

def test_recommendations_has_accept_candidate_for_paper():
    assert "ACCEPT_CANDIDATE_FOR_PAPER" in get_sandbox_recommendations()

def test_recommendations_has_no_change():
    assert "NO_CHANGE" in get_sandbox_recommendations()

def test_recommendations_has_reject_candidate():
    assert "REJECT_CANDIDATE" in get_sandbox_recommendations()


# ── Forbidden / allowed sandbox actions ──────────────────────────────────────

def test_get_forbidden_sandbox_actions_count_9():
    assert len(get_forbidden_sandbox_actions()) == 9

def test_forbidden_actions_has_buy():
    assert "BUY" in get_forbidden_sandbox_actions()

def test_forbidden_actions_has_sell():
    assert "SELL" in get_forbidden_sandbox_actions()

def test_forbidden_actions_has_broker_order():
    assert "BROKER_ORDER" in get_forbidden_sandbox_actions()

def test_get_allowed_sandbox_actions_count_16():
    assert len(get_allowed_sandbox_actions()) == 16

def test_allowed_actions_has_sandbox_run():
    assert "SANDBOX_RUN" in get_allowed_sandbox_actions()

def test_allowed_actions_has_shadow_compare():
    assert "SHADOW_COMPARE" in get_allowed_sandbox_actions()

def test_allowed_actions_has_safety_audit():
    assert "SAFETY_AUDIT" in get_allowed_sandbox_actions()


# ── Hard block conditions ─────────────────────────────────────────────────────

def test_get_hard_block_conditions_count_17():
    assert len(get_hard_block_conditions()) == 17

def test_hard_block_has_real_order():
    assert "real_order_requested" in get_hard_block_conditions()

def test_hard_block_has_live_strategy_activation():
    assert "live_strategy_activation_attempted" in get_hard_block_conditions()

def test_hard_block_has_production_mutation():
    assert "production_strategy_mutation_attempted" in get_hard_block_conditions()

def test_hard_block_has_missing_baseline():
    assert "missing_baseline_strategy_snapshot" in get_hard_block_conditions()


# ── Version info dict ─────────────────────────────────────────────────────────

def test_get_version_info_returns_dict():
    assert isinstance(get_version_info(), dict)

def test_get_version_info_paper_only():
    assert get_version_info()["paper_only"] is True

def test_get_version_info_sandbox_only():
    assert get_version_info()["sandbox_only"] is True

def test_get_version_info_shadow_only():
    assert get_version_info()["shadow_only"] is True

def test_get_version_info_no_real_orders():
    assert get_version_info()["no_real_orders"] is True

def test_get_version_info_no_broker():
    assert get_version_info()["no_broker"] is True

def test_get_version_info_not_investment_advice():
    assert get_version_info()["not_investment_advice"] is True

def test_get_version_info_version_key():
    assert get_version_info()["version"] == "1.9.2"

def test_get_version_info_schema_version():
    assert get_version_info()["schema_version"] == "192"
