"""tests/test_abc_enums_v172.py — Enum tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
    ABCBuyPointType, ABCExecutionStatus, ABCConditionStatus,
    ABCEntryMode, ABCAddMode, ABCStopLossMode, ABCTakeProfitMode,
    ABCInvalidationReason, ABCExecutionGrade, ABCRiskPermission,
    ABCPaperOrderIntentType, ABCExecutionBlockReason, ABCExecutionWarningReason,
    ABCMarketCompatibility, ABCWatchlistCompatibility, ValidationSeverity,
    get_all_enum_names,
)


def test_buy_point_type_a():
    assert ABCBuyPointType.A_10MA_PULLBACK.value == "A_10MA_PULLBACK"


def test_buy_point_type_b():
    assert ABCBuyPointType.B_PLATFORM_BREAKOUT.value == "B_PLATFORM_BREAKOUT"


def test_buy_point_type_c():
    assert ABCBuyPointType.C_20MA_RECLAIM.value == "C_20MA_RECLAIM"


def test_buy_point_type_unsupported():
    assert ABCBuyPointType.UNSUPPORTED.value == "UNSUPPORTED"


def test_execution_status_ready():
    assert ABCExecutionStatus.READY.value == "READY"


def test_execution_status_blocked():
    assert ABCExecutionStatus.BLOCKED.value == "BLOCKED"


def test_execution_status_invalidated():
    assert ABCExecutionStatus.INVALIDATED.value == "INVALIDATED"


def test_execution_status_waiting():
    assert ABCExecutionStatus.WAITING_CONFIRMATION.value == "WAITING_CONFIRMATION"


def test_condition_status_met():
    assert ABCConditionStatus.MET.value == "MET"


def test_entry_mode_ma10_reclaim():
    assert ABCEntryMode.MA10_RECLAIM.value == "MA10_RECLAIM"


def test_entry_mode_breakout():
    assert ABCEntryMode.BREAKOUT_CONFIRMATION.value == "BREAKOUT_CONFIRMATION"


def test_entry_mode_ma20_reclaim():
    assert ABCEntryMode.MA20_RECLAIM.value == "MA20_RECLAIM"


def test_grade_no_a_plus():
    assert not hasattr(ABCExecutionGrade, "A_PLUS")


def test_grade_a():
    assert ABCExecutionGrade.A.value == "A"


def test_grade_blocked():
    assert ABCExecutionGrade.BLOCKED.value == "BLOCKED"


def test_paper_buy_intent():
    assert ABCPaperOrderIntentType.PAPER_BUY.value == "PAPER_BUY"


def test_paper_block_intent():
    assert ABCPaperOrderIntentType.PAPER_BLOCK.value == "PAPER_BLOCK"


def test_block_reason_real_order():
    assert ABCExecutionBlockReason.REAL_ORDER_REQUESTED.value == "REAL_ORDER_REQUESTED"


def test_block_reason_no_stop_loss():
    assert ABCExecutionBlockReason.NO_STOP_LOSS.value == "NO_STOP_LOSS"


def test_block_reason_watchlist_excluded():
    assert ABCExecutionBlockReason.WATCHLIST_EXCLUDED.value == "WATCHLIST_EXCLUDED"


def test_market_compat_compatible():
    assert ABCMarketCompatibility.COMPATIBLE.value == "COMPATIBLE"


def test_watchlist_compat_blocked():
    assert ABCWatchlistCompatibility.BLOCKED.value == "BLOCKED"


def test_validation_severity_critical():
    assert ValidationSeverity.CRITICAL.value == "CRITICAL"


def test_get_all_enum_names_count_16():
    assert len(get_all_enum_names()) == 16


def test_get_all_enum_names_contains_buy_point_type():
    assert "ABCBuyPointType" in get_all_enum_names()


def test_all_enum_classes_str_enum():
    for bpt in ABCBuyPointType:
        assert isinstance(bpt.value, str)
