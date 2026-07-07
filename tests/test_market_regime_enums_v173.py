"""
tests/test_market_regime_enums_v173.py
Tests for Market Regime Position Control enums_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_enums_v173 import (
    MarketRegime, RegimeDetectionStatus, TrendSignal, VolatilityLevel,
    BreadthSignal, RiskOffSignal, AllocationBucket, RegimePermissionStatus,
    RegimeScorecardGrade, RegimeBlockReason, RegimeWarningReason,
    get_all_enum_names,
)


class TestMarketRegime:
    def test_five_values(self):
        assert len(MarketRegime) == 5

    def test_bull_exists(self):
        assert MarketRegime.BULL.value == "BULL"

    def test_range_exists(self):
        assert MarketRegime.RANGE.value == "RANGE"

    def test_bear_exists(self):
        assert MarketRegime.BEAR.value == "BEAR"

    def test_risk_off_exists(self):
        assert MarketRegime.RISK_OFF.value == "RISK_OFF"

    def test_unknown_exists(self):
        assert MarketRegime.UNKNOWN.value == "UNKNOWN"


class TestRegimeDetectionStatus:
    def test_four_values(self):
        assert len(RegimeDetectionStatus) == 4

    def test_detected_exists(self):
        assert RegimeDetectionStatus.DETECTED.value == "DETECTED"

    def test_insufficient_exists(self):
        assert RegimeDetectionStatus.INSUFFICIENT.value == "INSUFFICIENT"

    def test_conflicted_exists(self):
        assert RegimeDetectionStatus.CONFLICTED.value == "CONFLICTED"

    def test_blocked_exists(self):
        assert RegimeDetectionStatus.BLOCKED.value == "BLOCKED"


class TestTrendSignal:
    def test_six_values(self):
        assert len(TrendSignal) == 6

    def test_strong_up_exists(self):
        assert TrendSignal.STRONG_UP.value == "STRONG_UP"

    def test_unknown_exists(self):
        assert TrendSignal.UNKNOWN.value == "UNKNOWN"


class TestVolatilityLevel:
    def test_five_values(self):
        assert len(VolatilityLevel) == 5

    def test_extreme_exists(self):
        assert VolatilityLevel.EXTREME.value == "EXTREME"


class TestBreadthSignal:
    def test_five_values(self):
        assert len(BreadthSignal) == 5

    def test_very_weak_exists(self):
        assert BreadthSignal.VERY_WEAK.value == "VERY_WEAK"

    def test_healthy_exists(self):
        assert BreadthSignal.HEALTHY.value == "HEALTHY"


class TestRiskOffSignal:
    def test_four_values(self):
        assert len(RiskOffSignal) == 4

    def test_none_exists(self):
        assert RiskOffSignal.NONE.value == "NONE"

    def test_extreme_exists(self):
        assert RiskOffSignal.EXTREME.value == "EXTREME"


class TestAllocationBucket:
    def test_five_values(self):
        assert len(AllocationBucket) == 5

    def test_core_exists(self):
        assert AllocationBucket.CORE.value == "CORE"

    def test_cash_exists(self):
        assert AllocationBucket.CASH.value == "CASH"


class TestRegimePermissionStatus:
    def test_five_values(self):
        assert len(RegimePermissionStatus) == 5

    def test_allowed_exists(self):
        assert RegimePermissionStatus.ALLOWED.value == "ALLOWED"

    def test_blocked_exists(self):
        assert RegimePermissionStatus.BLOCKED.value == "BLOCKED"

    def test_degraded_exists(self):
        assert RegimePermissionStatus.DEGRADED.value == "DEGRADED"


class TestRegimeScorecardGrade:
    def test_six_values(self):
        assert len(RegimeScorecardGrade) == 6

    def test_no_a_plus(self):
        assert not hasattr(RegimeScorecardGrade, "A_PLUS")

    def test_a_exists(self):
        assert RegimeScorecardGrade.A.value == "A"

    def test_blocked_exists(self):
        assert RegimeScorecardGrade.BLOCKED.value == "BLOCKED"


class TestRegimeBlockReason:
    def test_14_values(self):
        assert len(RegimeBlockReason) == 14

    def test_regime_bear_exists(self):
        assert RegimeBlockReason.REGIME_BEAR.value == "REGIME_BEAR"

    def test_regime_risk_off_exists(self):
        assert RegimeBlockReason.REGIME_RISK_OFF.value == "REGIME_RISK_OFF"

    def test_safety_violation_exists(self):
        assert RegimeBlockReason.SAFETY_VIOLATION.value == "SAFETY_VIOLATION"

    def test_insufficient_data_exists(self):
        assert RegimeBlockReason.INSUFFICIENT_DATA.value == "INSUFFICIENT_DATA"


class TestRegimeWarningReason:
    def test_four_values(self):
        assert len(RegimeWarningReason) == 4

    def test_regime_degraded_exists(self):
        assert RegimeWarningReason.REGIME_DEGRADED.value == "REGIME_DEGRADED"


class TestGetAllEnumNames:
    def test_returns_11_names(self):
        names = get_all_enum_names()
        assert len(names) == 11

    def test_market_regime_in_names(self):
        assert "MarketRegime" in get_all_enum_names()

    def test_returns_list(self):
        assert isinstance(get_all_enum_names(), list)
