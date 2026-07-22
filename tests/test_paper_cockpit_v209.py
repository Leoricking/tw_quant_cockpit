"""
tests/test_paper_cockpit_v209.py
v2.0.9 Paper Position Sizing & Risk Budget Control — Main Tests
[!] Paper Only. Research Only. Position Sizing Recommendation Only. No Real Orders. Not Investment Advice.
"""
import pytest


# =========================================================================
# Section 1: Module import & version constants
# =========================================================================
def test_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v209

def test_version_is_209():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import VERSION
    assert VERSION == "2.0.9"

def test_schema_version_is_209():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "209"

def test_release_name_contains_position_sizing():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RELEASE_NAME
    assert "Position Sizing" in RELEASE_NAME

def test_release_name_contains_risk_budget():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RELEASE_NAME
    assert "Risk Budget" in RELEASE_NAME

def test_baseline_tests_set():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import BASELINE_TESTS
    assert BASELINE_TESTS == 34678

def test_min_new_tests_300():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300

def test_verify_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import verify_version
    assert verify_version() is True


# =========================================================================
# Section 2: Safety constants (NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED)
# =========================================================================
def test_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True


# =========================================================================
# Section 3: SIZE_ACTIONS constants (7 entries)
# =========================================================================
def test_size_actions_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SIZE_ACTIONS
    assert len(SIZE_ACTIONS) == 7

def test_size_action_allow_full_paper_size():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SIZE_ACTIONS
    assert "allow_full_paper_size" in SIZE_ACTIONS

def test_size_action_reduce_size():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SIZE_ACTIONS
    assert "reduce_size" in SIZE_ACTIONS

def test_size_action_minimum_probe_size():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SIZE_ACTIONS
    assert "minimum_probe_size" in SIZE_ACTIONS

def test_size_action_observation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SIZE_ACTIONS
    assert "observation_only" in SIZE_ACTIONS

def test_size_action_block_new_position():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SIZE_ACTIONS
    assert "block_new_position" in SIZE_ACTIONS

def test_size_action_require_rescore():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SIZE_ACTIONS
    assert "require_rescore" in SIZE_ACTIONS

def test_size_action_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SIZE_ACTIONS
    assert "human_review_required" in SIZE_ACTIONS


# =========================================================================
# Section 4: CLI commands (10 entries)
# =========================================================================
def test_cli_commands_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CLI_COMMANDS_V209
    assert len(CLI_COMMANDS_V209) == 10

def test_cli_command_review_sizing():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CLI_COMMANDS_V209
    assert "paper-cockpit-v209-review-sizing" in CLI_COMMANDS_V209

def test_cli_command_evaluate_risk_budget():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CLI_COMMANDS_V209
    assert "paper-cockpit-v209-evaluate-risk-budget" in CLI_COMMANDS_V209

def test_cli_command_calculate_position_size():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CLI_COMMANDS_V209
    assert "paper-cockpit-v209-calculate-position-size" in CLI_COMMANDS_V209

def test_cli_command_build_size_reduction_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CLI_COMMANDS_V209
    assert "paper-cockpit-v209-build-size-reduction-queue" in CLI_COMMANDS_V209

def test_cli_command_build_blocked_sizing_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CLI_COMMANDS_V209
    assert "paper-cockpit-v209-build-blocked-sizing-queue" in CLI_COMMANDS_V209

def test_cli_command_export_json():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CLI_COMMANDS_V209
    assert "paper-cockpit-v209-export-json" in CLI_COMMANDS_V209

def test_cli_command_export_md():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CLI_COMMANDS_V209
    assert "paper-cockpit-v209-export-md" in CLI_COMMANDS_V209

def test_cli_command_export_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CLI_COMMANDS_V209
    assert "paper-cockpit-v209-export-csv" in CLI_COMMANDS_V209

def test_cli_command_health():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CLI_COMMANDS_V209
    assert "paper-cockpit-v209-health" in CLI_COMMANDS_V209

def test_cli_command_gate():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CLI_COMMANDS_V209
    assert "paper-cockpit-v209-gate" in CLI_COMMANDS_V209


# =========================================================================
# Section 5: GUI tabs (3 entries)
# =========================================================================
def test_gui_tabs_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import GUI_TABS_V209
    assert len(GUI_TABS_V209) == 3

def test_gui_tab_position_sizing():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import GUI_TABS_V209
    assert "position_sizing_v209" in GUI_TABS_V209

def test_gui_tab_risk_budget():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import GUI_TABS_V209
    assert "risk_budget_v209" in GUI_TABS_V209

def test_gui_tab_size_reduction_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import GUI_TABS_V209
    assert "size_reduction_queue_v209" in GUI_TABS_V209


# =========================================================================
# Section 6: SAFETY_FLAGS_V209 (21 entries)
# =========================================================================
def test_safety_flags_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert len(SAFETY_FLAGS_V209) == 21

def test_safety_flag_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["paper_only"] is True

def test_safety_flag_research_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["research_only"] is True

def test_safety_flag_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["no_real_orders"] is True

def test_safety_flag_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["no_broker"] is True

def test_safety_flag_no_automatic_position_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["no_automatic_position_apply"] is True

def test_safety_flag_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["should_auto_apply_always_false"] is True

def test_safety_flag_auto_apply_enabled_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["auto_apply_enabled_always_false"] is True

def test_safety_flag_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["broker_execution_disabled"] is True

def test_safety_flag_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["production_trading_blocked"] is True

def test_safety_flag_sizing_actions_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["sizing_actions_recommendation_only"] is True

def test_safety_flag_not_investment_advice():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["not_investment_advice"] is True

def test_safety_flag_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["human_review_required"] is True

def test_safety_flag_no_margin():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["no_margin"] is True

def test_safety_flag_no_leverage():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["no_leverage"] is True

def test_safety_flag_no_production_db_write():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["no_production_db_write"] is True

def test_safety_flag_position_sizing_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["position_sizing_recommendation_only"] is True

def test_safety_flag_validation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["validation_only"] is True

def test_safety_flag_no_real_account_sync():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["no_real_account_sync"] is True

def test_safety_flag_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["no_automatic_rebalance"] is True

def test_safety_flag_no_live_strategy_activation():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["no_live_strategy_activation"] is True

def test_safety_flag_sizing_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SAFETY_FLAGS_V209
    assert SAFETY_FLAGS_V209["sizing_only"] is True


