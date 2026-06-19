"""
abc_validation/filter_ablation_v141.py — Filter ablation analysis for A/B/C buy points v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Rules:
  - One filter added at a time
  - Same universe, period, costs
  - Preserve ALL results (not just best)
  - Show sample count change, signal decrease ratio, expectancy delta, drawdown change
  - Over-filtering warning
  - No declaring tiny-high-winrate as best
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


FILTER_STAGES = [
    "base_only",
    "+volume_contraction",
    "+kd",
    "+rsi",
    "+macd",
    "+foreign",
    "+investment_trust",
    "+dealer",
    "+margin",
    "+ma60_trend",
    "+second_wave",
    "full_composite",
]

OVER_FILTER_THRESHOLD = 0.5  # signal decrease ratio > 50% → warn


def _apply_filter(signals: List[dict], stage: str) -> List[dict]:
    """Apply a single filter stage. Returns filtered signals."""
    if stage == "base_only":
        return list(signals)
    if stage == "+volume_contraction":
        return [s for s in signals if s.get("vol_contraction", True)]
    if stage == "+kd":
        kd = [s for s in signals if s.get("kd_value") is not None]
        return [s for s in kd if s["kd_value"] <= 50]
    if stage == "+rsi":
        rsi = [s for s in signals if s.get("rsi_value") is not None]
        return [s for s in rsi if s["rsi_value"] <= 60]
    if stage == "+macd":
        return [s for s in signals if s.get("macd_improving", True)]
    if stage == "+foreign":
        return [s for s in signals if s.get("foreign_net", 0) >= 0]
    if stage == "+investment_trust":
        return [s for s in signals if s.get("trust_net", 0) >= 0]
    if stage == "+dealer":
        return [s for s in signals if s.get("dealer_net", 0) >= 0]
    if stage == "+margin":
        return [s for s in signals if s.get("margin_stable", True)]
    if stage == "+ma60_trend":
        return [s for s in signals if s.get("ma60_up", True)]
    if stage == "+second_wave":
        return [s for s in signals if s.get("is_second_wave", False)]
    if stage == "full_composite":
        return _apply_all_filters(signals)
    return list(signals)


def _apply_all_filters(signals: List[dict]) -> List[dict]:
    result = list(signals)
    for stage in FILTER_STAGES[1:-1]:  # skip base_only and full_composite
        result = _apply_filter(result, stage)
    return result


def _compute_metrics(signals: List[dict], trade_results: List[dict]) -> dict:
    """Compute metrics for a set of signals."""
    sig_ids = {s.get("signal_id") for s in signals}
    relevant_trades = [t for t in trade_results if t.get("signal_id") in sig_ids]
    if not relevant_trades:
        return {"signal_count": len(signals), "trade_count": 0,
                "win_rate": None, "expectancy": None, "drawdown": None}
    net_rets = [t.get("net_return", 0) for t in relevant_trades]
    wins = [r for r in net_rets if r > 0]
    losses = [r for r in net_rets if r <= 0]
    win_rate = len(wins) / len(net_rets) if net_rets else 0.0
    avg_win = sum(wins) / len(wins) if wins else 0.0
    avg_loss = abs(sum(losses) / len(losses)) if losses else 0.0
    expectancy = win_rate * avg_win - (1 - win_rate) * avg_loss
    cumret = peak = max_dd = 0.0
    for r in net_rets:
        cumret += r
        if cumret > peak:
            peak = cumret
        dd = peak - cumret
        if dd > max_dd:
            max_dd = dd
    return {
        "signal_count": len(signals),
        "trade_count": len(relevant_trades),
        "win_rate": win_rate,
        "expectancy": expectancy,
        "drawdown": max_dd,
    }


class ABCFilterAblationAnalyzer:
    """
    Ablation study: adds one filter at a time and measures impact.

    Preserves ALL results — not just the best.
    Warns on over-filtering (signal decrease ratio > threshold).
    Never declares tiny high-winrate subset as best.
    """

    def analyze(
        self,
        signals: List[dict],
        trade_results: Optional[List[dict]] = None,
        buy_point_type: str = "A",
    ) -> Dict[str, Any]:
        """Run full filter ablation analysis."""
        trade_results = trade_results or []
        ablation_results = {}
        base_count = len(signals)
        base_metrics = _compute_metrics(signals, trade_results)
        warnings = []

        for stage in FILTER_STAGES:
            filtered = _apply_filter(signals, stage)
            metrics = _compute_metrics(filtered, trade_results)

            # Compute deltas vs base
            sig_decrease_ratio = 1.0 - (len(filtered) / base_count) if base_count > 0 else 0.0
            exp_delta = None
            dd_delta = None
            if base_metrics.get("expectancy") is not None and metrics.get("expectancy") is not None:
                exp_delta = metrics["expectancy"] - base_metrics["expectancy"]
            if base_metrics.get("drawdown") is not None and metrics.get("drawdown") is not None:
                dd_delta = metrics["drawdown"] - base_metrics["drawdown"]

            # Over-filtering warning
            if sig_decrease_ratio > OVER_FILTER_THRESHOLD and stage != "base_only":
                warnings.append(
                    f"OVER_FILTERING at {stage}: signal count dropped {sig_decrease_ratio:.0%} "
                    f"from base ({base_count} → {len(filtered)})"
                )

            # No declaring tiny high-winrate as best
            is_reliable = len(filtered) >= 10 and metrics.get("trade_count", 0) >= 5

            ablation_results[stage] = {
                "stage": stage,
                "signal_count": len(filtered),
                "trade_count": metrics.get("trade_count", 0),
                "signal_decrease_ratio": sig_decrease_ratio,
                "win_rate": metrics.get("win_rate"),
                "expectancy": metrics.get("expectancy"),
                "expectancy_delta": exp_delta,
                "drawdown": metrics.get("drawdown"),
                "drawdown_delta": dd_delta,
                "is_reliable": is_reliable,
            }

        return {
            "buy_point_type": buy_point_type,
            "base_signal_count": base_count,
            "ablation_results": ablation_results,
            "filter_stages": FILTER_STAGES,
            "warnings": warnings,
            "note": "ALL stages preserved. No single best declared. Tiny high-winrate NOT valid conclusion.",
            "no_real_orders": True,
        }
