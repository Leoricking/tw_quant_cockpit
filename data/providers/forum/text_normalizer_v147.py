"""
data/providers/forum/text_normalizer_v147.py — Forum Text Normalizer v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Traditional Chinese text normalization for PTT content.
"""
from __future__ import annotations

import html
import re
from typing import List, Tuple

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Whitespace normalization
_WS_PATTERN = re.compile(r"[ \t\u3000\u00a0]+")
# URL extraction
_URL_PATTERN = re.compile(r"https?://[^\s\u3000\u300c\u300d\uff08\uff09<>\"']+")
# 4-digit stock code candidate (but NOT 4-digit years or prices)
_STOCK_CODE_CANDIDATE = re.compile(r"\b([0-9]{4,6}[A-Z]?)\b")
# Year pattern (reject as stock code)
_YEAR_PATTERN = re.compile(r"\b(19|20)\d{2}\b")
# Price pattern (reject as stock code) e.g. 500元 500.5
_PRICE_PATTERN = re.compile(r"\b\d{1,5}(?:\.\d+)?(?:元|塊|點)\b")


class ForumTextNormalizer:
    """
    Traditional Chinese forum text normalizer.
    Handles HTML entities, whitespace, URL extraction, stock code candidates, emoji.
    """

    def normalize(self, text: str) -> str:
        """Full normalization pipeline."""
        if not text:
            return ""
        text = self.decode_html_entities(text)
        text = self.normalize_whitespace(text)
        return text

    def decode_html_entities(self, text: str) -> str:
        """Decode HTML entities (&amp;, &lt;, etc.)."""
        if not text:
            return ""
        return html.unescape(text)

    def normalize_whitespace(self, text: str) -> str:
        """Normalize various whitespace characters to single space."""
        if not text:
            return ""
        text = _WS_PATTERN.sub(" ", text)
        return text.strip()

    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text (does not resolve them)."""
        if not text:
            return []
        return _URL_PATTERN.findall(text)

    def extract_stock_code_candidates(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract stock code candidates from text.
        Returns list of (candidate, context) tuples.
        Filters out obvious years (19xx/20xx) and price patterns.
        """
        if not text:
            return []
        years = set(_YEAR_PATTERN.findall(text))
        results = []
        for m in _STOCK_CODE_CANDIDATE.finditer(text):
            code = m.group(1)
            if code in years:
                continue
            # Skip if obviously a price context
            start = max(0, m.start() - 5)
            end = min(len(text), m.end() + 5)
            ctx = text[start:end]
            if re.search(r"\d+(?:\.\d+)?(?:元|塊|點)", ctx):
                continue
            results.append((code, ctx))
        return results

    def preserve_emoji(self, text: str) -> str:
        """Emoji are preserved as-is (no stripping)."""
        return text  # emoji preserved
