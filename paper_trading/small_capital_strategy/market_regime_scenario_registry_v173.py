"""
paper_trading/small_capital_strategy/market_regime_scenario_registry_v173.py
Scenario registry for Market Regime Position Control v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_SCHEMA  = "173"
_POLICY  = "1.7.3-market-regime-position-control"
_LINEAGE = "paper_trading.small_capital_strategy.market_regime_scenario_registry_v173"

MIN_SCENARIOS         = 65
DETERMINISTIC_SEED    = 173
SCHEMA_VERSION        = _SCHEMA

# Scenario categories
SCENARIO_CATEGORIES = [
    "bull_detection",
    "range_detection",
    "bear_detection",
    "risk_off_detection",
    "unknown_detection",
    "cash_ratio",
    "exposure_control",
    "bucket_adjustment",
    "candidate_permission",
    "abc_regime_compatibility",
    "scorecard",
    "report",
    "safety",
]


def _make_scenario(
    scenario_id: str,
    name: str,
    category: str,
    fixture_id: str,
    expected_status: str,
    expected_regime: str = "BULL",
    seed: int = DETERMINISTIC_SEED,
) -> Dict[str, Any]:
    return {
        "scenario_id": scenario_id,
        "name": name,
        "category": category,
        "fixture_id": fixture_id,
        "expected_status": expected_status,
        "expected_regime": expected_regime,
        "deterministic_seed": seed,
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
        "paper_only": True,
        "no_real_orders": True,
    }


_SCENARIOS: List[Dict[str, Any]] = [
    # bull_detection (8 scenarios)
    _make_scenario("S173-001", "bull_strong_up_healthy_breadth", "bull_detection", "F173-001", "DETECTED", "BULL"),
    _make_scenario("S173-002", "bull_mild_up_mixed_breadth", "bull_detection", "F173-002", "DETECTED", "BULL"),
    _make_scenario("S173-003", "bull_low_volatility", "bull_detection", "F173-003", "DETECTED", "BULL"),
    _make_scenario("S173-004", "bull_high_volume", "bull_detection", "F173-004", "DETECTED", "BULL"),
    _make_scenario("S173-005", "bull_above_all_mas", "bull_detection", "F173-005", "DETECTED", "BULL"),
    _make_scenario("S173-006", "bull_ma20_above_ma60", "bull_detection", "F173-006", "DETECTED", "BULL"),
    _make_scenario("S173-007", "bull_institutional_bias_positive", "bull_detection", "F173-007", "DETECTED", "BULL"),
    _make_scenario("S173-008", "bull_full_signal_confirmation", "bull_detection", "F173-008", "DETECTED", "BULL"),
    # range_detection (8 scenarios)
    _make_scenario("S173-009", "range_sideways_trend", "range_detection", "F173-009", "DETECTED", "RANGE"),
    _make_scenario("S173-010", "range_mixed_breadth", "range_detection", "F173-010", "DETECTED", "RANGE"),
    _make_scenario("S173-011", "range_moderate_volatility", "range_detection", "F173-011", "DETECTED", "RANGE"),
    _make_scenario("S173-012", "range_between_ma20_ma60", "range_detection", "F173-012", "DETECTED", "RANGE"),
    _make_scenario("S173-013", "range_low_adv_decline", "range_detection", "F173-013", "DETECTED", "RANGE"),
    _make_scenario("S173-014", "range_no_trend_direction", "range_detection", "F173-014", "DETECTED", "RANGE"),
    _make_scenario("S173-015", "range_volume_flat", "range_detection", "F173-015", "DETECTED", "RANGE"),
    _make_scenario("S173-016", "range_trend_score_zero", "range_detection", "F173-016", "DETECTED", "RANGE"),
    # bear_detection (8 scenarios)
    _make_scenario("S173-017", "bear_strong_down_weak_breadth", "bear_detection", "F173-017", "DETECTED", "BEAR"),
    _make_scenario("S173-018", "bear_below_ma60", "bear_detection", "F173-018", "DETECTED", "BEAR"),
    _make_scenario("S173-019", "bear_ma20_below_ma60", "bear_detection", "F173-019", "DETECTED", "BEAR"),
    _make_scenario("S173-020", "bear_very_weak_breadth", "bear_detection", "F173-020", "DETECTED", "BEAR"),
    _make_scenario("S173-021", "bear_low_adv_decline_ratio", "bear_detection", "F173-021", "DETECTED", "BEAR"),
    _make_scenario("S173-022", "bear_institutional_bias_negative", "bear_detection", "F173-022", "DETECTED", "BEAR"),
    _make_scenario("S173-023", "bear_mild_down_weak_breadth", "bear_detection", "F173-023", "DETECTED", "BEAR"),
    _make_scenario("S173-024", "bear_full_signal_confirmation", "bear_detection", "F173-024", "DETECTED", "BEAR"),
    # risk_off_detection (8 scenarios)
    _make_scenario("S173-025", "risk_off_below_ma120", "risk_off_detection", "F173-025", "DETECTED", "RISK_OFF"),
    _make_scenario("S173-026", "risk_off_volatility_spike", "risk_off_detection", "F173-026", "DETECTED", "RISK_OFF"),
    _make_scenario("S173-027", "risk_off_event_flag", "risk_off_detection", "F173-027", "DETECTED", "RISK_OFF"),
    _make_scenario("S173-028", "risk_off_extreme_signal", "risk_off_detection", "F173-028", "DETECTED", "RISK_OFF"),
    _make_scenario("S173-029", "risk_off_below_ma240", "risk_off_detection", "F173-029", "DETECTED", "RISK_OFF"),
    _make_scenario("S173-030", "risk_off_breadth_very_weak", "risk_off_detection", "F173-030", "DETECTED", "RISK_OFF"),
    _make_scenario("S173-031", "risk_off_combined_triggers", "risk_off_detection", "F173-031", "DETECTED", "RISK_OFF"),
    _make_scenario("S173-032", "risk_off_full_confirmation", "risk_off_detection", "F173-032", "DETECTED", "RISK_OFF"),
    # unknown_detection (5 scenarios)
    _make_scenario("S173-033", "unknown_zero_close", "unknown_detection", "F173-033", "INSUFFICIENT", "UNKNOWN"),
    _make_scenario("S173-034", "unknown_conflicting_signals", "unknown_detection", "F173-034", "CONFLICTED", "UNKNOWN"),
    _make_scenario("S173-035", "unknown_partial_data", "unknown_detection", "F173-035", "CONFLICTED", "UNKNOWN"),
    _make_scenario("S173-036", "unknown_all_zeros", "unknown_detection", "F173-036", "INSUFFICIENT", "UNKNOWN"),
    _make_scenario("S173-037", "unknown_default_input", "unknown_detection", "F173-037", "CONFLICTED", "UNKNOWN"),
    # cash_ratio (5 scenarios)
    _make_scenario("S173-038", "cash_ratio_bull_allocation", "cash_ratio", "F173-038", "VALID", "BULL"),
    _make_scenario("S173-039", "cash_ratio_range_allocation", "cash_ratio", "F173-039", "VALID", "RANGE"),
    _make_scenario("S173-040", "cash_ratio_bear_allocation", "cash_ratio", "F173-040", "VALID", "BEAR"),
    _make_scenario("S173-041", "cash_ratio_risk_off_allocation", "cash_ratio", "F173-041", "VALID", "RISK_OFF"),
    _make_scenario("S173-042", "cash_ratio_unknown_allocation", "cash_ratio", "F173-042", "VALID", "UNKNOWN"),
    # exposure_control (5 scenarios)
    _make_scenario("S173-043", "exposure_bull_limits", "exposure_control", "F173-043", "VALID", "BULL"),
    _make_scenario("S173-044", "exposure_range_limits", "exposure_control", "F173-044", "VALID", "RANGE"),
    _make_scenario("S173-045", "exposure_bear_limits", "exposure_control", "F173-045", "VALID", "BEAR"),
    _make_scenario("S173-046", "exposure_risk_off_limits", "exposure_control", "F173-046", "VALID", "RISK_OFF"),
    _make_scenario("S173-047", "exposure_no_margin_any_regime", "exposure_control", "F173-047", "VALID", "BULL"),
    # bucket_adjustment (5 scenarios)
    _make_scenario("S173-048", "bucket_bull_300k", "bucket_adjustment", "F173-048", "VALID", "BULL"),
    _make_scenario("S173-049", "bucket_bear_training_zero", "bucket_adjustment", "F173-049", "VALID", "BEAR"),
    _make_scenario("S173-050", "bucket_risk_off_training_zero", "bucket_adjustment", "F173-050", "VALID", "RISK_OFF"),
    _make_scenario("S173-051", "bucket_unknown_training_zero", "bucket_adjustment", "F173-051", "VALID", "UNKNOWN"),
    _make_scenario("S173-052", "bucket_total_equals_capital", "bucket_adjustment", "F173-052", "VALID", "RANGE"),
    # candidate_permission (5 scenarios)
    _make_scenario("S173-053", "candidate_bull_core_allowed", "candidate_permission", "F173-053", "ALLOWED", "BULL"),
    _make_scenario("S173-054", "candidate_bear_main_blocked", "candidate_permission", "F173-054", "BLOCKED", "BEAR"),
    _make_scenario("S173-055", "candidate_risk_off_blocked", "candidate_permission", "F173-055", "BLOCKED", "RISK_OFF"),
    _make_scenario("S173-056", "candidate_unknown_degraded", "candidate_permission", "F173-056", "DEGRADED", "UNKNOWN"),
    _make_scenario("S173-057", "candidate_range_selective", "candidate_permission", "F173-057", "SELECTIVE", "RANGE"),
    # abc_regime_compatibility (5 scenarios)
    _make_scenario("S173-058", "abc_bull_abc_allowed", "abc_regime_compatibility", "F173-058", "ALLOWED", "BULL"),
    _make_scenario("S173-059", "abc_bear_blocked", "abc_regime_compatibility", "F173-059", "BLOCKED", "BEAR"),
    _make_scenario("S173-060", "abc_risk_off_blocked", "abc_regime_compatibility", "F173-060", "BLOCKED", "RISK_OFF"),
    _make_scenario("S173-061", "abc_range_partial", "abc_regime_compatibility", "F173-061", "SELECTIVE", "RANGE"),
    _make_scenario("S173-062", "abc_unknown_degraded", "abc_regime_compatibility", "F173-062", "DEGRADED", "UNKNOWN"),
    # scorecard (3 scenarios)
    _make_scenario("S173-063", "scorecard_bull_grade_a", "scorecard", "F173-063", "GRADE_A", "BULL"),
    _make_scenario("S173-064", "scorecard_bear_grade_d", "scorecard", "F173-064", "GRADE_D", "BEAR"),
    _make_scenario("S173-065", "scorecard_safety_always_100", "scorecard", "F173-065", "SAFE", "BULL"),
    # report / safety (extra to exceed minimum)
    _make_scenario("S173-066", "report_14_sections", "report", "F173-066", "VALID", "BULL"),
    _make_scenario("S173-067", "report_json_render", "report", "F173-067", "VALID", "RANGE"),
    _make_scenario("S173-068", "report_markdown_render", "report", "F173-068", "VALID", "BEAR"),
    _make_scenario("S173-069", "safety_no_real_orders", "safety", "F173-069", "SAFE", "BULL"),
    _make_scenario("S173-070", "safety_no_margin", "safety", "F173-070", "SAFE", "BULL"),
]


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Return all scenarios."""
    return list(_SCENARIOS)


