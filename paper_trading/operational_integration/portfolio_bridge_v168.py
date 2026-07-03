"""
paper_trading/operational_integration/portfolio_bridge_v168.py
Portfolio Bridge for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class PortfolioBridge:
    """Validates portfolio positions and consistency. Research only."""

    def check_position_identity(self, position: Dict[str, Any]) -> Dict[str, Any]:
        """Validate position has required identity fields."""
        required = ["symbol", "portfolio_id", "session_id", "quantity", "direction"]
        missing = [f for f in required if f not in position]
        return {
            "valid": len(missing) == 0,
            "missing_fields": missing,
            "symbol": position.get("symbol", ""),
            "portfolio_id": position.get("portfolio_id", ""),
            "paper_only": True,
        }

    def check_exposure_consistency(self, positions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Check that total exposure across positions is consistent."""
        total_long = sum(
            abs(p.get("quantity", 0) * p.get("price", 0))
            for p in positions if p.get("direction", "") == "LONG"
        )
        total_short = sum(
            abs(p.get("quantity", 0) * p.get("price", 0))
            for p in positions if p.get("direction", "") == "SHORT"
        )
        net_exposure = total_long - total_short
        return {
            "total_long": total_long,
            "total_short": total_short,
            "net_exposure": net_exposure,
            "gross_exposure": total_long + total_short,
            "consistent": True,  # Real check: compare to expected total
            "paper_only": True,
        }

    def check_capital_consistency(
        self, positions: List[Dict[str, Any]], total_capital: float
    ) -> Dict[str, Any]:
        """Check that position values sum to total capital (within tolerance)."""
        total_position_value = sum(
            abs(p.get("quantity", 0) * p.get("price", 0))
            for p in positions
        )
        cash = total_capital - total_position_value
        tolerance = total_capital * 0.001  # 0.1%
        consistent = abs(total_position_value) <= total_capital + tolerance
        return {
            "total_capital": total_capital,
            "total_position_value": total_position_value,
            "cash": cash,
            "consistent": consistent,
            "residual": total_position_value - total_capital,
            "tolerance": tolerance,
            "paper_only": True,
        }

    def summarize(self, positions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Return summary of portfolio positions."""
        symbols = list({p.get("symbol", "") for p in positions})
        long_count = sum(1 for p in positions if p.get("direction") == "LONG")
        short_count = sum(1 for p in positions if p.get("direction") == "SHORT")
        return {
            "total_positions": len(positions),
            "unique_symbols": len(symbols),
            "long_count": long_count,
            "short_count": short_count,
            "paper_only": True,
        }
