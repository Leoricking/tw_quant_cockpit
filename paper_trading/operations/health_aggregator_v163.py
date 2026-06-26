"""
Health Aggregator v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from paper_trading.operations.enums_v163 import HealthStatus


@dataclass
class ComponentHealth:
    component:      str
    status:         HealthStatus
    passed:         int       = 0
    failed:         int       = 0
    total:          int       = 0
    reasons:        List[str] = field(default_factory=list)
    warnings:       List[str] = field(default_factory=list)
    blocking:       bool      = False


@dataclass
class AggregatedHealth:
    overall:          HealthStatus
    components:       List[ComponentHealth]   = field(default_factory=list)
    reasons:          List[str]               = field(default_factory=list)
    failed_checks:    List[str]               = field(default_factory=list)
    warnings:         List[str]               = field(default_factory=list)
    blocking_checks:  List[str]               = field(default_factory=list)
    as_of:            Optional[datetime]      = None
    policy_version:   str                     = "1.6.3"


def aggregate_health(components: List[ComponentHealth]) -> AggregatedHealth:
    """
    Rule: BLOCKED > CRITICAL > UNHEALTHY > DEGRADED > WARNING > HEALTHY > UNKNOWN
    Safety status has highest priority.
    Composite health must not be better than any required dependency.
    """
    if not components:
        return AggregatedHealth(
            overall=HealthStatus.UNKNOWN,
            reasons=["No components provided"],
            as_of=datetime.now(timezone.utc),
        )

    worst = HealthStatus.UNKNOWN
    reasons       = []
    failed_checks = []
    warnings_list = []
    blocking      = []

    for comp in components:
        rank_comp = HealthStatus.severity_rank(comp.status)
        rank_worst = HealthStatus.severity_rank(worst)
        if rank_comp > rank_worst:
            worst = comp.status

        if comp.status in (HealthStatus.BLOCKED, HealthStatus.CRITICAL, HealthStatus.UNHEALTHY):
            reasons.extend(comp.reasons)
            if comp.blocking:
                blocking.extend([f"{comp.component}: {r}" for r in comp.reasons])
        if comp.status in (HealthStatus.WARNING,):
            warnings_list.extend(comp.warnings)
        if comp.failed > 0:
            failed_checks.append(f"{comp.component}: {comp.failed} failed")

    return AggregatedHealth(
        overall=worst,
        components=components,
        reasons=reasons,
        failed_checks=failed_checks,
        warnings=warnings_list,
        blocking_checks=blocking,
        as_of=datetime.now(timezone.utc),
    )


class SessionOperationsHealthAggregator:
    """Aggregate health from all session operations sub-components."""

    def run(
        self,
        market_data_health:    Optional[HealthStatus] = None,
        paper_trading_health:  Optional[HealthStatus] = None,
        paper_strategy_health: Optional[HealthStatus] = None,
        metrics_health:        Optional[HealthStatus] = None,
        alert_health:          Optional[HealthStatus] = None,
        incident_health:       Optional[HealthStatus] = None,
        storage_health:        Optional[HealthStatus] = None,
        replay_health:         Optional[HealthStatus] = None,
        recovery_health:       Optional[HealthStatus] = None,
        safety_health:         Optional[HealthStatus] = None,
    ) -> AggregatedHealth:
        components = []
        pairs = [
            ("market_data",    market_data_health),
            ("paper_trading",  paper_trading_health),
            ("paper_strategy", paper_strategy_health),
            ("metrics",        metrics_health),
            ("alerts",         alert_health),
            ("incidents",      incident_health),
            ("storage",        storage_health),
            ("replay",         replay_health),
            ("recovery",       recovery_health),
            ("safety",         safety_health),
        ]
        for name, status in pairs:
            hs = status if status is not None else HealthStatus.UNKNOWN
            comp = ComponentHealth(
                component=name,
                status=hs,
                blocking=(name == "safety" and hs == HealthStatus.BLOCKED),
            )
            if hs in (HealthStatus.BLOCKED, HealthStatus.CRITICAL):
                comp.reasons.append(f"{name}: {hs}")
            components.append(comp)

        return aggregate_health(components)


__all__ = ["ComponentHealth", "AggregatedHealth", "aggregate_health", "SessionOperationsHealthAggregator"]
