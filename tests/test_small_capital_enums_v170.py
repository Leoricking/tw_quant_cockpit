"""tests/test_small_capital_enums_v170.py — enum tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.enums_v170 import (
    BuyPointType, MarketRegime, AllocationBucket, SmallCapitalGrade,
    WatchlistTier, ThemeStrength, ForbiddenTradeReason, StrategyTemplateStatus,
    StopLossType, TakeProfitType, CashControlMode, TradePermissionStatus,
    EntryPlanStatus, ExitPlanStatus, CapitalProfileType, RiskBudgetType,
    PositionSizingMode, RiskLevel, ValidationSeverity,
)


def test_buy_point_a_exists():
    assert BuyPointType.A_10MA_PULLBACK is not None


def test_buy_point_b_exists():
    assert BuyPointType.B_PLATFORM_BREAKOUT is not None


def test_buy_point_c_exists():
    assert BuyPointType.C_20MA_RECLAIM is not None


def test_buy_point_unsupported_exists():
    assert BuyPointType.UNSUPPORTED is not None


def test_market_regime_bull():
    assert MarketRegime.BULL.value == "BULL"


def test_market_regime_bear():
    assert MarketRegime.BEAR.value == "BEAR"


def test_market_regime_range():
    assert MarketRegime.RANGE.value == "RANGE"


def test_market_regime_risk_off():
    assert MarketRegime.RISK_OFF.value == "RISK_OFF"


def test_market_regime_unknown():
    assert MarketRegime.UNKNOWN.value == "UNKNOWN"


def test_allocation_bucket_core():
    assert AllocationBucket.CORE is not None


def test_allocation_bucket_main_theme_swing():
    assert AllocationBucket.MAIN_THEME_SWING is not None


def test_allocation_bucket_second_wave():
    assert AllocationBucket.SECOND_WAVE_SETUP is not None


def test_allocation_bucket_short_term():
    assert AllocationBucket.SHORT_TERM_TRAINING is not None


def test_allocation_bucket_cash():
    assert AllocationBucket.CASH is not None


def test_grade_a():
    assert SmallCapitalGrade.A.value == "A"


def test_grade_b():
    assert SmallCapitalGrade.B.value == "B"


def test_grade_c():
    assert SmallCapitalGrade.C.value == "C"


def test_grade_d():
    assert SmallCapitalGrade.D.value == "D"


def test_grade_f():
    assert SmallCapitalGrade.F.value == "F"


def test_grade_blocked():
    assert SmallCapitalGrade.BLOCKED.value == "BLOCKED"


def test_watchlist_tier_core():
    assert WatchlistTier.CORE is not None


def test_watchlist_tier_main_theme():
    assert WatchlistTier.MAIN_THEME is not None


def test_watchlist_tier_excluded():
    assert WatchlistTier.EXCLUDED is not None


def test_theme_strength_strong():
    assert ThemeStrength.STRONG is not None


def test_theme_strength_moderate():
    assert ThemeStrength.MODERATE is not None


def test_theme_strength_weak():
    assert ThemeStrength.WEAK is not None


def test_theme_strength_none():
    assert ThemeStrength.NONE is not None


def test_forbidden_reason_margin():
    assert ForbiddenTradeReason.MARGIN_NOT_ALLOWED is not None


def test_forbidden_reason_day_trading():
    assert ForbiddenTradeReason.DAY_TRADING_AS_PRIMARY_NOT_ALLOWED is not None


def test_forbidden_reason_position_too_large():
    assert ForbiddenTradeReason.POSITION_TOO_LARGE is not None


def test_forbidden_reason_too_many_holdings():
    assert ForbiddenTradeReason.TOO_MANY_HOLDINGS is not None


def test_forbidden_reason_financing_overheated():
    assert ForbiddenTradeReason.FINANCING_OVERHEATED is not None


def test_strategy_template_status_active():
    assert StrategyTemplateStatus.ACTIVE is not None


def test_strategy_template_status_draft():
    assert StrategyTemplateStatus.DRAFT is not None


def test_stop_loss_type_ma_based():
    assert StopLossType.MA_BASED is not None


def test_stop_loss_type_swing_low():
    assert StopLossType.SWING_LOW is not None


def test_stop_loss_type_platform():
    assert StopLossType.PLATFORM is not None


def test_stop_loss_type_fixed_pct():
    assert StopLossType.FIXED_PCT is not None


def test_take_profit_type_staged():
    assert TakeProfitType.STAGED is not None


def test_take_profit_type_gain_target():
    assert TakeProfitType.GAIN_TARGET is not None


def test_cash_control_mode_bull():
    assert CashControlMode.BULL is not None


def test_cash_control_mode_bear():
    assert CashControlMode.BEAR is not None


def test_trade_permission_allowed():
    assert TradePermissionStatus.ALLOWED is not None


def test_trade_permission_blocked():
    assert TradePermissionStatus.BLOCKED is not None


def test_entry_plan_status_valid():
    assert EntryPlanStatus.VALID is not None


def test_entry_plan_status_blocked():
    assert EntryPlanStatus.BLOCKED is not None


def test_exit_plan_status_active():
    assert ExitPlanStatus.ACTIVE is not None


def test_capital_profile_type_small_300k():
    assert CapitalProfileType.SMALL_300K is not None


def test_risk_budget_type_standard():
    assert RiskBudgetType.STANDARD is not None


def test_position_sizing_mode_risk_based():
    assert PositionSizingMode.RISK_BASED is not None


def test_risk_level_low():
    assert RiskLevel.LOW is not None


def test_risk_level_blocked():
    assert RiskLevel.BLOCKED is not None


def test_validation_severity_error():
    assert ValidationSeverity.ERROR is not None
