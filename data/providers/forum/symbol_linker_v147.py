"""
data/providers/forum/symbol_linker_v147.py — Forum Symbol Linker v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] NEVER: year as symbol, price as symbol, article number as symbol.
[!] Formal features only use EXACT/HIGH confidence.
"""
from __future__ import annotations

import re
import uuid
from typing import List, Optional

from data.providers.forum.models_v147 import ForumSymbolMention, SymbolMatchConfidence
from data.providers.forum.entity_alias_v147 import EntityAliasRegistry
from data.providers.forum.text_normalizer_v147 import ForumTextNormalizer

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# 4-digit stock code pattern (Taiwan listed)
_DIRECT_4DIGIT = re.compile(r"\b(\d{4,6})\b")
# Year rejection
_YEAR = re.compile(r"^(19|20)\d{2}$")
# Price rejection context
_PRICE_CTX = re.compile(r"\b\d+(?:\.\d+)?(?:元|塊|點|%|％)\b")
# Article/reference number rejection: preceded by "第" or "頁"
_REF_CTX = re.compile(r"[第頁篇章]\s*\d{4,6}")


def _is_valid_tw_symbol(code: str) -> bool:
    """Basic validation: 4-6 digit numeric, not a year."""
    if not re.match(r"^\d{4,6}[A-Z]?$", code):
        return False
    if _YEAR.match(code):
        return False
    return True


class ForumSymbolLinker:
    """
    Links forum text to Taiwan stock symbols.
    Confidence levels: EXACT > HIGH > MEDIUM > LOW > AMBIGUOUS.
    Formal use: only EXACT/HIGH.
    """

    def __init__(self) -> None:
        self._alias = EntityAliasRegistry()
        self._normalizer = ForumTextNormalizer()

    def link(self, text: str, article_id: str = "") -> List[dict]:
        """
        Extract all symbol mentions from text.
        Returns list of dicts with 'symbol', 'match_confidence', 'match_text', 'context_snippet'.
        [!] NEVER: year, price, article reference as symbol.
        """
        if not text:
            return []
        if not article_id:
            import uuid as _uuid
            article_id = _uuid.uuid4().hex[:8]
        mentions: List[ForumSymbolMention] = []
        seen_symbols = set()

        # Pass 1: Direct 4-6 digit codes
        for m in _DIRECT_4DIGIT.finditer(text):
            code = m.group(1)
            if not _is_valid_tw_symbol(code):
                continue
            # Reject if in price or article reference context
            start = max(0, m.start() - 10)
            end = min(len(text), m.end() + 5)
            ctx = text[start:end]
            if _PRICE_CTX.search(ctx):
                continue
            if _REF_CTX.search(ctx):
                continue
            # Check if it's a known ETF (6-digit like 00878)
            alias_result = self._alias.lookup(code)
            if alias_result and alias_result[0] == code:
                conf = SymbolMatchConfidence.EXACT
            else:
                # Unknown 4-digit — use HIGH if looks like plausible symbol range
                # Taiwan stocks: 1xxx-9xxx main board, 00xxx OTC ETF
                if re.match(r"^[123456789]\d{3}$", code) or re.match(r"^00\d{3,4}$", code):
                    conf = SymbolMatchConfidence.HIGH
                else:
                    conf = SymbolMatchConfidence.MEDIUM
            symbol_key = (code, article_id)
            if symbol_key not in seen_symbols:
                seen_symbols.add(symbol_key)
                mentions.append(ForumSymbolMention(
                    mention_id=str(uuid.uuid4())[:8],
                    article_id=article_id,
                    symbol=code,
                    confidence=conf.value,
                    match_text=code,
                    context_snippet=ctx[:40],
                    formal_use_eligible=(conf in (SymbolMatchConfidence.EXACT, SymbolMatchConfidence.HIGH)),
                ))

        # Pass 2: Alias lookup
        for alias, (symbol, conf_str) in self._alias.all_aliases().items():
            if not symbol:
                continue  # skip ambiguous topics
            if conf_str == "AMBIGUOUS":
                continue
            if alias in text:
                conf = SymbolMatchConfidence[conf_str]
                symbol_key = (symbol, article_id)
                if symbol_key not in seen_symbols:
                    seen_symbols.add(symbol_key)
                    # Extract context
                    idx = text.find(alias)
                    ctx = text[max(0, idx-5):idx+len(alias)+10]
                    mentions.append(ForumSymbolMention(
                        mention_id=str(uuid.uuid4())[:8],
                        article_id=article_id,
                        symbol=symbol,
                        confidence=conf.value,
                        match_text=alias,
                        context_snippet=ctx[:40],
                        formal_use_eligible=(conf in (
                            SymbolMatchConfidence.EXACT,
                            SymbolMatchConfidence.HIGH,
                        )),
                    ))

        return [
            {
                "symbol": m.symbol,
                "match_confidence": m.confidence,
                "match_text": m.match_text,
                "context_snippet": m.context_snippet,
                "formal_use_eligible": m.formal_use_eligible,
            }
            for m in mentions
        ]
