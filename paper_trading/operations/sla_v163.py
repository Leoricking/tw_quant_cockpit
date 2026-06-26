"""
Research-only SLA Policy v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
NOT investment advice. Does not auto-repair production.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple

from paper_trading.operations.enums_v163 import SLAStatus


@dataclass
class SLAPolicy:
    sla_id:        str
    name:          str
    metric:        str          # what is being measured
    warning_secs:  float        # seconds before WARNING
    breach_secs:   float        # seconds before BREACHED
    version:       str          = "1.6.3"
    enabled:       bool         = True
    description:   str          = ""

    def __post_init__(self):
        assert self.warning_secs <= self.breach_secs, (
            f"SLA warning_secs must be <= breach_secs for {self.sla_id}"
        )


def evaluate_sla(
    policy: Optional[SLAPolicy],
    age_seconds: Optional[float],
) -> Tuple[SLAStatus, str]:
    if policy is None:
        return SLAStatus.BLOCKED, "Missing SLA policy — BLOCKED"

    if not policy.enabled:
        return SLAStatus.UNKNOWN, "SLA policy disabled"

    if age_seconds is None:
        return SLAStatus.UNKNOWN, "No measurement available"

    if age_seconds >= policy.breach_secs:
        return SLAStatus.BREACHED, f"{policy.name}: age={age_seconds:.1f}s >= breach={policy.breach_secs}s"
    if age_seconds >= policy.warning_secs:
        return SLAStatus.WARNING, f"{policy.name}: age={age_seconds:.1f}s >= warning={policy.warning_secs}s"
    return SLAStatus.PASS, f"{policy.name}: age={age_seconds:.1f}s OK"


RESEARCH_SLA_POLICIES: List[SLAPolicy] = [
    SLAPolicy("sla_heartbeat",      "Heartbeat Freshness",        "heartbeat_age",          warning_secs=30,   breach_secs=120),
    SLAPolicy("sla_data_fresh",     "Data Freshness",             "freshness_age",           warning_secs=60,   breach_secs=300),
    SLAPolicy("sla_startup",        "Session Startup Duration",   "session_startup_duration",warning_secs=30,   breach_secs=120),
    SLAPolicy("sla_pause",          "Pause Duration",             "pause_duration",          warning_secs=60,   breach_secs=300),
    SLAPolicy("sla_halt",           "Halt Duration",              "halt_duration",           warning_secs=300,  breach_secs=1800),
    SLAPolicy("sla_checkpoint",     "Checkpoint Age",             "checkpoint_age",          warning_secs=300,  breach_secs=900),
    SLAPolicy("sla_recovery",       "Recovery Duration",          "recovery_duration",       warning_secs=120,  breach_secs=600),
    SLAPolicy("sla_alert_ack",      "Alert Acknowledgement Age",  "alert_acknowledgement_age",warning_secs=300, breach_secs=900),
    SLAPolicy("sla_incident_res",   "Incident Resolution Age",    "incident_resolution_age", warning_secs=1800, breach_secs=7200),
]


class SLARegistry:
    def __init__(self):
        self._policies: Dict[str, SLAPolicy] = {}
        for p in RESEARCH_SLA_POLICIES:
            self._policies[p.sla_id] = p

    def get(self, sla_id: str) -> Optional[SLAPolicy]:
        return self._policies.get(sla_id)

    def get_by_metric(self, metric: str) -> Optional[SLAPolicy]:
        for p in self._policies.values():
            if p.metric == metric:
                return p
        return None

    def evaluate(self, sla_id: str, age_seconds: Optional[float]) -> Tuple[SLAStatus, str]:
        return evaluate_sla(self.get(sla_id), age_seconds)

    def list_all(self) -> List[SLAPolicy]:
        return list(self._policies.values())

    def count(self) -> int:
        return len(self._policies)


__all__ = ["SLAPolicy", "SLARegistry", "evaluate_sla", "RESEARCH_SLA_POLICIES"]
