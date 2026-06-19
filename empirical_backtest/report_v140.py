"""
empirical_backtest/report_v140.py — Empirical Backtest Report for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from .models_v140 import BacktestResult, BacktestConfiguration

SAFETY_FOOTER = (
    "Research Only | No Real Orders | Broker Execution Disabled | "
    "Production Trading BLOCKED | Backtest Does Not Guarantee Future Performance"
)


class EmpiricalBacktestReport:
    """Generates text and markdown reports for empirical backtest results."""

    def generate_text(self, result: BacktestResult, config: BacktestConfiguration = None) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append("EMPIRICAL BACKTEST REPORT v1.4.0")
        lines.append("=" * 60)

        # Section 1: Summary
        lines.append("")
        lines.append("[1] SUMMARY")
        lines.append(f"  Backtest ID:          {result.backtest_id}")
        lines.append(f"  Strategy Snapshot ID: {result.strategy_snapshot_id}")
        lines.append(f"  Status:               {result.status}")
        lines.append(f"  Trade Count:          {result.trade_count}")
        lines.append(f"  Started At:           {result.started_at}")
        lines.append(f"  Finished At:          {result.finished_at}")

        # Section 2: Date Range
        lines.append("")
        lines.append("[2] DATE RANGE")
        dr = result.date_range
        lines.append(f"  Start: {dr.get('start', 'N/A')}")
        lines.append(f"  End:   {dr.get('end', 'N/A')}")

        # Section 3: Symbols
        lines.append("")
        lines.append("[3] SYMBOLS")
        lines.append(f"  Requested: {result.symbols_requested}")
        lines.append(f"  Tested:    {result.symbols_tested}")
        lines.append(f"  Blocked:   {result.symbols_blocked}")

        # Section 4: Metrics
        lines.append("")
        lines.append("[4] PERFORMANCE METRICS")
        for k, v in result.metrics.items():
            if k == "assumptions":
                continue
            lines.append(f"  {k}: {v}")

        # Section 5: Benchmark
        lines.append("")
        lines.append("[5] BENCHMARK")
        for k, v in result.benchmark_metrics.items():
            lines.append(f"  {k}: {v}")

        # Section 6: Blocked Reasons
        if result.blocked_reasons:
            lines.append("")
            lines.append("[6] BLOCKED REASONS")
            for reason in result.blocked_reasons:
                lines.append(f"  - {reason}")

        # Section 7: Warnings
        if result.warnings:
            lines.append("")
            lines.append("[7] WARNINGS")
            for warning in result.warnings:
                lines.append(f"  - {warning}")

        # Section 8: Quality Summary
        lines.append("")
        lines.append("[8] QUALITY SUMMARY")
        for k, v in result.quality_summary.items():
            lines.append(f"  {k}: {v}")

        # Section 9: Reproducibility
        lines.append("")
        lines.append("[9] REPRODUCIBILITY")
        lines.append(f"  Hash: {result.reproducibility_hash}")

        # Safety Footer
        lines.append("")
        lines.append("=" * 60)
        lines.append(f"[!] {SAFETY_FOOTER}")
        lines.append("=" * 60)

        return "\n".join(lines)

    def generate_markdown(self, result: BacktestResult, config: BacktestConfiguration = None) -> str:
        lines = []
        lines.append("# Empirical Backtest Report v1.4.0")
        lines.append("")
        lines.append(f"> **[!] {SAFETY_FOOTER}**")
        lines.append("")

        lines.append("## Summary")
        lines.append(f"- **Backtest ID:** {result.backtest_id}")
        lines.append(f"- **Status:** {result.status}")
        lines.append(f"- **Trade Count:** {result.trade_count}")
        lines.append("")

        lines.append("## Performance Metrics")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        for k, v in result.metrics.items():
            if k == "assumptions":
                continue
            lines.append(f"| {k} | {v} |")
        lines.append("")

        lines.append("## Blocked Reasons")
        for r in result.blocked_reasons:
            lines.append(f"- {r}")
        lines.append("")

        lines.append("## Warnings")
        for w in result.warnings:
            lines.append(f"- {w}")
        lines.append("")

        lines.append(f"---")
        lines.append(f"**[!] {SAFETY_FOOTER}**")

        return "\n".join(lines)
