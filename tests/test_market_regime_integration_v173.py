"""
tests/test_market_regime_integration_v173.py
Integration tests for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimeDetectionStatus, RiskOffSignal,
)
from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput
from paper_trading.small_capital_strategy.market_regime_detector_v173 import detect_market_regime
from paper_trading.small_capital_strategy.cash_ratio_engine_v173 import build_cash_ratio_plan
from paper_trading.small_capital_strategy.exposure_control_engine_v173 import build_exposure_control_plan
from paper_trading.small_capital_strategy.bucket_adjustment_engine_v173 import build_bucket_adjustment_plan
from paper_trading.small_capital_strategy.candidate_permission_engine_v173 import (
    get_candidate_permission, get_abc_regime_permission,
)
from paper_trading.small_capital_strategy.market_regime_scorecard_v173 import build_regime_scorecard
from paper_trading.small_capital_strategy.market_regime_report_v173 import (
    build_market_regime_report, render_report_json,
)


def _full_pipeline(inp: MarketRegimeInput, regime: MarketRegime):
    detection     = detect_market_regime(inp)
    cash_plan     = build_cash_ratio_plan(regime)
    exposure_plan = build_exposure_control_plan(regime)
    bucket_plan   = build_bucket_adjustment_plan(regime)
    cand_perm     = get_candidate_permission(regime, "MAIN_THEME_SWING")
    abc_perm      = get_abc_regime_permission(regime)
    scorecard     = build_regime_scorecard(regime, detection, cash_plan, exposure_plan, cand_perm, abc_perm)
    report        = build_market_regime_report(
        regime, detection, cash_plan, exposure_plan, bucket_plan, cand_perm, abc_perm, scorecard
    )
    return {
        "detection": detection,
        "cash_plan": cash_plan,
        "exposure_plan": exposure_plan,
        "bucket_plan": bucket_plan,
        "cand_perm": cand_perm,
        "abc_perm": abc_perm,
        "scorecard": scorecard,
        "report": report,
    }


class TestBullFullPipeline:
    def setup_method(self):
        inp = MarketRegimeInput(
            index_close=20000, index_ma20=19500, index_ma60=18800, index_ma120=17500,
            index_ma240=16000, advance_decline_ratio=1.8, volatility_score=20.0,
            risk_event_flag=False, major_index_trend_score=1.0, institutional_market_bias=0.5,
        )
        self.pipeline = _full_pipeline(inp, MarketRegime.BULL)

    def test_regime_detected(self):
        assert self.pipeline["detection"].regime == MarketRegime.BULL

    def test_cash_plan_valid(self):
        assert self.pipeline["cash_plan"].allocation_valid is True

    def test_cash_total_100(self):
        assert self.pipeline["cash_plan"].total_pct == 100

    def test_no_margin(self):
        assert self.pipeline["exposure_plan"].margin_allowed is False

    def test_bucket_total_equals_capital(self):
        plan = self.pipeline["bucket_plan"]
        assert abs(plan.total_amount - plan.capital_twd) < 1.0

    def test_abc_all_allowed(self):
        perm = self.pipeline["abc_perm"]
        assert perm.a_allowed and perm.b_allowed and perm.c_allowed

    def test_scorecard_has_score(self):
        assert self.pipeline["scorecard"].total_score > 0

    def test_report_14_sections(self):
        assert len(self.pipeline["report"].sections) == 14

    def test_report_paper_only(self):
        assert self.pipeline["report"].paper_only is True

    def test_json_serializable(self):
        import json
        rendered = render_report_json(self.pipeline["report"])
        data = json.loads(rendered)
        assert data["paper_only"] is True


class TestBearFullPipeline:
    def setup_method(self):
        inp = MarketRegimeInput(
            index_close=15000, index_ma20=16000, index_ma60=17000, index_ma120=18000,
            index_ma240=19000, advance_decline_ratio=0.4, volatility_score=60.0,
            risk_event_flag=False, major_index_trend_score=-1.0,
        )
        self.pipeline = _full_pipeline(inp, MarketRegime.BEAR)

    def test_regime_detected(self):
        assert self.pipeline["detection"].regime == MarketRegime.BEAR

    def test_bear_main_theme_blocked(self):
        from paper_trading.small_capital_strategy.market_regime_enums_v173 import RegimePermissionStatus
        assert self.pipeline["cand_perm"].permission == RegimePermissionStatus.BLOCKED

    def test_bear_abc_blocked(self):
        perm = self.pipeline["abc_perm"]
        assert not perm.a_allowed
        assert not perm.b_allowed
        assert not perm.c_allowed

    def test_bear_training_zero(self):
        assert self.pipeline["bucket_plan"].short_term_training_amount == 0.0

    def test_bear_cash_50pct(self):
        assert self.pipeline["cash_plan"].cash_pct == 50


class TestRiskOffFullPipeline:
    def setup_method(self):
        inp = MarketRegimeInput(
            index_close=14000, index_ma20=15000, index_ma60=16000, index_ma120=17000,
            index_ma240=18000, advance_decline_ratio=0.3, volatility_score=80.0,
            risk_event_flag=True, major_index_trend_score=-2.0,
        )
        self.pipeline = _full_pipeline(inp, MarketRegime.RISK_OFF)

    def test_risk_off_detected(self):
        assert self.pipeline["detection"].regime == MarketRegime.RISK_OFF

    def test_risk_off_cash_60pct(self):
        assert self.pipeline["cash_plan"].cash_pct == 60

    def test_risk_off_training_zero(self):
        assert self.pipeline["bucket_plan"].short_term_training_amount == 0.0

    def test_risk_off_abc_blocked(self):
        perm = self.pipeline["abc_perm"]
        assert not perm.a_allowed


class TestSafetyInvariants:
    def test_no_margin_any_regime(self):
        for regime in MarketRegime:
            plan = build_exposure_control_plan(regime)
            assert plan.margin_allowed is False, f"Margin allowed in {regime.value}"

    def test_no_leverage_any_regime(self):
        for regime in MarketRegime:
            plan = build_exposure_control_plan(regime)
            assert plan.leverage_allowed is False, f"Leverage allowed in {regime.value}"

    def test_all_allocations_total_100(self):
        for regime in MarketRegime:
            plan = build_cash_ratio_plan(regime)
            assert plan.total_pct == 100, f"{regime.value} allocation does not sum to 100"

    def test_training_zero_in_restrictive_regimes(self):
        for regime in [MarketRegime.BEAR, MarketRegime.RISK_OFF, MarketRegime.UNKNOWN]:
            plan = build_cash_ratio_plan(regime)
            assert plan.short_term_training_pct == 0, f"Training non-zero in {regime.value}"
