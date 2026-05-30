"""
tuning/rule_weight_report.py - Rule Weight Tuning Lab Markdown report (v0.3.15).

Generates an 8-section Markdown report from tuning results:

  1. Title & metadata
  2. Executive summary (best config, balanced_score, constraints)
  3. Config comparison table (all 7 configs ranked)
  4. Weight configuration table
  5. Best config detail
  6. Signal Quality Integration (how signal_quality_boosted was derived)
  7. Disqualified configs
  8. Limitations & advisory

[!] Advisory only. Does NOT auto-apply weights to production strategy.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_REPORTS_DIR = os.path.join(_BASE_DIR, "reports")


class RuleWeightReport:
    """Builds and saves a Markdown report from RuleWeightTuner results."""

    def __init__(self, results: dict):
        self._results = results

    def build(self) -> str:
        sections = [
            self._section_title(),
            self._section_executive_summary(),
            self._section_comparison_table(),
            self._section_weight_table(),
            self._section_best_config_detail(),
            self._section_signal_quality_integration(),
            self._section_disqualified(),
            self._section_limitations(),
        ]
        return "\n\n".join(s for s in sections if s)

    def save(self, output_dir: Optional[str] = None) -> str:
        out_dir = output_dir or _DEFAULT_REPORTS_DIR
        os.makedirs(out_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d")
        fname = f"rule_weight_tuning_report_{ts}.md"
        path = os.path.join(out_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.build())
        logger.info("RuleWeightReport saved: %s", path)
        return path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_title(self) -> str:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        mode = self._results.get("mode", "real")
        n = self._results.get("n_configs", 7)
        return (
            f"# Rule Weight Tuning Lab Report — v0.3.15\n\n"
            f"**Generated**: {ts}  \n"
            f"**Mode**: {mode}  \n"
            f"**Configs evaluated**: {n}  \n\n"
            f"> **[!] Advisory Only. Does NOT auto-apply weights to production strategy.**  \n"
            f"> **[!] Simulation Only. No real orders.**  \n"
            f"> For research and simulation only. Not investment advice."
        )

    def _section_executive_summary(self) -> str:
        best = self._results.get("best_config")
        best_sharpe = self._results.get("best_by_sharpe")
        best_dd = self._results.get("best_by_drawdown")
        best_pf = self._results.get("best_by_pf")
        df = self._results.get("comparison_df")

        lines = ["## Executive Summary\n"]

        if best is not None:
            lines.append(f"**Best config (balanced_score)**: `{best.name}`  ")
            if df is not None and not df.empty:
                row = df[df["config_name"] == best.name]
                if not row.empty:
                    r = row.iloc[0]
                    bs = r.get("balanced_score", "—")
                    ret = r.get("total_return")
                    sh = r.get("sharpe")
                    dd = r.get("max_drawdown")
                    pf = r.get("profit_factor")
                    lines.append(f"- Balanced score  : {_fmt_f(bs, 4)}")
                    lines.append(f"- Total return    : {_fmt_pct(ret)}")
                    lines.append(f"- Sharpe          : {_fmt_f(sh)}")
                    lines.append(f"- Max drawdown    : {_fmt_pct(dd)}")
                    lines.append(f"- Profit factor   : {_fmt_f(pf)}")
        else:
            lines.append("**Best config**: all configs disqualified (see section 7)")

        lines.append("")
        lines.append("**Best by individual metric:**")
        lines.append(f"- Highest Sharpe   : `{best_sharpe.name if best_sharpe else '—'}`")
        lines.append(f"- Least drawdown   : `{best_dd.name if best_dd else '—'}`")
        lines.append(f"- Highest PF       : `{best_pf.name if best_pf else '—'}`")
        lines.append("")
        lines.append(
            "**Disqualification thresholds**: MaxDD > 25%, PF < 1.20, trade_count < 30"
        )

        return "\n".join(lines)

    def _section_comparison_table(self) -> str:
        df = self._results.get("comparison_df")
        if df is None or df.empty:
            return "## Config Comparison\n\n*No data.*"

        lines = ["## Config Comparison (All 7 Configs)\n"]
        header = (
            "| Rank | Config | Return | Sharpe | MaxDD | PF | Trades | "
            "Balanced Score | DQ? |"
        )
        sep = "|------|--------|--------|--------|-------|-----|--------|----------------|-----|"
        lines += [header, sep]

        for _, row in df.iterrows():
            rank   = row.get("rank", "")
            name   = row.get("config_name", "")
            ret    = _fmt_pct(row.get("total_return"))
            sh     = _fmt_f(row.get("sharpe"))
            dd     = _fmt_pct(row.get("max_drawdown"))
            pf     = _fmt_f(row.get("profit_factor"))
            trades = int(row.get("trade_count", 0))
            bs     = _fmt_f(row.get("balanced_score", None), 4)
            dq     = "YES" if row.get("disqualified") else "no"
            lines.append(
                f"| {rank} | {name} | {ret} | {sh} | {dd} | {pf} | "
                f"{trades} | {bs} | {dq} |"
            )

        return "\n".join(lines)

    def _section_weight_table(self) -> str:
        df = self._results.get("comparison_df")
        if df is None or df.empty:
            return "## Weight Configurations\n\n*No data.*"

        lines = ["## Weight Configurations\n"]
        header = (
            "| Config | Bull | BuyPt | StratKnow | Fund | Intraday | Sector | Sum |"
        )
        sep = "|--------|------|-------|-----------|------|----------|--------|-----|"
        lines += [header, sep]

        for _, row in df.iterrows():
            name = row.get("config_name", "")
            b    = _fmt_w(row.get("bull_stock_w"))
            bp   = _fmt_w(row.get("buy_point_w"))
            sk   = _fmt_w(row.get("sk_w"))
            f_   = _fmt_w(row.get("fundamental_w"))
            i_   = _fmt_w(row.get("intraday_w"))
            s_   = _fmt_w(row.get("sector_w"))
            vals = [row.get(c) for c in
                    ["bull_stock_w","buy_point_w","sk_w","fundamental_w",
                     "intraday_w","sector_w"]]
            try:
                total = round(sum(float(v) for v in vals if v is not None), 3)
            except Exception:
                total = "—"
            lines.append(
                f"| {name} | {b} | {bp} | {sk} | {f_} | {i_} | {s_} | {total} |"
            )

        return "\n".join(lines)

    def _section_best_config_detail(self) -> str:
        best = self._results.get("best_config")
        if best is None:
            return "## Best Config Detail\n\n*No qualified configs found.*"

        df = self._results.get("comparison_df")
        lines = [f"## Best Config Detail: `{best.name}`\n"]
        lines.append(f"**Description**: {best.description}  ")
        lines.append(f"**Source**: {best.source}  \n")

        lines.append("**Signal Weights:**\n")
        lines.append("| Component | Weight |")
        lines.append("|-----------|--------|")
        lines.append(f"| bull_stock_score (Screener) | {best.bull_stock_weight} |")
        lines.append(f"| buy_point_score (A/B/C)     | {best.buy_point_weight} |")
        lines.append(f"| strategy_knowledge_score    | {best.strategy_knowledge_weight} |")
        lines.append(f"| fundamental_quality_score   | {best.fundamental_weight} |")
        lines.append(f"| microstructure_score        | {best.intraday_weight} |")
        lines.append(f"| sector_strength_score       | {best.sector_strength_weight} |")
        lines.append(f"| **Sum**                     | **{best.weight_sum()}** |")

        lines.append("\n**Penalty Weights:**\n")
        lines.append("| Penalty | Value |")
        lines.append("|---------|-------|")
        lines.append(f"| no_chase_warning       | {best.penalty_no_chase} |")
        lines.append(f"| fake_breakout_risk      | {best.penalty_fake_breakout} |")
        lines.append(f"| fundamental_warning     | {best.penalty_fundamental_warn} |")
        lines.append(f"| overvalued_warning      | {best.penalty_overvalued} |")
        lines.append(f"| timing_estimated        | {best.penalty_timing_estimated} |")
        lines.append(f"| sector_concentration    | {best.penalty_sector_conc} |")

        # Metrics row from comparison
        if df is not None and not df.empty:
            row = df[df["config_name"] == best.name]
            if not row.empty:
                r = row.iloc[0]
                lines.append("\n**Simulation Metrics:**\n")
                lines.append("| Metric | Value |")
                lines.append("|--------|-------|")
                lines.append(f"| Total return   | {_fmt_pct(r.get('total_return'))} |")
                lines.append(f"| Sharpe         | {_fmt_f(r.get('sharpe'))} |")
                lines.append(f"| Max drawdown   | {_fmt_pct(r.get('max_drawdown'))} |")
                lines.append(f"| Profit factor  | {_fmt_f(r.get('profit_factor'))} |")
                lines.append(f"| Win rate       | {_fmt_pct(r.get('win_rate'), sign=False)} |")
                lines.append(f"| Trade count    | {int(r.get('trade_count', 0))} |")
                lines.append(f"| Balanced score | {_fmt_f(r.get('balanced_score'), 4)} |")

        return "\n".join(lines)

    def _section_signal_quality_integration(self) -> str:
        se_df = self._results.get("signal_effects_df")
        all_r = self._results.get("all_results", {})
        sq_result = all_r.get("signal_quality_boosted", {})

        lines = ["## Signal Quality Integration\n"]
        lines.append(
            "The `signal_quality_boosted` config is derived from "
            "`data/backtest_results/signal_quality_summary.csv`. "
            "For each signal group, the dominant recommendation "
            "(BOOST/KEEP/REDUCE/DISABLE/INSUFFICIENT_SAMPLE) adjusts "
            "the corresponding weight: BOOST ×1.15, KEEP ×1.00, "
            "REDUCE ×0.85, DISABLE ×0.60.\n"
        )

        # Show SQ result status
        sq_status = sq_result.get("status", "error")
        lines.append(f"**signal_quality_boosted simulation status**: `{sq_status}`\n")

        # Weight delta table
        if se_df is not None and not se_df.empty and "signal_quality_boosted" in se_df.columns:
            lines.append(
                "**Weight changes vs baseline** (signal_quality_boosted):\n"
            )
            lines.append("| Signal | Baseline | Boosted | Delta |")
            lines.append("|--------|----------|---------|-------|")
            for _, row in se_df.iterrows():
                sig     = row.get("signal", "")
                base_w  = row.get("baseline", 0)
                boost_w = row.get("signal_quality_boosted", 0)
                delta   = row.get("signal_quality_boosted_delta", 0)
                delta_s = f"+{delta:.4f}" if delta >= 0 else f"{delta:.4f}"
                lines.append(
                    f"| {sig} | {base_w:.4f} | {boost_w:.4f} | {delta_s} |"
                )

        return "\n".join(lines)

    def _section_disqualified(self) -> str:
        df = self._results.get("comparison_df")
        if df is None or df.empty:
            return ""

        dq_df = df[df["disqualified"] == True]
        if dq_df.empty:
            return "## Disqualified Configs\n\nAll configs passed disqualification thresholds."

        lines = ["## Disqualified Configs\n"]
        lines.append(
            "The following configs were excluded from best-config selection "
            "because they failed one or more thresholds "
            "(MaxDD > 25%, PF < 1.20, trade_count < 30):\n"
        )
        lines.append("| Config | Reason |")
        lines.append("|--------|--------|")
        for _, row in dq_df.iterrows():
            name   = row.get("config_name", "")
            reason = row.get("dq_reason", "")
            lines.append(f"| {name} | {reason} |")

        return "\n".join(lines)

    def _section_limitations(self) -> str:
        warnings = self._results.get("warnings", [])
        lines = [
            "## Limitations & Advisory\n",
            "- This tuning lab compares 7 weight configurations using the same "
            "historical dataset. Results may overfit to the available data.",
            "- Universe is currently 14 symbols → **OBSERVATIONAL** confidence. "
            "Do not draw definitive conclusions.",
            "- The signal_quality_boosted config reflects past backtest quality "
            "and does not guarantee future performance.",
            "- **Recommendations do NOT automatically change strategy weights.** "
            "Human review and confirmation required.",
            "- Simulation uses signal-date close entry (potential same-day "
            "execution bias). Future improvement: next-day open entry.",
            "- Fundamental data is a static snapshot (timing_estimated flag "
            "marks estimated announcement dates).",
            "",
            "> **[!] Simulation Only. No Real Orders.**  ",
            "> **[!] Advisory Only. Does NOT auto-apply weights.**  ",
            "> Not investment advice.",
        ]

        if warnings:
            lines.append("\n**Warnings:**")
            for w in warnings:
                lines.append(f"- {w}")

        return "\n".join(lines)


# ------------------------------------------------------------------
# Formatters
# ------------------------------------------------------------------

def _fmt_pct(v, sign=True) -> str:
    if v is None:
        return "—"
    try:
        f = float(v)
        return f"{f*100:+.2f}%" if sign else f"{f*100:.2f}%"
    except Exception:
        return str(v)


def _fmt_f(v, decimals: int = 2) -> str:
    if v is None:
        return "—"
    try:
        return f"{float(v):.{decimals}f}"
    except Exception:
        return str(v)


def _fmt_w(v) -> str:
    if v is None:
        return "—"
    try:
        return f"{float(v):.4f}"
    except Exception:
        return str(v)
