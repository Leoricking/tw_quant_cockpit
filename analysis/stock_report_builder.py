"""
analysis/stock_report_builder.py - Markdown stock analysis report builder.

Assembles a complete stock analysis report from multi-timeframe analysis results.
"""

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

_DATA_INSUFFICIENT_WARNING = "資料不足，只能做盤中初估，不能當正式短中長線操作依據"


class StockReportBuilder:
    """
    Builds Markdown stock analysis reports from analyzer outputs.
    """

    def build(self, symbol, name=None, bull_score_data=None,
              daytrade_result=None, short_result=None,
              mid_result=None, long_result=None, mode: str = 'mock'):
        """
        Build a complete Markdown analysis report.

        Parameters
        ----------
        symbol : str
            Stock symbol.
        name : str, optional
            Stock name in Chinese.
        bull_score_data : dict, optional
            Output from ScreenerPipeline.get_top_candidates() row.
        daytrade_result : dict, optional
            Output from DaytradeAnalyzer.analyze().
        short_result : dict, optional
            Output from ShortTermAnalyzer.analyze().
        mid_result : dict, optional
            Output from MidTermAnalyzer.analyze().
        long_result : dict, optional
            Output from LongTermAnalyzer.analyze().

        Returns
        -------
        str
            Formatted Markdown report text.
        """
        sym = str(symbol)
        stock_name = name or sym
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check overall data sufficiency
        has_sufficient_data = any([
            bull_score_data is not None,
            daytrade_result is not None and daytrade_result.get('data_completeness', 0) >= 40,
            short_result is not None and short_result.get('data_completeness', 0) >= 50,
        ])

        # Overall data mode (prefer explicit mode arg, then infer from results)
        all_results = [r for r in (daytrade_result, short_result, mid_result, long_result) if r]
        if mode == 'real':
            has_real_prices = any(r.get('data_source') == 'real' for r in all_results)
            overall_mode = ('🟢 REAL DATA'
                            if has_real_prices
                            else '🔴 REAL MODE — 缺真實資料，價格目標不可信')
        else:
            overall_mode = '🟡 MOCK DATA — 示範模式，非正式分析'

        lines = []
        lines.append(f"# 股票分析報告：{sym} {stock_name}")
        lines.append(f"報告時間：{ts}　　資料模式：**{overall_mode}**")
        lines.append("")

        if not has_sufficient_data:
            lines.append(f"> ⚠️ **{_DATA_INSUFFICIENT_WARNING}**")
            lines.append("")

        # Section 1: Bull Stock Score
        lines.append("## 一、飆股候選評分")
        if bull_score_data:
            score = bull_score_data.get('bull_stock_score', 'N/A')
            is_bull = bull_score_data.get('is_bull_candidate', False)
            is_second = bull_score_data.get('is_second_wave_buy_point', False)
            formal_allowed = bull_score_data.get('formal_allowed', True)
            themes = bull_score_data.get('theme_tags', [])
            theme_str = '、'.join(themes[:5]) if themes else '未分類'
            reason = bull_score_data.get('reason_summary', '-')
            risk = bull_score_data.get('risk_summary', '-')

            lines.append(f"- 綜合分數：**{score}/100**")
            lines.append(f"- 是否飆股候選：{'✅ 是' if is_bull else '❌ 否'}")
            lines.append(f"- 是否第二波買點：{'✅ 是' if is_second else '❌ 否'}")
            lines.append(f"- 是否允許正式判斷：{'✅ 是' if formal_allowed else '❌ 否（資料不足）'}")
            lines.append(f"- 主流題材：{bull_score_data.get('theme_score', bull_score_data.get('theme_score', 'N/A'))} / 20")
            lines.append(f"- 基本面：{bull_score_data.get('fundamental_score', 'N/A')} / 15")
            # Support both old field names (technical_score) and new (trend_score)
            _trend = bull_score_data.get('trend_score', bull_score_data.get('technical_score', 'N/A'))
            lines.append(f"- 均線轉強：{_trend} / 15")
            _bv = bull_score_data.get('breakout_volume_score', bull_score_data.get('breakout_score', 'N/A'))
            lines.append(f"- 突破與量能：{_bv} / 15")
            _inst = bull_score_data.get('institution_score', bull_score_data.get('chip_score', 'N/A'))
            lines.append(f"- 法人籌碼：{_inst} / 15")
            lines.append(f"- 大戶散戶：{bull_score_data.get('holder_score', 'N/A')} / 10")
            lines.append(f"- 融資風險：{bull_score_data.get('margin_score', 'N/A')} / 5")
            lines.append(f"- 過熱風險：{bull_score_data.get('overheat_score', 'N/A')} / 5")
            _tc = bull_score_data.get('trust_cost_score', 'N/A')
            _tc_note = bull_score_data.get('trust_cost_note', '')
            lines.append(f"- 投信成本支撐：{_tc}{' — ' + _tc_note if _tc_note else ''}")
            # Deduction and missing reasons
            deductions = bull_score_data.get('deduction_reasons', [])
            missing_r = bull_score_data.get('missing_data_reasons', [])
            lines.append(f"- 扣分原因：{' / '.join(deductions) if deductions else '無'}")
            lines.append(f"- 缺失資料：{' / '.join(missing_r) if missing_r else '無'}")
            lines.append(f"- 主題標籤：{theme_str}")
            if reason and reason != '-':
                lines.append(f"- 選股理由：{reason}")
            if risk and risk != '-':
                lines.append(f"- 風險提示：{risk}")
        else:
            lines.append("- 尚無篩選資料（請先執行 screener）")
        lines.append("")

        # Section 2: Life Cycle
        lines.append("## 二、生命週期定位")
        lines.append(self._infer_lifecycle(bull_score_data, daytrade_result, short_result, mid_result))
        lines.append("")

        # Section 3: Daytrade
        lines.append("## 三、當沖策略")
        if daytrade_result:
            self._append_strategy_section(lines, daytrade_result, mode=mode)
        else:
            lines.append("- 無即時盤口資料，無法生成當沖建議")
        lines.append("")

        # Section 4: Short term
        lines.append("## 四、短線策略（5-20日）")
        if short_result:
            self._append_strategy_section(lines, short_result, mode=mode)
        else:
            lines.append("- 短線資料不足")
        lines.append("")

        # Section 5: Mid term
        lines.append("## 五、中線策略（1-3月）")
        if mid_result:
            self._append_strategy_section(lines, mid_result, mode=mode)
        else:
            lines.append("- 中線資料不足")
        lines.append("")

        # Section 6: Long term
        lines.append("## 六、長線策略（3-12月）")
        if long_result:
            self._append_strategy_section(lines, long_result, mode=mode)
        else:
            lines.append("- 長線資料不足")
        lines.append("")

        # Section 7: Buy Point Grade
        lines.append("## 七、買點分級判斷")
        # Extract buy_point fields from daytrade_result first, then short_result
        bp_source = None
        for r in (daytrade_result, short_result):
            if r and r.get('buy_point_grade') is not None:
                bp_source = r
                break
        if bp_source:
            grade = bp_source.get('buy_point_grade', 'N/A')
            bp_type = bp_source.get('buy_point_type', 'N/A')
            support = bp_source.get('support_price', 'N/A')
            confirm = bp_source.get('confirm_price', 'N/A')
            invalid = bp_source.get('invalid_price', 'N/A')
            no_entry = bp_source.get('no_entry_conditions', [])
            bp_reasoning = bp_source.get('reasoning', '-')
            lines.append(f"- 買點等級：**{grade}**")
            lines.append(f"- 買點型態：{bp_type}")
            lines.append(f"- 支撐價：{support}")
            lines.append(f"- 確認價：{confirm}")
            lines.append(f"- 失效價：{invalid}")
            lines.append(f"- 可買條件：已符合 {grade} 級買點條件")
            lines.append(f"- 不可買條件：{' / '.join(no_entry) if no_entry else '無'}")
            lines.append(f"- 判斷依據：{bp_reasoning}")
        else:
            lines.append("- 買點等級：尚未觸發任何買點條件")
            lines.append("- 買點型態：-")
            lines.append("- 支撐價：-")
            lines.append("- 確認價：-")
            lines.append("- 失效價：-")
            lines.append("- 可買條件：-")
            no_entry_all = []
            for r in (daytrade_result, short_result):
                if r:
                    for c in r.get('no_entry_conditions', []):
                        if c not in no_entry_all:
                            no_entry_all.append(c)
            lines.append(f"- 不可買條件：{' / '.join(no_entry_all) if no_entry_all else '-'}")
            fallback_reasoning = (
                (daytrade_result or {}).get('reasoning')
                or (short_result or {}).get('reasoning')
                or '資料不足'
            )
            lines.append(f"- 判斷依據：{fallback_reasoning}")
        lines.append("")

        # Section 8: Data completeness
        lines.append("## 八、資料完整度")
        for label, result in [
            ('當沖', daytrade_result),
            ('短線', short_result),
            ('中線', mid_result),
            ('長線', long_result),
        ]:
            if result:
                comp = result.get('data_completeness', 0)
                w = result.get('warning', '')
                status = '✅' if comp >= 50 else '⚠️'
                lines.append(f"- {label}: {status} {comp:.0f}%{' — ' + w if w else ''}")
            else:
                lines.append(f"- {label}: ❌ 無資料")

        if not has_sufficient_data:
            lines.append("")
            lines.append(f"> **{_DATA_INSUFFICIENT_WARNING}**")

        lines.append("")
        lines.append("---")
        lines.append("*本報告由 TW Quant Cockpit v1 自動生成，僅供研究參考，不構成投資建議。*")

        return '\n'.join(lines)

    def _append_strategy_section(self, lines, result, mode: str = 'mock'):
        """Append strategy section lines from an analyzer result dict."""
        decision = result.get('decision', 'N/A')
        confidence = result.get('confidence', 0)
        add_price = result.get('add_position_price')
        exit_price = result.get('exit_price')
        stop_price = result.get('stop_loss_price')
        no_entry = result.get('no_entry_conditions', [])
        reasoning = result.get('reasoning', '-')
        warning = result.get('warning')
        data_source = result.get('data_source', 'mock')
        is_estimate = result.get('prices_are_estimates', True)

        # In real mode but data_source is mock (fallback seed prices), suppress targets
        suppress_prices = (mode == 'real' and data_source == 'mock')

        src_label = '🟡 [MOCK]' if data_source == 'mock' else ('🟢 [REAL]' if data_source == 'real' else '🔶 [PARTIAL]')
        price_note = '（估算值）' if is_estimate and not suppress_prices else ''

        lines.append(f"- 操作決策：**{decision}**（信心度 {confidence}%）{src_label}")
        _dash = "—"
        if suppress_prices or add_price is None:
            _add_str = f"{_dash} （real mode 缺真實資料）" if suppress_prices else _dash
        else:
            _add_str = f"{add_price}{price_note}"
        if suppress_prices or exit_price is None:
            _exit_str = f"{_dash} （real mode 缺真實資料）" if suppress_prices else _dash
        else:
            _exit_str = f"{exit_price}{price_note}"
        if suppress_prices or stop_price is None:
            _stop_str = f"{_dash} （real mode 缺真實資料）" if suppress_prices else _dash
        else:
            _stop_str = f"{stop_price}{price_note}"
        lines.append(f"- 補倉價位：{_add_str}")
        lines.append(f"- 出倉價位：{_exit_str}")
        lines.append(f"- 停損價位：{_stop_str}")
        lines.append(f"- 不可進場條件：{' / '.join(no_entry) if no_entry else '無'}")
        lines.append(f"- 判斷依據：{reasoning}")
        _completeness = result.get('data_completeness', 0)
        _formal = not result.get('prices_are_estimates', True)
        lines.append(f"- 資料完整度：{_completeness:.0f}%　是否允許正式判斷：{'✅ 是' if _formal else '❌ 否'}")
        if warning:
            lines.append(f"- ⚠️ 資料警告：{warning}")

    def _infer_lifecycle(self, bull_data, daytrade, short, mid):
        """Infer stock lifecycle phase from available data."""
        if bull_data:
            score = float(bull_data.get('bull_stock_score', 50))
            if score >= 80:
                return "**主升段** — 飆股候選，強勢股，建議持有或加碼"
            elif score >= 65:
                return "**初升段 / 第二波** — 強勢整理後確認，可布局"
            elif score >= 50:
                return "**盤整觀察** — 等待突破確認"
            else:
                return "**弱勢 / 避開** — 建議觀望"

        if short and short.get('decision') in ('BUY_BREAKOUT', 'BUY_PULLBACK'):
            return "**初升段** — 短線信號積極，技術面轉強"
        if mid and mid.get('decision') == 'AVOID':
            return "**修正段** — 中線偏空，謹慎操作"

        return "**不明** — 資料不足，無法判斷生命週期"

    def save(self, report_text, output_dir, filename=None):
        """
        Save the report to a file.

        Parameters
        ----------
        report_text : str
            Report Markdown content.
        output_dir : str
            Directory to save the file.
        filename : str, optional
            Filename. Defaults to stock_report_{timestamp}.md
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            if not filename:
                ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"stock_report_{ts}.md"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_text)
            logger.info("Report saved to %s", filepath)
            return filepath
        except Exception as exc:
            logger.error("Failed to save report: %s", exc)
            return None
