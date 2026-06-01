# TW Quant Cockpit — Release Notes v0.4

> [!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.

---

## v0.4.6 — Portfolio Journal & Trade Review

**Status:** Current

### Summary

v0.4.6 adds a research-only trade journal system for recording simulated trades, paper trades, intraday replay training notes, signal reviews, and portfolio reviews. Journal Only. No real orders. No broker connection. Not investment advice.

### New Files

- `journal/__init__.py` — package init
- `journal/journal_schema.py` — `JournalEntry` dataclass: UUID journal_id, 6 entry types, 7 statuses, 10 outcome labels, 13 mistake tags; `_sanitize()` blocks sensitive field names; `no_real_orders=True` enforced in `__post_init__`
- `journal/journal_store.py` — `PortfolioJournalStore`: JSONL persistence at `journal_data/journal_entries.jsonl`; CSV export; lazy-load; never raises
- `journal/signal_outcome_tracker.py` — `SignalOutcomeTracker`: links signal_id → journal entries; WIN/LOSS/FALSE_SIGNAL evaluation; MFE/MAE/process_quality; CSV export
- `journal/replay_training_notes.py` — `ReplayTrainingNotes`: creates ENTRY_REPLAY_NOTE entries from Intraday Replay session IDs
- `journal/mistake_taxonomy.py` — `MistakeTaxonomy`: 13 tags, 8 categories, severity (CRITICAL/HIGH/MEDIUM), suggested_fix
- `journal/journal_analytics.py` — `JournalAnalytics`: win rate, avg return/MFE/MAE; summarize by symbol/strategy/mistake/outcome/process_quality
- `reports/portfolio_journal_report.py` — `PortfolioJournalReport`: 8-section Markdown report (gitignored)
- `gui/portfolio_journal_adapter.py` — `PortfolioJournalAdapter`: GUI bridge; all methods return dicts; never raise
- `gui/portfolio_journal_panel.py` — `PortfolioJournalPanel`: PySide6 panel with safety banner, 6 summary cards, entry table, detail panel, new entry form, review panel; QThread for report generation
- `docs/portfolio_journal_trade_review.md` — full documentation

### Modified Files

- `main.py` — 7 new CLI commands: `journal-add`, `journal-list`, `journal-show`, `journal-review`, `journal-summary`, `journal-report`, `journal-link-replay`
- `gui/dashboard.py` — guarded import + "Portfolio Journal" tab
- `notifications/notification_rules.py` — `evaluate_portfolio_journal()`: review_required_count > 0 → NOTICE; repeated mistake tag ≥ 3 → WARNING
- `reports/auto_report_center.py` — `run_portfolio_journal_summary()`, `include_portfolio_journal` flag; full + daily profiles include portfolio journal
- `reports/auto_report_index.py` — 4 new manifest fields: `journal_entries_count`, `journal_review_required_count`, `journal_latest_entry`, `journal_most_common_mistake`
- `experiments/snapshot_builder.py` — `build_portfolio_journal_snapshot()`
- `release/regression_suite.py` — 2 new v0.4.6 tests (`_test_journal_imports`, `_test_journal_store_empty_state`)
- `release/stable_release_checklist.py` — 3 new v0.4.6 checks (`_check_journal_import_health`, `_check_journal_no_real_orders`, `_check_journal_data_ignored`)
- `.gitignore` — `journal_data/`, `portfolio_journal_report_*.md`, `portfolio_journal_summary.csv`, `signal_outcome_summary.csv`
- `README.md`, `docs/roadmap.md`, `docs/release_notes_v0.4.md`, `docs/index.md`

### Safety

- `no_real_orders = True`, `production_blocked = True`, `journal_only = True` enforced at every layer
- `__post_init__` reasserts all invariants — cannot be overridden by caller
- No broker connection. No submit_order. No real fills. No real account reads.
- `journal_data/` and all generated outputs are gitignored — never committed
- Not investment advice

---

## v0.4.0 — Research Platform Stable Release

**Status:** Current

### Summary

v0.4.0 consolidates all v0.3.x features into a verified, regression-tested, documented stable research platform. No new strategies. No production trading. Research only.

### New Files

- `release/__init__.py` — package init
- `release/version_info.py` — `VersionInfo` class; version=v0.4.0; `get_version_info()`, `print_version_info()`, `get_safety_banner()`, `get_feature_summary()`
- `release/stable_release_checklist.py` — `StableReleaseChecklist`: 18-item checklist (compileall, import health, GUI health, workflow, quality gate, provider reliability, intraday, backtest, rule governance, experiment registry, auto report, usability, paper, mock realtime, git safety, artifact ignore, token leak, real order check)
- `release/regression_suite.py` — `RegressionSuite`: quick (7 tests) + full (14 tests) suites; writes CSV; PASS/PARTIAL/FAIL status
- `reports/stable_release_report.py` — `StableReleaseReportBuilder`: 7-section Markdown report
- `gui/release_status_panel.py` — `ReleaseStatusPanel`: PySide6 GUI with version cards, feature coverage table, regression table, actions; QThread workers
- `gui/release_status_adapter.py` — `ReleaseStatusAdapter`: GUI bridge
- `docs/release_v0.4.0.md` — release overview documentation
- `docs/release_checklist.md` — manual release checklist
- `docs/release_notes_v0.4.md` — this file

### Modified Files

- `main.py` — 4 new CLI commands: `version-info`, `stable-release-check`, `regression-suite`, `stable-release-report`
- `gui/dashboard.py` — guarded import + "Release Status" tab
- `README.md` — updated to v0.4.0 as current version
- `docs/roadmap.md` — v0.4.0 marked Done; v0.4.1 API Fetch Productionization planned
- `docs/index.md` — added release_v0.4.0.md, release_checklist.md, release_notes_v0.4.md
- `.gitignore` — stable_release report artifacts excluded

### Safety

- `read_only=True`, `no_real_orders=True`, `production_blocked=True`, `real_order_ready=False` in all new classes
- No broker connections. No auto weight apply. No real orders.
- Token leak check in StableReleaseChecklist — BLOCKED status if any token found hardcoded

### Stable Features (from v0.3.x)

All 15 major features verified and regression-tested. See `docs/release_v0.4.0.md` for full feature table.

---

## v0.4.1 — API Fetch Productionization

**Status:** Current

### Summary

v0.4.1 adds a production-grade, read-only API data fetch layer on top of the stable v0.4.0 platform. Retry, cache, lineage, parser hardening, token safety — all read-only. No new strategies. No real orders.

### New Files

- `data/providers/token_setup_assistant.py` — `TokenSetupAssistant`: reads .env; masks tokens; never modifies .env
- `data/providers/retry_policy.py` — `RetryPolicy`: exponential backoff for safe fetches only; never used for orders
- `data/providers/api_cache.py` — `APICache`: SHA-256 keyed provider cache in `data_cache/api/`; TTL=24h
- `data/providers/data_lineage.py` — `DataLineageTracker`: LIN-XXXX IDs; masked URLs; CSV export
- `data/providers/api_diagnostics.py` — `APIFetchDiagnostics`: per-provider/dataset result aggregation; sanitized output
- `data/providers/twse_tpex_parser.py` — `TWSETPEXParser`: alias mapping, ROC year, comma numerics, schema status
- `data/providers/mops_financial_parser.py` — `MOPSFinancialParser`: estimated announcement dates, timing_quality
- `reports/api_fetch_production_report.py` — `APIFetchProductionReportBuilder`: 8-section Markdown report
- `gui/api_fetch_status_adapter.py` — `APIFetchStatusAdapter`: GUI bridge; lazy imports; no full token
- `gui/api_fetch_status_panel.py` — `APIFetchStatusPanel`: PySide6 GUI with QThread workers; safety banner
- `docs/api_fetch_productionization.md` — full documentation

### Modified Files

- `main.py` — 5 new CLI commands: `api-token-check`, `api-cache-status`, `api-fetch-diagnostics`, `api-cache-cleanup`, `api-fetch-production-report`
- `gui/dashboard.py` — guarded import + "API Fetch Status" tab
- `data/providers/provider_health.py` — `run_all()` adds `v041_components` availability dict
- `reports/auto_report_center.py` — `include_api_fetch_production` flag; `run_api_fetch_production_report()` method
- `release/regression_suite.py` — 3 new v0.4.1 tests added to full suite (api_fetch_imports, api_token_check, api_cache_stats)
- `release/stable_release_checklist.py` — 2 new v0.4.1 checks (api_token_safety, api_cache_ignored)
- `docs/roadmap.md` — v0.4.1 marked Done; v0.4.2 ML Feature Store planned
- `docs/index.md` — added api_fetch_productionization.md
- `.gitignore` — API fetch report and lineage artifacts excluded

### Safety

- `read_only=True`, `no_real_orders=True` in all new classes
- Tokens always masked; never committed; never displayed in full
- Cache keys never contain full token (SHA-256 of sanitized params)
- Lineage URLs masked (token query params replaced with ****)
- Production Trading: BLOCKED
- REAL_ORDER_READY: False

---

## v0.4.1.1 — Strategy Knowledge Ingestion from Transcripts

**Status:** Done

### Summary

v0.4.1.1 inserts a Knowledge Ingestion layer between v0.4.1 (API Fetch Productionization) and v0.4.2 (ML Feature Store). It converts user-imported transcripts (YouTube transcripts, manual notes, 阪田戰法 videos, 獅公 market commentary) into structured strategy knowledge. No real orders. No auto-apply. Confidence capped at PARTIAL. Long-cycle crash watch capped at PLANNED.

### New Files

- `knowledge/__init__.py` — package init
- `knowledge/transcript_source.py` — `TranscriptSource`: metadata (source_id, title, author, source_type, hash); from_file(), to_dict()
- `knowledge/transcript_loader.py` — `TranscriptLoader`: discovers `.txt`/`.md` in 4 dirs; parse_sections(), extract_metadata(), normalize_text(); no crash on missing dirs; no OCR; no network
- `knowledge/knowledge_schema.py` — `StrategyKnowledgeItem`: 17 fields; 11 categories; 5 polarities; 6 timeframes; to_dict()
- `knowledge/knowledge_extractor.py` — `StrategyKnowledgeExtractor`: rule-based keyword extractor; 8 methods; handles 阪田戰法 + 獅公 patterns; confidence ≤ PARTIAL
- `knowledge/rule_candidate_mapper.py` — `RuleCandidateMapper`: maps items to Rule Governance rule_ids; auto_activated=False always; CANDIDATE status for unmapped rules
- `knowledge/knowledge_store.py` — `StrategyKnowledgeStore`: 6 CSV outputs; never writes tokens; build_summary()
- `knowledge/ingestion_pipeline.py` — `StrategyKnowledgeIngestionPipeline`: 7-step orchestrator; dry_run support; production_blocked=True
- `reports/strategy_knowledge_ingestion_report.py` — `StrategyKnowledgeIngestionReportBuilder`: 9-section Markdown report
- `gui/strategy_knowledge_ingestion_panel.py` — PySide6 panel; safety banner; 6 summary cards; source/items/rule-candidate tables; QThread workers
- `gui/strategy_knowledge_ingestion_adapter.py` — `StrategyKnowledgeIngestionAdapter`: GUI bridge (run_ingestion, generate_report, load_latest_summary, load_sources, load_items, load_rule_candidates)
- `docs/strategy_knowledge_ingestion.md` — full documentation

### Modified Files

- `main.py` — 2 new CLI commands: `strategy-knowledge-ingest`, `strategy-knowledge-summary`
- `governance/rule_registry.py` — 6 new NEEDS_REVIEW transcript-candidate risk rules (RISK.TECHNICAL.TOP_PATTERN.V1, RISK.RELATIVE_WEAKNESS.MARKET_NEW_HIGH_STOCK_LAG.V1, RISK.CYCLE.CRASH_WATCH.V1, RISK.FUNDAMENTAL.REVENUE_NOT_SUPPORTING_THEME.V1, RISK.PORTFOLIO.OVER_CONCENTRATION.V1, RISK.PORTFOLIO.MARGIN_USAGE.V1); `RULE_STATUS_CANDIDATE` constant added
- `governance/rule_confidence.py` — transcript-only rule confidence capped at PARTIAL; CRASH_WATCH capped at PLANNED
- `reports/auto_report_center.py` — `include_strategy_knowledge_ingestion` flag; `run_strategy_knowledge_ingestion_summary()` method; full + daily profiles updated
- `reports/auto_report_index.py` — manifest includes 4 new strategy_knowledge fields
- `experiments/snapshot_builder.py` — `build_strategy_knowledge_snapshot()` added; included in `build_all()`
- `release/regression_suite.py` — 3 new v0.4.1.1 tests (strategy_knowledge_imports, strategy_knowledge_summary, strategy_knowledge_dry_run); full suite count: 29
- `release/stable_release_checklist.py` — 3 new v0.4.1.1 checks (strategy_knowledge_ingestion_import, no_auto_activate_candidate_rules, strategy_knowledge_artifacts_ignored)
- `gui/dashboard.py` — guarded import + "Strategy Knowledge" tab
- `docs/roadmap.md` — v0.4.1.1 marked Done
- `docs/index.md` — strategy_knowledge_ingestion.md added
- `.gitignore` — transcript and knowledge output dirs excluded

### Safety

- Knowledge Only, Research Only, No Real Orders, Production Trading BLOCKED
- `auto_activated=False` always — candidate rules require manual review before ACTIVE status
- Transcript-only confidence ≤ PARTIAL
- Long-cycle crash watch confidence = PLANNED — NOT a short-term sell signal
- No investment advice generated

---

## v0.4.2 — ML Feature Store v1

**Status:** Current

### Summary

v0.4.2 adds an ML data preparation layer on top of the stable v0.4.1 platform. Feature catalog, feature snapshot builder, label generation, time-series train/val/test split, data leakage check, feature quality check, and feature importance shell. No model training. No live prediction. No real orders.

### New Files

- `ml/__init__.py` — ML package init
- `ml/feature_catalog.py` — `FeatureDefinition`, `FeatureCatalog`: 50+ built-in features across 16 categories with leakage_risk/experimental/lookback metadata
- `ml/feature_snapshot.py` — `FeatureSnapshotBuilder`: extracts feature matrix from daily_k, institutional, fundamental, intraday CSV sources
- `ml/label_generator.py` — `LabelGenerator`: fwd_return_Nd, classification (label_direction_Nd, label_up/down_3pct), triple barrier; labels always prefix `label_` or `fwd_`
- `ml/split_manager.py` — `MLSplitManager`: time_series split (default, 60/20/20), symbol_grouped, walk_forward, random (with leakage warning)
- `ml/leakage_checker.py` — `DataLeakageChecker`: 7 finding types; CLEAN/WARNING/LEAKAGE_RISK/BLOCKED_FOR_TRAINING status
- `ml/feature_quality.py` — `FeatureQualityChecker`: missing_ratio, constant_features, label_balance, feature_quality_score (0–100)
- `ml/feature_importance_shell.py` — `FeatureImportanceShell`: Pearson correlation; sklearn mutual info (optional fallback)
- `ml/dataset_builder.py` — `MLFeatureDatasetBuilder`: features + labels + split + metadata; writes model_ready_dataset_*.csv (not committed)
- `reports/ml_feature_store_report.py` — `MLFeatureStoreReportBuilder`: 9-section Markdown report (not committed)
- `gui/ml_feature_store_adapter.py` — `MLFeatureStoreAdapter`: GUI bridge; lazy imports
- `gui/ml_feature_store_panel.py` — `MLFeatureStorePanel`: PySide6 GUI with QThread workers; safety banner; 8 sections
- `docs/ml_feature_store_v1.md` — full documentation

### Modified Files

- `main.py` — 8 new CLI commands: `ml-feature-catalog`, `ml-feature-snapshot`, `ml-labels`, `ml-build-dataset`, `ml-leakage-check`, `ml-feature-quality`, `ml-feature-importance`, `ml-feature-store-report`
- `gui/dashboard.py` — guarded import + "ML Feature Store" tab
- `reports/auto_report_center.py` — `include_ml_feature_store` flag; `run_ml_feature_store_report()` method
- `reports/auto_report_index.py` — manifest adds `ml_feature_count`, `ml_dataset_status`, `ml_leakage_status`, `ml_feature_quality_score`
- `release/regression_suite.py` — 4 new v0.4.2 tests added to full suite (ml_feature_catalog, ml_feature_snapshot_import, ml_leakage_checker, ml_feature_store_report)
- `release/stable_release_checklist.py` — 3 new v0.4.2 checks (ml_feature_store_import, ml_leakage_checker, ml_dataset_artifact_ignored)
- `experiments/snapshot_builder.py` — `build_ml_feature_snapshot()` added to `build_all()`
- `docs/roadmap.md` — v0.4.2 marked Done; v0.4.3 Model Monitoring Shell planned
- `docs/index.md` — added ml_feature_store_v1.md
- `.gitignore` — `data/ml_features/`, `reports/ml_feature_store_report_*.md`, and related artifacts excluded

### Safety

- `read_only=True`, `no_real_orders=True`, `production_blocked=True`, `real_order_ready=False` in all new classes
- Label columns always prefix `label_` or `fwd_` — never mixed with feature columns
- Default split: time_series (chronological) — random split emits DATA LEAKAGE RISK warning
- model_ready_dataset_*.csv and ml_feature_store_report_*.md never committed (gitignored)
- No live prediction. No auto-trading. No auto weight apply.
- Production Trading: BLOCKED
- REAL_ORDER_READY: False
- ML Research Only

---

## v0.4.2.1 — ML Feature Store Knowledge Integration

**Status:** Current

### Summary

v0.4.2.1 connects transcript-derived strategy knowledge (from v0.4.1.1 StrategyKnowledgeStore CSVs) into the v0.4.2 ML Feature Store. Converts factor_candidates, rule_candidates, avoid_conditions, and risk_conditions into ML feature metadata with readiness assessment and leakage checking. No model training. No auto-enabling. No real orders.

### New Files

- `ml/knowledge_feature_bridge.py` — `KnowledgeFeatureBridge`: loads v0.4.1.1 CSVs, converts 4 knowledge categories to ML feature metadata dicts; auto_enabled=False; confidence capped at PARTIAL; long_cycle → METADATA_ONLY
- `ml/knowledge_feature_catalog.py` — `KnowledgeFeatureCatalog`: register/list/get/export transcript-derived features; enforces auto_enabled=False on all entries
- `ml/knowledge_feature_readiness.py` — `KnowledgeFeatureReadinessChecker`: assigns READY/PARTIAL/METADATA_ONLY/NEEDS_MAPPING/NEEDS_BACKTEST/BLOCKED/LEAKAGE_RISK/INSUFFICIENT_DATA per feature
- `ml/knowledge_leakage_checker.py` — `KnowledgeLeakageChecker`: POST_EVENT_KNOWLEDGE, TIMING_ESTIMATED, LONG_CYCLE_RISK, PATTERN_INCOMPLETE, UNVALIDATED_CANDIDATE detection
- `ml/knowledge_dataset_exporter.py` — `KnowledgeDatasetExporter`: writes 4 output files; model_ready schema excludes long-cycle and auto_enabled=False always
- `reports/ml_knowledge_integration_report.py` — `MLKnowledgeIntegrationReport`: 7-section Markdown report
- `gui/ml_knowledge_integration_panel.py` — `MLKnowledgeIntegrationPanel`: PySide6 GUI with QThread workers, 6 summary cards (auto_enabled always 0), safety banner
- `gui/ml_knowledge_integration_adapter.py` — `MLKnowledgeIntegrationAdapter`: GUI bridge; run_integration, check_leakage, generate_report, load_latest_summary
- `docs/ml_feature_store_knowledge_integration.md` — full documentation

### Modified Files

- `main.py` — 3 new CLI commands: `ml-knowledge-integrate`, `ml-knowledge-leakage-check`, `ml-knowledge-feature-summary`
- `gui/dashboard.py` — guarded import + "ML Knowledge Integration" tab
- `reports/auto_report_center.py` — `include_ml_knowledge_integration` flag; `run_ml_knowledge_integration_summary()` method
- `reports/auto_report_index.py` — manifest adds 5 new ML knowledge fields
- `release/regression_suite.py` — 2 new v0.4.2.1 tests (ml_knowledge_imports, ml_knowledge_bridge_empty)
- `release/stable_release_checklist.py` — 3 new v0.4.2.1 checks (import, auto_enabled_false, artifacts_ignored)
- `experiments/snapshot_builder.py` — `build_ml_knowledge_integration_snapshot()` added to `build_all()`
- `docs/roadmap.md` — v0.4.2.1 marked Done
- `docs/index.md` — added ml_feature_store_knowledge_integration.md
- `.gitignore` — `data/backtest_results/ml_feature_store/`, `reports/ml_knowledge_integration_report_*.md` excluded

### Safety

- `auto_enabled=False` on all transcript-derived features — always, no exceptions
- Confidence capped at PARTIAL for all transcript-only sources
- `long_cycle_risk` → `METADATA_ONLY`, `not_for_short_term_label=True` — never used as short-term return label
- model_ready_knowledge_schema.json excludes long-cycle features and critical leakage features
- ML output files never committed (gitignored)
- No model training. No live prediction. No auto weight apply.
- Production Trading: BLOCKED
- REAL_ORDER_READY: False
- ML Research Only

---

## v0.4.3 — Model Monitoring Framework

**Status:** Current

### Summary

v0.4.3 adds a model and signal monitoring layer on top of the stable v0.4.2 platform. Prediction tracking, hit/miss review, drift detection, signal degradation warnings, and rule-vs-ML comparison — all research-only, no live prediction, no real orders.

### New Files

- `monitoring/__init__.py` — Monitoring package init
- `monitoring/model_registry.py` — `ModelMetadata`, `ModelRegistry`: metadata-only model registry; JSON files in `model_monitoring/`
- `monitoring/prediction_log.py` — `PredictionRecord`, `PredictionLog`: append-only JSONL prediction records; load/filter/summarize/update_actuals
- `monitoring/hit_miss_review.py` — `HitMissReviewer`: hit rate, precision, recall, grouping by symbol/rule/model/source
- `monitoring/drift_detector.py` — `DriftDetector`: feature distribution drift, missing ratio drift, label drift, prediction score drift; 5-level status
- `monitoring/signal_degradation.py` — `SignalDegradationMonitor`: rule/signal quality/portfolio degradation; no crash on missing files
- `monitoring/rule_vs_ml_comparator.py` — `RuleVsMLComparator`: agreement rate, disagreement; ML_NOT_AVAILABLE when no ML predictions
- `monitoring/monitoring_summary.py` — `ModelMonitoringSummary`: orchestrates all monitors; next_actions
- `reports/model_monitoring_report.py` — `ModelMonitoringReportBuilder`: 8-section Markdown report
- `gui/model_monitoring_adapter.py` — `ModelMonitoringAdapter`: GUI bridge with lazy imports
- `gui/model_monitoring_panel.py` — `ModelMonitoringPanel`: PySide6 GUI with QThread workers; safety banner; 5 tables; register model dialog
- `docs/model_monitoring.md` — full documentation

### Modified Files

- `main.py` — 9 new CLI commands: `model-monitoring`, `model-monitoring-report`, `model-registry-list`, `model-register`, `prediction-log`, `prediction-review`, `drift-check`, `signal-degradation`, `rule-vs-ml`
- `gui/dashboard.py` — guarded import + "Model Monitoring" tab
- `reports/auto_report_center.py` — `include_model_monitoring` flag; `run_model_monitoring_report()` method
- `reports/auto_report_index.py` — manifest adds `model_monitoring_status`, `prediction_count`, `drift_status`, `degradation_status`
- `release/regression_suite.py` — 3 new v0.4.3 tests added to full suite (24 total)
- `release/stable_release_checklist.py` — 3 new v0.4.3 checks (26 total)
- `experiments/snapshot_builder.py` — `build_model_monitoring_snapshot()` added to `build_all()`
- `docs/roadmap.md` — v0.4.3 marked Done; v0.4.4 Intraday Replay Cockpit planned
- `docs/index.md` — added model_monitoring.md
- `.gitignore` — `model_monitoring/` and all monitoring artifacts excluded

### Safety

- `read_only=True`, `no_real_orders=True`, `production_blocked=True` in all new classes
- No live prediction. Prediction logs are research records only.
- Drift warning is not a trading signal. Hit rate is not guaranteed win rate.
- Disagreement does not auto-change strategy. No auto weight apply.
- model_monitoring/ and model_monitoring_report_*.md never committed (gitignored)
- Production Trading: BLOCKED
- REAL_ORDER_READY: False
- Monitoring Only

---

---

## v0.4.4 — Intraday Replay Cockpit

**Status:** Current

### Summary

v0.4.4 adds an intraday bar replay layer on top of the stable v0.4.3 platform. Session manager, replay engine, event timeline, opening range, VWAP, fake breakout, volume profile, strategy overlay, training mode, replay metrics, report, and GUI Intraday Replay Cockpit tab — all replay training only, no live prediction, no real orders, no broker.

### New Files

- `replay/__init__.py` — Replay package init; `__version__ = "v0.4.4"`
- `replay/replay_session.py` — `ReplaySession` dataclass + `ReplaySessionManager`; session lifecycle CREATED/RUNNING/PAUSED/COMPLETED/FAILED/ARCHIVED; stores at `replay_sessions/sessions/{id}.json`
- `replay/replay_engine.py` — `IntradayReplayEngine`; discovers CSV at `data/import/intraday_standard/{freq}/`; returns `INSUFFICIENT_INTRADAY_DATA` on missing file; `reveal_future=False` default
- `replay/replay_events.py` — `ReplayEvent` dataclass + `ReplayEventBuilder`; 12 event type constants; `visible_at_index = bar_index` (no future leakage)
- `replay/opening_range_replay.py` — `OpeningRangeReplay(opening_minutes=15)`; 6 states: BUILDING_RANGE/INSIDE_RANGE/BREAK_HIGH/BREAK_LOW/FAILED_BREAK_HIGH/FAILED_BREAK_LOW
- `replay/vwap_replay.py` — `VWAPReplay`; cumulative VWAP; fallback to close mean if no volume
- `replay/fake_breakout_replay.py` — `FakeBreakoutReplay`; 10-bar high breakout; 5-level risk
- `replay/volume_profile_replay.py` — `VolumeProfileReplay(price_bins=20)`; POC; value area (70%); support pressure state
- `replay/strategy_replay.py` — `StrategyReplayOverlay`; reads existing research data read-only; NEVER calls submit_order; all signals labeled as training annotations
- `replay/training_mode.py` — `ReplayTrainingQuestion` dataclass + `ReplayTrainingMode`; 6 question types; A/B/C/D/F grading; answers NOT trading instructions
- `replay/replay_metrics.py` — `ReplayMetrics`; bars_replayed, quiz_accuracy, training_score, grade; summarize_sessions()
- `reports/intraday_replay_report.py` — `IntradayReplayReportBuilder`; 8-section Markdown to `reports/intraday_replay_report_YYYY-MM-DD.md`
- `gui/intraday_replay_adapter.py` — `IntradayReplayAdapter`; lazy engine instance; `build_current_state()` combines all overlays
- `gui/intraday_replay_panel.py` — `IntradayReplayPanel(QWidget)`; 4 QThread workers; stub if PySide6 unavailable; closeEvent cleanup
- `docs/intraday_replay_cockpit.md` — full documentation

### Modified Files

- `main.py` — 5 new CLI commands: `intraday-replay`, `intraday-replay-report`, `replay-session-list`, `replay-session-show`, `replay-training-summary`
- `gui/dashboard.py` — guarded import + "Intraday Replay" tab
- `reports/auto_report_center.py` — `include_intraday_replay` flag (full profile True, daily profile False); `run_intraday_replay_report()` method
- `reports/auto_report_index.py` — manifest adds `intraday_replay_session_count`, `intraday_replay_training_score`, `intraday_replay_event_count`
- `release/regression_suite.py` — 2 new v0.4.4 tests (intraday_replay_imports, intraday_replay_empty_state); 26 total
- `release/stable_release_checklist.py` — 3 new v0.4.4 checks (intraday_replay_import, replay_runtime_ignored, no_broker_call_in_replay); 29 total
- `experiments/snapshot_builder.py` — `build_intraday_replay_snapshot()` added to `build_all()`
- `docs/roadmap.md` — v0.4.4 marked Done; v0.4.5 Notification Center planned
- `docs/index.md` — updated version, added intraday_replay_cockpit.md
- `.gitignore` — `replay_sessions/`, `reports/intraday_replay_report_*.md`, and related artifacts excluded

### Safety

- `read_only=True`, `no_real_orders=True`, `production_blocked=True`, `real_order_ready=False` in all new classes
- `StrategyReplayOverlay` NEVER calls submit_order; all strategy signals labeled as training annotations
- Training mode answers are NOT trading instructions
- `reveal_future=False` default in replay engine; event `visible_at_index = bar_index` (no lookahead)
- `replay_sessions/` and `reports/intraday_replay_report_*.md` never committed (gitignored)
- No live prediction. No broker connection. No auto-trading. Replay Training Only.
- Production Trading: BLOCKED
- REAL_ORDER_READY: False

---

## v0.4.5 — Notification Center

**Status:** Current

### Summary

Research-only local notification system that records important platform events
(data quality alerts, provider failures, signal changes, ML leakage warnings,
intraday replay reminders) as read-only notifications in a local JSONL log.
No external messages (LINE/Telegram disabled). No real orders.

### New Files

| File | Description |
|------|-------------|
| `notifications/__init__.py` | Package init |
| `notifications/notification_schema.py` | NotificationEvent dataclass; 13 event types; 6 severities; 11 categories |
| `notifications/notification_center.py` | Main engine: JSONL persistence, lazy-load, add_event/notify/list/mark_read/clear_read |
| `notifications/notification_rules.py` | NotificationRuleEngine: 9 evaluate_* methods |
| `notifications/local_notifier.py` | Console + optional win10toast |
| `notifications/external_notifier_placeholder.py` | LINE/Telegram placeholder — always disabled |
| `notifications/notification_preferences.py` | User preferences with load/save |
| `reports/notification_center_report.py` | 8-section Markdown report |
| `gui/notification_center_adapter.py` | GUI bridge — all methods return dicts; never raise |
| `gui/notification_center_panel.py` | PySide6 panel with summary cards, table, detail, preferences |
| `docs/notification_center.md` | Documentation |
| `config/notification_preferences.example.json` | Safe example config (committable) |

### Modified Files

- `main.py` — 5 CLI commands: `notification-scan/list/report/clear-read/test`
- `gui/dashboard.py` — "Notification Center" tab added
- `reports/auto_report_center.py` — `run_notification_center_report()`; `include_notification_center` flag; full + daily profiles
- `reports/auto_report_index.py` — 4 new manifest fields: `notification_total`, `notification_unread`, `notification_critical`, `notification_external_enabled`
- `experiments/snapshot_builder.py` — `build_notification_snapshot()`
- `release/regression_suite.py` — 2 new v0.4.5 tests (imports, empty_state)
- `release/stable_release_checklist.py` — 4 new v0.4.5 checks
- `.gitignore` — `logs/notifications/`, `reports/notification_center_report_*.md`, `data/backtest_results/notification_summary.csv`, `config/notification_preferences.json`

### Safety

- `no_real_orders = True` enforced at every layer
- `external_enabled = False` always (LINE/Telegram placeholder; never sends messages)
- `production_blocked = True` is the EXPECTED safe state (triggers INFO, not ERROR)
- Notification creation never raises (failures logged as warnings)
- Notification metadata never contains tokens, passwords, or API keys

---

*Previous release notes: see `docs/release_notes_v0.3.md`*
