"""
paper_trading/small_capital_strategy/decision_workflow_fixtures_v188.py
JSON fixtures for Paper Decision Workflow Runner v1.8.8.
[!] Research Only. Paper Only. Workflow Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json
from typing import Dict, List

_SAFETY = dict(
    paper_only=True, research_only=True, simulate_only=True,
    validation_only=True, decision_only=True, workflow_only=True,
    report_only=True, audit_only=True, no_real_orders=True,
    no_broker=True, no_margin=True, no_leverage=True,
    not_investment_advice=True, demo_only=True,
    not_for_production=True, production_trading_blocked=True,
)

_FIXTURE_DIR = "fixtures/decision_workflow_v188/"

_FIXTURES: List[Dict] = []

# Build 75 fixtures programmatically
_WORKFLOW_TYPES = [
    "daily_workflow", "weekly_workflow", "pre_market_workflow",
    "post_market_workflow", "watchlist_workflow", "candidate_review_workflow",
    "risk_review_workflow", "portfolio_review_workflow", "blocked_market_workflow",
    "report_generation_workflow", "evidence_pack_workflow", "audit_trail_workflow",
]

_REGIMES = ["BULL", "WATCH", "BEAR", "BLOCKED", "RISK_OFF"]

_CAPITAL_STAGES = ["300K", "500K", "1M", "3M"]

for i in range(1, 76):
    wt = _WORKFLOW_TYPES[(i - 1) % len(_WORKFLOW_TYPES)]
    regime = _REGIMES[(i - 1) % len(_REGIMES)]
    capital = _CAPITAL_STAGES[(i - 1) % len(_CAPITAL_STAGES)]
    exposure = round(min(95.0, (i % 10) * 8.0), 1)
    cash = round(100.0 - exposure, 1)
    ruin = round((i % 5) * 2.0, 1)
    n_candidates = i % 4
    _FIXTURES.append({
        "fixture_id": f"DWF188-{i:03d}",
        "fixture_name": f"workflow_fixture_{i:03d}_{wt}",
        "workflow_type": wt,
        "market_regime": regime if regime not in ("BEAR", "BLOCKED", "RISK_OFF") or wt == "blocked_market_workflow" else "BULL",
        "capital_stage": capital,
        "candidates": [f"STOCK_{chr(65 + j)}" for j in range(n_candidates)],
        "watchlist": [f"WATCH_{chr(65 + j)}" for j in range(max(0, n_candidates - 1))],
        "portfolio_holdings": [],
        "total_exposure_pct": exposure,
        "cash_reserve_pct": cash,
        "monte_carlo_ruin_risk": ruin,
        "drawdown_budget_usage_pct": round(exposure * 0.3, 1),
        "theme_exposure_summary": {},
        "sector_exposure_summary": {},
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
    """Return the total fixture count."""
    return len(_FIXTURES)


def get_fixture_dir() -> str:
    """Return the fixture directory path."""
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
    return json.dumps(f, indent=2)


def get_fixture_info() -> Dict:
    """Return fixture registry info."""
    return {
        "count": len(_FIXTURES),
        "fixture_dir": _FIXTURE_DIR,
        "workflow_types": _WORKFLOW_TYPES,
        "paper_only": True,
        "research_only": True,
        "workflow_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "schema_version": "188",
    }
