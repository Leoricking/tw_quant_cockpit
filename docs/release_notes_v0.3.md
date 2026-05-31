# TW Quant Cockpit — Release Notes v0.3

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**

---

## v0.3.27 — Intraday / Tick Data Pipeline

**Status:** Current

### New Files

- `intraday/__init__.py` — package init
- `intraday/intraday_schema.py` — `IntradaySchema`: standard column spec (symbol/date/time/datetime/open/high/low/close/volume/source), XQ column map, validation, Taiwan session filter
- `intraday/intraday_pipeline.py` — `IntradayDataPipeline`: discovers raw CSV/XLSX from `data/import/intraday/`, normalizes to standard schema, writes to `data/import/intraday_standard/{freq}/`
- `intraday/intraday_quality.py` — `IntradayQualityChecker`: 0–100 quality score per symbol/freq; statuses OK/PARTIAL/MISSING/STALE/DUPLICATED/PRICE_ANOMALY/VOLUME_ANOMALY/INSUFFICIENT
- `intraday/opening_range_features.py` — `OpeningRangeFeatureBuilder`: 5/15/30-min return, volume ratio, range %, high/low break, strength score
- `intraday/vwap_features.py` — `VWAPFeatureBuilder`: intraday VWAP, price-vs-VWAP%, slope, above-VWAP ratio, reclaim/lost, support score
- `intraday/fake_breakout_detector.py` — `FakeBreakoutDetector`: volume-confirmed breakout, fake breakout risk/score, chase risk score, breakout quality
- `intraday/intraday_volume_profile.py` — `IntradayVolumeProfileBuilder`: cumulative VWAP, high-volume price zones, session distribution
- `intraday/microstructure_quality.py` — `MicrostructureQualityChecker`: INTRADAY_BAR_ONLY/TICK_PLANNED statuses; tick_api_ready=False, bidask_api_ready=False
- `intraday/tick_bidask_schema.py` — `TickBidaskSchema`: placeholder for future tick/bidask API (v0.4+)
- `reports/intraday_pipeline_report.py` — `IntradayPipelineReportBuilder`: Markdown report with quality, features, fake breakout, volume profile, tick readiness sections
- `gui/intraday_pipeline_panel.py` — `IntradayPipelinePanel`: PySide6 GUI with quality table, feature preview, fake breakout, volume profile, tick status; QThread workers
- `gui/intraday_pipeline_adapter.py` — `IntradayPipelineAdapter`: GUI bridge (run_pipeline, check_quality, preview_features)
- `docs/intraday_tick_pipeline.md` — documentation

### Modified Files

- `main.py` — 3 CLI commands: `intraday-pipeline` (--mode/--freq/--dry-run/--report), `intraday-quality` (--freq), `intraday-features` (--stock/--freq)
- `gui/dashboard.py` — guarded import + "Intraday Pipeline" tab
- `data/providers/data_freshness.py` — `intraday_1min` and `intraday_5min` freshness checks; `_check_intraday` handles standard pipeline datasets
- `quality/data_quality_gate.py` — `_compute_intraday_coverage_score` uses `IntradayQualityChecker`; tick/bidask planned = not a failure
- `reports/auto_report_center.py` — `include_intraday_pipeline` parameter; `run_intraday_pipeline_report()` method; full/daily profiles include intraday pipeline
- `reports/auto_report_index.py` — manifest records `intraday_quality_score`, `intraday_status`, `tick_bidask_readiness`
- `data/intraday_data_importer.py` — `load_intraday_standard()` method (prefers standardized path, falls back to legacy)
- `features/microstructure.py` — `microstructure_source` updated to `INTRADAY_BAR_ONLY`; `_enrich_last_bar_intraday()` helper adds opening range/VWAP/fake breakout features to last bar
- `features/indicators.py` — auto-load prefers `load_intraday_standard()` before legacy path
- `README.md` — v0.3.27 section
- `docs/roadmap.md` — v0.3.27 marked Done; v0.3.27 completed section added
- `docs/release_notes_v0.3.md` — this file
- `.gitignore` — intraday_pipeline_report_*.md, intraday standard directories excluded

### Safety

- Tick/bidask API: planned for v0.4+ — `tick_api_ready=False`, `bidask_api_ready=False` hardcoded
- No real orders. Production BLOCKED.

---

## v0.3.26 — Backtest Engine Hardening

**Status:** Superseded by v0.3.27

### New Files