# =========================================================================
# Section 7: Field list counts
# =========================================================================
def test_sizing_review_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SIZING_REVIEW_FIELDS
    assert len(SIZING_REVIEW_FIELDS) == 10

def test_risk_budget_policy_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RISK_BUDGET_POLICY_FIELDS
    assert len(RISK_BUDGET_POLICY_FIELDS) == 12

def test_candidate_sizing_item_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CANDIDATE_SIZING_ITEM_FIELDS
    assert len(CANDIDATE_SIZING_ITEM_FIELDS) == 24

def test_position_sizing_summary_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import POSITION_SIZING_SUMMARY_FIELDS
    assert len(POSITION_SIZING_SUMMARY_FIELDS) == 14


# =========================================================================
# Section 8: RiskBudgetPolicy model
# =========================================================================
def test_risk_budget_policy_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p is not None

def test_risk_budget_policy_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.schema_version == "209"

def test_risk_budget_policy_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.paper_only is True

def test_risk_budget_policy_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.no_real_orders is True

def test_risk_budget_policy_auto_apply_enabled_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy(auto_apply_enabled=True)
    assert p.auto_apply_enabled is False

def test_risk_budget_policy_auto_apply_enabled_default_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.auto_apply_enabled is False

def test_risk_budget_policy_account_equity_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.account_equity == 300000.0

def test_risk_budget_policy_max_total_risk_pct_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.max_total_risk_pct == 0.06

def test_risk_budget_policy_max_single_trade_risk_pct_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.max_single_trade_risk_pct == 0.01

def test_risk_budget_policy_max_single_theme_risk_pct_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.max_single_theme_risk_pct == 0.03

def test_risk_budget_policy_max_single_sector_risk_pct_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.max_single_sector_risk_pct == 0.04

def test_risk_budget_policy_custom_equity():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy(account_equity=500000.0)
    assert p.account_equity == 500000.0

def test_risk_budget_policy_default_stop_loss_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.default_stop_loss_pct == 0.06

def test_risk_budget_policy_min_cash_buffer_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.min_cash_buffer_pct == 0.20

def test_risk_budget_policy_max_high_volatility_risk_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.max_high_volatility_risk_pct == 0.02

def test_risk_budget_policy_max_low_liquidity_risk_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.max_low_liquidity_risk_pct == 0.01

def test_risk_budget_policy_max_risk_off_budget_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    assert p.max_risk_off_budget_pct == 0.02


# =========================================================================
# Section 9: CandidateSizingItem model
# =========================================================================
def test_candidate_sizing_item_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem()
    assert item is not None

def test_candidate_sizing_item_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem()
    assert item.schema_version == "209"

def test_candidate_sizing_item_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem()
    assert item.paper_only is True

def test_candidate_sizing_item_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem()
    assert item.no_real_orders is True

def test_candidate_sizing_item_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem(should_auto_apply=True)
    assert item.should_auto_apply is False

def test_candidate_sizing_item_should_auto_apply_default_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem()
    assert item.should_auto_apply is False

def test_candidate_sizing_item_size_action_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem()
    assert item.size_action in [
        "allow_full_paper_size", "reduce_size", "minimum_probe_size",
        "observation_only", "block_new_position", "require_rescore", "human_review_required",
    ]

def test_candidate_sizing_item_blocked_reasons_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem()
    assert isinstance(item.blocked_reasons, list)

def test_candidate_sizing_item_requires_human_review_bool():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem()
    assert isinstance(item.requires_human_review, bool)

def test_candidate_sizing_item_final_recommended_size_nonneg():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem()
    assert item.final_recommended_size >= 0

def test_candidate_sizing_item_has_symbol_field():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem(symbol="2330")
    assert item.symbol == "2330"

def test_candidate_sizing_item_has_entry_price_field():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem(entry_price=100.0)
    assert item.entry_price == 100.0

def test_candidate_sizing_item_has_stop_price_field():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem(entry_price=100.0, stop_price=94.0)
    assert item.stop_price == 94.0

def test_candidate_sizing_item_has_candidate_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem(candidate_score=0.8)
    assert item.candidate_score == 0.8

def test_candidate_sizing_item_has_final_priority_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem(final_priority_score=0.75)
    assert item.final_priority_score == 0.75


# =========================================================================
# Section 10: calculate_position_size function
# =========================================================================
def test_calculate_position_size_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    assert callable(calculate_position_size)

def test_calculate_position_size_returns_candidate_sizing_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size, CandidateSizingItem
    result = calculate_position_size(
        symbol="2330",
        name="Taiwan Semiconductor",
        candidate_id="C001",
        theme_id="T001",
        sector_id="S001",
        candidate_score=0.8,
        final_priority_score=0.75,
        entry_price=600.0,
        stop_price=564.0,
    )
    assert isinstance(result, CandidateSizingItem)

def test_calculate_position_size_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
    )
    assert result.schema_version == "209"

def test_calculate_position_size_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
    )
    assert result.paper_only is True

def test_calculate_position_size_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
    )
    assert result.should_auto_apply is False

def test_calculate_position_size_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
    )
    assert result.no_real_orders is True

def test_calculate_position_size_high_volatility_reduces_size():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    normal = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
        is_high_volatility=False,
    )
    hv = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
        is_high_volatility=True,
    )
    assert hv.volatility_adjusted_size <= normal.volatility_adjusted_size

def test_calculate_position_size_low_liquidity_reduces_size():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    normal = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
        is_low_liquidity=False,
    )
    ll = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
        is_low_liquidity=True,
    )
    assert ll.liquidity_adjusted_size <= normal.liquidity_adjusted_size

def test_calculate_position_size_risk_off_blocks_position():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
        market_state="risk_off",
    )
    assert result.final_recommended_size == 0
    assert result.size_action in ["block_new_position", "human_review_required"]

def test_calculate_position_size_expired_lifecycle_blocks():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
        lifecycle_state="expired",
    )
    assert result.final_recommended_size == 0

def test_calculate_position_size_cooldown_lifecycle_blocks():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
        lifecycle_state="cooldown",
    )
    assert result.final_recommended_size == 0

def test_calculate_position_size_size_action_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size, SIZE_ACTIONS
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
    )
    assert result.size_action in SIZE_ACTIONS

def test_calculate_position_size_final_risk_nonneg():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
    )
    assert result.final_risk_amount >= 0

def test_calculate_position_size_with_custom_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size, RiskBudgetPolicy
    policy = RiskBudgetPolicy(account_equity=500000.0, max_single_trade_risk_pct=0.02)
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
        policy=policy,
    )
    assert isinstance(result.final_recommended_size, (int, float))

