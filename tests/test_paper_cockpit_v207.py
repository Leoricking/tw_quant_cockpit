"""
tests/test_paper_cockpit_v207.py
v2.0.7 Paper Theme Rotation & Market Regime Control — Main Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest


# =========================================================================
# Import tests
# =========================================================================
def test_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v207

def test_version_is_207():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import VERSION
    assert VERSION == "2.0.7"

def test_schema_version_is_207():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "207"

def test_release_name_contains_theme():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import RELEASE_NAME
    assert "Theme" in RELEASE_NAME

def test_release_name_contains_regime():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import RELEASE_NAME
    assert "Regime" in RELEASE_NAME

def test_baseline_tests_set():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import BASELINE_TESTS
    assert BASELINE_TESTS == 34632

def test_min_new_tests_300():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300

def test_verify_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import verify_version
    assert verify_version() is True


# =========================================================================
# Safety constants
# =========================================================================
def test_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True


# =========================================================================
# Safety flags
# =========================================================================
def test_safety_flags_count_20():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert len(SAFETY_FLAGS_V207) == 20

def test_safety_flags_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["paper_only"] is True

def test_safety_flags_research_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["research_only"] is True

def test_safety_flags_theme_rotation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["theme_rotation_only"] is True

def test_safety_flags_market_regime_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["market_regime_only"] is True

def test_safety_flags_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["no_broker"] is True

def test_safety_flags_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["no_real_orders"] is True

def test_safety_flags_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["should_auto_apply_always_false"] is True

def test_safety_flags_should_auto_apply_theme_rotation_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["should_auto_apply_theme_rotation_always_false"] is True

def test_safety_flags_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["broker_execution_disabled"] is True

def test_safety_flags_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["production_trading_blocked"] is True

def test_safety_flags_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["no_automatic_rebalance"] is True

def test_safety_flags_no_real_account_sync():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["no_real_account_sync"] is True

def test_safety_flags_not_investment_advice():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["not_investment_advice"] is True

def test_safety_flags_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["human_review_required"] is True

def test_safety_flags_no_margin():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["no_margin"] is True

def test_safety_flags_no_leverage():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["no_leverage"] is True

def test_safety_flags_validation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["validation_only"] is True

def test_safety_flags_candidate_priority_adjustment_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import SAFETY_FLAGS_V207
    assert SAFETY_FLAGS_V207["candidate_priority_adjustment_only"] is True


# =========================================================================
# Theme states
# =========================================================================
def test_theme_states_count_10():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_STATES
    assert len(THEME_STATES) == 10

def test_theme_state_emerging():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_STATES
    assert "emerging" in THEME_STATES

def test_theme_state_strengthening():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_STATES
    assert "strengthening" in THEME_STATES

def test_theme_state_leading():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_STATES
    assert "leading" in THEME_STATES

def test_theme_state_crowded():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_STATES
    assert "crowded" in THEME_STATES

def test_theme_state_overheating():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_STATES
    assert "overheating" in THEME_STATES

def test_theme_state_weakening():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_STATES
    assert "weakening" in THEME_STATES

def test_theme_state_cooling():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_STATES
    assert "cooling" in THEME_STATES

def test_theme_state_stale():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_STATES
    assert "stale" in THEME_STATES

def test_theme_state_risk_off():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_STATES
    assert "risk_off" in THEME_STATES

def test_theme_state_neutral():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_STATES
    assert "neutral" in THEME_STATES


# =========================================================================
# Market states
# =========================================================================
def test_market_states_count_7():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MARKET_STATES
    assert len(MARKET_STATES) == 7

def test_market_state_strong_uptrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MARKET_STATES
    assert "strong_uptrend" in MARKET_STATES

def test_market_state_healthy_pullback():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MARKET_STATES
    assert "healthy_pullback" in MARKET_STATES

def test_market_state_range_bound():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MARKET_STATES
    assert "range_bound" in MARKET_STATES

def test_market_state_weak_rebound():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MARKET_STATES
    assert "weak_rebound" in MARKET_STATES

def test_market_state_downtrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MARKET_STATES
    assert "downtrend" in MARKET_STATES

def test_market_state_high_volatility():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MARKET_STATES
    assert "high_volatility" in MARKET_STATES

def test_market_state_risk_off():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MARKET_STATES
    assert "risk_off" in MARKET_STATES


# =========================================================================
# Allowed risk modes
# =========================================================================
def test_allowed_risk_modes_count_5():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ALLOWED_RISK_MODES
    assert len(ALLOWED_RISK_MODES) == 5

def test_allowed_risk_mode_aggressive_paper():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ALLOWED_RISK_MODES
    assert "aggressive_paper" in ALLOWED_RISK_MODES

def test_allowed_risk_mode_normal_paper():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ALLOWED_RISK_MODES
    assert "normal_paper" in ALLOWED_RISK_MODES

def test_allowed_risk_mode_defensive_paper():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ALLOWED_RISK_MODES
    assert "defensive_paper" in ALLOWED_RISK_MODES

def test_allowed_risk_mode_observation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ALLOWED_RISK_MODES
    assert "observation_only" in ALLOWED_RISK_MODES

def test_allowed_risk_mode_freeze_promotion():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ALLOWED_RISK_MODES
    assert "freeze_promotion" in ALLOWED_RISK_MODES


# =========================================================================
# Theme actions
# =========================================================================
def test_theme_actions_count_7():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_ACTIONS
    assert len(THEME_ACTIONS) == 7

def test_theme_action_increase_attention():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_ACTIONS
    assert "increase_attention" in THEME_ACTIONS

def test_theme_action_keep_priority():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_ACTIONS
    assert "keep_priority" in THEME_ACTIONS

def test_theme_action_reduce_priority():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_ACTIONS
    assert "reduce_priority" in THEME_ACTIONS

def test_theme_action_freeze_new_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_ACTIONS
    assert "freeze_new_candidates" in THEME_ACTIONS

def test_theme_action_require_rescore():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_ACTIONS
    assert "require_rescore" in THEME_ACTIONS

def test_theme_action_downgrade_theme():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_ACTIONS
    assert "downgrade_theme" in THEME_ACTIONS

def test_theme_action_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import THEME_ACTIONS
    assert "human_review_required" in THEME_ACTIONS


# =========================================================================
# Priority changes
# =========================================================================
def test_priority_changes_count_6():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import PRIORITY_CHANGES
    assert len(PRIORITY_CHANGES) == 6

def test_priority_change_promote_priority():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import PRIORITY_CHANGES
    assert "promote_priority" in PRIORITY_CHANGES

def test_priority_change_keep_priority():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import PRIORITY_CHANGES
    assert "keep_priority" in PRIORITY_CHANGES

def test_priority_change_reduce_priority():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import PRIORITY_CHANGES
    assert "reduce_priority" in PRIORITY_CHANGES

def test_priority_change_freeze_candidate():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import PRIORITY_CHANGES
    assert "freeze_candidate" in PRIORITY_CHANGES

def test_priority_change_require_rescore():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import PRIORITY_CHANGES
    assert "require_rescore" in PRIORITY_CHANGES

def test_priority_change_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import PRIORITY_CHANGES
    assert "human_review_required" in PRIORITY_CHANGES


# =========================================================================
# CLI commands
# =========================================================================
def test_cli_commands_count_11():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CLI_COMMANDS_V207
    assert len(CLI_COMMANDS_V207) == 11

def test_cli_cmd_review_theme_rotation():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CLI_COMMANDS_V207
    assert "paper-cockpit-v207-review-theme-rotation" in CLI_COMMANDS_V207

def test_cli_cmd_evaluate_market_regime():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CLI_COMMANDS_V207
    assert "paper-cockpit-v207-evaluate-market-regime" in CLI_COMMANDS_V207

def test_cli_cmd_rank_themes():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CLI_COMMANDS_V207
    assert "paper-cockpit-v207-rank-themes" in CLI_COMMANDS_V207

def test_cli_cmd_detect_overheating():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CLI_COMMANDS_V207
    assert "paper-cockpit-v207-detect-overheating" in CLI_COMMANDS_V207

def test_cli_cmd_detect_weakening():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CLI_COMMANDS_V207
    assert "paper-cockpit-v207-detect-weakening" in CLI_COMMANDS_V207

def test_cli_cmd_adjust_candidate_priority():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CLI_COMMANDS_V207
    assert "paper-cockpit-v207-adjust-candidate-priority" in CLI_COMMANDS_V207

def test_cli_cmd_export_json():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CLI_COMMANDS_V207
    assert "paper-cockpit-v207-export-json" in CLI_COMMANDS_V207

def test_cli_cmd_export_md():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CLI_COMMANDS_V207
    assert "paper-cockpit-v207-export-md" in CLI_COMMANDS_V207

def test_cli_cmd_export_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CLI_COMMANDS_V207
    assert "paper-cockpit-v207-export-csv" in CLI_COMMANDS_V207

def test_cli_cmd_health():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CLI_COMMANDS_V207
    assert "paper-cockpit-v207-health" in CLI_COMMANDS_V207

def test_cli_cmd_gate():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CLI_COMMANDS_V207
    assert "paper-cockpit-v207-gate" in CLI_COMMANDS_V207


# =========================================================================
# GUI tabs
# =========================================================================
def test_gui_tabs_count_3():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import GUI_TABS_V207
    assert len(GUI_TABS_V207) == 3

def test_gui_tab_theme_rotation_v207():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import GUI_TABS_V207
    assert "theme_rotation_v207" in GUI_TABS_V207

def test_gui_tab_market_regime_v207():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import GUI_TABS_V207
    assert "market_regime_v207" in GUI_TABS_V207

def test_gui_tab_candidate_priority_adjustment_v207():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import GUI_TABS_V207
    assert "candidate_priority_adjustment_v207" in GUI_TABS_V207


# =========================================================================
# Models
# =========================================================================
def test_model_count_13():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import _ALL_MODEL_NAMES_V207
    assert len(_ALL_MODEL_NAMES_V207) == 13

def test_model_ThemeStrengthItem_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ThemeStrengthItem
    item = ThemeStrengthItem()
    assert item.schema_version == "207"
    assert item.paper_only is True
    assert item.no_real_orders is True

def test_model_MarketRegime_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MarketRegime
    regime = MarketRegime()
    assert regime.schema_version == "207"
    assert regime.paper_only is True
    assert regime.should_auto_apply is False

def test_model_CandidatePriorityAdjustment_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CandidatePriorityAdjustment
    adj = CandidatePriorityAdjustment()
    assert adj.schema_version == "207"
    assert adj.paper_only is True
    assert adj.should_auto_apply is False

def test_model_ThemeRotationSummary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ThemeRotationSummary
    summary = ThemeRotationSummary()
    assert summary.schema_version == "207"
    assert summary.paper_only is True

def test_model_ThemeRotationReviewInput_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ThemeRotationReviewInput
    inp = ThemeRotationReviewInput()
    assert inp.schema_version == "207"
    assert inp.paper_only is True

def test_model_ThemeRotationReviewResult_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ThemeRotationReviewResult
    result = ThemeRotationReviewResult()
    assert result.schema_version == "207"
    assert result.paper_only is True
    assert result.should_auto_apply is False

def test_model_ThemeRotationExportResult_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ThemeRotationExportResult
    exp = ThemeRotationExportResult()
    assert exp.schema_version == "207"
    assert exp.paper_only is True

def test_model_ThemeRotationAuditSnapshot_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ThemeRotationAuditSnapshot
    snap = ThemeRotationAuditSnapshot()
    assert snap.schema_version == "207"
    assert snap.paper_only is True

def test_model_ThemeRotationReport_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ThemeRotationReport
    report = ThemeRotationReport()
    assert report.schema_version == "207"
    assert report.paper_only is True

def test_model_ThemeStrengthCSV_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ThemeStrengthCSV
    csv = ThemeStrengthCSV()
    assert csv.schema_version == "207"
    assert csv.paper_only is True

def test_model_MarketRegimeCSV_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MarketRegimeCSV
    csv = MarketRegimeCSV()
    assert csv.schema_version == "207"
    assert csv.paper_only is True

def test_model_V207HealthSummary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import V207HealthSummary
    h = V207HealthSummary()
    assert h.schema_version == "207"
    assert h.version == "2.0.7"

def test_model_V207ReleaseSummary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import V207ReleaseSummary
    r = V207ReleaseSummary()
    assert r.version == "2.0.7"
    assert r.models_count == 13
    assert r.cli_count == 11
    assert r.gui_tabs_count == 3


# =========================================================================
# should_auto_apply invariants
# =========================================================================
def test_market_regime_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MarketRegime
    regime = MarketRegime(should_auto_apply=True)
    assert regime.should_auto_apply is False

def test_candidate_priority_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CandidatePriorityAdjustment
    adj = CandidatePriorityAdjustment(should_auto_apply=True)
    assert adj.should_auto_apply is False

def test_review_result_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ThemeRotationReviewResult
    result = ThemeRotationReviewResult(should_auto_apply=True)
    assert result.should_auto_apply is False

def test_market_regime_default_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MarketRegime
    regime = MarketRegime()
    assert regime.should_auto_apply is False

def test_candidate_priority_default_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CandidatePriorityAdjustment
    adj = CandidatePriorityAdjustment()
    assert adj.should_auto_apply is False


# =========================================================================
# Theme state classification
# =========================================================================
def test_classify_theme_state_leading():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    state = classify_theme_state(85.0, 80.0, 25.0, 10.0, 75.0)
    assert state == "leading"

def test_classify_theme_state_strengthening():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    state = classify_theme_state(72.0, 65.0, 20.0, 15.0, 60.0)
    assert state == "strengthening"

def test_classify_theme_state_overheating():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    state = classify_theme_state(88.0, 75.0, 80.0, 5.0, 70.0)
    assert state == "overheating"

def test_classify_theme_state_weakening():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    state = classify_theme_state(50.0, 40.0, 20.0, 75.0, 50.0)
    assert state == "weakening"

def test_classify_theme_state_emerging():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    state = classify_theme_state(48.0, 42.0, 10.0, 20.0, 40.0)
    assert state == "emerging"

def test_classify_theme_state_crowded():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    state = classify_theme_state(75.0, 65.0, 55.0, 10.0, 85.0)
    assert state == "crowded"

def test_classify_theme_state_cooling():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    state = classify_theme_state(35.0, 30.0, 15.0, 55.0, 30.0)
    assert state == "cooling"

def test_classify_theme_state_stale():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    state = classify_theme_state(15.0, 18.0, 5.0, 55.0, 15.0)
    assert state == "stale"

def test_classify_theme_state_neutral():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    state = classify_theme_state(52.0, 48.0, 30.0, 25.0, 50.0)
    assert state == "neutral"

def test_classify_theme_state_risk_off():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    state = classify_theme_state(20.0, 15.0, 0.0, 30.0, 20.0)
    assert state == "risk_off"

def test_classify_theme_state_overheating_boundary():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    # Exactly at overheat threshold
    state = classify_theme_state(90.0, 80.0, 75.0, 5.0, 80.0)
    assert state == "overheating"

def test_classify_theme_state_weakening_boundary():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    state = classify_theme_state(45.0, 40.0, 10.0, 70.0, 45.0)
    assert state == "weakening"


# =========================================================================
# Theme action classification
# =========================================================================
def test_classify_theme_action_emerging():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_action
    assert classify_theme_action("emerging") == "increase_attention"

def test_classify_theme_action_strengthening():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_action
    assert classify_theme_action("strengthening") == "increase_attention"

def test_classify_theme_action_leading():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_action
    assert classify_theme_action("leading") == "keep_priority"

def test_classify_theme_action_crowded():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_action
    assert classify_theme_action("crowded") == "require_rescore"

def test_classify_theme_action_overheating():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_action
    assert classify_theme_action("overheating") == "freeze_new_candidates"

def test_classify_theme_action_weakening():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_action
    assert classify_theme_action("weakening") == "reduce_priority"

def test_classify_theme_action_cooling():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_action
    assert classify_theme_action("cooling") == "downgrade_theme"

def test_classify_theme_action_stale():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_action
    assert classify_theme_action("stale") == "downgrade_theme"

def test_classify_theme_action_risk_off():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_action
    assert classify_theme_action("risk_off") == "human_review_required"

def test_classify_theme_action_neutral():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_action
    assert classify_theme_action("neutral") == "keep_priority"


# =========================================================================
# Market state classification
# =========================================================================
def test_classify_market_state_strong_uptrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(80.0, 75.0, 30.0, 70.0, 75.0) == "strong_uptrend"

def test_classify_market_state_healthy_pullback():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(60.0, 58.0, 38.0, 55.0, 62.0) == "healthy_pullback"

def test_classify_market_state_range_bound():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(50.0, 50.0, 40.0, 45.0, 50.0) == "range_bound"

def test_classify_market_state_weak_rebound():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(44.0, 40.0, 48.0, 36.0, 44.0) == "weak_rebound"

def test_classify_market_state_downtrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(25.0, 28.0, 55.0, 40.0, 35.0) == "downtrend"

def test_classify_market_state_high_volatility():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(50.0, 45.0, 85.0, 60.0, 40.0) == "high_volatility"

def test_classify_market_state_risk_off():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(20.0, 22.0, 70.0, 30.0, 15.0) == "risk_off"

def test_classify_market_state_high_volatility_overrides_uptrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    # Even with high index, high volatility wins
    state = classify_market_state(75.0, 70.0, 82.0, 65.0, 55.0)
    assert state == "high_volatility"

def test_classify_market_state_risk_off_overrides_downtrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    state = classify_market_state(28.0, 25.0, 65.0, 30.0, 18.0)
    assert state == "risk_off"


# =========================================================================
# Allowed risk mode classification
# =========================================================================
def test_classify_allowed_risk_mode_strong_uptrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_allowed_risk_mode
    assert classify_allowed_risk_mode("strong_uptrend") == "aggressive_paper"

def test_classify_allowed_risk_mode_healthy_pullback():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_allowed_risk_mode
    assert classify_allowed_risk_mode("healthy_pullback") == "normal_paper"

def test_classify_allowed_risk_mode_range_bound():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_allowed_risk_mode
    assert classify_allowed_risk_mode("range_bound") == "normal_paper"

def test_classify_allowed_risk_mode_weak_rebound():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_allowed_risk_mode
    assert classify_allowed_risk_mode("weak_rebound") == "defensive_paper"

def test_classify_allowed_risk_mode_downtrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_allowed_risk_mode
    assert classify_allowed_risk_mode("downtrend") == "observation_only"

def test_classify_allowed_risk_mode_high_volatility():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_allowed_risk_mode
    assert classify_allowed_risk_mode("high_volatility") == "defensive_paper"

def test_classify_allowed_risk_mode_risk_off():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_allowed_risk_mode
    assert classify_allowed_risk_mode("risk_off") == "freeze_promotion"


# =========================================================================
# Market regime entry flags
# =========================================================================
def test_entry_flags_strong_uptrend_promotion_allowed():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import _regime_entry_flags
    flags = _regime_entry_flags("strong_uptrend")
    assert flags["candidate_promotion_allowed"] is True

def test_entry_flags_strong_uptrend_aggressive_allowed():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import _regime_entry_flags
    flags = _regime_entry_flags("strong_uptrend")
    assert flags["aggressive_entry_allowed"] is True

def test_entry_flags_downtrend_promotion_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import _regime_entry_flags
    flags = _regime_entry_flags("downtrend")
    assert flags["candidate_promotion_allowed"] is False

def test_entry_flags_risk_off_promotion_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import _regime_entry_flags
    flags = _regime_entry_flags("risk_off")
    assert flags["candidate_promotion_allowed"] is False

def test_entry_flags_range_bound_aggressive_not_allowed():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import _regime_entry_flags
    flags = _regime_entry_flags("range_bound")
    assert flags["aggressive_entry_allowed"] is False

def test_entry_flags_strong_uptrend_breakout_allowed():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import _regime_entry_flags
    flags = _regime_entry_flags("strong_uptrend")
    assert flags["breakout_entry_allowed"] is True

def test_entry_flags_weak_rebound_breakout_not_allowed():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import _regime_entry_flags
    flags = _regime_entry_flags("weak_rebound")
    assert flags["breakout_entry_allowed"] is False


# =========================================================================
# evaluate_market_regime engine
# =========================================================================
def test_evaluate_market_regime_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import evaluate_market_regime
    regime = evaluate_market_regime()
    assert regime.should_auto_apply is False
    assert regime.market_state in ["strong_uptrend", "healthy_pullback", "range_bound",
                                   "weak_rebound", "downtrend", "high_volatility", "risk_off"]

def test_evaluate_market_regime_strong_uptrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import evaluate_market_regime, MarketRegime
    regime = evaluate_market_regime(MarketRegime(
        index_trend_score=82.0, breadth_score=78.0, volume_score=75.0,
        volatility_score=28.0, risk_appetite_score=80.0
    ))
    assert regime.market_state == "strong_uptrend"
    assert regime.allowed_risk_mode == "aggressive_paper"
    assert regime.aggressive_entry_allowed is True
    assert regime.should_auto_apply is False

def test_evaluate_market_regime_downtrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import evaluate_market_regime, MarketRegime
    regime = evaluate_market_regime(MarketRegime(
        index_trend_score=22.0, breadth_score=25.0, volume_score=35.0,
        volatility_score=60.0, risk_appetite_score=30.0
    ))
    assert regime.market_state == "downtrend"
    assert regime.candidate_promotion_allowed is False

def test_evaluate_market_regime_risk_off():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import evaluate_market_regime, MarketRegime
    regime = evaluate_market_regime(MarketRegime(
        index_trend_score=18.0, breadth_score=20.0, volume_score=28.0,
        volatility_score=72.0, risk_appetite_score=12.0
    ))
    assert regime.market_state == "risk_off"
    assert regime.allowed_risk_mode == "freeze_promotion"
    assert regime.candidate_promotion_allowed is False

def test_evaluate_market_regime_high_volatility():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import evaluate_market_regime, MarketRegime
    regime = evaluate_market_regime(MarketRegime(
        index_trend_score=50.0, breadth_score=45.0, volume_score=60.0,
        volatility_score=88.0, risk_appetite_score=38.0
    ))
    assert regime.market_state == "high_volatility"
    assert regime.allowed_risk_mode == "defensive_paper"

def test_evaluate_market_regime_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import evaluate_market_regime, MarketRegime
    regime = evaluate_market_regime(MarketRegime(should_auto_apply=True))
    assert regime.should_auto_apply is False


# =========================================================================
# rank_themes engine
# =========================================================================
def test_rank_themes_returns_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import rank_themes
    result = rank_themes()
    assert isinstance(result, list)

def test_rank_themes_default_non_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import rank_themes
    result = rank_themes()
    assert len(result) > 0

def test_rank_themes_sorted_by_score_descending():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import rank_themes
    result = rank_themes()
    for i in range(len(result) - 1):
        assert result[i].theme_score >= result[i + 1].theme_score

def test_rank_themes_ranks_set():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import rank_themes
    result = rank_themes()
    for idx, item in enumerate(result):
        assert item.theme_rank == idx + 1

def test_rank_themes_states_classified():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import rank_themes, THEME_STATES
    result = rank_themes()
    for item in result:
        assert item.theme_state in THEME_STATES


# =========================================================================
# detect_overheating engine
# =========================================================================
def test_detect_overheating_returns_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import detect_overheating
    result = detect_overheating()
    assert isinstance(result, list)

def test_detect_overheating_only_overheating_themes():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import detect_overheating
    result = detect_overheating()
    for item in result:
        assert item.theme_state == "overheating"

def test_detect_overheating_with_overheating_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import detect_overheating, ThemeStrengthItem
    items = [ThemeStrengthItem(theme_id="T1", theme_score=85.0, momentum_score=70.0,
                                overheating_score=80.0, weakening_score=5.0, breadth_score=70.0)]
    result = detect_overheating(items)
    assert len(result) == 1
    assert result[0].theme_id == "T1"

def test_detect_overheating_excludes_non_overheating():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import detect_overheating, ThemeStrengthItem
    items = [ThemeStrengthItem(theme_id="T1", theme_score=85.0, momentum_score=80.0,
                                overheating_score=20.0, weakening_score=5.0, breadth_score=75.0)]
    result = detect_overheating(items)
    assert len(result) == 0


# =========================================================================
# detect_weakening engine
# =========================================================================
def test_detect_weakening_returns_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import detect_weakening
    result = detect_weakening()
    assert isinstance(result, list)

def test_detect_weakening_only_weakening_or_cooling():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import detect_weakening
    result = detect_weakening()
    for item in result:
        assert item.theme_state in ("weakening", "cooling")

def test_detect_weakening_with_weakening_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import detect_weakening, ThemeStrengthItem
    items = [ThemeStrengthItem(theme_id="T1", theme_score=45.0, momentum_score=40.0,
                                overheating_score=10.0, weakening_score=78.0, breadth_score=45.0)]
    result = detect_weakening(items)
    assert len(result) == 1

def test_detect_weakening_includes_cooling():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import detect_weakening, ThemeStrengthItem
    items = [ThemeStrengthItem(theme_id="T1", theme_score=35.0, momentum_score=30.0,
                                overheating_score=15.0, weakening_score=55.0, breadth_score=30.0)]
    result = detect_weakening(items)
    assert len(result) == 1
    assert result[0].theme_state == "cooling"


# =========================================================================
# adjust_candidate_priority engine
# =========================================================================
def test_adjust_candidate_priority_returns_adjustment():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
        adjust_candidate_priority, ThemeStrengthItem, MarketRegime,
    )
    item = ThemeStrengthItem(theme_id="T1", theme_state="leading")
    regime = MarketRegime(market_state="range_bound")
    adj = adjust_candidate_priority("2330", "台積電", "CAND-001", item, regime)
    assert adj.symbol == "2330"
    assert adj.should_auto_apply is False

def test_adjust_candidate_priority_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
        adjust_candidate_priority, ThemeStrengthItem, MarketRegime,
    )
    adj = adjust_candidate_priority(
        "2330", "台積電", "CAND-001",
        ThemeStrengthItem(theme_id="T1", theme_state="leading"),
        MarketRegime(market_state="strong_uptrend"),
    )
    assert adj.should_auto_apply is False

def test_adjust_candidate_priority_blocked_by_market_downtrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
        adjust_candidate_priority, ThemeStrengthItem, MarketRegime, evaluate_market_regime,
    )
    regime = evaluate_market_regime(MarketRegime(
        index_trend_score=22.0, breadth_score=25.0, volume_score=35.0,
        volatility_score=60.0, risk_appetite_score=30.0,
    ))
    adj = adjust_candidate_priority(
        "2330", "台積電", "CAND-001",
        ThemeStrengthItem(theme_id="T1", theme_state="neutral"),
        regime,
    )
    assert adj.blocked_by_market_regime is True

def test_adjust_candidate_priority_blocked_by_theme_overheating():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
        adjust_candidate_priority, ThemeStrengthItem, MarketRegime,
    )
    adj = adjust_candidate_priority(
        "2330", "台積電", "CAND-001",
        ThemeStrengthItem(theme_id="T1", theme_state="overheating"),
        MarketRegime(market_state="range_bound", candidate_promotion_allowed=True),
    )
    assert adj.blocked_by_theme_state is True

def test_adjust_candidate_priority_blocked_by_theme_stale():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
        adjust_candidate_priority, ThemeStrengthItem, MarketRegime,
    )
    adj = adjust_candidate_priority(
        "2330", "台積電", "CAND-001",
        ThemeStrengthItem(theme_id="T1", theme_state="stale"),
        MarketRegime(market_state="range_bound"),
    )
    assert adj.blocked_by_theme_state is True

def test_adjust_candidate_priority_human_review_for_risk_off():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
        adjust_candidate_priority, ThemeStrengthItem, MarketRegime, classify_theme_action,
    )
    item = ThemeStrengthItem(theme_id="T1", theme_state="risk_off",
                              theme_action=classify_theme_action("risk_off"))
    adj = adjust_candidate_priority(
        "2330", "台積電", "CAND-001",
        item,
        MarketRegime(market_state="range_bound"),
    )
    assert adj.requires_human_review is True

def test_adjust_candidate_priority_final_score_in_range():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import (
        adjust_candidate_priority, ThemeStrengthItem, MarketRegime,
    )
    adj = adjust_candidate_priority(
        "2330", "台積電", "CAND-001",
        ThemeStrengthItem(theme_id="T1", theme_state="leading"),
        MarketRegime(market_state="range_bound"),
        original_score=70.0,
    )
    assert 0.0 <= adj.final_priority_score <= 100.0


# =========================================================================
# run_theme_rotation_review engine
# =========================================================================
def test_run_theme_rotation_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result is not None

def test_run_theme_rotation_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.paper_only is True

def test_run_theme_rotation_review_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.all_passed is True

def test_run_theme_rotation_review_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.should_auto_apply is False

def test_run_theme_rotation_review_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.theme_rotation_version == "2.0.7"

def test_run_theme_rotation_review_has_review_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.theme_rotation_review_id != ""
    assert len(result.theme_rotation_review_id) == 10

def test_run_theme_rotation_review_has_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.theme_rotation_summary is not None

def test_run_theme_rotation_review_has_market_regime_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert len(result.market_regime_snapshot) >= 2

def test_run_theme_rotation_review_has_theme_strength_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert len(result.theme_strength_snapshot) > 0

def test_run_theme_rotation_review_paper_only_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.paper_only_safety_snapshot is True

def test_run_theme_rotation_review_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.no_real_orders is True

def test_run_theme_rotation_review_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.no_broker is True

def test_run_theme_rotation_review_research_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.research_only is True

def test_run_theme_rotation_review_theme_rotation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.theme_rotation_only is True


# =========================================================================
# Export functions
# =========================================================================
def test_export_json_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_json
    result = export_theme_rotation_json(run_theme_rotation_review())
    assert result is not None

def test_export_json_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_json
    result = export_theme_rotation_json(run_theme_rotation_review())
    assert result.is_valid is True

def test_export_json_has_review_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_json
    review = run_theme_rotation_review()
    result = export_theme_rotation_json(review)
    assert review.theme_rotation_review_id in result.content

def test_export_json_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_json
    result = export_theme_rotation_json(run_theme_rotation_review())
    assert result.paper_only is True
    assert "paper_only" in result.content

def test_export_json_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_json
    result = export_theme_rotation_json(run_theme_rotation_review())
    assert "should_auto_apply" in result.content
    assert "false" in result.content.lower()

def test_export_json_status_complete():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_json
    result = export_theme_rotation_json(run_theme_rotation_review())
    assert result.export_status == "complete"

def test_export_markdown_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_markdown
    result = export_theme_rotation_markdown(run_theme_rotation_review())
    assert result is not None

def test_export_markdown_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_markdown
    result = export_theme_rotation_markdown(run_theme_rotation_review())
    assert result.is_valid is True

def test_export_markdown_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_markdown
    result = export_theme_rotation_markdown(run_theme_rotation_review())
    assert "Theme Rotation Report v2.0.7" in result.content

def test_export_markdown_paper_only_disclaimer():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_markdown
    result = export_theme_rotation_markdown(run_theme_rotation_review())
    assert "Paper Only" in result.content

def test_export_markdown_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_markdown
    result = export_theme_rotation_markdown(run_theme_rotation_review())
    assert result.export_format == "markdown"

def test_export_theme_strength_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_strength_csv
    result = export_theme_strength_csv(run_theme_rotation_review())
    assert result is not None

def test_export_theme_strength_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_strength_csv
    result = export_theme_strength_csv(run_theme_rotation_review())
    assert result.is_valid is True

def test_export_theme_strength_csv_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_strength_csv
    result = export_theme_strength_csv(run_theme_rotation_review())
    assert "theme_id" in result.csv_content
    assert "theme_state" in result.csv_content

def test_export_theme_strength_csv_has_rows():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_strength_csv
    result = export_theme_strength_csv(run_theme_rotation_review())
    assert result.row_count > 0

def test_export_theme_strength_csv_false_column():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_strength_csv
    result = export_theme_strength_csv(run_theme_rotation_review())
    assert "False" in result.csv_content

def test_export_market_regime_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_market_regime_csv
    result = export_market_regime_csv(run_theme_rotation_review())
    assert result is not None

def test_export_market_regime_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_market_regime_csv
    result = export_market_regime_csv(run_theme_rotation_review())
    assert result.is_valid is True

def test_export_market_regime_csv_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_market_regime_csv
    result = export_market_regime_csv(run_theme_rotation_review())
    assert "should_auto_apply,False" in result.csv_content

def test_export_candidate_priority_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_candidate_priority_csv
    result = export_candidate_priority_csv(run_theme_rotation_review())
    assert result is not None

def test_export_candidate_priority_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_candidate_priority_csv
    result = export_candidate_priority_csv(run_theme_rotation_review())
    assert result.is_valid is True

def test_export_audit_snapshot_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_audit_snapshot
    result = export_theme_rotation_audit_snapshot(run_theme_rotation_review())
    assert result is not None

def test_export_audit_snapshot_has_hash():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_audit_snapshot
    result = export_theme_rotation_audit_snapshot(run_theme_rotation_review())
    assert result.reproducibility_hash != ""

def test_export_audit_snapshot_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, export_theme_rotation_audit_snapshot
    result = export_theme_rotation_audit_snapshot(run_theme_rotation_review())
    assert "paper_only=True" in result.safety_snapshot
    assert "should_auto_apply=False" in result.safety_snapshot


# =========================================================================
# ThemeRotationSummary
# =========================================================================
def test_summary_total_theme_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.theme_rotation_summary.total_theme_count == len(result.theme_rotation_action_queue)

def test_summary_quality_grades_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    summary = result.theme_rotation_summary
    assert summary.theme_rotation_quality_grade in ("A", "B", "C", "D")
    assert summary.market_regime_quality_grade in ("A", "B", "C", "D")

def test_summary_promotion_counts():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    summary = result.theme_rotation_summary
    total = summary.promotion_allowed_count + summary.promotion_blocked_count
    assert total == len(result.candidate_priority_adjustment_snapshot)


# =========================================================================
# CLI registration health
# =========================================================================
def test_cli_registry_has_v207_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd in [
        "paper-cockpit-v207-review-theme-rotation",
        "paper-cockpit-v207-evaluate-market-regime",
        "paper-cockpit-v207-rank-themes",
        "paper-cockpit-v207-detect-overheating",
        "paper-cockpit-v207-detect-weakening",
        "paper-cockpit-v207-adjust-candidate-priority",
        "paper-cockpit-v207-export-json",
        "paper-cockpit-v207-export-md",
        "paper-cockpit-v207-export-csv",
        "paper-cockpit-v207-health",
        "paper-cockpit-v207-gate",
    ]:
        assert cmd in cmd_names, f"CLI command '{cmd}' not in PROVIDER_COMMANDS"

def test_cli_registry_v207_group():
    from cli.command_registry import PROVIDER_COMMANDS
    v207_cmds = [c for c in PROVIDER_COMMANDS if c.group == "paper_cockpit_v207"]
    assert len(v207_cmds) == 11

def test_cli_registry_v207_introduced_in():
    from cli.command_registry import PROVIDER_COMMANDS
    v207_cmds = [c for c in PROVIDER_COMMANDS if c.group == "paper_cockpit_v207"]
    for cmd in v207_cmds:
        assert cmd.introduced_in == "2.0.7"

def test_cli_registry_v207_safety_classification():
    from cli.command_registry import PROVIDER_COMMANDS
    v207_cmds = [c for c in PROVIDER_COMMANDS if c.group == "paper_cockpit_v207"]
    for cmd in v207_cmds:
        assert cmd.safety_classification == "RESEARCH_ONLY"


# =========================================================================
# CLI handler resolution (main.py — handler existence, no module-level split)
# =========================================================================
_V207_HANDLER_NAMES = [
    "cmd_paper_cockpit_v207_review_theme_rotation",
    "cmd_paper_cockpit_v207_evaluate_market_regime",
    "cmd_paper_cockpit_v207_rank_themes",
    "cmd_paper_cockpit_v207_detect_overheating",
    "cmd_paper_cockpit_v207_detect_weakening",
    "cmd_paper_cockpit_v207_adjust_candidate_priority",
    "cmd_paper_cockpit_v207_export_json",
    "cmd_paper_cockpit_v207_export_md",
    "cmd_paper_cockpit_v207_export_csv",
    "cmd_paper_cockpit_v207_health",
    "cmd_paper_cockpit_v207_gate",
]

def test_main_has_no_split_command_map():
    """main.py must NOT export a module-level command_map that splits from runtime dispatch."""
    import main as _main
    # No module-level command_map should exist (it would split from the runtime one in main())
    assert not hasattr(_main, "command_map"), (
        "main.py must not have a module-level command_map; "
        "v207 commands are in the runtime dispatch dict inside main()"
    )

def test_main_v207_handlers_all_exist():
    import main as _main
    for name in _V207_HANDLER_NAMES:
        assert hasattr(_main, name), f"main.py missing handler: '{name}'"

def test_main_v207_handlers_all_callable():
    import main as _main
    for name in _V207_HANDLER_NAMES:
        assert callable(getattr(_main, name)), f"handler '{name}' is not callable"

def test_main_v207_no_isolated_fake_map():
    """Verify no module-level dict named command_map or _command_map exists (would be a fake)."""
    import main as _main
    for attr in ("command_map", "_command_map", "V207_COMMAND_MAP"):
        assert not hasattr(_main, attr), f"main.py must not export '{attr}' at module level"

def test_main_v207_review_handler_runs():
    import main as _main
    _main.cmd_paper_cockpit_v207_review_theme_rotation()

def test_main_v207_evaluate_regime_handler_runs():
    import main as _main
    _main.cmd_paper_cockpit_v207_evaluate_market_regime()

def test_main_v207_rank_themes_handler_runs():
    import main as _main
    _main.cmd_paper_cockpit_v207_rank_themes()

def test_main_v207_detect_overheating_handler_runs():
    import main as _main
    _main.cmd_paper_cockpit_v207_detect_overheating()

def test_main_v207_detect_weakening_handler_runs():
    import main as _main
    _main.cmd_paper_cockpit_v207_detect_weakening()

def test_main_v207_adjust_priority_handler_runs():
    import main as _main
    _main.cmd_paper_cockpit_v207_adjust_candidate_priority()

def test_main_v207_export_json_handler_runs():
    import main as _main
    _main.cmd_paper_cockpit_v207_export_json()

def test_main_v207_export_md_handler_runs():
    import main as _main
    _main.cmd_paper_cockpit_v207_export_md()

def test_main_v207_export_csv_handler_runs():
    import main as _main
    _main.cmd_paper_cockpit_v207_export_csv()

def test_main_v207_health_handler_runs():
    import main as _main
    _main.cmd_paper_cockpit_v207_health()

def test_main_v207_gate_handler_runs():
    import main as _main
    _main.cmd_paper_cockpit_v207_gate()

def test_main_v207_cli_registry_aligns_with_handlers():
    """CLI registry commands must align with existing handler functions in main."""
    import main as _main
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd, handler_name in zip([
        "paper-cockpit-v207-review-theme-rotation",
        "paper-cockpit-v207-evaluate-market-regime",
        "paper-cockpit-v207-rank-themes",
        "paper-cockpit-v207-detect-overheating",
        "paper-cockpit-v207-detect-weakening",
        "paper-cockpit-v207-adjust-candidate-priority",
        "paper-cockpit-v207-export-json",
        "paper-cockpit-v207-export-md",
        "paper-cockpit-v207-export-csv",
        "paper-cockpit-v207-health",
        "paper-cockpit-v207-gate",
    ], _V207_HANDLER_NAMES):
        assert cmd in cmd_names, f"CLI registry missing '{cmd}'"
        assert hasattr(_main, handler_name), f"main.py missing handler '{handler_name}'"


# =========================================================================
# GUI compatibility
# =========================================================================
def test_gui_panel_version_v207():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V207
    assert PANEL_VERSION_V207 == "2.0.7"

def test_gui_panel_version_still_200():
    from gui.small_capital_strategy_panel import PANEL_VERSION
    assert PANEL_VERSION == "2.0.0"

def test_gui_v207_tab_names():
    from gui.small_capital_strategy_panel import get_v207_tab_names
    tabs = get_v207_tab_names()
    assert len(tabs) == 3

def test_gui_v207_tab_theme_rotation():
    from gui.small_capital_strategy_panel import get_v207_tab_names
    assert "theme_rotation_v207" in get_v207_tab_names()

def test_gui_v207_tab_market_regime():
    from gui.small_capital_strategy_panel import get_v207_tab_names
    assert "market_regime_v207" in get_v207_tab_names()

def test_gui_v207_tab_candidate_priority():
    from gui.small_capital_strategy_panel import get_v207_tab_names
    assert "candidate_priority_adjustment_v207" in get_v207_tab_names()

def test_gui_get_tab_names_includes_v207():
    from gui.small_capital_strategy_panel import get_tab_names
    tabs = get_tab_names()
    for tab in ["theme_rotation_v207", "market_regime_v207", "candidate_priority_adjustment_v207"]:
        assert tab in tabs

def test_gui_render_theme_rotation_v207_tab():
    from gui.small_capital_strategy_panel import render_theme_rotation_v207_tab
    result = render_theme_rotation_v207_tab()
    assert result["tab"] == "theme_rotation_v207"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False

def test_gui_render_market_regime_v207_tab():
    from gui.small_capital_strategy_panel import render_market_regime_v207_tab
    result = render_market_regime_v207_tab()
    assert result["tab"] == "market_regime_v207"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False

def test_gui_render_candidate_priority_adjustment_v207_tab():
    from gui.small_capital_strategy_panel import render_candidate_priority_adjustment_v207_tab
    result = render_candidate_priority_adjustment_v207_tab()
    assert result["tab"] == "candidate_priority_adjustment_v207"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False

def test_gui_render_all_tabs_includes_v207():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    for tab in ["theme_rotation_v207", "market_regime_v207", "candidate_priority_adjustment_v207"]:
        assert tab in result

def test_gui_render_all_tabs_v207_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    for tab in ["theme_rotation_v207", "market_regime_v207", "candidate_priority_adjustment_v207"]:
        assert "error" not in result.get(tab, {}), f"Tab '{tab}' has error"

def test_gui_render_all_tabs_global_no_error_tabs():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    error_tabs = [k for k, v in result.items() if "error" in v]
    assert not error_tabs, f"render_all_tabs has error tabs: {error_tabs}"

def test_gui_render_theme_rotation_no_real_orders():
    from gui.small_capital_strategy_panel import render_theme_rotation_v207_tab
    result = render_theme_rotation_v207_tab()
    assert result["no_real_orders"] is True

def test_gui_render_market_regime_no_broker():
    from gui.small_capital_strategy_panel import render_market_regime_v207_tab
    result = render_market_regime_v207_tab()
    assert result["no_broker"] is True

def test_gui_render_candidate_priority_not_investment_advice():
    from gui.small_capital_strategy_panel import render_candidate_priority_adjustment_v207_tab
    result = render_candidate_priority_adjustment_v207_tab()
    assert result["not_investment_advice"] is True


# =========================================================================
# Replay lineage handler integrity
# =========================================================================
def test_replay_lineage_v207_review_id_deterministic():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, ThemeRotationReviewInput
    inp = ThemeRotationReviewInput(review_period="2026-W29")
    r1 = run_theme_rotation_review(inp)
    r2 = run_theme_rotation_review(inp)
    assert r1.theme_rotation_review_id == r2.theme_rotation_review_id

def test_replay_lineage_different_periods_different_ids():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review, ThemeRotationReviewInput
    r1 = run_theme_rotation_review(ThemeRotationReviewInput(review_period="2026-W29"))
    r2 = run_theme_rotation_review(ThemeRotationReviewInput(review_period="2026-W30"))
    assert r1.theme_rotation_review_id != r2.theme_rotation_review_id


# =========================================================================
# Paper-only safety
# =========================================================================
def test_paper_only_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_paper_only_broker_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_paper_only_production_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True

def test_paper_only_result_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.no_real_orders is True

def test_paper_only_result_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.no_broker is True

def test_paper_only_result_not_investment_advice():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.not_investment_advice is True

def test_paper_only_result_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.human_review_required is True


# =========================================================================
# Backward compatibility with v2.0.6
# =========================================================================
def test_backward_compat_v206_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v206

def test_backward_compat_v206_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import VERSION
    assert VERSION == "2.0.6"

def test_backward_compat_v206_lifecycle_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    result = run_lifecycle_review()
    assert result.paper_only is True
    assert result.should_auto_apply is False

def test_backward_compat_v205_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v205

def test_backward_compat_v205_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import VERSION
    assert VERSION == "2.0.5"

def test_backward_compat_v205_rotation_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    result = run_watchlist_rotation()
    assert result.paper_only is True

def test_backward_compat_v206_safety_flags_20():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert len(SAFETY_FLAGS_V206) == 20

def test_backward_compat_v206_gui_tabs_still_present():
    from gui.small_capital_strategy_panel import get_tab_names
    tabs = get_tab_names()
    for tab in ["candidate_lifecycle_v206", "setup_aging_v206", "stale_candidate_queue_v206"]:
        assert tab in tabs

def test_backward_compat_v205_gui_tabs_still_present():
    from gui.small_capital_strategy_panel import get_tab_names
    tabs = get_tab_names()
    for tab in ["watchlist_rotation_v205", "promotion_queue_v205", "human_review_queue_v205"]:
        assert tab in tabs


# =========================================================================
# v201 health relative-path compatibility
# =========================================================================
def test_v201_health_test_file_exists():
    import os
    test_file = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "test_paper_cockpit_v201.py"
    ))
    assert os.path.exists(test_file), "test_paper_cockpit_v201.py not found"


# =========================================================================
# Scenarios
# =========================================================================
def test_scenarios_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v207 import SCENARIOS
    assert len(SCENARIOS) == 80

def test_scenarios_schema_version_207():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v207 import SCENARIOS
    assert all(s["schema_version"] == "207" for s in SCENARIOS)

def test_scenarios_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v207 import SCENARIOS
    assert all(s["paper_only"] is True for s in SCENARIOS)

def test_scenarios_unique_ids():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v207 import SCENARIOS
    ids = [s["scenario_id"] for s in SCENARIOS]
    assert len(ids) == len(set(ids))

def test_scenarios_all_have_description():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v207 import SCENARIOS
    for s in SCENARIOS:
        assert "description" in s or "scenario_id" in s


# =========================================================================
# Fixtures
# =========================================================================
def test_fixtures_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v207 import FIXTURES
    assert len(FIXTURES) == 80

def test_fixtures_schema_version_207():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v207 import FIXTURES
    assert all(f["schema_version"] == "207" for f in FIXTURES)

def test_fixtures_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v207 import FIXTURES
    assert all(f["paper_only"] is True for f in FIXTURES)

def test_fixtures_have_fixture_id():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v207 import FIXTURES
    assert all("fixture_id" in f for f in FIXTURES)

def test_fixtures_unique_ids():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v207 import FIXTURES
    ids = [f["fixture_id"] for f in FIXTURES]
    assert len(ids) == len(set(ids))


# =========================================================================
# Health check
# =========================================================================
def test_health_check_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_health_v207

def test_health_check_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v207 import run_health_check
    result = run_health_check()
    assert result is not None

def test_health_check_returns_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v207 import run_health_check
    result = run_health_check()
    assert isinstance(result, dict)

def test_health_check_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v207 import run_health_check
    result = run_health_check()
    assert result["all_passed"] is True, f"Health check failed: {result.get('errors', [])}"

def test_health_check_version():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v207 import run_health_check
    result = run_health_check()
    assert result["version"] == "2.0.7"


# =========================================================================
# Release gate
# =========================================================================
def test_release_gate_importable():
    import release.paper_cockpit_release_gate_v207

def test_release_gate_callable():
    from release.paper_cockpit_release_gate_v207 import run_release_gate
    result = run_release_gate()
    assert result is not None

def test_release_gate_returns_dict():
    from release.paper_cockpit_release_gate_v207 import run_release_gate
    result = run_release_gate()
    assert isinstance(result, dict)

def test_release_gate_passed():
    from release.paper_cockpit_release_gate_v207 import run_release_gate
    result = run_release_gate()
    assert result["gate_passed"] is True, f"Gate failed: {result.get('errors', [])}"

def test_release_gate_version():
    from release.paper_cockpit_release_gate_v207 import GATE_VERSION
    assert GATE_VERSION == "2.0.7"


# =========================================================================
# get_cockpit_summary_v207
# =========================================================================
def test_cockpit_summary_v207():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import get_cockpit_summary_v207
    summary = get_cockpit_summary_v207()
    assert summary["version"] == "2.0.7"
    assert summary["paper_only"] is True
    assert summary["should_auto_apply"] is False
    assert summary["should_auto_apply_theme_rotation"] is False
    assert summary["models_count"] == 13
    assert summary["cli_commands_count"] == 11
    assert summary["gui_tabs_count"] == 3
    assert summary["safety_flags_count"] == 20
    assert summary["theme_states_count"] == 10
    assert summary["market_states_count"] == 7
    assert summary["allowed_risk_modes_count"] == 5
    assert summary["theme_actions_count"] == 7
    assert summary["priority_changes_count"] == 6


# =========================================================================
# Theme state boundary conditions (extended)
# =========================================================================
def test_classify_theme_state_emerging_upper_boundary():
    """theme_score just below 50 with sufficient momentum → emerging."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    assert classify_theme_state(49.9, 38.0, 10.0, 15.0, 35.0) == "emerging"

