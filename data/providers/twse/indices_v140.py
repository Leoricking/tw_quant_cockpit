"""
data/providers/twse/indices_v140.py — TWSE index service v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from data.providers.twse.models_v140 import TWSEIndexRecord

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

TAIEX_CODE = "TAIEX"


class TWSEIndicesService:
    """In-memory index service for TWSE."""

    def __init__(self) -> None:
        self._store: Dict[Tuple[str, str], TWSEIndexRecord] = {}

    def get_index(self, index_code: str, trade_date: str) -> Optional[TWSEIndexRecord]:
        return self._store.get((index_code, trade_date))

    def get_index_history(
        self, index_code: str, start_date: str, end_date: str
    ) -> List[TWSEIndexRecord]:
        return sorted(
            [
                rec
                for (code, d), rec in self._store.items()
                if code == index_code and start_date <= d <= end_date
            ],
            key=lambda r: r.trade_date,
        )

    def upsert(self, record: TWSEIndexRecord) -> None:
        self._store[(record.index_code, record.trade_date)] = record
