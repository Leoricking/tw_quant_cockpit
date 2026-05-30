"""
reports/signal_quality_report.py - Signal Quality Dashboard Markdown report (v0.3.14).

Generates a multi-section Markdown report from SignalQualityEngine output.

Sections:
  1. 總覽 (Overview)
  2. A/B/C 買點品質
  3. Screener 分數品質
  4. Strategy Knowledge 規則品質
  5. Long-Term 因子品質
  6. Portfolio Scenario 品質
  7. Microstructure 品質
  8. 建議調整
  9. 限制與風險

Output: reports/signal_quality_report_YYYY-MM-DD.md
"""

from __future__ import annotations

import logging
import os
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_REC_LABELS = {
    "BOOST":              "BOOST — 建議加權",
    "KEEP":               "KEEP — 維持現狀",
    "REDUCE":             "REDUCE — 建議降權",
    "DISABLE":            "DISABLE — 建議停用",
    "INSUFFICIENT_SAMPLE":"INSUFFICIENT_SAMPLE — 樣本不足，暫不判斷",
}


class SignalQualityReport:
    """Generates Markdown report from signal quality summary DataFrame."""

    def __init__(self, results: dict):
        """
        results: dict returned by SignalQualityEngine.run()
        """
        self.results     = results
        self.summary_df  = results.get("summary_df", pd.DataFrame())
        self.warnings    = results.get("warnings", [])
        self.sources_found   = results.get("sources_found", [])
        self.sources_missing = results.get("sources_missing", [])

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def build(self) -> str:
        """Build and return the full Markdown report string."""
        sections = [
            self._section_title(),
            self._section_overview(),
            self._section_buy_point(),
            self._section_screener(),
            self._section_strategy_knowledge(),
            self._section_long_term(),
            self._section_portfolio(),
            self._section_microstructure(),
            self._section_recommendations(),
            self._section_limitations(),
        ]
        return "\n\n".join(s for s in sections if s)

    def save(self, output_dir: str = None) -> str:
        """Save report to file. Returns path."""
        if output_dir is None:
            output_dir = os.path.join(_BASE_DIR, "reports")
        os.makedirs(output_dir, exist_ok=True)
        ts   = datetime.now().strftime("%Y-%m-%d")
        path = os.path.join(output_dir, f"signal_quality_report_{ts}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.build())
        logger.info("SignalQualityReport: saved to %s", path)
        return path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_title(self) -> str:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        return (
            f"# Signal Quality Dashboard Report\n\n"
            f"*Generated: {ts}*\n\n"
            f"**[!] Simulation Only. No Real Orders. "
            f"Recommendations do not automatically change strategy weights.**"
        )

    def _section_overview(self) -> str:
        df = self.summary_df
        total = len(df)
        if total == 0:
            return "## 一、總覽\n\nNo signal quality data available. Run backtests first."

        rec_counts = df["recommendation"].value_counts().to_dict() if "recommendation" in df.columns else {}
        boost = rec_counts.get("BOOST", 0)
        keep  = rec_counts.get("KEEP", 0)
        red   = rec_counts.get("REDUCE", 0)
        dis   = rec_counts.get("DISABLE", 0)
        ins   = rec_counts.get("INSUFFICIENT_SAMPLE", 0)

        conf_vals = df["confidence"].unique().tolist() if "confidence" in df.columns else []
        groups    = df["signal_group"].unique().tolist() if "signal_group" in df.columns else []

        lines = [
            "## 一、總覽",
            "",
            f"- **Data sources found:** {', '.join(self.sources_found) or '—'}",
            f"- **Data sources missing:** {', '.join(self.sources_missing) or 'none'}",
            f"- **Universe size:** 14 symbols",
            f"- **Total signals analyzed:** {total}",
            f"- **Signal groups:** {', '.join(str(g) for g in groups)}",
            f"- **Statistical confidence:** OBSERVATIONAL (14 symbols < 30 threshold)",
            "",
            "**Recommendation Summary:**",
            "",
            f"| Recommendation | Count |",
            f"|----------------|-------|",
            f"| BOOST          | {boost} |",
            f"| KEEP           | {keep} |",
            f"| REDUCE         | {red} |",
            f"| DISABLE        | {dis} |",
            f"| INSUFFICIENT_SAMPLE | {ins} |",
            f"| **Total**      | **{total}** |",
            "",
            "**Overall Conclusion:**",
            "Results are observational only. With 14 symbols, no recommendation should be treated "
            "as statistically reliable. Use as preliminary directional guidance.",
        ]
        if self.warnings:
            lines += ["", "**Warnings:**"] + [f"- {w}" for w in self.warnings]
        return "\n".join(lines)

    def _section_buy_point(self) -> str:
        df = self._filter(self.summary_df, source="buy_point")
        lines = ["## 二、A/B/C 買點品質", ""]
        if df.empty:
            lines.append("*Buy-point backtest data not found. Run: `python main.py backtest-buy-points --mode real`*")
            return "\n".join(lines)
        lines += _df_to_table(df, cols=["signal_name", "sample_count", "win_rate", "avg_return",
                                         "profit_factor", "max_drawdown", "confidence", "recommendation", "reason"])
        return "\n".join(lines)

    def _section_screener(self) -> str:
        df = self._filter(self.summary_df, source="screener")
        lines = ["## 三、Screener 分數品質", ""]
        if df.empty:
            lines.append("*Screener backtest data not found. Run: `python main.py validate-score --mode real`*")
            return "\n".join(lines)
        lines += _df_to_table(df, cols=["signal_name", "sample_count", "win_rate", "avg_return",
                                         "profit_factor", "max_drawdown", "confidence", "recommendation", "reason"])
        return "\n".join(lines)

    def _section_strategy_knowledge(self) -> str:
        df = self._filter(self.summary_df, source="strategy_knowledge")
        lines = ["## 四、Strategy Knowledge 規則品質", ""]
        if df.empty:
            lines.append("*Strategy Knowledge backtest data not found. Run: "
                         "`python main.py backtest-strategy-knowledge --mode real`*")
            return "\n".join(lines)
        lines += _df_to_table(df, cols=["signal_group", "signal_name", "sample_count", "win_rate",
                                         "avg_return", "profit_factor", "confidence", "recommendation", "reason"])
        return "\n".join(lines)

    def _section_long_term(self) -> str:
        df = self._filter(self.summary_df, source="long_term")
        lines = [
            "## 五、Long-Term 因子品質",
            "",
            "> TIMING_ESTIMATED limitation: financial announcement dates may be estimated by legal "
            "deadline, not confirmed MOPS publication date. Results have forward-looking bias risk.",
            "",
        ]
        if df.empty:
            lines.append("*Long-term factor data not found. Run: "
                         "`python main.py backtest-long-term-strategy --mode real`*")
            return "\n".join(lines)
        lines += _df_to_table(df, cols=["signal_group", "signal_name", "sample_count", "win_rate",
                                         "avg_return", "profit_factor", "confidence", "recommendation", "reason"])
        return "\n".join(lines)

    def _section_portfolio(self) -> str:
        df = self._filter(self.summary_df, source="portfolio")
        lines = ["## 六、Portfolio Scenario 品質", ""]
        if df.empty:
            lines.append("*Portfolio simulation data not found. Run: "
                         "`python main.py simulate-portfolio --mode real --scenario all`*")
            return "\n".join(lines)
        lines += _df_to_table(df, cols=["signal_name", "sample_count", "avg_return",
                                         "profit_factor", "max_drawdown", "sharpe",
                                         "confidence", "recommendation", "reason"])
        return "\n".join(lines)

    def _section_microstructure(self) -> str:
        df = self._filter(self.summary_df, source="microstructure")
        lines = [
            "## 七、Microstructure 品質",
            "",
            "> Intraday microstructure signals (opening_return_15m, volume_ratio, high_break, "
            "fake_breakout_warning) have not been independently backtested yet.",
            "> First version reports coverage status only.",
            "",
        ]
        if df.empty:
            lines.append("*Microstructure quality data not available.*")
            return "\n".join(lines)
        lines += _df_to_table(df, cols=["signal_name", "confidence", "data_quality", "recommendation", "reason"])
        return "\n".join(lines)

    def _section_recommendations(self) -> str:
        df = self.summary_df
        if df.empty:
            return "## 八、建議調整\n\n*No data available.*"

        lines = ["## 八、建議調整", ""]
        rec_col = "recommendation"
        if rec_col not in df.columns:
            lines.append("*Recommendations not computed.*")
            return "\n".join(lines)

        for rec_key, rec_label in _REC_LABELS.items():
            subset = df[df[rec_col] == rec_key]
            if subset.empty:
                continue
            lines.append(f"### {rec_label}")
            lines.append("")
            for _, row in subset.iterrows():
                src  = row.get("source", "?")
                name = row.get("signal_name", "?")
                grp  = row.get("signal_group", "")
                rsn  = row.get("reason", "")
                lines.append(f"- **[{src}]** {grp}/{name} — {rsn}")
            lines.append("")
        return "\n".join(lines)

    def _section_limitations(self) -> str:
        return """## 九、限制與風險

- **14-symbol universe only.** Statistical confidence is OBSERVATIONAL for all signals.
- **Backtest only.** All results are in-sample or walk-forward on historical data. Not live trading.
- **Simulation only.** No real orders. No broker API. No account connection.
- **Signal-date close entry assumption.** Entry uses close price on signal date (first version). Forward-looking bias possible for same-day signals.
- **OBSERVATIONAL confidence.** Results confirm framework functionality but cannot claim strategy effectiveness.
- **TIMING_ESTIMATED announcement dates.** Fundamental data uses static snapshot. Some announcement dates estimated by legal deadline, not confirmed MOPS publication.
- **Simple fee/slippage model.** Real-world friction may be higher.
- **Recommendation is advisory only.** Does not automatically change strategy weights.
- **No real orders will be sent.**

> **[!] 本報告僅供研究與模擬，不構成投資建議。**
> 所有推薦均為建議，不自動調整策略權重，不構成實盤操作依據。

---

*TW Quant Cockpit v0.3.14 — Signal Quality Dashboard*"""

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _filter(self, df: pd.DataFrame, source: str) -> pd.DataFrame:
        if df.empty or "source" not in df.columns:
            return pd.DataFrame()
        return df[df["source"] == source].copy()


def _df_to_table(df: pd.DataFrame, cols: list) -> list[str]:
    """Convert DataFrame to Markdown table lines."""
    available = [c for c in cols if c in df.columns]
    if not available:
        return [f"*Columns not found: {cols}*"]

    header = "| " + " | ".join(available) + " |"
    sep    = "| " + " | ".join(["---"] * len(available)) + " |"
    rows   = [header, sep]
    for _, row in df.iterrows():
        cells = []
        for c in available:
            v = row.get(c)
            if v is None or (isinstance(v, float) and v != v):
                cells.append("—")
            elif c in ("win_rate", "avg_return", "median_return", "max_drawdown"):
                try:
                    cells.append(f"{float(v)*100:.2f}%")
                except Exception:
                    cells.append(str(v))
            elif c in ("profit_factor", "sharpe"):
                try:
                    cells.append(f"{float(v):.3f}")
                except Exception:
                    cells.append(str(v))
            else:
                cells.append(str(v))
        rows.append("| " + " | ".join(cells) + " |")
    return rows
