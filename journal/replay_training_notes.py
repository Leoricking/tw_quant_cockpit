"""
journal/replay_training_notes.py — ReplayTrainingNotes (v0.4.6).

Creates journal entries from Intraday Replay training sessions.
Read-only integration — does NOT modify replay sessions or strategies.

[!] Journal Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

from journal.journal_schema import (
    JournalEntry,
    ENTRY_REPLAY_NOTE,
    STATUS_REVIEWED,
    OUTCOME_UNKNOWN,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_REPLAY_ROOT = os.path.join(BASE_DIR, "data", "backtest_results")

# Replay note fields that can be recorded
REPLAY_NOTE_FIELDS = [
    "opening_range",         # Opening range assessment (broke up / down / ranging)
    "vwap_reclaim",          # VWAP reclaim or lost
    "fake_breakout",         # Fake breakout observed
    "volume_profile_poc",    # Volume profile POC level
    "strategy_overlay",      # Strategy overlay notes
    "replay_mistake_tags",   # Mistakes observed during replay
    "training_score",        # Self-assessed training score (1–10)
    "next_practice_focus",   # Next session practice focus
]


class ReplayTrainingNotes:
    """
    Creates research journal entries from Intraday Replay training sessions.

    [!] Journal Only. Research Only. No Real Orders.
    """

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(
        self,
        journal_store=None,
        replay_root: str = _DEFAULT_REPLAY_ROOT,
    ):
        self._store = journal_store
        self._replay_root = (
            replay_root if os.path.isabs(replay_root)
            else os.path.join(BASE_DIR, replay_root)
        )

    def _get_store(self):
        if self._store is not None:
            return self._store
        from journal.journal_store import PortfolioJournalStore
        self._store = PortfolioJournalStore()
        return self._store

    # ------------------------------------------------------------------
    # Create note from replay session
    # ------------------------------------------------------------------

    def create_note_from_replay(
        self,
        replay_session_id: str,
        notes: Optional[dict] = None,
    ) -> JournalEntry:
        """
        Create a journal entry (ENTRY_REPLAY_NOTE) from a replay session ID.
        notes dict may include any REPLAY_NOTE_FIELDS keys.
        Returns the created JournalEntry.
        """
        try:
            store = self._get_store()
            n = notes or {}

            # Build thesis from replay observations
            thesis_parts = []
            if n.get("opening_range"):
                thesis_parts.append(f"Opening range: {n['opening_range']}")
            if n.get("vwap_reclaim"):
                thesis_parts.append(f"VWAP: {n['vwap_reclaim']}")
            if n.get("fake_breakout"):
                thesis_parts.append(f"Fake breakout: {n['fake_breakout']}")
            if n.get("volume_profile_poc"):
                thesis_parts.append(f"POC: {n['volume_profile_poc']}")

            review_parts = []
            if n.get("strategy_overlay"):
                review_parts.append(f"Strategy: {n['strategy_overlay']}")
            if n.get("next_practice_focus"):
                review_parts.append(f"Next focus: {n['next_practice_focus']}")
            if n.get("training_score") is not None:
                review_parts.append(f"Score: {n['training_score']}/10")

            # Validate mistake tags
            from journal.journal_schema import ALL_MISTAKE_TAGS
            raw_tags = n.get("replay_mistake_tags", [])
            if isinstance(raw_tags, str):
                raw_tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
            mistake_tags = [t for t in raw_tags if t in ALL_MISTAKE_TAGS]

            entry = JournalEntry(
                entry_type=ENTRY_REPLAY_NOTE,
                mode="replay",
                status=STATUS_REVIEWED,
                replay_session_id=replay_session_id,
                thesis="; ".join(thesis_parts) if thesis_parts else "Intraday replay training note",
                reason=f"Replay session: {replay_session_id}",
                review_notes="; ".join(review_parts),
                mistake_tags=mistake_tags,
                confidence_after=n.get("training_score"),
            )
            store.add_entry(entry)
            logger.info(
                "ReplayTrainingNotes: created note %s for session %s",
                entry.journal_id, replay_session_id,
            )
            return entry
        except Exception as exc:
            logger.warning("ReplayTrainingNotes.create_note_from_replay: %s", exc)
            # Return a minimal safe entry
            return JournalEntry(
                entry_type=ENTRY_REPLAY_NOTE,
                replay_session_id=replay_session_id,
                reason=f"[Error creating note: {exc}]",
            )

    # ------------------------------------------------------------------
    # Summarize replay notes
    # ------------------------------------------------------------------

    def summarize_replay_notes(self) -> dict:
        """Summarize all replay training notes from the journal store."""
        try:
            store = self._get_store()
            notes = store.list_entries(limit=500, entry_type=ENTRY_REPLAY_NOTE)

            if not notes:
                return {
                    "total_notes": 0,
                    "sessions_covered": [],
                    "avg_training_score": None,
                    "most_common_mistakes": [],
                    "journal_only": True,
                    "no_real_orders": True,
                }

            sessions = list({n.replay_session_id for n in notes if n.replay_session_id})
            scores = [n.confidence_after for n in notes if n.confidence_after is not None]
            all_mistakes: Dict[str, int] = {}
            for n in notes:
                for mt in n.mistake_tags:
                    all_mistakes[mt] = all_mistakes.get(mt, 0) + 1

            sorted_mistakes = sorted(all_mistakes.items(), key=lambda x: -x[1])

            return {
                "total_notes":         len(notes),
                "sessions_covered":    sessions[:20],
                "avg_training_score":  sum(scores) / len(scores) if scores else None,
                "most_common_mistakes": [m[0] for m in sorted_mistakes[:5]],
                "mistake_counts":       dict(sorted_mistakes[:10]),
                "latest_note_at":       notes[0].created_at[:19] if notes else "",
                "journal_only":         True,
                "no_real_orders":       True,
            }
        except Exception as exc:
            logger.warning("ReplayTrainingNotes.summarize_replay_notes: %s", exc)
            return {"error": str(exc), "total_notes": 0, "no_real_orders": True}

    # ------------------------------------------------------------------
    # Load replay session list (read-only)
    # ------------------------------------------------------------------

    def list_replay_sessions(self) -> List[str]:
        """Return known replay session IDs from the journal store."""
        try:
            store = self._get_store()
            notes = store.list_entries(limit=500, entry_type=ENTRY_REPLAY_NOTE)
            return list({n.replay_session_id for n in notes if n.replay_session_id})
        except Exception as exc:
            logger.warning("ReplayTrainingNotes.list_replay_sessions: %s", exc)
            return []
