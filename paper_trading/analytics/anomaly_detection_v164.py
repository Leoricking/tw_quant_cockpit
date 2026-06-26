"""
paper_trading/analytics/anomaly_detection_v164.py — Anomaly Detection v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
Deterministic rules only. No online learning. No auto session control.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional
import statistics
import uuid

from paper_trading.analytics.enums_v164 import AnomalySeverity, MetricQuality
from paper_trading.analytics.models_v164 import AnomalyRecord

NO_REAL_ORDERS = True
PAPER_ONLY = True
ONLINE_LEARNING_ENABLED = False
AUTO_SESSION_CONTROL_ENABLED = False
AUTO_STRATEGY_CHANGE_ENABLED = False

ANOMALY_RULE_VERSION = "1.6.4"


class AnomalyDetector:
    """
    Deterministic anomaly detection using versioned rules.
    Allowed: threshold, rolling median, MAD, IQR, historical baseline deviation.
    Forbidden: unversioned black-box models, online learning, auto-control.
    """

    def detect_threshold(
        self,
        metric_name: str,
        observed: Decimal,
        threshold: Decimal,
        severity: AnomalySeverity = AnomalySeverity.MEDIUM,
        expected: Optional[Decimal] = None,
        evidence: Optional[List[str]] = None,
        as_of: Any = None,
    ) -> Optional[AnomalyRecord]:
        """Threshold-based anomaly detection."""
        if observed <= threshold:
            return None
        return AnomalyRecord(
            anomaly_id=str(uuid.uuid4()),
            rule_id=f"threshold_{metric_name}",
            rule_version=ANOMALY_RULE_VERSION,
            metric=metric_name,
            observed=observed,
            expected=expected or threshold,
            threshold=threshold,
            severity=severity,
            evidence=evidence or [],
            as_of=as_of,
        )

    def detect_mad(
        self,
        metric_name: str,
        values: List[float],
        current: float,
        k: float = 3.5,
        severity: AnomalySeverity = AnomalySeverity.MEDIUM,
        as_of: Any = None,
    ) -> Optional[AnomalyRecord]:
        """Median Absolute Deviation anomaly detection."""
        if len(values) < 5:
            return None
        median = statistics.median(values)
        deviations = [abs(v - median) for v in values]
        mad = statistics.median(deviations)
        if mad == 0:
            return None
        modified_z = abs(current - median) / (1.4826 * mad)
        if modified_z <= k:
            return None
        return AnomalyRecord(
            anomaly_id=str(uuid.uuid4()),
            rule_id=f"mad_{metric_name}",
            rule_version=ANOMALY_RULE_VERSION,
            metric=metric_name,
            observed=Decimal(str(current)),
            expected=Decimal(str(median)),
            threshold=Decimal(str(k)),
            severity=severity,
            evidence=[f"MAD modified-z={modified_z:.2f} > k={k}"],
            as_of=as_of,
        )

    def detect_iqr(
        self,
        metric_name: str,
        values: List[float],
        current: float,
        multiplier: float = 1.5,
        severity: AnomalySeverity = AnomalySeverity.MEDIUM,
        as_of: Any = None,
    ) -> Optional[AnomalyRecord]:
        """IQR-based outlier detection."""
        if len(values) < 4:
            return None
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        q1 = sorted_vals[n // 4]
        q3 = sorted_vals[3 * n // 4]
        iqr = q3 - q1
        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr
        if lower <= current <= upper:
            return None
        return AnomalyRecord(
            anomaly_id=str(uuid.uuid4()),
            rule_id=f"iqr_{metric_name}",
            rule_version=ANOMALY_RULE_VERSION,
            metric=metric_name,
            observed=Decimal(str(current)),
            expected=Decimal(str((q1 + q3) / 2)),
            threshold=Decimal(str(upper)),
            severity=severity,
            evidence=[f"IQR bounds=[{lower:.2f},{upper:.2f}] current={current:.2f}"],
            as_of=as_of,
        )

    def detect_baseline_deviation(
        self,
        metric_name: str,
        current: Decimal,
        baseline: Decimal,
        deviation_threshold_pct: Decimal,
        severity: AnomalySeverity = AnomalySeverity.MEDIUM,
        as_of: Any = None,
    ) -> Optional[AnomalyRecord]:
        """Historical baseline deviation detection."""
        if baseline == Decimal("0"):
            return None
        deviation_pct = abs(current - baseline) / abs(baseline)
        if deviation_pct <= deviation_threshold_pct:
            return None
        return AnomalyRecord(
            anomaly_id=str(uuid.uuid4()),
            rule_id=f"baseline_deviation_{metric_name}",
            rule_version=ANOMALY_RULE_VERSION,
            metric=metric_name,
            observed=current,
            expected=baseline,
            threshold=deviation_threshold_pct,
            severity=severity,
            evidence=[f"Deviation {deviation_pct:.1%} > threshold {deviation_threshold_pct:.1%}"],
            as_of=as_of,
        )


__all__ = ["AnomalyDetector", "ANOMALY_RULE_VERSION"]
