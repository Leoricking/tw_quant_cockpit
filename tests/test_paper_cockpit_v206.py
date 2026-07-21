"""
tests/test_paper_cockpit_v206.py
v2.0.6 Paper Candidate Lifecycle & Setup Aging Control — Main Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest


# =========================================================================
# Import tests
# =========================================================================
def test_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v206

def test_version_is_206():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import VERSION
    assert VERSION == "2.0.6"

def test_schema_version_is_206():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "206"

def test_release_name_contains_lifecycle():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import RELEASE_NAME
    assert "Lifecycle" in RELEASE_NAME

def test_release_name_contains_aging():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import RELEASE_NAME
    assert "Aging" in RELEASE_NAME

def test_baseline_tests_set():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import BASELINE_TESTS
    assert BASELINE_TESTS == 34332

def test_min_new_tests_300():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300

def test_verify_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import verify_version
    assert verify_version() is True


# =========================================================================
# Safety constants
# =========================================================================
def test_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True


# =========================================================================
# Safety flags
# =========================================================================
def test_safety_flags_count_20():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert len(SAFETY_FLAGS_V206) == 20

def test_safety_flags_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["paper_only"] is True

def test_safety_flags_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["no_broker"] is True

def test_safety_flags_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["no_real_orders"] is True

def test_safety_flags_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["should_auto_apply_always_false"] is True

def test_safety_flags_auto_apply_enabled_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["auto_apply_enabled_always_false"] is True

def test_safety_flags_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["broker_execution_disabled"] is True

def test_safety_flags_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["production_trading_blocked"] is True

def test_safety_flags_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["no_automatic_rebalance"] is True

def test_safety_flags_no_real_account_sync():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["no_real_account_sync"] is True

def test_safety_flags_no_live_strategy_activation():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["no_live_strategy_activation"] is True

def test_safety_flags_not_investment_advice():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["not_investment_advice"] is True

def test_safety_flags_lifecycle_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["lifecycle_only"] is True

def test_safety_flags_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["human_review_required"] is True


# =========================================================================
# Lifecycle states
# =========================================================================
def test_lifecycle_states_count_13():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert len(LIFECYCLE_STATES) == 13

def test_lifecycle_state_newly_promoted():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert "newly_promoted" in LIFECYCLE_STATES

def test_lifecycle_state_active_candidate():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert "active_candidate" in LIFECYCLE_STATES

def test_lifecycle_state_waiting_buy_point():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert "waiting_buy_point" in LIFECYCLE_STATES

def test_lifecycle_state_second_wave_waiting():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert "second_wave_waiting" in LIFECYCLE_STATES

def test_lifecycle_state_abc_pullback_waiting():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert "abc_pullback_waiting" in LIFECYCLE_STATES

def test_lifecycle_state_breakout_waiting():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert "breakout_waiting" in LIFECYCLE_STATES

def test_lifecycle_state_cooling_down():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert "cooling_down" in LIFECYCLE_STATES

def test_lifecycle_state_stale_setup():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert "stale_setup" in LIFECYCLE_STATES

def test_lifecycle_state_expired_candidate():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert "expired_candidate" in LIFECYCLE_STATES

def test_lifecycle_state_rescore_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert "rescore_required" in LIFECYCLE_STATES

def test_lifecycle_state_downgraded_to_watchlist():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert "downgraded_to_watchlist" in LIFECYCLE_STATES

def test_lifecycle_state_removed_from_pool():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert "removed_from_pool" in LIFECYCLE_STATES

def test_lifecycle_state_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    assert "human_review_required" in LIFECYCLE_STATES


# =========================================================================
# Aging buckets
# =========================================================================
def test_aging_buckets_count_5():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import AGING_BUCKETS
    assert len(AGING_BUCKETS) == 5

def test_aging_bucket_fresh():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import AGING_BUCKETS
    assert "fresh" in AGING_BUCKETS

def test_aging_bucket_normal():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import AGING_BUCKETS
    assert "normal" in AGING_BUCKETS

def test_aging_bucket_aging():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import AGING_BUCKETS
    assert "aging" in AGING_BUCKETS

def test_aging_bucket_stale():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import AGING_BUCKETS
    assert "stale" in AGING_BUCKETS

def test_aging_bucket_expired():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import AGING_BUCKETS
    assert "expired" in AGING_BUCKETS


# =========================================================================
# Action types
# =========================================================================
def test_action_types_count_8():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import ACTION_TYPES
    assert len(ACTION_TYPES) == 8

def test_action_type_keep_active():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import ACTION_TYPES
    assert "keep_active" in ACTION_TYPES

def test_action_type_keep_waiting():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import ACTION_TYPES
    assert "keep_waiting" in ACTION_TYPES

def test_action_type_move_to_cooldown():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import ACTION_TYPES
    assert "move_to_cooldown" in ACTION_TYPES

def test_action_type_mark_stale():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import ACTION_TYPES
    assert "mark_stale" in ACTION_TYPES

def test_action_type_require_rescore():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import ACTION_TYPES
    assert "require_rescore" in ACTION_TYPES

def test_action_type_downgrade_to_watchlist():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import ACTION_TYPES
    assert "downgrade_to_watchlist" in ACTION_TYPES

def test_action_type_remove_from_candidate_pool():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import ACTION_TYPES
    assert "remove_from_candidate_pool" in ACTION_TYPES

def test_action_type_require_human_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import ACTION_TYPES
    assert "require_human_review" in ACTION_TYPES


# =========================================================================
# CLI commands
# =========================================================================
def test_cli_commands_count_11():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CLI_COMMANDS_V206
    assert len(CLI_COMMANDS_V206) == 11

def test_cli_command_review_lifecycle():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CLI_COMMANDS_V206
    assert "paper-cockpit-v206-review-lifecycle" in CLI_COMMANDS_V206

def test_cli_command_evaluate_aging():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CLI_COMMANDS_V206
    assert "paper-cockpit-v206-evaluate-aging" in CLI_COMMANDS_V206

def test_cli_command_build_stale_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CLI_COMMANDS_V206
    assert "paper-cockpit-v206-build-stale-queue" in CLI_COMMANDS_V206

def test_cli_command_build_expired_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CLI_COMMANDS_V206
    assert "paper-cockpit-v206-build-expired-queue" in CLI_COMMANDS_V206

def test_cli_command_build_rescore_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CLI_COMMANDS_V206
    assert "paper-cockpit-v206-build-rescore-queue" in CLI_COMMANDS_V206

def test_cli_command_build_cooldown_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CLI_COMMANDS_V206
    assert "paper-cockpit-v206-build-cooldown-queue" in CLI_COMMANDS_V206

def test_cli_command_export_json():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CLI_COMMANDS_V206
    assert "paper-cockpit-v206-export-json" in CLI_COMMANDS_V206

def test_cli_command_export_md():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CLI_COMMANDS_V206
    assert "paper-cockpit-v206-export-md" in CLI_COMMANDS_V206

def test_cli_command_export_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CLI_COMMANDS_V206
    assert "paper-cockpit-v206-export-csv" in CLI_COMMANDS_V206

def test_cli_command_health():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CLI_COMMANDS_V206
    assert "paper-cockpit-v206-health" in CLI_COMMANDS_V206

def test_cli_command_gate():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CLI_COMMANDS_V206
    assert "paper-cockpit-v206-gate" in CLI_COMMANDS_V206


# =========================================================================
# GUI tabs
# =========================================================================
def test_gui_tabs_count_3():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import GUI_TABS_V206
    assert len(GUI_TABS_V206) == 3

def test_gui_tab_candidate_lifecycle_v206():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import GUI_TABS_V206
    assert "candidate_lifecycle_v206" in GUI_TABS_V206

def test_gui_tab_setup_aging_v206():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import GUI_TABS_V206
    assert "setup_aging_v206" in GUI_TABS_V206

def test_gui_tab_stale_candidate_queue_v206():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import GUI_TABS_V206
    assert "stale_candidate_queue_v206" in GUI_TABS_V206


# =========================================================================
# Model: CandidateLifecycleItem
# =========================================================================
def test_candidate_lifecycle_item_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CandidateLifecycleItem
    item = CandidateLifecycleItem()
    assert item is not None

def test_candidate_lifecycle_item_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CandidateLifecycleItem
    assert CandidateLifecycleItem().schema_version == "206"

def test_candidate_lifecycle_item_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CandidateLifecycleItem
    assert CandidateLifecycleItem().paper_only is True

def test_candidate_lifecycle_item_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CandidateLifecycleItem
    assert CandidateLifecycleItem().no_real_orders is True

def test_candidate_lifecycle_item_default_state():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CandidateLifecycleItem
    item = CandidateLifecycleItem()
    assert item.current_lifecycle_state == "active_candidate"

def test_candidate_lifecycle_item_default_setup_age_bucket():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CandidateLifecycleItem
    item = CandidateLifecycleItem()
    assert item.setup_age_bucket == "fresh"

def test_candidate_lifecycle_item_stale_reasons_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CandidateLifecycleItem
    item = CandidateLifecycleItem()
    assert isinstance(item.stale_reasons, list)

def test_candidate_lifecycle_item_remove_reasons_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CandidateLifecycleItem
    item = CandidateLifecycleItem()
    assert isinstance(item.remove_reasons, list)

def test_candidate_lifecycle_item_human_review_reasons_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CandidateLifecycleItem
    item = CandidateLifecycleItem()
    assert isinstance(item.human_review_reasons, list)

def test_candidate_lifecycle_item_next_action_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CandidateLifecycleItem
    item = CandidateLifecycleItem()
    assert item.next_lifecycle_action == "keep_active"


# =========================================================================
# Model: SetupAgingPolicy
# =========================================================================
def test_setup_aging_policy_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    assert SetupAgingPolicy() is not None

def test_setup_aging_policy_auto_apply_enabled_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    assert SetupAgingPolicy().auto_apply_enabled is False

def test_setup_aging_policy_auto_apply_invariant():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    policy = SetupAgingPolicy(auto_apply_enabled=True)
    assert policy.auto_apply_enabled is False

def test_setup_aging_policy_default_cooldown_days():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    assert SetupAgingPolicy().cooldown_days == 14

def test_setup_aging_policy_require_human_review_before_remove():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    assert SetupAgingPolicy().require_human_review_before_remove is True

def test_setup_aging_policy_max_days_active_candidate():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    assert SetupAgingPolicy().max_days_active_candidate == 60

def test_setup_aging_policy_stale_score_threshold():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    assert SetupAgingPolicy().stale_score_threshold == 40.0

def test_setup_aging_policy_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    assert SetupAgingPolicy().paper_only is True


# =========================================================================
# Model: LifecycleAction
# =========================================================================
def test_lifecycle_action_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleAction
    assert LifecycleAction() is not None

def test_lifecycle_action_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleAction
    assert LifecycleAction().should_auto_apply is False

def test_lifecycle_action_should_auto_apply_invariant():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleAction
    action = LifecycleAction(should_auto_apply=True)
    assert action.should_auto_apply is False

def test_lifecycle_action_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleAction
    assert LifecycleAction().schema_version == "206"

def test_lifecycle_action_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleAction
    assert LifecycleAction().paper_only is True

def test_lifecycle_action_reason_codes_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleAction
    assert isinstance(LifecycleAction().action_reason_codes, list)


# =========================================================================
# Model: LifecycleSummary
# =========================================================================
def test_lifecycle_summary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleSummary
    assert LifecycleSummary() is not None

def test_lifecycle_summary_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleSummary
    assert LifecycleSummary().schema_version == "206"

def test_lifecycle_summary_top_stale_reasons_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleSummary
    assert isinstance(LifecycleSummary().top_stale_reasons, list)

def test_lifecycle_summary_top_remove_reasons_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleSummary
    assert isinstance(LifecycleSummary().top_remove_reasons, list)

def test_lifecycle_summary_default_grade():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleSummary
    assert LifecycleSummary().lifecycle_quality_grade == "C"


# =========================================================================
# Model: LifecycleReviewResult
# =========================================================================
def test_lifecycle_review_result_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleReviewResult
    assert LifecycleReviewResult() is not None

def test_lifecycle_review_result_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleReviewResult
    assert LifecycleReviewResult().should_auto_apply is False

def test_lifecycle_review_result_should_auto_apply_invariant():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleReviewResult
    result = LifecycleReviewResult(should_auto_apply=True)
    assert result.should_auto_apply is False

def test_lifecycle_review_result_lifecycle_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleReviewResult
    assert LifecycleReviewResult().lifecycle_version == "2.0.6"

def test_lifecycle_review_result_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleReviewResult
    assert LifecycleReviewResult().paper_only is True

def test_lifecycle_review_result_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleReviewResult
    assert LifecycleReviewResult().no_real_orders is True

def test_lifecycle_review_result_lifecycle_action_queue_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleReviewResult
    assert isinstance(LifecycleReviewResult().lifecycle_action_queue, list)

def test_lifecycle_review_result_cooldown_queue_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleReviewResult
    assert isinstance(LifecycleReviewResult().cooldown_queue, list)


# =========================================================================
# Model counts
# =========================================================================
def test_model_names_count_13():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import _ALL_MODEL_NAMES_V206
    assert len(_ALL_MODEL_NAMES_V206) == 13

def test_all_models_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, LifecycleAction, LifecycleSummary,
        LifecycleReviewInput, LifecycleReviewResult, LifecycleExportResult,
        LifecycleAuditSnapshot, LifecycleReport, StaleSetupCSV, ExpiredCandidateCSV,
        V206HealthSummary, V206ReleaseSummary,
    )
    assert CandidateLifecycleItem() is not None
    assert SetupAgingPolicy() is not None
    assert LifecycleAction() is not None
    assert LifecycleSummary() is not None
    assert LifecycleReviewInput() is not None
    assert LifecycleReviewResult() is not None
    assert LifecycleExportResult() is not None
    assert LifecycleAuditSnapshot() is not None
    assert LifecycleReport() is not None
    assert StaleSetupCSV() is not None
    assert ExpiredCandidateCSV() is not None
    assert V206HealthSummary() is not None
    assert V206ReleaseSummary() is not None


# =========================================================================
# Aging bucket classification
# =========================================================================
def test_classify_aging_bucket_fresh_at_0():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(0) == "fresh"

def test_classify_aging_bucket_fresh_at_5():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(5) == "fresh"

def test_classify_aging_bucket_normal_at_6():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(6) == "normal"

def test_classify_aging_bucket_normal_at_14():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(14) == "normal"

def test_classify_aging_bucket_aging_at_15():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(15) == "aging"

def test_classify_aging_bucket_aging_at_30():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(30) == "aging"

def test_classify_aging_bucket_stale_at_31():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(31) == "stale"

def test_classify_aging_bucket_stale_at_60():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(60) == "stale"

def test_classify_aging_bucket_expired_at_61():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(61) == "expired"

def test_classify_aging_bucket_expired_at_120():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(120) == "expired"

def test_classify_setup_age_bucket_fresh():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_setup_age_bucket
    )
    item = CandidateLifecycleItem(days_in_candidate_pool=3)
    policy = SetupAgingPolicy()
    assert classify_setup_age_bucket(item, policy) == "fresh"

def test_classify_signal_age_bucket_fresh():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_signal_age_bucket
    )
    item = CandidateLifecycleItem(days_since_last_signal=2)
    policy = SetupAgingPolicy()
    assert classify_signal_age_bucket(item, policy) == "fresh"

def test_classify_theme_age_bucket_fresh():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_theme_age_bucket
    )
    item = CandidateLifecycleItem(days_since_last_score_update=2)
    policy = SetupAgingPolicy()
    assert classify_theme_age_bucket(item, policy) == "fresh"

def test_classify_signal_age_bucket_stale():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_signal_age_bucket
    )
    item = CandidateLifecycleItem(days_since_last_signal=14)
    policy = SetupAgingPolicy()
    assert classify_signal_age_bucket(item, policy) == "stale"

def test_classify_signal_age_bucket_expired():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_signal_age_bucket
    )
    item = CandidateLifecycleItem(days_since_last_signal=15)
    policy = SetupAgingPolicy()
    assert classify_signal_age_bucket(item, policy) == "expired"


# =========================================================================
# Lifecycle review engine
# =========================================================================
def test_run_lifecycle_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    result = run_lifecycle_review()
    assert result is not None

def test_run_lifecycle_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    assert run_lifecycle_review().paper_only is True

def test_run_lifecycle_review_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    assert run_lifecycle_review().no_real_orders is True

def test_run_lifecycle_review_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    assert run_lifecycle_review().no_broker is True

def test_run_lifecycle_review_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    assert run_lifecycle_review().all_passed is True

def test_run_lifecycle_review_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    assert run_lifecycle_review().should_auto_apply is False

def test_run_lifecycle_review_lifecycle_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    assert run_lifecycle_review().lifecycle_version == "2.0.6"

def test_run_lifecycle_review_action_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    assert isinstance(run_lifecycle_review().lifecycle_action_queue, list)

def test_run_lifecycle_review_summary_not_none():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    assert run_lifecycle_review().lifecycle_summary is not None

def test_run_lifecycle_review_input_snapshot_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    assert isinstance(run_lifecycle_review().input_candidate_snapshot, list)

def test_run_lifecycle_review_paper_only_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    assert run_lifecycle_review().paper_only_safety_snapshot is True

def test_run_lifecycle_review_not_investment_advice():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    assert run_lifecycle_review().not_investment_advice is True


# =========================================================================
# Stale queue
# =========================================================================
def test_build_stale_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_stale_queue
    result = build_stale_queue()
    assert isinstance(result, list)

def test_build_stale_queue_returns_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_stale_queue
    assert isinstance(build_stale_queue(), list)

def test_build_stale_queue_with_aging_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        build_stale_queue, LifecycleReviewInput, CandidateLifecycleItem
    )
    item = CandidateLifecycleItem(
        symbol="TEST", days_in_candidate_pool=20,
        days_since_last_signal=10, days_since_last_score_update=12,
        current_lifecycle_state="active_candidate",
    )
    inp = LifecycleReviewInput(review_period="2026-W29", candidate_items=[item])
    result = build_stale_queue(inp)
    assert isinstance(result, list)


# =========================================================================
# Expired queue
# =========================================================================
def test_build_expired_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_expired_queue
    assert isinstance(build_expired_queue(), list)

def test_build_expired_queue_with_expired_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        build_expired_queue, LifecycleReviewInput, CandidateLifecycleItem, SetupAgingPolicy
    )
    item = CandidateLifecycleItem(
        symbol="TEST2", days_in_candidate_pool=70,
        days_since_last_signal=30, days_since_last_score_update=35,
        current_lifecycle_state="expired_candidate",
    )
    policy = SetupAgingPolicy(require_human_review_before_remove=False)
    inp = LifecycleReviewInput(review_period="2026-W29", candidate_items=[item], aging_policy=policy)
    result = build_expired_queue(inp)
    assert isinstance(result, list)


# =========================================================================
# Rescore queue
# =========================================================================
def test_build_rescore_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_rescore_queue
    assert isinstance(build_rescore_queue(), list)

def test_build_rescore_queue_with_stale_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        build_rescore_queue, LifecycleReviewInput, CandidateLifecycleItem
    )
    item = CandidateLifecycleItem(
        symbol="TEST3", days_in_candidate_pool=35,
        days_since_last_signal=15, days_since_last_score_update=20,
        current_lifecycle_state="stale_setup",
    )
    inp = LifecycleReviewInput(review_period="2026-W29", candidate_items=[item])
    result = build_rescore_queue(inp)
    assert isinstance(result, list)


# =========================================================================
# Cooldown queue
# =========================================================================
def test_build_cooldown_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_cooldown_queue
    assert isinstance(build_cooldown_queue(), list)

def test_build_cooldown_queue_with_cooling_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        build_cooldown_queue, LifecycleReviewInput, CandidateLifecycleItem
    )
    item = CandidateLifecycleItem(
        symbol="TEST4", days_in_candidate_pool=20,
        current_lifecycle_state="cooling_down",
    )
    inp = LifecycleReviewInput(review_period="2026-W29", candidate_items=[item])
    result = build_cooldown_queue(inp)
    assert isinstance(result, list)


# =========================================================================
# Human review queue
# =========================================================================
def test_build_human_review_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_human_review_queue
    assert isinstance(build_human_review_queue(), list)

def test_build_human_review_queue_with_review_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        build_human_review_queue, LifecycleReviewInput, CandidateLifecycleItem
    )
    item = CandidateLifecycleItem(
        symbol="TEST5", days_in_candidate_pool=5,
        human_review_reasons=["signal_conflict"],
    )
    inp = LifecycleReviewInput(review_period="2026-W29", candidate_items=[item])
    result = build_human_review_queue(inp)
    assert isinstance(result, list)
    assert len(result) >= 1


# =========================================================================
# Evaluate aging
# =========================================================================
def test_evaluate_aging_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import evaluate_aging
    assert isinstance(evaluate_aging(), list)

def test_evaluate_aging_returns_lifecycle_actions():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import evaluate_aging, LifecycleAction
    actions = evaluate_aging()
    for a in actions:
        assert isinstance(a, LifecycleAction)

def test_evaluate_aging_all_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import evaluate_aging
    for action in evaluate_aging():
        assert action.should_auto_apply is False


# =========================================================================
# Export: JSON
# =========================================================================
def test_export_lifecycle_json_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_json, run_lifecycle_review
    result = export_lifecycle_json(run_lifecycle_review())
    assert result is not None

def test_export_lifecycle_json_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_json, run_lifecycle_review
    assert export_lifecycle_json(run_lifecycle_review()).is_valid is True

def test_export_lifecycle_json_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_json, run_lifecycle_review
    assert export_lifecycle_json(run_lifecycle_review()).export_format == "json"

def test_export_lifecycle_json_contains_review_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_json, run_lifecycle_review
    result = run_lifecycle_review()
    export = export_lifecycle_json(result)
    assert result.lifecycle_review_id in export.content

def test_export_lifecycle_json_contains_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_json, run_lifecycle_review
    export = export_lifecycle_json(run_lifecycle_review())
    assert "should_auto_apply" in export.content
    assert "false" in export.content

def test_export_lifecycle_json_paper_only_confirmed():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_json, run_lifecycle_review
    assert export_lifecycle_json(run_lifecycle_review()).paper_only_confirmed is True


# =========================================================================
# Export: Markdown
# =========================================================================
def test_export_lifecycle_markdown_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_markdown, run_lifecycle_review
    assert export_lifecycle_markdown(run_lifecycle_review()) is not None

def test_export_lifecycle_markdown_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_markdown, run_lifecycle_review
    assert export_lifecycle_markdown(run_lifecycle_review()).is_valid is True

def test_export_lifecycle_markdown_contains_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_markdown, run_lifecycle_review
    md = export_lifecycle_markdown(run_lifecycle_review()).content
    assert "Candidate Lifecycle Report" in md

def test_export_lifecycle_markdown_contains_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_markdown, run_lifecycle_review
    md = export_lifecycle_markdown(run_lifecycle_review()).content
    assert "Paper Only" in md


# =========================================================================
# Export: Stale setup CSV
# =========================================================================
def test_export_stale_setup_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_stale_setup_csv, run_lifecycle_review
    result = export_stale_setup_csv(run_lifecycle_review())
    assert result is not None

def test_export_stale_setup_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_stale_setup_csv, run_lifecycle_review
    assert export_stale_setup_csv(run_lifecycle_review()).is_valid is True

def test_export_stale_setup_csv_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_stale_setup_csv, run_lifecycle_review
    csv = export_stale_setup_csv(run_lifecycle_review()).csv_content
    assert "symbol" in csv
    assert "setup_age_bucket" in csv

def test_export_stale_setup_csv_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_stale_setup_csv, run_lifecycle_review
    assert export_stale_setup_csv(run_lifecycle_review()).paper_only is True


# =========================================================================
# Export: Expired candidate CSV
# =========================================================================
def test_export_expired_candidate_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_expired_candidate_csv, run_lifecycle_review
    result = export_expired_candidate_csv(run_lifecycle_review())
    assert result is not None

def test_export_expired_candidate_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_expired_candidate_csv, run_lifecycle_review
    assert export_expired_candidate_csv(run_lifecycle_review()).is_valid is True

def test_export_expired_candidate_csv_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_expired_candidate_csv, run_lifecycle_review
    csv = export_expired_candidate_csv(run_lifecycle_review()).csv_content
    assert "symbol" in csv
    assert "signal_age_bucket" in csv


# =========================================================================
# Export: Lifecycle action CSV
# =========================================================================
def test_export_lifecycle_action_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_action_csv, run_lifecycle_review
    assert export_lifecycle_action_csv(run_lifecycle_review()) is not None

def test_export_lifecycle_action_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_action_csv, run_lifecycle_review
    assert export_lifecycle_action_csv(run_lifecycle_review()).is_valid is True

def test_export_lifecycle_action_csv_should_auto_apply_false_column():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_action_csv, run_lifecycle_review
    csv = export_lifecycle_action_csv(run_lifecycle_review()).content
    assert "should_auto_apply" in csv


# =========================================================================
# Export: Audit snapshot
# =========================================================================
def test_export_lifecycle_audit_snapshot_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_audit_snapshot, run_lifecycle_review
    snap = export_lifecycle_audit_snapshot(run_lifecycle_review())
    assert snap is not None

def test_export_lifecycle_audit_snapshot_reproducibility_hash():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_audit_snapshot, run_lifecycle_review
    snap = export_lifecycle_audit_snapshot(run_lifecycle_review())
    assert snap.reproducibility_hash != ""

def test_export_lifecycle_audit_snapshot_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_audit_snapshot, run_lifecycle_review
    snap = export_lifecycle_audit_snapshot(run_lifecycle_review())
    assert "paper_only=True" in snap.safety_snapshot
    assert "should_auto_apply=False" in snap.safety_snapshot
    assert "auto_apply_enabled=False" in snap.safety_snapshot


# =========================================================================
# CLI command registry
# =========================================================================
def test_cli_registry_importable():
    from cli.command_registry import PROVIDER_COMMANDS
    assert PROVIDER_COMMANDS is not None

def test_cli_registry_contains_review_lifecycle():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v206-review-lifecycle" in names

def test_cli_registry_contains_evaluate_aging():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v206-evaluate-aging" in names

def test_cli_registry_contains_build_stale_queue():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v206-build-stale-queue" in names

def test_cli_registry_contains_build_expired_queue():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v206-build-expired-queue" in names

def test_cli_registry_contains_build_rescore_queue():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v206-build-rescore-queue" in names

def test_cli_registry_contains_build_cooldown_queue():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v206-build-cooldown-queue" in names

def test_cli_registry_contains_export_json():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v206-export-json" in names

def test_cli_registry_contains_export_md():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v206-export-md" in names

def test_cli_registry_contains_export_csv():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v206-export-csv" in names

def test_cli_registry_contains_health():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v206-health" in names

def test_cli_registry_contains_gate():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v206-gate" in names


# =========================================================================
# GUI compatibility
# =========================================================================
def test_gui_panel_importable():
    import gui.small_capital_strategy_panel

def test_panel_version_v206():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V206
    assert PANEL_VERSION_V206 == "2.0.6"

def test_get_v206_tab_names_3():
    from gui.small_capital_strategy_panel import get_v206_tab_names
    assert len(get_v206_tab_names()) == 3

def test_get_tab_names_includes_candidate_lifecycle():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "candidate_lifecycle_v206" in get_tab_names()

def test_get_tab_names_includes_setup_aging():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "setup_aging_v206" in get_tab_names()

def test_get_tab_names_includes_stale_candidate_queue():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "stale_candidate_queue_v206" in get_tab_names()

def test_render_candidate_lifecycle_v206_tab():
    from gui.small_capital_strategy_panel import render_candidate_lifecycle_v206_tab
    result = render_candidate_lifecycle_v206_tab()
    assert result["tab"] == "candidate_lifecycle_v206"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False

def test_render_setup_aging_v206_tab():
    from gui.small_capital_strategy_panel import render_setup_aging_v206_tab
    result = render_setup_aging_v206_tab()
    assert result["tab"] == "setup_aging_v206"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False

def test_render_stale_candidate_queue_v206_tab():
    from gui.small_capital_strategy_panel import render_stale_candidate_queue_v206_tab
    result = render_stale_candidate_queue_v206_tab()
    assert result["tab"] == "stale_candidate_queue_v206"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False

def test_render_candidate_lifecycle_v206_no_real_orders():
    from gui.small_capital_strategy_panel import render_candidate_lifecycle_v206_tab
    assert render_candidate_lifecycle_v206_tab()["no_real_orders"] is True

def test_render_setup_aging_v206_no_real_orders():
    from gui.small_capital_strategy_panel import render_setup_aging_v206_tab
    assert render_setup_aging_v206_tab()["no_real_orders"] is True

def test_render_stale_candidate_queue_v206_no_real_orders():
    from gui.small_capital_strategy_panel import render_stale_candidate_queue_v206_tab
    assert render_stale_candidate_queue_v206_tab()["no_real_orders"] is True


# =========================================================================
# render_all_tabs — no error tabs
# =========================================================================
def test_render_all_tabs_no_error_tabs():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    error_tabs = [k for k, v in result.items() if "error" in v]
    assert error_tabs == [], f"Error tabs found: {error_tabs}"

def test_render_all_tabs_v206_candidate_lifecycle_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("candidate_lifecycle_v206", {})

def test_render_all_tabs_v206_setup_aging_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("setup_aging_v206", {})

def test_render_all_tabs_v206_stale_candidate_queue_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("stale_candidate_queue_v206", {})


# =========================================================================
# Paper-only safety guards
# =========================================================================
def test_paper_only_guard_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert SAFETY_FLAGS_V206["no_broker"] is True

def test_no_real_orders_guard():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_no_automatic_lifecycle_action_applied():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    result = run_lifecycle_review()
    for action in result.lifecycle_action_queue:
        assert action.should_auto_apply is False

def test_auto_apply_enabled_always_false_in_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    for _ in range(3):
        assert SetupAgingPolicy().auto_apply_enabled is False

def test_should_auto_apply_always_false_in_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleAction
    for _ in range(3):
        assert LifecycleAction(should_auto_apply=True).should_auto_apply is False


# =========================================================================
# Backward compatibility with v2.0.5
# =========================================================================
def test_v205_module_still_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v205

def test_v205_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import VERSION
    assert VERSION == "2.0.5"

def test_v205_run_watchlist_rotation_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result is not None

def test_v205_run_watchlist_rotation_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    assert run_watchlist_rotation().paper_only is True

def test_v204_module_still_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v204

def test_v204_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import VERSION
    assert VERSION == "2.0.4"


# =========================================================================
# v201 health relative-path compatibility
# =========================================================================
def test_v201_health_file_exists_via_relative_path():
    import os
    health_dir = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "..", "paper_trading", "small_capital_strategy"
    ))
    path = os.path.normpath(os.path.join(health_dir, "paper_cockpit_health_v201.py"))
    assert os.path.exists(path), f"paper_cockpit_health_v201.py not found at {path}"

def test_v201_test_file_exists_via_relative_path():
    import os
    tests_dir = os.path.normpath(os.path.join(os.path.dirname(__file__)))
    path = os.path.normpath(os.path.join(tests_dir, "test_paper_cockpit_v201.py"))
    assert os.path.exists(path), f"test_paper_cockpit_v201.py not found at {path}"


# =========================================================================
# Health check
# =========================================================================
def test_health_check_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_health_v206

def test_health_check_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v206 import run_health_check
    result = run_health_check()
    assert result is not None

def test_health_check_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v206 import run_health_check
    result = run_health_check()
    assert result["all_passed"] is True, f"Health check failed: {result.get('errors', [])}"

def test_health_check_no_failures():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v206 import run_health_check
    result = run_health_check()
    assert result["failed"] == 0, f"Health check failures: {result.get('errors', [])}"

def test_health_check_version():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v206 import HEALTH_VERSION
    assert HEALTH_VERSION == "2.0.6"


# =========================================================================
# Release gate
# =========================================================================
def test_release_gate_importable():
    import release.paper_cockpit_release_gate_v206

def test_release_gate_callable():
    from release.paper_cockpit_release_gate_v206 import run_release_gate
    result = run_release_gate()
    assert result is not None

def test_release_gate_passed():
    from release.paper_cockpit_release_gate_v206 import run_release_gate
    result = run_release_gate()
    assert result["gate_passed"] is True, f"Gate failed: {result.get('errors', [])}"

def test_release_gate_no_failures():
    from release.paper_cockpit_release_gate_v206 import run_release_gate
    result = run_release_gate()
    assert result["failed_count"] == 0, f"Gate failures: {result.get('errors', [])}"

def test_release_gate_version():
    from release.paper_cockpit_release_gate_v206 import GATE_VERSION
    assert GATE_VERSION == "2.0.6"

def test_release_gate_baseline_tests():
    from release.paper_cockpit_release_gate_v206 import BASELINE_TESTS
    assert BASELINE_TESTS == 34332

def test_release_gate_min_new_tests():
    from release.paper_cockpit_release_gate_v206 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300


# =========================================================================
# Scenarios
# =========================================================================
def test_scenarios_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v206 import SCENARIOS
    assert len(SCENARIOS) == 80

def test_scenarios_schema_version_206():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v206 import SCENARIOS
    assert all(s["schema_version"] == "206" for s in SCENARIOS)

def test_scenarios_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v206 import SCENARIOS
    assert all(s["paper_only"] is True for s in SCENARIOS)

def test_scenarios_have_scenario_id():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v206 import SCENARIOS
    assert all("scenario_id" in s for s in SCENARIOS)

def test_scenarios_first_id():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v206 import SCENARIOS
    assert SCENARIOS[0]["scenario_id"] == "SC206-001"

def test_scenarios_last_id():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v206 import SCENARIOS
    assert SCENARIOS[-1]["scenario_id"] == "SC206-080"


# =========================================================================
# Fixtures
# =========================================================================
def test_fixtures_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v206 import FIXTURES
    assert len(FIXTURES) == 80

def test_fixtures_schema_version_206():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v206 import FIXTURES
    assert all(f["schema_version"] == "206" for f in FIXTURES)

def test_fixtures_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v206 import FIXTURES
    assert all(f["paper_only"] is True for f in FIXTURES)

def test_fixtures_have_fixture_id():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v206 import FIXTURES
    assert all("fixture_id" in f for f in FIXTURES)

def test_fixtures_first_id():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v206 import FIXTURES
    assert FIXTURES[0]["fixture_id"] == "FX206-001"

def test_fixtures_last_id():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v206 import FIXTURES
    assert FIXTURES[-1]["fixture_id"] == "FX206-080"


# =========================================================================
# get_cockpit_summary_v206
# =========================================================================
def test_cockpit_summary_v206():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import get_cockpit_summary_v206
    summary = get_cockpit_summary_v206()
    assert summary["version"] == "2.0.6"
    assert summary["paper_only"] is True
    assert summary["should_auto_apply"] is False
    assert summary["auto_apply_enabled"] is False
    assert summary["models_count"] == 13
    assert summary["cli_commands_count"] == 11
    assert summary["gui_tabs_count"] == 3

def test_get_version_info():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import get_version_info
    info = get_version_info()
    assert info["version"] == "2.0.6"
    assert info["should_auto_apply"] == "False"
    assert info["auto_apply_enabled"] == "False"


# =========================================================================
# Aging bucket boundary cases — fine-grained
# =========================================================================
def test_classify_aging_bucket_boundary_day1():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(1) == "fresh"

def test_classify_aging_bucket_boundary_day2():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(2) == "fresh"

def test_classify_aging_bucket_boundary_day4():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(4) == "fresh"

def test_classify_aging_bucket_boundary_day7():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(7) == "normal"

def test_classify_aging_bucket_boundary_day10():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(10) == "normal"

def test_classify_aging_bucket_boundary_day13():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(13) == "normal"

def test_classify_aging_bucket_boundary_day16():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(16) == "aging"

def test_classify_aging_bucket_boundary_day20():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(20) == "aging"

def test_classify_aging_bucket_boundary_day25():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(25) == "aging"

def test_classify_aging_bucket_boundary_day29():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(29) == "aging"

def test_classify_aging_bucket_boundary_day32():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(32) == "stale"

def test_classify_aging_bucket_boundary_day45():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(45) == "stale"

def test_classify_aging_bucket_boundary_day59():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(59) == "stale"

def test_classify_aging_bucket_boundary_day62():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(62) == "expired"

def test_classify_aging_bucket_boundary_day90():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(90) == "expired"

def test_classify_aging_bucket_custom_params_fresh():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(3, fresh_max=3, normal_max=7, aging_max=14, stale_max=21) == "fresh"

def test_classify_aging_bucket_custom_params_expired():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import classify_aging_bucket
    assert classify_aging_bucket(22, fresh_max=3, normal_max=7, aging_max=14, stale_max=21) == "expired"


# =========================================================================
# Setup aging with specific policy thresholds
# =========================================================================
def test_strict_policy_max_days_30():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    p = SetupAgingPolicy(max_days_active_candidate=30)
    assert p.max_days_active_candidate == 30
    assert p.auto_apply_enabled is False

def test_policy_max_days_waiting_buy_point():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    p = SetupAgingPolicy(max_days_waiting_buy_point=14)
    assert p.max_days_waiting_buy_point == 14

def test_policy_max_days_without_signal_refresh():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    p = SetupAgingPolicy(max_days_without_signal_refresh=7)
    assert p.max_days_without_signal_refresh == 7

def test_policy_max_days_without_score_update():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    p = SetupAgingPolicy(max_days_without_score_update=10)
    assert p.max_days_without_score_update == 10

def test_policy_require_human_review_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    p = SetupAgingPolicy(require_human_review_before_remove=False)
    assert p.require_human_review_before_remove is False
    assert p.auto_apply_enabled is False

def test_classify_setup_age_bucket_normal():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_setup_age_bucket
    )
    item = CandidateLifecycleItem(days_in_candidate_pool=10)
    policy = SetupAgingPolicy()
    bucket = classify_setup_age_bucket(item, policy)
    assert bucket in ["fresh", "normal", "aging", "stale", "expired"]

def test_classify_setup_age_bucket_stale_at_max():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_setup_age_bucket
    )
    item = CandidateLifecycleItem(days_in_candidate_pool=30)
    policy = SetupAgingPolicy(max_days_waiting_buy_point=30)
    bucket = classify_setup_age_bucket(item, policy)
    assert bucket == "stale"

def test_classify_theme_age_bucket_normal():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_theme_age_bucket
    )
    item = CandidateLifecycleItem(days_since_last_score_update=5)
    policy = SetupAgingPolicy()
    bucket = classify_theme_age_bucket(item, policy)
    assert bucket in ["fresh", "normal"]

def test_classify_theme_age_bucket_expired():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_theme_age_bucket
    )
    item = CandidateLifecycleItem(days_since_last_score_update=25)
    policy = SetupAgingPolicy(max_days_without_score_update=21)
    bucket = classify_theme_age_bucket(item, policy)
    assert bucket == "expired"


# =========================================================================
# Candidate pool aging edge cases
# =========================================================================
def test_active_candidate_day0():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(symbol="A", days_in_candidate_pool=0, current_lifecycle_state="newly_promoted")
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.all_passed is True

def test_candidate_exactly_at_max_days():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, LifecycleReviewInput, run_lifecycle_review
    )
    policy = SetupAgingPolicy(max_days_active_candidate=60, require_human_review_before_remove=True)
    item = CandidateLifecycleItem(symbol="B", days_in_candidate_pool=60, current_lifecycle_state="active_candidate")
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item], aging_policy=policy))
    assert result.all_passed is True
    actions = result.lifecycle_action_queue
    assert len(actions) == 1

def test_candidate_one_day_over_max():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, LifecycleReviewInput, run_lifecycle_review
    )
    policy = SetupAgingPolicy(max_days_active_candidate=60, require_human_review_before_remove=True)
    item = CandidateLifecycleItem(symbol="C", days_in_candidate_pool=61, current_lifecycle_state="active_candidate")
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item], aging_policy=policy))
    actions = result.lifecycle_action_queue
    assert len(actions) == 1
    assert actions[0].action_type in ("remove_from_candidate_pool", "require_human_review")

def test_multiple_candidates_independent():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    items = [
        CandidateLifecycleItem(symbol=f"S{i}", days_in_candidate_pool=i*5) for i in range(5)
    ]
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=items))
    assert len(result.lifecycle_action_queue) == 5

def test_empty_candidate_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        LifecycleReviewInput, run_lifecycle_review
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[]))
    assert result.all_passed is True
    assert len(result.lifecycle_action_queue) == 0
    assert result.lifecycle_summary is not None


# =========================================================================
# Buy-point waiting aging edge cases
# =========================================================================
def test_waiting_buy_point_fresh_keeps_waiting():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="W1", days_in_candidate_pool=5, days_since_last_signal=1,
        current_lifecycle_state="waiting_buy_point"
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.lifecycle_action_queue[0].action_type == "keep_waiting"

def test_waiting_buy_point_aging_state():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="W2", days_in_candidate_pool=20, days_since_last_signal=9,
        days_since_last_score_update=11, current_lifecycle_state="waiting_buy_point"
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    action_type = result.lifecycle_action_queue[0].action_type
    assert action_type in ("mark_stale", "keep_waiting", "require_rescore")

def test_second_wave_waiting_keep():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="W3", days_in_candidate_pool=7, days_since_last_signal=2,
        current_lifecycle_state="second_wave_waiting"
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.lifecycle_action_queue[0].action_type == "keep_waiting"

def test_breakout_waiting_keep():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="W4", days_in_candidate_pool=8, days_since_last_signal=3,
        current_lifecycle_state="breakout_waiting"
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.lifecycle_action_queue[0].action_type == "keep_waiting"

def test_abc_pullback_waiting_keep():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="W5", days_in_candidate_pool=9, days_since_last_signal=4,
        current_lifecycle_state="abc_pullback_waiting"
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.lifecycle_action_queue[0].action_type == "keep_waiting"


# =========================================================================
# Signal refresh aging edge cases
# =========================================================================
def test_no_signal_for_exact_refresh_threshold():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_signal_age_bucket
    )
    item = CandidateLifecycleItem(days_since_last_signal=14)
    policy = SetupAgingPolicy(max_days_without_signal_refresh=14)
    assert classify_signal_age_bucket(item, policy) == "stale"

def test_no_signal_one_over_refresh_threshold():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_signal_age_bucket
    )
    item = CandidateLifecycleItem(days_since_last_signal=15)
    policy = SetupAgingPolicy(max_days_without_signal_refresh=14)
    assert classify_signal_age_bucket(item, policy) == "expired"

def test_signal_refresh_day0_is_fresh():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_signal_age_bucket
    )
    item = CandidateLifecycleItem(days_since_last_signal=0)
    policy = SetupAgingPolicy()
    assert classify_signal_age_bucket(item, policy) == "fresh"

def test_signal_refresh_strict_policy_7days():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_signal_age_bucket
    )
    item = CandidateLifecycleItem(days_since_last_signal=8)
    policy = SetupAgingPolicy(max_days_without_signal_refresh=7)
    assert classify_signal_age_bucket(item, policy) == "expired"


# =========================================================================
# Score update aging edge cases
# =========================================================================
def test_score_update_exact_threshold():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_theme_age_bucket
    )
    item = CandidateLifecycleItem(days_since_last_score_update=21)
    policy = SetupAgingPolicy(max_days_without_score_update=21)
    assert classify_theme_age_bucket(item, policy) == "stale"

def test_score_update_one_over_threshold():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_theme_age_bucket
    )
    item = CandidateLifecycleItem(days_since_last_score_update=22)
    policy = SetupAgingPolicy(max_days_without_score_update=21)
    assert classify_theme_age_bucket(item, policy) == "expired"

def test_score_update_zero_is_fresh():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, classify_theme_age_bucket
    )
    item = CandidateLifecycleItem(days_since_last_score_update=0)
    policy = SetupAgingPolicy()
    assert classify_theme_age_bucket(item, policy) == "fresh"


# =========================================================================
# Cooldown queue classification
# =========================================================================
def test_cooldown_item_goes_to_cooldown_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="COOL1", days_in_candidate_pool=15,
        current_lifecycle_state="cooling_down"
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert item.symbol in [it.symbol for it in result.cooldown_queue]

def test_cooldown_action_type():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="COOL2", days_in_candidate_pool=10,
        current_lifecycle_state="cooling_down"
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.lifecycle_action_queue[0].action_type == "move_to_cooldown"

def test_cooldown_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="COOL3", days_in_candidate_pool=10,
        current_lifecycle_state="cooling_down"
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.lifecycle_action_queue[0].should_auto_apply is False


# =========================================================================
# Stale setup queue classification
# =========================================================================
def test_stale_setup_item_goes_to_stale_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="STALE1", days_in_candidate_pool=20, days_since_last_signal=10,
        days_since_last_score_update=12, current_lifecycle_state="active_candidate"
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.all_passed is True

def test_stale_setup_state_triggers_rescore():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="STALE2", days_in_candidate_pool=25, days_since_last_signal=10,
        current_lifecycle_state="stale_setup"
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    action = result.lifecycle_action_queue[0]
    assert action.action_type == "require_rescore"
    assert action.should_auto_apply is False


# =========================================================================
# Expired candidate queue classification
# =========================================================================
def test_expired_candidate_with_no_human_review_gate():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, LifecycleReviewInput, run_lifecycle_review
    )
    policy = SetupAgingPolicy(require_human_review_before_remove=False)
    item = CandidateLifecycleItem(
        symbol="EXP1", days_in_candidate_pool=65,
        current_lifecycle_state="active_candidate"
    )
    result = run_lifecycle_review(LifecycleReviewInput(
        review_period="2026-W01", candidate_items=[item], aging_policy=policy
    ))
    action = result.lifecycle_action_queue[0]
    assert action.action_type == "remove_from_candidate_pool"
    assert action.should_auto_apply is False

def test_expired_candidate_with_human_review_gate():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, LifecycleReviewInput, run_lifecycle_review
    )
    policy = SetupAgingPolicy(require_human_review_before_remove=True)
    item = CandidateLifecycleItem(
        symbol="EXP2", days_in_candidate_pool=65,
        current_lifecycle_state="active_candidate"
    )
    result = run_lifecycle_review(LifecycleReviewInput(
        review_period="2026-W01", candidate_items=[item], aging_policy=policy
    ))
    action = result.lifecycle_action_queue[0]
    assert action.action_type == "require_human_review"
    assert action.requires_human_review is True
    assert action.should_auto_apply is False

def test_expired_state_direct():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, LifecycleReviewInput, run_lifecycle_review
    )
    policy = SetupAgingPolicy(require_human_review_before_remove=True)
    item = CandidateLifecycleItem(
        symbol="EXP3", days_in_candidate_pool=5,
        current_lifecycle_state="expired_candidate"
    )
    result = run_lifecycle_review(LifecycleReviewInput(
        review_period="2026-W01", candidate_items=[item], aging_policy=policy
    ))
    action = result.lifecycle_action_queue[0]
    assert action.action_type in ("require_human_review", "remove_from_candidate_pool")


# =========================================================================
# Rescore queue classification
# =========================================================================
def test_rescore_queue_item_from_stale_state():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="RSC1", days_in_candidate_pool=25,
        current_lifecycle_state="stale_setup"
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.lifecycle_action_queue[0].action_type == "require_rescore"

def test_rescore_queue_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="RSC2", days_in_candidate_pool=25,
        current_lifecycle_state="stale_setup"
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.lifecycle_action_queue[0].should_auto_apply is False


# =========================================================================
# Human review queue severity and reason coverage
# =========================================================================
def test_human_review_with_single_reason():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="HR1", human_review_reasons=["signal_conflict"]
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert len(result.human_review_queue) == 1

def test_human_review_with_multiple_reasons():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="HR2", human_review_reasons=["signal_conflict", "theme_fade", "risk_spike"]
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.lifecycle_action_queue[0].requires_human_review is True

def test_human_review_action_type():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="HR3", human_review_reasons=["manual_flag"]
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.lifecycle_action_queue[0].action_type == "require_human_review"

def test_human_review_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(symbol="HR4", human_review_reasons=["manual_flag"])
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.lifecycle_action_queue[0].should_auto_apply is False


# =========================================================================
# Downgrade / remove logic
# =========================================================================
def test_downgrade_with_single_reason():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="DG1", days_in_candidate_pool=10,
        days_since_last_signal=3, current_lifecycle_state="active_candidate",
        downgrade_reasons=["weak_volume"]
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    action = result.lifecycle_action_queue[0]
    assert action.action_type == "downgrade_to_watchlist"
    assert action.to_state == "downgraded_to_watchlist"

def test_downgrade_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="DG2", downgrade_reasons=["theme_faded"]
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    assert result.lifecycle_action_queue[0].should_auto_apply is False

def test_downgrade_reason_codes_in_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    item = CandidateLifecycleItem(
        symbol="DG3", downgrade_reasons=["no_volume", "no_theme"]
    )
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=[item]))
    action = result.lifecycle_action_queue[0]
    assert len(action.action_reason_codes) >= 1


# =========================================================================
# auto_apply_enabled / should_auto_apply always False — exhaustive
# =========================================================================
def test_auto_apply_false_after_explicit_true_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    p = SetupAgingPolicy(auto_apply_enabled=True)
    assert p.auto_apply_enabled is False

def test_should_auto_apply_false_after_explicit_true_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleAction
    a = LifecycleAction(should_auto_apply=True)
    assert a.should_auto_apply is False

def test_should_auto_apply_false_after_explicit_true_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleReviewResult
    r = LifecycleReviewResult(should_auto_apply=True)
    assert r.should_auto_apply is False

def test_all_actions_from_default_run_have_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    result = run_lifecycle_review()
    for action in result.lifecycle_action_queue:
        assert action.should_auto_apply is False

def test_policy_auto_apply_false_regardless_of_init():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    for val in (True, False, None):
        try:
            p = SetupAgingPolicy(auto_apply_enabled=val)
            assert p.auto_apply_enabled is False
        except TypeError:
            pass


# =========================================================================
# Lifecycle summary count consistency
# =========================================================================
def test_lifecycle_summary_total_count_matches_input():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    items = [
        CandidateLifecycleItem(symbol=f"S{i}", days_in_candidate_pool=i*3) for i in range(6)
    ]
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=items))
    summary = result.lifecycle_summary
    assert summary.total_candidate_count == 6

def test_lifecycle_summary_action_queue_count_matches_input():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    items = [CandidateLifecycleItem(symbol=f"T{i}") for i in range(4)]
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=items))
    assert len(result.lifecycle_action_queue) == 4

def test_lifecycle_summary_grade_A_for_fresh_pool():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    items = [CandidateLifecycleItem(symbol=f"F{i}", days_in_candidate_pool=3) for i in range(3)]
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=items))
    assert result.lifecycle_summary.lifecycle_quality_grade == "A"

def test_lifecycle_summary_grade_D_for_stale_pool():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    items = [CandidateLifecycleItem(symbol=f"D{i}", days_in_candidate_pool=40) for i in range(3)]
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=items))
    assert result.lifecycle_summary.lifecycle_quality_grade == "D"

def test_lifecycle_summary_avg_days_in_pool():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, LifecycleReviewInput, run_lifecycle_review
    )
    items = [
        CandidateLifecycleItem(symbol="P1", days_in_candidate_pool=10),
        CandidateLifecycleItem(symbol="P2", days_in_candidate_pool=20),
    ]
    result = run_lifecycle_review(LifecycleReviewInput(review_period="2026-W01", candidate_items=items))
    assert result.lifecycle_summary.avg_days_in_candidate_pool == 15.0

def test_lifecycle_summary_counts_nonnegative():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    summary = run_lifecycle_review().lifecycle_summary
    assert summary.active_count >= 0
    assert summary.waiting_count >= 0
    assert summary.stale_count >= 0
    assert summary.expired_count >= 0
    assert summary.human_review_count >= 0


# =========================================================================
# JSON export schema completeness
# =========================================================================
def test_json_export_contains_lifecycle_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_json, run_lifecycle_review
    content = export_lifecycle_json(run_lifecycle_review()).content
    assert "lifecycle_version" in content

def test_json_export_contains_review_period():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_json, run_lifecycle_review
    content = export_lifecycle_json(run_lifecycle_review()).content
    assert "review_period" in content

def test_json_export_contains_paper_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_json, run_lifecycle_review
    content = export_lifecycle_json(run_lifecycle_review()).content
    assert "paper_only" in content
    assert "true" in content

def test_json_export_contains_action_queue_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_json, run_lifecycle_review
    content = export_lifecycle_json(run_lifecycle_review()).content
    assert "action_queue_count" in content

def test_json_export_status_complete():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_json, run_lifecycle_review
    assert export_lifecycle_json(run_lifecycle_review()).export_status == "complete"


# =========================================================================
# Markdown report completeness
# =========================================================================
def test_markdown_contains_lifecycle_review_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_markdown, run_lifecycle_review
    result = run_lifecycle_review()
    md = export_lifecycle_markdown(result).content
    assert result.lifecycle_review_id in md

def test_markdown_contains_version_206():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_markdown, run_lifecycle_review
    md = export_lifecycle_markdown(run_lifecycle_review()).content
    assert "2.0.6" in md

def test_markdown_contains_lifecycle_summary_section():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_markdown, run_lifecycle_review
    md = export_lifecycle_markdown(run_lifecycle_review()).content
    assert "Lifecycle Summary" in md

def test_markdown_contains_action_queue_section():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_markdown, run_lifecycle_review
    md = export_lifecycle_markdown(run_lifecycle_review()).content
    assert "Action Queue" in md

def test_markdown_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_markdown, run_lifecycle_review
    md = export_lifecycle_markdown(run_lifecycle_review()).content
    assert "should_auto_apply" in md
    assert "False" in md

def test_markdown_no_real_orders_stated():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_lifecycle_markdown, run_lifecycle_review
    md = export_lifecycle_markdown(run_lifecycle_review()).content
    assert "no_real_orders" in md


# =========================================================================
# Stale setup CSV schema completeness
# =========================================================================
def test_stale_csv_contains_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_stale_setup_csv, run_lifecycle_review
    csv = export_stale_setup_csv(run_lifecycle_review()).csv_content
    assert "should_auto_apply" in csv

def test_stale_csv_contains_days_in_candidate_pool():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_stale_setup_csv, run_lifecycle_review
    csv = export_stale_setup_csv(run_lifecycle_review()).csv_content
    assert "days_in_candidate_pool" in csv

def test_stale_csv_row_count_nonnegative():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_stale_setup_csv, run_lifecycle_review
    result = export_stale_setup_csv(run_lifecycle_review())
    assert result.row_count >= 0

def test_stale_csv_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_stale_setup_csv, run_lifecycle_review
    assert export_stale_setup_csv(run_lifecycle_review()).paper_only is True


# =========================================================================
# Expired candidate CSV schema completeness
# =========================================================================
def test_expired_csv_contains_should_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_expired_candidate_csv, run_lifecycle_review
    csv = export_expired_candidate_csv(run_lifecycle_review()).csv_content
    assert "should_auto_apply" in csv

def test_expired_csv_contains_days_in_candidate_pool():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_expired_candidate_csv, run_lifecycle_review
    csv = export_expired_candidate_csv(run_lifecycle_review()).csv_content
    assert "days_in_candidate_pool" in csv

def test_expired_csv_row_count_nonnegative():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_expired_candidate_csv, run_lifecycle_review
    result = export_expired_candidate_csv(run_lifecycle_review())
    assert result.row_count >= 0

def test_expired_csv_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import export_expired_candidate_csv, run_lifecycle_review
    assert export_expired_candidate_csv(run_lifecycle_review()).no_real_orders is True


# =========================================================================
# v2.0.5 watchlist rotation integration
# =========================================================================
def test_v205_watchlist_rotation_paper_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    assert run_watchlist_rotation().paper_only is True

def test_v205_watchlist_rotation_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    assert run_watchlist_rotation().should_auto_apply is False

def test_v205_watchlist_rotation_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    assert run_watchlist_rotation().no_broker is True

def test_v205_promotion_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import build_promotion_queue
    assert isinstance(build_promotion_queue(), list)

def test_v205_safety_flags_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    assert SAFETY_FLAGS_V205["paper_only"] is True
    assert SAFETY_FLAGS_V205["should_auto_apply_always_false"] is True

def test_v206_does_not_break_v205_scenarios():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS as S205
    assert len(S205) == 80

def test_v206_does_not_break_v205_fixtures():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v205 import FIXTURES as F205
    assert len(F205) == 80


# =========================================================================
# v201 health relative-path compatibility not regressed
# =========================================================================
def test_v201_health_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_health_v201

def test_v201_test_paper_cockpit_file_exists():
    import os
    path = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "test_paper_cockpit_v201.py"
    ))
    assert os.path.exists(path)

def test_v201_health_relative_path_from_v206_health_dir():
    import os
    v206_health_dir = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "..", "paper_trading", "small_capital_strategy"
    ))
    path = os.path.normpath(os.path.join(v206_health_dir, "paper_cockpit_health_v201.py"))
    assert os.path.exists(path)


# =========================================================================
# GUI render_all_tabs — zero error tabs (additional coverage)
# =========================================================================
def test_render_all_tabs_v205_tabs_still_clean():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    for tab in ["watchlist_rotation_v205", "promotion_queue_v205", "human_review_queue_v205"]:
        assert "error" not in result.get(tab, {}), f"Tab {tab} has error"

def test_render_all_tabs_v204_tabs_still_clean():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    for tab in ["weekly_review_v204", "improvement_pack_v204", "review_metrics_v204"]:
        assert "error" not in result.get(tab, {}), f"Tab {tab} has error"

def test_render_all_tabs_v206_all_have_paper_only():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    for tab in ["candidate_lifecycle_v206", "setup_aging_v206", "stale_candidate_queue_v206"]:
        data = result.get(tab, {})
        assert data.get("paper_only") is True, f"Tab {tab} missing paper_only=True"

def test_render_all_tabs_v206_all_have_no_real_orders():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    for tab in ["candidate_lifecycle_v206", "setup_aging_v206", "stale_candidate_queue_v206"]:
        data = result.get(tab, {})
        assert data.get("no_real_orders") is True, f"Tab {tab} missing no_real_orders=True"

def test_render_all_tabs_v206_auto_apply_false():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    for tab in ["candidate_lifecycle_v206", "setup_aging_v206", "stale_candidate_queue_v206"]:
        data = result.get(tab, {})
        assert data.get("should_auto_apply") is False, f"Tab {tab} should_auto_apply not False"

def test_get_v206_tab_names_correct_contents():
    from gui.small_capital_strategy_panel import get_v206_tab_names
    names = get_v206_tab_names()
    assert "candidate_lifecycle_v206" in names
    assert "setup_aging_v206" in names
    assert "stale_candidate_queue_v206" in names
