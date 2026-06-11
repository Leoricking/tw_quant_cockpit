# TW Quant Cockpit GUI User Guide v1.0

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Launch the GUI

```
python main.py cockpit
```

The main window opens with a tab bar at the top.

---

## Safety Banner

Every tab displays a safety banner at the top:

```
Research Only | No Real Orders | Production Trading BLOCKED
Broker Execution Disabled | VALIDATED does not enable trading
```

This banner is always present. It cannot be disabled.

---

## Main Dashboard Tabs

### Strategy Lab Dashboard
- Unified single-view dashboard
- Shows validation grade distribution, evidence health, crash reversal warnings
- Action board: needs-backtest, needs-replay, needs-data lists
- Module health summary
- Research Only. No Real Orders.

### Strategy Validation Score
- Per-strategy confidence scores: INSUFFICIENT / OBSERVATIONAL / VALIDATING / VALIDATED / CONFLICTED / REJECTED
- Validation components table
- VALIDATED = Research Only — does NOT enable trading

### Evidence Graph
- Node types, edge relations, evidence threads
- Gap view: orphan nodes, missing data links, contradictions
- Conservative contradiction detection — never auto-modifies status

### Crash Reversal
- Crash cause classification
- Post-crash stabilization checklist
- Relative strength, EPS-backed dip filter, MA discipline
- Research Only

### Data Report Hygiene
- Runtime output inventory
- Stale data detection
- Gitignore coverage
- Review Only — no file deletion

### Strategy Memory
- Memory types and status lifecycle
- Validation queue, active threads, repeated patterns
- ACCEPTED = research only, never enables trading

### Backtest Coach
- Coach tasks from backtests and replay mistakes
- Task types: PRACTICE_REPLAY, REVIEW_RULE, BACKTEST_MORE, READ_REPORT, WAIT
- No real-trading tasks

### Training Metrics
- Training effectiveness tracking
- IMPROVING / STABLE / WORSENING trends
- INSUFFICIENT_DATA shown gracefully

### Research Intelligence
- P0/P1/P2/P3 priority board
- Daily/weekly research plan
- Signal aggregation from all modules

### Report Pack
- Daily / Weekly / Full report generation
- Reports saved as Markdown in reports/
- Not committed to git

---

## Empty State Behavior

When no data has been generated yet, the GUI shows an empty state message:

```
No data available — run the corresponding CLI command first.
Example: python main.py strategy-lab-dashboard --mode real
```

Empty state is normal for first-time use. Run the CLI commands to generate data.

---

## Copy Safe Command

Each panel has a "Copy Command" button that copies the corresponding CLI command to the clipboard. This makes it easy to run commands without typing them manually.

---

## QThread / Running State

Long-running operations (e.g., building a dashboard, running a report) use QThread to keep the GUI responsive. A spinning indicator shows while the operation is running.

Do not close the window while an operation is running.

---

## Common GUI Issues

| Issue | Cause | Resolution |
|-------|-------|-----------|
| Tab shows "No data" | CLI command not yet run | Run the corresponding CLI command |
| GUI freezes | Long-running operation | Wait for QThread to complete |
| Import error on startup | Missing dependency | Check Python environment |
| cp950 encoding warning | Windows terminal encoding | Non-critical, can ignore |
| Safety banner missing | GUI safety not loaded | Check gui/common/gui_safety.py |

---

## GUI Health Check

Run the GUI health check from CLI:

```
python main.py gui-health-check
```

This checks:
- All panels importable
- All adapters importable
- GUI navigation available
- Safety banner present
- Common utilities available

---

*TW Quant Cockpit v1.0.5 — Documentation & User Guide Polish — Research Only — Not Investment Advice*
