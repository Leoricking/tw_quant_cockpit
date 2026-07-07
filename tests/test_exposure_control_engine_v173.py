"""
tests/test_exposure_control_engine_v173.py
Tests for Market Regime Position Control exposure_control_engine_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_enums_v173 import MarketRegime
from paper_trading.small_capital_strategy.exposure_control_engine_v173 import (
    build_exposure_control_plan, check_exposure_within_limits,
)


class TestBuildExposureControlPlan:
    def test_bull_max_total_95(self):
        plan = build_exposure_control_plan(MarketRegime.BULL)
        assert plan.max_total_exposure_pct == 95

    def test_range_max_total_75(self):
        plan = build_exposure_control_plan(MarketRegime.RANGE)
        assert plan.max_total_exposure_pct == 75

    def test_bear_max_total_50(self):
        plan = build_exposure_control_plan(MarketRegime.BEAR)
        assert plan.max_total_exposure_pct == 50

    def test_risk_off_max_total_40(self):
        plan = build_exposure_control_plan(MarketRegime.RISK_OFF)
        assert plan.max_total_exposure_pct == 40

    def test_unknown_max_total_60(self):
        plan = build_exposure_control_plan(MarketRegime.UNKNOWN)
        assert plan.max_total_exposure_pct == 60

    def test_no_margin_allowed_any_regime(self):
        for regime in MarketRegime:
            plan = build_exposure_control_plan(regime)
            assert plan.margin_allowed is False

    def test_no_leverage_allowed_any_regime(self):
        for regime in MarketRegime:
            plan = build_exposure_control_plan(regime)
            assert plan.leverage_allowed is False

    def test_bull_single_position_40(self):
        plan = build_exposure_control_plan(MarketRegime.BULL)
        assert plan.max_single_position_pct == 40

    def test_risk_off_single_position_15(self):
        plan = build_exposure_control_plan(MarketRegime.RISK_OFF)
        assert plan.max_single_position_pct == 15

    def test_paper_only(self):
        plan = build_exposure_control_plan(MarketRegime.BULL)
        assert plan.paper_only is True

    def test_no_real_orders(self):
        plan = build_exposure_control_plan(MarketRegime.BULL)
        assert plan.no_real_orders is True

    def test_regime_stored(self):
        plan = build_exposure_control_plan(MarketRegime.BEAR)
        assert plan.regime == MarketRegime.BEAR

    def test_no_block_reasons(self):
        plan = build_exposure_control_plan(MarketRegime.BULL)
        assert plan.block_reasons == []


class TestCheckExposureWithinLimits:
    def test_within_limits_bull(self):
        result = check_exposure_within_limits(MarketRegime.BULL, 50.0, 20.0)
        assert result["within_limits"] is True

    def test_total_exceeds_limit(self):
        result = check_exposure_within_limits(MarketRegime.RISK_OFF, 50.0, 10.0)
        assert result["within_limits"] is False

    def test_violations_list_when_exceeds(self):
        result = check_exposure_within_limits(MarketRegime.RISK_OFF, 50.0, 10.0)
        assert len(result["violations"]) > 0

    def test_no_violations_when_within(self):
        result = check_exposure_within_limits(MarketRegime.BULL, 50.0, 20.0)
        assert result["violations"] == []

    def test_returns_plan(self):
        result = check_exposure_within_limits(MarketRegime.BULL, 50.0, 20.0)
        assert "plan" in result
