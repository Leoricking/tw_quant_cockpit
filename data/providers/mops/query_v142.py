"""
data/providers/mops/query_v142.py — MOPS query service v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class MOPSQueryService:
    """
    Query service for MOPS data. Reads from MOPSStore.
    No auto-fetch. No mock fallback.
    """

    def __init__(self) -> None:
        from data.providers.mops.store_v142 import MOPSStore
        self._store = MOPSStore()

    def get_profile(self, symbol: str) -> Optional[Any]:
        return self._store.get_profile(symbol)

    def get_revenue(self, symbol: str, year_month: str) -> Optional[Any]:
        return self._store.get_revenue(symbol, year_month)

    def get_balance_sheet(self, symbol: str, fiscal_year: int, fiscal_period: str) -> Optional[Any]:
        return self._store.get_balance_sheet(symbol, fiscal_year, fiscal_period)

    def get_income_statement(self, symbol: str, fiscal_year: int, fiscal_period: str) -> Optional[Any]:
        return self._store.get_income_statement(symbol, fiscal_year, fiscal_period)

    def get_cash_flow(self, symbol: str, fiscal_year: int, fiscal_period: str) -> Optional[Any]:
        return self._store.get_cash_flow(symbol, fiscal_year, fiscal_period)

    def get_material_info(self, symbol: str) -> List[Any]:
        return self._store.get_material_info(symbol)

    def get_conferences(self, symbol: str) -> List[Any]:
        return self._store.get_conferences(symbol)

    def get_xbrl_docs(self, symbol: str, fiscal_year: int) -> List[Any]:
        return self._store.get_xbrl_docs(symbol, fiscal_year)

    def get_revisions(self, symbol: str, filing_id: str) -> List[Any]:
        return self._store.get_revisions(symbol, filing_id)

    def store_ref(self):
        """Return reference to underlying store (for tests)."""
        return self._store

    def count_all(self) -> Dict[str, int]:
        return self._store.count_all()
