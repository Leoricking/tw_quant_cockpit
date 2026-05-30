"""
reports/daily_market_summary.py - Daily Market Summary builder (v0.3.16).

Generates a 6-section daily summary markdown combining universe, portfolio,
signal quality, and risk data.

Output: reports/auto_report_center/YYYY-MM-DD/daily_market_summary.md

[!] Research Only. Simulation Only. No Real Orders.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DailyMarketSummaryBuilder:
    """
    Assembles the daily_market_summary.md from cross-report context data.

    Parameters
    ----------
    report_date : YYYY-MM-DD string
    mode        : 'real' or 'mock'
    context     : cross-report context dict from AutoReportCenter._context
    """

    VERSION = "v0.3.16"

    def __init__(
        self,
        report_date: str,
        mode: str = "real",
        context: Optional[dict] = None,
    ):
        self.report_date = report_date
        self.mode        = mode
        self.context     = context or {}

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def build(self, output_dir: str) -> Optional[str]:
        """
        Build daily_market_summary.md in output_dir.

        Returns path to the written file, or None on failure.
        """
        os.makedirs(output_dir, exist_ok=True)
        try:
            lines: List[str] = []
            lines += self._header()
            lines += self._section_data_status()
            lines += self._section_today_candidates()
            lines += self._section_risk_warnings()
            lines += self._section_portfolio_observation()
            lines += self._section_signal_quality_observation()
            lines += self._section_conclusion()
            lines += self._footer()

            content = "\n".join(lines) + "\n"
            path = os.path.join(output_dir, "daily_market_summary.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("daily_market_summary.md written → %s", path)
            return path
        except Exception as exc:
            logger.error("DailyMarketSummaryBuilder.build failed: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------

    def _header(self) -> List[str]:
        return [
            f"# Daily Market Summary",
            f"",
            f"> **{self.VERSION}** | {self.report_date} | Mode: {self.mode.upper()}",
            f">",
            f"> [!] Research Only. Simulation Only. No Real Orders.",
            f"",
            f"---",
            f"",
        ]

    # ------------------------------------------------------------------
    # Section 1: 資料狀態
    # ------------------------------------------------------------------

    def _section_data_status(self) -> List[str]:
        ctx = self.context
        readiness  = ctx.get("data_readiness",  "UNKNOWN")
        usize      = ctx.get("universe_size",   "N/A")
        confidence = ctx.get("confidence",      "OBSERVATIONAL")
        daily_ok   = ctx.get("daily_data_ok",   None)
        fund_ok    = ctx.get("fundamental_ok",  None)
        inst_ok    = ctx.get("institutional_ok",None)

        def status_badge(v):
            if v is True:  return "✓ OK"
            if v is False: return "✗ Missing"
            return "? Unknown"

        lines = [
            "## 一、資料狀態",
            "",
            f"| 項目 | 狀態 |",
            f"|------|------|",
            f"| Data Readiness | {readiness} |",
            f"| Universe Size | {usize} symbols |",
            f"| Confidence | {confidence} |",
            f"| Daily K-line | {status_badge(daily_ok)} |",
            f"| Fundamental | {status_badge(fund_ok)} |",
            f"| Institutional | {status_badge(inst_ok)} |",
            "",
        ]

        missing_sources = ctx.get("missing_data_sources", [])
        if missing_sources:
            lines.append("**缺少資料來源：**")
            lines.append("")
            for src in missing_sources:
                lines.append(f"- ✗ {src}")
            lines.append("")

        return lines

    # ------------------------------------------------------------------
    # Section 2: 今日候選股票
    # ------------------------------------------------------------------

    def _section_today_candidates(self) -> List[str]:
        ctx = self.context
        candidates = ctx.get("top_candidates", [])

        lines = [
            "## 二、今日候選股票",
            "",
        ]

        if not candidates:
            lines.append("*未執行股票評分 / 資料不足*")
            lines.append("")
            return lines

        lines.append("| Rank | Symbol | Score | Bull | BuyPt | Strategy | Fund | Micro | Sector |")
        lines.append("|------|--------|-------|------|-------|----------|------|-------|--------|")

        for i, c in enumerate(candidates[:10], 1):
            if isinstance(c, dict):
                sym      = c.get("symbol", "—")
                score    = _fmt_f(c.get("portfolio_rank_score"))
                bull     = _fmt_f(c.get("bull_stock_score"))
                buypt    = _fmt_f(c.get("buy_point_score"))
                strat    = _fmt_f(c.get("strategy_knowledge_score"))
                fund     = _fmt_f(c.get("fundamental_quality_score"))
                micro    = _fmt_f(c.get("microstructure_score"))
                sector   = _fmt_f(c.get("sector_strength_score"))
            else:
                sym = str(c)
                score = buypt = bull = strat = fund = micro = sector = "—"
            lines.append(
                f"| {i} | {sym} | {score} | {bull} | {buypt} | {strat} | {fund} | {micro} | {sector} |"
            )

        lines.append("")

        # Warnings summary
        warned = [c for c in candidates if isinstance(c, dict) and c.get("has_warnings")]
        if warned:
            lines.append(f"**警示：{len(warned)} 支股票有一或多個 warning flag。**")
            lines.append("")

        return lines

    # ------------------------------------------------------------------
    # Section 3: 風險警示
    # ------------------------------------------------------------------

    def _section_risk_warnings(self) -> List[str]:
        ctx = self.context
        risk_warnings = ctx.get("risk_warnings", [])
        sector_conc   = ctx.get("sector_concentration_warning", False)
        overvalued    = ctx.get("overvalued_symbols", [])
        fake_bo       = ctx.get("fake_breakout_symbols", [])

        lines = [
            "## 三、風險警示",
            "",
        ]

        if not risk_warnings and not sector_conc and not overvalued and not fake_bo:
            lines.append("*本次掃描無特殊風險警示*")
            lines.append("")
            return lines

        if risk_warnings:
            for w in risk_warnings:
                lines.append(f"- ⚠️  {w}")
            lines.append("")

        if sector_conc:
            lines.append("- ⚠️  **板塊集中度偏高** — 候選股票集中在單一板塊，注意分散配置。")
            lines.append("")

        if overvalued:
            syms = ", ".join(str(s) for s in overvalued[:5])
            lines.append(f"- ⚠️  **估值偏高** — {syms}{'...' if len(overvalued) > 5 else ''}")
            lines.append("")

        if fake_bo:
            syms = ", ".join(str(s) for s in fake_bo[:5])
            lines.append(f"- ⚠️  **假突破警示** — {syms}{'...' if len(fake_bo) > 5 else ''}")
            lines.append("")

        return lines

    # ------------------------------------------------------------------
    # Section 4: 投資組合觀察
    # ------------------------------------------------------------------

    def _section_portfolio_observation(self) -> List[str]:
        ctx = self.context
        best_scenario = ctx.get("portfolio_best_scenario")
        best_return   = ctx.get("portfolio_best_return")
        best_sharpe   = ctx.get("portfolio_best_sharpe")
        best_maxdd    = ctx.get("portfolio_best_maxdd")
        best_pf       = ctx.get("portfolio_best_pf")
        n_scenarios   = ctx.get("portfolio_n_scenarios", 0)

        lines = [
            "## 四、投資組合觀察",
            "",
        ]

        if not best_scenario:
            lines.append("*投資組合模擬未執行 / 無結果*")
            lines.append("")
            return lines

        lines.append(f"模擬了 **{n_scenarios}** 個情境，最佳配置：")
        lines.append("")
        lines.append(f"| 指標 | 值 |")
        lines.append(f"|------|----|")
        lines.append(f"| Best Scenario | {best_scenario} |")
        if best_return is not None:
            lines.append(f"| Return | {best_return:+.2%} |")
        if best_sharpe is not None:
            lines.append(f"| Sharpe | {best_sharpe:.2f} |")
        if best_maxdd is not None:
            lines.append(f"| Max Drawdown | {best_maxdd:.2%} |")
        if best_pf is not None:
            lines.append(f"| Profit Factor | {best_pf:.2f} |")
        lines.append("")

        # Risk note
        if best_maxdd is not None and best_maxdd < -0.20:
            lines.append(
                f"> ⚠️  Max Drawdown {best_maxdd:.2%} 超過 20%，請留意資金配置。"
            )
            lines.append("")

        return lines

    # ------------------------------------------------------------------
    # Section 5: Signal Quality 觀察
    # ------------------------------------------------------------------

    def _section_signal_quality_observation(self) -> List[str]:
        ctx = self.context
        total    = ctx.get("signal_quality_total",  0)
        boost    = ctx.get("signal_quality_boost_count",  0)
        keep     = ctx.get("signal_quality_keep_count",   0)
        reduce   = ctx.get("signal_quality_reduce_count", 0)
        disable  = ctx.get("signal_quality_disable_count",0)
        insuf    = ctx.get("signal_quality_insufficient_count", 0)

        lines = [
            "## 五、Signal Quality 觀察",
            "",
        ]

        if total == 0:
            lines.append("*Signal Quality 分析未執行 / 無結果*")
            lines.append("")
            return lines

        lines.append(f"共評估 **{total}** 個訊號群組：")
        lines.append("")
        lines.append(f"| 推薦 | 數量 |")
        lines.append(f"|------|------|")
        lines.append(f"| BOOST | {boost} |")
        lines.append(f"| KEEP | {keep} |")
        lines.append(f"| REDUCE | {reduce} |")
        lines.append(f"| DISABLE | {disable} |")
        lines.append(f"| INSUFFICIENT_SAMPLE | {insuf} |")
        lines.append("")

        # Observation text
        if boost > reduce:
            lines.append(
                f"> 整體訊號品質偏正向（BOOST {boost} > REDUCE {reduce}），"
                f"現有訊號組合表現尚可。"
            )
        elif reduce > boost:
            lines.append(
                f"> ⚠️  整體訊號品質偏負向（REDUCE {reduce} > BOOST {boost}），"
                f"部分訊號歷史效果較差，建議審閱。"
            )
        else:
            lines.append("> 訊號品質 BOOST 與 REDUCE 持平，持續觀察。")
        lines.append("")

        return lines

    # ------------------------------------------------------------------
    # Section 6: 結論
    # ------------------------------------------------------------------

    def _section_conclusion(self) -> List[str]:
        ctx = self.context
        candidates = ctx.get("top_candidates", [])
        best_scenario = ctx.get("portfolio_best_scenario")
        boost  = ctx.get("signal_quality_boost_count", 0)
        reduce = ctx.get("signal_quality_reduce_count", 0)
        rw_best = ctx.get("rule_weight_best_config")
        risk_warnings = ctx.get("risk_warnings", [])

        lines = [
            "## 六、結論",
            "",
        ]

        bullets: List[str] = []

        if candidates:
            n = len(candidates)
            top_sym = candidates[0].get("symbol", candidates[0]) if isinstance(candidates[0], dict) else candidates[0]
            bullets.append(f"今日候選股票共 **{n}** 支，評分最高為 **{top_sym}**。")

        if best_scenario:
            bullets.append(f"投資組合最佳情境為 **{best_scenario}**。")

        if boost > 0 or reduce > 0:
            if boost > reduce:
                bullets.append(f"訊號品質整體正向（BOOST {boost} > REDUCE {reduce}）。")
            elif reduce > boost:
                bullets.append(f"訊號品質偏弱（REDUCE {reduce} > BOOST {boost}），請注意。")

        if rw_best:
            bullets.append(f"Rule Weight 建議最佳配置：**{rw_best}**（僅供參考，需手動套用）。")

        if risk_warnings:
            bullets.append(f"共有 **{len(risk_warnings)}** 項風險警示，請詳閱第三節。")

        if not bullets:
            lines.append("*本次執行結果有限，建議以完整 profile 重新執行。*")
            lines.append("")
        else:
            for b in bullets:
                lines.append(f"- {b}")
            lines.append("")

        lines.append(
            "> **[!] 所有結論僅供研究參考，不構成投資建議，不自動下單，"
            "不保證未來績效。**"
        )
        lines.append("")

        return lines

    # ------------------------------------------------------------------
    # Footer
    # ------------------------------------------------------------------

    def _footer(self) -> List[str]:
        return [
            "---",
            "",
            f"*Generated by TW Quant Cockpit {self.VERSION} — {self.report_date}*",
            "",
        ]


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _fmt_f(v, digits: int = 2) -> str:
    """Format a float value for display, or return '—' if None."""
    if v is None:
        return "—"
    try:
        return f"{float(v):.{digits}f}"
    except (TypeError, ValueError):
        return str(v)
