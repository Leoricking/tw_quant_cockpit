"""
tests/test_paper_cockpit_v212.py
v2.0.12 Paper Profit Taking & ETF Rebalancing Control — Main Tests
[!] Paper Only. Research Only. Profit Taking Recommendation Only. No Real Orders. Not Investment Advice.
"""
import pytest


# =========================================================================
# Section 1: Module import & version constants
# =========================================================================
def test_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v212

def test_version_is_212():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import VERSION
    assert VERSION == "2.0.12"

def test_schema_version_is_212():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "212"

def test_release_name_contains_profit():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import RELEASE_NAME
    assert "Profit" in RELEASE_NAME or "Taking" in RELEASE_NAME

def test_release_name_contains_etf():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import RELEASE_NAME
    assert "ETF" in RELEASE_NAME or "Rebalancing" in RELEASE_NAME

def test_baseline_tests_set():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import BASELINE_TESTS
    assert BASELINE_TESTS == 36361

def test_min_new_tests_300():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300

def test_verify_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import verify_version
    assert verify_version() is True


# =========================================================================
# Section 2: Safety constants
# =========================================================================
def test_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True


# =========================================================================
# Section 3: PROFIT_ACTIONS
# =========================================================================
def test_profit_actions_count_9():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_ACTIONS
    assert len(PROFIT_ACTIONS) == 9

def test_profit_action_hold_with_plan():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_ACTIONS
    assert "hold_with_plan" in PROFIT_ACTIONS

def test_profit_action_take_first_third():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_ACTIONS
    assert "take_first_third" in PROFIT_ACTIONS

def test_profit_action_take_second_third():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_ACTIONS
    assert "take_second_third" in PROFIT_ACTIONS

def test_profit_action_protect_runner():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_ACTIONS
    assert "protect_runner" in PROFIT_ACTIONS

def test_profit_action_tighten_trailing_stop():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_ACTIONS
    assert "tighten_trailing_stop" in PROFIT_ACTIONS

def test_profit_action_reduce_on_pressure():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_ACTIONS
    assert "reduce_on_pressure" in PROFIT_ACTIONS

def test_profit_action_observation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_ACTIONS
    assert "observation_only" in PROFIT_ACTIONS

def test_profit_action_block_new_add():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_ACTIONS
    assert "block_new_add" in PROFIT_ACTIONS

def test_profit_action_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_ACTIONS
    assert "human_review_required" in PROFIT_ACTIONS


# =========================================================================
# Section 4: ASSET_TYPES
# =========================================================================
def test_asset_types_count_5():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ASSET_TYPES
    assert len(ASSET_TYPES) == 5

def test_asset_type_stock():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ASSET_TYPES
    assert "stock" in ASSET_TYPES

def test_asset_type_etf():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ASSET_TYPES
    assert "etf" in ASSET_TYPES

def test_asset_type_leveraged_etf():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ASSET_TYPES
    assert "leveraged_etf" in ASSET_TYPES

def test_asset_type_theme_basket():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ASSET_TYPES
    assert "theme_basket" in ASSET_TYPES

def test_asset_type_watchlist_candidate():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ASSET_TYPES
    assert "watchlist_candidate" in ASSET_TYPES


# =========================================================================
# Section 5: REBALANCE_ACTIONS
# =========================================================================
def test_rebalance_actions_count_6():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import REBALANCE_ACTIONS
    assert len(REBALANCE_ACTIONS) == 6

def test_rebalance_action_within_band_hold():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import REBALANCE_ACTIONS
    assert "within_band_hold" in REBALANCE_ACTIONS

def test_rebalance_action_trim_to_target_band():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import REBALANCE_ACTIONS
    assert "trim_to_target_band" in REBALANCE_ACTIONS

def test_rebalance_action_add_back_to_target_band():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import REBALANCE_ACTIONS
    assert "add_back_to_target_band" in REBALANCE_ACTIONS

def test_rebalance_action_reduce_leveraged_exposure():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import REBALANCE_ACTIONS
    assert "reduce_leveraged_exposure" in REBALANCE_ACTIONS

def test_rebalance_action_observation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import REBALANCE_ACTIONS
    assert "observation_only" in REBALANCE_ACTIONS

def test_rebalance_action_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import REBALANCE_ACTIONS
    assert "human_review_required" in REBALANCE_ACTIONS


# =========================================================================
# Section 6: CLI commands
# =========================================================================
def test_cli_commands_count_10():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CLI_COMMANDS_V212
    assert len(CLI_COMMANDS_V212) == 10

def test_cli_cmd_review_profit_taking():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CLI_COMMANDS_V212
    assert "paper-cockpit-v212-review-profit-taking" in CLI_COMMANDS_V212

def test_cli_cmd_evaluate_giveback_risk():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CLI_COMMANDS_V212
    assert "paper-cockpit-v212-evaluate-giveback-risk" in CLI_COMMANDS_V212

def test_cli_cmd_build_profit_warning_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CLI_COMMANDS_V212
    assert "paper-cockpit-v212-build-profit-warning-queue" in CLI_COMMANDS_V212

def test_cli_cmd_build_giveback_review_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CLI_COMMANDS_V212
    assert "paper-cockpit-v212-build-giveback-review-queue" in CLI_COMMANDS_V212

def test_cli_cmd_review_etf_rebalancing():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CLI_COMMANDS_V212
    assert "paper-cockpit-v212-review-etf-rebalancing" in CLI_COMMANDS_V212

def test_cli_cmd_export_json():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CLI_COMMANDS_V212
    assert "paper-cockpit-v212-export-json" in CLI_COMMANDS_V212

def test_cli_cmd_export_md():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CLI_COMMANDS_V212
    assert "paper-cockpit-v212-export-md" in CLI_COMMANDS_V212

def test_cli_cmd_export_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CLI_COMMANDS_V212
    assert "paper-cockpit-v212-export-csv" in CLI_COMMANDS_V212

def test_cli_cmd_health():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CLI_COMMANDS_V212
    assert "paper-cockpit-v212-health" in CLI_COMMANDS_V212

def test_cli_cmd_gate():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CLI_COMMANDS_V212
    assert "paper-cockpit-v212-gate" in CLI_COMMANDS_V212


# =========================================================================
# Section 7: GUI tabs
# =========================================================================
def test_gui_tabs_count_3():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import GUI_TABS_V212
    assert len(GUI_TABS_V212) == 3

def test_gui_tab_profit_taking_v212():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import GUI_TABS_V212
    assert "profit_taking_v212" in GUI_TABS_V212

