"""
reports/data_import_onboarding_report.py — DataImportOnboardingReportBuilder for TW Quant Cockpit v1.1.1.

Builds Markdown report for a batch onboarding session.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] dry_run=True by default. Destructive import disabled.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataImportOnboardingReportBuilder:
    """Builds Markdown report for a batch onboarding session.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    def __init__(
        self,
        plan=None,
        summary=None,
        tier: Optional[str] = None,
        mode: str = "real",
        report_dir: str = "reports",
    ) -> None:
        self._plan       = plan
        self._summary    = summary
        self._tier       = tier or "research30"
        self._mode       = mode
        if not os.path.isabs(report_dir):
            self._report_dir = os.path.join(BASE_DIR, report_dir)
        else:
            self._report_dir = report_dir

    def build(self) -> str:
        """Return Markdown string."""
        lines = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines.append("# Data Import & Batch Onboarding Report v1.1.1")
        lines.append("")
        lines.append(f"> Generated: {now}")
        lines.append(f"> Mode: {self._mode} | Tier: {self._tier}")
        lines.append("> [!] Research Only. No Real Orders. dry_run=True default.")
        lines.append("> [!] Destructive import (REPLACE_EXPLICIT) is DISABLED by default.")
        lines.append("")

        # 一、總覽
        lines.append("## 一、總覽")
        lines.append("")
        try:
            from release.version_info import VERSION
            lines.append(f"- **Version**: {VERSION}")
        except Exception:
            lines.append("- **Version**: 1.1.1")
        lines.append(f"- **Tier**: {self._tier}")
        lines.append(f"- **Mode**: {self._mode}")

        if self._summary:
            lines.append(f"- **Total Files**: {self._summary.total_files}")
            lines.append(f"- **Succeeded**: {self._summary.succeeded}")
            lines.append(f"- **Partial**: {self._summary.partial}")
            lines.append(f"- **Failed**: {self._summary.failed}")
            lines.append(f"- **Skipped**: {self._summary.skipped}")
            lines.append(f"- **Blocked**: {self._summary.blocked}")
            lines.append(f"- **Dry Run**: {self._summary.dry_run}")
        elif self._plan:
            lines.append(f"- **Total Files**: {self._plan.total_files}")
            lines.append(f"- **Dry Run**: {self._plan.dry_run}")
        else:
            lines.append("- **Status**: No plan or summary available")
        lines.append("")

        # 二、Discovered Files
        lines.append("## 二、Discovered Files")
        lines.append("")
        if self._plan and self._plan.items:
            from collections import Counter
            type_counts = Counter(i.file_type for i in self._plan.items)
            lines.append("| File Type | Count |")
            lines.append("|-----------|-------|")
            for ft, cnt in sorted(type_counts.items()):
                lines.append(f"| {ft} | {cnt} |")
        else:
            lines.append("No files discovered.")
        lines.append("")

        # 三、Validation Summary
        lines.append("## 三、Validation Summary")
        lines.append("")
        if self._plan and self._plan.items:
            from collections import Counter
            status_counts = Counter(i.validation_status for i in self._plan.items)
            lines.append("| Status | Count |")
            lines.append("|--------|-------|")
            for st, cnt in sorted(status_counts.items()):
                lines.append(f"| {st} | {cnt} |")
        else:
            lines.append("No validation data available.")
        lines.append("")

        # 四、Import Plan
        lines.append("## 四、Import Plan")
        lines.append("")
        if self._plan and self._plan.items:
            lines.append(f"- MERGE_SAFE: {self._plan.merge_safe_count}")
            lines.append(f"- APPEND_SAFE: {self._plan.append_safe_count}")
            lines.append(f"- REPLACE_EXPLICIT: {self._plan.replace_explicit_count} (**BLOCKED by default**)")
            lines.append(f"- BLOCKED: {self._plan.blocked_count}")
            lines.append(f"- REVIEW: {self._plan.review_count}")
            lines.append(f"- SKIP: {self._plan.skip_count}")
            lines.append("")
            lines.append("| File | Symbol | Dataset | Action | Mode |")
            lines.append("|------|--------|---------|--------|------|")
            for item in self._plan.items[:20]:
                fn = os.path.basename(item.file_path)
                lines.append(f"| {fn} | {item.symbol or '-'} | {item.dataset} | {item.action} | {item.import_mode} |")
            if len(self._plan.items) > 20:
                lines.append(f"| ... ({len(self._plan.items) - 20} more) | | | | |")
        else:
            lines.append("No import plan available.")
        lines.append("")

        # 五、Execution Results
        lines.append("## 五、Execution Results")
        lines.append("")
        if self._summary and self._summary.results:
            lines.append("| File | Symbol | Status | Rows Imported | Rows Skipped |")
            lines.append("|------|--------|--------|---------------|--------------|")
            for r in self._summary.results[:20]:
                fn = os.path.basename(r.file_path)
                lines.append(f"| {fn} | {r.symbol or '-'} | {r.status} | {r.rows_imported} | {r.rows_skipped} |")
        elif self._plan and self._plan.dry_run:
            lines.append("Dry run — no files were written.")
        else:
            lines.append("No execution results available.")
        lines.append("")

        # 六、Conflicts & Review Required
        lines.append("## 六、Conflicts & Review Required")
        lines.append("")
        if self._plan:
            review_items = [i for i in self._plan.items if i.action == "REVIEW"]
            if review_items:
                lines.append(f"**{len(review_items)} file(s) require manual review before import:**")
                for item in review_items:
                    fn = os.path.basename(item.file_path)
                    lines.append(f"- `{fn}` | Symbol: {item.symbol or '-'} | Conflicts: {item.expected_conflict_rows}")
                lines.append("")
                lines.append("> [!] Conflict resolution is MANUAL. No auto-overwrite.")
            else:
                lines.append("No conflicts requiring review.")
        else:
            lines.append("No plan available.")
        lines.append("")

        # 七、Failed Files & Retry Manifest
        lines.append("## 七、Failed Files & Retry Manifest")
        lines.append("")
        if self._summary:
            failed = [r for r in self._summary.results if r.status == "FAILED"]
            if failed:
                lines.append(f"**{len(failed)} file(s) failed:**")
                for r in failed:
                    fn = os.path.basename(r.file_path)
                    err = r.errors[0] if r.errors else "unknown error"
                    lines.append(f"- `{fn}`: {err}")
                lines.append("")
                lines.append("Run `python main.py import-retry-manifest` to build retry plan.")
            else:
                lines.append("No failed imports.")
        else:
            lines.append("No summary available.")
        lines.append("")

        # 八、Universe Coverage After Import
        lines.append("## 八、Universe Coverage After Import")
        lines.append("")
        try:
            from universe.universe_coverage_analyzer import UniverseCoverageAnalyzer
            analyzer = UniverseCoverageAnalyzer()
            cov = analyzer.analyze()
            if isinstance(cov, dict):
                lines.append(f"- Coverage data refreshed after import.")
                if "coverage_pct" in cov:
                    lines.append(f"- Coverage: {cov.get('coverage_pct', 'N/A')}%")
            else:
                lines.append("- Coverage refresh attempted.")
        except Exception as exc:
            lines.append(f"- Coverage refresh unavailable: {exc}")
        lines.append("")

        # 九、Safety Declaration
        lines.append("## 九、Safety Declaration")
        lines.append("")
        lines.append("| Safety Flag | Value |")
        lines.append("|-------------|-------|")
        lines.append("| Research Only | True |")
        lines.append("| No Real Orders | True |")
        lines.append("| Dry Run Default | True |")
        lines.append("| Destructive Import Disabled | True |")
        lines.append("| REPLACE_EXPLICIT Blocked by Default | True |")
        lines.append("| Conflict Auto-Overwrite Enabled | False |")
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
        """Save to reports/data_import_onboarding_report_YYYY-MM-DD.md. Return path."""
        os.makedirs(self._report_dir, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        path = os.path.join(self._report_dir, f"data_import_onboarding_report_{date_str}.md")
        content = self.build()
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("Saved data import onboarding report to %s", path)
        return path
