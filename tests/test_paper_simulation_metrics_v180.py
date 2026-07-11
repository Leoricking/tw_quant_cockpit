"""tests/test_paper_simulation_metrics_v180.py — v1.8.0 Paper Simulation metrics tests"""
from __future__ import annotations

import pytest

from paper_trading.small_capital_strategy.paper_simulation_metrics_v180 import (
    compute_metrics,
    compute_equity_curve,
    compute_drawdown_report,
    compute_risk_report,
    compute_regime_performance,
    compute_theme_performance,
    compute_abc_performance,
    compute_mistake_impact,
    get_metrics_info,
    VALID_GRADES,
)
from paper_trading.small_capital_strategy.paper_simulation_models_v180 import (
    PaperSimulationInput,
    PaperSimulationTrade,
    PaperPerformanceMetrics,
    PaperEquityCurve,
    PaperDrawdownReport,
    PaperRiskReport,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _make_trade(
    pnl: float = 100.0,
    pnl_pct: float = 0.5,
    r_multiple: float = 1.0,
    abc_type: str = "A",
    theme: str = "LEADER",
    regime: str = "BULL",
    mistake_type: str = "none",
) -> PaperSimulationTrade:
    return PaperSimulationTrade(
        trade_id="T001",
        symbol="SIM",
        entry_price=100.0,
        exit_price=101.0,
        stop_loss=99.0,
        position_size=10.0,
        pnl=pnl,
        pnl_pct=pnl_pct,
        r_multiple=r_multiple,
        abc_type=abc_type,
        theme=theme,
        regime=regime,
        mistake_type=mistake_type,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        no_broker=True,
        not_investment_advice=True,
    )


# ---------------------------------------------------------------------------
# VALID_GRADES tests
# ---------------------------------------------------------------------------

def test_valid_grades_contains_a() -> None:
    assert "A" in VALID_GRADES


def test_valid_grades_contains_b() -> None:
    assert "B" in VALID_GRADES


def test_valid_grades_contains_c() -> None:
    assert "C" in VALID_GRADES


def test_valid_grades_contains_d() -> None:
    assert "D" in VALID_GRADES


def test_valid_grades_contains_blocked() -> None:
    assert "BLOCKED" in VALID_GRADES


def test_valid_grades_count_is_five() -> None:
    assert len(VALID_GRADES) == 5


# ---------------------------------------------------------------------------
# compute_metrics — empty trade list
# ---------------------------------------------------------------------------

def test_compute_metrics_empty_returns_metrics_type() -> None:
    result = compute_metrics([])
    assert isinstance(result, PaperPerformanceMetrics)


def test_compute_metrics_empty_trade_count_zero() -> None:
    result = compute_metrics([])
    assert result.trade_count == 0


def test_compute_metrics_empty_paper_only_true() -> None:
    result = compute_metrics([])
    assert result.paper_only is True


def test_compute_metrics_is_blocked_sets_blocked_grade() -> None:
    result = compute_metrics([], is_blocked=True)
    assert result.final_grade == "BLOCKED"


def test_compute_metrics_empty_not_blocked_grade_is_d() -> None:
    result = compute_metrics([])
    assert result.final_grade == "D"


# ---------------------------------------------------------------------------
# compute_metrics — with trades
# ---------------------------------------------------------------------------

def test_compute_metrics_two_trades_count() -> None:
    trades = [_make_trade(100, 1.0, 2.0), _make_trade(-50, -0.5, -1.0)]
    result = compute_metrics(trades)
    assert result.trade_count == 2


def test_compute_metrics_all_wins_win_rate_100() -> None:
    trades = [_make_trade(100), _make_trade(200), _make_trade(50)]
    result = compute_metrics(trades)
    assert result.win_rate_pct == 100.0


def test_compute_metrics_all_losses_win_rate_0() -> None:
    trades = [_make_trade(-100), _make_trade(-200)]
    result = compute_metrics(trades)
    assert result.win_rate_pct == 0.0


def test_compute_metrics_mixed_win_rate_between_0_and_100() -> None:
    trades = [_make_trade(100), _make_trade(-50)]
    result = compute_metrics(trades)
    assert 0.0 < result.win_rate_pct < 100.0


def test_compute_metrics_profit_factor_wins_only_positive() -> None:
    trades = [_make_trade(100), _make_trade(200)]
    result = compute_metrics(trades)
    assert result.profit_factor > 0


def test_compute_metrics_expectancy_r_is_float() -> None:
    trades = [_make_trade(100, 1.0, 2.0), _make_trade(-50, -0.5, -1.0)]
    result = compute_metrics(trades)
    assert isinstance(result.expectancy_r, float)


def test_compute_metrics_annualized_return_pct_is_float() -> None:
    trades = [_make_trade(100)]
    result = compute_metrics(trades)
    assert isinstance(result.annualized_return_pct, float)


def test_compute_metrics_10_wins_3_losses_grade_in_valid_grades() -> None:
    wins = [_make_trade(300, 3.0, 3.0) for _ in range(10)]
    losses = [_make_trade(-100, -1.0, -1.0) for _ in range(3)]
    result = compute_metrics(wins + losses)
    assert result.final_grade in VALID_GRADES


def test_compute_metrics_behavior_penalty_clean_trades_is_zero() -> None:
    trades = [_make_trade(100, mistake_type="none") for _ in range(5)]
    result = compute_metrics(trades)
    assert result.behavior_penalty_score == 0.0


def test_compute_metrics_overtrading_raises_behavior_penalty() -> None:
    trades = [_make_trade(100, mistake_type="overtrading") for _ in range(6)]
    result = compute_metrics(trades)
    assert result.behavior_penalty_score > 0.0


def test_compute_metrics_single_win_max_consecutive_wins_1() -> None:
    result = compute_metrics([_make_trade(100)])
    assert result.max_consecutive_wins == 1


def test_compute_metrics_single_loss_max_consecutive_losses_1() -> None:
    result = compute_metrics([_make_trade(-100)])
    assert result.max_consecutive_losses == 1


def test_compute_metrics_exposure_pct_nonnegative() -> None:
    trades = [_make_trade(100) for _ in range(5)]
    result = compute_metrics(trades)
    assert result.exposure_pct >= 0.0


def test_compute_metrics_cash_drag_plus_exposure_approx_100() -> None:
    trades = [_make_trade(100) for _ in range(5)]
    result = compute_metrics(trades)
    assert abs(result.cash_drag_pct + result.exposure_pct - 100.0) < 0.01


def test_compute_metrics_schema_version_180() -> None:
    result = compute_metrics([])
    assert result.schema_version == "180"


def test_compute_metrics_no_real_orders_true() -> None:
    result = compute_metrics([])
    assert result.no_real_orders is True


def test_compute_metrics_not_investment_advice_true() -> None:
    result = compute_metrics([])
    assert result.not_investment_advice is True


# ---------------------------------------------------------------------------
# compute_equity_curve
# ---------------------------------------------------------------------------

def test_compute_equity_curve_empty_returns_type() -> None:
    result = compute_equity_curve([])
    assert isinstance(result, PaperEquityCurve)


def test_compute_equity_curve_empty_has_one_value() -> None:
    result = compute_equity_curve([])
    assert len(result.values) == 1


def test_compute_equity_curve_empty_initial_capital_300k() -> None:
    result = compute_equity_curve([])
    assert result.values[0] == 300000.0


def test_compute_equity_curve_one_win_last_value_correct() -> None:
    result = compute_equity_curve([_make_trade(100)])
    assert result.values[-1] == 300100.0


def test_compute_equity_curve_one_loss_last_value_correct() -> None:
    result = compute_equity_curve([_make_trade(-50)])
    assert result.values[-1] == 299950.0


def test_compute_equity_curve_paper_only_true() -> None:
    result = compute_equity_curve([])
    assert result.paper_only is True


def test_compute_equity_curve_drawdowns_list() -> None:
    result = compute_equity_curve([_make_trade(100)])
    assert isinstance(result.drawdowns, list)


def test_compute_equity_curve_dates_length_matches_values() -> None:
    trades = [_make_trade(100), _make_trade(-50)]
    result = compute_equity_curve(trades)
    assert len(result.dates) == len(result.values)


def test_compute_equity_curve_drawdown_at_peak_is_zero() -> None:
    result = compute_equity_curve([_make_trade(100)])
    assert result.drawdowns[0] == 0.0


# ---------------------------------------------------------------------------
# compute_drawdown_report
# ---------------------------------------------------------------------------

def test_compute_drawdown_report_empty_curve_zero_drawdown() -> None:
    curve = compute_equity_curve([])
    report = compute_drawdown_report(curve)
    assert report.max_drawdown_pct == 0.0


def test_compute_drawdown_report_no_drawdown_returns_zero() -> None:
    trades = [_make_trade(100), _make_trade(200)]
    curve = compute_equity_curve(trades)
    report = compute_drawdown_report(curve)
    assert report.max_drawdown_pct == 0.0


def test_compute_drawdown_report_returns_type() -> None:
    curve = compute_equity_curve([])
    report = compute_drawdown_report(curve)
    assert isinstance(report, PaperDrawdownReport)


def test_compute_drawdown_report_with_loss_has_drawdown() -> None:
    trades = [_make_trade(100), _make_trade(-200)]
    curve = compute_equity_curve(trades)
    report = compute_drawdown_report(curve)
    assert report.max_drawdown_pct > 0.0


def test_compute_drawdown_report_paper_only_true() -> None:
    curve = compute_equity_curve([])
    report = compute_drawdown_report(curve)
    assert report.paper_only is True


# ---------------------------------------------------------------------------
# compute_risk_report
# ---------------------------------------------------------------------------

def test_compute_risk_report_returns_risk_report_type() -> None:
    inp = PaperSimulationInput()
    metrics = compute_metrics([])
    report = compute_risk_report(inp, metrics)
    assert isinstance(report, PaperRiskReport)


def test_compute_risk_report_status_in_known_values() -> None:
    inp = PaperSimulationInput()
    metrics = compute_metrics([])
    report = compute_risk_report(inp, metrics)
    assert report.risk_status in ("PASS", "WARNING", "BLOCKED")


def test_compute_risk_report_default_input_passes() -> None:
    inp = PaperSimulationInput()
    metrics = compute_metrics([])
    report = compute_risk_report(inp, metrics)
    assert report.risk_status == "PASS"


def test_compute_risk_report_paper_only_true() -> None:
    inp = PaperSimulationInput()
    metrics = compute_metrics([])
    report = compute_risk_report(inp, metrics)
    assert report.paper_only is True


# ---------------------------------------------------------------------------
# compute_regime_performance
# ---------------------------------------------------------------------------

def test_compute_regime_performance_empty_returns_empty_list() -> None:
    result = compute_regime_performance([])
    assert result == []


def test_compute_regime_performance_one_bull_trade_has_one_entry() -> None:
    result = compute_regime_performance([_make_trade(regime="BULL")])
    assert len(result) == 1


def test_compute_regime_performance_regime_name_correct() -> None:
    result = compute_regime_performance([_make_trade(regime="BULL")])
    assert result[0].regime == "BULL"


def test_compute_regime_performance_two_regimes_two_entries() -> None:
    trades = [_make_trade(regime="BULL"), _make_trade(regime="BEAR")]
    result = compute_regime_performance(trades)
    regimes = {r.regime for r in result}
    assert "BULL" in regimes and "BEAR" in regimes


def test_compute_regime_performance_win_rate_all_wins() -> None:
    trades = [_make_trade(100, regime="BULL"), _make_trade(200, regime="BULL")]
    result = compute_regime_performance(trades)
    assert result[0].win_rate_pct == 100.0


# ---------------------------------------------------------------------------
# compute_theme_performance
# ---------------------------------------------------------------------------

def test_compute_theme_performance_empty_returns_empty_list() -> None:
    result = compute_theme_performance([])
    assert result == []


def test_compute_theme_performance_one_trade_has_one_entry() -> None:
    result = compute_theme_performance([_make_trade(theme="LEADER")])
    assert len(result) == 1


def test_compute_theme_performance_theme_name_correct() -> None:
    result = compute_theme_performance([_make_trade(theme="LEADER")])
    assert result[0].theme == "LEADER"


# ---------------------------------------------------------------------------
# compute_abc_performance
# ---------------------------------------------------------------------------

def test_compute_abc_performance_empty_returns_empty_list() -> None:
    result = compute_abc_performance([])
    assert result == []


def test_compute_abc_performance_one_trade_has_one_entry() -> None:
    result = compute_abc_performance([_make_trade(abc_type="A")])
    assert len(result) == 1


def test_compute_abc_performance_abc_type_correct() -> None:
    result = compute_abc_performance([_make_trade(abc_type="A")])
    assert result[0].abc_type == "A"


def test_compute_abc_performance_three_types_three_entries() -> None:
    trades = [_make_trade(abc_type="A"), _make_trade(abc_type="B"), _make_trade(abc_type="C")]
    result = compute_abc_performance(trades)
    abc_types = {r.abc_type for r in result}
    assert abc_types == {"A", "B", "C"}


# ---------------------------------------------------------------------------
# compute_mistake_impact
# ---------------------------------------------------------------------------

def test_compute_mistake_impact_empty_returns_empty_list() -> None:
    result = compute_mistake_impact([])
    assert result == []


def test_compute_mistake_impact_none_mistake_has_one_entry() -> None:
    result = compute_mistake_impact([_make_trade(mistake_type="none")])
    assert len(result) == 1


def test_compute_mistake_impact_none_mistake_type_correct() -> None:
    result = compute_mistake_impact([_make_trade(mistake_type="none")])
    assert result[0].mistake_type == "none"


def test_compute_mistake_impact_overtrading_behavior_penalty_positive() -> None:
    result = compute_mistake_impact([_make_trade(mistake_type="overtrading")])
    assert result[0].behavior_penalty > 0


def test_compute_mistake_impact_none_behavior_penalty_zero() -> None:
    result = compute_mistake_impact([_make_trade(mistake_type="none")])
    assert result[0].behavior_penalty == 0.0


def test_compute_mistake_impact_no_stop_loss_highest_penalty() -> None:
    result_no_stop = compute_mistake_impact([_make_trade(mistake_type="no_stop_loss")])
    result_overtrading = compute_mistake_impact([_make_trade(mistake_type="overtrading")])
    assert result_no_stop[0].behavior_penalty > result_overtrading[0].behavior_penalty


# ---------------------------------------------------------------------------
# get_metrics_info
# ---------------------------------------------------------------------------

def test_get_metrics_info_returns_dict() -> None:
    assert isinstance(get_metrics_info(), dict)


def test_get_metrics_info_paper_only_true() -> None:
    assert get_metrics_info()["paper_only"] is True


def test_get_metrics_info_no_real_orders_true() -> None:
    assert get_metrics_info()["no_real_orders"] is True


def test_get_metrics_info_valid_grades_present() -> None:
    info = get_metrics_info()
    assert "valid_grades" in info


def test_get_metrics_info_schema_present() -> None:
    info = get_metrics_info()
    assert "schema" in info