- `backtest/execution_model.py` — `ExecutionModel`: signal_close/next_open/next_close/vwap_proxy entry; stop_loss/take_profit/trailing_stop/time_stop/combined exit; assumption recording
- `backtest/cost_model.py` — `CostModel`: Taiwan defaults (0.1425%×0.6 commission, 0.3% sell tax, 5bps slippage, min 20 NTD); PRESET_TAIWAN_REALISTIC and PRESET_ZERO_COST
- `backtest/liquidity_filter.py` — `LiquidityFilter`: min volume/turnover/participation checks; 0–100 liquidity score
- `backtest/gap_risk_model.py` — `GapRiskModel`: NO_GAP/GAP_UP_WARNING/GAP_UP_BLOCK/GAP_DOWN_WARNING/GAP_DOWN_STOP; gap stop-loss
- `backtest/validation_split.py` — `ValidationSplit`: walk_forward/out_of_sample/expanding_window/in_sample_only splits
- `backtest/regime_split.py` — `MarketRegimeSplitter`: bull/bear/sideways/high_volatility via MA20/MA60+rolling vol; proxy fallback
- `backtest/hardened_backtester.py` — `HardenedBacktester`: integrates all 6 models; A/B/C/D confidence grade; saves 5 result files
- `reports/hardened_backtest_report.py` — `HardenedBacktestReportBuilder`: 10-section Markdown report
- `gui/hardened_backtest_panel.py` — `HardenedBacktestPanel`: PySide6 GUI with 8 sections; QThread workers
- `gui/hardened_backtest_adapter.py` — `HardenedBacktestAdapter`: GUI bridge (no subprocess)
- `docs/backtest_engine_hardening.md` — documentation

### Modified Files

- `main.py` — `hardened-backtest` CLI command with 10 arguments
- `gui/dashboard.py` — guarded import + "Hardened Backtest" tab
- `reports/auto_report_center.py` — `include_hardened_backtest` parameter; `run_hardened_backtest_report()` method; full profile includes hardened backtest
- `README.md` — v0.3.26 section
- `docs/roadmap.md` — v0.3.26 marked Done; v0.3.27 Intraday pipeline planned
- `docs/release_notes_v0.3.md` — this file
- `.gitignore` — hardened_backtest_report_*.md and CSV/JSON exclusions

### Confidence Grade

| Grade | Criteria |
|-------|----------|
| A | trades≥100, splits≥4, each split count≥10, data quality≥75, max DD not extreme |
| B | trades≥50, splits≥2, data quality≥60 |
| C | trades≥20 |
| D | trades<20, insufficient data, too many missing prices |

> **Note:** Even Grade A does not authorize live trading. Production trading remains BLOCKED.

### Result Files (excluded from git)

- `data/backtest_results/hardened_backtest_trades.csv`
- `data/backtest_results/hardened_backtest_metrics.csv`
- `data/backtest_results/hardened_backtest_split_metrics.csv`
- `data/backtest_results/hardened_backtest_regime_metrics.csv`
- `data/backtest_results/hardened_backtest_assumptions.json`

### CLI

```
python main.py hardened-backtest --mode real --entry-model next_open --report
python main.py hardened-backtest --mode real --entry-model signal_close --zero-cost
python main.py hardened-backtest --mode real --split-method out_of_sample
python main.py hardened-backtest --mode mock --entry-model next_open
```

### Safety

- No real orders. No token in code. No weight auto-apply.
- Real mode never falls back to mock.
- Production trading remains BLOCKED.

---

## v0.3.25 — Universe Expansion & Sector Classification

**Status:** Superseded by v0.3.26

### New Files

- `universe/__init__.py` — package init
- `universe/universe_registry.py` — `UniverseRegistry`: 13 universe groups, build_default_universes(), export_universe_manifest()
- `universe/sector_classifier.py` — `SectorClassifier`: 9-sector taxonomy, classify_symbol(), classify_universe(), get_sector_summary()
- `universe/universe_quality.py` — `UniverseQualityAnalyzer`: 0–100 quality score (6 components); readiness levels
- `universe/universe_expander.py` — `UniverseExpander`: propose_expansion() — proposals only, no auto-write
- `reports/universe_expansion_report.py` — `UniverseExpansionReportBuilder`: 8-section Markdown report
- `gui/universe_manager_panel.py` — `UniverseManagerPanel`: PySide6 GUI tab with selector, symbol table, sector summary, quality cards
- `gui/universe_manager_adapter.py` — `UniverseManagerAdapter`: GUI bridge (no subprocess)
- `config/universe/sector_taxonomy.yaml` — 9 sectors with themes and keywords
- `config/universe/default_universe_seed.csv` — 60 Taiwan stocks with sector/theme/ai_exposure
- `docs/universe_expansion_and_sector_classification.md` — documentation

