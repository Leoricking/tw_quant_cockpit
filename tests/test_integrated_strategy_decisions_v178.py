"""
tests/test_integrated_strategy_decisions_v178.py
Tests for check_hard_blocks(), collect_no_trade_reasons(),
determine_action(), build_decision_summary() — v1.7.8.
[!] Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
    IntegratedDecisionAction,
    IntegratedNoTradeReasonCode,
    IntegratedBlockReason,
    IntegratedRegimeStatus,
    IntegratedWatchlistStatus,
    IntegratedABCStatus,
    IntegratedThemeStatus,
    IntegratedRiskLevel,
    IntegratedBehaviorStatus,
    IntegratedScoreGrade,
)
from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
    IntegratedStrategyInput,
    IntegratedScorecard,
)
from paper_trading.small_capital_strategy.integrated_strategy_decisions_v178 import (
    check_hard_blocks,
    collect_no_trade_reasons,
    determine_action,
    build_decision_summary,
)

# ---------------------------------------------------------------------------
# Safety invariants
# ---------------------------------------------------------------------------
paper_only = True
no_real_orders = True
no_broker = True
not_investment_advice = True


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _good_input(**overrides) -> IntegratedStrategyInput:
    kwargs = dict(
        symbol="2330",
        date="2026-07-10",
        has_stop_loss=True,
        regime_status=IntegratedRegimeStatus.BULL,
        theme_status=IntegratedThemeStatus.LEADER,
        watchlist_status=IntegratedWatchlistStatus.FOCUS,
        abc_status=IntegratedABCStatus.A_READY,
        risk_level=IntegratedRiskLevel.SAFE,
        behavior_status=IntegratedBehaviorStatus.CLEAN,
        theme_score=90.0,
        watchlist_score=90.0,
        abc_score=90.0,
        regime_score=90.0,
        risk_score=90.0,
        behavior_score=90.0,
        journal_quality_score=80.0,
    )
    kwargs.update(overrides)
    return IntegratedStrategyInput(**kwargs)


def _make_scorecard(
    final_score: float = 80.0,
    grade: IntegratedScoreGrade = IntegratedScoreGrade.EXCELLENT,
) -> IntegratedScorecard:
    return IntegratedScorecard(
        symbol="2330",
        date="2026-07-10",
        final_score=final_score,
        grade=grade,
        theme_score=final_score,
        watchlist_score=final_score,
        abc_score=final_score,
        regime_score=final_score,
        risk_score=final_score,
        behavior_score=final_score,
        journal_quality_score=final_score,
    )


# ===========================================================================
# check_hard_blocks — 14 tests
# ===========================================================================

def test_check_hard_blocks_no_stop_loss_adds_no_stop_loss():
    inp = _good_input(has_stop_loss=False)
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.NO_STOP_LOSS in blocks


def test_check_hard_blocks_real_order_requested_adds_real_order_requested():
    inp = _good_input(real_order_requested=True)
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.REAL_ORDER_REQUESTED in blocks


def test_check_hard_blocks_broker_requested_adds_broker_requested():
    inp = _good_input(broker_requested=True)
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.BROKER_REQUESTED in blocks


def test_check_hard_blocks_margin_requested_adds_margin_requested():
    inp = _good_input(margin_requested=True)
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.MARGIN_REQUESTED in blocks


def test_check_hard_blocks_risk_off_no_override_adds_regime_risk_off():
    inp = _good_input(
        regime_status=IntegratedRegimeStatus.RISK_OFF,
        regime_safety_override=False,
    )
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.REGIME_RISK_OFF in blocks


def test_check_hard_blocks_risk_off_with_override_does_not_add_regime_risk_off():
    inp = _good_input(
        regime_status=IntegratedRegimeStatus.RISK_OFF,
        regime_safety_override=True,
    )
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.REGIME_RISK_OFF not in blocks


def test_check_hard_blocks_behavior_blocked_adds_behavior_blocked():
    inp = _good_input(behavior_status=IntegratedBehaviorStatus.BLOCKED)
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.BEHAVIOR_BLOCKED in blocks


def test_check_hard_blocks_risk_blocked_adds_risk_blocked():
    inp = _good_input(risk_level=IntegratedRiskLevel.BLOCKED)
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.RISK_BLOCKED in blocks


def test_check_hard_blocks_watchlist_excluded_adds_watchlist_excluded():
    inp = _good_input(watchlist_status=IntegratedWatchlistStatus.EXCLUDED)
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.WATCHLIST_EXCLUDED in blocks


def test_check_hard_blocks_theme_excluded_adds_theme_excluded():
    inp = _good_input(theme_status=IntegratedThemeStatus.EXCLUDED)
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.THEME_EXCLUDED in blocks


def test_check_hard_blocks_abc_blocked_adds_abc_blocked():
    inp = _good_input(abc_status=IntegratedABCStatus.BLOCKED)
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.ABC_BLOCKED in blocks


def test_check_hard_blocks_empty_source_lineage_adds_lineage_missing():
    inp = _good_input(source_lineage="")
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.LINEAGE_MISSING in blocks


def test_check_hard_blocks_production_db_write_adds_production_write_attempted():
    inp = _good_input(production_db_write_attempted=True)
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.PRODUCTION_WRITE_ATTEMPTED in blocks


def test_check_hard_blocks_good_input_returns_empty_list():
    inp = _good_input()
    blocks = check_hard_blocks(inp)
    assert blocks == []


# ===========================================================================
# collect_no_trade_reasons — 16 tests
# ===========================================================================

def test_collect_no_trade_reasons_risk_off_regime_adds_market_risk_off():
    inp = _good_input(regime_status=IntegratedRegimeStatus.RISK_OFF)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.MARKET_RISK_OFF in reasons


def test_collect_no_trade_reasons_bear_regime_adds_market_risk_off():
    inp = _good_input(regime_status=IntegratedRegimeStatus.BEAR)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.MARKET_RISK_OFF in reasons


def test_collect_no_trade_reasons_weak_theme_adds_theme_weak():
    inp = _good_input(theme_status=IntegratedThemeStatus.WEAK)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.THEME_WEAK in reasons


def test_collect_no_trade_reasons_excluded_watchlist_adds_watchlist_excluded():
    inp = _good_input(watchlist_status=IntegratedWatchlistStatus.EXCLUDED)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.WATCHLIST_EXCLUDED in reasons


def test_collect_no_trade_reasons_not_ready_abc_adds_abc_not_ready():
    inp = _good_input(abc_status=IntegratedABCStatus.NOT_READY)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.ABC_NOT_READY in reasons


def test_collect_no_trade_reasons_high_risk_adds_risk_budget_exceeded():
    inp = _good_input(risk_level=IntegratedRiskLevel.HIGH)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.RISK_BUDGET_EXCEEDED in reasons


def test_collect_no_trade_reasons_no_stop_loss_adds_stop_loss_missing():
    inp = _good_input(has_stop_loss=False)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.STOP_LOSS_MISSING in reasons


def test_collect_no_trade_reasons_warning_behavior_adds_behavior_risk_blocked():
    inp = _good_input(behavior_status=IntegratedBehaviorStatus.WARNING)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.BEHAVIOR_RISK_BLOCKED in reasons


def test_collect_no_trade_reasons_mistake_repeat_detected_adds_mistake_repeat_blocked():
    inp = _good_input(mistake_repeat_detected=True)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.MISTAKE_REPEAT_BLOCKED in reasons


def test_collect_no_trade_reasons_journal_required_low_score_adds_journal_required():
    inp = _good_input(journal_required=True, journal_quality_score=20.0)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.JOURNAL_REQUIRED in reasons


def test_collect_no_trade_reasons_real_order_requested_adds_real_order_blocked():
    inp = _good_input(real_order_requested=True)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.REAL_ORDER_BLOCKED in reasons


def test_collect_no_trade_reasons_broker_requested_adds_broker_blocked():
    inp = _good_input(broker_requested=True)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.BROKER_BLOCKED in reasons


def test_collect_no_trade_reasons_margin_requested_adds_margin_blocked():
    inp = _good_input(margin_requested=True)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.MARGIN_BLOCKED in reasons


def test_collect_no_trade_reasons_no_symbol_adds_data_incomplete():
    inp = _good_input(symbol="")
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.DATA_INCOMPLETE in reasons


def test_collect_no_trade_reasons_empty_lineage_adds_lineage_missing():
    inp = _good_input(source_lineage="")
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.LINEAGE_MISSING in reasons


def test_collect_no_trade_reasons_no_duplicates_in_result():
    inp = _good_input(
        regime_status=IntegratedRegimeStatus.RISK_OFF,
        theme_status=IntegratedThemeStatus.WEAK,
        real_order_requested=True,
    )
    reasons = collect_no_trade_reasons(inp)
    assert len(reasons) == len(set(reasons))


# ===========================================================================
# determine_action — 12 tests
# ===========================================================================

def test_determine_action_with_blocks_returns_blocked():
    sc = _make_scorecard(90.0, IntegratedScoreGrade.EXCELLENT)
    inp = _good_input()
    action = determine_action(sc, [IntegratedBlockReason.NO_STOP_LOSS], [], inp)
    assert action == IntegratedDecisionAction.BLOCKED


def test_determine_action_market_risk_off_reason_returns_no_trade():
    sc = _make_scorecard(80.0, IntegratedScoreGrade.EXCELLENT)
    inp = _good_input()
    action = determine_action(sc, [], [IntegratedNoTradeReasonCode.MARKET_RISK_OFF], inp)
    assert action == IntegratedDecisionAction.NO_TRADE


def test_determine_action_real_order_blocked_reason_returns_no_trade():
    sc = _make_scorecard(80.0, IntegratedScoreGrade.EXCELLENT)
    inp = _good_input()
    action = determine_action(sc, [], [IntegratedNoTradeReasonCode.REAL_ORDER_BLOCKED], inp)
    assert action == IntegratedDecisionAction.NO_TRADE


def test_determine_action_stop_loss_missing_reason_returns_no_trade():
    sc = _make_scorecard(80.0, IntegratedScoreGrade.EXCELLENT)
    inp = _good_input()
    action = determine_action(sc, [], [IntegratedNoTradeReasonCode.STOP_LOSS_MISSING], inp)
    assert action == IntegratedDecisionAction.NO_TRADE


def test_determine_action_high_risk_no_blocks_no_critical_returns_reduce_risk():
    sc = _make_scorecard(70.0, IntegratedScoreGrade.GOOD)
    inp = _good_input(risk_level=IntegratedRiskLevel.HIGH)
    action = determine_action(sc, [], [], inp)
    assert action == IntegratedDecisionAction.REDUCE_RISK


def test_determine_action_excellent_score_a_ready_returns_paper_entry_allowed():
    sc = _make_scorecard(85.0, IntegratedScoreGrade.EXCELLENT)
    inp = _good_input(abc_status=IntegratedABCStatus.A_READY)
    action = determine_action(sc, [], [], inp)
    assert action == IntegratedDecisionAction.PAPER_ENTRY_ALLOWED


def test_determine_action_good_score_abc_not_ready_returns_paper_plan_ready():
    sc = _make_scorecard(70.0, IntegratedScoreGrade.GOOD)
    inp = _good_input(abc_status=IntegratedABCStatus.NOT_READY)
    action = determine_action(sc, [], [], inp)
    assert action == IntegratedDecisionAction.PAPER_PLAN_READY


def test_determine_action_acceptable_score_returns_wait():
    sc = _make_scorecard(55.0, IntegratedScoreGrade.ACCEPTABLE)
    inp = _good_input()
    action = determine_action(sc, [], [], inp)
    assert action == IntegratedDecisionAction.WAIT


def test_determine_action_marginal_score_returns_observe():
    sc = _make_scorecard(40.0, IntegratedScoreGrade.MARGINAL)
    inp = _good_input()
    action = determine_action(sc, [], [], inp)
    assert action == IntegratedDecisionAction.OBSERVE


def test_determine_action_caution_behavior_low_score_returns_review_required():
    sc = _make_scorecard(60.0, IntegratedScoreGrade.GOOD)
    inp = _good_input(behavior_status=IntegratedBehaviorStatus.CAUTION)
    action = determine_action(sc, [], [], inp)
    assert action == IntegratedDecisionAction.REVIEW_REQUIRED


def test_determine_action_result_is_integrated_decision_action_member():
    sc = _make_scorecard(80.0, IntegratedScoreGrade.EXCELLENT)
    inp = _good_input()
    action = determine_action(sc, [], [], inp)
    assert action in list(IntegratedDecisionAction)


def test_determine_action_multiple_blocks_still_returns_blocked():
    sc = _make_scorecard(90.0, IntegratedScoreGrade.EXCELLENT)
    inp = _good_input()
    blocks = [
        IntegratedBlockReason.NO_STOP_LOSS,
        IntegratedBlockReason.REAL_ORDER_REQUESTED,
    ]
    action = determine_action(sc, blocks, [], inp)
    assert action == IntegratedDecisionAction.BLOCKED


# ===========================================================================
# build_decision_summary — 10 tests
# ===========================================================================

def test_build_decision_summary_with_blocks_contains_blocked():
    sc = _make_scorecard(80.0, IntegratedScoreGrade.EXCELLENT)
    summary = build_decision_summary(
        IntegratedDecisionAction.BLOCKED,
        sc,
        [IntegratedBlockReason.NO_STOP_LOSS],
        [],
    )
    assert "BLOCKED" in summary


def test_build_decision_summary_with_blocks_contains_block_reason_value():
    sc = _make_scorecard(80.0, IntegratedScoreGrade.EXCELLENT)
    summary = build_decision_summary(
        IntegratedDecisionAction.BLOCKED,
        sc,
        [IntegratedBlockReason.NO_STOP_LOSS],
        [],
    )
    assert "NO_STOP_LOSS" in summary


def test_build_decision_summary_with_no_trade_reasons_contains_action_value():
    sc = _make_scorecard(80.0, IntegratedScoreGrade.EXCELLENT)
    summary = build_decision_summary(
        IntegratedDecisionAction.NO_TRADE,
        sc,
        [],
        [IntegratedNoTradeReasonCode.MARKET_RISK_OFF],
    )
    assert "NO_TRADE" in summary


def test_build_decision_summary_with_no_trade_reason_contains_reason_code():
    sc = _make_scorecard(80.0, IntegratedScoreGrade.EXCELLENT)
    summary = build_decision_summary(
        IntegratedDecisionAction.NO_TRADE,
        sc,
        [],
        [IntegratedNoTradeReasonCode.MARKET_RISK_OFF],
    )
    assert "MARKET_RISK_OFF" in summary


def test_build_decision_summary_empty_blocks_and_reasons_contains_score():
    sc = _make_scorecard(82.0, IntegratedScoreGrade.EXCELLENT)
    summary = build_decision_summary(
        IntegratedDecisionAction.PAPER_ENTRY_ALLOWED,
        sc,
        [],
        [],
    )
    assert "82.0" in summary


def test_build_decision_summary_empty_blocks_and_reasons_contains_grade():
    sc = _make_scorecard(82.0, IntegratedScoreGrade.EXCELLENT)
    summary = build_decision_summary(
        IntegratedDecisionAction.PAPER_ENTRY_ALLOWED,
        sc,
        [],
        [],
    )
    assert "EXCELLENT" in summary


def test_build_decision_summary_returns_string():
    sc = _make_scorecard(80.0, IntegratedScoreGrade.GOOD)
    summary = build_decision_summary(
        IntegratedDecisionAction.PAPER_PLAN_READY,
        sc,
        [],
        [],
    )
    assert isinstance(summary, str)


def test_build_decision_summary_blocks_take_priority_over_reasons():
    sc = _make_scorecard(80.0, IntegratedScoreGrade.EXCELLENT)
    summary = build_decision_summary(
        IntegratedDecisionAction.BLOCKED,
        sc,
        [IntegratedBlockReason.NO_STOP_LOSS],
        [IntegratedNoTradeReasonCode.MARKET_RISK_OFF],
    )
    # Block-driven summary should start with BLOCKED
    assert summary.startswith("BLOCKED")


def test_build_decision_summary_wait_action_reflected_in_output():
    sc = _make_scorecard(55.0, IntegratedScoreGrade.ACCEPTABLE)
    summary = build_decision_summary(
        IntegratedDecisionAction.WAIT,
        sc,
        [],
        [],
    )
    assert "WAIT" in summary


def test_build_decision_summary_observe_action_reflected_in_output():
    sc = _make_scorecard(40.0, IntegratedScoreGrade.MARGINAL)
    summary = build_decision_summary(
        IntegratedDecisionAction.OBSERVE,
        sc,
        [],
        [],
    )
    assert "OBSERVE" in summary


# ===========================================================================
# Additional edge-case tests — 8 tests
# ===========================================================================

def test_check_hard_blocks_returns_list():
    inp = _good_input()
    result = check_hard_blocks(inp)
    assert isinstance(result, list)


def test_collect_no_trade_reasons_returns_list():
    inp = _good_input()
    result = collect_no_trade_reasons(inp)
    assert isinstance(result, list)


def test_collect_no_trade_reasons_good_input_empty_list():
    inp = _good_input()
    reasons = collect_no_trade_reasons(inp)
    assert reasons == []


def test_check_hard_blocks_multiple_violations_all_captured():
    inp = _good_input(
        has_stop_loss=False,
        real_order_requested=True,
        broker_requested=True,
    )
    blocks = check_hard_blocks(inp)
    assert IntegratedBlockReason.NO_STOP_LOSS in blocks
    assert IntegratedBlockReason.REAL_ORDER_REQUESTED in blocks
    assert IntegratedBlockReason.BROKER_REQUESTED in blocks


def test_determine_action_blocks_win_over_excellent_score():
    sc = _make_scorecard(99.0, IntegratedScoreGrade.EXCELLENT)
    inp = _good_input()
    action = determine_action(sc, [IntegratedBlockReason.REAL_ORDER_REQUESTED], [], inp)
    assert action == IntegratedDecisionAction.BLOCKED


def test_collect_no_trade_reasons_unknown_theme_adds_theme_weak():
    inp = _good_input(theme_status=IntegratedThemeStatus.UNKNOWN)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.THEME_WEAK in reasons


def test_collect_no_trade_reasons_excluded_abc_adds_abc_not_ready():
    inp = _good_input(abc_status=IntegratedABCStatus.BLOCKED)
    reasons = collect_no_trade_reasons(inp)
    assert IntegratedNoTradeReasonCode.ABC_NOT_READY in reasons


def test_determine_action_excellent_abc_b_ready_returns_paper_entry_allowed():
    sc = _make_scorecard(85.0, IntegratedScoreGrade.EXCELLENT)
    inp = _good_input(abc_status=IntegratedABCStatus.B_READY)
    action = determine_action(sc, [], [], inp)
    assert action == IntegratedDecisionAction.PAPER_ENTRY_ALLOWED
