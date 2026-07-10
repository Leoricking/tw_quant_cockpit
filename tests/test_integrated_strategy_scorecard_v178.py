"""
tests/test_integrated_strategy_scorecard_v178.py
Tests for compute_scorecard() — Small Capital Strategy Integration v1.7.8.
[!] Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
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
from paper_trading.small_capital_strategy.integrated_strategy_scorecard_v178 import (
    compute_scorecard,
)

# ---------------------------------------------------------------------------
# Safety invariants
# ---------------------------------------------------------------------------
paper_only = True
no_real_orders = True
no_broker = True
not_investment_advice = True


# ---------------------------------------------------------------------------
# Helper
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


# ---------------------------------------------------------------------------
# Tests 1–5: Return type and basic structure
# ---------------------------------------------------------------------------
def test_compute_scorecard_returns_integrated_scorecard():
    inp = _good_input()
    result = compute_scorecard(inp)
    assert isinstance(result, IntegratedScorecard)


def test_compute_scorecard_paper_only_flag_is_true():
    inp = _good_input()
    result = compute_scorecard(inp)
    assert result.paper_only is True


def test_compute_scorecard_no_real_orders_flag_is_true():
    inp = _good_input()
    result = compute_scorecard(inp)
    assert result.no_real_orders is True


def test_compute_scorecard_no_broker_flag_is_true():
    inp = _good_input()
    result = compute_scorecard(inp)
    assert result.no_broker is True


def test_compute_scorecard_grade_is_not_none():
    inp = _good_input()
    result = compute_scorecard(inp)
    assert result.grade is not None


# ---------------------------------------------------------------------------
# Tests 6–8: final_score range and grade validity
# ---------------------------------------------------------------------------
def test_compute_scorecard_final_score_in_valid_range():
    inp = _good_input()
    result = compute_scorecard(inp)
    assert 0.0 <= result.final_score <= 100.0


def test_compute_scorecard_grade_is_valid_enum_member():
    inp = _good_input()
    result = compute_scorecard(inp)
    assert result.grade in list(IntegratedScoreGrade)


def test_compute_scorecard_final_score_not_negative():
    inp = IntegratedStrategyInput()
    result = compute_scorecard(inp)
    assert result.final_score >= 0.0


# ---------------------------------------------------------------------------
# Tests 9–10: Subscore passthrough when positive input
# ---------------------------------------------------------------------------
def test_compute_scorecard_theme_score_positive_when_input_is_90():
    inp = _good_input(theme_score=90.0)
    result = compute_scorecard(inp)
    assert result.theme_score > 0.0


def test_compute_scorecard_watchlist_score_positive_when_input_is_90():
    inp = _good_input(watchlist_score=90.0)
    result = compute_scorecard(inp)
    assert result.watchlist_score > 0.0


# ---------------------------------------------------------------------------
# Tests 11–15: Hard overrides force zero
# ---------------------------------------------------------------------------
def test_compute_scorecard_excluded_watchlist_forces_zero():
    inp = _good_input(watchlist_status=IntegratedWatchlistStatus.EXCLUDED, watchlist_score=90.0)
    result = compute_scorecard(inp)
    assert result.watchlist_score == 0.0


def test_compute_scorecard_excluded_theme_forces_zero():
    inp = _good_input(theme_status=IntegratedThemeStatus.EXCLUDED, theme_score=90.0)
    result = compute_scorecard(inp)
    assert result.theme_score == 0.0


def test_compute_scorecard_blocked_risk_forces_zero():
    inp = _good_input(risk_level=IntegratedRiskLevel.BLOCKED, risk_score=90.0)
    result = compute_scorecard(inp)
    assert result.risk_score == 0.0


def test_compute_scorecard_blocked_abc_forces_zero():
    inp = _good_input(abc_status=IntegratedABCStatus.BLOCKED, abc_score=90.0)
    result = compute_scorecard(inp)
    assert result.abc_score == 0.0


def test_compute_scorecard_blocked_behavior_forces_zero():
    inp = _good_input(behavior_status=IntegratedBehaviorStatus.BLOCKED, behavior_score=90.0)
    result = compute_scorecard(inp)
    assert result.behavior_score == 0.0


# ---------------------------------------------------------------------------
# Tests 16–17: RISK_OFF regime cap
# ---------------------------------------------------------------------------
def test_compute_scorecard_risk_off_no_override_caps_regime_score():
    inp = _good_input(
        regime_status=IntegratedRegimeStatus.RISK_OFF,
        regime_score=90.0,
        regime_safety_override=False,
    )
    result = compute_scorecard(inp)
    assert result.regime_score <= 10.0


def test_compute_scorecard_risk_off_with_override_regime_score_not_capped():
    inp = _good_input(
        regime_status=IntegratedRegimeStatus.RISK_OFF,
        regime_score=90.0,
        regime_safety_override=True,
    )
    result = compute_scorecard(inp)
    assert result.regime_score > 10.0


# ---------------------------------------------------------------------------
# Tests 18–20: Grade thresholds for best-case input
# ---------------------------------------------------------------------------
def test_compute_scorecard_bull_leader_focus_a_ready_safe_clean_grade_excellent_or_good():
    inp = _good_input()
    result = compute_scorecard(inp)
    assert result.grade in (IntegratedScoreGrade.EXCELLENT, IntegratedScoreGrade.GOOD)


def test_compute_scorecard_full_90s_final_score_above_80():
    inp = _good_input(
        theme_score=90.0, watchlist_score=90.0, abc_score=90.0,
        regime_score=90.0, risk_score=90.0, behavior_score=90.0,
        journal_quality_score=90.0,
    )
    result = compute_scorecard(inp)
    assert result.final_score > 80.0


def test_compute_scorecard_all_excluded_blocked_final_score_below_10():
    inp = IntegratedStrategyInput(
        symbol="2330",
        date="2026-07-10",
        theme_status=IntegratedThemeStatus.EXCLUDED,
        watchlist_status=IntegratedWatchlistStatus.EXCLUDED,
        abc_status=IntegratedABCStatus.BLOCKED,
        risk_level=IntegratedRiskLevel.BLOCKED,
        behavior_status=IntegratedBehaviorStatus.BLOCKED,
        regime_status=IntegratedRegimeStatus.RISK_OFF,
        regime_safety_override=False,
        theme_score=90.0,
        watchlist_score=90.0,
        abc_score=90.0,
        risk_score=90.0,
        behavior_score=90.0,
        regime_score=90.0,
        journal_quality_score=0.0,
    )
    result = compute_scorecard(inp)
    assert result.final_score < 10.0


# ---------------------------------------------------------------------------
# Tests 21–22: Score rounding
# ---------------------------------------------------------------------------
def test_compute_scorecard_final_score_is_rounded_to_two_decimal_places():
    inp = _good_input(
        theme_score=73.333,
        watchlist_score=66.667,
        abc_score=81.111,
        regime_score=55.555,
        risk_score=44.444,
        behavior_score=33.333,
        journal_quality_score=22.222,
    )
    result = compute_scorecard(inp)
    # If rounded, the string representation should have at most 2 decimal places
    as_str = str(result.final_score)
    decimal_part = as_str.split(".")[-1] if "." in as_str else ""
    assert len(decimal_part) <= 2


def test_compute_scorecard_subscore_rounded_to_two_decimal_places():
    inp = _good_input(theme_score=88.888)
    result = compute_scorecard(inp)
    as_str = str(result.theme_score)
    decimal_part = as_str.split(".")[-1] if "." in as_str else ""
    assert len(decimal_part) <= 2


# ---------------------------------------------------------------------------
# Tests 23–24: Weighted average sanity
# ---------------------------------------------------------------------------
def test_compute_scorecard_final_score_is_weighted_average_of_subscores():
    """
    Weights: theme=0.20, watchlist=0.15, abc=0.20, regime=0.15,
             risk=0.15, behavior=0.10, journal=0.05.
    All inputs 80.0 → final_score should be ~80.0.
    """
    inp = _good_input(
        theme_score=80.0, watchlist_score=80.0, abc_score=80.0,
        regime_score=80.0, risk_score=80.0, behavior_score=80.0,
        journal_quality_score=80.0,
    )
    result = compute_scorecard(inp)
    assert abs(result.final_score - 80.0) < 1.0


def test_compute_scorecard_higher_theme_and_abc_raises_score():
    low_inp = _good_input(
        theme_score=40.0, watchlist_score=40.0, abc_score=40.0,
        regime_score=40.0, risk_score=40.0, behavior_score=40.0,
        journal_quality_score=40.0,
    )
    high_inp = _good_input(
        theme_score=90.0, watchlist_score=90.0, abc_score=90.0,
        regime_score=90.0, risk_score=90.0, behavior_score=90.0,
        journal_quality_score=90.0,
    )
    low_result = compute_scorecard(low_inp)
    high_result = compute_scorecard(high_inp)
    assert high_result.final_score > low_result.final_score


# ---------------------------------------------------------------------------
# Tests 25–28: Regime-based score ranges
# ---------------------------------------------------------------------------
def test_compute_scorecard_bull_regime_score_above_50():
    inp = IntegratedStrategyInput(
        regime_status=IntegratedRegimeStatus.BULL,
        regime_score=0.0,  # force derivation from status
    )
    result = compute_scorecard(inp)
    assert result.regime_score > 50.0


def test_compute_scorecard_bear_regime_score_below_20():
    inp = IntegratedStrategyInput(
        regime_status=IntegratedRegimeStatus.BEAR,
        regime_score=0.0,
    )
    result = compute_scorecard(inp)
    assert result.regime_score < 20.0


def test_compute_scorecard_unknown_regime_score_below_30():
    inp = IntegratedStrategyInput(
        regime_status=IntegratedRegimeStatus.UNKNOWN,
        regime_score=0.0,
    )
    result = compute_scorecard(inp)
    assert result.regime_score < 30.0


def test_compute_scorecard_bull_soft_regime_score_between_50_and_80():
    inp = IntegratedStrategyInput(
        regime_status=IntegratedRegimeStatus.BULL_SOFT,
        regime_score=0.0,
    )
    result = compute_scorecard(inp)
    assert 50.0 <= result.regime_score <= 80.0


# ---------------------------------------------------------------------------
# Tests 29–31: Watchlist-based score ranges
# ---------------------------------------------------------------------------
def test_compute_scorecard_focus_watchlist_score_above_50():
    inp = IntegratedStrategyInput(
        watchlist_status=IntegratedWatchlistStatus.FOCUS,
        watchlist_score=0.0,
    )
    result = compute_scorecard(inp)
    assert result.watchlist_score > 50.0


def test_compute_scorecard_unknown_watchlist_score_below_30():
    inp = IntegratedStrategyInput(
        watchlist_status=IntegratedWatchlistStatus.UNKNOWN,
        watchlist_score=0.0,
    )
    result = compute_scorecard(inp)
    assert result.watchlist_score < 30.0


def test_compute_scorecard_watch_status_watchlist_score_between_40_and_80():
    inp = IntegratedStrategyInput(
        watchlist_status=IntegratedWatchlistStatus.WATCH,
        watchlist_score=0.0,
    )
    result = compute_scorecard(inp)
    assert 40.0 <= result.watchlist_score <= 80.0


# ---------------------------------------------------------------------------
# Tests 32–34: ABC-based score ranges
# ---------------------------------------------------------------------------
def test_compute_scorecard_a_ready_abc_score_above_80():
    inp = IntegratedStrategyInput(
        abc_status=IntegratedABCStatus.A_READY,
        abc_score=0.0,
    )
    result = compute_scorecard(inp)
    assert result.abc_score > 80.0


def test_compute_scorecard_not_ready_abc_score_below_30():
    inp = IntegratedStrategyInput(
        abc_status=IntegratedABCStatus.NOT_READY,
        abc_score=0.0,
    )
    result = compute_scorecard(inp)
    assert result.abc_score < 30.0


def test_compute_scorecard_b_ready_abc_score_above_80():
    inp = IntegratedStrategyInput(
        abc_status=IntegratedABCStatus.B_READY,
        abc_score=0.0,
    )
    result = compute_scorecard(inp)
    assert result.abc_score > 80.0


# ---------------------------------------------------------------------------
# Tests 35–37: Theme-based score ranges
# ---------------------------------------------------------------------------
def test_compute_scorecard_leader_theme_score_above_80():
    inp = IntegratedStrategyInput(
        theme_status=IntegratedThemeStatus.LEADER,
        theme_score=0.0,
    )
    result = compute_scorecard(inp)
    assert result.theme_score > 80.0


def test_compute_scorecard_weak_theme_score_below_30():
    inp = IntegratedStrategyInput(
        theme_status=IntegratedThemeStatus.WEAK,
        theme_score=0.0,
    )
    result = compute_scorecard(inp)
    assert result.theme_score < 30.0


def test_compute_scorecard_strong_theme_score_between_60_and_90():
    inp = IntegratedStrategyInput(
        theme_status=IntegratedThemeStatus.STRONG,
        theme_score=0.0,
    )
    result = compute_scorecard(inp)
    assert 60.0 <= result.theme_score <= 90.0


# ---------------------------------------------------------------------------
# Tests 38–40: Default input and symbol/date passthrough
# ---------------------------------------------------------------------------
def test_compute_scorecard_default_input_does_not_crash():
    inp = IntegratedStrategyInput()
    result = compute_scorecard(inp)
    assert isinstance(result, IntegratedScorecard)


def test_compute_scorecard_symbol_passed_through_to_scorecard():
    inp = _good_input(symbol="0050")
    result = compute_scorecard(inp)
    assert result.symbol == "0050"


def test_compute_scorecard_date_passed_through_to_scorecard():
    inp = _good_input(date="2026-07-10")
    result = compute_scorecard(inp)
    assert result.date == "2026-07-10"
