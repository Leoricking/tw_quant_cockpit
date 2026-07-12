"""
paper_trading/small_capital_strategy/monte_carlo_fixtures_v183.py
Fixture registry for Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pathlib


def get_fixture_dir() -> pathlib.Path:
    """Return path to Monte Carlo fixture directory."""
    return pathlib.Path(__file__).resolve().parent.parent.parent / "tests" / "fixtures" / "monte_carlo"


def get_fixture_count() -> int:
    """Return number of JSON fixture files."""
    d = get_fixture_dir()
    if not d.exists():
        return 0
    return len(list(d.glob("*.json")))


def get_fixture_info() -> dict:
    """Return fixture metadata dict."""
    return {
        "version": "1.8.3",
        "fixture_dir": str(get_fixture_dir()),
        "count": get_fixture_count(),
        "paper_only": True,
        "monte_carlo_only": True,
        "schema_version": "183",
    }
