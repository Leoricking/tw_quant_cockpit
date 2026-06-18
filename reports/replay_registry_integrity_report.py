"""
reports/replay_registry_integrity_report.py — Registry Integrity report v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def build_registry_integrity_report(
    dataset_registry=None,
    session_registry=None,
    date: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a registry integrity markdown report."""
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    markdown_lines = [
        f"# Registry Integrity Report — {date}",
        "",
        "[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.",
        "",
    ]

    try:
        if dataset_registry is None:
            from replay.dataset_registry import ReplayDatasetRegistry
            dataset_registry = ReplayDatasetRegistry()
        if session_registry is None:
            from replay.session_registry_v128 import ReplaySessionRegistryV128
            session_registry = ReplaySessionRegistryV128()

        from replay.dataset_integrity import ReplayDatasetIntegrityChecker
        from replay.registry_repair import ReplayRegistryRepairPlanner

        checker = ReplayDatasetIntegrityChecker()
        planner = ReplayRegistryRepairPlanner()

        datasets   = dataset_registry.list_datasets()
        missing    = dataset_registry.detect_missing()
        corrupted  = dataset_registry.detect_corrupted()
        stale      = dataset_registry.detect_stale()
        duplicates = dataset_registry.detect_duplicates()
        orphans    = session_registry.detect_orphans()
        broken     = session_registry.detect_broken_references()

        repair_preview = planner.preview(dataset_registry, session_registry)

        markdown_lines += [
            "## Dataset Integrity",
            "",
            f"- Total datasets: {len(datasets)}",
            f"- Missing files: {len(missing)}",
            f"- Corrupted: {len(corrupted)}",
            f"- Stale hash: {len(stale)}",
            f"- Duplicates: {len(duplicates)}",
            "",
            "## Session Integrity",
            "",
            f"- Orphaned sessions: {len(orphans)}",
            f"- Broken references: {len(broken)}",
            "",
            "## Repair Plan",
            "",
            f"- Issues found: {repair_preview.get('issues_found', 0)}",
            f"- Safe repairs: {repair_preview.get('safe_count', 0)}",
            f"- Blocked repairs: {repair_preview.get('blocked_count', 0)}",
            "",
        ]

        if missing:
            markdown_lines.append("### Missing Datasets")
            for d in missing:
                did = getattr(d, "dataset_id", None) or (d.get("dataset_id") if isinstance(d, dict) else str(d))
                markdown_lines.append(f"- {did}")
            markdown_lines.append("")

        if corrupted:
            markdown_lines.append("### Corrupted Datasets")
            for d in corrupted:
                did = getattr(d, "dataset_id", None) or (d.get("dataset_id") if isinstance(d, dict) else str(d))
                markdown_lines.append(f"- {did}")
            markdown_lines.append("")

    except Exception as exc:
        logger.warning("build_registry_integrity_report failed: %s", exc)
        markdown_lines.append(f"Report generation failed: {exc}")

    return {
        "report_type":   "REGISTRY_INTEGRITY_REPORT",
        "report_date":   date,
        "markdown":      "\n".join(markdown_lines),
        "research_only": True,
        "no_real_orders": True,
        "version":       "1.2.8",
    }
