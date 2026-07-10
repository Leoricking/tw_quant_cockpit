"""
paper_trading/small_capital_strategy/mistake_taxonomy_actions_v176.py
Improvement action generation for v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, MistakeSeverity, CATEGORY_SEVERITY,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_models_v176 import (
    MistakeEvent, ImprovementAction, RepeatedMistakePattern,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import (
    build_improvement_action,
)

_SCHEMA = "176"
_POLICY = "1.7.6-mistake-taxonomy-weekly-review"


def generate_actions_from_events(
    events: List[MistakeEvent],
    max_actions: int = 5,
) -> List[ImprovementAction]:
    """Generate top improvement actions from mistake events, deduped by category."""
    if not events:
        return []

    # Count & score by category
    cat_cost: dict = {}
    cat_count: dict = {}
    for ev in events:
        cat_cost[ev.category] = cat_cost.get(ev.category, 0.0) + ev.cost_twd
        cat_count[ev.category] = cat_count.get(ev.category, 0) + 1

    # Sort: BLOCKING first, then by cost+count
    def _priority_key(cat: MistakeCategory):
        sev = CATEGORY_SEVERITY.get(cat, MistakeSeverity.INFO)
        sev_order = {
            MistakeSeverity.BLOCKING: 0,
            MistakeSeverity.CRITICAL: 1,
            MistakeSeverity.HIGH:     2,
            MistakeSeverity.MEDIUM:   3,
            MistakeSeverity.LOW:      4,
            MistakeSeverity.INFO:     5,
        }.get(sev, 5)
        return (sev_order, -cat_cost.get(cat, 0.0))

    ranked = sorted(cat_cost.keys(), key=_priority_key)[:max_actions]
    actions: List[ImprovementAction] = []
    for i, cat in enumerate(ranked, start=1):
        act = build_improvement_action(
            category=cat,
            priority=i,
            action_id=f"ACT176-{i:03d}-{cat.value}",
        )
        actions.append(act)
    return actions


def generate_actions_from_patterns(
    patterns: List[RepeatedMistakePattern],
    max_actions: int = 3,
) -> List[ImprovementAction]:
    """Generate improvement actions focused on repeated patterns."""
    sorted_patterns = sorted(patterns, key=lambda p: p.count, reverse=True)[:max_actions]
    actions: List[ImprovementAction] = []
    for i, p in enumerate(sorted_patterns, start=1):
        act = build_improvement_action(
            category=p.category,
            priority=i,
            action_id=f"ACT176-REP-{i:03d}-{p.category.value}",
        )
        actions.append(act)
    return actions


def get_action_descriptions(actions: List[ImprovementAction]) -> List[str]:
    """Return list of action description strings."""
    return [a.description for a in actions]
