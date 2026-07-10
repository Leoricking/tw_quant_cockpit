"""
tests/test_integrated_strategy_enums_v178.py
Tests for integrated_strategy_enums_v178.py — v1.7.8 Small Capital Strategy Integration.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.

Safety invariants:
    paper_only=True, no_real_orders=True, no_broker=True, not_investment_advice=True
"""
import pytest
from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
    IntegratedDecisionAction,
    IntegratedNoTradeReasonCode,
    IntegratedScoreGrade,
    IntegratedBlockReason,
    IntegratedHealthStatus,
    IntegratedRegimeStatus,
    IntegratedWatchlistStatus,
    IntegratedABCStatus,
    IntegratedThemeStatus,
    IntegratedRiskLevel,
    IntegratedBehaviorStatus,
    get_all_enum_names,
    get_all_decision_actions,
    get_all_no_trade_reasons,
    get_all_block_reasons,
    score_to_grade,
    _SCHEMA,
    _POLICY,
)

# ---------------------------------------------------------------------------
# Safety invariants
# ---------------------------------------------------------------------------
paper_only = True
no_real_orders = True
no_broker = True
not_investment_advice = True


# ---------------------------------------------------------------------------
# IntegratedDecisionAction — member count and membership
# ---------------------------------------------------------------------------

def test_decision_action_has_exactly_9_members():
    assert len(IntegratedDecisionAction) == 9


def test_decision_action_has_observe():
    assert IntegratedDecisionAction.OBSERVE in IntegratedDecisionAction


def test_decision_action_has_wait():
    assert IntegratedDecisionAction.WAIT in IntegratedDecisionAction


def test_decision_action_has_paper_plan_ready():
    assert IntegratedDecisionAction.PAPER_PLAN_READY in IntegratedDecisionAction


def test_decision_action_has_paper_entry_allowed():
    assert IntegratedDecisionAction.PAPER_ENTRY_ALLOWED in IntegratedDecisionAction


def test_decision_action_has_paper_add_allowed():
    assert IntegratedDecisionAction.PAPER_ADD_ALLOWED in IntegratedDecisionAction


def test_decision_action_has_reduce_risk():
    assert IntegratedDecisionAction.REDUCE_RISK in IntegratedDecisionAction


def test_decision_action_has_review_required():
    assert IntegratedDecisionAction.REVIEW_REQUIRED in IntegratedDecisionAction


def test_decision_action_has_blocked():
    assert IntegratedDecisionAction.BLOCKED in IntegratedDecisionAction


def test_decision_action_has_no_trade():
    assert IntegratedDecisionAction.NO_TRADE in IntegratedDecisionAction


def test_all_9_decision_action_values_are_correct():
    expected = {
        "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED",
        "PAPER_ADD_ALLOWED", "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE",
    }
    actual = {a.value for a in IntegratedDecisionAction}
    assert actual == expected


# ---------------------------------------------------------------------------
# Forbidden values NOT in IntegratedDecisionAction
# ---------------------------------------------------------------------------

def test_buy_not_in_decision_action_values():
    assert "BUY" not in [a.value for a in IntegratedDecisionAction]


def test_sell_not_in_decision_action_values():
    assert "SELL" not in [a.value for a in IntegratedDecisionAction]


def test_order_not_in_decision_action_values():
    assert "ORDER" not in [a.value for a in IntegratedDecisionAction]


def test_execute_not_in_decision_action_values():
    assert "EXECUTE" not in [a.value for a in IntegratedDecisionAction]


def test_submit_order_not_in_decision_action_values():
    assert "SUBMIT_ORDER" not in [a.value for a in IntegratedDecisionAction]


def test_auto_trade_not_in_decision_action_values():
    assert "AUTO_TRADE" not in [a.value for a in IntegratedDecisionAction]


def test_real_trade_not_in_decision_action_values():
    assert "REAL_TRADE" not in [a.value for a in IntegratedDecisionAction]


def test_live_trade_not_in_decision_action_values():
    assert "LIVE_TRADE" not in [a.value for a in IntegratedDecisionAction]


def test_broker_order_not_in_decision_action_values():
    assert "BROKER_ORDER" not in [a.value for a in IntegratedDecisionAction]


# ---------------------------------------------------------------------------
# IntegratedNoTradeReasonCode — 15 members
# ---------------------------------------------------------------------------

