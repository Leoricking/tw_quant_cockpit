"""tests/test_mistake_taxonomy_repeat_v176.py — v1.7.6 repeat detection tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, MistakeSeverity,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import classify_event
from paper_trading.small_capital_strategy.mistake_taxonomy_repeat_v176 import (
    detect_repeated_patterns, get_most_repeated, has_blocking_repeat,
    count_repeat_categories, REPEAT_WARNING_THRESHOLD, REPEAT_BLOCKED_THRESHOLD,
)


def _ev(cat, date="2026-01-05", cost=0.0):
    return classify_event("2330", date, cat, cost)


class TestDetectRepeatedPatterns:
    def test_empty_events_returns_empty(self):
        assert detect_repeated_patterns([]) == []

    def test_single_event_returns_empty(self):
        assert detect_repeated_patterns([_ev(MistakeCategory.NO_STOP_LOSS)]) == []

    def test_two_same_category_detected(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, "2026-01-05"), _ev(MistakeCategory.NO_STOP_LOSS, "2026-01-06")]
        patterns = detect_repeated_patterns(evts)
        assert len(patterns) == 1
        assert patterns[0].category == MistakeCategory.NO_STOP_LOSS

    def test_pattern_count_correct(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, f"2026-01-0{i}") for i in range(1, 4)]
        patterns = detect_repeated_patterns(evts)
        assert patterns[0].count == 3

    def test_pattern_paper_only(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, "2026-01-05"), _ev(MistakeCategory.NO_STOP_LOSS, "2026-01-06")]
        patterns = detect_repeated_patterns(evts)
        assert patterns[0].paper_only is True

    def test_threshold_3_gives_warning(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, f"2026-01-0{i}") for i in range(1, 4)]
        patterns = detect_repeated_patterns(evts)
        assert patterns[0].risk_flag == "WARNING"

    def test_threshold_5_gives_blocked(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, f"2026-01-0{i}") for i in range(1, 6)]
        patterns = detect_repeated_patterns(evts)
        assert patterns[0].risk_flag == "BLOCKED"
        assert patterns[0].severity_escalation == MistakeSeverity.BLOCKING

    def test_two_repeat_warning_threshold(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, "2026-01-05"), _ev(MistakeCategory.NO_STOP_LOSS, "2026-01-06")]
        patterns = detect_repeated_patterns(evts)
        assert patterns[0].risk_flag == "WATCH"

    def test_total_cost_aggregated(self):
        ev1 = classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -3000.0)
        ev2 = classify_event("2330", "2026-01-06", MistakeCategory.NO_STOP_LOSS, -2000.0)
        patterns = detect_repeated_patterns([ev1, ev2])
        assert patterns[0].total_cost_twd == -5000.0

    def test_sorted_by_count_desc(self):
        evts_a = [_ev(MistakeCategory.NO_STOP_LOSS, f"2026-01-0{i}") for i in range(1, 4)]
        evts_b = [_ev(MistakeCategory.FOMO_CHASE, f"2026-01-1{i}") for i in range(1, 3)]
        patterns = detect_repeated_patterns(evts_a + evts_b)
        assert patterns[0].count >= patterns[-1].count


class TestRepeatHelpers:
    def test_get_most_repeated_empty(self):
        assert get_most_repeated([]) == MistakeCategory.UNKNOWN

    def test_get_most_repeated_correct(self):
        evts = [
            _ev(MistakeCategory.NO_STOP_LOSS), _ev(MistakeCategory.NO_STOP_LOSS),
            _ev(MistakeCategory.FOMO_CHASE),
        ]
        assert get_most_repeated(evts) == MistakeCategory.NO_STOP_LOSS

    def test_has_blocking_repeat_false(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, "2026-01-05"), _ev(MistakeCategory.NO_STOP_LOSS, "2026-01-06")]
        patterns = detect_repeated_patterns(evts)
        assert has_blocking_repeat(patterns) is False

    def test_has_blocking_repeat_true(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, f"2026-01-0{i}") for i in range(1, 6)]
        patterns = detect_repeated_patterns(evts)
        assert has_blocking_repeat(patterns) is True

    def test_count_repeat_categories_zero(self):
        assert count_repeat_categories([_ev(MistakeCategory.NO_STOP_LOSS)]) == 0

    def test_count_repeat_categories_one(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, "2026-01-05"), _ev(MistakeCategory.NO_STOP_LOSS, "2026-01-06")]
        assert count_repeat_categories(evts) == 1

    def test_repeat_warning_threshold_value(self):
        assert REPEAT_WARNING_THRESHOLD == 3

    def test_repeat_blocked_threshold_value(self):
        assert REPEAT_BLOCKED_THRESHOLD == 5
