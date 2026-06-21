"""
data/providers/forum/ptt/edit_history_v147.py — PTTEditHistoryParser v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

_EDIT_PATTERN = re.compile(
    r'※ 編輯.*?(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})',
    re.DOTALL
)
_EDIT_PATTERN_SHORT = re.compile(
    r'※ 編輯.*?(\d{4}/\d{2}/\d{2})',
    re.DOTALL
)


class PTTEditHistoryParser:
    """
    Parses edit history from PTT article footer.
    Handles multiple edit events. Timestamps marked with precision.
    """

    def parse(self, html: str) -> List[Dict[str, Any]]:
        """
        Extract all edit events from article HTML.
        Returns list of edit dicts with edited_at and time_precision.
        """
        edits = []
        # Full timestamp (YYYY/MM/DD HH:MM:SS)
        found_full = set()
        for m in _EDIT_PATTERN.finditer(html):
            ts = m.group(1).strip()
            if ts not in found_full:
                found_full.add(ts)
                edits.append({
                    "edited_at": ts,
                    "time_precision": "SECOND",
                    "raw": m.group(0)[:80],
                })
        # Date-only timestamps (fallback, YYYY/MM/DD)
        found_date = set()
        for m in _EDIT_PATTERN_SHORT.finditer(html):
            ts = m.group(1).strip()
            if ts not in found_full and ts not in found_date:
                found_date.add(ts)
                edits.append({
                    "edited_at": ts,
                    "time_precision": "DAY",
                    "raw": m.group(0)[:80],
                })
        # Sort by edit_at
        edits.sort(key=lambda x: x.get("edited_at", ""))
        # Assign sequence
        for i, e in enumerate(edits, 1):
            e["edit_seq"] = i
        return edits
