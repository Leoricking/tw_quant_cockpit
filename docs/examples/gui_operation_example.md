# GUI Operation Example

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Overview

This example shows how to operate the TW Quant Cockpit GUI for v1.0.6.
The GUI is for research review only — no trading actions can be taken.

---

## Step 1 — Launch the GUI Cockpit

```
python main.py cockpit
```

The main dashboard opens with all available tabs.

## Step 2 — Navigate Tabs

The GUI has the following tab groups:

- **Research Intelligence** — Priority board, daily plan, signal aggregation
- **Strategy Lab Dashboard** — Validation board, evidence board, action board
- **Strategy Validation Score** — INSUFFICIENT / OBSERVATIONAL / VALIDATING / VALIDATED
- **Crash Reversal** — Post-crash analysis
- **Evidence Graph** — Evidence threads, graph gaps
- **Data & Report Hygiene** — Runtime output inventory
- **GUI Navigation** — Tab search, favorites, recent tabs

## Step 3 — Use the Navigation Tab

In the GUI tab bar, find the **GUI Navigation** tab:
1. Type a keyword in the search box (e.g., "validation", "evidence", "daily")
2. The matching tabs are shown in the results panel
3. Click a tab name to jump to it

## Step 4 — Copy Safe Commands

In any research panel, use the **Copy Command** button to copy safe CLI commands.
These commands are READ-ONLY research commands — not trading commands.

## Step 5 — Run GUI Health Check

```
python main.py gui-health-check
```

REVIEW the GUI health report. All panels should import correctly.

---

## GUI Safety Notes

- All GUI panels display a safety banner: "Research Only | No Real Orders | Production BLOCKED"
- No GUI panel can place real trading actions
- QThread workers are used for non-blocking operations — they do not trigger trading
- Empty state panels show safe placeholder text when no data is available

---

## Allowed Actions (REVIEW mode)

- REVIEW all GUI panels and dashboards
- READ_REPORT by clicking report buttons in panels
- KEEP_OBSERVING strategy grades in the validation board
- WAIT when panels show insufficient data

## What NOT To Do

- Do NOT interpret any GUI output as a trading signal
- Do NOT run the GUI as a live trading terminal
- Do NOT skip GUI health check after updates

---

## Safety Declaration

This example is Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. GUI does not enable trading.

---

*TW Quant Cockpit v1.0.6 — Example Workflows & Templates — Research Only — Not Investment Advice*
