# Backtest Training Metrics v0.8.2

**[!] Research Only. No Real Orders. Production Trading BLOCKED.**
**[!] Not Investment Advice. No BUY/SELL/ORDER output.**

---

## Overview

Backtest Training Metrics (v0.8.2) measures and tracks training effectiveness
across all Research OS modules. It collects data from the Backtest-to-Coach Loop,
Replay Training, Strategy Memory, Portfolio Journal, and Regression Suite to
produce trend-aware metrics that help you understand your research improvement
over time.

---

## Metric Types

| Metric Type | Source | Description |
|-------------|--------|-------------|
| TASK_COMPLETION | backtest_coach | Coach task completion rate (%) |
| REPLAY_SCORE | replay_training | Average replay session score |
| MISTAKE_REDUCTION | replay_training | Reduction in replay mistakes (%) |
| BACKTEST_ISSUE | backtest_coach | Count of open backtest issues |
| JOURNAL_IMPROVEMENT | journal | Journal entry count trend |
| MEMORY_VALIDATION | strategy_memory | Strategy memory validation rate (%) |
| RULE_REVIEW | backtest_coach | Rule review tasks completed |
| DATA_FIX_PROGRESS | backtest_coach | Data fix tasks completed |
| TRAINING_STREAK | replay_training | Training sessions logged |
| QUALITY_SCORE | regression | Regression pass rate (%) |

---

## Trend Direction

Each metric is assigned a trend based on its change since the previous run:

- **IMPROVING** — metric moved in a positive direction (beyond threshold)
- **STABLE** — metric is approximately unchanged
- **WORSENING** — metric moved in a negative direction
- **UNKNOWN** — no previous data point available for comparison

---

## INSUFFICIENT_DATA

When a source module has not been run yet (no CSV files found), the metric
shows `INSUFFICIENT_DATA` with status `WARN`. This is always handled
gracefully — the system never crashes on missing data.

To populate data, run the relevant source module first:

```
python main.py backtest-coach --mode real
python main.py strategy-memory --mode real
python main.py regression-run --suite research_os --mode real
```

---

## CLI Commands

```
# Run full pipeline and generate metrics
python main.py training-metrics --mode real

# Show latest summary
python main.py training-metrics-summary

# Show metrics detail
python main.py training-metrics-detail

# Show trend analysis
python main.py training-metrics-trend

# Generate Markdown report
python main.py training-metrics-report --mode real
```

---

## GUI

The **Backtest Training Metrics** tab is available in the Research OS group
of the TW Quant Cockpit GUI dashboard. It shows:

- Summary cards: total, improving, stable, worsening, no-data, score, overall trend
- **Metrics** tab: full table of all metrics with trend and status
- **Trends** tab: summary of improving/worsening items and key metrics
- **Commands** tab: safe CLI commands for research use

---

## Data Storage

| File | Description |
|------|-------------|
| `data/backtest_results/training_metrics/training_metrics_YYYY-MM-DD.csv` | Daily metrics snapshot |
| `data/backtest_results/training_metrics/training_metrics_summary_YYYY-MM-DD.csv` | Daily summary |
| `data/backtest_results/training_metrics/training_metrics_history.csv` | Rolling history for trend computation |

---

## Safety

- All outputs are research only — no BUY/SELL/ORDER keywords ever appear
- Production Trading is permanently BLOCKED
- No automatic strategy activation based on any metric
- ACCEPTED memory status never enables trading

---

*TW Quant Cockpit v0.8.2 — Backtest Training Metrics — Research Only — Not Investment Advice*
