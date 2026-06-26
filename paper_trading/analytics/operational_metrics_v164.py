"""
paper_trading/analytics/operational_metrics_v164.py — Operational Metrics v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional

from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True
METRIC_POLICY_VERSION = "1.6.4"


@dataclass
class MetricObservation:
    """A single computed metric."""
    metric_name: str
    value: Any
    unit: str
    quality: MetricQuality
    sample_count: int = 0
    policy_version: str = METRIC_POLICY_VERSION
    notes: str = ""


def _percentile(values: List[Decimal], pct: int) -> Optional[Decimal]:
    """Deterministic percentile. None if empty."""
    if not values:
        return None
    sorted_vals = sorted(values)
    idx = int(len(sorted_vals) * pct / 100)
    idx = min(idx, len(sorted_vals) - 1)
    return sorted_vals[idx]


class OperationalMetricsComputer:
    """
    Computes operational metrics from raw session data.
    policy_version locks the computation rules.
    """

    MINIMUM_SAMPLES = 5

    def __init__(self, policy_version: str = METRIC_POLICY_VERSION) -> None:
        self._policy_version = policy_version

    def compute_latency_metrics(self, latency_ms_list: List[float]) -> Dict[str, MetricObservation]:
        """Compute P50/P95/P99 latency metrics."""
        vals = [Decimal(str(v)) for v in latency_ms_list]
        count = len(vals)
        quality = MetricQuality.VALID if count >= self.MINIMUM_SAMPLES else MetricQuality.INSUFFICIENT_DATA

        p50 = _percentile(vals, 50)
        p95 = _percentile(vals, 95)
        p99 = _percentile(vals, 99)

        return {
            "latency_p50_ms": MetricObservation(
                "latency_p50_ms", p50, "ms", quality, count, self._policy_version,
            ),
            "latency_p95_ms": MetricObservation(
                "latency_p95_ms", p95, "ms", quality, count, self._policy_version,
            ),
            "latency_p99_ms": MetricObservation(
                "latency_p99_ms", p99, "ms", quality, count, self._policy_version,
            ),
        }

    def compute_session_metrics(self, raw: Dict[str, Any]) -> Dict[str, MetricObservation]:
        """Compute session-level operational metrics."""
        results: Dict[str, MetricObservation] = {}

        def _obs(name: str, val: Any, unit: str, count: int = 1) -> MetricObservation:
            q = MetricQuality.VALID if val is not None else MetricQuality.UNKNOWN
            return MetricObservation(name, val, unit, q, count, self._policy_version)

        results["event_throughput"] = _obs(
            "event_throughput", raw.get("event_count"), "events", raw.get("event_count", 0)
        )
        results["error_rate"] = _obs(
            "error_rate", raw.get("error_rate"), "ratio", raw.get("event_count", 0)
        )
        results["warning_rate"] = _obs(
            "warning_rate", raw.get("warning_rate"), "ratio", raw.get("event_count", 0)
        )
        results["downtime_ratio"] = _obs(
            "downtime_ratio", raw.get("downtime_ratio"), "ratio", 1
        )
        results["alerts_opened"] = _obs(
            "alerts_opened", raw.get("alerts_opened"), "count", 1
        )
        results["incidents_opened"] = _obs(
            "incidents_opened", raw.get("incidents_opened"), "count", 1
        )
        results["recovery_success_rate"] = _obs(
            "recovery_success_rate", raw.get("recovery_success_rate"), "ratio", 1
        )

        return results

    def compute_market_data_metrics(self, raw: Dict[str, Any]) -> Dict[str, MetricObservation]:
        """Compute market data quality metrics."""
        results: Dict[str, MetricObservation] = {}
        update_count = raw.get("update_count", 0) or 0

        def _obs(name: str, val: Any, unit: str) -> MetricObservation:
            q = MetricQuality.VALID if val is not None else MetricQuality.UNKNOWN
            return MetricObservation(name, val, unit, q, update_count, self._policy_version)

        results["update_count"] = _obs("update_count", raw.get("update_count"), "count")
        results["stale_count"] = _obs("stale_count", raw.get("stale_count"), "count")
        results["missing_intervals"] = _obs("missing_intervals", raw.get("missing_intervals"), "count")
        results["out_of_order_count"] = _obs("out_of_order_count", raw.get("out_of_order_count"), "count")
        results["duplicate_count"] = _obs("duplicate_count", raw.get("duplicate_count"), "count")
        results["freshness_ratio"] = _obs("freshness_ratio", raw.get("freshness_ratio"), "ratio")
        results["data_quality_score"] = _obs("data_quality_score", raw.get("quality_score"), "score_0_100")

        if raw.get("latency_ms_list"):
            latency_metrics = self.compute_latency_metrics(raw["latency_ms_list"])
            results.update(latency_metrics)

        return results

    def compute_strategy_metrics(self, raw: Dict[str, Any]) -> Dict[str, MetricObservation]:
        """Compute strategy metrics."""
        results: Dict[str, MetricObservation] = {}
        signals = raw.get("signals_generated") or 0

        def _obs(name: str, val: Any, unit: str) -> MetricObservation:
            q = MetricQuality.VALID if val is not None else MetricQuality.UNKNOWN
            return MetricObservation(name, val, unit, q, signals, self._policy_version)

        results["signals_generated"] = _obs("signals_generated", raw.get("signals_generated"), "count")
        results["signals_accepted"] = _obs("signals_accepted", raw.get("signals_accepted"), "count")
        results["signals_rejected"] = _obs("signals_rejected", raw.get("signals_rejected"), "count")
        results["signal_to_proposal_ratio"] = _obs("signal_to_proposal_ratio", raw.get("signal_to_proposal_ratio"), "ratio")
        results["proposal_to_fill_ratio"] = _obs("proposal_to_fill_ratio", raw.get("proposal_to_fill_ratio"), "ratio")

        return results


__all__ = ["MetricObservation", "OperationalMetricsComputer", "METRIC_POLICY_VERSION"]
