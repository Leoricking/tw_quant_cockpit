"""
paper_trading/operational_integration/version_v168.py
Version identity for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION         = "1.6.8"
RELEASE_NAME    = "Operational Integration Hardening"
BASE_RELEASE    = "1.6.7 Paper Performance Attribution"
SCHEMA_VERSION  = "168"
POLICY_VERSION  = "1.6.8-operational-integration"

COMPONENT_COUNT = 43
MIN_SCENARIOS   = 100
MIN_FIXTURES    = 100
MIN_CLI         = 31
MIN_HEALTH      = 70
MIN_GATE        = 60

KNOWN_RELEASE_NAMES = frozenset({
    "Operational Integration Hardening",
    "Paper Performance Attribution",
    "Replay Session Lineage Handler Integrity Hotfix",
    "Fixture Governance & Safety Marker Hotfix",
    "Multi-session Coordination",
    "Failure Injection and Recovery Validation",
    "Operational Analytics and Review",
    "Session Operations Observability",
    "Paper Strategy Orchestration",
    "Market Data Session Adapter",
    "Live Paper Trading Foundation",
    "Portfolio Stable Rollup",
    "Portfolio Walk-Forward Validation",
    "Drawdown Risk Controls",
    "Correlation Exposure Manager",
    "Position Sizing Foundation",
    "Portfolio Research Foundation",
    "Provider Stable Rollup",
})

ACCEPTED_MINIMUM_VERSION = "1.6.7"


def get_version_info() -> dict:
    """Return version identity dict. Deterministic."""
    return {
        "version": VERSION,
        "release_name": RELEASE_NAME,
        "base_release": BASE_RELEASE,
        "schema_version": SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
        "component_count": COMPONENT_COUNT,
        "min_scenarios": MIN_SCENARIOS,
        "min_fixtures": MIN_FIXTURES,
        "min_cli": MIN_CLI,
        "min_health": MIN_HEALTH,
        "min_gate": MIN_GATE,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_for_production": True,
    }


def is_known_release(name: str) -> bool:
    """Return True if name is a known release name."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(version_str: str) -> bool:
    """Return True if version_str >= ACCEPTED_MINIMUM_VERSION (tuple comparison)."""
    def _parse(v: str):
        parts = []
        for p in v.split("."):
            try:
                parts.append(int(p))
            except ValueError:
                parts.append(0)
        return tuple(parts)

    return _parse(version_str) >= _parse(ACCEPTED_MINIMUM_VERSION)
