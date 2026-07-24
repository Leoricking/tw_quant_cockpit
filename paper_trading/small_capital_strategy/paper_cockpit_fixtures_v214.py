"""
paper_trading/small_capital_strategy/paper_cockpit_fixtures_v214.py
v2.0.14 Paper Pullback Reaction & Crash Rebound Confirmation — Fixtures
[!] Paper Only. Research Only. Pullback Reaction Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

FIXTURE_VERSION = "2.0.14"
FIXTURE_SCHEMA_VERSION = "214"


def fixture_default_pullback_policy() -> Dict[str, Any]:
    """Fixture: default pullback policy. Paper only."""
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import PullbackPolicy
    pol = PullbackPolicy(policy_id="fixture-default-v214")
    return {
        "policy_id": pol.policy_id,
        "observation_window_days": pol.observation_window_days,
        "seasonal_ma_period": pol.seasonal_ma_period,
        "reclaim_fast_ma_period": pol.reclaim_fast_ma_period,
        "reclaim_slow_ma_period": pol.reclaim_slow_ma_period,
        "require_index_near_ma60": pol.require_index_near_ma60,
        "require_reclaim_ma5_or_ma10_for_confirmation": pol.require_reclaim_ma5_or_ma10_for_confirmation,
        "require_tsmc_confirmation": pol.require_tsmc_confirmation,
        "require_futures_or_adr_confirmation": pol.require_futures_or_adr_confirmation,
        "require_margin_not_stressed": pol.require_margin_not_stressed,
        "failure_if_breaks_pullback_low": pol.failure_if_breaks_pullback_low,
        "auto_apply_enabled": pol.auto_apply_enabled,
        "paper_only": pol.paper_only,
        "schema_version": pol.schema_version,
    }


def fixture_pullback_event_observation() -> Dict[str, Any]:
    """Fixture: pullback event in observation state. Paper only."""
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import detect_pullback_event
    evt = detect_pullback_event(
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
    )
    return {
        "schema_version": evt.schema_version,
        "paper_only": evt.paper_only,
        "current_index_level": evt.current_index_level,
        "pullback_pct": evt.pullback_pct,
        "near_ma60": evt.near_ma60,
        "reclaimed_ma5": evt.reclaimed_ma5,
        "reclaimed_ma10": evt.reclaimed_ma10,
        "broke_pullback_low": evt.broke_pullback_low,
        "should_auto_apply": evt.should_auto_apply,
    }


def fixture_confirmation_signal_full() -> Dict[str, Any]:
    """Fixture: full confirmation signal with all signals positive. Paper only."""
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import evaluate_rebound_confirmation
    conf = evaluate_rebound_confirmation(
        tsmc_spot_up=True,
        tsmc_adr_positive=True,
        futures_night_stable=True,
        foreign_futures_short_increasing=False,
        margin_stress=False,
        volume_expansion=True,
        ma_reclaim=True,
    )
    return {
        "schema_version": conf.schema_version,
        "paper_only": conf.paper_only,
        "tsmc_spot_confirmed": conf.tsmc_spot_confirmed,
        "tsmc_adr_confirmed": conf.tsmc_adr_confirmed,
        "futures_night_session_stable": conf.futures_night_session_stable,
        "foreign_futures_short_not_increasing": conf.foreign_futures_short_not_increasing,
        "margin_stress_controlled": conf.margin_stress_controlled,
        "volume_confirmation": conf.volume_confirmation,
        "ma_reclaim_confirmation": conf.ma_reclaim_confirmation,
        "confirmation_score": conf.confirmation_score,
        "failed_confirmation_reasons": conf.failed_confirmation_reasons,
        "should_auto_apply": conf.should_auto_apply,
    }


def fixture_confirmation_signal_empty() -> Dict[str, Any]:
    """Fixture: empty confirmation signal with all signals negative. Paper only."""
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import evaluate_rebound_confirmation
    conf = evaluate_rebound_confirmation(
        tsmc_spot_up=False,
        tsmc_adr_positive=False,
        futures_night_stable=False,
        foreign_futures_short_increasing=True,
        margin_stress=True,
        volume_expansion=False,
        ma_reclaim=False,
    )
    return {
        "schema_version": conf.schema_version,
        "paper_only": conf.paper_only,
        "confirmation_score": conf.confirmation_score,
        "failed_count": len(conf.failed_confirmation_reasons),
        "should_auto_apply": conf.should_auto_apply,
    }


def fixture_default_review_result() -> Dict[str, Any]:
    """Fixture: default pullback review result. Paper only."""
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import run_pullback_reaction_review
    result = run_pullback_reaction_review()
    evt = result.index_snapshot
    conf = result.rebound_confirmation_snapshot
    summ = result.pullback_summary
    return {
        "schema_version": result.schema_version,
        "paper_only": result.paper_only,
        "pullback_review_id": result.pullback_review_id,
        "pullback_version": result.pullback_version,
        "should_auto_apply": result.should_auto_apply,
        "auto_apply_enabled": result.auto_apply_enabled,
        "reaction_state": evt.reaction_state if evt else "",
        "confirmation_score": conf.confirmation_score if conf else 0.0,
        "recommended_action": summ.recommended_action if summ else "",
    }


def get_all_fixtures() -> Dict[str, Any]:
    """Return all v2.0.14 fixtures. Paper only."""
    return {
        "default_pullback_policy": fixture_default_pullback_policy(),
        "pullback_event_observation": fixture_pullback_event_observation(),
        "confirmation_signal_full": fixture_confirmation_signal_full(),
        "confirmation_signal_empty": fixture_confirmation_signal_empty(),
        "default_review_result": fixture_default_review_result(),
        "fixture_version": FIXTURE_VERSION,
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "paper_only": True,
        "should_auto_apply": False,
        "auto_apply_enabled": False,
    }
