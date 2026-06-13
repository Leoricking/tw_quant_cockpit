"""
reports/data_universe_expansion_report.py — Data Universe Expansion Report for TW Quant Cockpit v1.1.0.

Generates a Markdown report covering universe tiers, coverage, quality, confidence.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Not Investment Advice. Not a trading recommendation.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NO_REAL_ORDERS             = True
BROKER_DISABLED            = True
PRODUCTION_TRADING_BLOCKED = True


class DataUniverseExpansionReportBuilder:
    """
    Builds a Markdown Data Universe Expansion Report.

    Output: reports/data_universe_expansion_report_YYYY-MM-DD.md

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Not Investment Advice.
    """

    NO_REAL_ORDERS             = True
    BROKER_DISABLED            = True
    PRODUCTION_TRADING_BLOCKED = True

    def __init__(
        self,
        tier: str = "RESEARCH_30",
        mode: str = "real",
        report_dir: str = "reports",
        output_dir: str = "data/backtest_results/universe",
    ) -> None:
        self.tier = tier
        self.mode = mode
        self._report_dir = os.path.join(_BASE_DIR, report_dir) if not os.path.isabs(report_dir) else report_dir
        self._output_dir = os.path.join(_BASE_DIR, output_dir) if not os.path.isabs(output_dir) else output_dir

    def build(self) -> str:
        """Build and return the full Markdown report string."""
        from universe.universe_tier_registry import UniverseTierRegistry
        from universe.universe_coverage import UniverseCoverageAnalyzer
        from universe.universe_schema import (
            TIER_CORE_10, TIER_RESEARCH_30, TIER_EXPANDED_50, TIER_BROAD_100,
            QUALITY_READY, QUALITY_PARTIAL, QUALITY_INSUFFICIENT, QUALITY_MISSING,
        )
        from backtest.stat_confidence import StatConfidence

        registry = UniverseTierRegistry()
        analyzer = UniverseCoverageAnalyzer(mode=self.mode)

        # Build coverage for the target tier
        tier_syms = registry.list_by_tier(self.tier)
        sym_strs = [s.symbol for s in tier_syms]
        coverage = analyzer.analyze_symbols(sym_strs) if sym_strs else []
        summary = analyzer.build_coverage_summary(coverage, universe_id=self.tier)

        # Tier counts
        core10_count     = len(registry.list_by_tier(TIER_CORE_10))
        research30_count = len(registry.list_by_tier(TIER_RESEARCH_30))
        expanded50_count = len(registry.list_by_tier(TIER_EXPANDED_50))
        broad100_count   = len(registry.list_by_tier(TIER_BROAD_100))

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_str = datetime.now().strftime("%Y-%m-%d")

        conf_result = StatConfidence.for_universe_coverage(
            registered_symbols=summary.symbol_count,
            ready_symbols=len(summary.ready_symbols),
            evaluated_symbols=len(summary.ready_symbols) + len(summary.partial_symbols),
        )
        confidence = conf_result["overall"]
        conf_reasons = conf_result.get("reasons", [])

        lines: List[str] = []
        lines += [
            "# Data Universe Expansion Report v1.1.0",
            "",
            "> [!] Research Only. No Real Orders. Production Trading: BLOCKED.",
            "> [!] VALIDATED does not enable trading. Broker Execution Disabled.",
            "> [!] Not Investment Advice. Mock Data Formal Conclusion: DISABLED.",
            "",
            f"Generated: {now}",
            f"Mode: {self.mode}",
            f"Tier: {self.tier}",
            "",
        ]

        # 一、總覽
        lines += [
            "## 一、總覽",
            "",
            f"| Field                    | Value |",
            f"|--------------------------|-------|",
            f"| Version                  | 1.1.0 |",
            f"| Release                  | Data Universe Expansion |",
            f"| Research Only            | True |",
            f"| No Real Orders           | True |",
            f"| Data Source              | {self.mode} |",
            f"| Universe Tier            | {self.tier} |",
            f"| Registered Symbols       | {summary.symbol_count} |",
            f"| Ready Symbols            | {len(summary.ready_symbols)} |",
            f"| Partial Symbols          | {len(summary.partial_symbols)} |",
            f"| Missing Symbols          | {len(summary.missing_symbols)} |",
            f"| Statistical Confidence   | {confidence} |",
            "",
        ]

        # 二、Universe Tiers
        lines += [
            "## 二、Universe Tiers",
            "",
            f"| Tier          | Registered |",
            f"|---------------|-----------|",
            f"| CORE_10       | {core10_count} |",
            f"| RESEARCH_30   | {research30_count} |",
            f"| EXPANDED_50   | {expanded50_count} |",
            f"| BROAD_100     | {broad100_count} (schema supported) |",
            "",
            "Tiers are cumulative: RESEARCH_30 includes CORE_10 symbols.",
            "",
        ]

        # 三、Data Coverage
        lines += [
            "## 三、Data Coverage",
            "",
            f"| Data Type     | Ready Count | Total |",
            f"|---------------|------------|-------|",
            f"| Daily         | {summary.daily_ready} | {summary.symbol_count} |",
            f"| Volume        | {summary.volume_ready} | {summary.symbol_count} |",
            f"| Chips         | {summary.chips_ready} | {summary.symbol_count} |",
            f"| Revenue       | {summary.revenue_ready} | {summary.symbol_count} |",
            f"| Fundamentals  | {summary.fundamental_ready} | {summary.symbol_count} |",
            "",
            f"Average Trading Days: {summary.average_trading_days:.1f}",
            f"Average Missing Ratio: {summary.average_missing_ratio:.2%}",
            "",
        ]

        # 四、Symbol Quality
        lines += [
            "## 四、Symbol Quality",
            "",
            f"| Status       | Count | Symbols |",
            f"|--------------|-------|---------|",
            f"| READY        | {len(summary.ready_symbols)} | {', '.join(summary.ready_symbols[:10])} |",
            f"| PARTIAL      | {len(summary.partial_symbols)} | {', '.join(summary.partial_symbols[:10])} |",
            f"| INSUFFICIENT | {len(summary.insufficient_symbols)} | {', '.join(summary.insufficient_symbols[:10])} |",
            f"| MISSING      | {len(summary.missing_symbols)} | {', '.join(summary.missing_symbols[:10])} |",
            "",
            "Quality Rules:",
            "- READY: daily rows >= 240, OHLC completeness >= 98%, no invalid prices",
            "- PARTIAL: daily rows >= 120, OHLC completeness >= 90%",
            "- INSUFFICIENT: daily rows < 120",
            "- MISSING: no real daily data",
            "- INVALID: duplicate dates or broken schema",
            "",
        ]

        # 五、Missing Data
        lines += [
            "## 五、Missing Data",
            "",
        ]
        if summary.missing_symbols:
            lines.append("### Missing Symbols")
            lines.append("")
            for s in summary.missing_symbols:
                lines.append(f"- {s}")
            lines.append("")
        else:
            lines.append("No missing symbols detected for this tier.")
            lines.append("")

        lines += [
            "**Recommended Action**: FIX_DATA — import missing real data before running formal analysis.",
            "",
        ]

        # 六、Validation Readiness
        ready_count = len(summary.ready_symbols)
        partial_count = len(summary.partial_symbols)
        evaluated = ready_count + partial_count
        lines += [
            "## 六、Validation Readiness",
            "",
            f"| Task                              | Readiness |",
            f"|-----------------------------------|-----------|",
            f"| validate-score                    | {'READY' if ready_count >= 5 else 'INSUFFICIENT'} |",
            f"| backtest-buy-points               | {'READY' if ready_count >= 5 else 'INSUFFICIENT'} |",
            f"| backtest-screener                 | {'READY' if ready_count >= 8 else 'INSUFFICIENT'} |",
            f"| backtest-strategy-knowledge       | {'READY' if ready_count >= 10 else 'INSUFFICIENT'} |",
            f"| local assistant data confidence   | {confidence} |",
            "",
            f"Ready: {ready_count} | Partial: {partial_count} | Evaluated: {evaluated}",
            "",
        ]

        # 七、Statistical Confidence
        lines += [
            "## 七、Statistical Confidence",
            "",
            f"**Overall Confidence: {confidence}**",
            "",
            f"| Level          | Threshold |",
            f"|----------------|-----------|",
            f"| INSUFFICIENT   | evaluated < 10 symbols |",
            f"| OBSERVATIONAL  | evaluated 10–29 symbols |",
            f"| RELIABLE       | evaluated >= 30, signal >= 200, trading_days >= 120 |",
            "",
            "**Why current universe receives this grade:**",
            "",
        ]
        if conf_reasons:
            for r in conf_reasons:
                lines.append(f"- {r}")
        else:
            lines.append(f"- Evaluated symbols: {evaluated}")
        lines.append("")
        lines += [
            "> 3–5 symbols cannot claim RELIABLE. Minimum 30 evaluated symbols required.",
            "> Mock data cannot be used for formal conclusions.",
            "",
        ]

        # 八、Next Data Tasks
        lines += [
            "## 八、Next Data Tasks",
            "",
            "**Safe Actions (ALLOWED):**",
            "",
        ]
        if summary.missing_symbols:
            lines.append(f"- FIX_DATA: import real data for {len(summary.missing_symbols)} missing symbols")
        lines += [
            "- BACKTEST_MORE: run with more symbols after data import",
            "- REVIEW: review coverage gaps per symbol",
            "- KEEP_OBSERVING: continue monitoring data quality",
            "",
            "**Import commands:**",
            "```",
            "python main.py universe-coverage --tier research30",
            "python main.py universe-missing --tier research30",
            "python main.py universe-build --tier research30",
            "```",
            "",
            "> [!] Import real data via authorized data provider only.",
            "> [!] Do NOT auto-download without authorization.",
            "",
        ]

        # 九、安全聲明
        lines += [
            "## 九、安全聲明",
            "",
            "- [!] No Real Orders — This report does not enable trading.",
            "- [!] No Broker Execution — Broker API is disabled.",
            "- [!] Mock Data — NOT used for formal conclusions.",
            "- [!] VALIDATED does not enable trading.",
            "- [!] Not Investment Advice.",
            "- [!] Paper trading is simulation only.",
            "- [!] Mock realtime is simulation only.",
            "",
            "---",
            "",
            f"*TW Quant Cockpit v1.1.0 — Data Universe Expansion — Research Only — Not Investment Advice*",
            "",
        ]

        return "\n".join(lines)

    def save(self, content: Optional[str] = None) -> str:
        """Build (if needed) and save the report. Returns path."""
        if content is None:
            content = self.build()
        os.makedirs(self._report_dir, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"data_universe_expansion_report_{date_str}.md"
        path = os.path.join(self._report_dir, filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("DataUniverseExpansionReportBuilder saved: %s", path)
        except Exception as exc:
            logger.error("save: %s", exc)
        return path
