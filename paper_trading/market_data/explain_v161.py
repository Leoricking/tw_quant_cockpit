"""
paper_trading/market_data/explain_v161.py — Explain v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Provides human-readable explanations for quality decisions, freshness, sequence, failover.
"""
from __future__ import annotations
from typing import Optional, Dict, Any

from paper_trading.market_data.enums_v161 import (
    FreshnessStatus, SequenceStatus, DataQualityStatus,
    FeedFailureType, FailoverPolicy, ReconnectPolicy, SourceClass,
)

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


class MarketDataExplainer:
    """
    Generates human-readable explanations for market data decisions.
    Used for audit trails, debug output, and operator dashboards.
    """

    def explain_freshness(self, status: FreshnessStatus) -> str:
        explanations = {
            FreshnessStatus.FRESH: "Event arrived within freshness SLA. Data is current.",
            FreshnessStatus.DELAYED: "Event arrived with delay but within tolerance threshold.",
            FreshnessStatus.STALE: "Event is stale — older than delayed threshold but within expiry.",
            FreshnessStatus.EXPIRED: "Event has expired — older than stale threshold. Consider discarding.",
            FreshnessStatus.UNKNOWN: "Freshness cannot be determined (parse error or future timestamp).",
            FreshnessStatus.NOT_APPLICABLE: "Freshness is not applicable for REPLAY/FIXTURE/OFFLINE sources.",
        }
        return explanations.get(status, f"Unknown freshness status: {status}")

    def explain_sequence(self, status: SequenceStatus) -> str:
        explanations = {
            SequenceStatus.IN_ORDER: "Sequence number is as expected. No gaps.",
            SequenceStatus.GAP_DETECTED: "Sequence gap detected — events may have been missed.",
            SequenceStatus.DUPLICATE: "Duplicate sequence number — event already seen.",
            SequenceStatus.OUT_OF_ORDER: "Event arrived out of sequence order.",
            SequenceStatus.RESET: "Sequence counter was reset (e.g., reconnect).",
            SequenceStatus.UNKNOWN: "No sequence number provided — cannot assess order.",
        }
        return explanations.get(status, f"Unknown sequence status: {status}")

    def explain_quality(self, status: DataQualityStatus) -> str:
        explanations = {
            DataQualityStatus.PASS: "Data quality checks passed. Event is suitable for use.",
            DataQualityStatus.WARN: "Data quality warning — review before using for formal analysis.",
            DataQualityStatus.FAIL: "Data quality failure — event should not be used for analysis.",
            DataQualityStatus.BLOCKED: "Event blocked — duplicate or bid>ask violation detected.",
        }
        return explanations.get(status, f"Unknown quality status: {status}")

    def explain_failover(self, policy: FailoverPolicy, blocked: bool = False) -> str:
        if blocked:
            return (
                "Failover BLOCKED. LIVE→FIXTURE and LIVE→OFFLINE failovers are "
                "permanently disabled (LIVE_TO_FIXTURE_FAILOVER_DISABLED=True)."
            )
        explanations = {
            FailoverPolicy.NO_FAILOVER: "No failover configured. Session will halt on failure.",
            FailoverPolicy.PAUSE_ON_FAILURE: "Session will pause on failure and wait for operator action.",
            FailoverPolicy.HALT_ON_FAILURE: "Session will halt on failure. Manual restart required.",
        }
        return explanations.get(policy, f"Unknown failover policy: {policy}")

    def explain_reconnect(self, policy: ReconnectPolicy) -> str:
        explanations = {
            ReconnectPolicy.NO_RECONNECT: "No automatic reconnect. Session stays disconnected.",
            ReconnectPolicy.FIXED_INTERVAL: "Reconnect at fixed intervals. No exponential backoff.",
            ReconnectPolicy.BOUNDED_EXPONENTIAL_BACKOFF: (
                "Reconnect with exponential backoff (bounded). "
                "Intervals grow until max_interval is reached."
            ),
        }
        return explanations.get(policy, f"Unknown reconnect policy: {policy}")

    def explain_source_class(self, source_class: SourceClass) -> str:
        explanations = {
            SourceClass.LIVE_PUBLIC: "Live public data from TWSE/TPEX/MOPS providers. Freshness applies.",
            SourceClass.REPLAY: "Historical replay. PIT-enforced. Freshness=NOT_APPLICABLE.",
            SourceClass.FIXTURE: "Static test fixture. Cannot substitute for LIVE data.",
            SourceClass.OFFLINE: "Cached/stored data. Cannot substitute for LIVE data.",
            SourceClass.SIMULATION: "Simulated data for paper trading. Research only.",
            SourceClass.UNKNOWN: "UNKNOWN source — not trusted. Registration required.",
        }
        return explanations.get(source_class, f"Unknown source class: {source_class}")

    def explain_event(self, event_dict: Dict[str, Any]) -> str:
        """Generate a one-line explanation for a canonical event dict."""
        src = event_dict.get("source_class", "?")
        sym = event_dict.get("symbol", "?")
        ts = event_dict.get("timestamp_utc", "?")
        fresh = event_dict.get("freshness_status", "?")
        quality = event_dict.get("quality_status", "?")
        return (
            f"Event: symbol={sym}, source={src}, ts={ts}, "
            f"freshness={fresh}, quality={quality} | "
            "[RESEARCH_ONLY][NO_REAL_ORDER][MARKET_DATA_ONLY]"
        )
