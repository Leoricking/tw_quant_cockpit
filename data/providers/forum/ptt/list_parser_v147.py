"""
data/providers/forum/ptt/list_parser_v147.py — PTTListParser v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Parses PTT board index HTML. Malformed rows isolated (don't fail whole page).
[!] No credentials. No private boards.
"""
from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Known PTT article categories
KNOWN_CATEGORIES = frozenset([
    "新聞", "標的", "請益", "情報", "心得", "公告", "閒聊",
    "討論", "問題", "轉錄",
])

# Push count pattern: 爆, X1-X9, numeric, empty
_PUSH_爆 = "爆"
_PUSH_X_PATTERN = re.compile(r"^X(\d)$")
_PUSH_NUMERIC = re.compile(r"^\d+$")


class PTTListParser:
    """
    Parses PTT board index HTML.
    [!] Malformed rows isolated — single malformed row does not fail whole page.
    [!] Handles 爆/X1-X9/numeric/empty push counts.
    [!] Handles deleted articles, pinned, announcements.
    """

    def parse(self, html: str) -> Dict[str, Any]:
        """
        Parse PTT board index HTML.
        Returns dict with articles list, prev_page URL, and parse_errors.
        """
        articles: List[Dict] = []
        parse_errors: List[str] = []
        prev_page: Optional[str] = None
        next_page: Optional[str] = None

        try:
            # Extract prev/next page links
            prev_match = re.search(r'href="(/bbs/Stock/index\d+\.html)"[^>]*>.*?上頁', html)
            if prev_match:
                prev_page = "https://www.ptt.cc" + prev_match.group(1)
            next_match = re.search(r'href="(/bbs/Stock/index\d+\.html)"[^>]*>.*?下頁', html)
            if next_match:
                next_page = "https://www.ptt.cc" + next_match.group(1)

            # Extract article rows
            row_pattern = re.compile(
                r'<div class="r-ent">(.*?)</div>\s*</div>',
                re.DOTALL
            )
            for m in row_pattern.finditer(html):
                try:
                    row_html = m.group(0)
                    article = self._parse_row(row_html)
                    if article:
                        articles.append(article)
                except Exception as exc:
                    parse_errors.append(f"Row parse error: {exc}")
                    logger.debug("PTTListParser: isolated row error: %s", exc)

        except Exception as exc:
            parse_errors.append(f"Page parse error: {exc}")
            logger.warning("PTTListParser: page-level error: %s", exc)

        return {
            "articles": articles,
            "prev_page": prev_page,
            "next_page": next_page,
            "parse_errors": parse_errors,
        }

    def _parse_row(self, row_html: str) -> Optional[Dict]:
        """Parse a single article row. Returns None for announcements/separators."""
        # Push count
        push_text = ""
        push_m = re.search(r'<div class="nrec"><span[^>]*>([^<]*)</span>', row_html)
        if push_m:
            push_text = push_m.group(1).strip()
        push_count = self._parse_push_count(push_text)

        # Title and URL
        title = ""
        url = None
        deleted = False
        deletion_type = None

        title_m = re.search(r'<div class="title">\s*(?:<a href="([^"]+)"[^>]*>([^<]*)</a>|([^<]*))', row_html)
        if title_m:
            if title_m.group(1):
                url = "https://www.ptt.cc" + title_m.group(1)
                title = title_m.group(2).strip() if title_m.group(2) else ""
            else:
                raw = title_m.group(3).strip() if title_m.group(3) else ""
                if raw:
                    deleted = True
                    deletion_type = self._detect_deletion_type(raw)
                    title = raw

        if not title and not url:
            return None

        # Category
        category = self._extract_category(title)

        # Author
        author = ""
        author_m = re.search(r'<div class="author">([^<]*)</div>', row_html)
        if author_m:
            author = author_m.group(1).strip()

        # Date
        date = ""
        date_m = re.search(r'<div class="date">\s*([^<]*)\s*</div>', row_html)
        if date_m:
            date = date_m.group(1).strip()

        # Is pinned/announcement
        is_pinned = "pinned" in row_html.lower() or "置頂" in row_html
        is_announcement = category == "公告"

        return {
            "title": title,
            "url": url,
            "author_display_id": author,
            "date_str": date,
            "push_count": push_count,
            "push_raw": push_text,
            "category": category,
            "is_deleted": deleted,
            "deletion_type": deletion_type,
            "is_pinned": is_pinned,
            "is_announcement": is_announcement,
        }

    def _parse_push_count(self, text: str) -> Any:
        """
        Parse PTT push count.
        爆 → "爆" (very popular, > 100 pushes)
        X1-X9 → negative (boo-heavy)
        numeric → int
        empty → 0
        """
        text = text.strip()
        if not text:
            return 0
        if text == _PUSH_爆:
            return "爆"
        m = _PUSH_X_PATTERN.match(text)
        if m:
            return -int(m.group(1))  # X1 → -1, X9 → -9
        m2 = _PUSH_NUMERIC.match(text)
        if m2:
            return int(text)
        return text  # Unknown format, preserve raw

    def _extract_category(self, title: str) -> str:
        """Extract category from [category] prefix in title."""
        m = re.match(r"^\[([^\]]+)\]", title)
        if m:
            cat = m.group(1)
            if cat in KNOWN_CATEGORIES:
                return cat
            return f"unknown:{cat}"
        return "unknown"

    def _detect_deletion_type(self, raw_text: str) -> str:
        """Detect deletion type from raw title text."""
        if "被刪除" in raw_text or "deleted by" in raw_text.lower():
            return "DELETED_BY_AUTHOR_OR_MOD"
        if "(本文已被刪除)" in raw_text:
            return "DELETED_BY_AUTHOR"
        if "違反版規" in raw_text:
            return "DELETED_BY_MOD_RULE_VIOLATION"
        return "DELETED_UNKNOWN"
