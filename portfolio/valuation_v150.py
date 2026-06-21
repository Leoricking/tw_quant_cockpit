"""
portfolio/valuation_v150.py — Portfolio Valuation Engine v1.5.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No mock price for formal valuation. Primary source required.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Optional
import datetime

_VALUATION_VERSION = "1.5.0"

# Price authority tiers
PRIMARY_AUTHORITIES = {"TWSE", "TPEX"}
SECONDARY_AUTHORITIES = {"FINMIND"}
MOCK_AUTHORITIES = {"MOCK", "FIXTURE", "TEST"}


class PortfolioValuationEngine:
    """
    Values a portfolio using provider-sourced prices with quality/authority checks.
    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] No silent fallback to secondary. No mock price for formal valuation.
    """
    VERSION = _VALUATION_VERSION

    def value_positions(
        self,
        positions: List[Dict[str, Any]],
        price_map: Dict[str, Dict[str, Any]],  # symbol -> {price, authority, as_of, available_from, quality, lineage_id}
        as_of: str,
        cash_twd: Decimal = Decimal("0"),
    ) -> Dict[str, Any]:
        """
        Value all positions. Returns PortfolioValuation-compatible dict.
        price_map must have authority, available_from, as_of for each symbol.
        """
        position_valuations = []
        missing_symbols = []
        stale_symbols = []
        blocked_symbols = []
        securities_value = Decimal("0")
        total_cost = Decimal("0")
        unrealized_pnl = Decimal("0")
        status = "VALID"

        for pos in positions:
            symbol = pos.get("symbol", "")
            qty = Decimal(str(pos.get("quantity", "0")))
            avg_cost = Decimal(str(pos.get("average_cost", "0")))
            cost_val = avg_cost * qty

            price_info = price_map.get(symbol)
            if not price_info:
                missing_symbols.append(symbol)
                status = "PARTIAL"
                position_valuations.append({
                    "symbol": symbol, "quantity": qty,
                    "average_cost": avg_cost, "market_price": None,
                    "market_value": None, "cost_value": cost_val,
                    "unrealized_pnl": None, "valuation_status": "MISSING",
                })
                continue

            authority = price_info.get("authority", "")
            avail = price_info.get("available_from", "")
            price = Decimal(str(price_info.get("price", "0")))

            # Block mock price for formal valuation
            if authority in MOCK_AUTHORITIES:
                blocked_symbols.append(symbol)
                status = "PARTIAL"
                position_valuations.append({
                    "symbol": symbol, "quantity": qty,
                    "average_cost": avg_cost, "market_price": price,
                    "market_value": None, "cost_value": cost_val,
                    "unrealized_pnl": None, "valuation_status": "BLOCKED",
                    "price_authority": authority,
                })
                continue

            # PIT check
            if avail > as_of:
                blocked_symbols.append(symbol)
                status = "PARTIAL"
                position_valuations.append({
                    "symbol": symbol, "quantity": qty,
                    "average_cost": avg_cost, "market_price": price,
                    "market_value": None, "cost_value": cost_val,
                    "unrealized_pnl": None, "valuation_status": "BLOCKED",
                    "price_authority": authority, "pit_violation": True,
                })
                continue

            mkt_val = price * qty
            upnl = mkt_val - cost_val
            securities_value += mkt_val
            total_cost += cost_val
            unrealized_pnl += upnl

            pv = {
                "symbol": symbol, "quantity": qty,
                "average_cost": avg_cost,
                "market_price": price,
                "market_value": mkt_val,
                "cost_value": cost_val,
                "unrealized_pnl": upnl,
                "unrealized_return": upnl / cost_val if cost_val != Decimal("0") else None,
                "price_authority": authority,
                "price_as_of": price_info.get("as_of", ""),
                "price_available_from": avail,
                "price_quality": price_info.get("quality", ""),
                "price_lineage_id": price_info.get("lineage_id", ""),
                "valuation_status": "VALID",
            }
            position_valuations.append(pv)

        # Calculate portfolio weights
        total_val = securities_value + cash_twd
        for pv in position_valuations:
            if pv.get("market_value") is not None and total_val > Decimal("0"):
                pv["portfolio_weight"] = pv["market_value"] / total_val

        if missing_symbols or blocked_symbols:
            if len(missing_symbols) + len(blocked_symbols) == len(positions):
                status = "BLOCKED"
            else:
                status = "PARTIAL"

        return {
            "portfolio_id": positions[0].get("portfolio_id", "") if positions else "",
            "as_of": as_of,
            "cash_value": cash_twd,
            "securities_value": securities_value,
            "total_value": securities_value + cash_twd,
            "total_cost": total_cost,
            "unrealized_pnl": unrealized_pnl,
            "valuation_status": status,
            "missing_symbols": missing_symbols,
            "stale_symbols": stale_symbols,
            "blocked_symbols": blocked_symbols,
            "position_valuations": position_valuations,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
