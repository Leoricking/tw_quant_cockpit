"""
replay/review_checklist.py — Replay Review Checklist v1.2.6

Checklist categories: SESSION/JOURNAL/PROCESS_SCORE/OUTCOME/MISTAKE/STRATEGY/
TIMEFRAME/DATA_INTEGRITY/REPORT/FINAL_NOTE.
Supports default checklist, scenario extension, user note, required/optional,
blocked reason, evidence link, completion history.

[!] NOT auto-complete Mistake Confirm / Outcome Reveal / Strategy Review Confirm /
    Timeframe Conflict Review.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from replay.review_dashboard_schema import (
    ReplayReviewChecklistItem,
    _new_id,
    _now_utc,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

CHECKLIST_CATEGORY_SESSION          = "SESSION"
CHECKLIST_CATEGORY_JOURNAL          = "JOURNAL"
CHECKLIST_CATEGORY_PROCESS_SCORE    = "PROCESS_SCORE"
CHECKLIST_CATEGORY_OUTCOME          = "OUTCOME"
CHECKLIST_CATEGORY_MISTAKE          = "MISTAKE"
CHECKLIST_CATEGORY_STRATEGY         = "STRATEGY"
CHECKLIST_CATEGORY_TIMEFRAME        = "TIMEFRAME"
CHECKLIST_CATEGORY_DATA_INTEGRITY   = "DATA_INTEGRITY"
CHECKLIST_CATEGORY_REPORT           = "REPORT"
CHECKLIST_CATEGORY_FINAL_NOTE       = "FINAL_NOTE"

_DEFAULT_ITEMS = [
    # SESSION
    (CHECKLIST_CATEGORY_SESSION,        "Session completed",                       True),
    # JOURNAL
    (CHECKLIST_CATEGORY_JOURNAL,        "Decision journal entry exists",           True),
    (CHECKLIST_CATEGORY_JOURNAL,        "Emotional state self-reported",           False),
    (CHECKLIST_CATEGORY_JOURNAL,        "Trade thesis captured",                   False),
    (CHECKLIST_CATEGORY_JOURNAL,        "Risk plan captured",                      False),
    # PROCESS_SCORE
    (CHECKLIST_CATEGORY_PROCESS_SCORE,  "Process score calculated",                True),
    (CHECKLIST_CATEGORY_PROCESS_SCORE,  "Process score reviewed",                  True),
    # OUTCOME
    (CHECKLIST_CATEGORY_OUTCOME,        "Outcome reveal (optional — user action)", False),
    # MISTAKE
    (CHECKLIST_CATEGORY_MISTAKE,        "Suggested mistakes reviewed",             True),
    (CHECKLIST_CATEGORY_MISTAKE,        "Mistake confirmation (manual)",           False),
    # STRATEGY
    (CHECKLIST_CATEGORY_STRATEGY,       "Strategy conflicts reviewed",             True),
    (CHECKLIST_CATEGORY_STRATEGY,       "Strategy rule review (manual)",           False),
    # TIMEFRAME
    (CHECKLIST_CATEGORY_TIMEFRAME,      "Timeframe conflicts reviewed",            True),
    (CHECKLIST_CATEGORY_TIMEFRAME,      "Timeframe conflict review (manual)",      False),
    # DATA_INTEGRITY
    (CHECKLIST_CATEGORY_DATA_INTEGRITY, "Point-in-time verified",                  True),
    (CHECKLIST_CATEGORY_DATA_INTEGRITY, "No future data detected",                 True),
    # REPORT
    (CHECKLIST_CATEGORY_REPORT,         "Session report generated",                False),
    # FINAL_NOTE
    (CHECKLIST_CATEGORY_FINAL_NOTE,     "Final review note added",                 True),
]

# Items that are NEVER auto-completed
_NO_AUTO_COMPLETE = {
    "Mistake confirmation (manual)",
    "Outcome reveal (optional — user action)",
    "Strategy rule review (manual)",
    "Timeframe conflict review (manual)",
}


class ReplayReviewChecklist:
    """
    Replay review checklist for a single session.

    [!] NOT auto-complete Mistake Confirm / Outcome Reveal / Strategy Review / TF Review.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True
    AUTO_COMPLETE  = False

    def __init__(self, session_id: str) -> None:
        self._session_id = session_id
        self._items: List[ReplayReviewChecklistItem] = []
        self._build_default()

    def _build_default(self) -> None:
        for category, label, required in _DEFAULT_ITEMS:
            item = ReplayReviewChecklistItem(
                item_id=_new_id("CL-"),
                session_id=self._session_id,
                category=category,
                label=label,
                required=required,
                auto_complete=False,
            )
            self._items.append(item)

    def items(self) -> List[ReplayReviewChecklistItem]:
        return list(self._items)

    def extend_for_scenario(self, scenario_items: List[Dict[str, Any]]) -> None:
        """Add scenario-specific checklist items."""
        for d in scenario_items:
            item = ReplayReviewChecklistItem(
                item_id=_new_id("CL-"),
                session_id=self._session_id,
                category=d.get("category", CHECKLIST_CATEGORY_FINAL_NOTE),
                label=d.get("label", ""),
                required=bool(d.get("required", False)),
                auto_complete=False,
            )
            self._items.append(item)

    def complete_item(self, item_id: str, evidence_link: str = "", user_note: str = "") -> Dict[str, Any]:
        """Mark an item as complete (manual only)."""
        for item in self._items:
            if item.item_id == item_id:
                if item.label in _NO_AUTO_COMPLETE:
                    return {
                        "status": "MANUAL_REQUIRED",
                        "item_id": item_id,
                        "note": f"'{item.label}' requires explicit manual action. Not auto-completed.",
                        "auto_complete": False,
                    }
                now = _now_utc()
                item.completed    = True
                item.completed_at = now
                item.evidence_link = evidence_link
                item.user_note     = user_note
                item.completion_history.append({
                    "completed_at": now,
                    "evidence_link": evidence_link,
                    "user_note": user_note,
                })
                return {"status": "OK", "item_id": item_id, "completed_at": now, "auto_complete": False}
        return {"status": "NOT_FOUND", "item_id": item_id}

    def block_item(self, item_id: str, reason: str = "") -> Dict[str, Any]:
        """Mark an item as blocked."""
        for item in self._items:
            if item.item_id == item_id:
                item.blocked        = True
                item.blocked_reason = reason
                return {"status": "OK", "item_id": item_id, "blocked_reason": reason}
        return {"status": "NOT_FOUND", "item_id": item_id}

    def progress(self) -> Dict[str, Any]:
        """Return checklist progress summary."""
        required = [i for i in self._items if i.required]
        optional = [i for i in self._items if not i.required]
        req_done = sum(1 for i in required if i.completed)
        opt_done = sum(1 for i in optional if i.completed)
        return {
            "session_id":           self._session_id,
            "required_total":       len(required),
            "required_complete":    req_done,
            "optional_total":       len(optional),
            "optional_complete":    opt_done,
            "all_required_done":    req_done == len(required),
            "progress_percent":     round(req_done / len(required) * 100, 1) if required else 0.0,
            "auto_complete":        False,
            "research_only":        True,
        }

    def to_list(self) -> List[Dict[str, Any]]:
        return [i.to_dict() for i in self._items]
