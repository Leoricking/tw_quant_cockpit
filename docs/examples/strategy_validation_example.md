# Strategy Validation Example

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Overview

This example shows how to run and interpret strategy validation checks using TW Quant Cockpit v1.0.6.
VALIDATED grade is research-only and does NOT enable trading.

---

## Step 1 — View Current Validation Queue

```
python main.py strategy-validation --mode real
```

Review all strategies and their current validation grades.

## Step 2 — Check Strategies Needing Backtest

```
python main.py strategy-validation-needs-backtest --mode real
```

Review strategies flagged as NEEDS_BACKTEST. Plan BACKTEST_MORE tasks.

## Step 3 — Check Conflicted Strategies

```
python main.py strategy-validation-conflicted --mode real
```

REVIEW conflicted strategies. WAIT for contradictions to resolve before advancing grade.

## Step 4 — Review Top Validated Strategies

```
python main.py strategy-validation-top --mode real
```

REVIEW strategies with the highest validation scores.
These are RESEARCH-VALIDATED only — no trading permission is granted.

## Step 5 — Generate Validation Report

```
python main.py strategy-validation-report --mode real
```

READ_REPORT the generated validation report. Archive for review.

## Step 6 — Check Evidence Graph Support

```
python main.py evidence-graph-thread-quality --mode real
```

REVIEW thread quality for top strategies. STRONG threads support validation.

---

## Grade Interpretation

| Grade | Meaning | Action |
|-------|---------|--------|
| INSUFFICIENT | Very little evidence | BACKTEST_MORE |
| OBSERVATIONAL | Some evidence, not validated | KEEP_OBSERVING |
| VALIDATING | Active validation in progress | WAIT |
| VALIDATED | Research validated | REVIEW — no trading permission |
| CONFLICTED | Contradicting evidence | WAIT for resolution |
| REJECTED | Evidence does not support | KEEP_OBSERVING or archive |

**VALIDATED does NOT enable trading.**

---

## Allowed Actions (REVIEW mode)

- REVIEW validation grades and scores
- READ_REPORT validation report
- BACKTEST_MORE for NEEDS_BACKTEST strategies
- KEEP_OBSERVING VALIDATING strategies
- WAIT when evidence is conflicted

## What NOT To Do

- Do NOT treat VALIDATED as trading permission
- Do NOT skip evidence graph check
- Do NOT use validation scores as trading signals

---

## Safety Declaration

This example is Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. Templates do not enable trading.
VALIDATED does not enable trading.

---

*TW Quant Cockpit v1.0.6 — Example Workflows & Templates — Research Only — Not Investment Advice*
