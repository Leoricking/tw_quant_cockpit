"""
reports/intraday_pipeline_report.py — Intraday Pipeline Report Builder (v0.3.27).
Generates reports/intraday_pipeline_report_YYYY-MM-DD.md
[!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_SAFETY_BANNER = """\
> [!] **Research Only / Intraday Research Only / No Real Orders / Not Investment Advice**
> **Production Trading: BLOCKED**
> This report is generated for research and analysis purposes only.
> No signals, outputs, or recommendations herein should be used for actual trading.
"""


class IntradayPipelineReportBuilder:
    """
    Builds an intraday pipeline Markdown report from pipeline and quality results.

    Output file: reports/intraday_pipeline_report_YYYY-MM-DD.md

    [!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.

    Safety flags
    ------------
    read_only           : True
    no_real_orders      : True
    production_blocked  : True
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(
        self,
        report_date: Optional[str] = None,
        pipeline_result: Optional[dict] = None,
        quality_result: Optional[dict] = None,
        feature_results: Optional[dict] = None,
        mode: str = "real",
    ):
        self.report_date = report_date or datetime.now().strftime("%Y-%m-%d")
        self.pipeline_result = pipeline_result or {}
        self.quality_result = quality_result or {}
        self.feature_results = feature_results or {}
        self.mode = mode

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def build(self, output_dir: Optional[str] = None) -> str:
        """
        Write the intraday pipeline report Markdown file.

        Parameters
        ----------
        output_dir : str or None
            Directory to write the report. Defaults to BASE_DIR/reports.

        Returns
        -------
        str path to the written file
        """
        if output_dir is None:
            output_dir = os.path.join(BASE_DIR, "reports")

        os.makedirs(output_dir, exist_ok=True)
        fname = f"intraday_pipeline_report_{self.report_date}.md"
        out_path = os.path.join(output_dir, fname)

        sections = [
            self._section_header(),
            self._section_overview(),
            self._section_quality(),
            self._section_opening_range(),
            self._section_vwap(),
            self._section_fake_breakout(),
            self._section_volume_profile(),
            self._section_tick_bidask(),
            self._section_safety(),
        ]

        content = "\n\n".join(sections) + "\n"
        try:
            with open(out_path, "w", encoding="utf-8") as fh:
                fh.write(content)
            logger.info("IntradayPipelineReportBuilder: wrote %s", out_path)
        except Exception as exc:
            logger.error("Failed to write report %s: %s", out_path, exc)
            raise

        return out_path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_header(self) -> str:
        lines = [
            f"# TW Quant Cockpit v0.3.27 — Intraday Pipeline Report",
            f"",
            f"**Date:** {self.report_date}  ",
            f"**Mode:** {self.mode}  ",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            _SAFETY_BANNER,
        ]
        return "\n".join(lines)

    def _section_overview(self) -> str:
        p = self.pipeline_result
        lines = [
            "## 1. 總覽 (Pipeline Overview)",
            "",
            f"| 項目 | 值 |",
            f"|------|-----|",
            f"| Mode | {p.get('mode', self.mode)} |",
            f"| Freq | {p.get('freq', 'N/A')} |",
            f"| Files Discovered | {p.get('files_discovered', 0)} |",
            f"| Files Standardized | {p.get('files_standardized', 0)} |",
            f"| Files Failed | {p.get('files_failed', 0)} |",
            f"| Pipeline Status | {p.get('status', 'N/A')} |",
        ]

        symbols = p.get("symbols_covered", [])
        if symbols:
            lines.append(f"| Symbols Covered | {', '.join(symbols)} |")
        else:
            lines.append("| Symbols Covered | (none) |")

        warnings = p.get("warnings", [])
        if warnings:
            lines.append("")
            lines.append("**Warnings:**")
            for w in warnings:
                lines.append(f"- {w}")

        return "\n".join(lines)

    def _section_quality(self) -> str:
        q = self.quality_result
        lines = [
            "## 2. Intraday Data Quality",
            "",
        ]

        if not q or q.get("status") == "NO_DATA":
            lines.append("*No data available.*")
            return "\n".join(lines)

        overall = q.get("overall_quality_score", 0.0)
        lines.append(f"**Overall Quality Score:** {overall:.1f} / 100")
        lines.append("")

        results = q.get("results", [])
        if not results:
            lines.append("*No quality results available.*")
            return "\n".join(lines)

        lines.append(
            "| Symbol | Freq | Rows | Days | Latest Date | Coverage | Missing | "
            "Duplicates | Score | Status |"
        )
        lines.append(
            "|--------|------|------|------|------------|----------|---------|"
            "-----------|-------|--------|"
        )
        for r in results:
            coverage = r.get("average_coverage_ratio", 0.0)
            lines.append(
                f"| {r.get('symbol', '')} "
                f"| {r.get('freq', '')} "
                f"| {r.get('rows', 0)} "
                f"| {r.get('days', 0)} "
                f"| {r.get('latest_date', 'N/A')} "
                f"| {coverage:.1%} "
                f"| {r.get('missing_minutes', 0)} "
                f"| {r.get('duplicate_rows', 0)} "
                f"| {r.get('quality_score', 0.0):.1f} "
                f"| {r.get('quality_status', 'N/A')} |"
            )

        return "\n".join(lines)

    def _section_opening_range(self) -> str:
        lines = [
            "## 3. Opening Range Features",
            "",
        ]

        opening_data = self.feature_results.get("opening_range", {})
        if not opening_data:
            lines.append("*No data available.*")
            return "\n".join(lines)

        lines.append(
            "| Symbol | Opening Return 15m | Volume Ratio 15m | Range % | Strength Score |"
        )
        lines.append(
            "|--------|-------------------|-----------------|---------|----------------|"
        )

        # Support both dict-per-symbol and list format
        if isinstance(opening_data, dict):
            items = opening_data.items()
        else:
            items = [(r.get("symbol", "?"), r) for r in opening_data]

        for symbol, r in items:
            if r is None or r.get("status") == "NO_DATA":
                lines.append(f"| {symbol} | N/A | N/A | N/A | N/A |")
                continue
            ret15 = r.get("opening_return_15m")
            vol_ratio = r.get("opening_volume_ratio_15m")
            range_pct = r.get("opening_range_pct")
            strength = r.get("opening_strength_score")
            lines.append(
                f"| {symbol} "
                f"| {_fmt_pct(ret15)} "
                f"| {_fmt_float(vol_ratio)} "
                f"| {_fmt_pct(range_pct)} "
                f"| {_fmt_float(strength)} |"
            )

        return "\n".join(lines)

    def _section_vwap(self) -> str:
        lines = [
            "## 4. VWAP Features",
            "",
        ]

        vwap_data = self.feature_results.get("vwap", {})
        if not vwap_data:
            lines.append("*No data available.*")
            return "\n".join(lines)

        lines.append(
            "| Symbol | Price vs VWAP % | Above VWAP Ratio | VWAP Reclaim | Support Score |"
        )
        lines.append(
            "|--------|----------------|-----------------|-------------|--------------|"
        )

        if isinstance(vwap_data, dict):
            items = vwap_data.items()
        else:
            items = [(r.get("symbol", "?"), r) for r in vwap_data]

        for symbol, r in items:
            if r is None or r.get("status") == "NO_DATA":
                lines.append(f"| {symbol} | N/A | N/A | N/A | N/A |")
                continue
            pvp = r.get("price_vs_vwap_pct")
            avr = r.get("above_vwap_ratio")
            reclaim = r.get("vwap_reclaim")
            score = r.get("vwap_support_score")
            lines.append(
                f"| {symbol} "
                f"| {_fmt_float(pvp)} "
                f"| {_fmt_float(avr)} "
                f"| {reclaim if reclaim is not None else 'N/A'} "
                f"| {_fmt_float(score)} |"
            )

        return "\n".join(lines)

    def _section_fake_breakout(self) -> str:
        lines = [
            "## 5. Fake Breakout Detection",
            "",
        ]

        bk_data = self.feature_results.get("fake_breakout", {})
        if not bk_data:
            lines.append("*No data available.*")
            return "\n".join(lines)

        lines.append(
            "| Symbol | Breakout Quality | Fake BK Risk | Fake BK Score | Chase Risk Score |"
        )
        lines.append(
            "|--------|-----------------|-------------|--------------|-----------------|"
        )

        if isinstance(bk_data, dict):
            items = bk_data.items()
        else:
            items = [(r.get("symbol", "?"), r) for r in bk_data]

        for symbol, r in items:
            if r is None or r.get("status") == "NO_DATA":
                lines.append(f"| {symbol} | N/A | N/A | N/A | N/A |")
                continue
            lines.append(
                f"| {symbol} "
                f"| {r.get('breakout_quality', 'N/A')} "
                f"| {r.get('fake_breakout_risk', 'N/A')} "
                f"| {_fmt_float(r.get('fake_breakout_score'))} "
                f"| {_fmt_float(r.get('chase_risk_score'))} |"
            )

        return "\n".join(lines)

    def _section_volume_profile(self) -> str:
        lines = [
            "## 6. Intraday Volume Profile",
            "",
        ]

        vp_data = self.feature_results.get("volume_profile", {})
        if not vp_data:
            lines.append("*No data available.*")
            return "\n".join(lines)

        lines.append(
            "| Symbol | POC Price | Value Area High | Value Area Low | Support Pressure Score |"
        )
        lines.append(
            "|--------|-----------|----------------|---------------|----------------------|"
        )

        if isinstance(vp_data, dict):
            items = vp_data.items()
        else:
            items = [(r.get("symbol", "?"), r) for r in vp_data]

        for symbol, r in items:
            if r is None or r.get("status") == "NO_DATA":
                lines.append(f"| {symbol} | N/A | N/A | N/A | N/A |")
                continue
            lines.append(
                f"| {symbol} "
                f"| {_fmt_float(r.get('intraday_poc_price'))} "
                f"| {_fmt_float(r.get('intraday_value_area_high'))} "
                f"| {_fmt_float(r.get('intraday_value_area_low'))} "
                f"| {_fmt_float(r.get('intraday_support_pressure_score'))} |"
            )

        return "\n".join(lines)

    def _section_tick_bidask(self) -> str:
        ms_data = self.feature_results.get("microstructure", {})
        overall_ms = ms_data.get("overall_status", "TICK_PLANNED") if ms_data else "TICK_PLANNED"

        lines = [
            "## 7. Tick / BidAsk Readiness",
            "",
            "| Provider | Status | Note |",
            "|----------|--------|------|",
            "| Tick Data | PLANNED | Not available in v0.3.27 |",
            "| BidAsk Data | PLANNED | Not available in v0.3.27 |",
            f"| Microstructure Status | {overall_ms} | Bar data only |",
            "",
            "> Tick and BidAsk data providers are planned for a future version.",
            "> Current status: INTRADAY_BAR_ONLY for symbols with imported 1min/5min data.",
        ]

        results = ms_data.get("results", []) if ms_data else []
        if results:
            lines.append("")
            lines.append("**Per-symbol microstructure status:**")
            lines.append("")
            lines.append("| Symbol | Has 1min | Has 5min | Status |")
            lines.append("|--------|---------|---------|--------|")
            for r in results:
                lines.append(
                    f"| {r.get('symbol', '')} "
                    f"| {r.get('has_1min', False)} "
                    f"| {r.get('has_5min', False)} "
                    f"| {r.get('status', 'N/A')} |"
                )

        return "\n".join(lines)

    def _section_safety(self) -> str:
        lines = [
            "## 8. 安全聲明 (Safety Statement)",
            "",
            _SAFETY_BANNER,
            "- **Research Only** — All outputs are for research purposes only.",
            "- **Intraday Research Only** — Intraday data and features are for analytical use only.",
            "- **No Real Orders** — No signals or features herein should trigger actual order execution.",
            "- **Not Investment Advice** — Nothing in this report constitutes investment advice.",
            "- **Production Trading: BLOCKED** — This system must not be connected to any live trading infrastructure.",
        ]
        return "\n".join(lines)


# ------------------------------------------------------------------
# Format helpers
# ------------------------------------------------------------------

def _fmt_float(val, decimals: int = 2) -> str:
    if val is None:
        return "N/A"
    try:
        return f"{float(val):.{decimals}f}"
    except Exception:
        return str(val)


def _fmt_pct(val, decimals: int = 2) -> str:
    if val is None:
        return "N/A"
    try:
        return f"{float(val) * 100:.{decimals}f}%"
    except Exception:
        return str(val)
