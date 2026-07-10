"""tests/test_mistake_taxonomy_monthly_review_v176.py — v1.7.6 monthly review tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import MistakeCategory
from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import classify_event
from paper_trading.small_capital_strategy.mistake_taxonomy_weekly_review_v176 import (
    run_weekly_review, create_weekly_input,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_monthly_review_v176 import run_monthly_review


def _wr(week_start, week_end, events, total_trades=1):
    wi = create_weekly_input(week_start, week_end, events, total_trades)
    return run_weekly_review(wi)


def _ev(cat, date="2026-01-05", cost=0.0):
    return classify_event("2330", date, cat, cost)


class TestRunMonthlyReview:
    def test_empty_weeks_paper_only(self):
        mr = run_monthly_review("2026-01", [])
        assert mr.paper_only is True

    def test_empty_weeks_trend_stable(self):
        mr = run_monthly_review("2026-01", [])
        assert mr.behavior_trend == "STABLE"

    def test_empty_weeks_events_zero(self):
        mr = run_monthly_review("2026-01", [])
        assert mr.total_events == 0

    def test_month_label_set(self):
        mr = run_monthly_review("2026-01", [])
        assert mr.month_label == "2026-01"

    def test_single_week_total_events(self):
        wr = _wr("2026-01-05", "2026-01-09", [_ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)], 1)
        mr = run_monthly_review("2026-01", [wr])
        assert mr.total_events == 1

    def test_two_weeks_total_events_aggregated(self):
        wr1 = _wr("2026-01-05", "2026-01-09", [_ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)], 1)
        wr2 = _wr("2026-01-12", "2026-01-16", [_ev(MistakeCategory.FOMO_CHASE, cost=-2000.0)], 1)
        mr = run_monthly_review("2026-01", [wr1, wr2])
        assert mr.total_events == 2

    def test_trend_valid_value(self):
        wr = _wr("2026-01-05", "2026-01-09", [], 1)
        mr = run_monthly_review("2026-01", [wr])
        assert mr.behavior_trend in ("STABLE", "IMPROVING", "DETERIORATING")

    def test_worst_week_set(self):
        wr1 = _wr("2026-01-05", "2026-01-09", [], 1)
        wr2 = _wr("2026-01-12", "2026-01-16", [_ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)], 1)
        mr = run_monthly_review("2026-01", [wr1, wr2])
        assert len(mr.worst_week) > 0

    def test_weekly_results_stored(self):
        wr = _wr("2026-01-05", "2026-01-09", [], 1)
        mr = run_monthly_review("2026-01", [wr])
        assert len(mr.weekly_results) == 1

    def test_schema_version_176(self):
        mr = run_monthly_review("2026-01", [])
        assert mr.schema_version == "176"

    def test_avg_behavior_score_zero_for_clean_weeks(self):
        wr = _wr("2026-01-05", "2026-01-09", [], 1)
        mr = run_monthly_review("2026-01", [wr])
        assert mr.avg_behavior_score == 0.0

    def test_total_cost_aggregated(self):
        ev1 = classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0)
        ev2 = classify_event("2330", "2026-01-12", MistakeCategory.NO_STOP_LOSS, -3000.0)
        wr1 = _wr("2026-01-05", "2026-01-09", [ev1], 1)
        wr2 = _wr("2026-01-12", "2026-01-16", [ev2], 1)
        mr = run_monthly_review("2026-01", [wr1, wr2])
        assert mr.total_cost_twd == -8000.0
