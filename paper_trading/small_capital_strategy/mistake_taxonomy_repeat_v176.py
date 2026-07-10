"""
paper_trading/small_capital_strategy/mistake_taxonomy_repeat_v176.py
Repeated mistake detection for v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from collections import Counter
from typing import Dict, List

from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, MistakeSeverity,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_models_v176 import (
    MistakeEvent, RepeatedMistakePattern,
)

_SCHEMA = "176"
_POLICY = "1.7.6-mistake-taxonomy-weekly-review"

# Thresholds for risk escalation
REPEAT_WARNING_THRESHOLD = 3   # >= 3 times same mistake in a week → WARNING
REPEAT_BLOCKED_THRESHOLD = 5   # >= 5 times same mistake in a week → BLOCKED


def detect_repeated_patterns(events: List[MistakeEvent]) -> List[RepeatedMistakePattern]:
    """Detect repeated mistake patterns across a list of events."""
    if not events:
        return []

    # Group by category
    by_cat: Dict[MistakeCategory, List[MistakeEvent]] = {}
    for ev in events:
        by_cat.setdefault(ev.category, []).append(ev)

    patterns: List[RepeatedMistakePattern] = []
    for category, cat_events in by_cat.items():
        count = len(cat_events)
        if count < 2:
            continue  # Single occurrences not considered "repeated"
        dates = sorted(ev.trade_date for ev in cat_events)
        total_cost = sum(ev.cost_twd for ev in cat_events)

        # Escalate severity based on repeat count
        base_sev = cat_events[0].severity
        if count >= REPEAT_BLOCKED_THRESHOLD:
            severity_escalation = MistakeSeverity.BLOCKING
            risk_flag = "BLOCKED"
        elif count >= REPEAT_WARNING_THRESHOLD:
            severity_escalation = MistakeSeverity.CRITICAL
            risk_flag = "WARNING"
        else:
            severity_escalation = base_sev
            risk_flag = "WATCH"

        patterns.append(RepeatedMistakePattern(
            category=category,
            count=count,
            dates=dates,
            total_cost_twd=round(total_cost, 2),
            severity_escalation=severity_escalation,
            risk_flag=risk_flag,
        ))

    return sorted(patterns, key=lambda p: p.count, reverse=True)


def get_most_repeated(events: List[MistakeEvent]) -> MistakeCategory:
    """Return the most repeated mistake category."""
    if not events:
        return MistakeCategory.UNKNOWN
    counter = Counter(ev.category for ev in events)
    return counter.most_common(1)[0][0]


def has_blocking_repeat(patterns: List[RepeatedMistakePattern]) -> bool:
    """Return True if any pattern has BLOCKED risk flag."""
    return any(p.risk_flag == "BLOCKED" for p in patterns)


def count_repeat_categories(events: List[MistakeEvent]) -> int:
    """Return count of categories that appear more than once."""
    counter = Counter(ev.category for ev in events)
    return sum(1 for c in counter.values() if c >= 2)
