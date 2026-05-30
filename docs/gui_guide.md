# TW Quant Cockpit — GUI Guide (v0.3.23)

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**

---

## Starting the Cockpit

```bash
python main.py cockpit --mode real
# or
python main.py open-cockpit --mode real
```

**Requirement:** PySide6 (`pip install PySide6`)

If PySide6 is not installed, all GUI tabs are skipped gracefully. CLI commands remain available.

---

## Tab Overview

| Tab | Purpose | Data Source |
|-----|---------|-------------|
| **Daily Workflow** | Run pipeline steps; view step results | workflow engine |
| **Data Quality Gate** | Readiness scores, gate decisions, blockers | data quality gate |
| **Data Provider Fetch** | Manually trigger provider fetches | auto fetcher |
| **Provider Health** | Token status, capability check | provider registry |
| **Automation Scheduler** | View and trigger scheduled tasks | task runner |
| **Auto Report Center** | Browse and regenerate daily reports | report builder |
| **Usability QA** | Run smoke tests, view error coverage | usability smoke test |
| **Rule Weight Tuning** | Compare 7 configs; view best config | weight tuner |
| **Signal Quality** | BOOST/KEEP/REDUCE per rule | signal evaluator |
| **Portfolio Cockpit** | Sharpe, MaxDD, Profit Factor | portfolio simulator |

---

## Tab Descriptions

### Daily Workflow Tab

**Purpose:** Run the full daily pipeline (update-data → run-research → reports) from the GUI.

**Controls:**
- **Run Daily Workflow** button — triggers `daily-workflow --mode real --profile standard`
- Profile selector — quick / standard / full
- Step result table — shows each step name, status (OK/FAILED/SKIPPED), duration, and any warnings

**Step result columns:** Step | Status | Duration | User Message | Can Ignore

**Empty state:** "No workflow has been run yet. Click 'Run Daily Workflow' to start."

**Warnings displayed:**
- Steps with `can_ignore=True` shown in yellow
- Steps with `can_ignore=False` shown in red
- Safety banner always visible at top

---

### Data Quality Gate Tab

**Purpose:** View production readiness and backtest readiness scores, gate decisions, and blockers.

**Sections:**
1. **Composite Scores** — Production Readiness (0–100), Backtest Readiness (0–100)
2. **Sub-scores** — freshness, coverage, source confidence, institutional completeness
3. **Gate Decision** — STRONG / READY_FOR_RESEARCH / PARTIAL / WEAK / BLOCKED
4. **Mock Contamination** — percentage of real vs. mock data
5. **Blockers** — list with severity (FATAL/HIGH/MEDIUM), can_continue_research flag, next_step

**Score color coding:**
- 90–100: green (STRONG)
- 75–89: blue (READY_FOR_RESEARCH)
- 60–74: yellow (PARTIAL)
- 40–59: orange (WEAK)
- 0–39: red (BLOCKED)

**Blocker table columns:** Blocker | Severity | Reason | Next Step | Can Continue Research

**Note:** PRODUCTION_BLOCKED is always listed (FATAL severity, can_continue_research=True). This is expected and does not prevent research use.

**Empty state:** "Data quality gate has not been run. Run 'data-quality-gate' or trigger from Daily Workflow tab."

---

### Data Provider Fetch Tab

**Purpose:** Manually trigger auto-fetch for individual data providers and datasets.

**Controls:**
- Provider selector (finmind, fugle, twse_public)
- Dataset selector (daily_price, institutional, margin, monthly_revenue)
- **Fetch** button
- Result log showing rows fetched, warnings, timing

**Warning display:** Structured warning details from auto_fetcher — message, cause, next_step, can_ignore.

**Empty state:** "Select a provider and dataset, then click Fetch."

---

### Provider Health Tab

**Purpose:** View token/API status for all configured data providers.

**Columns:** Provider | Token Status | Capability | Last Fetch | Notes

