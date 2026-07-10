"""
paper_trading/small_capital_strategy/mistake_taxonomy_weekly_review_v176.py
Weekly review logic for v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import MistakeCategory
from paper_trading.small_capital_strategy.mistake_taxonomy_models_v176 import (
    MistakeEvent, WeeklyReviewInput, WeeklyReviewResult,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_cost_v176 import calculate_cost_summary
from paper_trading.small_capital_strategy.mistake_taxonomy_repeat_v176 import detect_repeated_patterns
from paper_trading.small_capital_strategy.mistake_taxonomy_behavior_score_v176 import compute_behavior_score
from paper_trading.small_capital_strategy.mistake_taxonomy_actions_v176 import (
    generate_actions_from_events, get_action_descriptions,
)

_SCHEMA = "176"
_POLICY = "1.7.6-mistake-taxonomy-weekly-review"


def run_weekly_review(review_input: WeeklyReviewInput) -> WeeklyReviewResult:
    """Run weekly mistake review analysis and return WeeklyReviewResult."""
    events = review_input.events
    total_trades = max(review_input.total_trades, 1)

    cost_summary = calculate_cost_summary(events)
    repeat_patterns = detect_repeated_patterns(events)
    behavior_score = compute_behavior_score(events, repeat_patterns, total_trades)
    actions = generate_actions_from_events(events)
    action_descs = get_action_descriptions(actions)

    # Determine top mistakes (unique, sorted by severity)
    seen: set = set()
    top_mistakes: List[MistakeCategory] = []
    for ev in events:
        if ev.category not in seen:
            seen.add(ev.category)
            top_mistakes.append(ev.category)

    summary_parts = [
        f"Week {review_input.week_start}~{review_input.week_end}:",
        f"{len(events)} mistake events,",
        f"risk level={behavior_score.level.value},",
        f"score={behavior_score.score}/100.",
    ]

    return WeeklyReviewResult(
        week_start=review_input.week_start,
        week_end=review_input.week_end,
        total_events=len(events),
        top_mistakes=top_mistakes,
        cost_summary=cost_summary,
        repeat_patterns=repeat_patterns,
        behavior_score=behavior_score.score,
        risk_level=behavior_score.level,
        actions=action_descs,
        summary=" ".join(summary_parts),
    )


def create_weekly_input(
    week_start: str,
    week_end: str,
    events: List[MistakeEvent],
    total_trades: int = 1,
) -> WeeklyReviewInput:
    """Convenience factory for WeeklyReviewInput."""
    return WeeklyReviewInput(
        week_start=week_start,
        week_end=week_end,
        events=events,
        total_trades=total_trades,
    )
