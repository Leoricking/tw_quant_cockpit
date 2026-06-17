"""
replay/plan_adherence.py — ReplayPlanAdherenceEvaluator for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Plan adherence evaluates decision vs. original plan — no future data.
[!] WAIT/SKIP decisions that are well-reasoned are NOT failures.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_adherence_id() -> str:
    return f"PAD-{uuid.uuid4().hex[:12].upper()}"


class ReplayPlanAdherenceEvaluator:
    """
    Evaluates how well a decision adhered to the original plan.
    [!] Research Only. No Real Orders.
    [!] WAIT/SKIP with good reason is full adherence.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def evaluate(
        self,
        session_id: str,
        journal_entry: Optional[Dict[str, Any]] = None,
        decisions: Optional[List[Dict[str, Any]]] = None,
        notes: str = "",
    ) -> Dict[str, Any]:
        """
        Evaluate plan adherence.
        Returns a dict with adherence_score, status, and details.
        """
        entry = journal_entry or {}
        decision_list = decisions or []

        action = entry.get("action", "")
        planned_action = entry.get("planned_action", "")
        fallback_action = entry.get("fallback_action", "")
        confirmation_conditions = entry.get("confirmation_conditions", [])
        invalidation_conditions = entry.get("invalidation_conditions", [])
        no_trade_conditions = entry.get("no_trade_conditions", [])

        score_items: List[Tuple[str, float, str]] = []  # (item, score, note)

        # WAIT/SKIP with documented reason: full adherence
        if action in ("WAIT", "SKIP"):
            reason = entry.get("decision_reason", "")
            if reason or no_trade_conditions:
                return self._build_result(
                    session_id=session_id,
                    entry=entry,
                    adherence_score=100.0,
                    status="FULL_ADHERENCE",
                    details=f"Well-reasoned WAIT/SKIP: {reason or str(no_trade_conditions)[:80]}",
                    items=[("wait_skip_reasoned", 1.0, "WAIT/SKIP with documented rationale — full adherence.")],
                    notes=notes,
                )
            else:
                return self._build_result(
                    session_id=session_id,
                    entry=entry,
                    adherence_score=75.0,
                    status="PARTIAL_ADHERENCE",
                    details="WAIT/SKIP without documented rationale — partial credit.",
                    items=[("wait_skip_undocumented", 0.75, "WAIT/SKIP but no decision_reason or no_trade_conditions.")],
                    notes=notes,
                )

        # Check planned action match
        if planned_action and action:
            if action == planned_action:
                score_items.append(("action_matches_plan", 1.0, f"Action {action!r} matches planned_action."))
            elif action == fallback_action:
                score_items.append(("action_matches_fallback", 0.8, f"Action {action!r} matches fallback_action."))
            else:
                score_items.append(("action_deviation", 0.3, f"Action {action!r} differs from planned {planned_action!r}."))
        else:
            score_items.append(("no_planned_action", 0.6, "No planned_action documented — partial credit."))

        # Check confirmation conditions documented
        if confirmation_conditions:
            score_items.append(("confirmation_conditions_documented", 1.0, f"{len(confirmation_conditions)} confirmation conditions."))
        else:
            score_items.append(("no_confirmation_conditions", 0.5, "No confirmation conditions documented."))

        # Check invalidation conditions documented
        if invalidation_conditions:
            score_items.append(("invalidation_conditions_documented", 1.0, f"{len(invalidation_conditions)} invalidation conditions."))
        else:
            score_items.append(("no_invalidation_conditions", 0.5, "No invalidation conditions documented."))

        # Check revision quality
        revision_count = int(entry.get("revision_count", 0))
        if revision_count > 0:
            # Revisions are OK if documented
            latest_rev = entry.get("latest_revision_id")
            if latest_rev:
                score_items.append(("revisions_documented", 0.9, f"{revision_count} revision(s) with revision ID."))
            else:
                score_items.append(("revisions_not_tracked", 0.6, f"{revision_count} revision(s) but no revision ID."))

        # Aggregate
        if score_items:
            avg_score = sum(s for _, s, _ in score_items) / len(score_items) * 100
        else:
            avg_score = 50.0

        if avg_score >= 90:
            status = "FULL_ADHERENCE"
        elif avg_score >= 65:
            status = "PARTIAL_ADHERENCE"
        elif avg_score >= 40:
            status = "PLAN_DEVIATION"
        else:
            status = "PLAN_MISSING"

        details = "; ".join(f"{name}: {note}" for name, _, note in score_items)

        return self._build_result(
            session_id=session_id,
            entry=entry,
            adherence_score=round(avg_score, 2),
            status=status,
            details=details,
            items=score_items,
            notes=notes,
        )

    def _build_result(
        self,
        session_id: str,
        entry: Dict[str, Any],
        adherence_score: float,
        status: str,
        details: str,
        items: List[Tuple[str, float, str]],
        notes: str,
    ) -> Dict[str, Any]:
        return {
            "adherence_id": _new_adherence_id(),
            "session_id": session_id,
            "journal_entry_id": entry.get("journal_entry_id"),
            "decision_id": entry.get("decision_id"),
            "symbol": entry.get("symbol", ""),
            "replay_date": entry.get("replay_date", ""),
            "action": entry.get("action", ""),
            "adherence_score": adherence_score,
            "status": status,
            "details": details,
            "items": [{"name": n, "score": s, "note": nt} for n, s, nt in items],
            "notes": notes,
            "evaluated_at": _now_utc(),
            "simulation_only": True,
            "research_only": True,
            "no_real_orders": True,
        }
