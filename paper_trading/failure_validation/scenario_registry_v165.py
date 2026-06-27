"""
paper_trading/failure_validation/scenario_registry_v165.py — Built-in scenario registry v1.6.5.
[!] Research Only. No Real Orders. No Real Failure Injection. Not Investment Advice.
[!] ≥60 built-in scenario definitions. All paper/simulation only.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from paper_trading.failure_validation.enums_v165 import (
    ExpectedOutcome,
    FailureDomain,
    FailureSeverity,
    FailureType,
)
from paper_trading.failure_validation.models_v165 import FailureScenario

REAL_FAILURE_INJECTION_ENABLED = False
PAPER_ONLY = True
RESEARCH_ONLY = True


def _s(name: str, description: str, domain: FailureDomain, failure_type: FailureType,
        severity: FailureSeverity, expected_outcomes: List[ExpectedOutcome],
        seed: int = 42, max_duration_ms: int = 5000, tags: Optional[List[str]] = None,
        cascading_targets: Optional[List[str]] = None,
        parameters: Optional[Dict] = None) -> FailureScenario:
    return FailureScenario(
        name=name,
        description=description,
        domain=domain,
        failure_type=failure_type,
        severity=severity,
        expected_outcomes=expected_outcomes,
        seed=seed,
        max_duration_ms=max_duration_ms,
        tags=tags or [],
        cascading_targets=cascading_targets or [],
        parameters=parameters or {},
        reversible=True,
        bounded=True,
        fixture_only=True,
        research_only=True,
        paper_only=True,
        no_broker=True,
        no_real_account=True,
        no_real_order=True,
        not_for_production=True,
        not_live=True,
        failure_injection_only=True,
        demo_only=True,
    )


# ---------------------------------------------------------------------------
# Built-in scenario registry — ≥60 scenarios
# ---------------------------------------------------------------------------

BUILTIN_SCENARIOS: List[FailureScenario] = [
    # ---- Market Data (10 scenarios) ----
    _s("md_timeout_001", "Market data feed timeout",
       FailureDomain.MARKET_DATA, FailureType.TIMEOUT, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED], seed=1001,
       tags=["market_data", "timeout"]),

    _s("md_stale_001", "Market data stale (>30s old)",
       FailureDomain.MARKET_DATA, FailureType.STALE_DATA, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.DEGRADED], seed=1002,
       tags=["market_data", "stale"]),

    _s("md_missing_001", "Market data missing (all prices null)",
       FailureDomain.MARKET_DATA, FailureType.MISSING_DATA, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.HALTED], seed=1003,
       tags=["market_data", "missing"]),

    _s("md_invalid_payload_001", "Market data invalid payload (malformed JSON)",
       FailureDomain.MARKET_DATA, FailureType.INVALID_PAYLOAD, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.BLOCKED], seed=1004,
       tags=["market_data", "invalid_payload"]),

    _s("md_delay_001", "Market data delayed (500ms latency injection)",
       FailureDomain.MARKET_DATA, FailureType.DELAY, FailureSeverity.LOW,
       [ExpectedOutcome.DETECTED], seed=1005,
       tags=["market_data", "delay"], parameters={"delay_ms": 500}),

    _s("md_duplicate_event_001", "Market data duplicate tick event",
       FailureDomain.MARKET_DATA, FailureType.DUPLICATE_EVENT, FailureSeverity.LOW,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED], seed=1006,
       tags=["market_data", "duplicate"]),

    _s("md_out_of_order_001", "Market data out-of-order ticks",
       FailureDomain.MARKET_DATA, FailureType.OUT_OF_ORDER_EVENT, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.DEGRADED], seed=1007,
       tags=["market_data", "ordering"]),

    _s("md_clock_skew_001", "Market data clock skew (timestamps +5min)",
       FailureDomain.MARKET_DATA, FailureType.CLOCK_SKEW, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED], seed=1008,
       tags=["market_data", "clock_skew"], parameters={"skew_ms": 300000}),

    _s("md_partial_write_001", "Market data partial write to store",
       FailureDomain.MARKET_DATA, FailureType.PARTIAL_WRITE, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED], seed=1009,
       tags=["market_data", "partial_write"]),

    _s("md_read_failure_001", "Market data read failure from store",
       FailureDomain.MARKET_DATA, FailureType.READ_FAILURE, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.HALTED], seed=1010,
       tags=["market_data", "read_failure"]),

    # ---- Session State (5 scenarios) ----
    _s("ss_state_divergence_001", "Session state divergence (two nodes)",
       FailureDomain.SESSION_STATE, FailureType.STATE_DIVERGENCE, FailureSeverity.CRITICAL,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED, ExpectedOutcome.HALTED], seed=2001,
       tags=["session_state", "divergence"]),

    _s("ss_write_failure_001", "Session state write failure",
       FailureDomain.SESSION_STATE, FailureType.WRITE_FAILURE, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED], seed=2002,
       tags=["session_state", "write_failure"]),

    _s("ss_config_drift_001", "Session config drift (params changed externally)",
       FailureDomain.SESSION_STATE, FailureType.CONFIG_DRIFT, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED], seed=2003,
       tags=["session_state", "config_drift"]),

    _s("ss_timeout_001", "Session state persistence timeout",
       FailureDomain.SESSION_STATE, FailureType.TIMEOUT, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.DEGRADED], seed=2004,
       tags=["session_state", "timeout"]),

    _s("ss_degraded_mode_001", "Session forced into degraded mode",
       FailureDomain.SESSION_STATE, FailureType.DEGRADED_MODE, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DEGRADED, ExpectedOutcome.ALERTED], seed=2005,
       tags=["session_state", "degraded"]),

    # ---- Strategy Signal (5 scenarios) ----
    _s("sig_missing_001", "Strategy signal missing (no signal generated)",
       FailureDomain.STRATEGY_SIGNAL, FailureType.MISSING_DATA, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.BLOCKED], seed=3001,
       tags=["strategy_signal", "missing"]),

    _s("sig_stale_001", "Strategy signal stale (5min old)",
       FailureDomain.STRATEGY_SIGNAL, FailureType.STALE_DATA, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.BLOCKED], seed=3002,
       tags=["strategy_signal", "stale"]),

    _s("sig_invalid_payload_001", "Strategy signal invalid payload",
       FailureDomain.STRATEGY_SIGNAL, FailureType.INVALID_PAYLOAD, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.BLOCKED], seed=3003,
       tags=["strategy_signal", "invalid"]),

    _s("sig_duplicate_001", "Strategy signal duplicate emission",
       FailureDomain.STRATEGY_SIGNAL, FailureType.DUPLICATE_EVENT, FailureSeverity.LOW,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED], seed=3004,
       tags=["strategy_signal", "duplicate"]),

    _s("sig_delay_001", "Strategy signal generation delay",
       FailureDomain.STRATEGY_SIGNAL, FailureType.DELAY, FailureSeverity.LOW,
       [ExpectedOutcome.DETECTED], seed=3005,
       tags=["strategy_signal", "delay"]),

    # ---- Paper Order (5 scenarios) ----
    _s("po_write_failure_001", "Paper order write failure",
       FailureDomain.PAPER_ORDER, FailureType.WRITE_FAILURE, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED], seed=4001,
       tags=["paper_order", "write_failure"]),

    _s("po_duplicate_001", "Paper order duplicate submission",
       FailureDomain.PAPER_ORDER, FailureType.DUPLICATE_EVENT, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.BLOCKED], seed=4002,
       tags=["paper_order", "duplicate"]),

    _s("po_invalid_payload_001", "Paper order invalid payload",
       FailureDomain.PAPER_ORDER, FailureType.INVALID_PAYLOAD, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.BLOCKED], seed=4003,
       tags=["paper_order", "invalid"]),

    _s("po_timeout_001", "Paper order submission timeout",
       FailureDomain.PAPER_ORDER, FailureType.TIMEOUT, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED], seed=4004,
       tags=["paper_order", "timeout"]),

    _s("po_retry_exhaustion_001", "Paper order retry exhaustion",
       FailureDomain.PAPER_ORDER, FailureType.RETRY_EXHAUSTION, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED, ExpectedOutcome.CONTAINED], seed=4005,
       tags=["paper_order", "retry"]),

    # ---- Paper Fill (4 scenarios) ----
    _s("pf_missing_001", "Paper fill missing (order never filled)",
       FailureDomain.PAPER_FILL, FailureType.MISSING_DATA, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED], seed=5001,
       tags=["paper_fill", "missing"]),

    _s("pf_duplicate_001", "Paper fill duplicate event",
       FailureDomain.PAPER_FILL, FailureType.DUPLICATE_EVENT, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED], seed=5002,
       tags=["paper_fill", "duplicate"]),

    _s("pf_partial_write_001", "Paper fill partial write",
       FailureDomain.PAPER_FILL, FailureType.PARTIAL_WRITE, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED], seed=5003,
       tags=["paper_fill", "partial_write"]),

    _s("pf_invalid_payload_001", "Paper fill invalid payload",
       FailureDomain.PAPER_FILL, FailureType.INVALID_PAYLOAD, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.BLOCKED], seed=5004,
       tags=["paper_fill", "invalid"]),

    # ---- Event Stream (5 scenarios) ----
    _s("es_event_loss_001", "Event stream event loss",
       FailureDomain.EVENT_STREAM, FailureType.EVENT_LOSS, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED], seed=6001,
       tags=["event_stream", "loss"]),

    _s("es_event_storm_001", "Event stream storm (10x normal volume)",
       FailureDomain.EVENT_STREAM, FailureType.EVENT_STORM, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.DEGRADED, ExpectedOutcome.CONTAINED], seed=6002,
       tags=["event_stream", "storm"]),

    _s("es_out_of_order_001", "Event stream out-of-order delivery",
       FailureDomain.EVENT_STREAM, FailureType.OUT_OF_ORDER_EVENT, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.DEGRADED], seed=6003,
       tags=["event_stream", "ordering"]),

    _s("es_duplicate_001", "Event stream duplicate delivery",
       FailureDomain.EVENT_STREAM, FailureType.DUPLICATE_EVENT, FailureSeverity.LOW,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED], seed=6004,
       tags=["event_stream", "duplicate"]),

    _s("es_circuit_open_001", "Event stream circuit breaker open",
       FailureDomain.EVENT_STREAM, FailureType.CIRCUIT_OPEN, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED, ExpectedOutcome.CONTAINED], seed=6005,
       tags=["event_stream", "circuit_breaker"]),

    # ---- Checkpoint (5 scenarios) ----
    _s("cp_corruption_001", "Checkpoint corruption (hash mismatch)",
       FailureDomain.CHECKPOINT, FailureType.CHECKPOINT_CORRUPTION, FailureSeverity.CRITICAL,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED, ExpectedOutcome.HALTED], seed=7001,
       tags=["checkpoint", "corruption"]),

    _s("cp_hash_mismatch_001", "Checkpoint hash mismatch after write",
       FailureDomain.CHECKPOINT, FailureType.HASH_MISMATCH, FailureSeverity.CRITICAL,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED], seed=7002,
       tags=["checkpoint", "hash_mismatch"]),

    _s("cp_snapshot_mismatch_001", "Checkpoint snapshot mismatch",
       FailureDomain.CHECKPOINT, FailureType.SNAPSHOT_MISMATCH, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED], seed=7003,
       tags=["checkpoint", "snapshot"]),

    _s("cp_write_failure_001", "Checkpoint write failure",
       FailureDomain.CHECKPOINT, FailureType.WRITE_FAILURE, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED], seed=7004,
       tags=["checkpoint", "write_failure"]),

    _s("cp_read_failure_001", "Checkpoint read failure",
       FailureDomain.CHECKPOINT, FailureType.READ_FAILURE, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.HALTED], seed=7005,
       tags=["checkpoint", "read_failure"]),

    # ---- Recovery (5 scenarios) ----
    _s("rec_failure_001", "Recovery failure (recovery plan fails)",
       FailureDomain.RECOVERY, FailureType.RECOVERY_FAILURE, FailureSeverity.CRITICAL,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED, ExpectedOutcome.ROLLED_BACK], seed=8001,
       tags=["recovery", "failure"]),

    _s("rec_rollback_failure_001", "Rollback failure during recovery",
       FailureDomain.RECOVERY, FailureType.ROLLBACK_FAILURE, FailureSeverity.CRITICAL,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED, ExpectedOutcome.HALTED], seed=8002,
       tags=["recovery", "rollback"]),

    _s("rec_retry_exhaustion_001", "Recovery retry exhaustion",
       FailureDomain.RECOVERY, FailureType.RETRY_EXHAUSTION, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED, ExpectedOutcome.CONTAINED], seed=8003,
       tags=["recovery", "retry"]),

    _s("rec_replay_mismatch_001", "Replay mismatch during recovery",
       FailureDomain.RECOVERY, FailureType.REPLAY_MISMATCH, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED], seed=8004,
       tags=["recovery", "replay"]),

    _s("rec_circuit_open_001", "Recovery circuit breaker open",
       FailureDomain.RECOVERY, FailureType.CIRCUIT_OPEN, FailureSeverity.HIGH,
       [ExpectedOutcome.CONTAINED], seed=8005,
       tags=["recovery", "circuit_breaker"]),

    # ---- Alert (4 scenarios) ----
    _s("al_loss_001", "Alert loss (alert not generated)",
       FailureDomain.ALERT, FailureType.ALERT_LOSS, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED], seed=9001,
       tags=["alert", "loss"]),

    _s("al_duplication_001", "Alert duplication (same alert fires twice)",
       FailureDomain.ALERT, FailureType.ALERT_DUPLICATION, FailureSeverity.LOW,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED], seed=9002,
       tags=["alert", "duplicate"]),

    _s("al_incident_creation_failure_001", "Alert incident creation failure",
       FailureDomain.ALERT, FailureType.INCIDENT_CREATION_FAILURE, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED], seed=9003,
       tags=["alert", "incident"]),

    _s("al_timeout_001", "Alert delivery timeout",
       FailureDomain.ALERT, FailureType.TIMEOUT, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED], seed=9004,
       tags=["alert", "timeout"]),

    # ---- Dependency (4 scenarios) ----
    _s("dep_unavailable_001", "Dependency unavailable",
       FailureDomain.DEPENDENCY, FailureType.DEPENDENCY_UNAVAILABLE, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.DEGRADED, ExpectedOutcome.CONTAINED], seed=10001,
       tags=["dependency", "unavailable"]),

    _s("dep_circuit_open_001", "Dependency circuit breaker open",
       FailureDomain.DEPENDENCY, FailureType.CIRCUIT_OPEN, FailureSeverity.HIGH,
       [ExpectedOutcome.CONTAINED], seed=10002,
       tags=["dependency", "circuit_breaker"]),

    _s("dep_retry_exhaustion_001", "Dependency retry exhaustion",
       FailureDomain.DEPENDENCY, FailureType.RETRY_EXHAUSTION, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED, ExpectedOutcome.CONTAINED], seed=10003,
       tags=["dependency", "retry"]),

    _s("dep_degraded_mode_001", "Dependency degraded mode",
       FailureDomain.DEPENDENCY, FailureType.DEGRADED_MODE, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DEGRADED], seed=10004,
       tags=["dependency", "degraded"]),

    # ---- Cascading scenarios (6 scenarios) ----
    _s("casc_md_signal_order_001",
       "Cascading: Market Data stale → Signal invalid → Order blocked",
       FailureDomain.MARKET_DATA, FailureType.STALE_DATA, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED, ExpectedOutcome.CONTAINED], seed=20001,
       cascading_targets=["STRATEGY_SIGNAL", "PAPER_ORDER"],
       tags=["cascading", "market_data", "signal", "order"]),

    _s("casc_md_signal_alert_incident_001",
       "Cascading: Market Data stale → Signal invalid → Alert → Incident → Session degraded",
       FailureDomain.MARKET_DATA, FailureType.STALE_DATA, FailureSeverity.CRITICAL,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED, ExpectedOutcome.DEGRADED], seed=20002,
       cascading_targets=["STRATEGY_SIGNAL", "ALERT", "INCIDENT", "SESSION_STATE"],
       tags=["cascading", "full_chain"]),

    _s("casc_cp_recovery_replay_001",
       "Cascading: Checkpoint corruption → Recovery fails → Replay fallback → Hash mismatch → Blocked",
       FailureDomain.CHECKPOINT, FailureType.CHECKPOINT_CORRUPTION, FailureSeverity.CRITICAL,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED, ExpectedOutcome.BLOCKED], seed=20003,
       cascading_targets=["RECOVERY", "RECOVERY", "CHECKPOINT"],
       tags=["cascading", "checkpoint", "recovery", "replay"]),

    _s("casc_event_storm_degraded_001",
       "Cascading: Event storm → Alert loss → Session degraded",
       FailureDomain.EVENT_STREAM, FailureType.EVENT_STORM, FailureSeverity.HIGH,
       [ExpectedOutcome.DEGRADED, ExpectedOutcome.ALERTED], seed=20004,
       cascading_targets=["ALERT", "SESSION_STATE"],
       tags=["cascading", "event_storm"]),

    _s("casc_dep_circuit_halt_001",
       "Cascading: Dependency unavailable → Circuit open → Session halt",
       FailureDomain.DEPENDENCY, FailureType.DEPENDENCY_UNAVAILABLE, FailureSeverity.CRITICAL,
       [ExpectedOutcome.HALTED, ExpectedOutcome.ALERTED], seed=20005,
       cascading_targets=["DEPENDENCY", "SESSION_STATE"],
       tags=["cascading", "dependency", "circuit_breaker"]),

    _s("casc_config_drift_signal_001",
       "Cascading: Config drift → Strategy signal invalid → Paper order blocked",
       FailureDomain.CONFIGURATION, FailureType.CONFIG_DRIFT, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.BLOCKED], seed=20006,
       cascading_targets=["STRATEGY_SIGNAL", "PAPER_ORDER"],
       tags=["cascading", "config_drift"]),

    # ---- Store / Query (4 scenarios) ----
    _s("store_write_failure_001", "Store write failure",
       FailureDomain.STORE, FailureType.WRITE_FAILURE, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.CONTAINED], seed=11001,
       tags=["store", "write_failure"]),

    _s("store_read_failure_001", "Store read failure",
       FailureDomain.STORE, FailureType.READ_FAILURE, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.HALTED], seed=11002,
       tags=["store", "read_failure"]),

    _s("query_timeout_001", "Query timeout",
       FailureDomain.QUERY, FailureType.TIMEOUT, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.DEGRADED], seed=12001,
       tags=["query", "timeout"]),

    _s("query_missing_001", "Query missing results",
       FailureDomain.QUERY, FailureType.MISSING_DATA, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED], seed=12002,
       tags=["query", "missing"]),

    # ---- Analytics / Report (4 scenarios) ----
    _s("analytics_missing_001", "Analytics data missing",
       FailureDomain.ANALYTICS, FailureType.MISSING_DATA, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.DEGRADED], seed=13001,
       tags=["analytics", "missing"]),

    _s("analytics_stale_001", "Analytics stale data",
       FailureDomain.ANALYTICS, FailureType.STALE_DATA, FailureSeverity.LOW,
       [ExpectedOutcome.DETECTED], seed=13002,
       tags=["analytics", "stale"]),

    _s("report_missing_001", "Report generation data missing",
       FailureDomain.REPORT, FailureType.MISSING_DATA, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED], seed=14001,
       tags=["report", "missing"]),

    _s("report_timeout_001", "Report generation timeout",
       FailureDomain.REPORT, FailureType.TIMEOUT, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.DEGRADED], seed=14002,
       tags=["report", "timeout"]),

    # ---- Time / Configuration (4 scenarios) ----
    _s("time_clock_skew_001", "Clock skew (virtual clock divergence)",
       FailureDomain.TIME, FailureType.CLOCK_SKEW, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED], seed=15001,
       tags=["time", "clock_skew"]),

    _s("time_delay_001", "Time domain processing delay",
       FailureDomain.TIME, FailureType.DELAY, FailureSeverity.LOW,
       [ExpectedOutcome.DETECTED], seed=15002,
       tags=["time", "delay"]),

    _s("config_drift_001", "Configuration drift",
       FailureDomain.CONFIGURATION, FailureType.CONFIG_DRIFT, FailureSeverity.MEDIUM,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.ALERTED], seed=16001,
       tags=["configuration", "drift"]),

    _s("config_invalid_payload_001", "Configuration invalid payload",
       FailureDomain.CONFIGURATION, FailureType.INVALID_PAYLOAD, FailureSeverity.HIGH,
       [ExpectedOutcome.DETECTED, ExpectedOutcome.BLOCKED], seed=16002,
       tags=["configuration", "invalid"]),
]

assert len(BUILTIN_SCENARIOS) >= 60, f"Expected ≥60 scenarios, got {len(BUILTIN_SCENARIOS)}"

# Build name-to-scenario index
SCENARIO_BY_NAME: Dict[str, FailureScenario] = {s.name: s for s in BUILTIN_SCENARIOS}


def get_scenario(name: str) -> Optional[FailureScenario]:
    return SCENARIO_BY_NAME.get(name)


def get_scenarios_by_domain(domain: FailureDomain) -> List[FailureScenario]:
    return [s for s in BUILTIN_SCENARIOS if s.domain == domain]


def get_scenarios_by_severity(severity: FailureSeverity) -> List[FailureScenario]:
    return [s for s in BUILTIN_SCENARIOS if s.severity == severity]


def get_cascading_scenarios() -> List[FailureScenario]:
    return [s for s in BUILTIN_SCENARIOS if s.cascading_targets]


def scenario_count() -> int:
    return len(BUILTIN_SCENARIOS)
