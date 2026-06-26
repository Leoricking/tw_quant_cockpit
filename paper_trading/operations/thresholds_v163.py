"""
Threshold Policy v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from paper_trading.operations.enums_v163 import HealthStatus


BLOCKED_STATUS = "BLOCKED"


@dataclass
class ThresholdPolicy:
    threshold_id:      str
    metric_name:       str
    warning:           float
    degraded:          float
    critical:          float
    comparison:        str   = "gt"   # gt, lt, gte, lte
    evaluation_window: int   = 60     # seconds
    minimum_samples:   int   = 1
    cooldown:          int   = 0      # seconds
    suppression:       bool  = False
    enabled:           bool  = True
    version:           str   = "1.6.3"


BLOCKED_THRESHOLD = object()   # sentinel for missing policy


def _compare(value: float, threshold: float, op: str) -> bool:
    if op == "gt":  return value > threshold
    if op == "lt":  return value < threshold
    if op == "gte": return value >= threshold
    if op == "lte": return value <= threshold
    return False


def evaluate_threshold(
    metric_name: str,
    value: Optional[float],
    policy: Optional[ThresholdPolicy],
) -> Tuple[HealthStatus, str]:
    if policy is None:
        return HealthStatus.BLOCKED, f"Missing threshold policy for {metric_name} — BLOCKED"

    if not policy.enabled:
        return HealthStatus.UNKNOWN, "Threshold policy disabled"

    if value is None:
        return HealthStatus.UNKNOWN, "Insufficient data"

    op = policy.comparison
    if _compare(value, policy.critical, op):
        return HealthStatus.CRITICAL, f"{metric_name}={value} exceeds critical={policy.critical}"
    if _compare(value, policy.degraded, op):
        return HealthStatus.DEGRADED, f"{metric_name}={value} exceeds degraded={policy.degraded}"
    if _compare(value, policy.warning, op):
        return HealthStatus.WARNING, f"{metric_name}={value} exceeds warning={policy.warning}"
    return HealthStatus.HEALTHY, f"{metric_name}={value} within bounds"


# Research-only fixture thresholds (NOT production standards)
FIXTURE_THRESHOLDS: List[ThresholdPolicy] = [
    ThresholdPolicy("thr_heartbeat_age",     "heartbeat_age",      warning=30,  degraded=60,  critical=120),
    ThresholdPolicy("thr_freshness_age",     "freshness_age",      warning=60,  degraded=120, critical=300),
    ThresholdPolicy("thr_seq_gap",           "sequence_gap_count", warning=1,   degraded=5,   critical=20),
    ThresholdPolicy("thr_risk_blocks",       "risk_block_count",   warning=5,   degraded=20,  critical=50),
    ThresholdPolicy("thr_strategy_errors",   "strategy_error_count", warning=3, degraded=10,  critical=30),
    ThresholdPolicy("thr_open_incidents",    "open_incident_count",warning=1,   degraded=3,   critical=10),
]


class ThresholdRegistry:
    def __init__(self):
        self._policies: Dict[str, ThresholdPolicy] = {}
        for p in FIXTURE_THRESHOLDS:
            self._policies[p.threshold_id] = p

    def register(self, policy: ThresholdPolicy) -> bool:
        from paper_trading.operations.validation_v163 import validate_threshold_ordering
        ok, msg = validate_threshold_ordering(policy.warning, policy.degraded, policy.critical)
        if not ok:
            return False
        self._policies[policy.threshold_id] = policy
        return True

    def get_by_id(self, threshold_id: str) -> Optional[ThresholdPolicy]:
        return self._policies.get(threshold_id)

    def get_by_metric(self, metric_name: str) -> Optional[ThresholdPolicy]:
        for p in self._policies.values():
            if p.metric_name == metric_name:
                return p
        return None

    def evaluate(self, metric_name: str, value: Optional[float]) -> Tuple[HealthStatus, str]:
        policy = self.get_by_metric(metric_name)
        return evaluate_threshold(metric_name, value, policy)

    def list_all(self) -> List[ThresholdPolicy]:
        return list(self._policies.values())

    def count(self) -> int:
        return len(self._policies)


__all__ = ["ThresholdPolicy", "ThresholdRegistry", "evaluate_threshold", "FIXTURE_THRESHOLDS"]
