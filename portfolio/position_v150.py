"""
portfolio/position_v150.py — Portfolio Position Service v1.5.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List

_POSITION_VERSION = "1.5.0"


class PortfolioPositionService:
    """
    Derives portfolio positions from ledger replay.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """
    VERSION = _POSITION_VERSION

    def get_positions_as_of(self, ledger_replay: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert ledger replay output to list of position dicts."""
        positions = ledger_replay.get("positions", {})
        result = []
        for symbol, pos in positions.items():
            result.append({
                "portfolio_id": ledger_replay.get("portfolio_id", ""),
                "symbol": symbol,
                "quantity": pos.get("quantity", Decimal("0")),
                "average_cost": pos.get("average_cost", Decimal("0")),
                "total_cost": pos.get("total_cost", Decimal("0")),
                "realized_pnl": ledger_replay.get("realized_pnl", {}).get(symbol, Decimal("0")),
                "transaction_ids": pos.get("transaction_ids", []),
                "effective_at": ledger_replay.get("as_of", ""),
            })
        return result

    def get_open_symbols(self, ledger_replay: Dict[str, Any]) -> List[str]:
        return list(ledger_replay.get("positions", {}).keys())
