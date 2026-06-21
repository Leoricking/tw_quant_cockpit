"""
data/providers/forum/entity_alias_v147.py — Entity Alias Registry v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Built-in Taiwan stock alias table for forum symbol linking.
"""
from __future__ import annotations

from typing import Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

ALIAS_TABLE_VERSION = "v147"

# Format: alias_text -> (symbol, confidence_level)
# confidence: EXACT=direct 4-digit match, HIGH=well-known alias, MEDIUM=informal
_ALIAS_TABLE: Dict[str, tuple] = {
    # TWSE Blue chips
    "台積電": ("2330", "HIGH"),
    "tsmc": ("2330", "HIGH"),
    "護國神山": ("2330", "HIGH"),
    "聯發科": ("2454", "HIGH"),
    "mtk": ("2454", "HIGH"),
    "mediatek": ("2454", "HIGH"),
    "鴻海": ("2317", "HIGH"),
    "foxconn": ("2317", "HIGH"),
    "富邦金": ("2881", "HIGH"),
    "國泰金": ("2882", "HIGH"),
    "玉山金": ("2884", "HIGH"),
    "中鋼": ("2002", "HIGH"),
    "台塑": ("1301", "HIGH"),
    "南亞": ("1303", "HIGH"),
    "中華電": ("2412", "HIGH"),
    "大立光": ("3008", "HIGH"),
    "台達電": ("2308", "HIGH"),
    # AI/Server related
    "廣達": ("2382", "HIGH"),
    "緯創": ("3231", "HIGH"),
    "英業達": ("2356", "HIGH"),
    "仁寶": ("2324", "HIGH"),
    "緯穎": ("6669", "HIGH"),
    "川普概念股": ("", "AMBIGUOUS"),
    "ai伺服器": ("", "AMBIGUOUS"),
    # ASIC / CoWoS
    "日月光": ("3711", "HIGH"),
    "矽品": ("2325", "HIGH"),
    "力積電": ("6770", "HIGH"),
    "聯電": ("2303", "HIGH"),
    "umc": ("2303", "HIGH"),
    "旺宏": ("2337", "HIGH"),
    # ETFs
    "0050": ("0050", "EXACT"),
    "台灣50": ("0050", "HIGH"),
    "0056": ("0056", "EXACT"),
    "高股息": ("0056", "MEDIUM"),
    "00878": ("00878", "EXACT"),
    "00881": ("00881", "EXACT"),
    "00919": ("00919", "EXACT"),
    "00929": ("00929", "EXACT"),
    # Networking
    "中磊": ("5388", "HIGH"),
    "智邦": ("2345", "HIGH"),
    "正文": ("4906", "HIGH"),
    # PCB/CCL
    "南電": ("8046", "HIGH"),
    "欣興": ("3037", "HIGH"),
    "台光電": ("2383", "HIGH"),
    "聯茂": ("6213", "HIGH"),
    # Common shorthand
    "台股": ("", "AMBIGUOUS"),  # entire market, not a symbol
}

# Symbols that must NEVER be matched (ambiguous number patterns)
_REJECT_SYMBOLS: set = set()


class EntityAliasRegistry:
    """
    Taiwan stock entity alias registry v1.4.7.
    Maps company names, ETF names, topic terms to stock symbols.
    """

    VERSION = ALIAS_TABLE_VERSION

    def __init__(self) -> None:
        self._table = dict(_ALIAS_TABLE)

    def lookup(self, text: str) -> Optional[tuple]:
        """
        Look up text as alias. Returns (symbol, confidence) or None.
        Case-insensitive for Latin text.
        """
        if not text:
            return None
        # Direct lookup
        result = self._table.get(text)
        if result:
            return result
        # Case-insensitive for ASCII
        result = self._table.get(text.lower())
        if result:
            return result
        return None

    def all_aliases(self) -> Dict[str, tuple]:
        return dict(self._table)

    def is_ambiguous_topic(self, text: str) -> bool:
        """Returns True if text maps to an ambiguous topic (no single symbol)."""
        r = self.lookup(text)
        return r is not None and r[1] == "AMBIGUOUS"
