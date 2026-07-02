"""
paper_trading/performance_attribution/version_v167.py
Version identity for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION         = "1.6.7"
RELEASE_NAME    = "Paper Performance Attribution"
BASE_RELEASE    = "1.6.6.2 Replay Session Lineage Handler Integrity Hotfix"
SCHEMA_VERSION  = "167"
POLICY_VERSION  = "1.6.7-paper-attribution"

KNOWN_RELEASE_NAMES = frozenset({
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

ACCEPTED_MINIMUM_VERSION = "1.6.6.2"


def verify_version() -> dict:
    """Return version identity dict. Deterministic."""
    return {
        "version": VERSION,
        "release_name": RELEASE_NAME,
        "base_release": BASE_RELEASE,
        "schema_version": SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_for_production": True,
    }


def is_known_release(name: str) -> bool:
    """Return True if name is a known release name."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(version_str: str) -> bool:
    """Return True if version_str >= ACCEPTED_MINIMUM_VERSION (lexicographic on tuple)."""
    def _parse(v: str):
        parts = []
        for p in v.split("."):
            try:
                parts.append(int(p))
            except ValueError:
                parts.append(0)
        return tuple(parts)

    return _parse(version_str) >= _parse(ACCEPTED_MINIMUM_VERSION)
