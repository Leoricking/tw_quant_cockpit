"""
reports/portfolio_simulation_report.py - Portfolio simulation Markdown report (v0.3.12).

Generates an 8-section Markdown report covering:
  1. 總覽 (Overview)
  2. 核心 KPI
  3. Scenario 比較
  4. 持倉與交易分析
  5. 風控規則效果
  6. 訊號來源效果
  7. 風險與限制
  8. 結論

Usage:
    rpt = PortfolioSimulationReport(results, all_scenario_results=scenario_dict)
    path = rpt.save()
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

_BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REPORTS_DIR = os.path.join(_BASE_DIR, 'reports')


class PortfolioSimulationReport:
    """Generates a Markdown Portfolio & Risk Simulation report."""

    def __init__(
        self,
        results: dict,
        all_scenario_results: Optional[dict] = None,
    ):
        self.results              = results
        self.all_scenario_results = all_scenario_results or {}

    # ------------------------------------------------------------------
    # Formatting
    # ------------------------------------------------------------------

    @staticmethod
    def _pct(v, dec=2):
        if v is None:
            return '—'
        try:
            return f'{float(v)*100:+.{dec}f}%'
        except Exception:
            return str(v)

    @staticmethod
    def _pct_plain(v, dec=2):
        if v is None:
            return '—'
        try:
            return f'{float(v)*100:.{dec}f}%'
        except Exception:
            return str(v)

    @staticmethod
    def _f(v, dec=3):
        if v is None:
            return '—'
        try:
            f = float(v)
            if f == float('inf'):
                return '∞'
            return f'{f:.{dec}f}'
        except Exception:
            return str(v)

    @staticmethod
    def _n(v):
        if v is None:
            return '—'
        return str(int(v))

    @staticmethod
    def _ntd(v):
        if v is None:
            return '—'
        try:
            return f'NTD {float(v):,.0f}'
        except Exception:
            return str(v)

    # ------------------------------------------------------------------
    # Section 1: Overview
    # ------------------------------------------------------------------

    def _section_overview(self) -> str:
        r    = self.results
        conf = r.get('confidence', {})
        cfg  = r.get('config', {})
        m    = r.get('metrics', {})

        lines = [
            '## 一、總覽',
            '',
            f"- **Data source**       : {'REAL CSV SAMPLE' if r.get('is_sample') else 'REAL CSV'}",
            f"- **Mode**              : {r.get('mode', '—')}",
            f"- **Universe size**     : {r.get('n_symbols', 0)}",
            f"- **Period**            : {r.get('start', '—')} → {r.get('end', '—')}",
            f"- **Trading days**      : {r.get('trading_days', '—')}",
            f"- **Initial capital**   : {self._ntd(cfg.get('initial_capital'))}",
            f"- **Final equity**      : {self._ntd(m.get('final_equity'))}",
            f"- **Max positions**     : {cfg.get('max_positions', '—')}",
            f"- **Position size**     : {self._pct_plain(cfg.get('position_size_pct'))} per position",
            f"- **Scenarios**         : {', '.join(self.all_scenario_results.keys()) if self.all_scenario_results else '1'}",
            f"- **Statistical confidence** : **{conf.get('overall', 'INSUFFICIENT')}**",
            '',
        ]
        for reason in conf.get('reasons', []):
            lines.append(f'  - {reason}')
        if conf.get('timing_warning'):
            lines.append(f'\n> ⚠ {conf["timing_warning"]}')

        tr = self.results.get('timing_estimated_ratio', None)
        if tr is not None:
            lines.append(f'\n- **Timing estimated ratio** : {self._pct_plain(tr)} of symbols have estimated announcement dates')

        entry_note = cfg.get('entry_price_note', '')
        if entry_note:
            lines.append(f'\n> **[Entry price note]** {entry_note}')

        lines += [
            '',
            '> [!] For research and simulation only. Not investment advice.',
            '',
        ]
        return '\n'.join(lines)

    # ------------------------------------------------------------------
    # Section 2: Core KPI
    # ------------------------------------------------------------------

    def _section_kpi(self) -> str:
        m = self.results.get('metrics', {})
        lines = [
            '## 二、核心 KPI',
            '',
            f"| KPI | Value | Target |",
            f"|-----|-------|--------|",
            f"| Total Return       | {self._pct(m.get('total_return'))} | — |",
            f"| Annualized Return  | {self._pct(m.get('annualized_return'))} | — |",
            f"| Volatility         | {self._pct(m.get('volatility'))} | — |",
            f"| Sharpe Ratio       | {self._f(m.get('sharpe'))} | > 1.5 |",
            f"| Max Drawdown       | {self._pct(m.get('max_drawdown'))} | > -20% |",
            f"| Profit Factor      | {self._f(m.get('profit_factor'))} | > 1.5 |",
            f"| Win Rate           | {self._pct_plain(m.get('win_rate'))} | 參考用 |",
            f"| Avg Win            | {self._pct(m.get('avg_win'))} | — |",
            f"| Avg Loss           | {self._pct(m.get('avg_loss'))} | — |",
            f"| Expectancy         | {self._pct(m.get('expectancy'))} | > 0% |",
            f"| Trade Count        | {self._n(m.get('trade_count'))} | — |",
            f"| Avg Holding Days   | {self._f(m.get('avg_holding_days'), 1)} | — |",
            f"| Average Exposure   | {self._pct_plain(m.get('average_exposure'))} | — |",
            f"| Turnover           | {self._f(m.get('turnover'), 2)}x | — |",
            f"| Recovery Factor    | {self._f(m.get('recovery_factor'))} | — |",
            '',
        ]
        return '\n'.join(lines)

    # ------------------------------------------------------------------
    # Section 3: Scenario comparison
    # ------------------------------------------------------------------

    def _section_scenarios(self) -> str:
        if not self.all_scenario_results:
            return '## 三、Scenario 比較\n\n*僅執行單一 scenario，無比較資料。*\n\n'

        from backtest.portfolio_scenarios import PortfolioScenarios
        comp_df = PortfolioScenarios.build_comparison_df(self.all_scenario_results)

        lines = [
            '## 三、Scenario 比較',
            '',
            '| Scenario | Total Ret | Sharpe | Max DD | PF | Win% | Trades | Note |',
            '|----------|----------|--------|--------|-----|------|--------|------|',
        ]
        for _, row in comp_df.iterrows():
            if row.get('status') != 'ok':
                lines.append(
                    f"| {row.get('scenario_name','')} | ERROR | — | — | — | — | — | {row.get('error','')} |"
                )
                continue
            lines.append(
                f"| {row.get('scenario_name','')} "
                f"| {self._pct(row.get('total_return'))} "
                f"| {self._f(row.get('sharpe'))} "
                f"| {self._pct(row.get('max_drawdown'))} "
                f"| {self._f(row.get('profit_factor'))} "
                f"| {self._pct_plain(row.get('win_rate'))} "
                f"| {self._n(row.get('trade_count'))} "
                f"| {row.get('note','')} |"
            )
        lines.append('')
        return '\n'.join(lines)

    # ------------------------------------------------------------------
    # Section 4: Trade analysis
    # ------------------------------------------------------------------

    def _section_trades(self) -> str:
        trades_df = self.results.get('trades_df', pd.DataFrame())
        lines = ['## 四、持倉與交易分析', '']

        if trades_df.empty:
            lines.append('*無成交記錄。*\n')
            return '\n'.join(lines)

        m = self.results.get('metrics', {})
        lines += [
            f"- Trade count        : {len(trades_df)}",
            f"- Avg holding days   : {self._f(m.get('avg_holding_days'), 1)}",
            '',
        ]

        # Exit reason breakdown
        if 'reason' in trades_df.columns:
            reasons = trades_df['reason'].value_counts()
            lines.append('**Exit reasons:**')
            lines.append('')
            lines.append('| Reason | Count |')
            lines.append('|--------|-------|')
            for reason, cnt in reasons.items():
                lines.append(f'| {reason} | {cnt} |')
            lines.append('')

        # Top 3 wins
        if 'pnl' in trades_df.columns and not trades_df.empty:
            top_wins = trades_df.nlargest(3, 'pnl')[['symbol','entry_date','exit_date','return_pct','pnl','reason']]
            worst    = trades_df.nsmallest(3, 'pnl')[['symbol','entry_date','exit_date','return_pct','pnl','reason']]

            lines.append('**Top 3 wins:**')
            lines.append('')
            lines.append('| Symbol | Entry | Exit | Ret% | P&L | Reason |')
            lines.append('|--------|-------|------|------|-----|--------|')
            for _, row in top_wins.iterrows():
                lines.append(
                    f"| {row.get('symbol','')} "
                    f"| {str(row.get('entry_date',''))[:10]} "
                    f"| {str(row.get('exit_date',''))[:10]} "
                    f"| {self._pct(row.get('return_pct'))} "
                    f"| {self._ntd(row.get('pnl'))} "
                    f"| {row.get('reason','')} |"
                )
            lines.append('')

            lines.append('**Worst 3 trades:**')
            lines.append('')
            lines.append('| Symbol | Entry | Exit | Ret% | P&L | Reason |')
            lines.append('|--------|-------|------|------|-----|--------|')
            for _, row in worst.iterrows():
                lines.append(
                    f"| {row.get('symbol','')} "
                    f"| {str(row.get('entry_date',''))[:10]} "
                    f"| {str(row.get('exit_date',''))[:10]} "
                    f"| {self._pct(row.get('return_pct'))} "
                    f"| {self._ntd(row.get('pnl'))} "
                    f"| {row.get('reason','')} |"
                )
            lines.append('')

            # Most traded symbols
            if 'symbol' in trades_df.columns:
                sym_counts = trades_df['symbol'].value_counts().head(5)
                lines.append('**Most traded symbols:**')
                lines.append('')
                for sym, cnt in sym_counts.items():
                    lines.append(f'- {sym}: {cnt} trades')
                lines.append('')

            # Sector concentration
            if 'sector' in trades_df.columns:
                sect_counts = trades_df['sector'].value_counts()
                lines.append('**Sector breakdown (by trades):**')
                lines.append('')
                for sec, cnt in sect_counts.items():
                    lines.append(f'- {sec}: {cnt} trades')
                lines.append('')

        return '\n'.join(lines)

    # ------------------------------------------------------------------
    # Section 5: Risk control effectiveness
    # ------------------------------------------------------------------

    def _section_risk_controls(self) -> str:
        trades_df = self.results.get('trades_df', pd.DataFrame())
        lines = ['## 五、風控規則效果', '']

        if trades_df.empty or 'reason' not in trades_df.columns:
            lines.append('*無成交記錄，無法分析風控規則效果。*\n')
            return '\n'.join(lines)

        for rule, label in [
            ('STOP_LOSS',        '固定停損'),
            ('TAKE_PROFIT_HALF', '停利一半'),
            ('TRAILING_STOP',    '移動停損'),
            ('END_OF_SIMULATION','模擬結束強平'),
        ]:
            subset = trades_df[trades_df['reason'] == rule]
            n = len(subset)
            if n == 0:
                lines.append(f'- **{label}** ({rule}): 0 次觸發')
                continue
            avg_ret = float(subset['return_pct'].mean()) if 'return_pct' in subset.columns else 0
            pnl_sum = float(subset['pnl'].sum()) if 'pnl' in subset.columns else 0
            lines.append(
                f'- **{label}** ({rule}): {n} 次觸發, '
                f'avg return {self._pct(avg_ret)}, '
                f'total P&L {self._ntd(pnl_sum)}'
            )

        lines.append('')
        cfg = self.results.get('config', {})
        lines += [
            '**Configuration:**',
            '',
            f"- Fixed stop loss     : {self._pct(cfg.get('stop_loss_pct'))}",
            f"- Take profit (half)  : {self._pct(cfg.get('take_profit_pct'))} (use_half={cfg.get('use_half_take_profit')})",
            f"- Trailing stop       : {self._pct(cfg.get('trailing_stop_pct'))}",
            f"- Max sector exposure : {self._pct(cfg.get('max_sector_exposure_pct'))}",
            f"- Max positions       : {cfg.get('max_positions')}",
            '',
        ]
        return '\n'.join(lines)

    # ------------------------------------------------------------------
    # Section 6: Signal source effectiveness
    # ------------------------------------------------------------------

    def _section_signals(self) -> str:
        lines = [
            '## 六、訊號來源效果',
            '',
            '本版本（v0.3.12）使用簡化技術訊號（MA alignment + volume expansion）作為 candidate 生成來源。',
            '基本面資料為靜態快照，非 per-date 時間序列過濾。',
            '',
            '訊號組合建議進化路徑：',
            '',
            '| 訊號來源 | v0.3.12 | 未來版本 |',
            '|---------|---------|---------|',
            '| bull_stock_score | 簡化 MA 技術分 | 完整 8 子分 from screener |',
            '| buy_point_grade | 未整合 | A/B/C from BuyPointAnalyzer |',
            '| strategy_knowledge | MA trend proxy | build_strategy_signals() |',
            '| fundamental_quality | EPS + GM 靜態 | per-date announcement_date 過濾 |',
            '| microstructure | volume ratio | intraday 1min 微結構分析 |',
            '| sector_strength | 固定 50 | 族群輪動分析 |',
            '',
        ]
        return '\n'.join(lines)

    # ------------------------------------------------------------------
    # Section 7: Risks and limitations
    # ------------------------------------------------------------------

    def _section_risks(self) -> str:
        r    = self.results
        conf = r.get('confidence', {})
        cfg  = r.get('config', {})
        tr   = r.get('timing_estimated_ratio', 0)

        lines = [
            '## 七、風險與限制',
            '',
            '以下限制適用於本次回測結果，所有數字不得用於實際投資決策：',
            '',
            f"1. **Universe size** : {r.get('n_symbols', 0)} symbols — "
            f"統計置信度 {conf.get('overall', 'INSUFFICIENT')}，樣本不足不可宣稱策略有效",
            f"2. **Signal-date close entry** : 進場使用當日收盤價，"
            "未考慮次日開盤價差（look-ahead bias risk）",
            f"3. **TIMING_ESTIMATED** : {self._pct_plain(tr)} of symbols 的財報公告日為估計值，"
            "財報品質因子時效性存疑",
            "4. **靜態基本面快照** : 基本面資料未按歷史日期過濾，"
            "存在資料穿越風險（未來版本改進）",
            "5. **No real orders** : 所有交易為模擬，不代表真實成交價格",
            "6. **Simple fee model** : "
            f"fee={cfg.get('fee_rate',0.001425):.4f}, tax={cfg.get('tax_rate_sell',0.003):.3f}, "
            f"slippage={cfg.get('slippage_bps',5)}bps，未考慮市場衝擊與流動性",
            "7. **No short selling** : 模擬僅做多，不做空",
            "8. **No margin / leverage** : 不使用槓桿，現金不足時不買入",
            '',
        ]
        return '\n'.join(lines)

    # ------------------------------------------------------------------
    # Section 8: Conclusions
    # ------------------------------------------------------------------

    def _section_conclusions(self) -> str:
        r    = self.results
        conf = r.get('confidence', {})
        m    = r.get('metrics', {})
        overall = conf.get('overall', 'INSUFFICIENT')

        lines = [
            '## 八、結論',
            '',
            f'統計置信度: **{overall}**',
            '',
        ]

        if overall == 'INSUFFICIENT':
            lines += [
                '- 樣本量不足（< 30 symbols 或 < 30 trades），無法得出可靠結論。',
                '- 本報告僅確認 portfolio simulation 框架功能正常。',
                '- 擴大 universe 至 ≥30 個股後可提升到 OBSERVATIONAL 等級。',
                '',
            ]
        else:
            sharpe = m.get('sharpe')
            max_dd = m.get('max_drawdown')
            pf     = m.get('profit_factor')
            notes  = []
            if sharpe is not None and float(sharpe) > 1.5:
                notes.append(f'Sharpe {float(sharpe):.2f} > 1.5 目標 ✓')
            elif sharpe is not None:
                notes.append(f'Sharpe {float(sharpe):.2f} 未達 1.5 目標')
            if max_dd is not None and float(max_dd) > -0.20:
                notes.append(f'Max Drawdown {float(max_dd)*100:.1f}% < 20% 目標 ✓')
            elif max_dd is not None:
                notes.append(f'Max Drawdown {float(max_dd)*100:.1f}% 超過 20% 目標')
            if pf is not None and float(pf) > 1.5:
                notes.append(f'Profit Factor {float(pf):.2f} > 1.5 目標 ✓')
            elif pf is not None and float(pf) != float('inf'):
                notes.append(f'Profit Factor {float(pf):.2f} 未達 1.5 目標')
            for n in notes:
                lines.append(f'- {n}')

        # Scenario recommendation (only if multiple scenarios run)
        if self.all_scenario_results and len(self.all_scenario_results) > 1:
            from backtest.portfolio_scenarios import PortfolioScenarios
            comp_df = PortfolioScenarios.build_comparison_df(self.all_scenario_results)
            ok_df   = comp_df[comp_df.get('status', 'ok') == 'ok']
            if not ok_df.empty and 'sharpe' in ok_df.columns:
                best = ok_df.loc[ok_df['sharpe'].idxmax()]
                lines.append(f"\n- **建議 scenario**: `{best.get('scenario_name','—')}` "
                              f"(Sharpe={self._f(best.get('sharpe'))})")

        lines += [
            '',
            '> **[!] 本報告僅供研究與模擬，不構成投資建議。**',
            '> Generated by TW Quant Cockpit v0.3.12',
            '',
        ]
        return '\n'.join(lines)

    # ------------------------------------------------------------------
    # Build & save
    # ------------------------------------------------------------------

    def build(self) -> str:
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        header = (
            '# TW Quant Cockpit — Portfolio & Risk Simulation Report\n\n'
            f'Generated: {ts}  \n'
            'Version: v0.3.12\n\n'
            '---\n\n'
        )
        sections = [
            self._section_overview(),
            self._section_kpi(),
            self._section_scenarios(),
            self._section_trades(),
            self._section_risk_controls(),
            self._section_signals(),
            self._section_risks(),
            self._section_conclusions(),
        ]
        return header + '\n'.join(sections)

    def save(self, output_dir: Optional[str] = None) -> str:
        """Save to reports/portfolio_simulation_report_YYYY-MM-DD.md and return path."""
        out_dir = output_dir or _REPORTS_DIR
        os.makedirs(out_dir, exist_ok=True)
        today = datetime.now().strftime('%Y-%m-%d')
        path  = os.path.join(out_dir, f'portfolio_simulation_report_{today}.md')
        content = self.build()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info("PortfolioSimulationReport: saved to %s", path)
        return path
