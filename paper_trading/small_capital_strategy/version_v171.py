"""
paper_trading/small_capital_strategy/version_v171.py
Version identity for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION         = "1.7.1"
RELEASE_NAME    = "Watchlist Strategy Layer"
BASE_RELEASE    = "1.7.0 Small Capital Growth Strategy Template"
SCHEMA_VERSION  = "171"
POLICY_VERSION  = "1.7.1-watchlist-strategy-layer"

COMPONENT_COUNT = 25
MIN_SCENARIOS   = 70
MIN_FIXTURES    = 70
MIN_CLI         = 22
MIN_HEALTH      = 70
MIN_GATE        = 65

ACCEPTED_MINIMUM_VERSION = "1.7.0"

KNOWN_RELEASE_NAMES: frozenset = frozenset({
    "Watchlist Strategy Layer",
    "Small Capital Growth Strategy Template",
    "Stable Rollup Compatibility Hotfix",
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
})


def get_version_info() -> dict:
    """Return version identity dictionary. Deterministic."""
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
        "not_investment_advice": True,
    }


def verify_version() -> dict:
    """Return version identity dict. Deterministic."""
    return get_version_info()


def is_known_release(name: str) -> bool:
    """Return True if name is a known release name."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(version_str: str) -> bool:
    """Return True if version_str meets or exceeds ACCEPTED_MINIMUM_VERSION."""
    def _to_tuple(v: str):
        parts = []
        for p in v.split("."):
            try:
                parts.append(int(p))
            except ValueError:
                parts.append(0)
        return tuple(parts)

    try:
        return _to_tuple(version_str) >= _to_tuple(ACCEPTED_MINIMUM_VERSION)
    except Exception:
        return False
