"""
replay/dataset_catalog.py — ReplayDatasetCatalog v1.2.8

Thin presentation layer over the dataset registry.
Provides catalog-style views (tabular, summary) of registered datasets.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDatasetCatalog:
    """
    Catalog view over the dataset registry.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self, registry=None):
        self._registry = registry

    def list_catalog(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Return catalog rows for all datasets."""
        if self._registry is None:
            return []
        datasets = self._registry.list_datasets(filters)
        rows = []
        for d in datasets:
            rows.append({
                "dataset_id":    d.dataset_id,
                "name":          d.dataset_name,
                "version":       d.dataset_version,
                "mode":          d.mode,
                "qualification": d.qualification,
                "symbols":       d.symbols,
                "timeframes":    d.timeframes,
                "start":         d.start_timestamp[:10] if d.start_timestamp else "",
                "end":           d.end_timestamp[:10] if d.end_timestamp else "",
                "rows":          d.row_count,
                "files":         d.file_count,
                "fingerprint":   d.fingerprint[:12] + "..." if d.fingerprint else "",
                "frozen":        d.frozen_at is not None,
                "status":        d.status,
                "warnings":      len(d.warnings),
            })
        return rows

    def summary(self) -> str:
        rows = self.list_catalog()
        if not rows:
            return "Dataset Catalog: empty."
        lines = [f"Dataset Catalog: {len(rows)} dataset(s)"]
        for r in rows:
            frozen = "[F]" if r["frozen"] else "   "
            lines.append(
                f"  {frozen} {r['dataset_id']:20s} v{r['version']:8s} "
                f"{r['mode']:4s} {r['qualification']:18s} "
                f"files={r['files']} rows={r['rows']}"
            )
        return "\n".join(lines)
