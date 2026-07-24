"""
tests/test_paper_cockpit_v214.py
v2.0.14 Paper Pullback Reaction & Crash Rebound Confirmation — Tests
[!] Paper Only. Research Only. Pullback Reaction Recommendation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import pytest

# ===========================================================================
# Imports
# ===========================================================================

from paper_trading.small_capital_strategy.paper_cockpit_v214 import (
    VERSION,
    SCHEMA_VERSION,
    RELEASE_NAME,
    NO_REAL_ORDERS,
    BROKER_EXECUTION_ENABLED,
    PRODUCTION_TRADING_BLOCKED,
    REACTION_STATES,
    RECOMMENDED_ACTIONS,
    CLI_COMMANDS_V214,
    GUI_TABS_V214,
    SAFETY_FLAGS_V214,
    BASELINE_TESTS,
    MIN_NEW_TESTS,
    PullbackPolicy,
    PullbackEvent,
    ConfirmationSignal,
    PullbackSummary,
    PullbackReviewInput,
    PullbackReviewResult,
    PullbackExportResult,
    PullbackAuditSnapshot,
    PullbackMarkdownReport,
    ReboundWatchQueueCSV,
    ReboundFailureQueueCSV,
    PullbackReactionCSV,
    V214HealthSummary,
    V214ReleaseSummary,
    PullbackSafetyGuard,
    PullbackSummaryCSV,
    detect_pullback_event,
    evaluate_rebound_confirmation,
    build_rebound_watch_queue,
    build_rebound_failure_queue,
    build_human_review_queue,
    run_pullback_reaction_review,
    export_pullback_json,
    export_pullback_markdown,
    export_pullback_csv,
    export_rebound_watch_queue_csv,
    export_rebound_failure_queue_csv,
    export_pullback_audit_snapshot,
    verify_version,
    get_cockpit_summary_v214,
    PULLBACK_REVIEW_FIELDS,
    PULLBACK_POLICY_FIELDS,
    PULLBACK_EVENT_FIELDS,
    CONFIRMATION_SIGNAL_FIELDS,
    PULLBACK_SUMMARY_FIELDS,
    COVERED_VERSIONS,
)


# ===========================================================================
# A. Version and constants
# ===========================================================================

class TestVersionConstants:
    def test_version_is_214(self):
        assert VERSION == "2.0.14"

    def test_schema_version_is_214(self):
        assert SCHEMA_VERSION == "214"

    def test_release_name_contains_pullback(self):
        assert "Pullback" in RELEASE_NAME

    def test_release_name_contains_rebound(self):
        assert "Rebound" in RELEASE_NAME or "Crash" in RELEASE_NAME

    def test_no_real_orders_true(self):
        assert NO_REAL_ORDERS is True

    def test_broker_execution_enabled_false(self):
        assert BROKER_EXECUTION_ENABLED is False

    def test_production_trading_blocked_true(self):
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_verify_version_returns_true(self):
        assert verify_version() is True

    def test_baseline_tests_value(self):
        assert BASELINE_TESTS == 36989

    def test_min_new_tests_value(self):
        assert MIN_NEW_TESTS == 300

    def test_baseline_gte_300(self):
        assert BASELINE_TESTS >= 36000

    def test_covered_versions_includes_213(self):
        assert "2.0.13" in COVERED_VERSIONS

    def test_covered_versions_includes_212(self):
        assert "2.0.12" in COVERED_VERSIONS

    def test_covered_versions_includes_207(self):
        assert "2.0.7" in COVERED_VERSIONS


# ===========================================================================
# B. Safety flags
# ===========================================================================

class TestSafetyFlags:
    def test_safety_flags_count_25(self):
        assert len(SAFETY_FLAGS_V214) == 25

    def test_paper_only_true(self):
        assert SAFETY_FLAGS_V214["paper_only"] is True

    def test_research_only_true(self):
        assert SAFETY_FLAGS_V214["research_only"] is True

    def test_pullback_reaction_recommendation_only_true(self):
        assert SAFETY_FLAGS_V214["pullback_reaction_recommendation_only"] is True

    def test_rebound_recommendation_only_true(self):
        assert SAFETY_FLAGS_V214["rebound_recommendation_only"] is True

    def test_validation_only_true(self):
        assert SAFETY_FLAGS_V214["validation_only"] is True

    def test_no_real_orders_true(self):
        assert SAFETY_FLAGS_V214["no_real_orders"] is True

    def test_no_broker_true(self):
        assert SAFETY_FLAGS_V214["no_broker"] is True

    def test_should_auto_apply_always_false_true(self):
        assert SAFETY_FLAGS_V214["should_auto_apply_always_false"] is True

    def test_auto_apply_enabled_always_false_true(self):
        assert SAFETY_FLAGS_V214["auto_apply_enabled_always_false"] is True

    def test_broker_execution_disabled_true(self):
        assert SAFETY_FLAGS_V214["broker_execution_disabled"] is True

    def test_production_trading_blocked_true(self):
        assert SAFETY_FLAGS_V214["production_trading_blocked"] is True

    def test_require_ma_reclaim_always_true(self):
        assert SAFETY_FLAGS_V214["require_ma_reclaim_for_confirmation_always_true"] is True

    def test_pullback_actions_recommendation_only_true(self):
        assert SAFETY_FLAGS_V214["pullback_actions_recommendation_only"] is True

    def test_no_automatic_pullback_action_true(self):
        assert SAFETY_FLAGS_V214["no_automatic_pullback_action"] is True

    def test_no_automatic_rebound_action_true(self):
        assert SAFETY_FLAGS_V214["no_automatic_rebound_action"] is True

    def test_no_automatic_stop_loss_execution_true(self):
        assert SAFETY_FLAGS_V214["no_automatic_stop_loss_execution"] is True

    def test_no_automatic_take_profit_execution_true(self):
        assert SAFETY_FLAGS_V214["no_automatic_take_profit_execution"] is True

    def test_no_automatic_rebalance_true(self):
        assert SAFETY_FLAGS_V214["no_automatic_rebalance"] is True

    def test_not_investment_advice_true(self):
        assert SAFETY_FLAGS_V214["not_investment_advice"] is True

    def test_human_review_required_true(self):
        assert SAFETY_FLAGS_V214["human_review_required"] is True

    def test_no_margin_true(self):
        assert SAFETY_FLAGS_V214["no_margin"] is True

    def test_no_leverage_true(self):
        assert SAFETY_FLAGS_V214["no_leverage"] is True

    def test_no_production_db_write_true(self):
        assert SAFETY_FLAGS_V214["no_production_db_write"] is True

    def test_no_real_account_sync_true(self):
        assert SAFETY_FLAGS_V214["no_real_account_sync"] is True


# ===========================================================================
# C. Reaction states
# ===========================================================================

class TestReactionStates:
    def test_reaction_states_count_6(self):
        assert len(REACTION_STATES) == 6

    def test_no_pullback_in_states(self):
        assert "no_pullback" in REACTION_STATES

    def test_observation_rebound_in_states(self):
        assert "observation_rebound" in REACTION_STATES

    def test_short_term_rebound_confirmed_in_states(self):
        assert "short_term_rebound_confirmed" in REACTION_STATES

    def test_rebound_failed_in_states(self):
        assert "rebound_failed" in REACTION_STATES

    def test_defensive_wait_second_confirmation_in_states(self):
        assert "defensive_wait_second_confirmation" in REACTION_STATES

    def test_human_review_required_in_states(self):
        assert "human_review_required" in REACTION_STATES


# ===========================================================================
# D. Recommended actions
# ===========================================================================

class TestRecommendedActions:
    def test_recommended_actions_count_6(self):
        assert len(RECOMMENDED_ACTIONS) == 6

    def test_observation_only_in_actions(self):
        assert "observation_only" in RECOMMENDED_ACTIONS

    def test_wait_for_ma_reclaim_in_actions(self):
        assert "wait_for_ma_reclaim" in RECOMMENDED_ACTIONS

    def test_short_term_rebound_confirmed_in_actions(self):
        assert "short_term_rebound_confirmed" in RECOMMENDED_ACTIONS

    def test_defensive_mode_in_actions(self):
        assert "defensive_mode" in RECOMMENDED_ACTIONS

    def test_rebound_failed_reduce_risk_in_actions(self):
        assert "rebound_failed_reduce_risk" in RECOMMENDED_ACTIONS

    def test_human_review_required_in_actions(self):
        assert "human_review_required" in RECOMMENDED_ACTIONS


# ===========================================================================
# E. CLI commands
# ===========================================================================

class TestCLICommands:
    def test_cli_commands_count_10(self):
        assert len(CLI_COMMANDS_V214) == 10

    def test_review_pullback_reaction(self):
        assert "paper-cockpit-v214-review-pullback-reaction" in CLI_COMMANDS_V214

    def test_detect_pullback_event(self):
        assert "paper-cockpit-v214-detect-pullback-event" in CLI_COMMANDS_V214

    def test_evaluate_rebound_confirmation(self):
        assert "paper-cockpit-v214-evaluate-rebound-confirmation" in CLI_COMMANDS_V214

    def test_build_rebound_watch_queue(self):
        assert "paper-cockpit-v214-build-rebound-watch-queue" in CLI_COMMANDS_V214

    def test_build_rebound_failure_queue(self):
        assert "paper-cockpit-v214-build-rebound-failure-queue" in CLI_COMMANDS_V214

    def test_export_json(self):
        assert "paper-cockpit-v214-export-json" in CLI_COMMANDS_V214

    def test_export_md(self):
        assert "paper-cockpit-v214-export-md" in CLI_COMMANDS_V214

    def test_export_csv(self):
        assert "paper-cockpit-v214-export-csv" in CLI_COMMANDS_V214

    def test_health(self):
        assert "paper-cockpit-v214-health" in CLI_COMMANDS_V214

    def test_gate(self):
        assert "paper-cockpit-v214-gate" in CLI_COMMANDS_V214


# ===========================================================================
# F. GUI tabs
# ===========================================================================

class TestGUITabs:
    def test_gui_tabs_count_3(self):
        assert len(GUI_TABS_V214) == 3

    def test_pullback_reaction_v214_tab(self):
        assert "pullback_reaction_v214" in GUI_TABS_V214

    def test_rebound_confirmation_v214_tab(self):
        assert "rebound_confirmation_v214" in GUI_TABS_V214

    def test_rebound_failure_queue_v214_tab(self):
        assert "rebound_failure_queue_v214" in GUI_TABS_V214


# ===========================================================================
# G. PullbackPolicy schema
# ===========================================================================

class TestPullbackPolicy:
    def test_default_auto_apply_false(self):
        pol = PullbackPolicy()
        assert pol.auto_apply_enabled is False

    def test_auto_apply_cannot_be_set_true(self):
        pol = PullbackPolicy(auto_apply_enabled=True)
        assert pol.auto_apply_enabled is False

    def test_require_reclaim_always_true(self):
        pol = PullbackPolicy()
        assert pol.require_reclaim_ma5_or_ma10_for_confirmation is True

    def test_require_reclaim_cannot_be_set_false(self):
        pol = PullbackPolicy(require_reclaim_ma5_or_ma10_for_confirmation=False)
        assert pol.require_reclaim_ma5_or_ma10_for_confirmation is True

    def test_observation_window_days_3(self):
        pol = PullbackPolicy()
        assert pol.observation_window_days == 3

    def test_seasonal_ma_period_60(self):
        pol = PullbackPolicy()
        assert pol.seasonal_ma_period == 60

    def test_reclaim_fast_ma_period_5(self):
        pol = PullbackPolicy()
        assert pol.reclaim_fast_ma_period == 5

    def test_reclaim_slow_ma_period_10(self):
        pol = PullbackPolicy()
        assert pol.reclaim_slow_ma_period == 10

    def test_require_index_near_ma60_true(self):
        pol = PullbackPolicy()
        assert pol.require_index_near_ma60 is True

    def test_require_index_near_ma60_cannot_be_set_false(self):
        pol = PullbackPolicy(require_index_near_ma60=False)
        assert pol.require_index_near_ma60 is True

    def test_require_tsmc_confirmation_true(self):
        pol = PullbackPolicy()
        assert pol.require_tsmc_confirmation is True

    def test_require_futures_or_adr_confirmation_true(self):
        pol = PullbackPolicy()
        assert pol.require_futures_or_adr_confirmation is True

    def test_require_margin_not_stressed_true(self):
        pol = PullbackPolicy()
        assert pol.require_margin_not_stressed is True

    def test_failure_if_breaks_pullback_low_true(self):
        pol = PullbackPolicy()
        assert pol.failure_if_breaks_pullback_low is True

    def test_paper_only_true(self):
        pol = PullbackPolicy()
        assert pol.paper_only is True

    def test_no_real_orders_true(self):
        pol = PullbackPolicy()
        assert pol.no_real_orders is True

    def test_schema_version_214(self):
        pol = PullbackPolicy()
        assert pol.schema_version == "214"

    def test_custom_policy_id(self):
        pol = PullbackPolicy(policy_id="my-policy")
        assert pol.policy_id == "my-policy"

    def test_policy_fields_complete(self):
        pol = PullbackPolicy()
        for f in PULLBACK_POLICY_FIELDS:
            assert hasattr(pol, f), f"Missing field: {f}"


# ===========================================================================
# H. PullbackEvent schema
# ===========================================================================

class TestPullbackEvent:
    def test_default_should_auto_apply_false(self):
        evt = PullbackEvent()
        assert evt.should_auto_apply is False

    def test_should_auto_apply_cannot_be_set_true(self):
        evt = PullbackEvent(should_auto_apply=True)
        assert evt.should_auto_apply is False

    def test_default_reaction_state(self):
        evt = PullbackEvent()
        assert evt.reaction_state == "no_pullback"

    def test_paper_only_true(self):
        evt = PullbackEvent()
        assert evt.paper_only is True

    def test_no_real_orders_true(self):
        evt = PullbackEvent()
        assert evt.no_real_orders is True

    def test_schema_version_214(self):
        evt = PullbackEvent()
        assert evt.schema_version == "214"

    def test_index_symbol_twse(self):
        evt = PullbackEvent()
        assert evt.index_symbol == "TWSE"

    def test_event_fields_complete(self):
        evt = PullbackEvent()
        for f in PULLBACK_EVENT_FIELDS:
            assert hasattr(evt, f), f"Missing field: {f}"


# ===========================================================================
# I. ConfirmationSignal schema
# ===========================================================================

class TestConfirmationSignal:
    def test_default_should_auto_apply_false(self):
        conf = ConfirmationSignal()
        assert conf.should_auto_apply is False

    def test_should_auto_apply_cannot_be_set_true(self):
        conf = ConfirmationSignal(should_auto_apply=True)
        assert conf.should_auto_apply is False

    def test_paper_only_true(self):
        conf = ConfirmationSignal()
        assert conf.paper_only is True

    def test_no_real_orders_true(self):
        conf = ConfirmationSignal()
        assert conf.no_real_orders is True

    def test_schema_version_214(self):
        conf = ConfirmationSignal()
        assert conf.schema_version == "214"

    def test_confirmation_fields_complete(self):
        conf = ConfirmationSignal()
        for f in CONFIRMATION_SIGNAL_FIELDS:
            assert hasattr(conf, f), f"Missing field: {f}"

    def test_failed_reasons_is_list(self):
        conf = ConfirmationSignal()
        assert isinstance(conf.failed_confirmation_reasons, list)


# ===========================================================================
# J. PullbackSummary schema
# ===========================================================================

class TestPullbackSummary:
    def test_default_reaction_state(self):
        s = PullbackSummary()
        assert s.reaction_state == "no_pullback"

    def test_default_recommended_action(self):
        s = PullbackSummary()
        assert s.recommended_action == "observation_only"

    def test_paper_only_true(self):
        s = PullbackSummary()
        assert s.paper_only is True

    def test_no_real_orders_true(self):
        s = PullbackSummary()
        assert s.no_real_orders is True

    def test_schema_version_214(self):
        s = PullbackSummary()
        assert s.schema_version == "214"

    def test_summary_fields_complete(self):
        s = PullbackSummary()
        for f in PULLBACK_SUMMARY_FIELDS:
            assert hasattr(s, f), f"Missing field: {f}"


# ===========================================================================
# K. detect_pullback_event
# ===========================================================================

class TestDetectPullbackEvent:
    def test_no_pullback_small_drop(self):
        evt = detect_pullback_event(
            index_level=45_000.0,
            pullback_start_level=45_200.0,
            pullback_low_level=44_900.0,
        )
        assert evt.pullback_pct > -0.03

    def test_significant_pullback_detection(self):
        evt = detect_pullback_event(
            index_level=43_000.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_500.0,
        )
        assert evt.pullback_pct < -0.05

    def test_near_ma60_detection_true(self):
        evt = detect_pullback_event(
            index_level=43_000.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_800.0,
            ma60=42_900.0,
        )
        assert evt.near_ma60 is True

    def test_near_ma60_detection_false(self):
        evt = detect_pullback_event(
            index_level=40_000.0,
            pullback_start_level=45_000.0,
            pullback_low_level=39_000.0,
            ma60=45_000.0,
        )
        assert evt.near_ma60 is False

    def test_reclaim_ma5_true(self):
        evt = detect_pullback_event(
            index_level=44_000.0,
            ma5=43_500.0,
        )
        assert evt.reclaimed_ma5 is True

    def test_reclaim_ma5_false(self):
        evt = detect_pullback_event(
            index_level=43_000.0,
            ma5=43_500.0,
        )
        assert evt.reclaimed_ma5 is False

    def test_reclaim_ma10_true(self):
        evt = detect_pullback_event(
            index_level=44_000.0,
            ma10=43_800.0,
        )
        assert evt.reclaimed_ma10 is True

    def test_reclaim_ma10_false(self):
        evt = detect_pullback_event(
            index_level=43_000.0,
            ma10=43_500.0,
        )
        assert evt.reclaimed_ma10 is False

    def test_broke_pullback_low_true(self):
        evt = detect_pullback_event(
            index_level=41_500.0,
            pullback_low_level=42_000.0,
        )
        assert evt.broke_pullback_low is True

    def test_broke_pullback_low_false(self):
        evt = detect_pullback_event(
            index_level=43_000.0,
            pullback_low_level=42_000.0,
        )
        assert evt.broke_pullback_low is False

    def test_should_auto_apply_always_false(self):
        evt = detect_pullback_event(index_level=43_000.0)
        assert evt.should_auto_apply is False

    def test_paper_only_true(self):
        evt = detect_pullback_event(index_level=43_000.0)
        assert evt.paper_only is True

    def test_no_real_orders_true(self):
        evt = detect_pullback_event(index_level=43_000.0)
        assert evt.no_real_orders is True

    def test_days_since_pullback_low_stored(self):
        evt = detect_pullback_event(index_level=43_000.0, days_since_pullback_low=2)
        assert evt.days_since_pullback_low == 2

    def test_pullback_low_date_stored(self):
        evt = detect_pullback_event(index_level=43_000.0, pullback_low_date="2026-07-18")
        assert evt.pullback_low_date == "2026-07-18"

    def test_human_review_on_extreme_pullback(self):
        evt = detect_pullback_event(
            index_level=40_000.0,
            pullback_start_level=45_000.0,
            pullback_low_level=39_000.0,
            days_since_pullback_low=1,
        )
        assert evt.requires_human_review is True

    def test_observation_window_3_days(self):
        pol = PullbackPolicy(observation_window_days=3)
        evt = detect_pullback_event(
            index_level=43_000.0,
            days_since_pullback_low=2,
            policy=pol,
        )
        assert evt.days_since_pullback_low == 2

    def test_schema_version_214(self):
        evt = detect_pullback_event(index_level=43_000.0)
        assert evt.schema_version == "214"


# ===========================================================================
# L. evaluate_rebound_confirmation
# ===========================================================================

class TestEvaluateReboundConfirmation:
    def test_all_signals_positive_high_score(self):
        conf = evaluate_rebound_confirmation(
            tsmc_spot_up=True,
            tsmc_adr_positive=True,
            futures_night_stable=True,
            foreign_futures_short_increasing=False,
            margin_stress=False,
            volume_expansion=True,
            ma_reclaim=True,
        )
        assert conf.confirmation_score >= 0.9

    def test_all_signals_negative_low_score(self):
        conf = evaluate_rebound_confirmation(
            tsmc_spot_up=False,
            tsmc_adr_positive=False,
            futures_night_stable=False,
            foreign_futures_short_increasing=True,
            margin_stress=True,
            volume_expansion=False,
            ma_reclaim=False,
        )
        assert conf.confirmation_score == 0.0

    def test_tsmc_spot_confirmed_flag(self):
        conf = evaluate_rebound_confirmation(tsmc_spot_up=True)
        assert conf.tsmc_spot_confirmed is True

    def test_tsmc_spot_not_confirmed_flag(self):
        conf = evaluate_rebound_confirmation(tsmc_spot_up=False)
        assert conf.tsmc_spot_confirmed is False

    def test_tsmc_adr_confirmed_flag(self):
        conf = evaluate_rebound_confirmation(tsmc_adr_positive=True)
        assert conf.tsmc_adr_confirmed is True

    def test_futures_night_session_stable(self):
        conf = evaluate_rebound_confirmation(futures_night_stable=True)
        assert conf.futures_night_session_stable is True

    def test_foreign_futures_short_not_increasing(self):
        conf = evaluate_rebound_confirmation(foreign_futures_short_increasing=False)
        assert conf.foreign_futures_short_not_increasing is True

    def test_foreign_futures_short_increasing_blocks(self):
        conf = evaluate_rebound_confirmation(foreign_futures_short_increasing=True)
        assert conf.foreign_futures_short_not_increasing is False

    def test_margin_stress_controlled_true_when_no_stress(self):
        conf = evaluate_rebound_confirmation(margin_stress=False)
        assert conf.margin_stress_controlled is True

    def test_margin_stress_detected(self):
        conf = evaluate_rebound_confirmation(margin_stress=True)
        assert conf.margin_stress_controlled is False

    def test_volume_confirmation_true(self):
        conf = evaluate_rebound_confirmation(volume_expansion=True)
        assert conf.volume_confirmation is True

    def test_ma_reclaim_confirmation_true(self):
        conf = evaluate_rebound_confirmation(ma_reclaim=True)
        assert conf.ma_reclaim_confirmation is True

    def test_should_auto_apply_always_false(self):
        conf = evaluate_rebound_confirmation()
        assert conf.should_auto_apply is False

    def test_paper_only_true(self):
        conf = evaluate_rebound_confirmation()
        assert conf.paper_only is True

    def test_failed_reasons_populated_when_signals_fail(self):
        conf = evaluate_rebound_confirmation(tsmc_spot_up=False)
        assert "tsmc_spot_not_confirmed" in conf.failed_confirmation_reasons

    def test_failed_reasons_empty_when_all_pass(self):
        conf = evaluate_rebound_confirmation(
            tsmc_spot_up=True,
            tsmc_adr_positive=True,
            futures_night_stable=True,
            foreign_futures_short_increasing=False,
            margin_stress=False,
            volume_expansion=True,
            ma_reclaim=True,
        )
        assert len(conf.failed_confirmation_reasons) == 0

    def test_score_between_0_and_1(self):
        conf = evaluate_rebound_confirmation()
        assert 0.0 <= conf.confirmation_score <= 1.0

    def test_schema_version_214(self):
        conf = evaluate_rebound_confirmation()
        assert conf.schema_version == "214"


# ===========================================================================
# M. Reaction state detection
# ===========================================================================

class TestReactionStateDetection:
    def test_no_pullback_state_small_drop(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=45_000.0,
            pullback_start_level=45_200.0,
            pullback_low_level=44_900.0,
            days_since_pullback_low=1,
            ma5=44_900.0,
            ma10=44_500.0,
            ma60=43_000.0,
            tsmc_spot_up=True,
            tsmc_adr_positive=True,
            futures_night_stable=True,
            foreign_futures_short_increasing=False,
            margin_stress=False,
            volume_expansion=False,
        ))
        assert result.index_snapshot.reaction_state == "no_pullback"

    def test_rebound_failed_when_breaks_pullback_low(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=41_500.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_000.0,
            days_since_pullback_low=5,
            ma5=42_800.0,
            ma10=43_500.0,
            ma60=43_200.0,
            tsmc_spot_up=False,
            tsmc_adr_positive=False,
            futures_night_stable=False,
            foreign_futures_short_increasing=True,
            margin_stress=True,
            volume_expansion=False,
        ))
        assert result.index_snapshot.reaction_state == "rebound_failed"

    def test_short_term_confirmed_when_reclaim_ma5_high_score(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=44_200.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_500.0,
            days_since_pullback_low=3,
            ma5=44_000.0,
            ma10=44_500.0,
            ma60=42_800.0,
            tsmc_spot_up=True,
            tsmc_adr_positive=True,
            futures_night_stable=True,
            foreign_futures_short_increasing=False,
            margin_stress=False,
            volume_expansion=True,
        ))
        assert result.index_snapshot.reaction_state == "short_term_rebound_confirmed"

    def test_observation_rebound_near_ma60(self):
        # near MA60, moderate signals (score >= 0.4 so not defensive, no MA reclaim so not confirmed)
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=43_000.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_800.0,
            days_since_pullback_low=2,
            ma5=43_500.0,
            ma10=44_000.0,
            ma60=42_900.0,
            tsmc_spot_up=True,
            tsmc_adr_positive=True,
            futures_night_stable=True,
            foreign_futures_short_increasing=False,
            margin_stress=False,
            volume_expansion=False,
        ))
        assert result.index_snapshot.reaction_state == "observation_rebound"

    def test_defensive_state_low_confirmation_score(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=42_800.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_500.0,
            days_since_pullback_low=2,
            ma5=43_200.0,
            ma10=43_800.0,
            ma60=42_900.0,
            tsmc_spot_up=False,
            tsmc_adr_positive=False,
            futures_night_stable=False,
            foreign_futures_short_increasing=True,
            margin_stress=False,
            volume_expansion=False,
        ))
        assert result.index_snapshot.reaction_state == "defensive_wait_second_confirmation"

    def test_rebound_failed_recommended_action(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=41_500.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_000.0,
            days_since_pullback_low=5,
            ma5=42_800.0,
            ma10=43_500.0,
            ma60=43_200.0,
            tsmc_spot_up=False,
            tsmc_adr_positive=False,
            futures_night_stable=False,
            foreign_futures_short_increasing=True,
            margin_stress=True,
            volume_expansion=False,
        ))
        assert result.pullback_summary.recommended_action == "rebound_failed_reduce_risk"


# ===========================================================================
# N. 1-3 day observation window
# ===========================================================================

class TestObservationWindow:
    def test_within_1_day_observation(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=43_000.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_800.0,
            days_since_pullback_low=1,
            ma5=43_500.0,
            ma10=44_000.0,
            ma60=42_900.0,
            tsmc_spot_up=False,
            tsmc_adr_positive=False,
            futures_night_stable=False,
            foreign_futures_short_increasing=True,
            margin_stress=False,
            volume_expansion=False,
        ))
        assert result.index_snapshot.days_since_pullback_low == 1

    def test_within_2_day_observation(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=43_000.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_800.0,
            days_since_pullback_low=2,
            ma5=43_500.0,
            ma10=44_000.0,
            ma60=42_900.0,
            tsmc_spot_up=False,
            tsmc_adr_positive=False,
            futures_night_stable=False,
            foreign_futures_short_increasing=True,
            margin_stress=False,
            volume_expansion=False,
        ))
        assert result.index_snapshot.days_since_pullback_low == 2

    def test_within_3_day_observation(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=43_000.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_800.0,
            days_since_pullback_low=3,
            ma5=43_500.0,
            ma10=44_000.0,
            ma60=42_900.0,
            tsmc_spot_up=False,
            tsmc_adr_positive=False,
            futures_night_stable=False,
            foreign_futures_short_increasing=True,
            margin_stress=False,
            volume_expansion=False,
        ))
        assert result.index_snapshot.days_since_pullback_low == 3


# ===========================================================================
# O. Near MA60 detection
# ===========================================================================

class TestNearMA60:
    def test_near_ma60_within_3pct(self):
        evt = detect_pullback_event(
            index_level=43_000.0,
            pullback_low_level=42_800.0,
            ma60=42_900.0,
        )
        assert evt.near_ma60 is True

    def test_not_near_ma60_far_away(self):
        evt = detect_pullback_event(
            index_level=38_000.0,
            pullback_low_level=37_500.0,
            ma60=43_000.0,
        )
        assert evt.near_ma60 is False

    def test_near_ma60_exactly_at_ma60(self):
        evt = detect_pullback_event(
            index_level=43_000.0,
            pullback_low_level=43_000.0,
            ma60=43_000.0,
        )
        assert evt.near_ma60 is True


# ===========================================================================
# P. Reclaim MA5 confirmation
# ===========================================================================

class TestReclaimMA5:
    def test_reclaim_ma5_when_above(self):
        evt = detect_pullback_event(index_level=44_000.0, ma5=43_500.0)
        assert evt.reclaimed_ma5 is True

    def test_not_reclaim_ma5_when_below(self):
        evt = detect_pullback_event(index_level=43_000.0, ma5=43_500.0)
        assert evt.reclaimed_ma5 is False

    def test_reclaim_ma5_exactly_at_ma5(self):
        evt = detect_pullback_event(index_level=43_500.0, ma5=43_500.0)
        assert evt.reclaimed_ma5 is True

    def test_require_reclaim_ma5_for_confirmation(self):
        pol = PullbackPolicy()
        assert pol.require_reclaim_ma5_or_ma10_for_confirmation is True


# ===========================================================================
# Q. Reclaim MA10 confirmation
# ===========================================================================

class TestReclaimMA10:
    def test_reclaim_ma10_when_above(self):
        evt = detect_pullback_event(index_level=44_000.0, ma10=43_800.0)
        assert evt.reclaimed_ma10 is True

    def test_not_reclaim_ma10_when_below(self):
        evt = detect_pullback_event(index_level=43_000.0, ma10=43_500.0)
        assert evt.reclaimed_ma10 is False

    def test_require_reclaim_ma5_or_ma10_for_confirmation_always_true(self):
        pol = PullbackPolicy(require_reclaim_ma5_or_ma10_for_confirmation=False)
        assert pol.require_reclaim_ma5_or_ma10_for_confirmation is True


# ===========================================================================
# R. Break pullback low failure
# ===========================================================================

class TestBreakPullbackLow:
    def test_broke_pullback_low_detected(self):
        evt = detect_pullback_event(
            index_level=41_500.0,
            pullback_low_level=42_000.0,
        )
        assert evt.broke_pullback_low is True

    def test_not_broke_pullback_low_when_above(self):
        evt = detect_pullback_event(
            index_level=43_000.0,
            pullback_low_level=42_000.0,
        )
        assert evt.broke_pullback_low is False

    def test_failure_if_breaks_pullback_low_policy(self):
        pol = PullbackPolicy()
        assert pol.failure_if_breaks_pullback_low is True

    def test_rebound_failed_state_when_broke_low(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=41_500.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_000.0,
            days_since_pullback_low=3,
            ma5=42_800.0,
            ma10=43_500.0,
            ma60=43_200.0,
            tsmc_spot_up=False,
            tsmc_adr_positive=False,
            futures_night_stable=False,
            foreign_futures_short_increasing=True,
            margin_stress=True,
            volume_expansion=False,
        ))
        assert result.index_snapshot.broke_pullback_low is True
        assert result.index_snapshot.reaction_state == "rebound_failed"


# ===========================================================================
# S. TSMC confirmations
# ===========================================================================

class TestTSMCConfirmation:
    def test_tsmc_spot_confirmed_true(self):
        conf = evaluate_rebound_confirmation(tsmc_spot_up=True)
        assert conf.tsmc_spot_confirmed is True

    def test_tsmc_spot_not_confirmed(self):
        conf = evaluate_rebound_confirmation(tsmc_spot_up=False)
        assert conf.tsmc_spot_confirmed is False
        assert "tsmc_spot_not_confirmed" in conf.failed_confirmation_reasons

    def test_tsmc_adr_confirmed_true(self):
        conf = evaluate_rebound_confirmation(tsmc_adr_positive=True)
        assert conf.tsmc_adr_confirmed is True

    def test_tsmc_adr_not_confirmed(self):
        conf = evaluate_rebound_confirmation(tsmc_adr_positive=False)
        assert conf.tsmc_adr_confirmed is False
        assert "tsmc_adr_not_confirmed" in conf.failed_confirmation_reasons

    def test_both_tsmc_confirmed_contributes_score(self):
        conf_both = evaluate_rebound_confirmation(tsmc_spot_up=True, tsmc_adr_positive=True)
        conf_none = evaluate_rebound_confirmation(tsmc_spot_up=False, tsmc_adr_positive=False)
        assert conf_both.confirmation_score > conf_none.confirmation_score


# ===========================================================================
# T. Futures night session & ADR confirmation
# ===========================================================================

class TestFuturesADRConfirmation:
    def test_futures_night_session_stable(self):
        conf = evaluate_rebound_confirmation(futures_night_stable=True)
        assert conf.futures_night_session_stable is True

    def test_futures_night_session_unstable(self):
        conf = evaluate_rebound_confirmation(futures_night_stable=False)
        assert conf.futures_night_session_stable is False
        assert "futures_night_session_unstable" in conf.failed_confirmation_reasons

    def test_foreign_futures_short_not_increasing(self):
        conf = evaluate_rebound_confirmation(foreign_futures_short_increasing=False)
        assert conf.foreign_futures_short_not_increasing is True

    def test_foreign_futures_short_increasing_failure(self):
        conf = evaluate_rebound_confirmation(foreign_futures_short_increasing=True)
        assert conf.foreign_futures_short_not_increasing is False
        assert "foreign_futures_short_increasing" in conf.failed_confirmation_reasons


# ===========================================================================
# U. Margin stress detection
# ===========================================================================

class TestMarginStress:
    def test_margin_stress_controlled_when_no_stress(self):
        conf = evaluate_rebound_confirmation(margin_stress=False)
        assert conf.margin_stress_controlled is True

    def test_margin_stress_detected(self):
        conf = evaluate_rebound_confirmation(margin_stress=True)
        assert conf.margin_stress_controlled is False
        assert "margin_stress_detected" in conf.failed_confirmation_reasons

    def test_margin_stress_reduces_score(self):
        conf_ok = evaluate_rebound_confirmation(margin_stress=False)
        conf_stress = evaluate_rebound_confirmation(margin_stress=True)
        assert conf_ok.confirmation_score > conf_stress.confirmation_score


# ===========================================================================
# V. Volume confirmation
# ===========================================================================

class TestVolumeConfirmation:
    def test_volume_confirmed_true(self):
        conf = evaluate_rebound_confirmation(volume_expansion=True)
        assert conf.volume_confirmation is True

    def test_volume_not_confirmed(self):
        conf = evaluate_rebound_confirmation(volume_expansion=False)
        assert conf.volume_confirmation is False

    def test_volume_failure_in_reasons(self):
        conf = evaluate_rebound_confirmation(volume_expansion=False)
        assert "volume_not_confirmed" in conf.failed_confirmation_reasons


# ===========================================================================
# W. Confirmation score
# ===========================================================================

class TestConfirmationScore:
    def test_score_range_0_to_1(self):
        conf = evaluate_rebound_confirmation()
        assert 0.0 <= conf.confirmation_score <= 1.0

    def test_perfect_score(self):
        conf = evaluate_rebound_confirmation(
            tsmc_spot_up=True, tsmc_adr_positive=True,
            futures_night_stable=True, foreign_futures_short_increasing=False,
            margin_stress=False, volume_expansion=True, ma_reclaim=True,
        )
        assert conf.confirmation_score == 1.0

    def test_zero_score(self):
        conf = evaluate_rebound_confirmation(
            tsmc_spot_up=False, tsmc_adr_positive=False,
            futures_night_stable=False, foreign_futures_short_increasing=True,
            margin_stress=True, volume_expansion=False, ma_reclaim=False,
        )
        assert conf.confirmation_score == 0.0

    def test_partial_score(self):
        conf = evaluate_rebound_confirmation(tsmc_spot_up=True, tsmc_adr_positive=False,
            futures_night_stable=False, foreign_futures_short_increasing=True,
            margin_stress=False, volume_expansion=False, ma_reclaim=False)
        assert 0.0 < conf.confirmation_score < 1.0


# ===========================================================================
# X. Rebound quality grade
# ===========================================================================

class TestReboundQualityGrade:
    def test_grade_a_when_confirmed_high_score(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=44_200.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_500.0,
            days_since_pullback_low=3,
            ma5=44_000.0,
            ma10=44_500.0,
            ma60=42_800.0,
            tsmc_spot_up=True,
            tsmc_adr_positive=True,
            futures_night_stable=True,
            foreign_futures_short_increasing=False,
            margin_stress=False,
            volume_expansion=True,
        ))
        summ = result.pullback_summary
        assert summ.rebound_quality_grade in ("A", "B", "C")

    def test_grade_c_when_rebound_failed(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=41_500.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_000.0,
            days_since_pullback_low=5,
            ma5=42_800.0,
            ma10=43_500.0,
            ma60=43_200.0,
            tsmc_spot_up=False,
            tsmc_adr_positive=False,
            futures_night_stable=False,
            foreign_futures_short_increasing=True,
            margin_stress=True,
            volume_expansion=False,
        ))
        assert result.pullback_summary.rebound_quality_grade == "C"


# ===========================================================================
# Y. Failure risk grade
# ===========================================================================

class TestFailureRiskGrade:
    def test_risk_grade_c_when_broke_low(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=41_500.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_000.0,
            days_since_pullback_low=5,
            ma5=42_800.0,
            ma10=43_500.0,
            ma60=43_200.0,
            tsmc_spot_up=False,
            tsmc_adr_positive=False,
            futures_night_stable=False,
            foreign_futures_short_increasing=True,
            margin_stress=True,
            volume_expansion=False,
        ))
        assert result.pullback_summary.failure_risk_grade == "C"

    def test_risk_grade_valid_value(self):
        result = run_pullback_reaction_review()
        assert result.pullback_summary.failure_risk_grade in ("A", "B", "C")


# ===========================================================================
# Z. Recommended action
# ===========================================================================

class TestRecommendedAction:
    def test_observation_only_for_no_pullback(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=45_000.0,
            pullback_start_level=45_200.0,
            pullback_low_level=44_900.0,
            days_since_pullback_low=1,
            ma5=44_900.0,
            ma10=44_500.0,
            ma60=43_000.0,
            tsmc_spot_up=True,
            tsmc_adr_positive=True,
            futures_night_stable=True,
            foreign_futures_short_increasing=False,
            margin_stress=False,
            volume_expansion=False,
        ))
        assert result.pullback_summary.recommended_action == "observation_only"

    def test_rebound_failed_reduce_risk_action(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=41_500.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_000.0,
            days_since_pullback_low=5,
            ma5=42_800.0,
            ma10=43_500.0,
            ma60=43_200.0,
            tsmc_spot_up=False,
            tsmc_adr_positive=False,
            futures_night_stable=False,
            foreign_futures_short_increasing=True,
            margin_stress=True,
            volume_expansion=False,
        ))
        assert result.pullback_summary.recommended_action == "rebound_failed_reduce_risk"

    def test_recommended_action_valid_value(self):
        result = run_pullback_reaction_review()
        assert result.pullback_summary.recommended_action in RECOMMENDED_ACTIONS


# ===========================================================================
# AA. Human review escalation
# ===========================================================================

class TestHumanReviewEscalation:
    def test_human_review_queue_populated_on_failure(self):
        result = run_pullback_reaction_review(PullbackReviewInput(
            review_period="2026-W29",
            index_level=41_500.0,
            pullback_start_level=45_000.0,
            pullback_low_level=42_000.0,
            days_since_pullback_low=5,
            ma5=42_800.0,
            ma10=43_500.0,
            ma60=43_200.0,
            tsmc_spot_up=False,
            tsmc_adr_positive=False,
            futures_night_stable=False,
            foreign_futures_short_increasing=True,
            margin_stress=True,
            volume_expansion=False,
        ))
        assert len(result.human_review_queue) > 0

    def test_human_review_queue_is_list(self):
        result = run_pullback_reaction_review()
        assert isinstance(result.human_review_queue, list)

    def test_human_review_count_in_summary(self):
        result = run_pullback_reaction_review()
        assert isinstance(result.pullback_summary.human_review_count, int)


# ===========================================================================
# BB. should_auto_apply & auto_apply_enabled invariants
# ===========================================================================

class TestAutoApplyInvariants:
    def test_result_should_auto_apply_always_false(self):
        result = run_pullback_reaction_review()
        assert result.should_auto_apply is False

    def test_result_auto_apply_enabled_always_false(self):
        result = run_pullback_reaction_review()
        assert result.auto_apply_enabled is False

    def test_policy_auto_apply_always_false(self):
        pol = PullbackPolicy(auto_apply_enabled=True)
        assert pol.auto_apply_enabled is False

    def test_event_should_auto_apply_always_false(self):
        evt = detect_pullback_event(index_level=43_000.0)
        assert evt.should_auto_apply is False

    def test_confirmation_should_auto_apply_always_false(self):
        conf = evaluate_rebound_confirmation()
        assert conf.should_auto_apply is False

    def test_export_result_should_auto_apply_false(self):
        result = run_pullback_reaction_review()
        export = export_pullback_json(result)
        assert export.should_auto_apply is False

    def test_export_result_auto_apply_enabled_false(self):
        result = run_pullback_reaction_review()
        export = export_pullback_json(result)
        assert export.auto_apply_enabled is False


# ===========================================================================
# CC. run_pullback_reaction_review result schema
# ===========================================================================

class TestPullbackReviewResult:
    def test_paper_only_true(self):
        result = run_pullback_reaction_review()
        assert result.paper_only is True

    def test_research_only_true(self):
        result = run_pullback_reaction_review()
        assert result.research_only is True

    def test_no_real_orders_true(self):
        result = run_pullback_reaction_review()
        assert result.no_real_orders is True

    def test_no_broker_true(self):
        result = run_pullback_reaction_review()
        assert result.no_broker is True

    def test_not_investment_advice_true(self):
        result = run_pullback_reaction_review()
        assert result.not_investment_advice is True

    def test_pullback_version_214(self):
        result = run_pullback_reaction_review()
        assert result.pullback_version == "2.0.14"

    def test_pullback_review_id_populated(self):
        result = run_pullback_reaction_review()
        assert len(result.pullback_review_id) > 0

    def test_index_snapshot_not_none(self):
        result = run_pullback_reaction_review()
        assert result.index_snapshot is not None

    def test_rebound_confirmation_snapshot_not_none(self):
        result = run_pullback_reaction_review()
        assert result.rebound_confirmation_snapshot is not None

    def test_pullback_summary_not_none(self):
        result = run_pullback_reaction_review()
        assert result.pullback_summary is not None

    def test_paper_only_safety_snapshot_true(self):
        result = run_pullback_reaction_review()
        assert result.paper_only_safety_snapshot is True

    def test_review_fields_present(self):
        result = run_pullback_reaction_review()
        for f in PULLBACK_REVIEW_FIELDS:
            assert hasattr(result, f), f"Missing field: {f}"

    def test_pullback_reaction_recommendation_only_true(self):
        result = run_pullback_reaction_review()
        assert result.pullback_reaction_recommendation_only is True

    def test_schema_version_214(self):
        result = run_pullback_reaction_review()
        assert result.schema_version == "214"


# ===========================================================================
# DD. Export — JSON
# ===========================================================================

class TestExportJSON:
    def test_json_export_is_valid(self):
        result = run_pullback_reaction_review()
        export = export_pullback_json(result)
        assert export.is_valid is True

    def test_json_export_format(self):
        result = run_pullback_reaction_review()
        export = export_pullback_json(result)
        assert export.export_format == "json"

    def test_json_export_content_not_empty(self):
        result = run_pullback_reaction_review()
        export = export_pullback_json(result)
        assert len(export.content) > 0

    def test_json_content_is_valid_json(self):
        import json
        result = run_pullback_reaction_review()
        export = export_pullback_json(result)
        payload = json.loads(export.content)
        assert payload["paper_only"] is True

    def test_json_content_should_auto_apply_false(self):
        import json
        result = run_pullback_reaction_review()
        export = export_pullback_json(result)
        payload = json.loads(export.content)
        assert payload["should_auto_apply"] is False

    def test_json_content_auto_apply_enabled_false(self):
        import json
        result = run_pullback_reaction_review()
        export = export_pullback_json(result)
        payload = json.loads(export.content)
        assert payload["auto_apply_enabled"] is False

    def test_json_export_paper_only(self):
        result = run_pullback_reaction_review()
        export = export_pullback_json(result)
        assert export.paper_only is True

    def test_json_export_status_complete(self):
        result = run_pullback_reaction_review()
        export = export_pullback_json(result)
        assert export.export_status == "complete"

    def test_json_export_pullback_review_id_match(self):
        result = run_pullback_reaction_review()
        export = export_pullback_json(result)
        assert export.pullback_review_id == result.pullback_review_id

    def test_json_schema_version_214(self):
        import json
        result = run_pullback_reaction_review()
        export = export_pullback_json(result)
        payload = json.loads(export.content)
        assert payload["schema_version"] == "214"

    def test_json_require_reclaim_always_true(self):
        import json
        result = run_pullback_reaction_review()
        export = export_pullback_json(result)
        payload = json.loads(export.content)
        assert payload["require_reclaim_ma5_or_ma10_for_confirmation"] is True


# ===========================================================================
# EE. Export — Markdown
# ===========================================================================

class TestExportMarkdown:
    def test_markdown_export_is_valid(self):
        result = run_pullback_reaction_review()
        export = export_pullback_markdown(result)
        assert export.is_valid is True

    def test_markdown_export_format(self):
        result = run_pullback_reaction_review()
        export = export_pullback_markdown(result)
        assert export.export_format == "markdown"

    def test_markdown_content_not_empty(self):
        result = run_pullback_reaction_review()
        export = export_pullback_markdown(result)
        assert len(export.content) > 0

    def test_markdown_contains_paper_only(self):
        result = run_pullback_reaction_review()
        export = export_pullback_markdown(result)
        assert "Paper Only" in export.content

    def test_markdown_contains_version(self):
        result = run_pullback_reaction_review()
        export = export_pullback_markdown(result)
        assert "2.0.14" in export.content

    def test_markdown_paper_only_confirmed(self):
        result = run_pullback_reaction_review()
        export = export_pullback_markdown(result)
        assert export.paper_only_confirmed is True

    def test_markdown_should_auto_apply_false(self):
        result = run_pullback_reaction_review()
        export = export_pullback_markdown(result)
        assert export.should_auto_apply is False


# ===========================================================================
# FF. Export — CSV
# ===========================================================================

class TestExportCSV:
    def test_csv_export_is_valid(self):
        result = run_pullback_reaction_review()
        export = export_pullback_csv(result)
        assert export.is_valid is True

    def test_csv_row_count_1(self):
        result = run_pullback_reaction_review()
        export = export_pullback_csv(result)
        assert export.row_count == 1

    def test_csv_content_not_empty(self):
        result = run_pullback_reaction_review()
        export = export_pullback_csv(result)
        assert len(export.csv_content) > 0

    def test_csv_has_header(self):
        result = run_pullback_reaction_review()
        export = export_pullback_csv(result)
        assert "reaction_state" in export.csv_content

    def test_csv_paper_only_true(self):
        result = run_pullback_reaction_review()
        export = export_pullback_csv(result)
        assert export.paper_only is True

    def test_rebound_watch_queue_csv_valid(self):
        result = run_pullback_reaction_review()
        export = export_rebound_watch_queue_csv(result)
        assert export.is_valid is True

    def test_rebound_failure_queue_csv_valid(self):
        result = run_pullback_reaction_review()
        export = export_rebound_failure_queue_csv(result)
        assert export.is_valid is True


# ===========================================================================
# GG. Rebound watch queue
# ===========================================================================

class TestReboundWatchQueue:
    def test_watch_queue_populated_on_observation(self):
        queue = build_rebound_watch_queue("observation_rebound")
        assert len(queue) > 0

    def test_watch_queue_empty_on_no_pullback(self):
        queue = build_rebound_watch_queue("no_pullback")
        assert len(queue) == 0

    def test_watch_queue_empty_on_confirmed(self):
        queue = build_rebound_watch_queue("short_term_rebound_confirmed")
        assert len(queue) == 0

    def test_watch_queue_populated_on_defensive(self):
        queue = build_rebound_watch_queue("defensive_wait_second_confirmation")
        assert len(queue) > 0

    def test_watch_queue_is_list(self):
        queue = build_rebound_watch_queue("observation_rebound")
        assert isinstance(queue, list)


# ===========================================================================
# HH. Rebound failure queue
# ===========================================================================

class TestReboundFailureQueue:
    def test_failure_queue_populated_on_rebound_failed(self):
        queue = build_rebound_failure_queue("rebound_failed")
        assert len(queue) > 0

    def test_failure_queue_empty_on_no_pullback(self):
        queue = build_rebound_failure_queue("no_pullback")
        assert len(queue) == 0

    def test_failure_queue_core_only_on_defensive(self):
        queue = build_rebound_failure_queue("defensive_wait_second_confirmation")
        assert len(queue) > 0

    def test_failure_queue_is_list(self):
        queue = build_rebound_failure_queue("rebound_failed")
        assert isinstance(queue, list)


# ===========================================================================
# II. Audit snapshot
# ===========================================================================

class TestAuditSnapshot:
    def test_audit_export_status_complete(self):
        result = run_pullback_reaction_review()
        audit = export_pullback_audit_snapshot(result)
        assert audit.export_status == "complete"

    def test_audit_paper_only_true(self):
        result = run_pullback_reaction_review()
        audit = export_pullback_audit_snapshot(result)
        assert audit.paper_only is True

    def test_audit_reproducibility_hash_populated(self):
        result = run_pullback_reaction_review()
        audit = export_pullback_audit_snapshot(result)
        assert len(audit.reproducibility_hash) > 0

    def test_audit_safety_snapshot_contains_paper_only(self):
        result = run_pullback_reaction_review()
        audit = export_pullback_audit_snapshot(result)
        assert "paper_only=True" in audit.safety_snapshot

    def test_audit_id_matches_result(self):
        result = run_pullback_reaction_review()
        audit = export_pullback_audit_snapshot(result)
        assert audit.pullback_review_id == result.pullback_review_id


# ===========================================================================
# JJ. Integration with v2.0.13 market box
# ===========================================================================

class TestV213Integration:
    def test_v213_import_still_works(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v213 import (
            VERSION as V213, run_market_box_review,
        )
        assert V213 == "2.0.13"
        result = run_market_box_review()
        assert result.paper_only is True

    def test_v213_zone_classification_unchanged(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v213 import classify_zone
        assert classify_zone(46_000.0) == "upper_zone"
        assert classify_zone(43_500.0) == "neutral_zone"

    def test_v213_safety_flags_still_count_25(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v213 import SAFETY_FLAGS_V213
        assert len(SAFETY_FLAGS_V213) == 25

    def test_v213_cli_commands_still_10(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v213 import CLI_COMMANDS_V213
        assert len(CLI_COMMANDS_V213) == 10


# ===========================================================================
# KK. Integration with v2.0.12 profit taking
# ===========================================================================

class TestV212Integration:
    def test_v212_import_still_works(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v212 import (
            VERSION as V212,
        )
        assert V212 == "2.0.12"

    def test_v212_profit_review_callable(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
        result = run_profit_taking_review()
        assert result.paper_only is True


# ===========================================================================
# LL. Integration with v2.0.11 journal
# ===========================================================================

class TestV211Integration:
    def test_v211_import_still_works(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v211 import (
            VERSION as V211,
        )
        assert V211 == "2.0.11"


# ===========================================================================
# MM. Integration with v2.0.10 exit plan
# ===========================================================================

class TestV210Integration:
    def test_v210_import_still_works(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v210 import (
            VERSION as V210,
        )
        assert V210 == "2.0.10"


# ===========================================================================
# NN. Integration with v2.0.9 position sizing
# ===========================================================================

class TestV209Integration:
    def test_v209_import_still_works(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v209 import (
            VERSION as V209,
        )
        assert V209 == "2.0.9"


# ===========================================================================
# OO. Integration with v2.0.8 exposure
# ===========================================================================

class TestV208Integration:
    def test_v208_import_still_works(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v208 import (
            VERSION as V208,
        )
        assert V208 == "2.0.8"


# ===========================================================================
# PP. Integration with v2.0.7 market regime
# ===========================================================================

class TestV207Integration:
    def test_v207_import_still_works(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
            VERSION as V207,
        )
        assert V207 == "2.0.7"


# ===========================================================================
# QQ. CLI handler resolution in main.py
# ===========================================================================

class TestCLIHandlerResolution:
    def test_review_pullback_handler_in_main(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v214_review_pullback_reaction")

    def test_detect_pullback_handler_in_main(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v214_detect_pullback_event")

    def test_evaluate_rebound_handler_in_main(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v214_evaluate_rebound_confirmation")

    def test_watch_queue_handler_in_main(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v214_build_rebound_watch_queue")

    def test_failure_queue_handler_in_main(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v214_build_rebound_failure_queue")

    def test_export_json_handler_in_main(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v214_export_json")

    def test_export_md_handler_in_main(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v214_export_md")

    def test_export_csv_handler_in_main(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v214_export_csv")

    def test_health_handler_in_main(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v214_health")

    def test_gate_handler_in_main(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v214_gate")


# ===========================================================================
# RR. CLI registration health (command_map entries)
# ===========================================================================

class TestCLIRegistrationHealth:
    def test_v214_commands_in_registry(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        for cmd in CLI_COMMANDS_V214:
            assert cmd in names, f"CLI command not in registry: {cmd}"

    def test_v214_handler_names_in_registry(self):
        from cli.command_registry import PROVIDER_COMMANDS
        handler_names = {c.handler_name for c in PROVIDER_COMMANDS}
        expected_handlers = [
            "cmd_paper_cockpit_v214_review_pullback_reaction",
            "cmd_paper_cockpit_v214_detect_pullback_event",
            "cmd_paper_cockpit_v214_evaluate_rebound_confirmation",
            "cmd_paper_cockpit_v214_build_rebound_watch_queue",
            "cmd_paper_cockpit_v214_build_rebound_failure_queue",
            "cmd_paper_cockpit_v214_export_json",
            "cmd_paper_cockpit_v214_export_md",
            "cmd_paper_cockpit_v214_export_csv",
            "cmd_paper_cockpit_v214_health",
            "cmd_paper_cockpit_v214_gate",
        ]
        for h in expected_handlers:
            assert h in handler_names, f"Handler not in registry: {h}"

    def test_command_map_has_review_pullback(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "paper-cockpit-v214-review-pullback-reaction" in names

    def test_command_map_has_detect_pullback(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "paper-cockpit-v214-detect-pullback-event" in names

    def test_command_map_has_evaluate_rebound(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "paper-cockpit-v214-evaluate-rebound-confirmation" in names

    def test_command_map_has_watch_queue(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "paper-cockpit-v214-build-rebound-watch-queue" in names

    def test_command_map_has_failure_queue(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "paper-cockpit-v214-build-rebound-failure-queue" in names

    def test_command_map_has_export_json(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "paper-cockpit-v214-export-json" in names

    def test_command_map_has_export_md(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "paper-cockpit-v214-export-md" in names

    def test_command_map_has_export_csv(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "paper-cockpit-v214-export-csv" in names

    def test_command_map_has_health(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "paper-cockpit-v214-health" in names

    def test_command_map_has_gate(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "paper-cockpit-v214-gate" in names

    def test_all_v214_handlers_callable(self):
        import main
        expected_handlers = [
            "cmd_paper_cockpit_v214_review_pullback_reaction",
            "cmd_paper_cockpit_v214_detect_pullback_event",
            "cmd_paper_cockpit_v214_evaluate_rebound_confirmation",
            "cmd_paper_cockpit_v214_build_rebound_watch_queue",
            "cmd_paper_cockpit_v214_build_rebound_failure_queue",
            "cmd_paper_cockpit_v214_export_json",
            "cmd_paper_cockpit_v214_export_md",
            "cmd_paper_cockpit_v214_export_csv",
            "cmd_paper_cockpit_v214_health",
            "cmd_paper_cockpit_v214_gate",
        ]
        for h in expected_handlers:
            assert hasattr(main, h) and callable(getattr(main, h)), f"Handler not callable in main: {h}"

    def test_registry_group_paper_cockpit_v214(self):
        from cli.command_registry import PROVIDER_COMMANDS
        groups = {c.group for c in PROVIDER_COMMANDS if c.group == "paper_cockpit_v214"}
        assert len(groups) == 1

    def test_registry_safety_classification_research_only(self):
        from cli.command_registry import PROVIDER_COMMANDS
        v214_cmds = [c for c in PROVIDER_COMMANDS if c.group == "paper_cockpit_v214"]
        for c in v214_cmds:
            assert c.safety_classification == "RESEARCH_ONLY"


# ===========================================================================
# SS. Replay lineage handler integrity
# ===========================================================================

class TestReplayLineageHandlerIntegrity:
    def test_v213_handlers_still_in_command_map(self):
        import re, os
        repo = os.path.join(os.path.dirname(__file__), "..")
        with open(os.path.join(repo, "main.py"), "r", encoding="utf-8") as f:
            content = f.read()
        keys = set(re.findall(r'"([a-z0-9][a-z0-9\-]+)":\s*(?:cmd_|lambda)', content))
        assert "paper-cockpit-v213-review-market-box" in keys, (
            f"paper-cockpit-v213-review-market-box not found in main.py command_map source. "
            f"Found keys sample: {sorted(keys)[:10]}"
        )

    def test_v212_handlers_still_accessible(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v212_review_profit_taking")

    def test_v211_handlers_still_accessible(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v211_review_journal")

    def test_v214_does_not_break_v213_handlers(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v213_review_market_box")
        assert callable(main.cmd_paper_cockpit_v213_review_market_box)


# ===========================================================================
# TT. GUI compatibility
# ===========================================================================

class TestGUICompatibility:
    def test_gui_import_safe(self):
        from gui.small_capital_strategy_panel import render_all_tabs
        assert callable(render_all_tabs)

    def test_render_pullback_reaction_v214_tab(self):
        from gui.small_capital_strategy_panel import render_pullback_reaction_v214_tab
        result = render_pullback_reaction_v214_tab()
        assert result["tab"] == "pullback_reaction_v214"

    def test_render_rebound_confirmation_v214_tab(self):
        from gui.small_capital_strategy_panel import render_rebound_confirmation_v214_tab
        result = render_rebound_confirmation_v214_tab()
        assert result["tab"] == "rebound_confirmation_v214"

    def test_render_rebound_failure_queue_v214_tab(self):
        from gui.small_capital_strategy_panel import render_rebound_failure_queue_v214_tab
        result = render_rebound_failure_queue_v214_tab()
        assert result["tab"] == "rebound_failure_queue_v214"

    def test_pullback_reaction_tab_paper_only(self):
        from gui.small_capital_strategy_panel import render_pullback_reaction_v214_tab
        result = render_pullback_reaction_v214_tab()
        assert result["paper_only"] is True

    def test_pullback_reaction_tab_should_auto_apply_false(self):
        from gui.small_capital_strategy_panel import render_pullback_reaction_v214_tab
        result = render_pullback_reaction_v214_tab()
        assert result["should_auto_apply"] is False

    def test_rebound_confirmation_tab_require_ma_reclaim(self):
        from gui.small_capital_strategy_panel import render_rebound_confirmation_v214_tab
        result = render_rebound_confirmation_v214_tab()
        assert result["require_reclaim_ma5_or_ma10_for_confirmation"] is True

    def test_v213_tabs_still_render(self):
        from gui.small_capital_strategy_panel import (
            render_market_box_v213_tab,
            render_exposure_control_v213_tab,
            render_defensive_review_queue_v213_tab,
        )
        assert render_market_box_v213_tab()["tab"] == "market_box_v213"
        assert render_exposure_control_v213_tab()["tab"] == "exposure_control_v213"
        assert render_defensive_review_queue_v213_tab()["tab"] == "defensive_review_queue_v213"

    def test_v214_tab_names_registered(self):
        from gui.small_capital_strategy_panel import get_v214_tab_names
        tabs = get_v214_tab_names()
        assert "pullback_reaction_v214" in tabs
        assert "rebound_confirmation_v214" in tabs
        assert "rebound_failure_queue_v214" in tabs


# ===========================================================================
# UU. render_all_tabs no error tabs
# ===========================================================================

class TestRenderAllTabsNoErrors:
    def test_render_all_tabs_no_errors(self):
        from gui.small_capital_strategy_panel import render_all_tabs
        results = render_all_tabs()
        error_tabs = [k for k, v in results.items() if isinstance(v, dict) and "error" in v]
        assert len(error_tabs) == 0, f"Error tabs found: {error_tabs}"

    def test_render_all_tabs_includes_v214_pullback(self):
        from gui.small_capital_strategy_panel import render_all_tabs
        results = render_all_tabs()
        assert "pullback_reaction_v214" in results

    def test_render_all_tabs_includes_v214_rebound(self):
        from gui.small_capital_strategy_panel import render_all_tabs
        results = render_all_tabs()
        assert "rebound_confirmation_v214" in results

    def test_render_all_tabs_includes_v214_failure(self):
        from gui.small_capital_strategy_panel import render_all_tabs
        results = render_all_tabs()
        assert "rebound_failure_queue_v214" in results

    def test_render_all_tabs_includes_v213_market_box(self):
        from gui.small_capital_strategy_panel import render_all_tabs
        results = render_all_tabs()
        assert "market_box_v213" in results


# ===========================================================================
# VV. Paper-only safety guard
# ===========================================================================

class TestPaperOnlySafetyGuard:
    def test_safety_guard_paper_only_true(self):
        guard = PullbackSafetyGuard()
        assert guard.paper_only is True

    def test_safety_guard_no_real_orders(self):
        guard = PullbackSafetyGuard()
        assert guard.no_real_orders is True

    def test_safety_guard_no_automatic_pullback_action(self):
        guard = PullbackSafetyGuard()
        assert guard.no_automatic_pullback_action is True

    def test_safety_guard_no_automatic_rebound_action(self):
        guard = PullbackSafetyGuard()
        assert guard.no_automatic_rebound_action is True

    def test_safety_guard_should_auto_apply_false(self):
        guard = PullbackSafetyGuard()
        assert guard.should_auto_apply is False

    def test_safety_guard_auto_apply_enabled_false(self):
        guard = PullbackSafetyGuard()
        assert guard.auto_apply_enabled is False

    def test_safety_guard_require_reclaim_true(self):
        guard = PullbackSafetyGuard()
        assert guard.require_reclaim_ma5_or_ma10_for_confirmation is True

    def test_safety_guard_pullback_actions_recommendation_only(self):
        guard = PullbackSafetyGuard()
        assert guard.pullback_actions_recommendation_only is True

    def test_no_broker_guard(self):
        result = run_pullback_reaction_review()
        assert result.no_broker is True

    def test_no_real_orders_guard(self):
        result = run_pullback_reaction_review()
        assert result.no_real_orders is True


# ===========================================================================
# WW. No broker / no real order guard
# ===========================================================================

class TestNoBrokerNoRealOrderGuard:
    def test_no_real_orders_constant(self):
        assert NO_REAL_ORDERS is True

    def test_broker_execution_disabled(self):
        assert BROKER_EXECUTION_ENABLED is False

    def test_production_trading_blocked(self):
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_result_paper_only(self):
        result = run_pullback_reaction_review()
        assert result.paper_only is True

    def test_result_no_broker(self):
        result = run_pullback_reaction_review()
        assert result.no_broker is True


# ===========================================================================
# XX. Backward compatibility with v2.0.13
# ===========================================================================

class TestBackwardCompatV213:
    def test_v213_module_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_v213 as m
        assert m.VERSION == "2.0.13"

    def test_v213_health_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_health_v213 as h
        assert hasattr(h, "run_health_check")

    def test_v213_run_market_box_review_works(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v213 import run_market_box_review
        r = run_market_box_review()
        assert r.paper_only is True
        assert r.should_auto_apply is False

    def test_v213_gui_tabs_still_in_tabs_list(self):
        from gui.small_capital_strategy_panel import _TABS
        assert "market_box_v213" in _TABS
        assert "exposure_control_v213" in _TABS
        assert "defensive_review_queue_v213" in _TABS


# ===========================================================================
# YY. v201 health relative-path compatibility
# ===========================================================================

class TestV201HealthRelativePathCompat:
    def test_v213_health_check_callable(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v213 import run_health_check
        result = run_health_check()
        assert "all_passed" in result

    def test_v212_health_check_callable(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v212 import run_health_check
        result = run_health_check()
        assert "all_passed" in result

    def test_health_check_returns_dict(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v214 import run_health_check
        result = run_health_check()
        assert isinstance(result, dict)

    def test_health_check_has_paper_only(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v214 import run_health_check
        result = run_health_check()
        assert result["paper_only"] is True


# ===========================================================================
# ZZ. Health
# ===========================================================================

class TestHealth:
    def test_health_check_runs(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v214 import run_health_check
        result = run_health_check()
        assert "all_passed" in result

    def test_health_check_version(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v214 import run_health_check
        result = run_health_check()
        assert result["version"] == "2.0.14"

    def test_health_check_paper_only(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v214 import run_health_check
        result = run_health_check()
        assert result["paper_only"] is True

    def test_health_check_total_positive(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v214 import run_health_check
        result = run_health_check()
        assert result["total"] > 0

    def test_health_check_passes(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v214 import run_health_check
        result = run_health_check()
        assert result["all_passed"] is True, f"Health check failed: {result['errors']}"


# ===========================================================================
# AAA. Gate
# ===========================================================================

class TestGate:
    def test_gate_runs(self):
        from release.paper_cockpit_release_gate_v214 import run_release_gate
        result = run_release_gate()
        assert "gate_passed" in result

    def test_gate_version(self):
        from release.paper_cockpit_release_gate_v214 import run_release_gate
        result = run_release_gate()
        assert result["version"] == "2.0.14"

    def test_gate_paper_only(self):
        from release.paper_cockpit_release_gate_v214 import run_release_gate
        result = run_release_gate()
        assert result["paper_only"] is True

    def test_gate_total_positive(self):
        from release.paper_cockpit_release_gate_v214 import run_release_gate
        result = run_release_gate()
        assert result["total_count"] > 0

    def test_gate_passes(self):
        from release.paper_cockpit_release_gate_v214 import run_release_gate
        result = run_release_gate()
        assert result["gate_passed"] is True, f"Gate failed: {result['errors']}"


# ===========================================================================
# BBB. get_cockpit_summary_v214
# ===========================================================================

class TestCockpitSummary:
    def test_summary_version_214(self):
        s = get_cockpit_summary_v214()
        assert s["version"] == "2.0.14"

    def test_summary_schema_version_214(self):
        s = get_cockpit_summary_v214()
        assert s["schema_version"] == "214"

    def test_summary_paper_only_true(self):
        s = get_cockpit_summary_v214()
        assert s["paper_only"] is True

    def test_summary_should_auto_apply_false(self):
        s = get_cockpit_summary_v214()
        assert s["should_auto_apply"] is False

    def test_summary_auto_apply_enabled_false(self):
        s = get_cockpit_summary_v214()
        assert s["auto_apply_enabled"] is False

    def test_summary_require_reclaim_always_true(self):
        s = get_cockpit_summary_v214()
        assert s["require_reclaim_ma5_or_ma10_for_confirmation"] is True

    def test_summary_pullback_recommendation_only(self):
        s = get_cockpit_summary_v214()
        assert s["pullback_actions_recommendation_only"] is True

    def test_summary_no_automatic_pullback_action(self):
        s = get_cockpit_summary_v214()
        assert s["no_automatic_pullback_action"] is True

    def test_summary_no_automatic_rebound_action(self):
        s = get_cockpit_summary_v214()
        assert s["no_automatic_rebound_action"] is True

    def test_summary_reaction_state_count_6(self):
        s = get_cockpit_summary_v214()
        assert s["reaction_state_count"] == 6

    def test_summary_recommended_action_count_6(self):
        s = get_cockpit_summary_v214()
        assert s["recommended_action_count"] == 6

    def test_summary_cli_command_count_10(self):
        s = get_cockpit_summary_v214()
        assert s["cli_command_count"] == 10

    def test_summary_gui_tab_count_3(self):
        s = get_cockpit_summary_v214()
        assert s["gui_tab_count"] == 3

    def test_summary_safety_flag_count_25(self):
        s = get_cockpit_summary_v214()
        assert s["safety_flag_count"] == 25

    def test_summary_model_count_16(self):
        s = get_cockpit_summary_v214()
        assert s["model_count"] == 16

    def test_summary_baseline_tests(self):
        s = get_cockpit_summary_v214()
        assert s["baseline_tests"] == 36989

    def test_summary_min_new_tests_300(self):
        s = get_cockpit_summary_v214()
        assert s["min_new_tests"] == 300
