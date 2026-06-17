"""
replay/composite_score_engine.py — ReplayCompositeScoreEngine for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Before outcome reveal: PROCESS_ONLY (not COMPOSITE).
[!] outcome_weight > 0.5 shows warning.
[!] Default process_weight=0.70, outcome_weight=0.30.
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


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_score_id() -> str:
    return f"CSC-{uuid.uuid4().hex[:12].upper()}"


class ReplayCompositeScoreEngine:
    """
    Builds composite scores from process and outcome components.

    [!] Before outcome reveal: PROCESS_ONLY (not COMPOSITE).
    [!] outcome_weight > 0.5 shows warning.
    [!] Scoring NEVER triggers paper orders or broker execution.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    SCORING_TRIGGERS_NO_ORDERS = True

    DEFAULT_PROCESS_WEIGHT = 0.70
    DEFAULT_OUTCOME_WEIGHT = 0.30
    OUTCOME_WEIGHT_WARNING_THRESHOLD = 0.50

    GOOD_THRESHOLD = 60.0

    def build(
        self,
        session_id: str,
        process_score: Optional[Dict[str, Any]] = None,
        outcome_score: Optional[Dict[str, Any]] = None,
        process_weight: float = DEFAULT_PROCESS_WEIGHT,
        outcome_weight: float = DEFAULT_OUTCOME_WEIGHT,
        journal_entry: Optional[Dict[str, Any]] = None,
        notes: str = "",
    ) -> "ReplayCompositeScore":
        """
        Build composite score.
        Returns PROCESS_ONLY if outcome is not revealed.
        Returns BLOCKED if nothing is available.
        """
        from replay.scoring_schema import (
            ReplayCompositeScore, CompositeScoreStatus,
            CompositeClassification, ScoreConfidenceLevel,
        )

        entry = journal_entry or {}
        warnings: List[str] = []
        flags: List[str] = []

        # Validate weights
        total_weight = process_weight + outcome_weight
        if abs(total_weight - 1.0) > 0.01:
            warnings.append(
                f"process_weight + outcome_weight = {total_weight:.2f} (should be 1.0). "
                f"Normalizing."
            )
            if total_weight > 0:
                process_weight = process_weight / total_weight
                outcome_weight = outcome_weight / total_weight

        if outcome_weight > self.OUTCOME_WEIGHT_WARNING_THRESHOLD:
            warnings.append(
                f"[WARNING] outcome_weight={outcome_weight:.2f} > 0.5. "
                "Outcome-heavy weighting is not recommended for research training."
            )

        # No process score → BLOCKED
        if not process_score:
            return ReplayCompositeScore(
                score_id=_new_score_id(),
                session_id=session_id,
                journal_entry_id=entry.get("journal_entry_id"),
                decision_id=entry.get("decision_id"),
                symbol=entry.get("symbol", ""),
                classification=CompositeClassification.BLOCKED.value,
                status=CompositeScoreStatus.BLOCKED.value,
                confidence_level=ScoreConfidenceLevel.INSUFFICIENT.value,
                confidence_note="No process score available.",
                notes=notes,
                warnings=["BLOCKED: No process score available."],
            )

        ps_total = float(process_score.get("total_score", 0.0))
        ps_id = process_score.get("score_id")
        ps_status = process_score.get("status", "")

        if ps_status in ("INSUFFICIENT_DATA", "BLOCKED"):
            return ReplayCompositeScore(
                score_id=_new_score_id(),
                session_id=session_id,
                process_score_id=ps_id,
                journal_entry_id=entry.get("journal_entry_id"),
                decision_id=entry.get("decision_id"),
                symbol=entry.get("symbol", ""),
                process_score=ps_total,
                process_weight=process_weight,
                outcome_weight=outcome_weight,
                classification=CompositeClassification.INSUFFICIENT.value,
                status=CompositeScoreStatus.INSUFFICIENT.value,
                confidence_level=ScoreConfidenceLevel.INSUFFICIENT.value,
                confidence_note="Process score is insufficient.",
                notes=notes,
                warnings=[f"INSUFFICIENT: process_score status={ps_status}."],
            )

        # Check outcome availability
        outcome_available = False
        os_total = None
        os_id = None

        if outcome_score:
            os_status = outcome_score.get("status", "BLOCKED")
            if os_status == "REVEALED":
                outcome_available = True
                os_total = float(outcome_score.get("outcome_score", 0.0))
                os_id = outcome_score.get("score_id")

        # Determine classification
        ps_good = ps_total >= self.GOOD_THRESHOLD

        if not outcome_available:
            # PROCESS_ONLY mode
            classification = CompositeClassification.PROCESS_ONLY.value
            status = CompositeScoreStatus.PROCESS_ONLY.value
            composite = ps_total  # Just process score
            confidence = ScoreConfidenceLevel.OBSERVATIONAL.value
            confidence_note = "PROCESS_ONLY — outcome not revealed."
            warnings.append("Outcome not revealed — composite is PROCESS_ONLY.")
        else:
            os_good = os_total >= self.GOOD_THRESHOLD
            if ps_good and os_good:
                classification = CompositeClassification.GOOD_PROCESS_GOOD_OUTCOME.value
            elif ps_good and not os_good:
                classification = CompositeClassification.GOOD_PROCESS_BAD_OUTCOME.value
            elif not ps_good and os_good:
                classification = CompositeClassification.BAD_PROCESS_GOOD_OUTCOME.value
            else:
                classification = CompositeClassification.BAD_PROCESS_BAD_OUTCOME.value

            status = CompositeScoreStatus.COMPOSITE.value
            composite = round(ps_total * process_weight + os_total * outcome_weight, 2)
            confidence = ScoreConfidenceLevel.OBSERVATIONAL.value
            confidence_note = "Single session composite — OBSERVATIONAL."

        return ReplayCompositeScore(
            score_id=_new_score_id(),
            session_id=session_id,
            process_score_id=ps_id,
            outcome_score_id=os_id,
            journal_entry_id=entry.get("journal_entry_id"),
            decision_id=entry.get("decision_id"),
            symbol=entry.get("symbol", ""),
            process_score=ps_total,
            outcome_score=os_total,
            process_weight=process_weight,
            outcome_weight=outcome_weight,
            composite_score=composite,
            classification=classification,
            status=status,
            confidence_level=confidence,
            confidence_note=confidence_note,
            notes=notes,
            flags=flags,
            warnings=warnings,
        )


# Fix missing import
from typing import List  # noqa: E402 — placed after class to avoid circular issues
