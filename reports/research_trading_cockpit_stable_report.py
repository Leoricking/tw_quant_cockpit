"""
reports/research_trading_cockpit_stable_report.py — ResearchTradingCockpitStableReportBuilder v1.0.0

Generates the v1.0.0 Research Trading Cockpit Stable Markdown report.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] VALIDATED does not enable trading. Broker Execution Disabled.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchTradingCockpitStableReportBuilder:
    """Generate v1.0.0 Research Trading Cockpit Stable Markdown report.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        output_dir: str = "data/backtest_results/release",
        report_dir: str = "reports",
    ) -> None:
        self._output_dir = (
            output_dir if os.path.isabs(output_dir)
            else os.path.join(BASE_DIR, output_dir)
        )
        self._report_dir = (
            report_dir if os.path.isabs(report_dir)
            else os.path.join(BASE_DIR, report_dir)
        )

    def build(self, mode: str = "real") -> str:
        """Build the report. Returns path to generated Markdown file."""
        lines: List[str] = []

        lines += self._section_header()
        lines += self._section_overview()
        lines += self._section_modules()
        lines += self._section_research_workflow()
        lines += self._section_crash_reversal_workflow()
        lines += self._section_validation_workflow()
        lines += self._section_dashboard_summary()
        lines += self._section_release_checklist(mode)
        lines += self._section_regression_summary()
        lines += self._section_known_warnings()
        lines += self._section_data_hygiene_status()
        lines += self._section_safety_declaration()
        lines += self._section_next_roadmap()

        content = "\n".join(lines) + "\n"

        os.makedirs(self._report_dir, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        path = os.path.join(
            self._report_dir,
            f"research_trading_cockpit_stable_report_{today}.md",
        )
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)

        logger.info("Research Trading Cockpit Stable Report saved: %s", path)
        return path

    # ------------------------------------------------------------------
    # Section builders
    # ------------------------------------------------------------------

    def _section_header(self) -> List[str]:
        today = datetime.now().strftime("%Y-%m-%d")
        return [
            "# Research Trading Cockpit Stable Report v1.0.0",
            "",
            f"**Date:** {today}",
            "",
            "> **[!] Research Only / No Real Orders / Production Trading BLOCKED**",
            "> **[!] VALIDATED does not enable trading**",
            "> **[!] Broker Execution Disabled**",
            "> **[!] Not Investment Advice**",
            "",
            "---",
            "",
        ]

    def _section_overview(self) -> List[str]:
        lines = [
            "## 一、總覽 (Overview)",
            "",
            "| Field | Value |",
            "|-------|-------|",
            "| Version | 1.0.0 |",
            "| Release Name | Research Trading Cockpit Stable |",
            "| Stage | STABLE |",
            "| Research Only | True |",
            "| No Real Orders | True |",
            "| Production Trading BLOCKED | True |",
            "| Broker Execution | Disabled |",
            "| VALIDATED does not enable trading | True |",
            "| Paper Trading | Simulation Only |",
            "| Mock Realtime | Simulation Only |",
            "| Not Investment Advice | True |",
            "",
            "---",
            "",
        ]
        return lines

    def _section_modules(self) -> List[str]:
        module_checks = [
            ("Strategy Lab Dashboard",      "strategy_lab.strategy_lab_dashboard_engine",  "StrategyLabDashboardEngine"),
            ("Strategy Validation Score",   "strategy_validation.strategy_validation_engine", "StrategyValidationEngine"),
            ("Evidence Graph UX",           "evidence_graph.evidence_graph_query",           "EvidenceGraphQuery"),
            ("Crash Reversal Strategy Pack","strategy_rules.crash_reversal_pack",            "CrashReversalStrategyPack"),
            ("Strategy Lab Stable",         "strategy_lab.strategy_lab_engine",              "StrategyLabEngine"),
            ("Training Metrics",            "training_metrics.training_metrics_engine",       "TrainingMetricsEngine"),
            ("Backtest Coach",              "backtest_coach.backtest_coach_engine",           "BacktestCoachEngine"),
            ("Strategy Memory",             "strategy_memory.strategy_memory_engine",         "StrategyMemoryEngine"),
            ("Research Intelligence",       "research_intelligence.research_intelligence_engine", "ResearchIntelligenceEngine"),
            ("Data Coverage",               "data_coverage.data_coverage_engine",             "DataCoverageEngine"),
            ("Report Pack",                 "report_pack.report_registry",                   "ReportRegistry"),
            ("Regression Gate",             "regression.suite_registry",                     "RegressionSuiteRegistry"),
            ("Paper Trading",               "sim.simulator",                                  "PaperTrader"),
            ("Mock Realtime",               "broker.mock_broker",                             "MockBroker"),
        ]

        lines = [
            "## 二、System Modules",
            "",
            "| Module | Status |",
            "|--------|--------|",
        ]
        import importlib
        for name, mod_path, cls_name in module_checks:
            try:
                mod = importlib.import_module(mod_path)
                if cls_name:
                    status = "AVAILABLE" if hasattr(mod, cls_name) else "PARTIAL"
                else:
                    status = "AVAILABLE"
            except Exception:
                status = "UNAVAILABLE"
            lines.append(f"| {name} | {status} |")

        lines += ["", "---", ""]
        return lines

    def _section_research_workflow(self) -> List[str]:
        return [
            "## 三、Strategy Research Workflow",
            "",
            "```",
            "Research Intelligence → Strategy Memory → Evidence Graph",
            "    → Strategy Validation Score → Backtest Coach",
            "    → Training Metrics → Strategy Lab Dashboard",
            "```",
            "",
            "All steps are Research Only. No trading actions.",
            "",
            "---",
            "",
        ]

    def _section_crash_reversal_workflow(self) -> List[str]:
        return [
            "## 四、Crash Reversal Workflow",
            "",
            "| Rule | Description |",
            "|------|-------------|",
            "| 1. Crash Cause Classifier | Fundamental / Financial / Technical / Systemic |",
            "| 2. Post-Crash Stabilization | 8-condition checklist |",
            "| 3. Relative Strength Score | Relative strength after crash |",
            "| 4. EPS-backed Dip Filter | Sakata EPS-backed dip buy filter |",
            "| 5. MA Profit Discipline | Moving average profit discipline |",
            "| 6. High-Risk Industry Guard | High-risk industry exposure guard |",
            "",
            "Research Only — Crash Reversal checks do NOT trigger any real actions.",
            "",
            "---",
            "",
        ]

    def _section_validation_workflow(self) -> List[str]:
        return [
            "## 五、Validation Workflow",
            "",
            "```",
            "INSUFFICIENT → OBSERVATIONAL → VALIDATING → VALIDATED",
            "                                          → CONFLICTED",
            "                                          → REJECTED",
            "```",
            "",
            "> **VALIDATED = Research Validated Only.**",
            "> **VALIDATED does NOT enable trading.**",
            "> **No Real Orders at any stage.**",
            "",
            "---",
            "",
        ]

    def _section_dashboard_summary(self) -> List[str]:
        lines = [
            "## 六、Dashboard Summary",
            "",
        ]
        try:
            from strategy_lab.strategy_lab_dashboard_store import StrategyLabDashboardStore
            store = StrategyLabDashboardStore()
            summary = store.load_latest_summary()
            if summary:
                sd = summary.to_dict() if hasattr(summary, "to_dict") else summary
                lines += [
                    "| Field | Value |",
                    "|-------|-------|",
                    f"| Overall Status | {sd.get('overall_status', 'UNKNOWN')} |",
                    f"| Health Score | {float(sd.get('overall_health_score', 0)):.1f} / 100 |",
                    f"| Strategy Count | {sd.get('strategy_count', 0)} |",
                    f"| Needs Backtest | {sd.get('needs_backtest_count', 0)} |",
                    f"| Crash Warnings | {sd.get('crash_reversal_warning_count', 0)} |",
                    "",
                ]
            else:
                lines += [
                    "*(No dashboard summary — run: `python main.py strategy-lab-dashboard --mode real`)*",
                    "",
                ]
        except Exception as exc:
            lines += [
                f"*(Dashboard summary unavailable: {exc})*",
                "",
                "Run: `python main.py strategy-lab-dashboard --mode real`",
                "",
            ]
        lines += ["---", ""]
        return lines

    def _section_release_checklist(self, mode: str) -> List[str]:
        lines = [
            "## 七、Release Checklist v1.0.0",
            "",
        ]
        try:
            from release.research_cockpit_stable_checklist import ResearchCockpitStableChecklist
            checker = ResearchCockpitStableChecklist(project_root=BASE_DIR)
            checks, summary = checker.run(mode=mode)

            lines += [
                "| # | Check | Category | Status | Detail |",
                "|---|-------|----------|--------|--------|",
            ]
            for i, c in enumerate(checks, 1):
                detail_trunc = str(c.get("detail", ""))[:80]
                lines.append(
                    f"| {i} | {c['name']} | {c['category']} | {c['status']} | {detail_trunc} |"
                )

            lines += [
                "",
                "**Summary:**",
                "",
                f"- Total: {summary['total']}",
                f"- PASS: {summary['pass_count']}",
                f"- WARN: {summary['warn_count']}",
                f"- FAIL: {summary['fail_count']}",
                f"- BLOCKED: {summary['blocked_count']}",
                f"- Overall: **{summary['overall_status']}**",
                "",
            ]
        except Exception as exc:
            lines += [
                f"*(Checklist error: {exc})*",
                "",
            ]
        lines += ["---", ""]
        return lines

    def _section_regression_summary(self) -> List[str]:
        return [
            "## 八、Regression Summary",
            "",
            "Run: `python main.py regression-run --suite release_gate --mode real`",
            "",
            "| Suite | Description |",
            "|-------|-------------|",
            "| quick | Core smoke tests |",
            "| release_gate | Data + Quick + Safety + GUI + Smoke + v1.0.0 checks |",
            "| safety | Safety and forbidden-action checks |",
            "",
            "---",
            "",
        ]

    def _section_known_warnings(self) -> List[str]:
        return [
            "## 九、Known Warnings",
            "",
            "| Warning | Severity | Notes |",
            "|---------|----------|-------|",
            "| cp950 subprocess encoding (Windows) | INFO | Non-critical; subprocess output encoding |",
            "| Paper smoke WARN if paper_state.json missing | WARN | Non-critical; run paper to generate |",
            "| no_real_orders flag pre-existing check | INFO | Advisory only |",
            "| Optional report_pack ENV_LIMITED | INFO | Non-critical; some providers not available |",
            "",
            "---",
            "",
        ]

    def _section_data_hygiene_status(self) -> List[str]:
        try:
            from maintenance.data_report_hygiene_engine import DataReportHygieneEngine
            engine_available = True
            try:
                eng = DataReportHygieneEngine()
                review_only = eng.review_only
            except Exception:
                review_only = True
        except ImportError:
            engine_available = False
            review_only = True
        return [
            "## 十一、Data & Report Hygiene Status (v1.0.2)",
            "",
            "| Field | Value |",
            "|-------|-------|",
            f"| Module Available | {engine_available} |",
            f"| Review Only | {review_only} |",
            "| Data Cleanup | Review Only — no automatic deletion |",
            "| Archive Suggestions | Review Only — no automatic archive |",
            "| No Real Orders | True |",
            "| Production Blocked | True |",
            "",
            "> Run `python main.py data-report-hygiene --mode real` to scan.",
            "",
            "---",
            "",
        ]

    def _section_safety_declaration(self) -> List[str]:
        return [
            "## 十、Safety Declaration",
            "",
            "> **Research Only** — All outputs are for research and learning purposes only.",
            ">",
            "> **No Real Orders** — This system does not and cannot place real trading orders.",
            ">",
            "> **Production Trading BLOCKED** — Production trading is permanently blocked.",
            ">",
            "> **Broker Execution Disabled** — There is no connection to any broker API.",
            ">",
            "> **VALIDATED does not enable trading** — VALIDATED grade is research-validated only.",
            ">",
            "> **Paper trading is simulation only** — Paper trades are simulated, not real.",
            ">",
            "> **Mock realtime is simulation only** — Mock realtime is not live market data.",
            ">",
            "> **Not Investment Advice** — Nothing in this report constitutes investment advice.",
            "",
            "---",
            "",
            "*TW Quant Cockpit v1.0.0 — Research Trading Cockpit Stable — Research Only — Not Investment Advice*",
            "",
        ]

    def _section_next_roadmap(self) -> List[str]:
        return [
            "## 十一、Next Roadmap",
            "",
            "| Version | Feature | Priority |",
            "|---------|---------|---------|",
            "| v1.0.x | Maintenance releases — bug fixes, warning cleanup | P1 |",
            "| v1.1 | Data Quality / Universe Expansion — broader coverage | P2 |",
            "| broker-api-branch | Broker API (only if explicitly requested, separate branch) | ON_REQUEST |",
            "",
            "---",
            "",
        ]
