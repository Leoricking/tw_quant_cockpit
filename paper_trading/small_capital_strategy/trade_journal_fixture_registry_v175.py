"""
paper_trading/small_capital_strategy/trade_journal_fixture_registry_v175.py
Fixture registry for Small Account Trade Journal v1.7.5.
55+ JSON fixtures. All paper/research only.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.trade_journal_fixture_schema_v175 import validate_fixture

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"
_LINEAGE = "paper_trading.small_capital_strategy.trade_journal_fixture_registry_v175"

MIN_FIXTURES = 55


def _f(fid, symbol, direction, entry_date, exit_date, entry_price, exit_price,
       outcome, abc_pattern, market_regime, watchlist_tier, mistakes):
    return {
        "id":                 fid,
        "symbol":             symbol,
        "direction":          direction,
        "entry_date":         entry_date,
        "exit_date":          exit_date,
        "entry_price":        entry_price,
        "exit_price":         exit_price,
        "outcome":            outcome,
        "abc_pattern":        abc_pattern,
        "market_regime":      market_regime,
        "watchlist_tier":     watchlist_tier,
        "mistake_categories": mistakes,
        "paper_only":         True,
        "research_only":      True,
        "no_real_orders":     True,
        "no_broker":          True,
        "not_investment_advice": True,
        "demo_only":          True,
        "not_for_production": True,
        "schema_version":     _SCHEMA,
        "policy_version":     _POLICY,
        "source_lineage":     _LINEAGE,
    }


FIXTURES: List[Dict[str, Any]] = [
    # --- WIN fixtures: BULL regime, B_BREAKOUT / C_RECLAIM (15) ---
    _f("F175-001","2330","LONG","2026-01-05","2026-01-20",580.0,638.0,
       "WIN","B_BREAKOUT","BULL",1,["NONE"]),
    _f("F175-002","2317","LONG","2026-01-06","2026-01-22",95.0,106.0,
       "WIN","C_RECLAIM","BULL",1,["NONE"]),
    _f("F175-003","2454","LONG","2026-01-07","2026-01-25",185.0,205.0,
       "WIN","B_BREAKOUT","BULL",2,["NONE"]),
    _f("F175-004","2382","LONG","2026-01-08","2026-02-01",220.0,245.0,
       "WIN","C_RECLAIM","BULL",1,["NONE"]),
    _f("F175-005","3711","LONG","2026-01-09","2026-02-05",305.0,340.0,
       "WIN","B_BREAKOUT","BULL",2,["NONE"]),
    _f("F175-006","2412","LONG","2026-01-10","2026-02-10",75.0,84.0,
       "WIN","C_RECLAIM","BULL",1,["NONE"]),
    _f("F175-007","2308","LONG","2026-01-12","2026-02-12",46.0,52.0,
       "WIN","A_PULLBACK","BULL",2,["NONE"]),
    _f("F175-008","2303","LONG","2026-01-13","2026-02-14",68.0,77.0,
       "WIN","B_BREAKOUT","BULL",1,["NONE"]),
    _f("F175-009","2881","LONG","2026-01-14","2026-02-18",26.0,29.5,
       "WIN","C_RECLAIM","BULL",2,["NONE"]),
    _f("F175-010","2886","LONG","2026-01-15","2026-02-20",30.0,34.0,
       "WIN","B_BREAKOUT","BULL",1,["NONE"]),
    _f("F175-011","2891","LONG","2026-01-16","2026-02-22",25.0,28.0,
       "WIN","C_RECLAIM","BULL",2,["NONE"]),
    _f("F175-012","5871","LONG","2026-01-17","2026-02-25",415.0,460.0,
       "WIN","B_BREAKOUT","BULL",1,["NONE"]),
    _f("F175-013","2395","LONG","2026-01-19","2026-02-28",540.0,600.0,
       "WIN","C_RECLAIM","BULL",1,["NONE"]),
    _f("F175-014","3034","LONG","2026-01-20","2026-03-01",180.0,200.0,
       "WIN","B_BREAKOUT","BULL",2,["NONE"]),
    _f("F175-015","2357","LONG","2026-01-21","2026-03-03",285.0,318.0,
       "WIN","C_RECLAIM","BULL",1,["NONE"]),

    # --- LOSS fixtures: various mistakes (15) ---
    _f("F175-016","2330","LONG","2026-02-01","2026-02-15",600.0,540.0,
       "LOSS","UNKNOWN","BEAR",0,["FOMO","REGIME_MISMATCH"]),
    _f("F175-017","2317","LONG","2026-02-02","2026-02-16",100.0,88.0,
       "LOSS","UNKNOWN","RISK_OFF",0,["FOMO","REGIME_MISMATCH","NO_STOP_LOSS"]),
    _f("F175-018","2454","LONG","2026-02-03","2026-02-18",190.0,170.0,
       "LOSS","UNKNOWN","BEAR",0,["HELD_LOSER","REGIME_MISMATCH"]),
    _f("F175-019","2382","LONG","2026-02-04","2026-02-20",230.0,200.0,
       "LOSS","B_BREAKOUT","BULL",0,["WATCHLIST_MISS","OVERSIZE"]),
    _f("F175-020","3711","LONG","2026-02-05","2026-02-22",310.0,278.0,
       "LOSS","UNKNOWN","RANGE",2,["CHASED_BREAKOUT"]),
    _f("F175-021","2412","LONG","2026-02-06","2026-02-24",78.0,68.0,
       "LOSS","UNKNOWN","BEAR",0,["REVENGE","REGIME_MISMATCH"]),
    _f("F175-022","2308","LONG","2026-02-07","2026-02-26",48.0,42.0,
       "LOSS","UNKNOWN","RISK_OFF",0,["FOMO","NO_STOP_LOSS","REGIME_MISMATCH"]),
    _f("F175-023","2303","LONG","2026-02-08","2026-02-28",70.0,61.0,
       "LOSS","B_BREAKOUT","BEAR",0,["REGIME_MISMATCH","HELD_LOSER"]),
    _f("F175-024","2881","LONG","2026-02-09","2026-03-02",27.0,23.5,
       "LOSS","UNKNOWN","RISK_OFF",0,["FOMO","REGIME_MISMATCH"]),
    _f("F175-025","2886","LONG","2026-02-10","2026-03-04",31.0,27.0,
       "LOSS","UNKNOWN","BEAR",0,["NO_STOP_LOSS","HELD_LOSER"]),
    _f("F175-026","2891","LONG","2026-02-11","2026-03-06",26.0,22.5,
       "LOSS","UNKNOWN","RISK_OFF",0,["REGIME_MISMATCH","OVERSIZE"]),
    _f("F175-027","5871","LONG","2026-02-12","2026-03-08",420.0,370.0,
       "LOSS","UNKNOWN","BEAR",0,["FOMO","REGIME_MISMATCH","HELD_LOSER"]),
    _f("F175-028","2395","LONG","2026-02-13","2026-03-10",550.0,490.0,
       "LOSS","B_BREAKOUT","BEAR",1,["REGIME_MISMATCH"]),
    _f("F175-029","3034","LONG","2026-02-14","2026-03-12",185.0,162.0,
       "LOSS","UNKNOWN","RISK_OFF",0,["FOMO","NO_STOP_LOSS"]),
    _f("F175-030","2357","LONG","2026-02-15","2026-03-14",290.0,255.0,
       "LOSS","A_PULLBACK","BULL",0,["WATCHLIST_MISS"]),

    # --- RANGE regime: mixed outcomes (8) ---
    _f("F175-031","2330","LONG","2026-03-01","2026-03-15",590.0,620.0,
       "WIN","C_RECLAIM","RANGE",1,["NONE"]),
    _f("F175-032","2317","LONG","2026-03-02","2026-03-16",97.0,105.0,
       "WIN","B_BREAKOUT","RANGE",2,["NONE"]),
    _f("F175-033","2454","LONG","2026-03-03","2026-03-17",188.0,196.0,
       "WIN","C_RECLAIM","RANGE",1,["EARLY_EXIT"]),
    _f("F175-034","2382","LONG","2026-03-04","2026-03-18",225.0,218.0,
       "LOSS","A_PULLBACK","RANGE",2,["CHASED_BREAKOUT"]),
    _f("F175-035","3711","LONG","2026-03-05","2026-03-19",308.0,315.0,
       "WIN","B_BREAKOUT","RANGE",1,["NONE"]),
    _f("F175-036","2412","LONG","2026-03-06","2026-03-20",76.0,72.0,
       "LOSS","UNKNOWN","RANGE",0,["FOMO","WATCHLIST_MISS"]),
    _f("F175-037","2308","LONG","2026-03-07","2026-03-21",47.0,50.0,
       "WIN","C_RECLAIM","RANGE",2,["NONE"]),
    _f("F175-038","2303","LONG","2026-03-08","2026-03-22",69.0,65.0,
       "LOSS","B_BREAKOUT","RANGE",1,["EARLY_EXIT"]),

    # --- Breakeven fixtures (4) ---
    _f("F175-039","2330","LONG","2026-04-01","2026-04-10",595.0,595.0,
       "BREAKEVEN","A_PULLBACK","BULL",1,["EARLY_EXIT"]),
    _f("F175-040","2317","LONG","2026-04-02","2026-04-11",98.0,98.0,
       "BREAKEVEN","B_BREAKOUT","RANGE",2,["NONE"]),
    _f("F175-041","2454","LONG","2026-04-03","2026-04-12",187.0,187.0,
       "BREAKEVEN","C_RECLAIM","BULL",1,["NONE"]),
    _f("F175-042","2382","LONG","2026-04-04","2026-04-13",222.0,222.0,
       "BREAKEVEN","UNKNOWN","RANGE",0,["WATCHLIST_MISS"]),

    # --- Open positions (5) ---
    _f("F175-043","2330","LONG","2026-05-01","",580.0,0.0,
       "OPEN","C_RECLAIM","BULL",1,["NONE"]),
    _f("F175-044","2317","LONG","2026-05-02","",96.0,0.0,
       "OPEN","B_BREAKOUT","BULL",2,["NONE"]),
    _f("F175-045","2454","LONG","2026-05-03","",186.0,0.0,
       "OPEN","A_PULLBACK","RANGE",1,["NONE"]),
    _f("F175-046","2382","LONG","2026-05-04","",221.0,0.0,
       "OPEN","C_RECLAIM","BULL",1,["NONE"]),
    _f("F175-047","3711","LONG","2026-05-05","",304.0,0.0,
       "OPEN","B_BREAKOUT","BULL",2,["NONE"]),

    # --- Cancelled fixtures (3) ---
    _f("F175-048","2412","LONG","2026-05-06","2026-05-06",77.0,0.0,
       "OPEN","UNKNOWN","RISK_OFF",0,["REGIME_MISMATCH"]),
    _f("F175-049","2308","LONG","2026-05-07","2026-05-07",46.5,0.0,
       "OPEN","UNKNOWN","BEAR",0,["REGIME_MISMATCH"]),
    _f("F175-050","2303","LONG","2026-05-08","2026-05-08",67.5,0.0,
       "OPEN","UNKNOWN","RISK_OFF",0,["REGIME_MISMATCH"]),

    # --- Additional compliance fixtures (5) ---
    _f("F175-051","2330","LONG","2026-06-01","2026-06-15",600.0,666.0,
       "WIN","C_RECLAIM","BULL",1,["NONE"]),
    _f("F175-052","2317","LONG","2026-06-02","2026-06-16",99.0,110.0,
       "WIN","B_BREAKOUT","BULL",1,["NONE"]),
    _f("F175-053","2454","LONG","2026-06-03","2026-06-17",192.0,213.0,
       "WIN","C_RECLAIM","BULL",2,["NONE"]),
    _f("F175-054","2382","LONG","2026-06-04","2026-06-18",228.0,253.0,
       "WIN","B_BREAKOUT","BULL",1,["NONE"]),
    _f("F175-055","3711","LONG","2026-06-05","2026-06-19",312.0,347.0,
       "WIN","C_RECLAIM","BULL",1,["NONE"]),
]


def get_fixtures() -> List[Dict[str, Any]]:
    """Return all fixtures."""
    return list(FIXTURES)


def get_fixture_by_id(fid: str) -> Optional[Dict[str, Any]]:
    """Return fixture by id, or None."""
    for f in FIXTURES:
        if f["id"] == fid:
            return f
    return None


def count_fixtures() -> int:
    """Return total number of fixtures."""
    return len(FIXTURES)


def validate_registry() -> Dict[str, Any]:
    """Validate all fixtures. Returns {valid, errors}."""
    errors = []
    for f in FIXTURES:
        if not validate_fixture(f):
            errors.append(f"invalid_fixture:{f.get('id', 'unknown')}")
    return {"valid": len(errors) == 0, "errors": errors}
