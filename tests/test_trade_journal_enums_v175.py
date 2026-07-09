"""
tests/test_trade_journal_enums_v175.py
Tests for Trade Journal enums v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    TradeDirection, TradeOutcome, EntryQuality, ExitQuality,
    ABCPattern, MistakeCategory, ReviewStatus, JournalEntryStatus,
    get_all_enum_names,
)


class TestTradeDirection:
    def test_long_value(self):
        assert TradeDirection.LONG.value == "LONG"

    def test_short_value(self):
        assert TradeDirection.SHORT.value == "SHORT"

    def test_unknown_value(self):
        assert TradeDirection.UNKNOWN.value == "UNKNOWN"

    def test_count_3(self):
        assert len(TradeDirection) == 3


class TestTradeOutcome:
    def test_win(self):
        assert TradeOutcome.WIN.value == "WIN"

    def test_loss(self):
        assert TradeOutcome.LOSS.value == "LOSS"

    def test_breakeven(self):
        assert TradeOutcome.BREAKEVEN.value == "BREAKEVEN"

    def test_open(self):
        assert TradeOutcome.OPEN.value == "OPEN"

    def test_unknown(self):
        assert TradeOutcome.UNKNOWN.value == "UNKNOWN"

    def test_count_5(self):
        assert len(TradeOutcome) == 5


class TestEntryQuality:
    def test_ideal(self):
        assert EntryQuality.IDEAL.value == "IDEAL"

    def test_acceptable(self):
        assert EntryQuality.ACCEPTABLE.value == "ACCEPTABLE"

    def test_marginal(self):
        assert EntryQuality.MARGINAL.value == "MARGINAL"

    def test_poor(self):
        assert EntryQuality.POOR.value == "POOR"

    def test_unknown(self):
        assert EntryQuality.UNKNOWN.value == "UNKNOWN"

    def test_count_5(self):
        assert len(EntryQuality) == 5


class TestExitQuality:
    def test_ideal(self):
        assert ExitQuality.IDEAL.value == "IDEAL"

    def test_too_early(self):
        assert ExitQuality.TOO_EARLY.value == "TOO_EARLY"

    def test_too_late(self):
        assert ExitQuality.TOO_LATE.value == "TOO_LATE"

    def test_panic(self):
        assert ExitQuality.PANIC.value == "PANIC"

    def test_count_5(self):
        assert len(ExitQuality) == 5


class TestABCPattern:
    def test_a_pullback(self):
        assert ABCPattern.A_PULLBACK.value == "A_PULLBACK"

    def test_b_breakout(self):
        assert ABCPattern.B_BREAKOUT.value == "B_BREAKOUT"

    def test_c_reclaim(self):
        assert ABCPattern.C_RECLAIM.value == "C_RECLAIM"

    def test_unknown(self):
        assert ABCPattern.UNKNOWN.value == "UNKNOWN"

    def test_count_4(self):
        assert len(ABCPattern) == 4


class TestMistakeCategory:
    def test_none_value(self):
        assert MistakeCategory.NONE.value == "NONE"

    def test_fomo_value(self):
        assert MistakeCategory.FOMO.value == "FOMO"

    def test_no_stop_loss(self):
        assert MistakeCategory.NO_STOP_LOSS.value == "NO_STOP_LOSS"

    def test_count_10(self):
        assert len(MistakeCategory) == 10


class TestReviewStatus:
    def test_pass(self):
        assert ReviewStatus.PASS.value == "PASS"

    def test_warn(self):
        assert ReviewStatus.WARN.value == "WARN"

    def test_fail(self):
        assert ReviewStatus.FAIL.value == "FAIL"

    def test_pending(self):
        assert ReviewStatus.PENDING.value == "PENDING"

    def test_count_4(self):
        assert len(ReviewStatus) == 4


class TestJournalEntryStatus:
    def test_open(self):
        assert JournalEntryStatus.OPEN.value == "OPEN"

    def test_closed(self):
        assert JournalEntryStatus.CLOSED.value == "CLOSED"

    def test_cancelled(self):
        assert JournalEntryStatus.CANCELLED.value == "CANCELLED"

    def test_count_3(self):
        assert len(JournalEntryStatus) == 3


class TestGetAllEnumNames:
    def test_returns_list(self):
        assert isinstance(get_all_enum_names(), list)

    def test_count_8(self):
        assert len(get_all_enum_names()) == 8

    def test_contains_trade_direction(self):
        assert "TradeDirection" in get_all_enum_names()

    def test_contains_mistake_category(self):
        assert "MistakeCategory" in get_all_enum_names()
