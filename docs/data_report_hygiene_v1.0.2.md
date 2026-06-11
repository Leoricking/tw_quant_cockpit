# Data & Report Hygiene v1.0.2

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Data Cleanup is Review Only. Archive Suggestions Only.**
> **[!] No automatic deletion. No file moves. No automatic archive.**
> **[!] Not Investment Advice.**

Current version: **v1.0.2** — Data & Report Hygiene (base: v1.0.0 Research Trading Cockpit Stable)

---

## Overview

v1.0.2 adds a **review-only** Data & Report Hygiene module to TW Quant Cockpit.

This module scans the project for:
- Runtime output files (reports, backtest CSVs, JSON, databases, spreadsheets)
- Report manifest (all .md reports in reports/)
- .gitignore coverage for key runtime output patterns
- Git-tracked runtime outputs that should be ignored

**All outputs are for review only.** No files are deleted, moved, or archived.

---

## Safety Declaration

| Safety Flag | Value |
|-------------|-------|
| Research Only | True |
| No Real Orders | True |
| Production Trading BLOCKED | True |
| Broker Execution | Disabled |
| Data Cleanup | Review Only |
| Archive Suggestions | Review Only |
| No automatic deletion | True |
| No file moves | True |
| Not Investment Advice | True |

---

## CLI Usage

```bash
# Run full hygiene scan
python main.py data-report-hygiene --mode real

# Print latest summary
python main.py data-report-hygiene-summary

# List inventory items
python main.py data-report-hygiene-inventory

# List report manifest
python main.py data-report-hygiene-reports

# Check .gitignore coverage
python main.py data-report-hygiene-gitignore

# List git-tracked runtime outputs
python main.py data-report-hygiene-tracked

# List stale files (>30 days)
python main.py data-report-hygiene-stale

# List large files (>5MB)
python main.py data-report-hygiene-large-files

# Generate Markdown report
python main.py data-report-hygiene-report --mode real
```

---

## GUI Usage

Open the cockpit:

```bash
python main.py cockpit
```

Navigate to the **Data & Report Hygiene** tab.

The panel shows:
- Safety banner at top
- Summary cards: Total Items, Runtime Outputs, Git-tracked Runtime, Missing Gitignore, Stale Reports, Large Files, Warnings, Blocked
- Six tabs: Inventory, Reports, Gitignore Coverage, Tracked Runtime Outputs, Stale/Large Files, Explanation
- Buttons: Run Hygiene Scan, Generate Hygiene Report, Refresh, Copy Review Suggestion, Copy Gitignore Suggestion
- Keyword/category/severity filters

---

## Output Files

All outputs are runtime artifacts and are gitignored:

| Output | Location |
|--------|----------|
| Inventory CSV | data/backtest_results/maintenance/data_report_hygiene_inventory_*.csv |
| Report Manifest CSV | data/backtest_results/maintenance/data_report_hygiene_report_manifest_*.csv |
| Summary CSV | data/backtest_results/maintenance/data_report_hygiene_summary_*.csv |
| Hygiene Report | reports/data_report_hygiene_report_YYYY-MM-DD.md |

---

## Modules

| Module | Description |
|--------|-------------|
| maintenance/data_report_hygiene_engine.py | Scan engine — never deletes files |
| maintenance/data_report_hygiene_schema.py | Dataclasses: HygieneInventoryItem, HygieneReportManifest, HygieneSummary |
| maintenance/data_report_hygiene_store.py | Save/load CSV outputs |
| maintenance/data_report_hygiene_query.py | Query interface |
| reports/data_report_hygiene_report.py | Markdown report builder |
| gui/data_report_hygiene_panel.py | PySide6 GUI panel |
| gui/data_report_hygiene_adapter.py | GUI adapter |

---

## Categories

| Category | Description |
|----------|-------------|
| REPORT | Markdown report files in reports/ |
| BACKTEST_RESULT | CSV/JSON in data/backtest_results/ |
| DATABASE | .db/.sqlite files |
| SPREADSHEET | .xlsx/.xls files |
| JSON_OUTPUT | .json output files |
| LOG | Log files |
| CACHE | Cache files |
| EXPERIMENT_OUTPUT | Files in experiments/ |
| UNKNOWN | Other files |

---

## Action Hints

| Action | Meaning |
|--------|---------|
| REVIEW | Review this file — no automatic action |
| READ_REPORT | This is a report — read it |
| ARCHIVE_REVIEW | Consider archiving (review only — no automatic action) |
| CLEANUP_REVIEW | Consider cleanup (review only — no automatic action) |
| KEEP_OBSERVING | Normal runtime output |
| WAIT | No action needed |

---

## Safety Guarantees

1. **No deletion** — DataReportHygieneEngine never calls os.remove() or shutil.rmtree()
2. **No moves** — No os.rename() or shutil.move() calls
3. **No archive** — No zip creation or file copy operations
4. **Review-only** — review_only=True, no_real_orders=True on all objects
5. **No broker connection** — No shioaji, sinopac, or broker imports
6. **Not Investment Advice** — All outputs are for research review only

---

*TW Quant Cockpit v1.0.2 — Data & Report Hygiene — Research Only — Not Investment Advice*
