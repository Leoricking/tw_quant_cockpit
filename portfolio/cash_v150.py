"""
portfolio/cash_v150.py — Portfolio Cash Service v1.5.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List

_CASH_VERSION = "1.5.0"


class PortfolioCashService:
    """
    Derives cash balances from ledger replay.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """
    VERSION = _CASH_VERSION

    def get_cash_as_of(self, ledger_replay: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert ledger replay cash to list of CashBalance dicts."""
        cash = ledger_replay.get("cash", {})
        result = []
        for currency, amount in cash.items():
            result.append({
                "portfolio_id": ledger_replay.get("portfolio_id", ""),
                "currency": currency,
                "amount": amount,
                "effective_at": ledger_replay.get("as_of", ""),
            })
        return result

    def total_cash_twd(self, ledger_replay: Dict[str, Any]) -> Decimal:
        """Return total TWD cash (for now just TWD; FX not supported)."""
        cash = ledger_replay.get("cash", {})
        return cash.get("TWD", Decimal("0"))

    def has_negative_cash(self, ledger_replay: Dict[str, Any]) -> bool:
        cash = ledger_replay.get("cash", {})
        return any(v < Decimal("0") for v in cash.values())
