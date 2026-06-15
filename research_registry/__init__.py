"""
research_registry — Research Run Registry v1.1.8

Append-only registry for all research command runs. Tracks run metadata,
qualification, lineage, artifacts, duplicate detection, and reproducibility.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Registry does NOT execute research commands. No Auto Rerun. No Auto Execution.
[!] Run Auto Rerun DISABLED. Broker DISABLED. Trading DISABLED.
"""
from __future__ import annotations

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True
REGISTRY_AUTO_RERUN_ENABLED = False
REGISTRY_AUTO_EXECUTION_ENABLED = False
REGISTRY_TRADE_EXECUTION_ENABLED = False

from research_registry.registry_schema import (
    ResearchRunRecord,
    RunArtifact,
    RunLineage,
    RunComparison,
    RegistrySummary,
)
from research_registry.registry_engine import ResearchRunRegistryEngine
from research_registry.registry_health import ResearchRunRegistryHealthCheck
from research_registry.registry_query import RegistryQuery

__all__ = [
    "ResearchRunRecord",
    "RunArtifact",
    "RunLineage",
    "RunComparison",
    "RegistrySummary",
    "ResearchRunRegistryEngine",
    "ResearchRunRegistryHealthCheck",
    "RegistryQuery",
    "NO_REAL_ORDERS",
    "BROKER_DISABLED",
    "RESEARCH_ONLY",
    "REGISTRY_AUTO_RERUN_ENABLED",
    "REGISTRY_AUTO_EXECUTION_ENABLED",
    "REGISTRY_TRADE_EXECUTION_ENABLED",
]
