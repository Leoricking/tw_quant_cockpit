"""
tests/test_market_regime_models_v173.py
Tests for Market Regime Position Control models_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_models_v173 import (
    MarketRegimeInput, TrendFilterResult, VolatilityFilterResult,
    BreadthFilterResult, RiskOffDetectionResult, MarketRegimeDetectionResult,
    CashRatioPlan, ExposureControlPlan, BucketAdjustmentPlan,
    CandidateRegimePermission, ABCRegimePermission, MarketRegimeScorecard,
    MarketRegimeReport, MarketRegimeHealthSummary,
)
from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimeDetectionStatus,
)


class TestMarketRegimeInput:
    def test_default_paper_only(self):
        assert MarketRegimeInput().paper_only is True

    def test_default_no_real_orders(self):
        assert MarketRegimeInput().no_real_orders is True

    def test_default_research_only(self):
        assert MarketRegimeInput().research_only is True

    def test_default_not_investment_advice(self):
        assert MarketRegimeInput().not_investment_advice is True

    def test_schema_version(self):
        assert MarketRegimeInput().schema_version == "173"

    def test_custom_index_close(self):
        inp = MarketRegimeInput(index_close=20000.0)
        assert inp.index_close == 20000.0

    def test_default_index_close_zero(self):
        assert MarketRegimeInput().index_close == 0.0

    def test_volume_ratio_default_one(self):
        assert MarketRegimeInput().index_volume_ratio == 1.0


class TestTrendFilterResult:
    def test_paper_only_default(self):
        assert TrendFilterResult().paper_only is True

    def test_schema_version(self):
        assert TrendFilterResult().schema_version == "173"

    def test_no_real_orders(self):
        assert TrendFilterResult().no_real_orders is True


class TestVolatilityFilterResult:
    def test_paper_only_default(self):
        assert VolatilityFilterResult().paper_only is True

    def test_controlled_default_true(self):
        assert VolatilityFilterResult().volatility_controlled is True


class TestBreadthFilterResult:
    def test_paper_only_default(self):
        assert BreadthFilterResult().paper_only is True

    def test_advance_decline_default_one(self):
        assert BreadthFilterResult().advance_decline_ratio == 1.0


class TestRiskOffDetectionResult:
    def test_paper_only_default(self):
        assert RiskOffDetectionResult().paper_only is True

    def test_no_real_orders(self):
        assert RiskOffDetectionResult().no_real_orders is True


class TestMarketRegimeDetectionResult:
    def test_paper_only_default(self):
        assert MarketRegimeDetectionResult().paper_only is True

    def test_default_regime_unknown(self):
        assert MarketRegimeDetectionResult().regime == MarketRegime.UNKNOWN

    def test_default_status_insufficient(self):
        assert MarketRegimeDetectionResult().status == RegimeDetectionStatus.INSUFFICIENT

    def test_block_reasons_default_empty(self):
        assert MarketRegimeDetectionResult().block_reasons == []

    def test_warnings_default_empty(self):
        assert MarketRegimeDetectionResult().warnings == []


class TestCashRatioPlan:
    def test_paper_only_default(self):
        assert CashRatioPlan().paper_only is True

    def test_no_real_orders(self):
        assert CashRatioPlan().no_real_orders is True

    def test_default_total_100(self):
        assert CashRatioPlan().total_pct == 100


class TestExposureControlPlan:
    def test_paper_only_default(self):
        assert ExposureControlPlan().paper_only is True

    def test_no_margin_default(self):
        assert ExposureControlPlan().margin_allowed is False

    def test_no_leverage_default(self):
        assert ExposureControlPlan().leverage_allowed is False


class TestBucketAdjustmentPlan:
    def test_paper_only_default(self):
        assert BucketAdjustmentPlan().paper_only is True

    def test_capital_default_300k(self):
        assert BucketAdjustmentPlan().capital_twd == 300_000.0


class TestCandidateRegimePermission:
    def test_paper_only_default(self):
        assert CandidateRegimePermission().paper_only is True

    def test_buy_points_default_empty(self):
        assert CandidateRegimePermission().buy_points_allowed == []


class TestABCRegimePermission:
    def test_paper_only_default(self):
        assert ABCRegimePermission().paper_only is True

    def test_all_blocked_default(self):
        p = ABCRegimePermission()
        assert p.a_allowed is False
        assert p.b_allowed is False
        assert p.c_allowed is False


class TestMarketRegimeScorecard:
    def test_paper_only_default(self):
        assert MarketRegimeScorecard().paper_only is True

    def test_weights_sum_100(self):
        assert MarketRegimeScorecard().weights_sum == 100

    def test_schema_version(self):
        assert MarketRegimeScorecard().schema_version == "173"


class TestMarketRegimeReport:
    def test_paper_only_default(self):
        assert MarketRegimeReport().paper_only is True

    def test_no_real_orders(self):
        assert MarketRegimeReport().no_real_orders is True

    def test_sections_default_empty(self):
        assert MarketRegimeReport().sections == {}

    def test_report_format_json(self):
        assert MarketRegimeReport().report_format == "JSON"


class TestMarketRegimeHealthSummary:
    def test_paper_only_default(self):
        assert MarketRegimeHealthSummary().paper_only is True

    def test_all_passed_default_false(self):
        assert MarketRegimeHealthSummary().all_passed is False

    def test_status_default_fail(self):
        assert MarketRegimeHealthSummary().status == "FAIL"
