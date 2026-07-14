"""
paper_trading/small_capital_strategy/decision_report_fixtures_v187.py
Fixture registry for Decision Report Export & Evidence Pack v1.8.7.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os

_FIXTURE_DIR = _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)),
    "..", "..", "tests", "fixtures", "decision_report",
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
        "simulate_only": True,
        "validation_only": True,
        "decision_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "no_margin": True,
        "no_leverage": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "production_trading_blocked": True,
        "schema_version": "187",
    }
