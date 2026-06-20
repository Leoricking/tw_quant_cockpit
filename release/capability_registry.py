"""
release/capability_registry.py — Central capability registry for TW Quant Cockpit v1.3.9.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import json
from typing import Any

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
AVAILABLE   = "AVAILABLE"
STABLE      = "STABLE"
EXPERIMENTAL = "EXPERIMENTAL"
PLANNED     = "PLANNED"
DISABLED    = "DISABLED"
BLOCKED     = "BLOCKED"
DEPRECATED  = "DEPRECATED"

# ---------------------------------------------------------------------------
# Capability definitions
# ---------------------------------------------------------------------------
_CAPABILITIES: list[dict[str, Any]] = [
    {
        "id": "real_data_quality",
        "display_name": "Real Data Quality Foundation",
        "feature_version": "v1.3.0",
        "introduced_in": "1.3.0",
        "canonical_version": "1.3.0",
        "status": STABLE,
        "available": True,
        "stable": True,
        "research_only": True,
        "requires_real_data": True,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": [],
        "health_check": "real_data_quality.health",
        "metadata": {"track": "real_data_quality"},
    },
    {
        "id": "universe_expansion",
        "display_name": "Universe Expansion Foundation",
        "feature_version": "v1.3.1",
        "introduced_in": "1.3.1",
        "canonical_version": "1.3.1",
        "status": STABLE,
        "available": True,
        "stable": True,
        "research_only": True,
        "requires_real_data": True,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["real_data_quality"],
        "health_check": "universe.health",
        "metadata": {"track": "real_data_quality"},
    },
    {
        "id": "provider_adapter_foundation",
        "display_name": "Real Data Provider Adapter Foundation",
        "feature_version": "v1.3.2",
        "introduced_in": "1.3.2",
        "canonical_version": "1.3.2",
        "status": STABLE,
        "available": True,
        "stable": True,
        "research_only": True,
        "requires_real_data": False,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["real_data_quality", "universe_expansion"],
        "health_check": "real_data_provider.health",
        "metadata": {"track": "real_data_quality"},
    },
    {
        "id": "coverage_repair",
        "display_name": "Coverage Repair Workflow",
        "feature_version": "v1.3.3",
        "introduced_in": "1.3.3",
        "canonical_version": "1.3.3",
        "status": STABLE,
        "available": True,
        "stable": True,
        "research_only": True,
        "requires_real_data": False,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["real_data_quality", "universe_expansion"],
        "health_check": "coverage_repair.health",
        "metadata": {"track": "real_data_quality"},
    },
    {
        "id": "data_freshness",
        "display_name": "Data Freshness Monitor",
        "feature_version": "v1.3.4",
        "introduced_in": "1.3.4",
        "canonical_version": "1.3.4",
        "status": STABLE,
        "available": True,
        "stable": True,
        "research_only": True,
        "requires_real_data": False,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["real_data_quality", "provider_adapter_foundation"],
        "health_check": "data_freshness.health",
        "metadata": {"track": "real_data_quality"},
    },
    {
        "id": "empirical_backtest",
        "display_name": "Strategy Knowledge Empirical Backtest",
        "feature_version": "v1.3.5",
        "introduced_in": "1.3.5",
        "canonical_version": "1.3.5",
        "status": STABLE,
        "available": True,
        "stable": True,
        "research_only": True,
        "requires_real_data": True,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["real_data_quality", "data_freshness", "coverage_repair"],
        "health_check": "empirical_backtest.health_v140",
        "metadata": {"internal_label": "1.4.0", "canonical_label": "1.3.5"},
    },
    {
        "id": "abc_validation",
        "display_name": "A/B/C Buy Point Validation",
        "feature_version": "v1.3.6",
        "introduced_in": "1.3.6",
        "canonical_version": "1.3.6",
        "status": STABLE,
        "available": True,
        "stable": True,
        "research_only": True,
        "requires_real_data": True,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["empirical_backtest"],
        "health_check": "abc_validation.health_v141",
        "metadata": {"internal_label": "1.4.1", "canonical_label": "1.3.6"},
    },
    {
        "id": "strategy_robustness",
        "display_name": "Strategy Robustness & Regime Validation",
        "feature_version": "v1.3.7",
        "introduced_in": "1.3.7",
        "canonical_version": "1.3.7",
        "status": STABLE,
        "available": True,
        "stable": True,
        "research_only": True,
        "requires_real_data": True,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["abc_validation"],
        "health_check": "strategy_robustness.health_v142",
        "metadata": {"internal_label": "1.4.2", "canonical_label": "1.3.7"},
    },
    {
        "id": "canonical_version_alignment",
        "display_name": "Canonical Version Alignment",
        "feature_version": "v1.3.7",
        "introduced_in": "1.3.7",
        "canonical_version": "1.3.7",
        "status": STABLE,
        "available": True,
        "stable": True,
        "research_only": True,
        "requires_real_data": False,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": [],
        "health_check": "release.version_alignment",
        "metadata": {},
    },
    # v1.4.x Public Data Provider Integration
    {
        "id": "twse_provider",
        "display_name": "TWSE Provider",
        "feature_version": "v1.4.0",
        "introduced_in": "1.4.0",
        "canonical_version": "1.4.0",
        "status": STABLE,
        "available": True,
        "stable": True,
        "research_only": True,
        "requires_real_data": True,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["provider_adapter_foundation"],
        "health_check": "data.providers.twse.health_v140",
        "metadata": {"roadmap_phase": "v1.4.x Public Data Provider Integration"},
    },
    {
        "id": "tpex_provider",
        "display_name": "TPEx Provider",
        "feature_version": "v1.4.1",
        "introduced_in": "1.4.1",
        "canonical_version": "1.4.1",
        "status": STABLE,
        "available": True,
        "stable": True,
        "research_only": True,
        "requires_real_data": True,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["provider_adapter_foundation", "twse_provider"],
        "health_check": "data.providers.tpex.health_v141",
        "metadata": {"roadmap_phase": "v1.4.x Public Data Provider Integration"},
    },
    {
        "id": "mops_provider",
        "display_name": "MOPS Provider",
        "feature_version": "v1.4.2",
        "introduced_in": "1.4.2",
        "canonical_version": "1.4.2",
        "status": STABLE,
        "available": True,
        "stable": True,
        "research_only": True,
        "requires_real_data": True,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["twse_provider", "tpex_provider"],
        "health_check": "data.providers.mops.health_v142",
        "metadata": {"roadmap_phase": "v1.4.x Public Data Provider Integration"},
    },
    {
        "id": "data_gov_tw_provider",
        "display_name": "data.gov.tw Provider",
        "feature_version": "v1.4.3",
        "introduced_in": "1.4.3",
        "canonical_version": "1.4.3",
        "status": PLANNED,
        "available": False,
        "stable": False,
        "research_only": True,
        "requires_real_data": True,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["twse_provider"],
        "health_check": None,
        "metadata": {"roadmap_phase": "v1.4.x Public Data Provider Integration"},
    },
    {
        "id": "finmind_adapter_hardening",
        "display_name": "FinMind Adapter Hardening",
        "feature_version": "v1.4.4",
        "introduced_in": "1.4.4",
        "canonical_version": "1.4.4",
        "status": PLANNED,
        "available": False,
        "stable": False,
        "research_only": True,
        "requires_real_data": True,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["provider_adapter_foundation"],
        "health_check": None,
        "metadata": {"roadmap_phase": "v1.4.x Public Data Provider Integration"},
    },
    {
        "id": "provider_lineage_rate_limit",
        "display_name": "Source Lineage & Rate Limit",
        "feature_version": "v1.4.5",
        "introduced_in": "1.4.5",
        "canonical_version": "1.4.5",
        "status": PLANNED,
        "available": False,
        "stable": False,
        "research_only": True,
        "requires_real_data": False,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["provider_adapter_foundation"],
        "health_check": None,
        "metadata": {"roadmap_phase": "v1.4.x Public Data Provider Integration"},
    },
    {
        "id": "provider_quality_gates",
        "display_name": "Provider Quality Gates",
        "feature_version": "v1.4.6",
        "introduced_in": "1.4.6",
        "canonical_version": "1.4.6",
        "status": PLANNED,
        "available": False,
        "stable": False,
        "research_only": True,
        "requires_real_data": False,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["real_data_quality", "provider_adapter_foundation"],
        "health_check": None,
        "metadata": {"roadmap_phase": "v1.4.x Public Data Provider Integration"},
    },
    {
        "id": "forum_intelligence",
        "display_name": "Forum Intelligence & Market Sentiment",
        "feature_version": "v1.4.7",
        "introduced_in": "1.4.7",
        "canonical_version": "1.4.7",
        "status": PLANNED,
        "available": False,
        "stable": False,
        "research_only": True,
        "requires_real_data": False,
        "allows_mock_formal_conclusion": False,
        "allows_auto_trading": False,
        "dependencies": ["provider_adapter_foundation"],
        "health_check": None,
        "metadata": {"roadmap_phase": "v1.4.x Public Data Provider Integration"},
    },
]

# Build index
_CAP_INDEX: dict[str, dict] = {cap["id"]: cap for cap in _CAPABILITIES}


def get_capabilities() -> list[dict]:
    """Return all capability definitions (shallow copies)."""
    return [dict(cap) for cap in _CAPABILITIES]


def is_capability_available(name: str) -> bool:
    """Return True if the capability is available (not just planned/disabled)."""
    cap = _CAP_INDEX.get(name)
    if cap is None:
        return False
    return cap.get("available", False) is True


def list_available_capabilities() -> list[str]:
    """Return ids of all currently available capabilities."""
    return [cap["id"] for cap in _CAPABILITIES if cap.get("available", False)]


def list_planned_capabilities() -> list[str]:
    """Return ids of all planned (not yet implemented) capabilities."""
    return [cap["id"] for cap in _CAPABILITIES if cap.get("status") == PLANNED]


def validate_capability_dependencies() -> dict:
    """
    Validate that all declared dependencies exist and are not circular.
    Returns {"valid": bool, "errors": list[str], "warnings": list[str]}.
    """
    errors: list[str] = []
    warnings: list[str] = []
    known_ids = set(_CAP_INDEX.keys())

    for cap in _CAPABILITIES:
        for dep in cap.get("dependencies", []):
            if dep not in known_ids:
                errors.append(f"{cap['id']}: unknown dependency {dep!r}")

    # Simple cycle detection via DFS
    def _has_cycle(node: str, visited: set, stack: set) -> bool:
        visited.add(node)
        stack.add(node)
        for dep in _CAP_INDEX.get(node, {}).get("dependencies", []):
            if dep not in visited:
                if _has_cycle(dep, visited, stack):
                    return True
            elif dep in stack:
                return True
        stack.discard(node)
        return False

    visited: set = set()
    for cap_id in known_ids:
        if cap_id not in visited:
            if _has_cycle(cap_id, set(), set()):
                errors.append(f"Dependency cycle detected involving {cap_id!r}")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def build_capability_summary() -> dict:
    """Return a JSON-safe summary of all capabilities."""
    available = list_available_capabilities()
    planned = list_planned_capabilities()
    stable = [cap["id"] for cap in _CAPABILITIES if cap.get("stable", False)]
    dep_validation = validate_capability_dependencies()

    return {
        "total": len(_CAPABILITIES),
        "available_count": len(available),
        "planned_count": len(planned),
        "stable_count": len(stable),
        "available": available,
        "planned": planned,
        "stable": stable,
        "dependency_validation": dep_validation,
    }
