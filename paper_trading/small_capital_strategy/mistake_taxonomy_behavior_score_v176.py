"""
paper_trading/small_capital_strategy/mistake_taxonomy_behavior_score_v176.py
Behavior risk scoring for v1.7.6 (0-100, higher = more risk).
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List

from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, MistakeSeverity, BehaviorRiskLevel,
    get_severity_weight,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_models_v176 import (
    MistakeEvent, BehaviorRiskScore, RepeatedMistakePattern,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_repeat_v176 import (
    REPEAT_WARNING_THRESHOLD, REPEAT_BLOCKED_THRESHOLD,
)

_SCHEMA = "176"
_POLICY = "1.7.6-mistake-taxonomy-weekly-review"

# Score thresholds for risk levels
SCORE_WATCH_MIN   = 20.0
SCORE_WARNING_MIN = 50.0
SCORE_BLOCKED_MIN = 80.0

# Instant BLOCKED categories (regardless of score)
BLOCKING_CATEGORIES = {
    MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT,
    MistakeCategory.BROKER_OR_REAL_ORDER_ATTEMPT,
}


def compute_behavior_score(
    events: List[MistakeEvent],
    patterns: List[RepeatedMistakePattern],
    total_trades: int = 1,
) -> BehaviorRiskScore:
    """Compute 0-100 behavior risk score from events and patterns."""
    if not events:
        return BehaviorRiskScore(
            score=0.0, level=BehaviorRiskLevel.PASS,
            factors={}, description="No mistakes recorded.",
        )

    # Check for instant BLOCKED
    for ev in events:
        if ev.category in BLOCKING_CATEGORIES:
            return BehaviorRiskScore(
                score=100.0,
                level=BehaviorRiskLevel.BLOCKED,
                factors={"blocking_category": 100.0},
                description=f"BLOCKED: {ev.category.value} detected.",
            )

    # Check for BLOCKED repeat patterns
    for p in patterns:
        if p.risk_flag == "BLOCKED":
            return BehaviorRiskScore(
                score=95.0,
                level=BehaviorRiskLevel.BLOCKED,
                factors={"repeat_blocked": 95.0},
                description=f"BLOCKED: {p.category.value} repeated {p.count} times.",
            )

    factors: Dict[str, float] = {}

    # Factor 1: severity-weighted mistake score
    sev_total = sum(get_severity_weight(ev.severity) for ev in events)
    sev_score = min(sev_total / max(total_trades, 1) * 2.0, 60.0)
    factors["severity_weighted"] = round(sev_score, 2)

    # Factor 2: repeat pattern penalty
    repeat_score = 0.0
    for p in patterns:
        if p.count >= REPEAT_BLOCKED_THRESHOLD:
            repeat_score += 25.0
        elif p.count >= REPEAT_WARNING_THRESHOLD:
            repeat_score += 15.0
        else:
            repeat_score += 5.0
    repeat_score = min(repeat_score, 30.0)
    factors["repeat_patterns"] = round(repeat_score, 2)

    # Factor 3: high-severity event count
    high_count = sum(
        1 for ev in events
        if ev.severity in (MistakeSeverity.HIGH, MistakeSeverity.CRITICAL, MistakeSeverity.BLOCKING)
    )
    high_score = min(high_count * 5.0, 20.0)
    factors["high_severity_events"] = round(high_score, 2)

    # Final score
    raw = sev_score + repeat_score + high_score
    score = round(min(max(raw, 0.0), 100.0), 2)

    # Determine level
    if score >= SCORE_BLOCKED_MIN:
        level = BehaviorRiskLevel.BLOCKED
        description = f"BLOCKED: Score {score}/100. Immediate behavior correction required."
    elif score >= SCORE_WARNING_MIN:
        level = BehaviorRiskLevel.WARNING
        description = f"WARNING: Score {score}/100. Significant behavior risk detected."
    elif score >= SCORE_WATCH_MIN:
        level = BehaviorRiskLevel.WATCH
        description = f"WATCH: Score {score}/100. Monitor behavior trend."
    else:
        level = BehaviorRiskLevel.PASS
        description = f"PASS: Score {score}/100. Behavior within acceptable range."

    return BehaviorRiskScore(
        score=score,
        level=level,
        factors=factors,
        description=description,
    )


def score_to_level(score: float) -> BehaviorRiskLevel:
    """Convert numeric score to BehaviorRiskLevel."""
    if score >= SCORE_BLOCKED_MIN:
        return BehaviorRiskLevel.BLOCKED
    if score >= SCORE_WARNING_MIN:
        return BehaviorRiskLevel.WARNING
    if score >= SCORE_WATCH_MIN:
        return BehaviorRiskLevel.WATCH
    return BehaviorRiskLevel.PASS
