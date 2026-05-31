"""
reports/hardened_backtest_report.py — Hardened Backtest Report Builder (v0.3.26).

Generates reports/hardened_backtest_report_YYYY-MM-DD.md

[!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)

try:
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False


class HardenedBacktestReportBuilder:
    """
    Builds a Markdown report for the hardened backtest results.

    Output: reports/hardened_backtest_report_YYYY-MM-DD.md

    [!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only = True
    no_real_orders = True
    production_blocked = True

    VERSION = "0.3.26"

    SAFETY_BANNER = (
        "> [!WARNING]\n"
        "> **Research Only / Backtest Only / No Real Orders / Production Trading: BLOCKED**\n"
        "> This report is for research and educational purposes only.\n"
        "> It does NOT constitute investment advice and MUST NOT be used for live trading.\n"
    )

    def __init__(
        self,
        report_date: str | None = None,
        backtest_result: dict | None = None,
        mode: str = "real",
    ) -> None:
        self.report_date = report_date or str(date.today())
        self.backtest_result = backtest_result or {}
        self.mode = mode

    # ------------------------------------------------------------------
    # Main build
    # ------------------------------------------------------------------

    def build(self, output_dir: str | None = None) -> str:
        """
        Build and write the Markdown report.

        Returns path to the written file.
        """
        if output_dir is None:
            output_dir = os.path.join(BASE_DIR, "reports")

        os.makedirs(output_dir, exist_ok=True)
        filename = f"hardened_backtest_report_{self.report_date}.md"
        output_path = os.path.join(output_dir, filename)

        r = self.backtest_result
        assumptions = r.get("assumptions", {})
        exec_assumptions = assumptions.get("execution", {})
        cost_assumptions = assumptions.get("costs", {})
        split_assumptions = assumptions.get("split", {})
        split_metrics = r.get("split_metrics", [])
        regime_metrics = r.get("regime_metrics", {})

        lines = []

        # ------------------------------------------------------------------
        # 1. Header + safety banner
        # ------------------------------------------------------------------
        lines += [
            f"# TW Quant Cockpit v{self.VERSION} — Hardened Backtest Report",
            f"**Date:** {self.report_date}  ",
            f"**Mode:** {self.mode}  ",
            "",
            self.SAFETY_BANNER,
            "",
            "---",
            "",
        ]

        # ------------------------------------------------------------------
        # 2. 總覽 (Overview)
        # ------------------------------------------------------------------
        lines += [
            "## 2. 總覽 (Overview)",
            "",
            "| 參數 | 值 |",
            "|------|-----|",
            f"| mode | `{self.mode}` |",
            f"| entry_model | `{exec_assumptions.get('entry_model', 'N/A')}` |",
            f"| exit_model | `{exec_assumptions.get('exit_model', 'N/A')}` |",
            f"| cost_model | `{cost_assumptions.get('zero_cost', False) and 'zero_cost' or 'taiwan_realistic'}` |",
            f"| split_method | `{split_assumptions.get('method', 'N/A')}` |",
            f"| max_holding_days | `{exec_assumptions.get('max_holding_days', 'N/A')}` |",
            f"| stop_loss_pct | `{exec_assumptions.get('stop_loss_pct', 'N/A')}` |",
            f"| take_profit_pct | `{exec_assumptions.get('take_profit_pct', 'N/A')}` |",
            f"| read_only | `True` |",
            f"| no_real_orders | `True` |",
            f"| production_blocked | `True` |",
            "",
        ]

        # ------------------------------------------------------------------
        # 3. 核心績效 (Core Performance)
        # ------------------------------------------------------------------
        net_ret = r.get("net_return", 0.0)
        gross_ret = r.get("gross_return", 0.0)
        sharpe = r.get("sharpe")
        max_dd = r.get("max_drawdown")
        pf = r.get("profit_factor")
        wr = r.get("win_rate")
        tc = r.get("trade_count", 0)
        grade = r.get("confidence_grade", "D")

        def _fmt(v, pct=False, digits=4):
            if v is None:
                return "N/A"
            if pct:
                return f"{float(v):.2%}"
            return f"{float(v):.{digits}f}"

        # Annualized estimate (rough): assuming ~20 trading days per month
        ann_return = None
        if net_ret is not None and tc is not None and tc > 0:
            try:
                ann_return = float(net_ret) * 252.0  # per-trade avg * 252
            except Exception:
                pass

        lines += [
            "## 3. 核心績效 (Core Performance)",
            "",
            "| 指標 | 值 |",
            "|------|-----|",
            f"| 總淨報酬 (avg per trade) | `{_fmt(net_ret, pct=True)}` |",
            f"| 總毛報酬 (avg per trade) | `{_fmt(gross_ret, pct=True)}` |",
            f"| 年化估計 (rough) | `{_fmt(ann_return, pct=True) if ann_return else 'N/A'}` |",
            f"| Sharpe Ratio | `{_fmt(sharpe)}` |",
            f"| Max Drawdown | `{_fmt(max_dd, pct=True)}` |",
            f"| Profit Factor | `{_fmt(pf)}` |",
            f"| Win Rate | `{_fmt(wr, pct=True)}` |",
            f"| Trade Count | `{tc}` |",
            f"| Confidence Grade | `{grade}` |",
            "",
        ]

        # ------------------------------------------------------------------
        # 4. 與舊回測差異 (Differences vs Old Backtest)
        # ------------------------------------------------------------------
        lines += [
            "## 4. 與舊回測差異 (Differences vs Old Backtest)",
            "",
            "| 項目 | 舊版 (non-hardened) | v0.3.26 Hardened |",
            "|------|---------------------|-----------------|",
            "| Entry price | signal_close (look-ahead bias) | next_open (realistic) |",
            "| Transaction cost | zero_cost | 0.1425% commission × 0.6 + 0.3% sell tax + 5bps slippage |",
            "| Slippage | none | 5 bps base; scales with participation |",
            "| Liquidity filter | none | min volume 500, min turnover 10M NTD |",
            "| Gap risk | ignored | warn ≥3%, block ≥6% |",
            "| Validation | in-sample only | walk-forward / OOS |",
            "| Regime split | none | bull / bear / sideways / high_volatility |",
            "",
        ]

        # ------------------------------------------------------------------
        # 5. Walk-forward / OOS
        # ------------------------------------------------------------------
        lines += [
            "## 5. Walk-forward / OOS 分割績效",
            "",
        ]
        if split_metrics:
            lines += [
                "| split_id | split_type | train_start | train_end | test_start | test_end | trade_count | net_return | sharpe |",
                "|----------|------------|-------------|-----------|------------|----------|-------------|------------|--------|",
            ]
            for s in split_metrics:
                lines.append(
                    f"| {s.get('split_id', '-')} "
                    f"| {s.get('split_type', '-')} "
                    f"| {s.get('train_start', '-')} "
                    f"| {s.get('train_end', '-')} "
                    f"| {s.get('test_start', '-')} "
                    f"| {s.get('test_end', '-')} "
                    f"| {s.get('trade_count', '-')} "
                    f"| {_fmt(s.get('net_return'), pct=True)} "
                    f"| {_fmt(s.get('sharpe'))} |"
                )
        else:
            lines.append("_No split metrics available — run backtest to generate._")
        lines.append("")

        # ------------------------------------------------------------------
        # 6. Market Regime
        # ------------------------------------------------------------------
        lines += [
            "## 6. 市場環境分析 (Market Regime)",
            "",
        ]
        if regime_metrics:
            lines += [
                "| Regime | trade_count | net_return | sharpe | win_rate |",
                "|--------|-------------|------------|--------|----------|",
            ]
            for regime, rm in regime_metrics.items():
                lines.append(
                    f"| {regime} "
                    f"| {rm.get('trade_count', '-')} "
                    f"| {_fmt(rm.get('net_return'), pct=True)} "
                    f"| {_fmt(rm.get('sharpe'))} "
                    f"| {_fmt(rm.get('win_rate'), pct=True)} |"
                )
        else:
            lines.append("_No regime metrics available — run backtest with use_regime_split=True._")
        lines.append("")

        # ------------------------------------------------------------------
        # 7. 交易成本影響 (Cost Impact)
        # ------------------------------------------------------------------
        cost_impact = r.get("cost_impact")
        lines += [
            "## 7. 交易成本影響 (Transaction Cost Impact)",
            "",
            "| 項目 | 值 |",
            "|------|-----|",
            f"| Gross Return (avg) | `{_fmt(gross_ret, pct=True)}` |",
            f"| Net Return (avg) | `{_fmt(net_ret, pct=True)}` |",
            f"| Avg Cost Impact | `{_fmt(cost_impact, pct=True) if cost_impact else 'N/A'}` |",
            f"| Commission Rate | `{cost_assumptions.get('commission_rate', 'N/A')}` |",
            f"| Commission Discount | `{cost_assumptions.get('commission_discount', 'N/A')}` |",
            f"| Sell Tax Rate | `{cost_assumptions.get('tax_rate', 'N/A')}` |",
            f"| Slippage (bps) | `{cost_assumptions.get('slippage_bps', 'N/A')}` |",
            f"| Min Commission (NTD) | `{cost_assumptions.get('min_commission', 'N/A')}` |",
            "",
        ]

        # ------------------------------------------------------------------
        # 8. 流動性與跳空風險 (Liquidity & Gap Risk)
        # ------------------------------------------------------------------
        all_trades = r.get("_all_trades", [])
        rejected = sum(1 for t in all_trades if t.get("status") == "LIQUIDITY_REJECTED")
        gap_blocked = sum(1 for t in all_trades if t.get("status") == "GAP_BLOCKED")
        gap_warnings = sum(
            1 for t in all_trades
            if t.get("gap_status", "").startswith("GAP_") and t.get("status") == "OK"
        )

        liquidity_assumptions = assumptions.get("liquidity", {})
        gap_assumptions = assumptions.get("gap_risk", {})

        lines += [
            "## 8. 流動性與跳空風險 (Liquidity & Gap Risk)",
            "",
            "| 項目 | 值 |",
            "|------|-----|",
            f"| 流動性拒絕 (trades) | `{rejected}` |",
            f"| 跳空阻擋 (trades) | `{gap_blocked}` |",
            f"| 跳空警告 (OK trades with gap warning) | `{gap_warnings}` |",
            f"| min_daily_volume | `{liquidity_assumptions.get('min_daily_volume', 'N/A')}` |",
            f"| min_daily_turnover | `{liquidity_assumptions.get('min_daily_turnover', 'N/A')}` |",
            f"| max_participation_rate | `{liquidity_assumptions.get('max_participation_rate', 'N/A')}` |",
            f"| gap_warning_pct | `{gap_assumptions.get('gap_warning_pct', 'N/A')}` |",
            f"| gap_block_pct | `{gap_assumptions.get('gap_block_pct', 'N/A')}` |",
            "",
        ]

        # ------------------------------------------------------------------
        # 9. 回測可信度 (Backtest Credibility)
        # ------------------------------------------------------------------
        grade_explanation = {
            "A": "A級：交易筆數≥100，分割≥4，各分割≥10筆，最大回撤未達極端。最高可信度（仍不授權實盤交易）。",
            "B": "B級：交易筆數≥50，分割≥2。中等可信度。",
            "C": "C級：交易筆數≥20。低可信度，樣本有限。",
            "D": "D級：交易筆數不足20筆或資料嚴重不足。可信度極低。",
        }.get(grade, "未知等級")

        lines += [
            "## 9. 回測可信度 (Backtest Credibility)",
            "",
            f"**Confidence Grade: {grade}**",
            "",
            f"{grade_explanation}",
            "",
            "| 項目 | 值 |",
            "|------|-----|",
            f"| trade_count | `{tc}` |",
            f"| split_count | `{len(split_metrics)}` |",
            f"| confidence_grade | `{grade}` |",
            "",
            "> **重要提醒：即使達到 A 級，也不代表可以進行實盤交易。**",
            "> Walk-forward 指標優於 in-sample，但回測仍受資料限制、前視偏誤風險、滑價假設等制約。",
            "",
        ]

        # ------------------------------------------------------------------
        # 10. 安全聲明 (Safety Statement)
        # ------------------------------------------------------------------
        lines += [
            "## 10. 安全聲明 (Safety Statement)",
            "",
            "```",
            "════════════════════════════════════════════════════════════════════",
            "  RESEARCH ONLY / BACKTEST ONLY / NO REAL ORDERS",
            "  NOT INVESTMENT ADVICE",
            "════════════════════════════════════════════════════════════════════",
            "",
            "  This report is generated for research and educational purposes ONLY.",
            "  All results are simulated backtest results, NOT real trading results.",
            "",
            "  - read_only       = True",
            "  - no_real_orders  = True",
            "  - production_blocked = True",
            "",
            "  No orders, positions, or trades have been placed.",
            "  Past simulated performance does NOT guarantee future results.",
            "  All information herein does NOT constitute investment advice.",
            "  Consult a licensed financial advisor before making any investment decisions.",
            "",
            "  TW Quant Cockpit v0.3.26 — Production Trading: BLOCKED",
            "════════════════════════════════════════════════════════════════════",
            "```",
            "",
        ]

        content = "\n".join(lines)
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("HardenedBacktestReportBuilder: report written to %s", output_path)
        except Exception as exc:
            logger.error("HardenedBacktestReportBuilder.build write error: %s", exc)

        return output_path
