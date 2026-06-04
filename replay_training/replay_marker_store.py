"""replay_training/replay_marker_store.py — ReplayMarkerStore for TW Replay Training Cockpit v0.5.6.

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import logging
import os
import uuid
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_MARKERS_FILENAME = "replay_markers.csv"
_NOTES_FILENAME   = "replay_notes.csv"

_MARKER_FIELDS = [
    "marker_id", "session_id", "symbol", "trade_date", "bar_time",
    "bar_index", "marker_type", "price", "reason", "confidence",
    "note", "tags", "created_at", "no_real_orders",
]

_NOTE_FIELDS = [
    "note_id", "session_id", "bar_time", "note", "tags", "created_at",
]


class ReplayMarkerStore:
    """Persists replay markers and notes to CSV files.

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, output_dir: str = "data/backtest_results/replay_training") -> None:
        self._output_dir   = os.path.join(BASE_DIR, output_dir)
        os.makedirs(self._output_dir, exist_ok=True)
        self._markers_path = os.path.join(self._output_dir, _MARKERS_FILENAME)
        self._notes_path   = os.path.join(self._output_dir, _NOTES_FILENAME)
        self._markers: List = []
        self._notes: List[dict] = []
        self._load()

    # ------------------------------------------------------------------
    # Internal load
    # ------------------------------------------------------------------

    def _load(self) -> None:
        """Load existing markers and notes from CSV (graceful if missing)."""
        try:
            from replay_training.replay_training_schema import ReplayMarker
            if os.path.isfile(self._markers_path):
                with open(self._markers_path, newline="", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        try:
                            m = ReplayMarker(
                                marker_id=row.get("marker_id", ""),
                                session_id=row.get("session_id", ""),
                                symbol=row.get("symbol", ""),
                                trade_date=row.get("trade_date", ""),
                                bar_time=row.get("bar_time", ""),
                                bar_index=int(row.get("bar_index", 0)),
                                marker_type=row.get("marker_type", "NOTE"),
                                price=float(row.get("price", 0.0)),
                                reason=row.get("reason", ""),
                                confidence=int(row.get("confidence", 0)),
                                note=row.get("note", ""),
                                tags=row.get("tags", ""),
                                created_at=row.get("created_at", ""),
                                no_real_orders=True,
                            )
                            self._markers.append(m)
                        except Exception as exc:
                            logger.warning("[ReplayMarkerStore] skip malformed row: %s", exc)
        except Exception as exc:
            logger.warning("[ReplayMarkerStore] load markers error: %s", exc)

        try:
            if os.path.isfile(self._notes_path):
                with open(self._notes_path, newline="", encoding="utf-8") as f:
                    self._notes = [dict(row) for row in csv.DictReader(f)]
        except Exception as exc:
            logger.warning("[ReplayMarkerStore] load notes error: %s", exc)

    # ------------------------------------------------------------------
    # Markers
    # ------------------------------------------------------------------

    def add_marker(self, marker) -> None:
        """Add a ReplayMarker and persist to CSV."""
        try:
            self._markers.append(marker)
            self._save_markers()
        except Exception as exc:
            logger.error("[ReplayMarkerStore] add_marker error: %s", exc)

    def list_markers(self, session_id: Optional[str] = None) -> list:
        """Return markers, optionally filtered by session_id."""
        if session_id:
            return [m for m in self._markers if m.session_id == session_id]
        return list(self._markers)

    def _save_markers(self) -> None:
        try:
            with open(self._markers_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=_MARKER_FIELDS)
                writer.writeheader()
                for m in self._markers:
                    writer.writerow(m.to_dict())
        except Exception as exc:
            logger.error("[ReplayMarkerStore] save markers error: %s", exc)

    # ------------------------------------------------------------------
    # Notes
    # ------------------------------------------------------------------

    def add_note(
        self, session_id: str, bar_time: str, note: str, tags: Optional[str] = None
    ) -> None:
        """Add a text note for a bar and persist to CSV."""
        try:
            record = {
                "note_id":    f"NOTE-{uuid.uuid4().hex[:8].upper()}",
                "session_id": session_id,
                "bar_time":   bar_time,
                "note":       note,
                "tags":       tags or "",
                "created_at": datetime.now().isoformat(),
            }
            self._notes.append(record)
            self._save_notes()
        except Exception as exc:
            logger.error("[ReplayMarkerStore] add_note error: %s", exc)

    def _save_notes(self) -> None:
        try:
            with open(self._notes_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=_NOTE_FIELDS)
                writer.writeheader()
                for n in self._notes:
                    writer.writerow({k: n.get(k, "") for k in _NOTE_FIELDS})
        except Exception as exc:
            logger.error("[ReplayMarkerStore] save notes error: %s", exc)

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_markers(self) -> dict:
        """Return paths to saved markers and notes files."""
        return {
            "markers_path": self._markers_path if os.path.isfile(self._markers_path) else None,
            "notes_path":   self._notes_path   if os.path.isfile(self._notes_path)   else None,
            "markers_count": len(self._markers),
            "notes_count":   len(self._notes),
            "no_real_orders": True,
        }
