"""
tests/test_trade_journal_review_entry_v175.py
Tests for Trade Journal entry review v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    TradeDirection, ABCPattern, EntryQuality, ReviewStatus,
)
from paper_trading.small_capital_strategy.trade_journal_entry_v175 import create_journal_entry
from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    TradeDecisionSnapshot, EntryReviewResult,
)
from paper_trading.small_capital_strategy.trade_journal_review_entry_v175 import (
    review_entry, score_entry,
)


def _entry(regime="BULL", tier=1, sl_pct=0.05, sl_price=552.0):
    return create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                580.0, 50000.0, sl_price, sl_pct,
                                ABCPattern.B_BREAKOUT, regime, tier)


def _snap(trigger="B_BREAKOUT", regime="BULL", sl_pct=0.05, size=50000.0, tier=1):
    return TradeDecisionSnapshot(entry_trigger=trigger, market_regime=regime,
                                 stop_loss_pct=sl_pct, position_size_twd=size,
                                 watchlist_tier=tier)


class TestScoreEntry:
    def test_perfect_score_100(self):
        e = _entry(regime="BULL", tier=1, sl_pct=0.05, sl_price=552.0)
        s = _snap(trigger="B_BREAKOUT", regime="BULL")
        assert score_entry(e, s) == 100.0

    def test_score_range_0_100(self):
        e = _entry()
        s = score_entry(e)
        assert 0 <= s <= 100

    def test_no_trigger_reduces_score(self):
        e = _entry(regime="BULL", tier=1, sl_pct=0.05, sl_price=552.0)
        s_no_trigger = score_entry(e, _snap(trigger=""))
        s_with_trigger = score_entry(e, _snap(trigger="B_BREAKOUT"))
        assert s_with_trigger > s_no_trigger

    def test_bear_regime_lower_score(self):
        e_bull = _entry(regime="BULL")
        e_bear = _entry(regime="BEAR")
        assert score_entry(e_bull) >= score_entry(e_bear)

    def test_no_watchlist_reduces_score(self):
        e_tier1 = _entry(tier=1)
        e_tier0 = _entry(tier=0)
        assert score_entry(e_tier1) > score_entry(e_tier0)

    def test_no_stop_loss_reduces_score(self):
        e_with_sl = _entry(sl_pct=0.05, sl_price=552.0)
        e_no_sl   = _entry(sl_pct=0.0, sl_price=0.0)
        assert score_entry(e_with_sl) > score_entry(e_no_sl)


class TestReviewEntry:
    def _full_review(self):
        e = _entry(regime="BULL", tier=1, sl_pct=0.05, sl_price=552.0)
        s = _snap(trigger="B_BREAKOUT", regime="BULL", sl_pct=0.05, tier=1)
        return review_entry(e, s)

    def test_returns_entry_review_result(self):
        assert isinstance(self._full_review(), EntryReviewResult)

    def test_perfect_entry_ideal_quality(self):
        assert self._full_review().entry_quality == EntryQuality.IDEAL

    def test_perfect_entry_pass_status(self):
        assert self._full_review().review_status == ReviewStatus.PASS

    def test_paper_only_true(self):
        assert self._full_review().paper_only is True

    def test_no_broker_true(self):
        assert self._full_review().no_broker is True

    def test_not_investment_advice_true(self):
        assert self._full_review().not_investment_advice is True

    def test_symbol_preserved(self):
        assert self._full_review().symbol == "2330"

    def test_entry_date_preserved(self):
        assert self._full_review().entry_date == "2026-01-05"

    def test_stop_loss_set_true(self):
        assert self._full_review().stop_loss_set is True

    def test_watchlist_confirmed_true(self):
        assert self._full_review().watchlist_confirmed is True

    def test_regime_aligned_true(self):
        assert self._full_review().regime_aligned is True

    def test_trigger_met_true(self):
        assert self._full_review().trigger_met is True

    def test_poor_entry_fail_status(self):
        e = _entry(regime="BEAR", tier=0, sl_pct=0.0, sl_price=0.0)
        result = review_entry(e, _snap(trigger="", regime="BEAR"))
        assert result.review_status == ReviewStatus.FAIL

    def test_no_snap_still_returns_result(self):
        e = _entry()
        result = review_entry(e, None)
        assert isinstance(result, EntryReviewResult)

    def test_score_positive_for_good_entry(self):
        r = self._full_review()
        assert r.entry_score > 0

    def test_schema_version(self):
        r = self._full_review()
        assert r.schema_version == "175"
