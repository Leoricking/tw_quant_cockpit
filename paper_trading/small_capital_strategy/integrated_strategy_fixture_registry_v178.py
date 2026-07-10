"""
paper_trading/small_capital_strategy/integrated_strategy_fixture_registry_v178.py
Fixture registry for Small Capital Strategy Integration v1.7.8. 70 fixtures.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "178"
_POLICY  = "1.7.8-small-capital-strategy-integration"

_SAFETY = {
    "paper_only": True, "research_only": True, "no_real_orders": True,
    "no_broker": True, "not_investment_advice": True,
    "demo_only": True, "not_for_production": True,
}


def _f(fid: str, name: str, action: str, **kw) -> Dict[str, Any]:
    d = {
        "fixture_id": fid, "name": name, "expected_action": action,
        "schema_version": _SCHEMA, "policy_version": _POLICY,
    }
    d.update(_SAFETY)
    d.update(kw)
    return d


_FIXTURES: List[Dict[str, Any]] = [
    # ── PAPER_ENTRY_ALLOWED (10) ─────────────────────────────────────────────
    _f("FX178-001", "Bull/Leader/Focus/A_Ready – Entry", "PAPER_ENTRY_ALLOWED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, final_score=88.0),
    _f("FX178-002", "Bull/Leader/Focus/B_Ready – Entry", "PAPER_ENTRY_ALLOWED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="B_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, final_score=85.0),
    _f("FX178-003", "Bull/Leader/Focus/C_Ready – Entry", "PAPER_ENTRY_ALLOWED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="C_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, final_score=82.0),
    _f("FX178-004", "Bull/Strong/Focus/A_Ready – Entry", "PAPER_ENTRY_ALLOWED",
       regime="BULL", theme="STRONG", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, final_score=80.0),
    _f("FX178-005", "BullSoft/Leader/Focus/A_Ready – Entry", "PAPER_ENTRY_ALLOWED",
       regime="BULL_SOFT", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, final_score=78.0),
    _f("FX178-006", "Bull/Leader/Focus/A_Ready + journal 90 – Entry", "PAPER_ENTRY_ALLOWED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       journal_quality_score=90.0, final_score=86.0),
    _f("FX178-007", "Bull/Leader/Focus/B_Ready + journal 85 – Entry", "PAPER_ENTRY_ALLOWED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="B_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       journal_quality_score=85.0, final_score=84.0),
    _f("FX178-008", "Bull/Strong/Focus/B_Ready – Entry", "PAPER_ENTRY_ALLOWED",
       regime="BULL", theme="STRONG", watchlist="FOCUS", abc="B_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, final_score=79.0),
    _f("FX178-009", "Bull/Leader/Focus/C_Ready + high behavior – Entry", "PAPER_ENTRY_ALLOWED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="C_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       behavior_score=95.0, final_score=81.0),
    _f("FX178-010", "BullSoft/Strong/Focus/A_Ready – Entry", "PAPER_ENTRY_ALLOWED",
       regime="BULL_SOFT", theme="STRONG", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, final_score=76.0),
    # ── PAPER_PLAN_READY (10) ────────────────────────────────────────────────
    _f("FX178-011", "Bull/Strong/Watch/B_Ready – Plan", "PAPER_PLAN_READY",
       regime="BULL", theme="STRONG", watchlist="WATCH", abc="B_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, final_score=68.0),
    _f("FX178-012", "Bull/Leader/Watch/C_Ready – Plan", "PAPER_PLAN_READY",
       regime="BULL", theme="LEADER", watchlist="WATCH", abc="C_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, final_score=70.0),
    _f("FX178-013", "BullSoft/Strong/Focus/B_Ready – Plan", "PAPER_PLAN_READY",
       regime="BULL_SOFT", theme="STRONG", watchlist="FOCUS", abc="B_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, final_score=67.0),
    _f("FX178-014", "Bull/Watch/Focus/A_Ready – Plan", "PAPER_PLAN_READY",
       regime="BULL", theme="WATCH", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       theme_score=70.0, final_score=66.0),
    _f("FX178-015", "Bull/Leader/Focus/NotReady – Plan", "PAPER_PLAN_READY",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       theme_score=95.0, watchlist_score=90.0, abc_score=0.0, final_score=65.0),
    _f("FX178-016", "Neutral/Leader/Focus/A_Ready – Plan", "PAPER_PLAN_READY",
       regime="NEUTRAL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, final_score=66.0),
    _f("FX178-017", "Bull/Leader/Watch/A_Ready – Plan", "PAPER_PLAN_READY",
       regime="BULL", theme="LEADER", watchlist="WATCH", abc="A_READY",
       risk="SAFE", behavior="CAUTION", behavior_score=70.0,
       has_stop_loss=True, final_score=67.0),
    _f("FX178-018", "Bull/Strong/Focus/C_Ready/Moderate – Plan", "PAPER_PLAN_READY",
       regime="BULL", theme="STRONG", watchlist="FOCUS", abc="C_READY",
       risk="MODERATE", behavior="CLEAN", has_stop_loss=True, final_score=65.0),
    _f("FX178-019", "BullSoft/Strong/Watch/A_Ready – Plan", "PAPER_PLAN_READY",
       regime="BULL_SOFT", theme="STRONG", watchlist="WATCH", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, final_score=65.0),
    _f("FX178-020", "Bull/Watch/Focus/B_Ready – Plan", "PAPER_PLAN_READY",
       regime="BULL", theme="WATCH", watchlist="FOCUS", abc="B_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       theme_score=72.0, watchlist_score=90.0, final_score=66.0),
    # ── BLOCKED (15) ─────────────────────────────────────────────────────────
    _f("FX178-021", "No stop loss", "BLOCKED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=False),
    _f("FX178-022", "Real order requested", "BLOCKED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, real_order_requested=True),
    _f("FX178-023", "Broker requested", "BLOCKED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, broker_requested=True),
    _f("FX178-024", "Margin requested", "BLOCKED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, margin_requested=True),
    _f("FX178-025", "RISK_OFF no override", "BLOCKED",
       regime="RISK_OFF", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, regime_safety_override=False),
    _f("FX178-026", "Behavior BLOCKED", "BLOCKED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="BLOCKED", has_stop_loss=True),
    _f("FX178-027", "Risk level BLOCKED", "BLOCKED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="BLOCKED", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-028", "Watchlist EXCLUDED", "BLOCKED",
       regime="BULL", theme="LEADER", watchlist="EXCLUDED", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-029", "Theme EXCLUDED", "BLOCKED",
       regime="BULL", theme="EXCLUDED", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-030", "ABC BLOCKED", "BLOCKED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="BLOCKED",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-031", "Production DB write", "BLOCKED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       production_db_write_attempted=True),
    _f("FX178-032", "No stop + broker", "BLOCKED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=False, broker_requested=True),
    _f("FX178-033", "No stop + margin", "BLOCKED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=False, margin_requested=True),
    _f("FX178-034", "Real order + broker", "BLOCKED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       real_order_requested=True, broker_requested=True),
    _f("FX178-035", "All blocks at once", "BLOCKED",
       regime="RISK_OFF", theme="EXCLUDED", watchlist="EXCLUDED", abc="BLOCKED",
       risk="BLOCKED", behavior="BLOCKED", has_stop_loss=False,
       real_order_requested=True, broker_requested=True, margin_requested=True),
    # ── NO_TRADE (10) ────────────────────────────────────────────────────────
    _f("FX178-036", "Bear regime no override", "NO_TRADE",
       regime="BEAR", theme="WATCH", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-037", "Theme WEAK low score", "NO_TRADE",
       regime="BULL", theme="WEAK", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       theme_score=15.0, final_score=20.0),
    _f("FX178-038", "Mistake repeat detected", "NO_TRADE",
       regime="BULL", theme="WEAK", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, mistake_repeat_detected=True),
    _f("FX178-039", "Journal required score 20", "NO_TRADE",
       regime="BULL", theme="WEAK", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       journal_required=True, journal_quality_score=20.0),
    _f("FX178-040", "Unknown theme + NOT_READY", "NO_TRADE",
       regime="BULL", theme="UNKNOWN", watchlist="UNKNOWN", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-041", "Bear + weak + high risk", "NO_TRADE",
       regime="BEAR", theme="WEAK", watchlist="WATCH", abc="NOT_READY",
       risk="HIGH", behavior="WARNING", has_stop_loss=True),
    _f("FX178-042", "Behavior WARNING + low score", "NO_TRADE",
       regime="NEUTRAL", theme="WEAK", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="WARNING", has_stop_loss=True, final_score=25.0),
    _f("FX178-043", "Risk HIGH + weak signals", "NO_TRADE",
       regime="NEUTRAL", theme="WEAK", watchlist="WATCH", abc="NOT_READY",
       risk="HIGH", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-044", "RISK_OFF override + weak theme", "NO_TRADE",
       regime="RISK_OFF", theme="WEAK", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, regime_safety_override=True,
       final_score=20.0),
    _f("FX178-045", "Missing date", "NO_TRADE",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, date=""),
    # ── WAIT (5) ─────────────────────────────────────────────────────────────
    _f("FX178-046", "Bull/Watch/Watch/NotReady", "WAIT",
       regime="BULL", theme="WATCH", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-047", "BullSoft/Watch/Watch/NotReady", "WAIT",
       regime="BULL_SOFT", theme="WATCH", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-048", "Neutral/Strong/Focus/NotReady", "WAIT",
       regime="NEUTRAL", theme="STRONG", watchlist="FOCUS", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-049", "Bull/Watch/Focus/NotReady/Moderate", "WAIT",
       regime="BULL", theme="WATCH", watchlist="FOCUS", abc="NOT_READY",
       risk="MODERATE", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-050", "Neutral/Leader/Watch/NotReady/Caution", "WAIT",
       regime="NEUTRAL", theme="LEADER", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CAUTION", has_stop_loss=True),
    # ── OBSERVE (5) ──────────────────────────────────────────────────────────
    _f("FX178-051", "Neutral/Weak/Watch/NotReady", "OBSERVE",
       regime="NEUTRAL", theme="WEAK", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-052", "Unknown/Watch/Watch/NotReady", "OBSERVE",
       regime="UNKNOWN", theme="WATCH", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-053", "Neutral/Watch/Unknown/NotReady", "OBSERVE",
       regime="NEUTRAL", theme="WATCH", watchlist="UNKNOWN", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-054", "RISK_OFF+override/Weak/Unknown/NotReady", "OBSERVE",
       regime="RISK_OFF", theme="WEAK", watchlist="UNKNOWN", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True, regime_safety_override=True),
    _f("FX178-055", "All unknown", "OBSERVE",
       regime="UNKNOWN", theme="UNKNOWN", watchlist="UNKNOWN", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True),
    # ── REDUCE_RISK (5) ──────────────────────────────────────────────────────
    _f("FX178-056", "Risk HIGH + Bull + Strong + A_Ready", "REDUCE_RISK",
       regime="BULL", theme="STRONG", watchlist="FOCUS", abc="A_READY",
       risk="HIGH", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-057", "Risk HIGH + Bull + Leader + B_Ready", "REDUCE_RISK",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="B_READY",
       risk="HIGH", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-058", "Risk HIGH + Neutral + Watch + B_Ready", "REDUCE_RISK",
       regime="NEUTRAL", theme="WATCH", watchlist="WATCH", abc="B_READY",
       risk="HIGH", behavior="CLEAN", has_stop_loss=True),
    _f("FX178-059", "Risk HIGH + BullSoft + Strong + Caution", "REDUCE_RISK",
       regime="BULL_SOFT", theme="STRONG", watchlist="WATCH", abc="C_READY",
       risk="HIGH", behavior="CAUTION", has_stop_loss=True),
    _f("FX178-060", "Risk HIGH + Bull + Leader + journal 80", "REDUCE_RISK",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="HIGH", behavior="CLEAN", has_stop_loss=True, journal_quality_score=80.0),
    # ── REVIEW_REQUIRED (5) ──────────────────────────────────────────────────
    _f("FX178-061", "Caution + Watch/Watch/NotReady", "REVIEW_REQUIRED",
       regime="BULL", theme="WATCH", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CAUTION", behavior_score=45.0, has_stop_loss=True),
    _f("FX178-062", "Journal required + 35", "REVIEW_REQUIRED",
       regime="BULL", theme="WATCH", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       journal_required=True, journal_quality_score=35.0),
    _f("FX178-063", "Caution + Neutral + Watch/Watch/NotReady", "REVIEW_REQUIRED",
       regime="NEUTRAL", theme="WATCH", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CAUTION", behavior_score=40.0, has_stop_loss=True),
    _f("FX178-064", "Journal 30 + Caution", "REVIEW_REQUIRED",
       regime="NEUTRAL", theme="WATCH", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CAUTION", has_stop_loss=True,
       journal_required=True, journal_quality_score=30.0),
    _f("FX178-065", "Caution + BullSoft + Watch theme", "REVIEW_REQUIRED",
       regime="BULL_SOFT", theme="WATCH", watchlist="WATCH", abc="NOT_READY",
       risk="SAFE", behavior="CAUTION", behavior_score=50.0, has_stop_loss=True),
    # ── PAPER_ADD_ALLOWED (5) ────────────────────────────────────────────────
    _f("FX178-066", "Add signal – Bull/Leader/Focus/B_Ready all high", "PAPER_ADD_ALLOWED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="B_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       theme_score=92.0, watchlist_score=92.0, abc_score=88.0,
       regime_score=90.0, risk_score=90.0, behavior_score=90.0,
       journal_quality_score=85.0, final_score=90.5),
    _f("FX178-067", "Add signal – Bull/Leader/Focus/C_Ready all high", "PAPER_ADD_ALLOWED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="C_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       theme_score=90.0, watchlist_score=90.0, abc_score=85.0,
       regime_score=90.0, risk_score=90.0, behavior_score=90.0,
       journal_quality_score=80.0, final_score=89.0),
    _f("FX178-068", "Add signal – Bull/Strong/Focus/A_Ready all high", "PAPER_ADD_ALLOWED",
       regime="BULL", theme="STRONG", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       theme_score=85.0, watchlist_score=90.0, abc_score=92.0,
       regime_score=88.0, risk_score=92.0, behavior_score=92.0,
       journal_quality_score=90.0, final_score=89.5),
    _f("FX178-069", "Add signal – Bull/Leader/Focus/A_Ready journal 90", "PAPER_ADD_ALLOWED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       theme_score=94.0, watchlist_score=94.0, abc_score=92.0,
       regime_score=90.0, risk_score=94.0, behavior_score=92.0,
       journal_quality_score=90.0, final_score=92.4),
    _f("FX178-070", "Perfect scenario – all 95+", "PAPER_ADD_ALLOWED",
       regime="BULL", theme="LEADER", watchlist="FOCUS", abc="A_READY",
       risk="SAFE", behavior="CLEAN", has_stop_loss=True,
       theme_score=98.0, watchlist_score=98.0, abc_score=96.0,
       regime_score=95.0, risk_score=98.0, behavior_score=96.0,
       journal_quality_score=95.0, final_score=96.9),
]


def get_fixtures() -> List[Dict[str, Any]]:
    """Return all fixtures."""
    return list(_FIXTURES)


def count_fixtures() -> int:
    """Return number of fixtures."""
    return len(_FIXTURES)


def get_fixture_by_id(fixture_id: str) -> Dict[str, Any]:
    """Return a single fixture by ID, or None."""
    for f in _FIXTURES:
        if f["fixture_id"] == fixture_id:
            return f
    return None


def validate_registry() -> Dict[str, Any]:
    """Validate all fixtures have required safety fields."""
    required_keys = [
        "paper_only", "research_only", "no_real_orders",
        "no_broker", "not_investment_advice", "demo_only", "not_for_production",
    ]
    issues = []
    for fx in _FIXTURES:
        for k in required_keys:
            if not fx.get(k):
                issues.append(f"{fx['fixture_id']}: missing {k}")
        if not fx.get("fixture_id"):
            issues.append("Fixture missing fixture_id")
        if not fx.get("expected_action"):
            issues.append(f"{fx.get('fixture_id', '?')}: missing expected_action")
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "count": len(_FIXTURES),
        "paper_only": True,
        "research_only": True,
    }
