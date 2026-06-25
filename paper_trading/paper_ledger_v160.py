"""paper_trading/paper_ledger_v160.py — Paper Ledger v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY. PAPER_ONLY.
Append-only, immutable, hash-chained. Completely isolated from formal Portfolio Ledger.
No import of formal Portfolio Ledger writer. No production order table writes.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from .models_v160 import PaperLedgerEntry


class PaperLedger:
    """
    Append-only, hash-chained paper ledger.
    Completely isolated from formal Portfolio Ledger.
    paper_only=True on every entry.
    """

    def __init__(self, session_id: str) -> None:
        self._session_id = session_id
        self._entries: List[PaperLedgerEntry] = []
        self._last_hash: str = "GENESIS"

    def append(
        self,
        event_type: str,
        paper_order_id: str = "",
        fill_id: str = "",
        symbol: str = "",
        quantity_delta: Decimal = Decimal("0"),
        cash_delta: Decimal = Decimal("0"),
        fee: Decimal = Decimal("0"),
        tax: Decimal = Decimal("0"),
        timestamp: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> PaperLedgerEntry:
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat()
        entry_id = f"led_{uuid.uuid4().hex[:12]}"
        sequence = len(self._entries)
        entry = PaperLedgerEntry(
            entry_id=entry_id,
            session_id=self._session_id,
            sequence=sequence,
            event_type=event_type,
            paper_order_id=paper_order_id,
            fill_id=fill_id,
            symbol=symbol,
            quantity_delta=quantity_delta,
            cash_delta=cash_delta,
            fee=fee,
            tax=tax,
            timestamp=timestamp,
            previous_hash=self._last_hash,
            paper_only=True,
            metadata=metadata or {},
        )
        entry.content_hash = entry.compute_hash()
        self._entries.append(entry)
        self._last_hash = entry.content_hash
        return entry

    def get_entries(self) -> List[PaperLedgerEntry]:
        return list(self._entries)

    def verify_chain(self) -> bool:
        prev = "GENESIS"
        for entry in self._entries:
            if entry.previous_hash != prev:
                return False
            expected = entry.compute_hash()
            if entry.content_hash != expected:
                return False
            prev = entry.content_hash
        return True

    def current_hash(self) -> str:
        return self._last_hash

    def count(self) -> int:
        return len(self._entries)

    def reconstruct_cash(self) -> Decimal:
        return sum((e.cash_delta for e in self._entries), Decimal("0"))

    def reconstruct_position(self, symbol: str) -> Decimal:
        return sum(
            (e.quantity_delta for e in self._entries if e.symbol == symbol),
            Decimal("0"),
        )
