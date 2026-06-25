"""
paper_trading/strategy/proposal_v162.py — Paper order proposal builder for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from paper_trading.strategy.enums_v162 import ProposalStatus, SignalType
from paper_trading.strategy.models_v162 import (
    DecisionResult,
    PaperOrderProposal,
    PaperSignal,
    _new_id,
    _now_iso,
)

logger = logging.getLogger(__name__)


def build_proposal(
    decision: DecisionResult,
    signal: PaperSignal,
    suggested_size: float,
    proposed_price: Optional[float] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> PaperOrderProposal:
    """
    Build a PaperOrderProposal from an approved decision and its originating signal.

    [!] The proposal is PAPER ONLY. It is submitted to the paper order machine,
        NOT to any real broker or exchange.
    [!] NOT a real order. No real capital is at risk.
    """
    assert decision.paper_only is True, "Decision must be paper_only"
    assert decision.not_a_real_order is True, "Decision must be not_a_real_order"
    assert signal.paper_only is True, "Signal must be paper_only"
    assert suggested_size >= 0, "Suggested size must be non-negative"

    meta = {
        "signal_strength": signal.strength,
        "signal_confidence": signal.confidence,
        "normalized_value": signal.normalized_value,
        "trigger_type": signal.trigger_type,
        **(metadata or {}),
    }

    proposal = PaperOrderProposal(
        proposal_id=_new_id(),
        decision_id=decision.decision_id,
        strategy_id=decision.strategy_id,
        ticker=decision.ticker,
        signal_type=signal.signal_type,
        proposed_size=suggested_size,
        proposed_price=proposed_price,
        status=ProposalStatus.PENDING.value,
        created_at=_now_iso(),
        metadata=meta,
        paper_only=True,
        research_only=True,
        simulation_only=True,
        not_a_real_order=True,
        no_broker_call=True,
        no_real_account=True,
        no_formal_portfolio_ledger_write=True,
    )

    logger.info(
        "[v1.6.2][proposal] Created proposal %s: %s %s size=%.2f (PAPER_ONLY)",
        proposal.proposal_id[:8],
        signal.signal_type,
        proposal.ticker,
        proposal.proposed_size,
    )
    return proposal


def submit_proposal(proposal: PaperOrderProposal) -> PaperOrderProposal:
    """
    Mark a proposal as submitted to the paper order machine.
    Does NOT call any broker or real execution system.
    """
    assert proposal.paper_only is True
    assert proposal.not_a_real_order is True
    assert proposal.no_broker_call is True

    proposal.status = ProposalStatus.SUBMITTED.value
    proposal.submitted_at = _now_iso()
    logger.info(
        "[v1.6.2][proposal] Submitted proposal %s (PAPER_ONLY. NO BROKER. NO REAL ORDER.)",
        proposal.proposal_id[:8]
    )
    return proposal


def accept_proposal(proposal: PaperOrderProposal) -> PaperOrderProposal:
    """Mark a proposal as accepted by the paper order machine."""
    proposal.status = ProposalStatus.ACCEPTED.value
    proposal.accepted_at = _now_iso()
    return proposal


def reject_proposal(proposal: PaperOrderProposal, reason: str = "") -> PaperOrderProposal:
    """Mark a proposal as rejected by the paper order machine."""
    proposal.status = ProposalStatus.REJECTED.value
    proposal.rejected_at = _now_iso()
    proposal.rejection_reason = reason
    return proposal


def cancel_proposal(proposal: PaperOrderProposal) -> PaperOrderProposal:
    """Cancel a pending proposal."""
    proposal.status = ProposalStatus.CANCELLED.value
    return proposal


def proposal_to_dict(proposal: PaperOrderProposal) -> Dict[str, Any]:
    """Serialize a PaperOrderProposal to a plain dict."""
    return {
        "proposal_id": proposal.proposal_id,
        "decision_id": proposal.decision_id,
        "strategy_id": proposal.strategy_id,
        "ticker": proposal.ticker,
        "signal_type": proposal.signal_type,
        "proposed_size": proposal.proposed_size,
        "proposed_price": proposal.proposed_price,
        "status": proposal.status,
        "created_at": proposal.created_at,
        "submitted_at": proposal.submitted_at,
        "accepted_at": proposal.accepted_at,
        "rejected_at": proposal.rejected_at,
        "rejection_reason": proposal.rejection_reason,
        "metadata": proposal.metadata,
        "paper_only": proposal.paper_only,
        "research_only": proposal.research_only,
        "simulation_only": proposal.simulation_only,
        "not_a_real_order": proposal.not_a_real_order,
        "no_broker_call": proposal.no_broker_call,
        "no_real_account": proposal.no_real_account,
        "no_formal_portfolio_ledger_write": proposal.no_formal_portfolio_ledger_write,
    }