def test_no_trade_reason_code_has_exactly_15_members():
    assert len(IntegratedNoTradeReasonCode) == 15


def test_no_trade_reason_code_has_market_risk_off():
    assert IntegratedNoTradeReasonCode.MARKET_RISK_OFF in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_theme_weak():
    assert IntegratedNoTradeReasonCode.THEME_WEAK in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_watchlist_excluded():
    assert IntegratedNoTradeReasonCode.WATCHLIST_EXCLUDED in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_abc_not_ready():
    assert IntegratedNoTradeReasonCode.ABC_NOT_READY in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_risk_budget_exceeded():
    assert IntegratedNoTradeReasonCode.RISK_BUDGET_EXCEEDED in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_stop_loss_missing():
    assert IntegratedNoTradeReasonCode.STOP_LOSS_MISSING in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_behavior_risk_blocked():
    assert IntegratedNoTradeReasonCode.BEHAVIOR_RISK_BLOCKED in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_mistake_repeat_blocked():
    assert IntegratedNoTradeReasonCode.MISTAKE_REPEAT_BLOCKED in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_overtrading_risk():
    assert IntegratedNoTradeReasonCode.OVERTRADING_RISK in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_journal_required():
    assert IntegratedNoTradeReasonCode.JOURNAL_REQUIRED in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_real_order_blocked():
    assert IntegratedNoTradeReasonCode.REAL_ORDER_BLOCKED in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_broker_blocked():
    assert IntegratedNoTradeReasonCode.BROKER_BLOCKED in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_margin_blocked():
    assert IntegratedNoTradeReasonCode.MARGIN_BLOCKED in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_data_incomplete():
    assert IntegratedNoTradeReasonCode.DATA_INCOMPLETE in IntegratedNoTradeReasonCode


def test_no_trade_reason_code_has_lineage_missing():
    assert IntegratedNoTradeReasonCode.LINEAGE_MISSING in IntegratedNoTradeReasonCode


def test_all_no_trade_reason_code_values_are_strings():
    for member in IntegratedNoTradeReasonCode:
        assert isinstance(member.value, str)


# ---------------------------------------------------------------------------
# IntegratedScoreGrade — 5 members
# ---------------------------------------------------------------------------

def test_score_grade_has_exactly_5_members():
    assert len(IntegratedScoreGrade) == 5


def test_score_grade_has_excellent():
    assert IntegratedScoreGrade.EXCELLENT in IntegratedScoreGrade


def test_score_grade_has_good():
    assert IntegratedScoreGrade.GOOD in IntegratedScoreGrade


def test_score_grade_has_acceptable():
    assert IntegratedScoreGrade.ACCEPTABLE in IntegratedScoreGrade


def test_score_grade_has_marginal():
    assert IntegratedScoreGrade.MARGINAL in IntegratedScoreGrade


def test_score_grade_has_blocked():
    assert IntegratedScoreGrade.BLOCKED in IntegratedScoreGrade


# ---------------------------------------------------------------------------
# IntegratedBlockReason — 12 members
# ---------------------------------------------------------------------------

def test_block_reason_has_exactly_12_members():
    assert len(IntegratedBlockReason) == 12


def test_block_reason_has_no_stop_loss():
    assert IntegratedBlockReason.NO_STOP_LOSS in IntegratedBlockReason


def test_block_reason_has_real_order_requested():
    assert IntegratedBlockReason.REAL_ORDER_REQUESTED in IntegratedBlockReason


def test_block_reason_has_broker_requested():
    assert IntegratedBlockReason.BROKER_REQUESTED in IntegratedBlockReason


def test_block_reason_has_margin_requested():
    assert IntegratedBlockReason.MARGIN_REQUESTED in IntegratedBlockReason


def test_block_reason_has_regime_risk_off():
    assert IntegratedBlockReason.REGIME_RISK_OFF in IntegratedBlockReason


def test_block_reason_has_behavior_blocked():
    assert IntegratedBlockReason.BEHAVIOR_BLOCKED in IntegratedBlockReason


def test_block_reason_has_risk_blocked():
    assert IntegratedBlockReason.RISK_BLOCKED in IntegratedBlockReason


def test_block_reason_has_watchlist_excluded():
    assert IntegratedBlockReason.WATCHLIST_EXCLUDED in IntegratedBlockReason


