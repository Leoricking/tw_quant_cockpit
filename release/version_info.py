"""
release/version_info.py — Centralized version info for TW Quant Cockpit v1.1.2.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] VALIDATED does not enable trading. Broker Execution Disabled.
[!] Data Universe Expansion. Real Data Coverage Required.
[!] Data Import UX & Batch Onboarding. dry_run=True default.
[!] Coverage Repair Workflow. Destructive repair disabled.
[!] Mock Data Formal Conclusion: DISABLED. Not Investment Advice.
"""
from __future__ import annotations
import logging
import os

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# v1.1.2 module-level constants (Coverage Repair Workflow)
# ---------------------------------------------------------------------------
VERSION                             = "1.1.2"
RELEASE_NAME                        = "Coverage Repair Workflow"
BASE_RELEASE                        = "1.1.1 Data Import UX & Batch Onboarding"
BASE_RELEASE_NAME                   = "Data Import UX & Batch Onboarding"
MAINTENANCE_RELEASE                 = False
RELEASE_STAGE                       = "STABLE"
RELEASE_TRACK                       = "research"
TRADING_MODE                        = "research_only"
REAL_ORDERS_ENABLED                 = False
BROKER_EXECUTION_ENABLED            = False
PRODUCTION_TRADING_BLOCKED          = True
VALIDATED_DOES_NOT_ENABLE_TRADING   = True
PAPER_TRADING_IS_SIMULATION         = True
MOCK_REALTIME_IS_SIMULATION         = True
NO_REAL_ORDERS                      = True
read_only                           = True
production_blocked                  = True
# v1.0.x preserved flags
EXAMPLE_WORKFLOWS_RELEASE           = True
WORKFLOW_TEMPLATES_AVAILABLE        = True
TEMPLATE_GUIDE_AVAILABLE            = True
KNOWLEDGE_BASE_SEARCH_RELEASE       = True
KNOWLEDGE_BASE_INDEX_AVAILABLE      = True
SAFE_SEARCH_SUMMARY_AVAILABLE       = True
LOCAL_RESEARCH_ASSISTANT_RELEASE    = True
LOCAL_ONLY_ASSISTANT                = True
EXTERNAL_API_DISABLED               = True
SAFE_RESEARCH_SUMMARY_AVAILABLE     = True
FINAL_MAINTENANCE_ROLLUP_RELEASE    = True
V1_MAINTENANCE_LINE_COMPLETE        = True
LONG_TERM_MAINTENANCE_READY         = True
# v1.1.0 new flags
DATA_UNIVERSE_EXPANSION_RELEASE     = True
UNIVERSE_TIERS_AVAILABLE            = True
REAL_DATA_COVERAGE_REQUIRED         = True
MOCK_DATA_FORMAL_CONCLUSION_ALLOWED = False
# v1.1.1 new flags
DATA_IMPORT_ONBOARDING_RELEASE      = True
DRY_RUN_DEFAULT                     = True
DESTRUCTIVE_IMPORT_DISABLED         = True
CONFLICT_AUTO_OVERWRITE_ENABLED     = False
# v1.1.2 new flags
COVERAGE_REPAIR_RELEASE             = True
DESTRUCTIVE_REPAIR_DISABLED         = True
SYNTHETIC_OHLC_REPAIR_DISABLED      = True
INVALID_OHLC_AUTO_MODIFY_DISABLED   = True
MOCK_DATA_REPAIR_DISABLED           = True


