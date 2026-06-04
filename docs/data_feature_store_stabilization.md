# Data / Feature Store Stabilization — TW Quant Cockpit v0.5.5

> [!] **Data Stabilization Only. Research Only. No Real Orders. Production Trading: BLOCKED.**

---

## Overview

v0.5.5 introduces the **Data / Feature Store Stabilization** subsystem, which strengthens the
data layer with end-to-end traceability, schema governance, feature readiness gating, and
data leakage prevention.

It is **read-only** and **metadata-only**: it scans file system metadata and CSV headers, never
loads full dataset content, never connects to a broker, and never places real orders.

---

## Architecture

```
data_stabilization/
├── __init__.py                   — Package exports
├── data_schema_registry.py       — 22 dataset schemas, 5 categories
├── data_lineage_tracker.py       — File-system lineage scan, MD5 (first 64KB), freshness
├── feature_readiness_checker.py  — Per-group readiness: READY/PARTIAL/MISSING/STALE/LEAKAGE_RISK/FAILED
├── feature_store_health.py       — Aggregate health: HEALTHY/DEGRADED/PARTIAL/BLOCKED/UNKNOWN
├── leakage_guard.py              — Forbidden keyword guard; distinguishes feature input vs label output
├── data_stabilization_store.py   — CSV persistence (6 save + 6 load methods)
└── data_stabilization_engine.py  — Orchestrator; outputs 6 CSV files

gui/
├── data_stabilization_adapter.py — Non-GUI bridge (run_stabilization, generate_report, load_latest_*)
└── data_stabilization_panel.py   — PySide6 GUI panel (7 sections)

reports/
└── data_stabilization_report.py  — 9-section Markdown report
```

---

## Dataset Schema Registry

22 schemas across 5 categories:

| Category        | Schemas |
|----------------|---------|
| Market          | daily_k, intraday_1min, intraday_5min, tick, bidask |
| Financial       | monthly_revenue, quarterly_financials, eps, gross_margin, operating_margin |
| Chip            | institutional_trading, margin_balance, short_selling, foreign_buy |
| Feature Store   | technical_features, microstructure_features, financial_features, chip_features, strategy_filter_features, ml_knowledge_features |
| Runtime         | signal_log, trade_journal, regime_labels |

Each schema defines: `dataset_name`, `category`, `required_columns`, `optional_columns`,
`freshness_rule`, `source_provider`.

---

## Data Lineage Tracker

- Scans `data/` directory for CSV files matching known schema names
- Records: `dataset_name`, `path`, `source_provider`, `modified_at`, `size_bytes`, `rows`, `columns`
- MD5 hash: **first 64KB only** — never logs data content
- CSV sampling: **header + 5 rows only**
- Freshness: `FRESH` (<1 day), `STALE` (1–7 days), `VERY_STALE` (>7 days), `MISSING`

---

## Feature Readiness Checker

6 feature groups, each with a list of expected CSV files:

| Feature Group             | Status Values |
|--------------------------|---------------|
| technical_features        | READY / PARTIAL / MISSING / STALE / LEAKAGE_RISK / FAILED |
| microstructure_features   | Same |
| financial_features        | Same |
| chip_features             | Same |
| strategy_filter_features  | Same |
| ml_knowledge_features     | Same |

**Score logic:** READY=100, PARTIAL/STALE=50, MISSING=0.

---

## Feature Store Health

Aggregates readiness into an overall health score:

| Status   | Condition |
|----------|-----------|
| HEALTHY  | All feature groups READY |
| DEGRADED | ≥70% READY |
| PARTIAL  | <70% READY or >50% MISSING |
| BLOCKED  | Any LEAKAGE_RISK detected |
| UNKNOWN  | No readiness data |

---

## Leakage Guard

Conservative approach: unknown → WARNING.

**Forbidden feature input keywords:**
`future`, `next_return`, `next_close`, `next_high`, `next_low`,
`label`, `target`, `forward`, `tomorrow`, `future_return`, `realized_return`

**Exempted in label/outcome datasets:**
`future_return`, `realized_return`, `label`, `target` are OK in:
`label`, `outcome`, `target`, `journal`, `signal_outcome`, `replay_score` datasets.

Severity: `HIGH` (forbidden column in feature input), `MEDIUM` (auto_enabled without backtest_passed),
`WARNING` (unknown / path check).

---

## CLI Commands

```bash
# Run all stabilization checks and save 6 CSV outputs
python main.py data-stabilization --mode real

# Generate 9-section Markdown report
python main.py data-stabilization-report --mode real

# Show latest summary from store (no re-run required)
python main.py data-stabilization-summary

# Show data lineage records from store
python main.py data-lineage

# Show feature readiness results from store
python main.py feature-readiness

# Show feature store health from store
python main.py feature-store-health

# Show leakage guard findings from store
python main.py leakage-guard
```

---

## Output Files

All outputs written to `data/backtest_results/data_stabilization/` (gitignored):

| File | Contents |
|------|----------|
| `data_stabilization_summary_YYYY-MM-DD.csv` | Overall summary: status, scores, counts |
| `dataset_schema_status_YYYY-MM-DD.csv` | Schema registry dump |
| `data_lineage_YYYY-MM-DD.csv` | Per-dataset lineage records |
| `feature_readiness_YYYY-MM-DD.csv` | Per-group readiness status and scores |
| `feature_store_health_YYYY-MM-DD.csv` | Aggregate health metrics |
| `leakage_guard_summary_YYYY-MM-DD.csv` | Leakage findings |

Report written to `reports/data_stabilization_report_YYYY-MM-DD.md` (gitignored).

---

## Integration

- **Auto Report Center:** `include_data_stabilization=True` in `full` and `daily` profiles;
  loads summary only — does NOT run full engine (avoids recursive loop)
- **Report Pack:** `data_stabilization` added to daily/weekly/full pack definitions
- **Report Index (manifest.json):** 5 new fields: `data_stabilization_status`,
  `feature_readiness_score`, `feature_store_health_score`, `leakage_warning_count`,
  `data_lineage_records`
- **Snapshot Builder:** `build_data_stabilization_snapshot()` added to `build_all()`
- **Regression Suite (SUITE_DATA):** 5 new tests including import check and CLI smoke tests
- **Stable Release Checklist:** 6 new checks (import, no_real_orders, schema registry,
  feature readiness, leakage guard, output ignored)
- **GUI Tab Registry:** `data_stabilization` tab in `data_providers` group, P1 priority
- **GUI Dashboard:** Data Stabilization tab added after Report Pack tab

---

## Safety Invariants

All classes carry:
```python
read_only          = True
no_real_orders     = True
production_blocked = True
real_order_ready   = False
```

No broker connection. No BUY/SELL/ORDER. No subprocess shell=True.
Metadata-only scan: file system attributes + CSV header + 5 rows.

---

*TW Quant Cockpit v0.5.5 — Data Stabilization Only — Not Investment Advice*
