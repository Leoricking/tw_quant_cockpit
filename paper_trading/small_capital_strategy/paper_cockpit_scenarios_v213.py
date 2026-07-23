"""
paper_trading/small_capital_strategy/paper_cockpit_scenarios_v213.py
v2.0.13 Paper Market Box Range & Index Regime Control — Scenarios
[!] Paper Only. Research Only. Market Box Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

SCENARIO_VERSION = "2.0.13"
SCENARIO_SCHEMA_VERSION = "213"


def scenario_upper_zone_review() -> Dict[str, Any]:
    """Scenario: TWI in upper zone 45,000-47,000. Reduce exposure, no chase-high."""
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import (
        MarketBoxReviewInput, MarketBoxPolicy, run_market_box_review,
    )
    policy = MarketBoxPolicy(policy_id="scenario-upper-zone-v213")
    review_input = MarketBoxReviewInput(
        review_period="2026-W29",
        index_level=46_000.0,
        previous_close=45_800.0,
        volume_ratio=0.95,
        ma5=45_500.0,
        ma10=44_800.0,
        ma20=44_000.0,
        ma60=42_500.0,
        current_exposure_pct=0.78,
        policy=policy,
    )
    result = run_market_box_review(review_input)
    return {
        "scenario": "upper_zone_review",
        "zone": result.zone_classification,
        "exposure_action": result.exposure_control_snapshot.exposure_action if result.exposure_control_snapshot else "",
        "chase_high_blocked": len(result.chase_risk_snapshot),
        "should_auto_apply": result.should_auto_apply,
        "auto_apply_enabled": result.auto_apply_enabled,
        "paper_only": result.paper_only,
    }


def scenario_neutral_zone_review() -> Dict[str, Any]:
    """Scenario: TWI in neutral zone 42,000-45,000. Normal selective exposure."""
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import (
        MarketBoxReviewInput, MarketBoxPolicy, run_market_box_review,
    )
    policy = MarketBoxPolicy(policy_id="scenario-neutral-zone-v213")
    review_input = MarketBoxReviewInput(
        review_period="2026-W29",
        index_level=43_500.0,
        previous_close=43_200.0,
        volume_ratio=1.05,
        ma5=43_000.0,
        ma10=42_500.0,
        ma20=42_000.0,
        ma60=40_800.0,
        current_exposure_pct=0.62,
        policy=policy,
    )
    result = run_market_box_review(review_input)
    return {
        "scenario": "neutral_zone_review",
        "zone": result.zone_classification,
        "exposure_action": result.exposure_control_snapshot.exposure_action if result.exposure_control_snapshot else "",
        "should_auto_apply": result.should_auto_apply,
        "auto_apply_enabled": result.auto_apply_enabled,
        "paper_only": result.paper_only,
    }


def scenario_lower_zone_review() -> Dict[str, Any]:
    """Scenario: TWI in lower zone 40,000-42,000. Core-only low-zone filter."""
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import (
        MarketBoxReviewInput, MarketBoxPolicy, run_market_box_review,
    )
    policy = MarketBoxPolicy(policy_id="scenario-lower-zone-v213")
    review_input = MarketBoxReviewInput(
        review_period="2026-W29",
        index_level=41_000.0,
        previous_close=41_300.0,
        volume_ratio=0.80,
        ma5=41_500.0,
        ma10=42_000.0,
        ma20=42_500.0,
        ma60=43_000.0,
        current_exposure_pct=0.50,
        policy=policy,
    )
    result = run_market_box_review(review_input)
    return {
        "scenario": "lower_zone_review",
        "zone": result.zone_classification,
        "exposure_action": result.exposure_control_snapshot.exposure_action if result.exposure_control_snapshot else "",
        "core_only_candidates": len(result.low_zone_core_only_snapshot),
        "should_auto_apply": result.should_auto_apply,
        "auto_apply_enabled": result.auto_apply_enabled,
        "paper_only": result.paper_only,
    }


def scenario_extreme_risk_zone_review() -> Dict[str, Any]:
    """Scenario: TWI in extreme risk zone 38,000-40,000. Defensive mode."""
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import (
        MarketBoxReviewInput, MarketBoxPolicy, run_market_box_review,
    )
    policy = MarketBoxPolicy(policy_id="scenario-extreme-risk-v213")
    review_input = MarketBoxReviewInput(
        review_period="2026-W29",
        index_level=39_000.0,
        previous_close=39_500.0,
        volume_ratio=1.50,
        ma5=40_000.0,
        ma10=40_500.0,
        ma20=41_000.0,
        ma60=42_000.0,
        current_exposure_pct=0.45,
        policy=policy,
    )
    result = run_market_box_review(review_input)
    return {
        "scenario": "extreme_risk_zone_review",
        "zone": result.zone_classification,
        "exposure_action": result.exposure_control_snapshot.exposure_action if result.exposure_control_snapshot else "",
        "defensive_count": len(result.defensive_mode_snapshot),
        "human_review_count": len(result.human_review_queue),
        "should_auto_apply": result.should_auto_apply,
        "auto_apply_enabled": result.auto_apply_enabled,
        "paper_only": result.paper_only,
    }


def scenario_below_box_defense() -> Dict[str, Any]:
    """Scenario: TWI below box < 38,000. Full defensive mode."""
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import (
        MarketBoxReviewInput, MarketBoxPolicy, run_market_box_review,
    )
    policy = MarketBoxPolicy(policy_id="scenario-below-box-v213")
    review_input = MarketBoxReviewInput(
        review_period="2026-W29",
        index_level=36_000.0,
        previous_close=37_500.0,
        volume_ratio=2.20,
        ma5=37_000.0,
        ma10=38_000.0,
        ma20=39_000.0,
        ma60=41_000.0,
        current_exposure_pct=0.30,
        policy=policy,
    )
    result = run_market_box_review(review_input)
    return {
        "scenario": "below_box_defense",
        "zone": result.zone_classification,
        "exposure_action": result.exposure_control_snapshot.exposure_action if result.exposure_control_snapshot else "",
        "human_review_count": len(result.human_review_queue),
        "should_auto_apply": result.should_auto_apply,
        "auto_apply_enabled": result.auto_apply_enabled,
        "paper_only": result.paper_only,
    }


def scenario_above_box_overheating() -> Dict[str, Any]:
    """Scenario: TWI above box > 47,000. Overheating mode."""
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import (
        MarketBoxReviewInput, MarketBoxPolicy, run_market_box_review,
    )
    policy = MarketBoxPolicy(policy_id="scenario-above-box-v213")
    review_input = MarketBoxReviewInput(
        review_period="2026-W29",
        index_level=48_000.0,
        previous_close=47_500.0,
        volume_ratio=1.80,
        ma5=47_000.0,
        ma10=46_000.0,
        ma20=45_000.0,
        ma60=43_000.0,
        current_exposure_pct=0.80,
        policy=policy,
    )
    result = run_market_box_review(review_input)
    return {
        "scenario": "above_box_overheating",
        "zone": result.zone_classification,
        "exposure_action": result.exposure_control_snapshot.exposure_action if result.exposure_control_snapshot else "",
        "chase_high_blocked": len(result.chase_risk_snapshot),
        "human_review_count": len(result.human_review_queue),
        "should_auto_apply": result.should_auto_apply,
        "auto_apply_enabled": result.auto_apply_enabled,
        "paper_only": result.paper_only,
    }


def run_all_scenarios() -> Dict[str, Any]:
    """Run all v2.0.13 scenarios. Paper only."""
    return {
        "upper_zone": scenario_upper_zone_review(),
        "neutral_zone": scenario_neutral_zone_review(),
        "lower_zone": scenario_lower_zone_review(),
        "extreme_risk_zone": scenario_extreme_risk_zone_review(),
        "below_box": scenario_below_box_defense(),
        "above_box": scenario_above_box_overheating(),
        "schema_version": SCENARIO_SCHEMA_VERSION,
        "paper_only": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
    }
