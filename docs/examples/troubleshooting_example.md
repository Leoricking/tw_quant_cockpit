# Troubleshooting Example

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Overview

This example shows how to diagnose and resolve common issues in TW Quant Cockpit v1.0.6.
All troubleshooting steps are safe research operations.

---

## Common Issue 1 — Import Error

**Symptom:** `ImportError: No module named 'workflows'`

**Steps:**
1. Check Python path
2. Run from the project root:

```
python main.py version-info
```

If this fails, check that you are in `C:/Users/Rossi/Documents/Claude/trading_master`.

## Common Issue 2 — CP950 Encoding Warning

**Symptom:** `UnicodeDecodeError: 'cp950' codec can't decode...`

**Classification:** KNOWN_CP950_WARNING — non-critical

This is an acceptable warning. The system uses UTF-8 for all new files.
No action required.

## Common Issue 3 — Report Not Generated

**Symptom:** Report shows as MISSING or NOT_GENERATED in report pack

**Steps:**

```
python main.py data-report-hygiene-summary
```

REVIEW which reports are missing. Run the specific report generator:

```
python main.py documentation-report --mode real
```

## Common Issue 4 — Safety Scanner BLOCKED

**Symptom:** `safety-scan` returns BLOCKED files

**Steps:**
1. READ_REPORT the blocked file paths
2. REVIEW the forbidden keywords found
3. Fix the file to use safe alternatives (REVIEW instead of forbidden keywords)
4. Re-run safety scan:

```
python main.py safety-scan --target all
```

## Common Issue 5 — Regression Failures

**Symptom:** `regression-run` returns FAIL

**Steps:**

```
python main.py regression-run --suite release_gate --mode real
```

REVIEW which tests failed. Check the error message.
WAIT before attempting a fix — read the error carefully.

## Common Issue 6 — GUI Won't Launch

**Symptom:** `python main.py cockpit` fails

**Steps:**

```
python main.py gui-health-check
```

REVIEW the health check output for import errors.

## Common Issue 7 — paper_state.json Missing

**Symptom:** Paper smoke test shows WARN about missing state file

**Classification:** KNOWN_PAPER_SMOKE_WARNING — non-critical

This is an acceptable warning. The paper state file is created on first run.

---

## Allowed Actions (REVIEW mode)

- REVIEW error messages carefully
- READ_REPORT health check outputs
- WAIT before making changes
- KEEP_OBSERVING if issue is a known acceptable warning

## What NOT To Do

- Do NOT make changes without understanding the error
- Do NOT skip safety scan when fixing issues
- Do NOT commit broken code

---

## Safety Declaration

This example is Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. Troubleshooting does not enable trading.

---

*TW Quant Cockpit v1.0.6 — Example Workflows & Templates — Research Only — Not Investment Advice*
