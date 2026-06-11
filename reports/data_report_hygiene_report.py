"""
reports/data_report_hygiene_report.py — DataReportHygieneReportBuilder for v1.0.2.

Generates the Data & Report Hygiene review report as a Markdown file.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Data Cleanup is Review Only. Archive Suggestions Only.
[!] No automatic deletion. No automatic archive. No file moves.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataReportHygieneReportBuilder:
    """Generate v1.0.2 Data & Report Hygiene Markdown report.

    [!] Research Only. No Real Orders. Data Cleanup Review Only.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    review_only        = True
    data_cleanup_review_only  = True
    archive_suggestions_only  = True

    def build(
        self,
        mode: str = "real",
        project_root: str = ".",
        report_dir: str = "reports",
        output_dir: str = "data/backtest_results/maintenance",
    ) -> str:
        """Build the report. Returns path to generated Markdown file."""
        from maintenance.data_report_hygiene_engine import DataReportHygieneEngine
        from maintenance.data_report_hygiene_store import DataReportHygieneStore

        abs_root       = project_root if os.path.isabs(project_root) else os.path.join(BASE_DIR, project_root)
        abs_report_dir = report_dir  if os.path.isabs(report_dir)  else os.path.join(BASE_DIR, report_dir)
        abs_output_dir = output_dir  if os.path.isabs(output_dir)  else os.path.join(BASE_DIR, output_dir)

        engine = DataReportHygieneEngine(project_root=abs_root, output_dir=abs_output_dir)
        store  = DataReportHygieneStore(output_dir=abs_output_dir)

        inventory, manifests, summary, suggestions = engine.run(mode=mode)

        # Save CSVs
        store.save_inventory(inventory)
        store.save_report_manifest(manifests)
        store.save_summary(summary)

        lines: List[str] = []
        lines += self._section_header(mode)
        lines += self._section_overview(summary)
        lines += self._section_runtime_outputs(inventory)
        lines += self._section_report_manifest(manifests)
        lines += self._section_gitignore_coverage(engine)
        lines += self._section_tracked_runtime(engine)
        lines += self._section_stale_large(inventory)
        lines += self._section_suggestions(suggestions)
        lines += self._section_safety_declaration()

        content = "\n".join(lines) + "\n"
        os.makedirs(abs_report_dir, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        path  = os.path.join(abs_report_dir, f"data_report_hygiene_report_{today}.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        logger.info("Data & Report Hygiene report saved: %s", path)
        return path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_header(self, mode: str) -> List[str]:
        today = datetime.now().strftime("%Y-%m-%d")
        return [
            "# Data & Report Hygiene Report v1.0.2",
            "",
            f"**Date:** {today}  **Mode:** {mode}",
            "",
            "> **[!] Research Only / No Real Orders / Production Trading BLOCKED**",
            "> **[!] Data Cleanup is Review Only — No automatic deletion**",
            "> **[!] Archive Suggestions Only — No automatic archive**",
            "> **[!] No file moves. No file deletes. Review before any action.**",
            "",
            "---",
            "",
        ]

    def _section_overview(self, summary) -> List[str]:
        return [
            "## Overview",
            "",
            "| Field | Value |",
            "|-------|-------|",
            f"| Generated At | {summary.generated_at} |",
            f"| Version | {summary.version} |",
            f"| Total Items | {summary.total_items} |",
            f"| Runtime Outputs | {summary.runtime_outputs} |",
            f"| Git-tracked Runtime Outputs | {summary.git_tracked_runtime_outputs} |",
            f"| Ignored Outputs | {summary.ignored_outputs} |",
            f"| Missing Gitignore Rules | {summary.missing_gitignore_rules} |",
            f"| Stale Reports (>30d) | {summary.stale_reports} |",
            f"| Stale CSV Outputs | {summary.stale_csv_outputs} |",
            f"| Stale JSON Outputs | {summary.stale_json_outputs} |",
            f"| Large Files (>5MB) | {summary.large_files} |",
            f"| Database Files | {summary.database_files} |",
            f"| Spreadsheet Files | {summary.spreadsheet_files} |",
            f"| Warnings | {summary.warning_count} |",
            f"| Blocked | {summary.blocked_count} |",
            f"| Report Count | {summary.report_count} |",
            f"| Latest Reports | {summary.latest_reports} |",
            f"| No Real Orders | {summary.no_real_orders} |",
            f"| Production Blocked | {summary.production_blocked} |",
            f"| Review Only | {summary.review_only} |",
            "",
            "---",
            "",
        ]

    def _section_runtime_outputs(self, inventory) -> List[str]:
        lines = ["## Runtime Output Inventory", ""]
        runtime = [i for i in inventory if i.is_runtime_output]
        if not runtime:
            lines += ["No runtime output files found.", ""]
        else:
            lines += [
                f"Found {len(runtime)} runtime output files.",
                "",
                "| Path | Category | Age (d) | Size (B) | Severity | Action |",
                "|------|----------|---------|----------|----------|--------|",
            ]
            for item in runtime[:50]:
                lines.append(
                    f"| {item.path[:60]} | {item.category} | {item.age_days} "
                    f"| {item.size_bytes} | {item.severity} | {item.action_hint} |"
                )
            if len(runtime) > 50:
                lines.append(f"| ... | {len(runtime) - 50} more items | | | | |")
        lines += ["", "---", ""]
        return lines

    def _section_report_manifest(self, manifests) -> List[str]:
        lines = ["## Report Manifest", ""]
        if not manifests:
            lines += ["No report files found.", ""]
        else:
            lines += [
                f"Found {len(manifests)} report files.",
                "",
                "| Report | Type | Module | Latest | Ignored |",
                "|--------|------|--------|--------|---------|",
            ]
            for m in manifests[:40]:
                lines.append(
                    f"| {m.report_path[-50:]} | {m.report_type[:30]} | {m.module[:20]} "
                    f"| {m.is_latest} | {m.is_git_ignored} |"
                )
        lines += ["", "---", ""]
        return lines

    def _section_gitignore_coverage(self, engine) -> List[str]:
        coverage = engine.scan_gitignore_coverage()
        lines = ["## Gitignore Coverage", ""]
        lines += [
            "| Pattern | Covered |",
            "|---------|---------|",
        ]
        for pattern, covered in coverage.items():
            lines.append(f"| `{pattern}` | {covered} |")
        missing = [p for p, c in coverage.items() if not c]
        if missing:
            lines += [
                "",
                f"**Missing patterns:** {', '.join(f'`{p}`' for p in missing)}",
                "",
                "_Review the .gitignore file and add any missing patterns._",
            ]
        lines += ["", "---", ""]
        return lines

    def _section_tracked_runtime(self, engine) -> List[str]:
        tracked = engine.scan_git_tracked_runtime_outputs()
        lines = ["## Tracked Runtime Outputs", ""]
        if not tracked:
            lines += ["No tracked runtime outputs found in data/backtest_results/ or reports/.", ""]
        else:
            lines += [
                f"**WARNING:** Found {len(tracked)} tracked runtime output(s).",
                "Consider adding to .gitignore.",
                "",
                "| File |",
                "|------|",
            ]
            for f in tracked[:30]:
                lines.append(f"| {f} |")
            if len(tracked) > 30:
                lines.append(f"| ... {len(tracked) - 30} more |")
        lines += ["", "---", ""]
        return lines

    def _section_stale_large(self, inventory) -> List[str]:
        from maintenance.data_report_hygiene_engine import _STALE_DAYS, _LARGE_BYTES
        from maintenance.data_report_hygiene_schema import CATEGORY_REPORT
        stale = [i for i in inventory if i.age_days > _STALE_DAYS]
        large = [i for i in inventory if i.size_bytes > _LARGE_BYTES]
        lines = ["## Stale & Large Files", ""]
        if stale:
            lines += [
                f"**Stale files (>{_STALE_DAYS}d):** {len(stale)}",
                "",
                "| Path | Age (d) | Category |",
                "|------|---------|----------|",
            ]
            for i in sorted(stale, key=lambda x: x.age_days, reverse=True)[:20]:
                lines.append(f"| {i.path[-60:]} | {i.age_days} | {i.category} |")
        if large:
            lines += [
                "",
                f"**Large files (>{_LARGE_BYTES // (1024*1024)}MB):** {len(large)}",
                "",
                "| Path | Size (B) | Category |",
                "|------|----------|----------|",
            ]
            for i in sorted(large, key=lambda x: x.size_bytes, reverse=True)[:20]:
                lines.append(f"| {i.path[-60:]} | {i.size_bytes} | {i.category} |")
        if not stale and not large:
            lines += ["No stale or large files found.", ""]
        lines += ["", "---", ""]
        return lines

    def _section_suggestions(self, suggestions) -> List[str]:
        lines = ["## Suggested Actions", ""]
        lines += [
            "> **All suggestions are review-only.**",
            "> **No automatic deletion, archive, or file moves will occur.**",
            "> **Data Cleanup is Review Only.**",
            "",
        ]
        if not suggestions:
            lines += ["No high/medium severity items found. No suggested actions.", ""]
        else:
            lines += [
                f"Found {len(suggestions)} suggested review actions:",
                "",
                "| Item | Action | Reason |",
                "|------|--------|--------|",
            ]
            for s in suggestions[:30]:
                lines.append(
                    f"| {s['item_id'][:40]} | {s['action']} | {s['reason'][:60]} |"
                )
        lines += ["", "---", ""]
        return lines

    def _section_safety_declaration(self) -> List[str]:
        return [
            "## Safety Declaration",
            "",
            "> **Research Only** — All outputs are for research and review purposes only.",
            ">",
            "> **No Real Orders** — This system does not and cannot place real trading orders.",
            ">",
            "> **Production Trading BLOCKED** — Production trading is permanently blocked.",
            ">",
            "> **Data Cleanup is Review Only** — No automatic deletion of files.",
            ">",
            "> **Archive Suggestions Only** — No automatic archiving of files.",
            ">",
            "> **No file moves** — This tool does not move or rename files.",
            ">",
            "> **Not Investment Advice** — Nothing in this report constitutes investment advice.",
            "",
            "---",
            "",
            "*TW Quant Cockpit v1.0.2 — Data & Report Hygiene — Research Only — Not Investment Advice*",
            "",
        ]
