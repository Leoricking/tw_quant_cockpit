# TW Quant Cockpit — Data Coverage Expansion v0.6.2

> **[!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.**

---

## Overview

v0.6.2 introduces a comprehensive data coverage tracking system that scans the filesystem for
actual data files and classifies each data item's availability status across 12 research domains.

The system tracks ~35 data items and classifies each as:

| Status | Meaning |
|--------|---------|
| `READY` | File(s) found with size > 0 |
| `ENV_LIMITED` | Requires environment token (e.g. FINMIND_TOKEN) not set |
| `NOT_GENERATED` | Optional / on-demand item not yet generated |
| `MISSING_OPTIONAL` | Optional item not found |
| `MISSING_REQUIRED` | Required item not found — action needed |
| `PARTIAL` | Files found but incomplete |
| `FAILED` | Scanner error |

---

## Domains

| Domain | Items | Description |
|--------|-------|-------------|
| `provider` | 5 | Provider health, reliability, FinMind token, TWSE, API diagnostics |
| `daily_data` | 5 | Daily K-line, monthly revenue, institutional, margin, major holders |
| `intraday` | 4 | 1-min/5-min OHLCV, quality, pipeline report |
| `financial` | 4 | EPS, quarterly financials, gross margin, operating margin |
| `feature_store` | 5 | Technical, microstructure, financial, chip, ML knowledge features |
| `replay` | 3 | Intraday replay report, replay training report, replay training summary |
| `experiment` | 3 | Experiment registry, report, snapshots |
| `rule_governance` | 3 | Rule governance report, rule confidence, strategy knowledge summary |
| `report_pack` | 3 | Full report pack, health, links |
| `stable_release` | 3 | Stable release report, manifest, v0.6.0 check |

---

## CLI Commands

```bash
# Run full coverage scan
python main.py data-coverage --mode real

# Show coverage scan from store (no rescan)
python main.py data-coverage-summary

# List all items from store
python main.py data-coverage-items

# Generate Markdown coverage report
python main.py data-coverage-report --mode real

# Show gaps only (missing required + optional)
python main.py data-coverage-gaps
```

---

## Coverage Score

The engine computes a weighted coverage score (0–100):

- Required READY: +3.0 points each
- Optional READY: +1.0 point each
- ENV_LIMITED: partial credit, small penalty
- MISSING_OPTIONAL: -0.2 penalty
- MISSING_REQUIRED: 0 points
- FAILED: -2.0 heavy penalty

---

## GUI Panel

The Data Coverage tab is available in the Cockpit GUI:

- **Summary Cards**: Total, Ready, ENV Limited, Not Generated, Missing Required, Score
- **Domain Filter**: Filter matrix by domain
- **Coverage Matrix Table**: Domain / Item / Status / Required / Suggested Command / Warning
- **Gaps Panel**: Blockers and warnings
- **Run Scan**: Trigger background scan via QThread
- **Generate Report**: Create Markdown report

Empty state: displays "尚未執行掃描，請點擊 Run Scan"

---

## Architecture

```
data_coverage/
  __init__.py                    # Package init
  data_coverage_schema.py        # DataCoverageItem, DataCoverageSummary, constants
  data_coverage_registry.py      # DataCoverageRegistry (35 items)
  data_coverage_scanner.py       # DataCoverageScanner (glob matching, classify_status)
  data_coverage_engine.py        # DataCoverageEngine (orchestrator, scoring)
  data_coverage_store.py         # DataCoverageStore (CSV save/load)

reports/data_coverage_report.py  # DataCoverageReport (Markdown report)
gui/data_coverage_panel.py       # DataCoveragePanel (PySide6 GUI)
gui/data_coverage_adapter.py     # DataCoverageAdapter (GUI-to-backend bridge)
```

---

## Integration

- **Report Pack**: `REPORT_DATA_COVERAGE` added to schema; included as optional in PACK_FULL
- **Regression Suites**: Added to `data`, `report`, and `release_gate` suites
- **Stable Release Checklist**: Checks `data_coverage.data_coverage_engine` importability
- **Capability Matrix**: "Data Coverage Expansion" capability added
- **Auto Report Center**: Optional `include_data_coverage=True` in `full` profile
- **GUI Navigation**: Tab registered in `data_providers` group

---

## Safety

```
[!] Data Coverage Only | Research Only | No Real Orders | Production BLOCKED
```

- All classes have `read_only = True`, `no_real_orders = True`, `production_blocked = True`
- No broker connections, no real orders, no live market access
- FINMIND_TOKEN presence checked via `os.environ.get()` — value never printed or logged
- All outputs are read-only filesystem scans
