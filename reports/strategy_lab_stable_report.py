"""
reports/strategy_lab_stable_report.py — StrategyLabStableReportBuilder v0.9.0

Generate the Strategy Lab Stable Markdown report.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import glob
import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_OUTPUT_DIR       = os.path.join(BASE_DIR, "reports")
_DEFAULT_LAB_OUTPUT       = "data/backtest_results/strategy_lab"


class StrategyLabStableReportBuilder:
    """Generate the v0.9.0 Strategy Lab Stable Markdown report.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    [!] Not Investment Advice. No BUY/SELL/ORDER output.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def build(
        self,
        mode: str = "real",
        output_dir: str = _DEFAULT_OUTPUT_DIR,
        lab_output_dir: str = _DEFAULT_LAB_OUTPUT,
    ) -> str:
        """Build the report. Returns path to generated Markdown file."""
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        if not os.path.isabs(lab_output_dir):
            lab_output_dir = os.path.join(BASE_DIR, lab_output_dir)

        data = self._load_or_run(mode=mode, lab_output_dir=lab_output_dir)

        capabilities = data.get("capabilities", [])
        checks       = data.get("checks", [])
        summary      = data.get("summary")
        manifest     = data.get("manifest", {})

        lines   = self._build_lines(capabilities, checks, summary, manifest, mode)
        content = "\n".join(lines) + "\n"

        os.makedirs(output_dir, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        path  = os.path.join(output_dir, f"strategy_lab_stable_report_{today}.md")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("StrategyLabStableReportBuilder: report written -> %s", path)
        except Exception as exc:
            logger.warning("StrategyLabStableReportBuilder: write error: %s", exc)
        return path

    # ------------------------------------------------------------------
    # Load or run
    # ------------------------------------------------------------------

    def _load_or_run(self, mode: str, lab_output_dir: str) -> dict:
        try:
            from strategy_lab.strategy_lab_store import StrategyLabStore
            from strategy_lab.strategy_lab_schema import StrategyLabCapability, StrategyLabCheck
            store   = StrategyLabStore(output_dir=lab_output_dir)
            caps_raw  = store.load_capabilities()
            chks_raw  = store.load_latest_checks()
            summary   = store.load_latest_summary()
            if caps_raw and chks_raw and summary:
                capabilities = [StrategyLabCapability.from_dict(d) for d in caps_raw]
                checks       = [StrategyLabCheck.from_dict(d) for d in chks_raw]
                return {"capabilities": capabilities, "checks": checks,
                        "summary": summary, "manifest": {}}
        except Exception as exc:
            logger.warning("StrategyLabStableReportBuilder: store load error: %s", exc)

        try:
            from strategy_lab.strategy_lab_engine import StrategyLabEngine
            engine = StrategyLabEngine(project_root=BASE_DIR, output_dir=lab_output_dir)
            return engine.run(mode=mode)
        except Exception as exc:
            logger.warning("StrategyLabStableReportBuilder: engine run error: %s", exc)
            return {"capabilities": [], "checks": [], "summary": None, "manifest": {}}

    # ------------------------------------------------------------------
    # Build Markdown
    # ------------------------------------------------------------------

    def _build_lines(self, capabilities, checks, summary, manifest, mode) -> List[str]:
        lines: List[str] = []
        lines += self._section_header()
        lines += self._section_release_overview(summary, manifest)
        lines += self._section_capability_matrix(capabilities)
        lines += self._section_stable_checklist(checks, summary)
        lines += self._section_safety_audit(summary)
        lines += self._section_ri_layer()
        lines += self._section_sm_layer()
        lines += self._section_bc_layer()
        lines += self._section_tm_layer()
        lines += self._section_eg_layer()
        lines += self._section_regression_report_data()
        lines += self._section_known_limitations()
        lines += self._section_next_roadmap()
        lines += self._section_safety_declaration()
        return lines

    def _section_header(self) -> List[str]:
        today = datetime.now().strftime("%Y-%m-%d")
        return [
            "# Strategy Lab Stable Report v0.9.0",
            "",
            f"**Date:** {today}",
            "",
            "> **[!] Research Only. No Real Orders. Production Trading BLOCKED.**",
            "> **[!] Not Investment Advice.**",
            "> **[!] No BUY/SELL/ORDER output.**",
            "",
            "---",
            "",
        ]

    def _section_release_overview(self, summary, manifest) -> List[str]:
        lines = ["## 一、Release Overview", ""]
        if summary and hasattr(summary, "version"):
            lines += [
                "| Field | Value |",
                "|-------|-------|",
                f"| Version | {summary.version} |",
                f"| Release Name | {summary.release_name} |",
                f"| Previous Version | v0.8.3 |",
                f"| Mode | {summary.mode} |",
                f"| Overall Status | **{summary.overall_status}** |",
                f"| Generated At | {summary.generated_at} |",
                f"| Research Only | True |",
                f"| No Real Orders | True |",
                f"| Production Trading | BLOCKED |",
            ]
        else:
            lines += ["*(No summary available — run: python main.py strategy-lab --mode real)*"]
        lines += ["", "---", ""]
        return lines

    def _section_capability_matrix(self, capabilities) -> List[str]:
        lines = [
            "## 二、Strategy Lab Capability Matrix",
            "",
            f"**Total Capabilities:** {len(capabilities)}",
            "",
        ]
        if capabilities:
            lines += [
                "| Capability | Category | Status | Maturity | CLI | GUI | Report | Regression |",
                "|-----------|----------|--------|----------|-----|-----|--------|------------|",
            ]
            for cap in capabilities:
                cli = (cap.cli_commands[0][:30] if cap.cli_commands else "—")
                gui = (cap.gui_tabs[0][:20] if cap.gui_tabs else "—")
                rpt = (cap.reports[0][:25] if cap.reports else "—")
                reg = (cap.regression_suites[0][:20] if cap.regression_suites else "—")
                lines.append(
                    f"| {cap.name[:35]} | {cap.category[:18]} | {cap.stable_status} "
                    f"| {cap.maturity} | {cli} | {gui} | {rpt} | {reg} |"
                )
        else:
            lines.append("*(No capabilities loaded)*")
        lines += ["", "---", ""]
        return lines

    def _section_stable_checklist(self, checks, summary) -> List[str]:
        lines = ["## 三、Stable Checklist", ""]
        if summary and hasattr(summary, "total_checks"):
            lines += [
                f"- Total: {summary.total_checks}",
                f"- PASS: {summary.pass_count}",
                f"- WARN: {summary.warn_count}",
                f"- FAIL: {summary.fail_count}",
                f"- BLOCKED: {summary.blocked_check_count}",
                f"- Overall Status: **{summary.overall_status}**",
                "",
            ]
        if checks:
            lines += [
                "| Category | Check | Status | Severity | Message |",
                "|----------|-------|--------|----------|---------|",
            ]
            for chk in checks[:50]:
                msg = (chk.message[:60] + "...") if len(chk.message) > 60 else chk.message
                lines.append(
                    f"| {chk.category} | {chk.name[:40]} | {chk.status} "
                    f"| {chk.severity} | {msg} |"
                )
        else:
            lines.append("*(No checks loaded — run: python main.py strategy-lab --mode real)*")
        lines += ["", "---", ""]
        return lines

    def _section_safety_audit(self, summary) -> List[str]:
        lines = ["## 四、Safety Audit", ""]
        if summary and hasattr(summary, "recommendations_safe"):
            lines += [
                "| Safety Item | Status |",
                "|-------------|--------|",
                f"| Recommendations Safe | {summary.recommendations_safe} |",
                f"| Memories Safe | {summary.memories_safe} |",
                f"| Coach Tasks Safe | {summary.coach_tasks_safe} |",
                f"| Training Metrics Safe | {summary.metrics_safe} |",
                f"| Evidence Graph Safe | {summary.evidence_graph_safe} |",
                f"| Forbidden Action Count | {summary.forbidden_action_count} |",
                f"| No Real Orders | {summary.no_real_orders} |",
                f"| Production Trading BLOCKED | {summary.production_blocked} |",
            ]
        else:
            lines += [
                "| Safety Item | Status |",
                "|-------------|--------|",
                "| No Real Orders | True |",
                "| Production Trading BLOCKED | True |",
                "| Forbidden Action Count | 0 |",
            ]
        lines += [
            "",
            "**Broker connection:** DISABLED",
            "**Real order execution:** BLOCKED",
            "**Auto-trading:** NOT IMPLEMENTED",
            "",
            "---",
            "",
        ]
        return lines

    def _section_ri_layer(self) -> List[str]:
        return [
            "## 五、Research Intelligence Layer",
            "",
            "The Research Intelligence layer aggregates signals from 8 source modules,",
            "builds research recommendations, and generates daily/weekly research plans.",
            "",
            "**Status: STABLE** (v0.7.0–v0.7.1)",
            "",
            "**Key CLI commands:**",
            "- `python main.py research-intelligence --mode real`",
            "- `python main.py research-intelligence-summary`",
            "- `python main.py research-intelligence-recommendations`",
            "- `python main.py research-intelligence-priority`",
            "- `python main.py research-intelligence-daily-plan`",
            "- `python main.py research-intelligence-weekly-plan`",
            "- `python main.py research-intelligence-report`",
            "",
            "---",
            "",
        ]

    def _section_sm_layer(self) -> List[str]:
        return [
            "## 六、Strategy Memory Layer",
            "",
            "The Strategy Memory layer extracts and persists 10 memory types.",
            "Status lifecycle: NEW → REVIEWING → VALIDATING → ACCEPTED/REJECTED/NEEDS_MORE_EVIDENCE.",
            "ACCEPTED = research accepted only. ACCEPTED ≠ trading enabled.",
            "",
            "**Status: STABLE** (v0.7.2–v0.8.1)",
            "",
            "**Key CLI commands:**",
            "- `python main.py strategy-memory --mode real`",
            "- `python main.py strategy-memory-summary`",
            "- `python main.py strategy-memory-validation-queue`",
            "- `python main.py strategy-memory-active-threads`",
            "- `python main.py strategy-memory-repeated-patterns`",
            "- `python main.py strategy-memory-report`",
            "",
            "---",
            "",
        ]

    def _section_bc_layer(self) -> List[str]:
        return [
            "## 七、Backtest Coach Layer",
            "",
            "The Backtest Coach layer converts backtest weaknesses into safe coach training tasks.",
            "Task types: PRACTICE_REPLAY, REVIEW_RULE, REVIEW_JOURNAL, FIX_DATA, BACKTEST_MORE,",
            "READ_REPORT, UPDATE_MEMORY, WAIT — no trading actions.",
            "",
            "**Status: STABLE** (v0.7.3)",
            "",
            "**Key CLI commands:**",
            "- `python main.py backtest-coach --mode real`",
            "- `python main.py backtest-coach-summary`",
            "- `python main.py backtest-coach-tasks`",
            "- `python main.py backtest-coach-daily-plan`",
            "- `python main.py backtest-coach-weekly-plan`",
            "- `python main.py backtest-coach-report`",
            "",
            "---",
            "",
        ]

    def _section_tm_layer(self) -> List[str]:
        return [
            "## 八、Training Metrics Layer",
            "",
            "The Training Metrics layer measures training effectiveness across all Research OS modules.",
            "Metric types: TASK_COMPLETION, REPLAY_SCORE, MISTAKE_REDUCTION, BACKTEST_ISSUE,",
            "JOURNAL_IMPROVEMENT, MEMORY_VALIDATION, RULE_REVIEW, DATA_FIX_PROGRESS,",
            "TRAINING_STREAK, QUALITY_SCORE.",
            "",
            "**Status: USABLE** (v0.8.2)",
            "",
            "**Key CLI commands:**",
            "- `python main.py training-metrics --mode real`",
            "- `python main.py training-metrics-summary`",
            "- `python main.py training-metrics-detail`",
            "- `python main.py training-metrics-trend`",
            "- `python main.py training-metrics-report`",
            "",
            "---",
            "",
        ]

    def _section_eg_layer(self) -> List[str]:
        return [
            "## 九、Evidence Graph Layer",
            "",
            "The Evidence Graph links all research conclusions into a traceable directed graph.",
            "14 node types. 12 edge relations. Evidence Threads via BFS max depth 3.",
            "Conservative contradiction detection. Never auto-modifies any module status.",
            "",
            "**Status: USABLE** (v0.8.3)",
            "",
            "**Key CLI commands:**",
            "- `python main.py evidence-graph --mode real`",
            "- `python main.py evidence-graph-summary`",
            "- `python main.py evidence-graph-nodes`",
            "- `python main.py evidence-graph-edges`",
            "- `python main.py evidence-graph-threads`",
            "- `python main.py evidence-graph-orphans`",
            "- `python main.py evidence-graph-requires-backtest`",
            "- `python main.py evidence-graph-requires-data`",
            "- `python main.py evidence-graph-report`",
            "",
            "---",
            "",
        ]

    def _section_regression_report_data(self) -> List[str]:
        return [
            "## 十、Regression / Report / Data Coverage",
            "",
            "**Release Gate:**",
            "- `python main.py regression-run --suite release_gate --mode real`",
            "",
            "**Report Pack:**",
            "- `python main.py report-pack --type full --mode real`",
            "",
            "**Data Coverage:**",
            "- `python main.py data-coverage-summary`",
            "",
            "**Stable Checklist:**",
            "- `python main.py stable-v060-check --mode real`",
            "",
            "**Strategy Lab Validation:**",
            "- `python main.py strategy-lab --mode real`",
            "",
            "**Integration Notes:**",
            "- Strategy Validation Score: v0.9.2 available"
            " (INSUFFICIENT/OBSERVATIONAL/VALIDATING/VALIDATED/CONFLICTED/REJECTED)."
            " VALIDATED does not enable trading.",
            "",
            "---",
            "",
        ]

    def _section_known_limitations(self) -> List[str]:
        return [
            "## 十一、Known Limitations",
            "",
            "1. No investment advice — all outputs are research tasks only",
            "2. No automatic strategy activation",
            "3. No live order execution — production trading is BLOCKED",
            "4. Provider token environment limits may affect some reports",
            "5. Optional reports may be missing if not yet generated",
            "6. Backtest quality depends on data coverage and import completeness",
            "7. Evidence graph quality depends on available research outputs",
            "8. Training metrics may show INSUFFICIENT_DATA until enough history accumulates",
            "",
            "---",
            "",
        ]

    def _section_next_roadmap(self) -> List[str]:
        return [
            "## 十二、Next Roadmap",
            "",
            "| Version | Feature | Priority |",
            "|---------|---------|---------|",
            "| v0.9.1 | Evidence Graph UX — node detail drill, thread visualization | P2 |",
            "| v0.9.2 | Strategy Validation Score — cross-module confidence scoring | P2 |",
            "| v0.9.3 | Strategy Lab Dashboard Polish — unified layer status board | P2 |",
            "| v1.0.0 | Research Trading Cockpit Stable — still No Real Orders unless explicitly enabled | P1 |",
            "",
            "---",
            "",
        ]

    def _section_safety_declaration(self) -> List[str]:
        return [
            "## 十三、Safety Declaration",
            "",
            "> **Research Only** — All outputs are for research and learning purposes only.",
            ">",
            "> **No Real Orders** — This system does not and cannot place real trading orders.",
            ">",
            "> **No Broker Execution** — There is no connection to any broker API.",
            ">",
            "> **No Auto Trading** — No strategy is automatically activated or executed.",
            ">",
            "> **Not Investment Advice** — Nothing in this report constitutes investment advice.",
            "",
            "---",
            "",
            "*TW Quant Cockpit v0.9.0 — Strategy Lab Stable — Research Only — Not Investment Advice*",
            "",
        ]