class VersionInfo:
    """Centralized version and safety metadata for v0.9.0."""

    version            = "v0.9.0"
    release_name       = "Strategy Lab Stable"
    release_stage      = "STABLE"
    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False
    research_only      = True
    supported_modes    = ["real", "mock"]
    major_features     = [
        "Strategy Lab Stable v0.9.0",
        "Unified Strategy Lab validation over Research OS v0.7.x-v0.8.x",
        "47-capability matrix (RI 9, SM 8, BC 7, TM 6, EG 8, Supporting 9)",
        "Strategy Lab stable checklist (7 categories A-G)",
        "Strategy Lab release manifest builder (JSON + Markdown)",
        "Strategy Lab stable report (13 sections)",
        "Strategy Lab GUI panel (8 summary cards, capability table, checklist)",
        "6 new CLI commands (strategy-lab, strategy-lab-summary, etc.)",
        "Research Intelligence Evidence Graph v0.8.3",
        "14 node types, 12 edge relations, BFS max depth 3",
        "Conservative contradiction detection (never auto-modifies status)",
        "Evidence graph context reading in all Research OS engines",
        "9 new CLI commands (evidence-graph, evidence-graph-threads, etc.)",
        "Backtest Training Metrics v0.8.2",
        "Strategy Memory UX v0.8.1",
        "Status lifecycle: NEW→REVIEWING→VALIDATING→ACCEPTED/REJECTED/NEEDS_MORE_EVIDENCE",
        "accepted_is_research_only=True invariant — ACCEPTED ≠ trading enabled",
        "UX fields: needs_action, validation_ready, status_hint, next_step, last_action_at",
        "Safe command labels: SAFE_READ_ONLY/SAFE_REPORT/SAFE_REGRESSION/SAFE_REPLAY/SAFE_DATA_CHECK",
        "3 new CLI views: validation-queue, active-threads, repeated-patterns",
        "7-tab detail panel in GUI: Summary/Hypothesis/Evidence/Validation/Commands/Links/Safety",
        "Memory link improvements: target_title, why_linked, suggested_next_step",
        "Conservative duplicate detection (>80% similarity + same type + same module)",
        "Research/Coach integration: memory_summary/memory_items params",
        "Research Intelligence Stable v0.8.0",
        "Intelligence Stable Schema (29 capabilities)",
        "Intelligence Capability Matrix",
        "Intelligence Stable Checklist (7 categories)",
        "Intelligence Release Manifest Builder",
        "Intelligence Stable Engine + Store",
        "Intelligence Stable Report (11 sections)",
        "Intelligence Stable GUI Panel",
        "6 new CLI commands (intelligence-stable, etc.)",
        "Safety audit: recommendations/memories/coach tasks",
        "Forbidden action count = 0",
        "Research Intelligence Engine (v0.7.0)",
        "Research Intelligence UX Polish (v0.7.1)",
        "Strategy Research Memory (v0.7.2)",
        "Backtest-to-Coach Loop (v0.7.3)",
        "Research OS Stable Release v0.6.0",
        "Stable Capability Matrix (30+ capabilities)",
        "v0.6.0 Stable Release Checklist",
        "Release Manifest Builder",
        "Known Limitations Registry",
        "Stable Release Report",
        "Stable Release GUI Panel",
        "Daily Workflow Engine",
        "Data Quality Gate",
        "Provider Reliability & Fallback Matrix",
        "Universe Expansion & Sector Classification",
        "Hardened Backtest Engine",
        "Intraday / Tick Data Pipeline",
        "Strategy Rule Governance",
        "Research Notebook / Experiment Registry",
        "Auto Report Center",
        "Signal Quality Dashboard",
        "Rule Weight Tuning Lab",
        "Portfolio Cockpit",
        "Automation Scheduler",
        "Usability QA",
        "Release Status & Regression Suite",
        "Research OS Module Inventory",
        "Research OS CLI Inventory",
        "Research OS GUI Tab Inventory",
        "Research OS Regression Audit",
        "Research OS Artifact Hygiene",
        "Research OS Safety Matrix",
        "Research OS Stabilization Report",
        "CLI Command Registry",
        "CLI Alias Map (35 aliases)",
        "CLI Command Discovery",
        "CLI Help Examples",
        "CLI UX Report",
        "CLI UX GUI Panel",
        "GUI Tab Registry",
        "GUI Navigation Panel",
        "GUI Navigation Report",
    ]
    safety_flags = [
        "read_only=True",
        "no_real_orders=True",
        "production_blocked=True",
        "real_order_ready=False",
        "research_only=True",
        "no_broker_connection=True",
        "no_auto_weight_apply=True",
        "no_shioaji=True",
        "no_mega_broker=True",
    ]


