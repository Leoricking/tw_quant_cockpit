"""
paper_trading/market_data/symbol_mapper_v161.py — Symbol Mapper v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Ambiguous symbol mapping → BLOCKED (no guessing). Canonical TW stock code format.
"""
from __future__ import annotations
from typing import Dict, Optional, Tuple

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True
AMBIGUOUS_SYMBOL_MAPPING_BLOCKED: bool = True


class SymbolMappingError(Exception):
    pass


class SymbolMapper:
    """
    Maps provider-specific symbol formats to canonical TW stock codes.
    Ambiguous mappings are BLOCKED (raises SymbolMappingError).
    No guessing — explicit registration required.
    """

    def __init__(self) -> None:
        self._mappings: Dict[str, str] = {}    # provider_symbol → canonical
        self._ambiguous: Dict[str, int] = {}   # provider_symbol → count of registrations

    def register(self, provider_symbol: str, canonical_symbol: str) -> None:
        """Register a provider symbol → canonical mapping."""
        if not provider_symbol or not canonical_symbol:
            raise SymbolMappingError("provider_symbol and canonical_symbol must be non-empty")

        if provider_symbol in self._ambiguous:
            self._ambiguous[provider_symbol] += 1
        elif provider_symbol in self._mappings:
            existing = self._mappings[provider_symbol]
            if existing != canonical_symbol:
                # Conflict: mark as ambiguous
                self._ambiguous[provider_symbol] = 2
                del self._mappings[provider_symbol]
                raise SymbolMappingError(
                    f"BLOCKED: ambiguous symbol mapping for '{provider_symbol}': "
                    f"previously mapped to '{existing}', now '{canonical_symbol}'. "
                    "AMBIGUOUS_SYMBOL_MAPPING_BLOCKED=True."
                )
        else:
            self._mappings[provider_symbol] = canonical_symbol

    def resolve(self, provider_symbol: str) -> str:
        """Resolve provider symbol to canonical. Raises SymbolMappingError if ambiguous or unknown."""
        if provider_symbol in self._ambiguous:
            raise SymbolMappingError(
                f"BLOCKED: symbol '{provider_symbol}' has ambiguous mappings. "
                "AMBIGUOUS_SYMBOL_MAPPING_BLOCKED=True. Register unambiguous mapping first."
            )
        if provider_symbol not in self._mappings:
            raise SymbolMappingError(
                f"Symbol '{provider_symbol}' not registered. "
                "Register it explicitly — no guessing allowed."
            )
        return self._mappings[provider_symbol]

    def try_resolve(self, provider_symbol: str) -> Tuple[bool, Optional[str], str]:
        """Returns (success, canonical_or_None, reason)."""
        try:
            canonical = self.resolve(provider_symbol)
            return True, canonical, ""
        except SymbolMappingError as e:
            return False, None, str(e)

    def list_mappings(self) -> Dict[str, str]:
        return dict(self._mappings)

    def count(self) -> int:
        return len(self._mappings)
