"""
portfolio/walk_forward/slippage_model_v154.py — Slippage Model Engine v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
No negative slippage unless explicitly modelling price improvement.
"""
from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, Optional

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
SLIPPAGE_MODEL_VERSION = "1.5.4"


class SlippageModelEngine:
    """Apply slippage model to simulated transactions."""

    def __init__(self):
        self.version = SLIPPAGE_MODEL_VERSION

    def apply_fixed_bps(self, value: float, bps: float) -> Decimal:
        """Apply fixed basis-points slippage. No negative slippage."""
        if bps < 0:
            raise ValueError("Negative slippage not allowed without explicit price improvement flag")
        v = Decimal(str(value))
        rate = Decimal(str(bps)) / Decimal("10000")
        return (v * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def apply_volume_participation(
        self, value: float, adv: Optional[float], participation: float
    ) -> Dict[str, Any]:
        """
        Apply volume-participation slippage.
        Missing ADV → BLOCKED.
        """
        if adv is None or adv <= 0:
            return {
                "slippage": None,
                "status": "BLOCKED",
                "reason": "Missing or zero ADV — cannot estimate volume participation slippage",
                "research_only": True,
            }
        v = Decimal(str(value))
        part = Decimal(str(participation))
        # Simple linear model: slippage = participation_rate * (order_value / adv) * value
        impact = (part * (v / Decimal(str(adv))) * v).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        impact = max(impact, Decimal("0"))  # No negative slippage
        return {
            "slippage": float(impact),
            "status": "VALID",
            "adv": adv,
            "participation_rate": participation,
            "research_only": True,
        }

    def apply_volatility_adjusted(
        self, value: float, volatility: float, participation: float
    ) -> Dict[str, Any]:
        """
        Apply volatility-adjusted slippage.
        """
        if volatility <= 0:
            return {
                "slippage": None,
                "status": "BLOCKED",
                "reason": "volatility must be > 0",
                "research_only": True,
            }
        v = Decimal(str(value))
        vol = Decimal(str(volatility))
        part = Decimal(str(participation))
        # Simple model: slippage = vol * participation * value
        impact = (vol * part * v).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        impact = max(impact, Decimal("0"))  # No negative slippage
        return {
            "slippage": float(impact),
            "status": "VALID",
            "volatility": volatility,
            "participation_rate": participation,
            "research_only": True,
        }
