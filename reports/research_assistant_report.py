"""
reports/research_assistant_report.py — ResearchAssistantReport (v0.4.8).

Generates Research Assistant / Coach Report in Markdown.

Output: reports/research_assistant_report_YYYY-MM-DD.md

[!] Coaching Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No tokens. No broker data. Report is gitignored.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchAssistantReport:
    """
    Generates Research Assistant / Coach Report.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
      No tokens. No broker data.
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
        session_summary: dict,
        mode:   str = "real",
        period: str = "daily",
    ) -> str:
        """
        Generate Markdown report from coach session summary.
        Returns output file path.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"research_assistant_report_{today}.md"
        os.makedirs(self._report_dir, exist_ok=True)
        path = os.path.join(self._report_dir, filename)

        lines = self._build_report(session_summary, mode, period, today)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))

        logger.info("[ResearchAssistantReport] Report written: %s", path)
        return path

    # ------------------------------------------------------------------
    # Section builders
    # ------------------------------------------------------------------

    def _build_report(
        self,
        s:      dict,
        mode:   str,
        period: str,
        today:  str,
    ) -> List[str]:
        lines: List[str] = []
        lines += self._section_header(s, mode, period, today)
        lines += self._section_overview(s, mode, period)
        lines += self._section_daily_checklist(s.get("daily_checklist", []))
        lines += self._section_weekly_checklist(s.get("weekly_checklist", []))
        lines += self._section_replay_plan(s.get("replay_training_plan", []))
        lines += self._section_rule_queue(s.get("rule_review_queue", []))
        lines += self._section_data_repair(s.get("data_repair_plan", []))
        lines += self._section_journal_coaching(s)
        lines += self._section_model_coaching(s)
        lines += self._section_safety()
        return lines

    def _section_header(self, s, mode, period, today) -> List[str]:
        return [
            "# Research Assistant / Coach Report",
            "",
            f"> Generated: {today} | Mode: {mode} | Period: {period}",
            ">",
            "> **[!] Coaching Only. Research Only. No Real Orders. Production Trading: BLOCKED.**",
            "> This report is for research process improvement only.",
            "> Not investment advice. No buy/sell recommendations.",
            "",
        ]

    def _section_overview(self, s, mode, period) -> List[str]:
        lines = [
            "## 一、總覽",
            "",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Mode | {mode} |",
            f"| Period | {period} |",
            f"| Coaching Only | True |",
            f"| Research Only | True |",
            f"| No Real Orders | True |",
            f"| Total Recommendations | {s.get('total_recommendations', 0)} |",
            f"| P0 | {s.get('p0_count', 0)} |",
            f"| P1 | {s.get('p1_count', 0)} |",
            f"| P2 | {s.get('p2_count', 0)} |",
            f"| P3 | {s.get('p3_count', 0)} |",
            f"| Daily Checklist | {s.get('daily_checklist_count', 0)} |",
            f"| Weekly Checklist | {s.get('weekly_checklist_count', 0)} |",
            f"| Replay Training Tasks | {s.get('replay_tasks_count', 0)} |",
            f"| Rule Review Tasks | {s.get('rule_review_count', 0)} |",
            f"| Data Repair Tasks | {s.get('data_repair_count', 0)} |",
            "",
        ]
        return lines

    def _section_daily_checklist(self, items: list) -> List[str]:
        lines = ["## 二、今日研究檢查清單", ""]
        if not items:
            lines += ["_No daily checklist items._", ""]
            return lines
        lines += ["| Priority | Task | Summary | Suggested Command |",
                  "|----------|------|---------|-------------------|"]
        for item in items:
            p   = item.get("priority", "")
            t   = item.get("title", "")
            s   = item.get("summary", "")
            cmd = item.get("suggested_command", "")
            lines.append(f"| {p} | {t} | {s} | `{cmd}` |")
        lines.append("")
        return lines

    def _section_weekly_checklist(self, items: list) -> List[str]:
        lines = ["## 三、本週研究檢查清單", ""]
        if not items:
            lines += ["_No weekly checklist items._", ""]
            return lines
        lines += ["| Priority | Task | Summary | Suggested Command |",
                  "|----------|------|---------|-------------------|"]
        for item in items:
            p   = item.get("priority", "")
            t   = item.get("title", "")
            s   = item.get("summary", "")
            cmd = item.get("suggested_command", "")
            lines.append(f"| {p} | {t} | {s} | `{cmd}` |")
        lines.append("")
        return lines

    def _section_replay_plan(self, items: list) -> List[str]:
        lines = ["## 四、Replay 訓練菜單", ""]
        if not items:
            lines += ["_No replay training tasks._", ""]
            return lines
        lines += ["| Priority | Scenario | Reason | Expected Skill | Suggested Command |",
                  "|----------|----------|--------|----------------|-------------------|"]
        for item in items:
            p      = item.get("priority", "")
            t      = item.get("title", "")
            reason = item.get("rationale", item.get("summary", ""))
            skill  = item.get("expected_benefit", "")
            cmd    = item.get("suggested_command", "")
            lines.append(f"| {p} | {t} | {reason} | {skill} | `{cmd}` |")
        lines.append("")
        return lines

    def _section_rule_queue(self, items: list) -> List[str]:
        lines = ["## 五、Rule Review Queue", ""]
        if not items:
            lines += ["_No rule review tasks._", ""]
            return lines
        lines += ["| Priority | Rule ID | Reason | Rationale | Suggested Command |",
                  "|----------|---------|--------|-----------|-------------------|"]
        for item in items:
            p       = item.get("priority", "")
            t       = item.get("title", "")
            reason  = item.get("summary", "")
            rat     = item.get("rationale", "")
            cmd     = item.get("suggested_command", "")
            lines.append(f"| {p} | {t} | {reason} | {rat} | `{cmd}` |")
        lines.append("")
        return lines

    def _section_data_repair(self, items: list) -> List[str]:
        lines = ["## 六、Data Repair Priority", ""]
        if not items:
            lines += ["_No data repair tasks._", ""]
            return lines
        lines += ["| Priority | Dataset / Provider | Issue | Suggested Command |",
                  "|----------|--------------------|-------|-------------------|"]
        for item in items:
            p    = item.get("priority", "")
            t    = item.get("title", "")
            s    = item.get("summary", "")
            cmd  = item.get("suggested_command", "")
            lines.append(f"| {p} | {t} | {s} | `{cmd}` |")
        lines.append("")
        return lines

    def _section_journal_coaching(self, s: dict) -> List[str]:
        journal_tasks = s.get("journal_tasks", [])
        lines = ["## 七、Journal / Process Coaching", ""]
        if not journal_tasks:
            lines += ["_No journal coaching tasks._", ""]
            return lines
        for item in journal_tasks:
            t   = item.get("title", "")
            sm  = item.get("summary", "")
            cmd = item.get("suggested_command", "")
            lines += [f"- **{t}**: {sm}", f"  - Suggested: `{cmd}`"]
        lines.append("")
        return lines

    def _section_model_coaching(self, s: dict) -> List[str]:
        model_tasks = s.get("model_tasks", [])
        lines = ["## 八、Model / ML Coaching", ""]
        if not model_tasks:
            lines += ["_No model/ML coaching tasks._", ""]
            return lines
        for item in model_tasks:
            t   = item.get("title", "")
            sm  = item.get("summary", "")
            cmd = item.get("suggested_command", "")
            lines += [f"- **{t}**: {sm}", f"  - Suggested: `{cmd}`"]
        lines.append("")
        return lines

    def _section_safety(self) -> List[str]:
        return [
            "## 九、安全聲明",
            "",
            "- **Coaching Only** — This assistant provides research process coaching only.",
            "- **Research Only** — All recommendations are for research improvement, not trading.",
            "- **No Real Orders** — No buy/sell/order suggestions. No broker connection.",
            "- **Not Investment Advice** — Not financial advice. Not investment recommendations.",
            "- **Production Trading BLOCKED** — REAL_ORDER_READY=False. No live trading.",
            "",
        ]
