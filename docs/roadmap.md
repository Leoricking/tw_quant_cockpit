# TW Quant Cockpit — Roadmap

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**

---

## Completed Milestones

| Version | Feature | Status |
|---------|---------|--------|
| v0.3.1–v0.3.8 | Core infrastructure, data pipeline, signal engine | Done |
| v0.3.9 | Public data API layer (TWSE public endpoints) | Done |
| v0.3.10 | Intraday OHLC fix, microstructure display fix | Done |
| v0.3.11 | Long-term strategy validation (multi-year backtest) | Done |
| v0.3.12 | Portfolio & risk simulation | Done |
| v0.3.13 | GUI Portfolio Cockpit tab | Done |
| v0.3.14 | Signal Quality Dashboard | Done |
| v0.3.15 | Rule Weight Tuning Lab | Done |
| v0.3.16 | Auto Report Center | Done |
| v0.3.17 | Automation Scheduler | Done |
| v0.3.18 | API Provider Hardening | Done |
| v0.3.19 | Data Provider Auto Fetch | Done |
| v0.3.20 | Data Quality Gate | Done |
| v0.3.21 | Daily Workflow Engine | Done |
| v0.3.22 | Usability QA & Error Message Polish | Done |
| v0.3.23 | Documentation & Release Notes Pack | Done |
| v0.3.24 | Data Provider Reliability & Fallback Matrix | Done |
| v0.3.25 | Universe Expansion & Sector Classification | Done |
| v0.3.26 | Backtest Engine Hardening | Done |
| v0.3.27 | Intraday / Tick Data Pipeline | Done |
| v0.3.28 | Strategy Rule Governance | Done |
| v0.3.29 | Research Notebook / Experiment Registry | Done |
| v0.4.0 | Research Platform Stable Release | Done |

---

## Completed: v0.3.26 — Backtest Engine Hardening

- `ExecutionModel`: signal_close / next_open / next_close / vwap_proxy entry; stop_loss, take_profit, trailing_stop, time_stop, combined exit
- `CostModel`: Taiwan defaults (0.1425%×0.6 commission, 0.3% tax, 5bps slippage, min 20 NTD); zero-cost preset
- `LiquidityFilter`: min volume 500, min turnover 10M NTD, max participation 5%; 0–100 liquidity score
- `GapRiskModel`: 5-category gap classifier; gap stop-loss; no-chase-gap logic
- `ValidationSplit`: walk_forward / out_of_sample / expanding_window / in_sample_only
- `MarketRegimeSplitter`: bull/bear/sideways/high_volatility via MA20/MA60 + rolling vol; proxy fallback
- `HardenedBacktester`: orchestrator; A/B/C/D confidence grade; saves 5 result files
- `HardenedBacktestReportBuilder`: 10-section Markdown report
- `HardenedBacktestPanel`: PySide6 GUI tab with controls, summary cards, assumption/metrics/split/regime tables
- `HardenedBacktestAdapter`: GUI bridge (no subprocess)
- CLI: `python main.py hardened-backtest [options]`
- `AutoReportCenter` full profile includes hardened backtest
- No real orders. Production BLOCKED.

---

## Completed: v0.3.25 — Universe Expansion & Sector Classification

- `UniverseRegistry`: 13 universe groups (core_14–core_200 + 8 theme groups); build_default_universes(), export_universe_manifest()
- `SectorClassifier`: 9-sector / 25+ theme taxonomy; classify_symbol(), classify_universe(), get_sector_summary()
- `UniverseQualityAnalyzer`: 0–100 score (6 components); readiness levels INSUFFICIENT → STRONG_RESEARCH_UNIVERSE
- `UniverseExpander`: propose_expansion() — proposals only, no auto-write; ranked by AI exposure + data availability
- `UniverseExpansionReportBuilder`: 8-section Markdown report
- `UniverseManagerPanel`: GUI tab (Universe Manager) with selector, symbol table, sector summary, quality cards
- `UniverseManagerAdapter`: GUI bridge (list_universes, load_universe, build_default_universes, analyze_quality, generate_report)
- CLI: `python main.py universe-list | universe-build-defaults | universe-show | universe-quality-score | universe-expand | universe-report`
- `DataProviderAutoFetcher` accepts `universe_name` parameter
- `DailyResearchWorkflow` accepts `universe_name` parameter
- `DataQualityGate` accepts `universe` parameter for symbol-level coverage scoring
- `AutoReportCenter` accepts `universe_name` parameter, records in manifest
- No mock fallback in real mode. No real orders. Production BLOCKED.

---

## Completed: v0.3.24 — Data Provider Reliability & Fallback Matrix

- `ProviderReliabilityMatrix`: builds dataset fallback chains, provider reliability scores, dataset confidence scores
- `ProviderMetricsCollector`: reads logs to compute success rates
- `DatasetConfidenceScorer`: 0–100 confidence per dataset (6-component weighted formula)
- `ProviderReliabilityReportBuilder`: Markdown report with 8 sections
- `ProviderReliabilityPanel`: GUI tab (Provider Reliability)
- CLI: `python main.py provider-reliability [--report] [--dataset X] [--provider X]`
- No mock fallback in real mode. No real orders. Production BLOCKED.

