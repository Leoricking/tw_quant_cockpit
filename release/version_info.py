"""
release/version_info.py — Centralized version info for TW Quant Cockpit v1.3.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] VALIDATED does not enable trading. Broker Execution Disabled.
[!] Replay Challenge Mode. Challenge Training Only. Simulation Only.
[!] Future data hidden. Outcome hidden until explicit reveal. Answer Key separate.
[!] No Public Leaderboard. No Network Submission. Local personal records only.
[!] Process weight always >= Outcome weight. No auto-decision. No auto-reveal.
[!] Deterministic seed: same seed + data version = same challenge.
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
[!] Replay Scoring & Mistake Taxonomy. Scoring NEVER triggers paper orders or broker execution.
[!] Process scores use NO future data, NO outcome, NO PnL. Outcome reveal EXPLICIT ONLY.
[!] Mistake detection SUGGESTED status only. System cannot auto-confirm mistakes.
[!] Auto Outcome Reveal DISABLED. Auto Mistake Confirmation DISABLED. Score-to-Trade DISABLED.
[!] Replay Trade Execution DISABLED. No Auto Strategy Change. Not Investment Advice.
[!] Strategy Knowledge Replay. Point-in-time verified. No forward return. No outcome.
[!] Auto Strategy Decision DISABLED. Auto Strategy Execution DISABLED.
[!] Auto Strategy Weight Change DISABLED. Broker Disabled. Not Investment Advice.
[!] Multi-Timeframe Replay. Synchronized D1/M60/M20/M5/M1. No future K-lines.
[!] Partial bar NEVER used for confirmed signals. Past-only asof join. No bfill.
[!] Agreement/Conflict analysis is TRAINING ONLY. No Auto-Trade. No Auto-Block.
[!] Batch default preview mode. BLOCKED without --execute --allow-write.
[!] Replay Review Dashboard. No Auto Review Complete. No Auto Outcome Reveal. No Auto Confirm.
[!] No Auto Decision. No Auto Execution. No Score-to-Trade. Broker Disabled. Not Investment Advice.
[!] Replay Dataset & Session Registry. Dataset Registry Only. Session Registry Only.
[!] No Auto Dataset Overwrite. No Auto Dataset Repair. No Auto Session Rebind.
[!] No Auto Package Import. No Auto Conflict Resolution. Registry does not execute trades.
[!] Portable packages use RELATIVE_ONLY paths. No absolute paths in portable manifests.
[!] Frozen datasets are immutable. Modification requires new version. Not Investment Advice.
[!] Replay Training Stable Rollup. Freeze and validate Replay Training v1.2 line.
[!] No new trading functionality. Stable manifests, audits, contracts only. Not Investment Advice.
[!] No Auto Replay Decision. No Auto Replay Execution. No Auto Conflict Resolution.
[!] Stable health check does NOT repair, execute, or enable trading. Research Only.
[!] Real Data Quality Foundation. Mock fallback DISABLED. Real mode does not substitute mock data.
[!] BLOCKED status: no precise prices, no formal buy recommendations. Research Only.
[!] UNAVAILABLE: returns REAL DATA UNAVAILABLE. No mock fallback. Not Investment Advice.
[!] Data quality score 0-100. CRITICAL issue caps score at 49. Not Investment Advice.
[!] Universe Expansion Foundation. Registry only. No Auto Download. No Real API Connected.
[!] Universe Ready does NOT enable trading. Universe Registered != data complete.
[!] Universe Covered != can generate precise prices. No mock fallback on scan failure.
[!] No auto-generation of fake OHLCV. No auto-backtest. No auto-trading suggestions.
"""
from __future__ import annotations
import logging
import os

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# v1.3.3 module-level constants (Coverage Repair Workflow)
# ---------------------------------------------------------------------------
VERSION                             = "1.4.5"
RELEASE_NAME                        = "Source Lineage & Rate Limit"
BASE_RELEASE                        = "1.4.4 FinMind Adapter Hardening"