def test_gui_tab_etf_rebalancing_v212():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import GUI_TABS_V212
    assert "etf_rebalancing_v212" in GUI_TABS_V212

def test_gui_tab_giveback_review_queue_v212():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import GUI_TABS_V212
    assert "giveback_review_queue_v212" in GUI_TABS_V212


# =========================================================================
# Section 8: Safety flags
# =========================================================================
def test_safety_flags_count_25():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert len(SAFETY_FLAGS_V212) == 25

def test_safety_flag_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["paper_only"] is True

def test_safety_flag_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["no_broker"] is True

def test_safety_flag_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["no_real_orders"] is True

def test_safety_flag_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["should_auto_apply_always_false"] is True

def test_safety_flag_auto_apply_enabled_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["auto_apply_enabled_always_false"] is True

def test_safety_flag_profit_taking_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["profit_taking_recommendation_only"] is True

def test_safety_flag_etf_rebalance_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["etf_rebalance_recommendation_only"] is True

def test_safety_flag_no_automatic_profit_taking_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["no_automatic_profit_taking_action"] is True

def test_safety_flag_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["no_automatic_rebalance"] is True

def test_safety_flag_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["broker_execution_disabled"] is True

def test_safety_flag_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["production_trading_blocked"] is True

def test_safety_flag_require_profit_plan_before_entry_always_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["require_profit_plan_before_entry_always_true"] is True

def test_safety_flag_profit_actions_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["profit_actions_recommendation_only"] is True

def test_safety_flag_etf_rebalance_actions_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212["etf_rebalance_actions_recommendation_only"] is True


# =========================================================================
# Section 9: Field list checks
# =========================================================================
def test_profit_review_fields_count_11():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_REVIEW_FIELDS
    assert len(PROFIT_REVIEW_FIELDS) == 11

def test_profit_taking_policy_fields_count_12():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_TAKING_POLICY_FIELDS
    assert len(PROFIT_TAKING_POLICY_FIELDS) == 12

def test_candidate_profit_plan_fields_count_26():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CANDIDATE_PROFIT_PLAN_FIELDS
    assert len(CANDIDATE_PROFIT_PLAN_FIELDS) == 26

def test_etf_rebalancing_item_fields_count_15():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ETF_REBALANCING_ITEM_FIELDS
    assert len(ETF_REBALANCING_ITEM_FIELDS) == 15

def test_profit_taking_summary_fields_count_15():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_TAKING_SUMMARY_FIELDS
    assert len(PROFIT_TAKING_SUMMARY_FIELDS) == 15

def test_profit_review_fields_has_profit_review_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_REVIEW_FIELDS
    assert "profit_review_id" in PROFIT_REVIEW_FIELDS

def test_profit_review_fields_has_paper_only_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_REVIEW_FIELDS
    assert "paper_only_safety_snapshot" in PROFIT_REVIEW_FIELDS

def test_candidate_plan_fields_has_should_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CANDIDATE_PROFIT_PLAN_FIELDS
    assert "should_auto_apply" in CANDIDATE_PROFIT_PLAN_FIELDS

def test_etf_item_fields_has_should_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ETF_REBALANCING_ITEM_FIELDS
    assert "should_auto_apply" in ETF_REBALANCING_ITEM_FIELDS

def test_policy_fields_has_auto_apply_enabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import PROFIT_TAKING_POLICY_FIELDS
    assert "auto_apply_enabled" in PROFIT_TAKING_POLICY_FIELDS


# =========================================================================
# Section 10: ProfitTakingPolicy schema
# =========================================================================
def test_profit_taking_policy_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingPolicy
    p = ProfitTakingPolicy()
    assert p is not None

def test_profit_taking_policy_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingPolicy
    p = ProfitTakingPolicy()
    assert p.schema_version == "212"

def test_profit_taking_policy_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingPolicy
    p = ProfitTakingPolicy()
    assert p.paper_only is True

def test_profit_taking_policy_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingPolicy
    p = ProfitTakingPolicy()
    assert p.no_real_orders is True

def test_profit_taking_policy_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingPolicy
    p = ProfitTakingPolicy(auto_apply_enabled=True)
    assert p.auto_apply_enabled is False

def test_profit_taking_policy_require_profit_plan_always_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingPolicy
    p = ProfitTakingPolicy(require_profit_plan_before_entry=False)
    assert p.require_profit_plan_before_entry is True

def test_profit_taking_policy_first_take_profit_pct_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingPolicy
    p = ProfitTakingPolicy()
    assert p.first_take_profit_pct == 0.20

def test_profit_taking_policy_second_take_profit_pct_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingPolicy
    p = ProfitTakingPolicy()
    assert p.second_take_profit_pct == 0.40

def test_profit_taking_policy_trailing_stop_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingPolicy
    p = ProfitTakingPolicy()
    assert p.trailing_stop_from_high_pct == 0.12

def test_profit_taking_policy_max_giveback_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingPolicy
    p = ProfitTakingPolicy()
    assert p.max_profit_giveback_pct == 0.15


# =========================================================================
# Section 11: CandidateProfitPlan schema
# =========================================================================
def test_candidate_profit_plan_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CandidateProfitPlan
    p = CandidateProfitPlan()
    assert p is not None

def test_candidate_profit_plan_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CandidateProfitPlan
    p = CandidateProfitPlan()
    assert p.schema_version == "212"

def test_candidate_profit_plan_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CandidateProfitPlan
    p = CandidateProfitPlan()
    assert p.paper_only is True

def test_candidate_profit_plan_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CandidateProfitPlan
    p = CandidateProfitPlan()
    assert p.no_real_orders is True

def test_candidate_profit_plan_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CandidateProfitPlan
    p = CandidateProfitPlan(should_auto_apply=True)
    assert p.should_auto_apply is False

def test_candidate_profit_plan_default_asset_type():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CandidateProfitPlan
    p = CandidateProfitPlan()
    assert p.asset_type == "stock"

def test_candidate_profit_plan_default_profit_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import CandidateProfitPlan
    p = CandidateProfitPlan()
    assert p.profit_action == "hold_with_plan"


# =========================================================================
# Section 12: ETFRebalancingItem schema
# =========================================================================
def test_etf_rebalancing_item_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ETFRebalancingItem
    e = ETFRebalancingItem()
    assert e is not None

def test_etf_rebalancing_item_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ETFRebalancingItem
    e = ETFRebalancingItem()
    assert e.schema_version == "212"

def test_etf_rebalancing_item_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ETFRebalancingItem
    e = ETFRebalancingItem()
    assert e.paper_only is True

