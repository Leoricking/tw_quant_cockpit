"""
release/version_info.py — Centralized version info for TW Quant Cockpit v1.2.2.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] VALIDATED does not enable trading. Broker Execution Disabled.
[!] Data Universe Expansion. Real Data Coverage Required.
[!] Data Import UX & Batch Onboarding. dry_run=True default.
[!] Coverage Repair Workflow. Destructive repair disabled.
[!] Data Freshness Monitor. Auto external refresh DISABLED.
[!] Future date does not count as fresh. Mock formal freshness DISABLED.
[!] Coverage Quality Gates. Mock/stale/conflict/invalid data cannot pass formal gate.
[!] Quality Gate Override DISABLED by default. Gate does NOT enable trading.
[!] Mock Data Formal Conclusion: DISABLED. Not Investment Advice.
[!] Quality Gate Enforcement & Audit. Gate bypass DISABLED. Not Investment Advice.
[!] Data Governance Operations Dashboard. Auto Repair DISABLED. Auto Download DISABLED.
[!] Governance Gate Override DISABLED. Trade Execution DISABLED. Not Investment Advice.
[!] Governance Alerts & Daily Operations. External Notification Send DISABLED.
[!] Alert detection does NOT repair, import, override gates, or enable trading. Not Investment Advice.
[!] Research Run Registry. Registry does NOT execute commands. Auto Rerun DISABLED. Trading DISABLED.
[!] Data Governance Stable Rollup. No Auto Store Repair. No Auto Data Repair. No Auto Download.
[!] No Auto Import. No Auto Research Execution. No Trade Execution. Not Investment Advice.
[!] Replay Training UX Foundation. Replay Auto Scoring DISABLED. Replay Auto Execution DISABLED.
[!] Replay Trade Execution DISABLED. Replay decisions are SIMULATION ONLY. Not Investment Advice.
[!] Replay Scenario & Session Manager. Scenario templates never contain future answers.
[!] Replay Session Fork/Checkpoint NEVER copies future data. Not Investment Advice.
[!] Decision Journal Integration. Journal decisions are SIMULATION ONLY. No paper orders. No broker.
[!] No hindsight scoring. No future results. No realized PnL. Not Investment Advice.
[!] Emotional state self-reported only. NOT psychological diagnosis. No auto scoring.
[!] Cognitive bias flags self-reported or rule-triggered only. Not auto-inferred from performance.
"""
from __future__ import annotations
import logging
import os

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# v1.1.9 module-level constants (Data Governance Stable Rollup)
# ---------------------------------------------------------------------------
VERSION                             = "1.2.2"
RELEASE_NAME                        = "Decision Journal Integration"
BASE_RELEASE                        = "1.2.1 Replay Scenario & Session Manager"
BASE_RELEASE_NAME                   = "Data Governance Stable Rollup"
MAINTENANCE_RELEASE                 = False
RELEASE_STAGE                       = "FOUNDATION"
RELEASE_TRACK                       = "replay_training"
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
COVERAGE_REPAIR_AVAILABLE           = True
COVERAGE_REPAIR_DRY_RUN_DEFAULT     = True
DESTRUCTIVE_REPAIR_DISABLED         = True
DESTRUCTIVE_REPAIR_DISABLED_BY_DEFAULT = True
SYNTHETIC_OHLC_REPAIR_DISABLED      = True
INVALID_OHLC_AUTO_MODIFY_DISABLED   = True
MOCK_DATA_REPAIR_DISABLED           = True
SYNTHETIC_PRICE_REPAIR_ENABLED      = False
EXTERNAL_DATA_DOWNLOAD_ENABLED      = False
# v1.1.3 new flags
DATA_FRESHNESS_MONITOR_AVAILABLE    = True
FRESHNESS_SLA_AVAILABLE             = True
SOURCE_INTERRUPTION_DETECTION_AVAILABLE = True
AUTO_EXTERNAL_REFRESH_ENABLED       = False
STALE_DATA_AUTO_REPAIR_ENABLED      = False
FUTURE_DATE_COUNTS_AS_FRESH         = False
MOCK_DATA_FORMAL_FRESHNESS_ALLOWED  = False
# v1.1.4 preserved flags
COVERAGE_QUALITY_GATES_AVAILABLE    = True
FORMAL_BACKTEST_GATE_AVAILABLE      = True
FORMAL_VALIDATION_GATE_AVAILABLE    = True
MOCK_DATA_FORMAL_GATE_ALLOWED       = False
STALE_DATA_FORMAL_GATE_ALLOWED      = False
CONFLICT_DATA_FORMAL_GATE_ALLOWED   = False
INVALID_DATA_FORMAL_GATE_ALLOWED    = False
# v1.1.5 new flags
QUALITY_GATE_ENFORCEMENT_AVAILABLE      = True
QUALITY_GATE_AUDIT_AVAILABLE            = True
RUN_GATE_SNAPSHOT_AVAILABLE             = True
RUN_REPRODUCIBILITY_HASH_AVAILABLE      = True
QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT = True
QUALITY_GATE_BYPASS_ALLOWED             = False
MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED    = False
BLOCKED_DATA_FORMAL_ENFORCEMENT_ALLOWED = False
# v1.1.6 new flags
DATA_GOVERNANCE_DASHBOARD_AVAILABLE     = True
GOVERNANCE_ACTION_QUEUE_AVAILABLE       = True
GOVERNANCE_DAILY_SUMMARY_AVAILABLE      = True
GOVERNANCE_AUTO_REPAIR_ENABLED          = False
GOVERNANCE_AUTO_DOWNLOAD_ENABLED        = False
GOVERNANCE_GATE_OVERRIDE_ENABLED        = False
GOVERNANCE_TRADE_EXECUTION_ENABLED      = False
# v1.1.7 new flags
GOVERNANCE_ALERTS_AVAILABLE             = True
GOVERNANCE_DAILY_DIGEST_AVAILABLE       = True
GOVERNANCE_ALERT_DEDUP_AVAILABLE        = True
GOVERNANCE_ALERT_SNOOZE_AVAILABLE       = True
GOVERNANCE_ALERT_ESCALATION_AVAILABLE   = True
GOVERNANCE_AUTO_IMPORT_ENABLED          = False
EXTERNAL_NOTIFICATION_SEND_ENABLED      = False
# v1.1.8 new flags
RESEARCH_RUN_REGISTRY_AVAILABLE         = True
RUN_LINEAGE_AVAILABLE                   = True
RUN_ARTIFACT_CATALOG_AVAILABLE          = True
RUN_COMPARISON_AVAILABLE                = True
RUN_DUPLICATE_DETECTION_AVAILABLE       = True
RUN_AUTO_RERUN_ENABLED                  = False
RUN_AUTO_EXECUTION_ENABLED              = False
RUN_TRADE_EXECUTION_ENABLED             = False
# v1.1.9 new flags
DATA_GOVERNANCE_STABLE_ROLLUP_AVAILABLE = True
CROSS_MODULE_CONSISTENCY_AVAILABLE      = True
STORE_RECOVERY_AVAILABLE                = True
STORE_INDEX_REBUILD_AVAILABLE           = True
CROSS_MACHINE_PATH_NORMALIZATION_AVAILABLE = True
LEGACY_METADATA_MIGRATION_AVAILABLE     = True
AUTO_STORE_REPAIR_ENABLED               = False
AUTO_DATA_REPAIR_ENABLED                = False
AUTO_DATA_DOWNLOAD_ENABLED              = False
AUTO_DATA_IMPORT_ENABLED                = False
AUTO_RESEARCH_EXECUTION_ENABLED         = False
AUTO_RESEARCH_RERUN_ENABLED             = False
TRADE_EXECUTION_ENABLED                 = False
# v1.2.0 new flags
REPLAY_TRAINING_AVAILABLE               = True
REPLAY_SESSION_AVAILABLE                = True
REPLAY_DAILY_STEP_AVAILABLE             = True
REPLAY_FUTURE_DATA_FIREWALL_AVAILABLE   = True
REPLAY_DECISION_CAPTURE_AVAILABLE       = True
REPLAY_AUTO_SCORING_ENABLED             = False
REPLAY_AUTO_EXECUTION_ENABLED           = False
REPLAY_TRADE_EXECUTION_ENABLED          = False
# v1.2.1 new flags
REPLAY_SCENARIO_LIBRARY_AVAILABLE       = True
REPLAY_SESSION_MANAGER_AVAILABLE        = True
REPLAY_CHECKPOINT_AVAILABLE             = True
REPLAY_SESSION_FORK_AVAILABLE           = True
REPLAY_SESSION_COMPARE_AVAILABLE        = True
REPLAY_BATCH_SESSION_CREATION_AVAILABLE = True
REPLAY_AUTO_SCORING_ENABLED             = False   # noqa: F811 (overrides above, both False)
REPLAY_AUTO_DECISION_ENABLED            = False
REPLAY_AUTO_EXECUTION_ENABLED           = False   # noqa: F811
REPLAY_TRADE_EXECUTION_ENABLED          = False   # noqa: F811
# v1.2.2 Decision Journal Integration flags
DECISION_JOURNAL_AVAILABLE              = True
DECISION_REVISION_HISTORY_AVAILABLE     = True
DISCIPLINE_CHECKLIST_AVAILABLE          = True
EMOTIONAL_STATE_CAPTURE_AVAILABLE       = True
TRADE_THESIS_CAPTURE_AVAILABLE          = True
RISK_PLAN_CAPTURE_AVAILABLE             = True
DECISION_AUTO_SCORING_ENABLED           = False
DECISION_AUTO_GENERATION_ENABLED        = False
DECISION_AUTO_EXECUTION_ENABLED         = False
REPLAY_TRADE_EXECUTION_ENABLED          = False   # noqa: F811


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
    print(f"  Base Release: {BASE_RELEASE}")
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
    print(f"  Coverage Repair Available: {COVERAGE_REPAIR_AVAILABLE}")
    print(f"  Coverage Repair Dry Run Default: {COVERAGE_REPAIR_DRY_RUN_DEFAULT}")
    print(f"  Destructive Repair Disabled By Default: {DESTRUCTIVE_REPAIR_DISABLED_BY_DEFAULT}")
    print(f"  Conflict Auto Overwrite Enabled: {CONFLICT_AUTO_OVERWRITE_ENABLED}")
    print(f"  Synthetic Price Repair Enabled: {SYNTHETIC_PRICE_REPAIR_ENABLED}")
    print(f"  External Data Download Enabled: {EXTERNAL_DATA_DOWNLOAD_ENABLED}")
    print(f"  Mock Data Formal Conclusion Allowed: {MOCK_DATA_FORMAL_CONCLUSION_ALLOWED}")
    print(f"  Data Freshness Monitor Available: {DATA_FRESHNESS_MONITOR_AVAILABLE}")
    print(f"  Freshness SLA Available: {FRESHNESS_SLA_AVAILABLE}")
    print(f"  Source Interruption Detection Available: {SOURCE_INTERRUPTION_DETECTION_AVAILABLE}")
    print(f"  Auto External Refresh Enabled: {AUTO_EXTERNAL_REFRESH_ENABLED}")
    print(f"  Stale Data Auto Repair Enabled: {STALE_DATA_AUTO_REPAIR_ENABLED}")
    print(f"  Future Date Counts As Fresh: {FUTURE_DATE_COUNTS_AS_FRESH}")
    print(f"  Mock Data Formal Freshness Allowed: {MOCK_DATA_FORMAL_FRESHNESS_ALLOWED}")
    print(f"  Coverage Quality Gates Available: {COVERAGE_QUALITY_GATES_AVAILABLE}")
    print(f"  Formal Backtest Gate Available: {FORMAL_BACKTEST_GATE_AVAILABLE}")
    print(f"  Formal Validation Gate Available: {FORMAL_VALIDATION_GATE_AVAILABLE}")
    print(f"  Mock Data Formal Gate Allowed: {MOCK_DATA_FORMAL_GATE_ALLOWED}")
    print(f"  Stale Data Formal Gate Allowed: {STALE_DATA_FORMAL_GATE_ALLOWED}")
    print(f"  Conflict Data Formal Gate Allowed: {CONFLICT_DATA_FORMAL_GATE_ALLOWED}")
    print(f"  Invalid Data Formal Gate Allowed: {INVALID_DATA_FORMAL_GATE_ALLOWED}")
    print(f"  Quality Gate Enforcement Available: {QUALITY_GATE_ENFORCEMENT_AVAILABLE}")
    print(f"  Quality Gate Audit Available: {QUALITY_GATE_AUDIT_AVAILABLE}")
    print(f"  Run Gate Snapshot Available: {RUN_GATE_SNAPSHOT_AVAILABLE}")
    print(f"  Run Reproducibility Hash Available: {RUN_REPRODUCIBILITY_HASH_AVAILABLE}")
    print(f"  Quality Gate Override Disabled By Default: {QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT}")
    print(f"  Quality Gate Bypass Allowed: {QUALITY_GATE_BYPASS_ALLOWED}")
    print(f"  Mock Data Formal Enforcement Allowed: {MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED}")
    print(f"  Blocked Data Formal Enforcement Allowed: {BLOCKED_DATA_FORMAL_ENFORCEMENT_ALLOWED}")
    print(f"  Data Governance Dashboard Available: {DATA_GOVERNANCE_DASHBOARD_AVAILABLE}")
    print(f"  Governance Action Queue Available: {GOVERNANCE_ACTION_QUEUE_AVAILABLE}")
    print(f"  Governance Daily Summary Available: {GOVERNANCE_DAILY_SUMMARY_AVAILABLE}")
    print(f"  Governance Auto Repair Enabled: {GOVERNANCE_AUTO_REPAIR_ENABLED}")
    print(f"  Governance Auto Download Enabled: {GOVERNANCE_AUTO_DOWNLOAD_ENABLED}")
    print(f"  Governance Gate Override Enabled: {GOVERNANCE_GATE_OVERRIDE_ENABLED}")
    print(f"  Governance Trade Execution Enabled: {GOVERNANCE_TRADE_EXECUTION_ENABLED}")
    print(f"  Governance Alerts Available: {GOVERNANCE_ALERTS_AVAILABLE}")
    print(f"  Governance Daily Digest Available: {GOVERNANCE_DAILY_DIGEST_AVAILABLE}")
    print(f"  Governance Alert Dedup Available: {GOVERNANCE_ALERT_DEDUP_AVAILABLE}")
    print(f"  Governance Alert Snooze Available: {GOVERNANCE_ALERT_SNOOZE_AVAILABLE}")
    print(f"  Governance Alert Escalation Available: {GOVERNANCE_ALERT_ESCALATION_AVAILABLE}")
    print(f"  Governance Auto Import Enabled: {GOVERNANCE_AUTO_IMPORT_ENABLED}")
    print(f"  External Notification Send Enabled: {EXTERNAL_NOTIFICATION_SEND_ENABLED}")
    print(f"  Research Run Registry Available: {RESEARCH_RUN_REGISTRY_AVAILABLE}")
    print(f"  Run Lineage Available: {RUN_LINEAGE_AVAILABLE}")
    print(f"  Run Artifact Catalog Available: {RUN_ARTIFACT_CATALOG_AVAILABLE}")
    print(f"  Run Comparison Available: {RUN_COMPARISON_AVAILABLE}")
    print(f"  Run Duplicate Detection Available: {RUN_DUPLICATE_DETECTION_AVAILABLE}")
    print(f"  Run Auto Rerun Enabled: {RUN_AUTO_RERUN_ENABLED}")
    print(f"  Run Auto Execution Enabled: {RUN_AUTO_EXECUTION_ENABLED}")
    print(f"  Run Trade Execution Enabled: {RUN_TRADE_EXECUTION_ENABLED}")
    print(f"  Data Governance Stable Rollup Available: {DATA_GOVERNANCE_STABLE_ROLLUP_AVAILABLE}")
    print(f"  Cross Module Consistency Available: {CROSS_MODULE_CONSISTENCY_AVAILABLE}")
    print(f"  Store Recovery Available: {STORE_RECOVERY_AVAILABLE}")
    print(f"  Store Index Rebuild Available: {STORE_INDEX_REBUILD_AVAILABLE}")
    print(f"  Cross Machine Path Normalization Available: {CROSS_MACHINE_PATH_NORMALIZATION_AVAILABLE}")
    print(f"  Legacy Metadata Migration Available: {LEGACY_METADATA_MIGRATION_AVAILABLE}")
    print(f"  Auto Store Repair Enabled: {AUTO_STORE_REPAIR_ENABLED}")
    print(f"  Auto Data Repair Enabled: {AUTO_DATA_REPAIR_ENABLED}")
    print(f"  Auto Data Download Enabled: {AUTO_DATA_DOWNLOAD_ENABLED}")
    print(f"  Auto Data Import Enabled: {AUTO_DATA_IMPORT_ENABLED}")
    print(f"  Auto Research Execution Enabled: {AUTO_RESEARCH_EXECUTION_ENABLED}")
    print(f"  Auto Research Rerun Enabled: {AUTO_RESEARCH_RERUN_ENABLED}")
    print(f"  Trade Execution Enabled: {TRADE_EXECUTION_ENABLED}")
    print(f"  Replay Training Available: {REPLAY_TRAINING_AVAILABLE}")
    print(f"  Replay Session Available: {REPLAY_SESSION_AVAILABLE}")
    print(f"  Replay Daily Step Available: {REPLAY_DAILY_STEP_AVAILABLE}")
    print(f"  Replay Future Data Firewall Available: {REPLAY_FUTURE_DATA_FIREWALL_AVAILABLE}")
    print(f"  Replay Decision Capture Available: {REPLAY_DECISION_CAPTURE_AVAILABLE}")
    print(f"  Replay Auto Scoring Enabled: {REPLAY_AUTO_SCORING_ENABLED}")
    print(f"  Replay Auto Execution Enabled: {REPLAY_AUTO_EXECUTION_ENABLED}")
    print(f"  Replay Trade Execution Enabled: {REPLAY_TRADE_EXECUTION_ENABLED}")
    print(f"  Replay Scenario Library Available: {REPLAY_SCENARIO_LIBRARY_AVAILABLE}")
    print(f"  Replay Session Manager Available: {REPLAY_SESSION_MANAGER_AVAILABLE}")
    print(f"  Replay Checkpoint Available: {REPLAY_CHECKPOINT_AVAILABLE}")
    print(f"  Replay Session Fork Available: {REPLAY_SESSION_FORK_AVAILABLE}")
    print(f"  Replay Session Compare Available: {REPLAY_SESSION_COMPARE_AVAILABLE}")
    print(f"  Replay Batch Session Creation Available: {REPLAY_BATCH_SESSION_CREATION_AVAILABLE}")
    print(f"  Replay Auto Decision Enabled: {REPLAY_AUTO_DECISION_ENABLED}")
    print(f"  Decision Journal Available: {DECISION_JOURNAL_AVAILABLE}")
    print(f"  Decision Revision History Available: {DECISION_REVISION_HISTORY_AVAILABLE}")
    print(f"  Discipline Checklist Available: {DISCIPLINE_CHECKLIST_AVAILABLE}")
    print(f"  Emotional State Capture Available: {EMOTIONAL_STATE_CAPTURE_AVAILABLE}")
    print(f"  Trade Thesis Capture Available: {TRADE_THESIS_CAPTURE_AVAILABLE}")
    print(f"  Risk Plan Capture Available: {RISK_PLAN_CAPTURE_AVAILABLE}")
    print(f"  Decision Auto Scoring Enabled: {DECISION_AUTO_SCORING_ENABLED}")
    print(f"  Decision Auto Generation Enabled: {DECISION_AUTO_GENERATION_ENABLED}")
    print(f"  Decision Auto Execution Enabled: {DECISION_AUTO_EXECUTION_ENABLED}")
    print(f"  Replay Trade Execution Enabled: {REPLAY_TRADE_EXECUTION_ENABLED}")
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
