"""
paper_trading/small_capital_strategy/position_sizing_fixtures_v184.py
Fixture registry for Position Sizing & Capital Allocation Lab v1.8.4.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Allocation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os

_FIXTURE_DIR = _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)),
    "..", "..", "tests", "fixtures", "position_sizing",
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
        "allocation_only": True,
        "no_real_orders": True,
        "schema_version": "184",
    }
