"""
data/providers/tpex/margin_v141.py — TPEx margin service v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
[!] Never assign market total to a symbol.
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

from data.providers.tpex.models_v141 import TPExMarginRecord
from data.providers.tpex.normalizer_v141 import TPExNormalizer

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TPExMarginService:
    """In-memory margin service for TPEx. Never substitutes missing margin with market total."""

    def __init__(self) -> None:
        self._store: Dict[Tuple[str, str], TPExMarginRecord] = {}
        self._normalizer = TPExNormalizer()

    def get_margin(self, symbol: str, trade_date: str) -> Optional[TPExMarginRecord]:
        """Return margin record for symbol/date, or None. Never returns market total for missing symbol."""
        canonical = self._normalizer.canonical_symbol(symbol)
        return self._store.get((canonical, trade_date))

    def upsert(self, record: TPExMarginRecord) -> None:
        canonical = self._normalizer.canonical_symbol(record.symbol)
        self._store[(canonical, record.trade_date)] = record
