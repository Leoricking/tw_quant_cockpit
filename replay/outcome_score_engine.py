"""
replay/outcome_score_engine.py — ReplayOutcomeScoreEngine for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Outcome score only available AFTER explicit outcome reveal.
[!] Default: BLOCKED. Must have --reveal AND --confirm-review flags.
[!] Missing outcome data shows INSUFFICIENT, does NOT crash.
[!] Scoring NEVER triggers paper orders or broker execution.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
SCORING_TRIGGERS_NO_ORDERS = True
AUTO_OUTCOME_REVEAL_ENABLED = False


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_score_id() -> str:
    return f"OSC-{uuid.uuid4().hex[:12].upper()}"


class ReplayOutcomeScoreEngine:
    """
    Calculates outcome scores after explicit outcome reveal.

    [!] Default: BLOCKED. Requires explicit reveal record.
    [!] Missing outcome data shows INSUFFICIENT, does NOT crash.
    [!] Scoring NEVER triggers paper orders or broker execution.
    [!] AUTO_OUTCOME_REVEAL_ENABLED = False (invariant).
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    SCORING_TRIGGERS_NO_ORDERS = True
    AUTO_OUTCOME_REVEAL_ENABLED = False

    GOOD_OUTCOME_THRESHOLD = 60.0

    def score(
        self,
        session_id: str,
        reveal_record: Optional[Dict[str, Any]] = None,
        journal_entry: Optional[Dict[str, Any]] = None,
        notes: str = "",
    ) -> "ReplayOutcomeScore":
        """
        Calculate outcome score after explicit reveal.
        Returns BLOCKED if reveal_record is missing or not confirmed.
        Returns INSUFFICIENT if data is missing — does NOT crash.
        """
        from replay.scoring_schema import (
            ReplayOutcomeScore, OutcomeRevealStatus,
            ScoreConfidenceLevel,
        )

        entry = journal_entry or {}

        # Guard: No reveal record → BLOCKED
        if not reveal_record:
            return ReplayOutcomeScore(
                score_id=_new_score_id(),
                session_id=session_id,
                reveal_id="",
                journal_entry_id=entry.get("journal_entry_id"),
                decision_id=entry.get("decision_id"),
                symbol=entry.get("symbol", ""),
                status=OutcomeRevealStatus.BLOCKED.value,
                confidence_level=ScoreConfidenceLevel.INSUFFICIENT.value,
                confidence_note="Outcome reveal required before scoring. Use --reveal --confirm-review.",
                warnings=["BLOCKED: Outcome not revealed."],
            )

        reveal_status = reveal_record.get("status", OutcomeRevealStatus.BLOCKED.value)
        reveal_confirmed = bool(reveal_record.get("reveal_confirmed", False))
        confirm_review_flag = bool(reveal_record.get("confirm_review_flag", False))

        # Guard: Not confirmed
        if not reveal_confirmed or not confirm_review_flag:
            return ReplayOutcomeScore(
                score_id=_new_score_id(),
                session_id=session_id,
                reveal_id=reveal_record.get("reveal_id", ""),
                journal_entry_id=entry.get("journal_entry_id"),
                decision_id=entry.get("decision_id"),
                symbol=entry.get("symbol", ""),
                status=OutcomeRevealStatus.BLOCKED.value,
                confidence_level=ScoreConfidenceLevel.INSUFFICIENT.value,
                confidence_note="Outcome reveal not confirmed. --confirm-review required.",
                warnings=["BLOCKED: reveal_confirmed=False or confirm_review_flag=False."],
            )

        if reveal_status != OutcomeRevealStatus.REVEALED.value:
            return ReplayOutcomeScore(
                score_id=_new_score_id(),
                session_id=session_id,
                reveal_id=reveal_record.get("reveal_id", ""),
                journal_entry_id=entry.get("journal_entry_id"),
                decision_id=entry.get("decision_id"),
                symbol=entry.get("symbol", ""),
                status=reveal_status,
                confidence_level=ScoreConfidenceLevel.INSUFFICIENT.value,
                confidence_note=f"Outcome reveal status: {reveal_status}",
                warnings=[f"Outcome reveal status is {reveal_status}, expected REVEALED."],
            )

        # Outcome data summary
        outcome_summary = reveal_record.get("outcome_data_summary", "")
        reveal_window_bars = int(reveal_record.get("reveal_window_bars", 0))

        if not outcome_summary:
            return ReplayOutcomeScore(
                score_id=_new_score_id(),
                session_id=session_id,
                reveal_id=reveal_record.get("reveal_id", ""),
                journal_entry_id=entry.get("journal_entry_id"),
                decision_id=entry.get("decision_id"),
                symbol=entry.get("symbol", ""),
                reveal_window_bars=reveal_window_bars,
                status=OutcomeRevealStatus.PARTIAL.value,
                confidence_level=ScoreConfidenceLevel.INSUFFICIENT.value,
                confidence_note="Outcome data missing — INSUFFICIENT (not a crash).",
                warnings=["INSUFFICIENT: outcome_data_summary is empty."],
            )

        # Simple outcome label scoring
        outcome_score, outcome_label, outcome_notes = self._calculate_outcome(
            outcome_summary, reveal_window_bars, entry
        )

        return ReplayOutcomeScore(
            score_id=_new_score_id(),
            session_id=session_id,
            reveal_id=reveal_record.get("reveal_id", ""),
            journal_entry_id=entry.get("journal_entry_id"),
            decision_id=entry.get("decision_id"),
            symbol=entry.get("symbol", reveal_record.get("symbol", "")),
            reveal_window_bars=reveal_window_bars,
            outcome_score=outcome_score,
            outcome_label=outcome_label,
            outcome_notes=outcome_notes,
            status=OutcomeRevealStatus.REVEALED.value,
            confidence_level=ScoreConfidenceLevel.OBSERVATIONAL.value,
            confidence_note="Single session outcome — OBSERVATIONAL only.",
            warnings=["Single session outcome is OBSERVATIONAL. Not a strategy conclusion."],
        )

    def _calculate_outcome(
        self,
        outcome_summary: str,
        reveal_window_bars: int,
        entry: Dict[str, Any],
    ):
        """Derive a simple outcome score from summary text."""
        summary_lower = outcome_summary.lower()
        action = entry.get("action", "")

        # WAIT/SKIP with good outcome handling
        if action in ("WAIT", "SKIP"):
            return 75.0, "WAIT_OR_SKIP_VALIDATED", (
                f"WAIT/SKIP decision outcome: {outcome_summary[:100]}"
            )

        # Heuristic outcome classification
        positive_signals = ["breakout", "gained", "rose", "advanced", "confirmed", "target reached"]
        negative_signals = ["declined", "fell", "broke down", "failed", "stopped out", "loss"]

        pos_count = sum(1 for s in positive_signals if s in summary_lower)
        neg_count = sum(1 for s in negative_signals if s in summary_lower)

        if pos_count > neg_count:
            score = 70.0 + min(pos_count * 5, 25.0)
            label = "FAVORABLE_OUTCOME"
        elif neg_count > pos_count:
            score = 30.0 - min(neg_count * 5, 20.0)
            label = "UNFAVORABLE_OUTCOME"
        else:
            score = 50.0
            label = "NEUTRAL_OUTCOME"

        notes = (
            f"Outcome window: {reveal_window_bars} bars. "
            f"Summary: {outcome_summary[:100]}"
        )
        return round(max(0.0, min(score, 100.0)), 2), label, notes

    def is_good_outcome(self, outcome_score: float) -> bool:
        return outcome_score >= self.GOOD_OUTCOME_THRESHOLD
