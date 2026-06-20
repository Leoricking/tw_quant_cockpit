"""
data/providers/tpex/indices_v141.py — TPEx indices service v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
[!] Not TAIEX. TPEx composite index is separate from TWSE TAIEX.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from data.providers.tpex.models_v141 import TPExIndexRecord

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

TPEX_INDEX_CODE = "TPEX"


class TPExIndicesService:
    """In-memory indices service for TPEx."""

    def __init__(self) -> None:
        self._store: Dict[Tuple[str, str], TPExIndexRecord] = {}

    def get_index(self, index_code: str, trade_date: str) -> Optional[TPExIndexRecord]:
        return self._store.get((index_code, trade_date))

    def get_index_history(
        self, index_code: str, start_date: str, end_date: str
    ) -> List[TPExIndexRecord]:
        return sorted(
            [
                rec
                for (code, d), rec in self._store.items()
                if code == index_code and start_date <= d <= end_date
            ],
            key=lambda r: r.trade_date,
        )

    def upsert(self, record: TPExIndexRecord) -> None:
        self._store[(record.index_code, record.trade_date)] = record
