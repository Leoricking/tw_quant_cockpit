"""gui/live_paper_trading_panel.py — Live Paper Trading GUI Panel v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. NO BROKER. PRODUCTION TRADING: BLOCKED.
Headless-safe: no QApplication import crash. No QThread leak.
Navigation: tab_id=live_paper_trading, group=paper_trading, priority=P1.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

# ---- Safety Banner (always visible) ----
SAFETY_BANNER = [
    "PAPER TRADING ONLY",
    "NO REAL ORDERS",
    "NO BROKER CONNECTION",
    "NO REAL ACCOUNT",
    "PRODUCTION TRADING BLOCKED",
]

# ---- Navigation metadata ----
PANEL_METADATA = {
    "tab_id": "live_paper_trading",
    "display_name": "Live Paper Trading",
    "group": "paper_trading",
    "priority": "P1",
    "paper_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "production_trading_blocked": True,
}

# ---- Forbidden actions (raise if called) ----
FORBIDDEN_ACTIONS = [
    "connect_broker",
    "real_buy",
    "real_sell",
    "send_order",
    "sync_account",
    "apply_live",
]


class LivePaperTradingPanel:
    """
    Headless-safe Live Paper Trading GUI Panel.
    Can be imported without QApplication. Workers are cancellable.
    """

    def __init__(self) -> None:
        self._session_data: Optional[Dict[str, Any]] = None
        self._headless = True  # default headless-safe

    def get_metadata(self) -> Dict[str, Any]:
        return dict(PANEL_METADATA)

    def get_safety_banner(self) -> List[str]:
        return list(SAFETY_BANNER)

    def render_session_summary(self, session: Optional[Any] = None) -> Dict[str, Any]:
        if session is None:
            return {"empty_state": True, "paper_only": True}
        return {
            "session_id": getattr(session, "config", None) and session.config.session_id or "",
            "status": getattr(session, "status", None) and session.status.value or "UNKNOWN",
            "data_mode": getattr(session, "config", None) and session.config.data_mode.value or "UNKNOWN",
            "paper_only": True,
            "no_real_orders": True,
        }

    def render_market_state(self, market_status: str = "UNKNOWN", data_mode: str = "OFFLINE") -> Dict[str, Any]:
        return {
            "market_status": market_status,
            "data_mode": data_mode,
            "paper_only": True,
        }

    def render_orders(self, orders: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        if not orders:
            return []
        return [
            {
                "order_id": getattr(o, "paper_order_id", ""),
                "symbol": getattr(o, "symbol", ""),
                "side": getattr(o, "side", None) and o.side.value or "",
                "type": getattr(o, "order_type", None) and o.order_type.value or "",
                "quantity": str(getattr(o, "quantity", 0)),
                "filled": str(getattr(o, "filled_quantity", 0)),
                "remaining": str(getattr(o, "remaining_quantity", 0)),
                "status": getattr(o, "status", None) and o.status.value or "",
                "paper_only": True,
            }
            for o in orders
        ]

    def render_positions(self, positions: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        if not positions:
            return []
        return [
            {
                "symbol": getattr(p, "symbol", ""),
                "quantity": str(getattr(p, "quantity", 0)),
                "average_cost": str(getattr(p, "average_cost", 0)),
                "market_price": str(getattr(p, "market_price", None) or "N/A"),
                "unrealized_pnl": str(getattr(p, "unrealized_pnl", 0)),
                "paper_only": True,
            }
            for p in positions
        ]

    def render_risk_summary(self, risk: Optional[Any] = None) -> Dict[str, Any]:
        return {
            "risk_available": risk is not None,
            "paper_only": True,
            "no_broker": True,
        }

    # Supported actions (paper-only)
    def action_create_session(self) -> Dict[str, Any]:
        return {"action": "create_paper_session", "paper_only": True}

    def action_start(self) -> Dict[str, Any]:
        return {"action": "start", "paper_only": True}

    def action_pause(self) -> Dict[str, Any]:
        return {"action": "pause", "paper_only": True}

    def action_resume(self) -> Dict[str, Any]:
        return {"action": "resume", "paper_only": True}

    def action_halt(self) -> Dict[str, Any]:
        return {"action": "halt", "paper_only": True}

    def action_complete(self) -> Dict[str, Any]:
        return {"action": "complete", "paper_only": True}

    def action_submit_paper_order(self) -> Dict[str, Any]:
        return {"action": "submit_paper_order", "paper_only": True, "not_a_real_order": True}

    def action_cancel_paper_order(self) -> Dict[str, Any]:
        return {"action": "cancel_paper_order", "paper_only": True}

    def action_create_snapshot(self) -> Dict[str, Any]:
        return {"action": "create_snapshot", "paper_only": True}

    def action_verify_ledger(self) -> Dict[str, Any]:
        return {"action": "verify_ledger", "paper_only": True}

    def action_replay(self) -> Dict[str, Any]:
        return {"action": "replay", "paper_only": True, "not_live": True}

    def action_recover(self) -> Dict[str, Any]:
        return {"action": "recover", "paper_only": True}

    def action_export_report(self) -> Dict[str, Any]:
        return {"action": "export_report", "paper_only": True}

    # Forbidden actions — raise on call
    def connect_broker(self, *args, **kwargs):
        raise NotImplementedError("connect_broker FORBIDDEN — NO BROKER CONNECTION")

    def real_buy(self, *args, **kwargs):
        raise NotImplementedError("real_buy FORBIDDEN — NO REAL ORDERS")

    def real_sell(self, *args, **kwargs):
        raise NotImplementedError("real_sell FORBIDDEN — NO REAL ORDERS")

    def send_order(self, *args, **kwargs):
        raise NotImplementedError("send_order FORBIDDEN — NO REAL ORDERS")

    def sync_account(self, *args, **kwargs):
        raise NotImplementedError("sync_account FORBIDDEN — NO REAL ACCOUNT")

    def apply_live(self, *args, **kwargs):
        raise NotImplementedError("apply_live FORBIDDEN — PRODUCTION TRADING BLOCKED")
