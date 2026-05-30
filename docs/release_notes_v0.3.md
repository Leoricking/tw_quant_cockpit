# TW Quant Cockpit — Release Notes v0.3

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**

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
