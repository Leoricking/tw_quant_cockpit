"""tests/test_mistake_taxonomy_models_v176.py — v1.7.6 model tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_models_v176 import (
    MistakeTaxonomyRule, MistakeEvent, MistakeCostSummary,
    RepeatedMistakePattern, WeeklyReviewInput, WeeklyReviewResult,
    MonthlyReviewResult, BehaviorRiskScore, ImprovementAction,
    ReviewDashboard, ReviewHealthSummary,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, MistakeSeverity, BehaviorRiskLevel,
)


class TestMistakeTaxonomyRule:
    def test_paper_only_default(self):
        assert MistakeTaxonomyRule().paper_only is True

    def test_research_only_default(self):
        assert MistakeTaxonomyRule().research_only is True

    def test_no_real_orders_default(self):
        assert MistakeTaxonomyRule().no_real_orders is True

    def test_no_broker_default(self):
        assert MistakeTaxonomyRule().no_broker is True

    def test_schema_version_176(self):
        assert MistakeTaxonomyRule().schema_version == "176"


class TestMistakeEvent:
    def test_paper_only_default(self):
        assert MistakeEvent().paper_only is True

    def test_research_only_default(self):
        assert MistakeEvent().research_only is True

    def test_no_real_orders_default(self):
        assert MistakeEvent().no_real_orders is True

    def test_no_broker_default(self):
        assert MistakeEvent().no_broker is True

    def test_schema_version_176(self):
        assert MistakeEvent().schema_version == "176"

    def test_cost_twd_default_zero(self):
        assert MistakeEvent().cost_twd == 0.0


class TestMistakeCostSummary:
    def test_paper_only_default(self):
        assert MistakeCostSummary().paper_only is True

    def test_total_cost_default_zero(self):
        assert MistakeCostSummary().total_cost_twd == 0.0

    def test_event_count_default_zero(self):
        assert MistakeCostSummary().event_count == 0


class TestRepeatedMistakePattern:
    def test_paper_only_default(self):
        assert RepeatedMistakePattern().paper_only is True

    def test_count_default_zero(self):
        assert RepeatedMistakePattern().count == 0

    def test_dates_default_empty(self):
        assert RepeatedMistakePattern().dates == []


class TestWeeklyReviewInput:
    def test_paper_only_default(self):
        assert WeeklyReviewInput().paper_only is True

    def test_events_default_empty(self):
        assert WeeklyReviewInput().events == []

    def test_total_trades_default_zero(self):
        assert WeeklyReviewInput().total_trades == 0


class TestWeeklyReviewResult:
    def test_paper_only_default(self):
        assert WeeklyReviewResult().paper_only is True

    def test_risk_level_default_pass(self):
        assert WeeklyReviewResult().risk_level == BehaviorRiskLevel.PASS

    def test_total_events_default_zero(self):
        assert WeeklyReviewResult().total_events == 0

    def test_schema_version_176(self):
        assert WeeklyReviewResult().schema_version == "176"


class TestMonthlyReviewResult:
    def test_paper_only_default(self):
        assert MonthlyReviewResult().paper_only is True

    def test_behavior_trend_default_stable(self):
        assert MonthlyReviewResult().behavior_trend == "STABLE"

    def test_weekly_results_default_empty(self):
        assert MonthlyReviewResult().weekly_results == []


class TestBehaviorRiskScore:
    def test_paper_only_default(self):
        assert BehaviorRiskScore().paper_only is True

    def test_score_default_zero(self):
        assert BehaviorRiskScore().score == 0.0

    def test_level_default_pass(self):
        assert BehaviorRiskScore().level == BehaviorRiskLevel.PASS


class TestImprovementAction:
    def test_paper_only_default(self):
        assert ImprovementAction().paper_only is True

    def test_priority_default_3(self):
        assert ImprovementAction().priority == 3


class TestReviewDashboard:
    def test_paper_only_default(self):
        assert ReviewDashboard().paper_only is True

    def test_entries_count_default_zero(self):
        assert ReviewDashboard().entries_count == 0

    def test_top_actions_default_empty(self):
        assert ReviewDashboard().top_actions == []


class TestReviewHealthSummary:
    def test_paper_only_default(self):
        assert ReviewHealthSummary().paper_only is True

    def test_status_default_pass(self):
        assert ReviewHealthSummary().status == "PASS"

    def test_all_passed_default_true(self):
        assert ReviewHealthSummary().all_passed is True
