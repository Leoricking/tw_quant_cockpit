"""
reports/local_research_assistant_report.py — LocalResearchAssistantReportBuilder for TW Quant Cockpit v1.0.8.
[!] Research Only. No Real Orders. No external API.
[!] Local assistant does not enable trading.
"""
from __future__ import annotations

import logging
import os
from datetime import date
from typing import List

logger = logging.getLogger(__name__)

_SAFETY_BANNERS = [
    "[!] Research Only. No Real Orders. Production Trading: BLOCKED.",
    "[!] Not Investment Advice.",
    "[!] No external API. No broker execution.",
    "[!] Local assistant does not enable trading.",
    "[!] VALIDATED does not enable trading.",
]

_SAMPLE_QUESTIONS = [
    "strategy validation",
    "crash reversal",
    "data hygiene",
    "release gate warning",
    "handoff guide",
    "daily workflow",
]

_ALLOWED_ACTIONS_DESCRIPTIONS = {
    "REVIEW":          "Review the relevant module or report",
    "READ_REPORT":     "Read an existing research report",
    "BACKTEST_MORE":   "Run additional backtests before deciding",
    "PRACTICE_REPLAY": "Practice with replay sessions",
    "REVIEW_JOURNAL":  "Review trading journal entries",
    "REVIEW_RISK":     "Review risk parameters and discipline",
    "REVIEW_EARNINGS": "Review earnings context for a stock",
    "REVIEW_CHIPS":    "Review chip distribution data",
    "DO_NOT_CHASE":    "Do not chase a move — wait for setup",
    "KEEP_OBSERVING":  "Continue observing without action",
    "FIX_DATA":        "Fix or clean data issues",
    "WAIT":            "Wait for clearer signals or context",
}


class LocalResearchAssistantReportBuilder:
    """Builds a Local Research Assistant report in Markdown format.

    [!] Research Only. No Real Orders. No external API.
    [!] Local assistant does not enable trading.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        mode: str = "real",
        output_dir: str = "reports",
        project_root: str = ".",
    ) -> None:
        self._mode = mode
        if not os.path.isabs(output_dir):
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_dir = os.path.join(base, output_dir)
        self._output_dir = output_dir
        if not os.path.isabs(project_root):
            project_root = os.path.abspath(project_root)
        self._root = project_root
        os.makedirs(self._output_dir, exist_ok=True)

    def build(self) -> str:
        """Build and return full Markdown report content."""
        lines: List[str] = []

        # Header
        lines += [
            "# Local Research Assistant Report v1.0.8",
            "",
            "**TW Quant Cockpit — Local Research Assistant Polish**",
            "",
        ]
        for banner in _SAFETY_BANNERS:
            lines.append(f"> {banner}")
        lines.append("")

        # 一、總覽
        lines += [
            "## 一、總覽",
            "",
            "| 項目 | 值 |",
            "|------|-----|",
            "| Version | 1.0.8 |",
            "| Research Only | True |",
            "| No Real Orders | True |",
            "| Production Trading BLOCKED | True |",
            "| Broker Execution Disabled | True |",
            "| Local Only Assistant | True |",
            "| External API Disabled | True |",
            "",
        ]

        # 二、Assistant Health
        lines += [
            "## 二、Assistant Health",
            "",
        ]
        try:
            from local_assistant.local_assistant_health import LocalResearchAssistantHealthCheck
            checker = LocalResearchAssistantHealthCheck(project_root=self._root)
            result = checker.run()
            lines += [
                f"| Check | Status | Message |",
                f"|-------|--------|---------|",
            ]
            for c in result.get("checks", []):
                name = c.get("name", "")
                status = c.get("status", "?")
                msg = c.get("message", "")
                lines.append(f"| {name} | {status} | {msg} |")
            lines += [
                "",
                f"**Overall: {result.get('overall_status', 'UNKNOWN')}** "
                f"(PASS: {result.get('pass_count', 0)}, "
                f"WARN: {result.get('warn_count', 0)}, "
                f"FAIL: {result.get('fail_count', 0)})",
                "",
            ]
        except Exception as exc:
            lines += [f"Health check error: {exc}", ""]

        # 三、Sample Questions
        lines += [
            "## 三、Sample Questions",
            "",
        ]
        try:
            from local_assistant.local_assistant_engine import LocalResearchAssistantEngine
            engine = LocalResearchAssistantEngine()
            for q in _SAMPLE_QUESTIONS:
                answer = engine.ask(question=q, limit=3)
                lines += [
                    f"### Q: {q}",
                    "",
                    f"- **Status**: {answer.status}",
                    f"- **Confidence**: {answer.confidence}",
                    f"- **Sources**: {len(answer.sources)}",
                    f"- **Answer excerpt**: {answer.answer[:200].replace(chr(10), ' ')}",
                    "",
                ]
        except Exception as exc:
            lines += [f"Sample questions error: {exc}", ""]

        # 四、Module Routing
        lines += [
            "## 四、Module Routing",
            "",
        ]
        try:
            from local_assistant.research_router import ResearchRouter, _MODULE_ROUTE_MAP
            lines += [
                "| Module | Safe Action | GUI Tab |",
                "|--------|-------------|---------|",
            ]
            for entry in _MODULE_ROUTE_MAP:
                lines.append(
                    f"| {entry['module']} | {entry['safe_action']} | {entry['suggested_gui_tab']} |"
                )
            lines.append("")
        except Exception as exc:
            lines += [f"Module routing error: {exc}", ""]

        # 五、Safe Next Steps
        lines += [
            "## 五、Safe Next Steps (ALLOWED_ACTIONS)",
            "",
            "| Action | Description |",
            "|--------|-------------|",
        ]
        for action, desc in _ALLOWED_ACTIONS_DESCRIPTIONS.items():
            lines.append(f"| {action} | {desc} |")
        lines.append("")

        # 六、Limitations
        lines += [
            "## 六、Limitations",
            "",
            "- Local KB search only — results depend on indexed local files.",
            "- No external LLM, no embedding API, no network access.",
            "- Not investment advice.",
            "- No real orders. Broker execution disabled.",
            "- Answers reflect locally indexed document summaries, not live market data.",
            "- Confidence is based on number of matching documents, not semantic quality.",
            "- VALIDATED does not enable trading.",
            "",
        ]

        # 七、安全聲明
        lines += [
            "## 七、安全聲明",
            "",
            "- **No Real Orders** — This system does not place real orders.",
            "- **No broker execution** — No broker API connection.",
            "- **No auto trading** — Automation is for research data collection only.",
            "- **Assistant does not enable trading** — The local assistant is research-only.",
            "- **Not Investment Advice** — All outputs are for research and educational purposes.",
            "",
            "---",
            "*Generated by TW Quant Cockpit v1.0.8 Local Research Assistant Polish*",
            "*[!] Research Only. No Real Orders. No external API.*",
        ]

        return "\n".join(lines)

    def save(self) -> str:
        """Save report to reports/local_research_assistant_report_YYYY-MM-DD.md."""
        today = date.today().strftime("%Y-%m-%d")
        filename = f"local_research_assistant_report_{today}.md"
        path = os.path.join(self._output_dir, filename)
        try:
            content = self.build()
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
            logger.info("Local Research Assistant report saved: %s", path)
        except Exception as exc:
            logger.warning("Report save failed: %s", exc)
        return path
