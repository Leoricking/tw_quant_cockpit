"""
reports/research_run_registry_report.py — ResearchRunRegistryReportBuilder v1.1.8

Builds Markdown report for the research run registry.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Registry does NOT execute research commands. No Auto Rerun. No Trading.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchRunRegistryReportBuilder:
    """
    Builds a Markdown report for the research run registry.

    [!] Research Only. No Real Orders.
    Output: reports/research_run_registry_report_YYYY-MM-DD.md
    """

    no_real_orders = True
    research_only = True

    def build(self, output_dir: str = "reports") -> str:
        """Build the registry report and return the output path."""
        try:
            date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            abs_output_dir = output_dir if os.path.isabs(output_dir) else os.path.join(BASE_DIR, output_dir)
            os.makedirs(abs_output_dir, exist_ok=True)
            output_path = os.path.join(abs_output_dir, f"research_run_registry_report_{date_str}.md")

            from research_registry.registry_query import RegistryQuery
            q = RegistryQuery()
            summary = q.registry_summary()
            latest = q.latest_runs(limit=10)
            formal = q.list_by_qualification("FORMALLY_QUALIFIED")[:5]
            observational = q.list_by_qualification("OBSERVATIONAL_ONLY")[:5]
            blocked = q.list_blocked()[:5]
            failed = q.list_failed()[:5]
            duplicates = q.list_duplicates()[:5]
            missing_arts = q.list_missing_artifacts()[:5]

            lines = self._render(
                date_str=date_str,
                summary=summary,
                latest=latest,
                formal=formal,
                observational=observational,
                blocked=blocked,
                failed=failed,
                duplicates=duplicates,
                missing_arts=missing_arts,
                query=q,
            )

            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

            logger.info("ResearchRunRegistryReportBuilder: written to %s", output_path)
            return output_path

        except Exception as exc:
            logger.warning("ResearchRunRegistryReportBuilder.build failed: %s", exc)
            return ""

    def _render(self, date_str, summary, latest, formal, observational,
                blocked, failed, duplicates, missing_arts, query) -> List[str]:
        lines = []

        lines += [
            "# Research Run Registry Report v1.1.8",
            "",
            f"**Generated:** {date_str}",
            "",
            "[!] Research Only. No Real Orders. Production Trading: BLOCKED.",
            "[!] Registry does NOT execute research commands.",
            "[!] Auto Rerun DISABLED. Broker DISABLED. Trading DISABLED.",
            "",
        ]

        # Executive Summary
        lines += [
            "## Executive Summary",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Runs | {summary.total_runs} |",
            f"| Completed | {summary.completed_runs} |",
            f"| With Warnings | {summary.warning_runs} |",
            f"| Blocked | {summary.blocked_runs} |",
            f"| Failed | {summary.failed_runs} |",
            f"| Formally Qualified | {summary.formal_runs} |",
            f"| Observational Only | {summary.observational_runs} |",
            f"| Demo Only | {summary.demo_runs} |",
            f"| Duplicates | {summary.duplicate_runs} |",
            f"| Missing Artifact Runs | {summary.missing_artifact_runs} |",
            f"| Reproducibility Verified | {summary.reproducibility_verified_runs} |",
            "",
        ]

        # Latest Runs
        lines += ["## Latest Runs", ""]
        if latest:
            lines += [
                "| Run ID | Command | Type | Status | Qualification | Version | Started |",
                "|--------|---------|------|--------|---------------|---------|---------|",
            ]
            for r in latest:
                lines.append(
                    f"| {r.run_id[:12]}... | {r.command_name} | {r.run_type} | "
                    f"{r.status} | {r.qualification} | {r.code_version} | {r.started_at[:19] if r.started_at else ''} |"
                )
        else:
            lines.append("_No runs recorded yet._")
        lines.append("")

        # Formal Runs
        lines += ["## Formal Runs", ""]
        if formal:
            lines += [
                "| Run ID | Command | Status | Version | Commit | Started |",
                "|--------|---------|--------|---------|--------|---------|",
            ]
            for r in formal:
                lines.append(
                    f"| {r.run_id[:12]}... | {r.command_name} | {r.status} | "
                    f"{r.code_version} | {r.git_commit} | {r.started_at[:19] if r.started_at else ''} |"
                )
        else:
            lines.append("_No formally qualified runs recorded yet._")
        lines.append("")

        # Observational Runs
        lines += ["## Observational Runs", ""]
        if observational:
            lines += [
                "| Run ID | Command | Status | Started |",
                "|--------|---------|--------|---------|",
            ]
            for r in observational[:5]:
                lines.append(
                    f"| {r.run_id[:12]}... | {r.command_name} | {r.status} | "
                    f"{r.started_at[:19] if r.started_at else ''} |"
                )
        else:
            lines.append("_No observational runs recorded yet._")
        lines.append("")

        # Blocked/Failed
        lines += ["## Blocked / Failed Runs", ""]
        all_issues = list(blocked) + list(failed)
        if all_issues:
            lines += [
                "| Run ID | Command | Status | Reason Codes |",
                "|--------|---------|--------|--------------|",
            ]
            for r in all_issues[:10]:
                rc = ", ".join(r.blocked_reason_codes) if r.blocked_reason_codes else "—"
                lines.append(f"| {r.run_id[:12]}... | {r.command_name} | {r.status} | {rc} |")
        else:
            lines.append("_No blocked or failed runs._")
        lines.append("")

        # Lineage
        lines += ["## Run Lineage", ""]
        lines.append("_See `research-run-lineage <run_id>` for detailed lineage trees._")
        lines.append("")

        # Duplicates
        lines += ["## Duplicate Runs", ""]
        if duplicates:
            lines += [
                "| Run ID | Command | Duplicate Of |",
                "|--------|---------|-------------|",
            ]
            for r in duplicates:
                lines.append(f"| {r.run_id[:12]}... | {r.command_name} | {r.duplicate_of[:12] if r.duplicate_of else ''}... |")
        else:
            lines.append("_No duplicate runs detected._")
        lines.append("")

        # Artifacts
        lines += ["## Artifacts", ""]
        if missing_arts:
            lines.append(f"**Missing Artifact Runs:** {len(missing_arts)}")
            lines += [
                "",
                "| Run ID | Command | Status |",
                "|--------|---------|--------|",
            ]
            for r in missing_arts:
                lines.append(f"| {r.run_id[:12]}... | {r.command_name} | {r.status} |")
        else:
            lines.append("_No missing artifacts detected._")
        lines.append("")

        # Reproducibility
        lines += ["## Reproducibility", ""]
        lines.append(f"Runs with reproducibility hash: **{summary.reproducibility_verified_runs}**")
        lines.append("")
        lines.append("_Reproducibility hash is computed during gate enforcement runs._")
        lines.append("")

        # Recent Comparisons
        lines += ["## Recent Comparisons", ""]
        try:
            comps = query._store.list_comparisons()[-5:]
            if comps:
                lines += [
                    "| Comparison ID | Run A | Run B | Comparable | Hash Match |",
                    "|--------------|-------|-------|------------|------------|",
                ]
                for c in comps:
                    lines.append(
                        f"| {c.get('comparison_id', '')[:12]}... | "
                        f"{c.get('run_a', '')[:12]} | {c.get('run_b', '')[:12]} | "
                        f"{c.get('comparable', '')} | {c.get('hash_match', '')} |"
                    )
            else:
                lines.append("_No comparisons recorded yet._")
        except Exception:
            lines.append("_Comparisons unavailable._")
        lines.append("")

        # Safety Statement
        lines += [
            "## 安全聲明 (Safety Statement)",
            "",
            "- **[!] Research Only (僅供研究)** — 本系統不執行真實交易。",
            "- **[!] No Real Orders (無真實委託)** — 不連接券商，不下委託單。",
            "- **[!] Registry Does Not Execute Runs** — 本登錄系統不執行研究指令。",
            "- **[!] Auto Rerun DISABLED** — 不自動重跑研究。",
            "- **[!] Broker DISABLED** — 無券商連線。",
            "- **[!] Trading DISABLED** — 生產交易永久封鎖。",
            "",
        ]

        return lines
