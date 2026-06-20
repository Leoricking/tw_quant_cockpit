"""
data/providers/tpex/market_summary_v141.py — TPEx market summary service v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
"""
from __future__ import annotations

from typing import Dict, Optional

from data.providers.tpex.models_v141 import TPExMarketSummary

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TPExMarketSummaryService:
    """In-memory market summary service for TPEx."""

    def __init__(self) -> None:
        self._store: Dict[str, TPExMarketSummary] = {}

    def get_summary(self, trade_date: str) -> Optional[TPExMarketSummary]:
        return self._store.get(trade_date)

    def upsert(self, summary: TPExMarketSummary) -> None:
        self._store[summary.trade_date] = summary
