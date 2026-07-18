"""
paper_trading/small_capital_strategy/strategy_sandbox_fixtures_v192.py
75 JSON fixtures for Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_SCHEMA = "192"
_SAFETY: Dict[str, Any] = dict(
    paper_only=True,
    research_only=True,
    simulate_only=True,
    validation_only=True,
    sandbox_only=True,
    shadow_only=True,
    review_only=True,
    report_only=True,
    audit_only=True,
    no_real_orders=True,
    no_broker=True,
    no_margin=True,
    no_leverage=True,
    no_production_strategy_mutation=True,
    no_live_strategy_activation=True,
    not_investment_advice=True,
    demo_only=True,
    not_for_production=True,
    production_trading_blocked=True,
)

_SANDBOX_MODES: List[str] = [
    "BASELINE_ONLY",
    "CANDIDATE_ONLY",
    "SHADOW_COMPARE",
    "A_B_RULE_COMPARE",
    "GUARDRAIL_COMPARE",
    "POSITION_SIZING_COMPARE",
    "CASH_RESERVE_COMPARE",
    "CONCENTRATION_LIMIT_COMPARE",
    "FULL_RULESET_COMPARE",
    "REGRESSION_ONLY",
    "SAFETY_ONLY",
]

_APPROVAL_STATES: List[str] = [
    "SHADOW_ONLY",
    "PAPER_APPROVED",
    "REVIEW_REQUIRED",
    "BLOCKED",
    "REGRESSION_DETECTED",
    "INVALID",
]

_RECOMMENDATIONS: List[str] = [
    "KEEP_BASELINE",
    "ACCEPT_CANDIDATE_FOR_PAPER",
    "KEEP_SHADOW_TESTING",
    "REJECT_CANDIDATE",
    "TIGHTEN_MORE",
    "LOOSEN_MORE",
    "REQUIRE_MORE_DATA",
    "REQUIRE_MANUAL_REVIEW",
    "ADD_GUARDRAIL",
    "REMOVE_CANDIDATE_GUARDRAIL",
    "LOWER_POSITION_SIZE",
    "RAISE_CASH_RESERVE",
    "NO_CHANGE",
]

_VALIDATION_DIMENSIONS: List[str] = [
    "signal_count_delta",
    "blocked_signal_delta",
    "win_rate_delta",
    "expectancy_delta_r",
    "average_gain_delta_r",
    "average_loss_delta_r",
    "profit_factor_delta",
    "max_drawdown_delta_r",
    "drawdown_budget_usage_delta_pct",
    "mistake_rate_delta",
    "chase_high_delta",
    "early_entry_delta",
    "over_concentration_delta",
    "low_cash_reserve_delta",
    "evidence_completeness_delta",
    "blocked_condition_respect_delta",
    "opportunity_loss_score",
    "risk_reduction_score",
    "rule_stability_score",
    "shadow_validation_score",
]

FIXTURES: List[Dict[str, Any]] = []

for _i in range(75):
    _idx = _i + 1
    _fid = f"SSF192-{_idx:03d}"
    _mode = _SANDBOX_MODES[_i % len(_SANDBOX_MODES)]
    _state = _APPROVAL_STATES[_i % len(_APPROVAL_STATES)]
    _rec = _RECOMMENDATIONS[_i % len(_RECOMMENDATIONS)]
    _dim = _VALIDATION_DIMENSIONS[_i % len(_VALIDATION_DIMENSIONS)]
    _win_rate = round(0.25 + (_i % 40) * 0.01, 2)
    _win_rate_delta = round(-0.1 + (_i % 20) * 0.01, 4)
    _expectancy_r = round(-0.3 + (_i % 30) * 0.03, 4)
    _expectancy_delta_r = round(-0.2 + (_i % 25) * 0.02, 4)
    _max_drawdown_r = round(-2.0 - (_i % 15) * 0.1, 4)
    _signal_count = 10 + (_i % 30)
    _blocked = (_i % 7 == 0)
    FIXTURES.append({
        "fixture_id": _fid,
        "sandbox_id": f"sandbox_{_fid}",
        "period_label": f"period_{_idx:03d}",
        "sandbox_mode": _mode,
        "approval_state": _state,
        "recommendation": _rec,
        "primary_dimension": _dim,
        "baseline_win_rate": _win_rate,
        "win_rate_delta": _win_rate_delta,
        "baseline_expectancy_r": _expectancy_r,
        "expectancy_delta_r": _expectancy_delta_r,
        "max_drawdown_r": _max_drawdown_r,
        "signal_count": _signal_count,
        "blocked": _blocked,
        "evidence_count": 3 + (_i % 10),
        "tuning_proposal_source": f"tuning_proposal_{_idx:03d}",
        "baseline_snapshot_id": f"baseline_snap_{_idx:03d}",
        "candidate_snapshot_id": f"candidate_snap_{_idx:03d}",
        "schema_version": _SCHEMA,
        **_SAFETY,
    })

assert len(FIXTURES) == 75, f"Expected 75 fixtures, got {len(FIXTURES)}"


def get_all_fixtures() -> List[Dict[str, Any]]:
    """Return all 75 sandbox fixtures for v1.9.2."""
    return list(FIXTURES)


def get_fixture_by_id(fixture_id: str) -> Optional[Dict[str, Any]]:
    """Return a single fixture by its fixture_id, or None if not found."""
    for fixture in FIXTURES:
        if fixture["fixture_id"] == fixture_id:
            return fixture
    return None
