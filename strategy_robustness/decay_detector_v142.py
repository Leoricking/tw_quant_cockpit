"""
strategy_robustness/decay_detector_v142.py — Strategy decay detection for v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import statistics
from typing import List, Dict

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class StrategyDecayDetector:
    """
    Detects signs of strategy performance decay over time.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def analyze(self, trades: list, config) -> dict:
        """
        Analyze strategy for decay signals.

        Parameters
        ----------
        trades : list of dicts with keys: return_pct, date, symbol, win, cost
        config : RobustnessConfiguration

        Returns
        -------
        dict with decay detection results including DecayStatus
        """
        from strategy_robustness.models_v142 import DecayStatus

        if not trades or len(trades) < 6:
            return {
                "decay_status": DecayStatus.INSUFFICIENT_DATA,
                "trade_count": len(trades) if trades else 0,
                "evidence": ["INSUFFICIENT_DATA: need at least 6 trades"],
                "metrics": {},
                "warnings": ["INSUFFICIENT_TRADES_FOR_DECAY_DETECTION"],
            }

        sorted_trades = sorted(trades, key=lambda t: t.get("date", ""))
        n = len(sorted_trades)
        mid = n // 2

        early_trades = sorted_trades[:mid]
        recent_trades = sorted_trades[mid:]

        def period_stats(tlist):
            rets = [t.get("return_pct", 0.0) for t in tlist]
            costs = [t.get("cost", 0.0) for t in tlist]
            net_rets = [r - c for r, c in zip(rets, costs)]
            if not net_rets:
                return {"expectancy": 0.0, "win_rate": 0.0, "drawdown": 0.0, "profit_factor": 0.0, "count": 0}
            wins = [r for r in net_rets if r > 0]
            losses = [r for r in net_rets if r < 0]
            exp = statistics.mean(net_rets)
            wr = len(wins) / len(net_rets)
            win_sum = sum(wins)
            loss_sum = abs(sum(losses))
            pf = win_sum / loss_sum if loss_sum > 0 else (float("inf") if win_sum > 0 else 0.0)
            cum = 0.0
            peak = 0.0
            max_dd = 0.0
            for r in net_rets:
                cum += r
                if cum > peak:
                    peak = cum
                dd = peak - cum
                if dd > max_dd:
                    max_dd = dd
            return {"expectancy": round(exp, 6), "win_rate": round(wr, 4), "drawdown": round(max_dd, 6),
                    "profit_factor": round(min(pf, 9999.0), 4), "count": len(tlist)}

        early_stats = period_stats(early_trades)
        recent_stats = period_stats(recent_trades)

        # Decay metrics
        expectancy_decline = recent_stats["expectancy"] - early_stats["expectancy"]
        win_rate_decline = recent_stats["win_rate"] - early_stats["win_rate"]
        drawdown_increase = recent_stats["drawdown"] - early_stats["drawdown"]
        profit_factor_decline = recent_stats["profit_factor"] - early_stats["profit_factor"]
        signal_freq_change = recent_stats["count"] - early_stats["count"]

        evidence = []
        decay_signals = 0

        if expectancy_decline < -0.005:
            evidence.append(f"EXPECTANCY_DECLINE: {expectancy_decline:.4f}")
            decay_signals += 1

        if win_rate_decline < -0.05:
            evidence.append(f"WIN_RATE_DECLINE: {win_rate_decline:.4f}")
            decay_signals += 1

        if drawdown_increase > 0.02:
            evidence.append(f"DRAWDOWN_INCREASE: {drawdown_increase:.4f}")
            decay_signals += 1

        if profit_factor_decline < -0.3:
            evidence.append(f"PROFIT_FACTOR_DECLINE: {profit_factor_decline:.4f}")
            decay_signals += 1

        if signal_freq_change < -early_stats["count"] * 0.3:
            evidence.append(f"SIGNAL_FREQUENCY_DROP: {signal_freq_change}")
            decay_signals += 1

        # Determine decay status
        if n < 10:
            decay_status = DecayStatus.INSUFFICIENT_DATA
        elif decay_signals == 0:
            decay_status = DecayStatus.NO_DECAY
        elif decay_signals <= 1:
            decay_status = DecayStatus.POSSIBLE_DECAY
        elif decay_signals <= 2:
            decay_status = DecayStatus.POSSIBLE_DECAY
        else:
            decay_status = DecayStatus.SIGNIFICANT_DECAY

        warnings = []
        if decay_status in (DecayStatus.POSSIBLE_DECAY, DecayStatus.SIGNIFICANT_DECAY):
            warnings.append(f"DECAY_DETECTED_{decay_status}")
        if n < 20:
            warnings.append("LOW_TRADE_COUNT")

        return {
            "decay_status": decay_status,
            "trade_count": n,
            "early_period": early_stats,
            "recent_period": recent_stats,
            "metrics": {
                "expectancy_decline": round(expectancy_decline, 6),
                "win_rate_decline": round(win_rate_decline, 4),
                "drawdown_increase": round(drawdown_increase, 6),
                "profit_factor_decline": round(profit_factor_decline, 4),
                "signal_frequency_change": signal_freq_change,
            },
            "evidence": evidence,
            "decay_signals": decay_signals,
            "warnings": warnings,
        }
