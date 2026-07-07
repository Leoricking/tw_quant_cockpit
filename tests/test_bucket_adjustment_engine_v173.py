"""
tests/test_bucket_adjustment_engine_v173.py
Tests for Market Regime Position Control bucket_adjustment_engine_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_enums_v173 import MarketRegime
from paper_trading.small_capital_strategy.bucket_adjustment_engine_v173 import (
    build_bucket_adjustment_plan, get_training_amount, DEFAULT_CAPITAL_TWD,
)


class TestBuildBucketAdjustmentPlan:
    def test_bull_total_equals_capital(self):
        plan = build_bucket_adjustment_plan(MarketRegime.BULL)
        assert abs(plan.total_amount - 300_000.0) < 1.0

    def test_bull_core_amount_correct(self):
        plan = build_bucket_adjustment_plan(MarketRegime.BULL)
        # 40% of 300k = 120,000
        assert abs(plan.core_amount - 120_000.0) < 1.0

    def test_bull_training_amount_correct(self):
        plan = build_bucket_adjustment_plan(MarketRegime.BULL)
        # 5% of 300k = 15,000
        assert abs(plan.short_term_training_amount - 15_000.0) < 1.0

    def test_bull_cash_amount_correct(self):
        plan = build_bucket_adjustment_plan(MarketRegime.BULL)
        # 5% of 300k = 15,000
        assert abs(plan.cash_amount - 15_000.0) < 1.0

    def test_bear_training_zero(self):
        plan = build_bucket_adjustment_plan(MarketRegime.BEAR)
        assert plan.short_term_training_amount == 0.0

    def test_risk_off_training_zero(self):
        plan = build_bucket_adjustment_plan(MarketRegime.RISK_OFF)
        assert plan.short_term_training_amount == 0.0

    def test_unknown_training_zero(self):
        plan = build_bucket_adjustment_plan(MarketRegime.UNKNOWN)
        assert plan.short_term_training_amount == 0.0

    def test_range_training_5pct(self):
        plan = build_bucket_adjustment_plan(MarketRegime.RANGE)
        # 5% of 300k = 15,000
        assert abs(plan.short_term_training_amount - 15_000.0) < 1.0

    def test_all_regimes_total_equals_capital(self):
        for regime in MarketRegime:
            plan = build_bucket_adjustment_plan(regime)
            assert abs(plan.total_amount - DEFAULT_CAPITAL_TWD) < 1.0

    def test_custom_capital(self):
        plan = build_bucket_adjustment_plan(MarketRegime.BULL, 600_000.0)
        assert abs(plan.total_amount - 600_000.0) < 1.0

    def test_capital_stored(self):
        plan = build_bucket_adjustment_plan(MarketRegime.BULL)
        assert plan.capital_twd == DEFAULT_CAPITAL_TWD

    def test_bucket_pcts_dict(self):
        plan = build_bucket_adjustment_plan(MarketRegime.BULL)
        assert "CORE" in plan.bucket_pcts
        assert "CASH" in plan.bucket_pcts

    def test_paper_only(self):
        plan = build_bucket_adjustment_plan(MarketRegime.BULL)
        assert plan.paper_only is True

    def test_no_real_orders(self):
        plan = build_bucket_adjustment_plan(MarketRegime.BULL)
        assert plan.no_real_orders is True

    def test_risk_off_cash_60pct_of_capital(self):
        plan = build_bucket_adjustment_plan(MarketRegime.RISK_OFF)
        assert abs(plan.cash_amount - 180_000.0) < 1.0


class TestGetTrainingAmount:
    def test_bull_training_nonzero(self):
        assert get_training_amount(MarketRegime.BULL) > 0

    def test_bear_training_zero(self):
        assert get_training_amount(MarketRegime.BEAR) == 0.0

    def test_risk_off_training_zero(self):
        assert get_training_amount(MarketRegime.RISK_OFF) == 0.0

    def test_unknown_training_zero(self):
        assert get_training_amount(MarketRegime.UNKNOWN) == 0.0

    def test_range_training_nonzero(self):
        assert get_training_amount(MarketRegime.RANGE) > 0


class TestDefaultCapital:
    def test_default_capital_300k(self):
        assert DEFAULT_CAPITAL_TWD == 300_000.0
