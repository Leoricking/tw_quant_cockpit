"""
reports/buy_point_validation_report.py - Markdown buy-point validation report generator.

Reads from BuyPointBacktester results and generates a structured Markdown report
covering A/B/C grade win rates, average returns, stop-loss rates, and conclusions.

Usage:
    from reports.buy_point_validation_report import BuyPointValidationReport
    rpt = BuyPointValidationReport(results)
    path = rpt.save()
    print(rpt.build())
"""

import os
import logging
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)
_DASH = '\u2014'   # em dash — safe to use inside f-string variables

_BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REPORTS_DIR = os.path.join(_BASE_DIR, 'reports')


def _pct(v, decimals=2):
    if v is None:
        return '—'
    try:
        f = float(v)
        if pd.isna(f):
            return '—'
        return f"{f:+.{decimals}f}%"
    except (TypeError, ValueError):
        return '—'


def _val(v, decimals=2):
    if v is None:
        return '—'
    try:
        f = float(v)
        if pd.isna(f):
            return '—'
        return f"{f:.{decimals}f}"
    except (TypeError, ValueError):
        return '—'


class BuyPointValidationReport:
    """Generates a Markdown report from BuyPointBacktester results."""

    def __init__(self, results: dict):
        self.results   = results or {}
        self._date_str = datetime.now().strftime('%Y-%m-%d')

    def build(self) -> str:
        """Assemble and return the full Markdown report."""
        r = self.results
        lines = []

        lines.append("# TW Quant Cockpit Buy Point Validation Report")
        lines.append("")
        lines.append("> NOTE: This report is for research reference only and does not constitute investment advice.")
        lines.append("> Live order execution is disabled in v1.")
        lines.append("")

        # ---- 1. Validation overview ----
        lines.append("## 1. Validation Overview")
        lines.append("")
        lines.append(f"- Total signals : {r.get('n_signals', 0)}")
        src_tag = 'REAL CSV SAMPLE' if r.get('is_sample') else 'REAL CSV'
        lines.append(f"- Data source   : {src_tag}")
        _dsrc = r.get('data_source', _DASH)
        lines.append(f"- Data path     : `{_dsrc}`")
        lines.append(f"- Report date   : {self._date_str}")

        conf = r.get('confidence', {})
        overall = conf.get('overall', 'INSUFFICIENT')
        lines.append(f"- Statistical confidence: {overall}")
        for reason in conf.get('reasons', []):
            lines.append(f"  - {reason}")
        lines.append("")

        # ---- 2. A/B/C grade summary ----
        lines.append("## 2. A/B/C Grade Summary")
        lines.append("")
        grade_df = r.get('grade_df', pd.DataFrame())
        if grade_df is not None and not grade_df.empty:
            lines.append("| Grade | Signals | Win 5d% | Win 10d% | Win 20d% | Avg ret 20d% | Med ret 20d% | Stop-loss% | Profit factor | Confidence | Note |")
            lines.append("|-------|---------|---------|----------|----------|-------------|-------------|------------|--------------|------------|------|")
            for _, row in grade_df.iterrows():
                note   = row.get('sample_note', '')
                gconf  = row.get('grade_confidence', 'INSUFFICIENT')
                _grade = row.get('buy_point_grade', _DASH)
                _nsig  = row.get('signal_count', _DASH)
                lines.append(
                    f"| {_grade} "
                    f"| {_nsig} "
                    f"| {_pct(row.get('win_rate_5d'))} "
                    f"| {_pct(row.get('win_rate_10d'))} "
                    f"| {_pct(row.get('win_rate_20d'))} "
                    f"| {_pct(row.get('avg_return_20d'))} "
                    f"| {_pct(row.get('median_return_20d'))} "
                    f"| {_pct(row.get('stop_loss_hit_rate'))} "
                    f"| {_val(row.get('profit_factor'))} "
                    f"| {gconf} "
                    f"| {note} |"
                )
        else:
            lines.append("_Insufficient data to compute._")
        lines.append("")

        # ---- Per-grade detail sections ----
        _sec = {'A': '3', 'B': '4', 'C': '5'}
        for grade_letter, title in [('A', 'Grade A (MA10 pullback)'), ('B', 'Grade B (MA5 pullback)'), ('C', 'Grade C (platform breakout)')]:
            lines.append(f"## {_sec[grade_letter]}. {title} 績效")
            lines.append("")
            if grade_df is not None and not grade_df.empty:
                sub = grade_df[grade_df['buy_point_grade'] == grade_letter]
                if not sub.empty:
                    row = sub.iloc[0]
                    gconf  = row.get('grade_confidence', 'INSUFFICIENT')
                    _nsig2 = row.get('signal_count', _DASH)
                    lines.append(f"- Signals      : {_nsig2}")
                    lines.append(f"- Confidence   : {gconf}")
                    lines.append(f"- Win rate 5d  : {_pct(row.get('win_rate_5d'))}")
                    lines.append(f"- Win rate 10d : {_pct(row.get('win_rate_10d'))}")
                    lines.append(f"- Win rate 20d : {_pct(row.get('win_rate_20d'))}")
                    lines.append(f"- Avg ret 20d  : {_pct(row.get('avg_return_20d'))}")
                    lines.append(f"- Med ret 20d  : {_pct(row.get('median_return_20d'))}")
                    lines.append(f"- Avg drawdown : {_pct(row.get('avg_drawdown'))}")
                    lines.append(f"- Stop-loss hit: {_pct(row.get('stop_loss_hit_rate'))}")
                    lines.append(f"- Take-profit  : {_pct(row.get('take_profit_hit_rate'))}")
                    lines.append(f"- Profit factor: {_val(row.get('profit_factor'))}")
                    lines.append(f"- Best case    : {_pct(row.get('best_case'))}")
                    lines.append(f"- Worst case   : {_pct(row.get('worst_case'))}")
                    if row.get('sample_note'):
                        lines.append(f"- {row['sample_note']}")
                else:
                    lines.append(f"_No grade {grade_letter} signal data._")
            else:
                lines.append("_Insufficient data._")
            lines.append("")

        # ---- 6. Stop-loss / take-profit summary ----
        lines.append("## 6. Stop-Loss / Take-Profit Summary")
        lines.append("")
        trades_df = r.get('trades_df', pd.DataFrame())
        if trades_df is not None and not trades_df.empty:
            sl_col = 'stop_loss_hit' if 'stop_loss_hit' in trades_df.columns else None
            tp_col = 'take_profit_hit' if 'take_profit_hit' in trades_df.columns else None
            if sl_col:
                sl_rate = trades_df[sl_col].mean() * 100 if len(trades_df) > 0 else 0
                lines.append(f"- Overall stop-loss rate (-5%): {sl_rate:.1f}%")
            if tp_col:
                tp_rate = trades_df[tp_col].mean() * 100 if len(trades_df) > 0 else 0
                lines.append(f"- Overall take-profit rate (+10%): {tp_rate:.1f}%")
            if 'holding_days' in trades_df.columns:
                avg_hold = trades_df['holding_days'].dropna().mean()
                lines.append(f"- Avg holding days: {avg_hold:.1f}")
        else:
            lines.append("_Trade detail data insufficient._")
        lines.append("")

        # ---- 7. Best / worst cases ----
        lines.append("## 7. Best / Worst Cases")
        lines.append("")
        if trades_df is not None and not trades_df.empty and 'forward_return_20d' in trades_df.columns:
            valid = trades_df.dropna(subset=['forward_return_20d'])
            if len(valid) >= 3:
                best  = valid.nlargest(3, 'forward_return_20d')
                worst = valid.nsmallest(3, 'forward_return_20d')
                lines.append("**Top 3 (20d return)**")
                for _, row in best.iterrows():
                    _sym = row.get('symbol', _DASH); _dt = row.get('entry_date', _DASH); _g = row.get('buy_point_grade', _DASH)
                    lines.append(f"- {_sym} @ {_dt} [{_g}] -> {_pct(row.get('forward_return_20d'))}")
                lines.append("")
                lines.append("**Bottom 3 (20d return)**")
                for _, row in worst.iterrows():
                    _sym = row.get('symbol', _DASH); _dt = row.get('entry_date', _DASH); _g = row.get('buy_point_grade', _DASH)
                    lines.append(f"- {_sym} @ {_dt} [{_g}] -> {_pct(row.get('forward_return_20d'))}")
            else:
                lines.append("_Insufficient sample to list cases._")
        else:
            lines.append("_Trade detail data insufficient._")
        lines.append("")

        # ---- 8. Conclusion ----
        lines.append("## 8. Conclusion")
        lines.append("")
        self._build_conclusion(lines, r)
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"_Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")
        lines.append("")
        lines.append("> NOTE: This system is for research and simulation only. Not investment advice. Live order execution is disabled in v1.")

        return '\n'.join(lines)

    def _build_conclusion(self, lines: list, r: dict):
        """Append conclusion section based on grade performance."""
        grade_df = r.get('grade_df', pd.DataFrame())
        conf     = r.get('confidence', {})
        overall  = conf.get('overall', 'INSUFFICIENT')

        lines.append(f"Statistical confidence: **{overall}**")
        lines.append("")

        if overall == 'INSUFFICIENT':
            lines.append(
                "> [WARN] Sample size is INSUFFICIENT. "
                "The observations below reflect current sample data only. "
                "Do not use these results as a basis for live trading decisions."
            )
            lines.append("")

        if grade_df is None or grade_df.empty:
            lines.append("- Insufficient data — cannot provide conclusions.")
            return

        for grade in ['A', 'B', 'C']:
            sub = grade_df[grade_df['buy_point_grade'] == grade]
            if sub.empty:
                continue
            row   = sub.iloc[0]
            wr    = row.get('win_rate_20d')
            ret   = row.get('avg_return_20d')
            n     = row.get('signal_count', 0)
            gconf = row.get('grade_confidence', 'INSUFFICIENT')

            if n < 10:
                lines.append(f"- Grade {grade}: [WARN] sample < 10, no conclusion.")
                continue

            try:
                wr_f  = float(wr)  if wr  is not None else None
                ret_f = float(ret) if ret is not None else None
            except (TypeError, ValueError):
                wr_f = ret_f = None

            if wr_f is not None and ret_f is not None:
                obs = (
                    f"win rate {wr_f:.0f}%, avg ret {ret_f:+.1f}% "
                    f"({n} signals, confidence: {gconf})"
                )
                if gconf == 'INSUFFICIENT':
                    lines.append(f"- Grade {grade}: [OBSERVED in current sample] {obs} — INSUFFICIENT sample, do not conclude effectiveness.")
                elif wr_f >= 60 and ret_f >= 5:
                    lines.append(f"- Grade {grade}: [OBSERVED] {obs} — positive pattern in sample.")
                elif wr_f >= 50:
                    lines.append(f"- Grade {grade}: [OBSERVED] {obs} — mixed result, continue observing.")
                else:
                    lines.append(f"- Grade {grade}: [OBSERVED] {obs} — below average, review entry conditions.")
            else:
                lines.append(f"- Grade {grade}: insufficient data to evaluate.")

        lines.append("")
        lines.append(
            "- Recommendation: accumulate more real CSV data (50+ symbols, 120+ K-line days)"
            " then re-run `python main.py backtest-buy-points --mode real`."
        )

    def save(self, output_dir: str = None) -> str:
        """Build report and save to file. Returns output path."""
        if output_dir is None:
            output_dir = _REPORTS_DIR
        os.makedirs(output_dir, exist_ok=True)
        filename = f"buy_point_validation_report_{self._date_str}.md"
        path     = os.path.join(output_dir, filename)
        content  = self.build()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info("BuyPointValidationReport saved → %s", path)
        return path