def test_block_reason_has_theme_excluded():
    assert IntegratedBlockReason.THEME_EXCLUDED in IntegratedBlockReason


def test_block_reason_has_abc_blocked():
    assert IntegratedBlockReason.ABC_BLOCKED in IntegratedBlockReason


def test_block_reason_has_lineage_missing():
    assert IntegratedBlockReason.LINEAGE_MISSING in IntegratedBlockReason


def test_block_reason_has_production_write_attempted():
    assert IntegratedBlockReason.PRODUCTION_WRITE_ATTEMPTED in IntegratedBlockReason


# ---------------------------------------------------------------------------
# IntegratedHealthStatus — 3 members
# ---------------------------------------------------------------------------

def test_health_status_has_exactly_3_members():
    assert len(IntegratedHealthStatus) == 3


def test_health_status_has_pass():
    assert IntegratedHealthStatus.PASS in IntegratedHealthStatus


def test_health_status_has_fail():
    assert IntegratedHealthStatus.FAIL in IntegratedHealthStatus


def test_health_status_has_warning():
    assert IntegratedHealthStatus.WARNING in IntegratedHealthStatus


# ---------------------------------------------------------------------------
# IntegratedRegimeStatus — 6 members
# ---------------------------------------------------------------------------

def test_regime_status_has_exactly_6_members():
    assert len(IntegratedRegimeStatus) == 6


def test_regime_status_has_bull():
    assert IntegratedRegimeStatus.BULL in IntegratedRegimeStatus


def test_regime_status_has_bull_soft():
    assert IntegratedRegimeStatus.BULL_SOFT in IntegratedRegimeStatus


def test_regime_status_has_neutral():
    assert IntegratedRegimeStatus.NEUTRAL in IntegratedRegimeStatus


def test_regime_status_has_risk_off():
    assert IntegratedRegimeStatus.RISK_OFF in IntegratedRegimeStatus


def test_regime_status_has_bear():
    assert IntegratedRegimeStatus.BEAR in IntegratedRegimeStatus


def test_regime_status_has_unknown():
    assert IntegratedRegimeStatus.UNKNOWN in IntegratedRegimeStatus


# ---------------------------------------------------------------------------
# IntegratedWatchlistStatus — 4 members
# ---------------------------------------------------------------------------

def test_watchlist_status_has_exactly_4_members():
    assert len(IntegratedWatchlistStatus) == 4


def test_watchlist_status_has_focus():
    assert IntegratedWatchlistStatus.FOCUS in IntegratedWatchlistStatus


def test_watchlist_status_has_watch():
    assert IntegratedWatchlistStatus.WATCH in IntegratedWatchlistStatus


def test_watchlist_status_has_excluded():
    assert IntegratedWatchlistStatus.EXCLUDED in IntegratedWatchlistStatus


def test_watchlist_status_has_unknown():
    assert IntegratedWatchlistStatus.UNKNOWN in IntegratedWatchlistStatus


# ---------------------------------------------------------------------------
# IntegratedABCStatus — 5 members
# ---------------------------------------------------------------------------

def test_abc_status_has_exactly_5_members():
    assert len(IntegratedABCStatus) == 5


def test_abc_status_has_a_ready():
    assert IntegratedABCStatus.A_READY in IntegratedABCStatus


def test_abc_status_has_b_ready():
    assert IntegratedABCStatus.B_READY in IntegratedABCStatus


def test_abc_status_has_c_ready():
    assert IntegratedABCStatus.C_READY in IntegratedABCStatus


def test_abc_status_has_not_ready():
    assert IntegratedABCStatus.NOT_READY in IntegratedABCStatus


def test_abc_status_has_blocked():
    assert IntegratedABCStatus.BLOCKED in IntegratedABCStatus


# ---------------------------------------------------------------------------
# IntegratedThemeStatus — 6 members
# ---------------------------------------------------------------------------

def test_theme_status_has_exactly_6_members():
    assert len(IntegratedThemeStatus) == 6


def test_theme_status_has_leader():
    assert IntegratedThemeStatus.LEADER in IntegratedThemeStatus


def test_theme_status_has_strong():
    assert IntegratedThemeStatus.STRONG in IntegratedThemeStatus


def test_theme_status_has_watch():
    assert IntegratedThemeStatus.WATCH in IntegratedThemeStatus


def test_theme_status_has_weak():
    assert IntegratedThemeStatus.WEAK in IntegratedThemeStatus