def test_classify_theme_state_neutral_at_50():
    """theme_score exactly 50 → neutral (not emerging)."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    assert classify_theme_state(50.0, 40.0, 20.0, 25.0, 45.0) == "neutral"

def test_classify_theme_state_strengthening_at_55_50():
    """theme_score=55, momentum=50 → strengthening (meets the >= 55 / >= 50 threshold)."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    assert classify_theme_state(55.0, 50.0, 30.0, 20.0, 50.0) == "strengthening"

def test_classify_theme_state_risk_off_low_weakening():
    """risk_off requires weakening_score < 50 (not in weakening/cooling zone)."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    assert classify_theme_state(18.0, 12.0, 5.0, 10.0, 15.0) == "risk_off"

def test_classify_theme_state_cooling_not_risk_off_high_weakening():
    """weakening_score >= 50 → cooling, not risk_off, even if momentum/theme are low."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    assert classify_theme_state(25.0, 18.0, 5.0, 55.0, 20.0) == "cooling"

def test_classify_theme_state_overheating_exact_threshold():
    """overheating_score exactly 75.0 → overheating."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    assert classify_theme_state(85.0, 70.0, 75.0, 5.0, 70.0) == "overheating"

def test_classify_theme_state_weakening_exact_threshold():
    """weakening_score exactly 70.0 → weakening."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    assert classify_theme_state(50.0, 42.0, 20.0, 70.0, 48.0) == "weakening"

