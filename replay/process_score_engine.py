"""
replay/process_score_engine.py — ReplayProcessScoreEngine for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Process score uses NO future data, NO outcome, NO PnL.
[!] WAIT/SKIP decisions that are well-reasoned should NOT get low scores.
[!] Process score CAN be calculated before outcome reveal.
[!] Scoring NEVER triggers paper orders or broker execution.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
SCORING_TRIGGERS_NO_ORDERS = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_score_id() -> str:
    return f"PSC-{uuid.uuid4().hex[:12].upper()}"


class ReplayProcessScoreEngine:
    """
    Calculates process quality scores for replay sessions.

    [!] NO future data used. NO outcome. NO PnL.
    [!] Process score CAN be calculated before outcome reveal.
    [!] WAIT/SKIP decisions that are well-reasoned should NOT get low scores.
    [!] Scoring NEVER triggers paper orders or broker execution.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    SCORING_TRIGGERS_NO_ORDERS = True

    WEIGHTS = {
        "thesis_quality": 15,
        "risk_planning": 15,
        "discipline_checklist": 15,
        "evidence_quality": 10,
        "confirmation_invalidation": 10,
        "point_in_time_integrity": 10,
        "emotional_awareness": 5,
        "revision_quality": 5,
        "data_sufficiency": 5,
        "scenario_objective": 5,
        "session_completion": 5,
    }

    GOOD_PROCESS_THRESHOLD = 60.0

    def score(
        self,
        session_id: str,
        journal_entry: Optional[Dict[str, Any]] = None,
        session_state: Optional[Dict[str, Any]] = None,
        session_config: Optional[Dict[str, Any]] = None,
        decisions: Optional[List[Dict[str, Any]]] = None,
        notes: str = "",
    ) -> "ReplayProcessScore":
        """
        Calculate process score for a session.
        Returns a ReplayProcessScore dataclass.
        """
        from replay.scoring_schema import (
            ReplayProcessScore, ScoreComponent,
            ProcessScoreStatus, ScoreConfidenceLevel,
        )

        components: List[ScoreComponent] = []
        total = 0.0
        flags: List[str] = []
        warnings: List[str] = []

        entry = journal_entry or {}
        state = session_state or {}
        config = session_config or {}
        decision_list = decisions or []

        # ---- Thesis Quality (15) ----
        tq_score, tq_notes, tq_evidence, tq_missing = self._score_thesis_quality(entry)
        tq_w = self.WEIGHTS["thesis_quality"]
        components.append(ScoreComponent(
            dimension="thesis_quality",
            raw_score=tq_score,
            weight=tq_w,
            weighted_score=tq_score * tq_w,
            rationale=tq_notes,
            evidence_items=tq_evidence,
            missing_items=tq_missing,
        ))
        total += tq_score * tq_w

        # ---- Risk Planning (15) ----
        rp_score, rp_notes, rp_evidence, rp_missing = self._score_risk_planning(entry)
        rp_w = self.WEIGHTS["risk_planning"]
        components.append(ScoreComponent(
            dimension="risk_planning",
            raw_score=rp_score,
            weight=rp_w,
            weighted_score=rp_score * rp_w,
            rationale=rp_notes,
            evidence_items=rp_evidence,
            missing_items=rp_missing,
        ))
        total += rp_score * rp_w

        # ---- Discipline Checklist (15) ----
        dc_score, dc_notes, dc_evidence, dc_missing = self._score_discipline_checklist(entry)
        dc_w = self.WEIGHTS["discipline_checklist"]
        components.append(ScoreComponent(
            dimension="discipline_checklist",
            raw_score=dc_score,
            weight=dc_w,
            weighted_score=dc_score * dc_w,
            rationale=dc_notes,
            evidence_items=dc_evidence,
            missing_items=dc_missing,
        ))
        total += dc_score * dc_w

        # ---- Evidence Quality (10) ----
        eq_score, eq_notes, eq_evidence, eq_missing = self._score_evidence_quality(entry)
        eq_w = self.WEIGHTS["evidence_quality"]
        components.append(ScoreComponent(
            dimension="evidence_quality",
            raw_score=eq_score,
            weight=eq_w,
            weighted_score=eq_score * eq_w,
            rationale=eq_notes,
            evidence_items=eq_evidence,
            missing_items=eq_missing,
        ))
        total += eq_score * eq_w

        # ---- Confirmation/Invalidation (10) ----
        ci_score, ci_notes, ci_evidence, ci_missing = self._score_confirmation_invalidation(entry)
        ci_w = self.WEIGHTS["confirmation_invalidation"]
        components.append(ScoreComponent(
            dimension="confirmation_invalidation",
            raw_score=ci_score,
            weight=ci_w,
            weighted_score=ci_score * ci_w,
            rationale=ci_notes,
            evidence_items=ci_evidence,
            missing_items=ci_missing,
        ))
        total += ci_score * ci_w

        # ---- Point-in-Time Integrity (10) ----
        pit_score, pit_notes, pit_flags = self._score_point_in_time(entry, state)
        pit_w = self.WEIGHTS["point_in_time_integrity"]
        components.append(ScoreComponent(
            dimension="point_in_time_integrity",
            raw_score=pit_score,
            weight=pit_w,
            weighted_score=pit_score * pit_w,
            rationale=pit_notes,
            flags=pit_flags,
        ))
        total += pit_score * pit_w
        flags.extend(pit_flags)

        # ---- Emotional Awareness (5) ----
        ea_score, ea_notes, ea_evidence = self._score_emotional_awareness(entry)
        ea_w = self.WEIGHTS["emotional_awareness"]
        components.append(ScoreComponent(
            dimension="emotional_awareness",
            raw_score=ea_score,
            weight=ea_w,
            weighted_score=ea_score * ea_w,
            rationale=ea_notes,
            evidence_items=ea_evidence,
        ))
        total += ea_score * ea_w

        # ---- Revision Quality (5) ----
        rv_score, rv_notes = self._score_revision_quality(entry)
        rv_w = self.WEIGHTS["revision_quality"]
        components.append(ScoreComponent(
            dimension="revision_quality",
            raw_score=rv_score,
            weight=rv_w,
            weighted_score=rv_score * rv_w,
            rationale=rv_notes,
        ))
        total += rv_score * rv_w

        # ---- Data Sufficiency (5) ----
        ds_score, ds_notes, ds_missing = self._score_data_sufficiency(entry, state)
        ds_w = self.WEIGHTS["data_sufficiency"]
        components.append(ScoreComponent(
            dimension="data_sufficiency",
            raw_score=ds_score,
            weight=ds_w,
            weighted_score=ds_score * ds_w,
            rationale=ds_notes,
            missing_items=ds_missing,
        ))
        total += ds_score * ds_w

        # ---- Scenario Objective (5) ----
        so_score, so_notes = self._score_scenario_objective(entry, config, decision_list)
        so_w = self.WEIGHTS["scenario_objective"]
        components.append(ScoreComponent(
            dimension="scenario_objective",
            raw_score=so_score,
            weight=so_w,
            weighted_score=so_score * so_w,
            rationale=so_notes,
        ))
        total += so_score * so_w

        # ---- Session Completion (5) ----
        sc_score, sc_notes = self._score_session_completion(state)
        sc_w = self.WEIGHTS["session_completion"]
        components.append(ScoreComponent(
            dimension="session_completion",
            raw_score=sc_score,
            weight=sc_w,
            weighted_score=sc_score * sc_w,
            rationale=sc_notes,
        ))
        total += sc_score * sc_w

        # Warn if entry has no data
        if not entry:
            warnings.append("No journal entry provided — scores are based on session state only.")
            status = ProcessScoreStatus.INSUFFICIENT_DATA.value
        else:
            status = ProcessScoreStatus.SCORED.value

        mode = config.get("mode", "real")
        if mode == "mock":
            from replay.scoring_schema import ScoreConfidenceLevel
            confidence = ScoreConfidenceLevel.DEMO_ONLY.value
            warnings.append("Mock mode: DEMO_ONLY confidence. Not a real research conclusion.")
        else:
            confidence = ScoreConfidenceLevel.OBSERVATIONAL.value

        return ReplayProcessScore(
            score_id=_new_score_id(),
            session_id=session_id,
            journal_entry_id=entry.get("journal_entry_id"),
            decision_id=entry.get("decision_id"),
            symbol=entry.get("symbol", config.get("symbol", "")),
            replay_date=entry.get("replay_date", state.get("current_date", "")),
            total_score=round(total, 2),
            max_score=100.0,
            components=components,
            status=status,
            confidence_level=confidence,
            scoring_notes=notes,
            flags=flags,
            warnings=warnings,
        )

    # ---- Dimension scorers ----

    def _score_thesis_quality(self, entry: Dict[str, Any]):
        thesis_id = entry.get("thesis_id")
        thesis_text = entry.get("thesis_text", entry.get("decision_reason", ""))
        summary = entry.get("summary", "")
        action = entry.get("action", "")
        evidence = []
        missing = []
        score = 0.0

        # WAIT/SKIP with documented reason: treat as good thesis quality
        if action in ("WAIT", "SKIP"):
            if thesis_text or summary or entry.get("decision_reason"):
                return 0.9, "Well-reasoned WAIT/SKIP decision with documented rationale.", evidence, missing
            else:
                return 0.6, "WAIT/SKIP decision — no documented rationale (partial credit).", evidence, ["decision_reason"]

        if thesis_id:
            evidence.append("thesis_id present")
            score += 0.4
        else:
            missing.append("thesis_id")

        if thesis_text and len(thesis_text) > 20:
            evidence.append("thesis_text documented")
            score += 0.3
        else:
            missing.append("thesis_text (>20 chars)")

        if summary and len(summary) > 10:
            evidence.append("summary documented")
            score += 0.3
        else:
            missing.append("summary")

        notes = f"Thesis quality: {len(evidence)} of 3 items present."
        return min(score, 1.0), notes, evidence, missing

    def _score_risk_planning(self, entry: Dict[str, Any]):
        risk_plan_id = entry.get("risk_plan_id")
        stop_price_note = entry.get("stop_price_note", "")
        target_price_note = entry.get("target_price_note", "")
        action = entry.get("action", "")
        evidence = []
        missing = []
        score = 0.0

        # WAIT/SKIP/WATCH: risk planning not required
        if action in ("WAIT", "SKIP", "WATCH"):
            return 0.85, f"Risk planning N/A for {action} decision — full credit.", evidence, missing

        if risk_plan_id:
            evidence.append("risk_plan_id present")
            score += 0.5
        else:
            missing.append("risk_plan_id")

        if stop_price_note and len(stop_price_note) > 3:
            evidence.append("stop_price_note documented")
            score += 0.3
        else:
            missing.append("stop_price_note")

        if target_price_note and len(target_price_note) > 3:
            evidence.append("target_price_note documented")
            score += 0.2
        else:
            missing.append("target_price_note")

        notes = f"Risk planning: {len(evidence)} of 3 items present."
        return min(score, 1.0), notes, evidence, missing

    def _score_discipline_checklist(self, entry: Dict[str, Any]):
        checklist_ids = entry.get("checklist_ids", [])
        action = entry.get("action", "")
        evidence = []
        missing = []

        # WAIT/SKIP: partial credit even without checklist
        if action in ("WAIT", "SKIP"):
            if checklist_ids:
                evidence.append(f"{len(checklist_ids)} checklist(s) completed")
                return 1.0, "WAIT/SKIP with checklist completed.", evidence, missing
            return 0.75, "WAIT/SKIP decision — checklist optional.", evidence, missing

        if not checklist_ids:
            missing.append("checklist_ids (no checklist completed)")
            return 0.0, "No checklist completed for this decision.", evidence, missing

        evidence.append(f"{len(checklist_ids)} checklist(s) completed")
        return 1.0, f"Discipline checklist completed ({len(checklist_ids)} items).", evidence, missing

    def _score_evidence_quality(self, entry: Dict[str, Any]):
        evidence_for = entry.get("evidence_for", [])
        evidence_against = entry.get("evidence_against", [])
        evidence = []
        missing = []
        score = 0.0

        if evidence_for:
            evidence.append(f"{len(evidence_for)} evidence_for items")
            score += 0.6
        else:
            missing.append("evidence_for")

        if evidence_against:
            evidence.append(f"{len(evidence_against)} evidence_against items")
            score += 0.4
        else:
            missing.append("evidence_against (balanced view)")

        notes = f"Evidence: {len(evidence_for)} for, {len(evidence_against)} against."
        return min(score, 1.0), notes, evidence, missing

    def _score_confirmation_invalidation(self, entry: Dict[str, Any]):
        confirmation_conditions = entry.get("confirmation_conditions", [])
        invalidation_conditions = entry.get("invalidation_conditions", [])
        evidence = []
        missing = []
        score = 0.0

        if confirmation_conditions:
            evidence.append(f"{len(confirmation_conditions)} confirmation conditions")
            score += 0.5
        else:
            missing.append("confirmation_conditions")

        if invalidation_conditions:
            evidence.append(f"{len(invalidation_conditions)} invalidation conditions")
            score += 0.5
        else:
            missing.append("invalidation_conditions")

        notes = f"Confirmation/Invalidation: {len(evidence)} of 2 documented."
        return min(score, 1.0), notes, evidence, missing

    def _score_point_in_time(self, entry: Dict[str, Any], state: Dict[str, Any]):
        pit_verified = entry.get("point_in_time_verified", False)
        state_pit = state.get("point_in_time_verified", False)
        flags = []

        if pit_verified or state_pit:
            return 1.0, "Point-in-time integrity verified.", flags
        else:
            flags.append("POINT_IN_TIME_NOT_VERIFIED")
            return 0.5, "point_in_time_verified=False — partial credit.", flags

    def _score_emotional_awareness(self, entry: Dict[str, Any]):
        emotional_state_id = entry.get("emotional_state_id")
        evidence = []

        if emotional_state_id:
            evidence.append("emotional_state_id present (self-reported)")
            return 1.0, "Emotional state documented (self-reported).", evidence
        else:
            return 0.5, "Emotional state not documented — partial credit.", evidence

    def _score_revision_quality(self, entry: Dict[str, Any]):
        revision_count = int(entry.get("revision_count", 0))
        latest_revision_id = entry.get("latest_revision_id")

        if revision_count == 0:
            return 0.8, "No revisions — original plan maintained.",
        if revision_count > 0 and latest_revision_id:
            return 1.0, f"Revision(s) documented ({revision_count}) with revision ID."
        return 0.6, f"{revision_count} revision(s) but no revision ID tracked."

    def _score_data_sufficiency(self, entry: Dict[str, Any], state: Dict[str, Any]):
        available_records = int(state.get("available_records", 0))
        missing = []

        if available_records >= 20:
            return 1.0, f"Sufficient data: {available_records} records available.", missing
        elif available_records >= 5:
            missing.append("More historical records recommended (< 20)")
            return 0.7, f"Partial data: {available_records} records available.", missing
        else:
            missing.append("Insufficient data records for reliable scoring")
            return 0.3, f"Limited data: {available_records} records available.", missing

    def _score_scenario_objective(
        self,
        entry: Dict[str, Any],
        config: Dict[str, Any],
        decisions: List[Dict[str, Any]],
    ):
        scenario_id = config.get("scenario_id") or entry.get("scenario_id")
        if scenario_id:
            return 1.0, f"Scenario objective linked: {scenario_id}."
        if decisions:
            return 0.8, "No scenario_id but decisions are present."
        return 0.5, "No scenario_id and no decisions recorded."

    def _score_session_completion(self, state: Dict[str, Any]):
        status = state.get("status", "")
        completed = bool(state.get("completed", False))

        if completed or status == "COMPLETED":
            return 1.0, "Session completed."
        elif status in ("PLAYING", "PAUSED"):
            return 0.7, f"Session in progress: {status}."
        else:
            return 0.4, f"Session status: {status}."

    def is_good_process(self, total_score: float) -> bool:
        return total_score >= self.GOOD_PROCESS_THRESHOLD
