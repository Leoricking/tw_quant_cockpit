"""
reports/universe_quality_report.py - Universe quality Markdown report generator.

Generates reports/universe_quality_report_YYYY-MM-DD.md.

Usage:
    from reports.universe_quality_report import UniverseQualityReport
    rpt = UniverseQualityReport(df, summary)
    path = rpt.save()
"""

import logging
import os
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REPORTS_DIR = os.path.join(_BASE_DIR, 'reports')
_DASH        = '\u2014'


def _yn(v) -> str:
    if v is True or str(v).lower() in ('true', '1', 'yes'):
        return 'Y'
    return '\u2014'


class UniverseQualityReport:
    """Generates a Markdown quality report from UniverseQualityChecker results."""

    def __init__(self, df: pd.DataFrame, summary: dict):
        self.df        = df if df is not None else pd.DataFrame()
        self.summary   = summary or {}
        self._date_str = datetime.now().strftime('%Y-%m-%d')

    def build(self) -> str:
        lines = []
        s     = self.summary

        # Title
        lines.append('# Universe Quality Report')
        lines.append('')
        lines.append(f'> **Generated:** {self._date_str}')
        lines.append('')
        lines.append('> This report is for research reference only and does not '
                     'constitute investment advice.')
        lines.append('')

        # Section 1: Overview
        lines.append('## 一、總覽')
        lines.append('')
        conf     = s.get('confidence', {})
        bt_count = s.get('strategy_bt_ready_count', 0)
        lines.append('| Item | Value |')
        lines.append('|------|-------|')
        lines.append(f'| Universe size | {s.get("universe_size", 0)} |')
        lines.append(f'| Imported symbols (daily > 0) | {s.get("imported_count", 0)} |')
        lines.append(f'| Short-term ready | {s.get("short_ready_count", 0)} |')
        lines.append(f'| Mid-term ready | {s.get("mid_ready_count", 0)} |')
        lines.append(f'| Long-term ready | {s.get("long_ready_count", 0)} |')
        lines.append(f'| Strategy backtest eligible | {bt_count} |')
        lines.append(f'| Statistical confidence expectation | **{conf.get("overall", "INSUFFICIENT")}** |')
        lines.append('')

        for reason in conf.get('reasons', []):
            lines.append(f'- {reason}')
        if conf.get('reasons'):
            lines.append('')

        # Section 2: Per-symbol table
        lines.append('## 二、股票資料完整度表')
        lines.append('')
        if not self.df.empty:
            cols_show = ['symbol', 'name', 'daily_rows', 'institutional_rows',
                         'margin_rows', 'holder_rows', 'trust_cost_rows',
                         'monthly_revenue_rows', 'short_term_ready',
                         'mid_term_ready', 'long_term_ready', 'warning']
            header = ['Symbol', 'Name', 'Daily', 'Inst', 'Margin',
                      'Holder', 'TC', 'Rev', 'Short✓', 'Mid✓', 'Long✓', 'Warning']
            lines.append('| ' + ' | '.join(header) + ' |')
            lines.append('|' + '|'.join(['---'] * len(header)) + '|')
            for _, row in self.df.iterrows():
                cells = []
                for col in cols_show:
                    v = row.get(col, '')
                    if col in ('short_term_ready', 'mid_term_ready', 'long_term_ready'):
                        cells.append(_yn(v))
                    elif v is None or (isinstance(v, float) and pd.isna(v)):
                        cells.append(_DASH)
                    else:
                        cells.append(str(v))
                lines.append('| ' + ' | '.join(cells) + ' |')
        else:
            lines.append('_No data._')
        lines.append('')

        # Section 3: Missing data lists
        lines.append('## 三、缺資料清單')
        lines.append('')
        missing_map = [
            ('缺 daily K 線',       'missing_daily'),
            ('缺 institutional',    'missing_institutional'),
            ('缺 margin',           'missing_margin'),
            ('缺 monthly_revenue',  'missing_monthly_revenue'),
            ('缺 holder',           'missing_holder'),
        ]
        any_missing = False
        for label, key in missing_map:
            items = s.get(key, [])
            if items:
                any_missing = True
                lines.append(f'**{label}:** {", ".join(items)}')
                lines.append('')
        if not any_missing:
            lines.append('_All symbols have basic data coverage._')
            lines.append('')

        # Section 4: Next steps
        lines.append('## 四、下一步建議')
        lines.append('')
        next_steps = s.get('next_steps', [])
        if next_steps:
            for step in next_steps:
                lines.append(f'- {step}')
        else:
            lines.append('- Run `python main.py run-validation-suite --mode real`')
        lines.append('')
        lines.append('**Import workflow:**')
        lines.append('```bash')
        lines.append('# 1. Build manifest')
        lines.append('python main.py build-universe-manifest --size 10')
        lines.append('# 2. Dry-run import check')
        lines.append('python main.py batch-import-xq --folder D:\\XQ\\twqc_bundle\\raw --universe 10 --dry-run')
        lines.append('# 3. Import')
        lines.append('python main.py batch-import-xq --folder D:\\XQ\\twqc_bundle\\raw --universe 10')
        lines.append('# 4. Check quality again')
        lines.append('python main.py universe-quality --report')
        lines.append('# 5. Run validation')
        lines.append('python main.py run-validation-suite --mode real --min-symbols 10')
        lines.append('```')
        lines.append('')
        lines.append('> Statistical confidence: < 10 symbols = INSUFFICIENT | '
                     '10–29 = OBSERVATIONAL | ≥ 30 = RELIABLE (requires ≥120 trading days)')
        lines.append('')
        lines.append('> Not investment advice. No live API connected.')
        lines.append('')

        return '\n'.join(lines)

    def save(self, output_dir: str = None) -> str:
        out_dir  = output_dir or _REPORTS_DIR
        os.makedirs(out_dir, exist_ok=True)
        filename = f'universe_quality_report_{self._date_str}.md'
        path     = os.path.join(out_dir, filename)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.build())
            logger.info("Universe quality report saved: %s", path)
        except Exception as exc:
            logger.warning("Could not save universe quality report: %s", exc)
        return path
