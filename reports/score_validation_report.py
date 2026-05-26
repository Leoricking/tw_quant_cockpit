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
        lines.append("> ⚠️ 本報告僅供研究參考，不構成投資建議。第一版禁止實盤自動下單。")
        lines.append("")

        # ---- 1. 驗證期間 ----
        lines.append("## 1. 驗證期間")
        lines.append("")
        lines.append(f"- 起始日：{r.get('start', '—')}")
        lines.append(f"- 結束日：{r.get('end',   '—')}")
        lines.append(f"- 股票數：{r.get('n_symbols', 0)}")
        lines.append(f"- 記錄筆數：{r.get('n_records', 0)}")
        src_tag = '🟡 SAMPLE CSV' if r.get('is_sample') else '🟢 REAL CSV'
        lines.append(f"- 資料來源：{src_tag}")
        lines.append(f"- 資料路徑：`{r.get('data_source', '—')}`")
        if r.get('n_symbols', 0) < 5:
            lines.append("")
            lines.append("> ⚠️ **樣本不足 5 支股票，統計可信度低，僅供觀察。**")
        lines.append("")

        # ---- 2. Score Bucket Performance ----
        lines.append("## 2. Score Bucket Performance")
        lines.append("")
        bucket_df = r.get('score_bucket_df', pd.DataFrame())
        if bucket_df is not None and not bucket_df.empty:
            lines.append("| 分數區間 | 樣本數 | 平均5日% | 平均10日% | 平均20日% | 勝率20日% | 最大回撤20日% | 停損觸發率% | 獲利因子20d | 備註 |")
            lines.append("|----------|--------|----------|-----------|-----------|-----------|--------------|-------------|------------|------|")
            for _, row in bucket_df.iterrows():
                note = row.get('sample_note', '')
                lines.append(
                    f"| {row.get('score_bucket','—')} "
                    f"| {row.get('sample_count','—')} "
                    f"| {_pct(row.get('avg_return_5d'))} "
                    f"| {_pct(row.get('avg_return_10d'))} "
                    f"| {_pct(row.get('avg_return_20d'))} "
                    f"| {_pct(row.get('win_rate_20d'))} "
                    f"| {_pct(row.get('avg_max_drawdown_20d'))} "
                    f"| {_pct(row.get('stop_loss_5pct_rate'))} "
                    f"| {_val(row.get('profit_factor_20d'), 2)} "
                    f"| {note} |"
                )
        else:
            lines.append("_資料不足，無法計算。_")
        lines.append("")

        # ---- 3. Factor Effectiveness ----
        lines.append("## 3. Factor Effectiveness（分項得分有效性）")
        lines.append("")
        factor_df = r.get('factor_df', pd.DataFrame())
        if factor_df is not None and not factor_df.empty:
            lines.append("| 因子 | 相關性5日 | 相關性10日 | 相關性20日 | 頂分位20日均報酬% | 底分位20日均報酬% | 有效性判斷 |")
            lines.append("|------|----------|-----------|-----------|-----------------|-----------------|----------|")
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
            lines.append("_資料不足，無法計算。_")
        lines.append("")

        # ---- 4. No-Entry Condition Effectiveness ----
        lines.append("## 4. No-Entry Condition Effectiveness（不可進場條件有效性）")
        lines.append("")
        no_entry_df = r.get('no_entry_df', pd.DataFrame())
        if no_entry_df is not None and not no_entry_df.empty:
            lines.append("| 條件 | 樣本數 | 平均5日% | 平均20日% | 勝率20日% | 最大回撤% | 降風險效果% | 建議 |")
            lines.append("|------|--------|----------|-----------|-----------|-----------|------------|------|")
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
            lines.append("_資料不足，無法計算。_")
        lines.append("")

        # ---- 5. Trust Cost Validation ----
        lines.append("## 5. Trust Cost Validation（投信成本線有效性）")
        lines.append("")
        trust_df = r.get('trust_cost_df', pd.DataFrame())
        if trust_df is not None and not trust_df.empty:
            lines.append("| 條件 | 樣本數 | 平均5日% | 平均10日% | 平均20日% | 勝率20日% | 最大回撤% |")
            lines.append("|------|--------|----------|-----------|-----------|-----------|-----------|")
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
            lines.append("_投信成本資料不足，無法計算。_")
        lines.append("")

        # ---- 6. Margin Risk Validation ----
        lines.append("## 6. Margin Risk Validation（融資風險有效性）")
        lines.append("")
        margin_df = r.get('margin_df', pd.DataFrame())
        if margin_df is not None and not margin_df.empty:
            lines.append("| 條件 | 樣本數 | 平均5日% | 平均10日% | 平均20日% | 勝率20日% | 最大回撤% |")
            lines.append("|------|--------|----------|-----------|-----------|-----------|-----------|")
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
            lines.append("_融資資料不足，無法計算。_")
        lines.append("")

        # ---- 7. 結論 ----
        lines.append("## 7. 結論")
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
        """Append conclusion section based on validation results."""
        bucket_df = r.get('score_bucket_df', pd.DataFrame())
        factor_df = r.get('factor_df', pd.DataFrame())
        n_sym     = r.get('n_symbols', 0)

        if n_sym < 5:
            lines.append("> ⚠️ 樣本股票數量不足 5 支，以下結論參考性有限。")
            lines.append("")

        if bucket_df is not None and not bucket_df.empty:
            high = bucket_df[bucket_df['score_bucket'] == '80-100']
            low  = bucket_df[bucket_df['score_bucket'] == '<50']
            h_ret = high['avg_return_20d'].values[0] if len(high) > 0 else None
            l_ret = low['avg_return_20d'].values[0]  if len(low)  > 0 else None
            if h_ret is not None and l_ret is not None and not pd.isna(h_ret) and not pd.isna(l_ret):
                try:
                    if float(h_ret) > float(l_ret) + 2.0:
                        lines.append("- ✅ **高分有效**：80-100 分區間 20 日報酬顯著優於低分，建議保留高分篩選邏輯。")
                    elif float(h_ret) < float(l_ret) - 2.0:
                        lines.append("- ❌ **高分無效**：低分組表現反而優於高分，需檢討分數邏輯。")
                    else:
                        lines.append("- ⚪ **差異不顯著**：各分數區間表現接近，可能需要更長時間驗證。")
                except (TypeError, ValueError):
                    pass
        else:
            lines.append("- 分數區間資料不足，無法給出結論。")

        if factor_df is not None and not factor_df.empty:
            strong = factor_df[factor_df['effectiveness_label'] == 'strong_positive']['factor'].tolist()
            negative = factor_df[factor_df['effectiveness_label'] == 'negative']['factor'].tolist()
            insufficient = factor_df[factor_df['effectiveness_label'] == 'insufficient_sample']['factor'].tolist()
            if strong:
                lines.append(f"- ✅ **建議保留**：{', '.join(strong)}")
            if negative:
                lines.append(f"- ⚠️ **建議降權重**：{', '.join(negative)}")
            if insufficient:
                lines.append(f"- ❓ **樣本不足**：{', '.join(insufficient)}")

        lines.append("- 建議累積更多真實 CSV 資料（至少 120 日 K 線、50+ 信號）後重新驗證。")
        lines.append("- 下一步：匯入更完整的 CSV 資料，接著執行 `python main.py validate-score --mode real`。")

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
