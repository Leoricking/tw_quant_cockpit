"""
paper_trading/analytics/session_analytics_v164.py — Session Analytics Engine v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
Coordinates all analytics modules for a complete session analysis.
"""
from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid

from paper_trading.analytics.enums_v164 import ReviewScope, MetricQuality
from paper_trading.analytics.models_v164 import (
    OperationalAnalyticsRequest, OperationalAnalyticsResult,
    AnalyticsLineage,
)
from paper_trading.analytics.session_summary_v164 import SessionSummaryBuilder
from paper_trading.analytics.operational_metrics_v164 import OperationalMetricsComputer
from paper_trading.analytics.performance_metrics_v164 import PaperPerformanceMetricsComputer
from paper_trading.analytics.execution_quality_v164 import ExecutionQualityAnalyzer
from paper_trading.analytics.signal_quality_v164 import SignalQualityAnalyzer
from paper_trading.analytics.anomaly_detection_v164 import AnomalyDetector
from paper_trading.analytics.lineage_v164 import AnalyticsLineageTracker
from paper_trading.analytics.snapshot_v164 import AnalyticsSnapshotManager
from paper_trading.analytics.reproducibility_v164 import ReproducibilityChecker

NO_REAL_ORDERS = True
NO_BROKER = True
PAPER_ONLY = True
AUTO_STRATEGY_CHANGE_ENABLED = False
AUTO_DEPLOYMENT_ENABLED = False


class SessionAnalyticsEngine:
    """
    Coordinates all analytics for a single session.
    PIT-safe. Deterministic. Append-only. No broker. No real orders.
    """

    def __init__(self) -> None:
        self._summary_builder = SessionSummaryBuilder()
        self._metrics_computer = OperationalMetricsComputer()
        self._perf_computer = PaperPerformanceMetricsComputer()
        self._exec_analyzer = ExecutionQualityAnalyzer()
        self._signal_analyzer = SignalQualityAnalyzer()
        self._anomaly_detector = AnomalyDetector()
        self._lineage_tracker = AnalyticsLineageTracker()
        self._snapshot_manager = AnalyticsSnapshotManager()
        self._repro_checker = ReproducibilityChecker()

    def run(
        self,
        request: OperationalAnalyticsRequest,
        raw_data: Optional[Dict[str, Any]] = None,
    ) -> OperationalAnalyticsResult:
        """
        Run full analytics for a session. Returns OperationalAnalyticsResult.
        """
        request.validate()
        raw_data = raw_data or {}
        analytics_id = str(uuid.uuid4())
        now = datetime.now(tz=timezone.utc)

        # Session summary
        summary = self._summary_builder.build(
            session_id=request.session_id,
            as_of=request.as_of,
            raw_data=raw_data,
        )
        summary.validate_pit()

        # Metrics
        session_metrics = self._metrics_computer.compute_session_metrics(raw_data)
        market_metrics = self._metrics_computer.compute_market_data_metrics(
            raw_data.get("market_data", {})
        )
        all_metrics = {**session_metrics, **market_metrics}

        # Performance
        perf = self._perf_computer.compute(request.session_id, raw_data)

        # Execution quality
        exec_quality = self._exec_analyzer.analyze(request.session_id, raw_data)

        # Signal quality
        signal_quality = self._signal_analyzer.analyze(request.session_id, raw_data)

        # Anomaly detection
        anomalies = []
        downtime_ratio = raw_data.get("downtime_ratio")
        if downtime_ratio is not None:
            anomaly = self._anomaly_detector.detect_threshold(
                metric_name="downtime_ratio",
                observed=Decimal(str(downtime_ratio)),
                threshold=Decimal("0.2"),
                as_of=request.as_of,
            )
            if anomaly:
                anomalies.append(anomaly)

        # Lineage
        lineage_obj = self._lineage_tracker.create_lineage(
            analytics_id=analytics_id,
            source_session_ids=[request.session_id],
            as_of=request.as_of,
            metric_policy_version=request.metric_policy_version,
            attribution_policy_version=request.attribution_policy_version,
        )
        lineage_dict = self._lineage_tracker.to_dict(lineage_obj)

        # Reproducibility
        repro_record = self._repro_checker.record(
            analytics_id=analytics_id,
            input_data={"session_id": request.session_id, "as_of": str(request.as_of)},
            output_data={"analytics_id": analytics_id},
            metric_policy_version=request.metric_policy_version,
        )

        # Determine overall data quality
        if perf.quality == MetricQuality.VALID and signal_quality.quality == MetricQuality.VALID:
            data_quality = MetricQuality.VALID
        elif perf.quality == MetricQuality.INSUFFICIENT_DATA:
            data_quality = MetricQuality.INSUFFICIENT_DATA
        else:
            data_quality = MetricQuality.PARTIAL

        result = OperationalAnalyticsResult(
            analytics_id=analytics_id,
            session_id=request.session_id,
            scope=request.scope,
            as_of=request.as_of,
            metrics=all_metrics,
            anomalies=anomalies,
            incidents=raw_data.get("incidents", []),
            alerts=raw_data.get("alerts", []),
            recovery_events=raw_data.get("recovery_events", []),
            data_quality=data_quality,
            lineage=lineage_dict,
            reproducibility_hash=repro_record.reproducibility_hash,
            created_at=now,
            metric_policy_version=request.metric_policy_version,
            attribution_policy_version=request.attribution_policy_version,
        )

        return result


__all__ = ["SessionAnalyticsEngine"]
