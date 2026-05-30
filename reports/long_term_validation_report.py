"""
reports/long_term_validation_report.py - Markdown report for long-term strategy validation (v0.3.11).

Generates a structured Markdown report with 8 sections:
  1. Overview & statistical confidence
  2. EPS factor analysis
  3. Gross margin / operating margin factor analysis
  4. Valuation zone / PE bucket analysis
  5. Long-term score bucket performance
  6. BUY_BREAKOUT signal filter comparison
  7. TIMING_ESTIMATED impact analysis
  8. Per-symbol summary & conclusions

Usage:
    from reports.long_term_validation_report import LongTermValidationReport
    rpt = LongTermValidationReport(results)
    path = rpt.save()
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REPORTS_DIR = os.path.join(_BASE_DIR, 'reports')


class LongTermValidationReport:
    """Generates a Markdown long-term strategy validation report."""

    def __init__(self, results: dict):
        self.results = results

    # ------------------------------------------------------------------
    # Formatting helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _pct(v, decimals=2):
        if v is None:
            return '—'
        try:
            return f'{float(v)*100:+.{decimals}f}%'
        except Exception:
            return str(v)

    @staticmethod
    def _fmt(v, fmt='.4f'):
        if v is None:
            return '—'
        try:
            return format(float(v), fmt)
        except Exception:
            return str(v)

    @staticmethod
    def _n(v):
        if v is None:
            return '—'
        return str(int(v))

    # ------------------------------------------------------------------
    # Section builders
    # ------------------------------------------------------------------

    def _section_overview(self) -> str:
        r = self.results
        conf    = r.get('confidence', {})
        overall = conf.get('overall', 'INSUFFICIENT')
        reasons = conf.get('reasons', [])
        tw_warn = conf.get('timing_warning', '')

        lines = [
            '## 1. Overview',
            '',
            f"- **Mode**          : {r.get('mode', '—')}",
            f"- **Holding days**  : {r.get('holding_days', '—')}",
            f"- **Symbols**       : {r.get('n_symbols', 0)}",
            f"- **Signal rows**   : {r.get('n_signals', 0)}",
            f"- **Valid fwd rows**: {r.get('n_valid_fwd', 0)}",
            f"- **Period**        : {r.get('start', '—')} → {r.get('end', '—')}",
            f"- **Trading days**  : {r.get('trading_days', '—')}",
            f"- **Data source**   : {'REAL CSV SAMPLE' if r.get('is_sample') else 'REAL CSV'}",
            '',
            '### Statistical Confidence',
            '',
            f'**Overall: {overall}**',
            '',
        ]
        if reasons:
            for reason in reasons:
                lines.append(f'- {reason}')
        else:
            lines.append('- 無置信度降級原因')
        if tw_warn:
            lines.append('')
            lines.append(f'> ⚠ {tw_warn}')
        lines.append('')
        lines.append(
            '> [!] For research and simulation only. Not investment advice. '
            '統計樣本量不足時，所有結論僅供參考，不可用於實際交易決策。'
        )
        lines.append('')
        return '\n'.join(lines)

    def _factor_table(self, factor_data: list, title: str) -> str:
        """Render a factor analysis list as a Markdown table."""
        if not factor_data:
            return f'*{title}: 無資料*\n\n'
        lines = [
            f'### {title}',
            '',
            '| Bucket | N | Avg Return | Win Rate | Profit Factor | Confidence |',
            '|--------|---|-----------|---------|--------------|-----------|',
        ]
        for row in factor_data:
            lines.append(
                f"| {row.get('bucket','—')} "
                f"| {self._n(row.get('n'))} "
                f"| {self._pct(row.get('avg_return'))} "
                f"| {self._pct(row.get('win_rate'))} "
                f"| {self._fmt(row.get('profit_factor'), '.2f')} "
                f"| {row.get('confidence','—')} |"
            )
        lines.append('')
        return '\n'.join(lines)

    def _filter_table(self, filter_data: dict, title: str) -> str:
        """Render a filter effect (filtered vs excluded) as a Markdown table."""
        if not filter_data:
            return f'*{title}: 無資料*\n\n'
        lines = [
            f'### {title}',
            '',
            '| Group | N | Avg Return | Win Rate | Profit Factor | Confidence |',
            '|-------|---|-----------|---------|--------------|-----------|',
        ]
        for grp in ('filtered', 'excluded'):
            d = filter_data.get(grp, {})
            lines.append(
                f"| {grp} "
                f"| {self._n(d.get('n'))} "
                f"| {self._pct(d.get('avg_return'))} "
                f"| {self._pct(d.get('win_rate'))} "
                f"| {self._fmt(d.get('profit_factor'), '.2f')} "
                f"| {d.get('confidence','—')} |"
            )
        lines.append('')
        return '\n'.join(lines)

    def _section_eps(self) -> str:
        factors = self.results.get('factors', {})
        lines = ['## 2. EPS Factor Analysis', '']
        lines.append(self._factor_table(factors.get('eps_positive', []), 'EPS Positive vs Negative'))
        lines.append(self._factor_table(factors.get('eps_growth_bucket', []), 'EPS Growth Bucket'))
        return '\n'.join(lines)

    def _section_margins(self) -> str:
        factors = self.results.get('factors', {})
        lines = ['## 3. Margin Factor Analysis', '']
        lines.append(self._factor_table(factors.get('gross_margin_bucket', []), 'Gross Margin Bucket'))
        lines.append(self._factor_table(factors.get('operating_margin_bucket', []), 'Operating Margin Bucket'))
        return '\n'.join(lines)

    def _section_valuation(self) -> str:
        factors = self.results.get('factors', {})
        lines = ['## 4. Valuation Analysis', '']
        lines.append(self._factor_table(factors.get('valuation_zone', []), 'Valuation Zone'))
        lines.append(self._factor_table(factors.get('pe_bucket', []), 'PE Bucket'))
        return '\n'.join(lines)

    def _section_score_bucket(self) -> str:
        factors = self.results.get('factors', {})
        lines = ['## 5. Long-Term Score Bucket Performance', '']
        lines.append(self._factor_table(factors.get('long_term_score_bucket', []), 'Score Bucket'))
        return '\n'.join(lines)

    def _section_signal_filter(self) -> str:
        factors = self.results.get('factors', {})
        lines = ['## 6. BUY_BREAKOUT Signal Filter Effect', '']
        lines.append(self._filter_table(factors.get('signal_filter', {}), 'BUY_BREAKOUT vs Others'))
        return '\n'.join(lines)

    def _section_timing(self) -> str:
        factors = self.results.get('factors', {})
        lines = [
            '## 7. TIMING_ESTIMATED Impact',
            '',
            '比較 `timing_estimated=True`（法定申報期限推算）vs `False`（已知公告日）的前向報酬差異。',
            '',
        ]
        lines.append(self._factor_table(factors.get('timing_estimated', []), 'Timing Estimated vs MOPS'))
        return '\n'.join(lines)

    def _section_per_symbol(self) -> str:
        per_sym = self.results.get('per_symbol_summary', {})
        lines = ['## 8. Per-Symbol Summary', '']
        if not per_sym:
            lines.append('*無 per-symbol 資料*')
            lines.append('')
            return '\n'.join(lines)
        lines += [
            '| Symbol | Bars | Eval Rows | Buy Signals | Has EPS | Has GM | Timing Est |',
            '|--------|------|----------|------------|---------|--------|-----------|',
        ]
        for sym, s in sorted(per_sym.items()):
            lines.append(
                f"| {sym} "
                f"| {s.get('daily_bars','—')} "
                f"| {s.get('n_rows','—')} "
                f"| {s.get('n_buy_signals','—')} "
                f"| {'Y' if s.get('has_eps') else 'N'} "
                f"| {'Y' if s.get('has_gm') else 'N'} "
                f"| {'Y' if s.get('timing_est') else 'N'} |"
            )
        lines.append('')
        return '\n'.join(lines)

    def _section_conclusions(self) -> str:
        r       = self.results
        conf    = r.get('confidence', {})
        overall = conf.get('overall', 'INSUFFICIENT')
        factors = r.get('factors', {})
        holding = r.get('holding_days', 60)

        lines = [
            '## 9. Conclusions',
            '',
            f'統計置信度: **{overall}**',
            '',
        ]

        if overall == 'INSUFFICIENT':
            lines += [
                '- 樣本量不足，無法得出可靠策略結論。',
                '- 本報告僅確認回測框架功能正常，數字不可用於策略調整。',
                f'- 建議：擴大 universe 至 ≥30 個股、增加至少 {holding*3} 個交易日歷史資料後重跑。',
                '',
            ]
        elif overall == 'OBSERVATIONAL':
            lines += [
                '- 樣本量達到可觀測等級，可識別初步模式，但不足以可靠調整策略。',
                '- 建議擴大 universe 或增加資料後再下結論。',
                '',
            ]
        else:
            lines += [
                '- 樣本量達到可參考等級。以下為初步觀察（非投資建議）：',
                '',
            ]

        # EPS insight
        eps_data = factors.get('eps_positive', [])
        eps_true  = next((r for r in eps_data if r.get('bucket') == 'True'),  None)
        eps_false = next((r for r in eps_data if r.get('bucket') == 'False'), None)
        if eps_true and eps_false and eps_true.get('avg_return') and eps_false.get('avg_return'):
            diff = float(eps_true['avg_return']) - float(eps_false['avg_return'])
            lines.append(
                f'- EPS 為正組 ({holding}d avg={self._pct(eps_true["avg_return"])}) '
                f'vs 虧損組 ({self._pct(eps_false["avg_return"])}), '
                f'差異: {diff*100:+.2f}pct'
            )

        # Signal filter insight
        sf = factors.get('signal_filter', {})
        flt  = sf.get('filtered', {})
        excl = sf.get('excluded', {})
        if flt.get('avg_return') is not None and excl.get('avg_return') is not None:
            diff = float(flt['avg_return']) - float(excl['avg_return'])
            lines.append(
                f'- BUY_BREAKOUT 信號 ({holding}d avg={self._pct(flt["avg_return"])}) '
                f'vs 非 BUY_BREAKOUT ({self._pct(excl["avg_return"])}), '
                f'差異: {diff*100:+.2f}pct'
            )

        lines += [
            '',
            '---',
            '',
            '> **[!] 本報告僅供研究與模擬，不構成投資建議。**',
            '> Generated by TW Quant Cockpit v0.3.11',
            '',
        ]
        return '\n'.join(lines)

    # ------------------------------------------------------------------
    # Build full report
    # ------------------------------------------------------------------

    def build(self) -> str:
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        header = (
            f'# TW Quant Cockpit — Long-Term Strategy Validation Report\n\n'
            f'Generated: {ts}  \n'
            f'Version: v0.3.11\n\n'
            '---\n\n'
        )
        sections = [
            self._section_overview(),
            self._section_eps(),
            self._section_margins(),
            self._section_valuation(),
            self._section_score_bucket(),
            self._section_signal_filter(),
            self._section_timing(),
            self._section_per_symbol(),
            self._section_conclusions(),
        ]
        return header + '\n'.join(sections)

    def save(self, output_dir: Optional[str] = None) -> str:
        """Save report to Markdown file and return the path."""
        out_dir = output_dir or _REPORTS_DIR
        os.makedirs(out_dir, exist_ok=True)
        ts   = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = os.path.join(out_dir, f'long_term_validation_report_{ts}.md')
        content = self.build()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info("LongTermValidationReport: saved to %s", path)
        return path
