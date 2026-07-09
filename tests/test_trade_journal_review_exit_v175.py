"""
tests/test_trade_journal_review_exit_v175.py
Tests for Trade Journal exit review v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    TradeDirection, ExitQuality, ReviewStatus, JournalEntryStatus,
)
from paper_trading.small_capital_strategy.trade_journal_entry_v175 import (
    create_journal_entry, close_journal_entry,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import ExitReviewResult
from paper_trading.small_capital_strategy.trade_journal_review_exit_v175 import (
    review_exit, score_exit,
)


def _closed(exit_price=638.0, entry_price=580.0, sl_price=552.0, sl_pct=0.05):
    e = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                             entry_price, 50000.0, sl_price, sl_pct)
    return close_journal_entry(e, "2026-01-20", exit_price)


def _open_entry():
    return create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                580.0, 50000.0, 552.0, 0.05)


class TestScoreExit:
    def test_win_at_target_high_score(self):
        e = _closed(exit_price=638.0, entry_price=580.0)  # ~10% gain
        assert score_exit(e) >= 75.0

    def test_loss_low_score(self):
        e = _closed(exit_price=520.0, entry_price=580.0)
        assert score_exit(e) < 50.0

    def test_open_entry_score_zero(self):
        e = _open_entry()
        assert score_exit(e) == 0.0

    def test_score_range_0_100(self):
        e = _closed()
        assert 0 <= score_exit(e) <= 100


class TestReviewExit:
    def test_returns_exit_review_result(self):
        e = _closed()
        assert isinstance(review_exit(e), ExitReviewResult)

    def test_win_at_target_ideal_quality(self):
        e = _closed(exit_price=640.0, entry_price=580.0)  # >10% gain
        result = review_exit(e)
        assert result.exit_quality == ExitQuality.IDEAL

    def test_target_reached_true_for_10pct_gain(self):
        e = _closed(exit_price=640.0, entry_price=580.0)
        result = review_exit(e)
        assert result.target_reached is True

    def test_target_reached_false_for_small_gain(self):
        e = _closed(exit_price=590.0, entry_price=580.0)
        result = review_exit(e)
        assert result.target_reached is False

    def test_stop_triggered_when_below_sl(self):
        e = _closed(exit_price=549.0, entry_price=580.0, sl_price=552.0)
        result = review_exit(e)
        assert result.stop_triggered is True

    def test_paper_only_true(self):
        result = review_exit(_closed())
        assert result.paper_only is True

    def test_no_broker_true(self):
        result = review_exit(_closed())
        assert result.no_broker is True

    def test_not_investment_advice_true(self):
        result = review_exit(_closed())
        assert result.not_investment_advice is True

    def test_symbol_preserved(self):
        result = review_exit(_closed())
        assert result.symbol == "2330"

    def test_open_entry_pending_status(self):
        e = _open_entry()
        result = review_exit(e)
        assert result.review_status == ReviewStatus.PENDING

    def test_win_pass_status(self):
        e = _closed(exit_price=640.0, entry_price=580.0)
        result = review_exit(e)
        assert result.review_status == ReviewStatus.PASS

    def test_schema_version(self):
        result = review_exit(_closed())
        assert result.schema_version == "175"

    def test_held_too_long_for_big_loss(self):
        e = _closed(exit_price=490.0, entry_price=580.0)
        result = review_exit(e)
        assert result.held_too_long is True
