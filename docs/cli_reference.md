# TW Quant Cockpit — CLI Reference (v0.5.1)

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**

---

## Usage

```bash
python main.py <command> [options]
```

All commands are read-only research operations. No orders are ever placed.

---

## Command Categories

- [Daily Workflow](#daily-workflow)
- [Data](#data)
- [Research](#research)
- [Reports](#reports)
- [Scheduler](#scheduler)
- [GUI](#gui)
- [QA & Diagnostics](#qa--diagnostics)

---

## Daily Workflow

### `daily-workflow`

Run the full daily pipeline (update-data → run-research → open report).

```bash
python main.py daily-workflow --mode real --profile standard
python main.py daily-workflow --mode real --profile quick
python main.py daily-workflow --mode real --profile full
python main.py daily-workflow --mode mock --profile standard
```

**Options:**

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--mode` | `real`, `mock` | `real` | Data mode |
| `--profile` | `quick`, `standard`, `full` | `standard` | Step set |

**Profiles:**

| Profile | Steps | Est. Time |
|---------|-------|-----------|
| `quick` | data_quality_gate + auto_report | ~30s |
| `standard` | update-data + run-research + data_quality_gate + auto_report | ~3min |
| `full` | All steps including long-term backtest | ~10min |

**Output:** `reports/daily_workflow/YYYY-MM-DD/workflow_summary.md`

**Safety:** Read-only. No orders. No data writes.

**Common warnings:**
- `FINMIND_TOKEN not configured` — provider will use cached data only
- `Step 'update_data' took longer than expected` — network latency; non-blocking

---

### `run-research`

Run the research analysis pipeline.

```bash
python main.py run-research --mode real --profile standard
python main.py run-research --mode mock --profile quick
```

**Options:**

| Option | Values | Default |
|--------|--------|---------|
| `--mode` | `real`, `mock` | `real` |
| `--profile` | `quick`, `standard`, `full` | `standard` |

**Output:** Signal quality report, portfolio simulation report in `reports/auto_report_center/YYYY-MM-DD/`

---

## Data

### `update-data`

Fetch latest market data from all configured providers.

```bash
python main.py update-data --mode real
python main.py update-data --mode real --dry-run
```

**Options:**

| Option | Description |
|--------|-------------|
| `--mode real` | Use real data sources |
| `--mode mock` | Use mock/cached data |
| `--dry-run` | Show what would be fetched; no writes |

**Data sources updated:**
- Daily price (OHLCV)
- Institutional (法人) buy/sell
- Margin trading (融資融券)
- Monthly revenue (月營收)

**Output:** Updated CSV files in `data/` (real mode only; dry-run prints plan)

**Safety:** `--dry-run` performs zero file writes.

**Common warnings:**
- `Provider 'finmind' returned 0 rows` — check FINMIND_TOKEN in `.env`
- `Data freshness STALE for institutional` — data >2 days old; non-blocking for research
- `Timeout fetching monthly_revenue` — retry or check network

---

### `data-quality-gate`

Run the data quality gate and display readiness scores.

```bash
python main.py data-quality-gate --mode real
python main.py data-quality-gate --mode mock
```

**Output:** Production Readiness Score, Backtest Readiness Score, blockers list, gate decision.

**Score thresholds:**

| Score | Gate Decision |
|-------|--------------|
| ≥ 90 | STRONG |
| 75–89 | READY_FOR_RESEARCH |
| 60–74 | PARTIAL |
| 40–59 | WEAK |
| 0–39 | BLOCKED |

**Report:** `reports/auto_report_center/YYYY-MM-DD/data_quality_gate_report_YYYY-MM-DD.md`

**Common warnings:**
- `MOCK_CONTAMINATION blocker` — mock data mixed with real; backtest score capped at 60
- `LOW_COVERAGE` — fewer than 70% of expected tickers have data

---

### `fetch-provider`

Manually trigger auto-fetch for a specific data provider.

```bash
python main.py fetch-provider --provider finmind --dataset daily_price
python main.py fetch-provider --provider fugle --dataset institutional
```

**Options:**

| Option | Description |
|--------|-------------|
| `--provider` | Provider name (finmind, fugle, twse_public) |
| `--dataset` | Dataset name |

**Common warnings:**
- `Token not configured` — set token in `.env`; fetch will be skipped

---

### `provider-health`

Check API provider token status and capabilities.

```bash
python main.py provider-health
```

**Output:** Table of providers with token status, capability, last fetch time.

---

## Research

### `signal-quality`

Run signal quality analysis and generate BOOST/KEEP/REDUCE recommendations.

```bash
python main.py signal-quality --mode real
python main.py signal-quality --mode mock
```

**Output:** `reports/auto_report_center/YYYY-MM-DD/signal_quality_report_YYYY-MM-DD.md`

**Labels:**

| Label | Meaning |
|-------|---------|
| BOOST | Rule contributes positively; consider weight increase |
| KEEP | Rule neutral; no change needed |
| REDUCE | Rule underperforms; consider weight decrease |
| DISABLE | Rule consistently negative; consider disabling |

**Safety:** Recommendations are for research review only. Weights are NOT auto-applied.

---

### `portfolio-simulation`

Run portfolio simulation with current signals.

```bash
python main.py portfolio-simulation --mode real
python main.py portfolio-simulation --mode mock
```

**Output:** `reports/auto_report_center/YYYY-MM-DD/portfolio_simulation_report_YYYY-MM-DD.md`

**KPI targets:** Sharpe > 1.5 | MaxDD < 20% | Profit Factor > 1.5

---

### `tune-rule-weights`

Compare 7 weight configurations and identify the best config.

```bash
python main.py tune-rule-weights --mode real
python main.py tune-rule-weights --mode mock
```

**Output:** Weight comparison table; best config stored in `data/rule_weight_tuning/`.

**Safety:** Best config is a suggestion only. Not auto-applied. Manual review required.

---

### `long-term-validation`

Run long-term strategy validation (multi-year backtest).

```bash
python main.py long-term-validation --mode real
```

**Note:** Takes ~5–10 min. Include via `--profile full` in `daily-workflow`.

---

## Reports

### `auto-report`

Generate the daily auto report.

```bash
python main.py auto-report --mode real
python main.py auto-report --mode mock
```

**Output directory:** `reports/auto_report_center/YYYY-MM-DD/`

**Reports generated:**
- `daily_summary_YYYY-MM-DD.md`
- `signal_quality_report_YYYY-MM-DD.md`
- `portfolio_simulation_report_YYYY-MM-DD.md`
- `data_quality_gate_report_YYYY-MM-DD.md`

---

### `usability-smoke-test`

Run smoke tests for CLI and GUI usability.

```bash
python main.py usability-smoke-test
python main.py usability-smoke-test --report
```

**Options:**

| Option | Description |
|--------|-------------|
| `--report` | Also generate Markdown QA report after test |

**Output:** `data/backtest_results/usability_smoke_test_summary.csv`

**Test categories:** CLI (8 tests), GUI import (8 tests)

**Common warnings:**
- `GUI tests SKIP` — PySide6 not installed; non-blocking for CLI-only use
- `Token NOT_CONFIGURED` — test passes with WARNING status; not a failure

---

### `usability-qa-report`

Generate the Usability QA Markdown report from latest smoke test results.

```bash
python main.py usability-qa-report
```

**Output:** `reports/auto_report_center/YYYY-MM-DD/usability_qa_report_YYYY-MM-DD.md`

---

## Scheduler

### `list-tasks`

List all scheduled automation tasks.

```bash
python main.py list-tasks
```

**Output:** Table of tasks with schedule, last run, next run, status.

---

### `run-task`

Manually trigger a scheduled task.

```bash
python main.py run-task --task daily_update
python main.py run-task --task weekly_backtest
```

---

## GUI

### `cockpit` / `open-cockpit`

Open the GUI cockpit.

```bash
python main.py cockpit --mode real
python main.py open-cockpit --mode real
python main.py cockpit --mode mock
```

**Requires:** PySide6 installed (`pip install PySide6`)

**Opens:** Full GUI with all tabs. See [GUI Guide](gui_guide.md).

---

## QA & Diagnostics

### `mock-realtime`

Run a mock real-time data simulation session.

```bash
python main.py mock-realtime
```

**Safety:** Uses mock data only. No real market connections.

---

### `paper`

Run paper trading simulation (no real orders).

```bash
python main.py paper --mode mock
```

**Safety:** REAL_ORDER_READY=False. No orders placed.

---

## Global Options

| Option | Description |
|--------|-------------|
| `--mode real` | Use real data files |
| `--mode mock` | Use mock/test data |
| `--dry-run` | Preview actions without writing |
| `--profile quick\|standard\|full` | Step set for workflow commands |

---

## Safety Banner

Every command prints a safety banner:

```
Read Only         : YES
No Real Orders    : YES
Production Trading: BLOCKED
Real Order Ready  : NO
```

This banner confirms the system's read-only, no-order guarantee.

---

---

## Aliases (v0.5.1)

Short aliases for common workflows. Each alias maps to an existing command.

| Alias | Equivalent To | Notes |
|-------|--------------|-------|
| `daily` | `run-research --profile daily` | Daily research workflow |
| `quick` | `run-research --profile quick` | Quick research run |
| `dq` | `data-quality-gate` | Data quality check |
| `quality` | `data-quality-gate` | Data quality check |
| `providers` | `provider-reliability` | Provider status |
| `rules` | `rule-governance` | Rule governance |
| `signals` | `signal-quality` | Signal quality |
| `journal` | `journal-summary` | Journal summary |
| `notify` | `notification-list` | Notifications |
| `coach-daily` | `research-coach --period daily` | Daily coaching |
| `review-daily` | `research-review --period daily` | Daily review |
| `workflow-daily` | `research-workflow --type daily_research` | Daily workflow |
| `workflow-weekly` | `research-workflow --type weekly_review` | Weekly workflow |
| `os` | `research-os-summary` | OS summary |
| `version` | `version-info` | Version info |
| `gui` | `cockpit` | Launch GUI |
| `dashboard` | `cockpit` | Launch GUI |

---

## Quick Start

```bash
python main.py version-info
python main.py research-os-summary
python main.py run-research --profile quick --mode real
python main.py auto-report --mode real --profile daily
python main.py cockpit --mode real
```

---

## Daily Research Workflow

```bash
python main.py data-quality-gate --mode real
python main.py provider-reliability --mode real
python main.py research-coach --mode real --period daily
python main.py research-workflow --mode real --type daily_research --dry-run
python main.py research-workflow --mode real --type daily_research
```

Or using aliases:
```bash
python main.py dq --mode real
python main.py providers --mode real
python main.py coach-daily --mode real
python main.py workflow-daily --mode real --dry-run
python main.py workflow-daily --mode real
```

---

## Weekly Review

```bash
python main.py research-review --mode real --period weekly
python main.py journal-summary
python main.py rule-governance --mode real
python main.py experiment-list
python main.py research-workflow --mode real --type weekly_review
```

---

## Research OS Commands (v0.5.0–v0.5.1)

```bash
python main.py research-os-summary          # OS inventory summary
python main.py research-os-audit            # Full OS audit
python main.py research-os-modules          # List all modules
python main.py research-os-cli              # List all CLI commands
python main.py research-os-gui              # List all GUI tabs
python main.py research-os-safety           # Safety matrix
python main.py research-os-report           # Generate stabilization report
```

---

## CLI UX Commands (v0.5.1)

```bash
python main.py cli-list                     # List all commands
python main.py cli-list --category data     # Filter by category
python main.py cli-search --keyword replay  # Search by keyword
python main.py cli-aliases                  # Show alias map
python main.py cli-examples                 # Show help examples
python main.py cli-examples --category daily
python main.py cli-resolve --alias dq       # Resolve alias (display only)
python main.py cli-ux-report --mode real    # Generate UX report
```

---

## Safety Commands

```bash
python main.py stable-release-check --mode real
python main.py regression-suite --mode real --quick
python main.py research-os-safety
python main.py version-info
```

---

*TW Quant Cockpit v0.5.1 — Research Only — Not Investment Advice*
