"""
Alert Rules v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
No external notification. No PagerDuty. No webhook.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from paper_trading.operations.enums_v163 import AlertSeverity, IncidentCategory


@dataclass
class AlertRule:
    rule_id:          str
    name:             str
    source_metrics:   List[str]
    condition:        str         # description
    severity:         AlertSeverity
    dedup_key:        str
    suppression_window: int = 300  # seconds
    cooldown:         int   = 60   # seconds
    auto_resolve:     bool  = True
    runbook_id:       str   = ""
    enabled:          bool  = True
    version:          str   = "1.6.3"
    category:         str   = ""


ALERT_RULES: List[AlertRule] = [
    AlertRule("ar_md_disconnect",     "Market Data Disconnected",      ["reconnect_count"],        "reconnect_count > 0",              AlertSeverity.CRITICAL, "md:disconnect",     runbook_id="rb_market_disconnect"),
    AlertRule("ar_md_stale",          "Market Data Stale",             ["freshness_age"],           "freshness_age > threshold",         AlertSeverity.ERROR,   "md:stale",          runbook_id="rb_stale_data"),
    AlertRule("ar_md_future_ts",      "Market Data Future Timestamp",  ["rejected_event_count"],    "future timestamp detected",         AlertSeverity.ERROR,   "md:future_ts"),
    AlertRule("ar_seq_gap",           "Sequence Gap Detected",         ["sequence_gap_count"],      "sequence_gap_count > 0",            AlertSeverity.WARNING, "md:seq_gap"),
    AlertRule("ar_data_quality",      "Data Quality Degraded",         ["data_acceptance_ratio"],   "acceptance_ratio < threshold",      AlertSeverity.WARNING, "md:quality"),
    AlertRule("ar_paper_not_running", "Paper Session Not Running",     [],                          "paper session status != RUNNING",   AlertSeverity.ERROR,   "paper:not_running"),
    AlertRule("ar_kill_switch",       "Paper Kill Switch Active",      ["kill_switch_count"],       "kill_switch_count > 0",             AlertSeverity.CRITICAL,"paper:kill_switch"),
    AlertRule("ar_risk_spike",        "Paper Risk Blocks Spike",       ["risk_block_count"],        "risk_block_count > threshold",      AlertSeverity.WARNING, "paper:risk_spike"),
    AlertRule("ar_order_reject_spike","Paper Order Rejection Spike",   ["rejected_order_count"],    "rejected_order_count > threshold",  AlertSeverity.WARNING, "paper:order_reject"),
    AlertRule("ar_strategy_errors",   "Strategy Error Spike",          ["strategy_error_count"],    "strategy_error_count > threshold",  AlertSeverity.ERROR,   "strategy:errors"),
    AlertRule("ar_proposal_blocked",  "Strategy Proposal Blocked Spike",["blocked_decision_count"], "blocked_decision_count > threshold",AlertSeverity.WARNING, "strategy:proposals"),
    AlertRule("ar_conflict_spike",    "Strategy Conflict Spike",       ["conflict_count"],          "conflict_count > threshold",        AlertSeverity.WARNING, "strategy:conflicts"),
    AlertRule("ar_checkpoint_stale",  "Checkpoint Stale",              ["last_checkpoint_age"],     "checkpoint_age > threshold",        AlertSeverity.ERROR,   "ops:checkpoint_stale"),
    AlertRule("ar_recovery_failed",   "Recovery Failed",               [],                          "recovery result != RECOVERED",      AlertSeverity.CRITICAL,"ops:recovery_failed", runbook_id="rb_checkpoint_corruption"),
    AlertRule("ar_replay_mismatch",   "Replay Mismatch",               [],                          "replay hash mismatch detected",     AlertSeverity.ERROR,   "ops:replay_mismatch"),
    AlertRule("ar_lineage_missing",   "Lineage Missing",               [],                          "orphan entity detected",            AlertSeverity.ERROR,   "ops:lineage_missing"),
    AlertRule("ar_storage_failure",   "Storage Failure",               [],                          "store write/read failure",          AlertSeverity.CRITICAL,"ops:storage_failure"),
    AlertRule("ar_safety_violation",  "Safety Violation",              [],                          "safety flag violated",              AlertSeverity.CRITICAL,"ops:safety",          runbook_id="rb_safety_violation"),
]


class AlertRuleRegistry:
    def __init__(self):
        self._rules: Dict[str, AlertRule] = {}
        for r in ALERT_RULES:
            self._rules[r.rule_id] = r

    def get(self, rule_id: str) -> Optional[AlertRule]:
        return self._rules.get(rule_id)

    def list_enabled(self) -> List[AlertRule]:
        return [r for r in self._rules.values() if r.enabled]

    def list_all(self) -> List[AlertRule]:
        return list(self._rules.values())

    def count(self) -> int:
        return len(self._rules)


__all__ = ["AlertRule", "AlertRuleRegistry", "ALERT_RULES"]
