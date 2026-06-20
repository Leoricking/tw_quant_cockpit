"""
data/providers/tpex/suspension_v141.py — TPEx suspension service v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from data.providers.tpex.models_v141 import TPExSuspensionRecord
from data.providers.tpex.normalizer_v141 import TPExNormalizer

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TPExSuspensionService:
    """In-memory suspension/resumption service for TPEx."""

    def __init__(self) -> None:
        self._store: Dict[str, List[TPExSuspensionRecord]] = {}
        self._normalizer = TPExNormalizer()

    def get_suspensions(self, symbol: Optional[str] = None) -> List[TPExSuspensionRecord]:
        if symbol is not None:
            canonical = self._normalizer.canonical_symbol(symbol)
            return list(self._store.get(canonical, []))
        result = []
        for records in self._store.values():
            result.extend(records)
        return result

    def get_current_suspensions(self) -> List[TPExSuspensionRecord]:
        """Return records where status indicates currently suspended."""
        result = []
        for records in self._store.values():
            for rec in records:
                if rec.status and str(rec.status).upper() in ("SUSPENDED", "ACTIVE"):
                    result.append(rec)
                elif rec.action and str(rec.action).upper() == "SUSPEND" and not rec.resume_date:
                    result.append(rec)
        return result

    def upsert(self, record: TPExSuspensionRecord) -> None:
        canonical = self._normalizer.canonical_symbol(record.symbol)
        if canonical not in self._store:
            self._store[canonical] = []
        self._store[canonical].append(record)

    def is_suspended(self, symbol: str, date: str) -> bool:
        """Return True if the symbol is suspended on the given date."""
        records = self.get_suspensions(symbol)
        for rec in records:
            effective = rec.effective_date
            resume = rec.resume_date
            if effective and date >= effective:
                if resume is None or date < resume:
                    return True
        return False
