"""
portfolio/what_if_v150.py — Hypothetical what-if analysis for v1.5.0.

ALL HYPOTHETICAL. No orders created. No transactions persisted. No broker calls.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
HYPOTHETICAL_ONLY = True
NO_ORDER_CREATED = True
NO_TRANSACTION_PERSISTED = True
NO_BROKER_CALL = True

_WHAT_IF_DISCLAIMER = (
    "HYPOTHETICAL_ONLY. NO_ORDER_CREATED. NO_TRANSACTION_PERSISTED. NO_BROKER_CALL. "
    "Research purposes only. Not investment advice."
)


class PortfolioWhatIfAnalyzer:
    RESEARCH_ONLY = True
    HYPOTHETICAL_ONLY = True
    NO_ORDER_CREATED = True
    NO_TRANSACTION_PERSISTED = True
    NO_BROKER_CALL = True

    def simulate_buy(
        self,
        current_positions: List[Dict],
        current_cash_twd: Decimal,
        symbol: str,
        quantity: Decimal,
        price_twd: Decimal,
        fee_twd: Decimal = Decimal("0"),
    ) -> Dict[str, Any]:
        """
        Simulate a hypothetical buy. Returns projected state WITHOUT persisting anything.
        """
        gross = Decimal(str(quantity)) * Decimal(str(price_twd))
        total_cost = gross + Decimal(str(fee_twd))
        projected_cash = Decimal(str(current_cash_twd)) - total_cost

        feasible = projected_cash >= Decimal("0")

        return {
            "action": "HYPOTHETICAL_BUY",
            "symbol": symbol,
            "quantity": Decimal(str(quantity)),
            "price_twd": Decimal(str(price_twd)),
            "gross_twd": gross,
            "fee_twd": Decimal(str(fee_twd)),
            "total_cost_twd": total_cost,
            "projected_cash_twd": projected_cash,
            "feasible": feasible,
            "infeasibility_reason": None if feasible else "INSUFFICIENT_CASH",
            "disclaimer": _WHAT_IF_DISCLAIMER,
            "research_only": True,
            "no_order_created": True,
            "no_transaction_persisted": True,
        }

    def simulate_sell(
        self,
        current_positions: List[Dict],
        symbol: str,
        quantity: Decimal,
        price_twd: Decimal,
        fee_twd: Decimal = Decimal("0"),
        tax_twd: Decimal = Decimal("0"),
    ) -> Dict[str, Any]:
        """
        Simulate a hypothetical sell. Returns projected state WITHOUT persisting anything.
        """
        # Find current position
        current_qty = Decimal("0")
        for pos in current_positions:
            if pos.get("symbol") == symbol:
                current_qty = Decimal(str(pos.get("quantity", 0)))
                break

        qty = Decimal(str(quantity))
        feasible = current_qty >= qty
        gross = qty * Decimal(str(price_twd))
        net_proceeds = gross - Decimal(str(fee_twd)) - Decimal(str(tax_twd))

        return {
            "action": "HYPOTHETICAL_SELL",
            "symbol": symbol,
            "quantity": qty,
            "price_twd": Decimal(str(price_twd)),
            "gross_twd": gross,
            "fee_twd": Decimal(str(fee_twd)),
            "tax_twd": Decimal(str(tax_twd)),
            "net_proceeds_twd": net_proceeds,
            "current_quantity": current_qty,
            "feasible": feasible,
            "infeasibility_reason": None if feasible else "INSUFFICIENT_QUANTITY",
            "disclaimer": _WHAT_IF_DISCLAIMER,
            "research_only": True,
            "no_order_created": True,
            "no_transaction_persisted": True,
        }

    def simulate_rebalance(
        self,
        current_positions: List[Dict],
        target_weights: Dict[str, Decimal],
        total_value_twd: Decimal,
        current_prices: Dict[str, Decimal],
    ) -> Dict[str, Any]:
        """
        Simulate hypothetical rebalance. HYPOTHETICAL ONLY — no orders, no persistence.
        """
        trades = []
        total = Decimal(str(total_value_twd))

        current_weights: Dict[str, Decimal] = {}
        current_values: Dict[str, Decimal] = {}
        if total > Decimal("0"):
            for pos in current_positions:
                sym = pos.get("symbol", "")
                mkt_val = Decimal(str(pos.get("market_value_twd", 0) or 0))
                current_values[sym] = mkt_val
                current_weights[sym] = mkt_val / total

        for sym, target_w in target_weights.items():
            target_val = Decimal(str(target_w)) * total
            current_val = current_values.get(sym, Decimal("0"))
            diff_val = target_val - current_val

            if sym in current_prices and current_prices[sym] > Decimal("0"):
                diff_qty = diff_val / Decimal(str(current_prices[sym]))
            else:
                diff_qty = None

            trades.append({
                "symbol": sym,
                "target_weight": Decimal(str(target_w)),
                "current_weight": current_weights.get(sym, Decimal("0")),
                "target_value_twd": target_val,
                "current_value_twd": current_val,
                "diff_value_twd": diff_val,
                "diff_quantity": diff_qty,
                "action": "BUY" if diff_val > 0 else ("SELL" if diff_val < 0 else "HOLD"),
            })

        return {
            "action": "HYPOTHETICAL_REBALANCE",
            "trades": trades,
            "disclaimer": _WHAT_IF_DISCLAIMER,
            "research_only": True,
            "no_order_created": True,
            "no_transaction_persisted": True,
            "no_broker_call": True,
        }
