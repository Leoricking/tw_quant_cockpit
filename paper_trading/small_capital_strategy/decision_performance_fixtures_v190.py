"""
paper_trading/small_capital_strategy/decision_performance_fixtures_v190.py
75 JSON fixtures for Paper Trading Performance Review & Strategy Improvement Lab v1.9.0.
[!] Research Only. Paper Only. Performance Review Only. Strategy Improvement Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA = "190"
_SAFETY = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "review_only": True,
    "performance_review_only": True,
    "strategy_improvement_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "not_investment_advice": True,
    "demo_only": True,
    "not_for_production": True,
    "production_trading_blocked": True,
}

_SETUP_TYPES = [
    "A_10MA_PULLBACK", "B_BASE_BREAKOUT", "C_20MA_RECLAIM",
    "SECOND_WAVE", "WATCHLIST_ONLY", "REDUCE_RISK",
    "BLOCKED_MARKET", "BLOCKED_RISK", "BLOCKED_EVIDENCE",
    "NO_TRADE_DAY", "UNKNOWN_SETUP",
]
_GRADES = ["EXCELLENT", "GOOD", "ACCEPTABLE", "REVIEW_REQUIRED", "POOR", "INVALID"]
_SUGGESTIONS = [
    "KEEP_RULE", "TIGHTEN_RULE", "LOOSEN_RULE", "LOWER_POSITION_SIZE",
    "RAISE_CASH_RESERVE", "BLOCK_SETUP", "REQUIRE_MORE_EVIDENCE",
    "REQUIRE_MARKET_REGIME_CONFIRMATION", "REQUIRE_VOLUME_CONFIRMATION",
    "REQUIRE_MA_CONFIRMATION", "REQUIRE_RISK_REVIEW", "REVIEW_MANUALLY", "NO_CHANGE",
]

FIXTURES: List[Dict[str, Any]] = []

for _i in range(75):
    _idx = _i + 1
    _fid = f"DPF190-{_idx:03d}"
    _grade = _GRADES[_i % len(_GRADES)]
    _setup = _SETUP_TYPES[_i % len(_SETUP_TYPES)]
    _suggestion = _SUGGESTIONS[_i % len(_SUGGESTIONS)]
    _win_rate = round(0.30 + (_i % 40) * 0.01, 2)
    _expectancy = round(-0.2 + (_i % 30) * 0.03, 4)
    _total = 10 + (_i % 15)
    _wins = int(_total * _win_rate)
    _losses = _total - _wins
    _r_avg_win = round(1.0 + (_i % 10) * 0.1, 2)
    _r_avg_loss = round(-1.0 - (_i % 5) * 0.1, 2)
    FIXTURES.append({
        "fixture_id": _fid,
        "review_id": f"review_{_fid}",
        "period_label": f"period_{_idx:03d}",
        "setup_type": _setup,
        "total_decisions": _total,
        "wins": _wins,
        "losses": _losses,
        "win_rate": _win_rate,
        "average_gain_r": _r_avg_win,
        "average_loss_r": _r_avg_loss,
        "expectancy_r": _expectancy,
        "quality_grade": _grade,
        "improvement_suggestion": _suggestion,
        "max_drawdown_r": round(1.0 + (_i % 8) * 0.4, 2),
        "drawdown_budget_r": 6.0,
        "drawdown_within_budget": True,
        "mistake_rate": round((_i % 30) * 0.01, 2),
        "evidence_completeness_rate": round(0.70 + (_i % 30) * 0.01, 2),
        "blocked_condition_respect_rate": round(0.80 + (_i % 20) * 0.01, 2),
        "overtrade_score": round((_i % 20) * 0.02, 2),
        "chase_high_score": round((_i % 15) * 0.02, 2),
        "early_entry_score": round((_i % 12) * 0.02, 2),
        "risk_control_score": round(0.60 + (_i % 40) * 0.01, 2),
        "strategy_improvement_score": round(0.50 + (_i % 50) * 0.01, 2),
        "export_path": "reports/",
        "safe_export_path": True,
        "audit_trail_complete": True,
        "deterministic_timestamp_policy": "date_label_only_no_wall_clock",
        "schema_version": _SCHEMA,
        **_SAFETY,
    })

assert len(FIXTURES) == 75, f"Expected 75 fixtures, got {len(FIXTURES)}"


def get_all_fixtures() -> List[Dict[str, Any]]:
    """Return all 75 performance review fixtures."""
    return list(FIXTURES)


def get_fixture_by_id(fixture_id: str) -> Dict[str, Any]:
    """Return a fixture by its ID, or empty dict if not found."""
    for f in FIXTURES:
        if f.get("fixture_id") == fixture_id:
            return f
    return {}


def get_fixtures_by_grade(grade: str) -> List[Dict[str, Any]]:
    """Return fixtures filtered by quality_grade."""
    return [f for f in FIXTURES if f.get("quality_grade") == grade]
