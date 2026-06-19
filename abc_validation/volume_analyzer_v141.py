"""
abc_validation/volume_analyzer_v141.py — Volume analysis for A/B/C buy points v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


VOLUME_STATES = [
    "pullback_volume_contraction",
    "breakout_volume_expansion",
    "no_volume_reclaim",
    "abnormal_single_day",
    "multi_day_confirmation",
    "volume_unavailable",
    "volume_baseline_insufficient",
]


class ABCVolumeAnalyzer:
    """
    Analyzes volume patterns for A/B/C buy point signals.

    Output per volume state: signal_count, fill_count, expectancy,
    false_signal_rate, stop_out_rate, drawdown, sample_confidence.
    """

    def classify_volume_state(self, signal: dict, bars: Optional[list] = None) -> str:
        """Classify volume state for a signal."""
        if bars is None or len(bars) < 5:
            return "volume_baseline_insufficient"

        volumes = [b.get("volume") for b in bars if b.get("volume") is not None]
        if not volumes:
            return "volume_unavailable"
        if len(volumes) < 5:
            return "volume_baseline_insufficient"

        baseline_vol = sum(volumes[-20:]) / min(len(volumes), 20)
        signal_vol = signal.get("signal_volume") or (volumes[-1] if volumes else None)

        if signal_vol is None:
            return "volume_unavailable"

        vol_ratio = signal_vol / baseline_vol if baseline_vol > 0 else 1.0

        # Check for abnormal single day
        if vol_ratio > 3.0:
            return "abnormal_single_day"

        buy_point_type = signal.get("buy_point_type", "A")

        if buy_point_type == "C":
            # C buy point needs volume expansion for reclaim
            if vol_ratio >= 1.2:
                return "breakout_volume_expansion"
            elif vol_ratio < 0.8:
                return "no_volume_reclaim"
            return "multi_day_confirmation"

        # A and B: pullback should have volume contraction
        if vol_ratio < 0.8:
            return "pullback_volume_contraction"
        elif vol_ratio > 1.5:
            return "breakout_volume_expansion"
        return "multi_day_confirmation"

    def analyze(
        self,
        signals: List[dict],
        bars_by_symbol: Optional[Dict[str, list]] = None,
        trade_results: Optional[List[dict]] = None,
        buy_point_type: str = "A",
    ) -> Dict[str, Any]:
        """Analyze volume patterns for all signals."""
        bars_by_symbol = bars_by_symbol or {}
        trade_results = trade_results or []

        state_signals: Dict[str, List[dict]] = {s: [] for s in VOLUME_STATES}

        for sig in signals:
            symbol = sig.get("symbol", "")
            signal_date = sig.get("signal_date", "")
            bars = bars_by_symbol.get(symbol, [])
            bars_before = [b for b in bars if b.get("date", "") <= signal_date]
            state = self.classify_volume_state(sig, bars_before)
            state_signals[state].append(sig)

        state_metrics = {}
        for state, sigs in state_signals.items():
            if not sigs:
                state_metrics[state] = {
                    "signal_count": 0, "fill_count": 0, "expectancy": None,
                    "false_signal_rate": None, "stop_out_rate": None,
                    "drawdown": None, "sample_confidence": "INSUFFICIENT"
                }
                continue

            sig_ids = {s.get("signal_id") for s in sigs}
            rel_trades = [t for t in trade_results if t.get("signal_id") in sig_ids]

            if not rel_trades:
                state_metrics[state] = {
                    "signal_count": len(sigs), "fill_count": 0,
                    "expectancy": None, "false_signal_rate": None,
                    "stop_out_rate": None, "drawdown": None,
                    "sample_confidence": "INSUFFICIENT"
                }
                continue

            net_rets = [t.get("net_return", 0) for t in rel_trades]
            wins = [r for r in net_rets if r > 0]
            losses = [r for r in net_rets if r <= 0]
            wr = len(wins) / len(net_rets) if net_rets else 0.0
            aw = sum(wins) / len(wins) if wins else 0.0
            al = abs(sum(losses) / len(losses)) if losses else 0.0
            expectancy = wr * aw - (1 - wr) * al
            false_signal_rate = 1.0 - wr
            stop_outs = sum(1 for t in rel_trades if t.get("exit_reason", "").startswith("STOP"))
            stop_out_rate = stop_outs / len(rel_trades) if rel_trades else 0.0

            cumret = peak = max_dd = 0.0
            for r in net_rets:
                cumret += r
                if cumret > peak:
                    peak = cumret
                dd = peak - cumret
                if dd > max_dd:
                    max_dd = dd

            confidence = "LOW" if len(rel_trades) < 10 else ("MEDIUM" if len(rel_trades) < 30 else "HIGH")

            state_metrics[state] = {
                "signal_count": len(sigs),
                "fill_count": len(rel_trades),
                "expectancy": expectancy,
                "false_signal_rate": false_signal_rate,
                "stop_out_rate": stop_out_rate,
                "drawdown": max_dd,
                "sample_confidence": confidence,
            }

        return {
            "buy_point_type": buy_point_type,
            "total_signals": len(signals),
            "volume_states": VOLUME_STATES,
            "state_metrics": state_metrics,
            "no_real_orders": True,
        }