# ---------------------------------------------------------------------------
# v1.3.2 module-level constants (Real Data Provider Adapter Foundation)
# ---------------------------------------------------------------------------
# VERSION                           = "1.3.2"  # superseded by v1.3.3
# RELEASE_NAME                      = "Real Data Provider Adapter Foundation"
# BASE_RELEASE                      = "1.3.1 Universe Expansion Foundation"
BASE_RELEASE_NAME                   = "Universe Expansion Foundation"
MAINTENANCE_RELEASE                 = False
RELEASE_STAGE                       = "STABLE"
RELEASE_TRACK                       = "real_data_quality"
STABLE_ROLLUP                       = True
REPLAY_TRAINING_LINE_COMPLETE       = True
LONG_TERM_MAINTENANCE_READY         = True
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
# v1.2.3 Replay Scoring & Mistake Taxonomy flags
REPLAY_SCORING_AVAILABLE                = True
PROCESS_OUTCOME_SEPARATION_AVAILABLE    = True
MISTAKE_TAXONOMY_AVAILABLE              = True
MISTAKE_REVIEW_AVAILABLE                = True
OUTCOME_REVEAL_AVAILABLE                = True
PLAN_ADHERENCE_AVAILABLE                = True
AUTO_OUTCOME_REVEAL_ENABLED             = False
AUTO_MISTAKE_CONFIRMATION_ENABLED       = False
AUTO_STRATEGY_CHANGE_ENABLED            = False
AUTO_SCORE_TO_TRADE_ENABLED             = False
REPLAY_TRADE_EXECUTION_ENABLED          = False   # noqa: F811 (all False)
# v1.2.4 Strategy Knowledge Replay flags
STRATEGY_KNOWLEDGE_REPLAY_AVAILABLE     = True
STRATEGY_SIGNAL_TIMELINE_AVAILABLE      = True
STRATEGY_RULE_REVIEW_AVAILABLE          = True
STRATEGY_AGREEMENT_ANALYSIS_AVAILABLE   = True
STRATEGY_CONFLICT_ANALYSIS_AVAILABLE    = True
ABC_BUY_POINT_REPLAY_AVAILABLE          = True
AUTO_STRATEGY_DECISION_ENABLED          = False
AUTO_STRATEGY_EXECUTION_ENABLED         = False
AUTO_STRATEGY_WEIGHT_CHANGE_ENABLED     = False
AUTO_STRATEGY_MISTAKE_CONFIRMATION_ENABLED = False
# v1.2.5 Multi-Timeframe Replay flags
MULTI_TIMEFRAME_REPLAY_AVAILABLE        = True
MTF_SYNCHRONIZED_CLOCK_AVAILABLE        = True
MTF_FUTURE_FIREWALL_AVAILABLE           = True
MTF_POINT_IN_TIME_VERIFIER_AVAILABLE    = True
MTF_AGREEMENT_ANALYSIS_AVAILABLE        = True
MTF_CONFLICT_ANALYSIS_AVAILABLE         = True
MTF_BAR_AGGREGATION_AVAILABLE           = True
MTF_BATCH_RUNNER_AVAILABLE              = True
MTF_PARTIAL_BAR_PROTECTION_AVAILABLE    = True
MTF_PAST_ONLY_ASOF_JOIN                 = True
MTF_NO_BFILL                            = True
MTF_NO_CENTERED_ROLLING                 = True
MTF_NO_FUTURE_KLINES                    = True
MTF_DAILY_NO_FAKE_INTRADAY              = True
MTF_REAL_NO_MOCK_FALLBACK               = True
MTF_AUTO_TRADE_ENABLED                  = False
MTF_AUTO_BLOCK_ENABLED                  = False
MTF_AUTO_DECISION_ENABLED               = False
MTF_BATCH_AUTO_EXECUTE_ENABLED          = False
# Aliases used by health check
AUTO_MULTI_TIMEFRAME_DECISION_ENABLED       = False
AUTO_TIMEFRAME_MISTAKE_CONFIRMATION_ENABLED = False
AUTO_TIMEFRAME_STRATEGY_EXECUTION_ENABLED   = False
# v1.2.6 Replay Review Dashboard flags
REPLAY_REVIEW_DASHBOARD_AVAILABLE      = True
REPLAY_REVIEW_QUEUE_AVAILABLE          = True
REPLAY_REVIEW_PROGRESS_AVAILABLE       = True
REPLAY_CROSS_MODULE_NAVIGATION_AVAILABLE = True
REPLAY_REVIEW_COMPARISON_AVAILABLE     = True
REPLAY_BATCH_REVIEW_AVAILABLE          = True
AUTO_REVIEW_COMPLETE_ENABLED           = False
AUTO_OUTCOME_REVEAL_ENABLED            = False  # noqa: F811
AUTO_MISTAKE_CONFIRMATION_ENABLED      = False  # noqa: F811
AUTO_DECISION_CREATION_ENABLED         = False
AUTO_STRATEGY_CHANGE_ENABLED           = False  # noqa: F811
AUTO_SCORE_TO_TRADE_ENABLED            = False  # noqa: F811
REPLAY_TRADE_EXECUTION_ENABLED         = False  # noqa: F811
# v1.2.7 Replay Challenge Mode flags
REPLAY_CHALLENGE_MODE_AVAILABLE             = True
REPLAY_CHALLENGE_LIBRARY_AVAILABLE          = True
TIMED_CHALLENGE_AVAILABLE                   = True
HIDDEN_FUTURE_CHALLENGE_AVAILABLE           = True
CHALLENGE_DIFFICULTY_AVAILABLE              = True
CHALLENGE_PERSONAL_LEADERBOARD_AVAILABLE    = True
CHALLENGE_MISTAKE_TRAINING_AVAILABLE        = True
PUBLIC_LEADERBOARD_ENABLED                  = False
NETWORK_SCORE_SUBMISSION_ENABLED            = False
AUTO_CHALLENGE_DECISION_ENABLED             = False
AUTO_CHALLENGE_OUTCOME_REVEAL_ENABLED       = False
AUTO_CHALLENGE_MISTAKE_CONFIRMATION_ENABLED = False
AUTO_STRATEGY_CHANGE_ENABLED                = False  # noqa: F811
AUTO_SCORE_TO_TRADE_ENABLED                 = False  # noqa: F811
REPLAY_TRADE_EXECUTION_ENABLED              = False  # noqa: F811
# v1.2.8 Replay Dataset & Session Registry flags
REPLAY_DATASET_REGISTRY_AVAILABLE          = True
REPLAY_SESSION_REGISTRY_AVAILABLE          = True
DATASET_VERSIONING_AVAILABLE               = True
DATASET_FINGERPRINT_AVAILABLE              = True
SESSION_FINGERPRINT_AVAILABLE              = True
DATASET_LINEAGE_AVAILABLE                  = True
SESSION_LINEAGE_AVAILABLE                  = True
PORTABLE_REPLAY_PACKAGE_AVAILABLE          = True
CROSS_COMPUTER_PATH_REMAP_AVAILABLE        = True
REGISTRY_REPAIR_PREVIEW_AVAILABLE          = True
AUTO_DATASET_OVERWRITE_ENABLED             = False
AUTO_DATASET_REPAIR_ENABLED                = False
AUTO_SESSION_REBIND_ENABLED                = False
AUTO_PACKAGE_IMPORT_ENABLED                = False
AUTO_REGISTRY_CONFLICT_RESOLUTION_ENABLED  = False
AUTO_TRADING_ENABLED                       = False
REPLAY_TRADE_EXECUTION_ENABLED             = False  # noqa: F811
# v1.2.9 Replay Training Stable Rollup flags
REPLAY_STABLE_BASELINE                      = "1.2.9"   # frozen Replay Training v1.2 line
REPLAY_STABLE_HEALTH_AVAILABLE              = True
REPLAY_STABLE_MANIFEST_AVAILABLE            = True
REPLAY_CAPABILITY_MATRIX_AVAILABLE          = True
REPLAY_BACKWARD_COMPATIBILITY_AVAILABLE     = True
REPLAY_CROSS_MODULE_CONTRACT_CHECK_AVAILABLE = True
REPLAY_RELEASE_GATE_AVAILABLE               = True
REPLAY_FOUNDATION_AVAILABLE                 = True
REPLAY_SCENARIO_MANAGER_AVAILABLE           = True
REPLAY_SESSION_MANAGER_AVAILABLE            = True  # noqa: F811
REPLAY_DECISION_JOURNAL_AVAILABLE           = True
REPLAY_SCORING_AVAILABLE                    = True  # noqa: F811
REPLAY_MISTAKE_TAXONOMY_AVAILABLE           = True
REPLAY_STRATEGY_KNOWLEDGE_AVAILABLE         = True
REPLAY_MULTI_TIMEFRAME_AVAILABLE            = True
REPLAY_REVIEW_DASHBOARD_AVAILABLE           = True  # noqa: F811
REPLAY_CHALLENGE_MODE_AVAILABLE             = True  # noqa: F811
REPLAY_DATASET_REGISTRY_AVAILABLE           = True  # noqa: F811
REPLAY_SESSION_REGISTRY_AVAILABLE           = True  # noqa: F811
AUTO_REPLAY_DECISION_ENABLED                = False
AUTO_REPLAY_EXECUTION_ENABLED               = False
AUTO_MISTAKE_CONFIRMATION_ENABLED           = False  # noqa: F811
AUTO_OUTCOME_REVEAL_ENABLED                 = False  # noqa: F811
AUTO_STRATEGY_CHANGE_ENABLED                = False  # noqa: F811
AUTO_STRATEGY_WEIGHT_CHANGE_ENABLED         = False
AUTO_CONFLICT_RESOLUTION_ENABLED            = False
# v1.3.0 Real Data Quality Foundation flags
REAL_DATA_QUALITY_FOUNDATION                = True
REAL_DATA_QUALITY_VALIDATOR                 = True
DATA_COMPLETENESS_GATE_PROFILES             = True
QUALITY_SCORE_0_100                         = True
DATA_PROVENANCE_TRACKING                    = True
MOCK_FALLBACK_ENABLED                       = False  # ALWAYS FALSE
REAL_NO_MOCK_FALLBACK                       = True
MOCK_DEMO_ONLY_LABEL_ENFORCED               = True
REAL_DATA_QUALITY_CLI_ENABLED               = True
REAL_DATA_QUALITY_GUI_PANEL                 = True
REAL_DATA_QUALITY_HEALTH                    = True
# v1.3.1 Universe Expansion Foundation flags
UNIVERSE_REGISTRY_AVAILABLE                 = True
UNIVERSE_COVERAGE_AVAILABLE                 = True
UNIVERSE_BATCH_QUALITY_SCAN_AVAILABLE       = True
UNIVERSE_REAL_API_CONNECTED                 = False  # ALWAYS FALSE
UNIVERSE_AUTO_DOWNLOAD_ENABLED              = False  # ALWAYS FALSE
REAL_ORDERS_ENABLED                         = False  # noqa: F811  ALWAYS FALSE
# v1.3.2 Real Data Provider Adapter Foundation flags
REAL_DATA_PROVIDER_ADAPTER_FOUNDATION               = True
REAL_DATA_PROVIDER_ADAPTER_AVAILABLE                = True   # spec alias
REAL_DATA_PROVIDER_REGISTRY_V132_AVAILABLE          = True
REAL_DATA_PROVIDER_REGISTRY_AVAILABLE               = True   # spec alias
REAL_DATA_PROVIDER_CAPABILITY_MATRIX                = True
REAL_DATA_PROVIDER_CAPABILITY_MATRIX_AVAILABLE      = True   # spec alias
REAL_DATA_PROVIDER_CACHE_AVAILABLE                  = True
REAL_DATA_PROVIDER_RETRY_AVAILABLE                  = True
REAL_DATA_PROVIDER_SERVICE_AVAILABLE                = True
REAL_DATA_PROVIDER_PROVENANCE_V132                  = True
REAL_DATA_PROVIDER_MERGER_AVAILABLE                 = True
LOCAL_FILE_PROVIDER_ADAPTER_AVAILABLE               = True
LOCAL_REPO_PROVIDER_ADAPTER_AVAILABLE               = True
REAL_DATA_PROVIDER_LIVE_CONNECTION_AVAILABLE        = False  # ALWAYS FALSE
REAL_DATA_PROVIDER_AUTO_DOWNLOAD_ENABLED            = False  # ALWAYS FALSE
REAL_DATA_PROVIDER_CREDENTIAL_STORAGE_ENABLED       = False  # ALWAYS FALSE
REAL_DATA_PROVIDER_ORDER_SUBMISSION_ENABLED         = False  # ALWAYS FALSE
REAL_DATA_PROVIDER_MOCK_FALLBACK_ENABLED            = False  # ALWAYS FALSE
# v1.3.3 Coverage Repair Workflow flags
COVERAGE_REPAIR_WORKFLOW_AVAILABLE          = True
COVERAGE_REPAIR_QUEUE_AVAILABLE             = True
COVERAGE_REPAIR_PLANNER_AVAILABLE           = True
COVERAGE_REPAIR_RETRY_AVAILABLE             = True
COVERAGE_REPAIR_AUTO_EXECUTION_ENABLED      = False
COVERAGE_REPAIR_DESTRUCTIVE_ACTIONS_ENABLED = False
COVERAGE_REPAIR_MOCK_FALLBACK_ENABLED       = False
# v1.3.4 Data Freshness Monitor flags
DATA_FRESHNESS_MONITOR_AVAILABLE       = True   # noqa: F811 (overrides v1.1.3 alias)
DATA_FRESHNESS_POLICY_AVAILABLE        = True
TRADING_CALENDAR_AWARE_FRESHNESS       = True
PROVIDER_SLA_MONITOR_AVAILABLE         = True
FRESHNESS_ALERTS_AVAILABLE             = True
FRESHNESS_AUTO_REFRESH_ENABLED         = False
FRESHNESS_AUTO_REPAIR_ENABLED          = False
FRESHNESS_MOCK_FALLBACK_ENABLED        = False
# v1.4.0 Strategy Knowledge Empirical Backtest flags
STRATEGY_KNOWLEDGE_EMPIRICAL_BACKTEST_AVAILABLE = True
STRATEGY_RULE_REGISTRY_AVAILABLE        = True
LOOKAHEAD_BIAS_GUARD_AVAILABLE          = True
WALK_FORWARD_VALIDATION_AVAILABLE       = True
OUT_OF_SAMPLE_VALIDATION_AVAILABLE      = True
TRANSACTION_COST_MODEL_AVAILABLE        = True
SLIPPAGE_MODEL_AVAILABLE                = True
CORPORATE_ACTION_GUARD_AVAILABLE        = True
BACKTEST_REAL_DATA_REQUIRED             = True
BACKTEST_MOCK_FORMAL_CONCLUSION_ALLOWED = False
BACKTEST_AUTO_OPTIMIZATION_ENABLED      = False
BACKTEST_AUTO_TRADING_ENABLED           = False
# v1.4.1 A/B/C Buy Point Validation flags
ABC_BUY_POINT_VALIDATION_AVAILABLE          = True
ABC_BUY_POINT_A_AVAILABLE                   = True
ABC_BUY_POINT_B_AVAILABLE                   = True
ABC_BUY_POINT_C_AVAILABLE                   = True
ABC_BUY_POINT_REGIME_VALIDATION_AVAILABLE   = True
ABC_BUY_POINT_FILTER_ABLATION_AVAILABLE     = True
ABC_BUY_POINT_HOLDING_PERIOD_ANALYSIS_AVAILABLE = True
ABC_BUY_POINT_STOP_LOSS_ANALYSIS_AVAILABLE  = True
ABC_BUY_POINT_FORMAL_CONCLUSION_REQUIRES_REAL_DATA = True
ABC_BUY_POINT_MOCK_FORMAL_CONCLUSION_ALLOWED = False
ABC_BUY_POINT_AUTO_OPTIMIZATION_ENABLED     = False
ABC_BUY_POINT_AUTO_TRADING_ENABLED          = False
# v1.4.2 Strategy Robustness & Regime Validation flags
STRATEGY_ROBUSTNESS_VALIDATION_AVAILABLE       = True
REGIME_ROBUSTNESS_VALIDATION_AVAILABLE         = True
PARAMETER_SENSITIVITY_ANALYSIS_AVAILABLE       = True
COST_STRESS_TEST_AVAILABLE                     = True
BOOTSTRAP_CONFIDENCE_AVAILABLE                 = True
MONTE_CARLO_TRADE_ORDER_AVAILABLE              = True
CROSS_SECTIONAL_ROBUSTNESS_AVAILABLE           = True
INDUSTRY_ROBUSTNESS_AVAILABLE                  = True
STRATEGY_DECAY_DETECTION_AVAILABLE             = True
ROBUSTNESS_FORMAL_CONCLUSION_REQUIRES_REAL_DATA = True
ROBUSTNESS_MOCK_FORMAL_CONCLUSION_ALLOWED      = False
ROBUSTNESS_AUTO_OPTIMIZATION_ENABLED          = False
ROBUSTNESS_AUTO_TRADING_ENABLED               = False