def test_classify_theme_state_stale_very_low_theme():
    """theme_score < 20 with weakening → stale."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    assert classify_theme_state(10.0, 8.0, 2.0, 60.0, 10.0) == "stale"

def test_classify_theme_state_leading_high_breadth():
    """high theme + momentum + high breadth → leading."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_state
    assert classify_theme_state(85.0, 78.0, 20.0, 8.0, 80.0) == "leading"


# =========================================================================
# Market state boundary conditions (extended)
# =========================================================================
def test_classify_market_state_range_bound_exact_boundary():
    """Scores exactly at range_bound thresholds."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(40.0, 45.0, 30.0, 40.0, 45.0) == "range_bound"

def test_classify_market_state_healthy_pullback_at_threshold():
    """index=55, breadth=55 at exact healthy_pullback threshold."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(55.0, 55.0, 35.0, 50.0, 58.0) == "healthy_pullback"

def test_classify_market_state_high_volatility_priority():
    """high_volatility checked first regardless of other scores."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(80.0, 75.0, 80.0, 70.0, 75.0) == "high_volatility"

def test_classify_market_state_risk_off_priority():
    """risk_off: low risk_appetite AND low index."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(20.0, 25.0, 60.0, 15.0, 15.0) == "risk_off"

def test_classify_market_state_downtrend_exact():
    """index <= 35, breadth <= 40 → downtrend."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(35.0, 40.0, 55.0, 40.0, 35.0) == "downtrend"

def test_classify_market_state_weak_rebound_low_breadth():
    """weak_rebound: index 40-55, breadth < 45, volume < 50."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(44.0, 40.0, 48.0, 36.0, 44.0) == "weak_rebound"

