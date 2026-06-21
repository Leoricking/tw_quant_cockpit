"""
portfolio/ledger_v150.py — Append-only Portfolio Ledger v1.5.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Transactions are immutable. Corrections use adjustment entries.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Optional
import datetime

_LEDGER_VERSION = "1.5.0"
RESEARCH_ONLY = True
BROKER_LINKED = False
REAL_ORDER_ENABLED = False


class LedgerError(Exception):
    """Raised when ledger invariant is violated."""


class PortfolioLedger:
    """
    Append-only research portfolio ledger.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """
    VERSION = _LEDGER_VERSION

    def __init__(self):
        self._transactions: List[Dict[str, Any]] = []
        self._seen_ids: set = set()

    def append(self, txn: Dict[str, Any]) -> Dict[str, Any]:
        """Append a transaction. Returns {ok, transaction_id, error}."""
        tid = txn.get("transaction_id", "")
        if not tid:
            return {"ok": False, "transaction_id": "", "error": "transaction_id required"}
        if tid in self._seen_ids:
            return {"ok": False, "transaction_id": tid, "error": f"duplicate transaction_id={tid!r}"}
        if txn.get("research_only") is not True:
            return {"ok": False, "transaction_id": tid, "error": "research_only must be True"}
        ttype = txn.get("transaction_type", "")
        qty = Decimal(str(txn.get("quantity", "0")))
        # Block unsupported short position
        if ttype == "RESEARCH_SELL":
            available = self._available_quantity(
                txn.get("portfolio_id", ""), txn.get("symbol", ""))
            if qty > available:
                return {"ok": False, "transaction_id": tid,
                        "error": f"BLOCKED_OVERSELL: sell qty={qty} > available={available}"}
        # Block negative long
        if ttype == "RESEARCH_BUY" and qty < Decimal("0"):
            return {"ok": False, "transaction_id": tid,
                    "error": "BLOCKED_UNSUPPORTED_SHORT_POSITION"}
        entry = dict(txn)
        entry["_ledger_seq"] = len(self._transactions)
        entry["_appended_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self._transactions.append(entry)
        self._seen_ids.add(tid)
        return {"ok": True, "transaction_id": tid, "error": None}

    def _available_quantity(self, portfolio_id: str, symbol: str) -> Decimal:
        qty = Decimal("0")
        for t in self._transactions:
            if t.get("portfolio_id") != portfolio_id or t.get("symbol") != symbol:
                continue
            ttype = t.get("transaction_type", "")
            q = Decimal(str(t.get("quantity", "0")))
            if ttype == "RESEARCH_BUY":
                qty += q
            elif ttype == "RESEARCH_SELL":
                qty -= q
            elif ttype == "STOCK_DIVIDEND":
                qty += q
            elif ttype == "SPLIT":
                # split quantity replaces existing
                qty = q
        return qty

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self._transactions)

    def get_for_portfolio(self, portfolio_id: str) -> List[Dict[str, Any]]:
        return [t for t in self._transactions if t.get("portfolio_id") == portfolio_id]

    def get_as_of(self, portfolio_id: str, as_of: str) -> List[Dict[str, Any]]:
        """Return transactions where effective_at <= as_of AND available_from <= as_of."""
        result = []
        for t in self._transactions:
            if t.get("portfolio_id") != portfolio_id:
                continue
            eff = t.get("effective_at", "")
            avail = t.get("available_from", "")
            if eff <= as_of and avail <= as_of:
                result.append(t)
        return result

    def replay(self, portfolio_id: str, as_of: str) -> Dict[str, Any]:
        """
        Deterministic replay of ledger as of date.
        Returns {positions, cash_balances, realized_pnl_by_symbol}.
        """
        txns = self.get_as_of(portfolio_id, as_of)
        txns_sorted = sorted(txns, key=lambda t: (t.get("effective_at", ""), t.get("_ledger_seq", 0)))
        positions: Dict[str, Dict[str, Any]] = {}
        cash: Dict[str, Decimal] = {}
        realized: Dict[str, Decimal] = {}

        for t in txns_sorted:
            symbol = t.get("symbol", "")
            ttype = t.get("transaction_type", "")
            qty = Decimal(str(t.get("quantity", "0")))
            price = Decimal(str(t.get("price", "0")))
            fee = Decimal(str(t.get("fee", "0")))
            tax = Decimal(str(t.get("tax", "0")))
            currency = t.get("currency", "TWD")
            gross = qty * price

            if ttype == "RESEARCH_BUY":
                pos = positions.get(symbol, {"quantity": Decimal("0"),
                                              "total_cost": Decimal("0"),
                                              "average_cost": Decimal("0"),
                                              "transaction_ids": []})
                new_qty = pos["quantity"] + qty
                new_cost = pos["total_cost"] + gross + fee
                avg = new_cost / new_qty if new_qty > 0 else Decimal("0")
                pos.update({"quantity": new_qty, "total_cost": new_cost, "average_cost": avg})
                pos["transaction_ids"].append(t.get("transaction_id", ""))
                positions[symbol] = pos
                cash[currency] = cash.get(currency, Decimal("0")) - (gross + fee + tax)

            elif ttype == "RESEARCH_SELL":
                pos = positions.get(symbol, {"quantity": Decimal("0"),
                                              "total_cost": Decimal("0"),
                                              "average_cost": Decimal("0"),
                                              "transaction_ids": []})
                avg_cost = pos.get("average_cost", Decimal("0"))
                pnl = (price - avg_cost) * qty - fee - tax
                realized[symbol] = realized.get(symbol, Decimal("0")) + pnl
                new_qty = pos["quantity"] - qty
                new_cost = avg_cost * new_qty if new_qty > 0 else Decimal("0")
                pos.update({"quantity": new_qty, "total_cost": new_cost,
                             "average_cost": avg_cost if new_qty > 0 else Decimal("0")})
                pos["transaction_ids"].append(t.get("transaction_id", ""))
                positions[symbol] = pos
                cash[currency] = cash.get(currency, Decimal("0")) + gross - fee - tax

            elif ttype == "CASH_DEPOSIT":
                amt = Decimal(str(t.get("net_amount", str(gross))))
                cash[currency] = cash.get(currency, Decimal("0")) + amt

            elif ttype == "CASH_WITHDRAWAL":
                amt = Decimal(str(t.get("net_amount", str(gross))))
                cash[currency] = cash.get(currency, Decimal("0")) - amt

            elif ttype == "DIVIDEND":
                amt = Decimal(str(t.get("net_amount", str(gross))))
                cash[currency] = cash.get(currency, Decimal("0")) + amt

            elif ttype in ("FEE", "TAX"):
                amt = Decimal(str(t.get("net_amount", str(fee + tax))))
                cash[currency] = cash.get(currency, Decimal("0")) - abs(amt)

            elif ttype == "STOCK_DIVIDEND":
                pos = positions.get(symbol, {"quantity": Decimal("0"),
                                              "total_cost": Decimal("0"),
                                              "average_cost": Decimal("0"),
                                              "transaction_ids": []})
                new_qty = pos["quantity"] + qty
                # Stock dividend: add shares at 0 cost; adjust average cost
                avg = pos["total_cost"] / new_qty if new_qty > 0 else Decimal("0")
                pos.update({"quantity": new_qty, "average_cost": avg})
                pos["transaction_ids"].append(t.get("transaction_id", ""))
                positions[symbol] = pos

            elif ttype == "SPLIT":
                pos = positions.get(symbol, {"quantity": Decimal("0"),
                                              "total_cost": Decimal("0"),
                                              "average_cost": Decimal("0"),
                                              "transaction_ids": []})
                # qty is the new total quantity after split
                old_cost = pos["total_cost"]
                new_qty = qty
                avg = old_cost / new_qty if new_qty > 0 else Decimal("0")
                pos.update({"quantity": new_qty, "average_cost": avg})
                pos["transaction_ids"].append(t.get("transaction_id", ""))
                positions[symbol] = pos

        # Remove zero-quantity positions
        open_positions = {s: p for s, p in positions.items() if p["quantity"] > Decimal("0")}
        return {
            "portfolio_id": portfolio_id,
            "as_of": as_of,
            "positions": open_positions,
            "cash": dict(cash),
            "realized_pnl": dict(realized),
            "transaction_count": len(txns_sorted),
        }

    def count(self) -> int:
        return len(self._transactions)

    def has_transaction(self, transaction_id: str) -> bool:
        return transaction_id in self._seen_ids
