"""
data/providers/twse/market_summary_v140.py — TWSE market summary service v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
"""
from __future__ import annotations

from typing import Dict, Optional

from data.providers.twse.models_v140 import TWSEMarketSummary

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TWSEMarketSummaryService:
    """In-memory market summary service for TWSE."""

    def __init__(self) -> None:
        self._store: Dict[str, TWSEMarketSummary] = {}

    def get_summary(self, trade_date: str) -> Optional[TWSEMarketSummary]:
        return self._store.get(trade_date)

    def upsert(self, summary: TWSEMarketSummary) -> None:
        self._store[summary.trade_date] = summary