def test_theme_status_has_excluded():
    assert IntegratedThemeStatus.EXCLUDED in IntegratedThemeStatus


def test_theme_status_has_unknown():
    assert IntegratedThemeStatus.UNKNOWN in IntegratedThemeStatus


# ---------------------------------------------------------------------------
# IntegratedRiskLevel — 4 members
# ---------------------------------------------------------------------------

def test_risk_level_has_exactly_4_members():
    assert len(IntegratedRiskLevel) == 4


def test_risk_level_has_safe():
    assert IntegratedRiskLevel.SAFE in IntegratedRiskLevel


def test_risk_level_has_moderate():
    assert IntegratedRiskLevel.MODERATE in IntegratedRiskLevel


def test_risk_level_has_high():
    assert IntegratedRiskLevel.HIGH in IntegratedRiskLevel


def test_risk_level_has_blocked():
    assert IntegratedRiskLevel.BLOCKED in IntegratedRiskLevel


# ---------------------------------------------------------------------------
# IntegratedBehaviorStatus — 4 members
# ---------------------------------------------------------------------------

def test_behavior_status_has_exactly_4_members():
    assert len(IntegratedBehaviorStatus) == 4


def test_behavior_status_has_clean():
    assert IntegratedBehaviorStatus.CLEAN in IntegratedBehaviorStatus


def test_behavior_status_has_caution():
    assert IntegratedBehaviorStatus.CAUTION in IntegratedBehaviorStatus


def test_behavior_status_has_warning():
    assert IntegratedBehaviorStatus.WARNING in IntegratedBehaviorStatus


def test_behavior_status_has_blocked():
    assert IntegratedBehaviorStatus.BLOCKED in IntegratedBehaviorStatus


# ---------------------------------------------------------------------------
# Each enum member value equals its string name
# ---------------------------------------------------------------------------

def test_decision_action_values_equal_names():
    for member in IntegratedDecisionAction:
        assert member.value == member.name


def test_no_trade_reason_values_equal_names():
    for member in IntegratedNoTradeReasonCode:
        assert member.value == member.name


def test_score_grade_values_equal_names():
    for member in IntegratedScoreGrade:
        assert member.value == member.name


def test_block_reason_values_equal_names():
    for member in IntegratedBlockReason:
        assert member.value == member.name


def test_health_status_values_equal_names():
    for member in IntegratedHealthStatus:
        assert member.value == member.name


def test_regime_status_values_equal_names():
    for member in IntegratedRegimeStatus:
        assert member.value == member.name


def test_watchlist_status_values_equal_names():
    for member in IntegratedWatchlistStatus:
        assert member.value == member.name


def test_abc_status_values_equal_names():
    for member in IntegratedABCStatus:
        assert member.value == member.name


def test_theme_status_values_equal_names():
    for member in IntegratedThemeStatus:
        assert member.value == member.name


def test_risk_level_values_equal_names():
    for member in IntegratedRiskLevel:
        assert member.value == member.name


def test_behavior_status_values_equal_names():
    for member in IntegratedBehaviorStatus:
        assert member.value == member.name


# ---------------------------------------------------------------------------
# Module-level _SCHEMA and _POLICY
# ---------------------------------------------------------------------------

def test_schema_is_178():
    assert _SCHEMA == "178"


def test_policy_is_178_string():
    assert _POLICY == "1.7.8-small-capital-strategy-integration"


def test_decision_action_schema_attribute():
    assert IntegratedDecisionAction._SCHEMA == "178"


def test_decision_action_policy_attribute():
    assert IntegratedDecisionAction._POLICY == "1.7.8-small-capital-strategy-integration"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def test_get_all_enum_names_returns_list():
    result = get_all_enum_names()
    assert isinstance(result, list)


def test_get_all_enum_names_returns_11_items():
    assert len(get_all_enum_names()) == 11


def test_get_all_decision_actions_returns_9_items():
    assert len(get_all_decision_actions()) == 9


def test_get_all_decision_actions_returns_list_of_enum_members():
    result = get_all_decision_actions()
    assert all(isinstance(a, IntegratedDecisionAction) for a in result)


def test_get_all_no_trade_reasons_returns_15_items():
    assert len(get_all_no_trade_reasons()) == 15


