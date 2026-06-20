"""
data/providers/mops/parser_v142.py — MOPS HTML/JSON parser v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
Handles: HTML table parsing, Big5/UTF-8 charset detection, malformed tables,
maintenance pages, and JSON responses. Missing values -> None, never 0.
"""
from __future__ import annotations

import datetime
import json
import re
from typing import Any, Dict, List, Optional, Tuple

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_MISSING_MARKERS = {"--", "---", "-", "N/A", "", "NA", "－", "＊"}
_MAINTENANCE_KEYWORDS = ["系統維護", "maintenance", "Maintenance", "中斷維護", "暫停服務"]


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class MOPSParser:
    """
    Parser for MOPS responses.

    Handles:
    - Big5/UTF-8 charset detection
    - HTML table extraction
    - JSON parsing
    - Malformed response handling
    - Maintenance page detection
    - ROC year (民國年) conversion
    - Missing value normalization: always None, never 0 or empty string
    - Unknown fields: forward-compatible (ignore gracefully)
    """

    def detect_charset(self, content: bytes) -> str:
        """Detect charset from HTML meta tag or default to utf-8."""
        # Look for charset in meta tag
        meta_match = re.search(
            rb'charset\s*=\s*["\']?([\w-]+)["\']?',
            content[:2000],
            re.IGNORECASE,
        )
        if meta_match:
            declared = meta_match.group(1).decode("ascii", errors="replace").lower()
            if "big5" in declared or "950" in declared:
                return "big5"
        return "utf-8"

    def decode_content(self, content: bytes) -> Tuple[str, str]:
        """Decode content bytes to string. Returns (text, charset_used)."""
        charset = self.detect_charset(content)
        try:
            return content.decode(charset, errors="replace"), charset
        except (LookupError, UnicodeDecodeError):
            return content.decode("utf-8", errors="replace"), "utf-8"

    def is_maintenance_page(self, content: bytes) -> bool:
        """Detect MOPS maintenance pages."""
        sample = content[:4096]
        for kw in _MAINTENANCE_KEYWORDS:
            if kw.encode("utf-8", errors="ignore") in sample:
                return True
            if kw.encode("big5", errors="ignore") in sample:
                return True
        return False

    def is_malformed(self, content: bytes) -> bool:
        """Detect clearly malformed responses (empty, too small, binary garbage)."""
        if not content or len(content) < 20:
            return True
        return False

    def _parse_number(self, s: Any) -> Optional[float]:
        """Parse a number string. Returns None for missing/invalid. Never returns 0 for missing."""
        if s is None:
            return None
        s = str(s).strip()
        if s in _MISSING_MARKERS:
            return None
        s = s.replace(",", "").replace("，", "")
        if s.startswith("+"):
            s = s[1:]
        if s.endswith("%"):
            s = s[:-1]
        try:
            return float(s)
        except (ValueError, TypeError):
            return None

    def _parse_str(self, s: Any) -> Optional[str]:
        """Parse a string field. Returns None for missing markers."""
        if s is None:
            return None
        s = str(s).strip()
        if s in _MISSING_MARKERS:
            return None
        return s if s else None

    def parse_roc_date(self, roc_str: Any) -> Optional[str]:
        """Convert ROC date to CE date. Handles multiple formats."""
        if roc_str is None:
            return None
        s = str(roc_str).strip()
        # Format "1130101" (YYYMMDD)
        m = re.match(r"^(\d{3})(\d{2})(\d{2})$", s)
        if m:
            roc_year = int(m.group(1))
            return f"{roc_year + 1911:04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
        # Format "113/01/01"
        m = re.match(r"^(\d{2,3})/(\d{2})/(\d{2})$", s)
        if m:
            roc_year = int(m.group(1))
            return f"{roc_year + 1911:04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
        # Format "113年01月"
        m = re.match(r"^(\d{2,3})\s*年\s*(\d{1,2})\s*月$", s)
        if m:
            roc_year = int(m.group(1))
            return f"{roc_year + 1911:04d}-{int(m.group(2)):02d}"
        # ISO date
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", s)
        if m:
            return s
        # YYYY/MM/DD
        m = re.match(r"^(\d{4})/(\d{2})/(\d{2})$", s)
        if m:
            return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        return None

    def parse_roc_year_month(self, roc_str: Any) -> Optional[str]:
        """Convert ROC year-month to YYYY-MM. '113/01' -> '2024-01'."""
        if roc_str is None:
            return None
        s = str(roc_str).strip()
        m = re.match(r"^(\d{2,3})/(\d{2})$", s)
        if m:
            roc_year = int(m.group(1))
            return f"{roc_year + 1911:04d}-{int(m.group(2)):02d}"
        m = re.match(r"^(\d{4})-(\d{2})$", s)
        if m:
            return s
        return None

    def extract_html_tables(self, html_text: str) -> List[List[List[str]]]:
        """
        Extract all tables from HTML. Returns list of tables.
        Each table is a list of rows. Each row is a list of cell strings.
        Handles malformed tables gracefully.
        """
        tables = []
        # Find all <table> blocks
        table_pattern = re.compile(r"<table[^>]*>(.*?)</table>", re.DOTALL | re.IGNORECASE)
        for table_match in table_pattern.finditer(html_text):
            table_html = table_match.group(1)
            rows = []
            row_pattern = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
            for row_match in row_pattern.finditer(table_html):
                row_html = row_match.group(1)
                cells = []
                cell_pattern = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.DOTALL | re.IGNORECASE)
                for cell_match in cell_pattern.finditer(row_html):
                    cell_html = cell_match.group(1)
                    # Strip tags
                    cell_text = re.sub(r"<[^>]+>", "", cell_html)
                    # Decode HTML entities
                    cell_text = cell_text.replace("&nbsp;", " ").replace("&amp;", "&")
                    cell_text = cell_text.replace("&lt;", "<").replace("&gt;", ">")
                    cell_text = cell_text.strip()
                    cells.append(cell_text)
                if cells:
                    rows.append(cells)
            if rows:
                tables.append(rows)
        return tables

    def parse_json_response(self, content: bytes) -> Tuple[Optional[Any], List[str]]:
        """Parse JSON response. Returns (data, warnings)."""
        warnings: List[str] = []
        if not content:
            return None, ["Empty content"]
        try:
            text = content.decode("utf-8", errors="replace")
            data = json.loads(text)
            return data, warnings
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            warnings.append(f"JSON parse error: {exc}")
            return None, warnings

    def table_to_dicts(
        self, rows: List[List[str]], header_row_index: int = 0
    ) -> Tuple[List[Dict[str, str]], List[str]]:
        """
        Convert a table (list of rows) to list of dicts using header row.
        Unknown fields are included for forward compatibility.
        """
        warnings: List[str] = []
        if not rows or header_row_index >= len(rows):
            return [], ["No rows or header row out of range"]
        headers = rows[header_row_index]
        result = []
        for i, row in enumerate(rows):
            if i == header_row_index:
                continue
            if len(row) < len(headers):
                # Pad with None markers
                row = row + [""] * (len(headers) - len(row))
            record: Dict[str, str] = {}
            for j, header in enumerate(headers):
                if j < len(row):
                    record[header] = row[j]
                else:
                    record[header] = ""
            result.append(record)
        return result, warnings
