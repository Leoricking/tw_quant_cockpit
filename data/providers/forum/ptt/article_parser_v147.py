"""
data/providers/forum/ptt/article_parser_v147.py — PTTArticleParser v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] IP in footer → privacy_v147.py redaction. No full IP stored.
[!] Missing header degrades gracefully. External links extracted.
"""
from __future__ import annotations

import html as html_module
import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_META_AUTHOR = re.compile(r'作者\s*(.*?)\s*看板', re.DOTALL)
_META_BOARD = re.compile(r'看板\s*([^\s<]+)')
_META_TITLE = re.compile(r'標題\s*(.*?)\n')
_META_TIME = re.compile(r'時間\s*([^\n<]+)')
_IP_PATTERN = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
_EDIT_PATTERN = re.compile(r'※ 編輯.*?(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})', re.DOTALL)
_EXTERNAL_LINK = re.compile(r'https?://[^\s<>"]+')


class PTTArticleParser:
    """
    Parses PTT article HTML.
    [!] IP in footer: calls privacy redaction. No full IP in output.
    [!] Missing header: degrades gracefully, marks precision as DAY.
    [!] Mobile footers (BePTT/MeowPtt) handled.
    """

    def __init__(self) -> None:
        from data.providers.forum.privacy_v147 import ForumPrivacyRedactor
        self._privacy = ForumPrivacyRedactor()

    def parse(self, html: str, canonical_url: str = "") -> Dict[str, Any]:
        """
        Parse PTT article HTML. Returns structured article dict.
        [!] IP addresses are redacted via privacy layer.
        """
        result: Dict[str, Any] = {
            "canonical_url": canonical_url,
            "author_display_id": None,
            "board": None,
            "title": None,
            "published_at": None,
            "published_at_precision": "UNKNOWN",
            "body": "",
            "external_links": [],
            "has_mobile_footer": False,
            "edit_history": [],
            "missing_header": False,
            "parse_errors": [],
        }

        try:
            # Decode HTML entities
            content = html_module.unescape(html)

            # Extract main content div
            main_m = re.search(r'<div id="main-content"[^>]*>(.*?)</div>\s*</div>',
                               content, re.DOTALL)
            main_content = main_m.group(1) if main_m else content

            # Strip push/comment section
            push_start = main_content.find('<div class="push">')
            body_section = main_content[:push_start] if push_start > 0 else main_content

            # Extract metadata lines (metas)
            meta_lines = re.findall(r'<span[^>]*class="[^"]*article-meta-value[^"]*"[^>]*>([^<]*)</span>',
                                    body_section)
            keys = re.findall(r'<span[^>]*class="[^"]*article-meta-tag[^"]*"[^>]*>([^<]*)</span>',
                               body_section)

            meta: Dict[str, str] = {}
            for k, v in zip(keys, meta_lines):
                meta[k.strip()] = v.strip()

            # Author
            author = meta.get("作者", "").split()[0] if meta.get("作者") else None
            result["author_display_id"] = author
            # Board
            result["board"] = meta.get("看板")
            # Title
            result["title"] = meta.get("標題", "").strip() or None
            # Time
            time_str = meta.get("時間", "").strip()
            if time_str:
                try:
                    published = self._parse_ptt_time(time_str)
                    result["published_at"] = published
                    result["published_at_precision"] = "MINUTE"
                except Exception:
                    result["published_at"] = time_str
                    result["published_at_precision"] = "DAY"
            else:
                result["missing_header"] = True
                result["published_at_precision"] = "UNKNOWN"

            # Body text (stripped)
            body_text = re.sub(r'<[^>]+>', '', body_section)
            body_text = html_module.unescape(body_text)
            # Remove metadata portion
            body_text = self._remove_meta_prefix(body_text)
            # Conservative signature separation
            body_text = self._remove_signature(body_text)
            body_text = body_text.strip()

            # Redact IPs from body
            body_text = self._privacy.redact_text(body_text)
            result["body"] = body_text

            # External links
            result["external_links"] = list(set(_EXTERNAL_LINK.findall(body_section)))

            # Edit history from footer
            result["edit_history"] = self._parse_edit_history(content)

            # Mobile footer detection
            if "beptt" in content.lower() or "meowptt" in content.lower():
                result["has_mobile_footer"] = True

            # Footer IP redaction
            footer_m = re.search(r'(※ 發信站.*?)(?:</div>|$)', content, re.DOTALL)
            if footer_m:
                footer_raw = footer_m.group(1)
                footer_result = self._privacy.process_article_footer(footer_raw)
                result["footer_redacted"] = footer_result.get("redacted_text", "")
                result["ip_redacted"] = footer_result.get("ip_redacted", False)

        except Exception as exc:
            result["parse_errors"].append(str(exc))
            logger.warning("PTTArticleParser: parse error: %s", exc)

        return result

    def _parse_ptt_time(self, time_str: str) -> str:
        """Parse PTT time string to ISO format."""
        # Example: "Thu Jan  1 12:00:00 2024"
        try:
            dt = datetime.strptime(time_str.strip(), "%a %b %d %H:%M:%S %Y")
            return dt.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            pass
        # Try shorter format
        try:
            dt = datetime.strptime(time_str.strip(), "%Y/%m/%d %H:%M:%S")
            return dt.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            pass
        return time_str

    def _remove_meta_prefix(self, text: str) -> str:
        """Remove PTT metadata header lines from body text."""
        lines = text.split("\n")
        # Skip first 4-5 meta lines (作者/看板/標題/時間)
        in_meta = True
        body_lines = []
        meta_count = 0
        for line in lines:
            if in_meta and meta_count < 6:
                if any(line.strip().startswith(k) for k in ("作者", "看板", "標題", "時間", "author", "board")):
                    meta_count += 1
                    continue
                elif meta_count > 0:
                    in_meta = False
            body_lines.append(line)
        return "\n".join(body_lines)

    def _remove_signature(self, text: str) -> str:
        """Conservative signature separation. Only remove known sig markers."""
        # PTT signature typically starts with "--"
        sig_marker = "\n--\n"
        idx = text.find(sig_marker)
        if idx >= 0:
            return text[:idx]
        return text

    def _parse_edit_history(self, html: str) -> List[Dict]:
        """Extract edit events from article footer."""
        edits = []
        for m in _EDIT_PATTERN.finditer(html):
            edits.append({
                "edited_at": m.group(1),
                "time_precision": "SECOND",
            })
        return edits
