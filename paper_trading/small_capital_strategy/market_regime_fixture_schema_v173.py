"""
paper_trading/small_capital_strategy/market_regime_fixture_schema_v173.py
Fixture schema for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.market_regime_fixture_schema_v173"

REQUIRED_FIXTURE_FIELDS = [
    "fixture_id",
    "name",
    "category",
    "scenario_id",
    "inputs",
    "expected",
    "deterministic_seed",
    "paper_only",
    "no_real_orders",
]

REQUIRED_INPUT_FIELDS = [
    "index_close",
    "index_ma20",
    "index_ma60",
    "index_ma120",
    "index_ma240",
]

# Categories that require market data inputs
_DETECTION_CATEGORIES = {
    "bull_detection", "range_detection", "bear_detection",
    "risk_off_detection", "unknown_detection",
}


def validate_fixture(fixture: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a single fixture dict.
    Returns {valid, errors}.
    """
    errors = []
    for f in REQUIRED_FIXTURE_FIELDS:
        if f not in fixture:
            errors.append(f"missing_field:{f}")
    if not fixture.get("paper_only"):
        errors.append("paper_only_false")
    if not fixture.get("no_real_orders"):
        errors.append("no_real_orders_false")
    inputs = fixture.get("inputs", {})
    category = fixture.get("category", "")
    if category in _DETECTION_CATEGORIES:
        for f in REQUIRED_INPUT_FIELDS:
            if f not in inputs:
                errors.append(f"missing_input:{f}")
    if fixture.get("deterministic_seed") != int(_SCHEMA):
        errors.append(f"wrong_seed:{fixture.get('deterministic_seed')}")
    return {"valid": len(errors) == 0, "errors": errors}


def make_fixture(
    fixture_id: str,
    name: str,
    category: str,
    scenario_id: str,
    inputs: Dict[str, Any],
    expected: Dict[str, Any],
    seed: int = int(_SCHEMA),
) -> Dict[str, Any]:
    """Create a validated fixture dict."""
    return {
        "fixture_id": fixture_id,
        "name": name,
        "category": category,
        "scenario_id": scenario_id,
        "inputs": inputs,
        "expected": expected,
        "deterministic_seed": seed,
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def get_required_fields() -> List[str]:
    """Return required fixture fields."""
    return list(REQUIRED_FIXTURE_FIELDS)


def get_required_input_fields() -> List[str]:
    """Return required input fields."""
    return list(REQUIRED_INPUT_FIELDS)
