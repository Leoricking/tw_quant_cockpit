"""reports/research_intelligence_report.py — Research Intelligence Report generator v0.7.0.

[!] Research Intelligence Only. Research Only. No Real Orders.
[!] Production Trading: BLOCKED. Not investment advice.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION  = "v0.7.0"


class ResearchIntelligenceReport:
    """Generates Markdown Research Intelligence Reports.

    [!] Research Intelligence Only. Research Only. No Real Orders.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def generate(
        self,
        summary: Optional[dict] = None,
        signals: Optional[list] = None,
        recommendations: Optional[list] = None,
        priority_board: Optional[dict] = None,
        daily_plan: Optional[list] = None,
        weekly_plan: Optional[list] = None,
        mode: str = "real",
    ) -> str:
        summary          = summary or {}
        signals          = signals or []
        recommendations  = recommendations or []
        priority_board   = priority_board or {}
        daily_plan       = daily_plan or []
        weekly_plan      = weekly_plan or []

        sections = [
            self._header(summary, mode),
            self._section_overview(summary),
            self._section_priority_board(priority_board),
            self._section_daily_plan(daily_plan),
            self._section_weekly_plan(weekly_plan),
            self._section_data_report_gaps(signals),
            self._section_replay_journal(signals),
            self._section_rule_strategy(signals),
            self._section_system_regression(signals, summary),
            self._section_safety(),
        ]
        return "\n\n".join(sections)

    def save(self, content: str, report_dir: str = "reports") -> str:
        abs_dir = os.path.join(BASE_DIR, report_dir) if not os.path.isabs(report_dir) else report_dir
        os.makedirs(abs_dir, exist_ok=True)
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(abs_dir, f"research_intelligence_report_{ts}.md")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("[ResearchIntelligenceReport] saved → %s", path)
        except Exception as exc:
            logger.error("[ResearchIntelligenceReport] save error: %s", exc)
        return path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _header(self, summary: dict, mode: str) -> str:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        return (
            f"# TW Quant Cockpit — Research Intelligence Report {VERSION}\n\n"
            f"> **[!] Research Intelligence Only. Research Only. No Real Orders.**\n"
            f"> **[!] Production Trading: BLOCKED. Not investment advice.**\n"
            f"> **[!] All recommendations are research actions only (REVIEW / RESEARCH / PRACTICE / FIX_DATA / GENERATE_REPORT).**\n\n"
            f"**Generated:** {ts}  \n"
            f"**Mode:** {mode}  \n"
            f"**Overall Status:** {summary.get('overall_status', '—')}  \n"
        )

    def _section_overview(self, summary: dict) -> str:
        if not summary:
            return "## 一、總覽\n\n*No summary available.*"
        lines = [
            "## 一、總覽\n",
            f"| Item | Value |",
            f"|------|-------|",
            f"| Version | {VERSION} |",
            f"| Research Intelligence Only | TRUE |",
            f"| Research Only | TRUE |",
            f"| No Real Orders | TRUE |",
            f"| Production Trading BLOCKED | TRUE |",
            f"| Total Signals | {summary.get('total_signals', 0)} |",
            f"| Recommendations | {summary.get('recommendations_count', 0)} |",
            f"| P0 (Critical) | {summary.get('system_risk_count', 0)} |",
            f"| High Priority Signals | {summary.get('high_priority_count', 0)} |",
            f"| Data Gaps | {summary.get('data_gap_count', 0)} |",
            f"| Replay Issues | {summary.get('replay_issue_count', 0)} |",
            f"| Rule Reviews | {summary.get('rule_review_count', 0)} |",
            f"| Report Gaps | {summary.get('report_gap_count', 0)} |",
            f"| Overall Status | **{summary.get('overall_status', '—')}** |",
            f"| Top Priority | {summary.get('top_priority', '—')} |",
        ]
        return "\n".join(lines)

    def _section_priority_board(self, board: dict) -> str:
        if not board:
            return "## 二、Top Priority Board\n\n*No priority items.*"
        lines = ["## 二、Top Priority Board\n"]
        for pri in ("P0", "P1", "P2", "P3"):
            items = board.get(pri, [])
            if not items:
                continue
            desc = {"P0": "必修", "P1": "高優先", "P2": "中優先", "P3": "低優先"}.get(pri, "")
            lines.append(f"\n### {pri} — {desc}\n")
            lines.append("| Priority | Title | Module | Suggested Command |")
            lines.append("|----------|-------|--------|-------------------|")
            for item in items:
                if isinstance(item, dict):
                    title = item.get("title", "")
                    module= item.get("module", "")
                    cmd   = f"`{item.get('command', '')}`" if item.get("command") else "—"
                    lines.append(f"| {pri} | {title} | {module} | {cmd} |")
        return "\n".join(lines)

    def _section_daily_plan(self, daily_plan: list) -> str:
        if not daily_plan:
            return "## 三、Daily Research Plan\n\n*No daily plan items.*"
        lines = ["## 三、Daily Research Plan\n",
                 "| # | Task | Category | Command | Expected Benefit |",
                 "|---|------|----------|---------|-----------------|"]
        for i, item in enumerate(daily_plan, 1):
            if isinstance(item, dict):
                title   = item.get("title", "")
                cat     = item.get("category", "")
                cmds    = item.get("suggested_commands", "")
                if isinstance(cmds, list):
                    cmd = cmds[0] if cmds else ""
                else:
                    cmd = str(cmds).split("|")[0]
                cmd_fmt = f"`{cmd}`" if cmd else "—"
                benefit = item.get("expected_benefit", "")
                lines.append(f"| {i} | {title} | {cat} | {cmd_fmt} | {benefit} |")
        return "\n".join(lines)

    def _section_weekly_plan(self, weekly_plan: list) -> str:
        if not weekly_plan:
            return "## 四、Weekly Research Plan\n\n*No weekly plan items.*"
        lines = ["## 四、Weekly Research Plan\n",
                 "| # | Task | Category | Command | Expected Benefit |",
                 "|---|------|----------|---------|-----------------|"]
        for i, item in enumerate(weekly_plan, 1):
            if isinstance(item, dict):
                title   = item.get("title", "")
                cat     = item.get("category", "")
                cmds    = item.get("suggested_commands", "")
                if isinstance(cmds, list):
                    cmd = cmds[0] if cmds else ""
                else:
                    cmd = str(cmds).split("|")[0]
                cmd_fmt = f"`{cmd}`" if cmd else "—"
                benefit = item.get("expected_benefit", "")
                lines.append(f"| {i} | {title} | {cat} | {cmd_fmt} | {benefit} |")
        return "\n".join(lines)

    def _section_data_report_gaps(self, signals: list) -> str:
        data_sigs = [s for s in signals if isinstance(s, dict)
                     and s.get("category") in ("DATA_GAP", "REPORT_GAP", "PROVIDER_LIMITATION")]
        if not data_sigs:
            # Try object-style
            data_sigs_obj = [s for s in signals if hasattr(s, "category")
                             and s.category in ("DATA_GAP", "REPORT_GAP", "PROVIDER_LIMITATION")]
            if not data_sigs_obj:
                return "## 五、Data / Report Gaps\n\n*No data or report gaps detected.*"
        lines = ["## 五、Data / Report Gaps\n",
                 "| Source | Severity | Title | Command |",
                 "|--------|----------|-------|---------|"]
        for s in signals:
            cat = s.get("category") if isinstance(s, dict) else getattr(s, "category", "")
            if cat in ("DATA_GAP", "REPORT_GAP", "PROVIDER_LIMITATION"):
                src = s.get("source_module") if isinstance(s, dict) else getattr(s, "source_module", "")
                sev = s.get("severity") if isinstance(s, dict) else getattr(s, "severity", "")
                title = s.get("title") if isinstance(s, dict) else getattr(s, "title", "")
                cmd = s.get("suggested_command") if isinstance(s, dict) else getattr(s, "suggested_command", "")
                cmd_fmt = f"`{cmd}`" if cmd else "—"
                lines.append(f"| {src} | {sev} | {title} | {cmd_fmt} |")
        return "\n".join(lines)

    def _section_replay_journal(self, signals: list) -> str:
        cats = ("REPLAY_MISTAKE", "TRAINING_TASK", "JOURNAL_PATTERN")
        rel = [s for s in signals if
               (s.get("category") if isinstance(s, dict) else getattr(s, "category", "")) in cats]
        if not rel:
            return "## 六、Replay / Journal Intelligence\n\n*No replay or journal issues.*"
        lines = ["## 六、Replay / Journal Intelligence\n",
                 "| Source | Priority | Title | Evidence |",
                 "|--------|----------|-------|----------|"]
        for s in rel:
            src   = s.get("source_module") if isinstance(s, dict) else getattr(s, "source_module", "")
            pri   = s.get("priority") if isinstance(s, dict) else getattr(s, "priority", "")
            title = s.get("title") if isinstance(s, dict) else getattr(s, "title", "")
            ev    = s.get("evidence") if isinstance(s, dict) else getattr(s, "evidence", "")
            lines.append(f"| {src} | {pri} | {title} | {ev} |")
        return "\n".join(lines)

    def _section_rule_strategy(self, signals: list) -> str:
        cats = ("RULE_REVIEW", "STRATEGY_RESEARCH")
        rel = [s for s in signals if
               (s.get("category") if isinstance(s, dict) else getattr(s, "category", "")) in cats]
        if not rel:
            return "## 七、Rule / Strategy Intelligence\n\n*No rule or strategy review items.*"
        lines = ["## 七、Rule / Strategy Intelligence\n",
                 "| Source | Priority | Title | Command |",
                 "|--------|----------|-------|---------|"]
        for s in rel:
            src   = s.get("source_module") if isinstance(s, dict) else getattr(s, "source_module", "")
            pri   = s.get("priority") if isinstance(s, dict) else getattr(s, "priority", "")
            title = s.get("title") if isinstance(s, dict) else getattr(s, "title", "")
            cmd   = s.get("suggested_command") if isinstance(s, dict) else getattr(s, "suggested_command", "")
            cmd_fmt = f"`{cmd}`" if cmd else "—"
            lines.append(f"| {src} | {pri} | {title} | {cmd_fmt} |")
        return "\n".join(lines)

    def _section_system_regression(self, signals: list, summary: dict) -> str:
        cats = ("SYSTEM_RISK", "REGRESSION_WARNING", "STABLE_RELEASE_NOTE")
        rel = [s for s in signals if
               (s.get("category") if isinstance(s, dict) else getattr(s, "category", "")) in cats]
        lines = ["## 八、System / Regression / Stable Release Signals\n"]
        lines.append(f"**Overall Status:** {summary.get('overall_status', '—')}\n")
        if not rel:
            lines.append("*No system risk signals. Stable.*")
        else:
            lines += ["| Source | Severity | Title | Command |",
                      "|--------|----------|-------|---------|"]
            for s in rel:
                src   = s.get("source_module") if isinstance(s, dict) else getattr(s, "source_module", "")
                sev   = s.get("severity") if isinstance(s, dict) else getattr(s, "severity", "")
                title = s.get("title") if isinstance(s, dict) else getattr(s, "title", "")
                cmd   = s.get("suggested_command") if isinstance(s, dict) else getattr(s, "suggested_command", "")
                cmd_fmt = f"`{cmd}`" if cmd else "—"
                lines.append(f"| {src} | {sev} | {title} | {cmd_fmt} |")
        return "\n".join(lines)

    def _section_safety(self) -> str:
        return (
            "## 九、安全聲明\n\n"
            "| Constraint | Status |\n"
            "|------------|--------|\n"
            "| Research Intelligence Only | TRUE |\n"
            "| Research Only | TRUE |\n"
            "| No Real Orders | TRUE |\n"
            "| No Broker Execution | TRUE |\n"
            "| No Auto Trading | TRUE |\n"
            "| Production Trading Blocked | TRUE |\n"
            "| Real Order Ready | FALSE |\n"
            "| Not Investment Advice | TRUE |\n\n"
            "> [!] This report is for research decision support only.\n"
            "> No real orders are placed. No broker is connected.\n"
            "> All recommendations are research actions (REVIEW / RESEARCH / PRACTICE / FIX_DATA).\n"
            "> BUY / SELL / ORDER are not generated."
        )
