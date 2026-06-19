"""
universe/symbol_normalizer.py — Symbol normalization for TW Quant Cockpit v1.3.1.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Normalization handles identification only — NOT quality gate.
[!] Extension .TW does NOT mean data is real/live.
[!] Unknown market -> UNKNOWN (do not guess). Not Investment Advice.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Optional

from universe.models import UniverseMarket

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS             = True
BROKER_DISABLED            = True
PRODUCTION_TRADING_BLOCKED = True

# ---------------------------------------------------------------------------
# Known TPEx codes (4-digit starting with 4-6, but not always)
# This is a RESEARCH SEED set — NOT a complete market master.
# ---------------------------------------------------------------------------
_KNOWN_TPEX_PREFIXES = {
    "4", "5", "6",  # Common TPEx prefixes
}

# Known TWSE prefixes (most 4-digit codes not in TPEx range)
_KNOWN_TWSE_PREFIXES = {
    "1", "2", "3", "8",  # Common TWSE prefixes
}

# Extension -> market mapping
_EXTENSION_MARKET_MAP = {
    ".TW": UniverseMarket.TWSE.value,
    ".TWO": UniverseMarket.TPEX.value,
}

# Prefix -> market mapping
_PREFIX_MARKET_MAP = {
    "TWSE:": UniverseMarket.TWSE.value,
    "TPEx:": UniverseMarket.TPEX.value,
    "TPEX:": UniverseMarket.TPEX.value,
}

# Warrant/option symbol pattern (6+ digits, or letters+digits)
_WARRANT_PATTERN = re.compile(r"^\d{6,}[A-Z]?$")
_VALID_TW_SYMBOL = re.compile(r"^\d{4,6}$")
_FOREIGN_PATTERN = re.compile(r"^[A-Z]{1,5}$")


@dataclass
class NormalizedSymbolResult:
    """
    Result of a symbol normalization attempt.

    [!] normalized_symbol is identification only — NOT quality gate.
    [!] is_valid=True means parseable — NOT data is available or tradeable.
    """
    normalized_symbol: str = ""
    detected_market: str = UniverseMarket.UNKNOWN.value
    original_symbol: str = ""
    is_valid: bool = False
    warning: str = ""

    def to_dict(self) -> dict:
        return {
            "normalized_symbol": self.normalized_symbol,
            "detected_market": self.detected_market,
            "original_symbol": self.original_symbol,
            "is_valid": self.is_valid,
            "warning": self.warning,
        }


class SymbolNormalizer:
    """
    Normalizes Taiwan stock symbols to a canonical form.

    Rules:
    - Leading zeros must NOT be stripped
    - Unknown market -> UNKNOWN (never guess)
    - Warrants, ETFs, common stocks must NOT be mixed as same security type
    - Stock names cannot be symbols
    - Extension .TW does not mean data is real/live
    - Non-Taiwan symbols -> graceful UNSUPPORTED

    [!] Research Only. No Real Orders.
    """

    NO_REAL_ORDERS             = True
    BROKER_DISABLED            = True
    PRODUCTION_TRADING_BLOCKED = True

    def normalize(self, symbol_str: str) -> NormalizedSymbolResult:
        """
        Normalize a symbol string.

        Supports:
        - "2330"        -> TWSE
        - "2330.TW"     -> TWSE
        - "2330.tw"     -> TWSE (case insensitive suffix)
        - "TWSE:2330"   -> TWSE
        - "6488"        -> TPEx (if known prefix, else UNKNOWN)
        - "6488.TWO"    -> TPEx
        - "TPEx:6488"   -> TPEx

        Returns NormalizedSymbolResult.
        """
        if not symbol_str or not isinstance(symbol_str, str):
            return NormalizedSymbolResult(
                original_symbol=str(symbol_str or ""),
                is_valid=False,
                warning="Empty or non-string symbol",
            )

        raw = symbol_str.strip()
        original = raw
        detected_market = UniverseMarket.UNKNOWN.value
        warning_parts = []

        # Step 1: Strip known prefix
        code = raw
        for prefix, mkt in _PREFIX_MARKET_MAP.items():
            if raw.upper().startswith(prefix.upper()):
                code = raw[len(prefix):]
                detected_market = mkt
                break

        # Step 2: Strip known extension (case insensitive)
        upper_code = code.upper()
        ext_stripped = False
        for ext, mkt in _EXTENSION_MARKET_MAP.items():
            if upper_code.endswith(ext):
                code = code[: -len(ext)]
                if detected_market == UniverseMarket.UNKNOWN.value:
                    detected_market = mkt
                elif detected_market != mkt:
                    warning_parts.append(
                        f"Extension market {mkt} conflicts with prefix market {detected_market}"
                    )
                ext_stripped = True
                break

        # Step 3: Validate the remaining code
        code = code.strip()

        # Must not be a Chinese name or description
        if _contains_chinese(code):
            return NormalizedSymbolResult(
                original_symbol=original,
                normalized_symbol="",
                detected_market=UniverseMarket.UNKNOWN.value,
                is_valid=False,
                warning="Symbol appears to be a stock name, not a symbol code",
            )

        # Must not be a pure alphabetic foreign symbol (graceful UNSUPPORTED)
        if _FOREIGN_PATTERN.match(code) and not code.isdigit():
            return NormalizedSymbolResult(
                original_symbol=original,
                normalized_symbol=code,
                detected_market=UniverseMarket.UNKNOWN.value,
                is_valid=False,
                warning="Foreign/non-Taiwan symbol: UNSUPPORTED — only Taiwan symbols are supported",
            )

        # Warrant detection (6+ digit codes ending in letter or very long)
        if _WARRANT_PATTERN.match(code):
            warning_parts.append(
                "Symbol pattern suggests warrant or option — verify security type separately"
            )

        # Must be 4-6 digits for a valid TW symbol
        if not _VALID_TW_SYMBOL.match(code):
            return NormalizedSymbolResult(
                original_symbol=original,
                normalized_symbol=code,
                detected_market=UniverseMarket.UNKNOWN.value,
                is_valid=False,
                warning=f"Symbol '{code}' does not match Taiwan 4-6 digit pattern",
            )

        # Step 4: Infer market from leading digit if still UNKNOWN
        if detected_market == UniverseMarket.UNKNOWN.value and len(code) >= 4:
            first_digit = code[0]
            if first_digit in _KNOWN_TWSE_PREFIXES and first_digit not in _KNOWN_TPEX_PREFIXES:
                detected_market = UniverseMarket.TWSE.value
            elif first_digit in _KNOWN_TPEX_PREFIXES and first_digit not in _KNOWN_TWSE_PREFIXES:
                detected_market = UniverseMarket.TPEX.value
            else:
                # Ambiguous or unknown — keep UNKNOWN, do not guess
                warning_parts.append(
                    f"Market could not be determined for '{code}' — labeled UNKNOWN"
                )
                detected_market = UniverseMarket.UNKNOWN.value

        # Step 5: Ensure leading zeros preserved (pad to 4 digits if under 4)
        # But do NOT strip leading zeros from what was given
        normalized = code  # Keep as-is (leading zeros preserved)

        return NormalizedSymbolResult(
            normalized_symbol=normalized,
            detected_market=detected_market,
            original_symbol=original,
            is_valid=True,
            warning="; ".join(warning_parts) if warning_parts else "",
        )


def _contains_chinese(s: str) -> bool:
    """Return True if string contains CJK characters."""
    for ch in s:
        if "\u4e00" <= ch <= "\u9fff":
            return True
        if "\u3400" <= ch <= "\u4dbf":
            return True
        if "\uf900" <= ch <= "\ufaff":
            return True
    return False
