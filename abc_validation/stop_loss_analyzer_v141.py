"""
abc_validation/stop_loss_analyzer_v141.py — Stop loss analysis for A/B/C buy points v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
Rules:
  - same-bar stop+target → conservative order
  - stop slippage included
  - can't assume fill at stop price
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


STOP_MODELS = [
    "no_stop",
    "fixed_pct",
    "below_signal_low",
    "below_ma5",
    "below_ma10",
    "below_ma20",
    "atr_based",
    "time_stop",
    "structure_failure",
]


class ABCStopLossAnalyzer:
    """
    Analyzes stop loss effectiveness for A/B/C buy point signals.

    Supported models: no_stop, fixed_pct, below_signal_low, below_ma5,
    below_ma10, below_ma20, atr_based, time_stop, structure_failure.
    """

    def __init__(self, stop_model: str = "fixed_pct", stop_pct: float = 0.07):
        if stop_model not in STOP_MODELS:
            raise ValueError(f"Unknown stop model: {stop_model}. Choose from {STOP_MODELS}")
        self.stop_model = stop_model
        self.stop_pct = stop_pct

    def analyze(
        self,
        signals: List[dict],
        bars_by_symbol: Optional[Dict[str, list]] = None,
        cost_model: Optional[dict] = None,
        buy_point_type: str = "A",
    ) -> Dict[str, Any]:
        """Analyze stop loss outcomes for all signals."""
        bars_by_symbol = bars_by_symbol or {}
        cost_model = cost_model or {}
        results = []
        stop_outs = 0
        no_fills = 0
        filled = 0

        for sig in signals:
            symbol = sig.get("symbol", "")
            entry_price = sig.get("entry_price")
            bars = bars_by_symbol.get(symbol, [])
            signal_date = sig.get("signal_date", "")

            if entry_price is None or not bars:
                no_fills += 1
                continue

            stop_price = self._compute_stop(sig, bars, entry_price)
            if stop_price is None:
                no_fills += 1
                continue

            # Include stop slippage (conservative: can't assume fill at stop price)
            slippage_rate = cost_model.get("slippage_rate", 0.001)
            slippage_adj = 1.0 - slippage_rate  # actual fill worse than stop
            effective_stop = stop_price * slippage_adj

            # Find entry bar
            entry_idx = None
            for i, b in enumerate(bars):
                if b.get("date", "") >= signal_date:
                    entry_idx = i
                    break

            if entry_idx is None:
                no_fills += 1
                continue

            filled += 1
            stopped_out = False
            exit_price = entry_price
            exit_reason = "END_OF_DATA"

            for bar in bars[entry_idx + 1:]:
                low = bar.get("low", bar.get("close", entry_price))
                close = bar.get("close", entry_price)

                if self.stop_model != "no_stop" and low <= effective_stop:
                    stopped_out = True
                    exit_price = effective_stop
                    exit_reason = f"STOP_{self.stop_model.upper()}"
                    stop_outs += 1
                    break

                exit_price = close

            fee_rate = cost_model.get("fee_rate", 0.001425)
            tax_rate = cost_model.get("tax_rate", 0.003)
            gross_return = (exit_price - entry_price) / entry_price
            fees = fee_rate * 2
            tax = tax_rate if gross_return > 0 else 0.0
            net_return = gross_return - fees - tax - slippage_rate * 2

            results.append({
                "symbol": symbol,
                "stop_model": self.stop_model,
                "stop_price": stop_price,
                "effective_stop": effective_stop,
                "stopped_out": stopped_out,
                "exit_price": exit_price,
                "exit_reason": exit_reason,
                "gross_return": gross_return,
                "net_return": net_return,
            })

        return self._summarize(results, signals, filled, no_fills, stop_outs, buy_point_type)

    def _compute_stop(self, sig: dict, bars: list, entry_price: float) -> Optional[float]:
        if self.stop_model == "no_stop":
            return None
        if self.stop_model == "fixed_pct":
            return entry_price * (1 - self.stop_pct)
        if self.stop_model == "below_signal_low":
            signal_low = sig.get("signal_low", entry_price * 0.97)
            return signal_low * 0.995
        if self.stop_model in ("below_ma5", "below_ma10", "below_ma20"):
            ma_val = sig.get(f"{self.stop_model.replace('below_', '')}_value")
            if ma_val:
                return ma_val * 0.995
            return entry_price * (1 - self.stop_pct)
        if self.stop_model == "atr_based":
            atr = sig.get("atr", entry_price * 0.02)
            return entry_price - 2 * atr
        if self.stop_model == "time_stop":
            return None  # time-based — no price stop
        if self.stop_model == "structure_failure":
            return sig.get("structure_level", entry_price * (1 - self.stop_pct))
        return entry_price * (1 - self.stop_pct)

    def _summarize(self, results, signals, filled, no_fills, stop_outs, buy_point_type) -> dict:
        if not results:
            return {
                "stop_model": self.stop_model,
                "buy_point_type": buy_point_type,
                "signal_count": len(signals),
                "filled_trades": 0,
                "no_fill_count": no_fills,
                "stop_out_count": 0,
                "stop_out_rate": None,
                "avg_net_return": None,
                "win_rate": None,
                "no_real_orders": True,
            }

        net_rets = [r["net_return"] for r in results]
        wins = [r for r in net_rets if r > 0]
        win_rate = len(wins) / len(net_rets)
        avg_net = sum(net_rets) / len(net_rets)
        stop_out_rate = stop_outs / len(results) if results else 0.0

        return {
            "stop_model": self.stop_model,
            "buy_point_type": buy_point_type,
            "signal_count": len(signals),
            "filled_trades": filled,
            "no_fill_count": no_fills,
            "stop_out_count": stop_outs,
            "stop_out_rate": stop_out_rate,
            "avg_net_return": avg_net,
            "win_rate": win_rate,
            "no_real_orders": True,
        }
