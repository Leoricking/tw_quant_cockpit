"""reports/replay_training_report.py — ReplayTrainingReport for TW Replay Training Cockpit v0.5.6.

Generates 9-section Markdown report.

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ReplayTrainingReport:
    """Generates a Markdown report for a TW Replay Training Cockpit session.

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    VERSION = "v0.5.6"

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def generate(
        self,
        session=None,
        markers: Optional[list] = None,
        mistakes: Optional[list] = None,
        ai_review=None,
        score: Optional[dict] = None,
        drills: Optional[List[dict]] = None,
        mode: str = "real",
    ) -> str:
        """Generate full Markdown report string."""
        markers  = markers  or []
        mistakes = mistakes or []
        drills   = drills   or []
        score    = score    or {}

        lines = []
        lines += self._section_header(session, mode)
        lines += self._section_overview(session, score, mistakes, drills)
        lines += self._section_session(session)
        lines += self._section_markers(markers)
        lines += self._section_ai_review(ai_review)
        lines += self._section_tape_reading(ai_review)
        lines += self._section_score(score)
        lines += self._section_drills(drills)
        lines += self._section_journal(ai_review)
        lines += self._section_safety()
        return "\n".join(lines) + "\n"

    def save(self, content: str, report_dir: str = "reports") -> str:
        """Save report to file. Returns absolute path."""
        try:
            abs_dir = os.path.join(BASE_DIR, report_dir)
            os.makedirs(abs_dir, exist_ok=True)
            ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(abs_dir, f"replay_training_report_{ts}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("[ReplayTrainingReport] saved → %s", path)
            return path
        except Exception as exc:
            logger.error("[ReplayTrainingReport] save error: %s", exc)
            return ""

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_header(self, session, mode: str) -> list:
        symbol     = session.symbol     if session else "N/A"
        trade_date = session.trade_date if session else "N/A"
        return [
            f"# TW Replay Training Cockpit Report",
            f"",
            f"> **{self.VERSION}** | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} "
            f"| Mode: {mode.upper()}",
            f">",
            f"> [!] **Replay Training Only | Research Only | No Real Orders | "
            f"Production Trading BLOCKED**",
            f">",
            f"> Symbol: {symbol} | Date: {trade_date}",
            f"",
            f"---",
            f"",
        ]

    def _section_overview(self, session, score: dict, mistakes: list, drills: list) -> list:
        symbol     = session.symbol     if session else "N/A"
        trade_date = session.trade_date if session else "N/A"
        timeframe  = session.timeframe  if session else "N/A"
        total_score = score.get("total_score", 0.0)
        grade       = score.get("grade", "N/A")
        n_mistakes  = len(mistakes)
        n_drills    = len(drills)
        return [
            f"## 一、總覽",
            f"",
            f"| 項目 | 值 |",
            f"|------|---|",
            f"| Version | {self.VERSION} |",
            f"| Replay Training Only | True |",
            f"| Research Only | True |",
            f"| No Real Orders | True |",
            f"| Symbol | {symbol} |",
            f"| Date | {trade_date} |",
            f"| Timeframe | {timeframe} |",
            f"| Score | {total_score:.1f}/100 ({grade}) |",
            f"| Mistakes Detected | {n_mistakes} |",
            f"| Drills Suggested | {n_drills} |",
            f"",
            f"---",
            f"",
        ]

    def _section_session(self, session) -> list:
        if session is None:
            return ["## 二、Replay Session", "", "*No session data.*", "", "---", ""]
        d = session.to_dict() if hasattr(session, "to_dict") else {}
        return [
            f"## 二、Replay Session",
            f"",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Symbol | {d.get('symbol', 'N/A')} |",
            f"| Trade Date | {d.get('trade_date', 'N/A')} |",
            f"| Timeframe | {d.get('timeframe', 'N/A')} |",
            f"| Total Bars | {d.get('total_bars', 0)} |",
            f"| Current Bar | {d.get('current_bar_index', 0)} |",
            f"| Hidden Future Data | {d.get('hidden_future_data', True)} |",
            f"| Replay Speed | {d.get('replay_speed', 1)}x |",
            f"| Status | {d.get('status', 'N/A')} |",
            f"| Mode | {d.get('mode', 'real')} |",
            f"",
            f"---",
            f"",
        ]

    def _section_markers(self, markers: list) -> list:
        lines = [
            f"## 三、User Markers / Notes",
            f"",
        ]
        if not markers:
            lines += ["*No markers placed.*", "", "---", ""]
            return lines
        lines += [
            f"| Marker ID | Type | Bar Time | Price | Note |",
            f"|-----------|------|----------|-------|------|",
        ]
        for m in markers:
            d = m.to_dict() if hasattr(m, "to_dict") else {}
            lines.append(
                f"| {d.get('marker_id', '')} | {d.get('marker_type', '')} | "
                f"{d.get('bar_time', '')} | {d.get('price', 0):.2f} | "
                f"{d.get('note', '')} |"
            )
        lines += ["", "---", ""]
        return lines

    def _section_ai_review(self, ai_review) -> list:
        if ai_review is None:
            return ["## 四、AI Replay Review", "", "*No AI review data.*", "", "---", ""]
        d = ai_review.to_dict() if hasattr(ai_review, "to_dict") else {}
        return [
            f"## 四、AI Replay Review",
            f"",
            f"**Summary:** {d.get('summary', 'N/A')}",
            f"",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Best Entry | {d.get('best_entry', 'N/A')} |",
            f"| Worst Entry | {d.get('worst_entry', 'N/A')} |",
            f"| Best Exit | {d.get('best_exit', 'N/A')} |",
            f"| Worst Exit | {d.get('worst_exit', 'N/A')} |",
            f"| Detected Mistakes | {d.get('detected_mistakes', 'None')} |",
            f"| Strategy Violations | {d.get('strategy_violations', 'None')} |",
            f"| Next Training Focus | {d.get('next_training_focus', 'N/A')} |",
            f"",
            f"---",
            f"",
        ]

    def _section_tape_reading(self, ai_review) -> list:
        if ai_review is None:
            return ["## 五、Tape Reading Feedback", "", "*No feedback.*", "", "---", ""]
        d = ai_review.to_dict() if hasattr(ai_review, "to_dict") else {}
        feedback = d.get("tape_reading_feedback", "N/A")
        return [
            f"## 五、Tape Reading Feedback",
            f"",
            f"{feedback}",
            f"",
            f"---",
            f"",
        ]

    def _section_score(self, score: dict) -> list:
        if not score:
            return ["## 六、Replay Score", "", "*No score data.*", "", "---", ""]
        breakdown = score.get("breakdown", {})
        lines = [
            f"## 六、Replay Score",
            f"",
            f"**Total Score:** {score.get('total_score', 0):.1f}/100 — "
            f"Grade: **{score.get('grade', 'N/A')}**",
            f"",
            f"*{score.get('interpretation', '')}*",
            f"",
            f"| Component | Score |",
            f"|-----------|-------|",
        ]
        for k, v in breakdown.items():
            lines.append(f"| {k.replace('_', ' ').title()} | {v:.1f} |")
        lines += ["", "---", ""]
        return lines

    def _section_drills(self, drills: list) -> list:
        lines = ["## 七、Next Training Drills", ""]
        if not drills:
            lines += ["*No drills suggested.*", "", "---", ""]
            return lines
        for i, d in enumerate(drills, 1):
            lines += [
                f"### Drill {i}: {d.get('drill_name', 'N/A')}",
                f"",
                f"- **Reason:** {d.get('reason', 'N/A')}",
                f"- **Focus Points:** {d.get('focus_points', 'N/A')}",
                f"- **Expected Skill:** {d.get('expected_skill', 'N/A')}",
                f"- **Priority:** {d.get('priority', 'N/A')}",
                f"",
            ]
        lines += ["---", ""]
        return lines

    def _section_journal(self, ai_review) -> list:
        return [
            f"## 八、Journal / Coach Integration",
            f"",
            f"- Journal Export: Research/Replay Training entry only. No real trade data.",
            f"- Coach Task: Review mistakes in next session.",
            f"- Suggested Focus: "
            + (getattr(ai_review, "next_training_focus", "General practice") if ai_review else "General practice"),
            f"",
            f"---",
            f"",
        ]

    def _section_safety(self) -> list:
        return [
            f"## 九、安全聲明",
            f"",
            f"| 聲明 | 狀態 |",
            f"|------|------|",
            f"| Replay Training Only | TRUE |",
            f"| Research Only | TRUE |",
            f"| No Real Orders | TRUE |",
            f"| No Broker Execution | TRUE |",
            f"| No Auto Trading | TRUE |",
            f"| Production Blocked | TRUE |",
            f"| Real Order Ready | FALSE |",
            f"",
            f"> [!] This report is for replay training and research simulation only. "
            f"No real orders are placed. No broker is connected. "
            f"Not investment advice.",
        ]
