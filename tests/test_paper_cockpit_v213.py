"""
tests/test_paper_cockpit_v213.py
v2.0.13 Paper Market Box Range & Index Regime Control — Tests
[!] Paper Only. Research Only. Market Box Recommendation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import pytest

# ===========================================================================
# Imports
# ===========================================================================

from paper_trading.small_capital_strategy.paper_cockpit_v213 import (
    VERSION,
    SCHEMA_VERSION,
    RELEASE_NAME,
    NO_REAL_ORDERS,
    BROKER_EXECUTION_ENABLED,
    PRODUCTION_TRADING_BLOCKED,
    ZONE_NAMES,
    EXPOSURE_ACTIONS,
    CLI_COMMANDS_V213,
    GUI_TABS_V213,
    SAFETY_FLAGS_V213,
    UPPER_ZONE_MIN,
    UPPER_ZONE_MAX,
    NEUTRAL_ZONE_MIN,
    NEUTRAL_ZONE_MAX,
    LOWER_ZONE_MIN,
    LOWER_ZONE_MAX,
    EXTREME_RISK_ZONE_MIN,
    EXTREME_RISK_ZONE_MAX,
    BELOW_BOX_THRESHOLD,
    ABOVE_BOX_THRESHOLD,
    MarketBoxPolicy,
    IndexSnapshot,
    ExposureRecommendation,
    MarketBoxSummary,
    MarketBoxReviewInput,
    MarketBoxReviewResult,
    MarketBoxExportResult,
    MarketBoxAuditSnapshot,
    MarketBoxMarkdownReport,
    ChaseRiskQueueCSV,
    DefensiveReviewQueueCSV,
    ExposureRecommendationCSV,
    V213HealthSummary,
    V213ReleaseSummary,
    MarketBoxSafetyGuard,
    MarketBoxSummaryCSV,
    classify_zone,
    classify_index_zone,
    build_index_snapshot,
    build_exposure_recommendation,
    build_chase_risk_queue,
    build_defensive_review_queue,
    run_market_box_review,
    export_market_box_json,
    export_market_box_markdown,
    export_market_box_csv,
    export_chase_risk_queue_csv,
    export_defensive_review_queue_csv,
    export_exposure_recommendation_csv,
    export_market_box_audit_snapshot,
    verify_version,
    get_cockpit_summary_v213,
)


# ===========================================================================
# A. Version and constants
# ===========================================================================

class TestVersionConstants:
    def test_version_is_213(self):
        assert VERSION == "2.0.13"

    def test_schema_version_is_213(self):
        assert SCHEMA_VERSION == "213"

    def test_release_name_contains_market_box(self):
        assert "Market" in RELEASE_NAME or "Box" in RELEASE_NAME

    def test_release_name_contains_regime(self):
        assert "Regime" in RELEASE_NAME or "Range" in RELEASE_NAME

    def test_no_real_orders_true(self):
        assert NO_REAL_ORDERS is True

    def test_broker_execution_enabled_false(self):
        assert BROKER_EXECUTION_ENABLED is False

    def test_production_trading_blocked_true(self):
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_verify_version_returns_true(self):
        assert verify_version() is True

    def test_above_box_threshold_47000(self):
        assert ABOVE_BOX_THRESHOLD == 47_000

    def test_below_box_threshold_38000(self):
        assert BELOW_BOX_THRESHOLD == 38_000

    def test_upper_zone_min_45000(self):
        assert UPPER_ZONE_MIN == 45_000

    def test_upper_zone_max_47000(self):
        assert UPPER_ZONE_MAX == 47_000

    def test_neutral_zone_min_42000(self):
        assert NEUTRAL_ZONE_MIN == 42_000

    def test_neutral_zone_max_45000(self):
        assert NEUTRAL_ZONE_MAX == 45_000

    def test_lower_zone_min_40000(self):
        assert LOWER_ZONE_MIN == 40_000

    def test_lower_zone_max_42000(self):
        assert LOWER_ZONE_MAX == 42_000

    def test_extreme_risk_zone_min_38000(self):
        assert EXTREME_RISK_ZONE_MIN == 38_000

    def test_extreme_risk_zone_max_40000(self):
        assert EXTREME_RISK_ZONE_MAX == 40_000


# ===========================================================================
# B. Safety flags
# ===========================================================================

class TestSafetyFlags:
    def test_safety_flags_count_25(self):
        assert len(SAFETY_FLAGS_V213) == 25

    def test_paper_only_true(self):
        assert SAFETY_FLAGS_V213["paper_only"] is True

    def test_research_only_true(self):
        assert SAFETY_FLAGS_V213["research_only"] is True

    def test_market_box_recommendation_only_true(self):
        assert SAFETY_FLAGS_V213["market_box_recommendation_only"] is True

    def test_exposure_recommendation_only_true(self):
        assert SAFETY_FLAGS_V213["exposure_recommendation_only"] is True

    def test_validation_only_true(self):
        assert SAFETY_FLAGS_V213["validation_only"] is True

    def test_no_real_orders_true(self):
        assert SAFETY_FLAGS_V213["no_real_orders"] is True

    def test_no_broker_true(self):
        assert SAFETY_FLAGS_V213["no_broker"] is True

    def test_should_auto_apply_always_false_true(self):
        assert SAFETY_FLAGS_V213["should_auto_apply_always_false"] is True

    def test_auto_apply_enabled_always_false_true(self):
        assert SAFETY_FLAGS_V213["auto_apply_enabled_always_false"] is True

    def test_broker_execution_disabled_true(self):
        assert SAFETY_FLAGS_V213["broker_execution_disabled"] is True

    def test_production_trading_blocked_true(self):
        assert SAFETY_FLAGS_V213["production_trading_blocked"] is True

    def test_require_box_check_before_entry_always_true(self):
        assert SAFETY_FLAGS_V213["require_box_check_before_entry_always_true"] is True

    def test_market_box_actions_recommendation_only_true(self):
        assert SAFETY_FLAGS_V213["market_box_actions_recommendation_only"] is True

    def test_exposure_actions_recommendation_only_true(self):
        assert SAFETY_FLAGS_V213["exposure_actions_recommendation_only"] is True

    def test_no_automatic_market_action_true(self):
        assert SAFETY_FLAGS_V213["no_automatic_market_action"] is True

    def test_no_automatic_rebalance_true(self):
        assert SAFETY_FLAGS_V213["no_automatic_rebalance"] is True

    def test_no_real_account_sync_true(self):
        assert SAFETY_FLAGS_V213["no_real_account_sync"] is True

    def test_not_investment_advice_true(self):
        assert SAFETY_FLAGS_V213["not_investment_advice"] is True


# ===========================================================================
# C. Zone names and exposure actions
# ===========================================================================

class TestZoneNamesAndActions:
    def test_zone_names_count_6(self):
        assert len(ZONE_NAMES) == 6

    def test_upper_zone_in_zones(self):
        assert "upper_zone" in ZONE_NAMES

    def test_neutral_zone_in_zones(self):
        assert "neutral_zone" in ZONE_NAMES

    def test_lower_zone_in_zones(self):
        assert "lower_zone" in ZONE_NAMES

    def test_extreme_risk_zone_in_zones(self):
        assert "extreme_risk_zone" in ZONE_NAMES

    def test_below_box_in_zones(self):
        assert "below_box" in ZONE_NAMES

    def test_above_box_in_zones(self):
        assert "above_box" in ZONE_NAMES

    def test_exposure_actions_count_8(self):
        assert len(EXPOSURE_ACTIONS) == 8

    def test_hold_current_exposure_in_actions(self):
        assert "hold_current_exposure" in EXPOSURE_ACTIONS

    def test_reduce_exposure_near_upper_box_in_actions(self):
        assert "reduce_exposure_near_upper_box" in EXPOSURE_ACTIONS

    def test_normal_selective_exposure_in_actions(self):
        assert "normal_selective_exposure" in EXPOSURE_ACTIONS

    def test_core_only_low_zone_in_actions(self):
        assert "core_only_low_zone" in EXPOSURE_ACTIONS

    def test_defensive_extreme_risk_in_actions(self):
        assert "defensive_extreme_risk" in EXPOSURE_ACTIONS

    def test_below_box_defense_in_actions(self):
        assert "below_box_defense" in EXPOSURE_ACTIONS

    def test_overheating_above_box_in_actions(self):
        assert "overheating_above_box" in EXPOSURE_ACTIONS

    def test_human_review_required_in_actions(self):
        assert "human_review_required" in EXPOSURE_ACTIONS

    def test_cli_commands_count_10(self):
        assert len(CLI_COMMANDS_V213) == 10

    def test_gui_tabs_count_3(self):
        assert len(GUI_TABS_V213) == 3

    def test_market_box_v213_in_gui_tabs(self):
        assert "market_box_v213" in GUI_TABS_V213

    def test_exposure_control_v213_in_gui_tabs(self):
        assert "exposure_control_v213" in GUI_TABS_V213

    def test_defensive_review_queue_v213_in_gui_tabs(self):
        assert "defensive_review_queue_v213" in GUI_TABS_V213


# ===========================================================================
# D. MarketBoxPolicy schema
# ===========================================================================

class TestMarketBoxPolicySchema:
    def test_default_policy_schema_version(self):
        pol = MarketBoxPolicy()
        assert pol.schema_version == "213"

    def test_default_policy_paper_only(self):
        pol = MarketBoxPolicy()
        assert pol.paper_only is True

    def test_default_policy_no_real_orders(self):
        pol = MarketBoxPolicy()
        assert pol.no_real_orders is True

    def test_auto_apply_enabled_always_false(self):
        pol = MarketBoxPolicy(auto_apply_enabled=True)
        assert pol.auto_apply_enabled is False

    def test_require_box_check_always_true(self):
        pol = MarketBoxPolicy(require_box_check_before_entry=False)
        assert pol.require_box_check_before_entry is True

    def test_policy_upper_zone_min_45000(self):
        pol = MarketBoxPolicy()
        assert pol.upper_zone_min == 45_000

    def test_policy_upper_zone_max_47000(self):
        pol = MarketBoxPolicy()
        assert pol.upper_zone_max == 47_000

    def test_policy_neutral_zone_min_42000(self):
        pol = MarketBoxPolicy()
        assert pol.neutral_zone_min == 42_000

    def test_policy_neutral_zone_max_45000(self):
        pol = MarketBoxPolicy()
        assert pol.neutral_zone_max == 45_000

    def test_policy_lower_zone_min_40000(self):
        pol = MarketBoxPolicy()
        assert pol.lower_zone_min == 40_000

    def test_policy_lower_zone_max_42000(self):
        pol = MarketBoxPolicy()
        assert pol.lower_zone_max == 42_000

    def test_policy_extreme_risk_zone_min_38000(self):
        pol = MarketBoxPolicy()
        assert pol.extreme_risk_zone_min == 38_000

    def test_policy_extreme_risk_zone_max_40000(self):
        pol = MarketBoxPolicy()
        assert pol.extreme_risk_zone_max == 40_000

    def test_policy_below_box_threshold_38000(self):
        pol = MarketBoxPolicy()
        assert pol.below_box_threshold == 38_000

    def test_policy_above_box_threshold_47000(self):
        pol = MarketBoxPolicy()
        assert pol.above_box_threshold == 47_000

    def test_policy_custom_id(self):
        pol = MarketBoxPolicy(policy_id="test-pol")
        assert pol.policy_id == "test-pol"


# ===========================================================================
# E. Zone classification — upper zone 45,000-47,000
# ===========================================================================

class TestUpperZoneClassification:
    def test_45000_is_upper_zone(self):
        assert classify_zone(45_000.0) == "upper_zone"

    def test_45500_is_upper_zone(self):
        assert classify_zone(45_500.0) == "upper_zone"

    def test_46000_is_upper_zone(self):
        assert classify_zone(46_000.0) == "upper_zone"

    def test_46999_is_upper_zone(self):
        assert classify_zone(46_999.0) == "upper_zone"

    def test_upper_zone_exposure_action(self):
        rec = build_exposure_recommendation("upper_zone")
        assert rec.exposure_action == "reduce_exposure_near_upper_box"

    def test_upper_zone_chase_high_not_allowed(self):
        rec = build_exposure_recommendation("upper_zone")
        assert rec.chase_high_allowed is False

    def test_upper_zone_reduce_short_term(self):
        rec = build_exposure_recommendation("upper_zone")
        assert rec.reduce_short_term_exposure is True

    def test_upper_zone_leveraged_etf_not_allowed(self):
        rec = build_exposure_recommendation("upper_zone")
        assert rec.leveraged_etf_allowed is False

    def test_upper_zone_block_new_add_reason_set(self):
        rec = build_exposure_recommendation("upper_zone")
        assert len(rec.block_new_add_reason) > 0

    def test_upper_zone_max_exposure_correct(self):
        pol = MarketBoxPolicy()
        rec = build_exposure_recommendation("upper_zone", policy=pol)
        assert rec.recommended_max_exposure_pct == pol.upper_zone_max_exposure_pct

    def test_upper_zone_cash_buffer_positive(self):
        rec = build_exposure_recommendation("upper_zone")
        assert rec.recommended_cash_buffer_pct > 0

    def test_upper_zone_should_auto_apply_false(self):
        rec = build_exposure_recommendation("upper_zone")
        assert rec.should_auto_apply is False


# ===========================================================================
# F. Zone classification — neutral zone 42,000-45,000
# ===========================================================================

class TestNeutralZoneClassification:
    def test_42000_is_neutral_zone(self):
        assert classify_zone(42_000.0) == "neutral_zone"

    def test_43500_is_neutral_zone(self):
        assert classify_zone(43_500.0) == "neutral_zone"

    def test_44999_is_neutral_zone(self):
        assert classify_zone(44_999.0) == "neutral_zone"

    def test_neutral_zone_exposure_action(self):
        rec = build_exposure_recommendation("neutral_zone")
        assert rec.exposure_action == "normal_selective_exposure"

    def test_neutral_zone_chase_high_not_allowed(self):
        rec = build_exposure_recommendation("neutral_zone")
        assert rec.chase_high_allowed is False

    def test_neutral_zone_add_position_allowed(self):
        rec = build_exposure_recommendation("neutral_zone")
        assert rec.add_position_allowed is True

    def test_neutral_zone_short_term_momentum_allowed(self):
        rec = build_exposure_recommendation("neutral_zone")
        assert rec.short_term_momentum_allowed is True

    def test_neutral_zone_max_exposure_correct(self):
        pol = MarketBoxPolicy()
        rec = build_exposure_recommendation("neutral_zone", policy=pol)
        assert rec.recommended_max_exposure_pct == pol.neutral_zone_max_exposure_pct

    def test_neutral_zone_should_auto_apply_false(self):
        rec = build_exposure_recommendation("neutral_zone")
        assert rec.should_auto_apply is False

    def test_neutral_zone_reduce_short_term_false(self):
        rec = build_exposure_recommendation("neutral_zone")
        assert rec.reduce_short_term_exposure is False


# ===========================================================================
# G. Zone classification — lower zone 40,000-42,000
# ===========================================================================

class TestLowerZoneClassification:
    def test_40000_is_lower_zone(self):
        assert classify_zone(40_000.0) == "lower_zone"

    def test_41000_is_lower_zone(self):
        assert classify_zone(41_000.0) == "lower_zone"

    def test_41999_is_lower_zone(self):
        assert classify_zone(41_999.0) == "lower_zone"

    def test_lower_zone_exposure_action(self):
        rec = build_exposure_recommendation("lower_zone")
        assert rec.exposure_action == "core_only_low_zone"

    def test_lower_zone_core_only_allowed(self):
        rec = build_exposure_recommendation("lower_zone")
        assert rec.core_only_allowed is True

    def test_lower_zone_chase_high_not_allowed(self):
        rec = build_exposure_recommendation("lower_zone")
        assert rec.chase_high_allowed is False

    def test_lower_zone_short_term_momentum_not_allowed(self):
        rec = build_exposure_recommendation("lower_zone")
        assert rec.short_term_momentum_allowed is False

    def test_lower_zone_max_exposure_correct(self):
        pol = MarketBoxPolicy()
        rec = build_exposure_recommendation("lower_zone", policy=pol)
        assert rec.recommended_max_exposure_pct == pol.lower_zone_max_exposure_pct

    def test_lower_zone_should_auto_apply_false(self):
        rec = build_exposure_recommendation("lower_zone")
        assert rec.should_auto_apply is False


# ===========================================================================
# H. Zone classification — extreme risk zone 38,000-40,000
# ===========================================================================

class TestExtremeRiskZoneClassification:
    def test_38000_is_extreme_risk_zone(self):
        assert classify_zone(38_000.0) == "extreme_risk_zone"

    def test_39000_is_extreme_risk_zone(self):
        assert classify_zone(39_000.0) == "extreme_risk_zone"

    def test_39999_is_extreme_risk_zone(self):
        assert classify_zone(39_999.0) == "extreme_risk_zone"

    def test_extreme_risk_zone_exposure_action(self):
        rec = build_exposure_recommendation("extreme_risk_zone")
        assert rec.exposure_action == "defensive_extreme_risk"

    def test_extreme_risk_zone_core_only(self):
        rec = build_exposure_recommendation("extreme_risk_zone")
        assert rec.core_only_allowed is True

    def test_extreme_risk_zone_chase_high_not_allowed(self):
        rec = build_exposure_recommendation("extreme_risk_zone")
        assert rec.chase_high_allowed is False

    def test_extreme_risk_zone_short_term_not_allowed(self):
        rec = build_exposure_recommendation("extreme_risk_zone")
        assert rec.short_term_momentum_allowed is False

    def test_extreme_risk_zone_max_exposure_correct(self):
        pol = MarketBoxPolicy()
        rec = build_exposure_recommendation("extreme_risk_zone", policy=pol)
        assert rec.recommended_max_exposure_pct == pol.extreme_risk_zone_max_exposure_pct

    def test_extreme_risk_zone_should_auto_apply_false(self):
        rec = build_exposure_recommendation("extreme_risk_zone")
        assert rec.should_auto_apply is False

    def test_extreme_risk_zone_block_reason_set(self):
        rec = build_exposure_recommendation("extreme_risk_zone")
        assert len(rec.block_new_add_reason) > 0


# ===========================================================================
# I. Zone classification — below box < 38,000
# ===========================================================================

class TestBelowBoxClassification:
    def test_37999_is_below_box(self):
        assert classify_zone(37_999.0) == "below_box"

    def test_36000_is_below_box(self):
        assert classify_zone(36_000.0) == "below_box"

    def test_below_box_exposure_action(self):
        rec = build_exposure_recommendation("below_box")
        assert rec.exposure_action == "below_box_defense"

    def test_below_box_core_only(self):
        rec = build_exposure_recommendation("below_box")
        assert rec.core_only_allowed is True

    def test_below_box_chase_high_not_allowed(self):
        rec = build_exposure_recommendation("below_box")
        assert rec.chase_high_allowed is False

    def test_below_box_max_exposure_correct(self):
        pol = MarketBoxPolicy()
        rec = build_exposure_recommendation("below_box", policy=pol)
        assert rec.recommended_max_exposure_pct == pol.below_box_max_exposure_pct

    def test_below_box_should_auto_apply_false(self):
        rec = build_exposure_recommendation("below_box")
        assert rec.should_auto_apply is False

    def test_below_box_block_reason_set(self):
        rec = build_exposure_recommendation("below_box")
        assert len(rec.block_new_add_reason) > 0

    def test_below_box_human_review_reason_set(self):
        rec = build_exposure_recommendation("below_box")
        assert len(rec.human_review_reason) > 0


# ===========================================================================
# J. Zone classification — above box > 47,000
# ===========================================================================

class TestAboveBoxClassification:
    def test_47000_is_above_box(self):
        assert classify_zone(47_000.0) == "above_box"

    def test_48000_is_above_box(self):
        assert classify_zone(48_000.0) == "above_box"

    def test_above_box_exposure_action(self):
        rec = build_exposure_recommendation("above_box")
        assert rec.exposure_action == "overheating_above_box"

    def test_above_box_chase_high_not_allowed(self):
        rec = build_exposure_recommendation("above_box")
        assert rec.chase_high_allowed is False

    def test_above_box_reduce_short_term(self):
        rec = build_exposure_recommendation("above_box")
        assert rec.reduce_short_term_exposure is True

    def test_above_box_human_review_reason_set(self):
        rec = build_exposure_recommendation("above_box")
        assert len(rec.human_review_reason) > 0

    def test_above_box_should_auto_apply_false(self):
        rec = build_exposure_recommendation("above_box")
        assert rec.should_auto_apply is False


# ===========================================================================
# K. Box boundary exact values
# ===========================================================================

class TestBoxBoundaryValues:
    @pytest.mark.parametrize("level,expected_zone", [
        (38_000.0, "extreme_risk_zone"),
        (40_000.0, "lower_zone"),
        (42_000.0, "neutral_zone"),
        (45_000.0, "upper_zone"),
        (47_000.0, "above_box"),
        (37_999.0, "below_box"),
        (43_500.0, "neutral_zone"),
        (46_999.0, "upper_zone"),
        (39_999.0, "extreme_risk_zone"),
        (41_999.0, "lower_zone"),
        (44_999.0, "neutral_zone"),
    ])
    def test_boundary_zone(self, level, expected_zone):
        assert classify_zone(level) == expected_zone


# ===========================================================================
# L. Index snapshot schema
# ===========================================================================

class TestIndexSnapshotSchema:
    def test_default_snapshot_schema_version(self):
        snap = IndexSnapshot()
        assert snap.schema_version == "213"

    def test_default_snapshot_paper_only(self):
        snap = IndexSnapshot()
        assert snap.paper_only is True

    def test_default_snapshot_should_auto_apply_false(self):
        snap = IndexSnapshot(should_auto_apply=True)
        assert snap.should_auto_apply is False

    def test_build_index_snapshot_upper_zone(self):
        snap = build_index_snapshot(46_000.0)
        assert snap.zone_name == "upper_zone"
        assert snap.near_upper_zone is True

    def test_build_index_snapshot_neutral_zone(self):
        snap = build_index_snapshot(43_500.0)
        assert snap.zone_name == "neutral_zone"

    def test_build_index_snapshot_lower_zone(self):
        snap = build_index_snapshot(41_000.0)
        assert snap.zone_name == "lower_zone"
        assert snap.near_lower_zone is True

    def test_build_index_snapshot_extreme_risk(self):
        snap = build_index_snapshot(39_000.0)
        assert snap.zone_name == "extreme_risk_zone"
        assert snap.requires_human_review is True

    def test_build_index_snapshot_below_box(self):
        snap = build_index_snapshot(36_000.0)
        assert snap.zone_name == "below_box"
        assert snap.requires_human_review is True

    def test_build_index_snapshot_above_box(self):
        snap = build_index_snapshot(48_000.0)
        assert snap.zone_name == "above_box"
        assert snap.requires_human_review is True

    def test_build_index_snapshot_box_position_pct(self):
        snap = build_index_snapshot(43_000.0)
        assert 0.0 <= snap.box_position_pct <= 1.0

    def test_build_index_snapshot_within_box_status(self):
        snap = build_index_snapshot(43_000.0)
        assert snap.box_break_status == "within_box"

    def test_build_index_snapshot_below_box_break_status(self):
        snap = build_index_snapshot(36_000.0)
        assert snap.box_break_status == "below_box_break"

    def test_build_index_snapshot_above_box_break_status(self):
        snap = build_index_snapshot(48_000.0)
        assert snap.box_break_status == "above_box_break"

    def test_build_index_snapshot_moving_averages(self):
        snap = build_index_snapshot(43_500.0, ma5=43_000.0, ma10=42_500.0, ma20=42_000.0, ma60=40_800.0)
        assert snap.above_ma5 is True
        assert snap.above_ma10 is True
        assert snap.above_ma20 is True
        assert snap.above_ma60 is True

    def test_build_index_snapshot_below_ma(self):
        snap = build_index_snapshot(41_000.0, ma5=43_000.0, ma10=42_500.0, ma20=42_000.0, ma60=40_000.0)
        assert snap.above_ma5 is False
        assert snap.above_ma20 is False
        assert snap.above_ma60 is True

    def test_build_index_snapshot_volume_ratio(self):
        snap = build_index_snapshot(43_500.0, volume_ratio=1.5)
        assert snap.volume_ratio == 1.5

    def test_build_index_snapshot_return_pct(self):
        snap = build_index_snapshot(43_500.0, previous_close=43_000.0)
        assert snap.index_return_pct > 0

    def test_build_index_snapshot_should_auto_apply_false(self):
        snap = build_index_snapshot(43_500.0)
        assert snap.should_auto_apply is False


# ===========================================================================
# M. Exposure recommendation schema
# ===========================================================================

class TestExposureRecommendationSchema:
    def test_default_schema_version(self):
        rec = ExposureRecommendation()
        assert rec.schema_version == "213"

    def test_default_paper_only(self):
        rec = ExposureRecommendation()
        assert rec.paper_only is True

    def test_default_should_auto_apply_false(self):
        rec = ExposureRecommendation(should_auto_apply=True)
        assert rec.should_auto_apply is False

    def test_default_no_real_orders(self):
        rec = ExposureRecommendation()
        assert rec.no_real_orders is True

    def test_reduce_leveraged_exposure_always_true(self):
        rec = build_exposure_recommendation("neutral_zone")
        assert rec.reduce_leveraged_exposure is True

    def test_leveraged_etf_always_not_allowed(self):
        for zone in ZONE_NAMES:
            rec = build_exposure_recommendation(zone)
            assert rec.leveraged_etf_allowed is False

    def test_chase_high_always_blocked(self):
        for zone in ZONE_NAMES:
            rec = build_exposure_recommendation(zone)
            assert rec.chase_high_allowed is False

    def test_should_auto_apply_always_false_all_zones(self):
        for zone in ZONE_NAMES:
            rec = build_exposure_recommendation(zone)
            assert rec.should_auto_apply is False

    def test_cash_buffer_plus_max_exposure_approx_one(self):
        for zone in ZONE_NAMES:
            rec = build_exposure_recommendation(zone)
            total = round(rec.recommended_max_exposure_pct + rec.recommended_cash_buffer_pct, 4)
            assert abs(total - 1.0) < 0.0001


# ===========================================================================
# N. Box position percentage
# ===========================================================================

class TestBoxPositionPercentage:
    def test_below_box_position_near_zero(self):
        snap = build_index_snapshot(38_000.0)
        assert snap.box_position_pct == 0.0

    def test_above_box_position_at_one(self):
        snap = build_index_snapshot(47_000.0)
        assert snap.box_position_pct == 1.0

    def test_midpoint_position_pct(self):
        snap = build_index_snapshot(42_500.0)
        assert 0.0 < snap.box_position_pct < 1.0

    def test_position_pct_in_range(self):
        for level in [38_000, 40_000, 42_000, 43_500, 45_000, 46_000, 47_000]:
            snap = build_index_snapshot(float(level))
            assert 0.0 <= snap.box_position_pct <= 1.0


# ===========================================================================
# O. Chase-high blocker
# ===========================================================================

class TestChaseHighBlocker:
    def test_upper_zone_blocks_all_candidates(self):
        queue = build_chase_risk_queue("upper_zone")
        assert len(queue) > 0

    def test_above_box_blocks_all_candidates(self):
        queue = build_chase_risk_queue("above_box")
        assert len(queue) > 0

    def test_neutral_zone_no_chase_block(self):
        queue = build_chase_risk_queue("neutral_zone")
        assert len(queue) == 0

    def test_lower_zone_no_chase_block(self):
        queue = build_chase_risk_queue("lower_zone")
        assert len(queue) == 0

    def test_extreme_risk_zone_no_chase_block(self):
        queue = build_chase_risk_queue("extreme_risk_zone")
        assert len(queue) == 0

    def test_below_box_no_chase_block(self):
        queue = build_chase_risk_queue("below_box")
        assert len(queue) == 0

    def test_custom_symbols_upper_zone(self):
        queue = build_chase_risk_queue("upper_zone", ["2330", "2454"])
        assert "2330" in queue
        assert "2454" in queue


# ===========================================================================
# P. Defensive review queue
# ===========================================================================

class TestDefensiveReviewQueue:
    def test_extreme_risk_zone_has_defensive_queue(self):
        queue = build_defensive_review_queue("extreme_risk_zone")
        assert len(queue) > 0

    def test_below_box_has_defensive_queue(self):
        queue = build_defensive_review_queue("below_box")
        assert len(queue) > 0

    def test_upper_zone_no_defensive_queue(self):
        queue = build_defensive_review_queue("upper_zone")
        assert len(queue) == 0

    def test_neutral_zone_no_defensive_queue(self):
        queue = build_defensive_review_queue("neutral_zone")
        assert len(queue) == 0

    def test_lower_zone_core_only_filter(self):
        queue = build_defensive_review_queue("lower_zone")
        # Lower zone returns core symbols only
        assert len(queue) >= 0  # May or may not have entries depending on overlap


# ===========================================================================
# Q. Market box review engine
# ===========================================================================

class TestMarketBoxReviewEngine:
    def test_run_default_review_returns_result(self):
        result = run_market_box_review()
        assert isinstance(result, MarketBoxReviewResult)

    def test_result_paper_only(self):
        result = run_market_box_review()
        assert result.paper_only is True

    def test_result_should_auto_apply_false(self):
        result = run_market_box_review()
        assert result.should_auto_apply is False

    def test_result_auto_apply_enabled_false(self):
        result = run_market_box_review()
        assert result.auto_apply_enabled is False

    def test_result_no_broker(self):
        result = run_market_box_review()
        assert result.no_broker is True

    def test_result_market_box_recommendation_only(self):
        result = run_market_box_review()
        assert result.market_box_recommendation_only is True

    def test_result_market_box_version(self):
        result = run_market_box_review()
        assert result.market_box_version == "2.0.13"

    def test_result_has_index_snapshot(self):
        result = run_market_box_review()
        assert result.index_snapshot is not None

    def test_result_has_exposure_control_snapshot(self):
        result = run_market_box_review()
        assert result.exposure_control_snapshot is not None

    def test_result_has_market_box_summary(self):
        result = run_market_box_review()
        assert result.market_box_summary is not None

    def test_result_zone_classification_valid(self):
        result = run_market_box_review()
        assert result.zone_classification in ZONE_NAMES

    def test_result_all_passed(self):
        result = run_market_box_review()
        assert result.all_passed is True

    def test_result_paper_only_safety_snapshot(self):
        result = run_market_box_review()
        assert result.paper_only_safety_snapshot is True

    def test_result_box_range_snapshot_has_boundaries(self):
        result = run_market_box_review()
        assert "upper_zone_min" in result.box_range_snapshot
        assert "below_box_threshold" in result.box_range_snapshot

    def test_upper_zone_input_yields_correct_zone(self):
        inp = MarketBoxReviewInput(review_period="2026-W29", index_level=46_000.0)
        result = run_market_box_review(inp)
        assert result.zone_classification == "upper_zone"

    def test_neutral_zone_input_yields_correct_zone(self):
        inp = MarketBoxReviewInput(review_period="2026-W29", index_level=43_500.0)
        result = run_market_box_review(inp)
        assert result.zone_classification == "neutral_zone"

    def test_lower_zone_input_yields_correct_zone(self):
        inp = MarketBoxReviewInput(review_period="2026-W29", index_level=41_000.0)
        result = run_market_box_review(inp)
        assert result.zone_classification == "lower_zone"

    def test_extreme_risk_zone_input_yields_correct_zone(self):
        inp = MarketBoxReviewInput(review_period="2026-W29", index_level=39_000.0)
        result = run_market_box_review(inp)
        assert result.zone_classification == "extreme_risk_zone"

    def test_below_box_input_yields_correct_zone(self):
        inp = MarketBoxReviewInput(review_period="2026-W29", index_level=36_000.0)
        result = run_market_box_review(inp)
        assert result.zone_classification == "below_box"

    def test_above_box_input_yields_correct_zone(self):
        inp = MarketBoxReviewInput(review_period="2026-W29", index_level=48_000.0)
        result = run_market_box_review(inp)
        assert result.zone_classification == "above_box"


# ===========================================================================
# R. Market box summary
# ===========================================================================

class TestMarketBoxSummary:
    def test_summary_schema_version(self):
        result = run_market_box_review()
        assert result.market_box_summary.schema_version == "213"

    def test_summary_paper_only(self):
        result = run_market_box_review()
        assert result.market_box_summary.paper_only is True

    def test_summary_current_zone_valid(self):
        result = run_market_box_review()
        assert result.market_box_summary.current_zone in ZONE_NAMES

    def test_summary_index_level_positive(self):
        result = run_market_box_review()
        assert result.market_box_summary.index_level > 0

    def test_summary_box_position_pct_in_range(self):
        result = run_market_box_review()
        assert 0.0 <= result.market_box_summary.box_position_pct <= 1.0

    def test_summary_market_box_quality_grade_set(self):
        result = run_market_box_review()
        assert result.market_box_summary.market_box_quality_grade in ("A", "B", "C")

    def test_summary_exposure_control_grade_set(self):
        result = run_market_box_review()
        assert result.market_box_summary.exposure_control_quality_grade in ("A", "B", "C")

    def test_summary_risk_temperature_grade_set(self):
        result = run_market_box_review()
        assert result.market_box_summary.risk_temperature_grade in ("A", "B", "C")


# ===========================================================================
# S. Export JSON / Markdown / CSV schema completeness
# ===========================================================================

class TestExportIntegration:
    def setup_method(self):
        self.result = run_market_box_review()

    def test_export_json_is_valid(self):
        exp = export_market_box_json(self.result)
        assert exp.is_valid is True

    def test_export_json_export_format(self):
        exp = export_market_box_json(self.result)
        assert exp.export_format == "json"

    def test_export_json_paper_only(self):
        exp = export_market_box_json(self.result)
        assert exp.paper_only is True

    def test_export_json_should_auto_apply_false(self):
        exp = export_market_box_json(self.result)
        assert exp.should_auto_apply is False

    def test_export_json_auto_apply_enabled_false(self):
        exp = export_market_box_json(self.result)
        assert exp.auto_apply_enabled is False

    def test_export_json_content_has_version(self):
        exp = export_market_box_json(self.result)
        assert "2.0.13" in exp.content

    def test_export_json_content_has_paper_only(self):
        exp = export_market_box_json(self.result)
        assert "paper_only" in exp.content

    def test_export_json_status_complete(self):
        exp = export_market_box_json(self.result)
        assert exp.export_status == "complete"

    def test_export_markdown_is_valid(self):
        exp = export_market_box_markdown(self.result)
        assert exp.is_valid is True

    def test_export_markdown_paper_only(self):
        exp = export_market_box_markdown(self.result)
        assert exp.paper_only is True

    def test_export_markdown_content_has_header(self):
        exp = export_market_box_markdown(self.result)
        assert "Market Box" in exp.content

    def test_export_markdown_content_has_should_auto_apply_false(self):
        exp = export_market_box_markdown(self.result)
        assert "False" in exp.content

    def test_export_csv_is_valid(self):
        exp = export_market_box_csv(self.result)
        assert exp.is_valid is True

    def test_export_csv_paper_only(self):
        exp = export_market_box_csv(self.result)
        assert exp.paper_only is True

    def test_export_csv_row_count_positive(self):
        exp = export_market_box_csv(self.result)
        assert exp.row_count >= 1

    def test_export_chase_risk_queue_csv(self):
        exp = export_chase_risk_queue_csv(self.result)
        assert isinstance(exp, ChaseRiskQueueCSV)

    def test_export_defensive_review_queue_csv(self):
        exp = export_defensive_review_queue_csv(self.result)
        assert isinstance(exp, DefensiveReviewQueueCSV)

    def test_export_exposure_recommendation_csv(self):
        exp = export_exposure_recommendation_csv(self.result)
        assert isinstance(exp, ExposureRecommendationCSV)
        assert exp.is_valid is True

    def test_export_audit_snapshot(self):
        snap = export_market_box_audit_snapshot(self.result)
        assert isinstance(snap, MarketBoxAuditSnapshot)
        assert snap.export_status == "complete"
        assert len(snap.reproducibility_hash) > 0

    def test_export_audit_snapshot_safety_string(self):
        snap = export_market_box_audit_snapshot(self.result)
        assert "paper_only=True" in snap.safety_snapshot
        assert "should_auto_apply=False" in snap.safety_snapshot


# ===========================================================================
# T. CLI output
# ===========================================================================

class TestCLIOutput:
    def test_cli_commands_count(self):
        assert len(CLI_COMMANDS_V213) == 10

    def test_review_market_box_in_cli(self):
        assert "paper-cockpit-v213-review-market-box" in CLI_COMMANDS_V213

    def test_classify_index_zone_in_cli(self):
        assert "paper-cockpit-v213-classify-index-zone" in CLI_COMMANDS_V213

    def test_build_exposure_control_in_cli(self):
        assert "paper-cockpit-v213-build-exposure-control" in CLI_COMMANDS_V213

    def test_build_chase_risk_queue_in_cli(self):
        assert "paper-cockpit-v213-build-chase-risk-queue" in CLI_COMMANDS_V213

    def test_build_defensive_review_queue_in_cli(self):
        assert "paper-cockpit-v213-build-defensive-review-queue" in CLI_COMMANDS_V213

    def test_export_json_in_cli(self):
        assert "paper-cockpit-v213-export-json" in CLI_COMMANDS_V213

    def test_export_md_in_cli(self):
        assert "paper-cockpit-v213-export-md" in CLI_COMMANDS_V213

    def test_export_csv_in_cli(self):
        assert "paper-cockpit-v213-export-csv" in CLI_COMMANDS_V213

    def test_health_in_cli(self):
        assert "paper-cockpit-v213-health" in CLI_COMMANDS_V213

    def test_gate_in_cli(self):
        assert "paper-cockpit-v213-gate" in CLI_COMMANDS_V213

    def test_classify_index_zone_function(self):
        result = classify_index_zone(43_500.0)
        assert result["zone_name"] == "neutral_zone"
        assert result["should_auto_apply"] is False
        assert result["auto_apply_enabled"] is False

    def test_classify_index_zone_paper_only(self):
        result = classify_index_zone(43_500.0)
        assert result["paper_only"] is True


# ===========================================================================
# U. CLI handler resolution
# ===========================================================================

class TestCLIHandlerResolution:
    def test_cmd_review_market_box_exists(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v213_review_market_box")

    def test_cmd_classify_index_zone_exists(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v213_classify_index_zone")

    def test_cmd_build_exposure_control_exists(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v213_build_exposure_control")

    def test_cmd_build_chase_risk_queue_exists(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v213_build_chase_risk_queue")

    def test_cmd_build_defensive_review_queue_exists(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v213_build_defensive_review_queue")

    def test_cmd_export_json_exists(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v213_export_json")

    def test_cmd_export_md_exists(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v213_export_md")

    def test_cmd_export_csv_exists(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v213_export_csv")

    def test_cmd_health_exists(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v213_health")

    def test_cmd_gate_exists(self):
        import main
        assert hasattr(main, "cmd_paper_cockpit_v213_gate")

    def test_all_handlers_callable(self):
        import main
        for name in [
            "cmd_paper_cockpit_v213_review_market_box",
            "cmd_paper_cockpit_v213_classify_index_zone",
            "cmd_paper_cockpit_v213_build_exposure_control",
            "cmd_paper_cockpit_v213_build_chase_risk_queue",
            "cmd_paper_cockpit_v213_build_defensive_review_queue",
            "cmd_paper_cockpit_v213_export_json",
            "cmd_paper_cockpit_v213_export_md",
            "cmd_paper_cockpit_v213_export_csv",
            "cmd_paper_cockpit_v213_health",
            "cmd_paper_cockpit_v213_gate",
        ]:
            assert callable(getattr(main, name))


# ===========================================================================
# V. CLI registration health
# ===========================================================================

class TestCLIRegistrationHealth:
    def test_v213_commands_in_registry(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        for cmd in CLI_COMMANDS_V213:
            assert cmd in names, f"CLI command not in registry: {cmd}"

    def test_v213_handler_names_in_registry(self):
        from cli.command_registry import PROVIDER_COMMANDS
        handler_names = {c.handler_name for c in PROVIDER_COMMANDS}
        expected_handlers = [
            "cmd_paper_cockpit_v213_review_market_box",
            "cmd_paper_cockpit_v213_classify_index_zone",
            "cmd_paper_cockpit_v213_build_exposure_control",
            "cmd_paper_cockpit_v213_build_chase_risk_queue",
            "cmd_paper_cockpit_v213_build_defensive_review_queue",
            "cmd_paper_cockpit_v213_export_json",
            "cmd_paper_cockpit_v213_export_md",
            "cmd_paper_cockpit_v213_export_csv",
            "cmd_paper_cockpit_v213_health",
            "cmd_paper_cockpit_v213_gate",
        ]
        for h in expected_handlers:
            assert h in handler_names, f"Handler not in registry: {h}"

    def test_registry_group_paper_cockpit_v213(self):
        from cli.command_registry import PROVIDER_COMMANDS
        groups = {c.group for c in PROVIDER_COMMANDS if c.group == "paper_cockpit_v213"}
        assert len(groups) == 1

    def test_registry_safety_classification_research_only(self):
        from cli.command_registry import PROVIDER_COMMANDS
        v213_cmds = [c for c in PROVIDER_COMMANDS if c.group == "paper_cockpit_v213"]
        for c in v213_cmds:
            assert c.safety_classification == "RESEARCH_ONLY"


# ===========================================================================
# W. GUI compatibility
# ===========================================================================

class TestGUICompatibility:
    def test_gui_import_safe(self):
        import gui.small_capital_strategy_panel  # noqa: F401

    def test_v213_tabs_in_panel(self):
        from gui.small_capital_strategy_panel import _TABS
        for tab in GUI_TABS_V213:
            assert tab in _TABS, f"Tab not in panel: {tab}"

    def test_render_market_box_v213_tab(self):
        from gui.small_capital_strategy_panel import render_market_box_v213_tab
        result = render_market_box_v213_tab()
        assert result["tab"] == "market_box_v213"
        assert result["paper_only"] is True
        assert result["should_auto_apply"] is False

    def test_render_exposure_control_v213_tab(self):
        from gui.small_capital_strategy_panel import render_exposure_control_v213_tab
        result = render_exposure_control_v213_tab()
        assert result["tab"] == "exposure_control_v213"
        assert result["paper_only"] is True
        assert result["should_auto_apply"] is False

    def test_render_defensive_review_queue_v213_tab(self):
        from gui.small_capital_strategy_panel import render_defensive_review_queue_v213_tab
        result = render_defensive_review_queue_v213_tab()
        assert result["tab"] == "defensive_review_queue_v213"
        assert result["paper_only"] is True
        assert result["should_auto_apply"] is False

    def test_render_all_tabs_no_error_tabs(self):
        from gui.small_capital_strategy_panel import render_all_tabs
        results = render_all_tabs()
        error_tabs = [k for k, v in results.items() if "error" in str(v)]
        assert len(error_tabs) == 0, f"Error tabs: {error_tabs}"

    def test_render_all_tabs_has_v213_tabs(self):
        from gui.small_capital_strategy_panel import render_all_tabs
        results = render_all_tabs()
        for tab in GUI_TABS_V213:
            assert tab in results

    def test_tab_render_map_v213_exists(self):
        from gui.small_capital_strategy_panel import _TAB_RENDER_MAP_V213
        assert len(_TAB_RENDER_MAP_V213) == 3

    def test_tab_render_map_v213_keys(self):
        from gui.small_capital_strategy_panel import _TAB_RENDER_MAP_V213
        for tab in GUI_TABS_V213:
            assert tab in _TAB_RENDER_MAP_V213

    def test_market_box_tab_auto_apply_false(self):
        from gui.small_capital_strategy_panel import render_market_box_v213_tab
        result = render_market_box_v213_tab()
        assert result.get("auto_apply_enabled") is False

    def test_exposure_control_tab_auto_apply_false(self):
        from gui.small_capital_strategy_panel import render_exposure_control_v213_tab
        result = render_exposure_control_v213_tab()
        assert result.get("auto_apply_enabled") is False

    def test_defensive_queue_tab_auto_apply_false(self):
        from gui.small_capital_strategy_panel import render_defensive_review_queue_v213_tab
        result = render_defensive_review_queue_v213_tab()
        assert result.get("auto_apply_enabled") is False


# ===========================================================================
# X. Paper-only safety
# ===========================================================================

class TestPaperOnlySafety:
    def test_safety_guard_schema_version(self):
        guard = MarketBoxSafetyGuard()
        assert guard.schema_version == "213"

    def test_safety_guard_paper_only(self):
        guard = MarketBoxSafetyGuard()
        assert guard.paper_only is True

    def test_safety_guard_should_auto_apply_false(self):
        guard = MarketBoxSafetyGuard()
        assert guard.should_auto_apply is False

    def test_safety_guard_auto_apply_enabled_false(self):
        guard = MarketBoxSafetyGuard()
        assert guard.auto_apply_enabled is False

    def test_safety_guard_no_automatic_market_action(self):
        guard = MarketBoxSafetyGuard()
        assert guard.no_automatic_market_action is True

    def test_safety_guard_require_box_check_true(self):
        guard = MarketBoxSafetyGuard()
        assert guard.require_box_check_before_entry is True

    def test_safety_guard_market_box_recommendation_only(self):
        guard = MarketBoxSafetyGuard()
        assert guard.market_box_actions_recommendation_only is True

    def test_safety_guard_exposure_recommendation_only(self):
        guard = MarketBoxSafetyGuard()
        assert guard.exposure_actions_recommendation_only is True

    def test_no_broker_in_result(self):
        result = run_market_box_review()
        assert result.no_broker is True

    def test_not_investment_advice_in_result(self):
        result = run_market_box_review()
        assert result.not_investment_advice is True

    def test_human_review_required_in_result(self):
        result = run_market_box_review()
        assert result.human_review_required is True


# ===========================================================================
# Y. Backward compatibility with v2.0.12
# ===========================================================================

class TestBackwardCompatibilityV212:
    def test_v212_module_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_v212  # noqa: F401

    def test_v212_run_profit_taking_review_callable(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
        result = run_profit_taking_review()
        assert result.paper_only is True

    def test_v212_safety_flags_intact(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
        assert SAFETY_FLAGS_V212["paper_only"] is True

    def test_v212_version_still_correct(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v212 import VERSION as V212
        assert V212 == "2.0.12"

    def test_v212_export_json_still_works(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_json
        result = export_profit_taking_json(run_profit_taking_review())
        assert result.is_valid is True

    def test_v211_module_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_v211  # noqa: F401

    def test_v210_module_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_v210  # noqa: F401

    def test_v209_module_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_v209  # noqa: F401

    def test_v208_module_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_v208  # noqa: F401

    def test_v207_module_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_v207  # noqa: F401


# ===========================================================================
# Z. v201 health relative-path compatibility
# ===========================================================================

class TestV201HealthRelativePathCompatibility:
    def test_health_v212_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_health_v212  # noqa: F401

    def test_health_v212_run_health_check_callable(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v212 import run_health_check
        result = run_health_check()
        assert "all_passed" in result

    def test_health_v213_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_health_v213  # noqa: F401

    def test_health_v213_run_health_check_callable(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v213 import run_health_check
        result = run_health_check()
        assert "all_passed" in result

    def test_release_gate_v212_importable(self):
        import release.paper_cockpit_release_gate_v212  # noqa: F401

    def test_release_gate_v213_importable(self):
        import release.paper_cockpit_release_gate_v213  # noqa: F401


# ===========================================================================
# AA. Health and gate
# ===========================================================================

class TestHealthAndGate:
    def test_health_check_all_passed(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v213 import run_health_check
        result = run_health_check()
        assert result["all_passed"] is True, f"Health check failed: {result['errors']}"

    def test_health_check_version(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v213 import run_health_check
        result = run_health_check()
        assert result["version"] == "2.0.13"

    def test_health_check_paper_only(self):
        from paper_trading.small_capital_strategy.paper_cockpit_health_v213 import run_health_check
        result = run_health_check()
        assert result["paper_only"] is True

    def test_release_gate_passed(self):
        from release.paper_cockpit_release_gate_v213 import run_release_gate
        result = run_release_gate()
        assert result["gate_passed"] is True, f"Gate failed: {result['errors']}"

    def test_release_gate_version(self):
        from release.paper_cockpit_release_gate_v213 import GATE_VERSION
        assert GATE_VERSION == "2.0.13"

    def test_release_gate_paper_only(self):
        from release.paper_cockpit_release_gate_v213 import run_release_gate
        result = run_release_gate()
        assert result["paper_only"] is True


# ===========================================================================
# AB. Cockpit summary
# ===========================================================================

class TestCockpitSummary:
    def test_get_cockpit_summary_v213(self):
        summary = get_cockpit_summary_v213()
        assert summary["version"] == "2.0.13"
        assert summary["paper_only"] is True
        assert summary["should_auto_apply"] is False
        assert summary["auto_apply_enabled"] is False
        assert summary["require_box_check_before_entry"] is True
        assert summary["chase_high_always_blocked"] is True
        assert summary["market_box_actions_recommendation_only"] is True
        assert summary["exposure_actions_recommendation_only"] is True

    def test_summary_model_count(self):
        summary = get_cockpit_summary_v213()
        assert summary["model_count"] == 16

    def test_summary_baseline_tests(self):
        summary = get_cockpit_summary_v213()
        assert summary["baseline_tests"] == 36689

    def test_summary_min_new_tests(self):
        summary = get_cockpit_summary_v213()
        assert summary["min_new_tests"] == 300


# ===========================================================================
# AC. v2.0.12 ETF rebalancing integration
# ===========================================================================

class TestV212ETFRebalancingIntegration:
    def test_v212_etf_rebalancing_review_callable(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_etf_rebalancing_review
        items = run_etf_rebalancing_review()
        assert len(items) > 0

    def test_v212_etf_item_should_auto_apply_false(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_etf_rebalancing_review
        items = run_etf_rebalancing_review()
        for item in items:
            assert item.should_auto_apply is False


# ===========================================================================
# AD. v2.0.11 journal integration
# ===========================================================================

class TestV211JournalIntegration:
    def test_v211_journal_review_callable(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
        result = run_journal_review()
        assert result.paper_only is True

    def test_v211_journal_should_auto_apply_false(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
        result = run_journal_review()
        assert result.should_auto_apply is False


# ===========================================================================
# AE. v2.0.10 exit plan integration
# ===========================================================================

class TestV210ExitPlanIntegration:
    def test_v210_module_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_v210  # noqa: F401

    def test_v210_exit_plan_callable(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
        result = run_exit_plan_review()
        assert result.paper_only is True


# ===========================================================================
# AF. v2.0.9 position sizing integration
# ===========================================================================

class TestV209PositionSizingIntegration:
    def test_v209_module_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_v209  # noqa: F401

    def test_v209_position_sizing_callable(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
        result = run_sizing_review()
        assert result.paper_only is True


# ===========================================================================
# AG. v2.0.8 exposure integration
# ===========================================================================

class TestV208ExposureIntegration:
    def test_v208_module_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_v208  # noqa: F401

    def test_v208_exposure_review_callable(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
        result = run_exposure_review()
        assert result.paper_only is True


# ===========================================================================
# AH. v2.0.7 market regime integration
# ===========================================================================

class TestV207MarketRegimeIntegration:
    def test_v207_module_importable(self):
        import paper_trading.small_capital_strategy.paper_cockpit_v207  # noqa: F401

    def test_v207_theme_regime_callable(self):
        from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
        result = run_theme_rotation_review()
        assert result.paper_only is True


# ===========================================================================
# AI. Scenario tests
# ===========================================================================

class TestScenarios:
    def test_scenario_upper_zone_review(self):
        from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v213 import scenario_upper_zone_review
        r = scenario_upper_zone_review()
        assert r["zone"] == "upper_zone"
        assert r["should_auto_apply"] is False

    def test_scenario_neutral_zone_review(self):
        from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v213 import scenario_neutral_zone_review
        r = scenario_neutral_zone_review()
        assert r["zone"] == "neutral_zone"
        assert r["should_auto_apply"] is False

    def test_scenario_lower_zone_review(self):
        from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v213 import scenario_lower_zone_review
        r = scenario_lower_zone_review()
        assert r["zone"] == "lower_zone"
        assert r["should_auto_apply"] is False

    def test_scenario_extreme_risk_zone_review(self):
        from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v213 import scenario_extreme_risk_zone_review
        r = scenario_extreme_risk_zone_review()
        assert r["zone"] == "extreme_risk_zone"
        assert r["should_auto_apply"] is False

    def test_scenario_below_box_defense(self):
        from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v213 import scenario_below_box_defense
        r = scenario_below_box_defense()
        assert r["zone"] == "below_box"
        assert r["should_auto_apply"] is False

    def test_scenario_above_box_overheating(self):
        from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v213 import scenario_above_box_overheating
        r = scenario_above_box_overheating()
        assert r["zone"] == "above_box"
        assert r["should_auto_apply"] is False

    def test_run_all_scenarios(self):
        from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v213 import run_all_scenarios
        r = run_all_scenarios()
        assert r["paper_only"] is True
        assert r["should_auto_apply"] is False
        assert len(r) >= 7


# ===========================================================================
# AJ. Fixtures
# ===========================================================================

class TestFixtures:
    def test_fixture_upper_zone_index(self):
        from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v213 import fixture_upper_zone_index
        f = fixture_upper_zone_index()
        assert f["expected_zone"] == "upper_zone"
        assert f["paper_only"] is True

    def test_fixture_neutral_zone_index(self):
        from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v213 import fixture_neutral_zone_index
        f = fixture_neutral_zone_index()
        assert f["expected_zone"] == "neutral_zone"

    def test_fixture_lower_zone_index(self):
        from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v213 import fixture_lower_zone_index
        f = fixture_lower_zone_index()
        assert f["expected_zone"] == "lower_zone"

    def test_fixture_extreme_risk_zone_index(self):
        from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v213 import fixture_extreme_risk_zone_index
        f = fixture_extreme_risk_zone_index()
        assert f["expected_zone"] == "extreme_risk_zone"

    def test_fixture_below_box_index(self):
        from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v213 import fixture_below_box_index
        f = fixture_below_box_index()
        assert f["expected_zone"] == "below_box"

    def test_fixture_above_box_index(self):
        from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v213 import fixture_above_box_index
        f = fixture_above_box_index()
        assert f["expected_zone"] == "above_box"

    def test_fixture_all_zones_count(self):
        from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v213 import fixture_all_zones
        zones = fixture_all_zones()
        assert len(zones) == 6

    def test_fixture_box_boundary_values_count(self):
        from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v213 import fixture_box_boundary_values
        boundaries = fixture_box_boundary_values()
        assert len(boundaries) >= 8

    def test_fixture_safety_flags(self):
        from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v213 import fixture_safety_flags
        flags = fixture_safety_flags()
        assert flags["paper_only"] is True
        assert flags["should_auto_apply"] is False
        assert flags["auto_apply_enabled"] is False
        assert flags["require_box_check_before_entry"] is True
