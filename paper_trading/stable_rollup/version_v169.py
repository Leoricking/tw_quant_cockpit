"""
paper_trading/stable_rollup/version_v169.py
Version identity module for Live Paper Trading Stable Rollup v1.6.9.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER.
"""
from __future__ import annotations

VERSION = "1.6.9"
RELEASE_NAME = "Live Paper Trading Stable Rollup"
BASE_RELEASE = "1.6.8 Operational Integration Hardening"
SCHEMA_VERSION = "169"
POLICY_VERSION = "1.6.9-live-paper-stable-rollup"

COMPONENT_COUNT = 32
MIN_SCENARIOS = 80
MIN_FIXTURES = 80
MIN_CLI = 26
MIN_HEALTH = 80
MIN_GATE = 70

ACCEPTED_MINIMUM_VERSION = "1.6.8"

KNOWN_RELEASE_NAMES: frozenset = frozenset({
    "Live Paper Trading Stable Rollup",
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
    "Warning Clean Hotfix",
    "Stable Rollup Compatibility Hotfix",
    "Small Capital Growth Strategy Template",
})


def get_version_info() -> dict:
    """Return version identity dictionary."""
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
        "accepted_minimum_version": ACCEPTED_MINIMUM_VERSION,
        "known_release_names": sorted(KNOWN_RELEASE_NAMES),
        "paper_only": True,
        "research_only": True,
        "read_only": True,
        "no_real_orders": True,
        "not_for_production": True,
    }


def is_known_release(name: str) -> bool:
    """Return True if the given release name is known."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(version_str: str) -> bool:
    """
    Return True if version_str meets or exceeds ACCEPTED_MINIMUM_VERSION.
    Uses tuple comparison on dot-separated integers.
    """
    def _to_tuple(v: str):
        parts = []
        for p in v.split("."):
            try:
                parts.append(int(p))
            except ValueError:
                parts.append(0)
        return tuple(parts)

    try:
        current = _to_tuple(version_str)
        minimum = _to_tuple(ACCEPTED_MINIMUM_VERSION)
        return current >= minimum
    except Exception:
        return False
