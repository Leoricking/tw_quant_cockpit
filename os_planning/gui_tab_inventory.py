"""
os_planning/gui_tab_inventory.py — GUITabInventoryBuilder (v0.5.0).

Inventories all GUI tabs in TW Quant Cockpit and suggests logical grouping
for the v0.5.0 collapsible tab-group refactor.

[!] OS Planning Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# Hardcoded GUI tab inventory — all ~32 current tabs
# ---------------------------------------------------------------------------

_TABS: list[dict] = [
    # ── Group G — Core (always visible) ────────────────────────────────────
    {
        "tab_name":        "Details",
        "suggested_group": "G - Core",
        "purpose":         "Single-stock detail view — price, fundamentals, indicators",
        "priority":        "HIGH",
        "risk_if_hidden":  "Primary research view; must always be accessible",
    },
    {
        "tab_name":        "Strategy",
        "suggested_group": "G - Core",
        "purpose":         "Strategy signal scoring and rule output for selected stock",
        "priority":        "HIGH",
        "risk_if_hidden":  "Core research output; must always be accessible",
    },
    {
        "tab_name":        "Order Book",
        "suggested_group": "G - Core",
        "purpose":         "Simulated order book visualization (mock only)",
        "priority":        "HIGH",
        "risk_if_hidden":  "Used for paper/mock sessions; should always show",
    },
    {
        "tab_name":        "Scoring",
        "suggested_group": "G - Core",
        "purpose":         "Composite rule/signal scoring dashboard",
        "priority":        "HIGH",
        "risk_if_hidden":  "Core scoring is primary workflow output",
    },
    {
        "tab_name":        "Positions",
        "suggested_group": "G - Core",
        "purpose":         "Current simulated portfolio positions",
        "priority":        "HIGH",
        "risk_if_hidden":  "Needed for paper trading sessions",
    },
    # ── Group A — Daily Research ────────────────────────────────────────────
    {
        "tab_name":        "Daily Workflow",
        "suggested_group": "A - Daily Research",
        "purpose":         "Run and view daily research pipeline checklist",
        "priority":        "HIGH",
        "risk_if_hidden":  "Primary starting point for daily routine",
    },
    {
        "tab_name":        "Auto Report Center",
        "suggested_group": "A - Daily Research",
        "purpose":         "Generate and view all auto-generated research reports",
        "priority":        "HIGH",
        "risk_if_hidden":  "Report hub — loss of discoverability if hidden",
    },
    {
        "tab_name":        "Research Workflow",
        "suggested_group": "A - Daily Research",
        "purpose":         "Build and execute research workflow automations",
        "priority":        "HIGH",
        "risk_if_hidden":  "New in v0.4.9; key productivity tab",
    },
    {
        "tab_name":        "Research Coach",
        "suggested_group": "A - Daily Research",
        "purpose":         "Research assistant / coaching checklist and recommendations",
        "priority":        "HIGH",
        "risk_if_hidden":  "Guidance tab; important for daily discipline",
    },
    {
        "tab_name":        "Research Review",
        "suggested_group": "A - Daily Research",
        "purpose":         "Aggregated research review dashboard and scorecard",
        "priority":        "HIGH",
        "risk_if_hidden":  "Daily review hub; high usage",
    },
    # ── Group B — Data & Providers ──────────────────────────────────────────
    {
        "tab_name":        "API Fetch Status",
        "suggested_group": "B - Data & Providers",
        "purpose":         "API provider status, token health, and fetch diagnostics",
        "priority":        "HIGH",
        "risk_if_hidden":  "Critical for diagnosing data gaps",
    },
    {
        "tab_name":        "Provider Health",
        "suggested_group": "B - Data & Providers",
        "purpose":         "Real-time provider health scorecard",
        "priority":        "HIGH",
        "risk_if_hidden":  "Quick health check; used at session start",
    },
    {
        "tab_name":        "Provider Reliability",
        "suggested_group": "B - Data & Providers",
        "purpose":         "Historical provider reliability matrix and trends",
        "priority":        "MEDIUM",
        "risk_if_hidden":  "Infrequent use; safe to group/collapse",
    },
    {
        "tab_name":        "Data Provider Fetch",
        "suggested_group": "B - Data & Providers",
        "purpose":         "Manual data fetch trigger and import status",
        "priority":        "MEDIUM",
        "risk_if_hidden":  "Used for data refresh; moderate use frequency",
    },
    {
        "tab_name":        "Data Quality Gate",
        "suggested_group": "B - Data & Providers",
        "purpose":         "Data quality checks, freshness gates, and issue alerts",
        "priority":        "HIGH",
        "risk_if_hidden":  "Critical gating step before any analysis",
    },
    {
        "tab_name":        "Universe Manager",
        "suggested_group": "B - Data & Providers",
        "purpose":         "Manage stock universe list and quality filters",
        "priority":        "MEDIUM",
        "risk_if_hidden":  "Infrequent; safe to collapse",
    },
    # ── Group C — Strategy & Rules ──────────────────────────────────────────
    {
        "tab_name":        "Rule Governance",
        "suggested_group": "C - Strategy & Rules",
        "purpose":         "Rule registry management, activation, and audit trail",
        "priority":        "HIGH",
        "risk_if_hidden":  "Core governance; used for rule changes",
    },
    {
        "tab_name":        "Signal Quality",
        "suggested_group": "C - Strategy & Rules",
        "purpose":         "Signal quality engine analysis and precision/recall report",
        "priority":        "HIGH",
        "risk_if_hidden":  "Key quality gate for strategy validation",
    },
    {
        "tab_name":        "Rule Weight Tuning",
        "suggested_group": "C - Strategy & Rules",
        "purpose":         "Grid search tuning for rule weights",
        "priority":        "MEDIUM",
        "risk_if_hidden":  "Used periodically; safe to group",
    },
    {
        "tab_name":        "Strategy Knowledge",
        "suggested_group": "C - Strategy & Rules",
        "purpose":         "Strategy knowledge ingestion, transcript browser, rule candidates",
        "priority":        "MEDIUM",
        "risk_if_hidden":  "Used for knowledge ingestion sessions",
    },
    {
        "tab_name":        "ML Knowledge Integration",
        "suggested_group": "C - Strategy & Rules",
        "purpose":         "ML feature store, knowledge bridge, model monitoring",
        "priority":        "MEDIUM",
        "risk_if_hidden":  "Moderate; used for ML readiness reviews",
    },
    # ── Group D — Backtest & Simulation ─────────────────────────────────────
    {
        "tab_name":        "Hardened Backtest",
        "suggested_group": "D - Backtest & Simulation",
        "purpose":         "Run hardened backtester and view results",
        "priority":        "HIGH",
        "risk_if_hidden":  "Primary validation tool; high usage",
    },
    {
        "tab_name":        "Portfolio Cockpit",
        "suggested_group": "D - Backtest & Simulation",
        "purpose":         "Portfolio simulation dashboard and P&L tracker",
        "priority":        "HIGH",
        "risk_if_hidden":  "Core simulation view",
    },
    {
        "tab_name":        "Intraday Pipeline",
        "suggested_group": "D - Backtest & Simulation",
        "purpose":         "Intraday data ingestion pipeline management",
        "priority":        "MEDIUM",
        "risk_if_hidden":  "Used at intraday data import; moderate",
    },
    {
        "tab_name":        "Intraday Replay",
        "suggested_group": "D - Backtest & Simulation",
        "purpose":         "Intraday bar-by-bar replay and pattern drill",
        "priority":        "MEDIUM",
        "risk_if_hidden":  "Used for pattern training; safe to group",
    },
    # ── Group E — Journal & Review ──────────────────────────────────────────
    {
        "tab_name":        "Portfolio Journal",
        "suggested_group": "E - Journal & Review",
        "purpose":         "Trade journal entries, signal outcomes, mistake taxonomy",
        "priority":        "HIGH",
        "risk_if_hidden":  "Daily journaling is core habit; should be visible",
    },
    {
        "tab_name":        "Notification Center",
        "suggested_group": "E - Journal & Review",
        "purpose":         "Research event notifications and alert history",
        "priority":        "MEDIUM",
        "risk_if_hidden":  "Alerts are important but not primary; groupable",
    },
    {
        "tab_name":        "Experiment Registry",
        "suggested_group": "E - Journal & Review",
        "purpose":         "Experiment tracking, hypothesis log, outcome recording",
        "priority":        "MEDIUM",
        "risk_if_hidden":  "Important for long-term research hygiene",
    },
    # ── Group F — Release & QA ──────────────────────────────────────────────
    {
        "tab_name":        "Release Status",
        "suggested_group": "F - Release & QA",
        "purpose":         "Stable release checklist and regression suite runner",
        "priority":        "MEDIUM",
        "risk_if_hidden":  "Used at release time; low daily usage",
    },
    {
        "tab_name":        "Usability QA",
        "suggested_group": "F - Release & QA",
        "purpose":         "Usability smoke test runner and QA report",
        "priority":        "LOW",
        "risk_if_hidden":  "Developer/QA only; safe to hide by default",
    },
    {
        "tab_name":        "Research OS Planning",
        "suggested_group": "F - Release & QA",
        "purpose":         "v0.5.0 OS planning: module inventory, CLI audit, safety matrix",
        "priority":        "LOW",
        "risk_if_hidden":  "Planning/admin tab; safe to collapse by default",
    },
]

_GROUPS = [
    "A - Daily Research",
    "B - Data & Providers",
    "C - Strategy & Rules",
    "D - Backtest & Simulation",
    "E - Journal & Review",
    "F - Release & QA",
    "G - Core",
]


class GUITabInventoryBuilder:
    """Inventories all GUI tabs and suggests grouping for v0.5.0 refactor.

    [!] OS Planning Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True
    real_order_ready:   bool = False

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_inventory(self) -> list[dict]:
        """Return all tab info dicts."""
        try:
            return list(_TABS)
        except Exception as exc:
            logger.warning("build_inventory error: %s", exc)
            return []

    def suggest_tab_groups(self) -> dict:
        """Return grouping suggestions: {group_name: [tab_name, ...]}."""
        groups: dict[str, list[str]] = {g: [] for g in _GROUPS}
        try:
            for tab in _TABS:
                grp = tab.get("suggested_group", "")
                if grp in groups:
                    groups[grp].append(tab["tab_name"])
                else:
                    groups.setdefault(grp, []).append(tab["tab_name"])
        except Exception as exc:
            logger.warning("suggest_tab_groups error: %s", exc)
        return groups

    def export_inventory(self, output_dir: str) -> str:
        """Write gui_tab_inventory.csv to output_dir. Returns path."""
        fieldnames = [
            "tab_name", "suggested_group", "purpose", "priority", "risk_if_hidden",
        ]
        try:
            os.makedirs(output_dir, exist_ok=True)
            today = datetime.now().strftime("%Y-%m-%d")
            path = os.path.join(output_dir, f"gui_tab_inventory_{today}.csv")
            rows = self.build_inventory()
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            logger.info("gui_tab_inventory CSV saved: %s", path)
            return path
        except Exception as exc:
            logger.warning("export_inventory error: %s", exc)
            fallback = os.path.join(output_dir or ".", "gui_tab_inventory_error.csv")
            return fallback
