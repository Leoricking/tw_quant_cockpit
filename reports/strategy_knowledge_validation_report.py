"""
reports/strategy_knowledge_validation_report.py - Strategy Knowledge backtest report.

Generates a Markdown report summarising the StrategyKnowledgeBacktester results.

Output file: reports/strategy_knowledge_validation_report_YYYY-MM-DD.md

Usage:
    from reports.strategy_knowledge_validation_report import StrategyKnowledgeValidationReport
    rpt = StrategyKnowledgeValidationReport(results)
    path = rpt.save()
    print(rpt.build())
"""

import logging
import os
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REPORTS_DIR = os.path.join(_BASE_DIR, 'reports')
_DASH        = '\u2014'


def _pct(v, decimals=2):
    if v is None: return _DASH
    try:
        f = float(v)
        if pd.isna(f): return _DASH
        return f'{f:+.{decimals}f}%'
    except (TypeError, ValueError):
        return _DASH


def _val(v, decimals=3):
    if v is None: return _DASH
    try:
        f = float(v)
        if pd.isna(f): return _DASH
        return f'{f:.{decimals}f}'
    except (TypeError, ValueError):
        return str(v)


def _conf_badge(level):
    """Return a short badge string for a confidence level."""
    lvl = str(level).upper()
    if lvl == 'RELIABLE':       return '✔ RELIABLE'
    if lvl == 'OBSERVATIONAL':  return '◎ OBSERVATIONAL'
    return '⚠ INSUFFICIENT'


