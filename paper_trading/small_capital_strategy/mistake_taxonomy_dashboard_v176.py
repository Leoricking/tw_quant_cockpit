"""
paper_trading/small_capital_strategy/mistake_taxonomy_dashboard_v176.py
Review dashboard builder for v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Optional

from paper_trading.small_capital_strategy.mistake_taxonomy_models_v176 import (
    MistakeEvent, WeeklyReviewResult, MonthlyReviewResult,
    BehaviorRiskScore, ReviewDashboard,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_behavior_score_v176 import compute_behavior_score
from paper_trading.small_capital_strategy.mistake_taxonomy_repeat_v176 import detect_repeated_patterns
from paper_trading.small_capital_strategy.mistake_taxonomy_actions_v176 import generate_actions_from_events

_SCHEMA = "176"
_POLICY = "1.7.6-mistake-taxonomy-weekly-review"


def build_dashboard(
    events: List[MistakeEvent],
    weekly_result: Optional[WeeklyReviewResult] = None,
    monthly_result: Optional[MonthlyReviewResult] = None,
    total_trades: int = 1,
) -> ReviewDashboard:
    """Build a ReviewDashboard from events and optional review results."""
    patterns = detect_repeated_patterns(events)
    behavior_score = compute_behavior_score(events, patterns, total_trades)
    top_actions = generate_actions_from_events(events)

    return ReviewDashboard(
        weekly_result=weekly_result,
        monthly_result=monthly_result,
        behavior_score=behavior_score,
        top_actions=top_actions,
        entries_count=total_trades,
        events_count=len(events),
    )
