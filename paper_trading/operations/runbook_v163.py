"""
Runbooks v1.6.3 — Versioned, paper-only.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
Prohibited: connect broker, submit real order, sync real account,
            modify real position, write formal Portfolio Ledger,
            production auto-recovery.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


PROHIBITED_ACTIONS = [
    "connect_broker",
    "submit_real_order",
    "sync_real_account",
    "modify_real_position",
    "write_formal_portfolio_ledger",
    "production_auto_recovery",
]


@dataclass
class Runbook:
    runbook_id:          str
    name:                str
    trigger:             str
    severity:            str
    prerequisites:       List[str]      = field(default_factory=list)
    diagnosis_steps:     List[str]      = field(default_factory=list)
    safe_actions:        List[str]      = field(default_factory=list)
    prohibited_actions:  List[str]      = field(default_factory=list)
    validation:          List[str]      = field(default_factory=list)
    recovery:            List[str]      = field(default_factory=list)
    closure_criteria:    List[str]      = field(default_factory=list)
    version:             str            = "1.6.3"
    paper_only:          bool           = True
    research_only:       bool           = True

    def __post_init__(self):
        # Always include all prohibited actions
        for pa in PROHIBITED_ACTIONS:
            if pa not in self.prohibited_actions:
                self.prohibited_actions.append(pa)


_COMMON_SAFE = ["pause_paper_session", "check_health", "run_recovery_drill", "review_audit_trail"]
_COMMON_CLOSURE = ["health_status=HEALTHY", "no_critical_alerts", "incident_CLOSED"]


RUNBOOKS: List[Runbook] = [
    Runbook(
        "rb_market_disconnect", "Market Data Disconnect",
        trigger="market_data_disconnected alert",
        severity="CRITICAL",
        prerequisites=["paper session accessible"],
        diagnosis_steps=["check heartbeat_age", "check reconnect_count", "check feed status"],
        safe_actions=_COMMON_SAFE + ["pause_market_data_session"],
        validation=["heartbeat_age < threshold"],
        recovery=["resume after validation"],
        closure_criteria=_COMMON_CLOSURE,
    ),
    Runbook(
        "rb_stale_data", "Stale Data",
        trigger="market_data_stale alert",
        severity="ERROR",
        prerequisites=["data session accessible"],
        diagnosis_steps=["check freshness_age", "check data pipeline"],
        safe_actions=_COMMON_SAFE,
        validation=["freshness_age < threshold"],
        recovery=["resume after freshness restored"],
        closure_criteria=_COMMON_CLOSURE,
    ),
    Runbook(
        "rb_sequence_gap", "Sequence Gap",
        trigger="sequence_gap_detected alert",
        severity="WARNING",
        prerequisites=["market data accessible"],
        diagnosis_steps=["check sequence_gap_count", "check source integrity"],
        safe_actions=_COMMON_SAFE,
        validation=["sequence_gap_count = 0"],
        recovery=["replay missing events from fixture if available"],
        closure_criteria=_COMMON_CLOSURE,
    ),
    Runbook(
        "rb_kill_switch", "Paper Kill Switch",
        trigger="paper_kill_switch_active alert",
        severity="CRITICAL",
        prerequisites=["supervisor accessible"],
        diagnosis_steps=["check kill_switch reason", "check incident timeline"],
        safe_actions=_COMMON_SAFE,
        validation=["kill_switch_inactive", "health=HEALTHY"],
        recovery=["explicit resume required after validation"],
        closure_criteria=_COMMON_CLOSURE,
    ),
    Runbook(
        "rb_risk_block_spike", "Paper Risk Block Spike",
        trigger="paper_risk_blocks_spike alert",
        severity="WARNING",
        diagnosis_steps=["check risk_block_count", "check strategy config"],
        safe_actions=_COMMON_SAFE,
        validation=["risk_block_count within threshold"],
        recovery=["resume after risk review"],
        closure_criteria=_COMMON_CLOSURE,
    ),
    Runbook(
        "rb_strategy_failure", "Strategy Failure",
        trigger="strategy_error_spike alert",
        severity="ERROR",
        diagnosis_steps=["check strategy_error_count", "review signal logs"],
        safe_actions=_COMMON_SAFE + ["halt_paper_strategy"],
        validation=["strategy_error_count < threshold"],
        recovery=["explicit resume after validation"],
        closure_criteria=_COMMON_CLOSURE,
    ),
    Runbook(
        "rb_checkpoint_corruption", "Checkpoint Corruption",
        trigger="recovery_failed alert with checkpoint hash mismatch",
        severity="CRITICAL",
        diagnosis_steps=["compare checkpoint hash", "review audit trail"],
        safe_actions=_COMMON_SAFE,
        validation=["checkpoint hash verified", "lineage complete"],
        recovery=["restore from last valid checkpoint"],
        closure_criteria=_COMMON_CLOSURE,
    ),
    Runbook(
        "rb_replay_mismatch", "Replay Mismatch",
        trigger="replay_mismatch alert",
        severity="ERROR",
        diagnosis_steps=["compare replay hash with original", "check seed and clock"],
        safe_actions=_COMMON_SAFE,
        validation=["replay_hash matches", "no_policy_drift"],
        recovery=["investigate non-determinism source"],
        closure_criteria=_COMMON_CLOSURE,
    ),
    Runbook(
        "rb_lineage_failure", "Lineage Failure",
        trigger="lineage_missing alert",
        severity="ERROR",
        diagnosis_steps=["check orphan metrics", "check audit chain"],
        safe_actions=_COMMON_SAFE,
        validation=["orphan_count=0", "lineage_complete"],
        recovery=["rebuild lineage from audit trail"],
        closure_criteria=_COMMON_CLOSURE,
    ),
    Runbook(
        "rb_storage_failure", "Storage Failure",
        trigger="storage_failure alert",
        severity="CRITICAL",
        diagnosis_steps=["check store health", "check disk space"],
        safe_actions=_COMMON_SAFE + ["halt_session_gracefully"],
        validation=["store_write_ok", "store_read_ok"],
        recovery=["recover from last valid checkpoint"],
        closure_criteria=_COMMON_CLOSURE,
    ),
    Runbook(
        "rb_safety_violation", "Safety Violation",
        trigger="safety_violation alert",
        severity="CRITICAL",
        diagnosis_steps=["identify violated safety flag", "check all safety invariants"],
        safe_actions=["halt_all_paper_sessions", "review_safety_contract"],
        validation=["all_safety_flags_valid", "safety_contract_signed"],
        recovery=["explicit human review required before resume"],
        closure_criteria=_COMMON_CLOSURE + ["human_sign_off_received"],
    ),
]


class RunbookRegistry:
    def __init__(self):
        self._runbooks: Dict[str, Runbook] = {}
        for rb in RUNBOOKS:
            self._runbooks[rb.runbook_id] = rb

    def get(self, runbook_id: str) -> Optional[Runbook]:
        return self._runbooks.get(runbook_id)

    def list_all(self) -> List[Runbook]:
        return list(self._runbooks.values())

    def count(self) -> int:
        return len(self._runbooks)

    def verify_prohibited_actions(self) -> bool:
        """All runbooks must prohibit all standard prohibited actions."""
        for rb in self._runbooks.values():
            for pa in PROHIBITED_ACTIONS:
                if pa not in rb.prohibited_actions:
                    return False
        return True


__all__ = ["Runbook", "RunbookRegistry", "RUNBOOKS", "PROHIBITED_ACTIONS"]
