"""
tests/test_trade_journal_dashboard_v175.py
Tests for Trade Journal dashboard v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection
from paper_trading.small_capital_strategy.trade_journal_entry_v175 import (
    create_journal_entry, close_journal_entry,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import TradeJournalDashboard
from paper_trading.small_capital_strategy.trade_journal_dashboard_v175 import build_dashboard


def _win():
    e = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                             580.0, 50000.0, 552.0, 0.05,
                             market_regime="BULL")
    return close_journal_entry(e, "2026-01-20", 638.0)


def _loss():
    e = create_journal_entry("2317", TradeDirection.LONG, "2026-01-06",
                             100.0, 50000.0, 95.0, 0.05,
                             market_regime="BULL")
    return close_journal_entry(e, "2026-01-20", 90.0)


def _open_entry():
    return create_journal_entry("2454", TradeDirection.LONG, "2026-01-07",
                                180.0, 50000.0, 171.0, 0.05)


class TestBuildDashboard:
    def test_returns_trade_journal_dashboard(self):
        assert isinstance(build_dashboard([_win()]), TradeJournalDashboard)

    def test_empty_entries(self):
        d = build_dashboard([])
        assert d.entries_count == 0
        assert d.win_rate_pct == 0.0

    def test_entries_count_correct(self):
        d = build_dashboard([_win(), _loss(), _open_entry()])
        assert d.entries_count == 3

    def test_open_count_correct(self):
        d = build_dashboard([_win(), _open_entry()])
        assert d.open_count == 1

    def test_closed_count_correct(self):
        d = build_dashboard([_win(), _loss(), _open_entry()])
        assert d.closed_count == 2

    def test_win_count_correct(self):
        d = build_dashboard([_win(), _loss()])
        assert d.win_count == 1

    def test_loss_count_correct(self):
        d = build_dashboard([_win(), _loss()])
        assert d.loss_count == 1

    def test_win_rate_100_all_wins(self):
        d = build_dashboard([_win(), _win()])
        assert d.win_rate_pct == 100.0

    def test_win_rate_50_mixed(self):
        d = build_dashboard([_win(), _loss()])
        assert d.win_rate_pct == 50.0

    def test_paper_only_true(self):
        d = build_dashboard([_win()])
        assert d.paper_only is True

    def test_no_broker_true(self):
        d = build_dashboard([_win()])
        assert d.no_broker is True

    def test_not_investment_advice_true(self):
        d = build_dashboard([_win()])
        assert d.not_investment_advice is True

    def test_regime_reviews_not_empty(self):
        d = build_dashboard([_win()])
        assert len(d.regime_reviews) > 0

    def test_scorecard_paper_only(self):
        d = build_dashboard([_win()])
        assert d.scorecard.paper_only is True

    def test_schema_version(self):
        d = build_dashboard([_win()])
        assert d.schema_version == "175"

    def test_pnl_positive_for_win(self):
        d = build_dashboard([_win()])
        assert d.total_pnl_twd > 0

    def test_pnl_negative_for_loss(self):
        d = build_dashboard([_loss()])
        assert d.total_pnl_twd < 0

    def test_avg_return_positive_for_win(self):
        d = build_dashboard([_win()])
        assert d.avg_return_pct > 0
