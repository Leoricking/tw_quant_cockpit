"""
tests/test_trade_journal_integration_v175.py
Integration tests for Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_enums_v175 import (
    TradeDirection, ABCPattern, TradeOutcome, ReviewStatus, JournalEntryStatus,
)
from paper_trading.small_capital_strategy.trade_journal_entry_v175 import (
    create_journal_entry, close_journal_entry, validate_entry,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import TradeDecisionSnapshot
from paper_trading.small_capital_strategy.trade_journal_review_entry_v175 import review_entry
from paper_trading.small_capital_strategy.trade_journal_review_exit_v175 import review_exit
from paper_trading.small_capital_strategy.trade_journal_abc_review_v175 import review_abc_execution
from paper_trading.small_capital_strategy.trade_journal_risk_review_v175 import review_risk_violations
from paper_trading.small_capital_strategy.trade_journal_mistake_taxonomy_v175 import classify_mistakes
from paper_trading.small_capital_strategy.trade_journal_scorecard_v175 import build_scorecard
from paper_trading.small_capital_strategy.trade_journal_dashboard_v175 import build_dashboard
from paper_trading.small_capital_strategy.trade_journal_report_v175 import build_report


def _full_compliant_trade():
    """Create a fully compliant winning trade."""
    e = create_journal_entry(
        "2330", TradeDirection.LONG, "2026-01-05",
        580.0, 50000.0, 552.0, 0.05,
        ABCPattern.C_RECLAIM, "BULL", 1, "Full compliance trade"
    )
    return close_journal_entry(e, "2026-01-20", 638.0)


def _violation_trade():
    """Create a trade with violations."""
    e = create_journal_entry(
        "2317", TradeDirection.LONG, "2026-02-01",
        100.0, 100000.0, 0.0, 0.0,
        ABCPattern.UNKNOWN, "BEAR", 0, "Violation trade"
    )
    return close_journal_entry(e, "2026-02-15", 85.0)


class TestEndToEndCompliantTrade:
    def test_entry_valid(self):
        e = _full_compliant_trade()
        open_e = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                      580.0, 50000.0, 552.0, 0.05,
                                      ABCPattern.C_RECLAIM, "BULL", 1)
        assert validate_entry(open_e) is True

    def test_win_outcome(self):
        assert _full_compliant_trade().outcome == TradeOutcome.WIN

    def test_status_closed(self):
        assert _full_compliant_trade().status == JournalEntryStatus.CLOSED

    def test_entry_review_pass(self):
        e = _full_compliant_trade()
        snap = TradeDecisionSnapshot(entry_trigger="C_RECLAIM", market_regime="BULL",
                                     stop_loss_pct=0.05, position_size_twd=50000.0, watchlist_tier=1)
        r = review_entry(e, snap)
        assert r.review_status == ReviewStatus.PASS

    def test_exit_review_pass(self):
        r = review_exit(_full_compliant_trade())
        assert r.review_status == ReviewStatus.PASS

    def test_abc_review_pass(self):
        e = _full_compliant_trade()
        snap = TradeDecisionSnapshot(stop_loss_pct=0.05, position_size_twd=50000.0)
        r = review_abc_execution(e, snap)
        assert r.review_status == ReviewStatus.PASS

    def test_risk_review_pass(self):
        r = review_risk_violations(_full_compliant_trade())
        assert r.review_status == ReviewStatus.PASS

    def test_mistake_taxonomy_none(self):
        from paper_trading.small_capital_strategy.trade_journal_enums_v175 import MistakeCategory
        r = classify_mistakes(_full_compliant_trade())
        assert r.primary_mistake == MistakeCategory.NONE


class TestEndToEndViolationTrade:
    def test_violation_detected(self):
        r = review_risk_violations(_violation_trade())
        assert r.review_status in (ReviewStatus.WARN, ReviewStatus.FAIL)

    def test_loss_outcome(self):
        assert _violation_trade().outcome == TradeOutcome.LOSS

    def test_risk_review_violations_nonempty(self):
        r = review_risk_violations(_violation_trade())
        assert r.violation_type != "NONE"


class TestDashboardIntegration:
    def test_dashboard_with_mixed_entries(self):
        entries = [_full_compliant_trade(), _violation_trade()]
        d = build_dashboard(entries)
        assert d.entries_count == 2
        assert d.paper_only is True

    def test_report_from_dashboard(self):
        entries = [_full_compliant_trade()]
        d = build_dashboard(entries)
        r = build_report(d)
        assert r.paper_only is True
        assert len(r.sections) >= 13

    def test_scorecard_from_wins(self):
        entries = [_full_compliant_trade(), _full_compliant_trade()]
        sc = build_scorecard(entries)
        assert sc.win_rate_pct == 100.0
        assert sc.paper_only is True

    def test_all_models_paper_only(self):
        entries = [_full_compliant_trade(), _violation_trade()]
        d = build_dashboard(entries)
        assert d.paper_only is True
        assert d.scorecard.paper_only is True
        for r in d.regime_reviews:
            assert r.paper_only is True


class TestSafetyIntegration:
    def test_all_results_paper_only(self):
        e = _full_compliant_trade()
        snap = TradeDecisionSnapshot(entry_trigger="C_RECLAIM", market_regime="BULL",
                                     stop_loss_pct=0.05, position_size_twd=50000.0, watchlist_tier=1)
        er = review_entry(e, snap)
        xr = review_exit(e)
        rr = review_risk_violations(e)
        mt = classify_mistakes(e)
        assert er.paper_only is True
        assert xr.paper_only is True
        assert rr.paper_only is True
        assert mt.paper_only is True

    def test_no_real_orders_everywhere(self):
        e = _full_compliant_trade()
        assert e.no_real_orders is True
        rr = review_risk_violations(e)
        assert rr.no_real_orders is True

    def test_no_broker_everywhere(self):
        e = _full_compliant_trade()
        assert e.no_broker is True
        er = review_entry(e)
        assert er.no_broker is True
