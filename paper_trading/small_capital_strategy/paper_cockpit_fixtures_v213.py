"""
paper_trading/small_capital_strategy/paper_cockpit_fixtures_v213.py
v2.0.13 Paper Market Box Range & Index Regime Control — Fixtures
[!] Paper Only. Research Only. Market Box Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

FIXTURE_VERSION = "2.0.13"
FIXTURE_SCHEMA_VERSION = "213"


def fixture_upper_zone_index() -> Dict[str, Any]:
    """Fixture: index in upper zone (45,500)."""
    return {
        "index_level": 45_500.0,
        "previous_close": 45_200.0,
        "volume_ratio": 0.95,
        "ma5": 45_000.0,
        "ma10": 44_500.0,
        "ma20": 43_800.0,
        "ma60": 42_000.0,
        "current_exposure_pct": 0.75,
        "expected_zone": "upper_zone",
        "expected_action": "reduce_exposure_near_upper_box",
        "paper_only": True,
    }


def fixture_neutral_zone_index() -> Dict[str, Any]:
    """Fixture: index in neutral zone (43,500)."""
    return {
        "index_level": 43_500.0,
        "previous_close": 43_200.0,
        "volume_ratio": 1.05,
        "ma5": 43_000.0,
        "ma10": 42_500.0,
        "ma20": 42_000.0,
        "ma60": 40_800.0,
        "current_exposure_pct": 0.62,
        "expected_zone": "neutral_zone",
        "expected_action": "normal_selective_exposure",
        "paper_only": True,
    }


def fixture_lower_zone_index() -> Dict[str, Any]:
    """Fixture: index in lower zone (41,000)."""
    return {
        "index_level": 41_000.0,
        "previous_close": 41_300.0,
        "volume_ratio": 0.80,
        "ma5": 41_500.0,
        "ma10": 42_000.0,
        "ma20": 42_500.0,
        "ma60": 43_000.0,
        "current_exposure_pct": 0.50,
        "expected_zone": "lower_zone",
        "expected_action": "core_only_low_zone",
        "paper_only": True,
    }


def fixture_extreme_risk_zone_index() -> Dict[str, Any]:
    """Fixture: index in extreme risk zone (39,000)."""
    return {
        "index_level": 39_000.0,
        "previous_close": 39_500.0,
        "volume_ratio": 1.50,
        "ma5": 40_000.0,
        "ma10": 40_500.0,
        "ma20": 41_000.0,
        "ma60": 42_000.0,
        "current_exposure_pct": 0.45,
        "expected_zone": "extreme_risk_zone",
        "expected_action": "defensive_extreme_risk",
        "paper_only": True,
    }


def fixture_below_box_index() -> Dict[str, Any]:
    """Fixture: index below box (36,000)."""
    return {
        "index_level": 36_000.0,
        "previous_close": 37_500.0,
        "volume_ratio": 2.20,
        "ma5": 37_000.0,
        "ma10": 38_000.0,
        "ma20": 39_000.0,
        "ma60": 41_000.0,
        "current_exposure_pct": 0.30,
        "expected_zone": "below_box",
        "expected_action": "below_box_defense",
        "paper_only": True,
    }


def fixture_above_box_index() -> Dict[str, Any]:
    """Fixture: index above box (48,000)."""
    return {
        "index_level": 48_000.0,
        "previous_close": 47_500.0,
        "volume_ratio": 1.80,
        "ma5": 47_000.0,
        "ma10": 46_000.0,
        "ma20": 45_000.0,
        "ma60": 43_000.0,
        "current_exposure_pct": 0.80,
        "expected_zone": "above_box",
        "expected_action": "overheating_above_box",
        "paper_only": True,
    }


def fixture_box_boundary_values() -> List[Dict[str, Any]]:
    """Fixture: exact boundary values for all zones."""
    return [
        {"index_level": 38_000.0, "expected_zone": "extreme_risk_zone"},
        {"index_level": 40_000.0, "expected_zone": "lower_zone"},
        {"index_level": 42_000.0, "expected_zone": "neutral_zone"},
        {"index_level": 45_000.0, "expected_zone": "upper_zone"},
        {"index_level": 47_000.0, "expected_zone": "above_box"},
        {"index_level": 37_999.0, "expected_zone": "below_box"},
        {"index_level": 43_500.0, "expected_zone": "neutral_zone"},
        {"index_level": 46_999.0, "expected_zone": "upper_zone"},
    ]


def fixture_all_zones() -> List[Dict[str, Any]]:
    """Fixture: one sample for each zone."""
    return [
        fixture_upper_zone_index(),
        fixture_neutral_zone_index(),
        fixture_lower_zone_index(),
        fixture_extreme_risk_zone_index(),
        fixture_below_box_index(),
        fixture_above_box_index(),
    ]


def fixture_safety_flags() -> Dict[str, Any]:
    """Fixture: expected safety flags for v2.0.13."""
    return {
        "paper_only": True,
        "research_only": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
        "no_real_orders": True,
        "no_broker": True,
        "require_box_check_before_entry": True,
        "market_box_actions_recommendation_only": True,
        "exposure_actions_recommendation_only": True,
        "chase_high_always_blocked": True,
        "schema_version": "213",
        "version": "2.0.13",
    }
