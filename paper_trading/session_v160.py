"""paper_trading/session_v160.py — Paper Trading Session Engine v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY. NO_BROKER_CALL.
Deterministic state transitions. Invalid transitions blocked. No Broker call. No real order.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional

from .enums_v160 import (
    DataMode, MarketSessionStatus, PaperEventType,
    PaperOrderSide, PaperOrderStatus, PaperRiskStatus,
    PaperSessionStatus,
)
from .models_v160 import (
    PaperOrder, PaperSessionConfig, PaperSessionSnapshot,
)
from .event_v160 import PaperEvent
from .event_bus_v160 import PaperEventBus
from .snapshot_v160 import SnapshotService
from .audit_v160 import PaperAuditTrail
from .paper_ledger_v160 import PaperLedger
from .paper_cash_v160 import PaperCashManager
from .paper_position_v160 import PaperPositionManager
from .paper_kill_switch_v160 import PaperKillSwitch
from .paper_risk_gate_v160 import PaperRiskGate
from .execution_simulator_v160 import PaperExecutionSimulator
from .order_state_machine_v160 import PaperOrderStateMachine
from .market_session_v160 import TWMarketSessionState
from .data_classification_v160 import DataClassifier
from .validation_v160 import validate_session_config

# Legal session state transitions
_SESSION_TRANSITIONS: Dict[PaperSessionStatus, set] = {
    PaperSessionStatus.CREATED: {PaperSessionStatus.READY},
    PaperSessionStatus.READY: {PaperSessionStatus.RUNNING, PaperSessionStatus.CANCELLED},
    PaperSessionStatus.RUNNING: {
        PaperSessionStatus.PAUSED, PaperSessionStatus.HALTED,
        PaperSessionStatus.COMPLETED, PaperSessionStatus.FAILED,
    },
    PaperSessionStatus.PAUSED: {PaperSessionStatus.RUNNING, PaperSessionStatus.HALTED, PaperSessionStatus.COMPLETED},
    PaperSessionStatus.HALTED: {PaperSessionStatus.RECOVERED},
    PaperSessionStatus.RECOVERED: {PaperSessionStatus.PAUSED, PaperSessionStatus.RUNNING},
    PaperSessionStatus.COMPLETED: set(),
    PaperSessionStatus.FAILED: set(),
    PaperSessionStatus.CANCELLED: set(),
}


class PaperTradingSessionEngine:
    """
    Core paper trading session engine.
    Lifecycle: CREATED → READY → RUNNING → PAUSED ↔ RUNNING → COMPLETED
    Exception: RUNNING → HALTED → RECOVERED → PAUSED/RUNNING
    """

    def __init__(self, config: PaperSessionConfig) -> None:
        ok, errors = validate_session_config(config)
        if not ok:
            raise ValueError(f"Invalid session config: {errors}")
        self._config = config
        self._status = PaperSessionStatus.CREATED
        self._event_bus = PaperEventBus()
        self._audit = PaperAuditTrail(config.session_id)
        self._ledger = PaperLedger(config.session_id)
        self._cash = PaperCashManager(config.session_id, config.initial_cash, config.currency)
        self._positions = PaperPositionManager(config.session_id)
        self._snapshots = SnapshotService()
        self._kill_switch = PaperKillSwitch()
        self._risk_gate = PaperRiskGate()
        self._simulator = PaperExecutionSimulator()
        self._market = TWMarketSessionState()
        self._orders: Dict[str, PaperOrder] = {}
        self._client_order_ids: Dict[str, str] = {}  # client_id -> order_id (idempotency)
        self._rejected_count: int = 0
        self._malformed_event_count: int = 0
        self._created_at = datetime.now(timezone.utc).isoformat()

        # Emit creation event
        self._emit(PaperEventType.SESSION_CREATED, {"session_id": config.session_id})

    # --- Lifecycle ---

    def _transition(self, target: PaperSessionStatus, actor: str = "system", reason: str = "") -> None:
        allowed = _SESSION_TRANSITIONS.get(self._status, set())
        if target not in allowed:
            raise ValueError(f"Invalid transition {self._status.value} → {target.value}")
        before = self._status.value
        self._status = target
        self._audit.record(actor=actor, action=f"transition_{target.value}", reason=reason, before=before, after=target.value)

    def start(self, actor: str = "system") -> None:
        if self._status == PaperSessionStatus.CREATED:
            self._transition(PaperSessionStatus.READY, actor, "prepare")
        self._transition(PaperSessionStatus.RUNNING, actor, "start")
        self._emit(PaperEventType.SESSION_STARTED, {})

    def pause(self, actor: str = "system") -> None:
        self._transition(PaperSessionStatus.PAUSED, actor, "pause")
        self._emit(PaperEventType.SESSION_PAUSED, {})

    def resume(self, actor: str = "system") -> None:
        self._transition(PaperSessionStatus.RUNNING, actor, "resume")
        self._emit(PaperEventType.SESSION_RESUMED, {})

    def halt(self, actor: str = "system", reason: str = "") -> None:
        self._transition(PaperSessionStatus.HALTED, actor, reason or "halt")
        self._emit(PaperEventType.SESSION_HALTED, {"reason": reason})

    def complete(self, actor: str = "system") -> None:
        if self._status == PaperSessionStatus.PAUSED:
            self._transition(PaperSessionStatus.COMPLETED, actor, "complete from paused")
        else:
            self._transition(PaperSessionStatus.COMPLETED, actor, "complete")
        self._emit(PaperEventType.SESSION_COMPLETED, {})

    def recover(self, actor: str = "system") -> None:
        self._transition(PaperSessionStatus.RECOVERED, actor, "recover")
        self._emit(PaperEventType.RECOVERY_COMPLETED, {})

    @property
    def status(self) -> PaperSessionStatus:
        return self._status

    @property
    def config(self) -> PaperSessionConfig:
        return self._config

    # --- Order management ---

    def submit_order(
        self,
        client_order_id: str,
        symbol: str,
        side: PaperOrderSide,
        order_type,
        quantity: Decimal,
        limit_price: Optional[Decimal] = None,
        stop_price: Optional[Decimal] = None,
        actor: str = "user",
    ) -> PaperOrder:
        # Idempotency
        if client_order_id in self._client_order_ids:
            existing_id = self._client_order_ids[client_order_id]
            return self._orders[existing_id]

        if self._kill_switch.is_triggered:
            order = self._create_order(client_order_id, symbol, side, order_type, quantity, limit_price, stop_price)
            order.status = PaperOrderStatus.REJECTED
            order.rejection_reason = "KILL_SWITCH_TRIGGERED"
            self._orders[order.paper_order_id] = order
            self._rejected_count += 1
            self._emit(PaperEventType.PAPER_ORDER_REJECTED, {"order_id": order.paper_order_id, "reason": "KILL_SWITCH"})
            return order

        order = self._create_order(client_order_id, symbol, side, order_type, quantity, limit_price, stop_price)
        self._orders[order.paper_order_id] = order
        self._client_order_ids[client_order_id] = order.paper_order_id

        # Risk gate
        sm = PaperOrderStateMachine(order)
        sm.transition(PaperOrderStatus.VALIDATED)

        eval_id = f"risk_{uuid.uuid4().hex[:8]}"
        risk_result = self._risk_gate.evaluate(
            evaluation_id=eval_id,
            session_id=self._config.session_id,
            paper_order_id=order.paper_order_id,
            symbol=symbol,
            side=side,
            quantity=quantity,
            limit_price=limit_price,
            session_status=self._status,
            market_status=self._market.get_status(),
            data_mode=self._config.data_mode,
            data_fresh=True,
            available_cash=self._cash.available_cash,
            existing_position=self._positions.get_quantity(symbol),
            total_portfolio_value=self._cash.available_cash,
            drawdown_pct=Decimal("0"),
            kill_switch_triggered=self._kill_switch.is_triggered,
            allowed_symbols=self._config.allowed_symbols if self._config.allowed_symbols else None,
            price=limit_price,
        )
        order.risk_evaluation_id = eval_id

        if risk_result.status == PaperRiskStatus.BLOCKED:
            sm.transition(PaperOrderStatus.REJECTED)
            order.rejection_reason = "; ".join(risk_result.block_reasons)
            self._rejected_count += 1
            self._kill_switch.check_rejected_orders(self._rejected_count)
            self._emit(PaperEventType.PAPER_ORDER_REJECTED, {"order_id": order.paper_order_id, "reasons": risk_result.block_reasons})
            return order

        # Reserve cash for buy
        if side == PaperOrderSide.BUY:
            reserve_price = limit_price or Decimal("0")
            reserve_amount = reserve_price * quantity
            if reserve_amount > Decimal("0"):
                self._cash.reserve_for_order(reserve_amount, order.paper_order_id)

        sm.transition(PaperOrderStatus.QUEUED)
        self._ledger.append(
            event_type="ORDER_QUEUED",
            paper_order_id=order.paper_order_id,
            symbol=symbol,
        )
        self._emit(PaperEventType.PAPER_ORDER_QUEUED, {"order_id": order.paper_order_id})
        return order

    def cancel_order(self, paper_order_id: str, actor: str = "user") -> bool:
        order = self._orders.get(paper_order_id)
        if order is None:
            return False
        sm = PaperOrderStateMachine(order)
        if not sm.can_cancel():
            return False
        if order.status == PaperOrderStatus.QUEUED:
            sm.transition(PaperOrderStatus.CANCEL_REQUESTED)
        sm.transition(PaperOrderStatus.CANCELLED)
        # Release cash reservation
        if order.side == PaperOrderSide.BUY:
            reserve_amount = (order.limit_price or Decimal("0")) * order.remaining_quantity
            self._cash.release_reservation(reserve_amount)
        self._emit(PaperEventType.PAPER_ORDER_CANCELLED, {"order_id": paper_order_id})
        return True

    # --- Event ingestion ---

    def ingest_market_event(self, event) -> None:
        # Update market state
        self._emit(PaperEventType.DATA_RECEIVED, {"event_id": event.event_id if hasattr(event, "event_id") else ""})
        # Try to fill queued orders
        for order in list(self._orders.values()):
            sm = PaperOrderStateMachine(order)
            if not sm.can_fill():
                continue
            result = self._simulator.simulate(order, event)
            if result.filled and result.fill is not None:
                fill = result.fill
                # Update order
                order.filled_quantity += fill.quantity
                order.remaining_quantity -= fill.quantity
                order.average_fill_price = fill.price
                order.status = result.new_order_status

                # Update positions
                self._positions.apply_fill(
                    symbol=order.symbol,
                    side=order.side,
                    quantity=fill.quantity,
                    price=fill.price,
                    fee=fill.fee,
                    tax=fill.tax,
                )

                # Update cash
                if order.side == PaperOrderSide.BUY:
                    self._cash.apply_buy_fill(fill.gross_amount, fill.fee, fill.gross_amount)
                else:
                    self._cash.apply_sell_fill(fill.gross_amount, fill.fee, fill.tax)

                # Ledger
                qty_delta = fill.quantity if order.side == PaperOrderSide.BUY else -fill.quantity
                cash_delta = -(fill.gross_amount + fill.fee) if order.side == PaperOrderSide.BUY else (fill.gross_amount - fill.fee - fill.tax)
                self._ledger.append(
                    event_type="FILL",
                    paper_order_id=order.paper_order_id,
                    fill_id=fill.fill_id,
                    symbol=order.symbol,
                    quantity_delta=qty_delta,
                    cash_delta=cash_delta,
                    fee=fill.fee,
                    tax=fill.tax,
                )

                event_type = (PaperEventType.PAPER_ORDER_FILLED
                              if order.status == PaperOrderStatus.FILLED
                              else PaperEventType.PAPER_ORDER_PARTIALLY_FILLED)
                self._emit(event_type, {"order_id": order.paper_order_id, "fill_id": fill.fill_id})

    # --- Snapshot ---

    def create_snapshot(self) -> PaperSessionSnapshot:
        positions = [{"symbol": p.symbol, "quantity": str(p.quantity)} for p in self._positions.get_all_positions()]
        snap = self._snapshots.create(
            session_id=self._config.session_id,
            positions=positions,
            realized_pnl=self._positions.total_realized_pnl(),
            unrealized_pnl=self._positions.total_unrealized_pnl(),
            exposure=self._positions.total_exposure(),
            event_sequence=self._event_bus.event_count(),
            ledger_hash=self._ledger.current_hash(),
        )
        self._emit(PaperEventType.SNAPSHOT_CREATED, {"snapshot_id": snap.snapshot_id})
        return snap

    # --- Accessors ---

    def get_orders(self) -> List[PaperOrder]:
        return list(self._orders.values())

    def get_order(self, order_id: str) -> Optional[PaperOrder]:
        return self._orders.get(order_id)

    def get_cash(self):
        return self._cash.get_balance()

    def get_positions(self):
        return self._positions.get_all_positions()

    def get_ledger(self) -> PaperLedger:
        return self._ledger

    def get_kill_switch(self) -> PaperKillSwitch:
        return self._kill_switch

    def get_event_bus(self) -> PaperEventBus:
        return self._event_bus

    def get_snapshots(self):
        return self._snapshots.get_all()

    # --- Internal ---

    def _create_order(
        self,
        client_order_id: str,
        symbol: str,
        side: PaperOrderSide,
        order_type,
        quantity: Decimal,
        limit_price: Optional[Decimal],
        stop_price: Optional[Decimal],
    ) -> PaperOrder:
        paper_order_id = f"ord_{uuid.uuid4().hex[:12]}"
        return PaperOrder(
            paper_order_id=paper_order_id,
            session_id=self._config.session_id,
            client_order_id=client_order_id,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            limit_price=limit_price,
            stop_price=stop_price,
            created_at=datetime.now(timezone.utc).isoformat(),
            status=PaperOrderStatus.CREATED,
            filled_quantity=Decimal("0"),
            remaining_quantity=quantity,
            research_only=True,
            executable_on_broker=False,
            real_order_created=False,
        )

    def _emit(self, event_type: PaperEventType, payload: Dict[str, Any]) -> PaperEvent:
        seq = self._event_bus.next_sequence()
        idem_key = f"{self._config.session_id}:{event_type.value}:{seq}"
        event = PaperEvent(
            event_id=f"evt_{uuid.uuid4().hex[:12]}",
            sequence=seq,
            event_type=event_type,
            session_id=self._config.session_id,
            idempotency_key=idem_key,
            timestamp=datetime.now(timezone.utc).isoformat(),
            payload=payload,
        )
        return self._event_bus.publish(event)
