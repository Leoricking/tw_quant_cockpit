"""reports/research_intelligence_report.py — Research Intelligence Report generator v0.7.1.

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
VERSION  = "v0.7.1"


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
            self._section_today_focus(summary),
            self._section_overview(summary),
            self._section_priority_board(priority_board),
            self._section_daily_plan(daily_plan),
            self._section_weekly_plan(weekly_plan),
            self._section_signals_by_module(signals),
            self._section_command_safety(recommendations, summary),
            self._section_what_not_to_do(),
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

    def _section_today_focus(self, summary: dict) -> str:
        today_focus = summary.get("today_focus", "")
        top_p0      = summary.get("top_p0_title", "")
        top_p1      = summary.get("top_p1_title", "")
        safe_cmds   = summary.get("safe_command_count", 0)
        blocked     = summary.get("blocked_trading_action_count", 0)
        status      = summary.get("overall_status", "—")

        lines = ["## 一、Today Focus\n"]
        if today_focus:
            lines.append(f"> **{today_focus}**\n")
        lines += [
            f"| Item | Value |",
            f"|------|-------|",
            f"| Overall Status | **{status}** |",
            f"| Top P0 Issue | {top_p0 or '—'} |",
            f"| Top P1 Issue | {top_p1 or '—'} |",
            f"| Safe Commands Available | {safe_cmds} |",
            f"| Blocked Trading Actions | **{blocked}** (by design — no real orders) |",
            f"| What To Do | See Priority Board and Daily Plan below |",
            f"| What Not To Do | No BUY / SELL / ORDER / trade execution |",
        ]
        return "\n".join(lines)

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
        # board may be dict-of-lists or a flat list with "rows" key
        if isinstance(board, dict) and "rows" in board:
            rows = board["rows"]
            board = {"P0": [], "P1": [], "P2": [], "P3": []}
            for r in rows:
                pri = r.get("priority", "P3") if isinstance(r, dict) else "P3"
                if pri in board:
                    board[pri].append(r)
        if not board:
            return "## 三、Priority Board\n\n*No priority items.*"
        lines = ["## 三、Priority Board\n"]
        for pri in ("P0", "P1", "P2", "P3"):
            items = board.get(pri, [])
            if not items:
                continue
            desc = {"P0": "必修", "P1": "高優先", "P2": "中優先", "P3": "低優先"}.get(pri, "")
            lines.append(f"\n### {pri} — {desc}\n")
            lines.append("| Priority | Title | Why Now | Risk If Ignored | Safe Command |")
            lines.append("|----------|-------|---------|-----------------|--------------|")
            for item in items:
                if isinstance(item, dict):
                    title   = item.get("title", "")
                    why_now = item.get("why_now", "") or item.get("why", "")
                    risk    = item.get("risk_if_ignored", "")
                    cmd     = item.get("command", "") or item.get("safe_command", "")
                    cmd_fmt = f"`{cmd}`" if cmd else "—"
                    lines.append(f"| {pri} | {title} | {why_now[:60]} | {risk[:60]} | {cmd_fmt} |")
        return "\n".join(lines)

    def _section_daily_plan(self, daily_plan: list) -> str:
        if not daily_plan:
            return "## 四、Daily Research Plan\n\n*No daily plan items.*"
        lines = ["## 四、Daily Research Plan\n",
                 "| # | Task | Category | Command | Expected Benefit | Why Now | Risk If Ignored |",
                 "|---|------|----------|---------|-----------------|---------|-----------------|"]
        for i, item in enumerate(daily_plan, 1):
            if isinstance(item, dict):
                title    = item.get("title", "")
                cat      = item.get("category", "")
                cmds     = item.get("suggested_commands", "") or item.get("command", "")
                if isinstance(cmds, list):
                    cmd = cmds[0] if cmds else ""
                else:
                    cmd = str(cmds).split("|")[0]
                cmd_fmt  = f"`{cmd}`" if cmd else "—"
                benefit  = item.get("expected_benefit", "")
                why_now  = item.get("why_now", "")
                risk     = item.get("risk_if_ignored", "")
                lines.append(f"| {i} | {title} | {cat} | {cmd_fmt} | {benefit} | {why_now[:50]} | {risk[:50]} |")
        return "\n".join(lines)

    def _section_weekly_plan(self, weekly_plan: list) -> str:
        if not weekly_plan:
            return "## 五、Weekly Research Plan\n\n*No weekly plan items.*"
        lines = ["## 五、Weekly Research Plan\n",
                 "| # | Task | Category | Command | Expected Benefit | Why Now | Risk If Ignored |",
                 "|---|------|----------|---------|-----------------|---------|-----------------|"]
        for i, item in enumerate(weekly_plan, 1):
            if isinstance(item, dict):
                title    = item.get("title", "")
                cat      = item.get("category", "")
                cmds     = item.get("suggested_commands", "") or item.get("command", "")
                if isinstance(cmds, list):
                    cmd = cmds[0] if cmds else ""
                else:
                    cmd = str(cmds).split("|")[0]
                cmd_fmt  = f"`{cmd}`" if cmd else "—"
                benefit  = item.get("expected_benefit", "")
                why_now  = item.get("why_now", "")
                risk     = item.get("risk_if_ignored", "")
                lines.append(f"| {i} | {title} | {cat} | {cmd_fmt} | {benefit} | {why_now[:50]} | {risk[:50]} |")
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

    def _section_signals_by_module(self, signals: list) -> str:
        if not signals:
            return "## 六、Signals by Module\n\n*No signals.*"
        module_map: dict = {}
        for s in signals:
            mod = (s.get("source_module") if isinstance(s, dict) else getattr(s, "source_module", "")) or "unknown"
            module_map.setdefault(mod, []).append(s)
        lines = ["## 六、Signals by Module\n"]
        for mod, sigs in sorted(module_map.items()):
            lines.append(f"\n### {mod}\n")
            lines.append("| Severity | Priority | Category | Title | Safe Hint |")
            lines.append("|----------|----------|----------|-------|-----------|")
            for s in sigs:
                sev   = (s.get("severity") if isinstance(s, dict) else getattr(s, "severity", "")) or ""
                pri   = (s.get("priority") if isinstance(s, dict) else getattr(s, "priority", "")) or ""
                cat   = (s.get("category") if isinstance(s, dict) else getattr(s, "category", "")) or ""
                title = (s.get("title") if isinstance(s, dict) else getattr(s, "title", "")) or ""
                hint  = (s.get("safe_action_hint") if isinstance(s, dict) else getattr(s, "safe_action_hint", "")) or ""
                lines.append(f"| {sev} | {pri} | {cat} | {title} | {hint} |")
        return "\n".join(lines)

    def _section_command_safety(self, recommendations: list, summary: dict) -> str:
        safe_cmds   = summary.get("safe_command_count", 0) if isinstance(summary, dict) else getattr(summary, "safe_command_count", 0)
        blocked     = summary.get("blocked_trading_action_count", 0) if isinstance(summary, dict) else getattr(summary, "blocked_trading_action_count", 0)
        lines = [
            "## 七、Command Safety\n",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Safe Commands Available | **{safe_cmds}** |",
            f"| Blocked Trading Actions | **{blocked}** (by design — no real orders) |",
            "",
        ]
        safe_recs = [r for r in recommendations if isinstance(r, dict)
                     and r.get("command_safety", "") != "BLOCKED_FOR_TRADING"
                     and r.get("suggested_commands", "")]
        if safe_recs:
            lines.append("### Safe Commands\n")
            lines.append("| Priority | Action | Command | Safety Label |")
            lines.append("|----------|--------|---------|--------------|")
            for r in safe_recs:
                pri   = r.get("priority", "")
                act   = r.get("action_type", "")
                cmds  = r.get("suggested_commands", "")
                cmd   = cmds.split("|")[0] if isinstance(cmds, str) else (cmds[0] if isinstance(cmds, list) and cmds else "")
                label = r.get("command_safety", "") or r.get("safe_command_label", "")
                cmd_fmt = f"`{cmd}`" if cmd else "—"
                lines.append(f"| {pri} | {act} | {cmd_fmt} | {label} |")
        blocked_recs = [r for r in recommendations if isinstance(r, dict)
                        and r.get("command_safety", "") == "BLOCKED_FOR_TRADING"]
        if blocked_recs:
            lines.append("\n### Blocked Actions (by design)\n")
            for r in blocked_recs:
                lines.append(f"- ~~{r.get('title', '')}~~ — BLOCKED_FOR_TRADING")
        return "\n".join(lines)

    def _section_what_not_to_do(self) -> str:
        return (
            "## 八、What Not To Do\n\n"
            "| Forbidden Action | Why |\n"
            "|------------------|-----|\n"
            "| Place real orders (BUY / SELL / ORDER) | Production trading is blocked by design |\n"
            "| Execute recommendation actions automatically | All actions require manual review |\n"
            "| Auto-trade based on signals | No auto-trading. Research intelligence only |\n"
            "| Recommend positions or allocations | No position sizing or allocation advice |\n"
            "| Auto-clear or close positions | Not connected to any broker |\n"
            "| Auto-modify ML features or model weights | Read-only. No model modification |\n\n"
            "> [!] This system generates **research actions only**: REVIEW / RESEARCH / PRACTICE / FIX_DATA / GENERATE_REPORT.\n"
            "> Never BUY, SELL, ORDER, EXECUTE, SUBMIT_ORDER, AUTO_TRADE."
        )

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