# v1.3.9 Research Foundation Stable Rollup flags
RESEARCH_FOUNDATION_STABLE                 = True
RESEARCH_FOUNDATION_STABLE_ROLLUP_AVAILABLE = True
REAL_DATA_QUALITY_AVAILABLE                = True
UNIVERSE_EXPANSION_AVAILABLE               = True
EMPIRICAL_BACKTEST_AVAILABLE               = True
STRATEGY_ROBUSTNESS_AVAILABLE              = True
CANONICAL_VERSION_ALIGNMENT_AVAILABLE      = True
PUBLIC_DATA_PROVIDER_INTEGRATION_STARTED   = True   # was False
TWSE_PROVIDER_AVAILABLE                    = True
TPEX_PROVIDER_AVAILABLE                    = True
MOPS_PROVIDER_AVAILABLE                    = True
DATA_GOV_TW_PROVIDER_AVAILABLE             = True
FORUM_INTELLIGENCE_AVAILABLE               = False
AUTO_OPTIMIZATION_ENABLED                  = False

# v1.4.0 TWSE Provider flags
TWSE_PROVIDER_OFFICIAL_SOURCE_ONLY         = True
TWSE_PROVIDER_OPENAPI_AVAILABLE            = True
TWSE_PROVIDER_HISTORICAL_REPORT_AVAILABLE  = True
TWSE_SECURITY_MASTER_AVAILABLE             = True
TWSE_DAILY_OHLCV_AVAILABLE                 = True
TWSE_MARKET_SUMMARY_AVAILABLE              = True
TWSE_INSTITUTIONAL_AVAILABLE               = True
TWSE_MARGIN_AVAILABLE                      = True
TWSE_INDEX_AVAILABLE                       = True
TWSE_TRADING_CALENDAR_AVAILABLE            = True
TWSE_CORPORATE_ACTION_PREVIEW_AVAILABLE    = True
TWSE_REALTIME_AVAILABLE                    = False  # ALWAYS FALSE
TWSE_BROKER_EXECUTION_AVAILABLE            = False  # ALWAYS FALSE
TWSE_AUTO_DOWNLOAD_ENABLED                 = False  # ALWAYS FALSE
TWSE_MOCK_FALLBACK_ENABLED                 = False  # ALWAYS FALSE

# v1.4.1 TPEx Provider flags
TPEX_PROVIDER_OFFICIAL_SOURCE_ONLY         = True
TPEX_PROVIDER_OPENAPI_AVAILABLE            = True
TPEX_PROVIDER_HISTORICAL_REPORT_AVAILABLE  = True
TPEX_SECURITY_MASTER_AVAILABLE             = True
TPEX_DAILY_OHLCV_AVAILABLE                 = True
TPEX_MARKET_SUMMARY_AVAILABLE              = True
TPEX_INSTITUTIONAL_AVAILABLE               = True
TPEX_MARGIN_AVAILABLE                      = True
TPEX_INDEX_AVAILABLE                       = True
TPEX_TRADING_CALENDAR_AVAILABLE            = True
TPEX_SUSPENSION_RESUMPTION_AVAILABLE       = True
TPEX_CORPORATE_ACTION_PREVIEW_AVAILABLE    = True
TPEX_VALUATION_AVAILABLE                   = True
TPEX_REALTIME_AVAILABLE                    = False  # ALWAYS FALSE
TPEX_BROKER_EXECUTION_AVAILABLE            = False  # ALWAYS FALSE
TPEX_AUTO_DOWNLOAD_ENABLED                 = False  # ALWAYS FALSE
TPEX_MOCK_FALLBACK_ENABLED                 = False  # ALWAYS FALSE

# v1.4.2 MOPS Provider flags
MOPS_PROVIDER_OFFICIAL_SOURCE_ONLY         = True
MOPS_PROVIDER_FINANCIAL_DISCLOSURE         = True
MOPS_COMPANY_PROFILE_AVAILABLE             = True
MOPS_MONTHLY_REVENUE_AVAILABLE             = True
MOPS_FINANCIAL_REPORT_FILING_AVAILABLE     = True
MOPS_BALANCE_SHEET_AVAILABLE               = True
MOPS_INCOME_STATEMENT_AVAILABLE            = True
MOPS_CASH_FLOW_STATEMENT_AVAILABLE         = True
MOPS_EQUITY_STATEMENT_AVAILABLE            = True
MOPS_MATERIAL_INFORMATION_AVAILABLE        = True
MOPS_INVESTOR_CONFERENCE_AVAILABLE         = True
MOPS_XBRL_DOCUMENT_AVAILABLE               = True
MOPS_REVISION_LINEAGE_AVAILABLE            = True
MOPS_POINT_IN_TIME_AVAILABLE               = True
MOPS_DERIVED_METRICS_AVAILABLE             = True
MOPS_CACHE_POLICY_AVAILABLE                = True
MOPS_QUERY_SERVICE_AVAILABLE               = True
MOPS_STORE_AVAILABLE                       = True
MOPS_FINANCIAL_STATEMENTS_AVAILABLE        = True
MOPS_REALTIME_AVAILABLE                    = False  # ALWAYS FALSE
MOPS_BROKER_EXECUTION_AVAILABLE            = False  # ALWAYS FALSE
MOPS_AUTO_DOWNLOAD_ENABLED                 = False  # ALWAYS FALSE
MOPS_MOCK_FALLBACK_ENABLED                 = False  # ALWAYS FALSE

