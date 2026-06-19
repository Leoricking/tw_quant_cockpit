"""
abc_validation/take_profit_analyzer_v141.py — Take profit analysis for A/B/C buy points v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


TAKE_PROFIT_MODELS = [
    "fixed_pct",
    "risk_reward_multiple",
    "ma5_exit",
    "ma10_exit",
    "ma20_exit",
    "trailing_stop",
    "momentum_failure",
    "volume_price_failure",
    "max_holding_period",
    "strategy_defined_exit",
]


class ABCTakeProfitAnalyzer:
    """
    Analyzes take profit outcomes for A/B/C buy point signals.

    Output: gross_return, net_return, holding_period, win_rate, profit_factor,
    expectancy, drawdown, exit_reason_distribution, stop_target_collision_count.
    """

    def __init__(self, tp_model: str = "fixed_pct", tp_pct: float = 0.15,
                 max_holding: int = 20):
        if tp_model not in TAKE_PROFIT_MODELS:
            raise ValueError(f"Unknown take profit model: {tp_model}. Choose from {TAKE_PROFIT_MODELS}")
        self.tp_model = tp_model
        self.tp_pct = tp_pct
        self.max_holding = max_holding

    def analyze(
        self,
        signals: List[dict],
        bars_by_symbol: Optional[Dict[str, list]] = None,
        cost_model: Optional[dict] = None,
        stop_prices: Optional[Dict[str, float]] = None,
        buy_point_type: str = "A",
    ) -> Dict[str, Any]:
        """Analyze take profit outcomes for all signals."""
        bars_by_symbol = bars_by_symbol or {}
        cost_model = cost_model or {}
        stop_prices = stop_prices or {}
        results = []
        no_fills = 0
        stop_target_collisions = 0
        exit_reason_counts: Dict[str, int] = {}

        for sig in signals:
            symbol = sig.get("symbol", "")
            entry_price = sig.get("entry_price")
            bars = bars_by_symbol.get(symbol, [])
            signal_date = sig.get("signal_date", "")

            if entry_price is None or not bars:
                no_fills += 1
                continue

            tp_price = self._compute_target(sig, entry_price)
            stop_price = stop_prices.get(symbol, entry_price * 0.93)

            # Detect stop/target collision (same bar)
            if tp_price is not None and stop_price is not None:
                if abs(tp_price - stop_price) / entry_price < 0.001:
                    stop_target_collisions += 1
                    # Conservative: use stop (not target)
                    tp_price = None

            # Find entry bar
            entry_idx = None
            for i, b in enumerate(bars):
                if b.get("date", "") >= signal_date:
                    entry_idx = i
                    break

            if entry_idx is None:
                no_fills += 1
                continue

            exit_price = entry_price
            exit_reason = "END_OF_DATA"
            holding_days = 0

            for j, bar in enumerate(bars[entry_idx + 1:], 1):
                high = bar.get("high", bar.get("close", entry_price))
                low = bar.get("low", bar.get("close", entry_price))
                close = bar.get("close", entry_price)
                holding_days = j

                # Check take profit
                if tp_price is not None and high >= tp_price:
                    exit_price = tp_price
                    exit_reason = f"TAKE_PROFIT_{self.tp_model.upper()}"
                    break

                # Check stop
                if low <= stop_price:
                    exit_price = stop_price
                    exit_reason = "STOP_LOSS"
                    break

                # Max holding
                if j >= self.max_holding:
                    exit_price = close
                    exit_reason = "MAX_HOLDING_PERIOD"
                    break

                exit_price = close

            exit_reason_counts[exit_reason] = exit_reason_counts.get(exit_reason, 0) + 1

            fee_rate = cost_model.get("fee_rate", 0.001425)
            tax_rate = cost_model.get("tax_rate", 0.003)
            slippage = cost_model.get("slippage_rate", 0.001) * 2
            gross_return = (exit_price - entry_price) / entry_price
            fees = fee_rate * 2
            tax = tax_rate if gross_return > 0 else 0.0
            net_return = gross_return - fees - tax - slippage

            results.append({
                "symbol": symbol,
                "gross_return": gross_return,
                "net_return": net_return,
                "holding_period": holding_days,
                "exit_reason": exit_reason,
            })

        return self._summarize(results, signals, no_fills, stop_target_collisions,
                               exit_reason_counts, buy_point_type)

    def _compute_target(self, sig: dict, entry_price: float) -> Optional[float]:
        if self.tp_model == "fixed_pct":
            return entry_price * (1 + self.tp_pct)
        if self.tp_model == "risk_reward_multiple":
            risk = sig.get("risk_pct", 0.07)
            return entry_price * (1 + risk * 2)
        if self.tp_model in ("ma5_exit", "ma10_exit", "ma20_exit"):
            return None  # MA-based — no fixed target
        if self.tp_model == "strategy_defined_exit":
            return sig.get("target_price", entry_price * (1 + self.tp_pct))
        return entry_price * (1 + self.tp_pct)

    def _summarize(self, results, signals, no_fills, collisions, exit_reason_counts,
                   buy_point_type) -> dict:
        if not results:
            return {
                "tp_model": self.tp_model,
                "buy_point_type": buy_point_type,
                "signal_count": len(signals),
                "filled_trades": 0,
                "no_fill_count": no_fills,
                "gross_return": None,
                "net_return": None,
                "holding_period": None,
                "win_rate": None,
                "profit_factor": None,
                "expectancy": None,
                "drawdown": None,
                "exit_reason_distribution": {},
                "stop_target_collision_count": collisions,
                "no_real_orders": True,
            }

        net_rets = [r["net_return"] for r in results]
        gross_rets = [r["gross_return"] for r in results]
        wins = [r for r in net_rets if r > 0]
        losses = [r for r in net_rets if r <= 0]
        win_rate = len(wins) / len(net_rets) if net_rets else 0.0
        avg_win = sum(wins) / len(wins) if wins else 0.0
        avg_loss = abs(sum(losses) / len(losses)) if losses else 0.0
        profit_factor = (sum(wins) / abs(sum(losses))) if losses and sum(losses) != 0 else float("inf")
        expectancy = win_rate * avg_win - (1 - win_rate) * avg_loss

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

        avg_hold = sum(r["holding_period"] for r in results) / len(results)

        return {
            "tp_model": self.tp_model,
            "buy_point_type": buy_point_type,
            "signal_count": len(signals),
            "filled_trades": len(results),
            "no_fill_count": no_fills,
            "gross_return": sum(gross_rets) / len(gross_rets),
            "net_return": sum(net_rets) / len(net_rets),
            "holding_period": avg_hold,
            "win_rate": win_rate,
            "profit_factor": profit_factor,
            "expectancy": expectancy,
            "drawdown": max_dd,
            "exit_reason_distribution": exit_reason_counts,
            "stop_target_collision_count": collisions,
            "no_real_orders": True,
        }
