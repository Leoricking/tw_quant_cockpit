"""
paper_trading/small_capital_strategy/optimization_version_v182.py
Version metadata for Parameter Optimization & Walk-Forward Validation Lab v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

VERSION = "1.8.2"
RELEASE_NAME = "Parameter Optimization & Walk-Forward Validation Lab"
BASE_RELEASE = "v1.8.1-simulation-scenario-matrix-stress-test-lab"
SCHEMA_VERSION = "182"
POLICY_VERSION = "1.8.2-small-capital-strategy-parameter-optimization"
INCLUDED_RELEASES = [
    "Small Capital Strategy v1.7.0",
    "Watchlist Strategy Layer v1.7.1",
    "A/B/C Buy Point Execution Plan v1.7.2",
    "Market Regime Position Control v1.7.3",
    "Small Account Trade Journal v1.7.5",
    "Mistake Taxonomy Review Dashboard v1.7.6",
    "Theme Rotation Scanner v1.7.7",
    "Small Capital Strategy Integration v1.7.8",
    "Small Capital Strategy Stable Rollup v1.7.9",
    "Paper Simulation & Performance Lab v1.8.0",
    "Simulation Scenario Matrix & Stress Test Lab v1.8.1",
    "Parameter Optimization & Walk-Forward Validation Lab v1.8.2",
]
MIN_SCENARIOS = 75
MIN_FIXTURES = 75
MIN_CLI = 17
MIN_HEALTH_CHECKS = 60
KNOWN_RELEASE_NAMES = [
    "Small Capital Strategy v1.7.0",
    "Watchlist Strategy Layer v1.7.1",
    "A/B/C Buy Point Execution Plan v1.7.2",
    "Market Regime Position Control v1.7.3",
    "Small Account Trade Journal v1.7.5",
    "Mistake Taxonomy Review Dashboard v1.7.6",
    "Theme Rotation Scanner v1.7.7",
    "Small Capital Strategy Integration v1.7.8",
    "Small Capital Strategy Stable Rollup v1.7.9",
    "Paper Simulation & Performance Lab v1.8.0",
    "Simulation Scenario Matrix & Stress Test Lab v1.8.1",
    "Parameter Optimization & Walk-Forward Validation Lab v1.8.2",
]


def get_version_info() -> dict:
    """Return version metadata dict."""
    return {
        "version": VERSION,
        "release_name": RELEASE_NAME,
        "paper_only": True,
        "research_only": True,
        "simulate_only": True,
        "validation_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "no_broker": True,
        "schema_version": SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
    }


def verify_version() -> bool:
    """Return True if VERSION == '1.8.2'."""
    return VERSION == "1.8.2"


def is_known_release(name: str) -> bool:
    """Return True if name is in KNOWN_RELEASE_NAMES."""
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(min_version: str) -> bool:
    """Return True if VERSION >= min_version (simple string compare)."""
    return VERSION >= min_version
