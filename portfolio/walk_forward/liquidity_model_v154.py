"""
portfolio/walk_forward/liquidity_model_v154.py — Liquidity Model Engine v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
Suspended / missing ADV → BLOCKED. Partial fill hypothetical, simulation_only=True.
"""
from __future__ import annotations
from typing import Any, Dict, Optional

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
LIQUIDITY_MODEL_VERSION = "1.5.4"


class LiquidityModelEngine:
    """Check liquidity constraints for simulated transactions."""

    def __init__(self):
        self.version = LIQUIDITY_MODEL_VERSION

    def check_liquidity(
        self,
        symbol: str,
        quantity: float,
        adv: Optional[float],
        participation_rate: float = 0.10,
        suspended: bool = False,
    ) -> Dict[str, Any]:
        """
        Check liquidity for a simulated position.
        Missing ADV → BLOCKED. Suspended → BLOCKED.
        Returns dict with max_research_quantity, liquidation_days, partial_fill, status.
        """
        if suspended:
            return {
                "symbol": symbol,
                "max_research_quantity": 0,
                "liquidation_days": None,
                "partial_fill": False,
                "status": "BLOCKED",
                "reason": f"{symbol} is suspended",
                "simulation_only": True,
                "research_only": True,
            }

        if adv is None or adv <= 0:
            return {
                "symbol": symbol,
                "max_research_quantity": None,
                "liquidation_days": None,
                "partial_fill": None,
                "status": "BLOCKED",
                "reason": f"Missing or zero ADV for {symbol}",
                "simulation_only": True,
                "research_only": True,
            }

        max_qty = adv * participation_rate
        partial_fill = quantity > max_qty
        liquidation_days = max(1, int(quantity / max_qty + 0.5)) if max_qty > 0 else None

        return {
            "symbol": symbol,
            "quantity_requested": quantity,
            "max_research_quantity": max_qty,
            "liquidation_days": liquidation_days,
            "partial_fill": partial_fill,
            "partial_fill_qty": min(quantity, max_qty) if partial_fill else quantity,
            "adv": adv,
            "participation_rate": participation_rate,
            "status": "PARTIAL" if partial_fill else "VALID",
            "simulation_only": True,
            "research_only": True,
            "executable": False,
        }
