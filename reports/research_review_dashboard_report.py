"""
reports/research_review_dashboard_report.py — Research Review Dashboard Report (v0.4.7).

Generates a Markdown research review dashboard report.

Output: reports/research_review_dashboard_report_YYYY-MM-DD.md

[!] Review Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchReviewDashboardReport:
    """
    Generates the Research Review Dashboard Markdown report.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __init__(
        self,
        report_dir: str = "reports",
        output_dir: str = "data/backtest_results/research_review",
    ):
        self._report_dir = os.path.join(BASE_DIR, report_dir)
        self._output_dir = os.path.join(BASE_DIR, output_dir)
        os.makedirs(self._report_dir, exist_ok=True)

    def generate(
        self,
        summary:     dict,
        scorecard:   dict,
        review_items: List,
        action_plan: List[dict],
        mode:        str = "real",
        period:      str = "daily",
    ) -> str:
        """
        Build and write the Markdown report.

        Returns the output file path.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"research_review_dashboard_report_{today}.md"
        path = os.path.join(self._report_dir, filename)

        lines = []
        lines += self._header(summary, mode, period)
        lines += self._section_overview(summary)
        lines += self._section_scorecard(scorecard)
        lines += self._section_top_mistakes(summary)
        lines += self._section_weak_rules(summary, review_items)
        lines += self._section_data_blockers(summary, review_items)
        lines += self._section_model_monitoring(summary, review_items)
        lines += self._section_replay_training(summary, review_items)
        lines += self._section_journal_review(summary, review_items)
        lines += self._section_action_plan(action_plan)
        lines += self._section_safety()

        content = "\n".join(lines)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("[report] Research Review Dashboard report: %s", path)
        except Exception as exc:
            logger.warning("[report] Failed to write report: %s", exc)
        return path

    # ------------------------------------------------------------------
    # Section builders
    # ------------------------------------------------------------------

    def _header(self, summary: dict, mode: str, period: str) -> List[str]:
        generated = summary.get("generated_at", datetime.now().isoformat(timespec="seconds"))
        return [
            "# Research Review Dashboard Report",
            "",
            f"> **[!] Review Only | Research Only | No Real Orders | Production Trading: BLOCKED**",
            "",
            f"- **Generated:** {generated}",
            f"- **Mode:** {mode}",
            f"- **Period:** {period}",
            "",
        ]

    def _section_overview(self, summary: dict) -> List[str]:
        lines = [
            "## 一、總覽",
            "",
            f"| 項目 | 值 |",
            f"|------|-----|",
            f"| Mode | {summary.get('mode', '-')} |",
            f"| Period | {summary.get('period', '-')} |",
            f"| Review Only | Yes |",
            f"| Research Only | Yes |",
            f"| No Real Orders | Yes |",
            f"| Overall Review Score | {summary.get('overall_review_score', '-')} |",
            f"| Open Items | {summary.get('open_items', 0)} |",
            f"| Critical | {summary.get('critical_items', 0)} |",
            f"| Warnings | {summary.get('warning_items', 0)} |",
            f"| Action Items | {summary.get('action_items_count', 0)} |",
            "",
        ]
        return lines

    def _section_scorecard(self, scorecard: dict) -> List[str]:
        if not scorecard:
            return ["## 二、Daily / Weekly Scorecard", "", "_Scorecard not available._", ""]

        def row(area, score_key, grade_key):
            score = scorecard.get(score_key, "-")
            grade = scorecard.get(grade_key, "-")
            return f"| {area} | {score} | {grade} |"

        lines = [
            "## 二、Daily / Weekly Scorecard",
            "",
            "| Area | Score | Grade |",
            "|------|-------|-------|",
            row("Process Quality",    "process_quality_score",     "process_quality_grade"),
            row("Data Health",        "data_health_score",         "data_health_grade"),
            row("Signal Health",      "signal_health_score",       "signal_health_grade"),
            row("Rule Health",        "rule_health_score",         "rule_health_grade"),
            row("Model Health",       "model_health_score",        "model_health_grade"),
            row("Replay Training",    "replay_training_score",     "replay_training_grade"),
            row("Journal Completion", "journal_completion_score",  "journal_completion_grade"),
            row("Safety",             "safety_score",              "safety_grade"),
            f"| **Overall** | **{scorecard.get('overall_review_score', '-')}** | **{scorecard.get('overall_grade', '-')}** |",
            "",
        ]
        return lines

    def _section_top_mistakes(self, summary: dict) -> List[str]:
        mistakes = summary.get("top_mistakes", [])
        lines = ["## 三、Top Mistakes", ""]
        if not mistakes:
            lines += ["_No repeated mistakes found._", ""]
            return lines
        lines += ["| Mistake Tag | Note |", "|-------------|------|"]
        for m in mistakes:
            lines.append(f"| {m} | Practice intraday replay |")
        lines += [
            "",
            f"- **Most common:** {summary.get('most_common_mistake', '-')}",
            "- Suggested practice: `python main.py intraday-replay --mode real`",
            "",
        ]
        return lines

    def _section_weak_rules(self, summary: dict, review_items: List) -> List[str]:
        weak_count = summary.get("weak_rules", 0)
        lines = ["## 四、Weak Rules", ""]
        if weak_count == 0:
            lines += ["_No weak rules requiring review._", ""]
            return lines
        lines += [
            f"- **Rules needing review:** {weak_count}",
            "- Categories: low confidence / insufficient sample / experimental",
            "- **No auto rule status changes.**",
            "- Suggested: `python main.py rule-governance --mode real`",
            "",
        ]
        return lines

    def _section_data_blockers(self, summary: dict, review_items: List) -> List[str]:
        blockers = summary.get("data_blockers", 0)
        lines = ["## 五、Data Blockers", ""]
        if blockers == 0:
            lines += ["_No data blockers detected._", ""]
            return lines
        lines += [
            f"- **Data quality blockers:** {blockers}",
            "- Suggested: `python main.py data-quality-gate --mode real`",
            f"- Provider warnings: {summary.get('provider_warnings', 0)}",
            "- Suggested: `python main.py provider-reliability --mode real`",
            "",
        ]
        return lines

    def _section_model_monitoring(self, summary: dict, review_items: List) -> List[str]:
        model_warns = summary.get("model_warnings", 0)
        lines = ["## 六、Model Monitoring", ""]
        if model_warns == 0:
            lines += ["_No model drift or degradation warnings._", ""]
            return lines
        lines += [
            f"- **Drift warnings:** {model_warns}",
            "- Suggested: `python main.py model-monitoring --mode real`",
            "- Suggested: `python main.py model-monitoring-report --mode real`",
            "",
        ]
        return lines

    def _section_replay_training(self, summary: dict, review_items: List) -> List[str]:
        overdue = summary.get("replay_training_overdue", False)
        lines = ["## 七、Replay Training Focus", ""]
        if not overdue:
            lines += ["_Replay training is current._", ""]
            return lines
        lines += [
            "- **Training overdue** — practice recommended",
            "- Scenarios to practice:",
            "  - Fake breakout",
            "  - VWAP loss / reclaim",
            "  - Opening range",
            "- Suggested: `python main.py intraday-replay --mode real`",
            "",
        ]
        return lines

    def _section_journal_review(self, summary: dict, review_items: List) -> List[str]:
        review_req = summary.get("journal_review_required", 0)
        lines = ["## 八、Journal Review", ""]
        if review_req == 0:
            lines += ["_All journal entries reviewed._", ""]
            return lines
        lines += [
            f"- **Entries requiring review:** {review_req}",
            f"- **Open simulated trades:** {summary.get('open_simulated', 0)}",
            "- Suggested: `python main.py journal-summary`",
            "",
        ]
        return lines

    def _section_action_plan(self, action_plan: List[dict]) -> List[str]:
        lines = ["## 九、Action Plan", ""]
        if not action_plan:
            lines += ["_No action items._", ""]
            return lines
        lines += [
            "| Priority | Action Type | Title | Suggested Command |",
            "|----------|-------------|-------|-------------------|",
        ]
        for a in action_plan[:20]:
            p    = a.get("priority", "-")
            atype = a.get("action_type", "-")
            title = a.get("title", "-")[:60]
            cmd  = a.get("suggested_command", "")[:80]
            lines.append(f"| P{p} | {atype} | {title} | `{cmd}` |")
        lines += [
            "",
            "> **No trading actions included. All actions are research-only.**",
            "",
        ]
        return lines

    def _section_safety(self) -> List[str]:
        return [
            "## 十、安全聲明",
            "",
            "| 項目 | 值 |",
            "|------|-----|",
            "| Review Only | Yes |",
            "| Research Only | Yes |",
            "| No Real Orders | Yes |",
            "| Production Trading | BLOCKED |",
            "| REAL_ORDER_READY | False |",
            "",
            "> This report is for research and review purposes only.",
            "> It is NOT investment advice.",
            "> Production trading is permanently blocked.",
            "> No real orders are placed, no positions modified.",
            "",
        ]
