"""
reports/backtest_coach_report.py — BacktestCoachReportBuilder v0.7.3

Generates Markdown report for Backtest-to-Coach Loop.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_SAFETY_HEADER = (
    "[!] Research Only  |  No Real Orders  |  Production Trading BLOCKED  |  Not Investment Advice"
)


class BacktestCoachReportBuilder:
    """
    Generates a Markdown Backtest-to-Coach Loop report.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    VERSION = "v0.7.3"

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def build(
        self,
        mode:             str = "real",
        output_dir:       str = "reports",
        coach_output_dir: str = "data/backtest_results/backtest_coach",
    ) -> str:
        """
        Build Markdown report from latest backtest coach outputs.

        Returns path to the generated report file.
        """
        out_abs   = output_dir if os.path.isabs(output_dir) else os.path.join(_BASE_DIR, output_dir)
        coach_abs = coach_output_dir if os.path.isabs(coach_output_dir) else os.path.join(_BASE_DIR, coach_output_dir)

        os.makedirs(out_abs, exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"backtest_coach_report_{today}.md"
        path = os.path.join(out_abs, filename)

        try:
            from backtest_coach.backtest_coach_store import BacktestCoachStore
            store = BacktestCoachStore(output_dir=coach_abs)
            summary      = store.load_latest_summary()
            signals      = store.load_signals()
            tasks        = store.load_tasks()
            daily_tasks  = store.load_daily_tasks()
            weekly_tasks = store.load_weekly_tasks()
        except Exception as exc:
            logger.warning("BacktestCoachReportBuilder: load error: %s", exc)
            summary = None
            signals = []
            tasks = []
            daily_tasks = []
            weekly_tasks = []

        lines: List[str] = []
        lines += self._section_header(today, mode, summary)
        lines += self._section_overview(summary)
        lines += self._section_top_tasks(tasks[:10])
        lines += self._section_daily_plan(daily_tasks)
        lines += self._section_weekly_plan(weekly_tasks[:12])
        lines += self._section_signals(signals)
        lines += self._section_replay_journal(signals, tasks)
        lines += self._section_strategy_memory(tasks)
        lines += self._section_safety()

        content = "\n".join(lines) + "\n"
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("BacktestCoachReportBuilder: report saved → %s", path)
        except Exception as exc:
            logger.error("BacktestCoachReportBuilder: write failed: %s", exc)

        return path

    def _section_header(self, today: str, mode: str, summary) -> List[str]:
        overall = summary.overall_status if summary else "UNKNOWN"
        return [
            f"# Backtest-to-Coach Loop Report",
            f"",
            f"> **{self.VERSION}** | Report Date: {today} | Mode: {mode.upper()} | Status: {overall}",
            f">",
            f"> {_SAFETY_HEADER}",
            f"",
            f"---",
            f"",
        ]

    def _section_overview(self, summary) -> List[str]:
        if not summary:
            return ["## 總覽 (Overview)", "", "*No summary data available. Run: `python main.py backtest-coach --mode real`*", "", "---", ""]

        s = summary
        lines = [
            "## 總覽 (Overview)",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Total Signals | {s.total_signals} |",
            f"| Total Tasks | {s.total_tasks} |",
            f"| P0 Tasks | {s.p0_count} |",
            f"| P1 Tasks | {s.p1_count} |",
            f"| P2 Tasks | {s.p2_count} |",
            f"| P3 Tasks | {s.p3_count} |",
            f"| Replay Tasks | {s.replay_tasks} |",
            f"| Journal Tasks | {s.journal_tasks} |",
            f"| Backtest Tasks | {s.backtest_tasks} |",
            f"| Data Fix Tasks | {s.fix_data_tasks} |",
            f"| Daily Plan Tasks | {s.daily_tasks_count} |",
            f"| Weekly Plan Tasks | {s.weekly_tasks_count} |",
            f"| Top Task | {s.top_task or '—'} |",
            f"| Overall Status | **{s.overall_status}** |",
            f"| Research Only | YES |",
            f"| No Real Orders | YES |",
            f"| Production Blocked | YES |",
            "",
            "---",
            "",
        ]
        return lines

    def _section_top_tasks(self, tasks) -> List[str]:
        lines = [
            "## Top Coach Tasks",
            "",
        ]
        if not tasks:
            lines += ["*No tasks generated. Run backtest-coach to generate tasks.*", "", "---", ""]
            return lines

        lines += [
            "| Pri | Type | Title | Training Goal | Suggested Command | Success Criteria | Status |",
            "|-----|------|-------|---------------|-------------------|-----------------|--------|",
        ]
        for t in tasks:
            cmd = (t.suggested_commands[0] if t.suggested_commands else "—")
            lines.append(
                f"| {t.priority} | {t.task_type} | {t.title[:50]} | {t.training_goal[:50]} | "
                f"`{cmd[:60]}` | {t.success_criteria[:40]} | {t.status} |"
            )
        lines += ["", "---", ""]
        return lines

    def _section_daily_plan(self, tasks) -> List[str]:
        lines = [
            "## Daily Training Plan",
            "",
        ]
        if not tasks:
            lines += ["*No daily plan tasks. Run: `python main.py backtest-coach --mode real --period daily`*", "", "---", ""]
            return lines

        lines += [
            "| # | Type | Title | Method | Est. Min | Priority |",
            "|---|------|-------|--------|----------|----------|",
        ]
        for i, t in enumerate(tasks, 1):
            lines.append(
                f"| {i} | {t.task_type} | {t.title[:50]} | {t.practice_method[:50]} | "
                f"{t.estimated_minutes} | {t.priority} |"
            )
        lines += ["", "---", ""]
        return lines

    def _section_weekly_plan(self, tasks) -> List[str]:
        lines = [
            "## Weekly Training Plan",
            "",
        ]
        if not tasks:
            lines += ["*No weekly plan tasks. Run: `python main.py backtest-coach --mode real --period weekly`*", "", "---", ""]
            return lines

        lines += [
            "| # | Type | Title | Goal | Priority |",
            "|---|------|-------|------|----------|",
        ]
        for i, t in enumerate(tasks, 1):
            lines.append(
                f"| {i} | {t.task_type} | {t.title[:50]} | {t.training_goal[:60]} | {t.priority} |"
            )
        lines += ["", "---", ""]
        return lines

    def _section_signals(self, signals) -> List[str]:
        lines = [
            "## Backtest Weakness Signals",
            "",
        ]
        if not signals:
            lines += ["*No signals detected. Run backtests and replay training sessions first.*", "", "---", ""]
            return lines

        lines += [
            "| Source | Issue Type | Severity | Strategy | Symbol | Evidence | Suggested Action |",
            "|--------|-----------|----------|----------|--------|----------|-----------------|",
        ]
        for s in signals[:20]:
            lines.append(
                f"| {s.source_module} | {s.issue_type} | {s.severity} | "
                f"{s.strategy_name or '—'} | {s.symbol or '—'} | "
                f"{s.evidence[:40] if s.evidence else '—'} | {s.suggested_action[:50] if s.suggested_action else '—'} |"
            )
        if len(signals) > 20:
            lines.append(f"| ... | *{len(signals) - 20} more signals* | | | | | |")
        lines += ["", "---", ""]
        return lines

    def _section_replay_journal(self, signals, tasks) -> List[str]:
        from backtest_coach.backtest_coach_schema import (
            ISSUE_REPLAY_SCORE_LOW, ISSUE_FAKE_BREAKOUT, ISSUE_STOP_LOSS_DISCIPLINE,
            ISSUE_JOURNAL_REPEAT_MISTAKE, TASK_PRACTICE_REPLAY, TASK_REVIEW_JOURNAL,
        )
        replay_sigs   = [s for s in signals if s.issue_type in (ISSUE_REPLAY_SCORE_LOW, ISSUE_FAKE_BREAKOUT, ISSUE_STOP_LOSS_DISCIPLINE)]
        journal_sigs  = [s for s in signals if s.issue_type == ISSUE_JOURNAL_REPEAT_MISTAKE]
        replay_tasks  = [t for t in tasks if t.task_type == TASK_PRACTICE_REPLAY]
        journal_tasks = [t for t in tasks if t.task_type == TASK_REVIEW_JOURNAL]

        lines = [
            "## Replay / Journal Loop",
            "",
            f"**Replay mistakes:** {len(replay_sigs)} signals | **Journal patterns:** {len(journal_sigs)} signals",
            f"**Replay practice tasks:** {len(replay_tasks)} | **Journal review tasks:** {len(journal_tasks)}",
            "",
        ]

        if replay_sigs:
            lines.append("### Replay Mistakes")
            lines.append("")
            for s in replay_sigs[:5]:
                lines.append(f"- [{s.severity}] {s.description[:100]}")
                if s.suggested_command:
                    lines.append(f"  Command: `{s.suggested_command}`")
            lines.append("")

        if journal_sigs:
            lines.append("### Journal Patterns")
            lines.append("")
            for s in journal_sigs[:5]:
                lines.append(f"- [{s.priority}] {s.description[:100]}")
            lines.append("")

        lines += ["---", ""]
        return lines

    def _section_strategy_memory(self, tasks) -> List[str]:
        from backtest_coach.backtest_coach_schema import (
            TASK_BACKTEST_MORE, TASK_REVIEW_RULE, TASK_UPDATE_MEMORY, SRC_STRATEGY_MEMORY,
        )
        memory_tasks = [t for t in tasks if t.source_module == SRC_STRATEGY_MEMORY]
        backtest_mem = [t for t in tasks if t.task_type == TASK_BACKTEST_MORE]
        rule_review  = [t for t in tasks if t.task_type == TASK_REVIEW_RULE]

        lines = [
            "## Strategy Memory Follow-ups",
            "",
            f"**Memory-sourced tasks:** {len(memory_tasks)} | "
            f"**Backtest tasks:** {len(backtest_mem)} | **Rule review tasks:** {len(rule_review)}",
            "",
        ]

        if memory_tasks:
            lines += [
                "| Memory / Task | Status | Suggested Command |",
                "|--------------|--------|------------------|",
            ]
            for t in memory_tasks[:8]:
                cmd = t.suggested_commands[0] if t.suggested_commands else "—"
                lines.append(f"| {t.title[:60]} | {t.status} | `{cmd[:50]}` |")
            lines.append("")
        else:
            lines.append("*No memory follow-up tasks. Run: `python main.py strategy-memory --mode real`*")
            lines.append("")

        lines += ["---", ""]
        return lines

    def _section_safety(self) -> List[str]:
        return [
            "## Safety",
            "",
            "| Safety Check | Status |",
            "|-------------|--------|",
            "| Research Only | YES |",
            "| No Real Orders | YES |",
            "| No Broker Connection | YES |",
            "| No Auto Trading | YES |",
            "| Production Trading BLOCKED | YES |",
            "| Not Investment Advice | YES |",
            "| Read Only Mode | YES |",
            "",
            "> **[!] This report is for research and training purposes only.**",
            "> **No real orders. No broker execution. Production Trading: BLOCKED.**",
            "> **Not investment advice.**",
            "",
        ]
