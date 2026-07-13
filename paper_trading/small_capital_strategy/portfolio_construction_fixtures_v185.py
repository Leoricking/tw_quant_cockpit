"""
paper_trading/small_capital_strategy/portfolio_construction_fixtures_v185.py
Fixture registry for Portfolio Construction & Rebalancing Lab v1.8.5.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Portfolio Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os

_FIXTURE_DIR = _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)),
    "..", "..", "tests", "fixtures", "portfolio_construction",
)

_EXPECTED_COUNT = 75


def get_fixture_dir() -> str:
    """Return absolute path to fixture directory."""
    return _os.path.normpath(_FIXTURE_DIR)


def get_fixture_count() -> int:
    """Return expected fixture count."""
    return _EXPECTED_COUNT


def get_fixture_info() -> dict:
    """Return fixture registry info."""
    return {
        "fixture_dir": get_fixture_dir(),
        "expected_count": _EXPECTED_COUNT,
        "paper_only": True,
        "research_only": True,
        "portfolio_only": True,
        "no_real_orders": True,
        "schema_version": "185",
    }
