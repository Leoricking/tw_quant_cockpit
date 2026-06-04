"""stable_release/known_limitations.py — KnownLimitationsRegistry for v0.6.0.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List

logger = logging.getLogger(__name__)

_LIMITATIONS = [
    {
        "id": "LIM-001",
        "name": "No Real-Time Data Feed",
        "category": "data",
        "impact": "HIGH",
        "description": "System uses CSV imports and TWSE public endpoints only. No live streaming.",
        "workaround": "Import XQ/Excel CSV exports manually; use mock-realtime for simulation.",
    },
    {
        "id": "LIM-002",
        "name": "Manual Threshold Tuning",
        "category": "data",
        "impact": "MEDIUM",
        "description": "Data quality gate thresholds require manual configuration per dataset.",
        "workaround": "Review data_quality_gate.md for tuning guidance.",
    },
    {
        "id": "LIM-003",
        "name": "No Live Broker Connection",
        "category": "safety",
        "impact": "HIGH",
        "description": "No Shioaji / Mega broker API connection. All trading is simulated only.",
        "workaround": "This is intentional. Use paper-trading mode for simulation.",
    },
    {
        "id": "LIM-004",
        "name": "Bar Data Requires Manual Import",
        "category": "replay",
        "impact": "MEDIUM",
        "description": "Replay Training requires CSV bar data — no live feed integration.",
        "workaround": "Export intraday bars from XQ/TradingView and place in data/import/.",
    },
    {
        "id": "LIM-005",
        "name": "Rule-Based AI Review Only",
        "category": "replay",
        "impact": "LOW",
        "description": "AI replay review is rule-based (no GPT/LLM). Limited contextual reasoning.",
        "workaround": "Review AI feedback as a starting point; apply trader judgment.",
    },
    {
        "id": "LIM-006",
        "name": "Universe Size (~14-50 symbols)",
        "category": "data",
        "impact": "MEDIUM",
        "description": "Current universe is limited. Signals may not generalize to full TWSE/TPEX.",
        "workaround": "Expand universe using universe-manage and import-csv commands.",
    },
    {
        "id": "LIM-007",
        "name": "Strategy Filter Criteria Manually Defined",
        "category": "strategy",
        "impact": "MEDIUM",
        "description": "Financial turnaround filter weights are manually coded; no ML optimization.",
        "workaround": "Use rule-weight-tuning CLI to experiment with weight adjustments.",
    },
    {
        "id": "LIM-008",
        "name": "Walk-Forward Windows Not Auto-Tuned",
        "category": "backtest",
        "impact": "MEDIUM",
        "description": "Backtest walk-forward window sizes require manual configuration.",
        "workaround": "Refer to backtest_engine_hardening.md for window selection guidance.",
    },
    {
        "id": "LIM-009",
        "name": "No Multi-Currency Support",
        "category": "portfolio",
        "impact": "LOW",
        "description": "Portfolio simulation uses TWD only; no FX conversion.",
        "workaround": "Convert to TWD before input; planned for v0.7.x.",
    },
    {
        "id": "LIM-010",
        "name": "Leakage Detection Is Heuristic",
        "category": "data",
        "impact": "MEDIUM",
        "description": "Leakage guard uses heuristic column checks; not exhaustive causal analysis.",
        "workaround": "Manually review feature timestamps against label lookahead windows.",
    },
    {
        "id": "LIM-011",
        "name": "PySide6 Required for GUI",
        "category": "gui",
        "impact": "LOW",
        "description": "GUI dashboard requires PySide6. CLI works without GUI dependencies.",
        "workaround": "pip install PySide6. All features available via CLI without GUI.",
    },
]


class KnownLimitationsRegistry:
    """Registry of known limitations for v0.6.0.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    VERSION = "v0.6.0"

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def list_limitations(self) -> List[dict]:
        """Return all known limitations."""
        lims = list(_LIMITATIONS)
        print("=" * 60)
        print("  TW Quant Cockpit — Research OS Stable Release v0.6.0")
        print("  [!] Research Only | No Real Orders | Production BLOCKED")
        print("=" * 60)
        print(f"  Known Limitations ({len(lims)} total)")
        print()
        for lim in lims:
            print(f"  [{lim['id']}] {lim['name']}")
            print(f"    Category : {lim['category']}")
            print(f"    Impact   : {lim['impact']}")
            print(f"    Detail   : {lim['description']}")
            print(f"    Workaround: {lim['workaround']}")
            print()
        print("=" * 60)
        return lims

    def build_table(self) -> str:
        """Return a Markdown table of known limitations."""
        lines = [
            "| ID | Name | Category | Impact | Workaround |",
            "|-----|------|----------|--------|------------|",
        ]
        for lim in _LIMITATIONS:
            lines.append(
                f"| {lim['id']} | {lim['name']} | {lim['category']} "
                f"| {lim['impact']} | {lim['workaround']} |"
            )
        return "\n".join(lines)
