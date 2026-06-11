# Data Hygiene Example

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Overview

This example shows how to run data and report hygiene checks using TW Quant Cockpit v1.0.6.
Data hygiene is review-only — no file deletion is performed automatically.

---

## Step 1 — Run Data Report Hygiene Summary

```
python main.py data-report-hygiene-summary
```

REVIEW the summary of runtime outputs and report files.

## Step 2 — Check Report Inventory

```
python main.py data-report-hygiene-inventory
```

READ_REPORT the full inventory of runtime output files.

## Step 3 — Check Gitignore Coverage

```
python main.py data-report-hygiene-gitignore
```

REVIEW gitignore coverage. All runtime outputs should be gitignored.

## Step 4 — Check Tracked Files (should be 0)

```
python main.py data-report-hygiene-tracked
```

REVIEW any accidentally tracked runtime outputs. Expected: 0 tracked.

## Step 5 — Check for Large Files

```
python main.py data-report-hygiene-large-files
```

REVIEW large files (>5MB). Archive suggestions are suggestions only.

## Step 6 — Run Safety Scan

```
python main.py safety-scan --target all
```

Expected: 0 BLOCKED files. REVIEW any WARNs.

## Step 7 — Generate Hygiene Report

```
python main.py data-report-hygiene-report --mode real
```

READ_REPORT the generated hygiene report. Archive for review.

---

## Allowed Actions (REVIEW mode)

- REVIEW hygiene inventory and coverage
- READ_REPORT hygiene report
- WAIT before archiving large files (manual decision only)
- KEEP_OBSERVING tracked files list

## What NOT To Do

- Do NOT automatically delete files based on this system
- Do NOT commit runtime outputs
- Do NOT ignore BLOCKED safety scanner results

---

## Safety Declaration

This example is Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. Templates do not enable trading.
Data hygiene is review-only. No automatic file deletion.

---

*TW Quant Cockpit v1.0.6 — Example Workflows & Templates — Research Only — Not Investment Advice*
