"""
data/providers/forum/ptt/push_parser_v147.py — PTTPushParser v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] PUSH/BOO are engagement metrics ONLY. PUSH != bullish. BOO != bearish.
[!] No push=bullish shortcut. No boo=bearish shortcut.
"""
from __future__ import annotations

import html as html_module
import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_PUSH_ROW_PATTERN = re.compile(
    r'<div class="push">'
    r'<span[^>]*class="[^"]*push-tag[^"]*"[^>]*>([^<]*)</span>'
    r'<span[^>]*class="[^"]*push-userid[^"]*"[^>]*>([^<]*)</span>'
    r'<span[^>]*class="[^"]*push-content[^"]*"[^>]*>([^<]*)</span>'
    r'<span[^>]*class="[^"]*push-ipdatetime[^"]*"[^>]*>([^<]*)</span>',
    re.DOTALL
)

_TAG_MAP = {
    "推": "PUSH",
    "噓": "BOO",
    "→": "NEUTRAL",
}


class PTTPushParser:
    """
    Parses PTT push (comment) section.
    [!] PUSH/BOO are engagement only. NOT sentiment indicators.
    [!] No push=bullish shortcut. No boo=bearish shortcut.
    Handles empty, long, duplicate, unknown time comments.
    """

    # Safety: no sentiment inference from push/boo
    PUSH_EQUALS_BULLISH = False  # ALWAYS FALSE
    BOO_EQUALS_BEARISH = False   # ALWAYS FALSE

    def parse(self, html: str) -> List[Dict[str, Any]]:
        """
        Parse all push comments from PTT article HTML.
        Returns list of comment dicts.
        """
        comments = []
        seq = 0
        seen_hashes = set()

        for m in _PUSH_ROW_PATTERN.finditer(html):
            seq += 1
            try:
                comment = self._parse_push(m, seq, seen_hashes)
                if comment:
                    # Duplicate detection
                    key = f"{comment['author_display_id']}:{comment['text']}"
                    comment["is_duplicate"] = key in seen_hashes
                    seen_hashes.add(key)
                    comments.append(comment)
            except Exception as exc:
                logger.debug("PTTPushParser: push parse error at seq=%d: %s", seq, exc)

        return comments

    def _parse_push(self, m: re.Match, seq: int, seen: set) -> Optional[Dict[str, Any]]:
        tag_raw = html_module.unescape(m.group(1)).strip()
        author = html_module.unescape(m.group(2)).strip()
        text_raw = html_module.unescape(m.group(3)).strip()
        # Remove leading ": " from content
        if text_raw.startswith(":"):
            text_raw = text_raw[1:].strip()
        datetime_raw = html_module.unescape(m.group(4)).strip()

        tag = _TAG_MAP.get(tag_raw, "UNKNOWN")
        time_str, time_precision = self._parse_push_time(datetime_raw)

        # Truncate very long texts
        if len(text_raw) > 500:
            text_raw = text_raw[:497] + "..."

        return {
            "sequence": seq,
            "author_display_id": author if author else None,
            "tag": tag,
            "tag_raw": tag_raw,
            "text": text_raw,
            "comment_time": time_str,
            "time_precision": time_precision,
            # Safety: no sentiment shortcut
            "push_is_bullish": False,   # ALWAYS FALSE
            "boo_is_bearish": False,    # ALWAYS FALSE
        }

    def _parse_push_time(self, datetime_raw: str) -> tuple:
        """
        Parse push datetime. Returns (iso_str_or_raw, precision).
        PTT push times are typically MM/DD HH:MM (no year).
        Mark partial times accordingly.
        """
        datetime_raw = datetime_raw.strip()
        # Pattern: MM/DD HH:MM (no year = partial)
        m = re.match(r'^(\d{1,2}/\d{1,2}\s+\d{2}:\d{2})', datetime_raw)
        if m:
            return m.group(1), "PARTIAL_NO_YEAR"
        # Pattern: IP + datetime
        m2 = re.match(r'[\d.]+\s+(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})', datetime_raw)
        if m2:
            return m2.group(1), "SECOND"
        if datetime_raw:
            return datetime_raw, "UNKNOWN"
        return None, "UNKNOWN"
