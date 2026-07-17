"""
paper_trading/small_capital_strategy/strategy_tuning_fixtures_v191.py
75 JSON fixtures for Paper Strategy Rule Tuning & Guardrail Lab v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA = "191"
_SAFETY = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "tuning_only": True,
    "guardrail_only": True,
    "review_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_strategy_mutation": True,
    "not_investment_advice": True,
    "demo_only": True,
    "not_for_production": True,
    "production_trading_blocked": True,
}

_RULE_CATEGORIES = [
    "ABC_BUY_POINT", "SECOND_WAVE_ENTRY", "MARKET_REGIME_FILTER",
    "VOLUME_CONFIRMATION", "MOVING_AVERAGE_FILTER", "POSITION_SIZING",
    "CASH_RESERVE", "CONCENTRATION_LIMIT", "STOP_LOSS", "TAKE_PROFIT",
    "REDUCE_RISK", "BLOCKED_CONDITION", "EVIDENCE_REQUIREMENT", "MANUAL_REVIEW",
]
_GUARDRAIL_TRIGGERS = [
    "EXPECTANCY_NEGATIVE", "WIN_RATE_TOO_LOW", "AVERAGE_LOSS_TOO_HIGH",
    "DRAWDOWN_BUDGET_EXCEEDED", "MISTAKE_RATE_TOO_HIGH", "CHASE_HIGH_REPEATED",
    "EARLY_ENTRY_REPEATED", "OVER_CONCENTRATION_REPEATED", "LOW_CASH_RESERVE_REPEATED",
    "BLOCK_REASON_IGNORED", "EVIDENCE_MISSING_REPEATED", "MARKET_REGIME_MISMATCH",
    "VOLUME_CONFIRMATION_MISSING", "MA_BREAK_IGNORED", "NO_CLEAR_STOP",
    "NO_CLEAR_TAKE_PROFIT",
]
_RECOMMENDATIONS = [
    "KEEP_RULE", "TIGHTEN_RULE", "LOOSEN_RULE", "DISABLE_SETUP",
    "LOWER_POSITION_SIZE", "RAISE_CASH_RESERVE", "LOWER_CONCENTRATION_LIMIT",
    "REQUIRE_MORE_EVIDENCE", "REQUIRE_MARKET_REGIME_CONFIRMATION",
    "REQUIRE_VOLUME_CONFIRMATION", "REQUIRE_MA_CONFIRMATION",
    "REQUIRE_MANUAL_REVIEW", "ADD_GUARDRAIL", "ESCALATE_TO_REVIEW", "NO_CHANGE",
]
_APPROVAL_STATES = [
    "PROPOSED", "REVIEW_REQUIRED", "PAPER_APPROVED", "PAPER_REJECTED", "BLOCKED", "INVALID",
]
_SEVERITIES = ["INFO", "WARNING", "CRITICAL", "HARD_BLOCK"]

FIXTURES: List[Dict[str, Any]] = []

for _i in range(75):
    _idx = _i + 1
    _fid = f"STF191-{_idx:03d}"
    _rule_cat = _RULE_CATEGORIES[_i % len(_RULE_CATEGORIES)]
    _trigger = _GUARDRAIL_TRIGGERS[_i % len(_GUARDRAIL_TRIGGERS)]
    _rec = _RECOMMENDATIONS[_i % len(_RECOMMENDATIONS)]
    _state = _APPROVAL_STATES[_i % len(_APPROVAL_STATES)]
    _severity = _SEVERITIES[_i % len(_SEVERITIES)]
    _win_rate = round(0.25 + (_i % 40) * 0.01, 2)
    _expectancy = round(-0.3 + (_i % 30) * 0.03, 4)
    _mistake_rate = round((_i % 35) * 0.01, 2)
    _drawdown_usage = round(0.20 + (_i % 50) * 0.01, 2)
    _cash_reserve = round(0.15 + (_i % 25) * 0.01, 2)
    _concentration = round(0.10 + (_i % 20) * 0.01, 2)
    _evidence_count = 3 + (_i % 10)
    FIXTURES.append({
        "fixture_id": _fid,
        "tuning_id": f"tuning_{_fid}",
        "period_label": f"period_{_idx:03d}",
        "rule_category": _rule_cat,
        "guardrail_trigger": _trigger,
        "recommendation": _rec,
        "approval_state": _state,
        "severity": _severity,
        "win_rate": _win_rate,
        "expectancy_r": _expectancy,
        "mistake_rate": _mistake_rate,
        "drawdown_budget_usage_pct": _drawdown_usage,
        "cash_reserve_pct": _cash_reserve,
        "concentration_pct": _concentration,
        "evidence_count": _evidence_count,
        "all_evidence_present": _evidence_count >= 5,
        "guardrail_triggered": _expectancy < 0.0 or _win_rate < 0.35,
        "improvement_detected": _expectancy > 0.1,
        "requires_manual_review": _state in ("REVIEW_REQUIRED", "BLOCKED"),
        "auto_approve_blocked": True,
        "no_production_strategy_mutation": True,
        "production_trading_blocked": True,
        "schema_version": _SCHEMA,
        **_SAFETY,
    })


def get_all_fixtures() -> List[Dict[str, Any]]:
    """Return all 75 rule tuning fixtures."""
    return list(FIXTURES)


def get_fixture_by_id(fixture_id: str) -> Dict[str, Any]:
    """Return a fixture by ID, or empty dict if not found."""
    for f in FIXTURES:
        if f.get("fixture_id") == fixture_id:
            return f
    return {}


def get_fixtures_by_recommendation(recommendation: str) -> List[Dict[str, Any]]:
    """Return fixtures matching a given recommendation type."""
    return [f for f in FIXTURES if f.get("recommendation") == recommendation]


def get_fixtures_by_rule_category(rule_category: str) -> List[Dict[str, Any]]:
    """Return fixtures matching a given rule category."""
    return [f for f in FIXTURES if f.get("rule_category") == rule_category]


def get_fixtures_by_approval_state(state: str) -> List[Dict[str, Any]]:
    """Return fixtures matching a given approval state."""
    return [f for f in FIXTURES if f.get("approval_state") == state]
