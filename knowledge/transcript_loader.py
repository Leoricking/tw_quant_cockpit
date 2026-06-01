"""
knowledge/transcript_loader.py — TranscriptLoader: discovers and loads transcript files (v0.4.1.1).
[!] Knowledge Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Never reads .env. Never makes network requests.
"""
from __future__ import annotations

import logging
import os
import re
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_INPUT_DIRS = [
    "knowledge/transcripts",
    "data/import/transcripts",
    "data/import/knowledge",
    "data/strategy_knowledge/transcripts",
]

_DEFAULT_ALLOWED_EXTS = {".txt", ".md"}


class TranscriptLoader:
    """
    Discovers and loads transcript / knowledge files from configured directories.

    Safety:
      - Never reads .env files.
      - Never makes network requests.
      - Missing directories are silently skipped.
      - Empty transcript list returns gracefully (no crash).
    """

    read_only: bool = True
    no_real_orders: bool = True

    def __init__(
        self,
        input_dirs: Optional[list] = None,
        allowed_exts: Optional[set] = None,
    ):
        raw_dirs = input_dirs if input_dirs is not None else _DEFAULT_INPUT_DIRS
        self._input_dirs = [
            os.path.join(BASE_DIR, d) if not os.path.isabs(d) else d
            for d in raw_dirs
        ]
        self._allowed_exts = allowed_exts if allowed_exts is not None else _DEFAULT_ALLOWED_EXTS

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover_files(self) -> list:
        """
        Return sorted list of absolute paths for .txt/.md files found in
        any existing input directory. Missing directories are silently skipped.
        """
        found: list[str] = []
        for dir_path in self._input_dirs:
            if not os.path.isdir(dir_path):
                continue
            for fname in os.listdir(dir_path):
                ext = os.path.splitext(fname)[1].lower()
                if ext in self._allowed_exts:
                    full_path = os.path.join(dir_path, fname)
                    if os.path.isfile(full_path):
                        found.append(full_path)
        return sorted(set(found))

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load_file(self, path: str) -> tuple:
        """
        Load a single file into (TranscriptSource, text_str).
        Returns (None, "") on any error.
        """
        try:
            from knowledge.transcript_source import TranscriptSource
            source = TranscriptSource.from_file(path)
            text = getattr(source, "_transcript_text", "")
            if not text:
                # Fall back to reading raw file
                try:
                    with open(path, "r", encoding="utf-8", errors="replace") as fh:
                        text = fh.read()
                except Exception:
                    text = ""
            return source, text
        except Exception as exc:
            logger.warning("TranscriptLoader.load_file: failed to load %s — %s", path, exc)
            return None, ""

    def load_all(self) -> list:
        """
        Discover all files and load each into (TranscriptSource, text) tuples.
        Returns empty list if no files found — no crash.
        """
        paths = self.discover_files()
        results: list[tuple] = []
        for path in paths:
            source, text = self.load_file(path)
            if source is not None:
                results.append((source, text))
        if not results:
            logger.info("TranscriptLoader.load_all: no transcripts found — returning empty list.")
        return results

    # ------------------------------------------------------------------
    # Parsing helpers
    # ------------------------------------------------------------------

    def parse_sections(self, text: str) -> dict:
        """
        Parse a text string for structured section markers.

        Returns dict with keys:
          title, video_id, media_source, media_ref, transcript, summary
        """
        result = {
            "title": "",
            "video_id": "",
            "media_source": "",
            "media_ref": "",
            "transcript": "",
            "summary": "",
        }
        if not text:
            return result

        lines = text.splitlines()
        i = 0
        in_transcript = False
        in_summary = False
        transcript_lines: list[str] = []
        summary_lines: list[str] = []
        found_any = False

        while i < len(lines):
            stripped = lines[i].strip()
            lower = stripped.lower()

            if lower == "[title]":
                found_any = True
                in_transcript = False
                in_summary = False
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    result["title"] = lines[j].strip()
                    i = j + 1
                    continue

            elif lower == "[video_id]":
                found_any = True
                in_transcript = False
                in_summary = False
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    result["video_id"] = lines[j].strip()
                    i = j + 1
                    continue

            elif lower == "[media_source]":
                found_any = True
                in_transcript = False
                in_summary = False
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    result["media_source"] = lines[j].strip()
                    i = j + 1
                    continue

            elif lower == "[media_ref]":
                found_any = True
                in_transcript = False
                in_summary = False
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    result["media_ref"] = lines[j].strip()
                    i = j + 1
                    continue

            elif lower == "[transcript]":
                found_any = True
                in_transcript = True
                in_summary = False
                i += 1
                continue

            elif lower == "[summary]":
                found_any = True
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

        if found_any:
            result["transcript"] = "\n".join(transcript_lines).strip()
            result["summary"] = "\n".join(summary_lines).strip()
        else:
            result["transcript"] = text.strip()

        # Inline key-value fallback
        for line in lines:
            s = line.strip()
            if s.lower().startswith("title:") and not result["title"]:
                result["title"] = s[6:].strip()

        return result

    def extract_metadata(self, text: str, path: str) -> dict:
        """
        Extract metadata from text and path.

        Returns dict with keys:
          title, author, tags, language, video_id, media_source
        """
        meta = {
            "title": "",
            "author": "",
            "tags": [],
            "language": "zh-TW",
            "video_id": "",
            "media_source": "",
        }
        if not text:
            return meta

        sections = self.parse_sections(text)
        meta["title"] = sections.get("title", "")
        meta["video_id"] = sections.get("video_id", "")
        meta["media_source"] = sections.get("media_source", "")

        if not meta["title"] and path:
            meta["title"] = os.path.splitext(os.path.basename(path))[0]

        # Detect language heuristic: if mostly ASCII, assume English
        non_ascii = sum(1 for c in text if ord(c) > 127)
        if non_ascii < len(text) * 0.05:
            meta["language"] = "en"

        # Extract tags from filename
        fname = os.path.splitext(os.path.basename(path))[0] if path else ""
        if fname:
            meta["tags"] = [t.strip() for t in re.split(r"[_\-\s]+", fname) if t.strip()]

        return meta

    def normalize_text(self, text: str) -> str:
        """
        Normalize text: lowercase, collapse extra whitespace, strip.
        """
        if not text:
            return ""
        text = text.lower()
        # Collapse multiple whitespace/newlines into single space
        text = re.sub(r"\s+", " ", text)
        return text.strip()
