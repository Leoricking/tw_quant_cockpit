"""
paper_trading/small_capital_strategy/paper_cockpit_scenarios_v214.py
v2.0.14 Paper Pullback Reaction & Crash Rebound Confirmation — Scenarios
[!] Paper Only. Research Only. Pullback Reaction Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

SCENARIO_VERSION = "2.0.14"
SCENARIO_SCHEMA_VERSION = "214"


def scenario_no_pullback() -> Dict[str, Any]:
    """Scenario: No significant pullback. Observation only."""
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import (
        PullbackReviewInput, PullbackPolicy, run_pullback_reaction_review,
    )
    policy = PullbackPolicy(policy_id="scenario-no-pullback-v214")
    review_input = PullbackReviewInput(
        review_period="2026-W29",
        index_level=45_000.0,
        previous_close=44_800.0,
        pullback_start_level=45_200.0,
        pullback_low_level=44_800.0,
        pullback_low_date="2026-07-20",
        days_since_pullback_low=1,
        ma5=44_900.0,
        ma10=44_500.0,
        ma20=44_000.0,
        ma60=43_000.0,
        tsmc_spot_up=True,
        tsmc_adr_positive=True,
        futures_night_stable=True,
        foreign_futures_short_increasing=False,
        margin_stress=False,
        volume_expansion=False,
        policy=policy,
    )
    result = run_pullback_reaction_review(review_input)
    evt = result.index_snapshot
    return {
        "scenario": "no_pullback",
        "reaction_state": evt.reaction_state if evt else "",
        "pullback_pct": evt.pullback_pct if evt else 0.0,
        "should_auto_apply": result.should_auto_apply,
        "auto_apply_enabled": result.auto_apply_enabled,
        "paper_only": result.paper_only,
    }


def scenario_observation_rebound() -> Dict[str, Any]:
    """Scenario: Crash near MA60, 1-3 day observation window. Observation only."""
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import (
        PullbackReviewInput, PullbackPolicy, run_pullback_reaction_review,
    )
    policy = PullbackPolicy(policy_id="scenario-observation-v214")
    review_input = PullbackReviewInput(
        review_period="2026-W29",
        index_level=43_000.0,
        previous_close=44_500.0,
        pullback_start_level=45_000.0,
        pullback_low_level=42_800.0,
        pullback_low_date="2026-07-18",
        days_since_pullback_low=2,
        ma5=43_500.0,
        ma10=44_000.0,
        ma20=44_500.0,
        ma60=42_900.0,
        tsmc_spot_up=False,
        tsmc_adr_positive=False,
        futures_night_stable=False,
        foreign_futures_short_increasing=True,
        margin_stress=False,
        volume_expansion=False,
        policy=policy,
    )
    result = run_pullback_reaction_review(review_input)
    evt = result.index_snapshot
    return {
        "scenario": "observation_rebound",
        "reaction_state": evt.reaction_state if evt else "",
        "near_ma60": evt.near_ma60 if evt else False,
        "days_since_pullback_low": evt.days_since_pullback_low if evt else 0,
        "should_auto_apply": result.should_auto_apply,
        "auto_apply_enabled": result.auto_apply_enabled,
        "paper_only": result.paper_only,
    }


def scenario_short_term_rebound_confirmed() -> Dict[str, Any]:
    """Scenario: Reclaimed MA5, TSMC confirmed, high score. Short-term confirmed."""
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import (
        PullbackReviewInput, PullbackPolicy, run_pullback_reaction_review,
    )
    policy = PullbackPolicy(policy_id="scenario-confirmed-v214")
    review_input = PullbackReviewInput(
        review_period="2026-W29",
        index_level=44_200.0,
        previous_close=43_000.0,
        pullback_start_level=45_000.0,
        pullback_low_level=42_500.0,
        pullback_low_date="2026-07-16",
        days_since_pullback_low=3,
        ma5=44_000.0,
        ma10=44_500.0,
        ma20=44_800.0,
        ma60=42_800.0,
        tsmc_spot_up=True,
        tsmc_adr_positive=True,
        futures_night_stable=True,
        foreign_futures_short_increasing=False,
        margin_stress=False,
        volume_expansion=True,
        policy=policy,
    )
    result = run_pullback_reaction_review(review_input)
    evt = result.index_snapshot
    conf = result.rebound_confirmation_snapshot
    return {
        "scenario": "short_term_rebound_confirmed",
        "reaction_state": evt.reaction_state if evt else "",
        "reclaimed_ma5": evt.reclaimed_ma5 if evt else False,
        "confirmation_score": conf.confirmation_score if conf else 0.0,
        "should_auto_apply": result.should_auto_apply,
        "auto_apply_enabled": result.auto_apply_enabled,
        "paper_only": result.paper_only,
    }


def scenario_rebound_failed() -> Dict[str, Any]:
    """Scenario: Broke pullback low. Rebound failed — reduce risk."""
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import (
        PullbackReviewInput, PullbackPolicy, run_pullback_reaction_review,
    )
    policy = PullbackPolicy(policy_id="scenario-failed-v214")
    review_input = PullbackReviewInput(
        review_period="2026-W29",
        index_level=41_500.0,
        previous_close=42_000.0,
        pullback_start_level=45_000.0,
        pullback_low_level=42_000.0,
        pullback_low_date="2026-07-15",
        days_since_pullback_low=5,
        ma5=42_800.0,
        ma10=43_500.0,
        ma20=44_000.0,
        ma60=43_200.0,
        tsmc_spot_up=False,
        tsmc_adr_positive=False,
        futures_night_stable=False,
        foreign_futures_short_increasing=True,
        margin_stress=True,
        volume_expansion=False,
        policy=policy,
    )
    result = run_pullback_reaction_review(review_input)
    evt = result.index_snapshot
    return {
        "scenario": "rebound_failed",
        "reaction_state": evt.reaction_state if evt else "",
        "broke_pullback_low": evt.broke_pullback_low if evt else False,
        "should_auto_apply": result.should_auto_apply,
        "auto_apply_enabled": result.auto_apply_enabled,
        "paper_only": result.paper_only,
    }


def scenario_defensive_wait() -> Dict[str, Any]:
    """Scenario: Low confirmation score. Defensive wait for second confirmation."""
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import (
        PullbackReviewInput, PullbackPolicy, run_pullback_reaction_review,
    )
    policy = PullbackPolicy(policy_id="scenario-defensive-v214")
    review_input = PullbackReviewInput(
        review_period="2026-W29",
        index_level=42_800.0,
        previous_close=43_200.0,
        pullback_start_level=45_000.0,
        pullback_low_level=42_500.0,
        pullback_low_date="2026-07-17",
        days_since_pullback_low=2,
        ma5=43_200.0,
        ma10=43_800.0,
        ma20=44_200.0,
        ma60=42_900.0,
        tsmc_spot_up=False,
        tsmc_adr_positive=False,
        futures_night_stable=False,
        foreign_futures_short_increasing=True,
        margin_stress=False,
        volume_expansion=False,
        policy=policy,
    )
    result = run_pullback_reaction_review(review_input)
    evt = result.index_snapshot
    conf = result.rebound_confirmation_snapshot
    return {
        "scenario": "defensive_wait_second_confirmation",
        "reaction_state": evt.reaction_state if evt else "",
        "confirmation_score": conf.confirmation_score if conf else 0.0,
        "should_auto_apply": result.should_auto_apply,
        "auto_apply_enabled": result.auto_apply_enabled,
        "paper_only": result.paper_only,
    }


def scenario_human_review_required() -> Dict[str, Any]:
    """Scenario: Extreme pullback > 10%, human review required."""
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import (
        PullbackReviewInput, PullbackPolicy, run_pullback_reaction_review,
    )
    policy = PullbackPolicy(policy_id="scenario-human-review-v214")
    review_input = PullbackReviewInput(
        review_period="2026-W29",
        index_level=40_000.0,
        previous_close=40_500.0,
        pullback_start_level=45_000.0,
        pullback_low_level=39_500.0,
        pullback_low_date="2026-07-10",
        days_since_pullback_low=10,
        ma5=40_500.0,
        ma10=41_500.0,
        ma20=42_500.0,
        ma60=43_500.0,
        tsmc_spot_up=False,
        tsmc_adr_positive=False,
        futures_night_stable=False,
        foreign_futures_short_increasing=True,
        margin_stress=True,
        volume_expansion=False,
        policy=policy,
    )
    result = run_pullback_reaction_review(review_input)
    evt = result.index_snapshot
    return {
        "scenario": "human_review_required",
        "reaction_state": evt.reaction_state if evt else "",
        "requires_human_review": evt.requires_human_review if evt else False,
        "human_review_count": len(result.human_review_queue),
        "should_auto_apply": result.should_auto_apply,
        "auto_apply_enabled": result.auto_apply_enabled,
        "paper_only": result.paper_only,
    }


def run_all_scenarios() -> Dict[str, Any]:
    """Run all v2.0.14 scenarios. Paper only."""
    return {
        "no_pullback": scenario_no_pullback(),
        "observation_rebound": scenario_observation_rebound(),
        "short_term_rebound_confirmed": scenario_short_term_rebound_confirmed(),
        "rebound_failed": scenario_rebound_failed(),
        "defensive_wait": scenario_defensive_wait(),
        "human_review_required": scenario_human_review_required(),
        "schema_version": SCENARIO_SCHEMA_VERSION,
        "paper_only": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
    }
