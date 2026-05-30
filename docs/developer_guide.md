# TW Quant Cockpit — Developer Guide (v0.3.23)

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**

---

## Architecture Overview

```
trading_master/
├── main.py                    # CLI entry point; all subcommands
├── workflow/
│   └── daily_workflow.py      # DailyResearchWorkflow; step runner
├── data/
│   ├── providers/
│   │   ├── auto_fetcher.py    # AutoFetcher; provider fetch coordination
│   │   └── provider_registry.py
│   └── ...                    # CSV data files (read-only by research)
├── quality/
│   └── data_quality_gate.py   # DataQualityGate; readiness scoring
├── automation/
│   └── task_runner.py         # TaskRunner; scheduled task execution
├── reports/
│   ├── auto_report_center.py  # AutoReportCenter; report orchestration
│   ├── signal_quality_report.py
│   ├── portfolio_simulation_report.py
│   └── usability_qa_report.py
├── qa/
│   └── usability_smoke_test.py  # UsabilitySmokeTest; CLI+GUI smoke tests
├── utils/
│   ├── status_labels.py       # Status constants + normalization helpers
│   ├── user_facing_errors.py  # UserFacingError + formatter
│   └── cli_output.py          # CLIOutput; Windows cp950-safe formatter
├── gui/
│   ├── dashboard.py           # Main window; tab orchestration
│   ├── usability_qa_panel.py  # Usability QA tab
│   ├── usability_qa_adapter.py
│   └── portfolio_widgets.py   # Shared widgets (StatusBadge, DataFrameTableModel, EmptyStateWidget)
└── docs/                      # Documentation (this directory)
```

---

## Adding a New CLI Command

### 1. Write the command function in `main.py`

```python
def cmd_my_new_command(args):
    out = CLIOutput()
    out.safety_banner()
    out.header("My New Command")
    # ... implementation ...
    out.footer("my-new-command")
```

### 2. Add argparse subparser

```python
p_new = subparsers.add_parser("my-new-command", help="Description")
p_new.add_argument("--mode", choices=["real", "mock"], default="real")
```

### 3. Register in command_map

```python
command_map = {
    ...
    "my-new-command": cmd_my_new_command,
}
```

### Rules

- Always call `out.safety_banner()` first
- Always call `out.footer(command_name)` last
- Use `CLIOutput` methods for all output (no direct `print()`)
- Never write to data files from a research command
- Handle exceptions with `UserFacingErrorFormatter.from_exception(exc)`

---

## Adding a New GUI Tab

### 1. Create panel file: `gui/my_new_panel.py`

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from gui.portfolio_widgets import EmptyStateWidget

class MyNewPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        # Safety reminder at top
        banner = QLabel("[!] Read Only | No Real Orders | Production Trading: BLOCKED")
        layout.addWidget(banner)
        # Empty state until data is loaded
        self._empty = EmptyStateWidget(
            title="No Data Available",
            message="Run 'my-command' to populate this tab.",
            next_steps=["python main.py my-command --mode real"],
        )
        layout.addWidget(self._empty)
```

### 2. Register in `gui/dashboard.py`

```python
try:
    from gui.my_new_panel import MyNewPanel
    _MY_NEW_AVAILABLE = True
except Exception:
    _MY_NEW_AVAILABLE = False

# In _build_ui():
if _MY_NEW_AVAILABLE:
    self._my_new_panel = MyNewPanel()
    mid_tabs.addTab(self._my_new_panel, "My New Tab")
```

### Rules

- All GUI tab imports must be guarded with try/except
- Every tab must display the safety banner
- Every tab must have an `EmptyStateWidget` for empty data state
- Never place orders, modify data, or auto-apply weights from GUI
- Use `StatusBadge` and `DataFrameTableModel` from `portfolio_widgets.py`

---

## Adding a New Report

### 1. Create report file: `reports/my_new_report.py`

```python
class MyNewReportBuilder:
    def render(self, data: dict) -> str:
        lines = []
        lines.append("# My New Report")
        lines.append("")
        lines.append("> Research Only. Not Investment Advice.")
        # ... sections ...
        return "\n".join(lines)
```

### 2. Register in `reports/auto_report_center.py`

Add the report to the daily report generation pipeline.

### Rules

- All reports include the research-only disclaimer header
- Reports are Markdown (`.md`)
- Reports are written to `reports/auto_report_center/YYYY-MM-DD/`
- Report builders are pure functions (no side effects beyond writing the file)

---

## Status Labels

Use constants and helpers from `utils/status_labels.py`:

```python
from utils.status_labels import OK, PARTIAL, WARN, FAILED, BLOCKED, normalize_status, is_success_status

status = normalize_status("pass")   # → "OK"
is_success_status("OK")             # → True
is_failure_status("FAILED")         # → True
```

**Do not use raw string literals** for status values in new code. Always use the constants.

---

## User-Facing Errors

When a step or command fails, use `UserFacingErrorFormatter`:

```python
from utils.user_facing_errors import UserFacingErrorFormatter

try:
    # ... operation ...
except Exception as exc:
    err = UserFacingErrorFormatter.from_exception(exc, source="my_command")
    print(f"Error: {err.plain_message}")
    print(f"Cause: {err.likely_cause}")
    if err.next_steps:
        print("Next steps:")
        for step in err.next_steps:
            print(f"  - {step}")
```

---

## Git Conventions

### Branch strategy

- `main` — stable releases only
- All feature work committed directly to `main` after validation (small codebase)

### Commit message format

```
<type>: <short description>

<body>

Co-Authored-By: <name> <email>
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

### Tagging

Each version is tagged:

```bash
git tag -a v0.3.XX -m "v0.3.XX: <description>"
git push origin v0.3.XX
```

### Never commit

- `.env` files (tokens)
- `data/` CSV files (data files are local only)
- `reports/` output files
- `logs/` files

---

## Data Files Convention

- All data files live in `data/` subdirectories
- Data files are CSV format
- Column names follow XQ export conventions (see [xq_csv_mapping_guide.md](xq_csv_mapping_guide.md))
- Research pipeline reads data files; never modifies them
- `update-data` adds new files or appends new rows; never overwrites existing rows

---

## Testing

Run the usability smoke test after significant changes:

```bash
python main.py usability-smoke-test --report
```

This validates:
- 8 CLI commands run without error
- 8 GUI panels import without error
- Safety banner present in all CLI output
- Error messages are user-friendly

---

## Windows Encoding

The system runs on Windows with cp950 terminal encoding. All CLI output uses `CLIOutput` which handles encoding safely:

- No emoji in CLI output
- `flush()` uses `encode("ascii", errors="replace")` fallback
- All string operations guard against `UnicodeEncodeError`

Do not add emoji to any CLI output. Do not assume UTF-8 in Windows terminal output paths.

---

*TW Quant Cockpit v0.3.23 — Research Only — Not Investment Advice*
