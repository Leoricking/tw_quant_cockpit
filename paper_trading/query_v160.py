"""paper_trading/query_v160.py — Paper Trading Query Service v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
Forbidden: submit_real_order, connect_broker, sync_real_account, apply_to_real_portfolio, execute_real_trade.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, List, Optional

from .enums_v160 import DataMode, PaperOrderSide, PaperOrderType, PaperSessionStatus
from .models_v160 import PaperSessionConfig
from .session_v160 import PaperTradingSessionEngine
from .store_v160 import PaperTradingStore
from .session_replay_v160 import PaperSessionReplay
from .recovery_v160 import PaperSessionRecovery
from .reproducibility_v160 import ReproducibilityService
from .lineage_v160 import PaperLineageService
from .explain_v160 import PaperSessionExplainer


class PaperTradingQueryService:
    """
    Public API for paper trading. No real orders, no broker, no real account sync.
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, PaperTradingSessionEngine] = {}
        self._store = PaperTradingStore()
        self._replay_service = PaperSessionReplay()
        self._recovery_service = PaperSessionRecovery()
        self._reproducibility = ReproducibilityService()
        self._explainer = PaperSessionExplainer()

    # --- Session lifecycle ---

    def create_paper_session(self, config: PaperSessionConfig) -> PaperTradingSessionEngine:
        engine = PaperTradingSessionEngine(config)
        self._sessions[config.session_id] = engine
        self._store.save_session(config.session_id, {"session_id": config.session_id, "status": "CREATED"})
        return engine

    def start_paper_session(self, session_id: str) -> None:
        self._get_engine(session_id).start()

    def pause_paper_session(self, session_id: str) -> None:
        self._get_engine(session_id).pause()

    def resume_paper_session(self, session_id: str) -> None:
        self._get_engine(session_id).resume()

    def halt_paper_session(self, session_id: str, reason: str = "") -> None:
        self._get_engine(session_id).halt(reason=reason)

    def complete_paper_session(self, session_id: str) -> None:
        self._get_engine(session_id).complete()

    def get_paper_session(self, session_id: str) -> Optional[PaperTradingSessionEngine]:
        return self._sessions.get(session_id)

    def list_paper_sessions(self) -> List[str]:
        return list(self._sessions.keys())

    # --- Market events ---

    def ingest_market_event(self, session_id: str, event: Any) -> None:
        self._get_engine(session_id).ingest_market_event(event)

    # --- Orders ---

    def submit_paper_order(
        self,
        session_id: str,
        client_order_id: str,
        symbol: str,
        side: PaperOrderSide,
        order_type: PaperOrderType,
        quantity: Decimal,
        limit_price: Optional[Decimal] = None,
        stop_price: Optional[Decimal] = None,
    ) -> Any:
        return self._get_engine(session_id).submit_order(
            client_order_id=client_order_id,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            limit_price=limit_price,
            stop_price=stop_price,
        )

    def cancel_paper_order(self, session_id: str, paper_order_id: str) -> bool:
        return self._get_engine(session_id).cancel_order(paper_order_id)

    def get_paper_order(self, session_id: str, order_id: str) -> Optional[Any]:
        return self._get_engine(session_id).get_order(order_id)

    def list_paper_orders(self, session_id: str) -> List[Any]:
        return self._get_engine(session_id).get_orders()

    def list_paper_fills(self, session_id: str) -> List[Any]:
        return self._store.get_fills(session_id)

    # --- Positions & Cash ---

    def get_paper_positions(self, session_id: str) -> List[Any]:
        return self._get_engine(session_id).get_positions()

    def get_paper_cash(self, session_id: str) -> Any:
        return self._get_engine(session_id).get_cash()

    def get_paper_pnl(self, session_id: str) -> Dict[str, Any]:
        engine = self._get_engine(session_id)
        return {
            "realized_pnl": str(engine._positions.total_realized_pnl()),
            "unrealized_pnl": str(engine._positions.total_unrealized_pnl()),
            "paper_only": True,
        }

    # --- Snapshot ---

    def create_paper_snapshot(self, session_id: str) -> Any:
        return self._get_engine(session_id).create_snapshot()

    # --- Replay & Recovery ---

    def replay_paper_session(self, session_id: str) -> Any:
        engine = self._sessions.get(session_id)
        if engine is None:
            return {"error": "session not found"}
        events = engine.get_event_bus().get_journal().get_events()
        return self._replay_service.replay(session_id, events)

    def recover_paper_session(self, session_id: str) -> Any:
        engine = self._sessions.get(session_id)
        if engine is None:
            return {"error": "session not found"}
        snapshot = engine.get_snapshots()[-1] if engine.get_snapshots() else None
        ledger = engine.get_ledger()
        return self._recovery_service.recover(session_id, snapshot, ledger)

    # --- Audit & Lineage ---

    def verify_paper_ledger(self, session_id: str) -> Dict[str, Any]:
        ledger = self._get_engine(session_id).get_ledger()
        return {"valid": ledger.verify_chain(), "entries": ledger.count()}

    def get_paper_lineage(self, session_id: str) -> Dict[str, Any]:
        return {
            "session_id": session_id,
            "paper_only": True,
            "research_only": True,
        }

    def explain_paper_session(self, session_id: str) -> Dict[str, Any]:
        engine = self._sessions.get(session_id)
        if engine is None:
            return {"error": "session not found"}
        return self._explainer.explain_session(
            session_id=session_id,
            status=engine.status.value,
            data_mode=engine.config.data_mode.value,
        )

    def simulate_paper_execution(self, session_id: str, event: Any) -> None:
        self.ingest_market_event(session_id, event)

    # --- Forbidden methods (raise to prevent misuse) ---

    def submit_real_order(self, *args, **kwargs):
        raise NotImplementedError("submit_real_order is FORBIDDEN in paper trading — NO REAL ORDERS")

    def connect_broker(self, *args, **kwargs):
        raise NotImplementedError("connect_broker is FORBIDDEN — NO BROKER CONNECTION")

    def sync_real_account(self, *args, **kwargs):
        raise NotImplementedError("sync_real_account is FORBIDDEN — NO REAL ACCOUNT SYNC")

    def apply_to_real_portfolio(self, *args, **kwargs):
        raise NotImplementedError("apply_to_real_portfolio is FORBIDDEN — PAPER ONLY")

    def execute_real_trade(self, *args, **kwargs):
        raise NotImplementedError("execute_real_trade is FORBIDDEN — PRODUCTION TRADING BLOCKED")

    # --- Internal ---

    def _get_engine(self, session_id: str) -> PaperTradingSessionEngine:
        engine = self._sessions.get(session_id)
        if engine is None:
            raise KeyError(f"session not found: {session_id}")
        return engine
