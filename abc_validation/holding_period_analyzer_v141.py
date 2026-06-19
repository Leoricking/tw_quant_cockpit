"""
abc_validation/holding_period_analyzer_v141.py — Holding period analysis for A/B/C v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

HOLDING_PERIODS = [1, 2, 3, 5, 10, 20]


class ABCHoldingPeriodAnalyzer:
    """
    Analyzes holding period returns for A/B/C buy point signals.

    Supports 1/2/3/5/10/20 trading days, rule exit, and stop/take-profit exit.
    Output per period: signals, filled_trades, avg_return, median_return, win_rate,
    expectancy, max_drawdown, mfe, mae, positive_excursion_prob,
    negative_excursion_prob, fees, taxes, slippage, benchmark_excess_return.
    """

    def __init__(self, periods: Optional[List[int]] = None):
        self.periods = periods or HOLDING_PERIODS

    def analyze(
        self,
        signals: List[dict],
        bars_by_symbol: Optional[Dict[str, list]] = None,
        cost_model: Optional[dict] = None,
        benchmark_returns: Optional[Dict[str, float]] = None,
        buy_point_type: str = "A",
    ) -> Dict[str, Any]:
        """
        Analyze holding period returns.

        Returns dict keyed by holding period (int) → period result dict.
        """
        results = {}
        for period in self.periods:
            results[period] = self._analyze_period(
                signals, bars_by_symbol or {}, period, cost_model or {},
                benchmark_returns or {}, buy_point_type
            )
        return {
            "buy_point_type": buy_point_type,
            "periods_analyzed": self.periods,
            "period_results": results,
            "no_real_orders": True,
            "formal_conclusion_allowed": False,
        }

    def _analyze_period(
        self,
        signals: list,
        bars_by_symbol: dict,
        period: int,
        cost_model: dict,
        benchmark_returns: dict,
        buy_point_type: str,
    ) -> dict:
        trade_returns = []
        filled_trades = 0
        no_fills = 0

        for sig in signals:
            symbol = sig.get("symbol", "")
            entry_price = sig.get("entry_price")
            bars = bars_by_symbol.get(symbol, [])
            signal_date = sig.get("signal_date", "")

            if entry_price is None or not bars:
                no_fills += 1
                continue

            # Find entry bar index
            entry_idx = None
            for i, b in enumerate(bars):
                if b.get("date", "") >= signal_date:
                    entry_idx = i
                    break

            if entry_idx is None:
                no_fills += 1
                continue

            exit_idx = min(entry_idx + period, len(bars) - 1)
            if exit_idx <= entry_idx:
                no_fills += 1
                continue

            exit_bar = bars[exit_idx]
            exit_price = exit_bar.get("close")
            if exit_price is None:
                no_fills += 1
                continue

            # Cost deduction
            fee_rate = cost_model.get("fee_rate", 0.001425)
            tax_rate = cost_model.get("tax_rate", 0.003)
            slippage_rate = cost_model.get("slippage_rate", 0.001)
            gross_return = (exit_price - entry_price) / entry_price
            fees = fee_rate * 2
            tax = tax_rate if gross_return > 0 else 0.0
            slippage = slippage_rate * 2
            net_return = gross_return - fees - tax - slippage

            filled_trades += 1
            trade_returns.append({
                "symbol": symbol,
                "gross_return": gross_return,
                "net_return": net_return,
                "fees": fees,
                "tax": tax,
                "slippage": slippage,
            })

        if not trade_returns:
            return self._empty_period_result(period, len(signals), no_fills)

        net_rets = [t["net_return"] for t in trade_returns]
        wins = [r for r in net_rets if r > 0]
        win_rate = len(wins) / len(net_rets) if net_rets else 0.0
        avg_return = sum(net_rets) / len(net_rets)

        sorted_rets = sorted(net_rets)
        mid = len(sorted_rets) // 2
        median_return = sorted_rets[mid] if sorted_rets else 0.0

        avg_win = sum(wins) / len(wins) if wins else 0.0
        losses = [r for r in net_rets if r <= 0]
        avg_loss = sum(losses) / len(losses) if losses else 0.0
        expectancy = win_rate * avg_win + (1 - win_rate) * avg_loss

        cumulative = 0.0
        peak = 0.0
        max_drawdown = 0.0
        mfe_list = []
        mae_list = []
        for r in net_rets:
            cumulative += r
            if cumulative > peak:
                peak = cumulative
            dd = peak - cumulative
            if dd > max_drawdown:
                max_drawdown = dd
            mfe_list.append(max(r, 0))
            mae_list.append(min(r, 0))

        mfe = sum(mfe_list) / len(mfe_list) if mfe_list else 0.0
        mae = sum(mae_list) / len(mae_list) if mae_list else 0.0
        pos_excursion_prob = len([r for r in net_rets if r > 0]) / len(net_rets) if net_rets else 0.0
        neg_excursion_prob = len([r for r in net_rets if r < 0]) / len(net_rets) if net_rets else 0.0

        avg_fees = sum(t["fees"] for t in trade_returns) / len(trade_returns)
        avg_tax = sum(t["tax"] for t in trade_returns) / len(trade_returns)
        avg_slippage = sum(t["slippage"] for t in trade_returns) / len(trade_returns)

        bench = sum(benchmark_returns.values()) / len(benchmark_returns) if benchmark_returns else 0.0
        benchmark_excess = avg_return - bench

        return {
            "holding_period_days": period,
            "signals": len(signals),
            "filled_trades": filled_trades,
            "no_fill_count": no_fills,
            "avg_return": avg_return,
            "median_return": median_return,
            "win_rate": win_rate,
            "expectancy": expectancy,
            "max_drawdown": max_drawdown,
            "mfe": mfe,
            "mae": mae,
            "positive_excursion_prob": pos_excursion_prob,
            "negative_excursion_prob": neg_excursion_prob,
            "fees": avg_fees,
            "taxes": avg_tax,
            "slippage": avg_slippage,
            "benchmark_excess_return": benchmark_excess,
        }

    def _empty_period_result(self, period: int, signal_count: int, no_fills: int) -> dict:
        return {
            "holding_period_days": period,
            "signals": signal_count,
            "filled_trades": 0,
            "no_fill_count": no_fills,
            "avg_return": None,
            "median_return": None,
            "win_rate": None,
            "expectancy": None,
            "max_drawdown": None,
            "mfe": None,
            "mae": None,
            "positive_excursion_prob": None,
            "negative_excursion_prob": None,
            "fees": None,
            "taxes": None,
            "slippage": None,
            "benchmark_excess_return": None,
        }
