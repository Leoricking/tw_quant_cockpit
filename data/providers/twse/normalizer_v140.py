"""
data/providers/twse/normalizer_v140.py — TWSE symbol normalizer v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
"""
from __future__ import annotations

import re
from typing import Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_ETF_PREFIXES = {"0"}
_ETF_INDUSTRY_CODES = {"31", "ETF"}


class TWSENormalizer:
    """Normalizes TWSE symbols and classifies securities."""

    def canonical_symbol(self, symbol: str) -> str:
        """
        Normalize symbol to TWSE canonical form (bare numeric code).
        "2330.TW" → "2330"
        "TWSE:2330" → "2330"
        "2330" → "2330"
        """
        s = str(symbol).strip()
        # Remove TWSE: prefix
        if s.upper().startswith("TWSE:"):
            s = s[5:]
        # Remove .TW / .TWO suffix
        s = re.sub(r"\.(TW|TWO)$", "", s, flags=re.IGNORECASE)
        return s.strip()

    def is_common_stock(self, symbol: str, security_type: Optional[str]) -> bool:
        """Return True if the security is a common stock."""
        if security_type:
            st_upper = str(security_type).upper()
            if st_upper in ("ETF", "WARRANT", "TDR", "BOND", "INDEX", "PREFERRED_STOCK", "FOREIGN_STOCK"):
                return False
            if st_upper == "COMMON_STOCK":
                return True
        # Heuristic: 4-digit numeric code not starting with "0"
        sym = self.canonical_symbol(symbol)
        if re.match(r"^\d{4}$", sym) and not sym.startswith("0"):
            return True
        return False

    def is_etf(self, symbol: str, security_type: Optional[str]) -> bool:
        """Return True if the security is an ETF."""
        if security_type:
            st_upper = str(security_type).upper()
            if st_upper == "ETF":
                return True
        sym = self.canonical_symbol(symbol)
        # 4-digit starting with "0" heuristic
        if re.match(r"^0\d{3}$", sym):
            return True
        return False

    def classify_security_type(self, raw_type_str: Optional[str]) -> str:
        """Classify security type from raw string."""
        if not raw_type_str:
            return "UNKNOWN"
        s = str(raw_type_str).upper().strip()
        if "ETF" in s:
            return "ETF"
        if "WARRANT" in s or "認購" in raw_type_str or "認售" in raw_type_str:
            return "WARRANT"
        if "TDR" in s:
            return "TDR"
        if "PREFERRED" in s or "特別股" in raw_type_str:
            return "PREFERRED_STOCK"
        if "BOND" in s or "債" in raw_type_str:
            return "BOND"
        if "FOREIGN" in s or "外國" in raw_type_str:
            return "FOREIGN_STOCK"
        if "COMMON" in s or "普通股" in raw_type_str:
            return "COMMON_STOCK"
        return "UNKNOWN"

    def normalize_industry_code(self, raw: str) -> str:
        """Normalize industry code to a standard format."""
        if not raw:
            return ""
        return str(raw).strip()