def test_etf_rebalancing_item_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ETFRebalancingItem
    e = ETFRebalancingItem(should_auto_apply=True)
    assert e.should_auto_apply is False

def test_etf_rebalancing_item_default_rebalance_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ETFRebalancingItem
    e = ETFRebalancingItem()
    assert e.rebalance_action == "within_band_hold"


# =========================================================================
# Section 13: ProfitReviewResult safety
# =========================================================================
def test_profit_review_result_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitReviewResult
    r = ProfitReviewResult()
    assert r is not None

def test_profit_review_result_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitReviewResult
    r = ProfitReviewResult(should_auto_apply=True)
    assert r.should_auto_apply is False

def test_profit_review_result_auto_apply_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitReviewResult
    r = ProfitReviewResult(auto_apply_enabled=True)
    assert r.auto_apply_enabled is False

def test_profit_review_result_paper_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitReviewResult
    r = ProfitReviewResult()
    assert r.paper_only is True

def test_profit_review_result_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitReviewResult
    r = ProfitReviewResult()
    assert r.no_real_orders is True


# =========================================================================
# Section 14: +20% first take-profit trigger
# =========================================================================
def test_first_take_profit_below_20pct_holds():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-001", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 115.0, first_take_profit_triggered=False)
    assert p.profit_action == "hold_with_plan"

def test_first_take_profit_at_exactly_20pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-002", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 120.0, first_take_profit_triggered=False)
    assert p.profit_action == "take_first_third"

def test_first_take_profit_above_20pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-003", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 135.0, first_take_profit_triggered=False)
    assert p.profit_action == "take_first_third"

def test_first_take_profit_price_calculation():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-004", "TEST", "Test", "C", "T", "S",
                                    "stock", 500.0, 500.0)
    assert abs(p.first_take_profit_price - 600.0) < 0.01

def test_first_take_profit_not_retrigger_when_done():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-005", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 130.0, first_take_profit_triggered=True,
                                    second_take_profit_triggered=False)
    assert p.profit_action != "take_first_third"

def test_missing_profit_plan_blocks():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-006", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 125.0, has_profit_plan=False)
    assert p.profit_action == "block_new_add"
    assert p.blocked_by_missing_profit_plan is True

def test_unrealized_return_pct_calculated():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-007", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 125.0)
    assert abs(p.unrealized_return_pct - 0.25) < 0.001


# =========================================================================
# Section 15: +40% second take-profit trigger
# =========================================================================
def test_second_take_profit_at_40pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-010", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 145.0,
                                    first_take_profit_triggered=True,
                                    second_take_profit_triggered=False)
    assert p.profit_action == "take_second_third"

def test_second_take_profit_price_calculation():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-011", "TEST", "Test", "C", "T", "S",
                                    "stock", 500.0, 500.0)
    assert abs(p.second_take_profit_price - 700.0) < 0.01

def test_second_take_profit_requires_first_triggered():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-012", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 145.0,
                                    first_take_profit_triggered=False,
                                    second_take_profit_triggered=False)
    # Should trigger first, not second
    assert p.profit_action == "take_first_third"

def test_runner_active_when_both_triggered():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-013", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 160.0,
                                    high_watermark_price=165.0,
                                    first_take_profit_triggered=True,
                                    second_take_profit_triggered=True)
    assert p.runner_active is True


# =========================================================================
# Section 16: Trailing stop runner
# =========================================================================
def test_runner_protect_when_above_trailing_stop():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-020", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 165.0,
                                    high_watermark_price=170.0,
                                    first_take_profit_triggered=True,
                                    second_take_profit_triggered=True)
    # trailing_stop = 170 * 0.88 = 149.6, current=165 > 149.6
    assert p.profit_action == "protect_runner"

def test_runner_tighten_trailing_stop_when_below():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-021", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 148.0,
                                    high_watermark_price=180.0,
                                    first_take_profit_triggered=True,
                                    second_take_profit_triggered=True)
    # trailing_stop = 180 * 0.88 = 158.4, current=148 < 158.4
    assert p.profit_action == "tighten_trailing_stop"

def test_trailing_stop_price_calculation():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-022", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 180.0,
                                    high_watermark_price=200.0)
    assert abs(p.trailing_stop_price - 176.0) < 0.1  # 200 * 0.88 = 176

def test_runner_blowoff_reduces():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-023", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 180.0,
                                    high_watermark_price=185.0,
                                    first_take_profit_triggered=True,
                                    second_take_profit_triggered=True,
                                    has_blowoff_signal=True)
    assert p.profit_action == "reduce_on_pressure"

def test_runner_pressure_signal_reduces():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-024", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 180.0,
                                    high_watermark_price=185.0,
                                    first_take_profit_triggered=True,
                                    second_take_profit_triggered=True,
                                    has_pressure_signal=True)
    assert p.profit_action == "reduce_on_pressure"


# =========================================================================
# Section 17: High-watermark giveback detection
# =========================================================================
def test_giveback_zero_at_high():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-030", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 150.0, high_watermark_price=150.0)
    assert p.giveback_from_high_pct == 0.0

def test_giveback_pct_calculation():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-031", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 120.0, high_watermark_price=150.0)
    assert abs(p.giveback_from_high_pct - 0.2) < 0.001

def test_giveback_exceeds_max_triggers_human_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    # 20% giveback > 15% max
    p = evaluate_profit_taking_plan("PP-032", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 120.0, high_watermark_price=150.0)
    assert p.profit_action == "human_review_required"
    assert p.requires_human_review is True

def test_giveback_below_max_no_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    # 5% giveback < 15% max
    p = evaluate_profit_taking_plan("PP-033", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 142.5, high_watermark_price=150.0)
    assert p.profit_action != "human_review_required"

def test_giveback_from_high_uses_watermark():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-034", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 80.0, high_watermark_price=100.0)
    assert abs(p.giveback_from_high_pct - 0.20) < 0.001


# =========================================================================
# Section 18: Moving-average profit protection & pressure zone
# =========================================================================
def test_pressure_signal_before_first_tp_reduces():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-040", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 112.0,
                                    first_take_profit_triggered=False,
                                    has_pressure_signal=True)
    assert p.profit_action == "reduce_on_pressure"

def test_blowoff_signal_before_first_tp_reduces():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-041", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 112.0,
                                    first_take_profit_triggered=False,
                                    has_blowoff_signal=True)
    assert p.profit_action == "reduce_on_pressure"

def test_no_signal_no_pressure_action():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-042", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 112.0,
                                    first_take_profit_triggered=False,
                                    has_pressure_signal=False, has_blowoff_signal=False)
    assert p.profit_action == "hold_with_plan"


