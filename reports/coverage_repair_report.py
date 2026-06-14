"""
reports/coverage_repair_report.py — CoverageRepairReportBuilder for TW Quant Cockpit v1.1.2.

Builds Markdown report for a coverage repair session.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] dry_run=True default. Destructive repair disabled.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CoverageRepairReportBuilder:
    """Builds Markdown report for a coverage repair session.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    def __init__(
        self,
        plan=None,
        summary=None,
        mode: str = "real",
        report_dir: str = "reports",
    ) -> None:
        self._plan       = plan
        self._summary    = summary
        self._mode       = mode
        if not os.path.isabs(report_dir):
            self._report_dir = os.path.join(BASE_DIR, report_dir)
        else:
            self._report_dir = report_dir

    def build(self) -> str:
        """Return Markdown string."""
        lines = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines.append("# Coverage Repair Workflow Report v1.1.2")
        lines.append("")
        lines.append(f"> Generated: {now}")
        lines.append(f"> Mode: {self._mode}")
        lines.append("> [!] Research Only. No Real Orders. dry_run=True default.")
        lines.append("> [!] Destructive repair DISABLED. Conflict resolution is MANUAL.")
        lines.append("> [!] Synthetic OHLC repair DISABLED. Invalid OHLC not auto-modified.")
        lines.append("")

        # 一、總覽
        lines.append("## 一、總覽")
        lines.append("")
        try:
            from release.version_info import VERSION
            lines.append(f"- **Version**: {VERSION}")
        except Exception:
            lines.append("- **Version**: 1.1.2")
        lines.append(f"- **Mode**: {self._mode}")

        if self._summary:
            lines.append(f"- **Total Tasks**: {self._summary.total_tasks}")
            lines.append(f"- **Succeeded**: {self._summary.succeeded}")
            lines.append(f"- **Partial**: {self._summary.partial}")
            lines.append(f"- **Failed**: {self._summary.failed}")
            lines.append(f"- **Skipped**: {self._summary.skipped}")
            lines.append(f"- **Blocked**: {self._summary.blocked}")
            lines.append(f"- **Manual Review**: {self._summary.manual_review}")
            lines.append(f"- **Dry Run**: {self._summary.dry_run}")
        elif self._plan:
            lines.append(f"- **Total Tasks**: {self._plan.total_tasks}")
            lines.append(f"- **Dry Run**: {self._plan.dry_run}")
        else:
            lines.append("- **Status**: No plan or summary available")
        lines.append("")

        # 二、Issue Detection Summary
        lines.append("## 二、Issue Detection Summary")
        lines.append("")
        if self._plan:
            lines.append(f"- **Total Issues Detected**: {self._plan.total_issues}")
            lines.append(f"- **Total Tasks**: {self._plan.total_tasks}")
            lines.append("")
            lines.append("### Priority Breakdown")
            lines.append("")
            lines.append("| Priority | Count | Description |")
            lines.append("|----------|-------|-------------|")
            lines.append(f"| P0 | {self._plan.p0_count} | Critical — No data at all |")
            lines.append(f"| P1 | {self._plan.p1_count} | High — Conflicts / Invalid OHLC |")
            lines.append(f"| P2 | {self._plan.p2_count} | Medium — Insufficient / Partial / Stale |")
            lines.append(f"| P3 | {self._plan.p3_count} | Low — Identical duplicates |")
        else:
            lines.append("No issue detection data available.")
        lines.append("")

        # 三、Repair Action Summary
        lines.append("## 三、Repair Action Summary")
        lines.append("")
        if self._plan:
            lines.append("| Action | Count | Note |")
            lines.append("|--------|-------|------|")
            lines.append(f"| AUTO_SAFE | {self._plan.auto_safe_count} | Safe to execute (identical deduplication) |")
            lines.append(f"| MANUAL_REVIEW | {self._plan.manual_review_count} | **Human review required** (conflict) |")
            lines.append(f"| SOURCE_REQUIRED | {self._plan.source_required_count} | Import source data manually |")
            lines.append(f"| BLOCKED | {self._plan.blocked_count} | **Must not auto-modify** (invalid OHLC) |")
        else:
            lines.append("No repair plan available.")
        lines.append("")

        # 四、Task Details
        lines.append("## 四、Task Details")
        lines.append("")
        if self._plan and self._plan.tasks:
            lines.append("| Symbol | Dataset | Issue | Priority | Action |")
            lines.append("|--------|---------|-------|----------|--------|")
            for task in self._plan.tasks[:30]:
                lines.append(
                    f"| {task.symbol} | {task.dataset} | {task.issue_type} "
                    f"| {task.priority} | {task.action} |"
                )
            if len(self._plan.tasks) > 30:
                lines.append(f"| ... ({len(self._plan.tasks) - 30} more) | | | | |")
        else:
            lines.append("No tasks available.")
        lines.append("")

        # 五、Execution Results
        lines.append("## 五、Execution Results")
        lines.append("")
        if self._summary and self._summary.results:
            lines.append("| Symbol | Dataset | Issue | Status | Rows Before | Rows After | Removed |")
            lines.append("|--------|---------|-------|--------|-------------|------------|---------|")
            for r in self._summary.results[:30]:
                lines.append(
                    f"| {r.symbol} | {r.dataset} | {r.issue_type} | {r.status} "
                    f"| {r.rows_before} | {r.rows_after} | {r.rows_removed} |"
                )
        elif self._plan and self._plan.dry_run:
            lines.append("Dry run — no data was modified.")
        else:
            lines.append("No execution results available.")
        lines.append("")

        # 六、Manual Review Required
        lines.append("## 六、Manual Review Required")
        lines.append("")
        if self._plan:
            from coverage_repair.coverage_repair_schema import ACTION_MANUAL_REVIEW
            manual_tasks = [t for t in self._plan.tasks if t.action == ACTION_MANUAL_REVIEW]
            if manual_tasks:
                lines.append(f"**{len(manual_tasks)} task(s) require manual review:**")
                lines.append("")
                for t in manual_tasks[:20]:
                    lines.append(
                        f"- `{t.symbol}/{t.dataset}` — {t.issue_type} "
                        f"| Affected dates: {len(t.affected_dates)}"
                    )
                lines.append("")
                lines.append("> [!] Conflict resolution is MANUAL. No auto-overwrite ever.")
            else:
                lines.append("No tasks require manual review.")
        else:
            lines.append("No plan available.")
        lines.append("")

        # 七、Source Data Required
        lines.append("## 七、Source Data Required")
        lines.append("")
        if self._plan:
            from coverage_repair.coverage_repair_schema import ACTION_SOURCE_REQUIRED
            source_tasks = [t for t in self._plan.tasks if t.action == ACTION_SOURCE_REQUIRED]
            if source_tasks:
                lines.append(f"**{len(source_tasks)} task(s) require source data import:**")
                lines.append("")
                for t in source_tasks[:20]:
                    lines.append(f"- `{t.symbol}/{t.dataset}` — {t.issue_type}")
                lines.append("")
                lines.append(
                    "Use `python main.py import-batch --path <data_dir>` "
                    "to import missing data."
                )
            else:
                lines.append("No tasks require source data import.")
        else:
            lines.append("No plan available.")
        lines.append("")

        # 八、Universe Coverage After Repair
        lines.append("## 八、Universe Coverage After Repair")
        lines.append("")
        try:
            from universe.universe_coverage_analyzer import UniverseCoverageAnalyzer
            analyzer = UniverseCoverageAnalyzer()
            cov = analyzer.analyze()
            if isinstance(cov, dict):
                lines.append("- Coverage data refreshed.")
                if "coverage_pct" in cov:
                    lines.append(f"- Coverage: {cov.get('coverage_pct', 'N/A')}%")
            else:
                lines.append("- Coverage refresh attempted.")
        except Exception as exc:
            lines.append(f"- Coverage refresh unavailable: {exc}")
        lines.append("")

        # 九、Data Onboarding Integrity
        lines.append("## 九、Data Onboarding Integrity (v1.1.1)")
        lines.append("")
        try:
            from data_onboarding.onboarding_health import OnboardingHealthCheck
            checker = OnboardingHealthCheck()
            result = checker.run()
            lines.append(f"- Onboarding Health: **{result['overall']}** "
                         f"({result['passed']}/{result['total']} PASS)")
        except Exception as exc:
            lines.append(f"- Onboarding health check unavailable: {exc}")
        lines.append("")

        # 十、Safety Declaration
        lines.append("## 十、Safety Declaration")
        lines.append("")
        lines.append("| Safety Flag | Value |")
        lines.append("|-------------|-------|")
        lines.append("| Research Only | True |")
        lines.append("| No Real Orders | True |")
        lines.append("| Dry Run Default | True |")
        lines.append("| Destructive Repair Disabled | True |")
        lines.append("| Conflict Auto-Overwrite Enabled | False |")
        lines.append("| Synthetic OHLC Repair Disabled | True |")
        lines.append("| Invalid OHLC Auto-Modify Disabled | True |")
        lines.append("| Mock Data Repair Disabled | True |")
        lines.append("| Broker Execution | DISABLED |")
        lines.append("| Production Trading | BLOCKED |")
        lines.append("")
        lines.append(
            "> [!] This report is for research purposes only. "
            "No investment advice. Not for production trading."
        )
        lines.append("")

        return "\n".join(lines)

    def save(self) -> str:
        """Save to reports/coverage_repair_report_YYYY-MM-DD.md. Return path."""
        os.makedirs(self._report_dir, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        path = os.path.join(self._report_dir, f"coverage_repair_report_{date_str}.md")
        content = self.build()
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("Saved coverage repair report to %s", path)
        return path