def test_get_all_no_trade_reasons_returns_list_of_enum_members():
    result = get_all_no_trade_reasons()
    assert all(isinstance(r, IntegratedNoTradeReasonCode) for r in result)


def test_get_all_no_trade_reasons_has_no_duplicates():
    result = get_all_no_trade_reasons()
    assert len(result) == len(set(result))


def test_get_all_block_reasons_returns_12_items():
    assert len(get_all_block_reasons()) == 12


def test_get_all_block_reasons_returns_list_of_enum_members():
    result = get_all_block_reasons()
    assert all(isinstance(r, IntegratedBlockReason) for r in result)


def test_get_all_enum_names_contains_decision_action():
    assert "IntegratedDecisionAction" in get_all_enum_names()


def test_get_all_enum_names_contains_no_trade_reason_code():
    assert "IntegratedNoTradeReasonCode" in get_all_enum_names()


def test_get_all_enum_names_contains_score_grade():
    assert "IntegratedScoreGrade" in get_all_enum_names()


def test_get_all_enum_names_contains_block_reason():
    assert "IntegratedBlockReason" in get_all_enum_names()


# ---------------------------------------------------------------------------
# score_to_grade — boundary and representative values
# ---------------------------------------------------------------------------

def test_score_to_grade_85_is_excellent():
    assert score_to_grade(85.0) == IntegratedScoreGrade.EXCELLENT


def test_score_to_grade_70_is_good():
    assert score_to_grade(70.0) == IntegratedScoreGrade.GOOD


def test_score_to_grade_55_is_acceptable():
    assert score_to_grade(55.0) == IntegratedScoreGrade.ACCEPTABLE


def test_score_to_grade_40_is_marginal():
    assert score_to_grade(40.0) == IntegratedScoreGrade.MARGINAL


def test_score_to_grade_20_is_blocked():
    assert score_to_grade(20.0) == IntegratedScoreGrade.BLOCKED


def test_score_to_grade_0_is_blocked():
    assert score_to_grade(0.0) == IntegratedScoreGrade.BLOCKED


def test_score_to_grade_100_is_excellent():
    assert score_to_grade(100.0) == IntegratedScoreGrade.EXCELLENT


def test_score_to_grade_80_is_excellent():
    assert score_to_grade(80.0) == IntegratedScoreGrade.EXCELLENT


def test_score_to_grade_65_is_good():
    assert score_to_grade(65.0) == IntegratedScoreGrade.GOOD


def test_score_to_grade_50_is_acceptable():
    assert score_to_grade(50.0) == IntegratedScoreGrade.ACCEPTABLE


def test_score_to_grade_35_is_marginal():
    assert score_to_grade(35.0) == IntegratedScoreGrade.MARGINAL


def test_score_to_grade_79_is_good():
    """79.9 is just below EXCELLENT threshold — should be GOOD."""
    assert score_to_grade(79.9) == IntegratedScoreGrade.GOOD


def test_score_to_grade_64_is_acceptable():
    """64.9 is just below GOOD threshold — should be ACCEPTABLE."""
    assert score_to_grade(64.9) == IntegratedScoreGrade.ACCEPTABLE


def test_score_to_grade_49_is_marginal():
    """49.9 is just below ACCEPTABLE threshold — should be MARGINAL."""
    assert score_to_grade(49.9) == IntegratedScoreGrade.MARGINAL


def test_score_to_grade_34_is_blocked():
    """34.9 is just below MARGINAL threshold — should be BLOCKED."""
    assert score_to_grade(34.9) == IntegratedScoreGrade.BLOCKED


def test_score_to_grade_returns_score_grade_instance():
    result = score_to_grade(75.0)
    assert isinstance(result, IntegratedScoreGrade)


# ---------------------------------------------------------------------------
# Enum member accessibility by name
# ---------------------------------------------------------------------------

def test_decision_action_members_accessible_by_name():
    names = [a.name for a in IntegratedDecisionAction]
    for name in names:
        member = IntegratedDecisionAction[name]
        assert member.name == name


def test_no_trade_reason_members_accessible_by_name():
    names = [r.name for r in IntegratedNoTradeReasonCode]
    for name in names:
        member = IntegratedNoTradeReasonCode[name]
        assert member.name == name


def test_block_reason_members_accessible_by_name():
    names = [r.name for r in IntegratedBlockReason]
    for name in names:
        member = IntegratedBlockReason[name]
        assert member.name == name
