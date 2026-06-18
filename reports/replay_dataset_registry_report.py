"""
reports/replay_dataset_registry_report.py — Dataset Registry report v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def build_dataset_registry_report(
    dataset_registry=None,
    date: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a dataset registry markdown report."""
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    try:
        if dataset_registry is None:
            from replay.dataset_registry import ReplayDatasetRegistry
            dataset_registry = ReplayDatasetRegistry()
        from replay.dataset_report import ReplayDatasetReport
        report_obj = ReplayDatasetReport(dataset_registry)
        markdown = report_obj.full_report()
    except Exception as exc:
        logger.warning("build_dataset_registry_report failed: %s", exc)
        markdown = f"# Dataset Registry Report\n\nReport generation failed: {exc}\n"

    return {
        "report_type":   "DATASET_REGISTRY_REPORT",
        "report_date":   date,
        "markdown":      markdown,
        "research_only": True,
        "no_real_orders": True,
        "version":       "1.2.8",
    }


def build_dataset_summary(dataset_registry=None) -> Dict[str, Any]:
    """Build a concise dataset summary dict."""
    try:
        if dataset_registry is None:
            from replay.dataset_registry import ReplayDatasetRegistry
            dataset_registry = ReplayDatasetRegistry()
        from replay.dataset_summary import ReplayDatasetSummary
        return ReplayDatasetSummary().full_summary(dataset_registry)
    except Exception as exc:
        logger.warning("build_dataset_summary failed: %s", exc)
        return {"error": str(exc), "research_only": True}


def get_dataset_rows(dataset_registry=None) -> List[Dict[str, Any]]:
    """Return list of dataset dicts for table display."""
    try:
        if dataset_registry is None:
            from replay.dataset_registry import ReplayDatasetRegistry
            dataset_registry = ReplayDatasetRegistry()
        datasets = dataset_registry.list_datasets()
        return [vars(d) if hasattr(d, "__dict__") else d for d in datasets]
    except Exception as exc:
        logger.warning("get_dataset_rows failed: %s", exc)
        return []
