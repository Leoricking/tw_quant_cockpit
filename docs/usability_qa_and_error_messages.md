# Usability QA & Error Message Polish (v0.3.22)

> **[!] Research Only. Read Only. No Real Orders.**
> **[!] Production Trading: BLOCKED.**

## Overview

v0.3.22 adds structured, user-facing error messages and a usability smoke test suite
to ensure the CLI and GUI do not crash silently and provide actionable guidance to users.

---

## New Files

### `utils/status_labels.py`

Unified status label constants and normalization helpers.

**Constants:**
- Operational: `OK`, `PARTIAL`, `WARN`, `FAILED`, `BLOCKED`, `SKIPPED`, `MISSING`, `NOT_CONFIGURED`, `DISABLED`, `PLANNED`
- Safety: `READ_ONLY`, `NO_REAL_ORDERS`, `PRODUCTION_BLOCKED`, `RESEARCH_ONLY`
- Data quality: `OBSERVATIONAL`, `INSUFFICIENT`, `RELIABLE`
- Freshness: `FRESH`, `STALE`, `OLD`, `UNKNOWN`

**Functions:**
- `normalize_status(raw)` — maps variant spellings to canonical form
- `format_status(raw, width)` — returns `[OK]     ` padded label
- `is_success_status(raw)` — True for OK / RELIABLE / FRESH
- `is_warning_status(raw)` — True for PARTIAL / WARN / STALE etc.
- `is_failure_status(raw)` — True for FAILED / BLOCKED / MISSING etc.
- `status_sort_key(raw)` — integer sort key (lower = better)
- `safe_status_message(raw, fallback)` — returns fallback for UNKNOWN

---

### `utils/user_facing_errors.py`

Converts raw Python exceptions into structured, actionable error objects.

**`UserFacingError` fields:**
- `title` — short title (shown in bold/header)
- `plain_message` — 1-2 sentence plain-English explanation
- `technical_detail` — raw exception message
- `likely_cause` — most probable root cause
- `can_ignore` — True if system can continue without this data
- `next_steps` — list of actionable fix suggestions
- `severity` — INFO / WARNING / ERROR / FATAL
- `source` — originating module or step name

**`UserFacingErrorFormatter` handles:**
- `FileNotFoundError` — file not imported yet
- `PermissionError` — file locked or no access
- `UnicodeDecodeError` — wrong encoding (Big5 vs UTF-8)
- `pandas.ParserError` / `EmptyDataError` — malformed CSV
- Network timeout / connection error — retry later
- Token not configured — set `FINMIND_TOKEN` in `.env`
- Data missing / empty — import data first
- Stale data — run `update-data`
- Provider unsupported — use CSV fallback
- GUI import error — install PySide6
- `ImportError` — run `pip install -r requirements.txt`
- Generic fallback — check logs

---

### `utils/cli_output.py`

Windows cp950-safe CLI output formatter.

**`CLIOutput` methods:**
- `header(title, version)` — section header with safety notice
- `section(title)` — sub-section separator
- `key_value(key, value)` — aligned key: value pair
- `status_line(name, status, detail)` — `[STATUS]  name  detail`
- `warning(message)` — `[WARN] message`
- `error(message)` — `[ERROR] message`
- `table(headers, rows, col_widths)` — plain-text table
- `safety_banner()` — mandatory safety disclaimer
- `footer(extra)` — closing footer with safety reminder
- `user_facing_error(err)` — formatted `UserFacingError` display
- `flush()` — write all buffered lines to stdout

No emoji. Safe for Windows cp950 terminal.

---

### `qa/usability_smoke_test.py`

Runs CLI and GUI panel import smoke tests.

**CLI tests run:**
- `update-data --dry-run --mode mock`
- `run-research --profile quick --mode mock`
- `data-quality-gate --mode mock`
- `provider-health`
- `data-freshness`
- `auto-report --profile daily --mode mock`
- `signal-quality --mode mock`
- `simulate-portfolio --scenario balanced --mode mock`

**GUI import tests:**
- All major panel imports (dashboard, portfolio cockpit, signal quality, etc.)

