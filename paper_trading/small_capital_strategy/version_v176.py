"""
paper_trading/small_capital_strategy/version_v176.py
Version metadata for Mistake Taxonomy & Weekly Review Dashboard v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, Any

VERSION      = "1.7.6"
RELEASE_NAME = "Mistake Taxonomy & Weekly Review Dashboard"
BASE_RELEASE = "1.7.5 Small Account Trade Journal"
SCHEMA_VERSION  = "176"
POLICY_VERSION  = "1.7.6-mistake-taxonomy-weekly-review"

COMPONENT_COUNT = 14
MIN_SCENARIOS   = 60
MIN_FIXTURES    = 60
MIN_CLI         = 14
MIN_HEALTH      = 70
MIN_GATE        = 65

KNOWN_RELEASE_NAMES: frozenset = frozenset({
    "Live Paper Trading Stable Rollup",
    "Small Capital Growth Strategy",
    "Watchlist Strategy Layer",
    "A/B/C Buy Point Execution Plan",
    "Market Regime Position Control",
    "Small Account Risk Dashboard",
    "Small Account Trade Journal",
    "Mistake Taxonomy & Weekly Review Dashboard",
})


def get_version_info() -> Dict[str, Any]:
    """Return version metadata dict."""
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
        "not_investment_advice": True,
    }


def verify_version() -> bool:
    """Return True if version string is well-formed."""
    parts = VERSION.split(".")
    return len(parts) == 3 and all(p.isdigit() for p in parts)


def is_known_release(name: str) -> bool:
    """Return True if release name is in the known set."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(version_str: str) -> bool:
    """Return True if version_str >= VERSION."""
    def _parse(v: str):
        return tuple(int(x) for x in v.split("."))
    try:
        return _parse(version_str) >= _parse(VERSION)
    except (ValueError, AttributeError):
        return False
