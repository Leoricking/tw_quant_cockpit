"""
tests/test_portfolio_risk_report_version_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Version Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.portfolio_risk_report_version_v199 import (
    VERSION, SCHEMA_VERSION, RELEASE_NAME, BASELINE_TESTS, MIN_NEW_TESTS,
    ENTRY_TYPES, POSITION_SIZING_POLICIES, RISK_GRADES, RECOMMENDATIONS,
    PAPER_ACTIONS, CLI_COMMANDS, GUI_TABS, CAPITAL_PROFILE_300K,
    ENTRY_SIZE_MULTIPLIERS, FORBIDDEN_ACTIONS, HARD_BLOCK_CONDITIONS,
    verify_version, get_version_info,
)


def test_version_is_1_9_9():
    assert VERSION == "1.9.9"


def test_schema_version_is_199():
    assert SCHEMA_VERSION == "199"


def test_version_is_string():
    assert isinstance(VERSION, str)


def test_schema_version_is_string():
    assert isinstance(SCHEMA_VERSION, str)


def test_release_name_contains_portfolio():
    assert "Portfolio" in RELEASE_NAME


def test_release_name_contains_risk():
    assert "Risk" in RELEASE_NAME


def test_release_name_contains_lab():
    assert "Lab" in RELEASE_NAME


def test_release_name_is_string():
    assert isinstance(RELEASE_NAME, str)


def test_baseline_tests_is_31044():
    assert BASELINE_TESTS == 31044


def test_min_new_tests_is_400():
    assert MIN_NEW_TESTS == 400


def test_entry_types_count_is_7():
    assert len(ENTRY_TYPES) == 7


def test_entry_types_has_A_PULLBACK_10MA():
    assert "A_PULLBACK_10MA" in ENTRY_TYPES


def test_entry_types_has_B_BREAKOUT_BASE():
    assert "B_BREAKOUT_BASE" in ENTRY_TYPES


def test_entry_types_has_C_RECLAIM_20MA():
    assert "C_RECLAIM_20MA" in ENTRY_TYPES


def test_entry_types_has_TEST_POSITION():
    assert "TEST_POSITION" in ENTRY_TYPES


def test_entry_types_has_ADD_POSITION():
    assert "ADD_POSITION" in ENTRY_TYPES


def test_entry_types_has_REDUCE_POSITION():
    assert "REDUCE_POSITION" in ENTRY_TYPES


def test_entry_types_has_NO_ENTRY():
    assert "NO_ENTRY" in ENTRY_TYPES


def test_entry_types_is_list():
    assert isinstance(ENTRY_TYPES, list)


def test_position_sizing_policies_count_is_11():
    assert len(POSITION_SIZING_POLICIES) == 11


def test_position_sizing_policies_is_list():
    assert isinstance(POSITION_SIZING_POLICIES, list)


def test_position_sizing_policies_all_strings():
    assert all(isinstance(p, str) for p in POSITION_SIZING_POLICIES)


def test_risk_grades_count_is_6():
    assert len(RISK_GRADES) == 6


def test_risk_grades_has_LOW():
    assert "LOW" in RISK_GRADES


def test_risk_grades_has_MODERATE():
    assert "MODERATE" in RISK_GRADES


def test_risk_grades_has_ELEVATED():
    assert "ELEVATED" in RISK_GRADES


def test_risk_grades_has_HIGH():
    assert "HIGH" in RISK_GRADES


def test_risk_grades_has_CRITICAL():
    assert "CRITICAL" in RISK_GRADES


def test_risk_grades_has_INVALID():
    assert "INVALID" in RISK_GRADES


def test_recommendations_count_is_10():
    assert len(RECOMMENDATIONS) == 10


def test_recommendations_is_list():
    assert isinstance(RECOMMENDATIONS, list)


def test_recommendations_all_strings():
    assert all(isinstance(r, str) for r in RECOMMENDATIONS)


def test_paper_actions_count_is_7():
    assert len(PAPER_ACTIONS) == 7


def test_paper_actions_is_list():
    assert isinstance(PAPER_ACTIONS, list)


def test_paper_actions_has_PAPER_ALLOW_NORMAL_SIZE():
    assert "PAPER_ALLOW_NORMAL_SIZE" in PAPER_ACTIONS


def test_paper_actions_has_PAPER_ALLOW_REDUCED_SIZE():
    assert "PAPER_ALLOW_REDUCED_SIZE" in PAPER_ACTIONS


def test_cli_commands_count_is_18():
    assert len(CLI_COMMANDS) == 18


def test_cli_commands_is_list():
    assert isinstance(CLI_COMMANDS, list)


def test_cli_commands_all_strings():
    assert all(isinstance(c, str) for c in CLI_COMMANDS)


def test_gui_tabs_count_is_3():
    assert len(GUI_TABS) == 3


def test_gui_tabs_has_portfolio_risk_report():
    assert "portfolio_risk_report" in GUI_TABS


def test_gui_tabs_has_position_sizing_policy():
    assert "position_sizing_policy" in GUI_TABS


def test_gui_tabs_has_risk_budget_dashboard():
    assert "risk_budget_dashboard" in GUI_TABS


def test_capital_profile_300k_capital_base():
    assert CAPITAL_PROFILE_300K["capital_base"] == 300000


def test_capital_profile_300k_normal_single_trade_risk_pct_min():
    assert CAPITAL_PROFILE_300K["normal_single_trade_risk_pct_min"] == 0.008


def test_capital_profile_300k_normal_single_trade_risk_pct_max():
    assert CAPITAL_PROFILE_300K["normal_single_trade_risk_pct_max"] == 0.015


def test_capital_profile_300k_normal_single_trade_loss_min():
    assert CAPITAL_PROFILE_300K["normal_single_trade_loss_min"] == 2400


def test_capital_profile_300k_normal_single_trade_loss_max():
    assert CAPITAL_PROFILE_300K["normal_single_trade_loss_max"] == 4500


def test_capital_profile_300k_is_dict():
    assert isinstance(CAPITAL_PROFILE_300K, dict)


def test_entry_size_multiplier_A_is_1_0():
    assert ENTRY_SIZE_MULTIPLIERS["A_PULLBACK_10MA"] == 1.0


def test_entry_size_multiplier_B_is_0_7():
    assert ENTRY_SIZE_MULTIPLIERS["B_BREAKOUT_BASE"] == 0.7


def test_entry_size_multiplier_C_is_0_5():
    assert ENTRY_SIZE_MULTIPLIERS["C_RECLAIM_20MA"] == 0.5


def test_entry_size_multiplier_TEST_is_0_3():
    assert ENTRY_SIZE_MULTIPLIERS["TEST_POSITION"] == 0.3


def test_forbidden_actions_count_is_10():
    assert len(FORBIDDEN_ACTIONS) == 10


def test_forbidden_actions_no_overlap_with_paper_actions():
    assert not any(fa in PAPER_ACTIONS for fa in FORBIDDEN_ACTIONS)


def test_hard_block_conditions_count_is_22():
    assert len(HARD_BLOCK_CONDITIONS) == 22


def test_hard_block_conditions_is_list():
    assert isinstance(HARD_BLOCK_CONDITIONS, list)


def test_hard_block_conditions_has_real_order_requested():
    assert "real_order_requested" in HARD_BLOCK_CONDITIONS


def test_hard_block_conditions_has_missing_paper_only_flags():
    assert "missing_paper_only_flags" in HARD_BLOCK_CONDITIONS


def test_verify_version_returns_True():
    assert verify_version() is True


def test_get_version_info_returns_dict():
    assert isinstance(get_version_info(), dict)


def test_get_version_info_version_field():
    assert get_version_info()["version"] == "1.9.9"


def test_get_version_info_schema_version_field():
    assert get_version_info()["schema_version"] == "199"


def test_get_version_info_paper_only_True():
    assert get_version_info()["paper_only"] is True


def test_get_version_info_no_real_orders_True():
    assert get_version_info()["no_real_orders"] is True


def test_get_version_info_production_trading_blocked_True():
    assert get_version_info()["production_trading_blocked"] is True
