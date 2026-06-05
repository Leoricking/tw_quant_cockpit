"""
reports/data_coverage_report.py — DataCoverageReport for TW Quant Cockpit v0.6.2.

Generates a comprehensive Markdown report of data coverage across all domains.

[!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from collections import defaultdict
from datetime import datetime
from typing import List, Optional

from data_coverage.data_coverage_engine import DataCoverageEngine
from data_coverage.data_coverage_store import DataCoverageStore
from data_coverage.data_coverage_schema import (
    DataCoverageItem, DataCoverageSummary,
    STATUS_READY, STATUS_PARTIAL, STATUS_MISSING_REQUIRED,
    STATUS_MISSING_OPTIONAL, STATUS_ENV_LIMITED, STATUS_NOT_GENERATED,
    STATUS_STALE, STATUS_FAILED,
)

logger = logging.getLogger(__name__)

_SAFETY_BANNER = (
    "[!] Data Coverage Only | Research Only | No Real Orders | Production BLOCKED"
)


class DataCoverageReport:
    """Generates a Markdown report of data coverage gaps and status.

    [!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        project_root: str = ".",
        output_dir: str = "data/backtest_results/data_coverage",
        report_dir: str = "reports",
    ) -> None:
        self.project_root = project_root
        self.output_dir   = output_dir
        self.report_dir   = report_dir
        os.makedirs(self.report_dir, exist_ok=True)

    def run(self, mode: str = "real") -> str:
        """Run engine, save store outputs, generate markdown report. Returns report path."""
        engine  = DataCoverageEngine(project_root=self.project_root, output_dir=self.output_dir)
        items, summary = engine.run(mode=mode)

        store = DataCoverageStore(output_dir=self.output_dir)
        store.save_items(items)
        store.save_summary(summary)
        store.save_matrix(items)

        report_date = datetime.now().strftime("%Y-%m-%d")
        md = self._build_markdown(items, summary, report_date)

        report_path = os.path.join(self.report_dir, f"data_coverage_report_{report_date}.md")
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(md)
            logger.info("Data coverage report saved to %s", report_path)
        except Exception as exc:
            logger.warning("Failed to write report: %s", exc)

        return report_path

    def _build_markdown(
        self,
        items: List[DataCoverageItem],
        summary: DataCoverageSummary,
        report_date: str,
    ) -> str:
        lines: List[str] = []

        # Header
        lines.append(f"# TW Quant Cockpit — Data Coverage Report")
        lines.append(f"")
        lines.append(f"> **{_SAFETY_BANNER}**")
        lines.append(f"")
        lines.append(f"**Report Date:** {report_date}  ")
        lines.append(f"**Generated At:** {summary.generated_at}  ")
        lines.append(f"**Mode:** {summary.mode}  ")
        lines.append(f"")

        # 總覽 (Overview)
        lines.append("## 總覽 (Overview)")
        lines.append("")
        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Total Items | {summary.total_items} |")
        lines.append(f"| Ready | {summary.ready_count} |")
        lines.append(f"| Partial | {summary.partial_count} |")
        lines.append(f"| ENV Limited | {summary.env_limited_count} |")
        lines.append(f"| Not Generated | {summary.not_generated_count} |")
        lines.append(f"| Missing Required | {summary.missing_required_count} |")
        lines.append(f"| Missing Optional | {summary.missing_optional_count} |")
        lines.append(f"| Failed | {summary.failed_count} |")
        lines.append(f"| Coverage Score | {summary.coverage_score:.1f} / 100 |")
        lines.append(f"| Overall Status | **{summary.overall_status}** |")
        lines.append("")

        # Blockers
        if summary.blockers:
            lines.append("## Blockers (Missing Required)")
            lines.append("")
            for b in summary.blockers:
                lines.append(f"- {b}")
            lines.append("")

        # Coverage Matrix
        lines.append("## Coverage Matrix")
        lines.append("")
        lines.append("| Domain | Item | Status | Required | Suggested Command |")
        lines.append("|--------|------|--------|----------|-------------------|")
        for item in sorted(items, key=lambda x: (x.domain, x.item_id)):
            req_str = "Required" if item.required else "Optional"
            cmd = item.suggested_command or "—"
            lines.append(
                f"| {item.domain} | {item.dataset_name} | `{item.status}` | {req_str} | `{cmd}` |"
            )
        lines.append("")

        # Domain breakdowns
        by_domain: dict = defaultdict(list)
        for item in items:
            by_domain[item.domain].append(item)

        # Provider Coverage
        lines.append("## Provider Coverage")
        lines.append("")
        self._render_domain_table(lines, by_domain.get("provider", []))

        # Daily Data / Intraday
        lines.append("## Daily Data Coverage")
        lines.append("")
        self._render_domain_table(lines, by_domain.get("daily_data", []))

        lines.append("## Intraday / Replay Coverage")
        lines.append("")
        self._render_domain_table(lines, by_domain.get("intraday", []))
        self._render_domain_table(lines, by_domain.get("replay", []))

        # Feature Store
        lines.append("## Feature Store Coverage")
        lines.append("")
        self._render_domain_table(lines, by_domain.get("feature_store", []))

        # Report Pack Gaps
        lines.append("## Report Pack Coverage")
        lines.append("")
        self._render_domain_table(lines, by_domain.get("report_pack", []))

        # Next Data Actions
        lines.append("## Next Data Actions")
        lines.append("")
        gaps = [
            i for i in items
            if i.status in (STATUS_MISSING_REQUIRED, STATUS_FAILED)
        ]
        optionals = [
            i for i in items
            if i.status in (STATUS_MISSING_OPTIONAL, STATUS_NOT_GENERATED, STATUS_ENV_LIMITED)
        ]
        if gaps:
            lines.append("### Required Gaps (Action Needed)")
            lines.append("")
            for item in gaps:
                lines.append(f"- **{item.domain}/{item.item_id}**: `{item.suggested_command}`")
            lines.append("")
        if optionals:
            lines.append("### Optional Gaps")
            lines.append("")
            for item in optionals:
                lines.append(f"- {item.domain}/{item.item_id} [{item.status}]: `{item.suggested_command}`")
            lines.append("")

        # 安全聲明
        lines.append("## 安全聲明 (Safety Declaration)")
        lines.append("")
        lines.append("```")
        lines.append(_SAFETY_BANNER)
        lines.append("This report is for data coverage auditing and research gap tracking only.")
        lines.append("No real orders are placed. No broker connections are made.")
        lines.append("Production trading is BLOCKED.")
        lines.append("```")
        lines.append("")

        return "\n".join(lines)

    def _render_domain_table(self, lines: List[str], domain_items: List[DataCoverageItem]) -> None:
        if not domain_items:
            return
        lines.append("| Item | Status | Required | Last Updated | Suggested Command |")
        lines.append("|------|--------|----------|--------------|-------------------|")
        for item in domain_items:
            req_str = "Y" if item.required else "N"
            updated = item.last_updated or "—"
            cmd = item.suggested_command or "—"
            lines.append(
                f"| {item.dataset_name} | `{item.status}` | {req_str} | {updated} | `{cmd}` |"
            )
        lines.append("")
