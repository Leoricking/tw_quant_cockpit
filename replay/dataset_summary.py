"""
replay/dataset_summary.py — ReplayDatasetSummary v1.2.8

Generates text summaries of dataset registry state.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDatasetSummary:
    """
    Text summaries of the dataset registry.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self, registry=None):
        self._registry = registry

    def full_summary(self) -> str:
        if self._registry is None:
            return "Dataset Registry: not initialized."
        datasets = self._registry.list_datasets()
        total    = len(datasets)
        frozen   = sum(1 for d in datasets if d.frozen_at)
        corrupted = sum(1 for d in datasets if d.status == "CORRUPTED")
        missing  = sum(1 for d in datasets if d.status == "MISSING")
        real     = sum(1 for d in datasets if d.mode == "REAL")
        mock     = sum(1 for d in datasets if d.mode == "MOCK")
        dupes    = len(self._registry.detect_duplicates())
        lines = [
            "=" * 60,
            "  Replay Dataset Registry Summary v1.2.8",
            "  [!] Dataset Registry Only | No Real Orders",
            "=" * 60,
            f"  Total datasets:    {total}",
            f"  REAL datasets:     {real}",
            f"  MOCK datasets:     {mock}",
            f"  Frozen:            {frozen}",
            f"  Corrupted:         {corrupted}",
            f"  Missing:           {missing}",
            f"  Possible dupes:    {dupes}",
            "=" * 60,
        ]
        return "\n".join(lines)

    def per_dataset(self, dataset_id: str) -> str:
        if self._registry is None:
            return f"Dataset {dataset_id}: registry not initialized."
        d = self._registry.get_dataset(dataset_id)
        if d is None:
            return f"Dataset {dataset_id}: NOT FOUND."
        return (
            f"Dataset: {d.dataset_id}\n"
            f"  Name:         {d.dataset_name}\n"
            f"  Version:      {d.dataset_version}\n"
            f"  Mode:         {d.mode}\n"
            f"  Qualification:{d.qualification}\n"
            f"  Status:       {d.status}\n"
            f"  Symbols:      {d.symbols}\n"
            f"  Timeframes:   {d.timeframes}\n"
            f"  Files:        {d.file_count}\n"
            f"  Rows:         {d.row_count}\n"
            f"  Frozen:       {d.frozen_at or 'No'}\n"
            f"  Fingerprint:  {d.fingerprint[:16] if d.fingerprint else ''}...\n"
            f"  Warnings:     {d.warnings}"
        )
