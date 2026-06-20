"""
data/providers/tpex/normalizer_v141.py — TPEx symbol normalizer v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
"""
from __future__ import annotations

import re
from typing import Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TPExNormalizer:
    """Normalizes TPEx symbols and classifies securities."""

    def canonical_symbol(self, symbol: str) -> str:
        """
        Normalize symbol to TPEx canonical form (bare numeric code).
        "5274.TWO" -> "5274"
        "TPEx:5274" -> "5274"
        "OTC:5274" -> "5274"
        "5274" -> "5274"
        Unknown prefixes handled gracefully.
        """
        s = str(symbol).strip()
        # Remove known prefix types (case-insensitive)
        for prefix in ("TPEX:", "OTC:", "TWSE:", "TW:"):
            if s.upper().startswith(prefix.upper()):
                s = s[len(prefix):]
                break
        # Remove suffix: .TWO, .TW, .OTC
        s = re.sub(r"\.(TWO|TW|OTC)$", "", s, flags=re.IGNORECASE)
        # Handle unknown_market:XXXX pattern gracefully
        if ":" in s:
            s = s.split(":")[-1]
        return s.strip()

    def is_common_stock(self, symbol: str, security_type: Optional[str]) -> bool:
        """Return True if the security is a common stock."""
        if security_type:
            st_upper = str(security_type).upper()
            if st_upper in (
                "ETF", "ETN", "WARRANT", "TDR", "BOND", "REIT",
                "FOREIGN_STOCK", "EMERGING_STOCK", "PIONEER_STOCK",
                "GO_INCUBATION", "CONVERTIBLE_BOND", "OTHER",
            ):
                return False
            if st_upper == "COMMON_STOCK":
                return True
        return False

    def is_etf(self, symbol: str, security_type: Optional[str]) -> bool:
        """Return True if the security is an ETF."""
        if security_type:
            st_upper = str(security_type).upper()
            if st_upper in ("ETF", "ETN"):
                return True
        return False

    def is_emerging(self, symbol: str, security_type: Optional[str]) -> bool:
        """Return True if the security is an emerging/興櫃 stock."""
        if security_type:
            st_upper = str(security_type).upper()
            if st_upper in ("EMERGING_STOCK", "PIONEER_STOCK", "GO_INCUBATION"):
                return True
        return False

    def classify_security_type(self, raw_type_str: Optional[str]) -> str:
        """Classify security type from raw string."""
        if not raw_type_str:
            return "UNKNOWN"
        s = str(raw_type_str).upper().strip()
        if "ETN" in s:
            return "ETN"
        if "ETF" in s:
            return "ETF"
        if "REIT" in s:
            return "REIT"
        if "WARRANT" in s or "認購" in raw_type_str or "認售" in raw_type_str:
            return "WARRANT"
        if "TDR" in s:
            return "TDR"
        if "EMERGING" in s or "興櫃" in raw_type_str:
            return "EMERGING_STOCK"
        if "PIONEER" in s or "先驅" in raw_type_str:
            return "PIONEER_STOCK"
        if "GO_INCUBATION" in s or "創櫃" in raw_type_str:
            return "GO_INCUBATION"
        if "CONVERTIBLE" in s or "可轉換" in raw_type_str:
            return "CONVERTIBLE_BOND"
        if "BOND" in s or "債" in raw_type_str:
            return "BOND"
        if "FOREIGN" in s or "外國" in raw_type_str:
            return "FOREIGN_STOCK"
        if "COMMON" in s or "普通股" in raw_type_str:
            return "COMMON_STOCK"
        return "UNKNOWN"

    def is_universe_eligible(self, symbol: str, security_type: Optional[str], board: Optional[str]) -> bool:
        """
        Return True only for MAINBOARD COMMON_STOCK securities.
        All other types (ETF, emerging, warrant, etc.) are excluded.
        """
        if not self.is_common_stock(symbol, security_type):
            return False
        if board is None:
            return False
        board_upper = str(board).upper()
        return board_upper == "MAINBOARD"

    def detect_market_conflict(self, symbol: str, claimed_market: str) -> Optional[str]:
        """
        Detect market conflict.
        If symbol has .TW suffix and claimed_market is 'TPEx' -> MARKET_CONFLICT.
        Returns "MARKET_CONFLICT" string or None.
        """
        s = str(symbol).strip()
        claimed = str(claimed_market).upper().strip()
        # .TW suffix means TWSE
        if re.search(r"\.TW$", s, flags=re.IGNORECASE) and not re.search(r"\.TWO$", s, flags=re.IGNORECASE):
            if "TPEX" in claimed or "OTC" in claimed:
                return "MARKET_CONFLICT"
        # .TWO suffix means TPEx; if claimed is TWSE, also conflict
        if re.search(r"\.TWO$", s, flags=re.IGNORECASE):
            if "TWSE" in claimed:
                return "MARKET_CONFLICT"
        return None
