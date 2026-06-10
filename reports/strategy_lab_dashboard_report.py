"""
reports/strategy_lab_dashboard_report.py — Strategy Lab Dashboard Report Builder v0.9.3

Generates reports/strategy_lab_dashboard_report_YYYY-MM-DD.md

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class StrategyLabDashboardReportBuilder:
    """Generate the v0.9.3 Strategy Lab Dashboard Markdown report.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        output_dir: str = "data/backtest_results/strategy_lab_dashboard",
        report_dir: str = "reports",
    ) -> None:
        if os.path.isabs(output_dir):
            self._output_dir = output_dir
        else:
            self._output_dir = os.path.join(BASE_DIR, output_dir)

        if os.path.isabs(report_dir):
            self._report_dir = report_dir
        else:
            self._report_dir = os.path.join(BASE_DIR, report_dir)

    def build(self, mode: str = "real") -> str:
        """Run dashboard engine, build report, return file path."""
        # Run engine
        result = {}
        try:
            from strategy_lab.strategy_lab_dashboard_engine import StrategyLabDashboardEngine
            engine = StrategyLabDashboardEngine(output_dir=self._output_dir)
            result = engine.run(mode=mode)
        except Exception as exc:
            logger.warning("StrategyLabDashboardReportBuilder: engine error: %s", exc)

        cards   = result.get("cards", [])
        rows    = result.get("rows", [])
        actions = result.get("actions", [])
        summary = result.get("summary")

        lines = self._build_lines(cards, rows, actions, summary, mode)
        content = "\n".join(lines) + "\n"

        os.makedirs(self._report_dir, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        path  = os.path.join(self._report_dir, f"strategy_lab_dashboard_report_{today}.md")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("StrategyLabDashboardReportBuilder: report written -> %s", path)
        except Exception as exc:
            logger.warning("StrategyLabDashboardReportBuilder: write error: %s", exc)
        return path

    # ------------------------------------------------------------------
    # Build report lines
    # ------------------------------------------------------------------

    def _build_lines(self, cards, rows, actions, summary, mode) -> List[str]:
        today = datetime.now().strftime("%Y-%m-%d")
        lines = []

        def _d(obj):
            if obj is None:
                return {}
            if isinstance(obj, dict):
                return obj
            if hasattr(obj, "to_dict"):
                return obj.to_dict()
            return {}

        sd = _d(summary)

        # Header
        lines += [
            "# Strategy Lab Dashboard Report",
            "",
            f"> **Generated:** {today}",
            f"> **Mode:** {mode}",
            ">",
            "> **[!] Research Only. No Real Orders. Production Trading BLOCKED.**",
            "> **[!] VALIDATED = Research Validated Only. Does NOT enable trading.**",
            "> **[!] Not Investment Advice.**",
            "",
            "---",
            "",
        ]

        # 1. 總覽
        lines += [
            "## 1. 總覽 (Overview)",
            "",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Overall Status | **{sd.get('overall_status', 'UNKNOWN')}** |",
            f"| Health Score | {sd.get('overall_health_score', 0):.1f} / 100 |",
            f"| Mode | {sd.get('mode', mode)} |",
            f"| Strategy Count | {sd.get('strategy_count', 0)} |",
            f"| VALIDATED | {sd.get('validated_count', 0)} |",
            f"| VALIDATING | {sd.get('validating_count', 0)} |",
            f"| OBSERVATIONAL | {sd.get('observational_count', 0)} |",
            f"| INSUFFICIENT | {sd.get('insufficient_count', 0)} |",
            f"| CONFLICTED | {sd.get('conflicted_count', 0)} |",
            f"| REJECTED | {sd.get('rejected_count', 0)} |",
            f"| Evidence Threads | {sd.get('evidence_thread_count', 0)} |",
            f"| Graph Gaps | {sd.get('graph_gap_count', 0)} |",
            f"| Crash Warnings | {sd.get('crash_reversal_warning_count', 0)} |",
            f"| Needs Backtest | {sd.get('needs_backtest_count', 0)} |",
            f"| Needs Replay | {sd.get('needs_replay_count', 0)} |",
            f"| Needs Data | {sd.get('needs_data_count', 0)} |",
            f"| Forbidden Actions | {sd.get('forbidden_action_count', 0)} |",
            "",
        ]

        # 2. Dashboard Cards
        lines += [
            "## 2. Dashboard Cards",
            "",
            "| Card | Value | Status | Severity | Next Step |",
            "|------|-------|--------|----------|-----------|",
        ]
        for c in cards:
            cd = _d(c)
            lines.append(
                f"| {cd.get('title','')} | {cd.get('value','')} | "
                f"{cd.get('status','')} | {cd.get('severity','')} | "
                f"`{cd.get('safe_next_step','')}` |"
            )
        lines.append("")

        # 3. Validation Grade Board
        lines += [
            "## 3. Validation Grade Board",
            "",
            "| Strategy | Grade | Score | Next Step |",
            "|----------|-------|-------|-----------|",
        ]
        sv_rows = [r for r in rows if _d(r).get("category") == "strategy_validation"]
        for r in sv_rows[:15]:
            rd = _d(r)
            lines.append(
                f"| {rd.get('title','')} | {rd.get('grade','')} | "
                f"{float(rd.get('score',0)):.1f} | `{rd.get('safe_next_step','')}` |"
            )
        if not sv_rows:
            lines.append("| (none) | — | — | Run strategy-validation --mode real |")
        lines.append("")

        # 4. Evidence & Crash Reversal Board
        lines += [
            "## 4. Evidence & Crash Reversal Board",
            "",
            "| Item | Status | Grade | Evidence | Next Step |",
            "|------|--------|-------|----------|-----------|",
        ]
        eg_rows = [r for r in rows if _d(r).get("category") in ("evidence_graph", "crash_reversal")]
        for r in eg_rows[:10]:
            rd = _d(r)
            lines.append(
                f"| {rd.get('title','')} | {rd.get('status','')} | "
                f"{rd.get('grade','')} | {str(rd.get('evidence',''))[:40]} | "
                f"`{rd.get('safe_next_step','')}` |"
            )
        if not eg_rows:
            lines.append("| (none) | — | — | — | Run evidence-graph --mode real |")
        lines.append("")

        # 5. Action Board
        lines += [
            "## 5. Action Board",
            "",
            "| Priority | Action Type | Title | Command |",
            "|----------|-------------|-------|---------|",
        ]
        for a in sorted(actions, key=lambda x: _d(x).get("priority", "P9")):
            ad = _d(a)
            lines.append(
                f"| {ad.get('priority','')} | {ad.get('action_type','')} | "
                f"{ad.get('title','')} | `{ad.get('safe_command','')}` |"
            )
        if not actions:
            lines.append("| — | — | No actions needed | — |")
        lines.append("")

        # 6. Top Priorities
        lines += [
            "## 6. Top Priorities",
            "",
        ]
        top = sorted(actions, key=lambda x: _d(x).get("priority", "P9"))[:5]
        for i, a in enumerate(top, 1):
            ad = _d(a)
            lines.append(f"{i}. **[{ad.get('priority','')}]** {ad.get('title','')} — `{ad.get('safe_command','')}`")
        if not top:
            lines.append("No priority actions at this time.")
        lines.append("")

        # 7. Module Health
        lines += [
            "## 7. Module Health",
            "",
            "| Module | Status |",
            "|--------|--------|",
            "| strategy_validation | Available |",
            "| evidence_graph | Available |",
            "| crash_reversal | Available |",
            "| training_metrics | Available |",
            "| backtest_coach | Available |",
            "| strategy_memory | Available |",
            "| research_intelligence | Available |",
            "",
        ]

        # 8. Known Warnings
        lines += [
            "## 8. Known Warnings",
            "",
        ]
        warnings_found = False
        for c in cards:
            cd = _d(c)
            if cd.get("status") in ("WARNING", "BLOCKED", "WATCH") and cd.get("severity") in ("HIGH", "EXTREME", "MEDIUM"):
                lines.append(f"- **[{cd.get('status','')}]** {cd.get('title','')}: {cd.get('subtitle','')} — `{cd.get('safe_next_step','')}`")
                warnings_found = True
        if not warnings_found:
            lines.append("No high-severity warnings at this time.")
        lines.append("")

        # 9. 安全聲明
        lines += [
            "## 9. 安全聲明 (Safety Declaration)",
            "",
            "- **Research Only** — This dashboard is for research and analysis purposes only.",
            "- **No Real Orders** — No orders are placed, executed, or submitted by this system.",
            "- **No Broker Connection** — This system has no connection to any broker or trading system.",
            "- **No Auto Trading** — Auto-trading is permanently blocked (`production_blocked=True`).",
            "- **VALIDATED does not enable trading** — VALIDATED grade is research-only and does NOT enable or imply real trading.",
            "- **Not Investment Advice** — Nothing in this report constitutes investment advice.",
            "- `read_only=True`, `no_real_orders=True`, `production_blocked=True`, `real_order_ready=False`",
            "",
            "---",
            "",
            "_Strategy Lab Dashboard v0.9.3 — TW Quant Cockpit_",
        ]

        return lines