### Modified Files

- `data/providers/auto_fetcher.py` — `DataProviderAutoFetcher` accepts `universe_name` parameter; `_load_universe()` queries `UniverseRegistry` if specified
- `workflow/daily_workflow.py` — `DailyResearchWorkflow` accepts `universe_name`; passed to auto_fetcher step
- `reports/auto_report_center.py` — `AutoReportCenter` accepts `universe_name`; recorded in `_context` and manifest
- `reports/auto_report_index.py` — manifest includes `universe_name` field
- `quality/data_quality_gate.py` — `DataQualityGate` accepts `universe` parameter; blends in symbol-level coverage when specified
- `gui/dashboard.py` — guarded import for `UniverseManagerPanel`; new "Universe Manager" tab
- `README.md` — added v0.3.25 section
- `docs/roadmap.md` — v0.3.25 marked Done
- `docs/release_notes_v0.3.md` — this file

### Universe Groups

| Group | Size | Description |
|-------|------|-------------|
| core_14 | 14 | Original core universe |
| core_30 | 30 | Core 30 |
| core_50 | 50 | Core 50 |
| core_100 | 100 | Core 100 |
| core_200 | 200 | Core 200 |
| ai_mainstream | var | AI mainstream (TSMC, MediaTek, Delta, Foxconn...) |
| semiconductor | var | Semiconductor supply chain |
| high_speed_interconnect | var | High-speed networking / PCIe / CoWoS |
| server_supply_chain | var | Server and storage supply chain |
| power_thermal | var | Power supply and thermal management |
| financial | var | Banking, insurance, securities |
| etf_candidates | var | ETF component proxies |
| institutional_focus | var | High institutional net-buy focus |

### Universe Quality Score Formula

```
score = 0.25 * coverage
      + 0.20 * freshness
      + 0.20 * provider_reliability
      + 0.15 * sector_balance
      + 0.10 * liquidity
      + 0.10 * backtest_sample_readiness
```

Readiness levels: INSUFFICIENT (0–39), OBSERVATIONAL (40–59), RESEARCH_READY (60–74), BACKTEST_READY (75–89), STRONG_RESEARCH_UNIVERSE (90–100)

### CLI

```
python main.py universe-list
python main.py universe-build-defaults [--force]
python main.py universe-show --universe core_50
python main.py universe-quality-score --universe core_50 [--mode real]
python main.py universe-expand --from core_30 --target-size 50
python main.py universe-report --universe core_50 [--mode real] [--report-dir reports]
```

### Safety

- No real orders. No token in code. No weight auto-apply.
- Universe expansion proposals only — no files written automatically.
- Production trading remains BLOCKED.

---

## v0.3.24 — Data Provider Reliability & Fallback Matrix

**Status:** Superseded by v0.3.25

### New Files

- `data/providers/reliability_matrix.py` — `ProviderReliabilityMatrix` engine: builds provider summary, dataset fallback matrix, and dataset confidence scores
- `data/providers/provider_metrics.py` — `ProviderMetricsCollector`: reads fetch/health/scheduler logs to compute provider success rates and row coverage
- `data/providers/dataset_confidence.py` — `DatasetConfidenceScorer`: 0–100 confidence score per dataset using 6-component weighted formula
- `reports/provider_reliability_report.py` — `ProviderReliabilityReportBuilder`: generates `provider_reliability_report_YYYY-MM-DD.md`
- `gui/provider_reliability_panel.py` — `ProviderReliabilityPanel`: PySide6 GUI panel with provider table, fallback matrix, confidence table, and action buttons
- `gui/provider_reliability_adapter.py` — `ProviderReliabilityAdapter`: GUI bridge to `ProviderReliabilityMatrix` (no subprocess)
- `docs/provider_reliability_matrix.md` — documentation for v0.3.24 system

### Modified Files

- `data/providers/provider_registry.py` — added `get_provider_fallback_chain()`, `get_provider_reliability_metadata()`, `get_dataset_capability_matrix()`; extended `_DATASET_PROVIDER_PRIORITY` with tpex/mops fallbacks; added `_PROVIDER_RELIABILITY_METADATA`
- `data/providers/auto_fetcher.py` — `select_provider()` now consults registry fallback chain; `_build_result()` records `fallback_reason`, `primary_provider`, `fallback_provider`, `is_local_fallback`
- `data/providers/data_freshness.py` — `_make_result()` now includes `stale_reason`, `dataset_confidence_input`, `missing_symbol_count`
- `automation/task_runner.py` — `run_daily_data_update()` now includes `provider_reliability_summary` and `dataset_confidence_summary`
- `reports/auto_report_center.py` — added `run_provider_reliability_report()` method; `full` and `daily` profiles include `include_provider_reliability=True`
- `reports/auto_report_index.py` — manifest now includes `provider_reliability` section with `provider_reliability_score`, `weak_datasets`, `fallback_used`
- `main.py` — new CLI: `python main.py provider-reliability [--report] [--dataset X] [--provider X] [--mode real]`
- `gui/dashboard.py` — new `Provider Reliability` tab (v0.3.24)
- `README.md` — added v0.3.24 section
- `docs/roadmap.md` — v0.3.24 marked Done; v0.3.25 updated

