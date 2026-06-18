"""
gui/replay_dataset_catalog_panel.py — Dataset Catalog panel v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDatasetCatalogPanel:
    """
    Displays the dataset catalog with filtering by symbol, timeframe, mode,
    qualification, status, and search.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    COLUMNS = [
        "dataset_id", "name", "mode", "qualification", "status",
        "version", "symbols", "timeframes", "row_count", "fingerprint",
    ]

    def __init__(self) -> None:
        self._registry: Optional[Any] = None
        self._query: Optional[Any] = None

    def _get_query(self) -> Optional[Any]:
        if self._query is None:
            try:
                from replay.dataset_registry import ReplayDatasetRegistry
                from replay.dataset_query import ReplayDatasetQuery
                self._registry = ReplayDatasetRegistry()
                self._query = ReplayDatasetQuery(self._registry)
            except Exception as exc:
                logger.warning("DatasetQuery unavailable: %s", exc)
        return self._query

    def get_all_datasets(self) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.datasets()
        except Exception as exc:
            logger.warning("get_all_datasets failed: %s", exc)
            return []

    def search_datasets(self, query: str) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.search(query)
        except Exception as exc:
            logger.warning("search_datasets failed: %s", exc)
            return []

    def filter_by_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.by_symbol(symbol)
        except Exception as exc:
            logger.warning("filter_by_symbol failed: %s", exc)
            return []

    def filter_by_qualification(self, qualification: str) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.by_qualification(qualification)
        except Exception as exc:
            logger.warning("filter_by_qualification failed: %s", exc)
            return []

    def filter_by_mode(self, mode: str) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.by_mode(mode)
        except Exception as exc:
            logger.warning("filter_by_mode failed: %s", exc)
            return []

    def get_frozen_datasets(self) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.frozen()
        except Exception as exc:
            logger.warning("get_frozen_datasets failed: %s", exc)
            return []

    def get_missing_datasets(self) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.missing()
        except Exception as exc:
            logger.warning("get_missing_datasets failed: %s", exc)
            return []

    def get_corrupted_datasets(self) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.corrupted()
        except Exception as exc:
            logger.warning("get_corrupted_datasets failed: %s", exc)
            return []

    def summary(self) -> Dict[str, Any]:
        datasets = self.get_all_datasets()
        return {
            "total":      len(datasets),
            "research_only": True,
            "no_real_orders": True,
        }
