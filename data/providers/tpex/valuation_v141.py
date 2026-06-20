"""
data/providers/tpex/valuation_v141.py — TPEx valuation service v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
[!] '--' -> None (never 0). Negative PE preserved (valid for loss-making companies).
[!] Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from data.providers.tpex.models_v141 import TPExValuationRecord
from data.providers.tpex.normalizer_v141 import TPExNormalizer

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TPExValuationService:
    """In-memory valuation service for TPEx."""

    def __init__(self) -> None:
        self._store: Dict[Tuple[str, str], TPExValuationRecord] = {}
        self._normalizer = TPExNormalizer()

    def get_valuation(
        self, symbol: str, trade_date: Optional[str] = None
    ) -> Optional[TPExValuationRecord]:
        canonical = self._normalizer.canonical_symbol(symbol)
        if trade_date is not None:
            return self._store.get((canonical, trade_date))
        # Return latest if no date specified
        return self.get_latest_valuation(symbol)

    def get_latest_valuation(self, symbol: str) -> Optional[TPExValuationRecord]:
        canonical = self._normalizer.canonical_symbol(symbol)
        records = [rec for (sym, _), rec in self._store.items() if sym == canonical]
        if not records:
            return None
        return max(records, key=lambda r: r.trade_date)

    def upsert(self, record: TPExValuationRecord) -> None:
        """Upsert. '--' must have been parsed as None before reaching here."""
        canonical = self._normalizer.canonical_symbol(record.symbol)
        self._store[(canonical, record.trade_date)] = record
