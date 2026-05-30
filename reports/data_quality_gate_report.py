"""
reports/data_quality_gate_report.py - Data Quality Gate Report Builder (v0.3.20).

Generates a 9-section Markdown report from DataQualityGate results.

[!] Research Only. Simulation Only. No Real Orders.
[!] PRODUCTION_BLOCKED is always True in v1.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataQualityGateReportBuilder:
    """
    Builds a Markdown report from DataQualityGate run() output.

    Parameters
    ----------
    gate_result : dict returned by DataQualityGate.run()
    report_date : YYYY-MM-DD string (defaults to today)
    """

    VERSION = "v0.3.20"

    def __init__(
        self,
        gate_result: dict,
        report_date: Optional[str] = None,
    ):
        self.gate_result = gate_result
        self.report_date = report_date or datetime.now().strftime("%Y-%m-%d")

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def build(self, output_dir: Optional[str] = None) -> str:
        """
        Write the Markdown report to output_dir.

        Returns path to the generated file.
        """
        out_dir = output_dir or os.path.join(_BASE_DIR, "reports")
        os.makedirs(out_dir, exist_ok=True)

        fname = f"data_quality_gate_report_{self.report_date}.md"
        path  = os.path.join(out_dir, fname)

        content = self._render()
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info("DataQualityGateReport written → %s", path)
        return path

    def render(self) -> str:
        """Return rendered Markdown string (no file write)."""
        return self._render()

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render(self) -> str:
        r = self.gate_result
        sections = [
            self._section_header(r),
            self._section_composite_scores(r),
            self._section_sub_scores(r),
            self._section_gate_decisions(r),
            self._section_freshness_detail(r),
            self._section_coverage_detail(r),
            self._section_mock_contamination(r),
            self._section_provider_health(r),
            self._section_blockers_and_actions(r),
            self._section_limitations(),
        ]
        return "\n\n".join(sections) + "\n"

    # ---- Section 1: Header -----------------------------------------------

    def _section_header(self, r: dict) -> str:
        mode     = r.get("mode", "unknown").upper()
        checked  = r.get("checked_at", "")[:19]
        prod_cls = r.get("production_classification", "UNKNOWN")
        bt_cls   = r.get("backtest_classification", "UNKNOWN")

        return (
            f"# TW Quant Cockpit — Data Quality Gate Report\n"
            f"\n"
            f"> **{self.VERSION}** | Report Date: {self.report_date} | "
            f"Mode: {mode} | Checked At: {checked}\n"
            f">\n"
            f"> [!] Advisory Only. Simulation Only. No Real Orders.\n"
            f"> Production Classification: **{prod_cls}** | "
            f"Backtest Classification: **{bt_cls}**\n"
            f"\n"
            f"---"
        )

    # ---- Section 2: Composite Scores -------------------------------------

    def _section_composite_scores(self, r: dict) -> str:
        prod  = r.get("production_readiness_score", 0.0)
        btest = r.get("backtest_readiness_score", 0.0)
        p_cls = r.get("production_classification", "—")
        b_cls = r.get("backtest_classification", "—")

        lines = [
            "## 一、Composite Readiness Scores",
            "",
            "| Score | Value | Classification |",
            "|-------|-------|----------------|",
            f"| Production Readiness | **{prod:.1f}** | {p_cls} |",
            f"| Backtest Readiness   | **{btest:.1f}** | {b_cls} |",
            "",
            "_Score scale: 90-100=STRONG, 75-89=READY_FOR_RESEARCH, "
            "60-74=PARTIAL, 40-59=WEAK, 0-39=BLOCKED_",
        ]
        return "\n".join(lines)

    # ---- Section 3: Sub-scores -------------------------------------------

    def _section_sub_scores(self, r: dict) -> str:
        scores = r.get("scores", {})
        lines  = [
            "## 二、Sub-Scores",
            "",
            "| Sub-Score | Value |",
            "|-----------|-------|",
        ]
        _order = [
            ("freshness_score",          "Freshness Score"),
            ("coverage_score",           "Coverage Score"),
            ("source_confidence_score",  "Source Confidence Score"),
            ("timing_quality_score",     "Timing Quality Score"),
            ("sample_size_score",        "Sample Size Score"),
            ("intraday_coverage_score",  "Intraday Coverage Score"),
            ("provider_health_score",    "Provider Health Score"),
            ("mock_contamination_score", "Mock Contamination Score"),
        ]
        for key, label in _order:
            val = scores.get(key, "N/A")
            val_str = f"{val:.1f}" if isinstance(val, float) else str(val)
            lines.append(f"| {label} | {val_str} |")

        lines += [
            "",
            "_Weight formula:_",
            "",
            "```",
            "production_readiness_score =",
            "  0.20 * freshness_score",
            "  0.20 * coverage_score",
            "  0.15 * source_confidence_score",
            "  0.15 * timing_quality_score",
            "  0.10 * sample_size_score",
            "  0.10 * intraday_coverage_score",
            "  0.05 * provider_health_score",
            "  0.05 * mock_contamination_score",
            "",
            "backtest_readiness_score =",
            "  0.25 * coverage_score",
            "  0.20 * sample_size_score",
            "  0.20 * mock_contamination_score",
            "  0.15 * freshness_score",
            "  0.10 * timing_quality_score",
            "  0.10 * source_confidence_score",
            "  (capped at 60 if mock_contamination<90; capped at 70 if coverage<70)",
            "```",
        ]
        return "\n".join(lines)

    # ---- Section 4: Gate Decisions ---------------------------------------

    def _section_gate_decisions(self, r: dict) -> str:
        gates = r.get("gates", {})
        lines = [
            "## 三、Gate Decisions",
            "",
            "| Gate | Status |",
            "|------|--------|",
        ]
        _gate_labels = [
            ("RESEARCH_ONLY",       "Research Only"),
            ("BACKTEST_READY",      "Backtest Ready"),
            ("PAPER_TRADING_READY", "Paper Trading Ready"),
            ("PRODUCTION_BLOCKED",  "Production Blocked"),
            ("API_READY_READONLY",  "API Ready (Read-Only)"),
            ("INTRADAY_READY",      "Intraday Ready"),
            ("LONG_TERM_READY",     "Long-Term Ready"),
            ("PORTFOLIO_READY",     "Portfolio Ready"),
            ("REAL_ORDER_READY",    "Real Order Ready"),
        ]
        for key, label in _gate_labels:
            val = gates.get(key)
            if val is True:
                status = "YES"
            elif val is False:
                status = "NO"
            else:
                status = str(val)
            lines.append(f"| {label} | {status} |")

        lines += [
            "",
            "> **Note:** PRODUCTION_BLOCKED is always YES in v0.3 (v1). "
            "REAL_ORDER_READY is never allowed.",
        ]
        return "\n".join(lines)

    # ---- Section 5: Freshness Detail -------------------------------------

    def _section_freshness_detail(self, r: dict) -> str:
        details = r.get("details", {})
        fd      = details.get("freshness_score", {})
        datasets = fd.get("datasets", {})

        lines = [
            "## 四、Freshness Detail",
            "",
            "| Dataset | Status |",
            "|---------|--------|",
        ]
        if datasets:
            for ds, status in datasets.items():
                lines.append(f"| {ds} | {status} |")
        else:
            lines.append("| — | No freshness data available |")

        return "\n".join(lines)

    # ---- Section 6: Coverage Detail --------------------------------------

    def _section_coverage_detail(self, r: dict) -> str:
        details = r.get("details", {})
        cd      = details.get("coverage_score", {})
        datasets = cd.get("datasets", {})

        lines = [
            "## 五、Coverage Detail",
            "",
            "| Dataset | Status |",
            "|---------|--------|",
        ]
        if datasets:
            for ds, status in datasets.items():
                lines.append(f"| {ds} | {status} |")
        else:
            lines.append("| — | No coverage data available |")

        return "\n".join(lines)

    # ---- Section 7: Mock Contamination -----------------------------------

    def _section_mock_contamination(self, r: dict) -> str:
        details = r.get("details", {})
        mc      = details.get("mock_contamination_score", {})

        status  = mc.get("status", "UNKNOWN")
        score   = mc.get("score", 0.0)
        found   = mc.get("contamination_markers_found", [])
        files   = mc.get("contaminated_files", [])
        detail  = mc.get("details", [])
        action  = mc.get("recommended_action", "")

        lines = [
            "## 六、Mock Contamination",
            "",
            f"**Status:** {status}  |  **Score:** {score:.1f}",
            "",
        ]
        if detail:
            lines.append("**Issues found:**")
            lines.append("")
            for d in detail[:10]:
                lines.append(f"- {d}")
            lines.append("")
        else:
            lines.append("No mock contamination issues found.")
            lines.append("")

        if action:
            lines.append(f"**Recommended Action:** {action}")

        return "\n".join(lines)

    # ---- Section 8: Provider Health --------------------------------------

    def _section_provider_health(self, r: dict) -> str:
        details = r.get("details", {})
        ph      = details.get("provider_health_score", {})
        summary = ph.get("summary", {})

        lines = [
            "## 七、Provider Health",
            "",
            "| Status | Count |",
            "|--------|-------|",
        ]
        for status, count in summary.items():
            lines.append(f"| {status} | {count} |")

        if not summary:
            lines.append("| — | No provider health data |")

        return "\n".join(lines)

    # ---- Section 9: Blockers & Actions -----------------------------------

    def _section_blockers_and_actions(self, r: dict) -> str:
        warnings = r.get("warnings", [])
        gates    = r.get("gates", {})
        scores   = r.get("scores", {})

        blockers: list = []

        # Gate-based blockers
        if not gates.get("BACKTEST_READY", False):
            prod   = r.get("production_readiness_score", 0.0)
            cov    = scores.get("coverage_score", 0.0)
            mock   = scores.get("mock_contamination_score", 0.0)
            missing = []
            if prod  < 70: missing.append(f"production_readiness_score={prod:.1f} (need ≥70)")
            if cov   < 70: missing.append(f"coverage_score={cov:.1f} (need ≥70)")
            if mock  < 90: missing.append(f"mock_contamination_score={mock:.1f} (need ≥90)")
            if missing:
                blockers.append("BACKTEST_READY blocked: " + "; ".join(missing))

        if not gates.get("INTRADAY_READY", False):
            intra = scores.get("intraday_coverage_score", 0.0)
            blockers.append(f"INTRADAY_READY blocked: intraday_coverage_score={intra:.1f} (need ≥70)")

        lines = [
            "## 八、Blockers and Recommended Actions",
            "",
        ]
        if blockers:
            lines.append("**Gate Blockers:**")
            lines.append("")
            for b in blockers:
                lines.append(f"- {b}")
            lines.append("")

        if warnings:
            lines.append("**Warnings:**")
            lines.append("")
            for w in warnings[:10]:
                lines.append(f"- {w}")
            lines.append("")

        if not blockers and not warnings:
            lines.append("No blockers or warnings.")

        return "\n".join(lines)

    # ---- Section Limitations ---------------------------------------------

    def _section_limitations(self) -> str:
        return (
            "## 九、限制說明\n"
            "\n"
            "- 所有評分為研究參考，不構成投資建議。\n"
            "- PRODUCTION_BLOCKED 在 v0.3 (v1) 永遠為 True。\n"
            "- REAL_ORDER_READY 在本系統永遠不被允許。\n"
            "- 本報告由 DataQualityGate v0.3.20 自動生成。\n"
            "\n"
            "[!] Advisory Only. Research Only. Simulation Only. No Real Orders."
        )
