"""
paper_trading/strategy/order_bridge_v162.py — Paper order bridge for Paper Strategy Orchestration v1.6.2.
Connects the strategy layer to the v1.6.0 paper order machine.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

from paper_trading.strategy.enums_v162 import ProposalStatus
from paper_trading.strategy.models_v162 import PaperOrderProposal, _now_iso
from paper_trading.strategy.proposal_v162 import (
    accept_proposal,
    reject_proposal,
    submit_proposal,
)

logger = logging.getLogger(__name__)


class PaperOrderBridge:
    """
    Bridge between paper strategy proposals and the v1.6.0 paper order machine.

    This bridge:
      - Validates proposal safety invariants before submission
      - Submits to the paper order machine (NOT a real broker)
      - Tracks submission results
      - Records all activity (no real orders are ever placed)

    [!] This component explicitly does NOT connect to any broker, exchange,
        or real account. It only interacts with the local paper order simulation.
    """

    # Safety constant — must never be changed
    BROKER_CONNECTED: bool = False
    REAL_ORDERS_ENABLED: bool = False
    PRODUCTION_ENABLED: bool = False

    def __init__(self) -> None:
        self._submitted: List[str] = []
        self._accepted: List[str] = []
        self._rejected: List[str] = []
        self._submit_count: int = 0
        self._error_count: int = 0

    def submit(self, proposal: PaperOrderProposal) -> Tuple[bool, str]:
        """
        Submit a paper proposal to the paper order machine.

        Returns (ok, reason).
        [!] PAPER_ONLY. No real broker call. No real account interaction.
        """
        # Safety gate
        if not self._validate_safety(proposal):
            reason = "Safety invariant violated — proposal rejected before submission"
            logger.error("[v1.6.2][bridge] %s %s", reason, proposal.proposal_id[:8])
            self._error_count += 1
            return False, reason

        # Submit to paper machine
        try:
            submit_proposal(proposal)
            ok, reason = self._submit_to_paper_machine(proposal)
            self._submit_count += 1

            if ok:
                accept_proposal(proposal)
                self._submitted.append(proposal.proposal_id)
                self._accepted.append(proposal.proposal_id)
                logger.info(
                    "[v1.6.2][bridge] Proposal %s ACCEPTED by paper order machine (PAPER_ONLY)",
                    proposal.proposal_id[:8]
                )
            else:
                reject_proposal(proposal, reason)
                self._submitted.append(proposal.proposal_id)
                self._rejected.append(proposal.proposal_id)
                logger.info(
                    "[v1.6.2][bridge] Proposal %s REJECTED by paper machine: %s",
                    proposal.proposal_id[:8], reason
                )
            return ok, reason

        except Exception as exc:
            self._error_count += 1
            reason = f"Bridge error: {exc}"
            reject_proposal(proposal, reason)
            logger.error(
                "[v1.6.2][bridge] Submit error for %s: %s",
                proposal.proposal_id[:8], exc
            )
            return False, reason

    def _submit_to_paper_machine(
        self, proposal: PaperOrderProposal
    ) -> Tuple[bool, str]:
        """
        Interface with the v1.6.0 paper order machine.
        Returns (accepted, reason).
        """
        try:
            from paper_trading.order_machine_v160 import PaperOrderMachine
            machine = PaperOrderMachine()
            result = machine.submit_proposal(
                ticker=proposal.ticker,
                signal_type=proposal.signal_type,
                size=proposal.proposed_size,
                price=proposal.proposed_price,
                strategy_id=proposal.strategy_id,
                proposal_id=proposal.proposal_id,
                paper_only=True,
                metadata=proposal.metadata,
            )
            if result.get("accepted"):
                return True, "accepted"
            return False, result.get("reason", "rejected by paper order machine")
        except ImportError:
            # Paper order machine not yet integrated — log and accept in simulation
            logger.info(
                "[v1.6.2][bridge] paper_trading.order_machine_v160 not available "
                "— simulating acceptance (PAPER_ONLY)"
            )
            return True, "simulated_acceptance (order_machine not integrated)"
        except Exception as exc:
            return False, str(exc)

    @staticmethod
    def _validate_safety(proposal: PaperOrderProposal) -> bool:
        """Verify all safety flags before any submission attempt."""
        return (
            proposal.paper_only is True
            and proposal.research_only is True
            and proposal.simulation_only is True
            and proposal.not_a_real_order is True
            and proposal.no_broker_call is True
            and proposal.no_real_account is True
            and proposal.no_formal_portfolio_ledger_write is True
        )

    def stats(self) -> Dict[str, Any]:
        return {
            "submit_count": self._submit_count,
            "accepted_count": len(self._accepted),
            "rejected_count": len(self._rejected),
            "error_count": self._error_count,
            "broker_connected": self.BROKER_CONNECTED,
            "real_orders_enabled": self.REAL_ORDERS_ENABLED,
            "production_enabled": self.PRODUCTION_ENABLED,
            "paper_only": True,
            "research_only": True,
        }
