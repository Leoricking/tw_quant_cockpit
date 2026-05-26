"""
reports/score_validation_report.py - Markdown score validation report generator.

Reads from ScoreValidator results dicts (or saved CSVs) and produces a
structured Markdown report covering:
  - Score bucket performance
  - Factor effectiveness
  - No-entry condition analysis
  - Trust cost validation
  - Margin risk validation
  - Conclusions and recommendations

Usage:
    from reports.score_validation_report import ScoreValidationReport
    rpt = ScoreValidationReport(results)
    path = rpt.save()          # writes to reports/ directory
    print(rpt.build())         # returns Markdown string
"""

import os
import logging
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)
_DASH = '\u2014'   # em dash — safe to use inside f-string variables

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REPORTS_DIR = os.path.join(_BASE_DIR, 'reports')


def _pct(v, decimals=2):
    """Format a percentage value, or return '—' if None/NaN."""
    if v is None:
        return '—'
    try:
        f = float(v)
        if pd.isna(f):
            return '—'
        return f"{f:+.{decimals}f}%"
    except (TypeError, ValueError):
        return '—'


def _val(v, decimals=3):
    """Format a numeric value, or return '—' if None/NaN."""
    if v is None:
        return '—'
    try:
        f = float(v)
        if pd.isna(f):
            return '—'
        return f"{f:.{decimals}f}"
    except (TypeError, ValueError):
        return '—'


