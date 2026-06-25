"""
paper_trading/strategy/approval_v162.py — Approval policy for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Tuple

from paper_trading.strategy.enums_v162 import ApprovalMode, DecisionOutcome
from paper_trading.strategy.models_v162 import DecisionResult, _now_iso

logger = logging.getLogger(__name__)


class ApprovalPolicy:
    """
    Applies the approval policy to a DEFERRED paper decision.

    ApprovalMode.MANUAL_REQUIRED (default):
      - Pipeline returns DEFERRED; human must call approve() explicitly.
      - Auto-approval is never applied in this mode.

    ApprovalMode.AUTO_PAPER_ONLY:
      - Allowed only when all safety conditions verified.
      - Returns APPROVED immediately without human gate.
      - Only enabled when AUTO_PAPER_ONLY_ENABLED_BY_DEFAULT = False has been
        explicitly overridden per strategy config.

    [!] No real orders are created in either mode.
    """

    def __init__(self) -> None:
        self._pending_decisions: Dict[str, DecisionResult] = {}  # decision_id → result
        self._approved_count: int = 0
        self._denied_count: int = 0
        self._auto_count: int = 0

    def submit_for_approval(self, result: DecisionResult) -> None:
        """Park a DEFERRED decision for manual approval."""
        if result.outcome != DecisionOutcome.DEFERRED.value:
            return
        self._pending_decisions[result.decision_id] = result
        logger.info(
            "[v1.6.2][approval] Decision %s parked for MANUAL approval (ticker=%s)",
            result.decision_id[:8], result.ticker
        )

    def approve(self, decision_id: str, approver: str = "operator") -> Tuple[bool, str]:
        """
        Manually approve a deferred decision.
        Returns (ok, reason).
        """
        result = self._pending_decisions.get(decision_id)
        if result is None:
            return False, f"Decision not found or not pending: {decision_id}"

        result.outcome = DecisionOutcome.APPROVED.value
        result.reason = f"Manually approved by {approver}"
        result.extra["approved_by"] = approver
        result.extra["approved_at"] = _now_iso()
        del self._pending_decisions[decision_id]
        self._approved_count += 1
        logger.info(
            "[v1.6.2][approval] Decision %s APPROVED by %s (PAPER_ONLY)",
            decision_id[:8], approver
        )
        return True, "approved"

    def deny(self, decision_id: str, reason: str = "", denier: str = "operator") -> Tuple[bool, str]:
        """
        Deny a deferred decision.
        Returns (ok, reason).
        """
        result = self._pending_decisions.get(decision_id)
        if result is None:
            return False, f"Decision not found or not pending: {decision_id}"

        result.outcome = DecisionOutcome.REJECTED.value
        result.reason = f"Denied by {denier}: {reason}"
        result.extra["denied_by"] = denier
        result.extra["denied_at"] = _now_iso()
        del self._pending_decisions[decision_id]
        self._denied_count += 1
        logger.info(
            "[v1.6.2][approval] Decision %s DENIED by %s: %s",
            decision_id[:8], denier, reason
        )
        return True, "denied"

    def auto_approve(self, result: DecisionResult, strategy_config: Any) -> bool:
        """
        Auto-approve when approval_mode == AUTO_PAPER_ONLY.
        Returns True if auto-approved, False otherwise.

        Safety: only proceeds when:
          - approval_mode is AUTO_PAPER_ONLY
          - paper_only=True, research_only=True, not_a_real_order=True on the result
          - PRODUCTION_TRADING_BLOCKED is True on strategy_config
        """
        if result.outcome != DecisionOutcome.DEFERRED.value:
            return False

        if getattr(strategy_config, "approval_mode", None) != ApprovalMode.AUTO_PAPER_ONLY:
            return False

        # Safety invariant verification
        if not (
            result.paper_only is True
            and result.not_a_real_order is True
            and result.no_broker_call is True
            and getattr(strategy_config, "paper_only", False) is True
        ):
            logger.warning(
                "[v1.6.2][approval] AUTO_PAPER_ONLY refused — safety invariants not met"
            )
            return False

        result.outcome = DecisionOutcome.APPROVED.value
        result.reason = "Auto-approved (AUTO_PAPER_ONLY mode, all safety conditions verified)"
        result.extra["auto_approved_at"] = _now_iso()
        self._approved_count += 1
        self._auto_count += 1
        logger.info(
            "[v1.6.2][approval] Decision %s auto-approved (PAPER_ONLY)", result.decision_id[:8]
        )
        return True

    def pending_count(self) -> int:
        return len(self._pending_decisions)

    def list_pending(self) -> Dict[str, Dict]:
        return {
            did: {
                "decision_id": r.decision_id,
                "ticker": r.ticker,
                "strategy_id": r.strategy_id,
                "decided_at": r.decided_at,
            }
            for did, r in self._pending_decisions.items()
        }

    def stats(self) -> Dict[str, Any]:
        return {
            "approved_count": self._approved_count,
            "denied_count": self._denied_count,
            "auto_count": self._auto_count,
            "pending_count": self.pending_count(),
            "paper_only": True,
            "research_only": True,
        }