def test_classify_market_state_strong_uptrend_all_high():
    """All high scores → strong_uptrend."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_market_state
    assert classify_market_state(80.0, 75.0, 30.0, 70.0, 75.0) == "strong_uptrend"


# =========================================================================
# Market regime blocked promotion
# =========================================================================
def test_market_regime_risk_off_blocks_promotion_via_entry_flags():
    """_regime_entry_flags: risk_off → candidate_promotion_allowed=False."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import _regime_entry_flags
    flags = _regime_entry_flags("risk_off")
    assert flags["candidate_promotion_allowed"] is False

def test_market_regime_downtrend_blocks_promotion():
    """downtrend → observation_only, candidate_promotion_allowed=False."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MarketRegime
    regime = MarketRegime(market_state="downtrend", allowed_risk_mode="observation_only",
                          candidate_promotion_allowed=False)
    assert regime.candidate_promotion_allowed is False

def test_market_regime_observation_only_blocks_promotion():
    """observation_only mode blocks candidate promotion."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MarketRegime
    regime = MarketRegime(market_state="downtrend", allowed_risk_mode="observation_only",
                          candidate_promotion_allowed=False)
    assert regime.allowed_risk_mode == "observation_only"
    assert regime.candidate_promotion_allowed is False

def test_market_regime_evaluate_default_no_auto_apply():
    """evaluate_market_regime() always returns should_auto_apply=False."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import evaluate_market_regime
    regime = evaluate_market_regime()
    assert regime.should_auto_apply is False

def test_market_regime_should_auto_apply_cannot_be_set_true():
    """MarketRegime.__post_init__ forces should_auto_apply=False even if True passed."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import MarketRegime
    regime = MarketRegime(market_state="strong_uptrend", should_auto_apply=True)
    assert regime.should_auto_apply is False