# =========================================================================
# Section 19: ETF target allocation rebalancing
# =========================================================================
def test_etf_within_band_hold():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0050", "台灣50", 0.40, 0.43, 0.50, 0.35, False)
    assert e.rebalance_action == "within_band_hold"

def test_etf_at_exactly_upper_band():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0050", "台灣50", 0.40, 0.50, 0.50, 0.35, False)
    assert e.rebalance_action == "within_band_hold"

def test_etf_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0050", "台灣50", 0.40, 0.43, 0.50, 0.35, False)
    assert e.paper_only is True

def test_etf_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0050", "台灣50", 0.40, 0.43, 0.50, 0.35, False)
    assert e.no_real_orders is True

def test_etf_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0050", "台灣50", 0.40, 0.43, 0.50, 0.35, False)
    assert e.should_auto_apply is False

def test_etf_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0050", "台灣50", 0.40, 0.43, 0.50, 0.35, False)
    assert e.schema_version == "212"


# =========================================================================
# Section 20: ETF overweight trim
# =========================================================================
def test_etf_overweight_trim():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0050", "台灣50", 0.40, 0.55, 0.50, 0.35, False)
    assert e.rebalance_action == "trim_to_target_band"

def test_etf_overweight_trim_recommended_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0050", "台灣50", 0.40, 0.55, 0.50, 0.35, False)
    assert e.recommended_trim_pct > 0

def test_etf_overweight_pct_calculated():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0050", "台灣50", 0.40, 0.56, 0.50, 0.35, False)
    assert abs(e.overweight_pct - 0.06) < 0.001


# =========================================================================
# Section 21: ETF underweight add-back
# =========================================================================
def test_etf_underweight_add_back():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0056", "高股息", 0.20, 0.12, 0.25, 0.15, False)
    assert e.rebalance_action == "add_back_to_target_band"

def test_etf_underweight_add_recommended_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0056", "高股息", 0.20, 0.12, 0.25, 0.15, False)
    assert e.recommended_add_pct > 0

def test_etf_underweight_pct_calculated():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0056", "高股息", 0.20, 0.10, 0.25, 0.15, False)
    assert abs(e.underweight_pct - 0.05) < 0.001


# =========================================================================
# Section 22: Leveraged ETF warning
# =========================================================================
def test_leveraged_etf_overweight_reduces_exposure():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("00631L", "正2", 0.05, 0.12, 0.08, 0.02, True)
    assert e.rebalance_action == "reduce_leveraged_exposure"

def test_leveraged_etf_warning_nonempty():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("00631L", "正2", 0.05, 0.12, 0.08, 0.02, True)
    assert len(e.leveraged_etf_warning) > 0

def test_leveraged_etf_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("00631L", "正2", 0.05, 0.12, 0.08, 0.02, True)
    assert e.no_real_orders is True

def test_non_leveraged_etf_no_warning():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0050", "台灣50", 0.40, 0.43, 0.50, 0.35, False)
    assert e.leveraged_etf_warning == ""


# =========================================================================
# Section 23: Stock vs ETF rule separation
# =========================================================================
def test_etf_asset_type_uses_observation():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-060", "0050", "台灣50", "C", "T", "S",
                                    "etf", 35.0, 45.0, first_take_profit_triggered=False)
    assert p.profit_action == "observation_only"

def test_leveraged_etf_asset_type_uses_observation():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-061", "00631L", "正2", "C", "T", "S",
                                    "leveraged_etf", 10.0, 15.0, first_take_profit_triggered=False)
    assert p.profit_action == "observation_only"

def test_watchlist_candidate_uses_profit_plan():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-062", "TEST", "Test", "C", "T", "S",
                                    "watchlist_candidate", 100.0, 125.0,
                                    first_take_profit_triggered=False)
    assert p.profit_action == "take_first_third"

def test_theme_basket_uses_profit_plan():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-063", "BASKET", "Test", "C", "T", "S",
                                    "theme_basket", 100.0, 125.0,
                                    first_take_profit_triggered=False)
    assert p.profit_action == "take_first_third"


# =========================================================================
# Section 24: Missing profit plan guard
# =========================================================================
def test_missing_profit_plan_blocked_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-070", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 130.0, has_profit_plan=False)
    assert p.blocked_by_missing_profit_plan is True

def test_missing_profit_plan_action_block_new_add():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-071", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 130.0, has_profit_plan=False)
    assert p.profit_action == "block_new_add"

def test_has_profit_plan_not_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-072", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 130.0, has_profit_plan=True)
    assert p.blocked_by_missing_profit_plan is False


# =========================================================================
# Section 25: Giveback review queue
# =========================================================================
def test_build_giveback_review_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import build_giveback_review_queue
    q = build_giveback_review_queue()
    assert isinstance(q, list)

def test_build_giveback_review_queue_items_have_giveback():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import build_giveback_review_queue
    q = build_giveback_review_queue()
    for item in q:
        assert item.giveback_from_high_pct > 0.05

def test_build_giveback_review_queue_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import build_giveback_review_queue
    q = build_giveback_review_queue()
    for item in q:
        assert item.paper_only is True

def test_build_giveback_review_queue_no_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import build_giveback_review_queue
    q = build_giveback_review_queue()
    for item in q:
        assert item.should_auto_apply is False


# =========================================================================
# Section 26: Profit warning queue
# =========================================================================
def test_build_profit_warning_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import build_profit_warning_queue
    q = build_profit_warning_queue()
    assert isinstance(q, list)

def test_build_profit_warning_queue_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import build_profit_warning_queue
    q = build_profit_warning_queue()
    for item in q:
        assert item.paper_only is True

def test_build_profit_warning_queue_no_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import build_profit_warning_queue
    q = build_profit_warning_queue()
    for item in q:
        assert item.should_auto_apply is False


# =========================================================================
# Section 27: Human review escalation
# =========================================================================
def test_human_review_triggered_by_large_giveback():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-080", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 120.0, high_watermark_price=150.0)
    assert p.requires_human_review is True
    assert p.profit_action == "human_review_required"

def test_human_review_not_triggered_small_giveback():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-081", "TEST", "Test", "C", "T", "S",
                                    "stock", 100.0, 145.0, high_watermark_price=150.0)
    assert p.requires_human_review is False


# =========================================================================
# Section 28: run_profit_taking_review engine
# =========================================================================
def test_run_profit_taking_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result is not None

def test_run_profit_taking_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.paper_only is True

def test_run_profit_taking_review_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.all_passed is True

def test_run_profit_taking_review_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.should_auto_apply is False

def test_run_profit_taking_review_auto_apply_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.auto_apply_enabled is False

