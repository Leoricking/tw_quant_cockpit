"""
data/providers/twse/margin_v140.py — TWSE margin service v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

from data.providers.twse.models_v140 import TWSEMarginRecord
from data.providers.twse.normalizer_v140 import TWSENormalizer

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TWSEMarginService:
    """In-memory margin service for TWSE. Never substitutes missing margin with market total."""

    def __init__(self) -> None:
        self._store: Dict[Tuple[str, str], TWSEMarginRecord] = {}
        self._normalizer = TWSENormalizer()

    def get_margin(self, symbol: str, trade_date: str) -> Optional[TWSEMarginRecord]:
        """Return margin record for symbol/date, or None. Never returns market total for missing symbol."""
        canonical = self._normalizer.canonical_symbol(symbol)
        return self._store.get((canonical, trade_date))

    def upsert(self, record: TWSEMarginRecord) -> None:
        canonical = self._normalizer.canonical_symbol(record.symbol)
        self._store[(canonical, record.trade_date)] = record
