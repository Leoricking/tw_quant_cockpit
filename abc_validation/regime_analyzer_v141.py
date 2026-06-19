"""
abc_validation/regime_analyzer_v141.py — Regime analysis for A/B/C buy points v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Uses existing v1.4.0 MarketRegimeClassifier. No future regime labeling for signals.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


REGIME_VALUES = ["BULL", "BEAR", "SIDEWAYS", "HIGH_VOLATILITY", "LOW_VOLATILITY", "UNKNOWN"]


class ABCRegimeAnalyzer:
    """
    Analyzes A/B/C signals by market regime.

    Uses empirical_backtest.regime_classifier_v140.MarketRegimeClassifier.
    Output per regime: signal_count, trade_count, win_rate, expectancy,
    avg_return, median_return, drawdown, profit_factor, mfe, mae, confidence.
    """

    def __init__(self):
        self._classifier = None

    def _get_classifier(self):
        if self._classifier is None:
            from empirical_backtest.regime_classifier_v140 import MarketRegimeClassifier
            self._classifier = MarketRegimeClassifier()
        return self._classifier

    def classify_signal_regime(self, bars_before_signal: list) -> str:
        """Classify regime using only bars before the signal date (no lookahead)."""
        if not bars_before_signal:
            return "UNKNOWN"
        clf = self._get_classifier()
        return clf.classify(bars_before_signal)

    def analyze(
        self,
        signals: List[dict],
        bars_by_symbol: Optional[Dict[str, list]] = None,
        trade_results: Optional[List[dict]] = None,
        buy_point_type: str = "A",
    ) -> Dict[str, Any]:
        """
        Analyze signal and trade outcomes per regime.

        Returns dict keyed by regime string → regime result dict.
        """
        bars_by_symbol = bars_by_symbol or {}
        trade_results = trade_results or []

        # Build regime for each signal (no future data)
        signal_regimes: Dict[str, str] = {}
        for sig in signals:
            symbol = sig.get("symbol", "")
            signal_date = sig.get("signal_date", "")
            bars = bars_by_symbol.get(symbol, [])
            bars_before = [b for b in bars if b.get("date", "") < signal_date]
            regime = self.classify_signal_regime(bars_before)
            signal_regimes[sig.get("signal_id", "")] = regime

        # Map trades to regimes
        regime_signals: Dict[str, List[dict]] = {r: [] for r in REGIME_VALUES}
        regime_trades: Dict[str, List[dict]] = {r: [] for r in REGIME_VALUES}

        for sig in signals:
            sig_id = sig.get("signal_id", "")
            regime = signal_regimes.get(sig_id, "UNKNOWN")
            regime_signals[regime].append(sig)

        for trade in trade_results:
            sig_id = trade.get("signal_id", "")
            regime = signal_regimes.get(sig_id, "UNKNOWN")
            regime_trades[regime].append(trade)

        results = {}
        for regime in REGIME_VALUES:
            sigs = regime_signals[regime]
            trades = regime_trades[regime]
            results[regime] = self._summarize_regime(regime, sigs, trades)

        return {
            "buy_point_type": buy_point_type,
            "regime_results": results,
            "no_real_orders": True,
            "no_future_regime_labeling": True,
        }

    def _summarize_regime(self, regime: str, signals: list, trades: list) -> dict:
        if not signals:
            return {
                "regime": regime,
                "signal_count": 0,
                "trade_count": 0,
                "win_rate": None,
                "expectancy": None,
                "avg_return": None,
                "median_return": None,
                "drawdown": None,
                "profit_factor": None,
                "mfe": None,
                "mae": None,
                "confidence": "INSUFFICIENT",
            }

        net_rets = [t.get("net_return", 0) for t in trades]
        if not net_rets:
            return {
                "regime": regime,
                "signal_count": len(signals),
                "trade_count": 0,
                "win_rate": None,
                "expectancy": None,
                "avg_return": None,
                "median_return": None,
                "drawdown": None,
                "profit_factor": None,
                "mfe": None,
                "mae": None,
                "confidence": "INSUFFICIENT",
            }

        wins = [r for r in net_rets if r > 0]
        losses = [r for r in net_rets if r <= 0]
        win_rate = len(wins) / len(net_rets)
        avg_return = sum(net_rets) / len(net_rets)
        sorted_rets = sorted(net_rets)
        mid = len(sorted_rets) // 2
        median_return = sorted_rets[mid]
        avg_win = sum(wins) / len(wins) if wins else 0.0
        avg_loss = abs(sum(losses) / len(losses)) if losses else 0.0
        expectancy = win_rate * avg_win - (1 - win_rate) * avg_loss
        profit_factor = (sum(wins) / abs(sum(losses))) if losses and sum(losses) != 0 else float("inf")

        mfe = sum(max(r, 0) for r in net_rets) / len(net_rets)
        mae = sum(min(r, 0) for r in net_rets) / len(net_rets)

        # Simple drawdown
        cumret = 0.0
        peak = 0.0
        max_dd = 0.0
        for r in net_rets:
            cumret += r
            if cumret > peak:
                peak = cumret
            dd = peak - cumret
            if dd > max_dd:
                max_dd = dd

        confidence = "LOW" if len(trades) < 20 else ("MEDIUM" if len(trades) < 50 else "HIGH")

        return {
            "regime": regime,
            "signal_count": len(signals),
            "trade_count": len(trades),
            "win_rate": win_rate,
            "expectancy": expectancy,
            "avg_return": avg_return,
            "median_return": median_return,
            "drawdown": max_dd,
            "profit_factor": profit_factor,
            "mfe": mfe,
            "mae": mae,
            "confidence": confidence,
        }
