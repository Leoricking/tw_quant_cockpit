"""
paper_trading/multi_session/session_descriptor_v166.py — Session Descriptor factory v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.enums_v166 import SessionType, SessionLifecycleState, SessionPriority
from paper_trading.multi_session.models_v166 import SessionDescriptor

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True


def make_session_descriptor(
    name: str,
    owner: str,
    session_type: SessionType = SessionType.PAPER,
    priority: SessionPriority = SessionPriority.NORMAL,
    capabilities: Optional[List[str]] = None,
    symbols: Optional[List[str]] = None,
    strategies: Optional[List[str]] = None,
    data_sources: Optional[List[str]] = None,
    resource_requirements: Optional[Dict[str, Any]] = None,
    risk_budget: float = 0.0,
    capital_budget: float = 0.0,
    policy_version: str = "1.0",
    code_version: str = "1.6.6",
    paper_only: bool = True,
    research_only: bool = True,
    fixture_only: bool = False,
    session_id: Optional[str] = None,
) -> SessionDescriptor:
    return SessionDescriptor(
        session_id=session_id or str(uuid.uuid4()),
        session_type=session_type,
        name=name,
        owner=owner,
        created_at=datetime.now(timezone.utc),
        registered_at=None,
        lifecycle_state=SessionLifecycleState.CREATED,
        priority=priority,
        capabilities=capabilities or [],
        symbols=symbols or [],
        strategies=strategies or [],
        data_sources=data_sources or [],
        resource_requirements=resource_requirements or {},
        risk_budget=risk_budget,
        capital_budget=capital_budget,
        policy_version=policy_version,
        code_version=code_version,
        paper_only=paper_only,
        research_only=research_only,
        fixture_only=fixture_only,
    )
