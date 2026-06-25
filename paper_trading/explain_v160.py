"""paper_trading/explain_v160.py — Paper Session Explainability v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
"""
from __future__ import annotations
from typing import Any, Dict, List


class PaperSessionExplainer:
    """Provides human-readable explanations of paper session state and decisions."""

    def explain_session(self, session_id: str, status: str, data_mode: str) -> Dict[str, Any]:
        return {
            "session_id": session_id,
            "status": status,
            "data_mode": data_mode,
            "paper_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "explanation": (
                f"Paper trading session {session_id} in {status} state. "
                f"Data mode: {data_mode}. All orders are SIMULATION_ONLY. "
                "No real orders created. No broker connection. "
                "PRODUCTION TRADING BLOCKED."
            ),
        }

    def explain_fill(self, fill, order, latency_assumption: str, slippage_assumption: str) -> Dict[str, Any]:
        return {
            "fill_id": fill.fill_id,
            "paper_order_id": fill.paper_order_id,
            "symbol": fill.symbol,
            "side": fill.side.value,
            "quantity": str(fill.quantity),
            "price": str(fill.price),
            "latency": latency_assumption,
            "slippage": slippage_assumption,
            "fee": str(fill.fee),
            "tax": str(fill.tax),
            "paper_only": "PAPER_ONLY",
            "not_a_real_order": "NOT_A_REAL_ORDER",
            "no_broker_call": "NO_BROKER_CALL",
        }

    def explain_risk_evaluation(self, evaluation) -> Dict[str, Any]:
        return {
            "evaluation_id": evaluation.evaluation_id,
            "symbol": evaluation.symbol,
            "status": evaluation.status.value,
            "block_reasons": evaluation.block_reasons,
            "warning_reasons": evaluation.warning_reasons,
            "checks": [
                {"name": c.check_name, "status": c.status.value, "reason": c.reason}
                for c in evaluation.checks
            ],
        }

    def explain_assumptions(self) -> List[str]:
        return [
            "PAPER_TRADING_ONLY: All orders, fills, and P&L are simulations.",
            "NO_REAL_ORDERS: No orders are sent to any exchange or broker.",
            "NO_BROKER_CONNECTION: No broker API is called.",
            "NO_REAL_ACCOUNT: No real trading account is modified.",
            "SIMPLIFIED_PAPER_SETTLEMENT: Not real T+2 Taiwan settlement.",
            "ZERO_LATENCY_DISCLOSED: Default fill model assumes instant fill.",
            "SLIPPAGE_MODEL_DISCLOSED: Fixed BPS or spread-based slippage applied.",
            "LIQUIDITY_MODEL_DISCLOSED: Participation-rate fill limit applied.",
            "CORPORATE_ACTIONS_LIMITED: Corporate actions not fully modeled.",
            "PRODUCTION_TRADING_BLOCKED: System cannot place real trades.",
        ]
