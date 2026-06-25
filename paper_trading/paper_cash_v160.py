"""paper_trading/paper_cash_v160.py — Paper Cash & Settlement v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY. PAPER_ONLY.
Settlement model: SIMPLIFIED_PAPER_SETTLEMENT (not real T+2 Taiwan settlement).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from .enums_v160 import PaperOrderSide
from .models_v160 import PaperCashBalance

_SETTLEMENT_DISCLAIMER = "SIMPLIFIED_PAPER_SETTLEMENT: not real T+2 Taiwan settlement"


class PaperCashManager:
    """Manages paper cash: opening, available, reserved, settled. Paper-only."""

    def __init__(self, session_id: str, initial_cash: Decimal, currency: str = "TWD") -> None:
        self._balance = PaperCashBalance(
            session_id=session_id,
            currency=currency,
            opening_cash=initial_cash,
            available_cash=initial_cash,
            reserved_cash=Decimal("0"),
            settled_cash=initial_cash,
        )
        self._settlement_note = _SETTLEMENT_DISCLAIMER

    def get_balance(self) -> PaperCashBalance:
        return self._balance

    def reserve_for_order(self, amount: Decimal, order_id: str) -> bool:
        """Reserve cash for a buy order. Returns False if insufficient."""
        if amount <= Decimal("0"):
            return False
        if self._balance.available_cash < amount:
            return False
        self._balance.available_cash -= amount
        self._balance.reserved_cash += amount
        return True

    def release_reservation(self, amount: Decimal) -> None:
        """Release reserved cash (cancelled/rejected order)."""
        actual = min(amount, self._balance.reserved_cash)
        self._balance.reserved_cash -= actual
        self._balance.available_cash += actual

    def apply_buy_fill(self, gross_amount: Decimal, fee: Decimal, reserved: Decimal) -> None:
        """Apply buy fill: reduce reserved by reserved amount, add to settled."""
        cost = gross_amount + fee
        release_excess = max(reserved - cost, Decimal("0"))
        actual_used = min(reserved, cost)
        self._balance.reserved_cash -= actual_used
        if release_excess > Decimal("0"):
            self._balance.available_cash += release_excess
            self._balance.reserved_cash -= release_excess
        self._balance.settled_cash -= cost
        self._balance.total_fees += fee

    def apply_sell_fill(self, gross_amount: Decimal, fee: Decimal, tax: Decimal) -> None:
        """Apply sell fill: receive proceeds into available and settled."""
        proceeds = gross_amount - fee - tax
        self._balance.available_cash += proceeds
        self._balance.settled_cash += proceeds
        self._balance.realized_pnl += proceeds
        self._balance.total_fees += fee
        self._balance.total_taxes += tax

    def apply_partial_fill_reserve_update(self, filled_amount: Decimal, reserved: Decimal) -> None:
        """Update reserve after partial fill."""
        used = min(filled_amount, self._balance.reserved_cash)
        self._balance.reserved_cash -= used

    @property
    def available_cash(self) -> Decimal:
        return self._balance.available_cash

    @property
    def settlement_note(self) -> str:
        return self._settlement_note
