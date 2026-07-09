"""
tests/test_trade_journal_entry_v175.py
Tests for Trade Journal entry functions v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    TradeDirection, TradeOutcome, ABCPattern, JournalEntryStatus,
)
from paper_trading.small_capital_strategy.trade_journal_entry_v175 import (
    create_journal_entry, close_journal_entry, validate_entry,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import TradeJournalEntry


def _make_entry(symbol="2330", direction=TradeDirection.LONG, entry_date="2026-01-05",
                entry_price=580.0, size=50000.0, sl_price=552.0, sl_pct=0.05,
                abc=ABCPattern.B_BREAKOUT, regime="BULL", tier=1):
    return create_journal_entry(symbol, direction, entry_date, entry_price, size,
                                sl_price, sl_pct, abc, regime, tier)


class TestCreateJournalEntry:
    def test_returns_journal_entry(self):
        e = _make_entry()
        assert isinstance(e, TradeJournalEntry)

    def test_symbol_set(self):
        e = _make_entry(symbol="2454")
        assert e.symbol == "2454"

    def test_direction_long(self):
        e = _make_entry(direction=TradeDirection.LONG)
        assert e.direction == TradeDirection.LONG

    def test_entry_date_set(self):
        e = _make_entry(entry_date="2026-02-10")
        assert e.entry_date == "2026-02-10"

    def test_entry_price_set(self):
        e = _make_entry(entry_price=300.0)
        assert e.entry_price == 300.0

    def test_position_size_set(self):
        e = _make_entry(size=60000.0)
        assert e.position_size_twd == 60000.0

    def test_stop_loss_price_set(self):
        e = _make_entry(sl_price=540.0)
        assert e.stop_loss_price == 540.0

    def test_stop_loss_pct_set(self):
        e = _make_entry(sl_pct=0.07)
        assert e.stop_loss_pct == 0.07

    def test_abc_pattern_set(self):
        e = _make_entry(abc=ABCPattern.C_RECLAIM)
        assert e.abc_pattern == ABCPattern.C_RECLAIM

    def test_market_regime_set(self):
        e = _make_entry(regime="RANGE")
        assert e.market_regime == "RANGE"

    def test_watchlist_tier_set(self):
        e = _make_entry(tier=2)
        assert e.watchlist_tier == 2

    def test_status_open(self):
        e = _make_entry()
        assert e.status == JournalEntryStatus.OPEN

    def test_outcome_open(self):
        e = _make_entry()
        assert e.outcome == TradeOutcome.OPEN

    def test_paper_only_true(self):
        e = _make_entry()
        assert e.paper_only is True

    def test_no_real_orders_true(self):
        e = _make_entry()
        assert e.no_real_orders is True

    def test_no_broker_true(self):
        e = _make_entry()
        assert e.no_broker is True

    def test_not_investment_advice_true(self):
        e = _make_entry()
        assert e.not_investment_advice is True


class TestCloseJournalEntry:
    def _closed_win(self):
        e = _make_entry(entry_price=580.0)
        return close_journal_entry(e, "2026-01-20", 638.0)

    def _closed_loss(self):
        e = _make_entry(entry_price=580.0)
        return close_journal_entry(e, "2026-01-20", 540.0)

    def _closed_breakeven(self):
        e = _make_entry(entry_price=580.0)
        return close_journal_entry(e, "2026-01-20", 580.0)

    def test_win_outcome(self):
        assert self._closed_win().outcome == TradeOutcome.WIN

    def test_loss_outcome(self):
        assert self._closed_loss().outcome == TradeOutcome.LOSS

    def test_breakeven_outcome(self):
        assert self._closed_breakeven().outcome == TradeOutcome.BREAKEVEN

    def test_status_closed_after_close(self):
        assert self._closed_win().status == JournalEntryStatus.CLOSED

    def test_exit_date_set(self):
        e = self._closed_win()
        assert e.exit_date == "2026-01-20"

    def test_exit_price_set(self):
        e = self._closed_win()
        assert e.exit_price == 638.0

    def test_short_loss_on_price_up(self):
        e = create_journal_entry("2330", TradeDirection.SHORT, "2026-01-05",
                                 580.0, 50000.0, 610.0, 0.05)
        closed = close_journal_entry(e, "2026-01-20", 620.0)
        assert closed.outcome == TradeOutcome.LOSS

    def test_short_win_on_price_down(self):
        e = create_journal_entry("2330", TradeDirection.SHORT, "2026-01-05",
                                 580.0, 50000.0, 610.0, 0.05)
        closed = close_journal_entry(e, "2026-01-20", 520.0)
        assert closed.outcome == TradeOutcome.WIN


class TestValidateEntry:
    def test_valid_entry_true(self):
        e = _make_entry()
        assert validate_entry(e) is True

    def test_empty_symbol_false(self):
        e = _make_entry(symbol="")
        assert validate_entry(e) is False

    def test_zero_entry_price_false(self):
        e = _make_entry(entry_price=0.0)
        assert validate_entry(e) is False

    def test_empty_entry_date_false(self):
        e = create_journal_entry("2330", TradeDirection.LONG, "", 580.0, 50000.0, 552.0, 0.05)
        assert validate_entry(e) is False
