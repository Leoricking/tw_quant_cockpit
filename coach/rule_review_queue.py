"""
coach/rule_review_queue.py — RuleReviewQueueBuilder (v0.4.8).

Builds rule review queue from Rule Governance / Signal Quality / Journal mistakes.

[!] Coaching Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Does NOT auto-enable/disable rules. Does NOT auto-change weights.
"""
from __future__ import annotations

import logging
from typing import Dict, List

from coach.coach_schema import (
    CoachRecommendation,
    REC_RULE_REVIEW,
    PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
    CAT_RULE,
    EFFORT_MEDIUM, EFFORT_DEEP,
    DUE_TODAY, DUE_THIS_WEEK,
    STATUS_OPEN,
)

logger = logging.getLogger(__name__)


class RuleReviewQueueBuilder:
    """
    Builds rule review queue for coaching.

    Conditions:
      - low confidence rule
      - insufficient sample
      - repeated false signal
      - high mistake linkage
      - signal disabled / reduce candidate
      - transcript-derived candidate needs backtest
      - ML knowledge feature needs mapping

    Safety:
      Does NOT auto-enable / disable rules.
      Does NOT auto-change weights.
      read_only          = True
      no_real_orders     = True
      production_blocked = True
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def build(
        self,
        rule_governance: dict = None,
        review_summary:  dict = None,
    ) -> List[CoachRecommendation]:
        """Build rule review queue recommendations."""
        rule_governance = rule_governance or {}
        review_summary  = review_summary  or {}

        items: List[CoachRecommendation] = []

        # Low confidence rules
        low_confidence_rules = rule_governance.get("low_confidence_rules", [])
        if isinstance(low_confidence_rules, list):
            for rule in low_confidence_rules[:5]:  # cap at 5
                rule_id    = rule.get("rule_id", "unknown") if isinstance(rule, dict) else str(rule)
                confidence = rule.get("confidence", "low") if isinstance(rule, dict) else "low"
                sample_count = rule.get("sample_count", 0) if isinstance(rule, dict) else 0
                items.append(self._make_item(
                    rule_id=rule_id,
                    reason="Low confidence rule — needs more backtest data.",
                    confidence=confidence,
                    sample_count=sample_count,
                    priority=PRIORITY_P1,
                    due_type=DUE_THIS_WEEK,
                    tags=["rule", "low_confidence"],
                ))

        # Insufficient sample rules
        insufficient_rules = rule_governance.get("insufficient_sample_rules", [])
        if isinstance(insufficient_rules, list):
            for rule in insufficient_rules[:5]:
                rule_id    = rule.get("rule_id", "unknown") if isinstance(rule, dict) else str(rule)
                confidence = rule.get("confidence", "unknown") if isinstance(rule, dict) else "unknown"
                sample_count = rule.get("sample_count", 0) if isinstance(rule, dict) else 0
                items.append(self._make_item(
                    rule_id=rule_id,
                    reason="Insufficient sample count — run more backtests to validate.",
                    confidence=confidence,
                    sample_count=sample_count,
                    priority=PRIORITY_P2,
                    due_type=DUE_THIS_WEEK,
                    tags=["rule", "insufficient_sample"],
                ))

        # Weak/unknown rules from governance
        weak_rules = rule_governance.get("weak_rules", [])
        if isinstance(weak_rules, list):
            for rule in weak_rules[:3]:
                rule_id    = rule.get("rule_id", "unknown") if isinstance(rule, dict) else str(rule)
                confidence = rule.get("confidence", "weak") if isinstance(rule, dict) else "weak"
                sample_count = rule.get("sample_count", 0) if isinstance(rule, dict) else 0
                items.append(self._make_item(
                    rule_id=rule_id,
                    reason="Weak confidence — review or add sample data.",
                    confidence=confidence,
                    sample_count=sample_count,
                    priority=PRIORITY_P2,
                    due_type=DUE_THIS_WEEK,
                    tags=["rule", "weak"],
                ))

        # Transcript-derived rules needing backtest
        transcript_candidates = rule_governance.get("transcript_candidates", [])
        if isinstance(transcript_candidates, list):
            for rule in transcript_candidates[:3]:
                rule_id    = rule.get("rule_id", "unknown") if isinstance(rule, dict) else str(rule)
                items.append(self._make_item(
                    rule_id=rule_id,
                    reason="Transcript-derived rule candidate — needs formal backtest.",
                    confidence="planned",
                    sample_count=0,
                    priority=PRIORITY_P3,
                    due_type=DUE_THIS_WEEK,
                    tags=["rule", "transcript", "needs_backtest"],
                ))

        # ML knowledge feature needs mapping
        ml_needs_backtest = rule_governance.get("ml_needs_backtest", [])
        if isinstance(ml_needs_backtest, list):
            for feature in ml_needs_backtest[:3]:
                feature_id = feature.get("feature_id", "unknown") if isinstance(feature, dict) else str(feature)
                items.append(self._make_item(
                    rule_id=feature_id,
                    reason="ML knowledge feature candidate — needs rule mapping and backtest.",
                    confidence="unknown",
                    sample_count=0,
                    priority=PRIORITY_P2,
                    due_type=DUE_THIS_WEEK,
                    tags=["rule", "ml", "needs_mapping"],
                ))

        # From review_summary: weak_rules count
        weak_rule_count = int(review_summary.get("weak_rules", 0) or 0)
        if weak_rule_count > 0 and not items:
            items.append(self._make_item(
                rule_id="multiple",
                reason=f"{weak_rule_count} weak rules detected in Research Review. Run rule governance to identify.",
                confidence="weak",
                sample_count=0,
                priority=PRIORITY_P2,
                due_type=DUE_THIS_WEEK,
                tags=["rule", "weak"],
            ))

        return items

    @staticmethod
    def _make_item(
        rule_id:      str,
        reason:       str,
        confidence:   str,
        sample_count: int,
        priority:     str,
        due_type:     str,
        tags:         List[str],
    ) -> CoachRecommendation:
        return CoachRecommendation(
            recommendation_type=REC_RULE_REVIEW,
            priority=priority,
            category=CAT_RULE,
            title=f"Rule Review: {rule_id}",
            summary=reason,
            rationale=f"confidence={confidence}, sample_count={sample_count}",
            suggested_command="python main.py rule-governance --mode real",
            expected_benefit="Identify and validate rules needing more data or review.",
            effort_level=EFFORT_MEDIUM,
            due_type=due_type,
            tags=tags,
            status=STATUS_OPEN,
        )
