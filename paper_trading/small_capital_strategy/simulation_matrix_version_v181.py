"""
paper_trading/small_capital_strategy/simulation_matrix_version_v181.py
Version metadata for Simulation Scenario Matrix & Stress Test Lab v1.8.1.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict

VERSION      = "1.8.1"
RELEASE_NAME = "Simulation Scenario Matrix & Stress Test Lab"
BASE_RELEASE = "1.8.0 Paper Simulation & Performance Lab"
SCHEMA_VERSION  = "181"
POLICY_VERSION  = "1.8.1-simulation-scenario-matrix-stress-test"

INCLUDED_RELEASES = [
    "v1.7.0", "v1.7.1", "v1.7.2", "v1.7.3",
    "v1.7.4", "v1.7.5", "v1.7.6", "v1.7.7", "v1.7.8", "v1.7.9",
    "v1.8.0",
]

MIN_SCENARIOS = 75
MIN_FIXTURES  = 75
MIN_CLI       = 20
MIN_HEALTH    = 55
MIN_GATE      = 55

KNOWN_RELEASE_NAMES: frozenset = frozenset({
    "Live Paper Trading Stable Rollup",
    "Small Capital Growth Strategy",
    "Watchlist Strategy Layer",
    "A/B/C Buy Point Execution Plan",
    "Market Regime Position Control",
    "Small Account Risk Dashboard",
    "Small Account Trade Journal",
    "Mistake Taxonomy & Weekly Review Dashboard",
    "Theme Rotation Scanner",
    "Small Capital Strategy Integration",
    "Small Capital Strategy Stable Rollup",
    "Paper Simulation & Performance Lab",
    "Simulation Scenario Matrix & Stress Test Lab",
})


def get_version_info() -> Dict[str, Any]:
    """Return version metadata dict."""
    return {
        "version": VERSION,
        "release_name": RELEASE_NAME,
        "base_release": BASE_RELEASE,
        "schema_version": SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
        "included_releases": INCLUDED_RELEASES,
        "min_scenarios": MIN_SCENARIOS,
        "min_fixtures": MIN_FIXTURES,
        "min_cli": MIN_CLI,
        "min_health": MIN_HEALTH,
        "min_gate": MIN_GATE,
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "stress_test_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
    }


def verify_version() -> bool:
    """Return True if version string is well-formed."""
    parts = VERSION.split(".")
    return len(parts) == 3 and all(p.isdigit() for p in parts)


def is_known_release(name: str) -> bool:
    """Return True if release name is in the known set."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(ver: str) -> bool:
    """Return True if ver >= VERSION."""
    def _parse(v: str):
        return tuple(int(x) for x in v.split("."))
    try:
        return _parse(ver) >= _parse(VERSION)
    except (ValueError, AttributeError):
        return False