def get_scenario_by_id(scenario_id: str) -> Dict[str, Any]:
    """Return scenario by ID or empty dict if not found."""
    for s in _SCENARIOS:
        if s["scenario_id"] == scenario_id:
            return dict(s)
    return {}


def get_scenarios_by_category(category: str) -> List[Dict[str, Any]]:
    """Return scenarios filtered by category."""
    return [s for s in _SCENARIOS if s["category"] == category]


def count_scenarios() -> int:
    """Return total number of scenarios."""
    return len(_SCENARIOS)


def validate_registry() -> Dict[str, Any]:
    """Validate the scenario registry. Returns {valid, errors}."""
    errors = []
    seen_ids = set()
    for s in _SCENARIOS:
        sid = s.get("scenario_id", "")
        if not sid:
            errors.append("scenario_missing_id")
        if sid in seen_ids:
            errors.append(f"duplicate_scenario_id:{sid}")
        seen_ids.add(sid)
        if not s.get("name"):
            errors.append(f"scenario_missing_name:{sid}")
        if not s.get("category"):
            errors.append(f"scenario_missing_category:{sid}")
        if not s.get("fixture_id"):
            errors.append(f"scenario_missing_fixture_id:{sid}")
        if s.get("deterministic_seed") != DETERMINISTIC_SEED:
            errors.append(f"wrong_seed:{sid}")
        if not s.get("paper_only"):
            errors.append(f"paper_only_false:{sid}")
    if len(_SCENARIOS) < MIN_SCENARIOS:
        errors.append(f"too_few_scenarios:{len(_SCENARIOS)}<{MIN_SCENARIOS}")
    return {"valid": len(errors) == 0, "errors": errors, "count": len(_SCENARIOS)}