**Token statuses:**
- `CONFIGURED` — token set in `.env`
- `NOT_CONFIGURED` — no token; provider falls back to cached data or public API
- `INVALID` — token set but authentication failed

**Empty state:** "Provider health check not yet run."

---

### Automation Scheduler Tab

**Purpose:** View scheduled tasks and trigger them manually.

**Columns:** Task | Schedule | Last Run | Next Run | Status | Duration

**Controls:**
- **Trigger Now** button per task
- **Refresh** to reload schedule

**Empty state:** "No scheduled tasks configured. See automation scheduler docs."

---

### Auto Report Center Tab

**Purpose:** Browse generated daily reports and regenerate on demand.

**Left panel:** Date selector — lists available report dates.

**Right panel:** Report viewer — renders selected Markdown report.

**Reports available:** daily_summary, signal_quality, portfolio_simulation, data_quality_gate, usability_qa, workflow_summary

**Controls:**
- **Regenerate** button — re-runs report builder for selected date
- **Open Folder** button — opens report directory in file explorer

**Empty state:** "No reports found. Run 'auto-report' or trigger from Daily Workflow tab."

---

### Usability QA Tab

**Purpose:** Run smoke tests and view error message coverage.

**Controls:**
- **Run Smoke Test** button
- **Generate Report** button
- Test Results tab (table)
- Error Message Preview tab (text)

**Test result columns:** Test | Category | Status | Duration | Can Ignore | Note

**Status values:** PASS / WARN / FAIL / SKIP

**Summary cards:** Total | Passed | Warnings | Failed

**Empty state:** "No smoke test results. Click 'Run Smoke Test'."

**Notes:**
- GUI tests show SKIP (not FAIL) when PySide6 is unavailable
- Token NOT_CONFIGURED results show WARN (can_ignore=True)

---

### Rule Weight Tuning Tab

**Purpose:** Compare 7 rule weight configurations and see which performs best.

**Columns:** Config | Sharpe | MaxDD | Profit Factor | Win Rate | Score

**Best config:** Highlighted row + recommendation text.

**Warning:** "Best config is a suggestion only. Do NOT apply without manual review."

**Safety:** No auto-apply. Weight changes require manual intervention.

**Empty state:** "Run 'tune-rule-weights' to generate weight comparison data."

---

### Signal Quality Tab

**Purpose:** View BOOST / KEEP / REDUCE / DISABLE recommendations per rule.

**Columns:** Rule | Signal | Recommendation | Confidence | Last Updated

**Color coding:**
- BOOST: green
- KEEP: blue/neutral
- REDUCE: yellow
- DISABLE: red

**Warning:** "Signal Quality recommendations are for research review only. Do NOT auto-apply."

**Empty state:** "Run 'signal-quality' to populate this tab."

---

### Portfolio Cockpit Tab

**Purpose:** View portfolio simulation results — Sharpe, MaxDD, Profit Factor, equity curve.

**Sections:**
1. **KPI Summary** — Sharpe, MaxDD, Profit Factor vs. targets
2. **Equity Curve** — chart of cumulative returns
3. **Drawdown Chart** — rolling drawdown
4. **Trade Log** — individual trade entries (entry/exit/P&L)

**KPI target colors:**
- Above target: green
- Below target: red

**Empty state:** "Run 'portfolio-simulation' to populate portfolio results."

---

## Safety Banner

The safety banner appears at the top of every tab:

```
[!] Read Only | No Real Orders | Production Trading: BLOCKED | REAL_ORDER_READY=False
```

This banner cannot be dismissed and is present in all tab views.

---

## Empty State Behavior

All tabs handle empty/missing data gracefully:
- Descriptive title explaining what data is missing
- Next steps explaining how to populate the tab
- No crashes, no blank screens, no unhandled exceptions

---

## GUI Not Available

If PySide6 is not installed:

```
GUI not available: PySide6 not installed.
Install with: pip install PySide6
CLI commands remain fully available.
```

All CLI commands work without PySide6.

---

*TW Quant Cockpit v0.3.23 — Research Only — Not Investment Advice*