def test_run_profit_taking_review_policy_not_none():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.profit_policy is not None

def test_run_profit_taking_review_summary_not_none():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.profit_taking_summary is not None

def test_run_profit_taking_review_has_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert isinstance(result.profit_taking_snapshot, list)
    assert len(result.profit_taking_snapshot) > 0

def test_run_profit_taking_review_has_etf_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert isinstance(result.etf_rebalancing_snapshot, list)
    assert len(result.etf_rebalancing_snapshot) > 0

def test_run_profit_taking_review_paper_only_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.paper_only_safety_snapshot is True

def test_run_profit_taking_review_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.profit_version == "2.0.12"

def test_run_profit_taking_review_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.no_real_orders is True


# =========================================================================
# Section 29: v2.0.11 journal integration
# =========================================================================
def test_v211_import_still_works():
    import paper_trading.small_capital_strategy.paper_cockpit_v211

def test_v211_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import VERSION
    assert VERSION == "2.0.11"

def test_v211_run_journal_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert result is not None

def test_v211_run_journal_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import run_journal_review
    result = run_journal_review()
    assert result.paper_only is True


# =========================================================================
# Section 30: v2.0.10 exit plan integration
# =========================================================================
def test_v210_import_still_works():
    import paper_trading.small_capital_strategy.paper_cockpit_v210

def test_v210_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import VERSION
    assert VERSION == "2.0.10"

def test_v210_run_exit_plan_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v210 import run_exit_plan_review
    result = run_exit_plan_review()
    assert result is not None


# =========================================================================
# Section 31: v2.0.9 position sizing integration
# =========================================================================
def test_v209_import_still_works():
    import paper_trading.small_capital_strategy.paper_cockpit_v209

def test_v209_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import VERSION
    assert VERSION == "2.0.9"


# =========================================================================
# Section 32: v2.0.8 exposure integration
# =========================================================================
def test_v208_import_still_works():
    import paper_trading.small_capital_strategy.paper_cockpit_v208

def test_v208_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import VERSION
    assert VERSION == "2.0.8"


# =========================================================================
# Section 33: v2.0.7 market regime integration
# =========================================================================
def test_v207_import_still_works():
    import paper_trading.small_capital_strategy.paper_cockpit_v207

def test_v207_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import VERSION
    assert VERSION == "2.0.7"


# =========================================================================
# Section 34: v2.0.6 lifecycle integration
# =========================================================================
def test_v206_import_still_works():
    import paper_trading.small_capital_strategy.paper_cockpit_v206

def test_v206_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import VERSION
    assert VERSION == "2.0.6"


# =========================================================================
# Section 35: v2.0.5 watchlist rotation integration
# =========================================================================
def test_v205_import_still_works():
    import paper_trading.small_capital_strategy.paper_cockpit_v205

def test_v205_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import VERSION
    assert VERSION == "2.0.5"


# =========================================================================
# Section 36: Export JSON / Markdown / CSV schema completeness
# =========================================================================
def test_export_profit_taking_json_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_json
    result = run_profit_taking_review()
    ex = export_profit_taking_json(result)
    assert ex is not None

def test_export_profit_taking_json_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_json
    result = run_profit_taking_review()
    ex = export_profit_taking_json(result)
    assert ex.is_valid is True

def test_export_profit_taking_json_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_json
    result = run_profit_taking_review()
    ex = export_profit_taking_json(result)
    assert ex.paper_only is True

def test_export_profit_taking_json_export_status():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_json
    result = run_profit_taking_review()
    ex = export_profit_taking_json(result)
    assert ex.export_status == "complete"

def test_export_profit_taking_json_content_nonempty():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_json
    result = run_profit_taking_review()
    ex = export_profit_taking_json(result)
    assert len(ex.content) > 0

def test_export_profit_taking_markdown_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_markdown
    result = run_profit_taking_review()
    ex = export_profit_taking_markdown(result)
    assert ex is not None

def test_export_profit_taking_markdown_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_markdown
    result = run_profit_taking_review()
    ex = export_profit_taking_markdown(result)
    assert ex.is_valid is True

def test_export_candidate_profit_plan_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_candidate_profit_plan_csv
    result = run_profit_taking_review()
    ex = export_candidate_profit_plan_csv(result)
    assert ex is not None

def test_export_candidate_profit_plan_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_candidate_profit_plan_csv
    result = run_profit_taking_review()
    ex = export_candidate_profit_plan_csv(result)
    assert ex.is_valid is True

def test_export_etf_rebalancing_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_etf_rebalancing_csv
    result = run_profit_taking_review()
    ex = export_etf_rebalancing_csv(result)
    assert ex is not None

def test_export_etf_rebalancing_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_etf_rebalancing_csv
    result = run_profit_taking_review()
    ex = export_etf_rebalancing_csv(result)
    assert ex.is_valid is True

def test_export_profit_warning_queue_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_warning_queue_csv
    result = run_profit_taking_review()
    ex = export_profit_warning_queue_csv(result)
    assert ex is not None

def test_export_profit_warning_queue_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_warning_queue_csv
    result = run_profit_taking_review()
    ex = export_profit_warning_queue_csv(result)
    assert ex.is_valid is True

def test_export_giveback_review_queue_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_giveback_review_queue_csv
    result = run_profit_taking_review()
    ex = export_giveback_review_queue_csv(result)
    assert ex is not None

def test_export_giveback_review_queue_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_giveback_review_queue_csv
    result = run_profit_taking_review()
    ex = export_giveback_review_queue_csv(result)
    assert ex.is_valid is True

def test_export_audit_snapshot_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_audit_snapshot
    result = run_profit_taking_review()
    ex = export_profit_taking_audit_snapshot(result)
    assert ex is not None

def test_export_audit_snapshot_complete():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_audit_snapshot
    result = run_profit_taking_review()
    ex = export_profit_taking_audit_snapshot(result)
    assert ex.export_status == "complete"

def test_export_audit_snapshot_hash_nonempty():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_audit_snapshot
    result = run_profit_taking_review()
    ex = export_profit_taking_audit_snapshot(result)
    assert len(ex.reproducibility_hash) > 0


# =========================================================================
# Section 37: CLI output (handler resolution)
# =========================================================================
def test_cli_handler_review_profit_taking_exists():
    import main as m
    assert hasattr(m, "cmd_paper_cockpit_v212_review_profit_taking")
    assert callable(m.cmd_paper_cockpit_v212_review_profit_taking)