---

## Completed: v0.3.27 — Intraday / Tick Data Pipeline

- `IntradaySchema`: standard column spec, XQ column map, validation, Taiwan session filter
- `IntradayDataPipeline`: discovers raw intraday CSV/XLSX, normalizes to standard schema, writes `intraday_standard/{freq}/`
- `IntradayQualityChecker`: scans standardized files; quality statuses OK/PARTIAL/MISSING/STALE/DUPLICATED/PRICE_ANOMALY/VOLUME_ANOMALY/INSUFFICIENT; 0–100 quality score
- `OpeningRangeFeatureBuilder`: opening 5/15/30-min return, volume ratio, range %, high/low break, strength score
- `VWAPFeatureBuilder`: intraday VWAP, price-vs-VWAP%, slope, above-VWAP ratio, reclaim/lost, support score
- `FakeBreakoutDetector`: high/low break confirmation, volume confirmation, fake breakout risk/score, chase risk score
- `IntradayVolumeProfileBuilder`: volume by bar, cumulative VWAP, high-volume price zones, session volume distribution
- `MicrostructureQualityChecker`: tick_api_ready=False, bidask_api_ready=False; status INTRADAY_BAR_ONLY/TICK_PLANNED
- `TickBidaskSchema`: placeholder schema for future tick/bidask API (v0.4+)
- `IntradayPipelineReportBuilder`: Markdown report with quality, features, fake breakout, volume profile, tick readiness
- `IntradayPipelinePanel`: PySide6 GUI tab with quality table, feature preview, fake breakout, volume profile, tick status
- `IntradayPipelineAdapter`: GUI bridge (run_pipeline, check_quality, preview_features)
- CLI: `python main.py intraday-pipeline [--mode] [--freq] [--dry-run] [--report]`; `intraday-quality [--freq]`; `intraday-features --stock [--freq]`
- Integration: `DataFreshnessChecker` adds `intraday_1min`/`intraday_5min`; `DataQualityGate` uses `IntradayQualityChecker`; `AutoReportCenter` full/daily profiles include intraday pipeline; manifest records `intraday_quality_score`/`intraday_status`/`tick_bidask_readiness`; `features/microstructure.py` enriches last bar with opening range/VWAP/fake breakout; `features/indicators.py` prefers standardized path
- `IntradayDataImporter` adds `load_intraday_standard()` method
- No real orders. Production BLOCKED.

---

## Completed: v0.3.28 — Strategy Rule Governance

- `RuleMetadata`: dataclass with rule_id, category, version, status, confidence, sample_count, dependencies, safety_flags
- `RuleRegistry`: 53 built-in rules across 8 categories (buy_point, screener, strategy_knowledge, long_term, portfolio, signal_quality, intraday, governance/backtest assumption)
- `RuleDependencyGraph`: adjacency-list dependency graph; cycle detection; topological ordering; high-impact rule identification
- `RuleConfidenceScorer`: 0–100 scoring with degradation for experimental, low sample count, mock-only results; confidence levels HIGH/GOOD/PARTIAL/WEAK/LOW/UNKNOWN/PLANNED
- `RuleChangeLog`: append-only JSONL change log (runtime output → `logs/governance/`, not committed)
- `RuleSnapshotBuilder`: exports snapshot JSON + CSV to `data/backtest_results/` (not committed)
- `RuleGovernanceReportBuilder`: 8-section Markdown governance report
- `RuleGovernancePanel`: PySide6 GUI with safety banner, summary cards, rule table, dependency table, review queue, action buttons; QThread workers
- `RuleGovernanceAdapter`: GUI bridge (run_governance, generate_report, export_snapshot)
- CLI: `python main.py rule-governance [--mode] [--category] [--status] [--report] [--snapshot]`
- Integration: `AutoReportCenter` full profile includes rule governance; manifest records governance fields; `SignalQualityEngine` maps recommendations to rule_ids; `RuleWeightConfig` adds `rule_governance_refs`; `HardenedBacktester` outputs `assumption_rule_ids`; intraday feature builders output `feature_rule_id`
- Rule IDs follow format: CATEGORY.TIMEFRAME.NAME.VERSION (e.g. BUY.SHORT.PULLBACK_10MA.V1)
- Tick/bidask rules: status EXPERIMENTAL, confidence PLANNED — not pretending ready
- No auto-apply weights. No auto-enable rules. No real orders. Production BLOCKED.

---

## Completed: v0.3.29 — Research Notebook / Experiment Registry

