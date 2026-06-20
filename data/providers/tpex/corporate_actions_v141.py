"""
data/providers/tpex/corporate_actions_v141.py — TPEx corporate actions service v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
[!] adjusted_status = 'UNKNOWN' when no precise adjustment factor.
"""
from __future__ import annotations

from typing import Dict, List

from data.providers.tpex.models_v141 import TPExCorporateActionPreview
from data.providers.tpex.normalizer_v141 import TPExNormalizer

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TPExCorporateActionsService:
    """In-memory corporate actions service for TPEx."""

    def __init__(self) -> None:
        self._store: Dict[str, List[TPExCorporateActionPreview]] = {}
        self._normalizer = TPExNormalizer()

    def get_actions(self, symbol: str) -> List[TPExCorporateActionPreview]:
        canonical = self._normalizer.canonical_symbol(symbol)
        return list(self._store.get(canonical, []))

    def upsert(self, action: TPExCorporateActionPreview) -> None:
        canonical = self._normalizer.canonical_symbol(action.symbol)
        if canonical not in self._store:
            self._store[canonical] = []
        self._store[canonical].append(action)