### Dataset Fallback Chains (No Mock Fallback)

| Dataset | Primary | Fallbacks | Mock Fallback |
|---------|---------|-----------|---------------|
| daily_price | finmind | twse → tpex → csv → xq_export | disabled |
| monthly_revenue | finmind | twse → mops → csv → xq_export | disabled |
| institutional | finmind | twse → tpex → csv → xq_export | disabled |
| margin | finmind | twse → tpex → csv → xq_export | disabled |
| fundamental | finmind | mops → csv → xq_export | disabled |
| intraday | csv | xq_export → planned_tick_provider | disabled |
| tick | planned_tick_provider | — | disabled |
| bidask | planned_bidask_provider | — | disabled |

### Dataset Confidence Score Formula

```
score = 0.30 * provider_reliability
      + 0.25 * freshness
      + 0.20 * coverage
      + 0.10 * schema_completeness
      + 0.10 * source_priority
      + 0.05 * mock_clean
```

Score levels: HIGH (90–100), GOOD (75–89), PARTIAL (60–74), WEAK (40–59), LOW (0–39)

### Safety

- Mock fallback in real mode: always 0 / DISABLED
- No real orders. No token in code. No weight auto-apply.
- Production trading remains BLOCKED.

### CLI

```
python main.py provider-reliability
python main.py provider-reliability --report
python main.py provider-reliability --dataset daily_price
python main.py provider-reliability --provider finmind
```

---

## v0.3.23 — Documentation & Release Notes Pack

**Status:** Current

### Changes

- Added comprehensive documentation pack: 9 docs files
  - `docs/index.md` — full documentation index
  - `docs/README.md` — quick links pointer
  - `docs/user_guide.md` — daily usage, scores, GUI overview
  - `docs/cli_reference.md` — all commands with examples and safety notes
  - `docs/gui_guide.md` — tab descriptions, empty states, warnings
  - `docs/daily_research_sop.md` — step-by-step daily procedures
  - `docs/safety_and_limitations.md` — hard-coded invariants, backtest limits
  - `docs/developer_guide.md` — architecture, adding CLI/GUI/reports, git conventions
  - `docs/release_notes_v0.3.md` — this file; v0.3.9–v0.3.23 change log
  - `docs/roadmap.md` — completed milestones, future v0.3.24–v0.4.x plans
  - `docs/troubleshooting.md` — 13 common problems with fixes
- Restructured `README.md` with navigation to docs/

### No source code changes

Documentation-only release.

---

## v0.3.22 — Usability QA & Error Message Polish

### New Files

| File | Purpose |
|------|---------|
| `utils/status_labels.py` | 20 status constants + 7 normalization helpers |
| `utils/user_facing_errors.py` | `UserFacingError` + `UserFacingErrorFormatter` (14 exception types) |
| `utils/cli_output.py` | `CLIOutput` Windows cp950-safe formatter; safety banner |
| `qa/usability_smoke_test.py` | 8 CLI + 8 GUI smoke tests; CSV summary output |
| `reports/usability_qa_report.py` | 7-section Markdown QA report builder |
| `gui/usability_qa_panel.py` | Usability QA tab with QThread workers |
| `gui/usability_qa_adapter.py` | Adapter: run_smoke_test, generate_report, load_latest |

### Modified Files

| File | Change |
|------|--------|
| `quality/data_quality_gate.py` | Added `_build_blockers()` method; `blockers` in result dict |
| `workflow/daily_workflow.py` | `_run_step()` attaches `UserFacingErrorFormatter` metadata to `step.extra` |
| `automation/task_runner.py` | `_make_result()` adds usability fields: safety_banner_present, user_message, can_ignore, next_steps |
| `data/providers/auto_fetcher.py` | `_make_summary()` adds `warning_details` structured list |
| `gui/portfolio_widgets.py` | `StatusBadge` uses `normalize_status()`; `DataFrameTableModel` guards empty df; `EmptyStateWidget` new signature |
| `gui/dashboard.py` | Usability QA tab added (guarded import) |
| `main.py` | `usability-smoke-test` and `usability-qa-report` commands added |