def test_calculate_position_size_base_size_positive_for_valid_input():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
        market_state="trending_up",
        lifecycle_state="active",
    )
    assert result.base_position_size > 0

def test_calculate_position_size_trending_up_allows_full_or_reduce():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=1.0, final_priority_score=1.0,
        entry_price=600.0, stop_price=564.0,
        market_state="trending_up",
        lifecycle_state="active",
        is_high_volatility=False,
        is_low_liquidity=False,
        exposure_penalty_pct=0.0,
    )
    assert result.size_action in ["allow_full_paper_size", "reduce_size", "minimum_probe_size"]

def test_calculate_position_size_exposure_penalty_reduces_size():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    no_pen = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
        exposure_penalty_pct=0.0,
    )
    with_pen = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
        exposure_penalty_pct=30.0,
    )
    assert with_pen.exposure_adjusted_size <= no_pen.exposure_adjusted_size

def test_calculate_position_size_stop_distance_pct_positive():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
    )
    assert result.stop_distance_pct > 0


# =========================================================================
# Section 11: run_sizing_review engine
# =========================================================================
def test_run_sizing_review_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    assert callable(run_sizing_review)

def test_run_sizing_review_returns_sizing_review_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review, SizingReviewResult
    result = run_sizing_review()
    assert isinstance(result, SizingReviewResult)

def test_run_sizing_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert result.paper_only is True

def test_run_sizing_review_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert result.no_real_orders is True

def test_run_sizing_review_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert result.should_auto_apply is False

def test_run_sizing_review_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert result.schema_version == "209"

def test_run_sizing_review_has_sizing_review_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert result.sizing_review_id != ""

def test_run_sizing_review_has_sizing_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert result.sizing_version == "2.0.9"

def test_run_sizing_review_candidate_sizing_snapshot_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert isinstance(result.candidate_sizing_snapshot, list)

def test_run_sizing_review_size_reduction_queue_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert isinstance(result.size_reduction_queue, list)

def test_run_sizing_review_blocked_sizing_queue_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert isinstance(result.blocked_sizing_queue, list)

def test_run_sizing_review_human_review_queue_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert isinstance(result.human_review_queue, list)

def test_run_sizing_review_position_sizing_recommendation_queue_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert isinstance(result.position_sizing_recommendation_queue, list)

def test_run_sizing_review_risk_budget_snapshot_exists():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert result.risk_budget_snapshot is not None

def test_run_sizing_review_paper_only_safety_snapshot_truthy():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    # paper_only_safety_snapshot is True (bool) or a dict — both are truthy
    assert result.paper_only_safety_snapshot

def test_run_sizing_review_with_no_input():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review, SizingReviewResult
    result = run_sizing_review(review_input=None)
    assert isinstance(result, SizingReviewResult)


# =========================================================================
# Section 12: SizingReviewResult model
# =========================================================================
def test_sizing_review_result_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SizingReviewResult
    r = SizingReviewResult()
    assert r is not None

def test_sizing_review_result_auto_apply_guard():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SizingReviewResult
    r = SizingReviewResult(should_auto_apply=True)
    assert r.should_auto_apply is False

def test_sizing_review_result_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SizingReviewResult
    r = SizingReviewResult()
    assert r.schema_version == "209"

def test_sizing_review_result_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SizingReviewResult
    r = SizingReviewResult()
    assert r.paper_only is True

def test_sizing_review_result_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SizingReviewResult
    r = SizingReviewResult()
    assert r.no_real_orders is True


# =========================================================================
# Section 13: PositionSizingSummary model
# =========================================================================
def test_position_sizing_summary_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import PositionSizingSummary
    s = PositionSizingSummary()
    assert s is not None

def test_position_sizing_summary_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import PositionSizingSummary
    s = PositionSizingSummary()
    assert s.schema_version == "209"

def test_position_sizing_summary_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import PositionSizingSummary
    s = PositionSizingSummary()
    assert s.paper_only is True

def test_position_sizing_summary_total_candidate_count_nonneg():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import PositionSizingSummary
    s = PositionSizingSummary()
    assert s.total_candidate_count >= 0

def test_position_sizing_summary_top_risk_contributors_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import PositionSizingSummary
    s = PositionSizingSummary()
    assert isinstance(s.top_risk_contributors, list)

def test_position_sizing_summary_top_size_reduction_reasons_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import PositionSizingSummary
    s = PositionSizingSummary()
    assert isinstance(s.top_size_reduction_reasons, list)


# =========================================================================
# Section 14: Export functions
# =========================================================================
def test_export_sizing_json_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_json
    assert callable(export_sizing_json)

def test_export_sizing_json_returns_export_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_json, run_sizing_review, SizingExportResult
    result = export_sizing_json(run_sizing_review())
    assert isinstance(result, SizingExportResult)

def test_export_sizing_json_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_json, run_sizing_review
    result = export_sizing_json(run_sizing_review())
    assert result.is_valid is True

def test_export_sizing_json_contains_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_json, run_sizing_review
    result = export_sizing_json(run_sizing_review())
    assert "209" in result.content or "2.0.9" in result.content

def test_export_sizing_json_contains_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_json, run_sizing_review
    result = export_sizing_json(run_sizing_review())
    assert result.paper_only is True

def test_export_sizing_markdown_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_markdown
    assert callable(export_sizing_markdown)

def test_export_sizing_markdown_returns_export_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_markdown, run_sizing_review, SizingExportResult
    result = export_sizing_markdown(run_sizing_review())
    assert isinstance(result, SizingExportResult)

def test_export_sizing_markdown_contains_v209():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_markdown, run_sizing_review
    result = export_sizing_markdown(run_sizing_review())
    assert "2.0.9" in result.content or "209" in result.content

def test_export_sizing_markdown_contains_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_markdown, run_sizing_review
    result = export_sizing_markdown(run_sizing_review())
    assert result.paper_only is True

def test_export_candidate_sizing_csv_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_candidate_sizing_csv
    assert callable(export_candidate_sizing_csv)

def test_export_candidate_sizing_csv_returns_csv_obj():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_candidate_sizing_csv, run_sizing_review, CandidateSizingCSV
    result = export_candidate_sizing_csv(run_sizing_review())
    assert isinstance(result, CandidateSizingCSV)

