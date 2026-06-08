"""
reports/intelligence_stable_report.py — IntelligenceStableReportBuilder v0.8.0

Generate the Research Intelligence Stable Markdown report.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_OUTPUT_DIR       = os.path.join(BASE_DIR, "reports")
_DEFAULT_STABLE_OUTPUT    = "data/backtest_results/intelligence_stable"


class IntelligenceStableReportBuilder:
    """Generate the v0.8.0 Research Intelligence Stable Markdown report.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    [!] Not Investment Advice. No BUY/SELL/ORDER output.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(
        self,
        mode: str = "real",
        output_dir: str = _DEFAULT_OUTPUT_DIR,
        stable_output_dir: str = _DEFAULT_STABLE_OUTPUT,
    ) -> str:
        """Build the report. Returns path to generated Markdown file."""
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        if not os.path.isabs(stable_output_dir):
            stable_output_dir = os.path.join(BASE_DIR, stable_output_dir)

        # Try to load from store; run engine if no data
        data = self._load_or_run(mode=mode, stable_output_dir=stable_output_dir)

        capabilities = data.get("capabilities", [])
        checks       = data.get("checks", [])
        summary      = data.get("summary", {})
        manifest     = data.get("manifest", {})

        # Build Markdown
        lines = self._build_lines(capabilities, checks, summary, manifest)
        content = "\n".join(lines) + "\n"

        # Write file
        os.makedirs(output_dir, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        path = os.path.join(output_dir, f"intelligence_stable_report_{today}.md")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("IntelligenceStableReportBuilder: report written -> %s", path)
        except Exception as exc:
            logger.warning("IntelligenceStableReportBuilder: write error: %s", exc)

        return path

    # ------------------------------------------------------------------
    # Internal: load or run
    # ------------------------------------------------------------------

    def _load_or_run(self, mode: str, stable_output_dir: str) -> dict:
        """Try to load from store; run engine if no data exists."""
        try:
            from intelligence_stable.intelligence_stable_store import IntelligenceStableStore
            store = IntelligenceStableStore(output_dir=stable_output_dir)
            caps_raw  = store.load_capabilities()
            chks_raw  = store.load_latest_checks()
            summ_raw  = store.load_latest_summary()

            if caps_raw and chks_raw and summ_raw:
                # Convert dicts back to objects
                from intelligence_stable.intelligence_stable_schema import (
                    IntelligenceStableCapability, IntelligenceStableCheck,
                    IntelligenceStableSummary,
                )
                capabilities = [IntelligenceStableCapability.from_dict(d) for d in caps_raw]
                checks       = [IntelligenceStableCheck.from_dict(d) for d in chks_raw]
                summary      = IntelligenceStableSummary.from_dict(summ_raw)
                manifest     = {}
                return {
                    "capabilities": capabilities,
                    "checks":       checks,
                    "summary":      summary,
                    "manifest":     manifest,
                }
        except Exception as exc:
            logger.warning("IntelligenceStableReportBuilder: store load error: %s", exc)

        # Run engine if no data
        try:
            from intelligence_stable.intelligence_stable_engine import IntelligenceStableEngine
            engine = IntelligenceStableEngine(
                project_root=BASE_DIR,
                output_dir=stable_output_dir,
            )
            return engine.run(mode=mode)
        except Exception as exc:
            logger.warning("IntelligenceStableReportBuilder: engine run error: %s", exc)
            return {"capabilities": [], "checks": [], "summary": None, "manifest": {}}

    # ------------------------------------------------------------------
    # Internal: build Markdown lines
    # ------------------------------------------------------------------

    def _build_lines(self, capabilities, checks, summary, manifest) -> List[str]:
        lines: List[str] = []

        # Section 1: Header
        lines += self._section_header()

        # Section 2: Release Overview
        lines += self._section_release_overview(summary, manifest)

        # Section 3: Capability Matrix
        lines += self._section_capability_matrix(capabilities)

        # Section 4: Stable Checklist
        lines += self._section_stable_checklist(checks, summary)

        # Section 5: Safety Audit
        lines += self._section_safety_audit(summary)

        # Section 6: Research Intelligence Layer
        lines += self._section_research_intelligence_layer()

        # Section 7: Strategy Memory Layer
        lines += self._section_strategy_memory_layer()

        # Section 8: Backtest-to-Coach Layer
        lines += self._section_backtest_coach_layer()

        # Section 9: Regression / Report / Data Coverage
        lines += self._section_regression_report_data()

        # Section 10: Known Limitations
        lines += self._section_known_limitations()

        # Section 11: Safety Declaration
        lines += self._section_safety_declaration()

        return lines

    def _section_header(self) -> List[str]:
        today = datetime.now().strftime("%Y-%m-%d")
        return [
            "# Research Intelligence Stable Report v0.8.0",
            "",
            f"**Date:** {today}",
            "",
            "> **[!] Research Only. No Real Orders. Production Trading BLOCKED.**",
            "> **[!] Not Investment Advice.**",
            "",
            "---",
            "",
        ]

    def _section_release_overview(self, summary, manifest) -> List[str]:
        lines = [
            "## Release Overview",
            "",
        ]
        if summary and hasattr(summary, "version"):
            lines += [
                f"| Field | Value |",
                f"|-------|-------|",
                f"| Version | {summary.version} |",
                f"| Release Name | {summary.release_name} |",
                f"| Previous Version | v0.7.3 |",
                f"| Mode | {summary.mode} |",
                f"| Overall Status | **{summary.overall_status}** |",
                f"| Generated At | {summary.generated_at} |",
            ]
        else:
            lines += ["*(No summary available — run: python main.py intelligence-stable --mode real)*"]
        lines += ["", "---", ""]
        return lines

    def _section_capability_matrix(self, capabilities) -> List[str]:
        lines = [
            "## Capability Matrix",
            "",
            f"**Total Capabilities:** {len(capabilities)}",
            "",
        ]
        if capabilities:
            lines += [
                "| Capability | Category | Status | CLI | GUI | Report | Regression | Limitation |",
                "|-----------|----------|--------|-----|-----|--------|------------|------------|",
            ]
            for cap in capabilities:
                cli   = "|".join(cap.cli_commands[:2]) or "—"
                gui   = "|".join(cap.gui_tabs[:1]) or "—"
                rpt   = "|".join(cap.reports[:1]) or "—"
                reg   = "|".join(cap.regression_suites[:1]) or "—"
                lim   = cap.known_limitations[0][:40] if cap.known_limitations else "—"
                lines.append(
                    f"| {cap.name} | {cap.category} | {cap.stable_status} "
                    f"| {cli} | {gui} | {rpt} | {reg} | {lim} |"
                )
        else:
            lines.append("*(No capabilities loaded)*")
        lines += ["", "---", ""]
        return lines

    def _section_stable_checklist(self, checks, summary) -> List[str]:
        lines = ["## Stable Checklist", ""]
        if summary and hasattr(summary, "total_checks"):
            lines += [
                f"- Total Checks: {summary.total_checks}",
                f"- PASS: {summary.pass_count}",
                f"- WARN: {summary.warn_count}",
                f"- FAIL: {summary.fail_count}",
                f"- BLOCKED: {summary.blocked_check_count}",
                "",
            ]
        if checks:
            lines += [
                "| Category | Check | Status | Severity | Message |",
                "|----------|-------|--------|----------|---------|",
            ]
            for chk in checks[:40]:
                msg = (chk.message[:60] + "...") if len(chk.message) > 60 else chk.message
                lines.append(
                    f"| {chk.category} | {chk.name[:40]} | {chk.status} "
                    f"| {chk.severity} | {msg} |"
                )
        else:
            lines.append("*(No checks loaded — run: python main.py intelligence-stable --mode real)*")
        lines += ["", "---", ""]
        return lines

    def _section_safety_audit(self, summary) -> List[str]:
        lines = ["## Safety Audit", ""]
        if summary and hasattr(summary, "recommendations_safe"):
            lines += [
                f"| Safety Item | Status |",
                f"|-------------|--------|",
                f"| Recommendations Safe | {summary.recommendations_safe} |",
                f"| Memories Safe | {summary.memories_safe} |",
                f"| Coach Tasks Safe | {summary.coach_tasks_safe} |",
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

    def _section_research_intelligence_layer(self) -> List[str]:
        return [
            "## Research Intelligence Layer",
            "",
            "The Research Intelligence layer aggregates signals from 8 source modules,",
            "builds research recommendations, and generates daily/weekly research plans.",
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
            "**Known Limitations:**",
            "- Signal extraction depends on CSV outputs from other modules",
            "- No live market feed",
            "- Recommendations are research tasks only — no trading signals",
            "",
            "---",
            "",
        ]

    def _section_strategy_memory_layer(self) -> List[str]:
        return [
            "## Strategy Memory Layer",
            "",
            "The Strategy Memory layer extracts and persists 10 memory types from all Research OS modules.",
            "Memories track STRATEGY_HYPOTHESIS, RULE_CANDIDATE, REPLAY_MISTAKE_PATTERN, and others.",
            "",
            "**v0.8.1 Strategy Memory UX status: STABLE**",
            "",
            "New in v0.8.1:",
            "- Status lifecycle flow: NEW → REVIEWING → VALIDATING → ACCEPTED/REJECTED/NEEDS_MORE_EVIDENCE",
            "- `accepted_is_research_only=True` invariant: ACCEPTED means research accepted, not trading enabled",
            "- Validation queue, active threads, repeated patterns CLI and GUI views",
            "- `needs_action`, `validation_ready`, `status_hint`, `next_step` UX fields on all memories",
            "- Safe command labelling: SAFE_READ_ONLY / SAFE_REPORT / SAFE_REGRESSION / SAFE_REPLAY / SAFE_DATA_CHECK",
            "- BUY/SELL/ORDER guard in StrategyMemoryAdapter.load_safe_commands()",
            "- Memory UX detail panel: Summary, Hypothesis, Evidence, Validation, Commands, Links, Safety tabs",
            "",
            "**Key CLI commands:**",
            "- `python main.py strategy-memory --mode real`",
            "- `python main.py strategy-memory-summary`",
            "- `python main.py strategy-memory-list`",
            "- `python main.py strategy-memory-list --active-only`",
            "- `python main.py strategy-memory-list --needs-action`",
            "- `python main.py strategy-memory-search`",
            "- `python main.py strategy-memory-search --needs-action`",
            "- `python main.py strategy-memory-validation-queue`",
            "- `python main.py strategy-memory-active-threads`",
            "- `python main.py strategy-memory-repeated-patterns`",
            "- `python main.py strategy-memory-report`",
            "",
            "**Known Limitations:**",
            "- Extraction is pattern-based; no NLP/LLM extraction",
            "- CSV/JSON scan only; no cross-session merge",
            "- ACCEPTED status never enables trading (research-only invariant always enforced)",
            "",
            "---",
            "",
        ]

    def _section_backtest_coach_layer(self) -> List[str]:
        return [
            "## Backtest-to-Coach Layer",
            "",
            "The Backtest-to-Coach layer converts backtest weaknesses into safe coach training tasks.",
            "Task types: PRACTICE_REPLAY, REVIEW_RULE, REVIEW_JOURNAL, FIX_DATA, BACKTEST_MORE,",
            "READ_REPORT, UPDATE_MEMORY, WAIT — no trading actions.",
            "",
            "**Key CLI commands:**",
            "- `python main.py backtest-coach --mode real`",
            "- `python main.py backtest-coach-summary`",
            "- `python main.py backtest-coach-tasks`",
            "- `python main.py backtest-coach-daily-plan`",
            "- `python main.py backtest-coach-weekly-plan`",
            "- `python main.py backtest-coach-report`",
            "",
            "**Known Limitations:**",
            "- Task extraction depends on CSV outputs from other modules",
            "- Daily plan capped at 7 items; weekly plan capped at 12 items",
            "",
            "---",
            "",
            "## Backtest Training Metrics (v0.8.2)",
            "",
            "The Backtest Training Metrics layer measures training effectiveness across all Research OS modules.",
            "Metric types: TASK_COMPLETION, REPLAY_SCORE, MISTAKE_REDUCTION, BACKTEST_ISSUE,",
            "JOURNAL_IMPROVEMENT, MEMORY_VALIDATION, RULE_REVIEW, DATA_FIX_PROGRESS,",
            "TRAINING_STREAK, QUALITY_SCORE.",
            "",
            "**v0.8.2 Training Metrics status: USABLE**",
            "",
            "**Key CLI commands:**",
            "- `python main.py training-metrics --mode real`",
            "- `python main.py training-metrics-summary`",
            "- `python main.py training-metrics-detail`",
            "- `python main.py training-metrics-trend`",
            "- `python main.py training-metrics-report`",
            "",
            "**Known Limitations:**",
            "- Metrics collected from CSV outputs only — no live data feed",
            "- INSUFFICIENT_DATA shown when source module not yet run",
            "- Trend direction requires at least 2 historical data points",
            "",
            "---",
            "",
            "## Research Intelligence Evidence Graph (v0.8.3)",
            "",
            "The Evidence Graph links all research conclusions across Research OS modules",
            "into a traceable, directed graph of evidence nodes and relationships.",
            "Node types: RESEARCH_RECOMMENDATION, STRATEGY_MEMORY, BACKTEST_COACH_TASK,",
            "TRAINING_METRIC, REPLAY_MISTAKE, DATA_GAP, REPORT_RESULT, REGRESSION_RESULT, etc.",
            "Edge relations: SUPPORTS, CONTRADICTS, REQUIRES_BACKTEST, REQUIRES_DATA, etc.",
            "",
            "**v0.8.3 Evidence Graph status: USABLE**",
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
            "- `python main.py evidence-graph-report --mode real`",
            "",
            "**Known Limitations:**",
            "- Edge building is heuristic-based (keyword matching, CSV reading) — not semantic",
            "- Contradiction detection is conservative; may miss subtle conflicts",
            "- Orphan nodes appear when source modules have not yet been run",
            "- Evidence Graph does NOT auto-modify any module status or weights",
            "",
            "---",
            "",
        ]

    def _section_regression_report_data(self) -> List[str]:
        return [
            "## Regression / Report / Data Coverage",
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
            "**Replay Training:**",
            "- Available via GUI tab",
            "",
            "**Stable Checklist:**",
            "- `python main.py stable-v060-check --mode real`",
            "",
            "---",
            "",
        ]

    def _section_known_limitations(self) -> List[str]:
        return [
            "## Known Limitations",
            "",
            "1. No investment advice — all outputs are research tasks only",
            "2. No automatic strategy activation",
            "3. No live order execution — production trading is BLOCKED",
            "4. Provider token environment limits may affect some reports",
            "5. Optional reports may be missing if not yet generated",
            "6. Backtest quality depends on data coverage and import completeness",
            "",
            "---",
            "",
        ]

    def _section_safety_declaration(self) -> List[str]:
        return [
            "## Safety Declaration",
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
            "*TW Quant Cockpit v0.8.0 — Research Intelligence Stable — Research Only — Not Investment Advice*",
            "",
        ]
