# TW Quant Cockpit — User Guide (v0.3.23)

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not investment advice. REAL_ORDER_READY=False.**

---

## 1. 專案定位 (Project Purpose)

TW Quant Cockpit is a Taiwan stock quantitative research and monitoring platform.

| Purpose | Details |
|---------|---------|
| **台股量化研究** | Research and backtest Taiwan stock strategies using historical CSV data |
| **Research Only** | All operations are read-only. No orders are ever placed |
| **Read Only** | Data files are read, never modified by the research pipeline |
| **No Real Orders** | No connection to Shioaji, Mega, or any live broker |
| **Production Trading BLOCKED** | `PRODUCTION_BLOCKED=True` and `REAL_ORDER_READY=False` are hard-coded invariants |

**This system is for learning, research, and decision support. It does not constitute investment advice.**

---

## 2. 每日使用流程 (Daily Usage)

### Core Three Commands

```bash
# Step 1: Update all data sources
python main.py update-data --mode real

# Step 2: Run research analysis
python main.py run-research --mode real --profile standard

# Step 3: Open GUI cockpit to review results
python main.py open-cockpit --mode real
```

### Or One Command

```bash
python main.py daily-workflow --mode real --profile standard
```

### Dry-Run (No file writes)

```bash
python main.py update-data --mode real --dry-run
```

---

## 3. 推薦日常 SOP (Recommended Daily SOP)

### 收盤後標準流程 (Standard After-Market Flow)

```
16:30 收盤後
  │
  ├─ python main.py update-data --mode real
  │    更新 daily price / institutional / margin / revenue
  │
  ├─ python main.py run-research --mode real --profile standard
  │    計算 signal quality / portfolio simulation / auto report
  │
  └─ python main.py open-cockpit --mode real
       GUI 審閱報告與分數
```

### 快速檢查流程 (Quick Check)

```bash
python main.py run-research --mode real --profile quick
# Runs: data_quality_gate + auto_report only (~30s)
```

### 週末完整研究流程 (Weekend Full Research)

```bash
python main.py daily-workflow --mode real --profile full
# Runs all steps including long-term backtest
```

---

## 4. GUI 使用方式 (GUI Usage)

Start the cockpit:

```bash
python main.py cockpit --mode real
# or
python main.py open-cockpit --mode real
```

### Available Tabs

| Tab | Purpose |
|-----|---------|
| **Daily Workflow** | Run update-data / run-research from GUI; view step results |
| **Data Quality Gate** | View production readiness scores, gate decisions, blockers |
| **Data Provider Fetch** | Manually trigger provider auto-fetch per dataset |
| **Provider Health** | Check API provider token status and capability |
| **Automation Scheduler** | View and trigger scheduled tasks |
| **Auto Report Center** | Browse and regenerate daily reports |
| **Usability QA** | Run smoke tests, view error message coverage |
| **Rule Weight Tuning** | Compare 7 weight configurations; view best config |
| **Signal Quality** | View BOOST/KEEP/REDUCE/DISABLE signal recommendations |
| **Portfolio Cockpit** | Simulation results: Sharpe, MaxDD, Profit Factor |

See [GUI Guide](gui_guide.md) for detailed tab descriptions.

---

## 5. 報告怎麼看 (How to Read Reports)

### Auto Report

Reports are generated in `reports/auto_report_center/YYYY-MM-DD/`.

| Report | Location | Content |
|--------|----------|---------|
| Daily summary | `daily_summary_YYYY-MM-DD.md` | Market overview, top candidates |
| Signal quality | `signal_quality_report_YYYY-MM-DD.md` | BOOST/KEEP/REDUCE per rule |
| Portfolio simulation | `portfolio_simulation_report_YYYY-MM-DD.md` | Sharpe, MaxDD, return |
| Data quality gate | `data_quality_gate_report_YYYY-MM-DD.md` | Readiness scores and blockers |
| Workflow summary | `reports/daily_workflow/YYYY-MM-DD/workflow_summary.md` | Step status and durations |

### Data Quality Gate Report

Sections:
1. Composite scores (Production Readiness, Backtest Readiness)
2. Sub-scores (freshness, coverage, source confidence, etc.)
3. Gate decisions (RESEARCH_ONLY, BACKTEST_READY, etc.)
4. Mock contamination check
5. Blockers and next actions

---

## 6. 分數怎麼看 (How to Read Scores)

### Production Readiness Score

| Score | Classification | Meaning |
|-------|---------------|---------|
| 90–100 | STRONG | All data sources fresh and complete |
| 75–89 | READY_FOR_RESEARCH | Good for research |
| 60–74 | PARTIAL | Some data missing or stale |
| 40–59 | WEAK | Significant gaps |
| 0–39 | BLOCKED | Insufficient data |

### Backtest Readiness Score

Capped at 60 if mock contamination < 90.
Capped at 70 if coverage < 70.

### Signal Quality BOOST / KEEP / REDUCE

| Label | Meaning | Action |
|-------|---------|--------|
| BOOST | Rule contributes positively to returns | Consider increasing weight |
| KEEP | Rule neutral | No change needed |
| REDUCE | Rule underperforms | Consider reducing weight |
| DISABLE | Rule consistently negative | Consider disabling |

**Note: Signal Quality recommendations are for research review only. Do NOT auto-apply.**

### Portfolio KPI Targets

| KPI | Target | Meaning |
|-----|--------|---------|
| Sharpe Ratio | > 1.5 | Risk-adjusted return |
| Max Drawdown | < 20% | Worst peak-to-trough |
| Profit Factor | > 1.5 | Gross profit / gross loss |

### Rule Weight Best Config

The best config from `tune-rule-weights` is a suggestion only. It must be reviewed manually before any weight adjustment.

---

## 7. 安全限制 (Safety Constraints)

| Constraint | Status |
|------------|--------|
| Real order execution | **BLOCKED** |
| Auto trading | **BLOCKED** |
| Auto weight modification | **BLOCKED** |
| Shioaji connection | **Not implemented** |
| Mega connection | **Not implemented** |
| Investment advice | **Not provided** |

See [Safety & Limitations](safety_and_limitations.md) for full details.

---

## 8. 常見問題快速索引 (Quick Troubleshooting)

| Problem | See |
|---------|-----|
| FINMIND_TOKEN not configured | [Troubleshooting §1](troubleshooting.md) |
| Data freshness STALE | [Troubleshooting §2](troubleshooting.md) |
| Production Readiness BLOCKED | [Troubleshooting §4](troubleshooting.md) |
| UnicodeDecodeError | [Troubleshooting §5](troubleshooting.md) |
| GUI empty state | [Troubleshooting §8](troubleshooting.md) |

---

*TW Quant Cockpit v0.3.23 — Research Only — Not Investment Advice*