**Outputs:**
- `data/backtest_results/usability_smoke_test_summary.csv`
- `reports/usability_smoke_test_report_YYYY-MM-DD.md` (via report builder)

---

### `reports/usability_qa_report.py`

7-section Markdown report builder:
1. 總覽 (Overview) — pass/fail/warn counts, overall status
2. CLI UX Test Results — per-command status table
3. GUI Panel Import Results — per-panel import status
4. Error Message Coverage — table of handled error types
5. Empty State Coverage — EmptyStateWidget documentation
6. 安全訊息覆蓋率 (Safety Message Coverage) — CLI commands with/without banner
7. 待改善項目 (Improvement Recommendations) — failures and gaps

---

### `gui/usability_qa_panel.py`

GUI panel for running smoke tests and viewing results.

Features:
- Safety banner
- Summary cards: Tests Passed / Failed / Warnings / Safety Banner Coverage
- Test results table (Test, Category, Status, Duration, Can Ignore, Note)
- Error message preview tab
- "Run Smoke Test" and "Generate Report" buttons
- QThread workers (non-blocking)

---

### `gui/usability_qa_adapter.py`

Adapter between `UsabilityQAPanel` and the smoke test / report builders.

Methods:
- `run_smoke_test()` — runs `UsabilitySmokeTest.run()`
- `generate_report(smoke_result)` — builds Markdown report
- `load_latest_report_path()` — finds newest `.md` report
- `load_latest_summary()` — reads `usability_smoke_test_summary.csv`

---

## Modified Files

### `workflow/daily_workflow.py`

`_run_step()` now attaches user-facing error metadata when a step fails:
- `step.extra["user_message"]` — plain-language explanation
- `step.extra["likely_cause"]` — probable cause
- `step.extra["can_ignore"]` — whether research can continue
- `step.extra["next_steps"]` — actionable fix suggestions
- `step.extra["technical_detail"]` — raw exception message

---

### `automation/task_runner.py`

`_make_result()` now includes:
- `safety_banner_present: True` — safety invariant always present
- `user_message: ""` — populated by callers when needed
- `can_ignore: False` — populated by callers when needed
- `next_steps: []` — populated by callers when needed

---

### `data/providers/auto_fetcher.py`

`_make_summary()` now includes `warning_details` — a list of structured dicts:
```json
{
  "message":    "raw warning string",
  "cause":      "API token not configured or ...",
  "next_step":  "Set FINMIND_TOKEN in .env",
  "can_ignore": true
}
```

---

### `quality/data_quality_gate.py`

`run()` now returns a `blockers` field — a list of structured blocker dicts:
```json
{
  "blocker_name":          "LOW_COVERAGE",
  "severity":              "ERROR",
  "reason":                "Data coverage score is 45.2 (threshold: 70)...",
  "next_step":             "Import more CSV data or run: python main.py provider-auto-fetch",
  "can_continue_research": true
}
```

Always includes `PRODUCTION_BLOCKED` blocker (FATAL, `can_continue_research: true`).

---

### `gui/portfolio_widgets.py`

- `StatusBadge` — now normalizes status using `utils.status_labels.normalize_status()`; expanded `_STATUS_COLORS` map covers all v0.3.22 status constants
- `DataFrameTableModel.data()` — guards against empty DataFrame; returns `"-"` for missing columns
- `DataFrameTableModel.headerData()` — guards against empty column list
- `EmptyStateWidget` — new parameters: `title`, `next_steps`; shows list of actionable steps below message

---

### `gui/dashboard.py`

Added Usability QA tab (v0.3.22):
```python
try:
    from gui.usability_qa_panel import UsabilityQAPanel
    _USABILITY_QA_AVAILABLE = True
except Exception as _uqa_exc:
    _USABILITY_QA_AVAILABLE = False
```

---

## CLI Usage

```bash
# Run smoke tests
python main.py usability-smoke-test

# Run smoke tests and generate a report
python main.py usability-smoke-test --report

# Generate QA report from latest smoke test CSV
python main.py usability-qa-report
```

---

## Safety Invariants

All new code carries:
- `read_only = True`
- `no_real_orders = True`
- `production_blocked = True`
- `real_order_ready = False` (never)
