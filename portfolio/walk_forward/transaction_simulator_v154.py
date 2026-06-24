"""
portfolio/walk_forward/transaction_simulator_v154.py — Simulation Transaction Engine v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
All transactions: SIMULATION_ONLY, NOT_REAL_ORDER.
"""
from __future__ import annotations
import hashlib
import json
from typing import Any, Dict, Optional

from portfolio.walk_forward.enums_v154 import SimulatedTransactionType
from portfolio.walk_forward.models_v154 import SimulatedPortfolioTransaction
from portfolio.walk_forward.cost_model_v154 import CostModelEngine
from portfolio.walk_forward.slippage_model_v154 import SlippageModelEngine

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
TRANSACTION_SIMULATOR_VERSION = "1.5.4"


def _make_txn_id(window_id: str, decision_id: str, symbol: str, txn_type: str) -> str:
    raw = f"{window_id}_{decision_id}_{symbol}_{txn_type}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


class SimulationTransactionEngine:
    """
    Creates simulated (hypothetical) portfolio transactions.
    All transactions are SIMULATION_ONLY, NOT_REAL_ORDER, research_only=True, executable=False.
    """

    def __init__(self):
        self.version = TRANSACTION_SIMULATOR_VERSION
        self._cost = CostModelEngine()
        self._slip = SlippageModelEngine()

    def simulate_buy(
        self,
        decision_context,
        symbol: str,
        quantity: float,
        price: float,
        cost_policy=None,
        slippage_policy=None,
        window_id: str = "wf_0001",
    ) -> SimulatedPortfolioTransaction:
        """
        Simulate a hypothetical buy transaction.
        research_only=True, executable=False, real_order_created=False.
        """
        decision_id = getattr(decision_context, "decision_id", "demo_dec") if decision_context else "demo_dec"
        as_of = getattr(decision_context, "as_of", "2020-01-01") if decision_context else "2020-01-01"

        gross_amount = quantity * price
        fee = float(self._cost.apply_buy_cost(gross_amount, cost_policy))

        # Slippage
        slip_bps = getattr(slippage_policy, "fixed_bps", 5.0) if slippage_policy else 5.0
        slippage = float(self._slip.apply_fixed_bps(gross_amount, slip_bps or 5.0))

        simulated_price = price * (1 + (slip_bps or 5.0) / 10000)
        net_amount = gross_amount + fee + slippage

        return SimulatedPortfolioTransaction(
            transaction_id=_make_txn_id(window_id, decision_id, symbol, "BUY"),
            window_id=window_id,
            decision_id=decision_id,
            transaction_type=SimulatedTransactionType.HYPOTHETICAL_BUY,
            symbol=symbol,
            decision_date=as_of,
            simulated_execution_date=as_of,
            quantity=quantity,
            decision_price=price,
            simulated_price=simulated_price,
            gross_amount=gross_amount,
            fee=fee,
            tax=0.0,
            slippage=slippage,
            net_amount=net_amount,
            currency="TWD",
            reason="HYPOTHETICAL_BUY — SIMULATION_ONLY",
            research_only=True,
            executable=False,
            real_order_created=False,
            formal_ledger_persisted=False,
            source_lineage_ids=[f"lineage_{as_of}"],
            metadata={"simulation_only": True, "not_real_order": True},
        )

    def simulate_sell(
        self,
        decision_context,
        symbol: str,
        quantity: float,
        price: float,
        cost_policy=None,
        slippage_policy=None,
        window_id: str = "wf_0001",
    ) -> SimulatedPortfolioTransaction:
        """
        Simulate a hypothetical sell transaction.
        research_only=True, executable=False, real_order_created=False.
        """
        decision_id = getattr(decision_context, "decision_id", "demo_dec") if decision_context else "demo_dec"
        as_of = getattr(decision_context, "as_of", "2020-01-01") if decision_context else "2020-01-01"

        gross_amount = quantity * price
        fee = float(self._cost.apply_sell_cost(gross_amount, cost_policy))
        tax = float(self._cost.apply_tax(gross_amount, cost_policy))

        slip_bps = getattr(slippage_policy, "fixed_bps", 5.0) if slippage_policy else 5.0
        slippage = float(self._slip.apply_fixed_bps(gross_amount, slip_bps or 5.0))

        simulated_price = price * (1 - (slip_bps or 5.0) / 10000)
        net_amount = gross_amount - fee - tax - slippage

        return SimulatedPortfolioTransaction(
            transaction_id=_make_txn_id(window_id, decision_id, symbol, "SELL"),
            window_id=window_id,
            decision_id=decision_id,
            transaction_type=SimulatedTransactionType.HYPOTHETICAL_SELL,
            symbol=symbol,
            decision_date=as_of,
            simulated_execution_date=as_of,
            quantity=quantity,
            decision_price=price,
            simulated_price=simulated_price,
            gross_amount=gross_amount,
            fee=fee,
            tax=tax,
            slippage=slippage,
            net_amount=net_amount,
            currency="TWD",
            reason="HYPOTHETICAL_SELL — SIMULATION_ONLY",
            research_only=True,
            executable=False,
            real_order_created=False,
            formal_ledger_persisted=False,
            source_lineage_ids=[f"lineage_{as_of}"],
            metadata={"simulation_only": True, "not_real_order": True},
        )
