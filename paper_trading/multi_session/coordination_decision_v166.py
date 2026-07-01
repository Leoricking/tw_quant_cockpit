"""
paper_trading/multi_session/coordination_decision_v166.py — Coordination Decision v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List
from paper_trading.multi_session.enums_v166 import DecisionType, CoordinationOutcome
from paper_trading.multi_session.models_v166 import CoordinationDecision

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True

FORBIDDEN_DECISION_ACTIONS = [
    "auto_resume",
    "auto_restart",
    "broker_execution",
    "real_order",
    "capital_movement",
    "production_process_kill",
    "production_db_write",
]


def make_coordination_decision(
    session_ids: List[str],
    decision_type: DecisionType,
    reason: str,
    actor: str,
    input_state_hash: str,
    policy_version: str,
    selected_action: str,
    rejected_actions: List[str] = None,
    safety_blocks: List[str] = None,
    expected_state: Dict[str, Any] = None,
    lineage: List[str] = None,
) -> CoordinationDecision:
    if selected_action in FORBIDDEN_DECISION_ACTIONS:
        raise ValueError(f"Forbidden decision action: {selected_action}")
    return CoordinationDecision(
        decision_id=str(uuid.uuid4()),
        session_ids=list(session_ids),
        decision_type=decision_type,
        reason=reason,
        actor=actor,
        created_at=datetime.now(timezone.utc),
        input_state_hash=input_state_hash,
        policy_version=policy_version,
        selected_action=selected_action,
        rejected_actions=rejected_actions or [],
        safety_blocks=safety_blocks or [],
        expected_state=expected_state or {},
        lineage=lineage or [],
    )
