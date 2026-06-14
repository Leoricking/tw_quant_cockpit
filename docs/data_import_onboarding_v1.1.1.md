# Data Import UX & Batch Onboarding v1.1.1

> [!] Research Only. No Real Orders. Production Trading: BLOCKED.
> [!] dry_run=True by default. No write without explicit allow_write=True.
> [!] REPLACE_EXPLICIT disabled by default. Conflicts → manual review (not auto-overwrite).
> [!] Not Investment Advice.

## v1.1.1 目標

v1.1.1 adds a complete **Data Import UX & Batch Onboarding** system on top of the existing
XQ importer and batch importer infrastructure. Key goals:

- Discover importable files (XQ Excel, XQ CSV, standard CSV) automatically
- Map column headers to standard schema (Chinese + English)
- Detect duplicates and conflicts before any write occurs
- Build safe import plans (MERGE_SAFE / APPEND_SAFE by default)
- Execute in dry-run mode by default
- Route conflicts to REVIEW (never auto-overwrite)
- Build retry manifests for failed imports
- Refresh universe coverage after successful import
- Provide full CLI and GUI integration

---

## Import Modes

| Mode | Safe? | Description |
|------|-------|-------------|
| `MERGE_SAFE` | Yes | Add new rows only; skip exact duplicates; keep existing values on conflict |
| `APPEND_SAFE` | Yes | Append only; skip all duplicates (strict) |
| `REPLACE_EXPLICIT` | **NO** | Replace all existing data; **BLOCKED by default** |
| `DRY_RUN` | Yes | No writes at all; simulation only |

**Default**: `MERGE_SAFE` with `dry_run=True`.

---

## Supported File Types

| Type | Detection | Description |
|------|-----------|-------------|
| `XQ_EXCEL` | Chinese column headers in .xlsx/.xls | XQ technical analysis export (Excel) |
| `XQ_CSV` | Chinese column headers in .csv | XQ technical analysis export (CSV) |
| `STANDARD_CSV` | English column headers in .csv | Standard OHLCV CSV |
| `EXCEL` | .xlsx/.xls with English headers | Generic Excel file |
| `UNKNOWN` | Cannot determine | Not importable |

---

## Dry-run Default

**All operations default to dry_run=True.**

- `import-discover` — read-only scan, no writes ever
- `import-validate` — read-only validation, no writes ever
- `import-plan` — builds plan but writes nothing
- `import-batch` — executes plan in dry-run mode by default
  - Add `--execute` to allow execution
  - Add `--allow-write` to write to disk (requires `--execute`)

---

## Duplicate & Conflict Detection Rules

### Within-file duplicates
- **Identical rows** (same date, same OHLCV): treated as harmless duplicates → deduplicated on MERGE_SAFE
- **Conflicting rows** (same date, different OHLCV): → routed to `REVIEW`, never auto-resolved

### Against existing data
- **New rows** (date not in existing data): imported normally
- **Identical duplicates** (same date, same values): skipped silently
- **Conflicts** (same date, different values): → action=`REVIEW`, never auto-overwrite

---

## REPLACE_EXPLICIT Policy

`REPLACE_EXPLICIT` is **BLOCKED by default**.

To enable:
```python
from data_onboarding.import_planner import ImportPlanner
planner = ImportPlanner()
plan = planner.build_plan(path, mode="REPLACE_EXPLICIT", allow_replace=True)
```

This is a destructive operation. Use only when you are certain the existing data is wrong
and you have a backup. Never use for routine updates.

---

## CLI SOP

```bash
# 1. Discover files
python main.py import-discover --path /path/to/data

# 2. Preview a single file's columns
python main.py import-preview --file /path/to/data/2454.xlsx

# 3. Validate all files
python main.py import-validate --path /path/to/data

# 4. Build import plan (dry-run)
python main.py import-plan --path /path/to/data

# 5. Execute batch (dry-run by default)
python main.py import-batch --path /path/to/data --dry-run

# 6. Execute batch (write mode — use with caution)
python main.py import-batch --path /path/to/data --execute --allow-write

# 7. Check retry manifest
python main.py import-retry-manifest

# 8. Health check
python main.py import-onboarding-health

# 9. Build report
python main.py import-onboarding-report --mode real
```

