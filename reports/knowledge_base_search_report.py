"""
reports/knowledge_base_search_report.py — KnowledgeBaseSearchReportBuilder for TW Quant Cockpit v1.0.7.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Knowledge Base Search. No broker execution. Search does not enable trading.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

_SAFETY_BANNER = (
    "[!] Research Only. No Real Orders. Production Trading: BLOCKED.\n"
    "[!] Search does not enable trading. Broker Execution Disabled."
)

_SAMPLE_QUERIES = [
    "research cockpit",
    "strategy validation",
    "crash reversal",
    "data hygiene",
    "release gate",
    "safety",
    "handoff",
    "template",
]


class KnowledgeBaseSearchReportBuilder:
    """Build and save the Knowledge Base Search report.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Search does not enable trading.
    """

    no_real_orders     = True
    broker_disabled    = True
    research_only      = True
    production_blocked = True

    def __init__(
        self,
        mode: str = "real",
        output_dir: str = "reports",
        project_root: str = ".",
    ) -> None:
        self._mode        = mode
        self._output_dir  = os.path.abspath(output_dir)
        self._project_root = os.path.abspath(project_root)
        self._generated_at = datetime.now().isoformat()

    def build(self) -> str:
        """Return the full markdown report content."""
        sections = [
            self._section_header(),
            self._section_overview(),
            self._section_index_summary(),
            self._section_search_coverage(),
            self._section_sample_searches(),
            self._section_safe_search_summary(),
            self._section_health_check(),
            self._section_safety_declaration(),
        ]
        return "\n\n".join(sections)

    def save(self) -> str:
        """Save report to reports/knowledge_base_search_report_YYYY-MM-DD.md; return path."""
        os.makedirs(self._output_dir, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"knowledge_base_search_report_{date_str}.md"
        path = os.path.join(self._output_dir, filename)
        content = self.build()
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        logger.info("KnowledgeBaseSearchReportBuilder: saved to %s", path)
        return path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_header(self) -> str:
        return (
            "# Knowledge Base Search Report v1.0.7\n\n"
            f"> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**\n"
            f"> **[!] Search does not enable trading. Broker Execution Disabled.**\n\n"
            f"**Generated:** {self._generated_at}  \n"
            f"**Mode:** {self._mode}  \n"
            f"**Version:** 1.0.7 Knowledge Base Search Polish"
        )

    def _section_overview(self) -> str:
        return (
            "## 一、總覽 (Overview)\n\n"
            "| 項目 | 狀態 |\n"
            "|------|------|\n"
            "| Version | 1.0.7 |\n"
            "| Research Only | True |\n"
            "| No Real Orders | True |\n"
            "| Production Trading BLOCKED | True |\n"
            "| Broker Execution Disabled | True |\n"
            "| Knowledge Base Search Release | True |\n"
            "| Knowledge Base Index Available | True |\n"
            "| Safe Search Summary Available | True |"
        )

    def _section_index_summary(self) -> str:
        try:
            from knowledge_base.kb_summary import KnowledgeBaseSummaryBuilder
            builder = KnowledgeBaseSummaryBuilder()
            summary = builder.build_summary()
            return (
                "## 二、Index Summary\n\n"
                "| 項目 | 數量 |\n"
                "|------|------|\n"
                f"| Total Items | {summary.total_items} |\n"
                f"| Docs | {summary.docs_count} |\n"
                f"| Examples | {summary.examples_count} |\n"
                f"| Templates | {summary.templates_count} |\n"
                f"| Reports | {summary.reports_count} |\n"
                f"| Safety Docs | {summary.safety_docs_count} |\n"
                f"| Modules | {summary.modules_count} |"
            )
        except Exception as exc:
            return f"## 二、Index Summary\n\n_Index summary unavailable: {exc}_"

    def _section_search_coverage(self) -> str:
        root = self._project_root
        checks = [
            ("docs/", os.path.isdir(os.path.join(root, "docs"))),
            ("docs/examples/", os.path.isdir(os.path.join(root, "docs", "examples"))),
            ("docs/templates/", os.path.isdir(os.path.join(root, "docs", "templates"))),
            ("reports/", os.path.isdir(os.path.join(root, "reports"))),
            ("gui/navigation/tab_registry.py", os.path.isfile(os.path.join(root, "gui", "navigation", "tab_registry.py"))),
            ("strategy_memory/", os.path.isdir(os.path.join(root, "strategy_memory"))),
            ("evidence_graph/", os.path.isdir(os.path.join(root, "evidence_graph"))),
        ]
        rows = "\n".join(
            f"| {name} | {'OK' if found else 'MISSING'} |"
            for name, found in checks
        )
        return (
            "## 三、Search Coverage\n\n"
            "| 路徑 | 狀態 |\n"
            "|------|------|\n"
            + rows
        )

    def _section_sample_searches(self) -> str:
        lines = ["## 四、Sample Searches\n"]
        try:
            from knowledge_base.kb_search_engine import KnowledgeBaseSearchEngine
            engine = KnowledgeBaseSearchEngine()
            for q in _SAMPLE_QUERIES:
                results = engine.search(q, limit=3)
                lines.append(f"### Query: `{q}`\n")
                if results:
                    for r in results:
                        lines.append(f"- [{r.title}]({r.path}) — Score: {r.score:.1f} | {r.category} | {r.safe_next_step}")
                else:
                    lines.append("_No results_")
                lines.append("")
        except Exception as exc:
            lines.append(f"_Sample searches unavailable: {exc}_")
        return "\n".join(lines)

    def _section_safe_search_summary(self) -> str:
        lines = [
            "## 五、Safe Search Summary\n",
            "**Allowed next steps (research-only):**\n",
        ]
        from knowledge_base.kb_schema import SAFE_NEXT_STEPS
        for step in SAFE_NEXT_STEPS:
            lines.append(f"- `{step}`")
        lines.append("")
        lines.append("**Forbidden (never output):** BUY / SELL / ORDER / EXECUTE / SUBMIT_ORDER / AUTO_TRADE / REAL_TRADE / LIVE_TRADE / BROKER_ORDER\n")
        lines.append("> **No Real Orders.** Search does not enable trading. Broker Execution Disabled.")
        return "\n".join(lines)

    def _section_health_check(self) -> str:
        lines = ["## 六、Health Check\n"]
        try:
            from knowledge_base.kb_health_check import KnowledgeBaseHealthCheck
            checker = KnowledgeBaseHealthCheck(project_root=self._project_root)
            result = checker.run()
            checks = result.get("checks", [])
            lines.append("| Status | Check | Message |")
            lines.append("|--------|-------|---------|")
            for c in checks:
                lines.append(f"| {c['status']} | {c['name']} | {c['message']} |")
            lines.append("")
            lines.append(f"**Overall:** {result.get('overall_status', 'UNKNOWN')} | "
                         f"PASS: {result.get('pass_count', 0)} | "
                         f"WARN: {result.get('warn_count', 0)} | "
                         f"FAIL: {result.get('fail_count', 0)}")
        except Exception as exc:
            lines.append(f"_Health check unavailable: {exc}_")
        return "\n".join(lines)

    def _section_safety_declaration(self) -> str:
        return (
            "## 七、安全聲明\n\n"
            "- **No Real Orders** — 所有操作為研究用途，無真實訂單\n"
            "- **No broker execution** — 不連接任何券商 API\n"
            "- **No auto trading** — 不自動執行任何交易\n"
            "- **Search does not enable trading** — 搜尋功能不開啟交易\n"
            "- **Production Trading BLOCKED** — 生產交易已封鎖\n"
            "- **VALIDATED does not enable trading** — 驗證不等於交易授權\n"
            "- **Not Investment Advice** — 非投資建議\n\n"
            "> _TW Quant Cockpit v1.0.7 — Knowledge Base Search Polish — Research Only_"
        )
