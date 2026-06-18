"""
replay/review_progress.py — ReplayReviewProgressCalculator v1.2.6

Calculates review progress for each session.
Required steps: session_completed, journal_exists, process_score_calculated,
suggested_mistakes_reviewed, strategy_conflicts_reviewed,
timeframe_conflicts_reviewed, point_in_time_verified, review_note_added.
Optional steps: outcome_revealed, outcome_score_calculated,
composite_score_calculated, final_report_generated.

[!] PROCESS_REVIEW_COMPLETE != FULL_REVIEW_COMPLETE.
[!] Outcome Reveal is NOT required for PROCESS_REVIEW_COMPLETE.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from replay.review_dashboard_schema import (
    ReplayReviewProgress,
    ReviewProgressStatus,
    _new_id,
    _now_utc,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

REQUIRED_STEPS = [
    "session_completed",
    "journal_exists",
    "process_score_calculated",
    "suggested_mistakes_reviewed",
    "strategy_conflicts_reviewed",
    "timeframe_conflicts_reviewed",
    "point_in_time_verified",
    "review_note_added",
]

OPTIONAL_STEPS = [
    "outcome_revealed",
    "outcome_score_calculated",
    "composite_score_calculated",
    "final_report_generated",
]


class ReplayReviewProgressCalculator:
    """
    Calculates review progress for a session.

    [!] PROCESS_REVIEW_COMPLETE does NOT require Outcome Reveal.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True
    OUTCOME_REVEAL_REQUIRED = False

    def calculate(self, session_id: str, session_data: Optional[Dict[str, Any]] = None) -> ReplayReviewProgress:
        """Calculate progress for a session."""
        data = session_data or {}
        progress_id = _new_id("PRG-")

        # Evaluate required steps
        step_values: Dict[str, bool] = {}
        for step in REQUIRED_STEPS:
            step_values[step] = bool(data.get(step, False))

        for step in OPTIONAL_STEPS:
            step_values[step] = bool(data.get(step, False))

        req_complete = sum(1 for s in REQUIRED_STEPS if step_values[s])
        opt_complete = sum(1 for s in OPTIONAL_STEPS if step_values[s])

        pct = round(req_complete / len(REQUIRED_STEPS) * 100, 1)

        process_review_complete = req_complete == len(REQUIRED_STEPS)
        full_review_complete    = process_review_complete and opt_complete == len(OPTIONAL_STEPS)

        # Status determination
        if process_review_complete and full_review_complete:
            status = ReviewProgressStatus.REVIEW_COMPLETE.value
        elif req_complete > 0:
            status = ReviewProgressStatus.IN_PROGRESS.value
        elif data.get("_blocked"):
            status = ReviewProgressStatus.BLOCKED.value
        elif not data:
            status = ReviewProgressStatus.INSUFFICIENT.value
        else:
            status = ReviewProgressStatus.NOT_STARTED.value

        blocked_steps = [s for s in REQUIRED_STEPS if data.get(f"{s}_blocked")]
        missing_items = [s for s in REQUIRED_STEPS if not step_values[s]]

        explanation = self.explain(req_complete, process_review_complete, full_review_complete)

        return ReplayReviewProgress(
            progress_id=progress_id,
            session_id=session_id,
            status=status,
            session_completed=step_values["session_completed"],
            journal_exists=step_values["journal_exists"],
            process_score_calculated=step_values["process_score_calculated"],
            suggested_mistakes_reviewed=step_values["suggested_mistakes_reviewed"],
            strategy_conflicts_reviewed=step_values["strategy_conflicts_reviewed"],
            timeframe_conflicts_reviewed=step_values["timeframe_conflicts_reviewed"],
            point_in_time_verified=step_values["point_in_time_verified"],
            review_note_added=step_values["review_note_added"],
            outcome_revealed=step_values["outcome_revealed"],
            outcome_score_calculated=step_values["outcome_score_calculated"],
            composite_score_calculated=step_values["composite_score_calculated"],
            final_report_generated=step_values["final_report_generated"],
            required_steps_complete=req_complete,
            required_steps_total=len(REQUIRED_STEPS),
            optional_steps_complete=opt_complete,
            optional_steps_total=len(OPTIONAL_STEPS),
            progress_percent=pct,
            blocked_steps=blocked_steps,
            missing_items=missing_items,
            explanation=explanation,
            process_review_complete=process_review_complete,
            full_review_complete=full_review_complete,
            outcome_reveal_required=False,
        )

    def required_steps(self) -> List[str]:
        return list(REQUIRED_STEPS)

    def optional_steps(self) -> List[str]:
        return list(OPTIONAL_STEPS)

    def blocked_steps(self, session_data: Dict[str, Any]) -> List[str]:
        return [s for s in REQUIRED_STEPS if session_data.get(f"{s}_blocked")]

    def progress_percent(self, session_data: Dict[str, Any]) -> float:
        done = sum(1 for s in REQUIRED_STEPS if session_data.get(s))
        return round(done / len(REQUIRED_STEPS) * 100, 1)

    def status(self, session_data: Dict[str, Any]) -> str:
        prog = self.calculate("", session_data)
        return prog.status

    def explain(
        self,
        req_complete: int,
        process_review_complete: bool,
        full_review_complete: bool,
    ) -> str:
        if full_review_complete:
            return "Full review complete (including optional steps)."
        if process_review_complete:
            return (
                f"Process review complete ({req_complete}/{len(REQUIRED_STEPS)} required steps). "
                "Outcome reveal is optional."
            )
        return (
            f"{req_complete}/{len(REQUIRED_STEPS)} required steps complete. "
            "Outcome reveal is NOT required for process review completion."
        )
