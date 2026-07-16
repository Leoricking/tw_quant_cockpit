"""
paper_trading/small_capital_strategy/decision_journal_fixtures_v189.py
JSON fixtures for Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json
from typing import Dict, List

_SAFETY = dict(
    paper_only=True, research_only=True, simulate_only=True,
    validation_only=True, decision_only=True, journal_only=True,
    review_only=True, report_only=True, audit_only=True,
    no_real_orders=True, no_broker=True, no_margin=True, no_leverage=True,
    not_investment_advice=True, demo_only=True,
    not_for_production=True, production_trading_blocked=True,
)

_FIXTURE_DIR = "fixtures/decision_journal_v189/"

_FIXTURES: List[Dict] = []

_ENTRY_STATES = [
    "OBSERVE", "WAIT", "PAPER_PLAN_READY", "PAPER_ENTRY_ALLOWED", "PAPER_ADD_ALLOWED",
    "REDUCE_RISK", "REVIEW_REQUIRED", "BLOCKED", "NO_TRADE", "RESEARCH_ONLY",
    "SIMULATE_ONLY", "VALIDATION_ONLY", "DECISION_ONLY", "REPORT_ONLY",
    "WORKFLOW_ONLY", "AUDIT_ONLY",
]

_REVIEW_TYPES = [
    "daily_review", "weekly_review", "monthly_review",
]

_QUALITY_GRADES = [
    "EXCELLENT", "GOOD", "ACCEPTABLE", "REVIEW_REQUIRED", "POOR", "INVALID",
]

_REGIMES = ["BULL", "WATCH", "BEAR", "BLOCKED", "RISK_OFF"]
_CAPITAL_STAGES = ["300K", "500K", "1M", "3M"]
_SYMBOLS = ["TSMC", "MEDIATEK", "ASUS", "DELTA", "ACER", "HON_HAI", "LARGAN", "CATHAY",
            "FUBON", "CTBC", "STOCK_A", "STOCK_B", "STOCK_C", "STOCK_D", "STOCK_E"]
_MISTAKE_TAGS = [
    "CHASE_HIGH", "ENTER_TOO_EARLY", "IGNORE_MARKET_REGIME", "IGNORE_VOLUME_RISK",
    "OVERSIZE_POSITION", "OVER_CONCENTRATION", "LOW_CASH_RESERVE", "MISSING_EVIDENCE",
    "NO_CLEAR_STOP", "NO_CLEAR_TAKE_PROFIT", "NO_MISTAKE_FOUND",
]

for i in range(1, 76):
    state = _ENTRY_STATES[(i - 1) % len(_ENTRY_STATES)]
    review_type = _REVIEW_TYPES[(i - 1) % len(_REVIEW_TYPES)]
    grade = _QUALITY_GRADES[(i - 1) % len(_QUALITY_GRADES)]
    regime = _REGIMES[(i - 1) % len(_REGIMES)]
    capital = _CAPITAL_STAGES[(i - 1) % len(_CAPITAL_STAGES)]
    symbol = _SYMBOLS[(i - 1) % len(_SYMBOLS)]
    mistake = _MISTAKE_TAGS[(i - 1) % len(_MISTAKE_TAGS)]
    exposure = round(min(90.0, (i % 10) * 9.0), 1)
    cash = round(100.0 - exposure, 1)
    risk_usage = round(min(95.0, (i % 8) * 12.0), 1)
    size_pct = round(max(5.0, (i % 5) * 5.0), 1)
    stop = round((i % 4) * 2.5, 1)
    tp = round((i % 4) * 7.5, 1)
    has_evidence = (i % 3 != 0)
    has_workflow = (i % 4 != 0)
    _FIXTURES.append({
        "fixture_id": f"DJF189-{i:03d}",
        "fixture_name": f"journal_fixture_{i:03d}_{state.lower()}_{review_type}",
        "entry_state": state,
        "review_type": review_type,
        "quality_grade": grade,
        "market_regime": regime if regime not in ("BEAR", "BLOCKED", "RISK_OFF") or state == "BLOCKED" else "BULL",
        "capital_stage": capital,
        "symbol": symbol,
        "date_label": f"2026-W{(i % 52) + 1:02d}-D{(i % 5) + 1}",
        "workflow_id": f"WF-{i:04d}" if has_workflow else "",
        "evidence_refs": [f"evidence_{i:03d}_a", f"evidence_{i:03d}_b"] if has_evidence else [],
        "rationale": f"Scenario {i}: {state} for {symbol} in {regime} regime" if has_evidence else "",
        "planned_size_pct": size_pct,
        "stop_loss_pct": stop,
        "take_profit_pct": tp,
        "risk_budget_usage_pct": risk_usage,
        "total_exposure_pct": exposure,
        "cash_reserve_pct": cash,
        "monte_carlo_ruin_risk": round((i % 5) * 2.0, 1),
        "drawdown_budget_usage_pct": round(exposure * 0.3, 1),
        "mistake_tags": [mistake],
        "findings": [f"Finding {i}: check {mistake}"] if mistake != "NO_MISTAKE_FOUND" else [],
        "action_items": [f"Action {i}: address {mistake}"] if mistake != "NO_MISTAKE_FOUND" else [],
        "audit_trail_complete": True,
        "export_path": "reports/journal/",
        "deterministic_timestamp_policy": "date_label_only_no_wall_clock",
        "expected_paper_only": True,
        "expected_no_real_orders": True,
        "expected_no_broker": True,
        "expected_not_investment_advice": True,
        "expected_production_trading_blocked": True,
        **_SAFETY,
    })

assert len(_FIXTURES) == 75, f"Expected 75 fixtures, got {len(_FIXTURES)}"


def get_fixtures() -> List[Dict]:
    """Return all 75 fixtures."""
    return list(_FIXTURES)


def get_fixture_count() -> int:
    """Return total fixture count."""
    return len(_FIXTURES)


def get_fixture_dir() -> str:
    """Return fixture directory path."""
    return _FIXTURE_DIR


def get_fixture_by_id(fixture_id: str):
    """Return fixture by ID, or None."""
    for f in _FIXTURES:
        if f["fixture_id"] == fixture_id:
            return dict(f)
    return None


def get_fixture_as_json(fixture_id: str) -> str:
    """Return fixture serialized as JSON string."""
    f = get_fixture_by_id(fixture_id)
    if f is None:
        return "{}"
    return json.dumps(f, indent=2, ensure_ascii=False)


def get_fixture_info() -> Dict:
    """Return fixture registry info."""
    return {
        "count": len(_FIXTURES),
        "fixture_dir": _FIXTURE_DIR,
        "entry_states": _ENTRY_STATES,
        "review_types": _REVIEW_TYPES,
        "quality_grades": _QUALITY_GRADES,
        "paper_only": True,
        "research_only": True,
        "journal_only": True,
        "review_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "schema_version": "189",
    }
