"""
paper_trading/small_capital_strategy/watchlist_report_v171.py
Report generator for Watchlist Strategy Layer v1.7.1.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
Output: Markdown | JSON | CSV | Console | GUI model
"""
from __future__ import annotations
import json
import csv
import io
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.watchlist_enums_v171 import WatchlistReportFormat
from paper_trading.small_capital_strategy.watchlist_models_v171 import (
    WatchlistStrategyResult, WatchlistStrategyReport,
)

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"

_DISCLAIMER = (
    "Research Only | Paper Only | No Real Orders | Not Investment Advice"
)

SECTION_NAMES = [
    "watchlist_profile",
    "candidate_pool_summary",
    "theme_rotation",
    "ranking_method",
    "top_10_focus_candidates",
    "top_5_tradable_candidates",
    "tier_classification",
    "excluded_candidates",
    "overdiversification_check",
    "small_capital_fit",
    "v170_allocation_mapping",
    "risk_notes",
    "safety",
    "not_investment_advice",
]


def get_section_names() -> List[str]:
    """Return canonical section names list. Deterministic."""
    return list(SECTION_NAMES)


def _build_sections(result: WatchlistStrategyResult) -> Dict[str, Any]:
    """Build the sections dict from a WatchlistStrategyResult."""
    focus_symbols = [r.candidate.symbol for r in result.top_selection.focus_candidates]
    tradable_symbols = [r.candidate.symbol for r in result.top_selection.tradable_candidates]
    excluded = [c for c in result.candidate_pool.candidates
                if c.watchlist_tier.value == "EXCLUDED"]

    return {
        "watchlist_profile": {
            "profile_id": result.profile_id,
            "total_candidates": result.candidate_pool.total_count,
            "regime": result.regime,
        },
        "candidate_pool_summary": {
            "total": result.candidate_pool.total_count,
            "by_tier": _count_by_tier(result.candidate_pool.candidates),
        },
        "theme_rotation": {
            "note": "theme rotation signals not yet fed — use watchlist-theme command",
        },
        "ranking_method": {
            "sort": "tier_priority desc, total_score desc",
            "paper_only": True,
            "research_only": True,
        },
        "top_10_focus_candidates": {
            "count": len(focus_symbols),
            "symbols": focus_symbols,
            "paper_only": True,
            "research_only": True,
            "not_investment_advice": True,
        },
        "top_5_tradable_candidates": {
            "count": len(tradable_symbols),
            "symbols": tradable_symbols,
            "paper_only": True,
            "research_only": True,
            "not_investment_advice": True,
        },
        "tier_classification": {t.value: 0 for t in __import__(
            "paper_trading.small_capital_strategy.watchlist_enums_v171",
            fromlist=["WatchlistTier"]).WatchlistTier},
        "excluded_candidates": {
            "count": len(excluded),
            "symbols": [c.symbol for c in excluded],
        },
        "overdiversification_check": result.overdiversification.to_dict(),
        "small_capital_fit": {
            "capital_twd": 300_000,
            "max_holdings": 4,
            "training_max_twd": 15_000,
        },
        "v170_allocation_mapping": {
            "CORE": "CORE bucket",
            "MAIN_THEME": "MAIN_THEME_SWING bucket",
            "SECOND_WAVE": "SECOND_WAVE_SETUP bucket",
            "TRAINING": "SHORT_TERM_TRAINING bucket",
            "EXCLUDED": None,
        },
        "risk_notes": [
            "All outputs are research-only",
            "No position sizes implied",
            "Past ranking does not imply future performance",
        ],
        "safety": {
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
            "no_broker": True,
            "no_real_account": True,
        },
        "not_investment_advice": _DISCLAIMER,
    }


def _count_by_tier(candidates) -> Dict[str, int]:
    """Count candidates by tier."""
    counts: Dict[str, int] = {}
    for c in candidates:
        key = c.watchlist_tier.value
        counts[key] = counts.get(key, 0) + 1
    return counts


def build_watchlist_report(
    result: WatchlistStrategyResult,
    fmt: WatchlistReportFormat = WatchlistReportFormat.MARKDOWN,
) -> WatchlistStrategyReport:
    """Build a WatchlistStrategyReport from a WatchlistStrategyResult."""
    sections = _build_sections(result)
    return WatchlistStrategyReport(
        profile_id=result.profile_id,
        sections=sections,
        format=fmt,
        schema_version=_SCHEMA,
        policy_version=_POLICY,
        source_lineage=_LINEAGE,
        paper_only=True,
        research_only=True,
        no_real_orders=True,
        not_investment_advice=True,
    )


def report_to_markdown(report: WatchlistStrategyReport) -> str:
    """Render report as Markdown string."""
    lines = [
        f"# Watchlist Strategy Layer v1.7.1",
        f"",
        f"> {_DISCLAIMER}",
        f"",
        f"## Profile",
        f"- Profile ID: {report.profile_id}",
        f"- Total candidates: {report.sections.get('watchlist_profile', {}).get('total_candidates', 0)}",
        f"- Regime: {report.sections.get('watchlist_profile', {}).get('regime', 'UNKNOWN')}",
        f"",
        f"## Top 10 Focus Candidates",
    ]
    focus = report.sections.get("top_10_focus_candidates", {})
    for i, sym in enumerate(focus.get("symbols", []), 1):
        lines.append(f"{i}. {sym}")
    lines += [
        f"",
        f"## Top 5 Tradable Candidates",
    ]
    tradable = report.sections.get("top_5_tradable_candidates", {})
    for i, sym in enumerate(tradable.get("symbols", []), 1):
        lines.append(f"{i}. {sym}")
    lines += [
        f"",
        f"## Overdiversification",
        f"Status: {report.sections.get('overdiversification_check', {}).get('status', 'N/A')}",
        f"",
        f"---",
        f"*{_DISCLAIMER}*",
    ]
    return "\n".join(lines)


def report_to_json(report: WatchlistStrategyReport) -> str:
    """Render report as JSON string."""
    return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)


def report_to_csv(report: WatchlistStrategyReport) -> str:
    """Render top candidates as CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["rank", "symbol", "list_type", "paper_only", "not_investment_advice"])
    for i, sym in enumerate(
        report.sections.get("top_10_focus_candidates", {}).get("symbols", []), 1
    ):
        writer.writerow([i, sym, "focus", True, True])
    for i, sym in enumerate(
        report.sections.get("top_5_tradable_candidates", {}).get("symbols", []), 1
    ):
        writer.writerow([i, sym, "tradable", True, True])
    return output.getvalue()


def report_console_summary(report: WatchlistStrategyReport) -> str:
    """Return short console summary string."""
    total = report.sections.get("watchlist_profile", {}).get("total_candidates", 0)
    focus_count = report.sections.get("top_10_focus_candidates", {}).get("count", 0)
    tradable_count = report.sections.get("top_5_tradable_candidates", {}).get("count", 0)
    return (
        f"[Watchlist v1.7.1] total={total} focus={focus_count} tradable={tradable_count} "
        f"| {_DISCLAIMER}"
    )