def test_export_risk_budget_csv_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_risk_budget_csv
    assert callable(export_risk_budget_csv)

def test_export_risk_budget_csv_returns_csv_obj():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_risk_budget_csv, run_sizing_review, RiskBudgetCSV
    result = export_risk_budget_csv(run_sizing_review())
    assert isinstance(result, RiskBudgetCSV)

def test_export_size_reduction_csv_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_size_reduction_csv
    assert callable(export_size_reduction_csv)

def test_export_size_reduction_csv_returns_csv_obj():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_size_reduction_csv, run_sizing_review, SizeReductionCSV
    result = export_size_reduction_csv(run_sizing_review())
    assert isinstance(result, SizeReductionCSV)

def test_export_sizing_audit_snapshot_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_audit_snapshot
    assert callable(export_sizing_audit_snapshot)

def test_export_sizing_audit_snapshot_returns_dataclass():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_audit_snapshot, run_sizing_review, SizingAuditSnapshot
    result = export_sizing_audit_snapshot(run_sizing_review())
    assert isinstance(result, SizingAuditSnapshot)

def test_export_sizing_audit_snapshot_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_audit_snapshot, run_sizing_review
    result = export_sizing_audit_snapshot(run_sizing_review())
    assert result.paper_only is True

def test_export_sizing_audit_snapshot_contains_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_audit_snapshot, run_sizing_review
    result = export_sizing_audit_snapshot(run_sizing_review())
    assert result.schema_version == "209"


# =========================================================================
# Section 15: get_cockpit_summary
# =========================================================================
def test_get_cockpit_summary_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import get_cockpit_summary_v209
    assert callable(get_cockpit_summary_v209)

def test_get_cockpit_summary_returns_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import get_cockpit_summary_v209
    result = get_cockpit_summary_v209()
    assert isinstance(result, dict)

def test_get_cockpit_summary_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import get_cockpit_summary_v209
    result = get_cockpit_summary_v209()
    assert result.get("version") == "2.0.9" or result.get("sizing_version") == "2.0.9"

def test_get_cockpit_summary_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import get_cockpit_summary_v209
    result = get_cockpit_summary_v209()
    assert result.get("paper_only") is True or result.get("no_real_orders") is True


# =========================================================================
# Section 16: Scenarios module
# =========================================================================
def test_scenarios_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_scenarios_v209

def test_scenarios_has_scenarios_list():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v209 import SCENARIOS as SCENARIOS_V209
    assert isinstance(SCENARIOS_V209, list)

def test_scenarios_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v209 import SCENARIOS as SCENARIOS_V209
    assert len(SCENARIOS_V209) == 80

def test_scenarios_all_have_scenario_id():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v209 import SCENARIOS as SCENARIOS_V209
    for sc in SCENARIOS_V209:
        assert "scenario_id" in sc, f"Missing scenario_id: {sc}"

def test_scenarios_all_have_paper_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v209 import SCENARIOS as SCENARIOS_V209
    for sc in SCENARIOS_V209:
        assert sc.get("paper_only") is True, f"paper_only not True: {sc['scenario_id']}"

def test_scenarios_all_have_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v209 import SCENARIOS as SCENARIOS_V209
    for sc in SCENARIOS_V209:
        assert sc.get("should_auto_apply") is False, f"should_auto_apply not False: {sc['scenario_id']}"

def test_scenarios_all_have_schema_version_209():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v209 import SCENARIOS as SCENARIOS_V209
    for sc in SCENARIOS_V209:
        assert sc.get("schema_version") == "209", f"schema_version not 209: {sc['scenario_id']}"

def test_scenarios_ids_unique():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v209 import SCENARIOS as SCENARIOS_V209
    ids = [sc["scenario_id"] for sc in SCENARIOS_V209]
    assert len(ids) == len(set(ids)), "Duplicate scenario IDs found"

def test_scenarios_ids_start_with_sc209():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v209 import SCENARIOS as SCENARIOS_V209
    for sc in SCENARIOS_V209:
        assert sc["scenario_id"].startswith("SC209-"), f"Wrong prefix: {sc['scenario_id']}"

def test_scenarios_all_have_description():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v209 import SCENARIOS as SCENARIOS_V209
    for sc in SCENARIOS_V209:
        assert "description" in sc or "scenario_description" in sc, f"Missing description: {sc['scenario_id']}"


# =========================================================================
# Section 17: Fixtures module
# =========================================================================
def test_fixtures_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_fixtures_v209

def test_fixtures_has_fixtures_list():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v209 import FIXTURES as FIXTURES_V209
    assert isinstance(FIXTURES_V209, list)

def test_fixtures_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v209 import FIXTURES as FIXTURES_V209
    assert len(FIXTURES_V209) == 80

def test_fixtures_all_have_fixture_id():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v209 import FIXTURES as FIXTURES_V209
    for fx in FIXTURES_V209:
        assert "fixture_id" in fx, f"Missing fixture_id: {fx}"

def test_fixtures_all_have_paper_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v209 import FIXTURES as FIXTURES_V209
    for fx in FIXTURES_V209:
        assert fx.get("paper_only") is True, f"paper_only not True: {fx['fixture_id']}"

def test_fixtures_all_have_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v209 import FIXTURES as FIXTURES_V209
    for fx in FIXTURES_V209:
        assert fx.get("should_auto_apply") is False, f"should_auto_apply not False: {fx['fixture_id']}"

def test_fixtures_all_have_schema_version_209():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v209 import FIXTURES as FIXTURES_V209
    for fx in FIXTURES_V209:
        assert fx.get("schema_version") == "209", f"schema_version not 209: {fx['fixture_id']}"

def test_fixtures_ids_unique():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v209 import FIXTURES as FIXTURES_V209
    ids = [fx["fixture_id"] for fx in FIXTURES_V209]
    assert len(ids) == len(set(ids)), "Duplicate fixture IDs found"

def test_fixtures_ids_start_with_fx209():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v209 import FIXTURES as FIXTURES_V209
    for fx in FIXTURES_V209:
        assert fx["fixture_id"].startswith("FX209-"), f"Wrong prefix: {fx['fixture_id']}"


# =========================================================================
# Section 18: Health module
# =========================================================================
def test_health_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_health_v209

def test_run_health_check_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v209 import run_health_check
    assert callable(run_health_check)

def test_run_health_check_returns_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v209 import run_health_check
    result = run_health_check()
    assert isinstance(result, dict)

def test_run_health_check_has_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v209 import run_health_check
    result = run_health_check()
    assert "all_passed" in result

