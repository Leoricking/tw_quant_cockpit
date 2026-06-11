# Single Stock Research Example

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Overview

This example shows how to research a single stock using TW Quant Cockpit v1.0.6.
All steps are research-only. No trading actions are taken.

---

## Step 1 — Review Strategy Validation for the Stock

```
python main.py strategy-validation-summary --mode real
```

Find the stock's validation grade. Grade: INSUFFICIENT / OBSERVATIONAL / VALIDATING / VALIDATED.
REVIEW only — VALIDATED does not enable trading.

## Step 2 — Run Crash Reversal Check

```
python main.py crash-reversal --mode real
```

REVIEW post-crash stabilization checklist for the stock.
This is research analysis only — not a trading recommendation.

## Step 3 — Check Strategy Lab Dashboard

```
python main.py strategy-lab-dashboard --mode real
```

REVIEW all grades for the stock in the validation board.

## Step 4 — Review Evidence Graph

```
python main.py evidence-graph --mode real
```

REVIEW evidence threads linked to the stock. Look for STRONG or PARTIAL threads.

## Step 5 — Review Research Intelligence

```
python main.py research-intelligence --mode real
```

REVIEW any P0/P1 recommendations related to the stock.

## Step 6 — Review Backtest Coach Tasks

```
python main.py backtest-coach-summary --mode real
```

REVIEW BACKTEST_MORE and READ_REPORT tasks for the stock.

---

## Allowed Actions (REVIEW mode)

- REVIEW all modules for the stock
- READ_REPORT output files
- BACKTEST_MORE if grade is NEEDS_BACKTEST
- KEEP_OBSERVING while grade is VALIDATING
- WAIT for more evidence if grade is NEEDS_DATA

## What NOT To Do

- Do NOT place real trading actions based on this system
- Do NOT interpret VALIDATED as permission to trade
- Do NOT skip evidence graph check

---

## Safety Declaration

This example is Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. Templates do not enable trading.

---

*TW Quant Cockpit v1.0.6 — Example Workflows & Templates — Research Only — Not Investment Advice*
