"""tests/test_mistake_taxonomy_integration_v176.py — v1.7.6 integration tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, BehaviorRiskLevel,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import classify_event
from paper_trading.small_capital_strategy.mistake_taxonomy_cost_v176 import calculate_cost_summary
from paper_trading.small_capital_strategy.mistake_taxonomy_repeat_v176 import detect_repeated_patterns
from paper_trading.small_capital_strategy.mistake_taxonomy_behavior_score_v176 import compute_behavior_score
from paper_trading.small_capital_strategy.mistake_taxonomy_actions_v176 import generate_actions_from_events
from paper_trading.small_capital_strategy.mistake_taxonomy_weekly_review_v176 import (
    run_weekly_review, create_weekly_input,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_monthly_review_v176 import run_monthly_review
from paper_trading.small_capital_strategy.mistake_taxonomy_dashboard_v176 import build_dashboard
from paper_trading.small_capital_strategy.mistake_taxonomy_report_v176 import (
    build_report_dict, render_json, render_markdown,
)


def _ev(cat, date="2026-01-05", cost=0.0):
    return classify_event("2330", date, cat, cost)


class TestEndToEndCleanWeek:
    """Full pipeline with a clean week (no mistakes)."""

    def setup_method(self):
        self.events = []
        self.wi = create_weekly_input("2026-01-05", "2026-01-09", self.events, 2)
        self.wr = run_weekly_review(self.wi)
        self.mr = run_monthly_review("2026-01", [self.wr])
        self.dash = build_dashboard(self.events, self.wr, self.mr, 2)
        self.rpt = build_report_dict(self.dash)

    def test_weekly_review_pass_level(self):
        assert self.wr.risk_level == BehaviorRiskLevel.PASS

    def test_monthly_review_trend_stable(self):
        assert self.mr.behavior_trend == "STABLE"

    def test_dashboard_events_count_zero(self):
        assert self.dash.events_count == 0

    def test_report_paper_only(self):
        assert self.rpt["paper_only"] is True

    def test_report_json_parseable(self):
        import json
        parsed = json.loads(render_json(self.rpt))
        assert isinstance(parsed, dict)

    def test_markdown_contains_disclaimer(self):
        md = render_markdown(self.rpt)
        assert "Paper Only" in md or "Research Only" in md


class TestEndToEndBlockingWeek:
    """Full pipeline with a margin attempt (BLOCKED)."""

    def setup_method(self):
        self.events = [_ev(MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT)]
        self.wi = create_weekly_input("2026-01-05", "2026-01-09", self.events, 1)
        self.wr = run_weekly_review(self.wi)
        self.mr = run_monthly_review("2026-01", [self.wr])
        self.dash = build_dashboard(self.events, self.wr, self.mr, 1)

    def test_weekly_risk_blocked(self):
        assert self.wr.risk_level == BehaviorRiskLevel.BLOCKED

    def test_dashboard_behavior_blocked(self):
        assert self.dash.behavior_score.level == BehaviorRiskLevel.BLOCKED

    def test_dash_paper_only(self):
        assert self.dash.paper_only is True


class TestEndToEndRepeatPattern:
    """5 repeats of NO_STOP_LOSS → BLOCKED."""

    def setup_method(self):
        self.events = [_ev(MistakeCategory.NO_STOP_LOSS, f"2026-01-0{i}", -5000.0) for i in range(1, 6)]
        self.patterns = detect_repeated_patterns(self.events)
        self.bs = compute_behavior_score(self.events, self.patterns, 5)

    def test_patterns_detected(self):
        assert len(self.patterns) >= 1

    def test_most_repeated_no_stop_loss(self):
        assert self.patterns[0].category == MistakeCategory.NO_STOP_LOSS

    def test_pattern_risk_blocked(self):
        assert self.patterns[0].risk_flag == "BLOCKED"

    def test_behavior_score_blocked(self):
        assert self.bs.level == BehaviorRiskLevel.BLOCKED


class TestIntegrationCostAndActions:
    def test_cost_summary_reflects_events(self):
        ev1 = _ev(MistakeCategory.NO_STOP_LOSS, cost=-8000.0)
        ev2 = _ev(MistakeCategory.FOMO_CHASE, cost=-2000.0)
        cs = calculate_cost_summary([ev1, ev2])
        assert cs.total_cost_twd == -10000.0
        assert cs.event_count == 2

    def test_actions_from_events_paper_only(self):
        ev = _ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)
        acts = generate_actions_from_events([ev])
        assert all(a.paper_only for a in acts)

    def test_full_pipeline_paper_only(self):
        ev1 = _ev(MistakeCategory.NO_STOP_LOSS, "2026-01-05", -5000.0)
        ev2 = _ev(MistakeCategory.FOMO_CHASE, "2026-01-06", -2000.0)
        wi = create_weekly_input("2026-01-05", "2026-01-09", [ev1, ev2], 2)
        wr = run_weekly_review(wi)
        mr = run_monthly_review("2026-01", [wr])
        dash = build_dashboard([ev1, ev2], wr, mr, 2)
        assert dash.paper_only is True
        assert wr.paper_only is True
        assert mr.paper_only is True

    def test_backward_compat_v175_imports(self):
        from paper_trading.small_capital_strategy.version_v175 import VERSION as V175
        from paper_trading.small_capital_strategy.version_v176 import is_known_release
        assert V175 == "1.7.5"
        assert is_known_release("Small Account Trade Journal") is True
