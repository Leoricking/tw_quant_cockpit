"""
reports/generator.py - Daily report text generator.

Produces a formatted text report with:
- Date, market regime, selected strategy
- Top stock picks with score, predicted return, stop-loss, target price,
  and position size
- Portfolio performance summary (if backtest data is available)
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Main report function
# ---------------------------------------------------------------------------

def generate_daily_report(
    date: str,
    regime: str,
    vol_regime: str,
    strategy_name: str,
    picks: pd.DataFrame,
    backtest_metrics: Optional[dict] = None,
    regime_info: Optional[dict] = None,
    previous_picks: Optional[pd.DataFrame] = None,
) -> str:
    """
    Generate a formatted daily research report.

    Parameters
    ----------
    date : str
        Report date (YYYY-MM-DD).
    regime : str
        Market price regime ("bull", "bear", "sideways", "unknown").
    vol_regime : str
        Volatility regime ("high", "low").
    strategy_name : str
        Name of the selected strategy.
    picks : pd.DataFrame
        Top stock picks with metrics.  May include columns:
        microstructure_score, vp_support_score, vp_pressure_score,
        no_chase_reason, fake_breakout_risk, opening_return_15m,
        buy_sell_pressure.
    backtest_metrics : dict, optional
        Latest backtest performance metrics to include in the report.
    regime_info : dict, optional
        Additional regime details (bull_pct, bear_pct, etc.).
    previous_picks : pd.DataFrame, optional
        Yesterday's picks (same schema as picks) used to generate a
        model review (看對/看錯) section.

    Returns
    -------
    str
        Formatted report text.
    """
    lines = []

    # ---- Header ----------------------------------------------------------
    lines.append("=" * 70)
    lines.append("  TAIWAN QUANTITATIVE TRADING PLATFORM – DAILY REPORT")
    lines.append("=" * 70)
    lines.append(f"  Date        : {date}")
    lines.append(f"  Generated   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # ---- Market regime ---------------------------------------------------
    lines.append("-" * 70)
    lines.append("  MARKET REGIME")
    lines.append("-" * 70)

    regime_emoji = {"bull": "[BULL]", "bear": "[BEAR]", "sideways": "[SIDE]"}.get(regime, "[UNKN]")
    vol_label = "HIGH Volatility" if vol_regime == "high" else "LOW Volatility"
    lines.append(f"  Price Regime     : {regime_emoji} {regime.upper()}")
    lines.append(f"  Volatility Regime: {vol_label}")

    if regime_info:
        bull_pct = regime_info.get("bull_pct", 0) * 100
        bear_pct = regime_info.get("bear_pct", 0) * 100
        side_pct = max(0, 100 - bull_pct - bear_pct)
        lines.append(
            f"  Stock Distribution: {bull_pct:.0f}% Bull | "
            f"{bear_pct:.0f}% Bear | {side_pct:.0f}% Sideways"
        )

    lines.append("")

    # ---- Strategy --------------------------------------------------------
    lines.append("-" * 70)
    lines.append("  SELECTED STRATEGY")
    lines.append("-" * 70)

    strategy_descriptions = {
        "momentum": "Momentum – Buy top-N ranked stocks by composite momentum score",
        "mean_reversion": "Mean Reversion – Buy oversold stocks (RSI<30, below BB lower band)",
        "breakout": "Breakout – Buy on 20-day high breakout with volume confirmation",
    }
    desc = strategy_descriptions.get(strategy_name, strategy_name)
    lines.append(f"  {desc}")
    lines.append("")

    # ---- Stock picks -----------------------------------------------------
    lines.append("-" * 70)
    lines.append("  TOP STOCK PICKS")
    lines.append("-" * 70)

    if picks.empty:
        lines.append("  No stock picks available for this date.")
    else:
        # Table header
        header = (
            f"  {'#':>3} {'StockID':>8} {'Score':>7} {'PredRet':>8} "
            f"{'UpProb':>7} {'Close':>8} {'Stop':>8} {'Target':>8} {'Pos%':>5}"
        )
        lines.append(header)
        lines.append("  " + "-" * 67)

        for rank, (_, row) in enumerate(picks.iterrows(), start=1):
            sid = str(row.get("stock_id", "N/A"))
            score = row.get("composite_score", float("nan"))
            pred_ret = row.get("predicted_return", float("nan"))
            up_prob = row.get("up_probability", float("nan"))
            close = row.get("close", float("nan"))
            stop = row.get("stop_loss_price", float("nan"))
            target = row.get("target_price", float("nan"))
            pos_pct = row.get("position_size_pct", float("nan"))

            score_str = f"{score:.3f}" if not pd.isna(score) else "  N/A"
            pred_str = f"{pred_ret:+.2%}" if not pd.isna(pred_ret) else "   N/A"
            prob_str = f"{up_prob:.1%}" if not pd.isna(up_prob) else "  N/A"
            close_str = f"{close:.2f}" if not pd.isna(close) else "   N/A"
            stop_str = f"{stop:.2f}" if not pd.isna(stop) else "   N/A"
            target_str = f"{target:.2f}" if not pd.isna(target) else "   N/A"
            pos_str = f"{pos_pct:.1f}%" if not pd.isna(pos_pct) else " N/A"

            lines.append(
                f"  {rank:>3} {sid:>8} {score_str:>7} {pred_str:>8} "
                f"{prob_str:>7} {close_str:>8} {stop_str:>8} {target_str:>8} {pos_str:>5}"
            )

            # Optional additional info
            regime_stock = row.get("regime", "")
            rsi_val = row.get("rsi_14", float("nan"))
            notes = []
            if regime_stock:
                notes.append(f"Regime:{regime_stock}")
            if not pd.isna(rsi_val):
                notes.append(f"RSI:{rsi_val:.0f}")
            if notes:
                lines.append(f"       ({' | '.join(notes)})")

        lines.append("")

        # Summary statistics
        if "predicted_return" in picks.columns:
            avg_pred_ret = picks["predicted_return"].mean()
            avg_up_prob = picks.get("up_probability", pd.Series([float("nan")])).mean()
            lines.append(
                f"  Avg Predicted Return : {avg_pred_ret:+.2%}"
                f"   Avg Up Probability: {avg_up_prob:.1%}"
            )

    lines.append("")

    # ---- Volume Profile Support / Resistance (if available) ---------------
    has_vp = not picks.empty and "vp_support_score" in picks.columns
    if has_vp:
        lines.append("-" * 70)
        lines.append("  VOLUME PROFILE – SUPPORT / PRESSURE (分價量支撐壓力)")
        lines.append("-" * 70)
        vp_header = (
            f"  {'StockID':>8} {'SupportScore':>13} {'PressureScore':>14} "
            f"{'NetScore':>9} {'DistToPeak':>11} {'InValueArea':>12}"
        )
        lines.append(vp_header)
        lines.append("  " + "-" * 67)
        for _, row in picks.head(15).iterrows():
            sid = str(row.get("stock_id", "N/A"))
            sup = row.get("vp_support_score", float("nan"))
            pres = row.get("vp_pressure_score", float("nan"))
            net = row.get("support_pressure_score", float("nan"))
            dist = row.get("vp_distance_to_peak", float("nan"))
            in_va = row.get("vp_price_in_value_area", float("nan"))

            def _fv(v, fmt=".3f"):
                return format(v, fmt) if not pd.isna(v) else "  N/A"

            in_va_str = "Yes" if in_va == 1.0 else ("No" if in_va == 0.0 else " N/A")
            lines.append(
                f"  {sid:>8} {_fv(sup):>13} {_fv(pres):>14} "
                f"{_fv(net):>9} {_fv(dist, '+.2%'):>11} {in_va_str:>12}"
            )
        lines.append("")

    # ---- Opening 15-minute Microstructure (if available) ------------------
    has_ms = not picks.empty and "microstructure_score" in picks.columns
    if has_ms:
        lines.append("-" * 70)
        lines.append("  OPENING 15-MIN MARKET STRENGTH (開盤 15 分鐘盤口強弱)")
        lines.append("-" * 70)
        ms_header = (
            f"  {'StockID':>8} {'MSScore':>8} {'BuySellPres':>12} "
            f"{'Open15mRet':>11} {'VolRatio':>9} {'HiBreak':>8} {'LoBreak':>8}"
        )
        lines.append(ms_header)
        lines.append("  " + "-" * 67)
        for _, row in picks.head(15).iterrows():
            sid = str(row.get("stock_id", "N/A"))
            mss = row.get("microstructure_score", float("nan"))
            bsp = row.get("buy_sell_pressure", float("nan"))
            o15 = row.get("opening_return_15m", float("nan"))
            ovr = row.get("opening_volume_ratio", float("nan"))
            hib = row.get("opening_high_break", float("nan"))
            lob = row.get("opening_low_break", float("nan"))

            def _fv2(v, fmt=".3f"):
                return format(v, fmt) if not (isinstance(v, float) and pd.isna(v)) else "  N/A"

            hib_str = "Yes" if hib == 1.0 else ("No" if hib == 0.0 else "N/A")
            lob_str = "Yes" if lob == 1.0 else ("No" if lob == 0.0 else "N/A")
            lines.append(
                f"  {sid:>8} {_fv2(mss):>8} {_fv2(bsp):>12} "
                f"{_fv2(o15, '+.2%'):>11} {_fv2(ovr):>9} {hib_str:>8} {lob_str:>8}"
            )
        lines.append("")

    # ---- Model recommendation reasons & no-chase warnings ----------------
    has_reasons = not picks.empty and (
        "no_chase_reason" in picks.columns or "fake_breakout_risk" in picks.columns
    )
    if has_reasons:
        lines.append("-" * 70)
        lines.append("  MODEL RECOMMENDATION REASONS & WARNINGS (推薦理由 / 風險提示)")
        lines.append("-" * 70)
        for _, row in picks.head(15).iterrows():
            sid = str(row.get("stock_id", "N/A"))
            pred_ret = row.get("predicted_return", float("nan"))
            up_prob = row.get("up_probability", float("nan"))
            no_chase = row.get("no_chase_reason", None)
            fake_risk = row.get("fake_breakout_risk", False)
            chase_adj = row.get("chase_score_adj", 1.0)

            pred_str = f"{pred_ret:+.2%}" if not pd.isna(pred_ret) else "N/A"
            prob_str = f"{up_prob:.1%}" if not pd.isna(up_prob) else "N/A"

            lines.append(f"  [{sid}]  預測報酬: {pred_str}  上漲機率: {prob_str}")

            # Model rationale
            rationale_parts = []
            rsi_val = row.get("rsi_14", float("nan"))
            macd_hist = row.get("macd_hist", float("nan"))
            bb_pos = row.get("bb_position", float("nan"))
            mom_score = row.get("momentum_score", float("nan"))

            if not pd.isna(rsi_val):
                if rsi_val < 35:
                    rationale_parts.append(f"RSI 超賣 ({rsi_val:.0f})")
                elif rsi_val > 65:
                    rationale_parts.append(f"RSI 強勢 ({rsi_val:.0f})")
            if not pd.isna(macd_hist) and macd_hist > 0:
                rationale_parts.append("MACD 柱狀體翻正")
            if not pd.isna(bb_pos):
                if bb_pos < 0.2:
                    rationale_parts.append("價格接近布林下軌")
                elif bb_pos > 0.8:
                    rationale_parts.append("價格接近布林上軌")
            if not pd.isna(mom_score) and mom_score > 0:
                rationale_parts.append(f"動能分數 +{mom_score:.3f}")

            if rationale_parts:
                lines.append(f"       推薦理由: {' | '.join(rationale_parts)}")

            # No-chase warnings
            if no_chase:
                lines.append(f"       不建議追價: {no_chase}")
            if fake_risk:
                lines.append("       ⚠ 假突破風險: 開盤高走低，量能不足，注意回測支撐")
            if not pd.isna(chase_adj) and chase_adj < 0.85:
                lines.append(f"       綜合評分已下調 {(1-chase_adj):.0%} (風控調整)")

        lines.append("")

    # ---- Phase 2 Strategy Knowledge Engine summary (if available) --------
    _has_phase2 = not picks.empty and any(
        col in picks.columns
        for col in ("phase2_strategy_reason", "rebound_warning",
                    "squeeze_signal", "sector_linkage_reason", "fundamental_warning")
    )
    if _has_phase2:
        lines.append("-" * 70)
        lines.append("  STRATEGY KNOWLEDGE ENGINE — PHASE 2 SIGNALS")
        lines.append("-" * 70)
        for _, row in picks.head(10).iterrows():
            sid = str(row.get("stock_id", "N/A"))
            p2r  = row.get("phase2_strategy_reason")
            rbw  = row.get("rebound_warning")
            sqz  = row.get("squeeze_signal")
            slr  = row.get("sector_linkage_reason")
            fuw  = row.get("fundamental_warning")

            def _nv(v):
                return None if (v is None or (isinstance(v, float) and pd.isna(v)) or v == '') else str(v)

            p2r = _nv(p2r); rbw = _nv(rbw); sqz = _nv(sqz); slr = _nv(slr); fuw = _nv(fuw)
            if not any([p2r, rbw, sqz, slr, fuw]):
                continue
            lines.append(f"  [{sid}]")
            if p2r:
                lines.append(f"    KD / Phase2 : {p2r}")
            if sqz and sqz not in ("WATCH", "UNAVAILABLE"):
                lines.append(f"    融券訊號    : {sqz}")
            if rbw:
                lines.append(f"    破底翻警示  : {rbw}")
            if slr:
                lines.append(f"    族群聯動    : {slr}")
            if fuw:
                lines.append(f"    財報警示    : {fuw}")
        lines.append("")

    # ---- Model review (看對/看錯復盤) ------------------------------------
    if previous_picks is not None and not previous_picks.empty and not picks.empty:
        lines.append("-" * 70)
        lines.append("  MODEL REVIEW – YESTERDAY'S PICKS (昨日推薦復盤)")
        lines.append("-" * 70)
        lines.append(
            f"  {'StockID':>8} {'PredRet':>8} {'ActualRet':>10} {'Result':>8} {'UpProb':>7}"
        )
        lines.append("  " + "-" * 50)

        # previous_picks should have actual_return if pipeline enriched it
        for _, row in previous_picks.head(15).iterrows():
            sid = str(row.get("stock_id", "N/A"))
            pred = row.get("predicted_return", float("nan"))
            actual = row.get("actual_return", float("nan"))
            up_prob = row.get("up_probability", float("nan"))

            pred_str = f"{pred:+.2%}" if not pd.isna(pred) else "   N/A"
            actual_str = f"{actual:+.2%}" if not pd.isna(actual) else "   N/A"

            if not pd.isna(pred) and not pd.isna(actual):
                # "Correct" if model predicted direction matches actual direction
                correct_dir = (pred > 0 and actual > 0) or (pred < 0 and actual < 0)
                result = " PASS" if correct_dir else " FAIL"
            else:
                result = "  N/A"

            prob_str = f"{up_prob:.1%}" if not pd.isna(up_prob) else "  N/A"
            lines.append(
                f"  {sid:>8} {pred_str:>8} {actual_str:>10} {result:>8} {prob_str:>7}"
            )
        lines.append("")

    # ---- Backtest performance (if available) ----------------------------
    if backtest_metrics:
        lines.append("-" * 70)
        lines.append("  BACKTEST PERFORMANCE SUMMARY")
        lines.append("-" * 70)

        sharpe = backtest_metrics.get("sharpe_ratio", float("nan"))
        max_dd = backtest_metrics.get("max_drawdown", float("nan"))
        pf = backtest_metrics.get("profit_factor", float("nan"))
        total_ret = backtest_metrics.get("total_return", float("nan"))
        win_rate = backtest_metrics.get("win_rate", float("nan"))
        n_trades = backtest_metrics.get("n_trades", 0)

        def _fmt(v, fmt=".3f", fallback="N/A"):
            return format(v, fmt) if not (isinstance(v, float) and np.isnan(v)) else fallback

        lines.append(f"  Sharpe Ratio     : {_fmt(sharpe)}")
        lines.append(f"  Max Drawdown     : {_fmt(max_dd, '.2%')}")
        lines.append(f"  Profit Factor    : {_fmt(pf)}")
        lines.append(f"  Total Return     : {_fmt(total_ret, '+.2%')}")
        lines.append(f"  Win Rate         : {_fmt(win_rate, '.1%')}")
        lines.append(f"  Number of Trades : {n_trades}")

        # KPI target check
        lines.append("")
        lines.append("  KPI Target Assessment:")
        targets = [
            ("Sharpe Ratio > 1.5", sharpe, 1.5, ">="),
            ("Max Drawdown < 20%", max_dd, 0.20, "<="),
            ("Profit Factor > 1.5", pf, 1.5, ">="),
        ]
        for label, val, threshold, op in targets:
            if isinstance(val, float) and np.isnan(val):
                status = "  N/A"
            elif op == ">=" and val >= threshold:
                status = " PASS"
            elif op == "<=" and val <= threshold:
                status = " PASS"
            else:
                status = " FAIL"
            lines.append(f"  [{status}] {label}")

        lines.append("")

    # ---- Risk reminders --------------------------------------------------
    lines.append("-" * 70)
    lines.append("  RISK MANAGEMENT REMINDERS")
    lines.append("-" * 70)
    lines.append(f"  - Risk per trade       : {config.RISK_PER_TRADE:.1%} of portfolio")
    lines.append(f"  - Max position size    : {config.MAX_POSITION_SIZE:.0%} of portfolio")
    lines.append(f"  - Drawdown halt level  : {config.MAX_DRAWDOWN_HALT:.0%}")
    lines.append(f"  - Stop-loss multiplier : {config.ATR_STOP_MULTIPLIER:.1f} × ATR")
    lines.append(f"  - Target multiplier    : {config.ATR_TARGET_MULTIPLIER:.1f} × ATR")
    lines.append("")

    # ---- Disclaimer ------------------------------------------------------
    lines.append("=" * 70)
    lines.append(
        "  DISCLAIMER: This report is for research purposes only. Past performance"
    )
    lines.append(
        "  does not guarantee future results. Always apply proper risk management."
    )
    lines.append("=" * 70)

    report = "\n".join(lines)
    return report


# ---------------------------------------------------------------------------
# Report file I/O
# ---------------------------------------------------------------------------

def save_report_to_file(
    report_text: str,
    date: str,
    output_dir: str = config.REPORTS_DIR,
) -> str:
    """
    Save the report text to a file in the reports output directory.

    Parameters
    ----------
    report_text : str
        The report content.
    date : str
        Report date used in the filename.
    output_dir : str
        Directory to write the report file.

    Returns
    -------
    str
        Path to the saved report file.
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = f"report_{date}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_text)

    logger.info("Report saved to %s.", filepath)
    return filepath


def load_report_from_file(date: str, output_dir: str = config.REPORTS_DIR) -> Optional[str]:
    """
    Load a previously saved report from a file.

    Parameters
    ----------
    date : str
    output_dir : str

    Returns
    -------
    str or None
    """
    filepath = os.path.join(output_dir, f"report_{date}.txt")
    if not os.path.exists(filepath):
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def list_available_reports(output_dir: str = config.REPORTS_DIR) -> List[str]:
    """
    Return a sorted list of dates for which report files exist.

    Returns
    -------
    list of str
        Sorted date strings (newest first).
    """
    if not os.path.isdir(output_dir):
        return []

    dates = []
    for fname in os.listdir(output_dir):
        if fname.startswith("report_") and fname.endswith(".txt"):
            date_part = fname[len("report_"):-len(".txt")]
            dates.append(date_part)

    return sorted(dates, reverse=True)
