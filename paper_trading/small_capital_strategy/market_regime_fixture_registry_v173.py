"""
paper_trading/small_capital_strategy/market_regime_fixture_registry_v173.py
Fixture registry for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.market_regime_fixture_schema_v173 import (
    make_fixture, validate_fixture,
)

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.market_regime_fixture_registry_v173"

MIN_FIXTURES      = 65
DETERMINISTIC_SEED = 173

# Helper inputs
_BULL_INPUTS   = {"index_close": 20000.0, "index_ma20": 19500.0, "index_ma60": 18800.0, "index_ma120": 17500.0, "index_ma240": 16000.0, "index_volume_ratio": 1.3, "advance_decline_ratio": 1.8, "volatility_score": 20.0, "risk_event_flag": False, "institutional_market_bias": 0.5, "major_index_trend_score": 1.0}
_RANGE_INPUTS  = {"index_close": 18000.0, "index_ma20": 18200.0, "index_ma60": 18100.0, "index_ma120": 17000.0, "index_ma240": 15500.0, "index_volume_ratio": 1.0, "advance_decline_ratio": 1.1, "volatility_score": 40.0, "risk_event_flag": False, "institutional_market_bias": 0.0, "major_index_trend_score": 0.0}
_BEAR_INPUTS   = {"index_close": 15000.0, "index_ma20": 16000.0, "index_ma60": 17000.0, "index_ma120": 18000.0, "index_ma240": 19000.0, "index_volume_ratio": 0.8, "advance_decline_ratio": 0.4, "volatility_score": 60.0, "risk_event_flag": False, "institutional_market_bias": -0.5, "major_index_trend_score": -1.0}
_RISK_OFF_INPUTS = {"index_close": 14000.0, "index_ma20": 15000.0, "index_ma60": 16000.0, "index_ma120": 17000.0, "index_ma240": 18000.0, "index_volume_ratio": 0.6, "advance_decline_ratio": 0.3, "volatility_score": 80.0, "risk_event_flag": True, "institutional_market_bias": -1.0, "major_index_trend_score": -2.0}
_UNKNOWN_INPUTS = {"index_close": 0.0, "index_ma20": 0.0, "index_ma60": 0.0, "index_ma120": 0.0, "index_ma240": 0.0, "index_volume_ratio": 1.0, "advance_decline_ratio": 1.0, "volatility_score": 0.0, "risk_event_flag": False, "institutional_market_bias": 0.0, "major_index_trend_score": 0.0}


def _f(fid, name, cat, sid, inp, exp):
    return make_fixture(fid, name, cat, sid, inp, exp, seed=DETERMINISTIC_SEED)


_FIXTURES: List[Dict[str, Any]] = [
    # Bull fixtures
    _f("F173-001", "bull_strong_up_healthy_breadth", "bull_detection", "S173-001", _BULL_INPUTS, {"regime": "BULL", "status": "DETECTED"}),
    _f("F173-002", "bull_mild_up_mixed_breadth", "bull_detection", "S173-002", {**_BULL_INPUTS, "advance_decline_ratio": 1.2}, {"regime": "BULL", "status": "DETECTED"}),
    _f("F173-003", "bull_low_volatility", "bull_detection", "S173-003", {**_BULL_INPUTS, "volatility_score": 10.0}, {"regime": "BULL", "status": "DETECTED"}),
    _f("F173-004", "bull_high_volume", "bull_detection", "S173-004", {**_BULL_INPUTS, "index_volume_ratio": 2.0}, {"regime": "BULL", "status": "DETECTED"}),
    _f("F173-005", "bull_above_all_mas", "bull_detection", "S173-005", _BULL_INPUTS, {"above_ma20": True, "above_ma60": True}),
    _f("F173-006", "bull_ma20_above_ma60", "bull_detection", "S173-006", _BULL_INPUTS, {"ma20_above_ma60": True}),
    _f("F173-007", "bull_institutional_bias_positive", "bull_detection", "S173-007", _BULL_INPUTS, {"institutional_bias": 0.5}),
    _f("F173-008", "bull_full_signal_confirmation", "bull_detection", "S173-008", _BULL_INPUTS, {"regime": "BULL", "confidence_min": 0.75}),
    # Range fixtures
    _f("F173-009", "range_sideways_trend", "range_detection", "S173-009", _RANGE_INPUTS, {"regime": "RANGE", "status": "DETECTED"}),
    _f("F173-010", "range_mixed_breadth", "range_detection", "S173-010", _RANGE_INPUTS, {"breadth": "MIXED"}),
    _f("F173-011", "range_moderate_volatility", "range_detection", "S173-011", _RANGE_INPUTS, {"volatility_level": "MODERATE"}),
    _f("F173-012", "range_between_ma20_ma60", "range_detection", "S173-012", _RANGE_INPUTS, {"regime": "RANGE"}),
    _f("F173-013", "range_low_adv_decline", "range_detection", "S173-013", {**_RANGE_INPUTS, "advance_decline_ratio": 0.95}, {"breadth": "MIXED"}),
    _f("F173-014", "range_no_trend_direction", "range_detection", "S173-014", _RANGE_INPUTS, {"trend": "SIDEWAYS"}),
    _f("F173-015", "range_volume_flat", "range_detection", "S173-015", {**_RANGE_INPUTS, "index_volume_ratio": 1.0}, {"regime": "RANGE"}),
    _f("F173-016", "range_trend_score_zero", "range_detection", "S173-016", _RANGE_INPUTS, {"regime": "RANGE"}),
    # Bear fixtures
    _f("F173-017", "bear_strong_down_weak_breadth", "bear_detection", "S173-017", _BEAR_INPUTS, {"regime": "BEAR", "status": "DETECTED"}),
    _f("F173-018", "bear_below_ma60", "bear_detection", "S173-018", _BEAR_INPUTS, {"below_ma60": True}),
    _f("F173-019", "bear_ma20_below_ma60", "bear_detection", "S173-019", _BEAR_INPUTS, {"ma20_above_ma60": False}),
    _f("F173-020", "bear_very_weak_breadth", "bear_detection", "S173-020", {**_BEAR_INPUTS, "advance_decline_ratio": 0.3}, {"breadth": "VERY_WEAK"}),
    _f("F173-021", "bear_low_adv_decline_ratio", "bear_detection", "S173-021", _BEAR_INPUTS, {"advance_decline_ratio": 0.4}),
    _f("F173-022", "bear_institutional_bias_negative", "bear_detection", "S173-022", _BEAR_INPUTS, {"institutional_bias": -0.5}),
    _f("F173-023", "bear_mild_down_weak_breadth", "bear_detection", "S173-023", _BEAR_INPUTS, {"regime": "BEAR"}),
    _f("F173-024", "bear_full_signal_confirmation", "bear_detection", "S173-024", _BEAR_INPUTS, {"regime": "BEAR", "confidence_min": 0.75}),
    # Risk-off fixtures
    _f("F173-025", "risk_off_below_ma120", "risk_off_detection", "S173-025", _RISK_OFF_INPUTS, {"regime": "RISK_OFF"}),
    _f("F173-026", "risk_off_volatility_spike", "risk_off_detection", "S173-026", _RISK_OFF_INPUTS, {"vol_spike": True}),
    _f("F173-027", "risk_off_event_flag", "risk_off_detection", "S173-027", _RISK_OFF_INPUTS, {"risk_event": True}),
    _f("F173-028", "risk_off_extreme_signal", "risk_off_detection", "S173-028", _RISK_OFF_INPUTS, {"signal": "EXTREME"}),
    _f("F173-029", "risk_off_below_ma240", "risk_off_detection", "S173-029", _RISK_OFF_INPUTS, {"below_ma240": True}),
    _f("F173-030", "risk_off_breadth_very_weak", "risk_off_detection", "S173-030", _RISK_OFF_INPUTS, {"breadth": "VERY_WEAK"}),
    _f("F173-031", "risk_off_combined_triggers", "risk_off_detection", "S173-031", _RISK_OFF_INPUTS, {"regime": "RISK_OFF"}),
    _f("F173-032", "risk_off_full_confirmation", "risk_off_detection", "S173-032", _RISK_OFF_INPUTS, {"regime": "RISK_OFF", "status": "DETECTED"}),
    # Unknown fixtures
    _f("F173-033", "unknown_zero_close", "unknown_detection", "S173-033", _UNKNOWN_INPUTS, {"regime": "UNKNOWN", "status": "INSUFFICIENT"}),
    _f("F173-034", "unknown_conflicting_signals", "unknown_detection", "S173-034", {**_BULL_INPUTS, "advance_decline_ratio": 0.3, "volatility_score": 80.0}, {"regime": "UNKNOWN", "status": "CONFLICTED"}),
    _f("F173-035", "unknown_partial_data", "unknown_detection", "S173-035", {**_UNKNOWN_INPUTS, "index_close": 100.0}, {"regime": "UNKNOWN"}),
    _f("F173-036", "unknown_all_zeros", "unknown_detection", "S173-036", _UNKNOWN_INPUTS, {"status": "INSUFFICIENT"}),
    _f("F173-037", "unknown_default_input", "unknown_detection", "S173-037", _UNKNOWN_INPUTS, {"regime": "UNKNOWN"}),
    # Cash ratio fixtures
    _f("F173-038", "cash_ratio_bull_allocation", "cash_ratio", "S173-038", {"regime": "BULL"}, {"cash_pct": 5, "total_pct": 100}),
    _f("F173-039", "cash_ratio_range_allocation", "cash_ratio", "S173-039", {"regime": "RANGE"}, {"cash_pct": 25, "total_pct": 100}),
    _f("F173-040", "cash_ratio_bear_allocation", "cash_ratio", "S173-040", {"regime": "BEAR"}, {"cash_pct": 50, "total_pct": 100}),
    _f("F173-041", "cash_ratio_risk_off_allocation", "cash_ratio", "S173-041", {"regime": "RISK_OFF"}, {"cash_pct": 60, "total_pct": 100}),
    _f("F173-042", "cash_ratio_unknown_allocation", "cash_ratio", "S173-042", {"regime": "UNKNOWN"}, {"cash_pct": 40, "total_pct": 100}),
    # Exposure control fixtures
    _f("F173-043", "exposure_bull_limits", "exposure_control", "S173-043", {"regime": "BULL"}, {"max_total_pct": 95, "margin_allowed": False}),
    _f("F173-044", "exposure_range_limits", "exposure_control", "S173-044", {"regime": "RANGE"}, {"max_total_pct": 75, "margin_allowed": False}),
    _f("F173-045", "exposure_bear_limits", "exposure_control", "S173-045", {"regime": "BEAR"}, {"max_total_pct": 50, "margin_allowed": False}),
    _f("F173-046", "exposure_risk_off_limits", "exposure_control", "S173-046", {"regime": "RISK_OFF"}, {"max_total_pct": 40, "margin_allowed": False}),
    _f("F173-047", "exposure_no_margin_any_regime", "exposure_control", "S173-047", {"regime": "BULL"}, {"margin_allowed": False, "leverage_allowed": False}),
    # Bucket adjustment fixtures
    _f("F173-048", "bucket_bull_300k", "bucket_adjustment", "S173-048", {"regime": "BULL", "capital": 300000}, {"core_amount": 120000.0, "training_amount": 15000.0}),
    _f("F173-049", "bucket_bear_training_zero", "bucket_adjustment", "S173-049", {"regime": "BEAR", "capital": 300000}, {"training_amount": 0.0}),
    _f("F173-050", "bucket_risk_off_training_zero", "bucket_adjustment", "S173-050", {"regime": "RISK_OFF", "capital": 300000}, {"training_amount": 0.0}),
    _f("F173-051", "bucket_unknown_training_zero", "bucket_adjustment", "S173-051", {"regime": "UNKNOWN", "capital": 300000}, {"training_amount": 0.0}),
    _f("F173-052", "bucket_total_equals_capital", "bucket_adjustment", "S173-052", {"regime": "RANGE", "capital": 300000}, {"total_equals_capital": True}),
    # Candidate permission fixtures
    _f("F173-053", "candidate_bull_core_allowed", "candidate_permission", "S173-053", {"regime": "BULL", "tier": "CORE"}, {"permission": "ALLOWED", "max_candidates": 5}),
    _f("F173-054", "candidate_bear_main_blocked", "candidate_permission", "S173-054", {"regime": "BEAR", "tier": "MAIN_THEME_SWING"}, {"permission": "BLOCKED"}),
    _f("F173-055", "candidate_risk_off_blocked", "candidate_permission", "S173-055", {"regime": "RISK_OFF", "tier": "MAIN_THEME_SWING"}, {"permission": "BLOCKED"}),
    _f("F173-056", "candidate_unknown_degraded", "candidate_permission", "S173-056", {"regime": "UNKNOWN", "tier": "MAIN_THEME_SWING"}, {"permission": "DEGRADED"}),
    _f("F173-057", "candidate_range_selective", "candidate_permission", "S173-057", {"regime": "RANGE", "tier": "CORE"}, {"permission": "SELECTIVE"}),
    # ABC regime compatibility fixtures
    _f("F173-058", "abc_bull_abc_allowed", "abc_regime_compatibility", "S173-058", {"regime": "BULL"}, {"a": True, "b": True, "c": True}),
    _f("F173-059", "abc_bear_blocked", "abc_regime_compatibility", "S173-059", {"regime": "BEAR"}, {"a": False, "b": False, "c": False}),
    _f("F173-060", "abc_risk_off_blocked", "abc_regime_compatibility", "S173-060", {"regime": "RISK_OFF"}, {"a": False, "b": False, "c": False}),
    _f("F173-061", "abc_range_partial", "abc_regime_compatibility", "S173-061", {"regime": "RANGE"}, {"a": True, "b": True}),
    _f("F173-062", "abc_unknown_degraded", "abc_regime_compatibility", "S173-062", {"regime": "UNKNOWN"}, {"a": True}),
    # Scorecard fixtures
    _f("F173-063", "scorecard_bull_grade_a", "scorecard", "S173-063", {"regime": "BULL"}, {"grade_min": "A"}),
    _f("F173-064", "scorecard_bear_grade_d", "scorecard", "S173-064", {"regime": "BEAR"}, {"grade": "D_or_below"}),
    _f("F173-065", "scorecard_safety_always_100", "scorecard", "S173-065", {"regime": "BULL"}, {"safety_score": 100.0}),
    # Report/safety fixtures
    _f("F173-066", "report_14_sections", "report", "S173-066", {"regime": "BULL"}, {"section_count": 14}),
    _f("F173-067", "report_json_render", "report", "S173-067", {"regime": "RANGE"}, {"format": "JSON"}),
    _f("F173-068", "report_markdown_render", "report", "S173-068", {"regime": "BEAR"}, {"format": "markdown"}),
    _f("F173-069", "safety_no_real_orders", "safety", "S173-069", {}, {"no_real_orders": True}),
    _f("F173-070", "safety_no_margin", "safety", "S173-070", {}, {"margin_enabled": False}),
]


def get_all_fixtures() -> List[Dict[str, Any]]:
    """Return all fixtures."""
    return list(_FIXTURES)


def get_fixture_by_id(fixture_id: str) -> Dict[str, Any]:
    """Return fixture by ID or empty dict if not found."""
    for f in _FIXTURES:
        if f["fixture_id"] == fixture_id:
            return dict(f)
    return {}


def get_fixtures_by_category(category: str) -> List[Dict[str, Any]]:
    """Return fixtures filtered by category."""
    return [f for f in _FIXTURES if f["category"] == category]


def count_fixtures() -> int:
    """Return total number of fixtures."""
    return len(_FIXTURES)


def validate_registry() -> Dict[str, Any]:
    """Validate the fixture registry. Returns {valid, errors}."""
    errors = []
    seen_ids = set()
    for f in _FIXTURES:
        fid = f.get("fixture_id", "")
        if not fid:
            errors.append("fixture_missing_id")
        if fid in seen_ids:
            errors.append(f"duplicate_fixture_id:{fid}")
        seen_ids.add(fid)
        result = validate_fixture(f)
        if not result["valid"]:
            for e in result["errors"]:
                errors.append(f"{fid}:{e}")
    if len(_FIXTURES) < MIN_FIXTURES:
        errors.append(f"too_few_fixtures:{len(_FIXTURES)}<{MIN_FIXTURES}")
    return {"valid": len(errors) == 0, "errors": errors, "count": len(_FIXTURES)}