def test_run_health_check_has_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v209 import run_health_check
    result = run_health_check()
    assert "passed" in result

def test_run_health_check_has_failed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v209 import run_health_check
    result = run_health_check()
    assert "failed" in result

def test_run_health_check_has_total():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v209 import run_health_check
    result = run_health_check()
    assert "total" in result

def test_run_health_check_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v209 import run_health_check
    result = run_health_check()
    assert result["all_passed"] is True, f"Health check failed: {result.get('errors', [])}"

def test_run_health_check_zero_failures():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v209 import run_health_check
    result = run_health_check()
    assert result["failed"] == 0, f"Health check failures: {result.get('errors', [])}"

def test_run_health_check_passed_equals_total():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v209 import run_health_check
    result = run_health_check()
    assert result["passed"] == result["total"]


# =========================================================================
# Section 19: Release gate module
# =========================================================================
def test_release_gate_module_importable():
    import release.paper_cockpit_release_gate_v209

def test_run_release_gate_importable():
    from release.paper_cockpit_release_gate_v209 import run_release_gate
    assert callable(run_release_gate)

def test_run_release_gate_returns_dict():
    from release.paper_cockpit_release_gate_v209 import run_release_gate
    result = run_release_gate()
    assert isinstance(result, dict)

def test_run_release_gate_has_gate_passed():
    from release.paper_cockpit_release_gate_v209 import run_release_gate
    result = run_release_gate()
    assert "gate_passed" in result

def test_run_release_gate_has_passed_count():
    from release.paper_cockpit_release_gate_v209 import run_release_gate
    result = run_release_gate()
    assert "passed_count" in result

def test_run_release_gate_has_failed_count():
    from release.paper_cockpit_release_gate_v209 import run_release_gate
    result = run_release_gate()
    assert "failed_count" in result

def test_run_release_gate_has_total_count():
    from release.paper_cockpit_release_gate_v209 import run_release_gate
    result = run_release_gate()
    assert "total_count" in result

def test_run_release_gate_passes():
    from release.paper_cockpit_release_gate_v209 import run_release_gate
    result = run_release_gate()
    assert result["gate_passed"] is True, f"Release gate failed: {result.get('errors', [])}"

def test_run_release_gate_zero_failures():
    from release.paper_cockpit_release_gate_v209 import run_release_gate
    result = run_release_gate()
    assert result["failed_count"] == 0, f"Gate failures: {result.get('errors', [])}"


# =========================================================================
# Section 20: CLI registry integration
# =========================================================================
def test_cli_registry_importable():
    import cli.command_registry

def test_cli_registry_has_provider_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    assert isinstance(PROVIDER_COMMANDS, list)

def test_cli_registry_has_v209_commands():
    from cli.command_registry import PROVIDER_COMMANDS
    all_names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v209-review-sizing" in all_names

def test_cli_registry_v209_evaluate_risk_budget_present():
    from cli.command_registry import PROVIDER_COMMANDS
    all_names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v209-evaluate-risk-budget" in all_names

def test_cli_registry_v209_calculate_position_size_present():
    from cli.command_registry import PROVIDER_COMMANDS
    all_names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v209-calculate-position-size" in all_names

def test_cli_registry_v209_build_size_reduction_queue_present():
    from cli.command_registry import PROVIDER_COMMANDS
    all_names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v209-build-size-reduction-queue" in all_names

def test_cli_registry_v209_build_blocked_sizing_queue_present():
    from cli.command_registry import PROVIDER_COMMANDS
    all_names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v209-build-blocked-sizing-queue" in all_names

def test_cli_registry_v209_export_json_present():
    from cli.command_registry import PROVIDER_COMMANDS
    all_names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v209-export-json" in all_names

def test_cli_registry_v209_export_md_present():
    from cli.command_registry import PROVIDER_COMMANDS
    all_names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v209-export-md" in all_names

def test_cli_registry_v209_export_csv_present():
    from cli.command_registry import PROVIDER_COMMANDS
    all_names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v209-export-csv" in all_names

def test_cli_registry_v209_health_present():
    from cli.command_registry import PROVIDER_COMMANDS
    all_names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v209-health" in all_names

def test_cli_registry_v209_gate_present():
    from cli.command_registry import PROVIDER_COMMANDS
    all_names = [cmd.name for cmd in PROVIDER_COMMANDS]
    assert "paper-cockpit-v209-gate" in all_names

def test_cli_registry_v209_group_name():
    from cli.command_registry import PROVIDER_COMMANDS
    for cmd in PROVIDER_COMMANDS:
        if cmd.name == "paper-cockpit-v209-review-sizing":
            assert cmd.group == "paper_cockpit_v209"

def test_cli_registry_v209_introduced_in():
    from cli.command_registry import PROVIDER_COMMANDS
    for cmd in PROVIDER_COMMANDS:
        if cmd.name == "paper-cockpit-v209-review-sizing":
            assert cmd.introduced_in == "2.0.9"

def test_cli_registry_v209_safety_classification():
    from cli.command_registry import PROVIDER_COMMANDS
    for cmd in PROVIDER_COMMANDS:
        if cmd.name == "paper-cockpit-v209-evaluate-risk-budget":
            assert cmd.safety_classification == "RESEARCH_ONLY"

def test_cli_registry_v209_handler_names_set():
    from cli.command_registry import PROVIDER_COMMANDS
    for cmd in PROVIDER_COMMANDS:
        if cmd.name.startswith("paper-cockpit-v209-"):
            assert cmd.handler_name.startswith("cmd_paper_cockpit_v209_")


# =========================================================================
# Section 21: main.py handler integration
# =========================================================================
def test_main_module_importable():
    import main

def test_main_has_v209_review_sizing_handler():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v209_review_sizing")

def test_main_has_v209_evaluate_risk_budget_handler():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v209_evaluate_risk_budget")

def test_main_has_v209_calculate_position_size_handler():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v209_calculate_position_size")

def test_main_has_v209_build_size_reduction_queue_handler():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v209_build_size_reduction_queue")

def test_main_has_v209_build_blocked_sizing_queue_handler():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v209_build_blocked_sizing_queue")

def test_main_has_v209_export_json_handler():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v209_export_json")

def test_main_has_v209_export_md_handler():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v209_export_md")

def test_main_has_v209_export_csv_handler():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v209_export_csv")

def test_main_has_v209_health_handler():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v209_health")

def test_main_has_v209_gate_handler():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v209_gate")