class StrategyKnowledgeValidationReport:
    """Generates a Markdown Strategy Knowledge backtest validation report."""

    def __init__(self, results: dict):
        self.results   = results or {}
        self._date_str = datetime.now().strftime('%Y-%m-%d')

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self) -> str:
        r    = self.results
        mode = r.get('mode', 'real')
        lines = []

        # ---- Title ----
        lines.append('# Strategy Knowledge Backtest Report')
        lines.append('')
        lines.append(f'> **Generated:** {self._date_str}')
        if r.get('is_mock_demo'):
            lines.append('> **⚠ MOCK DEMO ONLY — Results are synthetic. '
                         'Do NOT use for strategy conclusions.**')
        lines.append('')
        lines.append('> This report is for research reference only and does not '
                     'constitute investment advice.')
        lines.append('')

        # ---- Section 1: Overview ----
        lines.append('## 一、總覽')
        lines.append('')
        conf     = r.get('confidence', {})
        uni_conf = r.get('universe_confidence', {})
        lines.append(f'| Item | Value |')
        lines.append(f'|------|-------|')
        src = 'MOCK SYNTHETIC' if r.get('is_mock_demo') else (
            'REAL CSV SAMPLE' if r.get('is_sample') else 'REAL CSV')
        lines.append(f'| Data source | {src} |')
        lines.append(f'| Mode | {mode} |')
        syms = r.get("processed_symbols", [])
        lines.append(f'| Symbols | {", ".join(syms) if syms else r.get("n_symbols", 0)} |')
        lines.append(f'| Records | {r.get("n_records", 0)} |')
        lines.append(f'| Signals detected | {r.get("n_signals", 0)} |')
        lines.append(f'| Period | {r.get("start", _DASH)} → {r.get("end", _DASH)} |')
        lines.append(f'| Trading days | {r.get("trading_days", _DASH)} |')
        lines.append(f'| Holding days | {r.get("holding_days", 20)} |')
        lines.append(f'| Statistical confidence | **{conf.get("overall", "INSUFFICIENT")}** |')
        lines.append(f'| Universe stage | {uni_conf.get("stage", "FUNCTIONAL_TEST")} |')
        lines.append('')

        # Confidence reasons
        reasons = conf.get('reasons', [])
        if reasons:
            lines.append('**Confidence notes:**')
            for reason in reasons:
                lines.append(f'- {reason}')
            lines.append('')

        # Overall conclusion
        overall = conf.get('overall', 'INSUFFICIENT')
        if r.get('is_mock_demo'):
            conclusion = 'MOCK DEMO ONLY — synthetic data, no strategy conclusions possible.'
        elif overall == 'INSUFFICIENT':
            conclusion = ('INSUFFICIENT sample — code execution verified, '
                          'but sample is too small to validate strategy effectiveness. '
                          'Import more real data to reach OBSERVATIONAL or RELIABLE level.')
        elif overall == 'OBSERVATIONAL':
            conclusion = ('OBSERVATIONAL — initial patterns visible. '
                          'Expand universe to ≥30 symbols and ≥200 signals for RELIABLE status.')
        else:
            conclusion = ('RELIABLE — sample is adequate for strategy-adjustment reference. '
                          'Still not investment advice.')
        lines.append(f'**Overall conclusion:** {conclusion}')
        lines.append('')

        # ---- Section 2: KD Advanced ----
        lines.append('## 二、KD Advanced 驗證')
        lines.append('')
        lines += self._module_section(
            r.get('module_performance'),
            module_name='KD Advanced',
            intro=(
                'Validates whether KD low golden cross (<25) and '
                'KD high death cross (>75) are more meaningful than '
                'mid-range (25–75) crossovers.'
            ),
            signal_rows=[
                'kd_low_golden_cross (buy)',
                'kd_high_death_cross (sell/no-chase)',
                'kd_mid_noise_cross (noise)',
                'kd_high_sticky_trend (hold)',
            ],
        )

        # ---- Section 3: Short Interest ----
        lines.append('## 三、Short Interest / 軋空驗證')
        lines.append('')
        lines += self._module_section(
            r.get('module_performance'),
            module_name='Short Interest',
            intro=(
                'Validates price/volume-based squeeze proxies. '
                'Note: full short balance data (margin_df) not yet available — '
                'results use price/volume proxy signals only.'
            ),
            signal_rows=[
                'price_up_short_balance_up (proxy)',
                'limit_up_short_balance_up (proxy)',
                'weak_stock_short_increase (risk)',
                'squeeze_fuel low  [0, 0.3)',
                'squeeze_fuel mid  [0.3, 0.6)',
                'squeeze_fuel high [0.6, 1.0+)',
            ],
        )

        # ---- Section 4: Bottom Reversal ----
        lines.append('## 四、Bottom Reversal / 破底翻驗證')
        lines.append('')
        lines += self._module_section(
            r.get('module_performance'),
            module_name='Bottom Reversal',
            intro=(
                'Validates breakdown-reversal detection. '
                'Signal date is confirmation day (one day after reversal candle). '
                'Bottom reversal is NOT an A/B/C strong-stock buy point.'
            ),
            signal_rows=[
                'bottom_reversal_detected',
                'is_speculative_rebound',
            ],
        )
        # Rebound detail table
        rb = r.get('rebound_validation')
        if rb is not None and not rb.empty:
            lines.append('**Rebound detail:**')
            lines.append('')
            lines += self._df_to_md_table(rb)
            lines.append('')

        # ---- Section 5: Sector Rotation ----
        lines.append('## 五、Sector Rotation / 族群聯動驗證')
        lines.append('')
        sr = r.get('sector_validation')
        if sr is None or (isinstance(sr, pd.DataFrame) and sr.empty):
            lines.append('> **UNAVAILABLE** — Sector rotation validation requires peer stock data '
                         '(leader_df, sector_peers). This will be activated in v0.3.8+ when '
                         'the universe expands to 30+ stocks.')
        else:
            lines += self._df_to_md_table(sr)
        lines.append('')

        # ---- Section 6: Fundamental Quality ----
        lines.append('## 六、Fundamental Quality / 財報防呆驗證')
        lines.append('')
        fq = r.get('fundamental_guard_validation')
        if fq is None or (isinstance(fq, pd.DataFrame) and fq.empty):
            lines.append('> **UNAVAILABLE** — Fundamental quality validation requires '
                         'quarterly EPS / margin / revenue time-series data aligned to '
                         'announcement dates. Available when fundamental data is imported.')
            lines.append('>')
            lines.append('> [WARN] fundamental timing may be approximate until '
                         'announcement_date field is populated.')
        else:
            lines += self._df_to_md_table(fq)
        lines.append('')

        # ---- Section 7: No Chase / No Panic Sell ----
        lines.append('## 七、No Chase / No Panic Sell / Do Not Rebuy Yet 驗證')
        lines.append('')
        nc = r.get('no_chase_validation')
        if nc is not None and not nc.empty:
            lines.append('Compares forward returns when no-chase warning signals are present '
                         'vs absent. If "with_warning" performance is worse, the filter adds value.')
            lines.append('')
            lines += self._df_to_md_table(nc)
        else:
            lines.append('_No no-chase validation data available._')
        lines.append('')

        # ---- Section 8: Phase 2 filter impact on buy points ----
        lines.append('## 八、Phase 2 對 A/B/C 買點品質的影響')
        lines.append('')
        fc = r.get('filter_comparison')
        if fc is not None and not fc.empty:
            lines.append('Compares forward returns across different Phase 2 filter scenarios:')
            lines.append('')
            lines += self._df_to_md_table(fc)
        else:
            lines.append('_No filter comparison data available._')
        lines.append('')

        # ---- Section 9: Module summary ----
        lines.append('## 九、結論')
        lines.append('')
        ms = r.get('module_summary', {})
        if ms:
            lines.append('| Module | Summary |')
            lines.append('|--------|---------|')
            for module, summary in ms.items():
                lines.append(f'| {module} | {summary} |')
            lines.append('')

        # Categorised conclusions
        lines.append('### 有效規則 (Effective — RELIABLE)')
        lines.append('')
        lines.append('_Requires RELIABLE confidence (≥30 symbols, ≥200 signals, ≥120 trading days)._')
        lines.append(_self_classify(r, 'RELIABLE'))
        lines.append('')

        lines.append('### 觀察規則 (Observational)')
        lines.append('')
        lines.append('_Initial pattern detected but insufficient sample for conclusions._')
        lines.append(_self_classify(r, 'OBSERVATIONAL'))
        lines.append('')

        lines.append('### 樣本不足規則 (INSUFFICIENT)')
        lines.append('')
        lines.append('_Too few signals to evaluate. Expand universe to activate._')
        lines.append(_self_classify(r, 'INSUFFICIENT'))
        lines.append('')

        lines.append('### 注意事項')
        lines.append('')
        lines.append('- This report is for research and simulation only.')
        lines.append('- Not investment advice.')
        lines.append('- No live trading API connected.')
        lines.append('- 本系統不接 Shioaji、不接兆豐 API、不自動下單。')
        if r.get('is_mock_demo'):
            lines.append('- **MOCK DEMO ONLY** — All results above are synthetic. '
                         'Do not draw any strategy conclusions from mock data.')
        lines.append('')

        return '\n'.join(lines)

    # ------------------------------------------------------------------
    # Section helpers
    # ------------------------------------------------------------------

    def _module_section(
        self,
        perf_df,
        module_name: str,
        intro: str,
        signal_rows: list,
    ) -> list:
        lines = [intro, '']
        if perf_df is None or perf_df.empty:
            lines.append('_No data._')
            lines.append('')
            return lines

        sub = perf_df[perf_df['module'] == module_name]
        if sub.empty:
            lines.append('_No data._')
            lines.append('')
            return lines

        # Filter to requested signal rows (order preserved)
        ordered = []
        for sig in signal_rows:
            row = sub[sub['signal'].str.contains(sig.split()[0], regex=False, na=False)]
            if not row.empty:
                ordered.append(row.iloc[0])
        if not ordered:
            ordered = [sub.iloc[i] for i in range(len(sub))]

        lines.append('| Signal | N | Win% | Avg Ret | PF | Max DD | Confidence |')
        lines.append('|--------|---|------|---------|-----|--------|------------|')
        for row in ordered:
            n    = row.get('sample_count', 0)
            wr   = _pct(row.get('win_rate'))
            avg  = _pct(row.get('avg_return'))
            pf   = _val(row.get('profit_factor'), decimals=2)
            dd   = _pct(row.get('avg_max_drawdown'))
            conf = _conf_badge(row.get('confidence', 'INSUFFICIENT'))
            sig  = row.get('signal', '')
            lines.append(f'| {sig} | {n} | {wr} | {avg} | {pf} | {dd} | {conf} |')
        lines.append('')
        return lines

    def _df_to_md_table(self, df: pd.DataFrame) -> list:
        """Convert a DataFrame to Markdown table lines."""
        if df is None or df.empty:
            return ['_No data._', '']
        cols = list(df.columns)
        lines = ['| ' + ' | '.join(str(c) for c in cols) + ' |']
        lines.append('|' + '|'.join(['---'] * len(cols)) + '|')
        for _, row in df.iterrows():
            cells = []
            for c in cols:
                v = row[c]
                if v is None or (isinstance(v, float) and pd.isna(v)):
                    cells.append(_DASH)
                else:
                    cells.append(str(v))
            lines.append('| ' + ' | '.join(cells) + ' |')
        return lines

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(self, output_dir: str = None) -> str:
        """Write the report to a Markdown file. Returns the file path."""
        out_dir = output_dir or _REPORTS_DIR
        os.makedirs(out_dir, exist_ok=True)
        filename = f'strategy_knowledge_validation_report_{self._date_str}.md'
        path     = os.path.join(out_dir, filename)
        content  = self.build()
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info("Strategy knowledge report saved: %s", path)
        except Exception as exc:
            logger.warning("Could not save report: %s", exc)
        return path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _self_classify(results: dict, target_conf: str) -> str:
    """Return bullet list of signals at the target confidence level."""
    perf_df = results.get('module_performance')
    if perf_df is None or perf_df.empty:
        return '_No data._'
    sub = perf_df[perf_df['confidence'].str.upper() == target_conf.upper()]
    if sub.empty:
        return '_None at this level._'
    bullets = []
    for _, row in sub.iterrows():
        avg = row.get('avg_return')
        avg_s = f"{avg:+.2f}%" if avg is not None and not pd.isna(float(avg if avg is not None else 0)) else _DASH
        bullets.append(
            f"- [{row.get('module', '')}] {row.get('signal', '')} "
            f"(N={row.get('sample_count', 0)}, avg={avg_s})"
        )
    return '\n'.join(bullets) if bullets else '_None at this level._'
