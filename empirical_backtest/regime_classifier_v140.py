"""
empirical_backtest/regime_classifier_v140.py — Market Regime Classifier for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from .models_v140 import MarketRegime


class MarketRegimeClassifier:
    """Classifies market regime from historical bar data."""

    def classify(self, bars: list, window: int = 60) -> str:
        """Classify regime using only past data (no future leakage)."""
        if not bars or len(bars) < 2:
            return MarketRegime.UNKNOWN

        # Use only up to window bars
        relevant_bars = bars[-window:] if len(bars) >= window else bars

        closes = []
        for bar in relevant_bars:
            c = bar.get("close")
            if c is not None:
                try:
                    closes.append(float(c))
                except (TypeError, ValueError):
                    pass

        if len(closes) < 2:
            return MarketRegime.UNKNOWN

        # Compute daily returns
        returns = [(closes[i] - closes[i - 1]) / closes[i - 1] for i in range(1, len(closes))]
        if not returns:
            return MarketRegime.UNKNOWN

        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        volatility = variance ** 0.5

        if volatility > 0.02:
            return MarketRegime.HIGH_VOLATILITY
        elif volatility < 0.005:
            return MarketRegime.LOW_VOLATILITY
        elif mean_return > 0.001:
            return MarketRegime.BULL
        elif mean_return < -0.001:
            return MarketRegime.BEAR
        else:
            return MarketRegime.SIDEWAYS

    def classify_period(self, bars: list) -> dict:
        """Return {date: regime} for each bar using only past data."""
        result = {}
        for i, bar in enumerate(bars):
            date = bar.get("date", str(i))
            past_bars = bars[:i + 1]  # No future leakage
            regime = self.classify(past_bars)
            result[date] = regime
        return result

    def split_by_regime(self, trades: list, regime_map: dict) -> dict:
        """Split trades by market regime."""
        by_regime: dict = {}
        for trade in trades:
            entry_date = trade.get("entry_date", "") if isinstance(trade, dict) else getattr(trade, "entry_date", "")
            regime = regime_map.get(entry_date, MarketRegime.UNKNOWN)
            if regime not in by_regime:
                by_regime[regime] = []
            by_regime[regime].append(trade)
        return by_regime

    def metrics_by_regime(self, trades: list, bars: list) -> dict:
        """Calculate per-regime metrics."""
        regime_map = self.classify_period(bars)
        by_regime = self.split_by_regime(trades, regime_map)
        result = {}

        for regime, regime_trades in by_regime.items():
            if not regime_trades:
                continue
            returns = []
            for t in regime_trades:
                r = t.get("net_return", 0.0) if isinstance(t, dict) else getattr(t, "net_return", 0.0)
                try:
                    returns.append(float(r))
                except (TypeError, ValueError):
                    pass

            wins = [r for r in returns if r > 0]
            losses = [r for r in returns if r <= 0]
            win_rate = len(wins) / len(returns) if returns else 0.0
            avg_return = sum(returns) / len(returns) if returns else 0.0

            # Simple max drawdown
            peak = 0.0
            cum = 0.0
            max_dd = 0.0
            for r in returns:
                cum += r
                if cum > peak:
                    peak = cum
                dd = peak - cum
                if dd > max_dd:
                    max_dd = dd

            avg_win = sum(wins) / len(wins) if wins else 0.0
            avg_loss = abs(sum(losses) / len(losses)) if losses else 0.0
            expectancy = win_rate * avg_win - (1 - win_rate) * avg_loss if returns else 0.0

            result[regime] = {
                "trade_count": len(regime_trades),
                "win_rate": win_rate,
                "avg_return": avg_return,
                "max_drawdown": max_dd,
                "expectancy": expectancy,
            }

        return result
