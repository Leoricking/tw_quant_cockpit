"""
tests/test_market_regime_regression_v173.py
Regression tests for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_enums_v173 import MarketRegime
from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput
from paper_trading.small_capital_strategy.market_regime_detector_v173 import detect_market_regime
from paper_trading.small_capital_strategy.cash_ratio_engine_v173 import build_cash_ratio_plan
from paper_trading.small_capital_strategy.exposure_control_engine_v173 import build_exposure_control_plan
from paper_trading.small_capital_strategy.bucket_adjustment_engine_v173 import build_bucket_adjustment_plan
from paper_trading.small_capital_strategy.candidate_permission_engine_v173 import get_abc_regime_permission
from paper_trading.small_capital_strategy.market_regime_safety_v173 import (
    audit_market_regime_safety,
)


class TestSafetyAlwaysHolds:
    def test_safety_audit_always_safe(self):
        result = audit_market_regime_safety()
        assert result["all_safe"] is True

    def test_no_dangerous_capabilities(self):
        result = audit_market_regime_safety()
        assert result["safety_capabilities"] == 0


class TestAllocationSumInvariant:
    """All regime allocations must sum to exactly 100%."""

    def test_bull_sums_100(self):
        plan = build_cash_ratio_plan(MarketRegime.BULL)
        total = (plan.core_pct + plan.main_theme_swing_pct + plan.second_wave_setup_pct
                 + plan.short_term_training_pct + plan.cash_pct)
        assert total == 100

    def test_range_sums_100(self):
        plan = build_cash_ratio_plan(MarketRegime.RANGE)
        total = (plan.core_pct + plan.main_theme_swing_pct + plan.second_wave_setup_pct
                 + plan.short_term_training_pct + plan.cash_pct)
        assert total == 100

    def test_bear_sums_100(self):
        plan = build_cash_ratio_plan(MarketRegime.BEAR)
        total = (plan.core_pct + plan.main_theme_swing_pct + plan.second_wave_setup_pct
                 + plan.short_term_training_pct + plan.cash_pct)
        assert total == 100

    def test_risk_off_sums_100(self):
        plan = build_cash_ratio_plan(MarketRegime.RISK_OFF)
        total = (plan.core_pct + plan.main_theme_swing_pct + plan.second_wave_setup_pct
                 + plan.short_term_training_pct + plan.cash_pct)
        assert total == 100

    def test_unknown_sums_100(self):
        plan = build_cash_ratio_plan(MarketRegime.UNKNOWN)
        total = (plan.core_pct + plan.main_theme_swing_pct + plan.second_wave_setup_pct
                 + plan.short_term_training_pct + plan.cash_pct)
        assert total == 100


class TestBucketAmountInvariant:
    """Bucket amounts in TWD must sum to capital for all regimes."""

    def test_all_regimes_bucket_sum_equals_capital(self):
        for regime in MarketRegime:
            plan = build_bucket_adjustment_plan(regime)
            computed = (plan.core_amount + plan.main_theme_swing_amount
                        + plan.second_wave_setup_amount + plan.short_term_training_amount
                        + plan.cash_amount)
            assert abs(computed - plan.capital_twd) < 1.0, f"Bucket sum mismatch for {regime.value}: {computed} != {plan.capital_twd}"


class TestNoMarginLeverageInvariant:
    """Margin and leverage must never be allowed in any regime."""

    def test_no_margin_all_regimes(self):
        for regime in MarketRegime:
            plan = build_exposure_control_plan(regime)
            assert not plan.margin_allowed, f"Margin enabled for {regime.value}"

    def test_no_leverage_all_regimes(self):
        for regime in MarketRegime:
            plan = build_exposure_control_plan(regime)
            assert not plan.leverage_allowed, f"Leverage enabled for {regime.value}"


class TestTrainingZeroInvariant:
    """TRAINING must be 0 in BEAR, RISK_OFF, and UNKNOWN."""

    def test_bear_training_zero(self):
        plan = build_cash_ratio_plan(MarketRegime.BEAR)
        assert plan.short_term_training_pct == 0

    def test_risk_off_training_zero(self):
        plan = build_cash_ratio_plan(MarketRegime.RISK_OFF)
        assert plan.short_term_training_pct == 0

    def test_unknown_training_zero(self):
        plan = build_cash_ratio_plan(MarketRegime.UNKNOWN)
        assert plan.short_term_training_pct == 0


class TestABCBlockingInvariant:
    """BEAR and RISK_OFF must block all ABC buy points."""

    def test_bear_blocks_a(self):
        assert not get_abc_regime_permission(MarketRegime.BEAR).a_allowed

    def test_bear_blocks_b(self):
        assert not get_abc_regime_permission(MarketRegime.BEAR).b_allowed

    def test_bear_blocks_c(self):
        assert not get_abc_regime_permission(MarketRegime.BEAR).c_allowed

    def test_risk_off_blocks_a(self):
        assert not get_abc_regime_permission(MarketRegime.RISK_OFF).a_allowed

    def test_risk_off_blocks_b(self):
        assert not get_abc_regime_permission(MarketRegime.RISK_OFF).b_allowed

    def test_risk_off_blocks_c(self):
        assert not get_abc_regime_permission(MarketRegime.RISK_OFF).c_allowed


class TestDetectorInsufficientDataInvariant:
    """Zero close price must always produce INSUFFICIENT status."""

    def test_zero_close_always_insufficient(self):
        for _ in range(3):
            result = detect_market_regime(MarketRegimeInput(index_close=0))
            from paper_trading.small_capital_strategy.market_regime_enums_v173 import RegimeDetectionStatus
            assert result.status == RegimeDetectionStatus.INSUFFICIENT

    def test_zero_close_always_unknown_regime(self):
        result = detect_market_regime(MarketRegimeInput(index_close=0))
        assert result.regime == MarketRegime.UNKNOWN


class TestPaperOnlyInvariant:
    """All models must always have paper_only=True."""

    def test_detection_result_paper_only(self):
        inp = MarketRegimeInput(
            index_close=20000, index_ma20=19500, index_ma60=18800, index_ma120=17500, index_ma240=16000,
        )
        result = detect_market_regime(inp)
        assert result.paper_only is True

    def test_cash_plan_paper_only(self):
        for regime in MarketRegime:
            assert build_cash_ratio_plan(regime).paper_only is True

    def test_exposure_plan_paper_only(self):
        for regime in MarketRegime:
            assert build_exposure_control_plan(regime).paper_only is True
