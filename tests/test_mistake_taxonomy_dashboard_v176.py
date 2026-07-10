"""tests/test_mistake_taxonomy_dashboard_v176.py — v1.7.6 dashboard tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, BehaviorRiskLevel,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import classify_event
from paper_trading.small_capital_strategy.mistake_taxonomy_dashboard_v176 import build_dashboard


def _ev(cat, date="2026-01-05", cost=0.0):
    return classify_event("2330", date, cat, cost)


class TestBuildDashboard:
    def test_empty_events_paper_only(self):
        dash = build_dashboard([], total_trades=0)
        assert dash.paper_only is True

    def test_empty_events_zero_events_count(self):
        dash = build_dashboard([], total_trades=0)
        assert dash.events_count == 0

    def test_one_event_events_count_one(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)]
        dash = build_dashboard(evts, total_trades=1)
        assert dash.events_count == 1

    def test_entries_count_set(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)]
        dash = build_dashboard(evts, total_trades=3)
        assert dash.entries_count == 3

    def test_behavior_score_not_none(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)]
        dash = build_dashboard(evts, total_trades=1)
        assert dash.behavior_score is not None

    def test_behavior_score_paper_only(self):
        dash = build_dashboard([], total_trades=1)
        assert dash.behavior_score.paper_only is True

    def test_margin_attempt_blocked(self):
        evts = [_ev(MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT)]
        dash = build_dashboard(evts, total_trades=1)
        assert dash.behavior_score.level == BehaviorRiskLevel.BLOCKED

    def test_top_actions_list(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)]
        dash = build_dashboard(evts, total_trades=1)
        assert isinstance(dash.top_actions, list)

    def test_schema_version_176(self):
        dash = build_dashboard([], total_trades=0)
        assert dash.schema_version == "176"

    def test_weekly_result_optional(self):
        dash = build_dashboard([], weekly_result=None, total_trades=0)
        assert dash.weekly_result is None

    def test_monthly_result_optional(self):
        dash = build_dashboard([], monthly_result=None, total_trades=0)
        assert dash.monthly_result is None

    def test_not_investment_advice(self):
        dash = build_dashboard([], total_trades=0)
        assert dash.not_investment_advice is True