def test_cli_handler_evaluate_giveback_risk_exists():
    import main as m
    assert hasattr(m, "cmd_paper_cockpit_v212_evaluate_giveback_risk")
    assert callable(m.cmd_paper_cockpit_v212_evaluate_giveback_risk)

def test_cli_handler_build_profit_warning_queue_exists():
    import main as m
    assert hasattr(m, "cmd_paper_cockpit_v212_build_profit_warning_queue")
    assert callable(m.cmd_paper_cockpit_v212_build_profit_warning_queue)

def test_cli_handler_build_giveback_review_queue_exists():
    import main as m
    assert hasattr(m, "cmd_paper_cockpit_v212_build_giveback_review_queue")
    assert callable(m.cmd_paper_cockpit_v212_build_giveback_review_queue)

def test_cli_handler_review_etf_rebalancing_exists():
    import main as m
    assert hasattr(m, "cmd_paper_cockpit_v212_review_etf_rebalancing")
    assert callable(m.cmd_paper_cockpit_v212_review_etf_rebalancing)

def test_cli_handler_export_json_exists():
    import main as m
    assert hasattr(m, "cmd_paper_cockpit_v212_export_json")
    assert callable(m.cmd_paper_cockpit_v212_export_json)

def test_cli_handler_export_md_exists():
    import main as m
    assert hasattr(m, "cmd_paper_cockpit_v212_export_md")
    assert callable(m.cmd_paper_cockpit_v212_export_md)

def test_cli_handler_export_csv_exists():
    import main as m
    assert hasattr(m, "cmd_paper_cockpit_v212_export_csv")
    assert callable(m.cmd_paper_cockpit_v212_export_csv)

def test_cli_handler_health_exists():
    import main as m
    assert hasattr(m, "cmd_paper_cockpit_v212_health")
    assert callable(m.cmd_paper_cockpit_v212_health)

def test_cli_handler_gate_exists():
    import main as m
    assert hasattr(m, "cmd_paper_cockpit_v212_gate")
    assert callable(m.cmd_paper_cockpit_v212_gate)


# =========================================================================
# Section 38: CLI registration health
# =========================================================================
def test_cli_registry_review_profit_taking():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v212-review-profit-taking" in names

def test_cli_registry_evaluate_giveback_risk():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v212-evaluate-giveback-risk" in names

def test_cli_registry_build_profit_warning_queue():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v212-build-profit-warning-queue" in names

def test_cli_registry_build_giveback_review_queue():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v212-build-giveback-review-queue" in names

def test_cli_registry_review_etf_rebalancing():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v212-review-etf-rebalancing" in names

def test_cli_registry_export_json():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v212-export-json" in names

def test_cli_registry_export_md():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v212-export-md" in names

def test_cli_registry_export_csv():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v212-export-csv" in names

def test_cli_registry_health():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v212-health" in names

def test_cli_registry_gate():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v212-gate" in names


# =========================================================================
# Section 39: Replay lineage handler integrity
# =========================================================================
def test_no_isolated_v212_command_map():
    import main as m
    assert not hasattr(m, "_ISOLATED_V212_COMMAND_MAP")

def test_v211_handlers_still_exist():
    import main as m
    assert hasattr(m, "cmd_paper_cockpit_v211_review_journal")
    assert callable(m.cmd_paper_cockpit_v211_review_journal)

def test_v210_handlers_still_exist():
    import main as m
    assert hasattr(m, "cmd_paper_cockpit_v210_review_exit_plan")
    assert callable(m.cmd_paper_cockpit_v210_review_exit_plan)


# =========================================================================
# Section 40: GUI compatibility
# =========================================================================
def test_gui_panel_version_v212():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V212
    assert PANEL_VERSION_V212 == "2.0.12"

def test_gui_v212_tab_names_count():
    from gui.small_capital_strategy_panel import get_v212_tab_names
    assert len(get_v212_tab_names()) == 3

def test_gui_profit_taking_v212_in_tabs():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "profit_taking_v212" in get_tab_names()

def test_gui_etf_rebalancing_v212_in_tabs():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "etf_rebalancing_v212" in get_tab_names()

def test_gui_giveback_review_queue_v212_in_tabs():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "giveback_review_queue_v212" in get_tab_names()


# =========================================================================
# Section 41: render_all_tabs no error tabs
# =========================================================================
def test_render_profit_taking_v212_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("profit_taking_v212", {})

def test_render_etf_rebalancing_v212_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("etf_rebalancing_v212", {})

def test_render_giveback_review_queue_v212_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("giveback_review_queue_v212", {})

def test_render_all_tabs_no_global_errors():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    error_tabs = [k for k, v in result.items() if "error" in v]
    assert len(error_tabs) == 0

def test_render_v211_tabs_still_work():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("trade_journal_v211", {})


# =========================================================================
# Section 42: Paper-only safety
# =========================================================================
def test_profit_safety_guard_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitSafetyGuard
    g = ProfitSafetyGuard()
    assert g.no_real_orders is True

def test_profit_safety_guard_no_auto_profit_taking():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitSafetyGuard
    g = ProfitSafetyGuard()
    assert g.no_automatic_profit_taking_action is True

def test_profit_safety_guard_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitSafetyGuard
    g = ProfitSafetyGuard()
    assert g.should_auto_apply is False

def test_profit_safety_guard_profit_actions_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitSafetyGuard
    g = ProfitSafetyGuard()
    assert g.profit_actions_recommendation_only is True

def test_profit_safety_guard_require_profit_plan():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitSafetyGuard
    g = ProfitSafetyGuard()
    assert g.require_profit_plan_before_entry is True

def test_no_broker_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import SAFETY_FLAGS_V212
    assert SAFETY_FLAGS_V212.get("no_broker") is True


# =========================================================================
# Section 43: Backward compatibility v2.0.11
# =========================================================================
def test_v211_schema_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "211"

def test_v211_safety_flags_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import SAFETY_FLAGS_V211
    assert len(SAFETY_FLAGS_V211) == 24

def test_v211_cli_commands_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import CLI_COMMANDS_V211
    assert len(CLI_COMMANDS_V211) == 10

def test_v211_gui_tabs_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v211 import GUI_TABS_V211
    assert len(GUI_TABS_V211) == 3


# =========================================================================
# Section 44: v201 health relative-path compatibility
# =========================================================================
def test_v201_health_relative_path():
    import os
    health_dir = os.path.join(
        os.path.dirname(__file__), "..", "paper_trading", "small_capital_strategy"
    )
    test_path = os.path.normpath(os.path.join(health_dir, "..", "..", "tests", "test_paper_cockpit_v201.py"))
    assert os.path.exists(test_path)