def get_version_info() -> dict:
    """Return all VersionInfo fields as a dict."""
    return {
        "version":            VersionInfo.version,
        "release_name":       VersionInfo.release_name,
        "release_stage":      VersionInfo.release_stage,
        "read_only":          VersionInfo.read_only,
        "no_real_orders":     VersionInfo.no_real_orders,
        "production_blocked": VersionInfo.production_blocked,
        "real_order_ready":   VersionInfo.real_order_ready,
        "supported_modes":    VersionInfo.supported_modes,
        "major_features":     VersionInfo.major_features,
        "safety_flags":       VersionInfo.safety_flags,
    }


def print_version_info() -> None:
    """Print formatted version info to stdout."""
    print("=" * 60)
    print("  TW Quant Cockpit — Version Info")
    print(f"  Version: {VERSION}")
    print(f"  Release: {RELEASE_NAME}")
    print(f"  Base Release: {BASE_RELEASE} {BASE_RELEASE_NAME}")
    print(f"  Stage: {RELEASE_STAGE}")
    print(f"  Track: {RELEASE_TRACK.capitalize()}")
    print(f"  Research Only: {not REAL_ORDERS_ENABLED}")
    print(f"  No Real Orders: {NO_REAL_ORDERS}")
    print(f"  Production Trading BLOCKED: {PRODUCTION_TRADING_BLOCKED}")
    print(f"  Broker Execution Enabled: {BROKER_EXECUTION_ENABLED}")
    print(f"  VALIDATED does not enable trading: {VALIDATED_DOES_NOT_ENABLE_TRADING}")
    print(f"  Final Maintenance Rollup Release: {FINAL_MAINTENANCE_ROLLUP_RELEASE}")
    print(f"  v1.0 Maintenance Line Complete: {V1_MAINTENANCE_LINE_COMPLETE}")
    print(f"  Long-term Maintenance Ready: {LONG_TERM_MAINTENANCE_READY}")
    print(f"  External API Disabled: {EXTERNAL_API_DISABLED}")
    print(f"  Paper Trading: {'Simulation Only' if PAPER_TRADING_IS_SIMULATION else 'N/A'}")
    print(f"  Mock Realtime: {'Simulation Only' if MOCK_REALTIME_IS_SIMULATION else 'N/A'}")
    print(f"  Data Import Onboarding Release: {DATA_IMPORT_ONBOARDING_RELEASE}")
    print(f"  Dry Run Default: {DRY_RUN_DEFAULT}")
    print(f"  Destructive Import Disabled: {DESTRUCTIVE_IMPORT_DISABLED}")
    print(f"  Conflict Auto-Overwrite Enabled: {CONFLICT_AUTO_OVERWRITE_ENABLED}")
    print(f"  Coverage Repair Release: {COVERAGE_REPAIR_RELEASE}")
    print(f"  Destructive Repair Disabled: {DESTRUCTIVE_REPAIR_DISABLED}")
    print(f"  Synthetic OHLC Repair Disabled: {SYNTHETIC_OHLC_REPAIR_DISABLED}")
    print(f"  Invalid OHLC Auto-Modify Disabled: {INVALID_OHLC_AUTO_MODIFY_DISABLED}")
    print(f"  Mock Data Repair Disabled: {MOCK_DATA_REPAIR_DISABLED}")
    print("=" * 60)


def get_safety_banner() -> str:
    """Return one-line safety banner string."""
    return (
        "[!] v0.9.0 Research Only | No Real Orders | "
        "Production BLOCKED | real_order_ready=False"
    )


def get_feature_summary() -> str:
    """Return formatted multi-line feature list string."""
    lines = [
        f"TW Quant Cockpit {VersionInfo.version} — Major Features",
        "-" * 50,
    ]
    for i, feat in enumerate(VersionInfo.major_features, 1):
        lines.append(f"  {i:2d}. {feat}")
    lines.append("-" * 50)
    lines.append(
        f"Total: {len(VersionInfo.major_features)} features | "
        f"Stage: {VersionInfo.release_stage}"
    )
    return "\n".join(lines)
