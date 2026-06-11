# GUI Stability & Usability Polish — v1.0.3

> Research Only | No Real Orders | Production Trading BLOCKED | Broker Execution Disabled | VALIDATED does not enable trading

## 一、v1.0.3 目標 (Goals)

v1.0.3 adds shared GUI stability and usability helpers to the TW Quant Cockpit without changing any strategy logic, trading rules, or safety constraints.

Goals:
- Prevent `QThread destroyed while running` warnings with safe thread lifecycle helpers
- Improve table readability (column width capping, ellipsis, tooltips, empty state)
- Add friendly empty state messages instead of blank panels
- Ensure copy actions never include forbidden trading text
- Add GUI health check CLI and usability report
- Preserve all v1.0.0 guarantees: no real orders, no broker execution, no auto trading

## 二、GUI Stability — QThread Cleanup

File: `gui/common/gui_threading.py`

Key components:
- `SafeWorkerResult` — typed result dataclass (success, data, error, warning)
- `SafeWorker` — QObject-based worker, prevents QThread destroyed warnings
- `run_in_qthread(parent, fn, on_finished, ...)` — safe thread launcher, returns (thread, worker) for caller to retain
- `cleanup_thread(thread, timeout_ms=2000)` — call from `closeEvent` to stop threads gracefully

Usage pattern:
```python
from gui.common.gui_threading import run_in_qthread, cleanup_thread

# In panel __init__:
self._thread = None

# Launch background work:
self._thread, self._worker = run_in_qthread(
    self, my_fn, self._on_finished, arg1, arg2
)

# In closeEvent:
cleanup_thread(self._thread)
```

## 三、Table Usability

File: `gui/common/table_utils.py`

Functions:
- `set_table_defaults(table)` — alternating rows, row selection, no edit, no word wrap
- `autosize_table_columns(table, max_width=360)` — auto-resize with max column cap
- `apply_ellipsis_delegate(table)` — ellipsis for long text, tooltip on hover
- `set_tooltip_from_cell(table)` — set tooltip on all cells
- `safe_set_rows(table, rows)` — populate rows, shows "No data yet" if empty
- `format_bool(value, use_checkmark=False)` — True/False or ✓/—
- `format_score(value)` — 1 decimal place
- `format_status(value)` — normalized status string

## 四、Empty State

File: `gui/common/empty_state.py`

Predefined empty states:
- `EMPTY_NO_DATA` — "No Data Yet"
- `EMPTY_INSUFFICIENT` — "Insufficient Evidence"
- `EMPTY_RUN_SCAN_FIRST` — "No Scan Results"
- `EMPTY_RUN_REPORT_FIRST` — "No Report Found"

`build_empty_state(title, description, next_step)` returns a dict with research_note.

## 五、Copy Safety

File: `gui/common/copy_utils.py`

Functions:
- `copy_safe_text(text)` — copies to clipboard if no forbidden trading action detected
- `copy_safe_command(command)` — copies only recognized research CLI commands
- `build_safe_next_step_copy(next_step, command, label)` — build copy-safe next step descriptor

Forbidden actions blocked: BUY, SELL, ORDER, EXECUTE, SUBMIT_ORDER, AUTO_TRADE, REAL_TRADE, LIVE_TRADE, BROKER_ORDER

Whitelist (not blocked): "No Real Orders", "Broker Execution Disabled", "No broker execution", etc.

## 六、Safety Banner

File: `gui/common/gui_safety.py`

- `SAFE_BANNER_TEXT` — standard research-only banner
- `build_research_only_banner()` — returns banner string
- `build_no_real_orders_label()` — short label
- `assert_no_forbidden_gui_text(text)` — raises if forbidden text found (after whitelist removal)
- `sanitize_gui_text(text)` — replaces forbidden words with `[RESEARCH_ONLY]`
- `SAFE_NEXT_STEPS` — list of approved next-step labels (REVIEW, BACKTEST_MORE, WAIT, etc.)

## 七、GUI Health Check

File: `gui/gui_health_check.py`
CLI: `python main.py gui-health-check`

Checks:
- Panel imports (strategy lab, validation, evidence graph, crash reversal, etc.)
- Adapter imports
- Navigation tab registry
- Safety banners (all 4 strings present)
- Forbidden GUI text scan
- QThread helpers
- Table utils
- Copy utils

## 八、GUI Usability Report

File: `reports/gui_usability_report.py`
CLI: `python main.py gui-usability-report --mode real`

Generates a Markdown report covering:
- Overview (version, safety flags)
- Panel health
- Navigation health
- QThread safety
- Table usability
- Copy safety
- Known warnings
- Safety declaration

## 九、No Real Orders

- No Real Orders — This system does not and cannot place real trading actions.
- No broker execution — There is no connection to any broker API.
- No auto trading — No automatic trading, no automatic rule weight changes.
- GUI does not enable trading — GUI panels are research-only displays.
- VALIDATED does not enable trading — VALIDATED grade is research-only.
- Not Investment Advice — Nothing in this system constitutes investment advice.

---
*TW Quant Cockpit v1.0.3 — GUI Stability & Usability Polish — Research Only — Not Investment Advice*
