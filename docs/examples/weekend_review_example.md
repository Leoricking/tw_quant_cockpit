# Weekend Review Example

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Overview

This example shows a typical weekend research review session.
All steps are research-only. No trading actions are taken.

---

## Step 1 — Run Full Research Cockpit Check

```
python main.py research-cockpit-stable --mode real
```

Review all module health indicators.

## Step 2 — Generate Weekly Report Pack

```
python main.py report-pack --type weekly --mode real
```

Review the weekly pack output.

## Step 3 — Review Strategy Validation Scores

```
python main.py strategy-validation-scores --mode real
```

Review INSUFFICIENT / OBSERVATIONAL / VALIDATING / VALIDATED grades.
REVIEW each grade — do not use as trading signal.

## Step 4 — Review Evidence Graph Threads

```
python main.py evidence-graph-threads --mode real
```

REVIEW thread quality: STRONG / PARTIAL / NEEDS_DATA / NEEDS_BACKTEST.

## Step 5 — Review Weekly Regression

```
python main.py regression-run --suite release_gate --mode real
```

Review pass/fail counts. WAIT if any new failures appear.

## Step 6 — Review Research Intelligence Recommendations

```
python main.py research-intelligence --mode real
```

REVIEW P0/P1/P2/P3 recommendations. Do not act on them as trading signals.

## Step 7 — Generate Full Report Pack

```
python main.py report-pack --type full --mode real
```

Archive the full report pack for the week.

---

## Allowed Actions (REVIEW mode)

- REVIEW all module health status
- READ_REPORT all generated reports
- KEEP_OBSERVING strategies that are VALIDATING
- BACKTEST_MORE strategies flagged as NEEDS_BACKTEST
- WAIT for more evidence before advancing any strategy grade

## What NOT To Do

- Do NOT place real trading actions
- Do NOT treat VALIDATED grade as a trading permission
- Do NOT skip the regression check

---

## Safety Declaration

This example is Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. Templates do not enable trading.

---

*TW Quant Cockpit v1.0.6 — Example Workflows & Templates — Research Only — Not Investment Advice*
