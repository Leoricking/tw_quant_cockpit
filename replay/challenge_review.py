"""
replay/challenge_review.py — ReplayChallengeReviewManager v1.2.7

[!] Outcome Reveal requires both --reveal AND --confirm-review.
[!] Review never auto-Confirms Mistakes.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayChallengeReviewManager:
    """
    Manages challenge attempt reviews.

    Outcome Reveal requires explicit=True AND confirm_review=True.
    Review never auto-Confirms Mistakes.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    AUTO_CONFIRM_MISTAKE = False
    AUTO_REVEAL_OUTCOME = False

    def __init__(self) -> None:
        self._reviews: Dict[str, Dict[str, Any]] = {}
        self._notes: Dict[str, List[str]] = {}
        self._tags: Dict[str, List[str]] = {}

    def build_review(self, attempt_id: str, attempt: Dict[str, Any], score: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build a review for a challenge attempt."""
        from replay.challenge_schema import _now_utc
        score_data = score or {}
        score_obj = score_data.get("score")

        review = {
            "attempt_id": attempt_id,
            "challenge_id": attempt.get("challenge_id", ""),
            "challenge_objective": attempt.get("objective", ""),
            "user_actions": attempt.get("actions", []),
            "decision_timeline": self._build_timeline(attempt.get("actions", [])),
            "time_used": attempt.get("active_elapsed_seconds", 0.0),
            "hints_used": attempt.get("hints_used", 0),
            "process_score": float(getattr(score_obj, "process_score", 0.0)) if score_obj else 0.0,
            "total_score": float(getattr(score_obj, "total_score", 0.0)) if score_obj else 0.0,
            "classification": getattr(score_obj, "classification", "PROCESS_ONLY") if score_obj else "PROCESS_ONLY",
            "rule_compliance": "Not evaluated",
            "suggested_mistakes": score_data.get("suggested_mistakes", []),
            "strategy_context": "Review strategy context here",
            "mtf_context": "Review multi-timeframe context here",
            "pit_integrity": True,
            "outcome_revealed": False,
            "outcome": "NOT_REVEALED",
            "better_alternatives": [],
            "limitations": [
                "This is a training simulation only.",
                "Scores do not represent investment ability.",
                "No real orders were placed.",
            ],
            "safety_declaration": (
                "[!] Challenge Training Only. Simulation Only. No Real Orders. "
                "Not Investment Advice. Process weight >= Outcome weight."
            ),
            "review_status": "DRAFT",
            "created_at": _now_utc(),
            "auto_confirm_mistake": False,
            "research_only": True,
            "no_real_orders": True,
        }
        self._reviews[attempt_id] = review
        return review

    def reveal_outcome(
        self,
        attempt_id: str,
        explicit: bool = False,
        confirm_review: bool = False,
    ) -> Dict[str, Any]:
        """
        Reveal outcome for an attempt.
        Requires both explicit=True AND confirm_review=True.
        """
        if not explicit or not confirm_review:
            return {
                "status": "BLOCKED",
                "message": (
                    "Outcome reveal requires both explicit=True AND confirm_review=True. "
                    "Use --reveal --confirm-review flags."
                ),
                "outcome": "NOT_REVEALED",
                "auto_reveal": False,
                "research_only": True,
            }
        if attempt_id not in self._reviews:
            return {"status": "NOT_FOUND", "attempt_id": attempt_id}
        self._reviews[attempt_id]["outcome_revealed"] = True
        self._reviews[attempt_id]["outcome"] = "REVEALED_EXPLICIT"
        return {
            "status": "REVEALED",
            "attempt_id": attempt_id,
            "explicit_reveal": True,
            "confirm_review": True,
            "outcome": "REVEALED_EXPLICIT",
            "auto_confirm_mistake": False,
            "research_only": True,
        }

    def compare_with_reference(self, attempt_id: str, reference_id: str) -> Dict[str, Any]:
        """Compare attempt with a reference attempt."""
        return {
            "attempt_id": attempt_id,
            "reference_id": reference_id,
            "comparison": "Not available without reference data",
            "research_only": True,
        }

    def compare_attempts(self, attempt_a: str, attempt_b: str) -> Dict[str, Any]:
        """Compare two attempts."""
        return {
            "attempt_a": attempt_a,
            "attempt_b": attempt_b,
            "comparison": "Not available",
            "research_only": True,
        }

    def add_note(self, attempt_id: str, note: str) -> Dict[str, Any]:
        """Add a review note (append-only)."""
        if attempt_id not in self._notes:
            self._notes[attempt_id] = []
        self._notes[attempt_id].append(note)
        return {"status": "OK", "attempt_id": attempt_id, "note_count": len(self._notes[attempt_id])}

    def add_tag(self, attempt_id: str, tag: str) -> Dict[str, Any]:
        """Add a review tag."""
        if attempt_id not in self._tags:
            self._tags[attempt_id] = []
        if tag not in self._tags[attempt_id]:
            self._tags[attempt_id].append(tag)
        return {"status": "OK", "attempt_id": attempt_id, "tags": self._tags[attempt_id]}

    def finalize_review(self, attempt_id: str) -> Dict[str, Any]:
        """Finalize a review."""
        if attempt_id not in self._reviews:
            return {"status": "NOT_FOUND"}
        self._reviews[attempt_id]["review_status"] = "FINALIZED"
        return {"status": "FINALIZED", "attempt_id": attempt_id}

    def reopen_review(self, attempt_id: str) -> Dict[str, Any]:
        """Reopen a finalized review."""
        if attempt_id not in self._reviews:
            return {"status": "NOT_FOUND"}
        self._reviews[attempt_id]["review_status"] = "REOPENED"
        return {"status": "REOPENED", "attempt_id": attempt_id}

    def history(self, attempt_id: str) -> List[Dict[str, Any]]:
        """Return review history for an attempt."""
        review = self._reviews.get(attempt_id)
        return [review] if review else []

    def _build_timeline(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {
                "elapsed": a.get("elapsed_since_start", 0.0),
                "action_type": a.get("action_type", ""),
                "created_at": a.get("created_at", ""),
            }
            for a in actions
        ]
