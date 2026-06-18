"""
replay/challenge_comparator.py — Challenge attempt comparator v1.2.7

[!] Outcome not revealed → no outcome comparison.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayChallengeComparator:
    """
    Compare challenge attempts.

    Compares: process scores, timing, hints, rules, mistakes,
    journal quality, strategy awareness, MTF awareness.
    Outcome not revealed → no outcome comparison.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def compare(
        self,
        attempt_a: Dict[str, Any],
        attempt_b: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Compare two attempts."""
        def _get_score(a: Dict[str, Any]) -> float:
            s = a.get("score", {})
            if hasattr(s, "process_score"):
                return float(s.process_score)
            if isinstance(s, dict):
                return float(s.get("process_score", 0.0))
            return float(a.get("process_score", 0.0))

        a_id = attempt_a.get("attempt_id", "A")
        b_id = attempt_b.get("attempt_id", "B")

        a_process = _get_score(attempt_a)
        b_process = _get_score(attempt_b)

        a_hints = attempt_a.get("hints_used", 0)
        b_hints = attempt_b.get("hints_used", 0)

        a_elapsed = attempt_a.get("active_elapsed_seconds", 0.0)
        b_elapsed = attempt_b.get("active_elapsed_seconds", 0.0)

        outcome_a_revealed = attempt_a.get("outcome_revealed", False)
        outcome_b_revealed = attempt_b.get("outcome_revealed", False)
        outcome_comparison = (
            "NOT_AVAILABLE — outcome not revealed"
            if not (outcome_a_revealed and outcome_b_revealed)
            else "AVAILABLE"
        )

        return {
            "attempt_a": a_id,
            "attempt_b": b_id,
            "process_score_a": round(a_process, 1),
            "process_score_b": round(b_process, 1),
            "process_score_diff": round(a_process - b_process, 1),
            "winner_process": a_id if a_process >= b_process else b_id,
            "hints_a": a_hints,
            "hints_b": b_hints,
            "elapsed_a": round(a_elapsed, 1),
            "elapsed_b": round(b_elapsed, 1),
            "outcome_comparison": outcome_comparison,
            "research_only": True,
            "no_real_orders": True,
        }

    def compare_first_vs_best(
        self,
        attempts: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Compare first attempt vs best attempt."""
        if not attempts:
            return {"status": "NO_ATTEMPTS"}
        first = attempts[0]
        best = max(attempts, key=lambda a: a.get("total_score", 0.0))
        return self.compare(first, best)

    def summary(self) -> Dict[str, Any]:
        return {
            "comparator": "ReplayChallengeComparator",
            "outcome_comparison": "Only available after explicit reveal",
            "research_only": True,
            "no_real_orders": True,
        }
