"""
tests/test_risk_dashboard_regression_v174.py
Regression tests for risk dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskDashboardScorecardGrade,
)
from paper_trading.small_capital_strategy.single_trade_risk_monitor_v174 import evaluate_single_trade_risk
from paper_trading.small_capital_strategy.portfolio_exposure_monitor_v174 import evaluate_portfolio_exposure
from paper_trading.small_capital_strategy.drawdown_monitor_v174 import evaluate_drawdown
from paper_trading.small_capital_strategy.losing_streak_monitor_v174 import evaluate_losing_streak
from paper_trading.small_capital_strategy.concentration_risk_monitor_v174 import evaluate_concentration_risk
from paper_trading.small_capital_strategy.cash_ratio_risk_monitor_v174 import evaluate_cash_ratio
from paper_trading.small_capital_strategy.stop_loss_coverage_monitor_v174 import evaluate_stop_loss_coverage
from paper_trading.small_capital_strategy.small_capital_risk_adapter_v174 import (
    build_risk_dashboard, get_default_pass_input,
)
from paper_trading.small_capital_strategy.risk_dashboard_scorecard_v174 import (
    compute_scorecard, GRADE_A_MIN, GRADE_B_MIN,
)


def _inp(**kw):
    return SmallAccountRiskInput(**kw)


class TestBearExposureBoundaryRegression:
    """Regression: bear exposure 50% must be PASS, not WARNING."""

    def test_bear_50_pct_invested_is_pass(self):
        r = evaluate_portfolio_exposure(_inp(market_regime="BEAR", total_invested_pct=50.0, cash_pct=50.0))
        assert r.status == RiskStatus.PASS

    def test_bear_51_pct_invested_is_blocked(self):
        r = evaluate_portfolio_exposure(_inp(market_regime="BEAR", total_invested_pct=51.0, cash_pct=49.0))
        assert r.status == RiskStatus.BLOCKED

    def test_bull_95_pct_invested_is_pass(self):
        r = evaluate_portfolio_exposure(_inp(market_regime="BULL", total_invested_pct=95.0, cash_pct=5.0))
        assert r.status == RiskStatus.PASS

    def test_bull_96_pct_invested_is_blocked(self):
        r = evaluate_portfolio_exposure(_inp(market_regime="BULL", total_invested_pct=96.0, cash_pct=4.0))
        assert r.status == RiskStatus.BLOCKED

    def test_risk_off_40_pct_invested_is_pass(self):
        r = evaluate_portfolio_exposure(_inp(market_regime="RISK_OFF", total_invested_pct=40.0, cash_pct=60.0))
        assert r.status == RiskStatus.PASS

    def test_risk_off_41_pct_invested_is_blocked(self):
        r = evaluate_portfolio_exposure(_inp(market_regime="RISK_OFF", total_invested_pct=41.0, cash_pct=59.0))
        assert r.status == RiskStatus.BLOCKED


class TestSingleTradeRiskBoundaries:
    """Regression: exact boundary values for single trade risk thresholds."""

    def test_loss_3000_is_pass(self):
        r = evaluate_single_trade_risk(_inp(position_size_amount=60000, stop_loss_pct=0.05, has_stop_loss=True))
        assert r.status == RiskStatus.PASS

    def test_loss_4500_is_warning(self):
        r = evaluate_single_trade_risk(_inp(position_size_amount=90000, stop_loss_pct=0.05, has_stop_loss=True))
        assert r.status == RiskStatus.WARNING

    def test_loss_4501_is_blocked(self):
        r = evaluate_single_trade_risk(_inp(position_size_amount=90020, stop_loss_pct=0.05, has_stop_loss=True))
        assert r.status == RiskStatus.BLOCKED

    def test_no_stop_loss_always_blocked(self):
        r = evaluate_single_trade_risk(_inp(has_stop_loss=False, position_size_amount=1000))
        assert r.status == RiskStatus.BLOCKED


class TestDrawdownBoundaries:
    """Regression: drawdown boundary values."""

    def test_drawdown_5_pct_is_pass(self):
        r = evaluate_drawdown(_inp(current_drawdown_pct=5.0))
        assert r.status == RiskStatus.PASS

    def test_drawdown_5_01_is_watch(self):
        r = evaluate_drawdown(_inp(current_drawdown_pct=5.01))
        assert r.status == RiskStatus.WATCH

    def test_drawdown_8_is_watch(self):
        r = evaluate_drawdown(_inp(current_drawdown_pct=8.0))
        assert r.status == RiskStatus.WATCH

    def test_drawdown_8_01_is_warning(self):
        r = evaluate_drawdown(_inp(current_drawdown_pct=8.01))
        assert r.status == RiskStatus.WARNING

    def test_drawdown_12_01_is_blocked(self):
        r = evaluate_drawdown(_inp(current_drawdown_pct=12.01))
        assert r.status == RiskStatus.BLOCKED


class TestLosingStreakBoundaries:
    """Regression: losing streak boundary values."""

    def test_streak_2_is_pass(self):
        assert evaluate_losing_streak(_inp(losing_streak_count=2)).status == RiskStatus.PASS

    def test_streak_3_is_watch(self):
        assert evaluate_losing_streak(_inp(losing_streak_count=3)).status == RiskStatus.WATCH

    def test_streak_4_is_warning(self):
        assert evaluate_losing_streak(_inp(losing_streak_count=4)).status == RiskStatus.WARNING

    def test_streak_5_is_blocked(self):
        assert evaluate_losing_streak(_inp(losing_streak_count=5)).status == RiskStatus.BLOCKED


class TestConcentrationBoundaries:
    """Regression: concentration boundary values."""

    def test_single_35_is_pass(self):
        r = evaluate_concentration_risk(_inp(max_single_position_pct=35.0, sector_exposure_pct=40.0))
        assert r.status == RiskStatus.PASS

    def test_single_36_is_blocked(self):
        r = evaluate_concentration_risk(_inp(max_single_position_pct=36.0, sector_exposure_pct=40.0))
        assert r.status == RiskStatus.BLOCKED

    def test_sector_55_is_pass(self):
        # warning threshold is >55%, so exactly 55 is PASS
        r = evaluate_concentration_risk(_inp(max_single_position_pct=20.0, sector_exposure_pct=55.0))
        assert r.status == RiskStatus.PASS

    def test_sector_60_is_warning(self):
        # 60 > 55 => WARNING, but 60 <= 60 => not BLOCKED
        r = evaluate_concentration_risk(_inp(max_single_position_pct=20.0, sector_exposure_pct=60.0))
        assert r.status == RiskStatus.WARNING

    def test_sector_61_is_blocked(self):
        r = evaluate_concentration_risk(_inp(max_single_position_pct=20.0, sector_exposure_pct=61.0))
        assert r.status == RiskStatus.BLOCKED


class TestScorecardGradeBoundaries:
    """Regression: scorecard grade thresholds."""

    def test_grade_a_min_85(self):
        assert GRADE_A_MIN == 85.0

    def test_grade_b_min_70(self):
        assert GRADE_B_MIN == 70.0

    def test_no_aplus_grade(self):
        assert not hasattr(RiskDashboardScorecardGrade, "A_PLUS")

    def test_default_pass_input_not_grade_f(self):
        dashboard = build_risk_dashboard(get_default_pass_input())
        scorecard = compute_scorecard(dashboard)
        assert scorecard.grade != RiskDashboardScorecardGrade.F


class TestSafetyRegressions:
    """Regression: safety flags must always be enforced."""

    def test_real_order_blocked_regardless_of_other_params(self):
        inp = SmallAccountRiskInput(
            real_order_requested=True, has_stop_loss=True, stop_loss_pct=0.05,
            capital_twd=300000.0, total_invested_pct=20.0, cash_pct=80.0,
        )
        dashboard = build_risk_dashboard(inp)
        assert dashboard.overall_status == RiskStatus.BLOCKED

    def test_broker_blocked_regardless_of_other_params(self):
        inp = SmallAccountRiskInput(
            broker_requested=True, has_stop_loss=True, stop_loss_pct=0.05,
            capital_twd=300000.0, total_invested_pct=20.0, cash_pct=80.0,
        )
        dashboard = build_risk_dashboard(inp)
        assert dashboard.overall_status == RiskStatus.BLOCKED

    def test_margin_blocked(self):
        inp = SmallAccountRiskInput(
            margin_requested=True, has_stop_loss=True, stop_loss_pct=0.05,
        )
        dashboard = build_risk_dashboard(inp)
        assert dashboard.overall_status == RiskStatus.BLOCKED
