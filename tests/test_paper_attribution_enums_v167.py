"""
tests/test_paper_attribution_enums_v167.py
Tests for paper attribution enums v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from paper_trading.performance_attribution.enums_v167 import (
    AttributionLevel,
    AttributionDimension,
    AttributionMethod,
    ContributionType,
    ReturnBasis,
    CostType,
    CostQuality,
    ExecutionQuality,
    ExecutionReference,
    RiskSource,
    DrawdownSource,
    RegimeType,
    BenchmarkMode,
    ReconciliationStatus,
    AttributionStatus,
    DataQualityStatus,
    ConfidenceLevel,
    PeriodType,
    TradeDirection,
    PositionState,
    SessionState,
    FixtureUsageType,
    AttributionPurpose,
    FORBIDDEN_FIELDS,
)


class TestAttributionLevel:
    def test_has_portfolio(self):
        assert AttributionLevel.PORTFOLIO in AttributionLevel

    def test_has_strategy(self):
        assert AttributionLevel.STRATEGY in AttributionLevel

    def test_has_session(self):
        assert AttributionLevel.SESSION in AttributionLevel

    def test_has_symbol(self):
        assert AttributionLevel.SYMBOL in AttributionLevel

    def test_has_sector(self):
        assert AttributionLevel.SECTOR in AttributionLevel

    def test_has_industry(self):
        assert AttributionLevel.INDUSTRY in AttributionLevel

    def test_has_position(self):
        assert AttributionLevel.POSITION in AttributionLevel

    def test_has_trade(self):
        assert AttributionLevel.TRADE in AttributionLevel

    def test_count_at_least_8(self):
        assert len(AttributionLevel) >= 8

    def test_values_are_strings(self):
        for v in AttributionLevel:
            assert isinstance(v.value, str)


class TestAttributionDimension:
    def test_has_selection(self):
        assert AttributionDimension.SELECTION in AttributionDimension

    def test_has_allocation(self):
        assert AttributionDimension.ALLOCATION in AttributionDimension

    def test_has_timing(self):
        assert AttributionDimension.TIMING in AttributionDimension

    def test_has_execution(self):
        assert AttributionDimension.EXECUTION in AttributionDimension

    def test_has_cost(self):
        assert AttributionDimension.COST in AttributionDimension

    def test_has_risk(self):
        assert AttributionDimension.RISK in AttributionDimension

    def test_has_drawdown(self):
        assert AttributionDimension.DRAWDOWN in AttributionDimension

    def test_has_regime(self):
        assert AttributionDimension.REGIME in AttributionDimension

    def test_has_benchmark(self):
        assert AttributionDimension.BENCHMARK in AttributionDimension

    def test_has_factor(self):
        assert AttributionDimension.FACTOR in AttributionDimension

    def test_has_residual(self):
        assert AttributionDimension.RESIDUAL in AttributionDimension

    def test_count_at_least_11(self):
        assert len(AttributionDimension) >= 11


class TestAttributionMethod:
    def test_has_brinson(self):
        assert AttributionMethod.BRINSON_HOOD_BEEBOWER in AttributionMethod

    def test_has_brinson_fachler(self):
        assert AttributionMethod.BRINSON_FACHLER in AttributionMethod

    def test_values_are_strings(self):
        for v in AttributionMethod:
            assert isinstance(v.value, str)


class TestReturnBasis:
    def test_has_gross(self):
        assert ReturnBasis.GROSS in ReturnBasis

    def test_has_net(self):
        assert ReturnBasis.NET in ReturnBasis

    def test_has_active(self):
        assert ReturnBasis.ACTIVE in ReturnBasis

    def test_has_time_weighted(self):
        assert ReturnBasis.TIME_WEIGHTED in ReturnBasis

    def test_has_money_weighted(self):
        assert ReturnBasis.MONEY_WEIGHTED in ReturnBasis


class TestCostType:
    def test_has_commission(self):
        assert CostType.COMMISSION in CostType

    def test_has_transaction_tax(self):
        assert CostType.TRANSACTION_TAX in CostType

    def test_has_spread_cost(self):
        assert CostType.SPREAD_COST in CostType

    def test_has_slippage(self):
        assert CostType.SLIPPAGE in CostType


class TestCostQuality:
    def test_has_known(self):
        assert CostQuality.KNOWN in CostQuality

    def test_has_estimated(self):
        assert CostQuality.ESTIMATED in CostQuality

    def test_has_unknown(self):
        assert CostQuality.UNKNOWN in CostQuality


class TestReconciliationStatus:
    def test_has_reconciled(self):
        assert ReconciliationStatus.RECONCILED in ReconciliationStatus

    def test_has_reconciled_with_rounding(self):
        assert ReconciliationStatus.RECONCILED_WITH_ROUNDING in ReconciliationStatus

    def test_has_degraded(self):
        assert ReconciliationStatus.DEGRADED in ReconciliationStatus

    def test_has_failed(self):
        assert ReconciliationStatus.FAILED in ReconciliationStatus

    def test_has_insufficient_data(self):
        assert ReconciliationStatus.INSUFFICIENT_DATA in ReconciliationStatus

    def test_count_is_5(self):
        assert len(ReconciliationStatus) == 5


class TestAttributionStatus:
    def test_has_complete(self):
        assert AttributionStatus.COMPLETE in AttributionStatus

    def test_has_degraded(self):
        assert AttributionStatus.DEGRADED in AttributionStatus

    def test_has_failed(self):
        assert AttributionStatus.FAILED in AttributionStatus

    def test_count_at_least_3(self):
        assert len(AttributionStatus) >= 3


class TestConfidenceLevel:
    def test_has_high(self):
        assert ConfidenceLevel.HIGH in ConfidenceLevel

    def test_has_medium(self):
        assert ConfidenceLevel.MEDIUM in ConfidenceLevel

    def test_has_low(self):
        assert ConfidenceLevel.LOW in ConfidenceLevel

    def test_has_unknown(self):
        assert ConfidenceLevel.UNKNOWN in ConfidenceLevel

    def test_count_is_4(self):
        assert len(ConfidenceLevel) == 4


class TestRegimeType:
    def test_has_bull(self):
        assert RegimeType.BULL in RegimeType

    def test_has_bear(self):
        assert RegimeType.BEAR in RegimeType

    def test_has_sideways(self):
        assert RegimeType.SIDEWAYS in RegimeType

    def test_has_unknown(self):
        assert RegimeType.UNKNOWN in RegimeType

    def test_count_at_least_4(self):
        assert len(RegimeType) >= 4


class TestBenchmarkMode:
    def test_has_none(self):
        assert BenchmarkMode.NONE in BenchmarkMode

    def test_has_market_benchmark(self):
        assert BenchmarkMode.MARKET_BENCHMARK in BenchmarkMode


class TestTradeDirection:
    def test_has_long(self):
        assert TradeDirection.LONG in TradeDirection

    def test_has_short(self):
        assert TradeDirection.SHORT in TradeDirection


class TestForbiddenFields:
    def test_is_frozenset(self):
        assert isinstance(FORBIDDEN_FIELDS, frozenset)

    def test_contains_broker_session(self):
        assert "broker_session" in FORBIDDEN_FIELDS

    def test_contains_real_account_token(self):
        assert "real_account_token" in FORBIDDEN_FIELDS

    def test_contains_api_secret(self):
        assert "api_secret" in FORBIDDEN_FIELDS

    def test_contains_password(self):
        assert "password" in FORBIDDEN_FIELDS

    def test_nonempty(self):
        assert len(FORBIDDEN_FIELDS) >= 10

    def test_no_false_positives(self):
        # These are safe fields — should NOT be in forbidden list
        for safe in ("paper_only", "research_only", "run_id", "portfolio_id"):
            assert safe not in FORBIDDEN_FIELDS