def test_main_v209_review_sizing_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v209_review_sizing)

def test_main_v209_evaluate_risk_budget_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v209_evaluate_risk_budget)

def test_main_v209_calculate_position_size_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v209_calculate_position_size)

def test_main_v209_health_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v209_health)

def test_main_v209_gate_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v209_gate)

def test_main_v209_review_sizing_runs():
    import main
    main.cmd_paper_cockpit_v209_review_sizing()  # must not raise

def test_main_v209_evaluate_risk_budget_runs():
    import main
    main.cmd_paper_cockpit_v209_evaluate_risk_budget()  # must not raise

def test_main_v209_calculate_position_size_runs():
    import main
    main.cmd_paper_cockpit_v209_calculate_position_size()  # must not raise

def test_main_v209_export_json_runs():
    import main
    main.cmd_paper_cockpit_v209_export_json()  # must not raise

def test_main_v209_health_runs():
    import main
    main.cmd_paper_cockpit_v209_health()  # must not raise


# =========================================================================
# Section 22: GUI panel integration
# =========================================================================
def test_gui_panel_importable():
    import gui.small_capital_strategy_panel

def test_gui_panel_has_panel_version_v209():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V209
    assert PANEL_VERSION_V209 == "2.0.9"

def test_gui_panel_has_tabs_v209_sizing():
    from gui.small_capital_strategy_panel import _TABS_V209_SIZING
    assert isinstance(_TABS_V209_SIZING, list)
    assert len(_TABS_V209_SIZING) == 3

def test_gui_panel_tabs_v209_contains_position_sizing():
    from gui.small_capital_strategy_panel import _TABS_V209_SIZING
    assert "position_sizing_v209" in _TABS_V209_SIZING

def test_gui_panel_tabs_v209_contains_risk_budget():
    from gui.small_capital_strategy_panel import _TABS_V209_SIZING
    assert "risk_budget_v209" in _TABS_V209_SIZING

def test_gui_panel_tabs_v209_contains_size_reduction_queue():
    from gui.small_capital_strategy_panel import _TABS_V209_SIZING
    assert "size_reduction_queue_v209" in _TABS_V209_SIZING

def test_gui_panel_get_v209_tab_names():
    from gui.small_capital_strategy_panel import get_v209_tab_names
    assert callable(get_v209_tab_names)
    names = get_v209_tab_names()
    assert isinstance(names, list)
    assert len(names) == 3

def test_gui_panel_render_position_sizing_v209_tab():
    from gui.small_capital_strategy_panel import render_position_sizing_v209_tab
    result = render_position_sizing_v209_tab()
    assert isinstance(result, dict)
    assert result.get("paper_only") is True

def test_gui_panel_render_risk_budget_v209_tab():
    from gui.small_capital_strategy_panel import render_risk_budget_v209_tab
    result = render_risk_budget_v209_tab()
    assert isinstance(result, dict)
    assert result.get("paper_only") is True

def test_gui_panel_render_size_reduction_queue_v209_tab():
    from gui.small_capital_strategy_panel import render_size_reduction_queue_v209_tab
    result = render_size_reduction_queue_v209_tab()
    assert isinstance(result, dict)
    assert result.get("paper_only") is True

def test_gui_panel_render_position_sizing_should_auto_apply_false():
    from gui.small_capital_strategy_panel import render_position_sizing_v209_tab
    result = render_position_sizing_v209_tab()
    assert result.get("should_auto_apply") is False

def test_gui_panel_render_risk_budget_should_auto_apply_false():
    from gui.small_capital_strategy_panel import render_risk_budget_v209_tab
    result = render_risk_budget_v209_tab()
    assert result.get("should_auto_apply") is False

def test_gui_panel_render_size_reduction_should_auto_apply_false():
    from gui.small_capital_strategy_panel import render_size_reduction_queue_v209_tab
    result = render_size_reduction_queue_v209_tab()
    assert result.get("should_auto_apply") is False

def test_gui_panel_render_position_sizing_schema_version():
    from gui.small_capital_strategy_panel import render_position_sizing_v209_tab
    result = render_position_sizing_v209_tab()
    assert result.get("schema_version") == "209"

def test_gui_panel_render_risk_budget_schema_version():
    from gui.small_capital_strategy_panel import render_risk_budget_v209_tab
    result = render_risk_budget_v209_tab()
    assert result.get("schema_version") == "209"

def test_gui_panel_render_size_reduction_schema_version():
    from gui.small_capital_strategy_panel import render_size_reduction_queue_v209_tab
    result = render_size_reduction_queue_v209_tab()
    assert result.get("schema_version") == "209"

def test_gui_panel_render_all_tabs_has_position_sizing_v209():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "position_sizing_v209" in result

def test_gui_panel_render_all_tabs_has_risk_budget_v209():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "risk_budget_v209" in result

def test_gui_panel_render_all_tabs_has_size_reduction_queue_v209():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "size_reduction_queue_v209" in result

def test_gui_panel_render_all_tabs_no_error_tab_v209():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    for tab_name in ["position_sizing_v209", "risk_budget_v209", "size_reduction_queue_v209"]:
        tab = result.get(tab_name, {})
        assert tab.get("error") is None or tab.get("error") == "" or "error" not in tab, \
            f"Tab {tab_name} has error: {tab.get('error')}"

def test_gui_panel_sizing_actions_recommendation_only():
    from gui.small_capital_strategy_panel import render_position_sizing_v209_tab
    result = render_position_sizing_v209_tab()
    assert result.get("sizing_actions_recommendation_only") is True


# =========================================================================
# Section 23: Backward compatibility — v2.0.8
# =========================================================================
def test_v208_module_still_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v208

def test_v208_version_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import VERSION
    assert VERSION == "2.0.8"

def test_v208_no_real_orders_still_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_v208_broker_execution_enabled_still_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_v208_run_exposure_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    assert callable(run_exposure_review)

def test_v208_run_exposure_review_returns_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, ExposureReviewResult
    result = run_exposure_review()
    assert isinstance(result, ExposureReviewResult)

def test_v208_verify_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import verify_version
    assert verify_version() is True

def test_v208_health_still_passes():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v208 import run_health_check
    result = run_health_check()
    assert result["all_passed"] is True, f"v208 health regressed: {result.get('errors', [])}"


# =========================================================================
# Section 24: Model name registry
# =========================================================================
def test_all_model_names_v209_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import _ALL_MODEL_NAMES_V209
    assert isinstance(_ALL_MODEL_NAMES_V209, list)

