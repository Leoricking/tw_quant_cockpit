# reports/crash_reversal_strategy_report.py
# TW Quant Cockpit — Crash Reversal & Risk Discipline Strategy Report
# v0.9.0.1 — Research Only / No Real Orders / Production Trading BLOCKED
#
# DISCLAIMER: This report is for research and educational purposes ONLY.
# It does NOT issue, suggest, or authorise any real trading orders.
# NOT investment advice. Production trading is BLOCKED.

from __future__ import annotations

import os
from datetime import date

VERSION = "v0.9.0.1"

# ---------------------------------------------------------------------------
# Inline safety guard — report must never emit forbidden action strings as
# actionable output text.  We substitute them during rendering.
# ---------------------------------------------------------------------------
_FORBIDDEN_RENDER = frozenset([
    "BUY", "SELL", "ORDER", "EXECUTE",
    "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE",
])


def _safe_render(value: str, default: str = "REVIEW") -> str:
    if str(value).upper() in _FORBIDDEN_RENDER:
        return default
    return str(value)


def _bool_icon(val) -> str:
    return "✔" if val else "✘"


def _fmt_list(items) -> str:
    if not items:
        return "—"
    if isinstance(items, list):
        return "; ".join(str(x) for x in items if x)
    return str(items)


class CrashReversalStrategyReportBuilder:
    """
    Build a markdown strategy report from CrashReversalStrategyPack results.

    RESEARCH ONLY — No Real Orders — Production Trading BLOCKED — Not Investment Advice
    """

    read_only = True
    no_real_orders = True
    production_blocked = True

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(self, pack_result: dict, mode: str = "real") -> str:
        """
        Build a markdown report from CrashReversalStrategyPack.evaluate_market()
        combined with one or more evaluate_symbol() results.

        pack_result structure (all keys optional — graceful fallback):
        {
            "crash_cause":      dict,   # from evaluate_market()
            "stabilization":    dict,   # from evaluate_market()
            "symbols":          list,   # list of evaluate_symbol() dicts  (optional)
            "no_real_orders":   True,
            "production_blocked": True,
        }

        Returns the absolute file path that was written.
        """
        try:
            if not isinstance(pack_result, dict):
                pack_result = {}

            try:
                os.makedirs(self.output_dir, exist_ok=True)
            except Exception:
                pass

            md = self._build_markdown(pack_result, mode)
            filepath = self._report_filename()
            try:
                with open(filepath, "w", encoding="utf-8") as fh:
                    fh.write(md)
            except Exception as write_err:
                return f"ERROR: Could not write report — {write_err}"
            return filepath
        except Exception as e:
            return f"ERROR: build() failed — {e}"

    # ------------------------------------------------------------------
    # Filename
    # ------------------------------------------------------------------

    def _report_filename(self) -> str:
        today = date.today().isoformat()
        return os.path.join(self.output_dir, f"crash_reversal_strategy_report_{today}.md")

    # ------------------------------------------------------------------
    # Markdown assembly
    # ------------------------------------------------------------------

    def _build_markdown(self, pack_result: dict, mode: str) -> str:
        """
        Build the full markdown content with all 9 sections.
        Never raises — returns an error-section string if anything fails.
        """
        try:
            lines: list[str] = []

            # ── Header ──────────────────────────────────────────────────────
            lines.append("# TW Quant Cockpit — Crash Reversal & Risk Discipline Strategy Report")
            lines.append(f"**Version:** {VERSION}  |  **Date:** {date.today().isoformat()}  |  **Mode:** {mode}")
            lines.append("")
            lines.append(
                "> **RESEARCH ONLY — No Real Orders — Production Trading BLOCKED — Not Investment Advice**"
            )
            lines.append("")
            lines.append("---")
            lines.append("")

            # ── 一. 總覽 ────────────────────────────────────────────────────
            lines.extend(self._section_overview(pack_result))

            # ── 二. 大跌原因分類 ─────────────────────────────────────────────
            lines.extend(self._section_crash_cause(pack_result.get("crash_cause", {})))

            # ── 三. 大跌後止穩檢查 ──────────────────────────────────────────
            lines.extend(self._section_stabilization(pack_result.get("stabilization", {})))

            # ── Symbol sections (四–七) ─────────────────────────────────────
            symbols_list = pack_result.get("symbols", [])
            if not isinstance(symbols_list, list):
                symbols_list = []

            if symbols_list:
                for sym_result in symbols_list:
                    if not isinstance(sym_result, dict):
                        continue
                    sym = sym_result.get("symbol", "UNKNOWN")

                    # ── 四. 抗跌股分數 ───────────────────────────────────────
                    lines.extend(self._section_relative_strength(
                        sym, sym_result.get("relative_strength", {})
                    ))

                    # ── 五. EPS 背書低接條件 ─────────────────────────────────
                    lines.extend(self._section_sakata(
                        sym, sym_result.get("sakata_dip_buy", {})
                    ))

                    # ── 六. 均線停利紀律 ─────────────────────────────────────
                    lines.extend(self._section_ma_discipline(
                        sym, sym_result.get("ma_discipline", {})
                    ))

                    # ── 七. 高風險產業限制 ───────────────────────────────────
                    lines.extend(self._section_industry_guard(
                        sym, sym_result.get("industry_guard", {})
                    ))
            else:
                lines.append("## 四–七. 個股評估")
                lines.append("")
                lines.append("_No symbol-level results provided in this report._")
                lines.append("")

            # ── 八. 整合到 Strategy Lab ─────────────────────────────────────
            lines.extend(self._section_strategy_lab_integration())

            # ── 九. 安全聲明 ─────────────────────────────────────────────────
            lines.extend(self._section_safety_disclaimer())

            return "\n".join(lines)
        except Exception as e:
            return (
                f"# Report Build Error\n\n"
                f"_build_markdown() encountered an exception: {e}_\n\n"
                f"> **RESEARCH ONLY — No Real Orders — Production Trading BLOCKED — Not Investment Advice**\n"
            )

    # ------------------------------------------------------------------
    # Section builders
    # ------------------------------------------------------------------

    def _section_overview(self, pack_result: dict) -> list[str]:
        lines: list[str] = []
        lines.append("## 一、總覽 (Overview)")
        lines.append("")

        if not pack_result:
            lines.append("| Field | Value |")
            lines.append("|-------|-------|")
            lines.append(f"| Version | {VERSION} |")
            lines.append("| Research Only | Yes |")
            lines.append("| No Real Orders | Yes |")
            lines.append("| Production Trading | BLOCKED |")
            lines.append("| Investment Advice | No |")
            lines.append("| Overall Status | **INSUFFICIENT_DATA** |")
            lines.append("")
            lines.append(
                "> No data was provided. All sections will show defaults or empty values."
            )
            lines.append("")
            return lines

        crash_cause   = pack_result.get("crash_cause", {})
        stabilization = pack_result.get("stabilization", {})
        symbols_list  = pack_result.get("symbols", [])

        cause_type  = crash_cause.get("cause_type", "UNKNOWN") if crash_cause else "UNKNOWN"
        risk_level  = crash_cause.get("risk_level", "UNKNOWN") if crash_cause else "UNKNOWN"
        stab_status = stabilization.get("status", "UNKNOWN") if stabilization else "UNKNOWN"
        stab_score  = stabilization.get("stabilization_score", 0.0) if stabilization else 0.0
        sym_count   = len(symbols_list) if isinstance(symbols_list, list) else 0

        lines.append("| Field | Value |")
        lines.append("|-------|-------|")
        lines.append(f"| Version | {VERSION} |")
        lines.append("| Research Only | Yes |")
        lines.append("| No Real Orders | **Yes — BLOCKED** |")
        lines.append("| Production Trading | **BLOCKED** |")
        lines.append("| Investment Advice | No |")
        lines.append(f"| Crash Cause Type | {_safe_render(cause_type)} |")
        lines.append(f"| Risk Level | {_safe_render(risk_level)} |")
        lines.append(f"| Stabilization Status | {_safe_render(stab_status)} |")
        lines.append(f"| Stabilization Score | {stab_score} / 100 |")
        lines.append(f"| Symbols Evaluated | {sym_count} |")
        lines.append("")
        return lines

    def _section_crash_cause(self, crash_cause: dict) -> list[str]:
        lines: list[str] = []
        lines.append("## 二、大跌原因分類 (Crash Cause Classification)")
        lines.append("")

        if not crash_cause:
            lines.append("_No crash cause data provided._")
            lines.append("")
            return lines

        cause_type  = _safe_render(crash_cause.get("cause_type",  "UNKNOWN"))
        score       = crash_cause.get("score", 0.0)
        risk_level  = _safe_render(crash_cause.get("risk_level",  "UNKNOWN"))
        action_hint = _safe_render(crash_cause.get("action_hint", "REVIEW"))
        evidence    = crash_cause.get("evidence", [])

        lines.append("| Field | Value |")
        lines.append("|-------|-------|")
        lines.append(f"| Cause Type | **{cause_type}** |")
        lines.append(f"| Confidence Score | {score} / 100 |")
        lines.append(f"| Risk Level | **{risk_level}** |")
        lines.append(f"| Research Action Hint | {action_hint} |")
        lines.append(f"| Evidence | {_fmt_list(evidence)} |")
        lines.append("")

        # Interpretation note
        lines.append("### Cause Type Descriptions")
        lines.append("")
        lines.append("| Cause | Description |")
        lines.append("|-------|-------------|")
        lines.append("| FUNDAMENTAL_BREAKDOWN | Revenue/EPS deterioration, margin compression, demand invalidation |")
        lines.append("| FINANCIAL_DELEVERAGING | Forced margin calls, leverage unwind, panic selling despite intact fundamentals |")
        lines.append("| TECHNICAL_OVERHEAT_CORRECTION | Overextension correction — high RSI/KD, far above MA20, profit-taking |")
        lines.append("| SYSTEMIC_CRISIS | Liquidity crisis, credit event, war, VIX spike extreme, global risk-off |")
        lines.append("| UNKNOWN | Insufficient signal data |")
        lines.append("")
        return lines

    def _section_stabilization(self, stabilization: dict) -> list[str]:
        lines: list[str] = []
        lines.append("## 三、大跌後止穩檢查 (Post-Crash Stabilization Checklist)")
        lines.append("")

        if not stabilization:
            lines.append("_No stabilization data provided._")
            lines.append("")
            return lines

        stab_score  = stabilization.get("stabilization_score", 0.0)
        status      = _safe_render(stabilization.get("status", "UNKNOWN"))
        passed_count = stabilization.get("passed_count", 0)
        total_count  = stabilization.get("total_count", 0)
        action_hint  = _safe_render(stabilization.get("action_hint", "WAIT"))
        signals      = stabilization.get("signals", [])

        lines.append(f"**Score:** {stab_score} / 100  |  "
                     f"**Status:** {status}  |  "
                     f"**Passed:** {passed_count}/{total_count}  |  "
                     f"**Research Action:** {action_hint}")
        lines.append("")

        if signals:
            lines.append("| # | Item | Passed | Score | Weight | Evidence |")
            lines.append("|---|------|--------|-------|--------|----------|")
            for i, sig in enumerate(signals, 1):
                if not isinstance(sig, dict):
                    continue
                item     = sig.get("item", "")
                passed   = sig.get("passed", False)
                sig_score = sig.get("score", 0.0)
                weight   = sig.get("weight", 0.0)
                evidence = sig.get("evidence", "")
                lines.append(
                    f"| {i} | {item} | {_bool_icon(passed)} | {sig_score} | {weight} | {evidence} |"
                )
            lines.append("")

        lines.append("### Status Thresholds")
        lines.append("")
        lines.append("| Score Range | Status | Research Action |")
        lines.append("|-------------|--------|-----------------|")
        lines.append("| 80–100 | HIGH_QUALITY_DIP | BUILD_WATCHLIST |")
        lines.append("| 60–79  | STABILIZING      | WATCH |")
        lines.append("| 40–59  | FIRST_REBOUND_ONLY | WAIT |")
        lines.append("| 0–39   | NOT_STABILIZED   | WAIT |")
        lines.append("")
        return lines

    def _section_relative_strength(self, symbol: str, rs: dict) -> list[str]:
        lines: list[str] = []
        lines.append(f"## 四、抗跌股分數 — {symbol} (Relative Strength After Crash)")
        lines.append("")

        if not rs:
            lines.append("_No relative strength data provided._")
            lines.append("")
            return lines

        score         = rs.get("score", 0.0)
        rating        = _safe_render(rs.get("rating", "UNKNOWN"))
        forbidden_trap = rs.get("forbidden_trap", False)
        conditions    = rs.get("conditions", [])
        evidence      = rs.get("evidence", [])

        lines.append("| Field | Value |")
        lines.append("|-------|-------|")
        lines.append(f"| Symbol | {symbol} |")
        lines.append(f"| Score | {score} / 100 |")
        lines.append(f"| Rating | **{rating}** |")
        lines.append(f"| Forbidden Trap | {'**YES — CAUTION**' if forbidden_trap else 'No'} |")
        lines.append(f"| Conditions Met | {_fmt_list(conditions)} |")
        lines.append(f"| Evidence | {_fmt_list(evidence)} |")
        lines.append("")

        lines.append("| Score Range | Rating |")
        lines.append("|-------------|--------|")
        lines.append("| 80–100 | HIGH_RELATIVE_STRENGTH |")
        lines.append("| 60–79  | WATCHLIST_CANDIDATE |")
        lines.append("| 40–59  | NORMAL |")
        lines.append("| 0–39   | WEAK |")
        lines.append("> If forbidden trap is triggered, rating is capped at NORMAL.")
        lines.append("")
        return lines

    def _section_sakata(self, symbol: str, sakata: dict) -> list[str]:
        lines: list[str] = []
        lines.append(f"## 五、EPS 背書低接條件 — {symbol} (Sakata Dip-Buy Eligibility)")
        lines.append("")

        if not sakata:
            lines.append("_No Sakata dip-buy data provided._")
            lines.append("")
            return lines

        eligible        = sakata.get("eligible", False)
        score           = sakata.get("score", 0.0)
        next_safe_action = _safe_render(sakata.get("next_safe_action", "WAIT"))
        eps_supported   = sakata.get("eps_supported", False)
        rev_supported   = sakata.get("revenue_supported", False)
        low_pos         = sakata.get("low_position", False)
        tech_turning    = sakata.get("technical_turning", False)
        chip_not_broken = sakata.get("chip_not_broken", False)
        forbidden_reason = sakata.get("forbidden_reason", [])
        allowed_reason  = sakata.get("allowed_reason", [])

        lines.append("| Field | Value |")
        lines.append("|-------|-------|")
        lines.append(f"| Symbol | {symbol} |")
        lines.append(f"| Eligible | {'**YES**' if eligible else 'No'} |")
        lines.append(f"| Score | {score} / 100 |")
        lines.append(f"| Research Next Action | {next_safe_action} |")
        lines.append(f"| EPS Supported | {_bool_icon(eps_supported)} |")
        lines.append(f"| Revenue Supported | {_bool_icon(rev_supported)} |")
        lines.append(f"| Low Price Position | {_bool_icon(low_pos)} |")
        lines.append(f"| Technical Turning | {_bool_icon(tech_turning)} |")
        lines.append(f"| Chip Not Broken | {_bool_icon(chip_not_broken)} |")
        lines.append(f"| Forbidden Reasons | {_fmt_list(forbidden_reason) if forbidden_reason else '—'} |")
        lines.append(f"| Supporting Reasons | {_fmt_list(allowed_reason) if allowed_reason else '—'} |")
        lines.append("")
        lines.append("> Eligible = Score ≥ 70 AND zero forbidden reasons. Research only — NOT a buy signal.")
        lines.append("")
        return lines

    def _section_ma_discipline(self, symbol: str, ma: dict) -> list[str]:
        lines: list[str] = []
        lines.append(f"## 六、均線停利紀律 — {symbol} (Moving Average Profit Discipline)")
        lines.append("")

        if not ma:
            lines.append("_No MA discipline data provided._")
            lines.append("")
            return lines

        trend_status  = _safe_render(ma.get("trend_status", "UNKNOWN"))
        action_hint   = _safe_render(ma.get("action_hint", "HOLD_REVIEW"))
        ma5           = ma.get("ma5_status", "UNKNOWN")
        ma10          = ma.get("ma10_status", "UNKNOWN")
        ma20          = ma.get("ma20_status", "UNKNOWN")
        ma60          = ma.get("ma60_status", "UNKNOWN")
        reclaim_rule  = ma.get("reclaim_rule", "")
        evidence      = ma.get("evidence", [])

        lines.append("| Field | Value |")
        lines.append("|-------|-------|")
        lines.append(f"| Symbol | {symbol} |")
        lines.append(f"| Trend Status | **{trend_status}** |")
        lines.append(f"| Research Action | {action_hint} |")
        lines.append(f"| MA5 | {ma5} |")
        lines.append(f"| MA10 | {ma10} |")
        lines.append(f"| MA20 | {ma20} |")
        lines.append(f"| MA60 | {ma60} |")
        lines.append(f"| Reclaim Rule | {reclaim_rule if reclaim_rule else '—'} |")
        lines.append(f"| Evidence | {_fmt_list(evidence)} |")
        lines.append("")

        lines.append("| Status | Meaning | Research Action |")
        lines.append("|--------|---------|-----------------|")
        lines.append("| TREND_HEALTHY | Above MA5/MA10/MA20 | HOLD_REVIEW |")
        lines.append("| WASHOUT | Broke then reclaimed MA20 within 3 days | HOLD_REVIEW |")
        lines.append("| MA20_WARNING | Below MA20 > 3 days no reclaim | REDUCE_RISK_REVIEW |")
        lines.append("| MA60_TREND_BREAK | Broke MA60 with volume | REDUCE_RISK_REVIEW |")
        lines.append("| RECOVERY_WATCH | Reclaimed MA20 within 3d, above MA60 | REVIEW_REENTRY |")
        lines.append("")
        return lines

    def _section_industry_guard(self, symbol: str, guard: dict) -> list[str]:
        lines: list[str] = []
        lines.append(f"## 七、高風險產業限制 — {symbol} (High-Risk Industry Guard)")
        lines.append("")

        if not guard:
            lines.append("_No industry guard data provided._")
            lines.append("")
            return lines

        industry           = guard.get("industry", "UNKNOWN")
        risk_multiplier    = guard.get("risk_multiplier", 1.0)
        max_pos_hint       = guard.get("max_position_hint", "N/A")
        core_allowed       = guard.get("core_holding_allowed", True)
        financing_allowed  = guard.get("financing_allowed", True)
        hard_stop          = guard.get("hard_stop_required", False)
        warning            = guard.get("warning", "")

        is_high_risk = risk_multiplier > 1.0

        lines.append("| Field | Value |")
        lines.append("|-------|-------|")
        lines.append(f"| Symbol | {symbol} |")
        lines.append(f"| Industry | {industry} |")
        lines.append(f"| High Risk | {'**YES**' if is_high_risk else 'No'} |")
        lines.append(f"| Risk Multiplier | {risk_multiplier}x |")
        lines.append(f"| Max Position Hint | {max_pos_hint} |")
        lines.append(f"| Core Holding Allowed | {_bool_icon(core_allowed)} |")
        lines.append(f"| Financing Allowed | {_bool_icon(financing_allowed)} |")
        lines.append(f"| Hard Stop Required | {'**Yes**' if hard_stop else 'No'} |")
        if warning:
            lines.append(f"| Warning | {warning} |")
        lines.append("")

        if is_high_risk:
            lines.append(
                "> **High-risk industry detected.** Position sizing must be limited. "
                "Core holding and financing are NOT advised. "
                "Hard stop-loss discipline required. Research only — NOT trading advice."
            )
        else:
            lines.append("> Industry classified as standard risk. Normal research review applies.")
        lines.append("")
        return lines

    def _section_strategy_lab_integration(self) -> list[str]:
        lines: list[str] = []
        lines.append("## 八、整合到 Strategy Lab (Strategy Lab Integration)")
        lines.append("")
        lines.append(
            "This strategy pack is designed to integrate with the TW Quant Cockpit Strategy Lab. "
            "Use the `CrashReversalStrategyPack` class from `strategy_rules.crash_reversal_pack` "
            "to produce structured evaluation results, then pass them to this report builder."
        )
        lines.append("")
        lines.append("**Integration checklist (research workflow only):**")
        lines.append("")
        lines.append("- [ ] Populate `market_context` dict with current market signals")
        lines.append("- [ ] Call `pack.evaluate_market(market_context)` for macro view")
        lines.append("- [ ] For each candidate symbol, call `pack.evaluate_symbol(symbol, stock_context, market_context)`")
        lines.append("- [ ] Combine results into a `pack_result` dict with keys: `crash_cause`, `stabilization`, `symbols`")
        lines.append("- [ ] Pass to `CrashReversalStrategyReportBuilder().build(pack_result)` to generate this report")
        lines.append("- [ ] Review report — research / watchlist building only, no orders")
        lines.append("")
        lines.append("**Note:** All outputs are research signals. No automated order routing is connected.")
        lines.append("")
        return lines

    def _section_safety_disclaimer(self) -> list[str]:
        lines: list[str] = []
        lines.append("## 九、安全聲明 (Safety Disclaimer)")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(
            "**RESEARCH ONLY — No Real Orders — Production Trading BLOCKED — Not Investment Advice**"
        )
        lines.append("")
        lines.append(
            "This report and the underlying strategy pack (`strategy_rules.crash_reversal_pack`) "
            "are provided for **research, education, and backtesting purposes only**."
        )
        lines.append("")
        lines.append("- No signals, scores, ratings, or action hints in this report constitute a trading order.")
        lines.append("- The flags `no_real_orders=True` and `production_blocked=True` are set on all outputs.")
        lines.append("- Forbidden trading actions (BUY / SELL / ORDER / EXECUTE / SUBMIT_ORDER / AUTO_TRADE / REAL_TRADE) are never emitted as actionable outputs.")
        lines.append("- Past performance of any pattern does not guarantee future results.")
        lines.append("- Always perform independent due diligence and consult a qualified financial adviser.")
        lines.append("")
        lines.append(f"*Report generated: {date.today().isoformat()} — TW Quant Cockpit {VERSION}*")
        lines.append("")
        return lines
