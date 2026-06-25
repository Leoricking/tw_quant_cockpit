"""paper_trading/order_state_machine_v160.py — Paper Order State Machine v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY. NO_BROKER_CALL.
"""
from __future__ import annotations
from typing import Dict, Set

from .enums_v160 import PaperOrderStatus

# Legal transitions
_TRANSITIONS: Dict[PaperOrderStatus, Set[PaperOrderStatus]] = {
    PaperOrderStatus.CREATED: {
        PaperOrderStatus.VALIDATED,
        PaperOrderStatus.REJECTED,
    },
    PaperOrderStatus.VALIDATED: {
        PaperOrderStatus.QUEUED,
        PaperOrderStatus.REJECTED,
    },
    PaperOrderStatus.QUEUED: {
        PaperOrderStatus.PARTIALLY_FILLED,
        PaperOrderStatus.FILLED,
        PaperOrderStatus.CANCEL_REQUESTED,
        PaperOrderStatus.EXPIRED,
        PaperOrderStatus.HALTED,
    },
    PaperOrderStatus.PARTIALLY_FILLED: {
        PaperOrderStatus.FILLED,
        PaperOrderStatus.CANCEL_REQUESTED,
        PaperOrderStatus.HALTED,
        PaperOrderStatus.EXPIRED,
    },
    PaperOrderStatus.CANCEL_REQUESTED: {
        PaperOrderStatus.CANCELLED,
    },
    # Terminal states — no further transitions
    PaperOrderStatus.FILLED: set(),
    PaperOrderStatus.REJECTED: set(),
    PaperOrderStatus.CANCELLED: set(),
    PaperOrderStatus.EXPIRED: set(),
    PaperOrderStatus.HALTED: set(),
}

_TERMINAL_STATES = {
    PaperOrderStatus.FILLED,
    PaperOrderStatus.REJECTED,
    PaperOrderStatus.CANCELLED,
    PaperOrderStatus.EXPIRED,
    PaperOrderStatus.HALTED,
}


class PaperOrderStateMachine:
    def __init__(self, order) -> None:
        self._order = order

    def can_transition(self, target: PaperOrderStatus) -> bool:
        allowed = _TRANSITIONS.get(self._order.status, set())
        return target in allowed

    def transition(self, target: PaperOrderStatus) -> None:
        if not self.can_transition(target):
            raise ValueError(
                f"Invalid transition {self._order.status.value} → {target.value} "
                f"for order {self._order.paper_order_id}"
            )
        self._order.status = target

    def is_terminal(self) -> bool:
        return self._order.status in _TERMINAL_STATES

    def can_fill(self) -> bool:
        return self._order.status in {
            PaperOrderStatus.QUEUED,
            PaperOrderStatus.PARTIALLY_FILLED,
        }

    def can_cancel(self) -> bool:
        return self._order.status in {
            PaperOrderStatus.QUEUED,
            PaperOrderStatus.PARTIALLY_FILLED,
            PaperOrderStatus.CANCEL_REQUESTED,
        }
