"""
replay/replay_decision.py — ReplayDecisionManager v1.2.0

Manages replay decisions. All decisions are SIMULATION_DECISION_ONLY.
No paper orders. No broker calls.
update: creates revision, does NOT overwrite.

[!] Research Only. No Real Orders. Replay Training Only. Simulation Only.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDecisionManager:
    """
    Manages replay decisions. All decisions are SIMULATION_DECISION_ONLY.
    No paper orders. No broker calls.
    update: creates revision, does NOT overwrite.
    """

    SIMULATION_DECISION_ONLY = True

    VALID_ACTIONS = [
        "WATCH", "WAIT", "ENTER", "ADD", "HOLD", "REDUCE", "EXIT", "STOP", "SKIP",
    ]

    def __init__(self, store=None):
        self._store = store

    def create_decision(
        self, session_id: str, symbol: str, replay_date: str, action: str, **kwargs
    ):
        """Create a new simulation decision. Returns ReplayDecision."""
        from replay.replay_schema import ReplayDecision

        self.validate_action(action)

        confidence = int(kwargs.get("confidence", 50))
        confidence = max(0, min(100, confidence))

        decision = ReplayDecision(
            decision_id=f"DEC-{uuid.uuid4().hex[:12].upper()}",
            session_id=session_id,
            symbol=symbol,
            replay_date=replay_date,
            action=action,
            planned_price=kwargs.get("planned_price"),
            planned_quantity=kwargs.get("planned_quantity"),
            planned_position_pct=kwargs.get("planned_position_pct"),
            stop_price=kwargs.get("stop_price"),
            target_price=kwargs.get("target_price"),
            confidence=confidence,
            reasons=kwargs.get("reasons", []),
            notes=kwargs.get("notes", ""),
            tags=kwargs.get("tags", []),
            research_only=True,
            no_real_orders=True,
            simulation_decision_only=True,
        )

        # Validate prices if provided
        if decision.planned_price is not None:
            self.validate_price(decision.planned_price)
        if decision.planned_position_pct is not None:
            self.validate_position_pct(decision.planned_position_pct)
        if decision.stop_price is not None and decision.target_price is not None and decision.planned_price is not None:
            self.validate_stop_target(decision.stop_price, decision.target_price, decision.planned_price)

        if self._store:
            self._store.append_decision(decision)

        return decision

    def update_decision(self, decision_id: str, **kwargs):
        """
        Creates a revision of the decision (does NOT overwrite original).
        Returns new ReplayDecision with updated fields.
        """
        from replay.replay_schema import ReplayDecision

        # Load existing decision if possible
        existing = None
        if self._store and "session_id" in kwargs:
            decisions = self._store.load_decisions(kwargs["session_id"])
            for d in decisions:
                if d.get("decision_id") == decision_id:
                    existing = d
                    break

        now = datetime.now(timezone.utc).isoformat()
        base = existing or {}

        # Build revision
        revision = ReplayDecision(
            decision_id=f"DEC-{uuid.uuid4().hex[:12].upper()}",  # new ID = revision
            session_id=kwargs.get("session_id", base.get("session_id", "")),
            symbol=base.get("symbol", ""),
            replay_date=base.get("replay_date", ""),
            action=kwargs.get("action", base.get("action", "WATCH")),
            planned_price=kwargs.get("planned_price", base.get("planned_price")),
            planned_quantity=kwargs.get("planned_quantity", base.get("planned_quantity")),
            planned_position_pct=kwargs.get("planned_position_pct", base.get("planned_position_pct")),
            stop_price=kwargs.get("stop_price", base.get("stop_price")),
            target_price=kwargs.get("target_price", base.get("target_price")),
            confidence=int(kwargs.get("confidence", base.get("confidence", 50))),
            reasons=kwargs.get("reasons", base.get("reasons", [])),
            notes=kwargs.get("notes", base.get("notes", "")),
            tags=kwargs.get("tags", base.get("tags", [])),
            created_at=base.get("created_at", now),
            updated_at=now,
            research_only=True,
            no_real_orders=True,
            simulation_decision_only=True,
        )
        revision.notes = f"[REVISION of {decision_id}] " + revision.notes

        if self._store:
            self._store.append_decision(revision)

        return revision

    def validate_action(self, action: str) -> None:
        """Raises ValueError if action is not valid."""
        if action not in self.VALID_ACTIONS:
            raise ValueError(f"Invalid action '{action}'. Must be one of {self.VALID_ACTIONS}")

    def validate_price(self, price) -> None:
        """Raises ValueError if price is invalid."""
        if price is not None and float(price) <= 0:
            raise ValueError(f"Price must be positive, got {price}")

    def validate_position_pct(self, pct) -> None:
        """Raises ValueError if position % is not 0-100."""
        if pct is not None and not (0 <= float(pct) <= 100):
            raise ValueError(f"Position % must be 0-100, got {pct}")

    def validate_stop_target(self, stop, target, price) -> None:
        """Validates stop/target relative to price (warning only, no crash)."""
        try:
            if stop and target and price:
                if float(stop) >= float(target):
                    logger.warning("[DecisionManager] stop >= target (%s >= %s)", stop, target)
        except Exception:
            pass

    def explain_decision(self, decision_id: str) -> str:
        """Returns human-readable explanation of decision."""
        return (
            f"Decision {decision_id}: SIMULATION_DECISION_ONLY. "
            "No order will be sent. No paper order. No broker call. Research Only."
        )

    def list_for_session(self, session_id: str) -> List[Dict[str, Any]]:
        """List all decisions for session."""
        if not self._store:
            return []
        return self._store.load_decisions(session_id)

    def latest_for_date(self, session_id: str, replay_date: str) -> Optional[Dict[str, Any]]:
        """Get most recent decision for a replay_date."""
        decisions = self.list_for_session(session_id)
        dated = [d for d in decisions if d.get("replay_date") == replay_date]
        return dated[-1] if dated else None
