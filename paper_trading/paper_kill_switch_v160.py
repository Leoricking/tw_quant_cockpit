"""paper_trading/paper_kill_switch_v160.py — Paper Kill Switch v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
On trigger: SESSION_HALTED, NO_NEW_PAPER_ORDERS. No auto close-out.
Preserves positions. Cancels queued orders. Human review required.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from .enums_v160 import KillSwitchReason


@dataclass
class KillSwitchEvent:
    triggered: bool
    reason: Optional[KillSwitchReason]
    triggered_at: Optional[str]
    detail: str = ""


class PaperKillSwitch:
    """
    Paper session kill switch.
    Halts new paper orders. Does NOT create sell orders or close positions.
    """

    def __init__(
        self,
        max_session_loss: Optional[Decimal] = None,
        max_drawdown_pct: Optional[Decimal] = None,
        max_rejected_orders: int = 20,
        max_malformed_events: int = 10,
        data_stale_seconds: int = 300,
    ) -> None:
        self._triggered = False
        self._reason: Optional[KillSwitchReason] = None
        self._triggered_at: Optional[str] = None
        self._detail: str = ""
        self._max_session_loss = max_session_loss
        self._max_drawdown_pct = max_drawdown_pct
        self._max_rejected_orders = max_rejected_orders
        self._max_malformed_events = max_malformed_events
        self._data_stale_seconds = data_stale_seconds

    @property
    def is_triggered(self) -> bool:
        return self._triggered

    def trigger(self, reason: KillSwitchReason, detail: str = "") -> KillSwitchEvent:
        if not self._triggered:
            self._triggered = True
            self._reason = reason
            self._triggered_at = datetime.now(timezone.utc).isoformat()
            self._detail = detail
        return self.get_event()

    def get_event(self) -> KillSwitchEvent:
        return KillSwitchEvent(
            triggered=self._triggered,
            reason=self._reason,
            triggered_at=self._triggered_at,
            detail=self._detail,
        )

    def check_session_loss(self, session_loss: Decimal) -> Optional[KillSwitchEvent]:
        if self._max_session_loss is not None and session_loss >= self._max_session_loss:
            return self.trigger(KillSwitchReason.MAX_SESSION_LOSS, f"loss={session_loss}")
        return None

    def check_drawdown(self, drawdown_pct: Decimal) -> Optional[KillSwitchEvent]:
        if self._max_drawdown_pct is not None and drawdown_pct >= self._max_drawdown_pct:
            return self.trigger(KillSwitchReason.MAX_DRAWDOWN, f"drawdown={drawdown_pct:.2%}")
        return None

    def check_rejected_orders(self, rejected_count: int) -> Optional[KillSwitchEvent]:
        if rejected_count >= self._max_rejected_orders:
            return self.trigger(KillSwitchReason.MAX_REJECTED_ORDERS, f"rejected={rejected_count}")
        return None

    def check_malformed_events(self, malformed_count: int) -> Optional[KillSwitchEvent]:
        if malformed_count >= self._max_malformed_events:
            return self.trigger(KillSwitchReason.MAX_MALFORMED_EVENTS, f"malformed={malformed_count}")
        return None

    def check_data_stale(self, stale: bool) -> Optional[KillSwitchEvent]:
        if stale:
            return self.trigger(KillSwitchReason.DATA_STALE, "data feed stale")
        return None

    def check_data_feed_lost(self, lost: bool) -> Optional[KillSwitchEvent]:
        if lost:
            return self.trigger(KillSwitchReason.DATA_FEED_LOST, "data feed lost")
        return None

    def check_ledger_integrity(self, hash_ok: bool) -> Optional[KillSwitchEvent]:
        if not hash_ok:
            return self.trigger(KillSwitchReason.LEDGER_HASH_MISMATCH, "ledger hash chain broken")
        return None

    def check_reconciliation(self, ok: bool) -> Optional[KillSwitchEvent]:
        if not ok:
            return self.trigger(KillSwitchReason.RECONCILIATION_FAILURE, "reconciliation failed")
        return None

    def check_safety_contract(self, ok: bool) -> Optional[KillSwitchEvent]:
        if not ok:
            return self.trigger(KillSwitchReason.SAFETY_CONTRACT_VIOLATION, "safety contract violated")
        return None

    def manual_halt(self, detail: str = "manual halt") -> KillSwitchEvent:
        return self.trigger(KillSwitchReason.MANUAL_HALT, detail)
