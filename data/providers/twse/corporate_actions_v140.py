"""
data/providers/twse/corporate_actions_v140.py — TWSE corporate actions service v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Never auto-calculates fake adjusted prices.
"""
from __future__ import annotations

from typing import Dict, List

from data.providers.twse.models_v140 import TWSECorporateActionPreview
from data.providers.twse.normalizer_v140 import TWSENormalizer

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TWSECorporateActionsService:
    """In-memory corporate actions service for TWSE."""

    def __init__(self) -> None:
        self._store: Dict[str, List[TWSECorporateActionPreview]] = {}
        self._normalizer = TWSENormalizer()

    def get_actions(self, symbol: str) -> List[TWSECorporateActionPreview]:
        canonical = self._normalizer.canonical_symbol(symbol)
        return list(self._store.get(canonical, []))

    def upsert(self, action: TWSECorporateActionPreview) -> None:
        canonical = self._normalizer.canonical_symbol(action.symbol)
        if canonical not in self._store:
            self._store[canonical] = []
        self._store[canonical].append(action)
