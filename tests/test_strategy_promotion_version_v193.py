"""tests/test_strategy_promotion_version_v193.py — v1.9.3 version metadata tests."""
import pytest
from paper_trading.small_capital_strategy.strategy_promotion_version_v193 import (
    VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION,
    INCLUDED_RELEASES, PROMOTION_APPROVAL_STATES, PROMOTION_RECOMMENDATIONS,
    ROLLBACK_TRIGGERS, FORBIDDEN_PROMOTION_ACTIONS, ALLOWED_PROMOTION_ACTIONS,
    HARD_BLOCK_CONDITIONS, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI,
    get_version_info, verify_version, is_known_release, check_minimum_version,
    get_promotion_approval_states, get_promotion_recommendations,
    get_rollback_triggers, get_forbidden_promotion_actions,
    get_allowed_promotion_actions, get_hard_block_conditions,
)


def test_version_is_193(): assert VERSION == "1.9.3"
def test_release_name(): assert RELEASE_NAME == "Paper Strategy Promotion Package & Rollback Plan Lab"
def test_schema_version(): assert SCHEMA_VERSION == "193"
def test_policy_version_contains_193(): assert "1.9.3" in POLICY_VERSION
def test_verify_version(): assert verify_version() is True
def test_version_info_is_dict(): assert isinstance(get_version_info(), dict)
def test_version_info_paper_only(): assert get_version_info()["paper_only"] is True
def test_version_info_research_only(): assert get_version_info()["research_only"] is True
def test_version_info_promotion_package_only(): assert get_version_info()["promotion_package_only"] is True
def test_version_info_rollback_plan_only(): assert get_version_info()["rollback_plan_only"] is True
def test_version_info_no_real_orders(): assert get_version_info()["no_real_orders"] is True
def test_version_info_no_broker(): assert get_version_info()["no_broker"] is True
def test_version_info_no_margin(): assert get_version_info()["no_margin"] is True
def test_version_info_no_leverage(): assert get_version_info()["no_leverage"] is True
def test_version_info_no_production_mutation(): assert get_version_info()["no_production_strategy_mutation"] is True
def test_version_info_no_live_activation(): assert get_version_info()["no_live_strategy_activation"] is True
def test_version_info_not_investment_advice(): assert get_version_info()["not_investment_advice"] is True
def test_version_info_demo_only(): assert get_version_info()["demo_only"] is True
def test_version_info_not_for_production(): assert get_version_info()["not_for_production"] is True
def test_version_info_production_trading_blocked(): assert get_version_info()["production_trading_blocked"] is True
def test_included_releases_is_list(): assert isinstance(INCLUDED_RELEASES, list)
def test_included_releases_has_v193(): assert "Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3" in INCLUDED_RELEASES
def test_included_releases_has_v192(): assert "Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2" in INCLUDED_RELEASES
def test_included_releases_has_v191(): assert "Paper Strategy Rule Tuning & Guardrail Lab v1.9.1" in INCLUDED_RELEASES
def test_included_releases_has_v190(): assert "Paper Trading Performance Review & Strategy Improvement Lab v1.9.0" in INCLUDED_RELEASES
def test_included_releases_count_at_least_23(): assert len(INCLUDED_RELEASES) >= 23
def test_approval_states_count(): assert len(get_promotion_approval_states()) == 8
def test_approval_states_has_draft(): assert "DRAFT" in get_promotion_approval_states()
def test_approval_states_has_paper_promotion_ready(): assert "PAPER_PROMOTION_READY" in get_promotion_approval_states()
def test_approval_states_has_shadow_only(): assert "SHADOW_ONLY" in get_promotion_approval_states()
def test_approval_states_has_review_required(): assert "REVIEW_REQUIRED" in get_promotion_approval_states()
def test_approval_states_has_blocked(): assert "BLOCKED" in get_promotion_approval_states()
def test_approval_states_has_regression_detected(): assert "REGRESSION_DETECTED" in get_promotion_approval_states()
def test_approval_states_has_rollback_required(): assert "ROLLBACK_REQUIRED" in get_promotion_approval_states()
def test_approval_states_has_invalid(): assert "INVALID" in get_promotion_approval_states()
def test_recommendations_count(): assert len(get_promotion_recommendations()) == 11
def test_recommendations_has_promote(): assert "PROMOTE_TO_PAPER_PACKAGE" in get_promotion_recommendations()
def test_recommendations_has_keep_baseline(): assert "KEEP_BASELINE" in get_promotion_recommendations()
def test_recommendations_has_rollback(): assert "ROLLBACK_TO_BASELINE" in get_promotion_recommendations()
def test_recommendations_has_split(): assert "SPLIT_PACKAGE" in get_promotion_recommendations()
def test_recommendations_has_no_change(): assert "NO_CHANGE" in get_promotion_recommendations()
def test_rollback_triggers_count(): assert len(get_rollback_triggers()) == 12
def test_rollback_triggers_has_win_rate(): assert "WIN_RATE_DETERIORATION" in get_rollback_triggers()
def test_rollback_triggers_has_drawdown(): assert "DRAWDOWN_INCREASED" in get_rollback_triggers()
def test_rollback_triggers_has_expectancy(): assert "EXPECTANCY_DETERIORATION" in get_rollback_triggers()
def test_rollback_triggers_has_safety_flag(): assert "SAFETY_FLAG_MISSING" in get_rollback_triggers()
def test_rollback_triggers_has_evidence_missing(): assert "EVIDENCE_MISSING" in get_rollback_triggers()
def test_forbidden_actions_count(): assert len(get_forbidden_promotion_actions()) == 9
def test_forbidden_buy(): assert "BUY" in get_forbidden_promotion_actions()
def test_forbidden_sell(): assert "SELL" in get_forbidden_promotion_actions()
def test_forbidden_order(): assert "ORDER" in get_forbidden_promotion_actions()
def test_forbidden_broker_order(): assert "BROKER_ORDER" in get_forbidden_promotion_actions()
def test_allowed_actions_count(): assert len(get_allowed_promotion_actions()) == 16
def test_allowed_review(): assert "REVIEW" in get_allowed_promotion_actions()
def test_allowed_promotion_build(): assert "PROMOTION_BUILD" in get_allowed_promotion_actions()
def test_allowed_rollback_plan(): assert "ROLLBACK_PLAN" in get_allowed_promotion_actions()
def test_hard_block_conditions_count(): assert len(get_hard_block_conditions()) == 19
def test_hard_block_has_real_order(): assert "real_order_requested" in get_hard_block_conditions()
def test_hard_block_has_missing_rollback(): assert "missing_rollback_plan" in get_hard_block_conditions()
def test_hard_block_has_forbidden_words(): assert "forbidden_action_words" in get_hard_block_conditions()
def test_min_scenarios(): assert MIN_SCENARIOS == 75
def test_min_fixtures(): assert MIN_FIXTURES == 75
def test_min_cli(): assert MIN_CLI == 18
def test_is_known_release_v193(): assert is_known_release("Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3") is True
def test_is_known_release_v192(): assert is_known_release("Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2") is True
def test_is_known_release_unknown(): assert is_known_release("Unknown Lab v0.0.0") is False
def test_check_minimum_version_193(): assert check_minimum_version("1.9.3") is True
def test_check_minimum_version_190(): assert check_minimum_version("1.9.0") is True
def test_approval_states_returns_list(): assert isinstance(get_promotion_approval_states(), list)
def test_recommendations_returns_list(): assert isinstance(get_promotion_recommendations(), list)
def test_rollback_triggers_returns_list(): assert isinstance(get_rollback_triggers(), list)
def test_forbidden_returns_list(): assert isinstance(get_forbidden_promotion_actions(), list)
def test_allowed_returns_list(): assert isinstance(get_allowed_promotion_actions(), list)
def test_hard_block_returns_list(): assert isinstance(get_hard_block_conditions(), list)
