"""
replay/review_notes.py — ReplayReviewNoteManager v1.2.6

Append-only revision notes for session/journal/mistake/strategy_review/
timeframe_review/final_review.

[!] Research Only. No Real Orders. Append-only. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from replay.review_dashboard_schema import _new_id, _now_utc

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

NOTE_TYPE_SESSION         = "session"
NOTE_TYPE_JOURNAL         = "journal"
NOTE_TYPE_MISTAKE         = "mistake"
NOTE_TYPE_STRATEGY_REVIEW = "strategy_review"
NOTE_TYPE_TIMEFRAME_REVIEW = "timeframe_review"
NOTE_TYPE_FINAL_REVIEW    = "final_review"

VALID_NOTE_TYPES = {
    NOTE_TYPE_SESSION, NOTE_TYPE_JOURNAL, NOTE_TYPE_MISTAKE,
    NOTE_TYPE_STRATEGY_REVIEW, NOTE_TYPE_TIMEFRAME_REVIEW, NOTE_TYPE_FINAL_REVIEW,
}


class ReplayReviewNoteManager:
    """
    Manages append-only review notes for all note types.

    [!] Append-only. Notes are never deleted or overwritten.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True
    APPEND_ONLY    = True

    def __init__(self) -> None:
        self._notes: List[Dict[str, Any]] = []

    def add_note(
        self,
        session_id: str,
        note_type: str,
        text: str,
        ref_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Append a note revision (append-only)."""
        if note_type not in VALID_NOTE_TYPES:
            return {"status": "INVALID_TYPE", "note_type": note_type, "valid": list(VALID_NOTE_TYPES)}
        if not text or not text.strip():
            return {"status": "EMPTY_TEXT", "session_id": session_id}
        note = {
            "note_id":    _new_id("NOTE-"),
            "session_id": session_id,
            "note_type":  note_type,
            "text":       text.strip(),
            "ref_id":     ref_id,
            "created_at": _now_utc(),
            "research_only": True,
            "append_only":   True,
        }
        self._notes.append(note)
        return {"status": "OK", "note_id": note["note_id"], "session_id": session_id}

    def get_notes(
        self,
        session_id: Optional[str] = None,
        note_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Return notes filtered by session_id and/or note_type."""
        result = self._notes
        if session_id:
            result = [n for n in result if n["session_id"] == session_id]
        if note_type:
            result = [n for n in result if n["note_type"] == note_type]
        return result

    def session_notes(self, session_id: str) -> List[Dict[str, Any]]:
        return self.get_notes(session_id=session_id, note_type=NOTE_TYPE_SESSION)

    def final_notes(self, session_id: str) -> List[Dict[str, Any]]:
        return self.get_notes(session_id=session_id, note_type=NOTE_TYPE_FINAL_REVIEW)

    def revisions(self, session_id: str) -> List[Dict[str, Any]]:
        """Return all note revisions for a session (append-only history)."""
        return self.get_notes(session_id=session_id)

    def summary(self) -> Dict[str, Any]:
        return {
            "total_notes": len(self._notes),
            "append_only": True,
            "research_only": True,
        }
