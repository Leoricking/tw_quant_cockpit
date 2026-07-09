"""
paper_trading/small_capital_strategy/trade_journal_fixture_schema_v175.py
Fixture schema for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"
_LINEAGE = "paper_trading.small_capital_strategy.trade_journal_fixture_schema_v175"

REQUIRED_FIXTURE_FIELDS: List[str] = [
    "id",
    "symbol",
    "direction",
    "entry_date",
    "exit_date",
    "entry_price",
    "exit_price",
    "outcome",
    "abc_pattern",
    "market_regime",
    "watchlist_tier",
    "mistake_categories",
    "paper_only",
    "research_only",
    "no_real_orders",
    "no_broker",
    "not_investment_advice",
    "demo_only",
    "not_for_production",
]

REQUIRED_SAFETY_MARKERS: List[str] = [
    "paper_only",
    "research_only",
    "no_real_orders",
    "no_broker",
    "not_investment_advice",
    "demo_only",
    "not_for_production",
]


def validate_fixture(fixture: Dict[str, Any]) -> bool:
    """Return True if the fixture has all required fields and safety markers."""
    for f in REQUIRED_FIXTURE_FIELDS:
        if f not in fixture:
            return False
    for marker in REQUIRED_SAFETY_MARKERS:
        if not fixture.get(marker):
            return False
    return True


def get_fixture_schema() -> Dict[str, Any]:
    """Return the fixture schema definition dict."""
    return {
        "required_fields":        REQUIRED_FIXTURE_FIELDS,
        "required_safety_markers": REQUIRED_SAFETY_MARKERS,
        "schema_version":         _SCHEMA,
        "policy_version":         _POLICY,
        "source_lineage":         _LINEAGE,
        "paper_only":             True,
        "no_real_orders":         True,
    }