# =========================================================================
# Section 45: Health check
# =========================================================================
def test_health_check_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v212 import run_health_check
    result = run_health_check()
    assert result is not None

def test_health_check_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v212 import run_health_check
    result = run_health_check()
    assert result["all_passed"] is True, f"Health check failures: {result.get('errors', [])}"

def test_health_check_version():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v212 import HEALTH_VERSION
    assert HEALTH_VERSION == "2.0.12"


# =========================================================================
# Section 46: Release gate
# =========================================================================
def test_release_gate_callable():
    from release.paper_cockpit_release_gate_v212 import run_release_gate
    result = run_release_gate()
    assert result is not None

def test_release_gate_passed():
    from release.paper_cockpit_release_gate_v212 import run_release_gate
    result = run_release_gate()
    assert result["gate_passed"] is True, f"Gate failures: {result.get('errors', [])}"

def test_release_gate_version():
    from release.paper_cockpit_release_gate_v212 import GATE_VERSION
    assert GATE_VERSION == "2.0.12"


# =========================================================================
# Section 47: Scenarios and fixtures
# =========================================================================
def test_scenarios_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v212 import SCENARIOS
    assert len(SCENARIOS) == 80

def test_scenarios_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v212 import SCENARIOS
    assert all(s["schema_version"] == "212" for s in SCENARIOS)

def test_scenarios_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v212 import SCENARIOS
    assert all(s["paper_only"] is True for s in SCENARIOS)

def test_scenarios_no_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v212 import SCENARIOS
    assert all(s["should_auto_apply"] is False for s in SCENARIOS)

def test_fixtures_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v212 import FIXTURES
    assert len(FIXTURES) == 80

def test_fixtures_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v212 import FIXTURES
    assert all(f["schema_version"] == "212" for f in FIXTURES)

def test_fixtures_have_fixture_id():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v212 import FIXTURES
    assert all("fixture_id" in f for f in FIXTURES)

def test_fixtures_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v212 import FIXTURES
    assert all(f["paper_only"] is True for f in FIXTURES)


# =========================================================================
# Section 48: Model count
# =========================================================================
def test_model_count_16():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import _ALL_MODEL_NAMES_V212
    assert len(_ALL_MODEL_NAMES_V212) == 16

def test_all_model_names_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import _ALL_MODEL_NAMES_V212
    assert "ProfitTakingPolicy" in _ALL_MODEL_NAMES_V212
    assert "CandidateProfitPlan" in _ALL_MODEL_NAMES_V212
    assert "ETFRebalancingItem" in _ALL_MODEL_NAMES_V212
    assert "ProfitTakingSummary" in _ALL_MODEL_NAMES_V212
    assert "ProfitReviewResult" in _ALL_MODEL_NAMES_V212
    assert "ProfitSafetyGuard" in _ALL_MODEL_NAMES_V212

def test_profit_summary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingSummary
    s = ProfitTakingSummary()
    assert s.paper_only is True

def test_profit_review_input_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitReviewInput
    r = ProfitReviewInput()
    assert r.paper_only is True

def test_profit_audit_snapshot_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingAuditSnapshot
    a = ProfitTakingAuditSnapshot()
    assert a.paper_only is True

def test_profit_markdown_report_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitTakingMarkdownReport
    r = ProfitTakingMarkdownReport()
    assert r.paper_only is True

def test_etf_rebalancing_csv_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ETFRebalancingCSV
    c = ETFRebalancingCSV()
    assert c.paper_only is True

def test_giveback_review_queue_csv_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import GivebackReviewQueueCSV
    c = GivebackReviewQueueCSV()
    assert c.paper_only is True

def test_v212_health_summary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import V212HealthSummary
    h = V212HealthSummary()
    assert h.version == "2.0.12"

def test_v212_release_summary_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import V212ReleaseSummary
    r = V212ReleaseSummary()
    assert r.version == "2.0.12"


# =========================================================================
# Section 49: get_cockpit_summary_v212
# =========================================================================
def test_get_cockpit_summary_v212_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import get_cockpit_summary_v212
    s = get_cockpit_summary_v212()
    assert isinstance(s, dict)

def test_get_cockpit_summary_v212_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import get_cockpit_summary_v212
    s = get_cockpit_summary_v212()
    assert s["paper_only"] is True

def test_get_cockpit_summary_v212_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import get_cockpit_summary_v212
    s = get_cockpit_summary_v212()
    assert s["version"] == "2.0.12"

def test_get_cockpit_summary_v212_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import get_cockpit_summary_v212
    s = get_cockpit_summary_v212()
    assert s["should_auto_apply"] is False

def test_get_cockpit_summary_v212_profit_actions_recommendation():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import get_cockpit_summary_v212
    s = get_cockpit_summary_v212()
    assert s["profit_actions_recommendation_only"] is True


# =========================================================================
# Section 50: Additional safety invariants
# =========================================================================
def test_evaluate_profit_plan_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-100", "TEST", "T", "C", "T", "S",
                                    "stock", 100.0, 100.0)
    assert p.no_real_orders is True

def test_evaluate_etf_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0050", "台灣50", 0.40, 0.40, 0.50, 0.35, False)
    assert e.no_real_orders is True

def test_run_etf_rebalancing_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_etf_rebalancing_review
    items = run_etf_rebalancing_review()
    assert isinstance(items, list)

def test_run_etf_rebalancing_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_etf_rebalancing_review
    items = run_etf_rebalancing_review()
    for item in items:
        assert item.paper_only is True

def test_evaluate_giveback_risk_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_giveback_risk
    r = evaluate_giveback_risk()
    assert isinstance(r, dict)

def test_evaluate_giveback_risk_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_giveback_risk
    r = evaluate_giveback_risk()
    assert r["paper_only"] is True

def test_evaluate_giveback_risk_no_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_giveback_risk
    r = evaluate_giveback_risk()
    assert r["should_auto_apply"] is False

def test_detect_giveback_risk_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import detect_giveback_risk
    items = detect_giveback_risk()
    assert isinstance(items, list)

def test_detect_giveback_risk_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import detect_giveback_risk
    items = detect_giveback_risk()
    for item in items:
        assert item.paper_only is True


# =========================================================================
# Section 51: ProfitTakingSummary field coverage
# =========================================================================
def test_profit_taking_summary_total_position_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.profit_taking_summary.total_position_count >= 0

def test_profit_taking_summary_stock_plan_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.profit_taking_summary.stock_profit_plan_count >= 0

def test_profit_taking_summary_etf_rebalance_plan_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.profit_taking_summary.etf_rebalance_plan_count >= 0

