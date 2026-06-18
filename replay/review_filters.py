"""
replay/review_filters.py — Replay Review Filters v1.2.6

Filters: session_status, review_status, outcome_revealed, classification,
score_range, mistake_severity, strategy_conflict, timeframe_conflict,
confidence, qualification, mode(real/mock), date_range.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayReviewFilters:
    """
    Filter builder for replay review tables.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def apply(self, rows: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply all specified filters to a list of row dicts."""
        result = list(rows)

        session_status = filters.get("session_status")
        if session_status:
            result = [r for r in result if r.get("status") == session_status]

        review_status = filters.get("review_status")
        if review_status:
            result = [r for r in result if r.get("review_progress") == review_status]

        outcome_revealed = filters.get("outcome_revealed")
        if outcome_revealed is not None:
            result = [r for r in result if r.get("outcome_revealed") == outcome_revealed]

        classification = filters.get("classification")
        if classification:
            result = [r for r in result if r.get("classification") == classification]

        score_range: Optional[Tuple[float, float]] = filters.get("score_range")
        if score_range:
            lo, hi = score_range
            result = [
                r for r in result
                if r.get("process_score") is not None and lo <= r["process_score"] <= hi
            ]

        strategy_conflict = filters.get("strategy_conflict")
        if strategy_conflict is not None:
            if strategy_conflict:
                result = [r for r in result if r.get("strategy_conflicts", 0) > 0]
            else:
                result = [r for r in result if r.get("strategy_conflicts", 0) == 0]

        timeframe_conflict = filters.get("timeframe_conflict")
        if timeframe_conflict is not None:
            if timeframe_conflict:
                result = [r for r in result if r.get("mtf_conflicts", 0) > 0]
            else:
                result = [r for r in result if r.get("mtf_conflicts", 0) == 0]

        confidence = filters.get("confidence")
        if confidence:
            result = [r for r in result if r.get("confidence") == confidence]

        mode = filters.get("mode")
        if mode:
            result = [r for r in result if r.get("mode") == mode]

        date_from = filters.get("date_from")
        if date_from:
            result = [r for r in result if r.get("created_at", "") >= date_from]

        date_to = filters.get("date_to")
        if date_to:
            result = [r for r in result if r.get("created_at", "") <= date_to]

        return result

    def filter_real_only(self, rows: List[Dict]) -> List[Dict]:
        return self.apply(rows, {"mode": "real"})

    def filter_mock_only(self, rows: List[Dict]) -> List[Dict]:
        return self.apply(rows, {"mode": "mock"})

    def filter_review_complete(self, rows: List[Dict]) -> List[Dict]:
        return [r for r in rows if r.get("review_complete")]

    def filter_outcome_revealed(self, rows: List[Dict]) -> List[Dict]:
        return [r for r in rows if r.get("outcome_revealed")]

    def filter_high_confidence(self, rows: List[Dict]) -> List[Dict]:
        return self.apply(rows, {"confidence": "SUFFICIENT"})

    def filter_low_confidence(self, rows: List[Dict]) -> List[Dict]:
        return [r for r in rows if r.get("confidence") in ("LOW", "INSUFFICIENT")]

    def available_filters(self) -> Dict[str, Any]:
        return {
            "session_status":   ["ACTIVE", "COMPLETED", "ARCHIVED", "UNKNOWN"],
            "review_status":    ["NOT_STARTED", "IN_PROGRESS", "REVIEW_COMPLETE", "BLOCKED", "INSUFFICIENT"],
            "outcome_revealed": [True, False],
            "classification":   ["GOOD_PROCESS_GOOD_OUTCOME", "GOOD_PROCESS_BAD_OUTCOME",
                                  "BAD_PROCESS_GOOD_OUTCOME", "BAD_PROCESS_BAD_OUTCOME", "UNCLASSIFIED"],
            "score_range":      "tuple (min, max) float 0-100",
            "strategy_conflict": [True, False],
            "timeframe_conflict": [True, False],
            "confidence":       ["SUFFICIENT", "LOW", "INSUFFICIENT"],
            "mode":             ["real", "mock"],
            "date_from":        "ISO date string",
            "date_to":          "ISO date string",
            "research_only":    True,
        }