# =========================================================================
# Theme state blocked promotion
# =========================================================================
def test_overheating_theme_freeze_new_candidates():
    """overheating theme_state → freeze_new_candidates action."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_action
    assert classify_theme_action("overheating") == "freeze_new_candidates"

def test_risk_off_theme_human_review_required():
    """risk_off theme_state → human_review_required action."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import classify_theme_action
    assert classify_theme_action("risk_off") == "human_review_required"

def test_detect_overheating_returns_list():
    """detect_overheating returns a list."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import detect_overheating, _default_theme_items
    items = _default_theme_items()
    result = detect_overheating(items)
    assert isinstance(result, list)

def test_detect_weakening_returns_list():
    """detect_weakening returns a list."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import detect_weakening, _default_theme_items
    items = _default_theme_items()
    result = detect_weakening(items)
    assert isinstance(result, list)

def test_candidate_priority_should_auto_apply_always_false_post_init():
    """CandidatePriorityAdjustment.__post_init__ enforces should_auto_apply=False."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import CandidatePriorityAdjustment
    adj = CandidatePriorityAdjustment(should_auto_apply=True)
    assert adj.should_auto_apply is False

def test_theme_rotation_review_result_auto_apply_always_false():
    """ThemeRotationReviewResult.__post_init__ enforces should_auto_apply=False."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import ThemeRotationReviewResult
    r = ThemeRotationReviewResult(should_auto_apply=True)
    assert r.should_auto_apply is False


