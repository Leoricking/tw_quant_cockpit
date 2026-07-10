"""
tests/test_integrated_strategy_engine_v178.py
Tests for IntegratedStrategyEngine, run_integrated_strategy(),
and build_integrated_dashboard() — v1.7.8.
[!] Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
    IntegratedDecisionAction,
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
    IntegratedStrategyDecision,
    IntegratedDashboard,
    IntegratedWatchlistDecision,
    IntegratedThemeDecision,
    IntegratedABCDecision,
    IntegratedRiskDecision,
    IntegratedBehaviorDecision,
)
from paper_trading.small_capital_strategy.integrated_strategy_engine_v178 import (
    IntegratedStrategyEngine,
    run_integrated_strategy,
    build_integrated_dashboard,
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


def _engine() -> IntegratedStrategyEngine:
    return IntegratedStrategyEngine()


# ===========================================================================
# IntegratedStrategyEngine.run() — 20 tests
# ===========================================================================

def test_engine_run_returns_integrated_strategy_decision():
    decision = _engine().run(_good_input())
    assert isinstance(decision, IntegratedStrategyDecision)


def test_engine_run_paper_only_is_true():
    decision = _engine().run(_good_input())
    assert decision.paper_only is True


def test_engine_run_no_real_orders_is_true():
    decision = _engine().run(_good_input())
    assert decision.no_real_orders is True


def test_engine_run_no_broker_is_true():
    decision = _engine().run(_good_input())
    assert decision.no_broker is True


def test_engine_run_not_investment_advice_is_true():
    decision = _engine().run(_good_input())
    assert decision.not_investment_advice is True


def test_engine_run_action_is_valid_enum_member():
    decision = _engine().run(_good_input())
    assert decision.action in list(IntegratedDecisionAction)


def test_engine_run_final_score_in_valid_range():
    decision = _engine().run(_good_input())
    assert 0.0 <= decision.final_score <= 100.0


def test_engine_run_grade_is_not_none():
    decision = _engine().run(_good_input())
    assert decision.grade is not None


def test_engine_run_no_trade_reasons_is_list():
    decision = _engine().run(_good_input())
    assert isinstance(decision.no_trade_reasons, list)


def test_engine_run_block_reasons_is_list():
    decision = _engine().run(_good_input())
    assert isinstance(decision.block_reasons, list)


def test_engine_run_summary_is_string():
    decision = _engine().run(_good_input())
    assert isinstance(decision.summary, str)


def test_engine_run_no_stop_loss_action_is_blocked():
    inp = _good_input(has_stop_loss=False)
    decision = _engine().run(inp)
    assert decision.action == IntegratedDecisionAction.BLOCKED


def test_engine_run_real_order_requested_action_is_blocked():
    inp = _good_input(real_order_requested=True)
    decision = _engine().run(inp)
    assert decision.action == IntegratedDecisionAction.BLOCKED


def test_engine_run_broker_requested_action_is_blocked():
    inp = _good_input(broker_requested=True)
    decision = _engine().run(inp)
    assert decision.action == IntegratedDecisionAction.BLOCKED


def test_engine_run_margin_requested_action_is_blocked():
    inp = _good_input(margin_requested=True)
    decision = _engine().run(inp)
    assert decision.action == IntegratedDecisionAction.BLOCKED


def test_engine_run_risk_off_no_override_action_is_blocked():
    inp = _good_input(
        regime_status=IntegratedRegimeStatus.RISK_OFF,
        regime_safety_override=False,
    )
    decision = _engine().run(inp)
    assert decision.action == IntegratedDecisionAction.BLOCKED


def test_engine_run_behavior_blocked_action_is_blocked():
    inp = _good_input(behavior_status=IntegratedBehaviorStatus.BLOCKED)
    decision = _engine().run(inp)
    assert decision.action == IntegratedDecisionAction.BLOCKED


def test_engine_run_risk_blocked_action_is_blocked():
    inp = _good_input(risk_level=IntegratedRiskLevel.BLOCKED)
    decision = _engine().run(inp)
    assert decision.action == IntegratedDecisionAction.BLOCKED


def test_engine_run_watchlist_excluded_action_is_blocked():
    inp = _good_input(watchlist_status=IntegratedWatchlistStatus.EXCLUDED)
    decision = _engine().run(inp)
    assert decision.action == IntegratedDecisionAction.BLOCKED


def test_engine_run_theme_excluded_action_is_blocked():
    inp = _good_input(theme_status=IntegratedThemeStatus.EXCLUDED)
    decision = _engine().run(inp)
    assert decision.action == IntegratedDecisionAction.BLOCKED


# ===========================================================================
# IntegratedStrategyEngine.run() — more action checks — 5 tests
# ===========================================================================

def test_engine_run_abc_blocked_action_is_blocked():
    inp = _good_input(abc_status=IntegratedABCStatus.BLOCKED)
    decision = _engine().run(inp)
    assert decision.action == IntegratedDecisionAction.BLOCKED


def test_engine_run_bull_leader_focus_a_ready_good_action_is_entry_or_plan():
    inp = _good_input()
    decision = _engine().run(inp)
    assert decision.action in (
        IntegratedDecisionAction.PAPER_ENTRY_ALLOWED,
        IntegratedDecisionAction.PAPER_PLAN_READY,
    )


def test_engine_run_high_risk_no_blocks_returns_reduce_risk():
    inp = _good_input(risk_level=IntegratedRiskLevel.HIGH)
    decision = _engine().run(inp)
    assert decision.action == IntegratedDecisionAction.REDUCE_RISK


def test_engine_run_symbol_passed_to_decision():
    inp = _good_input(symbol="0050")
    decision = _engine().run(inp)
    assert decision.symbol == "0050"


def test_engine_run_date_passed_to_decision():
    inp = _good_input(date="2026-07-10")
    decision = _engine().run(inp)
    assert decision.date == "2026-07-10"


# ===========================================================================
# IntegratedStrategyEngine.build_context() — 3 tests
# ===========================================================================

def test_engine_build_context_paper_only_is_true():
    ctx = _engine().build_context(_good_input())
    assert ctx.paper_only is True


def test_engine_build_context_all_subsystems_present_when_symbol_and_date_set():
    ctx = _engine().build_context(_good_input())
    assert ctx.all_subsystems_present is True


def test_engine_build_context_not_all_subsystems_present_when_no_symbol():
    inp = _good_input(symbol="")
    ctx = _engine().build_context(inp)
    assert ctx.all_subsystems_present is False


# ===========================================================================
# IntegratedStrategyEngine.build_sub_decisions() — 6 tests
# ===========================================================================

def test_engine_build_sub_decisions_returns_dict_with_expected_keys():
    sub = _engine().build_sub_decisions(_good_input())
    assert set(sub.keys()) == {"watchlist", "theme", "abc", "risk", "behavior"}


def test_engine_build_sub_decisions_watchlist_paper_only_is_true():
    sub = _engine().build_sub_decisions(_good_input())
    assert sub["watchlist"].paper_only is True


def test_engine_build_sub_decisions_theme_paper_only_is_true():
    sub = _engine().build_sub_decisions(_good_input())
    assert sub["theme"].paper_only is True


def test_engine_build_sub_decisions_abc_paper_only_is_true():
    sub = _engine().build_sub_decisions(_good_input())
    assert sub["abc"].paper_only is True


def test_engine_build_sub_decisions_risk_paper_only_is_true():
    sub = _engine().build_sub_decisions(_good_input())
    assert sub["risk"].paper_only is True


def test_engine_build_sub_decisions_behavior_paper_only_is_true():
    sub = _engine().build_sub_decisions(_good_input())
    assert sub["behavior"].paper_only is True


# ===========================================================================
# run_integrated_strategy() convenience function — 4 tests
# ===========================================================================

def test_run_integrated_strategy_paper_only_is_true():
    result = run_integrated_strategy(_good_input())
    assert result.paper_only is True


def test_run_integrated_strategy_no_real_orders_is_true():
    result = run_integrated_strategy(_good_input())
    assert result.no_real_orders is True


def test_run_integrated_strategy_returns_decision():
    result = run_integrated_strategy(_good_input())
    assert isinstance(result, IntegratedStrategyDecision)


def test_run_integrated_strategy_action_in_valid_actions():
    result = run_integrated_strategy(_good_input())
    assert result.action in list(IntegratedDecisionAction)


# ===========================================================================
# build_integrated_dashboard() — 8 tests
# ===========================================================================

def test_build_integrated_dashboard_paper_only_is_true():
    dashboard = build_integrated_dashboard(_good_input())
    assert dashboard.paper_only is True


def test_build_integrated_dashboard_decision_is_not_none():
    dashboard = build_integrated_dashboard(_good_input())
    assert dashboard.decision is not None


def test_build_integrated_dashboard_scorecard_is_not_none():
    dashboard = build_integrated_dashboard(_good_input())
    assert dashboard.scorecard is not None


def test_build_integrated_dashboard_sections_not_none_and_at_least_4():
    dashboard = build_integrated_dashboard(_good_input())
    assert dashboard.sections is not None
    assert len(dashboard.sections) >= 4


def test_build_integrated_dashboard_watchlist_decision_is_not_none():
    dashboard = build_integrated_dashboard(_good_input())
    assert dashboard.watchlist_decision is not None


def test_build_integrated_dashboard_theme_decision_is_not_none():
    dashboard = build_integrated_dashboard(_good_input())
    assert dashboard.theme_decision is not None


def test_build_integrated_dashboard_abc_decision_is_not_none():
    dashboard = build_integrated_dashboard(_good_input())
    assert dashboard.abc_decision is not None


def test_build_integrated_dashboard_risk_decision_is_not_none():
    dashboard = build_integrated_dashboard(_good_input())
    assert dashboard.risk_decision is not None


# ===========================================================================
# Sub-decision types — 4 tests
# ===========================================================================

def test_engine_build_sub_decisions_watchlist_is_correct_type():
    sub = _engine().build_sub_decisions(_good_input())
    assert isinstance(sub["watchlist"], IntegratedWatchlistDecision)


def test_engine_build_sub_decisions_theme_is_correct_type():
    sub = _engine().build_sub_decisions(_good_input())
    assert isinstance(sub["theme"], IntegratedThemeDecision)


def test_engine_build_sub_decisions_abc_is_correct_type():
    sub = _engine().build_sub_decisions(_good_input())
    assert isinstance(sub["abc"], IntegratedABCDecision)


def test_engine_build_sub_decisions_risk_is_correct_type():
    sub = _engine().build_sub_decisions(_good_input())
    assert isinstance(sub["risk"], IntegratedRiskDecision)