def test_profit_taking_summary_quality_grade_set():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.profit_taking_summary.profit_taking_quality_grade in ("A", "B", "C", "D", "F")

def test_profit_taking_summary_rebalancing_quality_grade_set():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.profit_taking_summary.rebalancing_quality_grade in ("A", "B", "C", "D", "F")

def test_profit_taking_summary_top_profit_symbols_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert isinstance(result.profit_taking_summary.top_unrealized_profit_symbols, list)

def test_profit_taking_summary_top_giveback_symbols_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert isinstance(result.profit_taking_summary.top_giveback_risk_symbols, list)

def test_profit_taking_summary_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert result.profit_taking_summary.paper_only is True


# =========================================================================
# Section 52: run_profit_taking_review snapshot lists
# =========================================================================
def test_run_review_one_third_snapshot_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert isinstance(result.one_third_profit_plan_snapshot, list)

def test_run_review_trailing_snapshot_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert isinstance(result.trailing_profit_snapshot, list)

def test_run_review_giveback_snapshot_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert isinstance(result.profit_giveback_snapshot, list)

def test_run_review_warning_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert isinstance(result.profit_warning_queue, list)

def test_run_review_human_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert isinstance(result.human_review_queue, list)

def test_run_review_giveback_queue_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert isinstance(result.giveback_review_queue, list)

def test_run_review_has_review_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert len(result.profit_review_id) > 0

def test_run_review_has_review_period():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review
    result = run_profit_taking_review()
    assert len(result.review_period) > 0


# =========================================================================
# Section 53: Export JSON content parsing
# =========================================================================
def test_export_json_content_parseable():
    import json
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_json
    result = run_profit_taking_review()
    ex = export_profit_taking_json(result)
    parsed = json.loads(ex.content)
    assert isinstance(parsed, dict)

def test_export_json_content_paper_only_field():
    import json
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_json
    result = run_profit_taking_review()
    ex = export_profit_taking_json(result)
    parsed = json.loads(ex.content)
    assert parsed["paper_only"] is True

def test_export_json_content_should_auto_apply_false():
    import json
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_json
    result = run_profit_taking_review()
    ex = export_profit_taking_json(result)
    parsed = json.loads(ex.content)
    assert parsed["should_auto_apply"] is False

def test_export_json_content_version_212():
    import json
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_json
    result = run_profit_taking_review()
    ex = export_profit_taking_json(result)
    parsed = json.loads(ex.content)
    assert parsed["version"] == "2.0.12"

def test_export_md_content_has_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import run_profit_taking_review, export_profit_taking_markdown
    result = run_profit_taking_review()
    ex = export_profit_taking_markdown(result)
    assert "Paper Only" in ex.content or "paper_only" in ex.content.lower() or "Paper" in ex.content


# =========================================================================
# Section 54: ETF rebalancing auto-band and edge cases
# =========================================================================
def test_etf_auto_upper_band_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("TEST", "Test ETF", 0.40, 0.40, 0.0, 0.0, False)
    assert e.upper_rebalance_band_pct == 0.50

def test_etf_auto_lower_band_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("TEST", "Test ETF", 0.40, 0.40, 0.0, 0.0, False)
    assert e.lower_rebalance_band_pct == 0.35

def test_etf_trim_pct_exact():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0050", "台灣50", 0.40, 0.55, 0.50, 0.35, False)
    assert abs(e.recommended_trim_pct - 0.15) < 0.001

def test_etf_add_pct_exact():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("0056", "高股息", 0.20, 0.10, 0.25, 0.15, False)
    assert abs(e.recommended_add_pct - 0.10) < 0.001

def test_etf_leveraged_within_band_no_reduce():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_etf_rebalancing
    e = evaluate_etf_rebalancing("00631L", "正2", 0.05, 0.04, 0.08, 0.02, True)
    assert e.rebalance_action != "reduce_leveraged_exposure"

def test_detect_giveback_risk_all_exceed_threshold():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import detect_giveback_risk, ProfitTakingPolicy
    policy = ProfitTakingPolicy(max_profit_giveback_pct=0.15)
    items = detect_giveback_risk(policy=policy)
    for item in items:
        assert item.giveback_from_high_pct > 0.15

def test_evaluate_giveback_risk_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_giveback_risk
    r = evaluate_giveback_risk()
    assert r["schema_version"] == "212"

def test_evaluate_giveback_risk_symbols_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_giveback_risk
    r = evaluate_giveback_risk()
    assert isinstance(r["giveback_symbols"], list)

def test_profit_safety_guard_no_auto_stop_loss():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitSafetyGuard
    g = ProfitSafetyGuard()
    assert g.no_automatic_stop_loss_execution is True

def test_profit_safety_guard_no_auto_take_profit():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitSafetyGuard
    g = ProfitSafetyGuard()
    assert g.no_automatic_take_profit_execution is True

def test_profit_safety_guard_no_auto_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitSafetyGuard
    g = ProfitSafetyGuard()
    assert g.no_automatic_rebalance is True

def test_profit_safety_guard_etf_rebalance_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitSafetyGuard
    g = ProfitSafetyGuard()
    assert g.etf_rebalance_actions_recommendation_only is True

def test_covered_versions_includes_v211():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import COVERED_VERSIONS
    assert "2.0.11" in COVERED_VERSIONS

def test_covered_versions_includes_v210():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import COVERED_VERSIONS
    assert "2.0.10" in COVERED_VERSIONS

def test_unrealized_return_pct_negative_position():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-NEG", "TEST", "T", "C", "T", "S",
                                    "stock", 100.0, 85.0)
    assert p.unrealized_return_pct < 0
    assert p.profit_action == "hold_with_plan"

def test_profit_plan_unrealized_profit_amount():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import evaluate_profit_taking_plan
    p = evaluate_profit_taking_plan("PP-AMT", "TEST", "T", "C", "T", "S",
                                    "stock", 100.0, 120.0, position_size=1000)
    assert abs(p.unrealized_profit_amount - 20000.0) < 0.01

def test_profit_review_result_not_investment_advice():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitReviewResult
    r = ProfitReviewResult()
    assert r.not_investment_advice is True

def test_profit_review_result_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitReviewResult
    r = ProfitReviewResult()
    assert r.human_review_required is True

def test_profit_review_result_research_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitReviewResult
    r = ProfitReviewResult()
    assert r.research_only is True

def test_profit_review_result_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitReviewResult
    r = ProfitReviewResult()
    assert r.no_broker is True

def test_profit_review_result_profit_taking_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v212 import ProfitReviewResult
    r = ProfitReviewResult()
    assert r.profit_taking_recommendation_only is True
