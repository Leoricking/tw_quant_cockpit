"""
paper_trading/multi_session/conflict_detector_v166.py — Conflict Detector v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List
from paper_trading.multi_session.enums_v166 import ConflictType, ConflictSeverity
from paper_trading.multi_session.models_v166 import SessionDescriptor, CoordinationPolicy, SessionConflict

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True


class ConflictDetector:
    """Detects coordination conflicts among paper/replay sessions."""

    def detect(
        self,
        sessions: List[SessionDescriptor],
        policy: CoordinationPolicy,
    ) -> List[SessionConflict]:
        conflicts: List[SessionConflict] = []
        now = datetime.now(timezone.utc)
        pv = policy.version

        # Symbol overlap detection
        symbol_to_sessions: Dict[str, List[str]] = {}
        for s in sessions:
            for sym in s.symbols:
                symbol_to_sessions.setdefault(sym, []).append(s.session_id)
        for sym, sids in symbol_to_sessions.items():
            if len(sids) > 1:
                conflicts.append(SessionConflict(
                    conflict_id=str(uuid.uuid4()),
                    session_ids=sids,
                    conflict_type=ConflictType.SYMBOL_OVERLAP,
                    severity=ConflictSeverity.WARN,
                    resource_key=None,
                    symbol=sym,
                    strategy=None,
                    detected_at=now,
                    evidence={"symbol": sym, "sessions": sids},
                    resolution_options=["degrade_lower_priority", "warn_only"],
                    blocking=False,
                    policy_version=pv,
                ))

        # Strategy conflict detection
        strategy_to_sessions: Dict[str, List[str]] = {}
        for s in sessions:
            for strat in s.strategies:
                strategy_to_sessions.setdefault(strat, []).append(s.session_id)
        for strat, sids in strategy_to_sessions.items():
            if len(sids) > 1:
                conflicts.append(SessionConflict(
                    conflict_id=str(uuid.uuid4()),
                    session_ids=sids,
                    conflict_type=ConflictType.STRATEGY_CONFLICT,
                    severity=ConflictSeverity.WARN,
                    resource_key=None,
                    symbol=None,
                    strategy=strat,
                    detected_at=now,
                    evidence={"strategy": strat, "sessions": sids},
                    resolution_options=["warn_only", "block_duplicate"],
                    blocking=False,
                    policy_version=pv,
                ))

        # Capital over-allocation detection
        total_capital = sum(s.capital_budget for s in sessions)
        if total_capital > policy.capital_rules.get("global_paper_capital_limit", 10_000_000.0):
            all_ids = [s.session_id for s in sessions]
            conflicts.append(SessionConflict(
                conflict_id=str(uuid.uuid4()),
                session_ids=all_ids,
                conflict_type=ConflictType.CAPITAL_OVERALLOCATION,
                severity=ConflictSeverity.BLOCK,
                resource_key="capital_budget",
                symbol=None,
                strategy=None,
                detected_at=now,
                evidence={"total_capital": total_capital},
                resolution_options=["reduce_capital", "block_lowest_priority"],
                blocking=True,
                policy_version=pv,
            ))

        return conflicts

    def detect_session_state_conflict(
        self,
        session_a_state: str,
        session_b_state: str,
        policy_version: str,
    ) -> List[SessionConflict]:
        conflicts: List[SessionConflict] = []
        if session_a_state == "RUNNING" and session_b_state == "RECOVERING":
            conflicts.append(SessionConflict(
                conflict_id=str(uuid.uuid4()),
                session_ids=["a", "b"],
                conflict_type=ConflictType.SESSION_STATE_CONFLICT,
                severity=ConflictSeverity.WARN,
                resource_key=None,
                symbol=None,
                strategy=None,
                detected_at=datetime.now(timezone.utc),
                evidence={"state_a": session_a_state, "state_b": session_b_state},
                resolution_options=["warn_only"],
                blocking=False,
                policy_version=policy_version,
            ))
        return conflicts
