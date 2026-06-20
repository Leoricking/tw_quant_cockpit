"""
data/providers/twse/institutional_v140.py — TWSE institutional service v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from data.providers.twse.models_v140 import TWSEInstitutionalFlow
from data.providers.twse.normalizer_v140 import TWSENormalizer

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TWSEInstitutionalService:
    """In-memory institutional flow service for TWSE."""

    def __init__(self) -> None:
        self._store: Dict[Tuple[str, str], TWSEInstitutionalFlow] = {}
        self._normalizer = TWSENormalizer()

    def get_flow(self, symbol: str, trade_date: str) -> Optional[TWSEInstitutionalFlow]:
        canonical = self._normalizer.canonical_symbol(symbol)
        return self._store.get((canonical, trade_date))

    def get_flows(self, symbol: str, start_date: str, end_date: str) -> List[TWSEInstitutionalFlow]:
        canonical = self._normalizer.canonical_symbol(symbol)
        return sorted(
            [
                flow
                for (sym, d), flow in self._store.items()
                if sym == canonical and start_date <= d <= end_date
            ],
            key=lambda f: f.trade_date,
        )

    def upsert(self, flow: TWSEInstitutionalFlow) -> None:
        canonical = self._normalizer.canonical_symbol(flow.symbol)
        self._store[(canonical, flow.trade_date)] = flow
