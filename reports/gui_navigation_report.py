"""
reports/gui_navigation_report.py — GUINavigationReport for TW Quant Cockpit v0.5.2.

Generates a Markdown report with 7 sections covering the GUI tab registry,
groups, search keywords, and safety status.

[!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GUINavigationReport:
    """Generates reports/gui_navigation_report_YYYY-MM-DD.md.

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        report_dir: str = "reports",
        mode: str = "real",
    ) -> None:
        self.mode = mode
        if os.path.isabs(report_dir):
            self.report_dir = report_dir
        else:
            self.report_dir = os.path.join(BASE_DIR, report_dir)
        os.makedirs(self.report_dir, exist_ok=True)

    def generate(self, mode: Optional[str] = None) -> str:
        """Generate the GUI navigation report Markdown file.

        Returns path to the generated file.
        """
        mode = mode or self.mode
        today = datetime.now().strftime("%Y-%m-%d")
        ts    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            from gui.navigation.tab_registry import GUITabRegistry
            from gui.navigation.navigation_report_data import GUINavigationReportData
            reg  = GUITabRegistry()
            data = GUINavigationReportData(registry=reg)
        except Exception as exc:
            logger.error("GUINavigationReport: failed to load registry: %s", exc)
            raise

        summary      = data.build_summary()
        group_table  = data.build_group_table()
        tab_table    = data.build_tab_table()
        all_keywords = data.build_search_keywords()

        lines = []

        # ----------------------------------------------------------------
        # Header
        # ----------------------------------------------------------------
        lines += [
            f"# GUI Navigation Report — v0.5.2",
            f"",
            f"> Generated: {ts}  |  Mode: {mode}  |  GUI UX Only  |  Research Only  |  No Real Orders  |  Production BLOCKED",
            f"",
        ]

        # ----------------------------------------------------------------
        # Section 1: 總覽 (Overview)
        # ----------------------------------------------------------------
        lines += [
            f"## 1. 總覽 (Overview)",
            f"",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Total Tabs | {summary['total_tabs']} |",
            f"| Tab Groups | {summary['groups_count']} |",
            f"| High Priority Tabs (P0+P1) | {len(summary['high_priority_tabs'])} |",
            f"| Hidden Tabs | {len(summary['hidden_tabs'])} |",
            f"| Duplicate Display Names | {len(summary['duplicate_tabs'])} |",
            f"| Missing Metadata | {len(summary['missing_metadata'])} |",
            f"| Safety Status | **{summary['safety_status']}** |",
            f"| Read Only | {summary['read_only']} |",
            f"| No Real Orders | {summary['no_real_orders']} |",
            f"| Production Blocked | {summary['production_blocked']} |",
            f"",
        ]

        # ----------------------------------------------------------------
        # Section 2: Tab Groups
        # ----------------------------------------------------------------
        lines += [
            f"## 2. Tab Groups",
            f"",
            f"| Group | Tabs | P0 | P1 | Description |",
            f"|-------|------|----|----|-------------|",
        ]
        for g in group_table:
            lines.append(
                f"| {g['group']} | {g['tab_count']} | {g['p0_count']} | {g['p1_count']} | {g['description']} |"
            )
        lines.append("")

        # ----------------------------------------------------------------
        # Section 3: High Priority Tabs (P0)
        # ----------------------------------------------------------------
        p0_tabs = [t for t in tab_table if t["priority"] == "P0"]
        lines += [
            f"## 3. High Priority Tabs (P0)",
            f"",
            f"| Tab | Group | CLI Commands | Description |",
            f"|-----|-------|--------------|-------------|",
        ]
        for t in p0_tabs:
            desc = t["description"][:80].replace("|", "\\|")
            lines.append(
                f"| {t['tab']} | {t['group']} | {t['related_cli']} | {desc} |"
            )
        lines.append("")

        # ----------------------------------------------------------------
        # Section 4: Tab Metadata (Full Table)
        # ----------------------------------------------------------------
        lines += [
            f"## 4. Tab Metadata",
            f"",
            f"| Tab | Group | Priority | Related CLI | Safety | Maturity |",
            f"|-----|-------|----------|-------------|--------|----------|",
        ]
        for t in tab_table:
            lines.append(
                f"| {t['tab']} | {t['group']} | {t['priority']} "
                f"| {t['related_cli']} | {t['safety']} | {t['maturity']} |"
            )
        lines.append("")

        # ----------------------------------------------------------------
        # Section 5: Search / Discovery
        # ----------------------------------------------------------------
        lines += [
            f"## 5. Search / Discovery — Keywords",
            f"",
            f"All unique keywords across all tabs ({len(all_keywords)} total):",
            f"",
            f"```",
            f"{', '.join(all_keywords)}",
            f"```",
            f"",
        ]

        # ----------------------------------------------------------------
        # Section 6: Compatibility
        # ----------------------------------------------------------------
        total = summary["total_tabs"]
        lines += [
            f"## 6. Backward Compatibility",
            f"",
            f"- All {total} existing tabs preserved — no tab deleted or renamed",
            f"- All v0.5.1 and earlier tabs remain accessible",
            f"- GUITabRegistry enriches metadata; does not modify dashboard.py tab order",
            f"- `build_inventory()` in `os_planning/gui_tab_inventory.py` unchanged",
            f"",
        ]

        # ----------------------------------------------------------------
        # Section 7: 安全聲明
        # ----------------------------------------------------------------
        lines += [
            f"## 7. 安全聲明 (Safety Declaration)",
            f"",
            f"| Safety Flag | Value |",
            f"|-------------|-------|",
            f"| GUI UX Only | True |",
            f"| Research Only | True |",
            f"| No Real Orders | True |",
            f"| No Auto Trading | True |",
            f"| Production BLOCKED | True |",
            f"| real_order_ready | False |",
            f"| No Broker Connection | True |",
            f"",
            f"---",
            f"*TW Quant Cockpit v0.5.2 — GUI Tab Grouping / Navigation Polish — Research Only — Not Investment Advice*",
        ]

        content = "\n".join(lines) + "\n"
        report_path = os.path.join(self.report_dir, f"gui_navigation_report_{today}.md")
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("GUINavigationReport saved: %s", report_path)
        except Exception as exc:
            logger.error("GUINavigationReport: could not write file: %s", exc)
            raise

        return report_path
