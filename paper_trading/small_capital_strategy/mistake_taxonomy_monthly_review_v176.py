"""
paper_trading/small_capital_strategy/mistake_taxonomy_monthly_review_v176.py
Monthly review rollup for v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List

from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import MistakeCategory
from paper_trading.small_capital_strategy.mistake_taxonomy_models_v176 import (
    WeeklyReviewResult, MonthlyReviewResult,
)

_SCHEMA = "176"
_POLICY = "1.7.6-mistake-taxonomy-weekly-review"


def run_monthly_review(
    month_label: str,
    weekly_results: List[WeeklyReviewResult],
) -> MonthlyReviewResult:
    """Aggregate weekly review results into a monthly review."""
    if not weekly_results:
        return MonthlyReviewResult(
            month_label=month_label,
            weekly_results=[],
            total_events=0,
            total_cost_twd=0.0,
            behavior_trend="STABLE",
            worst_week="",
            top_mistakes=[],
            avg_behavior_score=0.0,
        )

    total_events = sum(r.total_events for r in weekly_results)
    total_cost = sum(
        r.cost_summary.total_cost_twd for r in weekly_results if r.cost_summary
    )
    scores = [r.behavior_score for r in weekly_results]
    avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0

    # Worst week: highest behavior score
    worst_wr = max(weekly_results, key=lambda r: r.behavior_score)
    worst_week = f"{worst_wr.week_start}~{worst_wr.week_end}"

    # Trend: compare first half vs second half
    mid = len(weekly_results) // 2
    first_half = scores[:mid] if mid else scores
    second_half = scores[mid:] if mid else scores
    avg_first = sum(first_half) / len(first_half) if first_half else 0.0
    avg_second = sum(second_half) / len(second_half) if second_half else 0.0
    if avg_second > avg_first + 5:
        trend = "DETERIORATING"
    elif avg_second < avg_first - 5:
        trend = "IMPROVING"
    else:
        trend = "STABLE"

    # Aggregate top mistakes
    seen: set = set()
    top_mistakes: List[MistakeCategory] = []
    for r in weekly_results:
        for cat in r.top_mistakes:
            if cat not in seen:
                seen.add(cat)
                top_mistakes.append(cat)

    return MonthlyReviewResult(
        month_label=month_label,
        weekly_results=weekly_results,
        total_events=total_events,
        total_cost_twd=round(total_cost, 2),
        behavior_trend=trend,
        worst_week=worst_week,
        top_mistakes=top_mistakes,
        avg_behavior_score=avg_score,
    )
