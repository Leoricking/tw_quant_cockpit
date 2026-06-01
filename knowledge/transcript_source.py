"""
knowledge/transcript_source.py — TranscriptSource model (v0.4.1.1).
[!] Knowledge Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No auto-trading. Not investment advice.
"""
from __future__ import annotations

import hashlib
import logging
import os
import random
import string
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SOURCE_TYPE_YOUTUBE = "youtube_transcript"
SOURCE_TYPE_WHISPER = "whisper_transcript"
SOURCE_TYPE_MANUAL = "manual_note"
SOURCE_TYPE_ARTICLE = "article"
SOURCE_TYPE_IMPORTED = "imported_text"

VALID_SOURCE_TYPES = [
    SOURCE_TYPE_YOUTUBE,
    SOURCE_TYPE_WHISPER,
    SOURCE_TYPE_MANUAL,
    SOURCE_TYPE_ARTICLE,
    SOURCE_TYPE_IMPORTED,
]


class TranscriptSource:
    """
    Metadata and content model for a single ingested transcript / knowledge document.

    Safety invariants:
      research_only = True
      no_real_orders = True
      knowledge_only = True
    """

    research_only: bool = True
    no_real_orders: bool = True
    knowledge_only: bool = True

    def __init__(
        self,
        source_id: str = "",
        title: str = "",
        author: str = "",
        source_type: str = SOURCE_TYPE_MANUAL,
        media_source: str = "",
        media_ref: str = "",
        video_id: str = "",
        transcript_path: str = "",
        transcript_hash: str = "",
        generated_at: str = "",
        saved_at: str = "",
        language: str = "zh-TW",
        tags: Optional[list] = None,
        source_confidence: str = "LOW",
        notes: str = "",
    ):
        self.source_id = source_id or self._generate_source_id()
        self.title = title
        self.author = author
        self.source_type = source_type if source_type in VALID_SOURCE_TYPES else SOURCE_TYPE_MANUAL
        self.media_source = media_source
        self.media_ref = media_ref
        self.video_id = video_id
        self.transcript_path = transcript_path
        self.transcript_hash = transcript_hash
        self.generated_at = generated_at or datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.saved_at = saved_at or datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.language = language
        self.tags = tags if tags is not None else []
        self.source_confidence = source_confidence
        self.notes = notes
        # safety re-enforcement
        self.research_only = True
        self.no_real_orders = True
        self.knowledge_only = True

    # ------------------------------------------------------------------
    # Classmethods
    # ------------------------------------------------------------------

    @classmethod
    def from_file(cls, path: str) -> "TranscriptSource":
        """
        Read a .txt or .md transcript file and parse structured sections.

        Supported blocks:
          [title]         → title field
          [video_id]      → video_id field
          [media_source]  → media_source field
          [media_ref]     → media_ref field
          [Transcript]    → transcript_text (up to [Summary] or EOF)
          [Summary]       → notes field
          Title: ...      → inline key-value title

        If no section markers found, treat entire file as transcript_text.
        """
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                raw = fh.read()
        except Exception as exc:
            logger.warning("TranscriptSource.from_file: cannot read %s — %s", path, exc)
            raw = ""

        title = ""
        video_id = ""
        media_source = ""
        media_ref = ""
        transcript_text = ""
        notes = ""

        lines = raw.splitlines()
        i = 0
        found_sections = False
        in_transcript = False
        in_summary = False
        transcript_lines: list[str] = []
        summary_lines: list[str] = []

        # Inline key-value scan (e.g. "Title: My Video")
        for line in lines:
            stripped = line.strip()
            if stripped.lower().startswith("title:"):
                title = stripped[6:].strip()

        i = 0
        while i < len(lines):
            stripped = lines[i].strip()

            if stripped.lower() == "[title]":
                found_sections = True
                in_transcript = False
                in_summary = False
                # next non-empty line is the title
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    title = lines[j].strip()
                    i = j + 1
                    continue

            elif stripped.lower() == "[video_id]":
                found_sections = True
                in_transcript = False
                in_summary = False
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    video_id = lines[j].strip()
                    i = j + 1
                    continue

            elif stripped.lower() == "[media_source]":
                found_sections = True
                in_transcript = False
                in_summary = False
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    media_source = lines[j].strip()
                    i = j + 1
                    continue

            elif stripped.lower() == "[media_ref]":
                found_sections = True
                in_transcript = False
                in_summary = False
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    media_ref = lines[j].strip()
                    i = j + 1
                    continue

            elif stripped.lower() == "[transcript]":
                found_sections = True
                in_transcript = True
                in_summary = False
                i += 1
                continue

            elif stripped.lower() == "[summary]":
                found_sections = True
                in_transcript = False
                in_summary = True
                i += 1
                continue

            else:
                if in_transcript:
                    transcript_lines.append(lines[i])
                elif in_summary:
                    summary_lines.append(lines[i])

            i += 1

        if found_sections:
            transcript_text = "\n".join(transcript_lines).strip()
            notes = "\n".join(summary_lines).strip()
        else:
            transcript_text = raw.strip()

        # Determine source_type
        fname_lower = os.path.basename(path).lower()
        if "youtube" in fname_lower or video_id:
            source_type = SOURCE_TYPE_YOUTUBE
        elif "whisper" in fname_lower:
            source_type = SOURCE_TYPE_WHISPER
        elif "article" in fname_lower:
            source_type = SOURCE_TYPE_ARTICLE
        else:
            source_type = SOURCE_TYPE_MANUAL

        # Fallback title from filename
        if not title:
            title = os.path.splitext(os.path.basename(path))[0]

        transcript_hash = cls.hash_text(transcript_text)

        obj = cls(
            title=title,
            source_type=source_type,
            media_source=media_source,
            media_ref=media_ref,
            video_id=video_id,
            transcript_path=str(path),
            transcript_hash=transcript_hash,
            notes=notes,
        )
        # Store transcript text as non-schema attribute for pipeline use
        obj._transcript_text = transcript_text
        return obj

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return all fields as a plain dictionary."""
        return {
            "source_id": self.source_id,
            "title": self.title,
            "author": self.author,
            "source_type": self.source_type,
            "media_source": self.media_source,
            "media_ref": self.media_ref,
            "video_id": self.video_id,
            "transcript_path": self.transcript_path,
            "transcript_hash": self.transcript_hash,
            "generated_at": self.generated_at,
            "saved_at": self.saved_at,
            "language": self.language,
            "tags": ",".join(self.tags) if isinstance(self.tags, list) else str(self.tags),
            "source_confidence": self.source_confidence,
            "notes": self.notes,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "knowledge_only": self.knowledge_only,
        }

    @staticmethod
    def hash_text(text: str) -> str:
        """Return first 12 characters of SHA-256 hex digest of text."""
        if not text:
            return ""
        digest = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
        return digest[:12]

    @staticmethod
    def _generate_source_id() -> str:
        """Return SRC-YYYYMMDD-HHMMSS-XXXXXX format unique ID."""
        now = datetime.now()
        date_part = now.strftime("%Y%m%d")
        time_part = now.strftime("%H%M%S")
        rand_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"SRC-{date_part}-{time_part}-{rand_part}"

    def __repr__(self) -> str:
        return (
            f"TranscriptSource(source_id={self.source_id!r}, title={self.title!r}, "
            f"source_type={self.source_type!r})"
        )
