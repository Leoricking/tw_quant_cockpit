"""
paper_trading/multi_session/coordination_policy_v166.py — Coordination Policy v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List
from paper_trading.multi_session.models_v166 import CoordinationPolicy

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True

DEFAULT_FORBIDDEN_ACTIONS = [
    "real_order_creation",
    "broker_execution",
    "production_capital_movement",
    "external_coordination_bus",
    "distributed_lock_service",
    "automatic_live_session_resume",
    "automatic_global_risk_override",
    "automatic_capital_reallocation",
    "automatic_session_start",
    "automatic_session_stop",
    "production_process_control",
    "subprocess_control",
    "network_coordination",
    "production_db_write",
    "formal_ledger_write",
]


def make_default_policy(
    policy_id: str = "default_v166",
    version: str = "1.6.6",
    max_concurrent_sessions: int = 10,
) -> CoordinationPolicy:
    return CoordinationPolicy(
        policy_id=policy_id,
        version=version,
        max_concurrent_sessions=max_concurrent_sessions,
        priority_rules={
            "model": "weighted_priority",
            "aging_factor": 0.1,
            "max_consecutive_grants": 5,
            "deterministic_tie_break": True,
        },
        fairness_rules={
            "mode": "aging_weighted_fifo",
            "starvation_threshold_rounds": 10,
            "escalation": "recommend_only",
        },
        resource_rules={
            "allow_partial_grant": True,
            "allow_wait": True,
            "max_wait_rounds": 5,
            "idempotent_release": True,
        },
        symbol_overlap_rules={
            "direction_conflict": "BLOCK",
            "same_direction_over_concentration": "WARN",
            "max_overlap_ratio": 0.5,
        },
        strategy_conflict_rules={
            "duplicate_strategy": "BLOCK",
            "correlated_cluster": "WARN",
            "incompatible_horizon": "WARN",
            "stale_signal": "WARN",
        },
        risk_aggregation_rules={
            "aggregate_gross_limit": 1.0,
            "concentration_limit": 0.3,
            "action_on_exceed": "BLOCK",
        },
        capital_rules={
            "paper_only": True,
            "over_allocation_action": "BLOCK",
            "partial_grant_allowed": True,
            "no_real_capital_movement": True,
        },
        event_ordering_rules={
            "mode": "global_logical_sequence",
            "tie_break": "source_session_id",
            "late_event_action": "WARN",
            "duplicate_action": "DEDUP",
        },
        pause_rules={
            "auto_pause_on_conflict": False,
            "require_explicit_pause": True,
        },
        resume_rules={
            "require_eligibility_check": True,
            "require_safety_check": True,
            "require_conflict_check": True,
            "require_resource_check": True,
            "require_risk_check": True,
            "require_state_verification": True,
            "require_explicit_decision": True,
            "no_auto_resume": True,
        },
        failure_propagation_rules={
            "isolated_failure": True,
            "no_default_cascade": True,
            "shared_dependency_action": "BLOCK_DEPENDENT",
        },
        deadlock_rules={
            "detection": "wait_for_graph",
            "action": "mark_blocked",
            "auto_kill": False,
        },
        starvation_rules={
            "threshold_rounds": 10,
            "action": "recommend_escalation",
            "auto_production_priority": False,
        },
        forbidden_actions=DEFAULT_FORBIDDEN_ACTIONS,
    )