# =========================================================================
# render_all_tabs zero error tabs (extended)
# =========================================================================
def test_render_all_tabs_no_errors_v207():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    error_tabs = [k for k, v in result.items() if "error" in v]
    assert not error_tabs, f"render_all_tabs has error tabs: {error_tabs}"

def test_render_theme_rotation_tab_fields():
    from gui.small_capital_strategy_panel import render_theme_rotation_v207_tab
    tab = render_theme_rotation_v207_tab()
    assert tab.get("version") == "2.0.7"
    assert tab.get("paper_only") is True
    assert tab.get("should_auto_apply") is False

def test_render_market_regime_tab_fields():
    from gui.small_capital_strategy_panel import render_market_regime_v207_tab
    tab = render_market_regime_v207_tab()
    assert tab.get("version") == "2.0.7"
    assert tab.get("paper_only") is True
    assert tab.get("should_auto_apply") is False

def test_render_candidate_priority_adjustment_tab_fields():
    from gui.small_capital_strategy_panel import render_candidate_priority_adjustment_v207_tab
    tab = render_candidate_priority_adjustment_v207_tab()
    assert tab.get("version") == "2.0.7"
    assert tab.get("paper_only") is True
    assert tab.get("should_auto_apply") is False


# =========================================================================
# v2.0.6 lifecycle integration
# =========================================================================
def test_v206_lifecycle_review_runs_after_v207_import():
    """Importing v207 must not break v206 lifecycle review."""
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import VERSION as V207
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    result = run_lifecycle_review()
    assert result is not None
    assert result.paper_only is True

def test_v206_safety_flags_count_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    assert len(SAFETY_FLAGS_V206) == 20

def test_v206_no_real_orders_still_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_v206_broker_execution_still_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_v207_does_not_mutate_v206_module():
    """v207 import must not alter v206 VERSION or SCHEMA_VERSION."""
    import paper_trading.small_capital_strategy.paper_cockpit_v207  # noqa: F401
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import VERSION, SCHEMA_VERSION
    assert VERSION == "2.0.6"
    assert SCHEMA_VERSION == "206"
