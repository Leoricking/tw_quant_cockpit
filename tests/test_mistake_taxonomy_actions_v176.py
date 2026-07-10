"""tests/test_mistake_taxonomy_actions_v176.py — v1.7.6 improvement action tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, MistakeSeverity,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import classify_event
from paper_trading.small_capital_strategy.mistake_taxonomy_repeat_v176 import detect_repeated_patterns
from paper_trading.small_capital_strategy.mistake_taxonomy_actions_v176 import (
    generate_actions_from_events, generate_actions_from_patterns, get_action_descriptions,
)


def _ev(cat, cost=0.0):
    return classify_event("2330", "2026-01-05", cat, cost)


class TestGenerateActionsFromEvents:
    def test_empty_events_returns_empty(self):
        assert generate_actions_from_events([]) == []

    def test_single_event_one_action(self):
        acts = generate_actions_from_events([_ev(MistakeCategory.NO_STOP_LOSS, -5000.0)])
        assert len(acts) >= 1

    def test_all_actions_paper_only(self):
        acts = generate_actions_from_events([_ev(MistakeCategory.NO_STOP_LOSS, -5000.0)])
        assert all(a.paper_only for a in acts)

    def test_max_actions_respected(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, -5000.0)]
        acts = generate_actions_from_events(evts, max_actions=1)
        assert len(acts) <= 1

    def test_blocking_category_first(self):
        evts = [
            _ev(MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT, 0.0),
            _ev(MistakeCategory.FOMO_CHASE, -2000.0),
        ]
        acts = generate_actions_from_events(evts)
        assert acts[0].category == MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT

    def test_actions_have_descriptions(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, -5000.0)]
        acts = generate_actions_from_events(evts)
        assert all(len(a.description) > 0 for a in acts)

    def test_action_ids_unique(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, -5000.0), _ev(MistakeCategory.FOMO_CHASE, -2000.0)]
        acts = generate_actions_from_events(evts)
        ids = [a.action_id for a in acts]
        assert len(ids) == len(set(ids))


class TestGenerateActionsFromPatterns:
    def test_empty_patterns_returns_empty(self):
        assert generate_actions_from_patterns([]) == []

    def test_patterns_generate_actions(self):
        evts = [
            classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0),
            classify_event("2330", "2026-01-06", MistakeCategory.NO_STOP_LOSS, -4000.0),
        ]
        pats = detect_repeated_patterns(evts)
        acts = generate_actions_from_patterns(pats)
        assert len(acts) >= 1

    def test_pattern_actions_paper_only(self):
        evts = [
            classify_event("2330", "2026-01-05", MistakeCategory.NO_STOP_LOSS, -5000.0),
            classify_event("2330", "2026-01-06", MistakeCategory.NO_STOP_LOSS, -4000.0),
        ]
        pats = detect_repeated_patterns(evts)
        acts = generate_actions_from_patterns(pats)
        assert all(a.paper_only for a in acts)


class TestGetActionDescriptions:
    def test_empty_actions_returns_empty_list(self):
        assert get_action_descriptions([]) == []

    def test_descriptions_list_of_strings(self):
        evts = [_ev(MistakeCategory.NO_STOP_LOSS, -5000.0)]
        acts = generate_actions_from_events(evts)
        descs = get_action_descriptions(acts)
        assert isinstance(descs, list)
        assert all(isinstance(d, str) for d in descs)
