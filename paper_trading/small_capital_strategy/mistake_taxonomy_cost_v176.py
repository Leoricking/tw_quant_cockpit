"""
paper_trading/small_capital_strategy/mistake_taxonomy_cost_v176.py
Mistake cost calculation for v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List, Optional

from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import MistakeCategory
from paper_trading.small_capital_strategy.mistake_taxonomy_models_v176 import (
    MistakeEvent, MistakeCostSummary,
)

_SCHEMA = "176"
_POLICY = "1.7.6-mistake-taxonomy-weekly-review"


def calculate_cost_summary(events: List[MistakeEvent]) -> MistakeCostSummary:
    """Aggregate mistake events into a cost summary."""
    if not events:
        return MistakeCostSummary(
            total_cost_twd=0.0, event_count=0,
            by_category={}, worst_category=None, worst_cost_twd=0.0, avg_cost_twd=0.0,
        )
    by_category: Dict[str, float] = {}
    for ev in events:
        key = ev.category.value
        by_category[key] = by_category.get(key, 0.0) + ev.cost_twd

    total = sum(ev.cost_twd for ev in events)
    worst_key = min(by_category, key=lambda k: by_category[k])
    worst_category: Optional[MistakeCategory] = None
    for cat in MistakeCategory:
        if cat.value == worst_key:
            worst_category = cat
            break

    return MistakeCostSummary(
        total_cost_twd=round(total, 2),
        event_count=len(events),
        by_category=by_category,
        worst_category=worst_category,
        worst_cost_twd=round(by_category[worst_key], 2),
        avg_cost_twd=round(total / len(events), 2),
    )


def get_cost_by_category(summary: MistakeCostSummary, category: MistakeCategory) -> float:
    """Return cost for a specific category from a summary."""
    return summary.by_category.get(category.value, 0.0)


def rank_categories_by_cost(summary: MistakeCostSummary) -> List[str]:
    """Return category names sorted by cost descending."""
    return sorted(summary.by_category, key=lambda k: summary.by_category[k])
