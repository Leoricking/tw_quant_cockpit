"""
Metrics Registry v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from paper_trading.operations.enums_v163 import (
    ManagedSessionType, MetricType, AggregationType,
)


@dataclass
class MetricDefinition:
    metric_name:      str
    session_type:     ManagedSessionType
    metric_type:      MetricType
    unit:             str
    aggregation:      AggregationType
    threshold_policy: str          = ""
    version:          str          = "1.6.3"
    description:      str          = ""
    docs:             str          = ""
    tests:            List[str]    = field(default_factory=list)
    source:           str          = ""


# ── Market Data metrics ────────────────────────────────────────────────
_MD = ManagedSessionType.MARKET_DATA
_PT = ManagedSessionType.PAPER_TRADING
_PS = ManagedSessionType.PAPER_STRATEGY
_CM = ManagedSessionType.COMPOSITE

MARKET_DATA_METRICS: List[MetricDefinition] = [
    MetricDefinition("event_rate",             _MD, MetricType.GAUGE,   "events/s",  AggregationType.RATE,  description="Event ingestion rate"),
    MetricDefinition("quote_rate",             _MD, MetricType.GAUGE,   "quotes/s",  AggregationType.RATE,  description="Quote ingestion rate"),
    MetricDefinition("trade_rate",             _MD, MetricType.GAUGE,   "trades/s",  AggregationType.RATE,  description="Trade ingestion rate"),
    MetricDefinition("heartbeat_age",          _MD, MetricType.GAUGE,   "seconds",   AggregationType.LAST,  description="Age of last heartbeat"),
    MetricDefinition("freshness_age",          _MD, MetricType.GAUGE,   "seconds",   AggregationType.LAST,  description="Age of freshest data"),
    MetricDefinition("transport_delay",        _MD, MetricType.DURATION,"ms",        AggregationType.P95,   description="Transport-level latency"),
    MetricDefinition("market_delay",           _MD, MetricType.DURATION,"ms",        AggregationType.P95,   description="Exchange-to-consumer delay"),
    MetricDefinition("sequence_gap_count",     _MD, MetricType.COUNTER, "count",     AggregationType.SUM,   description="Sequence gaps detected"),
    MetricDefinition("duplicate_count",        _MD, MetricType.COUNTER, "count",     AggregationType.SUM,   description="Duplicate events received"),
    MetricDefinition("rejected_event_count",   _MD, MetricType.COUNTER, "count",     AggregationType.SUM,   description="Events rejected by validation"),
    MetricDefinition("anomaly_count",          _MD, MetricType.COUNTER, "count",     AggregationType.SUM,   description="Anomalies detected"),
    MetricDefinition("reconnect_count",        _MD, MetricType.COUNTER, "count",     AggregationType.SUM,   description="Reconnect attempts"),
    MetricDefinition("failover_count",         _MD, MetricType.COUNTER, "count",     AggregationType.SUM,   description="Failover events"),
    MetricDefinition("data_acceptance_ratio",  _MD, MetricType.RATIO,   "ratio",     AggregationType.RATIO, description="Accepted / total events"),
]

# ── Paper Trading metrics ──────────────────────────────────────────────
PAPER_TRADING_METRICS: List[MetricDefinition] = [
    MetricDefinition("order_count",               _PT, MetricType.COUNTER, "count",   AggregationType.SUM,  description="Total paper orders"),
    MetricDefinition("open_order_count",          _PT, MetricType.GAUGE,   "count",   AggregationType.LAST, description="Open paper orders"),
    MetricDefinition("rejected_order_count",      _PT, MetricType.COUNTER, "count",   AggregationType.SUM,  description="Rejected paper orders"),
    MetricDefinition("fill_count",                _PT, MetricType.COUNTER, "count",   AggregationType.SUM,  description="Filled orders"),
    MetricDefinition("partial_fill_count",        _PT, MetricType.COUNTER, "count",   AggregationType.SUM,  description="Partial fills"),
    MetricDefinition("execution_latency",         _PT, MetricType.DURATION,"ms",      AggregationType.P95,  description="Paper execution latency"),
    MetricDefinition("slippage",                  _PT, MetricType.GAUGE,   "bps",     AggregationType.AVG,  description="Simulated slippage"),
    MetricDefinition("liquidity_rejection_count", _PT, MetricType.COUNTER, "count",   AggregationType.SUM,  description="Liquidity check rejections"),
    MetricDefinition("risk_block_count",          _PT, MetricType.COUNTER, "count",   AggregationType.SUM,  description="Risk-based blocks"),
    MetricDefinition("kill_switch_count",         _PT, MetricType.COUNTER, "count",   AggregationType.SUM,  description="Kill switch activations"),
    MetricDefinition("cash",                      _PT, MetricType.GAUGE,   "TWD",     AggregationType.LAST, description="Paper cash balance"),
    MetricDefinition("exposure",                  _PT, MetricType.GAUGE,   "TWD",     AggregationType.LAST, description="Paper gross exposure"),
    MetricDefinition("session_pnl",               _PT, MetricType.GAUGE,   "TWD",     AggregationType.LAST, description="Session paper P&L"),
    MetricDefinition("drawdown",                  _PT, MetricType.GAUGE,   "ratio",   AggregationType.LAST, description="Current paper drawdown"),
]

# ── Paper Strategy metrics ─────────────────────────────────────────────
PAPER_STRATEGY_METRICS: List[MetricDefinition] = [
    MetricDefinition("signal_count",                _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Signals received"),
    MetricDefinition("duplicate_signal_count",      _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Duplicate signals rejected"),
    MetricDefinition("suppressed_signal_count",     _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Suppressed signals"),
    MetricDefinition("decision_count",              _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Pipeline decisions made"),
    MetricDefinition("blocked_decision_count",      _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Blocked decisions"),
    MetricDefinition("proposal_count",              _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Proposals generated"),
    MetricDefinition("approved_proposal_count",     _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Approved proposals"),
    MetricDefinition("rejected_proposal_count",     _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Rejected proposals"),
    MetricDefinition("submitted_order_count",       _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Orders submitted to bridge"),
    MetricDefinition("conflict_count",              _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Signal conflicts"),
    MetricDefinition("cooldown_block_count",        _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Cooldown blocks"),
    MetricDefinition("rate_limit_block_count",      _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Rate limit blocks"),
    MetricDefinition("strategy_error_count",        _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Strategy errors"),
    MetricDefinition("recovery_count",              _PS, MetricType.COUNTER, "count", AggregationType.SUM,  description="Recovery attempts"),
]

# ── Composite metrics ──────────────────────────────────────────────────
COMPOSITE_METRICS: List[MetricDefinition] = [
    MetricDefinition("healthy_session_count",      _CM, MetricType.GAUGE, "count", AggregationType.LAST, description="Sessions in HEALTHY state"),
    MetricDefinition("degraded_session_count",     _CM, MetricType.GAUGE, "count", AggregationType.LAST, description="Sessions in DEGRADED state"),
    MetricDefinition("halted_session_count",       _CM, MetricType.GAUGE, "count", AggregationType.LAST, description="Sessions in HALTED state"),
    MetricDefinition("open_alert_count",           _CM, MetricType.GAUGE, "count", AggregationType.LAST, description="Open alerts"),
    MetricDefinition("critical_alert_count",       _CM, MetricType.GAUGE, "count", AggregationType.LAST, description="Critical-severity open alerts"),
    MetricDefinition("open_incident_count",        _CM, MetricType.GAUGE, "count", AggregationType.LAST, description="Open incidents"),
    MetricDefinition("unresolved_incident_count",  _CM, MetricType.GAUGE, "count", AggregationType.LAST, description="Unresolved incidents"),
    MetricDefinition("last_snapshot_age",          _CM, MetricType.GAUGE, "seconds", AggregationType.LAST, description="Age of last snapshot"),
    MetricDefinition("last_checkpoint_age",        _CM, MetricType.GAUGE, "seconds", AggregationType.LAST, description="Age of last checkpoint"),
]

ALL_METRICS: List[MetricDefinition] = (
    MARKET_DATA_METRICS + PAPER_TRADING_METRICS + PAPER_STRATEGY_METRICS + COMPOSITE_METRICS
)


class MetricsRegistry:
    def __init__(self):
        self._definitions: Dict[str, MetricDefinition] = {}
        for defn in ALL_METRICS:
            self._definitions[defn.metric_name] = defn

    def get(self, metric_name: str) -> Optional[MetricDefinition]:
        return self._definitions.get(metric_name)

    def list_all(self) -> List[MetricDefinition]:
        return list(self._definitions.values())

    def list_by_session_type(self, session_type: ManagedSessionType) -> List[MetricDefinition]:
        return [d for d in self._definitions.values() if d.session_type == session_type]

    def count(self) -> int:
        return len(self._definitions)

    def is_registered(self, metric_name: str) -> bool:
        return metric_name in self._definitions


__all__ = [
    "MetricDefinition", "MetricsRegistry",
    "MARKET_DATA_METRICS", "PAPER_TRADING_METRICS",
    "PAPER_STRATEGY_METRICS", "COMPOSITE_METRICS", "ALL_METRICS",
]