- `ExperimentMetadata`: dataclass with experiment_id (EXP-YYYYMMDD-HHMMSS-shortuuid), name, type, status, mode, profile, git_commit, git_tag, universe, snapshots, reports; 6 status constants; 8 type constants
- `ExperimentRegistry`: create/register/list/get/update/archive experiments; stores `experiments/{id}/metadata.json`, snapshots/, reports/, notes.md; `registry.json` index; runtime outputs not committed
- `ExperimentSnapshotBuilder`: 10 snapshot types — config, universe, data_quality, provider_reliability, rule_governance, backtest, signal_quality, portfolio, intraday, reports; build_all(); summarizes only, no large data copies
- `ExperimentComparator`: compare_two() / compare() — scores/backtest/data_quality/rules/universe; IMPROVED/WORSENED/UNCHANGED/INSUFFICIENT_DATA; IMPROVED ≠ ready for real trading
- `ExperimentNotebookBuilder`: build_notebook() → `{id}/notebook.md`; 10 sections
- `ExperimentRegistryReportBuilder`: 6-section Markdown report → `reports/experiment_registry_report_YYYY-MM-DD.md`
- `ExperimentRegistryPanel`: PySide6 GUI with safety banner, summary cards, experiment table, snapshot table, compare panel, notebook preview, action buttons; QThread workers
- `ExperimentRegistryAdapter`: GUI bridge
- CLI: `python main.py experiment-create|register-latest|list|show|notebook|compare|report|snapshot`
- Integration: `DailyResearchWorkflow` accepts `register_experiment=False`; `AutoReportCenter` full profile includes experiment_registry; "Experiment Registry" tab in cockpit
- `experiments/` runtime excluded from git; `experiments/.gitkeep` committed
- No real orders. Production BLOCKED.

---

## Completed: v0.4.0 — Research Platform Stable Release

- `VersionInfo`: centralized version class; version=v0.4.0; get_version_info(), print_version_info(), get_safety_banner(), get_feature_summary()
- `StableReleaseChecklist`: 18-item checklist (compileall, import health, GUI, workflow, quality gate, provider reliability, intraday, backtest, rule governance, experiment registry, auto report, usability, paper, mock realtime, git safety, artifact ignore, token leak, real order check); PASS/PARTIAL/BLOCKED
- `RegressionSuite`: quick (7 tests) + full (14 tests) suites; CSV output; PASS/PARTIAL/FAIL
- `StableReleaseReportBuilder`: 7-section Markdown stable release report
- `ReleaseStatusPanel`: PySide6 GUI with version cards, feature coverage table, regression table, actions; QThread workers
- `ReleaseStatusAdapter`: GUI bridge
- CLI: `python main.py version-info | stable-release-check | regression-suite | stable-release-report`
- `gui/dashboard.py` adds "Release Status" tab
- v0.3.x features verified and regression-tested; no new strategies; no production trading
- No real orders. Production BLOCKED.

---

## Completed: v0.4.1 — API Fetch Productionization

**Status:** Done

- `TokenSetupAssistant` — reads .env without modifying; masks tokens; validates safety; generates setup instructions
- `RetryPolicy` — exponential backoff for TIMEOUT/NETWORK/RATE_LIMIT/SERVER_ERROR; never used for orders
- `APICache` (providers) — SHA-256 keyed, token-sanitized, TTL=24h; stats/cleanup; stored in `data_cache/api/`
- `DataLineageTracker` — LIN-XXXXXXXXXX IDs; per-fetch/write records; URL masking; CSV export
- `APIFetchDiagnostics` — aggregates provider/dataset results; sanitized messages; recommended_action
- `TWSETPEXParser` — alias mapping, comma numerics, ROC year conversion, SCHEMA_CHANGED/PARTIAL
- `MOPSFinancialParser` — estimated announcement dates (Q1/Q2/Q3=45d, Q4=90d), timing_quality, announcement_date_is_estimated
- `APIFetchProductionReportBuilder` — 8-section Markdown report
- `APIFetchStatusPanel` / `APIFetchStatusAdapter` — GUI tab with QThread workers; never shows full token
- 5 new CLI commands: `api-token-check`, `api-cache-status`, `api-fetch-diagnostics`, `api-cache-cleanup`, `api-fetch-production-report`
- Still not production trading; no real orders

---

## Planned: v0.4.2 — ML Feature Store v1

**Target:** Centralized, versioned feature store for ML model inputs

---

## Planned: v0.3.28 (old roadmap — superseded)

**Target:** Signal quality improvements

- Multi-period signal quality scoring (not just latest day)
- Signal stability metric (how consistent is the recommendation over N days)
- Rule dependency analysis (correlated rules detection)

---

## Planned: v0.4.0

**Target:** Architecture consolidation

- Unified data model (replace ad-hoc dict structures with dataclasses)
- Plugin architecture for custom rules
- Config file support (`config.yaml`) for provider tokens and thresholds
- Full test suite (pytest) with real data fixtures

**Safety constraints remain unchanged in v0.4.x:**
- PRODUCTION_BLOCKED=True
- REAL_ORDER_READY=False
- No broker connections

---

## Non-Goals (Permanent)

The following are explicitly out of scope for all future versions:

| Non-Goal | Reason |
|----------|--------|
| Real order execution | Research platform only |
| Broker API integration (Shioaji, Mega, etc.) | Out of scope |
| Investment advice generation | Not a registered advisor; legal constraint |
| Auto weight application | Manual review required; safety constraint |
| Cloud deployment | Local research tool |
| Multi-user access | Single-user research tool |

---

*TW Quant Cockpit v0.3.23 — Research Only — Not Investment Advice*
