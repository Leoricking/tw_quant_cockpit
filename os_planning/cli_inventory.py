"""
os_planning/cli_inventory.py — CLIInventoryBuilder (v0.5.0).

Inventories all main.py CLI commands for TW Quant Cockpit v0.4.x,
detects naming inconsistencies, and exports a CLI reference CSV.

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
# Hardcoded CLI command inventory — all known v0.4.x commands
# Format: (command, category, purpose, mode_support, report_support,
#           suggested_alias, deprecation_candidate, safety)
# ---------------------------------------------------------------------------

_COMMANDS: list[dict] = [
    # ── data ────────────────────────────────────────────────────────────────
    {"command": "download",                        "category": "data",     "purpose": "Download daily K-bar data for a symbol",            "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "data-download",               "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "import-csv",                      "category": "data",     "purpose": "Import daily K-bar CSV into local data store",       "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "import-intraday",                 "category": "data",     "purpose": "Import intraday CSV into intraday cache",            "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "import-institutional",            "category": "data",     "purpose": "Import institutional buy/sell CSV",                  "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "import-margin",                   "category": "data",     "purpose": "Import margin trading CSV",                         "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "import-monthly-revenue",          "category": "data",     "purpose": "Import monthly revenue CSV",                        "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "import-holder",                   "category": "data",     "purpose": "Import major holder CSV",                           "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "import-trust-cost",               "category": "data",     "purpose": "Import trust/cost basis CSV",                       "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "import-profile",                  "category": "data",     "purpose": "Import stock profile CSV",                          "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "data-freshness-check",            "category": "data",     "purpose": "Check freshness of all imported data files",        "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "data-provider-fetch",             "category": "data",     "purpose": "Fetch data via configured provider adapters",       "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    # ── provider ────────────────────────────────────────────────────────────
    {"command": "provider-health",                 "category": "provider", "purpose": "Check health of all data providers",               "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "provider-reliability",            "category": "provider", "purpose": "Run provider reliability matrix analysis",          "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "provider-reliability-report",     "category": "provider", "purpose": "Generate provider reliability Markdown report",     "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "api-fetch-status",                "category": "provider", "purpose": "Show API fetch status dashboard",                  "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "api-fetch-diagnostics",           "category": "provider", "purpose": "Run API fetch diagnostics",                        "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "api-fetch-report",                "category": "provider", "purpose": "Generate API fetch production report",             "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "token-setup",                     "category": "provider", "purpose": "Run token setup assistant (read-only inspection)", "mode_support": "real",        "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    # ── quality ─────────────────────────────────────────────────────────────
    {"command": "data-quality-gate",               "category": "quality",  "purpose": "Run data quality gate checks",                     "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "signal-quality",                  "category": "quality",  "purpose": "Run signal quality engine analysis",               "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "signal-quality-report",           "category": "quality",  "purpose": "Generate signal quality Markdown report",          "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "usability-qa",                    "category": "quality",  "purpose": "Run usability smoke test suite",                   "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    # ── strategy ────────────────────────────────────────────────────────────
    {"command": "strategy-knowledge-ingest",       "category": "strategy", "purpose": "Ingest strategy knowledge transcripts",            "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "strategy-knowledge-list",         "category": "strategy", "purpose": "List all ingested strategy knowledge items",       "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "strategy-knowledge-report",       "category": "strategy", "purpose": "Generate strategy knowledge ingestion report",     "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "rule-governance",                 "category": "strategy", "purpose": "View rule governance dashboard summary",           "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "rule-list",                       "category": "strategy", "purpose": "List all active rules in the registry",            "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "rule-add",                        "category": "strategy", "purpose": "Add a new rule to the registry (dry-run)",         "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "rule-disable",                    "category": "strategy", "purpose": "Disable an existing rule",                         "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "rule-weight-report",              "category": "strategy", "purpose": "Generate rule weight tuning report",               "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    # ── backtest ────────────────────────────────────────────────────────────
    {"command": "hardened-backtest",               "category": "backtest", "purpose": "Run hardened backtester for a symbol/range",        "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "backtest-report",                 "category": "backtest", "purpose": "Generate backtest Markdown report",                 "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "backtest-summary",                "category": "backtest", "purpose": "Print backtest summary to console",                 "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "backtest-compare",                "category": "backtest", "purpose": "Compare two backtest result files",                 "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "backtest-export",                 "category": "backtest", "purpose": "Export backtest results to CSV",                    "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "daily-workflow",                  "category": "backtest", "purpose": "Run daily research workflow pipeline",             "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    # ── portfolio ───────────────────────────────────────────────────────────
    {"command": "simulate-portfolio",              "category": "portfolio","purpose": "Run portfolio simulation (mock only)",              "mode_support": "mock",        "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "tune-rule-weights",               "category": "portfolio","purpose": "Run rule weight grid search tuning",               "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "portfolio-positions",             "category": "portfolio","purpose": "Show current simulated portfolio positions",        "mode_support": "mock",        "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "portfolio-summary",               "category": "portfolio","purpose": "Print portfolio simulation summary",               "mode_support": "mock",        "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "universe-manage",                 "category": "portfolio","purpose": "Manage stock universe list",                       "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "universe-quality",                "category": "portfolio","purpose": "Run universe quality report",                      "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    # ── ml ──────────────────────────────────────────────────────────────────
    {"command": "ml-feature-catalog",              "category": "ml",       "purpose": "Show ML feature catalog",                          "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "ml-feature-snapshot",             "category": "ml",       "purpose": "Build ML feature snapshot for a symbol",           "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "ml-feature-quality",              "category": "ml",       "purpose": "Run ML feature quality checks",                    "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "ml-feature-store-report",         "category": "ml",       "purpose": "Generate ML feature store report",                 "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "ml-knowledge-catalog",            "category": "ml",       "purpose": "Show ML knowledge feature catalog",                "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "ml-knowledge-readiness",          "category": "ml",       "purpose": "Check ML knowledge feature readiness",             "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "ml-knowledge-bridge",             "category": "ml",       "purpose": "Run ML knowledge feature bridge conversion",       "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "ml-knowledge-report",             "category": "ml",       "purpose": "Generate ML knowledge integration report",         "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "model-monitoring",                "category": "ml",       "purpose": "Run model monitoring summary",                     "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "model-monitoring-report",         "category": "ml",       "purpose": "Generate model monitoring Markdown report",        "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "drift-detect",                    "category": "ml",       "purpose": "Run drift detector on prediction log",             "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "ml-leakage-check",                "category": "ml",       "purpose": "Run data leakage checker on feature set",          "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "ml-dataset-build",                "category": "ml",       "purpose": "Build ML feature dataset for training",            "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    # ── replay ──────────────────────────────────────────────────────────────
    {"command": "intraday-replay",                 "category": "replay",   "purpose": "Launch intraday replay session for a symbol/date", "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "replay-session-list",             "category": "replay",   "purpose": "List all saved replay sessions",                   "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "replay-session-export",           "category": "replay",   "purpose": "Export a replay session to CSV",                   "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "replay-session-delete",           "category": "replay",   "purpose": "Delete a saved replay session",                    "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "replay-metrics",                  "category": "replay",   "purpose": "Show replay session metrics summary",              "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "replay-training",                 "category": "replay",   "purpose": "Run replay training mode (scored pattern drill)",  "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "replay-report",                   "category": "replay",   "purpose": "Generate intraday replay Markdown report",         "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "intraday-pipeline",               "category": "replay",   "purpose": "Run intraday data pipeline ingestion",             "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "intraday-pipeline-status",        "category": "replay",   "purpose": "Show intraday pipeline status",                    "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    # ── journal ─────────────────────────────────────────────────────────────
    {"command": "journal-add",                     "category": "journal",  "purpose": "Add a new journal entry",                          "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "journal-list",                    "category": "journal",  "purpose": "List all journal entries",                         "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "journal-export",                  "category": "journal",  "purpose": "Export journal to CSV",                            "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "journal-analytics",               "category": "journal",  "purpose": "Run journal analytics (patterns, mistakes)",       "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "journal-report",                  "category": "journal",  "purpose": "Generate portfolio journal Markdown report",       "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "signal-outcome-track",            "category": "journal",  "purpose": "Track signal outcome in journal",                  "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "replay-training-notes",           "category": "journal",  "purpose": "Add replay training notes to journal",             "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    # ── notification ────────────────────────────────────────────────────────
    {"command": "notification-scan",               "category": "notification","purpose": "Scan all sources and raise notifications",       "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "notification-list",               "category": "notification","purpose": "List recent notifications",                      "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "notification-report",             "category": "notification","purpose": "Generate notification center Markdown report",   "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "notification-clear",              "category": "notification","purpose": "Clear all notifications in the log",             "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "notification-prefs",              "category": "notification","purpose": "Show/edit notification preferences",             "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    # ── review / coach / workflow ────────────────────────────────────────────
    {"command": "research-review",                 "category": "review_coach_workflow","purpose": "Run research review aggregation",        "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "research-review-summary",         "category": "review_coach_workflow","purpose": "Print research review summary",          "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "research-review-report",          "category": "review_coach_workflow","purpose": "Generate research review Markdown report","mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                            "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "exp-list",                        "category": "review_coach_workflow","purpose": "List all experiments in registry",        "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "experiment-list",             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "exp-new",                         "category": "review_coach_workflow","purpose": "Register a new experiment",              "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "experiment-new",              "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "exp-update",                      "category": "review_coach_workflow","purpose": "Update an existing experiment",          "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "experiment-update",           "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "exp-close",                       "category": "review_coach_workflow","purpose": "Close an experiment with outcome",        "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "experiment-close",            "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "exp-report",                      "category": "review_coach_workflow","purpose": "Generate experiment registry report",    "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "experiment-report",           "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "research-coach",                  "category": "review_coach_workflow","purpose": "Run research assistant / coach engine",  "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "research-coach-summary",          "category": "review_coach_workflow","purpose": "Print research coach summary",           "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "research-coach-report",           "category": "review_coach_workflow","purpose": "Generate research coach Markdown report","mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "research-workflow",               "category": "review_coach_workflow","purpose": "Build and run a research workflow",      "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "research-workflow-run",           "category": "review_coach_workflow","purpose": "Execute a stored research workflow",     "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "research-workflow-summary",       "category": "review_coach_workflow","purpose": "Print research workflow summary",        "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "research-workflow-report",        "category": "review_coach_workflow","purpose": "Generate research workflow Markdown report","mode_support": "real,mock","report_support": "yes", "suggested_alias": "",                            "deprecation_candidate": "no",  "safety": "SAFE"},
    # ── release ─────────────────────────────────────────────────────────────
    {"command": "stable-release-check",            "category": "release",  "purpose": "Run stable release checklist",                     "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "regression-suite",                "category": "release",  "purpose": "Run quick or full regression suite",               "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "version-info",                    "category": "release",  "purpose": "Show version and safety flags",                    "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "os-planning-inventory",           "category": "release",  "purpose": "Run Research OS module inventory (v0.5.0)",        "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "os-planning-cli-audit",           "category": "release",  "purpose": "Run CLI inventory builder (v0.5.0)",               "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "os-planning-regression-audit",    "category": "release",  "purpose": "Run regression coverage audit (v0.5.0)",           "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "os-planning-safety-matrix",       "category": "release",  "purpose": "Export safety matrix for all modules (v0.5.0)",    "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "os-planning-artifact-hygiene",    "category": "release",  "purpose": "Run artifact hygiene / .gitignore audit (v0.5.0)", "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "os-planning-gui-audit",           "category": "release",  "purpose": "Run GUI tab inventory builder (v0.5.0)",           "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    # ── gui ─────────────────────────────────────────────────────────────────
    {"command": "cockpit",                         "category": "gui",      "purpose": "Launch TW Quant Cockpit GUI",                       "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "paper",                           "category": "gui",      "purpose": "Launch paper trading simulation GUI",               "mode_support": "mock",        "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "mock-realtime",                   "category": "gui",      "purpose": "Launch mock real-time simulation",                  "mode_support": "mock",        "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "stock-report",                    "category": "gui",      "purpose": "Generate single-stock research report",            "mode_support": "real,mock",  "report_support": "yes", "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "screener",                        "category": "gui",      "purpose": "Run stock screener and show results",               "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "",                             "deprecation_candidate": "no",  "safety": "SAFE"},
    {"command": "ui",                              "category": "gui",      "purpose": "Alias for cockpit command",                         "mode_support": "real,mock",  "report_support": "no",  "suggested_alias": "cockpit",                     "deprecation_candidate": "yes", "safety": "SAFE"},
]

_CATEGORIES = [
    "data", "provider", "quality", "strategy", "backtest",
    "portfolio", "ml", "replay", "journal", "notification",
    "review_coach_workflow", "release", "gui",
]

# Known naming inconsistencies to flag
_INCONSISTENCY_RULES = [
    {"pattern": "exp-",    "standard": "experiment-", "note": "Short 'exp-' prefix inconsistent with verbose 'research-' prefix used elsewhere"},
    {"pattern": "ui",      "standard": "cockpit",     "note": "Bare 'ui' alias duplicates 'cockpit'; deprecation candidate"},
    {"pattern": "-report", "standard": "-report",     "note": "Consistent '-report' suffix — OK"},
]


class CLIInventoryBuilder:
    """Inventories all main.py CLI commands for TW Quant Cockpit v0.4.x.

    [!] OS Planning Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True
    real_order_ready:   bool = False

    def __init__(self, main_py_path: str | None = None) -> None:
        self.main_py_path = main_py_path or os.path.join(BASE_DIR, "main.py")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_inventory(self) -> list[dict]:
        """Return the full hardcoded command inventory list."""
        try:
            return list(_COMMANDS)
        except Exception as exc:
            logger.warning("build_inventory error: %s", exc)
            return []

    def group_commands(self) -> dict:
        """Group commands by category. Returns {category: [cmd_dicts]}."""
        groups: dict[str, list[dict]] = {cat: [] for cat in _CATEGORIES}
        try:
            for cmd in _COMMANDS:
                cat = cmd.get("category", "")
                if cat in groups:
                    groups[cat].append(dict(cmd))
                else:
                    groups.setdefault(cat, []).append(dict(cmd))
        except Exception as exc:
            logger.warning("group_commands error: %s", exc)
        return groups

    def detect_naming_inconsistency(self) -> list[dict]:
        """Find commands with naming inconsistencies. Returns list of issue dicts."""
        issues: list[dict] = []
        try:
            for cmd in _COMMANDS:
                name = cmd.get("command", "")
                # Flag short exp- prefix
                if name.startswith("exp-"):
                    issues.append({
                        "command":    name,
                        "issue_type": "prefix_inconsistency",
                        "detail":     "Uses 'exp-' prefix; consider 'experiment-' for consistency with other research- prefixed commands",
                        "severity":   "LOW",
                    })
                # Flag deprecation candidates
                if cmd.get("deprecation_candidate") == "yes":
                    issues.append({
                        "command":    name,
                        "issue_type": "deprecation_candidate",
                        "detail":     f"Alias or duplicate of '{cmd.get('suggested_alias', '?')}'; consider removing",
                        "severity":   "LOW",
                    })
                # Flag commands with spaces in name (should never happen but guard)
                if " " in name:
                    issues.append({
                        "command":    name,
                        "issue_type": "invalid_name",
                        "detail":     "Command name contains space — invalid CLI argument",
                        "severity":   "HIGH",
                    })
        except Exception as exc:
            logger.warning("detect_naming_inconsistency error: %s", exc)
        return issues

    def build_cli_reference_table(self) -> list[dict]:
        """Return full CLI reference table with all fields."""
        try:
            return list(_COMMANDS)
        except Exception as exc:
            logger.warning("build_cli_reference_table error: %s", exc)
            return []

    def export_inventory(self, output_dir: str) -> str:
        """Write cli_inventory.csv to output_dir. Returns path."""
        fieldnames = [
            "command", "category", "purpose", "mode_support",
            "report_support", "suggested_alias", "deprecation_candidate", "safety",
        ]
        try:
            os.makedirs(output_dir, exist_ok=True)
            today = datetime.now().strftime("%Y-%m-%d")
            path = os.path.join(output_dir, f"cli_inventory_{today}.csv")
            rows = self.build_inventory()
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            logger.info("cli_inventory CSV saved: %s", path)
            return path
        except Exception as exc:
            logger.warning("export_inventory error: %s", exc)
            fallback = os.path.join(output_dir or ".", "cli_inventory_error.csv")
            return fallback
