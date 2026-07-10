"""
tests/test_integrated_strategy_paper_plan_v178.py
Tests for build_paper_plan() — Small Capital Strategy Integration v1.7.8.
[!] Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
    IntegratedDecisionAction,
    IntegratedScoreGrade,
    IntegratedRegimeStatus,
    IntegratedWatchlistStatus,
    IntegratedABCStatus,
    IntegratedThemeStatus,
    IntegratedRiskLevel,
    IntegratedBehaviorStatus,
)
from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
    IntegratedStrategyInput,
    IntegratedStrategyDecision,
    IntegratedPaperPlan,
)
from paper_trading.small_capital_strategy.integrated_strategy_paper_plan_v178 import (
    build_paper_plan,
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
        capital_twd=300_000.0,
        top_theme="AI",
    )
    kwargs.update(overrides)
    return IntegratedStrategyInput(**kwargs)


def _entry_allowed_decision(**overrides) -> IntegratedStrategyDecision:
    kwargs = dict(
        symbol="2330",
        date="2026-07-10",
        action=IntegratedDecisionAction.PAPER_ENTRY_ALLOWED,
        final_score=88.0,
        grade=IntegratedScoreGrade.EXCELLENT,
        summary="PAPER_ENTRY_ALLOWED: score=88.0 grade=EXCELLENT",
    )
    kwargs.update(overrides)
    return IntegratedStrategyDecision(**kwargs)


def _blocked_decision(**overrides) -> IntegratedStrategyDecision:
    kwargs = dict(
        symbol="2330",
        date="2026-07-10",
        action=IntegratedDecisionAction.BLOCKED,
        final_score=0.0,
        grade=IntegratedScoreGrade.BLOCKED,
        summary="BLOCKED: NO_STOP_LOSS",
    )
    kwargs.update(overrides)
    return IntegratedStrategyDecision(**kwargs)


# ===========================================================================
# Return type and safety flags — 8 tests
# ===========================================================================

def test_build_paper_plan_returns_integrated_paper_plan():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert isinstance(plan, IntegratedPaperPlan)


def test_build_paper_plan_paper_only_is_true():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert plan.paper_only is True


def test_build_paper_plan_no_real_orders_is_true():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert plan.no_real_orders is True


def test_build_paper_plan_no_broker_is_true():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert plan.no_broker is True


def test_build_paper_plan_broker_execution_enabled_is_false():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert plan.broker_execution_enabled is False


def test_build_paper_plan_not_investment_advice_is_true():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert plan.not_investment_advice is True


def test_build_paper_plan_demo_only_is_true():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert plan.demo_only is True


def test_build_paper_plan_not_for_production_is_true():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert plan.not_for_production is True


# ===========================================================================
# plan_id format — 2 tests
# ===========================================================================

def test_build_paper_plan_plan_id_starts_with_pp178_prefix():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert plan.plan_id.startswith("PP178-")


def test_build_paper_plan_plan_id_contains_symbol():
    plan = build_paper_plan(_good_input(symbol="2330"), _entry_allowed_decision())
    assert "2330" in plan.plan_id


# ===========================================================================
# buy_point_type — 4 tests
# ===========================================================================

def test_build_paper_plan_buy_point_type_is_string():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert isinstance(plan.buy_point_type, str)


def test_build_paper_plan_a_ready_buy_point_type_contains_a_prefix():
    inp = _good_input(abc_status=IntegratedABCStatus.A_READY)
    plan = build_paper_plan(inp, _entry_allowed_decision())
    assert "A:" in plan.buy_point_type


def test_build_paper_plan_b_ready_buy_point_type_contains_b_prefix():
    inp = _good_input(abc_status=IntegratedABCStatus.B_READY)
    plan = build_paper_plan(inp, _entry_allowed_decision())
    assert "B:" in plan.buy_point_type


def test_build_paper_plan_c_ready_buy_point_type_contains_c_prefix():
    inp = _good_input(abc_status=IntegratedABCStatus.C_READY)
    plan = build_paper_plan(inp, _entry_allowed_decision())
    assert "C:" in plan.buy_point_type


# ===========================================================================
# plan_notes content — 3 tests
# ===========================================================================

def test_build_paper_plan_notes_contain_paper_only():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert "PAPER ONLY" in plan.plan_notes


def test_build_paper_plan_notes_contain_no_real_orders():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert "NO REAL ORDERS" in plan.plan_notes


def test_build_paper_plan_notes_contain_regime():
    inp = _good_input(regime_status=IntegratedRegimeStatus.BULL)
    plan = build_paper_plan(inp, _entry_allowed_decision())
    assert "BULL" in plan.plan_notes


# ===========================================================================
# plan_valid conditions — 6 tests
# ===========================================================================

def test_build_paper_plan_plan_valid_true_when_entry_allowed_has_stop():
    inp = _good_input(has_stop_loss=True)
    decision = _entry_allowed_decision(action=IntegratedDecisionAction.PAPER_ENTRY_ALLOWED)
    plan = build_paper_plan(inp, decision)
    assert plan.plan_valid is True


def test_build_paper_plan_plan_valid_false_when_no_stop_loss():
    inp = _good_input(has_stop_loss=False)
    decision = _blocked_decision()
    plan = build_paper_plan(inp, decision)
    assert plan.plan_valid is False


def test_build_paper_plan_plan_valid_false_when_real_order_requested():
    inp = _good_input(real_order_requested=True)
    decision = _blocked_decision(action=IntegratedDecisionAction.BLOCKED)
    plan = build_paper_plan(inp, decision)
    assert plan.plan_valid is False


def test_build_paper_plan_plan_valid_false_when_broker_requested():
    inp = _good_input(broker_requested=True)
    decision = _blocked_decision()
    plan = build_paper_plan(inp, decision)
    assert plan.plan_valid is False


def test_build_paper_plan_plan_valid_false_when_blocked_action():
    inp = _good_input()
    decision = _blocked_decision()
    plan = build_paper_plan(inp, decision)
    assert plan.plan_valid is False


def test_build_paper_plan_plan_valid_true_when_paper_plan_ready_action():
    inp = _good_input(has_stop_loss=True)
    decision = _entry_allowed_decision(action=IntegratedDecisionAction.PAPER_PLAN_READY)
    plan = build_paper_plan(inp, decision)
    assert plan.plan_valid is True


# ===========================================================================
# Risk parameters — 3 tests
# ===========================================================================

def test_build_paper_plan_risk_pct_equals_002():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert plan.risk_pct == 0.02


def test_build_paper_plan_stop_loss_pct_equals_007():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision())
    assert plan.stop_loss_pct == 0.07


def test_build_paper_plan_max_capital_twd_matches_input():
    inp = _good_input(capital_twd=300_000.0)
    plan = build_paper_plan(inp, _entry_allowed_decision())
    assert plan.max_capital_twd == 300_000.0


# ===========================================================================
# Price fields when no reference price — 2 tests
# ===========================================================================

def test_build_paper_plan_stop_loss_price_zero_when_no_reference_price():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision(), reference_price=0.0)
    assert plan.stop_loss_price == 0.0


def test_build_paper_plan_entry_price_range_low_zero_when_no_reference_price():
    plan = build_paper_plan(_good_input(), _entry_allowed_decision(), reference_price=0.0)
    assert plan.entry_price_range_low == 0.0


# ===========================================================================
# plan_notes content checks for score and grade — 2 tests
# ===========================================================================

def test_build_paper_plan_notes_contain_score():
    decision = _entry_allowed_decision(final_score=88.0)
    plan = build_paper_plan(_good_input(), decision)
    assert "88.0" in plan.plan_notes


def test_build_paper_plan_notes_contain_grade():
    decision = _entry_allowed_decision(grade=IntegratedScoreGrade.EXCELLENT)
    plan = build_paper_plan(_good_input(), decision)
    assert "EXCELLENT" in plan.plan_notes
