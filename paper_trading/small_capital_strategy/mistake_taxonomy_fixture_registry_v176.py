"""
paper_trading/small_capital_strategy/mistake_taxonomy_fixture_registry_v176.py
Fixture registry for Mistake Taxonomy & Weekly Review Dashboard v1.7.6.
60+ JSON-compatible fixtures. All paper_only / research_only / no_real_orders.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.mistake_taxonomy_fixture_schema_v176 import (
    validate_all_fixtures,
)

_SCHEMA  = "176"
_POLICY  = "1.7.6-mistake-taxonomy-weekly-review"
_LINEAGE = "paper_trading.small_capital_strategy.mistake_taxonomy_fixture_registry_v176"


def _f(
    fid: str,
    symbol: str,
    trade_date: str,
    category: str,
    severity: str,
    cost_twd: float,
    week_label: str,
    outcome: str = "LOSS",
) -> Dict[str, Any]:
    return {
        "id": fid,
        "symbol": symbol,
        "trade_date": trade_date,
        "mistake_category": category,
        "severity": severity,
        "cost_twd": cost_twd,
        "week_label": week_label,
        "outcome": outcome,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
        "source_lineage": _LINEAGE,
    }


_FIXTURES: List[Dict[str, Any]] = [
    # NO_STOP_LOSS fixtures — week 2026-W01
    _f("F176-001", "2330", "2026-01-05", "NO_STOP_LOSS", "HIGH", -8000.0, "2026-W01"),
    _f("F176-002", "2317", "2026-01-06", "NO_STOP_LOSS", "HIGH", -5000.0, "2026-W01"),
    _f("F176-003", "2454", "2026-01-07", "NO_STOP_LOSS", "HIGH", -3500.0, "2026-W01"),

    # MOVED_STOP_LOSS fixtures — week 2026-W01
    _f("F176-004", "2382", "2026-01-05", "MOVED_STOP_LOSS", "HIGH", -9000.0, "2026-W01"),
    _f("F176-005", "3711", "2026-01-06", "MOVED_STOP_LOSS", "HIGH", -6000.0, "2026-W01"),

    # OVERSIZED_POSITION fixtures — week 2026-W01
    _f("F176-006", "2412", "2026-01-07", "OVERSIZED_POSITION", "HIGH", -4000.0, "2026-W01"),
    _f("F176-007", "2308", "2026-01-08", "OVERSIZED_POSITION", "HIGH", -7000.0, "2026-W01"),

    # IGNORE_MARKET_REGIME fixtures — week 2026-W02
    _f("F176-008", "2330", "2026-01-12", "IGNORE_MARKET_REGIME", "CRITICAL", -12000.0, "2026-W02"),
    _f("F176-009", "2317", "2026-01-13", "IGNORE_MARKET_REGIME", "CRITICAL", -9500.0, "2026-W02"),
    _f("F176-010", "2454", "2026-01-14", "IGNORE_MARKET_REGIME", "CRITICAL", -8000.0, "2026-W02"),

    # REVENGE_TRADE fixtures — week 2026-W02
    _f("F176-011", "2382", "2026-01-12", "REVENGE_TRADE", "CRITICAL", -11000.0, "2026-W02"),
    _f("F176-012", "3711", "2026-01-13", "REVENGE_TRADE", "CRITICAL", -8500.0, "2026-W02"),
    _f("F176-013", "2412", "2026-01-14", "REVENGE_TRADE", "CRITICAL", -7000.0, "2026-W02"),

    # FOMO_CHASE fixtures — week 2026-W03
    _f("F176-014", "2308", "2026-01-19", "FOMO_CHASE", "MEDIUM", -3000.0, "2026-W03"),
    _f("F176-015", "2330", "2026-01-20", "FOMO_CHASE", "MEDIUM", -2500.0, "2026-W03"),
    _f("F176-016", "2317", "2026-01-21", "FOMO_CHASE", "MEDIUM", -2000.0, "2026-W03"),

    # HOLD_LOSER_TOO_LONG fixtures — week 2026-W03
    _f("F176-017", "2454", "2026-01-19", "HOLD_LOSER_TOO_LONG", "HIGH", -15000.0, "2026-W03"),
    _f("F176-018", "2382", "2026-01-20", "HOLD_LOSER_TOO_LONG", "HIGH", -12000.0, "2026-W03"),

    # IGNORE_ABC_PLAN fixtures — week 2026-W03
    _f("F176-019", "3711", "2026-01-21", "IGNORE_ABC_PLAN", "HIGH", -5000.0, "2026-W03"),
    _f("F176-020", "2412", "2026-01-22", "IGNORE_ABC_PLAN", "HIGH", -4000.0, "2026-W03"),

    # OVERTRADING fixtures — week 2026-W04
    _f("F176-021", "2308", "2026-01-26", "OVERTRADING", "MEDIUM", -1000.0, "2026-W04"),
    _f("F176-022", "2330", "2026-01-27", "OVERTRADING", "MEDIUM", -800.0, "2026-W04"),
    _f("F176-023", "2317", "2026-01-28", "OVERTRADING", "MEDIUM", -600.0, "2026-W04"),
    _f("F176-024", "2454", "2026-01-29", "OVERTRADING", "MEDIUM", -400.0, "2026-W04"),

    # MARGIN_OR_LEVERAGE_ATTEMPT — week 2026-W04
    _f("F176-025", "2382", "2026-01-26", "MARGIN_OR_LEVERAGE_ATTEMPT", "BLOCKING", 0.0, "2026-W04"),
    _f("F176-026", "3711", "2026-01-27", "MARGIN_OR_LEVERAGE_ATTEMPT", "BLOCKING", 0.0, "2026-W04"),

    # BROKER_OR_REAL_ORDER_ATTEMPT — week 2026-W05
    _f("F176-027", "2412", "2026-02-02", "BROKER_OR_REAL_ORDER_ATTEMPT", "BLOCKING", 0.0, "2026-W05"),
    _f("F176-028", "2308", "2026-02-03", "BROKER_OR_REAL_ORDER_ATTEMPT", "BLOCKING", 0.0, "2026-W05"),

    # EARLY_ENTRY fixtures — week 2026-W05
    _f("F176-029", "2330", "2026-02-02", "EARLY_ENTRY", "LOW", -1500.0, "2026-W05"),
    _f("F176-030", "2317", "2026-02-03", "EARLY_ENTRY", "LOW", -1200.0, "2026-W05"),

    # LATE_ENTRY fixtures — week 2026-W05
    _f("F176-031", "2454", "2026-02-04", "LATE_ENTRY", "LOW", -2500.0, "2026-W05"),
    _f("F176-032", "2382", "2026-02-05", "LATE_ENTRY", "LOW", -2000.0, "2026-W05"),

    # TAKE_PROFIT_TOO_EARLY fixtures — week 2026-W06
    _f("F176-033", "3711", "2026-02-09", "TAKE_PROFIT_TOO_EARLY", "LOW", 1000.0, "2026-W06", "WIN"),
    _f("F176-034", "2412", "2026-02-10", "TAKE_PROFIT_TOO_EARLY", "LOW", 800.0, "2026-W06", "WIN"),

    # IGNORE_WATCHLIST_RANK fixtures — week 2026-W06
    _f("F176-035", "2308", "2026-02-09", "IGNORE_WATCHLIST_RANK", "MEDIUM", -3000.0, "2026-W06"),
    _f("F176-036", "2330", "2026-02-10", "IGNORE_WATCHLIST_RANK", "MEDIUM", -2500.0, "2026-W06"),

    # NEWS_CHASE fixtures — week 2026-W06
    _f("F176-037", "2317", "2026-02-11", "NEWS_CHASE", "MEDIUM", -4000.0, "2026-W06"),
    _f("F176-038", "2454", "2026-02-12", "NEWS_CHASE", "MEDIUM", -3500.0, "2026-W06"),

    # EARNINGS_RISK_IGNORED fixtures — week 2026-W07
    _f("F176-039", "2382", "2026-02-16", "EARNINGS_RISK_IGNORED", "HIGH", -8000.0, "2026-W07"),
    _f("F176-040", "3711", "2026-02-17", "EARNINGS_RISK_IGNORED", "HIGH", -6500.0, "2026-W07"),

    # Clean week fixtures (no mistake) — week 2026-W07
    _f("F176-041", "2412", "2026-02-16", "NONE", "INFO", 3000.0, "2026-W07", "WIN"),
    _f("F176-042", "2308", "2026-02-17", "NONE", "INFO", 4000.0, "2026-W07", "WIN"),

    # Repeated NO_STOP_LOSS (5x in one week) — week 2026-W08
    _f("F176-043", "2330", "2026-02-23", "NO_STOP_LOSS", "HIGH", -4000.0, "2026-W08"),
    _f("F176-044", "2317", "2026-02-24", "NO_STOP_LOSS", "HIGH", -4000.0, "2026-W08"),
    _f("F176-045", "2454", "2026-02-25", "NO_STOP_LOSS", "HIGH", -4000.0, "2026-W08"),
    _f("F176-046", "2382", "2026-02-26", "NO_STOP_LOSS", "HIGH", -4000.0, "2026-W08"),
    _f("F176-047", "3711", "2026-02-27", "NO_STOP_LOSS", "HIGH", -4000.0, "2026-W08"),

    # OVERSIZED + REVENGE combo — week 2026-W08
    _f("F176-048", "2412", "2026-02-23", "OVERSIZED_POSITION", "HIGH", -10000.0, "2026-W08"),
    _f("F176-049", "2308", "2026-02-24", "REVENGE_TRADE", "CRITICAL", -8000.0, "2026-W08"),

    # IGNORE_MARKET_REGIME × 3 — week 2026-W09
    _f("F176-050", "2330", "2026-03-02", "IGNORE_MARKET_REGIME", "CRITICAL", -9000.0, "2026-W09"),
    _f("F176-051", "2317", "2026-03-03", "IGNORE_MARKET_REGIME", "CRITICAL", -9000.0, "2026-W09"),
    _f("F176-052", "2454", "2026-03-04", "IGNORE_MARKET_REGIME", "CRITICAL", -9000.0, "2026-W09"),

    # Mixed good/bad week — week 2026-W09
    _f("F176-053", "2382", "2026-03-02", "NONE", "INFO", 5000.0, "2026-W09", "WIN"),
    _f("F176-054", "3711", "2026-03-03", "FOMO_CHASE", "MEDIUM", -2500.0, "2026-W09"),

    # HOLD_LOSER × 3 — week 2026-W10
    _f("F176-055", "2412", "2026-03-09", "HOLD_LOSER_TOO_LONG", "HIGH", -12000.0, "2026-W10"),
    _f("F176-056", "2308", "2026-03-10", "HOLD_LOSER_TOO_LONG", "HIGH", -10000.0, "2026-W10"),
    _f("F176-057", "2330", "2026-03-11", "HOLD_LOSER_TOO_LONG", "HIGH", -8000.0, "2026-W10"),

    # Perfect week — 3 trades, 0 mistakes — week 2026-W10
    _f("F176-058", "2317", "2026-03-09", "NONE", "INFO", 6000.0, "2026-W10", "WIN"),
    _f("F176-059", "2454", "2026-03-10", "NONE", "INFO", 5500.0, "2026-W10", "WIN"),
    _f("F176-060", "2382", "2026-03-11", "NONE", "INFO", 4500.0, "2026-W10", "WIN"),
]


def get_fixtures() -> List[Dict[str, Any]]:
    """Return all v1.7.6 fixtures."""
    return list(_FIXTURES)


def count_fixtures() -> int:
    """Return total fixture count."""
    return len(_FIXTURES)


def validate_registry() -> Dict[str, Any]:
    """Validate all fixtures in the registry."""
    return validate_all_fixtures(_FIXTURES)


def get_fixtures_by_week(week_label: str) -> List[Dict[str, Any]]:
    """Return fixtures for a specific week label."""
    return [f for f in _FIXTURES if f["week_label"] == week_label]


def get_fixtures_by_category(category: str) -> List[Dict[str, Any]]:
    """Return fixtures for a specific mistake category."""
    return [f for f in _FIXTURES if f["mistake_category"] == category]