---

## Batch Onboarding Workflow

1. **Prepare** — Place XQ export files or CSV files in a folder
2. **Discover** — `import-discover --path <folder>` — see what was found
3. **Validate** — `import-validate --path <folder>` — check required columns, dates, OHLC
4. **Plan** — `import-plan --path <folder>` — see planned actions; review BLOCKED/REVIEW items
5. **Dry Run** — `import-batch --path <folder> --dry-run` — simulate execution
6. **Execute** — `import-batch --path <folder> --execute --allow-write` — write (if ready)
7. **Retry** — `import-retry-manifest` — build plan for failed files
8. **Report** — `import-onboarding-report` — full Markdown report

---

## Retry Manifest

Failed import files are tracked in a **RetryManifest** JSON file:

```
data/import_reports/retry_manifest_YYYYMMDD_HHMMSS.json
```

The manifest contains:
- `failed_files`: list of file paths that failed
- `failed_symbols`: list of symbols that failed
- `retry_count`: how many times this manifest has been retried
- `resolved`: whether all failures are resolved

To retry:
```bash
python main.py import-retry-manifest
```

---

## Universe Coverage Refresh

After a successful import (`allow_write=True`), the system automatically calls
`UniverseCoverageAnalyzer` to refresh coverage statistics for imported symbols.

Manual refresh:
```bash
python main.py universe-coverage --tier research30
```

---

## GUI SOP

1. Open **Data Import & Batch Onboarding** tab (v1.1.1)
2. Enter or browse to source directory
3. Click **Discover** — cards update with file counts
4. Click **Validate** — status shows OK/WARNING/FAIL/BLOCKED
5. Click **Build Plan** — table shows planned actions
6. Review REVIEW items — resolve conflicts manually
7. Click **Execute Safe** — dry-run execution (no writes)
8. If ready to write: use CLI `--allow-write` (GUI is always dry-run safe)
9. Click **Refresh Coverage** — update universe coverage
10. Click **Build Report** — generates Markdown report

---

## Safety Declaration

| Safety Flag | Value |
|-------------|-------|
| Research Only | True |
| No Real Orders | True |
| Broker Execution | DISABLED |
| Production Trading | BLOCKED |
| Dry Run Default | True |
| Destructive Import Disabled | True |
| REPLACE_EXPLICIT Blocked by Default | True |
| Conflict Auto-Overwrite Enabled | False |
| Mock Data Formal Conclusion Allowed | False |

> [!] This documentation is for research purposes only.
> [!] No investment advice. Not for production trading.

## v1.1.2 Integration

v1.1.2 Coverage Repair Workflow integrates with v1.1.1 onboarding:
- `IMPORT_FAILED` → `CoverageIssue(IMPORT_FAILED)`
- PARTIAL import → `CoverageIssue(PARTIAL_OHLC)`
- conflict file → MANUAL review task
- retry manifest → `CoverageRepairTaskBuilder`
- `REIMPORT_SAFE` calls existing `BatchImportExecutor`, does not duplicate write logic

See `docs/coverage_repair_workflow_v1.1.2.md` for full v1.1.2 specification.

## v1.1.3 Integration

v1.1.3 Data Freshness Monitor extends the onboarding workflow with ongoing freshness tracking:
- After initial onboarding via `import-batch`, the freshness monitor detects when imported data becomes stale over time
- `freshness-scan` checks last-updated timestamps for all onboarded symbols across datasets (daily_price, chips, revenue, fundamentals)
- `freshness-repair-handoff` creates task dicts compatible with the data onboarding workflow — tasks can be resolved by running `import-batch` with fresh source files
- `freshness-alerts --severity critical` surfaces symbols where onboarded data has aged past the staleness threshold

See freshness monitor documentation for full v1.1.3 specification.
