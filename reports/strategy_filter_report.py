"""
reports/strategy_filter_report.py — Strategy Filter Report generator (v0.5.1.1).

Produces: reports/strategy_filter_report_YYYY-MM-DD.md

Sections:
  一、總覽
  二、Financial Turnaround & Trend Discipline
  三、Entry Conditions
  四、Exit / Reduce Conditions
  五、Avoid Conditions
  六、安全聲明

[!] Research Only. Strategy Filter Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_REPORTS_DIR = os.path.join(_BASE_DIR, "reports")


class StrategyFilterReport:
    """
    Generates Markdown strategy filter report from StrategyFilterPack results.

    [!] Research Only. Strategy Filter Only. No Real Orders. Production Trading: BLOCKED.
    """

    VERSION = "v0.5.1.1"

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(
        self,
        mode: str = "real",
        report_date: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> None:
        self.mode        = mode
        self.report_date = report_date or datetime.now().strftime("%Y-%m-%d")
        self.output_dir  = output_dir or _DEFAULT_REPORTS_DIR

    # ------------------------------------------------------------------
    # Public entry points
    # ------------------------------------------------------------------

    def generate(
        self,
        symbol: str,
        filter_result: Dict[str, Any],
    ) -> str:
        """
        Generate a single-stock strategy filter report as a Markdown string.

        Parameters
        ----------
        symbol        : stock symbol string
        filter_result : dict from FinancialTurnaroundFilter.evaluate()
        """
        date_str = self.report_date
        lines: List[str] = []

        lines.append(f"# Strategy Filter Report — {symbol} ({date_str})")
        lines.append("")
        lines.append("> **[!] Research Only. Strategy Filter Only. No Real Orders. Production Trading: BLOCKED.**")
        lines.append("")

        # --- 一、總覽 ---
        lines.append("## 一、總覽")
        lines.append("")
        lines.append(f"- Research Only: YES")
        lines.append(f"- Strategy Filter Only: YES")
        lines.append(f"- No Real Orders: YES")
        lines.append(f"- Mode: {self.mode}")
        lines.append(f"- Report Date: {date_str}")
        lines.append(f"- Symbol: {symbol}")
        lines.append(f"- Filter Version: {filter_result.get('filter_version', self.VERSION)}")
        lines.append("")

        # --- 二、Financial Turnaround & Trend Discipline ---
        lines.append("## 二、Financial Turnaround & Trend Discipline")
        lines.append("")
        score    = filter_result.get("score", 0)
        scenario = filter_result.get("scenario", "UNKNOWN")
        labels   = filter_result.get("labels", [])
        action   = filter_result.get("suggested_action", "WATCH")

        lines.append(f"| Field | Value |")
        lines.append(f"|-------|-------|")
        lines.append(f"| Score | {score} / 100 |")
        lines.append(f"| Scenario | {scenario} |")
        lines.append(f"| Suggested Action | **{action}** |")
        lines.append(f"| Labels | {', '.join(labels) if labels else '—'} |")
        lines.append("")

        # Score breakdown
        breakdown = filter_result.get("score_breakdown", {})
        if breakdown:
            lines.append("### Score Breakdown")
            lines.append("")
            lines.append("| Dimension | Score |")
            lines.append("|-----------|-------|")
            dim_labels = {
                "fundamental": "財報 / EPS 成長 (max 25)",
                "revenue":     "月營收 / 毛利率 / 營益率 (max 15)",
                "base":        "低位階 / 底部翻多 (max 15)",
                "technical":   "技術轉強 / 站回均線 (max 15)",
                "chip":        "法人 / 籌碼支持 (max 15)",
                "risk":        "風控健康度 / 融資 (max 10)",
                "deduction":   "避雷扣分 (最多 -30)",
            }
            for k, v in breakdown.items():
                label = dim_labels.get(k, k)
                lines.append(f"| {label} | {v:+.0f} |")
            lines.append("")

        # Bullish reasons
        bullish = filter_result.get("bullish_reasons", [])
        lines.append("### 利多理由")
        lines.append("")
        if bullish:
            for b in bullish:
                lines.append(f"- {b}")
        else:
            lines.append("- (無明顯利多)")
        lines.append("")

        # Risk reasons
        risk_r = filter_result.get("risk_reasons", [])
        lines.append("### 風險理由")
        lines.append("")
        if risk_r:
            for r in risk_r:
                lines.append(f"- {r}")
        else:
            lines.append("- (無明顯風險扣分)")
        lines.append("")

        # --- 三、Entry Conditions ---
        lines.append("## 三、Entry Conditions")
        lines.append("")
        entry = filter_result.get("entry_conditions", [])
        entry_defaults = [
            "財報好 (EPS正成長 / 月營收續強)",
            "技術翻多 (底部突破 / 站上均線)",
            "籌碼支持 (法人未大賣)",
            "回測不破 (5日線 / 10日線 / 頸線)",
        ]
        for cond in (entry or entry_defaults):
            lines.append(f"- {cond}")
        lines.append("")

        # --- 四、Exit / Reduce Conditions ---
        lines.append("## 四、Exit / Reduce Conditions")
        lines.append("")
        exits = filter_result.get("exit_conditions", [])
        exit_defaults = [
            "跌破20日線且3天站不回 → 減碼1/3～1/2",
            "跌破60日線 → 趨勢轉弱，考慮出場",
            "高檔爆量長上影 → 考慮減碼",
            "法人轉賣 → 降低持倉",
        ]
        for cond in (exits or exit_defaults):
            lines.append(f"- {cond}")
        lines.append("")

        # --- 五、Avoid Conditions ---
        lines.append("## 五、Avoid Conditions")
        lines.append("")
        avoids = filter_result.get("avoid_conditions", [])
        avoid_defaults = [
            "財報差 (EPS衰退 / 營收衰退)",
            "大盤創高但個股不創高 (相對弱勢)",
            "M頭 / 多重頂 / 頭肩頂 / 弧形頂",
            "純題材但營收跟不上",
        ]
        for cond in (avoids or avoid_defaults):
            lines.append(f"- {cond}")
        lines.append("")

        # --- 六、安全聲明 ---
        lines.append("## 六、安全聲明")
        lines.append("")
        lines.append("- 不下單")
        lines.append("- 不構成投資建議")
        lines.append("- Research Only / Strategy Filter Only / No Real Orders")
        lines.append("- **Production Trading: BLOCKED**")
        lines.append("")
        lines.append("---")
        lines.append(f"*Generated by StrategyFilterReport {self.VERSION} | {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

        return "\n".join(lines)

    def save(
        self,
        symbol: str,
        filter_result: Dict[str, Any],
        output_dir: Optional[str] = None,
    ) -> str:
        """
        Generate and save a strategy filter report to disk.

        Returns the absolute path of the saved Markdown file.
        """
        out_dir = output_dir or self.output_dir
        os.makedirs(out_dir, exist_ok=True)
        filename = f"strategy_filter_report_{self.report_date}.md"
        if symbol and symbol not in ("UNKNOWN", ""):
            filename = f"strategy_filter_report_{symbol}_{self.report_date}.md"
        path = os.path.join(out_dir, filename)

        content = self.generate(symbol, filter_result)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)

        logger.info("StrategyFilterReport: saved to %s", path)
        return path

    def generate_pack_report(
        self,
        pack_results: List[Dict[str, Any]],
        summary: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a multi-stock strategy filter pack report as Markdown.

        Parameters
        ----------
        pack_results : list of run_all() results from StrategyFilterPack
        summary      : optional summary dict from StrategyFilterPack.build_summary()
        """
        date_str = self.report_date
        lines: List[str] = []

        lines.append(f"# Strategy Filter Pack Report ({date_str})")
        lines.append("")
        lines.append("> **[!] Research Only. Strategy Filter Only. No Real Orders. Production Trading: BLOCKED.**")
        lines.append("")

        # 一、總覽
        lines.append("## 一、總覽")
        lines.append("")
        lines.append(f"- Research Only: YES")
        lines.append(f"- Strategy Filter Only: YES")
        lines.append(f"- No Real Orders: YES")
        lines.append(f"- Mode: {self.mode}")
        lines.append(f"- Stocks analyzed: {len(pack_results)}")
        lines.append("")

        if summary:
            action_counts = summary.get("action_counts", {})
            if action_counts:
                lines.append("### Action Distribution")
                lines.append("")
                lines.append("| Action | Count |")
                lines.append("|--------|-------|")
                for act, cnt in sorted(action_counts.items()):
                    lines.append(f"| {act} | {cnt} |")
                lines.append("")

        # 二、Candidates Table
        lines.append("## 二、Financial Turnaround & Trend Discipline — 個股總表")
        lines.append("")
        lines.append("| Symbol | Score | Scenario | Suggested Action | Labels |")
        lines.append("|--------|-------|----------|-----------------|--------|")

        for res in pack_results:
            sym    = res.get("symbol", "?")
            score  = res.get("aggregate_score", 0)
            ft     = res.get("filters", {}).get("financial_turnaround", {})
            scen   = ft.get("scenario", "—")
            action = res.get("suggested_action", "WATCH")
            lbls   = ", ".join(ft.get("labels", [])) or "—"
            lines.append(f"| {sym} | {score:.0f} | {scen} | **{action}** | {lbls} |")

        lines.append("")

        # 六、安全聲明
        lines.append("## 六、安全聲明")
        lines.append("")
        lines.append("- 不下單")
        lines.append("- 不構成投資建議")
        lines.append("- Research Only / Strategy Filter Only / No Real Orders")
        lines.append("- **Production Trading: BLOCKED**")
        lines.append("")
        lines.append("---")
        lines.append(f"*Generated by StrategyFilterReport {self.VERSION} | {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

        return "\n".join(lines)

    def save_pack_report(
        self,
        pack_results: List[Dict[str, Any]],
        summary: Optional[Dict[str, Any]] = None,
        output_dir: Optional[str] = None,
    ) -> str:
        """Save the pack report and return the path."""
        out_dir = output_dir or self.output_dir
        os.makedirs(out_dir, exist_ok=True)
        filename = f"strategy_filter_report_{self.report_date}.md"
        path = os.path.join(out_dir, filename)
        content = self.generate_pack_report(pack_results, summary)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        logger.info("StrategyFilterReport (pack): saved to %s", path)
        return path
