"""tests/test_mistake_taxonomy_cost_v176.py — v1.7.6 cost calculation tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import MistakeCategory
from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import classify_event
from paper_trading.small_capital_strategy.mistake_taxonomy_cost_v176 import (
    calculate_cost_summary, get_cost_by_category, rank_categories_by_cost,
)


def _mk_ev(cat, cost):
    return classify_event("2330", "2026-01-05", cat, cost)


class TestCalculateCostSummary:
    def test_empty_events_paper_only(self):
        cs = calculate_cost_summary([])
        assert cs.paper_only is True

    def test_empty_events_total_zero(self):
        cs = calculate_cost_summary([])
        assert cs.total_cost_twd == 0.0

    def test_empty_events_count_zero(self):
        cs = calculate_cost_summary([])
        assert cs.event_count == 0

    def test_single_event_total(self):
        ev = _mk_ev(MistakeCategory.NO_STOP_LOSS, -5000.0)
        cs = calculate_cost_summary([ev])
        assert cs.total_cost_twd == -5000.0

    def test_single_event_count_one(self):
        ev = _mk_ev(MistakeCategory.NO_STOP_LOSS, -5000.0)
        cs = calculate_cost_summary([ev])
        assert cs.event_count == 1

    def test_two_events_total(self):
        ev1 = _mk_ev(MistakeCategory.NO_STOP_LOSS, -5000.0)
        ev2 = _mk_ev(MistakeCategory.FOMO_CHASE, -2000.0)
        cs = calculate_cost_summary([ev1, ev2])
        assert cs.total_cost_twd == -7000.0

    def test_two_events_by_category(self):
        ev1 = _mk_ev(MistakeCategory.NO_STOP_LOSS, -5000.0)
        ev2 = _mk_ev(MistakeCategory.FOMO_CHASE, -2000.0)
        cs = calculate_cost_summary([ev1, ev2])
        assert "NO_STOP_LOSS" in cs.by_category
        assert "FOMO_CHASE" in cs.by_category

    def test_worst_category_is_largest(self):
        ev1 = _mk_ev(MistakeCategory.NO_STOP_LOSS, -8000.0)
        ev2 = _mk_ev(MistakeCategory.FOMO_CHASE, -2000.0)
        cs = calculate_cost_summary([ev1, ev2])
        assert cs.worst_category == MistakeCategory.NO_STOP_LOSS

    def test_avg_cost_twd_correct(self):
        ev1 = _mk_ev(MistakeCategory.NO_STOP_LOSS, -6000.0)
        ev2 = _mk_ev(MistakeCategory.FOMO_CHASE, -4000.0)
        cs = calculate_cost_summary([ev1, ev2])
        assert cs.avg_cost_twd == -5000.0

    def test_same_category_aggregated(self):
        ev1 = _mk_ev(MistakeCategory.NO_STOP_LOSS, -3000.0)
        ev2 = _mk_ev(MistakeCategory.NO_STOP_LOSS, -2000.0)
        cs = calculate_cost_summary([ev1, ev2])
        assert cs.by_category["NO_STOP_LOSS"] == -5000.0


class TestCostHelpers:
    def test_get_cost_by_category_found(self):
        ev = _mk_ev(MistakeCategory.NO_STOP_LOSS, -5000.0)
        cs = calculate_cost_summary([ev])
        assert get_cost_by_category(cs, MistakeCategory.NO_STOP_LOSS) == -5000.0

    def test_get_cost_by_category_not_found(self):
        ev = _mk_ev(MistakeCategory.NO_STOP_LOSS, -5000.0)
        cs = calculate_cost_summary([ev])
        assert get_cost_by_category(cs, MistakeCategory.FOMO_CHASE) == 0.0

    def test_rank_categories_by_cost_ordered(self):
        ev1 = _mk_ev(MistakeCategory.NO_STOP_LOSS, -8000.0)
        ev2 = _mk_ev(MistakeCategory.FOMO_CHASE, -2000.0)
        cs = calculate_cost_summary([ev1, ev2])
        ranked = rank_categories_by_cost(cs)
        assert ranked[0] == "NO_STOP_LOSS"
