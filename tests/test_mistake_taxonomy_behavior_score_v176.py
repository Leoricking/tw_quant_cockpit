"""tests/test_mistake_taxonomy_behavior_score_v176.py — v1.7.6 behavior score tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, BehaviorRiskLevel,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import classify_event
from paper_trading.small_capital_strategy.mistake_taxonomy_repeat_v176 import detect_repeated_patterns
from paper_trading.small_capital_strategy.mistake_taxonomy_behavior_score_v176 import (
    compute_behavior_score, score_to_level,
    SCORE_WATCH_MIN, SCORE_WARNING_MIN, SCORE_BLOCKED_MIN,
    BLOCKING_CATEGORIES,
)


def _ev(cat, date="2026-01-05", cost=0.0):
    return classify_event("2330", date, cat, cost)


class TestComputeBehaviorScore:
    def test_no_events_returns_pass(self):
        bs = compute_behavior_score([], [], 5)
        assert bs.level == BehaviorRiskLevel.PASS

    def test_no_events_score_zero(self):
        bs = compute_behavior_score([], [], 5)
        assert bs.score == 0.0

    def test_paper_only_true(self):
        bs = compute_behavior_score([], [], 5)
        assert bs.paper_only is True

    def test_margin_attempt_blocked(self):
        ev = _ev(MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT)
        bs = compute_behavior_score([ev], [], 1)
        assert bs.level == BehaviorRiskLevel.BLOCKED
        assert bs.score == 100.0

    def test_broker_attempt_blocked(self):
        ev = _ev(MistakeCategory.BROKER_OR_REAL_ORDER_ATTEMPT)
        bs = compute_behavior_score([ev], [], 1)
        assert bs.level == BehaviorRiskLevel.BLOCKED

    def test_5_repeats_blocked(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, f"2026-01-0{i}") for i in range(1, 6)]
        patterns = detect_repeated_patterns(evts)
        bs = compute_behavior_score(evts, patterns, 5)
        assert bs.level == BehaviorRiskLevel.BLOCKED

    def test_single_high_event_watch_or_warning(self):
        ev = _ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)
        bs = compute_behavior_score([ev], [], 10)
        assert bs.level in (BehaviorRiskLevel.WATCH, BehaviorRiskLevel.WARNING, BehaviorRiskLevel.PASS)

    def test_score_range_0_to_100(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, f"2026-01-0{i}", -5000.0) for i in range(1, 4)]
        patterns = detect_repeated_patterns(evts)
        bs = compute_behavior_score(evts, patterns, 3)
        assert 0.0 <= bs.score <= 100.0

    def test_factors_dict_not_empty_when_events(self):
        ev = _ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)
        bs = compute_behavior_score([ev], [], 1)
        assert isinstance(bs.factors, dict)

    def test_description_not_empty(self):
        ev = _ev(MistakeCategory.NO_STOP_LOSS, cost=-5000.0)
        bs = compute_behavior_score([ev], [], 1)
        assert len(bs.description) > 0


class TestScoreToLevel:
    def test_zero_is_pass(self):
        assert score_to_level(0.0) == BehaviorRiskLevel.PASS

    def test_watch_min_is_watch(self):
        assert score_to_level(SCORE_WATCH_MIN) == BehaviorRiskLevel.WATCH

    def test_warning_min_is_warning(self):
        assert score_to_level(SCORE_WARNING_MIN) == BehaviorRiskLevel.WARNING

    def test_blocked_min_is_blocked(self):
        assert score_to_level(SCORE_BLOCKED_MIN) == BehaviorRiskLevel.BLOCKED

    def test_100_is_blocked(self):
        assert score_to_level(100.0) == BehaviorRiskLevel.BLOCKED

    def test_watch_min_value_lte_50(self):
        assert SCORE_WATCH_MIN <= 50.0

    def test_warning_min_value_lte_80(self):
        assert SCORE_WARNING_MIN <= 80.0

    def test_blocking_categories_contains_margin(self):
        assert MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT in BLOCKING_CATEGORIES

    def test_blocking_categories_contains_broker(self):
        assert MistakeCategory.BROKER_OR_REAL_ORDER_ATTEMPT in BLOCKING_CATEGORIES
