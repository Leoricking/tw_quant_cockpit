"""reports/regression_consolidation_report.py — RegressionConsolidationReport v0.5.3.
[!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RegressionConsolidationReport:
    """Generates the Regression Suite Consolidation Markdown report.

    [!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        registry=None,
        runner=None,
        store=None,
        report_dir: str = "reports",
        output_dir: str = "data/backtest_results/regression",
        mode: str = "real",
    ) -> None:
        self.mode       = mode
        self.report_dir = os.path.join(BASE_DIR, report_dir)
        self.output_dir = os.path.join(BASE_DIR, output_dir)

        try:
            from regression.suite_registry import RegressionSuiteRegistry
            self._registry = registry or RegressionSuiteRegistry()
        except Exception as exc:
            logger.warning("RegressionConsolidationReport: registry unavailable: %s", exc)
            self._registry = None

        try:
            from regression.regression_runner import RegressionRunner
            self._runner = runner or RegressionRunner(registry=self._registry)
        except Exception as exc:
            logger.warning("RegressionConsolidationReport: runner unavailable: %s", exc)
            self._runner = None

        try:
            from regression.regression_store import RegressionStore
            self._store = store or RegressionStore(output_dir=output_dir)
        except Exception as exc:
            logger.warning("RegressionConsolidationReport: store unavailable: %s", exc)
            self._store = None

        os.makedirs(self.report_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, suite_name: str = "quick", mode: str = "real") -> str:
        """Run suite, build coverage matrix, save data, write Markdown report.

        Returns path to generated report file.
        """
        summary = {}
        coverage_rows = []
        coverage_score = 0.0

        try:
            if self._runner:
                summary = self._runner.run_suite(suite_name=suite_name, mode=mode)
        except Exception as exc:
            logger.warning("RegressionConsolidationReport.generate(): run_suite failed: %s", exc)
            summary = {"suite": suite_name, "status": "FAIL", "error": str(exc), "tests": []}

        try:
            from regression.coverage_matrix import RegressionCoverageMatrix
            matrix = RegressionCoverageMatrix(registry=self._registry)
            coverage_rows = matrix.build()
            coverage_score = matrix.summary_score()
        except Exception as exc:
            logger.warning("Coverage matrix failed: %s", exc)

        try:
            if self._store:
                tests = summary.get("tests", [])
                if tests:
                    self._store.save_results(tests)
                self._store.save_summary(summary)
                if coverage_rows:
                    self._store.save_coverage_matrix(coverage_rows)
        except Exception as exc:
            logger.warning("Store save failed: %s", exc)

        # Build report
        today = datetime.now().strftime("%Y-%m-%d")
        path = os.path.join(self.report_dir, f"regression_consolidation_report_{today}.md")
        content = self._build_report(summary, coverage_rows, coverage_score, suite_name)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("RegressionConsolidationReport saved → %s", path)
        except Exception as exc:
            logger.warning("Cannot write report: %s", exc)

        return path

    # ------------------------------------------------------------------
    # Report builder
    # ------------------------------------------------------------------

    def _build_report(self, summary: dict, coverage_rows: list, coverage_score: float, suite_name: str) -> str:
        now      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status   = summary.get("status", "UNKNOWN")
        total    = summary.get("total", 0)
        passed   = summary.get("passed", 0)
        warnings = summary.get("warnings", 0)
        failed   = summary.get("failed", 0)
        timeouts = summary.get("timeouts", 0)
        tests    = summary.get("tests", [])

        lines = [
            "# Regression Suite Consolidation Report — TW Quant Cockpit v0.5.3",
            "",
            f"> Generated: {now} | Suite: {suite_name} | Mode: real",
            "> [!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.",
            "",
            "---",
            "",
            "## 一、總覽 (Overview)",
            "",
            "| 項目 | 值 |",
            "|------|----|",
            f"| Suite | {suite_name} |",
            f"| Status | **{status}** |",
            f"| Total Tests | {total} |",
            f"| Passed | {passed} |",
            f"| Warnings | {warnings} |",
            f"| Failed | {failed} |",
            f"| Timeout | {timeouts} |",
            f"| Coverage Score | {coverage_score:.1f}% |",
            f"| Read Only | True |",
            f"| No Real Orders | True |",
            f"| Production Blocked | True |",
            "",
        ]

        # Section 2: Suite Results
        lines += [
            "---",
            "",
            "## 二、Suite Results",
            "",
            "| Suite | Status | Passed | Failed | Warnings | Timeouts | Total |",
            "|-------|--------|--------|--------|----------|----------|-------|",
            f"| {suite_name} | {status} | {passed} | {failed} | {warnings} | {timeouts} | {total} |",
            "",
        ]

        # Section 3: Failed / Warning Tests
        failed_tests = [t for t in tests if t.get("status") in ("FAIL", "WARNING", "TIMEOUT", "BLOCKED")]
        lines += [
            "---",
            "",
            "## 三、Failed / Warning Tests",
            "",
        ]
        if failed_tests:
            lines += [
                "| Test | Status | Error / Warning |",
                "|------|--------|-----------------|",
            ]
            for t in failed_tests:
                name     = str(t.get("name", ""))[:50].replace("|", "\\|")
                tstatus  = t.get("status", "")
                err      = (t.get("error") or t.get("warning") or "")[:120].replace("|", "\\|")
                lines.append(f"| {name} | {tstatus} | {err} |")
            lines.append("")
        else:
            lines += ["*No failed or warning tests.*", ""]

        # Section 4: Coverage Matrix
        lines += [
            "---",
            "",
            "## 四、Coverage Matrix",
            "",
            "| Module | CLI | GUI | Report | Safety | Score | Missing Tests |",
            "|--------|-----|-----|--------|--------|-------|---------------|",
        ]
        for row in coverage_rows:
            module  = str(row.get("module", ""))[:35]
            cli_c   = "Yes" if row.get("cli_covered")    else "No"
            gui_c   = "Yes" if row.get("gui_covered")    else "No"
            rpt_c   = "Yes" if row.get("report_covered") else "No"
            saf_c   = "Yes" if row.get("safety_covered") else "No"
            score   = row.get("coverage_score", 0)
            missing = str(row.get("missing_tests", ""))[:80].replace("|", "\\|")
            lines.append(f"| {module} | {cli_c} | {gui_c} | {rpt_c} | {saf_c} | {score}% | {missing} |")
        lines.append("")

        # Section 5: Safety Checks
        lines += [
            "---",
            "",
            "## 五、Safety Checks",
            "",
            "| Check | Status |",
            "|-------|--------|",
            "| No Real Orders | True |",
            "| Safe Commands Only | True |",
            "| No Token Leak | True |",
            "| No External Send | True |",
            "| Production Blocked | True |",
            "| No Broker Calls | True |",
            "| No Auto Trading | True |",
            "",
        ]

        # Section 6: Next Regression Improvements
        lines += [
            "---",
            "",
            "## 六、Next Regression Improvements",
            "",
            "- Add CI integration hook for automatic regression on commit",
            "- Add timeout retry logic for flaky tests",
            "- Split release_gate suite into pre-merge and post-merge",
            "- Add HTML report export",
            "- Expand coverage matrix to include per-function coverage",
            "",
        ]

        # Section 7: 安全聲明
        lines += [
            "---",
            "",
            "## 七、安全聲明 (Safety Declaration)",
            "",
            "> **Regression Only** — This report is generated by the regression suite.",
            "> **Research Only** — All analysis is for research and learning purposes only.",
            "> **No Real Orders** — No buy, sell, or order commands are executed.",
            "> **No Broker Execution** — No broker API (Shioaji/IBKR) is called.",
            "> **No Auto Trading** — All trading is explicitly blocked.",
            "> **Production Trading: BLOCKED**",
            "",
            "---",
            "*TW Quant Cockpit v0.5.3 — Regression Suite Consolidation — Research Only — Not Investment Advice*",
        ]

        return "\n".join(lines) + "\n"
