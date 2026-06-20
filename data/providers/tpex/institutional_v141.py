"""
data/providers/tpex/institutional_v141.py — TPEx institutional service v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
[!] Dealer proprietary and hedge are SEPARATE fields. Never mixed.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from data.providers.tpex.models_v141 import TPExInstitutionalFlow
from data.providers.tpex.normalizer_v141 import TPExNormalizer

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TPExInstitutionalService:
    """In-memory institutional flow service for TPEx. Dealer proprietary and hedge are separate."""

    def __init__(self) -> None:
        self._store: Dict[Tuple[str, str], TPExInstitutionalFlow] = {}
        self._normalizer = TPExNormalizer()

    def get_flow(self, symbol: str, trade_date: str) -> Optional[TPExInstitutionalFlow]:
        canonical = self._normalizer.canonical_symbol(symbol)
        return self._store.get((canonical, trade_date))

    def get_flows(self, symbol: str, start_date: str, end_date: str) -> List[TPExInstitutionalFlow]:
        canonical = self._normalizer.canonical_symbol(symbol)
        return sorted(
            [
                flow
                for (sym, d), flow in self._store.items()
                if sym == canonical and start_date <= d <= end_date
            ],
            key=lambda f: f.trade_date,
        )

    def upsert(self, flow: TPExInstitutionalFlow) -> None:
        """Upsert. dealer_proprietary and dealer_hedge must remain separate."""
        canonical = self._normalizer.canonical_symbol(flow.symbol)
        self._store[(canonical, flow.trade_date)] = flow