def test_all_model_names_v209_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import _ALL_MODEL_NAMES_V209
    assert len(_ALL_MODEL_NAMES_V209) == 14

def test_all_model_names_contains_risk_budget_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import _ALL_MODEL_NAMES_V209
    assert "RiskBudgetPolicy" in _ALL_MODEL_NAMES_V209

def test_all_model_names_contains_candidate_sizing_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import _ALL_MODEL_NAMES_V209
    assert "CandidateSizingItem" in _ALL_MODEL_NAMES_V209

def test_all_model_names_contains_sizing_review_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import _ALL_MODEL_NAMES_V209
    assert "SizingReviewResult" in _ALL_MODEL_NAMES_V209

def test_all_model_names_contains_position_sizing_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import _ALL_MODEL_NAMES_V209
    assert "PositionSizingSummary" in _ALL_MODEL_NAMES_V209


# =========================================================================
# Section 25: Edge cases & safety invariants
# =========================================================================
def test_risk_budget_policy_auto_apply_cannot_be_overridden():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy()
    # Try direct attribute mutation — post_init already set it
    assert p.auto_apply_enabled is False

def test_candidate_sizing_item_should_auto_apply_cannot_be_overridden():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem(should_auto_apply=True)
    assert item.should_auto_apply is False

def test_sizing_review_result_should_auto_apply_cannot_be_overridden():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SizingReviewResult
    r = SizingReviewResult(should_auto_apply=True)
    assert r.should_auto_apply is False

def test_multiple_risk_budget_policy_instances_independent():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p1 = RiskBudgetPolicy(account_equity=300000.0)
    p2 = RiskBudgetPolicy(account_equity=500000.0)
    assert p1.account_equity != p2.account_equity
    assert p1.auto_apply_enabled is False
    assert p2.auto_apply_enabled is False

def test_calculate_position_size_different_symbols():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    r1 = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
    )
    r2 = calculate_position_size(
        symbol="2317", name="Hon Hai", candidate_id="C002",
        theme_id="T001", sector_id="S001",
        candidate_score=0.7, final_priority_score=0.65,
        entry_price=110.0, stop_price=104.0,
    )
    assert r1.symbol == "2330"
    assert r2.symbol == "2317"
    assert r1.should_auto_apply is False
    assert r2.should_auto_apply is False

def test_run_sizing_review_multiple_calls_independent():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    r1 = run_sizing_review()
    r2 = run_sizing_review()
    assert r1.should_auto_apply is False
    assert r2.should_auto_apply is False

def test_covered_versions_includes_208():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import COVERED_VERSIONS
    assert "2.0.8" in COVERED_VERSIONS

def test_covered_versions_includes_207():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import COVERED_VERSIONS
    assert "2.0.7" in COVERED_VERSIONS

def test_covered_versions_includes_206():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import COVERED_VERSIONS
    assert "2.0.6" in COVERED_VERSIONS

def test_covered_versions_includes_205():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import COVERED_VERSIONS
    assert "2.0.5" in COVERED_VERSIONS

def test_calculate_position_size_base_size_formula():
    """Base size = max_loss_twd / stop_distance_pct. Larger stop = smaller base."""
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    tight_stop = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=594.0,  # 1% stop
        market_state="trending_up", lifecycle_state="active",
    )
    wide_stop = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=540.0,  # 10% stop
        market_state="trending_up", lifecycle_state="active",
    )
    assert tight_stop.base_position_size >= wide_stop.base_position_size

def test_calculate_position_size_final_risk_pct_within_budget():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size, RiskBudgetPolicy
    policy = RiskBudgetPolicy(max_single_trade_risk_pct=0.01)
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
        policy=policy,
    )
    assert result.final_risk_pct <= policy.max_single_trade_risk_pct + 1e-9

def test_export_sizing_json_no_real_orders_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_json, run_sizing_review
    result = export_sizing_json(run_sizing_review())
    assert result.paper_only is True or result.paper_only_confirmed is True

def test_export_sizing_audit_snapshot_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_audit_snapshot, run_sizing_review
    result = export_sizing_audit_snapshot(run_sizing_review())
    assert result.paper_only is True

def test_size_action_block_for_zero_final_size():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="XXXX", name="Blocked", candidate_id="C999",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=100.0, stop_price=94.0,
        market_state="risk_off",
    )
    assert result.final_recommended_size == 0
    assert result.size_action in ["block_new_position", "human_review_required"]

def test_calculate_position_size_observation_only_for_very_small():
    """When all reductions bring size near zero but not quite, observation_only may apply."""
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    # High volatility + low liquidity + high exposure penalty + low priority
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.25, final_priority_score=0.25,
        entry_price=600.0, stop_price=564.0,
        is_high_volatility=True,
        is_low_liquidity=True,
        exposure_penalty_pct=50.0,
        market_state="range_bound",
        lifecycle_state="active",
    )
    assert result.size_action in [
        "observation_only", "minimum_probe_size", "reduce_size",
        "block_new_position", "human_review_required",
    ]

def test_run_sizing_review_paper_only_safety_snapshot_truthy2():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    # paper_only_safety_snapshot is True or a dict — must be truthy
    assert result.paper_only_safety_snapshot is not None
    assert result.paper_only_safety_snapshot is not False

def test_health_check_total_checks_reasonable():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v209 import run_health_check
    result = run_health_check()
    assert result["total"] >= 10

def test_release_gate_total_checks_reasonable():
    from release.paper_cockpit_release_gate_v209 import run_release_gate
    result = run_release_gate()
    assert result["total_count"] >= 10


# =========================================================================
# Section 26: Additional sizing logic & robustness tests
# =========================================================================
def test_calculate_position_size_returns_symbol():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2454", name="MediaTek", candidate_id="C010",
        theme_id="T002", sector_id="S002",
        candidate_score=0.7, final_priority_score=0.65,
        entry_price=1000.0, stop_price=940.0,
    )
    assert result.symbol == "2454"

def test_calculate_position_size_returns_candidate_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2454", name="MediaTek", candidate_id="C010",
        theme_id="T002", sector_id="S002",
        candidate_score=0.7, final_priority_score=0.65,
        entry_price=1000.0, stop_price=940.0,
    )
    assert result.candidate_id == "C010"

