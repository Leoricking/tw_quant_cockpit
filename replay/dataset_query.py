"""
replay/dataset_query.py — ReplayDatasetQuery v1.2.8

Query interface for the dataset registry.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDatasetQuery:
    """
    Query interface for the dataset registry.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self, registry=None):
        self._registry = registry

    def datasets(self, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.list_datasets(filters)

    def dataset(self, dataset_id: str) -> Optional[Any]:
        if self._registry is None:
            return None
        return self._registry.get_dataset(dataset_id)

    def versions(self, dataset_id: str) -> List[Any]:
        if self._registry is None:
            return []
        return []  # implemented via version manager

    def lineage(self, dataset_id: str) -> List[Any]:
        return []

    def duplicates(self) -> List[Dict[str, Any]]:
        if self._registry is None:
            return []
        return self._registry.detect_duplicates()

    def missing(self) -> List[Dict[str, Any]]:
        if self._registry is None:
            return []
        return self._registry.detect_missing()

    def corrupted(self) -> List[Dict[str, Any]]:
        if self._registry is None:
            return []
        return self._registry.detect_corrupted()

    def stale(self) -> List[Dict[str, Any]]:
        if self._registry is None:
            return []
        return self._registry.detect_stale()

    def frozen(self) -> List[Any]:
        if self._registry is None:
            return []
        return [d for d in self._registry.list_datasets() if d.frozen_at]

    def archived(self) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.filter(status="ARCHIVED")

    def by_symbol(self, symbol: str) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.filter(symbol=symbol)

    def by_timeframe(self, timeframe: str) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.filter(timeframe=timeframe)

    def by_mode(self, mode: str) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.filter(mode=mode)

    def by_qualification(self, qualification: str) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.filter(qualification=qualification)

    def search(self, query: str) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.search(query)
