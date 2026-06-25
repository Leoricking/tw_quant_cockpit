"""reports/live_paper_trading_report.py — Live Paper Trading Research Report v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. NO BROKER. PRODUCTION TRADING: BLOCKED.
NOT INVESTMENT ADVICE.
"""
from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional


REPORT_SAFETY = {
    "paper_trading_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_real_account": True,
    "no_formal_portfolio_ledger_write": True,
    "production_trading_blocked": True,
    "not_investment_advice": True,
}


class LivePaperTradingReport:
    """Generates paper trading research report. Paper-only. No real orders."""

    REPORT_VERSION = "1.6.0"

    def generate(
        self,
        session_id: str,
        session_name: str = "",
        data_mode: str = "FIXTURE",
        market_status: str = "UNKNOWN",
        initial_cash: Optional[Decimal] = None,
        ending_cash: Optional[Decimal] = None,
        orders: Optional[List[Any]] = None,
        fills: Optional[List[Any]] = None,
        positions: Optional[List[Any]] = None,
        realized_pnl: Decimal = Decimal("0"),
        unrealized_pnl: Decimal = Decimal("0"),
        total_fees: Decimal = Decimal("0"),
        total_taxes: Decimal = Decimal("0"),
        total_slippage: Decimal = Decimal("0"),
        exposure: Decimal = Decimal("0"),
        drawdown: Decimal = Decimal("0"),
        drawdown_pct: Decimal = Decimal("0"),
        risk_checks: Optional[List[Dict[str, Any]]] = None,
        kill_switch_event: Optional[Any] = None,
        event_count: int = 0,
        ledger_valid: bool = True,
        ledger_hash: str = "",
        recovery_result: Optional[Any] = None,
        replay_result: Optional[Any] = None,
        lineage_summary: Optional[Dict[str, Any]] = None,
        reproducibility: Optional[Dict[str, Any]] = None,
        assumptions: Optional[List[str]] = None,
        limitations: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        generated_at = datetime.now(timezone.utc).isoformat()

        return {
            "report_title": "Live Paper Trading Research Report v1.6.0",
            "report_version": self.REPORT_VERSION,
            "generated_at": generated_at,
            "safety": REPORT_SAFETY,

            "session": {
                "session_id": session_id,
                "session_name": session_name,
                "data_mode": data_mode,
                "data_mode_label": f"{data_mode}_PAPER_SIMULATION_ONLY",
            },

            "market_state": {
                "status": market_status,
                "note": "Taiwan Stock Exchange (TWSE), Asia/Taipei",
            },

            "cash": {
                "initial_cash": str(initial_cash or Decimal("0")),
                "ending_cash": str(ending_cash or Decimal("0")),
                "currency": "TWD",
                "paper_only": True,
            },

            "orders": {
                "total": len(orders or []),
                "list": [self._format_order(o) for o in (orders or [])],
            },

            "fills": {
                "total": len(fills or []),
                "list": [self._format_fill(f) for f in (fills or [])],
            },

            "positions": {
                "total": len(positions or []),
                "list": [self._format_position(p) for p in (positions or [])],
            },

            "pnl": {
                "realized_pnl": str(realized_pnl),
                "unrealized_pnl": str(unrealized_pnl),
                "total_pnl": str(realized_pnl + unrealized_pnl),
                "total_fees": str(total_fees),
                "total_taxes": str(total_taxes),
                "total_slippage": str(total_slippage),
                "paper_only": True,
            },

            "risk": {
                "exposure": str(exposure),
                "drawdown": str(drawdown),
                "drawdown_pct": str(drawdown_pct),
                "checks": risk_checks or [],
            },

            "kill_switch": {
                "triggered": kill_switch_event.triggered if kill_switch_event else False,
                "reason": kill_switch_event.reason.value if (kill_switch_event and kill_switch_event.reason) else None,
                "detail": kill_switch_event.detail if kill_switch_event else "",
            },

            "events": {
                "count": event_count,
            },

            "ledger": {
                "valid": ledger_valid,
                "hash": ledger_hash,
                "paper_only": True,
                "no_formal_portfolio_ledger_write": True,
            },

            "recovery": {
                "result": str(recovery_result) if recovery_result else None,
            },

            "replay": {
                "result": str(replay_result) if replay_result else None,
            },

            "lineage": lineage_summary or {"paper_only": True},

            "reproducibility": reproducibility or {"paper_only": True},

            "assumptions": assumptions or [
                "PAPER_TRADING_ONLY: All results are simulated",
                "ZERO_LATENCY_DISCLOSED: Default instant fill assumption",
                "SLIPPAGE_MODEL_DISCLOSED: Fixed BPS or spread-based",
                "SIMPLIFIED_PAPER_SETTLEMENT: Not real T+2",
                "CORPORATE_ACTIONS_LIMITED: Not fully modeled v1.6.0",
            ],

            "limitations": limitations or [
                "Paper trading ≠ real trading",
                "No Broker integration",
                "No real account",
                "Simplified settlement model",
                "Corporate actions not fully modeled",
                "No HFT, no margin, no short selling, no options/futures",
            ],

            "footer": {
                "paper_trading_only": True,
                "no_real_orders": True,
                "no_broker": True,
                "no_real_account": True,
                "no_formal_portfolio_ledger_write": True,
                "production_trading_blocked": True,
                "not_investment_advice": True,
            },
        }

    def _format_order(self, o: Any) -> Dict[str, Any]:
        return {
            "order_id": getattr(o, "paper_order_id", str(o)),
            "symbol": getattr(o, "symbol", ""),
            "side": getattr(o, "side", None) and o.side.value or "",
            "status": getattr(o, "status", None) and o.status.value or "",
            "paper_only": True,
            "not_a_real_order": True,
        }

    def _format_fill(self, f: Any) -> Dict[str, Any]:
        return {
            "fill_id": getattr(f, "fill_id", str(f)),
            "symbol": getattr(f, "symbol", ""),
            "quantity": str(getattr(f, "quantity", 0)),
            "price": str(getattr(f, "price", 0)),
            "paper_only": True,
        }

    def _format_position(self, p: Any) -> Dict[str, Any]:
        return {
            "symbol": getattr(p, "symbol", ""),
            "quantity": str(getattr(p, "quantity", 0)),
            "paper_only": True,
        }