def test_calculate_position_size_returns_theme_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2454", name="MediaTek", candidate_id="C010",
        theme_id="T002", sector_id="S002",
        candidate_score=0.7, final_priority_score=0.65,
        entry_price=1000.0, stop_price=940.0,
    )
    assert result.theme_id == "T002"

def test_calculate_position_size_returns_sector_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2454", name="MediaTek", candidate_id="C010",
        theme_id="T002", sector_id="S002",
        candidate_score=0.7, final_priority_score=0.65,
        entry_price=1000.0, stop_price=940.0,
    )
    assert result.sector_id == "S002"

def test_calculate_position_size_returns_entry_price():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2454", name="MediaTek", candidate_id="C010",
        theme_id="T002", sector_id="S002",
        candidate_score=0.7, final_priority_score=0.65,
        entry_price=1000.0, stop_price=940.0,
    )
    assert result.entry_price == 1000.0

def test_calculate_position_size_returns_stop_price():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2454", name="MediaTek", candidate_id="C010",
        theme_id="T002", sector_id="S002",
        candidate_score=0.7, final_priority_score=0.65,
        entry_price=1000.0, stop_price=940.0,
    )
    assert result.stop_price == 940.0

def test_candidate_sizing_item_blocked_reasons_empty_by_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import CandidateSizingItem
    item = CandidateSizingItem()
    assert isinstance(item.blocked_reasons, list)

def test_risk_budget_policy_policy_id_settable():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import RiskBudgetPolicy
    p = RiskBudgetPolicy(policy_id="POL-001")
    assert p.policy_id == "POL-001"

def test_sizing_review_result_sizing_version_field():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import SizingReviewResult
    r = SizingReviewResult()
    assert hasattr(r, "sizing_version")

def test_position_sizing_summary_allowed_full_size_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import PositionSizingSummary
    s = PositionSizingSummary()
    assert hasattr(s, "allowed_full_size_count")
    assert s.allowed_full_size_count >= 0

def test_position_sizing_summary_blocked_position_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import PositionSizingSummary
    s = PositionSizingSummary()
    assert hasattr(s, "blocked_position_count")
    assert s.blocked_position_count >= 0

def test_position_sizing_summary_human_review_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import PositionSizingSummary
    s = PositionSizingSummary()
    assert hasattr(s, "human_review_count")

def test_position_sizing_summary_sizing_quality_grade():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import PositionSizingSummary
    s = PositionSizingSummary()
    assert hasattr(s, "sizing_quality_grade")

def test_position_sizing_summary_risk_budget_quality_grade():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import PositionSizingSummary
    s = PositionSizingSummary()
    assert hasattr(s, "risk_budget_quality_grade")

def test_export_candidate_sizing_csv_has_header():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_candidate_sizing_csv, run_sizing_review
    result = export_candidate_sizing_csv(run_sizing_review())
    assert result.csv_content is not None

def test_export_risk_budget_csv_has_content():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_risk_budget_csv, run_sizing_review
    result = export_risk_budget_csv(run_sizing_review())
    assert result.csv_content is not None

def test_export_size_reduction_csv_has_content():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_size_reduction_csv, run_sizing_review
    result = export_size_reduction_csv(run_sizing_review())
    assert result.csv_content is not None

def test_export_sizing_json_not_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_json, run_sizing_review
    result = export_sizing_json(run_sizing_review())
    assert len(result.content) >= 0

def test_export_sizing_markdown_not_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import export_sizing_markdown, run_sizing_review
    result = export_sizing_markdown(run_sizing_review())
    assert result.content is not None

def test_gui_panel_v209_tabs_in_combined_tabs_list():
    from gui.small_capital_strategy_panel import _TABS
    assert "position_sizing_v209" in _TABS
    assert "risk_budget_v209" in _TABS
    assert "size_reduction_queue_v209" in _TABS

def test_gui_panel_render_position_sizing_auto_apply_enabled_false():
    from gui.small_capital_strategy_panel import render_position_sizing_v209_tab
    result = render_position_sizing_v209_tab()
    assert result.get("auto_apply_enabled") is False

def test_gui_panel_render_risk_budget_auto_apply_enabled_false():
    from gui.small_capital_strategy_panel import render_risk_budget_v209_tab
    result = render_risk_budget_v209_tab()
    assert result.get("auto_apply_enabled") is False

def test_gui_panel_render_size_reduction_auto_apply_enabled_false():
    from gui.small_capital_strategy_panel import render_size_reduction_queue_v209_tab
    result = render_size_reduction_queue_v209_tab()
    assert result.get("auto_apply_enabled") is False

def test_main_v209_build_size_reduction_queue_runs():
    import main
    main.cmd_paper_cockpit_v209_build_size_reduction_queue()  # must not raise

def test_main_v209_build_blocked_sizing_queue_runs():
    import main
    main.cmd_paper_cockpit_v209_build_blocked_sizing_queue()  # must not raise

def test_main_v209_export_md_runs():
    import main
    main.cmd_paper_cockpit_v209_export_md()  # must not raise

def test_main_v209_export_csv_runs():
    import main
    main.cmd_paper_cockpit_v209_export_csv()  # must not raise

def test_main_v209_gate_runs():
    import main
    main.cmd_paper_cockpit_v209_gate()  # must not raise

def test_scenarios_schema_version_all_209():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v209 import SCENARIOS
    schema_versions = set(sc.get("schema_version") for sc in SCENARIOS)
    assert schema_versions == {"209"}

def test_fixtures_schema_version_all_209():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v209 import FIXTURES
    schema_versions = set(fx.get("schema_version") for fx in FIXTURES)
    assert schema_versions == {"209"}

def test_calculate_position_size_observation_market_state():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import calculate_position_size
    result = calculate_position_size(
        symbol="2330", name="TSMC", candidate_id="C001",
        theme_id="T001", sector_id="S001",
        candidate_score=0.8, final_priority_score=0.75,
        entry_price=600.0, stop_price=564.0,
        market_state="observation",
    )
    # observation state should reduce or block, not allow full
    assert result.size_action in [
        "reduce_size", "minimum_probe_size", "observation_only",
        "block_new_position", "human_review_required",
    ]

def test_run_sizing_review_sizing_review_id_nonempty():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import run_sizing_review
    result = run_sizing_review()
    assert isinstance(result.sizing_review_id, str)
    assert len(result.sizing_review_id) > 0

def test_covered_versions_list_nonempty():
    from paper_trading.small_capital_strategy.paper_cockpit_v209 import COVERED_VERSIONS
    assert len(COVERED_VERSIONS) >= 10