class ScoreValidationReport:
    """Generates a Markdown report from ScoreValidator results."""

    def __init__(self, results: dict):
        """
        Parameters
        ----------
        results : dict
            Output of ScoreValidator.run().
        """
        self.results = results or {}
        self._date_str = datetime.now().strftime('%Y-%m-%d')

    def build(self) -> str:
        """Assemble and return the full Markdown report as a string."""
        r = self.results
        lines = []

        # ---- Header ----
        lines.append("# TW Quant Cockpit Score Validation Report")
        lines.append("")
        lines.append("> NOTE: This report is for research reference only and does not constitute investment advice.")
        lines.append("> Live order execution is disabled in v1.")
        lines.append("")

        # ---- 1. 驗證期間 ----
        lines.append("## 1. Validation Period")
        lines.append("")
        _start = r.get('start', _DASH)
        _end   = r.get('end',   _DASH)
        _dsrc  = r.get('data_source', _DASH)
        lines.append(f"- Start date   : {_start}")
        lines.append(f"- End date     : {_end}")
        lines.append(f"- Symbols      : {r.get('n_symbols', 0)}")
        lines.append(f"- Records      : {r.get('n_records', 0)}")
        src_tag = 'REAL CSV SAMPLE' if r.get('is_sample') else 'REAL CSV'
        lines.append(f"- Data source  : {src_tag}")
        lines.append(f"- Data path    : `{_dsrc}`")

        conf = r.get('confidence', {})
        overall = conf.get('overall', 'INSUFFICIENT')
        lines.append(f"- Statistical confidence: {overall}")
        reasons = conf.get('reasons', [])
        for reason in reasons:
            lines.append(f"  - {reason}")
        if r.get('n_symbols', 0) < 5:
            lines.append("")
            lines.append("> [WARN] Fewer than 5 symbols — statistical reliability is very low, observational only.")
        lines.append("")

        # ---- 2. Score Bucket Performance ----
        lines.append("## 2. Score Bucket Performance")
        lines.append("")
        bucket_df = r.get('score_bucket_df', pd.DataFrame())
        if bucket_df is not None and not bucket_df.empty:
            lines.append("| Score range | Samples | Avg 5d% | Avg 10d% | Avg 20d% | Win rate 20d% | Max DD 20d% | Stop-loss% | Profit factor | Confidence | Note |")
            lines.append("|-------------|---------|---------|----------|----------|--------------|-------------|------------|--------------|------------|------|")
            for _, row in bucket_df.iterrows():
                note   = row.get('sample_note', '')
                bconf  = row.get('bucket_confidence', 'INSUFFICIENT')
                _bkt   = row.get('score_bucket', _DASH)
                _bcnt  = row.get('sample_count', _DASH)
                lines.append(
                    f"| {_bkt} "
                    f"| {_bcnt} "
                    f"| {_pct(row.get('avg_return_5d'))} "
                    f"| {_pct(row.get('avg_return_10d'))} "
                    f"| {_pct(row.get('avg_return_20d'))} "
                    f"| {_pct(row.get('win_rate_20d'))} "
                    f"| {_pct(row.get('avg_max_drawdown_20d'))} "
                    f"| {_pct(row.get('stop_loss_5pct_rate'))} "
                    f"| {_val(row.get('profit_factor_20d'), 2)} "
                    f"| {bconf} "
                    f"| {note} |"
                )
        else:
            lines.append("_Insufficient data to compute._")
        lines.append("")

        # ---- 3. Factor Effectiveness ----
        lines.append("## 3. Factor Effectiveness")
        lines.append("")
        factor_df = r.get('factor_df', pd.DataFrame())
        if factor_df is not None and not factor_df.empty:
            lines.append("| Factor | Corr 5d | Corr 10d | Corr 20d | Top quantile 20d% | Bottom quantile 20d% | Effectiveness |")
            lines.append("|--------|---------|----------|----------|-----------------|---------------------|--------------|")
            for _, row in factor_df.iterrows():
                lines.append(
                    f"| {row.get('factor','—')} "
                    f"| {_val(row.get('correlation_with_5d_return'))} "
                    f"| {_val(row.get('correlation_with_10d_return'))} "
                    f"| {_val(row.get('correlation_with_20d_return'))} "
                    f"| {_pct(row.get('top_quantile_avg_return_20d'))} "
                    f"| {_pct(row.get('bottom_quantile_avg_return_20d'))} "
                    f"| {row.get('effectiveness_label','—')} |"
                )
        else:
            lines.append("_Insufficient data to compute._")
        lines.append("")

        # ---- 4. No-Entry Condition Effectiveness ----
        lines.append("## 4. No-Entry Condition Effectiveness")
        lines.append("")
        no_entry_df = r.get('no_entry_df', pd.DataFrame())
        if no_entry_df is not None and not no_entry_df.empty:
            lines.append("| Condition | Samples | Avg 5d% | Avg 20d% | Win rate 20d% | Max DD% | Risk reduction% | Recommendation |")
            lines.append("|-----------|---------|---------|----------|--------------|---------|----------------|---------------|")
            for _, row in no_entry_df.iterrows():
                lines.append(
                    f"| {row.get('condition','—')} "
                    f"| {row.get('sample_count','—')} "
                    f"| {_pct(row.get('avg_return_5d'))} "
                    f"| {_pct(row.get('avg_return_20d'))} "
                    f"| {_pct(row.get('win_rate_20d'))} "
                    f"| {_pct(row.get('avg_drawdown_20d'))} "
                    f"| {_pct(row.get('risk_reduction_effect'))} "
                    f"| {row.get('recommendation','—')} |"
                )
        else:
            lines.append("_Insufficient data to compute._")
        lines.append("")

        # ---- 5. Trust Cost Validation ----
        lines.append("## 5. Trust Cost Validation")
        lines.append("")
        trust_df = r.get('trust_cost_df', pd.DataFrame())
        if trust_df is not None and not trust_df.empty:
            lines.append("| Condition | Samples | Avg 5d% | Avg 10d% | Avg 20d% | Win rate 20d% | Max DD% |")
            lines.append("|-----------|---------|---------|----------|----------|--------------|---------|")
            for _, row in trust_df.iterrows():
                lines.append(
                    f"| {row.get('condition','—')} "
                    f"| {row.get('sample_count','—')} "
                    f"| {_pct(row.get('avg_return_5d'))} "
                    f"| {_pct(row.get('avg_return_10d'))} "
                    f"| {_pct(row.get('avg_return_20d'))} "
                    f"| {_pct(row.get('win_rate_20d'))} "
                    f"| {_pct(row.get('avg_drawdown_20d'))} |"
                )
        else:
            lines.append("_Trust cost data insufficient._")
        lines.append("")

        # ---- 6. Margin Risk Validation ----
        lines.append("## 6. Margin Risk Validation")
        lines.append("")
        margin_df = r.get('margin_df', pd.DataFrame())
        if margin_df is not None and not margin_df.empty:
            lines.append("| Condition | Samples | Avg 5d% | Avg 10d% | Avg 20d% | Win rate 20d% | Max DD% |")
            lines.append("|-----------|---------|---------|----------|----------|--------------|---------|")
            for _, row in margin_df.iterrows():
                lines.append(
                    f"| {row.get('condition','—')} "
                    f"| {row.get('sample_count','—')} "
                    f"| {_pct(row.get('avg_return_5d'))} "
                    f"| {_pct(row.get('avg_return_10d'))} "
                    f"| {_pct(row.get('avg_return_20d'))} "
                    f"| {_pct(row.get('win_rate_20d'))} "
                    f"| {_pct(row.get('avg_drawdown_20d'))} |"
                )
        else:
            lines.append("_Margin data insufficient._")
        lines.append("")

        # ---- 7. Conclusion ----
        lines.append("## 7. Conclusion")
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
        """Append conclusion section based on validation results."""
        bucket_df = r.get('score_bucket_df', pd.DataFrame())
        factor_df = r.get('factor_df', pd.DataFrame())
        n_sym     = r.get('n_symbols', 0)
        conf      = r.get('confidence', {})
        overall   = conf.get('overall', 'INSUFFICIENT')

        lines.append(f"Statistical confidence: **{overall}**")
        lines.append("")

        if overall == 'INSUFFICIENT':
            lines.append(
                "> [WARN] Sample size is insufficient for strategy conclusions. "
                "Observations below reflect current sample data only."
            )
            lines.append("")

        if n_sym < 5:
            lines.append("> [WARN] Fewer than 5 symbols — results are for functional verification only.")
            lines.append("")

        if bucket_df is not None and not bucket_df.empty:
            high = bucket_df[bucket_df['score_bucket'] == '80-100']
            low  = bucket_df[bucket_df['score_bucket'] == '<50']
            h_ret = high['avg_return_20d'].values[0] if len(high) > 0 else None
            l_ret = low['avg_return_20d'].values[0]  if len(low)  > 0 else None
            if h_ret is not None and l_ret is not None and not pd.isna(h_ret) and not pd.isna(l_ret):
                try:
                    if float(h_ret) > float(l_ret) + 2.0:
                        lines.append(
                            f"- [OBSERVED] 80-100 bucket 20d avg return ({h_ret:+.2f}%) "
                            f"is higher than <50 bucket ({l_ret:+.2f}%) in the current sample."
                        )
                        if overall == 'INSUFFICIENT':
                            lines.append(
                                "  Sample is INSUFFICIENT — do not conclude that high score is effective."
                            )
                    elif float(h_ret) < float(l_ret) - 2.0:
                        lines.append(
                            f"- [OBSERVED] Low-score bucket outperformed high-score bucket "
                            f"({l_ret:+.2f}% vs {h_ret:+.2f}%). Review scoring logic."
                        )
                    else:
                        lines.append(
                            "- [OBSERVED] Score buckets show similar 20d returns. "
                            "More data needed to draw conclusions."
                        )
                except (TypeError, ValueError):
                    pass
        else:
            lines.append("- Score bucket data insufficient — cannot provide conclusions.")

        if factor_df is not None and not factor_df.empty:
            strong     = factor_df[factor_df['effectiveness_label'] == 'strong_positive']['factor'].tolist()
            negative   = factor_df[factor_df['effectiveness_label'] == 'negative']['factor'].tolist()
            insuf_list = factor_df[factor_df['effectiveness_label'] == 'insufficient_sample']['factor'].tolist()
            if strong:
                lines.append(f"- [OBSERVED] Positive correlation in current sample: {', '.join(strong)}")
            if negative:
                lines.append(f"- [WARN] Negative correlation in current sample: {', '.join(negative)}")
            if insuf_list:
                lines.append(f"- [WARN] Insufficient sample for factors: {', '.join(insuf_list)}")

        lines.append("")
        lines.append(
            "- Recommendation: import more real CSV data (at least 120 days K-line, 50+ symbols)"
            " then re-run `python main.py validate-score --mode real`."
        )

    def save(self, output_dir: str = None) -> str:
        """Build report and save to file. Returns output path."""
        if output_dir is None:
            output_dir = _REPORTS_DIR
        os.makedirs(output_dir, exist_ok=True)
        filename = f"score_validation_report_{self._date_str}.md"
        path     = os.path.join(output_dir, filename)
        content  = self.build()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info("ScoreValidationReport saved → %s", path)
        return path
