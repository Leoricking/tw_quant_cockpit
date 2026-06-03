"""
reports/research_workflow_report.py — ResearchWorkflowReport (v0.4.9).

Generates Research Workflow Automation Report in Markdown.

Output: reports/research_workflow_report_YYYY-MM-DD.md

[!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchWorkflowReport:
    """
    Generates Research Workflow Automation Report.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __init__(self, report_dir: str = "reports"):
        self._report_dir = (
            os.path.join(BASE_DIR, report_dir)
            if not os.path.isabs(report_dir)
            else report_dir
        )

    def generate(
        self,
        workflow_run:  Optional[object] = None,
        tasks:         Optional[list]   = None,
        package_path:  str = "",
        mode:          str = "real",
        workflow_type: str = "daily_research",
    ) -> str:
        """Generate Markdown report. Returns output file path."""
        today    = datetime.now().strftime("%Y-%m-%d")
        filename = f"research_workflow_report_{today}.md"
        os.makedirs(self._report_dir, exist_ok=True)
        path = os.path.join(self._report_dir, filename)

        lines = self._build_report(
            workflow_run=workflow_run,
            tasks=tasks or [],
            package_path=package_path,
            mode=mode,
            workflow_type=workflow_type,
            today=today,
        )
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))

        logger.info("[ResearchWorkflowReport] Report written: %s", path)
        return path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _build_report(
        self,
        workflow_run,
        tasks:         list,
        package_path:  str,
        mode:          str,
        workflow_type: str,
        today:         str,
    ) -> List[str]:
        lines: List[str] = []
        lines += self._section_header(today, mode, workflow_type)
        lines += self._section_overview(workflow_run, mode, workflow_type, package_path)
        lines += self._section_tasks(tasks)
        lines += self._section_blocked(tasks)
        lines += self._section_daily_package(package_path, workflow_type)
        lines += self._section_weekly_package(package_path, workflow_type)
        lines += self._section_safety()
        return lines

    def _section_header(self, today, mode, workflow_type) -> List[str]:
        return [
            "# Research Workflow Automation Report",
            "",
            f"> Generated: {today} | Mode: {mode} | Workflow: {workflow_type}",
            ">",
            "> **[!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.**",
            "",
        ]

    def _section_overview(self, run, mode, workflow_type, package_path) -> List[str]:
        lines = ["## 一、總覽", ""]
        if run:
            d = run.to_dict() if hasattr(run, "to_dict") else {}
            lines += [
                "| Field | Value |",
                "|-------|-------|",
                f"| Mode | {mode} |",
                f"| Workflow Type | {workflow_type} |",
                f"| Workflow Only | True |",
                f"| Research Only | True |",
                f"| No Real Orders | True |",
                f"| Tasks Total | {d.get('tasks_total', 0)} |",
                f"| Tasks Run | {d.get('tasks_run', 0)} |",
                f"| Tasks Passed | {d.get('tasks_passed', 0)} |",
                f"| Tasks Failed | {d.get('tasks_failed', 0)} |",
                f"| Tasks Blocked | {d.get('tasks_blocked', 0)} |",
                f"| Package Path | {package_path or '—'} |",
                "",
            ]
        else:
            lines += ["_No workflow run data._", ""]
        return lines

    def _section_tasks(self, tasks: list) -> List[str]:
        lines = ["## 二、Workflow Tasks", ""]
        run_tasks = [t for t in tasks if hasattr(t, "status") and t.status not in ("BLOCKED",)]
        if not run_tasks:
            lines += ["_No executed tasks._", ""]
            return lines
        lines += [
            "| Priority | Task | Command | Status | Duration | Warning |",
            "|----------|------|---------|--------|----------|---------|",
        ]
        for t in run_tasks:
            d = t.to_dict() if hasattr(t, "to_dict") else t
            p   = d.get("priority", "")
            tn  = d.get("task_name", "")
            cmd = d.get("suggested_command", "")
            s   = d.get("status", "")
            dur = d.get("duration_seconds", 0)
            w   = d.get("warning", "")
            lines.append(f"| {p} | {tn} | `{cmd}` | {s} | {dur}s | {w} |")
        lines.append("")
        return lines

    def _section_blocked(self, tasks: list) -> List[str]:
        lines = ["## 三、Blocked Commands", ""]
        blocked = [t for t in tasks if hasattr(t, "status") and t.status == "BLOCKED"]
        if not blocked:
            lines += ["_No blocked commands._", ""]
            return lines
        lines += [
            "| Command | Reason | Safety Rule |",
            "|---------|--------|-------------|",
        ]
        for t in blocked:
            d = t.to_dict() if hasattr(t, "to_dict") else t
            cmd    = d.get("suggested_command", "") or d.get("task_name", "")
            reason = d.get("warning", "Blocked by SafeCommandRegistry")
            lines.append(f"| `{cmd}` | {reason} | No execution |")
        lines.append("")
        return lines

    def _section_daily_package(self, package_path, workflow_type) -> List[str]:
        lines = ["## 四、Daily Research Package", ""]
        if workflow_type == "daily_research" and package_path:
            lines.append(f"- Package path: `{package_path}`")
            index = os.path.join(package_path, "index.md")
            lines.append(f"- Index: `{index}`")
        else:
            lines.append("_Run daily_research workflow to generate package._")
        lines.append("")
        return lines

    def _section_weekly_package(self, package_path, workflow_type) -> List[str]:
        lines = ["## 五、Weekly Review Package", ""]
        if workflow_type == "weekly_review" and package_path:
            lines.append(f"- Package path: `{package_path}`")
            index = os.path.join(package_path, "index.md")
            lines.append(f"- Index: `{index}`")
        else:
            lines.append("_Run weekly_review workflow to generate package._")
        lines.append("")
        return lines

    def _section_safety(self) -> List[str]:
        return [
            "## 六、安全聲明",
            "",
            "- **Workflow Only** — Research workflow automation only.",
            "- **Research Only** — All executed commands are read-only research commands.",
            "- **No Real Orders** — No buy/sell/order. No broker execution.",
            "- **No Broker** — No connection to any broker or trading system.",
            "- **No Auto Trading** — No automatic trading or order submission.",
            "- **Production Trading BLOCKED** — REAL_ORDER_READY=False.",
            "",
        ]