# v1.4.3 data.gov.tw Provider flags
DATA_GOV_TW_PROVIDER_OFFICIAL_SOURCE_ONLY      = True
DATA_GOV_TW_ALLOWLIST_REQUIRED                 = True
DATA_GOV_TW_ALLOWLIST_SYSTEM_AVAILABLE         = True
DATA_GOV_TW_LICENSE_VALIDATOR_AVAILABLE        = True
DATA_GOV_TW_SCHEMA_CONTRACT_AVAILABLE          = True
DATA_GOV_TW_JSON_ADAPTER_AVAILABLE             = True
DATA_GOV_TW_CSV_ADAPTER_AVAILABLE              = True
DATA_GOV_TW_XML_ADAPTER_AVAILABLE              = True
DATA_GOV_TW_ZIP_ADAPTER_AVAILABLE              = True
DATA_GOV_TW_OAS_ADAPTER_AVAILABLE              = True
DATA_GOV_TW_REVISION_TRACKING_AVAILABLE        = True
DATA_GOV_TW_LINEAGE_AVAILABLE                  = True
DATA_GOV_TW_FRESHNESS_POLICY_AVAILABLE         = True
DATA_GOV_TW_CACHE_POLICY_AVAILABLE             = True
DATA_GOV_TW_STORE_AVAILABLE                    = True
DATA_GOV_TW_QUERY_SERVICE_AVAILABLE            = True
DATA_GOV_TW_CATALOG_SERVICE_AVAILABLE          = True
DATA_GOV_TW_POINT_IN_TIME_AVAILABLE            = True
DATA_GOV_TW_GOVERNMENT_OBSERVATION_MODEL       = True
DATA_GOV_TW_ZIP_BOMB_PROTECTION_AVAILABLE      = True
DATA_GOV_TW_PATH_TRAVERSAL_PROTECTION_AVAILABLE = True
DATA_GOV_TW_REALTIME_AVAILABLE                 = False  # ALWAYS FALSE
DATA_GOV_TW_BROKER_EXECUTION_AVAILABLE         = False  # ALWAYS FALSE
DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED              = False  # ALWAYS FALSE
DATA_GOV_TW_AUTO_DISCOVERY_ENABLED             = False  # ALWAYS FALSE
DATA_GOV_TW_MOCK_FALLBACK_ENABLED              = False  # ALWAYS FALSE
DATA_GOV_TW_CAN_OVERRIDE_PRIMARY_PROVIDER      = False  # ALWAYS FALSE
DATA_GOV_TW_WILDCARD_ALLOWLIST_ENABLED         = False  # ALWAYS FALSE
DATA_GOV_TW_ALLOW_ALL_MODE_ENABLED             = False  # ALWAYS FALSE
DATA_GOV_TW_FORMAL_USE_ALLOWED_DEFAULT         = False  # ALWAYS FALSE

# v1.4.4 FinMind Adapter Hardening flags
FINMIND_ADAPTER_AVAILABLE               = True
FINMIND_ADAPTER_HARDENED                = True
FINMIND_API_V4_AVAILABLE                = True
FINMIND_SECONDARY_AGGREGATOR            = True
FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER   = False
FINMIND_SILENT_FALLBACK_ENABLED         = False
FINMIND_MOCK_FALLBACK_ENABLED           = False
FINMIND_AUTO_DOWNLOAD_ENABLED           = False
FINMIND_AUTO_DISCOVERY_ENABLED          = False
FINMIND_TOKEN_OPTIONAL                  = True
FINMIND_TOKEN_STORAGE_SECURE            = True
FINMIND_QUOTA_TRACKING_AVAILABLE        = True
FINMIND_RATE_LIMIT_HANDLING_AVAILABLE   = True
FINMIND_SCHEMA_DRIFT_DETECTION_AVAILABLE = True
FINMIND_DATASET_ALLOWLIST_REQUIRED      = True
FINMIND_POINT_IN_TIME_GUARD_AVAILABLE   = True
FINMIND_SOURCE_CONFLICT_DETECTION_AVAILABLE = True
FINMIND_REALTIME_FORMAL_USE_ALLOWED     = False
FINMIND_BROKER_EXECUTION_AVAILABLE      = False

