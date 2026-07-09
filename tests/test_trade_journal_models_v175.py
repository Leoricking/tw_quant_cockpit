"""
tests/test_trade_journal_models_v175.py
Tests for Trade Journal models v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    TradeJournalEntry, TradeDecisionSnapshot, EntryReviewResult, ExitReviewResult,
    ABCExecutionReview, WatchlistConversionReview, RiskViolationReview,
    RegimeOutcomeReview, MistakeTaxonomyResult, ReviewScorecard,
    TradeJournalDashboard, TradeJournalReport, TradeJournalHealthSummary,
)

_SCHEMA = "175"
_POLICY = "1.7.5-small-account-trade-journal"


class TestTradeJournalEntry:
    def test_paper_only(self):
        assert TradeJournalEntry().paper_only is True

    def test_research_only(self):
        assert TradeJournalEntry().research_only is True

    def test_no_real_orders(self):
        assert TradeJournalEntry().no_real_orders is True

    def test_no_broker(self):
        assert TradeJournalEntry().no_broker is True

    def test_not_investment_advice(self):
        assert TradeJournalEntry().not_investment_advice is True

    def test_schema_version(self):
        assert TradeJournalEntry().schema_version == _SCHEMA

    def test_policy_version(self):
        assert TradeJournalEntry().policy_version == _POLICY

    def test_created_at_not_empty(self):
        assert TradeJournalEntry().created_at != ""

    def test_default_entry_price(self):
        assert TradeJournalEntry().entry_price == 0.0

    def test_default_symbol_empty(self):
        assert TradeJournalEntry().symbol == ""


class TestTradeDecisionSnapshot:
    def test_paper_only(self):
        assert TradeDecisionSnapshot().paper_only is True

    def test_no_broker(self):
        assert TradeDecisionSnapshot().no_broker is True

    def test_default_risk(self):
        assert TradeDecisionSnapshot().risk_per_trade_twd == 3000.0

    def test_schema_version(self):
        assert TradeDecisionSnapshot().schema_version == _SCHEMA


class TestEntryReviewResult:
    def test_paper_only(self):
        assert EntryReviewResult().paper_only is True

    def test_no_broker(self):
        assert EntryReviewResult().no_broker is True

    def test_default_score_zero(self):
        assert EntryReviewResult().entry_score == 0.0

    def test_schema_version(self):
        assert EntryReviewResult().schema_version == _SCHEMA


class TestExitReviewResult:
    def test_paper_only(self):
        assert ExitReviewResult().paper_only is True

    def test_no_broker(self):
        assert ExitReviewResult().no_broker is True

    def test_default_score_zero(self):
        assert ExitReviewResult().exit_score == 0.0


class TestABCExecutionReview:
    def test_paper_only(self):
        assert ABCExecutionReview().paper_only is True

    def test_no_broker(self):
        assert ABCExecutionReview().no_broker is True

    def test_default_execution_score(self):
        assert ABCExecutionReview().execution_score == 0.0


class TestWatchlistConversionReview:
    def test_paper_only(self):
        assert WatchlistConversionReview().paper_only is True

    def test_no_broker(self):
        assert WatchlistConversionReview().no_broker is True

    def test_default_tier_zero(self):
        assert WatchlistConversionReview().watchlist_tier == 0


class TestRiskViolationReview:
    def test_paper_only(self):
        assert RiskViolationReview().paper_only is True

    def test_no_broker(self):
        assert RiskViolationReview().no_broker is True

    def test_default_oversize_false(self):
        assert RiskViolationReview().oversize_detected is False

    def test_default_no_stop_loss_false(self):
        assert RiskViolationReview().no_stop_loss_detected is False


class TestRegimeOutcomeReview:
    def test_paper_only(self):
        assert RegimeOutcomeReview().paper_only is True

    def test_no_broker(self):
        assert RegimeOutcomeReview().no_broker is True

    def test_default_trade_count(self):
        assert RegimeOutcomeReview().trade_count == 0

    def test_default_win_rate_zero(self):
        assert RegimeOutcomeReview().win_rate_pct == 0.0


class TestMistakeTaxonomyResult:
    def test_paper_only(self):
        assert MistakeTaxonomyResult().paper_only is True

    def test_no_broker(self):
        assert MistakeTaxonomyResult().no_broker is True

    def test_default_severity_zero(self):
        assert MistakeTaxonomyResult().severity_score == 0.0

    def test_default_categories_empty(self):
        assert MistakeTaxonomyResult().mistake_categories == []


class TestReviewScorecard:
    def test_paper_only(self):
        assert ReviewScorecard().paper_only is True

    def test_no_broker(self):
        assert ReviewScorecard().no_broker is True

    def test_default_grade_f(self):
        assert ReviewScorecard().grade == "F"

    def test_weights_sum_100(self):
        assert ReviewScorecard().weights_sum == 100

    def test_no_aplus_grade(self):
        assert ReviewScorecard().grade != "A+"


class TestTradeJournalDashboard:
    def test_paper_only(self):
        assert TradeJournalDashboard().paper_only is True

    def test_no_broker(self):
        assert TradeJournalDashboard().no_broker is True

    def test_default_entries_zero(self):
        assert TradeJournalDashboard().entries_count == 0

    def test_default_win_rate_zero(self):
        assert TradeJournalDashboard().win_rate_pct == 0.0


class TestTradeJournalReport:
    def test_paper_only(self):
        assert TradeJournalReport().paper_only is True

    def test_no_broker(self):
        assert TradeJournalReport().no_broker is True

    def test_default_format_json(self):
        assert TradeJournalReport().report_format == "JSON"

    def test_default_sections_empty(self):
        assert TradeJournalReport().sections == {}


class TestTradeJournalHealthSummary:
    def test_paper_only(self):
        assert TradeJournalHealthSummary().paper_only is True

    def test_no_broker(self):
        assert TradeJournalHealthSummary().no_broker is True

    def test_default_all_passed_false(self):
        assert TradeJournalHealthSummary().all_passed is False

    def test_default_status_fail(self):
        assert TradeJournalHealthSummary().status == "FAIL"
