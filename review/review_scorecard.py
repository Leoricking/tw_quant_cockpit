"""
review/review_scorecard.py — ResearchReviewScorecard (v0.4.7).

Calculates Daily / Weekly Research Scorecard from aggregated summary.

[!] Review Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import Dict

logger = logging.getLogger(__name__)

# Grade constants
GRADE_STRONG  = "STRONG"
GRADE_GOOD    = "GOOD"
GRADE_PARTIAL = "PARTIAL"
GRADE_WEAK    = "WEAK"
GRADE_BLOCKED = "BLOCKED"
GRADE_UNKNOWN = "UNKNOWN"

ALL_GRADES = [GRADE_STRONG, GRADE_GOOD, GRADE_PARTIAL, GRADE_WEAK, GRADE_BLOCKED, GRADE_UNKNOWN]

_GRADE_RANK = {g: i for i, g in enumerate(ALL_GRADES)}


def _grade(score: float) -> str:
    if score >= 85:
        return GRADE_STRONG
    if score >= 70:
        return GRADE_GOOD
    if score >= 50:
        return GRADE_PARTIAL
    if score >= 30:
        return GRADE_WEAK
    return GRADE_BLOCKED


class ResearchReviewScorecard:
    """
    Calculates Research Review Scorecard from aggregated summary dict.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
      No auto-weight changes. No order submission.
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __init__(self):
        pass

    def calculate(self, aggregated_summary: dict) -> dict:
        """
        Calculate all scorecard dimensions from aggregated_summary.

        Returns a dict with scores and grades for each dimension.
        """
        safety_score          = self._calc_safety_score(aggregated_summary)
        data_health_score     = self._calc_data_health_score(aggregated_summary)
        signal_health_score   = self._calc_signal_health_score(aggregated_summary)
        rule_health_score     = self._calc_rule_health_score(aggregated_summary)
        model_health_score    = self._calc_model_health_score(aggregated_summary)
        replay_training_score = self._calc_replay_training_score(aggregated_summary)
        journal_completion_score = self._calc_journal_completion_score(aggregated_summary)
        process_quality_score = self._calc_process_quality_score(aggregated_summary)

        # Critical safety issue caps overall at BLOCKED
        has_critical_safety = (
            not aggregated_summary.get("production_blocked", True)
            or aggregated_summary.get("real_order_ready", False)
            or aggregated_summary.get("critical_items", 0) > 3
        )

        component_scores = [
            safety_score, data_health_score, signal_health_score,
            rule_health_score, model_health_score, replay_training_score,
            journal_completion_score, process_quality_score,
        ]
        overall = sum(component_scores) / len(component_scores)

        if has_critical_safety:
            overall_grade = GRADE_BLOCKED
        else:
            overall_grade = _grade(overall)

        scorecard = {
            "overall_review_score":      round(overall, 1),
            "overall_grade":             overall_grade,
            "process_quality_score":     round(process_quality_score, 1),
            "process_quality_grade":     _grade(process_quality_score),
            "data_health_score":         round(data_health_score, 1),
            "data_health_grade":         _grade(data_health_score),
            "signal_health_score":       round(signal_health_score, 1),
            "signal_health_grade":       _grade(signal_health_score),
            "rule_health_score":         round(rule_health_score, 1),
            "rule_health_grade":         _grade(rule_health_score),
            "model_health_score":        round(model_health_score, 1),
            "model_health_grade":        _grade(model_health_score),
            "replay_training_score":     round(replay_training_score, 1),
            "replay_training_grade":     _grade(replay_training_score),
            "journal_completion_score":  round(journal_completion_score, 1),
            "journal_completion_grade":  _grade(journal_completion_score),
            "safety_score":              round(safety_score, 1),
            "safety_grade":              _grade(safety_score),
            # Safety flags
            "read_only":          True,
            "no_real_orders":     True,
            "production_blocked": True,
        }
        logger.info("[scorecard] overall=%.1f (%s)", overall, overall_grade)
        return scorecard

    # ------------------------------------------------------------------
    # Dimension calculators
    # ------------------------------------------------------------------

    def _calc_safety_score(self, s: dict) -> float:
        """Safety score: 100 if no_real_orders and production_blocked."""
        score = 100.0
        if not s.get("production_blocked", True):
            score -= 80
        if s.get("real_order_ready", False):
            score -= 80
        score = max(0.0, score)
        return score

    def _calc_data_health_score(self, s: dict) -> float:
        """Lower score for more data blockers."""
        blockers = s.get("data_blockers", 0)
        if blockers == 0:
            return 90.0
        return max(0.0, 90.0 - blockers * 20.0)

    def _calc_signal_health_score(self, s: dict) -> float:
        """Lower for more weak/disable signals."""
        weak = s.get("total_weak_signals", 0)
        if weak == 0:
            return 85.0
        return max(30.0, 85.0 - weak * 10.0)

    def _calc_rule_health_score(self, s: dict) -> float:
        """Lower for more weak rules."""
        weak = s.get("weak_rules", 0)
        if weak == 0:
            return 85.0
        return max(20.0, 85.0 - weak * 5.0)

    def _calc_model_health_score(self, s: dict) -> float:
        """Lower for drift/degradation warnings."""
        drift = s.get("model_warnings", 0)
        if drift == 0:
            return 80.0
        return max(10.0, 80.0 - drift * 15.0)

    def _calc_replay_training_score(self, s: dict) -> float:
        """Lower if training is overdue."""
        if s.get("replay_training_overdue", True):
            return 40.0
        return 85.0

    def _calc_journal_completion_score(self, s: dict) -> float:
        """Lower for more journal entries requiring review."""
        review_req = s.get("journal_review_required", 0)
        if review_req == 0:
            return 90.0
        return max(20.0, 90.0 - review_req * 10.0)

    def _calc_process_quality_score(self, s: dict) -> float:
        """Lower for repeated top mistakes."""
        top_mistakes = s.get("top_mistakes", [])
        most_common  = s.get("most_common_mistake", "")
        penalty = len(top_mistakes) * 5.0
        if most_common:
            penalty += 10.0
        return max(10.0, 90.0 - penalty)
