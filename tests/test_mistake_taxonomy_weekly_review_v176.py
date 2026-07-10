"""tests/test_mistake_taxonomy_weekly_review_v176.py — v1.7.6 weekly review tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, BehaviorRiskLevel,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import classify_event
from paper_trading.small_capital_strategy.mistake_taxonomy_weekly_review_v176 import (
    run_weekly_review, create_weekly_input,
)


def _ev(cat, date="2026-01-05", cost=0.0):
    return classify_event("2330", date, cat, cost)


class TestCreateWeeklyInput:
    def test_paper_only_true(self):
        wi = create_weekly_input("2026-01-05", "2026-01-09", [], 3)
        assert wi.paper_only is True

    def test_week_start_set(self):
        wi = create_weekly_input("2026-01-05", "2026-01-09", [], 3)
        assert wi.week_start == "2026-01-05"

    def test_week_end_set(self):
        wi = create_weekly_input("2026-01-05", "2026-01-09", [], 3)
        assert wi.week_end == "2026-01-09"

    def test_total_trades_set(self):
        wi = create_weekly_input("2026-01-05", "2026-01-09", [], 3)
        assert wi.total_trades == 3

    def test_events_stored(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS)]
        wi = create_weekly_input("2026-01-05", "2026-01-09", evts, 1)
        assert len(wi.events) == 1


class TestRunWeeklyReview:
    def test_empty_events_paper_only(self):
        wi = create_weekly_input("2026-01-05", "2026-01-09", [], 3)
        wr = run_weekly_review(wi)
        assert wr.paper_only is True

    def test_empty_events_zero_total(self):
        wi = create_weekly_input("2026-01-05", "2026-01-09", [], 3)
        wr = run_weekly_review(wi)
        assert wr.total_events == 0

    def test_empty_events_pass_level(self):
        wi = create_weekly_input("2026-01-05", "2026-01-09", [], 3)
        wr = run_weekly_review(wi)
        assert wr.risk_level == BehaviorRiskLevel.PASS

    def test_one_event_total_events_one(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)]
        wi = create_weekly_input("2026-01-05", "2026-01-09", evts, 1)
        wr = run_weekly_review(wi)
        assert wr.total_events == 1

    def test_week_start_preserved(self):
        wi = create_weekly_input("2026-01-05", "2026-01-09", [], 3)
        wr = run_weekly_review(wi)
        assert wr.week_start == "2026-01-05"

    def test_week_end_preserved(self):
        wi = create_weekly_input("2026-01-05", "2026-01-09", [], 3)
        wr = run_weekly_review(wi)
        assert wr.week_end == "2026-01-09"

    def test_top_mistakes_list(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)]
        wi = create_weekly_input("2026-01-05", "2026-01-09", evts, 1)
        wr = run_weekly_review(wi)
        assert isinstance(wr.top_mistakes, list)

    def test_actions_list_with_events(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)]
        wi = create_weekly_input("2026-01-05", "2026-01-09", evts, 1)
        wr = run_weekly_review(wi)
        assert isinstance(wr.actions, list)
        assert len(wr.actions) >= 1

    def test_summary_not_empty(self):
        wi = create_weekly_input("2026-01-05", "2026-01-09", [], 3)
        wr = run_weekly_review(wi)
        assert len(wr.summary) > 0

    def test_margin_attempt_blocked(self):
        evts = [_ev(MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT)]
        wi = create_weekly_input("2026-01-05", "2026-01-09", evts, 1)
        wr = run_weekly_review(wi)
        assert wr.risk_level == BehaviorRiskLevel.BLOCKED

    def test_cost_summary_paper_only(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)]
        wi = create_weekly_input("2026-01-05", "2026-01-09", evts, 1)
        wr = run_weekly_review(wi)
        assert wr.cost_summary is not None
        assert wr.cost_summary.paper_only is True

    def test_schema_version_176(self):
        wi = create_weekly_input("2026-01-05", "2026-01-09", [], 3)
        wr = run_weekly_review(wi)
        assert wr.schema_version == "176"