### CLI additions

```bash
python main.py usability-smoke-test [--report]
python main.py usability-qa-report
```

---

## v0.3.21 — Daily Workflow Engine

### New Features

- `DailyResearchWorkflow` class in `workflow/daily_workflow.py`
- Step-based execution: update_data → run_research → data_quality_gate → auto_report
- Profile support: quick (2 steps), standard (4 steps), full (6 steps)
- Per-step timing, status, and extra metadata
- Workflow summary report: `reports/daily_workflow/YYYY-MM-DD/workflow_summary.md`
- CLI: `daily-workflow` and `run-research` commands

---

## v0.3.20 — Data Quality Gate

### New Features

- `DataQualityGate` class in `quality/data_quality_gate.py`
- Composite scoring: Production Readiness (0–100), Backtest Readiness (0–100)
- Sub-scores: freshness, coverage, source_confidence, institutional_completeness
- Gate decisions: STRONG / READY_FOR_RESEARCH / PARTIAL / WEAK / BLOCKED
- Mock contamination detection
- Backtest Readiness caps (60 if mock_contamination < 90; 70 if coverage < 70)
- CLI: `data-quality-gate`
- GUI: Data Quality Gate tab
- Report: `data_quality_gate_report_YYYY-MM-DD.md`

---

## v0.3.19 — Data Provider Auto Fetch

### New Features

- `AutoFetcher` in `data/providers/auto_fetcher.py`
- Per-provider, per-dataset fetch with retry logic
- Structured `warning_details` in fetch summary
- CLI: `fetch-provider`
- GUI: Data Provider Fetch tab

---

## v0.3.18 — API Provider Hardening

### New Features

- `ProviderRegistry` — central provider configuration
- Token status: CONFIGURED / NOT_CONFIGURED / INVALID
- Capability matrix per provider
- CLI: `provider-health`
- GUI: Provider Health tab

---

## v0.3.17 — Automation Scheduler

### New Features

- `TaskRunner` in `automation/task_runner.py`
- Task scheduling with configurable intervals
- Manual trigger support
- Result structured with safety_banner_present, user_message, can_ignore, next_steps
- CLI: `list-tasks`, `run-task`
- GUI: Automation Scheduler tab

---

## v0.3.16 — Auto Report Center

### New Features

- `AutoReportCenter` in `reports/auto_report_center.py`
- Daily report generation: daily_summary, signal_quality, portfolio_simulation, data_quality_gate
- Date-organized output: `reports/auto_report_center/YYYY-MM-DD/`
- CLI: `auto-report`
- GUI: Auto Report Center tab

---

## v0.3.15 — Rule Weight Tuning Lab

### New Features

- 7 weight configuration comparison
- Best config identification by composite score
- Manual-review-only constraint (no auto-apply)
- CLI: `tune-rule-weights`
- GUI: Rule Weight Tuning tab

---

## v0.3.14 — Signal Quality Dashboard

### New Features

- Per-rule signal quality scoring
- BOOST / KEEP / REDUCE / DISABLE classification
- Confidence scoring
- CLI: `signal-quality`
- GUI: Signal Quality tab

---

## v0.3.13 — GUI Portfolio Cockpit

### New Features

- Portfolio Cockpit GUI tab
- KPI summary cards (Sharpe, MaxDD, Profit Factor)
- Equity curve and drawdown charts
- Trade log table
- `StatusBadge`, `DataFrameTableModel`, `EmptyStateWidget` shared widgets

---

## v0.3.12 — Portfolio & Risk Simulation

### New Features

- Portfolio simulation engine
- Sharpe ratio, MaxDD, Profit Factor calculation
- CLI: `portfolio-simulation`
- Report: `portfolio_simulation_report_YYYY-MM-DD.md`

---

## v0.3.11 — Long-Term Strategy Validation

### New Features

- Multi-year backtest validation
- Strategy performance consistency analysis
- CLI: `long-term-validation`
- Included in `--profile full`

---

## v0.3.10 — Intraday OHLC & Microstructure

### Changes (commit `569c7ee`)

- Fixed intraday OHLC column mapping
- Fixed microstructure_source display

---

## v0.3.9 — Public Data API Layer

### New Features

- TWSE public data endpoints (no token required)
- `twse_public` provider in provider registry
- CLI: public data fetch via `fetch-provider --provider twse_public`

---

*TW Quant Cockpit v0.3.23 — Research Only — Not Investment Advice*
