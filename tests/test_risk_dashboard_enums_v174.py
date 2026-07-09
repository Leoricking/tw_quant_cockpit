"""
tests/test_risk_dashboard_enums_v174.py
Tests for Small Account Risk Dashboard enums v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskSeverity, RiskBlockReason, RiskDashboardScorecardGrade,
    DrawdownLevel, LosingStreakLevel, ConcentrationLevel, ExposureComplianceStatus,
    get_all_enum_names,
)


class TestRiskStatus:
    def test_has_pass(self):
        assert RiskStatus.PASS.value == "PASS"

    def test_has_watch(self):
        assert RiskStatus.WATCH.value == "WATCH"

    def test_has_warning(self):
        assert RiskStatus.WARNING.value == "WARNING"

    def test_has_degraded(self):
        assert RiskStatus.DEGRADED.value == "DEGRADED"

    def test_has_blocked(self):
        assert RiskStatus.BLOCKED.value == "BLOCKED"

    def test_count_5(self):
        assert len(RiskStatus) == 5


class TestRiskSeverity:
    def test_has_info(self):
        assert RiskSeverity.INFO.value == "INFO"

    def test_has_low(self):
        assert RiskSeverity.LOW.value == "LOW"

    def test_has_medium(self):
        assert RiskSeverity.MEDIUM.value == "MEDIUM"

    def test_has_high(self):
        assert RiskSeverity.HIGH.value == "HIGH"

    def test_has_critical(self):
        assert RiskSeverity.CRITICAL.value == "CRITICAL"

    def test_has_blocking(self):
        assert RiskSeverity.BLOCKING.value == "BLOCKING"

    def test_count_6(self):
        assert len(RiskSeverity) == 6


class TestRiskBlockReason:
    def test_has_single_trade_risk(self):
        assert RiskBlockReason.SINGLE_TRADE_RISK_EXCEEDS_BUDGET

    def test_has_position_too_large(self):
        assert RiskBlockReason.POSITION_TOO_LARGE

    def test_has_too_many_holdings(self):
        assert RiskBlockReason.TOO_MANY_HOLDINGS

    def test_has_total_exposure(self):
        assert RiskBlockReason.TOTAL_EXPOSURE_TOO_HIGH

    def test_has_cash_ratio(self):
        assert RiskBlockReason.CASH_RATIO_TOO_LOW

    def test_has_drawdown(self):
        assert RiskBlockReason.DRAWDOWN_LIMIT_BREACHED

    def test_has_losing_streak(self):
        assert RiskBlockReason.LOSING_STREAK_LIMIT_BREACHED

    def test_has_no_stop_loss(self):
        assert RiskBlockReason.NO_STOP_LOSS

    def test_has_stop_loss_coverage(self):
        assert RiskBlockReason.STOP_LOSS_COVERAGE_INCOMPLETE

    def test_has_theme_concentration(self):
        assert RiskBlockReason.THEME_CONCENTRATION_TOO_HIGH

    def test_has_sector_concentration(self):
        assert RiskBlockReason.SECTOR_CONCENTRATION_TOO_HIGH

    def test_has_training_cap(self):
        assert RiskBlockReason.TRAINING_CAP_EXCEEDED

    def test_has_margin(self):
        assert RiskBlockReason.MARGIN_NOT_ALLOWED

    def test_has_real_order(self):
        assert RiskBlockReason.REAL_ORDER_REQUESTED

    def test_has_broker(self):
        assert RiskBlockReason.BROKER_REQUESTED

    def test_has_regime_block(self):
        assert RiskBlockReason.MARKET_REGIME_RISK_BLOCK

    def test_has_safety_violation(self):
        assert RiskBlockReason.SAFETY_VIOLATION

    def test_count_17(self):
        assert len(RiskBlockReason) == 17


class TestRiskDashboardScorecardGrade:
    def test_has_a(self):
        assert RiskDashboardScorecardGrade.A.value == "A"

    def test_has_b(self):
        assert RiskDashboardScorecardGrade.B.value == "B"

    def test_has_c(self):
        assert RiskDashboardScorecardGrade.C.value == "C"

    def test_has_d(self):
        assert RiskDashboardScorecardGrade.D.value == "D"

    def test_has_f(self):
        assert RiskDashboardScorecardGrade.F.value == "F"

    def test_has_blocked(self):
        assert RiskDashboardScorecardGrade.BLOCKED.value == "BLOCKED"

    def test_no_aplus(self):
        assert not hasattr(RiskDashboardScorecardGrade, "A_PLUS")


class TestOtherEnums:
    def test_drawdown_level_4(self):
        assert len(DrawdownLevel) == 4

    def test_losing_streak_4(self):
        assert len(LosingStreakLevel) == 4

    def test_concentration_3(self):
        assert len(ConcentrationLevel) == 3

    def test_exposure_compliance_3(self):
        assert len(ExposureComplianceStatus) == 3

    def test_get_all_enum_names_8(self):
        assert len(get_all_enum_names()) == 8

    def test_get_all_enum_names_contains_risk_status(self):
        assert "RiskStatus" in get_all_enum_names()
