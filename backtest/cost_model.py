"""
backtest/cost_model.py — Transaction cost model for hardened backtest (v0.3.26).

Taiwan stock default: 0.1425% commission (6-fold discount), 0.3% sell tax, 5 bps slippage.

[!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)

try:
    import math
    _MATH_AVAILABLE = True
except ImportError:
    _MATH_AVAILABLE = False


class CostModel:
    """
    Transaction cost model for Taiwan stock backtesting.

    Defaults reflect realistic retail trading costs:
    - Commission: 0.1425% with 6-fold discount applied
    - Sell tax: 0.3%
    - Slippage: 5 bps
    - Min commission: 20 NTD per trade

    [!] Research / Backtest Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only = True
    no_real_orders = True
    production_blocked = True

    PRESET_TAIWAN_REALISTIC = {
        "commission_rate": 0.001425,
        "commission_discount": 0.6,
        "tax_rate": 0.003,
        "slippage_bps": 5,
        "min_commission": 20,
        "zero_cost": False,
    }

    PRESET_ZERO_COST = {
        "commission_rate": 0.0,
        "commission_discount": 1.0,
        "tax_rate": 0.0,
        "slippage_bps": 0,
        "min_commission": 0,
        "zero_cost": True,
    }

    def __init__(
        self,
        commission_rate: float = 0.001425,
        commission_discount: float = 0.6,
        tax_rate: float = 0.003,
        slippage_bps: float = 5,
        min_commission: float = 20,
        zero_cost: bool = False,
    ) -> None:
        self.commission_rate = commission_rate
        self.commission_discount = commission_discount
        self.tax_rate = tax_rate
        self.slippage_bps = slippage_bps
        self.min_commission = min_commission
        self.zero_cost = zero_cost

        # Effective commission rate after discount
        self._effective_commission = commission_rate * commission_discount

    # ------------------------------------------------------------------
    # Buy cost
    # ------------------------------------------------------------------

    def calculate_buy_cost(self, trade_value: float) -> dict:
        """
        Calculate total cost of a buy trade.

        Returns:
            commission, slippage_cost, total_cost, effective_price_factor
        """
        if self.zero_cost or trade_value <= 0:
            return {
                "commission": 0.0,
                "slippage_cost": 0.0,
                "total_cost": 0.0,
                "effective_price_factor": 1.0,
            }

        commission = max(
            trade_value * self._effective_commission,
            float(self.min_commission),
        )
        slippage_cost = trade_value * (self.slippage_bps / 10000.0)
        total_cost = commission + slippage_cost
        effective_price_factor = 1.0 + (total_cost / trade_value) if trade_value > 0 else 1.0

        return {
            "commission": round(commission, 4),
            "slippage_cost": round(slippage_cost, 4),
            "total_cost": round(total_cost, 4),
            "effective_price_factor": round(effective_price_factor, 6),
        }

    # ------------------------------------------------------------------
    # Sell cost
    # ------------------------------------------------------------------

    def calculate_sell_cost(self, trade_value: float) -> dict:
        """
        Calculate total cost of a sell trade.

        Returns:
            commission, tax, slippage_cost, total_cost, effective_price_factor
        """
        if self.zero_cost or trade_value <= 0:
            return {
                "commission": 0.0,
                "tax": 0.0,
                "slippage_cost": 0.0,
                "total_cost": 0.0,
                "effective_price_factor": 1.0,
            }

        commission = max(
            trade_value * self._effective_commission,
            float(self.min_commission),
        )
        tax = trade_value * self.tax_rate
        slippage_cost = trade_value * (self.slippage_bps / 10000.0)
        total_cost = commission + tax + slippage_cost
        effective_price_factor = 1.0 - (total_cost / trade_value) if trade_value > 0 else 1.0

        return {
            "commission": round(commission, 4),
            "tax": round(tax, 4),
            "slippage_cost": round(slippage_cost, 4),
            "total_cost": round(total_cost, 4),
            "effective_price_factor": round(effective_price_factor, 6),
        }

    # ------------------------------------------------------------------
    # Round trip
    # ------------------------------------------------------------------

    def apply_round_trip_cost(
        self,
        entry_price: float,
        exit_price: float,
        shares: int,
    ) -> dict:
        """
        Apply round-trip cost to a trade.

        Returns:
            gross_pnl, buy_cost, sell_cost, total_cost, net_pnl, cost_impact_pct
        """
        try:
            entry_value = entry_price * shares
            exit_value = exit_price * shares
            gross_pnl = exit_value - entry_value

            buy_costs = self.calculate_buy_cost(entry_value)
            sell_costs = self.calculate_sell_cost(exit_value)

            buy_cost = buy_costs["total_cost"]
            sell_cost = sell_costs["total_cost"]
            total_cost = buy_cost + sell_cost
            net_pnl = gross_pnl - total_cost
            cost_impact_pct = (total_cost / entry_value * 100.0) if entry_value > 0 else 0.0

            return {
                "gross_pnl": round(gross_pnl, 4),
                "buy_cost": round(buy_cost, 4),
                "sell_cost": round(sell_cost, 4),
                "total_cost": round(total_cost, 4),
                "net_pnl": round(net_pnl, 4),
                "cost_impact_pct": round(cost_impact_pct, 4),
            }
        except Exception as exc:
            logger.error("apply_round_trip_cost error: %s", exc)
            return {
                "gross_pnl": 0.0,
                "buy_cost": 0.0,
                "sell_cost": 0.0,
                "total_cost": 0.0,
                "net_pnl": 0.0,
                "cost_impact_pct": 0.0,
            }

    # ------------------------------------------------------------------
    # Slippage estimation
    # ------------------------------------------------------------------

    def estimate_slippage(
        self,
        price: float,
        side: str = "buy",
        volume: float | None = None,
        trade_volume: float | None = None,
    ) -> float:
        """
        Estimate slippage for a trade.

        If volume and trade_volume provided and participation > 2%, increase slippage.
        """
        if self.zero_cost or price <= 0:
            return 0.0

        base_slippage = price * (self.slippage_bps / 10000.0)

        if volume is not None and trade_volume is not None and volume > 0:
            participation = trade_volume / volume
            if participation > 0.02:
                # Scale slippage proportionally beyond 2% participation
                scale = 1.0 + (participation - 0.02) * 10.0
                base_slippage *= min(scale, 5.0)  # cap at 5x

        return round(base_slippage, 4)

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def build_assumption_dict(self) -> dict:
        """Return all model parameters as a dictionary for reporting."""
        return {
            "commission_rate": self.commission_rate,
            "commission_discount": self.commission_discount,
            "effective_commission_rate": self._effective_commission,
            "tax_rate": self.tax_rate,
            "slippage_bps": self.slippage_bps,
            "min_commission": self.min_commission,
            "zero_cost": self.zero_cost,
            "read_only": self.read_only,
            "no_real_orders": self.no_real_orders,
            "production_blocked": self.production_blocked,
            "note": "Taiwan realistic: 0.1425% commission * 0.6 discount + 0.3% sell tax + 5bps slippage",
        }

    @classmethod
    def from_preset(cls, preset: str = "taiwan_realistic") -> "CostModel":
        """Create a CostModel from a named preset."""
        if preset in ("taiwan_realistic", "real"):
            return cls(**{k: v for k, v in cls.PRESET_TAIWAN_REALISTIC.items()})
        elif preset in ("zero_cost", "zero"):
            return cls(**{k: v for k, v in cls.PRESET_ZERO_COST.items()})
        else:
            logger.warning("Unknown preset '%s', using taiwan_realistic", preset)
            return cls(**{k: v for k, v in cls.PRESET_TAIWAN_REALISTIC.items()})
