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
        lines.append("> ⚠️ 本報告僅供研究參考，不構成投資建議。第一版禁止實盤自動下單。")
        lines.append("")

        # ---- 1. 驗證期間 ----
        lines.append("## 1. 驗證期間")
        lines.append("")
        lines.append(f"- 訊號總數：{r.get('n_signals', 0)}")
        src_tag = '🟡 SAMPLE CSV' if r.get('is_sample') else '🟢 REAL CSV'
        lines.append(f"- 資料來源：{src_tag}")
        lines.append(f"- 資料路徑：`{r.get('data_source', '—')}`")
        lines.append(f"- 報告日期：{self._date_str}")
        lines.append("")

        # ---- 2. A/B/C 買點總表 ----
        lines.append("## 2. A/B/C 買點總表")
        lines.append("")
        grade_df = r.get('grade_df', pd.DataFrame())
        if grade_df is not None and not grade_df.empty:
            lines.append("| 等級 | 訊號數 | 勝率5日% | 勝率10日% | 勝率20日% | 平均報酬20日% | 中位報酬20日% | 停損觸發% | 獲利因子 | 備註 |")
            lines.append("|------|--------|----------|-----------|-----------|--------------|--------------|----------|---------|------|")
            for _, row in grade_df.iterrows():
                note = row.get('sample_note', '')
                lines.append(
                    f"| {row.get('buy_point_grade','—')} "
                    f"| {row.get('signal_count','—')} "
                    f"| {_pct(row.get('win_rate_5d'))} "
                    f"| {_pct(row.get('win_rate_10d'))} "
                    f"| {_pct(row.get('win_rate_20d'))} "
                    f"| {_pct(row.get('avg_return_20d'))} "
                    f"| {_pct(row.get('median_return_20d'))} "
                    f"| {_pct(row.get('stop_loss_hit_rate'))} "
                    f"| {_val(row.get('profit_factor'))} "
                    f"| {note} |"
                )
        else:
            lines.append("_資料不足，無法計算。_")
        lines.append("")

        # ---- Per-grade detail sections ----
        _sec = {'A': '3', 'B': '4', 'C': '5'}
        for grade_letter, title in [('A', 'A 級（MA10 回測）'), ('B', 'B 級（MA5 回測）'), ('C', 'C 級（平台突破）')]:
            lines.append(f"## {_sec[grade_letter]}. {title} 績效")
            lines.append("")
            if grade_df is not None and not grade_df.empty:
                sub = grade_df[grade_df['buy_point_grade'] == grade_letter]
                if not sub.empty:
                    row = sub.iloc[0]
                    lines.append(f"- 訊號數：{row.get('signal_count', '—')}")
                    lines.append(f"- 勝率（5日）：{_pct(row.get('win_rate_5d'))}")
                    lines.append(f"- 勝率（10日）：{_pct(row.get('win_rate_10d'))}")
                    lines.append(f"- 勝率（20日）：{_pct(row.get('win_rate_20d'))}")
                    lines.append(f"- 平均報酬（20日）：{_pct(row.get('avg_return_20d'))}")
                    lines.append(f"- 中位報酬（20日）：{_pct(row.get('median_return_20d'))}")
                    lines.append(f"- 平均最大回撤：{_pct(row.get('avg_drawdown'))}")
                    lines.append(f"- 停損觸發率（-5%）：{_pct(row.get('stop_loss_hit_rate'))}")
                    lines.append(f"- 止盈觸發率（+10%）：{_pct(row.get('take_profit_hit_rate'))}")
                    lines.append(f"- 獲利因子：{_val(row.get('profit_factor'))}")
                    lines.append(f"- 最佳案例：{_pct(row.get('best_case'))}")
                    lines.append(f"- 最差案例：{_pct(row.get('worst_case'))}")
                    if row.get('sample_note'):
                        lines.append(f"- ⚠️ {row['sample_note']}")
                else:
                    lines.append(f"_無 {grade_letter} 級訊號資料。_")
            else:
                lines.append("_資料不足。_")
            lines.append("")

        # ---- 6. 停損/停利統計 ----
        lines.append("## 6. 停損 / 停利統計")
        lines.append("")
        trades_df = r.get('trades_df', pd.DataFrame())
        if trades_df is not None and not trades_df.empty:
            sl_col = 'stop_loss_hit' if 'stop_loss_hit' in trades_df.columns else None
            tp_col = 'take_profit_hit' if 'take_profit_hit' in trades_df.columns else None
            if sl_col:
                sl_rate = trades_df[sl_col].mean() * 100 if len(trades_df) > 0 else 0
                lines.append(f"- 總體停損觸發率（-5%）：{sl_rate:.1f}%")
            if tp_col:
                tp_rate = trades_df[tp_col].mean() * 100 if len(trades_df) > 0 else 0
                lines.append(f"- 總體止盈觸發率（+10%）：{tp_rate:.1f}%")
            if 'holding_days' in trades_df.columns:
                avg_hold = trades_df['holding_days'].dropna().mean()
                lines.append(f"- 平均持有天數：{avg_hold:.1f} 日")
        else:
            lines.append("_交易明細資料不足。_")
        lines.append("")

        # ---- 7. 最佳案例 / 最差案例 ----
        lines.append("## 7. 最佳案例 / 最差案例")
        lines.append("")
        if trades_df is not None and not trades_df.empty and 'forward_return_20d' in trades_df.columns:
            valid = trades_df.dropna(subset=['forward_return_20d'])
            if len(valid) >= 3:
                best  = valid.nlargest(3, 'forward_return_20d')
                worst = valid.nsmallest(3, 'forward_return_20d')
                lines.append("**最佳 3 筆（20日）**")
                for _, row in best.iterrows():
                    lines.append(f"- {row.get('symbol','—')} @ {row.get('entry_date','—')} [{row.get('buy_point_grade','—')}] → {_pct(row.get('forward_return_20d'))}")
                lines.append("")
                lines.append("**最差 3 筆（20日）**")
                for _, row in worst.iterrows():
                    lines.append(f"- {row.get('symbol','—')} @ {row.get('entry_date','—')} [{row.get('buy_point_grade','—')}] → {_pct(row.get('forward_return_20d'))}")
            else:
                lines.append("_樣本不足，無法列出案例。_")
        else:
            lines.append("_交易明細資料不足。_")
        lines.append("")

        # ---- 8. 結論 ----
        lines.append("## 8. 結論")
        lines.append("")
        self._build_conclusion(lines, r)
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"_報告產生時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")
        lines.append("")
        lines.append("> ⚠️ 本系統僅供研究與模擬交易，不構成投資建議。第一版禁止實盤自動下單。")

        return '\n'.join(lines)

    def _build_conclusion(self, lines: list, r: dict):
        """Append conclusion section based on grade performance."""
        grade_df = r.get('grade_df', pd.DataFrame())
        if grade_df is None or grade_df.empty:
            lines.append("- 資料不足，無法給出結論。")
            return

        for grade in ['A', 'B', 'C']:
            sub = grade_df[grade_df['buy_point_grade'] == grade]
            if sub.empty:
                continue
            row = sub.iloc[0]
            wr  = row.get('win_rate_20d')
            ret = row.get('avg_return_20d')
            n   = row.get('signal_count', 0)

            if n < 10:
                lines.append(f"- {grade} 級：⚠️ 樣本 < 10，不輸出結論。")
                continue

            try:
                wr_f  = float(wr)  if wr  is not None else None
                ret_f = float(ret) if ret is not None else None
            except (TypeError, ValueError):
                wr_f = ret_f = None

            if wr_f is not None and ret_f is not None:
                if wr_f >= 60 and ret_f >= 5:
                    lines.append(f"- {grade} 級：✅ 勝率 {wr_f:.0f}%、平均 {ret_f:+.1f}%，訊號有效。")
                elif wr_f >= 50:
                    lines.append(f"- {grade} 級：⚪ 勝率 {wr_f:.0f}%、平均 {ret_f:+.1f}%，表現普通，可繼續觀察。")
                else:
                    lines.append(f"- {grade} 級：❌ 勝率 {wr_f:.0f}%、平均 {ret_f:+.1f}%，效果不佳，建議檢討進場條件。")
            else:
                lines.append(f"- {grade} 級：樣本不足，無法評估。")

        lines.append("- 建議累積更多真實 CSV 資料後重新驗證。")

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
