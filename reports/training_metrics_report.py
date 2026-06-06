"""
reports/training_metrics_report.py — TrainingMetricsReportBuilder v0.8.2

Generate the Backtest Training Metrics Markdown report.

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

_DEFAULT_OUTPUT_DIR  = os.path.join(BASE_DIR, "reports")
_DEFAULT_METRICS_DIR = "data/backtest_results/training_metrics"


class TrainingMetricsReportBuilder:
    """Generate the v0.8.2 Backtest Training Metrics Markdown report.

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
        mode:           str = "real",
        output_dir:     str = _DEFAULT_OUTPUT_DIR,
        metrics_output_dir: str = _DEFAULT_METRICS_DIR,
    ) -> str:
        """Build the report. Returns path to generated Markdown file."""
        if not os.path.isabs(output_dir):
            output_dir = os.path.join(BASE_DIR, output_dir)
        if not os.path.isabs(metrics_output_dir):
            metrics_output_dir = os.path.join(BASE_DIR, metrics_output_dir)

        data    = self._load_or_run(mode=mode, metrics_output_dir=metrics_output_dir)
        metrics = data.get("metrics", [])
        summary = data.get("summary")

        lines   = self._build_lines(metrics, summary)
        content = "\n".join(lines) + "\n"

        os.makedirs(output_dir, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        path  = os.path.join(output_dir, f"training_metrics_report_{today}.md")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("TrainingMetricsReportBuilder: report written -> %s", path)
        except Exception as exc:
            logger.warning("TrainingMetricsReportBuilder: write error: %s", exc)
        return path

    # ------------------------------------------------------------------
    # Internal: load or run
    # ------------------------------------------------------------------

    def _load_or_run(self, mode: str, metrics_output_dir: str) -> dict:
        """Load from store; run engine if no data."""
        try:
            from training_metrics.training_metrics_store import TrainingMetricsStore
            from training_metrics.training_metrics_schema import TrainingMetric, TrainingMetricsSummary
            store   = TrainingMetricsStore(output_dir=metrics_output_dir)
            metrics = store.load_latest_metrics()
            summary = store.load_latest_summary()
            if metrics and summary:
                return {"metrics": metrics, "summary": summary}
        except Exception as exc:
            logger.warning("TrainingMetricsReportBuilder: store load error: %s", exc)

        try:
            from training_metrics.training_metrics_engine import TrainingMetricsEngine
            engine = TrainingMetricsEngine(
                project_root=BASE_DIR,
                output_dir=metrics_output_dir,
            )
            return engine.run(mode=mode)
        except Exception as exc:
            logger.warning("TrainingMetricsReportBuilder: engine run error: %s", exc)
            return {"metrics": [], "summary": None}

    # ------------------------------------------------------------------
    # Internal: build Markdown
    # ------------------------------------------------------------------

    def _build_lines(self, metrics, summary) -> List[str]:
        lines: List[str] = []
        lines += self._section_header()
        lines += self._section_overview(summary)
        lines += self._section_metrics_table(metrics)
        lines += self._section_trend_analysis(metrics, summary)
        lines += self._section_known_limitations()
        lines += self._section_safety_declaration()
        return lines

    def _section_header(self) -> List[str]:
        today = datetime.now().strftime("%Y-%m-%d")
        return [
            "# Backtest Training Metrics Report v0.8.2",
            "",
            f"**Date:** {today}",
            "",
            "> **[!] Research Only. No Real Orders. Production Trading BLOCKED.**",
            "> **[!] Not Investment Advice.**",
            "",
            "---",
            "",
        ]

    def _section_overview(self, summary) -> List[str]:
        lines = ["## Training Effectiveness Overview", ""]
        if summary and hasattr(summary, "total_metrics"):
            s = summary
            lines += [
                "| Field | Value |",
                "|-------|-------|",
                f"| Version | {s.version} |",
                f"| Period | {s.period} |",
                f"| Mode | {s.mode} |",
                f"| Total Metrics | {s.total_metrics} |",
                f"| Improving | {s.improving_count} |",
                f"| Stable | {s.stable_count} |",
                f"| Worsening | {s.worsening_count} |",
                f"| Insufficient Data | {s.insufficient_count} |",
                f"| Overall Trend | **{s.overall_trend}** |",
                f"| Overall Score | {s.overall_score}% |",
                f"| Task Completion Rate | {s.task_completion_rate}% |",
                f"| Avg Replay Score | {s.replay_score_avg} |",
                f"| Mistake Reduction | {s.mistake_reduction_pct}% |",
                f"| Memory Validation Rate | {s.memory_validation_rate}% |",
                f"| Training Sessions | {s.training_streak_days} |",
            ]
            if s.top_improving_metric:
                lines.append(f"| Top Improving | {s.top_improving_metric} |")
            if s.top_worsening_metric:
                lines.append(f"| Top Worsening | {s.top_worsening_metric} |")
        else:
            lines += ["*(No summary available — run: python main.py training-metrics --mode real)*"]
        lines += ["", "---", ""]
        return lines

    def _section_metrics_table(self, metrics) -> List[str]:
        lines = [
            "## Metrics Detail",
            "",
            f"**Total Metrics:** {len(metrics)}",
            "",
        ]
        if metrics:
            lines += [
                "| Metric | Type | Source | Value | Unit | Trend | Status | Description |",
                "|--------|------|--------|-------|------|-------|--------|-------------|",
            ]
            for m in metrics:
                desc = (m.description[:50] + "...") if len(m.description) > 50 else m.description
                lines.append(
                    f"| {m.label} | {m.metric_type} | {m.source_module} "
                    f"| {m.value} | {m.unit} | {m.trend} | {m.status} | {desc} |"
                )
        else:
            lines.append("*(No metrics loaded — run: python main.py training-metrics --mode real)*")
        lines += ["", "---", ""]
        return lines

    def _section_trend_analysis(self, metrics, summary) -> List[str]:
        lines = ["## Trend Analysis", ""]
        if not metrics:
            lines += ["*(No metrics available)*", "", "---", ""]
            return lines

        from training_metrics.training_metrics_schema import (
            TREND_IMPROVING, TREND_WORSENING, STATUS_INSUFFICIENT_DATA,
        )
        improving = [m for m in metrics if m.trend == TREND_IMPROVING]
        worsening = [m for m in metrics if m.trend == TREND_WORSENING]
        insuf     = [m for m in metrics if m.status == STATUS_INSUFFICIENT_DATA]

        if improving:
            lines.append("**Improving Metrics:**")
            for m in improving:
                lines.append(f"- {m.label}: {m.value} {m.unit}")
            lines.append("")

        if worsening:
            lines.append("**Worsening Metrics (attention needed):**")
            for m in worsening:
                lines.append(f"- {m.label}: {m.value} {m.unit}")
            lines.append("")

        if insuf:
            lines.append("**Insufficient Data (run source module first):**")
            for m in insuf:
                lines.append(f"- {m.label} (source: {m.source_module})")
            lines.append("")

        lines += ["---", ""]
        return lines

    def _section_known_limitations(self) -> List[str]:
        return [
            "## Known Limitations",
            "",
            "1. Metrics are collected from CSV outputs — no live data feed",
            "2. INSUFFICIENT_DATA shown when source module has not been run yet",
            "3. Trend direction requires at least two data points in history",
            "4. No investment advice — all outputs are research metrics only",
            "5. No automatic strategy activation based on any metric",
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
            "*TW Quant Cockpit v0.8.2 — Backtest Training Metrics — Research Only — Not Investment Advice*",
            "",
        ]
