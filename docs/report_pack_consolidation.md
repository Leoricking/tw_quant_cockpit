# Report Pack Consolidation — TW Quant Cockpit v0.5.4

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.

## Overview

The Report Pack Consolidation module (`report_pack/`) provides a unified view of all research report outputs. It assembles daily, weekly, or full report bundles, checks their health, and generates a consolidated Markdown report.

## Package Structure

```
report_pack/
├── __init__.py                  — Package exports
├── report_pack_schema.py        — ReportPackItem, ReportPack dataclasses
├── report_registry.py           — ReportRegistry (daily/weekly/full definitions)
├── report_collector.py          — ReportCollector (file-system scanner)
├── report_pack_builder.py       — ReportPackBuilder (assembles pack)
├── report_health_checker.py     — ReportHealthChecker (HEALTHY/DEGRADED/CRITICAL)
├── report_link_registry.py      — ReportLinkRegistry (CLI→GUI→doc mapping)
└── report_pack_store.py         — ReportPackStore (CSV persistence)

reports/
└── report_pack_consolidation_report.py   — 8-section Markdown report

gui/
├── report_pack_panel.py         — PySide6 GUI panel
└── report_pack_adapter.py       — Non-GUI bridge
```

## Pack Types

| Pack Type | Report Count | Description |
|-----------|-------------|-------------|
| `daily`   | 9           | Core daily: market, signals, data quality, portfolio |
| `weekly`  | 16          | Weekly + strategy, governance, workflow, OS, CLI/GUI |
| `full`    | 20          | All types: weekly + regression, replay, release, safety |
| `custom`  | —           | User-defined via ReportRegistry |

## Report Types (20 total)

| Report Type | CLI Command | GUI Tab |
|-------------|-------------|---------|
| daily_market | `auto-report --profile daily` | daily_workflow |
| auto_report | `auto-report` | daily_workflow |
| data_quality | `data-quality-gate` | data_quality |
| provider | `provider-reliability` | provider |
| strategy_filter | `strategy-filter-pack` | strategy_filter |
| signal_quality | `signal-quality-report` | signal_quality |
| rule_governance | `rule-governance-report` | rule_governance |
| portfolio_journal | `journal-summary` | portfolio_journal |
| research_review | `research-review-report` | research_review |
| research_coach | `research-coach-report` | research_coach |
| research_workflow | `research-workflow-report` | research_workflow |
| research_os | `research-os-report` | research_os |
| regression | `regression-run` | regression_suite |
| cli_ux | `cli-ux-report` | cli_ux |
| gui_navigation | `gui-nav-report` | gui_navigation |
| notification | `notification-list` | notification |
| intraday_replay | `intraday-replay-report` | intraday_replay |
| experiment | `experiment-registry` | experiment_registry |
| release | `stable-release-check` | release_status |
| safety | `regression-run --suite safety` | release_status |

## CLI Commands

```bash
# Build a report pack
python main.py report-pack --pack-type daily
python main.py report-pack --pack-type weekly
python main.py report-pack --pack-type full

# Show latest summary
python main.py report-pack-summary --pack-type daily

# Show report items
python main.py report-pack-items --pack-type daily

# Check health
python main.py report-pack-health --pack-type daily

# Show link index
python main.py report-pack-links

# Generate consolidation report
python main.py report-pack-report --pack-type daily --mode real
```

## Output Paths

All outputs are gitignored:
- `data/backtest_results/report_pack/{pack_type}_YYYY-MM-DD/index.md`
- `data/backtest_results/report_pack/{pack_type}_YYYY-MM-DD/manifest.json`
- `data/backtest_results/report_pack/report_pack_summary_YYYY-MM-DD.csv`
- `data/backtest_results/report_pack/report_pack_items_*.csv`
- `data/backtest_results/report_pack/report_pack_health_*.csv`
- `reports/report_pack_consolidation_report_YYYY-MM-DD.md`

## Health Check

| Label | Score | Meaning |
|-------|-------|---------|
| HEALTHY | ≥ 80% | All core reports ready |
| DEGRADED | 50–79% | Some reports missing |
| CRITICAL | < 50% | Many reports missing or failed |

## Safety

- `generate_missing=False` by default — does NOT auto-generate reports
- No recursive loop — does NOT call `auto-report full` from inside report_pack
- All classes carry `no_real_orders=True`, `production_blocked=True`

---

*TW Quant Cockpit v0.5.4 — Research Only — Not Investment Advice*
