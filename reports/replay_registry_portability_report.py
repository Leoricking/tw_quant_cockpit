"""
reports/replay_registry_portability_report.py — Registry Portability report v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
[!] RELATIVE_ONLY path mode. No secrets, no broker credentials, no absolute paths.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def build_registry_portability_report(
    dataset_registry=None,
    date: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a registry portability markdown report."""
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    markdown_lines = [
        f"# Registry Portability Report — {date}",
        "",
        "[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.",
        "[!] RELATIVE_ONLY path mode. No secrets, no broker credentials.",
        "",
    ]

    try:
        if dataset_registry is None:
            from replay.dataset_registry import ReplayDatasetRegistry
            dataset_registry = ReplayDatasetRegistry()

        from replay.dataset_portability import ReplayDatasetPortability
        from replay.dataset_package import ReplayDatasetPackage

        portability = ReplayDatasetPortability()
        package_builder = ReplayDatasetPackage()
        datasets = dataset_registry.list_datasets()

        safe_count    = 0
        unsafe_count  = 0
        abs_path_count = 0
        secret_count  = 0
        issues: List[str] = []

        for d in datasets:
            did = getattr(d, "dataset_id", None) or (d.get("dataset_id") if isinstance(d, dict) else str(d))
            try:
                scan = portability.scan_for_secrets(d)
                abs_scan = portability.scan_for_absolute_paths(d)
                if scan.get("found") or abs_scan.get("found"):
                    unsafe_count += 1
                    if scan.get("found"):
                        secret_count += 1
                        issues.append(f"{did}: SECRET detected")
                    if abs_scan.get("found"):
                        abs_path_count += 1
                        issues.append(f"{did}: ABSOLUTE PATH detected")
                else:
                    safe_count += 1
            except Exception as exc:
                logger.warning("portability scan failed for %s: %s", did, exc)
                issues.append(f"{did}: scan failed — {exc}")

        markdown_lines += [
            "## Portability Summary",
            "",
            f"- Total datasets: {len(datasets)}",
            f"- Portable (safe): {safe_count}",
            f"- Unsafe (secrets or absolute paths): {unsafe_count}",
            f"- Secret detections: {secret_count}",
            f"- Absolute path detections: {abs_path_count}",
            "",
        ]

        if issues:
            markdown_lines.append("## Issues")
            markdown_lines.append("")
            for issue in issues:
                markdown_lines.append(f"- {issue}")
            markdown_lines.append("")
        else:
            markdown_lines.append("All datasets passed portability checks.")
            markdown_lines.append("")

    except Exception as exc:
        logger.warning("build_registry_portability_report failed: %s", exc)
        markdown_lines.append(f"Report generation failed: {exc}")

    return {
        "report_type":   "REGISTRY_PORTABILITY_REPORT",
        "report_date":   date,
        "markdown":      "\n".join(markdown_lines),
        "research_only": True,
        "no_real_orders": True,
        "version":       "1.2.8",
    }