# v1.4.5 Source Lineage & Rate Limit flags
SOURCE_LINEAGE_AVAILABLE                    = True
CENTRAL_LINEAGE_REGISTRY_AVAILABLE          = True
REQUEST_LEDGER_AVAILABLE                    = True
FETCH_RUN_AUDIT_AVAILABLE                   = True
CACHE_LINEAGE_AVAILABLE                     = True
CONFLICT_LINEAGE_AVAILABLE                  = True
PROVENANCE_COMPLETENESS_GATE_AVAILABLE      = True
SOURCE_AUTHORITY_HIERARCHY_AVAILABLE        = True
CENTRAL_RATE_LIMIT_MANAGER_AVAILABLE        = True
HOST_LEVEL_RATE_LIMIT_AVAILABLE             = True
PROVIDER_REQUEST_BUDGET_AVAILABLE           = True
ENDPOINT_REQUEST_POLICY_AVAILABLE           = True
QUOTA_EVIDENCE_AVAILABLE                    = True
RETRY_AFTER_HANDLING_AVAILABLE              = True
BACKOFF_AUDIT_AVAILABLE                     = True
CROSS_PROCESS_LEDGER_AVAILABLE              = True
RATE_LIMIT_DASHBOARD_AVAILABLE              = True
RATE_LIMIT_AUTO_BYPASS_ENABLED              = False  # ALWAYS FALSE
TOKEN_ROTATION_ENABLED                      = False  # ALWAYS FALSE
PROXY_ROTATION_ENABLED                      = False  # ALWAYS FALSE
MULTI_ACCOUNT_LIMIT_BYPASS_ENABLED          = False  # ALWAYS FALSE
PRIMARY_SOURCE_OVERRIDE_ENABLED             = False  # ALWAYS FALSE


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
    # v1.2.3 flags
    print(f"  Replay Scoring Available: {REPLAY_SCORING_AVAILABLE}")
    print(f"  Process Outcome Separation Available: {PROCESS_OUTCOME_SEPARATION_AVAILABLE}")
    print(f"  Mistake Taxonomy Available: {MISTAKE_TAXONOMY_AVAILABLE}")
    print(f"  Mistake Review Available: {MISTAKE_REVIEW_AVAILABLE}")
    print(f"  Outcome Reveal Available: {OUTCOME_REVEAL_AVAILABLE}")
    print(f"  Plan Adherence Available: {PLAN_ADHERENCE_AVAILABLE}")
    print(f"  Auto Outcome Reveal Enabled: {AUTO_OUTCOME_REVEAL_ENABLED}")
    print(f"  Auto Mistake Confirmation Enabled: {AUTO_MISTAKE_CONFIRMATION_ENABLED}")
    print(f"  Auto Strategy Change Enabled: {AUTO_STRATEGY_CHANGE_ENABLED}")
    print(f"  Auto Score To Trade Enabled: {AUTO_SCORE_TO_TRADE_ENABLED}")
    # v1.2.4 flags
    print(f"  Strategy Knowledge Replay Available: {STRATEGY_KNOWLEDGE_REPLAY_AVAILABLE}")
    print(f"  Strategy Signal Timeline Available: {STRATEGY_SIGNAL_TIMELINE_AVAILABLE}")
    print(f"  Strategy Rule Review Available: {STRATEGY_RULE_REVIEW_AVAILABLE}")
    print(f"  Strategy Agreement Analysis Available: {STRATEGY_AGREEMENT_ANALYSIS_AVAILABLE}")
    print(f"  Strategy Conflict Analysis Available: {STRATEGY_CONFLICT_ANALYSIS_AVAILABLE}")
    print(f"  ABC Buy Point Replay Available: {ABC_BUY_POINT_REPLAY_AVAILABLE}")
    print(f"  Auto Strategy Decision Enabled: {AUTO_STRATEGY_DECISION_ENABLED}")
    print(f"  Auto Strategy Execution Enabled: {AUTO_STRATEGY_EXECUTION_ENABLED}")
    print(f"  Auto Strategy Weight Change Enabled: {AUTO_STRATEGY_WEIGHT_CHANGE_ENABLED}")
    print(f"  Auto Strategy Mistake Confirmation Enabled: {AUTO_STRATEGY_MISTAKE_CONFIRMATION_ENABLED}")
    # v1.2.5 flags
    print(f"  Multi Timeframe Replay Available: {MULTI_TIMEFRAME_REPLAY_AVAILABLE}")
    print(f"  MTF Synchronized Clock Available: {MTF_SYNCHRONIZED_CLOCK_AVAILABLE}")
    print(f"  MTF Future Firewall Available: {MTF_FUTURE_FIREWALL_AVAILABLE}")
    print(f"  MTF Point In Time Verifier Available: {MTF_POINT_IN_TIME_VERIFIER_AVAILABLE}")
    print(f"  MTF Agreement Analysis Available: {MTF_AGREEMENT_ANALYSIS_AVAILABLE}")
    print(f"  MTF Conflict Analysis Available: {MTF_CONFLICT_ANALYSIS_AVAILABLE}")
    print(f"  MTF Bar Aggregation Available: {MTF_BAR_AGGREGATION_AVAILABLE}")
    print(f"  MTF Batch Runner Available: {MTF_BATCH_RUNNER_AVAILABLE}")
    print(f"  MTF Partial Bar Protection Available: {MTF_PARTIAL_BAR_PROTECTION_AVAILABLE}")
    print(f"  MTF Past Only Asof Join: {MTF_PAST_ONLY_ASOF_JOIN}")
    print(f"  MTF No Bfill: {MTF_NO_BFILL}")
    print(f"  MTF No Centered Rolling: {MTF_NO_CENTERED_ROLLING}")
    print(f"  MTF No Future Klines: {MTF_NO_FUTURE_KLINES}")
    print(f"  MTF Daily No Fake Intraday: {MTF_DAILY_NO_FAKE_INTRADAY}")
    print(f"  MTF Real No Mock Fallback: {MTF_REAL_NO_MOCK_FALLBACK}")
    print(f"  MTF Auto Trade Enabled: {MTF_AUTO_TRADE_ENABLED}")
    print(f"  MTF Auto Block Enabled: {MTF_AUTO_BLOCK_ENABLED}")
    print(f"  MTF Auto Decision Enabled: {MTF_AUTO_DECISION_ENABLED}")
    print(f"  MTF Batch Auto Execute Enabled: {MTF_BATCH_AUTO_EXECUTE_ENABLED}")
    # v1.2.6 flags
    print(f"  Replay Review Dashboard Available: {REPLAY_REVIEW_DASHBOARD_AVAILABLE}")
    print(f"  Replay Review Queue Available: {REPLAY_REVIEW_QUEUE_AVAILABLE}")
    print(f"  Replay Review Progress Available: {REPLAY_REVIEW_PROGRESS_AVAILABLE}")
    print(f"  Replay Cross Module Navigation Available: {REPLAY_CROSS_MODULE_NAVIGATION_AVAILABLE}")
    print(f"  Replay Review Comparison Available: {REPLAY_REVIEW_COMPARISON_AVAILABLE}")
    print(f"  Replay Batch Review Available: {REPLAY_BATCH_REVIEW_AVAILABLE}")
    print(f"  Auto Review Complete Enabled: {AUTO_REVIEW_COMPLETE_ENABLED}")
    print(f"  Auto Outcome Reveal Enabled: {AUTO_OUTCOME_REVEAL_ENABLED}")
    print(f"  Auto Mistake Confirmation Enabled: {AUTO_MISTAKE_CONFIRMATION_ENABLED}")
    print(f"  Auto Decision Creation Enabled: {AUTO_DECISION_CREATION_ENABLED}")
    print(f"  Auto Strategy Change Enabled: {AUTO_STRATEGY_CHANGE_ENABLED}")
    print(f"  Auto Score To Trade Enabled: {AUTO_SCORE_TO_TRADE_ENABLED}")
    print(f"  Replay Trade Execution Enabled: {REPLAY_TRADE_EXECUTION_ENABLED}")
    # v1.2.7 flags
    print(f"  Replay Challenge Mode Available: {REPLAY_CHALLENGE_MODE_AVAILABLE}")
    print(f"  Replay Challenge Library Available: {REPLAY_CHALLENGE_LIBRARY_AVAILABLE}")
    print(f"  Timed Challenge Available: {TIMED_CHALLENGE_AVAILABLE}")
    print(f"  Hidden Future Challenge Available: {HIDDEN_FUTURE_CHALLENGE_AVAILABLE}")
    print(f"  Challenge Difficulty Available: {CHALLENGE_DIFFICULTY_AVAILABLE}")
    print(f"  Challenge Personal Leaderboard Available: {CHALLENGE_PERSONAL_LEADERBOARD_AVAILABLE}")
    print(f"  Challenge Mistake Training Available: {CHALLENGE_MISTAKE_TRAINING_AVAILABLE}")
    print(f"  Public Leaderboard Enabled: {PUBLIC_LEADERBOARD_ENABLED}")
    print(f"  Network Score Submission Enabled: {NETWORK_SCORE_SUBMISSION_ENABLED}")
    print(f"  Auto Challenge Decision Enabled: {AUTO_CHALLENGE_DECISION_ENABLED}")
    print(f"  Auto Challenge Outcome Reveal Enabled: {AUTO_CHALLENGE_OUTCOME_REVEAL_ENABLED}")
    print(f"  Auto Challenge Mistake Confirmation Enabled: {AUTO_CHALLENGE_MISTAKE_CONFIRMATION_ENABLED}")
    # v1.2.8 flags
    print(f"  Replay Dataset Registry Available: {REPLAY_DATASET_REGISTRY_AVAILABLE}")
    print(f"  Replay Session Registry Available: {REPLAY_SESSION_REGISTRY_AVAILABLE}")
    print(f"  Dataset Versioning Available: {DATASET_VERSIONING_AVAILABLE}")
    print(f"  Dataset Fingerprint Available: {DATASET_FINGERPRINT_AVAILABLE}")
    print(f"  Session Fingerprint Available: {SESSION_FINGERPRINT_AVAILABLE}")
    print(f"  Dataset Lineage Available: {DATASET_LINEAGE_AVAILABLE}")
    print(f"  Session Lineage Available: {SESSION_LINEAGE_AVAILABLE}")
    print(f"  Portable Replay Package Available: {PORTABLE_REPLAY_PACKAGE_AVAILABLE}")
    print(f"  Cross Computer Path Remap Available: {CROSS_COMPUTER_PATH_REMAP_AVAILABLE}")
    print(f"  Registry Repair Preview Available: {REGISTRY_REPAIR_PREVIEW_AVAILABLE}")
    print(f"  Auto Dataset Overwrite Enabled: {AUTO_DATASET_OVERWRITE_ENABLED}")
    print(f"  Auto Dataset Repair Enabled: {AUTO_DATASET_REPAIR_ENABLED}")
    print(f"  Auto Session Rebind Enabled: {AUTO_SESSION_REBIND_ENABLED}")
    print(f"  Auto Package Import Enabled: {AUTO_PACKAGE_IMPORT_ENABLED}")
    print(f"  Auto Registry Conflict Resolution Enabled: {AUTO_REGISTRY_CONFLICT_RESOLUTION_ENABLED}")
    print(f"  Replay Trade Execution Enabled: {REPLAY_TRADE_EXECUTION_ENABLED}")
    # v1.2.9 flags
    print(f"  Stable Rollup: {STABLE_ROLLUP}")
    print(f"  Replay Training Line Complete: {REPLAY_TRAINING_LINE_COMPLETE}")
    print(f"  Replay Stable Health Available: {REPLAY_STABLE_HEALTH_AVAILABLE}")
    print(f"  Replay Stable Manifest Available: {REPLAY_STABLE_MANIFEST_AVAILABLE}")
    print(f"  Replay Capability Matrix Available: {REPLAY_CAPABILITY_MATRIX_AVAILABLE}")
    print(f"  Replay Cross Module Contract Check Available: {REPLAY_CROSS_MODULE_CONTRACT_CHECK_AVAILABLE}")
    print(f"  Replay Release Gate Available: {REPLAY_RELEASE_GATE_AVAILABLE}")
    print(f"  Auto Replay Decision Enabled: {AUTO_REPLAY_DECISION_ENABLED}")
    print(f"  Auto Replay Execution Enabled: {AUTO_REPLAY_EXECUTION_ENABLED}")
    print(f"  Auto Conflict Resolution Enabled: {AUTO_CONFLICT_RESOLUTION_ENABLED}")
    # v1.3.0 flags
    print(f"  Real Data Quality Foundation: {REAL_DATA_QUALITY_FOUNDATION}")
    print(f"  Real Data Quality Validator: {REAL_DATA_QUALITY_VALIDATOR}")
    print(f"  Data Completeness Gate Profiles: {DATA_COMPLETENESS_GATE_PROFILES}")
    print(f"  Quality Score 0-100: {QUALITY_SCORE_0_100}")
    print(f"  Data Provenance Tracking: {DATA_PROVENANCE_TRACKING}")
    print(f"  Mock Fallback Enabled: {MOCK_FALLBACK_ENABLED}")
    print(f"  Real No Mock Fallback: {REAL_NO_MOCK_FALLBACK}")
    print(f"  Mock Demo Only Label Enforced: {MOCK_DEMO_ONLY_LABEL_ENFORCED}")
    print(f"  Real Data Quality CLI Enabled: {REAL_DATA_QUALITY_CLI_ENABLED}")
    print(f"  Real Data Quality GUI Panel: {REAL_DATA_QUALITY_GUI_PANEL}")
    print(f"  Real Data Quality Health: {REAL_DATA_QUALITY_HEALTH}")
    print(f"  No Real Orders: {NO_REAL_ORDERS}")
    print(f"  Broker Execution Enabled: {BROKER_EXECUTION_ENABLED}")
    print(f"  Production Trading BLOCKED: {PRODUCTION_TRADING_BLOCKED}")
    # v1.3.1 Universe Expansion Foundation flags
    print(f"  Universe Registry Available: {UNIVERSE_REGISTRY_AVAILABLE}")
    print(f"  Universe Coverage Available: {UNIVERSE_COVERAGE_AVAILABLE}")
    print(f"  Universe Batch Quality Scan Available: {UNIVERSE_BATCH_QUALITY_SCAN_AVAILABLE}")
    print(f"  Universe Real API Connected: {UNIVERSE_REAL_API_CONNECTED}")
    print(f"  Universe Auto Download Enabled: {UNIVERSE_AUTO_DOWNLOAD_ENABLED}")
    print(f"  Mock Fallback Enabled: {MOCK_FALLBACK_ENABLED}")
    # v1.3.2 Real Data Provider Adapter Foundation flags
    print(f"  Provider Adapter Available: {REAL_DATA_PROVIDER_ADAPTER_AVAILABLE}")
    print(f"  Provider Registry Available: {REAL_DATA_PROVIDER_REGISTRY_AVAILABLE}")
    print(f"  Provider Capability Matrix Available: {REAL_DATA_PROVIDER_CAPABILITY_MATRIX_AVAILABLE}")
    print(f"  Provider Cache Available: {REAL_DATA_PROVIDER_CACHE_AVAILABLE}")
    print(f"  Provider Retry Available: {REAL_DATA_PROVIDER_RETRY_AVAILABLE}")
    print(f"  Provider Live Connection Available: {REAL_DATA_PROVIDER_LIVE_CONNECTION_AVAILABLE}")
    print(f"  Provider Auto Download Enabled: {REAL_DATA_PROVIDER_AUTO_DOWNLOAD_ENABLED}")
    print(f"  Provider Credential Storage Enabled: {REAL_DATA_PROVIDER_CREDENTIAL_STORAGE_ENABLED}")
    print(f"  No Real Orders: {NO_REAL_ORDERS}")
    print(f"  Broker Execution Enabled: {BROKER_EXECUTION_ENABLED}")
    print(f"  Production Trading BLOCKED: {PRODUCTION_TRADING_BLOCKED}")
    print(f"  Mock Fallback Enabled: {MOCK_FALLBACK_ENABLED}")
    # v1.3.3 Coverage Repair Workflow flags
    print(f"  Coverage Repair Workflow Available: {COVERAGE_REPAIR_WORKFLOW_AVAILABLE}")
    print(f"  Coverage Repair Queue Available: {COVERAGE_REPAIR_QUEUE_AVAILABLE}")
    print(f"  Coverage Repair Planner Available: {COVERAGE_REPAIR_PLANNER_AVAILABLE}")
    print(f"  Coverage Repair Retry Available: {COVERAGE_REPAIR_RETRY_AVAILABLE}")
    print(f"  Coverage Repair Auto Execution Enabled: {COVERAGE_REPAIR_AUTO_EXECUTION_ENABLED}")
    print(f"  Coverage Repair Destructive Actions Enabled: {COVERAGE_REPAIR_DESTRUCTIVE_ACTIONS_ENABLED}")
    print(f"  Coverage Repair Mock Fallback Enabled: {COVERAGE_REPAIR_MOCK_FALLBACK_ENABLED}")
    # v1.3.4 Data Freshness Monitor flags
    print(f"  Data Freshness Monitor Available:      {DATA_FRESHNESS_MONITOR_AVAILABLE}")
    print(f"  Data Freshness Policy Available:       {DATA_FRESHNESS_POLICY_AVAILABLE}")
    print(f"  Trading Calendar Aware Freshness:      {TRADING_CALENDAR_AWARE_FRESHNESS}")
    print(f"  Provider SLA Monitor Available:        {PROVIDER_SLA_MONITOR_AVAILABLE}")
    print(f"  Freshness Alerts Available:            {FRESHNESS_ALERTS_AVAILABLE}")
    print(f"  Freshness Auto Refresh Enabled:        {FRESHNESS_AUTO_REFRESH_ENABLED}")
    print(f"  Freshness Auto Repair Enabled:         {FRESHNESS_AUTO_REPAIR_ENABLED}")
    print(f"  Freshness Mock Fallback Enabled:       {FRESHNESS_MOCK_FALLBACK_ENABLED}")
    # v1.4.0 Strategy Knowledge Empirical Backtest flags
    print(f"  Strategy Knowledge Empirical Backtest Available: {STRATEGY_KNOWLEDGE_EMPIRICAL_BACKTEST_AVAILABLE}")
    print(f"  Strategy Rule Registry Available: {STRATEGY_RULE_REGISTRY_AVAILABLE}")
    print(f"  Lookahead Bias Guard Available: {LOOKAHEAD_BIAS_GUARD_AVAILABLE}")
    print(f"  Walk Forward Validation Available: {WALK_FORWARD_VALIDATION_AVAILABLE}")
    print(f"  Out Of Sample Validation Available: {OUT_OF_SAMPLE_VALIDATION_AVAILABLE}")
    print(f"  Transaction Cost Model Available: {TRANSACTION_COST_MODEL_AVAILABLE}")
    print(f"  Slippage Model Available: {SLIPPAGE_MODEL_AVAILABLE}")
    print(f"  Corporate Action Guard Available: {CORPORATE_ACTION_GUARD_AVAILABLE}")
    print(f"  Backtest Real Data Required: {BACKTEST_REAL_DATA_REQUIRED}")
    print(f"  Mock Formal Conclusion Allowed: {BACKTEST_MOCK_FORMAL_CONCLUSION_ALLOWED}")
    print(f"  Backtest Auto Optimization Enabled: {BACKTEST_AUTO_OPTIMIZATION_ENABLED}")
    print(f"  Backtest Auto Trading Enabled: {BACKTEST_AUTO_TRADING_ENABLED}")
    # v1.4.1 A/B/C Buy Point Validation flags
    print(f"  A/B/C Validation Available: {ABC_BUY_POINT_VALIDATION_AVAILABLE}")
    print(f"  A Buy Point Available: {ABC_BUY_POINT_A_AVAILABLE}")
    print(f"  B Buy Point Available: {ABC_BUY_POINT_B_AVAILABLE}")
    print(f"  C Buy Point Available: {ABC_BUY_POINT_C_AVAILABLE}")
    print(f"  Regime Validation Available: {ABC_BUY_POINT_REGIME_VALIDATION_AVAILABLE}")
    print(f"  Filter Ablation Available: {ABC_BUY_POINT_FILTER_ABLATION_AVAILABLE}")
    print(f"  Holding Period Analysis Available: {ABC_BUY_POINT_HOLDING_PERIOD_ANALYSIS_AVAILABLE}")
    print(f"  Stop Loss Analysis Available: {ABC_BUY_POINT_STOP_LOSS_ANALYSIS_AVAILABLE}")
    print(f"  Formal Conclusion Requires Real Data: {ABC_BUY_POINT_FORMAL_CONCLUSION_REQUIRES_REAL_DATA}")
    print(f"  Mock Formal Conclusion Allowed: {ABC_BUY_POINT_MOCK_FORMAL_CONCLUSION_ALLOWED}")
    print(f"  Auto Optimization Enabled: {ABC_BUY_POINT_AUTO_OPTIMIZATION_ENABLED}")
    print(f"  Auto Trading Enabled: {ABC_BUY_POINT_AUTO_TRADING_ENABLED}")
    print(f"  No Real Orders: {NO_REAL_ORDERS}")
    print(f"  Broker Execution Enabled: {BROKER_EXECUTION_ENABLED}")
    print(f"  Production Trading BLOCKED: {PRODUCTION_TRADING_BLOCKED}")
    # v1.4.2 Strategy Robustness & Regime Validation flags
    print(f"  Strategy Robustness Validation Available: {STRATEGY_ROBUSTNESS_VALIDATION_AVAILABLE}")
    print(f"  Regime Robustness Validation Available: {REGIME_ROBUSTNESS_VALIDATION_AVAILABLE}")
    print(f"  Parameter Sensitivity Analysis Available: {PARAMETER_SENSITIVITY_ANALYSIS_AVAILABLE}")
    print(f"  Cost Stress Test Available: {COST_STRESS_TEST_AVAILABLE}")
    print(f"  Bootstrap Confidence Available: {BOOTSTRAP_CONFIDENCE_AVAILABLE}")
    print(f"  Monte Carlo Trade Order Available: {MONTE_CARLO_TRADE_ORDER_AVAILABLE}")
    print(f"  Cross Sectional Robustness Available: {CROSS_SECTIONAL_ROBUSTNESS_AVAILABLE}")
    print(f"  Industry Robustness Available: {INDUSTRY_ROBUSTNESS_AVAILABLE}")
    print(f"  Strategy Decay Detection Available: {STRATEGY_DECAY_DETECTION_AVAILABLE}")
    print(f"  Robustness Formal Conclusion Requires Real Data: {ROBUSTNESS_FORMAL_CONCLUSION_REQUIRES_REAL_DATA}")
    print(f"  Robustness Mock Formal Conclusion Allowed: {ROBUSTNESS_MOCK_FORMAL_CONCLUSION_ALLOWED}")
    print(f"  Robustness Auto Optimization Enabled: {ROBUSTNESS_AUTO_OPTIMIZATION_ENABLED}")
    print(f"  Robustness Auto Trading Enabled: {ROBUSTNESS_AUTO_TRADING_ENABLED}")
    # v1.3.9 Research Foundation Stable Rollup flags
    print(f"  Research Foundation Stable: {RESEARCH_FOUNDATION_STABLE}")
    print(f"  Research Foundation Stable Rollup Available: {RESEARCH_FOUNDATION_STABLE_ROLLUP_AVAILABLE}")
    print(f"  Real Data Quality Available: {REAL_DATA_QUALITY_AVAILABLE}")
    print(f"  Universe Expansion Available: {UNIVERSE_EXPANSION_AVAILABLE}")
    print(f"  Empirical Backtest Available: {EMPIRICAL_BACKTEST_AVAILABLE}")
    print(f"  A/B/C Buy Point Validation Available: {ABC_BUY_POINT_VALIDATION_AVAILABLE}")
    print(f"  Strategy Robustness Available: {STRATEGY_ROBUSTNESS_AVAILABLE}")
    print(f"  Canonical Version Alignment Available: {CANONICAL_VERSION_ALIGNMENT_AVAILABLE}")
    print(f"  Public Data Provider Integration Started: {PUBLIC_DATA_PROVIDER_INTEGRATION_STARTED}")
    print(f"  TWSE Provider Available: {TWSE_PROVIDER_AVAILABLE}")
    print(f"  TPEx Provider Available: {TPEX_PROVIDER_AVAILABLE}")
    print(f"  MOPS Provider Available: {MOPS_PROVIDER_AVAILABLE}")
    print(f"  data.gov.tw Provider Available: {DATA_GOV_TW_PROVIDER_AVAILABLE}")
    print(f"  Forum Intelligence Available: {FORUM_INTELLIGENCE_AVAILABLE}")
    print(f"  Replay Stable Baseline: {REPLAY_STABLE_BASELINE}")
    print(f"  Mock Fallback Enabled: {MOCK_FALLBACK_ENABLED}")
    print(f"  Auto Optimization Enabled: {AUTO_OPTIMIZATION_ENABLED}")
    print(f"  Auto Trading Enabled: {AUTO_TRADING_ENABLED}")
    # v1.4.0 TWSE Provider flags
    print(f"  TWSE Provider Available: {TWSE_PROVIDER_AVAILABLE}")
    print(f"  Official Source Only: {TWSE_PROVIDER_OFFICIAL_SOURCE_ONLY}")
    print(f"  TWSE OpenAPI Available: {TWSE_PROVIDER_OPENAPI_AVAILABLE}")
    print(f"  TWSE Historical Report Available: {TWSE_PROVIDER_HISTORICAL_REPORT_AVAILABLE}")
    print(f"  TWSE Daily OHLCV Available: {TWSE_DAILY_OHLCV_AVAILABLE}")
    print(f"  TWSE Institutional Available: {TWSE_INSTITUTIONAL_AVAILABLE}")
    print(f"  TWSE Margin Available: {TWSE_MARGIN_AVAILABLE}")
    print(f"  TWSE Index Available: {TWSE_INDEX_AVAILABLE}")
    print(f"  TWSE Trading Calendar Available: {TWSE_TRADING_CALENDAR_AVAILABLE}")
    print(f"  TWSE Real-time Available: {TWSE_REALTIME_AVAILABLE}")
    print(f"  Auto Download Enabled: {TWSE_AUTO_DOWNLOAD_ENABLED}")
    print(f"  TWSE Mock Fallback Enabled: {TWSE_MOCK_FALLBACK_ENABLED}")
    # v1.4.1 TPEx Provider flags
    print(f"  TPEx Provider Available: {TPEX_PROVIDER_AVAILABLE}")
    print(f"  TPEx Official Source Only: {TPEX_PROVIDER_OFFICIAL_SOURCE_ONLY}")
    print(f"  TPEx OpenAPI Available: {TPEX_PROVIDER_OPENAPI_AVAILABLE}")
    print(f"  TPEx Historical Report Available: {TPEX_PROVIDER_HISTORICAL_REPORT_AVAILABLE}")
    print(f"  TPEx Daily OHLCV Available: {TPEX_DAILY_OHLCV_AVAILABLE}")
    print(f"  TPEx Institutional Available: {TPEX_INSTITUTIONAL_AVAILABLE}")
    print(f"  TPEx Margin Available: {TPEX_MARGIN_AVAILABLE}")
    print(f"  TPEx Index Available: {TPEX_INDEX_AVAILABLE}")
    print(f"  TPEx Trading Calendar Available: {TPEX_TRADING_CALENDAR_AVAILABLE}")
    print(f"  TPEx Suspension/Resumption Available: {TPEX_SUSPENSION_RESUMPTION_AVAILABLE}")
    print(f"  TPEx Valuation Available: {TPEX_VALUATION_AVAILABLE}")
    print(f"  TPEx Real-time Available: {TPEX_REALTIME_AVAILABLE}")
    print(f"  TPEx Auto Download Enabled: {TPEX_AUTO_DOWNLOAD_ENABLED}")
    print(f"  TPEx Mock Fallback Enabled: {TPEX_MOCK_FALLBACK_ENABLED}")
    # v1.4.2 MOPS Provider flags
    print(f"  MOPS Provider Available: {MOPS_PROVIDER_AVAILABLE}")
    print(f"  MOPS Official Source Only: {MOPS_PROVIDER_OFFICIAL_SOURCE_ONLY}")
    print(f"  MOPS Financial Disclosure: {MOPS_PROVIDER_FINANCIAL_DISCLOSURE}")
    print(f"  MOPS Company Profile Available: {MOPS_COMPANY_PROFILE_AVAILABLE}")
    print(f"  MOPS Monthly Revenue Available: {MOPS_MONTHLY_REVENUE_AVAILABLE}")
    print(f"  MOPS Financial Report Filing Available: {MOPS_FINANCIAL_REPORT_FILING_AVAILABLE}")
    print(f"  MOPS Balance Sheet Available: {MOPS_BALANCE_SHEET_AVAILABLE}")
    print(f"  MOPS Income Statement Available: {MOPS_INCOME_STATEMENT_AVAILABLE}")
    print(f"  MOPS Cash Flow Statement Available: {MOPS_CASH_FLOW_STATEMENT_AVAILABLE}")
    print(f"  MOPS Equity Statement Available: {MOPS_EQUITY_STATEMENT_AVAILABLE}")
    print(f"  MOPS Material Information Available: {MOPS_MATERIAL_INFORMATION_AVAILABLE}")
    print(f"  MOPS Investor Conference Available: {MOPS_INVESTOR_CONFERENCE_AVAILABLE}")
    print(f"  MOPS XBRL Document Available: {MOPS_XBRL_DOCUMENT_AVAILABLE}")
    print(f"  MOPS Revision Lineage Available: {MOPS_REVISION_LINEAGE_AVAILABLE}")
    print(f"  MOPS Point In Time Available: {MOPS_POINT_IN_TIME_AVAILABLE}")
    print(f"  MOPS Derived Metrics Available: {MOPS_DERIVED_METRICS_AVAILABLE}")
    print(f"  MOPS Cache Policy Available: {MOPS_CACHE_POLICY_AVAILABLE}")
    print(f"  MOPS Query Service Available: {MOPS_QUERY_SERVICE_AVAILABLE}")
    print(f"  MOPS Store Available: {MOPS_STORE_AVAILABLE}")
    print(f"  MOPS Real-time Available: {MOPS_REALTIME_AVAILABLE}")
    print(f"  MOPS Auto Download Enabled: {MOPS_AUTO_DOWNLOAD_ENABLED}")
    print(f"  MOPS Mock Fallback Enabled: {MOPS_MOCK_FALLBACK_ENABLED}")
    # v1.4.3 data.gov.tw Provider flags
    print(f"  data.gov.tw Provider Available: {DATA_GOV_TW_PROVIDER_AVAILABLE}")
    print(f"  data.gov.tw Official Source Only: {DATA_GOV_TW_PROVIDER_OFFICIAL_SOURCE_ONLY}")
    print(f"  data.gov.tw Allowlist Required: {DATA_GOV_TW_ALLOWLIST_REQUIRED}")
    print(f"  data.gov.tw Allowlist System Available: {DATA_GOV_TW_ALLOWLIST_SYSTEM_AVAILABLE}")
    print(f"  data.gov.tw License Validator Available: {DATA_GOV_TW_LICENSE_VALIDATOR_AVAILABLE}")
    print(f"  data.gov.tw Schema Contract Available: {DATA_GOV_TW_SCHEMA_CONTRACT_AVAILABLE}")
    print(f"  data.gov.tw JSON Adapter Available: {DATA_GOV_TW_JSON_ADAPTER_AVAILABLE}")
    print(f"  data.gov.tw CSV Adapter Available: {DATA_GOV_TW_CSV_ADAPTER_AVAILABLE}")
    print(f"  data.gov.tw XML Adapter Available: {DATA_GOV_TW_XML_ADAPTER_AVAILABLE}")
    print(f"  data.gov.tw ZIP Adapter Available: {DATA_GOV_TW_ZIP_ADAPTER_AVAILABLE}")
    print(f"  data.gov.tw OAS Adapter Available: {DATA_GOV_TW_OAS_ADAPTER_AVAILABLE}")
    print(f"  data.gov.tw Revision Tracking Available: {DATA_GOV_TW_REVISION_TRACKING_AVAILABLE}")
    print(f"  data.gov.tw Lineage Available: {DATA_GOV_TW_LINEAGE_AVAILABLE}")
    print(f"  data.gov.tw Freshness Policy Available: {DATA_GOV_TW_FRESHNESS_POLICY_AVAILABLE}")
    print(f"  data.gov.tw Cache Policy Available: {DATA_GOV_TW_CACHE_POLICY_AVAILABLE}")
    print(f"  data.gov.tw Store Available: {DATA_GOV_TW_STORE_AVAILABLE}")
    print(f"  data.gov.tw Query Service Available: {DATA_GOV_TW_QUERY_SERVICE_AVAILABLE}")
    print(f"  data.gov.tw Catalog Service Available: {DATA_GOV_TW_CATALOG_SERVICE_AVAILABLE}")
    print(f"  data.gov.tw Point-In-Time Available: {DATA_GOV_TW_POINT_IN_TIME_AVAILABLE}")
    print(f"  data.gov.tw Government Observation Model: {DATA_GOV_TW_GOVERNMENT_OBSERVATION_MODEL}")
    print(f"  data.gov.tw ZIP Bomb Protection: {DATA_GOV_TW_ZIP_BOMB_PROTECTION_AVAILABLE}")
    print(f"  data.gov.tw Path Traversal Protection: {DATA_GOV_TW_PATH_TRAVERSAL_PROTECTION_AVAILABLE}")
    print(f"  data.gov.tw Real-time Available: {DATA_GOV_TW_REALTIME_AVAILABLE}")
    print(f"  data.gov.tw Broker Execution Available: {DATA_GOV_TW_BROKER_EXECUTION_AVAILABLE}")
    print(f"  data.gov.tw Auto Download Enabled: {DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED}")
    print(f"  data.gov.tw Auto Discovery Enabled: {DATA_GOV_TW_AUTO_DISCOVERY_ENABLED}")
    print(f"  data.gov.tw Mock Fallback Enabled: {DATA_GOV_TW_MOCK_FALLBACK_ENABLED}")
    print(f"  data.gov.tw Can Override Primary Provider: {DATA_GOV_TW_CAN_OVERRIDE_PRIMARY_PROVIDER}")
    print(f"  data.gov.tw Wildcard Allowlist Enabled: {DATA_GOV_TW_WILDCARD_ALLOWLIST_ENABLED}")
    print(f"  data.gov.tw Allow All Mode Enabled: {DATA_GOV_TW_ALLOW_ALL_MODE_ENABLED}")
    print(f"  data.gov.tw Formal Use Allowed Default: {DATA_GOV_TW_FORMAL_USE_ALLOWED_DEFAULT}")
    # v1.4.4 FinMind Adapter Hardening flags
    print(f"  FinMind Adapter Available: {FINMIND_ADAPTER_AVAILABLE}")
    print(f"  FinMind Adapter Hardened: {FINMIND_ADAPTER_HARDENED}")
    print(f"  FinMind API v4 Available: {FINMIND_API_V4_AVAILABLE}")
    print(f"  FinMind Secondary Aggregator: {FINMIND_SECONDARY_AGGREGATOR}")
    print(f"  FinMind Can Override Primary Provider: {FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER}")
    print(f"  FinMind Silent Fallback Enabled: {FINMIND_SILENT_FALLBACK_ENABLED}")
    print(f"  FinMind Mock Fallback Enabled: {FINMIND_MOCK_FALLBACK_ENABLED}")
    print(f"  FinMind Auto Download Enabled: {FINMIND_AUTO_DOWNLOAD_ENABLED}")
    print(f"  FinMind Auto Discovery Enabled: {FINMIND_AUTO_DISCOVERY_ENABLED}")
    print(f"  FinMind Token Optional: {FINMIND_TOKEN_OPTIONAL}")
    print(f"  FinMind Token Storage Secure: {FINMIND_TOKEN_STORAGE_SECURE}")
    print(f"  FinMind Quota Tracking Available: {FINMIND_QUOTA_TRACKING_AVAILABLE}")
    print(f"  FinMind Rate Limit Handling Available: {FINMIND_RATE_LIMIT_HANDLING_AVAILABLE}")
    print(f"  FinMind Schema Drift Detection Available: {FINMIND_SCHEMA_DRIFT_DETECTION_AVAILABLE}")
    print(f"  FinMind Dataset Allowlist Required: {FINMIND_DATASET_ALLOWLIST_REQUIRED}")
    print(f"  FinMind Point-in-Time Guard Available: {FINMIND_POINT_IN_TIME_GUARD_AVAILABLE}")
    print(f"  FinMind Source Conflict Detection Available: {FINMIND_SOURCE_CONFLICT_DETECTION_AVAILABLE}")
    print(f"  FinMind Realtime Formal Use Allowed: {FINMIND_REALTIME_FORMAL_USE_ALLOWED}")
    print(f"  FinMind Broker Execution Available: {FINMIND_BROKER_EXECUTION_AVAILABLE}")
    # v1.4.5 Source Lineage & Rate Limit flags
    print(f"  Source Lineage Available: {SOURCE_LINEAGE_AVAILABLE}")
    print(f"  Central Lineage Registry Available: {CENTRAL_LINEAGE_REGISTRY_AVAILABLE}")
    print(f"  Request Ledger Available: {REQUEST_LEDGER_AVAILABLE}")
    print(f"  Fetch Run Audit Available: {FETCH_RUN_AUDIT_AVAILABLE}")
    print(f"  Cache Lineage Available: {CACHE_LINEAGE_AVAILABLE}")
    print(f"  Conflict Lineage Available: {CONFLICT_LINEAGE_AVAILABLE}")
    print(f"  Provenance Completeness Gate Available: {PROVENANCE_COMPLETENESS_GATE_AVAILABLE}")
    print(f"  Source Authority Hierarchy Available: {SOURCE_AUTHORITY_HIERARCHY_AVAILABLE}")
    print(f"  Central Rate Limit Manager Available: {CENTRAL_RATE_LIMIT_MANAGER_AVAILABLE}")
    print(f"  Host Level Rate Limit Available: {HOST_LEVEL_RATE_LIMIT_AVAILABLE}")
    print(f"  Provider Request Budget Available: {PROVIDER_REQUEST_BUDGET_AVAILABLE}")
    print(f"  Endpoint Request Policy Available: {ENDPOINT_REQUEST_POLICY_AVAILABLE}")
    print(f"  Quota Evidence Available: {QUOTA_EVIDENCE_AVAILABLE}")
    print(f"  Retry After Handling Available: {RETRY_AFTER_HANDLING_AVAILABLE}")
    print(f"  Backoff Audit Available: {BACKOFF_AUDIT_AVAILABLE}")
    print(f"  Cross Process Ledger Available: {CROSS_PROCESS_LEDGER_AVAILABLE}")
    print(f"  Rate Limit Dashboard Available: {RATE_LIMIT_DASHBOARD_AVAILABLE}")
    print(f"  Rate Limit Auto Bypass Enabled: {RATE_LIMIT_AUTO_BYPASS_ENABLED}")
    print(f"  Token Rotation Enabled: {TOKEN_ROTATION_ENABLED}")
    print(f"  Proxy Rotation Enabled: {PROXY_ROTATION_ENABLED}")
    print(f"  Multi Account Limit Bypass Enabled: {MULTI_ACCOUNT_LIMIT_BYPASS_ENABLED}")
    print(f"  Primary Source Override Enabled: {PRIMARY_SOURCE_OVERRIDE_ENABLED}")
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
