"""
replay/replay_annotations.py — ReplayAnnotationManager v1.2.0

Manages replay annotations.
remove_from_view: marks hidden=True, does NOT delete from audit history.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

VALID_ANNOTATION_TYPES = [
    "NOTE", "SUPPORT", "RESISTANCE", "TREND", "VOLUME",
    "KD", "MACD", "CHIP", "FUNDAMENTAL", "RISK", "MISTAKE", "OTHER",
]


class ReplayAnnotationManager:
    """
    Manages replay annotations.
    remove_from_view: marks hidden=True, does NOT delete from audit history.
    """

    def __init__(self, store=None):
        self._store = store

    def add(
        self,
        session_id: str,
        replay_date: str,
        annotation_type: str,
        title: str,
        content: str,
        **kwargs,
    ):
        """Add a new annotation. Returns ReplayAnnotation."""
        from replay.replay_schema import ReplayAnnotation

        if annotation_type not in VALID_ANNOTATION_TYPES:
            logger.warning("[AnnotationManager] Unknown annotation_type=%s, using OTHER", annotation_type)
            annotation_type = "OTHER"

        annotation = ReplayAnnotation(
            annotation_id=f"ANN-{uuid.uuid4().hex[:12].upper()}",
            session_id=session_id,
            replay_date=replay_date,
            annotation_type=annotation_type,
            title=title,
            content=content,
            tags=kwargs.get("tags", []),
            price_level=kwargs.get("price_level"),
            start_date=kwargs.get("start_date"),
            end_date=kwargs.get("end_date"),
            style_metadata=kwargs.get("style_metadata", {}),
            hidden=False,
        )

        if self._store:
            self._store.append_annotation(annotation)

        return annotation

    def update(self, annotation_id: str, **kwargs):
        """Update an annotation (creates updated record, preserves original)."""
        from replay.replay_schema import ReplayAnnotation

        # Load existing
        existing = None
        if self._store and "session_id" in kwargs:
            annotations = self._store.load_annotations(kwargs["session_id"])
            for a in annotations:
                if a.get("annotation_id") == annotation_id:
                    existing = a
                    break

        now = datetime.now(timezone.utc).isoformat()
        base = existing or {}

        updated = ReplayAnnotation(
            annotation_id=annotation_id,  # keep same ID for updates
            session_id=kwargs.get("session_id", base.get("session_id", "")),
            replay_date=base.get("replay_date", ""),
            annotation_type=kwargs.get("annotation_type", base.get("annotation_type", "NOTE")),
            title=kwargs.get("title", base.get("title", "")),
            content=kwargs.get("content", base.get("content", "")),
            tags=kwargs.get("tags", base.get("tags", [])),
            price_level=kwargs.get("price_level", base.get("price_level")),
            start_date=kwargs.get("start_date", base.get("start_date")),
            end_date=kwargs.get("end_date", base.get("end_date")),
            style_metadata=kwargs.get("style_metadata", base.get("style_metadata", {})),
            hidden=kwargs.get("hidden", base.get("hidden", False)),
            created_at=base.get("created_at", now),
            updated_at=now,
        )

        if self._store:
            self._store.append_annotation(updated)

        return updated

    def remove_from_view(self, annotation_id: str, session_id: str = "") -> None:
        """
        Sets hidden=True on annotation. Does NOT delete from audit history.
        Appends a hidden=True version to the store.
        """
        self.update(annotation_id, session_id=session_id, hidden=True)

    def list_by_date(self, session_id: str, replay_date: str) -> List[Dict[str, Any]]:
        """List annotations for a specific replay_date (excluding hidden)."""
        if not self._store:
            return []
        all_ann = self._store.load_annotations(session_id)
        # Deduplicate by annotation_id, keep last version
        seen: Dict[str, Dict[str, Any]] = {}
        for a in all_ann:
            aid = a.get("annotation_id", "")
            if aid:
                seen[aid] = a
        return [a for a in seen.values()
                if a.get("replay_date") == replay_date and not a.get("hidden", False)]

    def list_by_type(self, session_id: str, annotation_type: str) -> List[Dict[str, Any]]:
        """List annotations of a specific type (excluding hidden)."""
        if not self._store:
            return []
        all_ann = self._store.load_annotations(session_id)
        seen: Dict[str, Dict[str, Any]] = {}
        for a in all_ann:
            aid = a.get("annotation_id", "")
            if aid:
                seen[aid] = a
        return [a for a in seen.values()
                if a.get("annotation_type") == annotation_type and not a.get("hidden", False)]

    def export_session_notes(self, session_id: str) -> str:
        """Export all visible annotations as markdown text."""
        if not self._store:
            return "No annotations."
        all_ann = self._store.load_annotations(session_id)
        seen: Dict[str, Dict[str, Any]] = {}
        for a in all_ann:
            aid = a.get("annotation_id", "")
            if aid:
                seen[aid] = a
        visible = [a for a in seen.values() if not a.get("hidden", False)]
        if not visible:
            return "No annotations."
        lines = [f"# Session Annotations — {session_id}\n"]
        for a in sorted(visible, key=lambda x: x.get("replay_date", "")):
            lines.append(f"## [{a.get('replay_date','')}] {a.get('annotation_type','')} — {a.get('title','')}")
            lines.append(a.get("content", ""))
            if a.get("tags"):
                lines.append(f"Tags: {', '.join(a['tags'])}")
            lines.append("")
        return "\n".join(lines)
