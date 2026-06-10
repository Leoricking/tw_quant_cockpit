# Strategy Lab Dashboard v0.9.3

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] VALIDATED = Research Validated Only. Does NOT enable trading.**
> **[!] Not Investment Advice.**

---

## v0.9.3 目標

v0.9.3 introduces the **Strategy Lab Dashboard** — a unified single-view dashboard that
summarizes validation grades, evidence graph health, crash reversal risks, training metrics,
coach tasks, strategy memories, and research intelligence into one place.

No BUY/SELL/ORDER. No trading actions. Production Trading: BLOCKED.
`read_only=True`, `no_real_orders=True`, `production_blocked=True`, `real_order_ready=False`.

---

## Dashboard Cards

| Card | Description |
|------|-------------|
| Strategy Lab Status | Total strategies, VALIDATED/VALIDATING counts |
| Validation Grade Mix | OBS/INSUF/CONF/REJ grade breakdown |
| Evidence Health | Evidence thread count, orphan count |
| Crash Reversal Risk | High/extreme risk crash reversal warnings |
| Needs Backtest | Count of strategies needing more backtest |
| Needs Replay | Count of strategies needing practice replay |
| Needs Data | Count of strategies with data gaps |
| Training Progress | Total metrics, IMPROVING vs WORSENING |
| Active Strategy Memories | Active/validating/accepted memory count |
| Coach Tasks | Backtest coach task count |
| Report Pack Health | Report pack availability |
| No Real Orders Safety | Safety declaration card |

---

## Validation Board

Shows each strategy's validation grade, score, and suggested next step.

Grades: `VALIDATED` / `VALIDATING` / `OBSERVATIONAL` / `INSUFFICIENT` / `CONFLICTED` / `REJECTED`

**VALIDATED = Research Validated Only — does NOT enable or imply real trading.**

---

## Evidence Board

Shows evidence graph threads and orphan nodes. Orphans indicate missing data or
not-yet-run modules.

---

## Crash Reversal Board

Shows crash reversal rule risk levels. HIGH/EXTREME risk rules are flagged for review.

No BUY/SELL/ORDER. Research classification only.

---

## Action Board

Shows recommended research actions. All action types are research-only:

| Action Type | Description |
|-------------|-------------|
| `REVIEW` | Review strategy or evidence |
| `BACKTEST_MORE` | Run more backtests for this strategy |
| `PRACTICE_REPLAY` | Practice replay for this strategy |
| `REVIEW_JOURNAL` | Review journal for this strategy |
| `FIX_DATA` | Fix data gaps |
| `READ_REPORT` | Read generated report |
| `WAIT` | Observe and wait |
| `REVIEW_RISK` | Review risk parameters |
| `REVIEW_EARNINGS` | Review earnings data |
| `REVIEW_CHIPS` | Review chip/ownership data |
| `BUILD_WATCHLIST` | Build a research watchlist |
| `DO_NOT_CHASE` | Do not chase a rejected strategy |
| `KEEP_OBSERVING` | Continue observing an observational strategy |

No BUY/SELL/ORDER action types are allowed.

---

## Module Health

Tracks availability and status of all Strategy Lab modules:

- strategy_validation
- evidence_graph
- crash_reversal
- training_metrics
- backtest_coach
- strategy_memory
- research_intelligence
- data_coverage

---

## CLI Usage

```bash
# Run full dashboard refresh
python main.py strategy-lab-dashboard --mode real

# Show summary from store
python main.py strategy-lab-dashboard-summary

# List dashboard cards
python main.py strategy-lab-dashboard-cards

# List action items
python main.py strategy-lab-dashboard-actions

# Top priority actions
python main.py strategy-lab-dashboard-priorities

# Strategies needing backtest
python main.py strategy-lab-dashboard-needs-backtest

# Strategies needing replay
python main.py strategy-lab-dashboard-needs-replay

# Strategies needing data
python main.py strategy-lab-dashboard-needs-data

# Generate Markdown report
python main.py strategy-lab-dashboard-report --mode real
```

---

## GUI Usage

The **Strategy Lab Dashboard** tab appears in the TW Quant Cockpit GUI.

- Safety banner at top (Research Only / No Real Orders)
- Summary cards grid at top
- Filter bar (filter by name/grade/status)
- Tabs: Overview, Validation Board, Evidence Board, Crash Reversal Board, Action Board, Module Health
- Action buttons: Run Refresh, Generate Report, Open Validation, Open Evidence Graph, Open Crash Reversal, Copy Summary

---

## No Real Orders

- `no_real_orders=True` on all dataclasses and engine classes
- `production_blocked=True` on all dataclasses and engine classes
- `_guard()` rejects BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE/REAL_TRADE in any field
- No broker connection, no auto-trading, no order submission

---

## VALIDATED does not enable trading

**VALIDATED grade = Research Validated Only.**

A strategy with `VALIDATED` grade has accumulated sufficient research evidence to be
considered research-validated. This does **NOT** mean it is safe to trade, does **NOT**
mean it generates profit, and does **NOT** enable or authorize real trading of any kind.

All outputs are for research, simulation, and decision support only.

---

_Strategy Lab Dashboard v0.9.3 — TW Quant Cockpit_
