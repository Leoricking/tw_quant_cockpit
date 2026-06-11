# Daily Operation Example

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Overview

This example shows a typical daily research session for TW Quant Cockpit v1.0.6.
All steps are research-only. No trading actions are taken.

---

## Step 1 — Check Version

```
python main.py version-info
```

Expected output: VERSION=1.0.6, all safety flags confirmed.

## Step 2 — Run Research Cockpit Stable Check

```
python main.py research-cockpit-stable --mode real
```

Expected: 49/49 PASS or acceptable WARNs.

## Step 3 — Run Strategy Lab Dashboard

```
python main.py strategy-lab-dashboard --mode real
```

Review validation grades, evidence health, and action board.

## Step 4 — Generate Daily Report Pack

```
python main.py report-pack --type daily --mode real
```

Review the daily pack output. Do not act on signals — REVIEW only.

## Step 5 — Check Data Coverage

```
python main.py data-coverage-summary --mode real
```

Identify any data gaps for research planning.

## Step 6 — Review Safety Scan

```
python main.py safety-scan --target all
```

Expected: 0 BLOCKED files.

---

## Allowed Actions (REVIEW mode)

- REVIEW reports and dashboards
- READ_REPORT output files
- WAIT for more data before acting on any signal
- KEEP_OBSERVING strategy validation grades
- BACKTEST_MORE if validation is insufficient

## What NOT To Do

- Do NOT place real trading actions based on this system
- Do NOT treat VALIDATED grade as a trading signal
- Do NOT skip safety checks

---

## Safety Declaration

This example is Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. Templates do not enable trading.

---

*TW Quant Cockpit v1.0.6 — Example Workflows & Templates — Research Only — Not Investment Advice*
