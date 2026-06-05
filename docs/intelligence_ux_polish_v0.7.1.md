# Intelligence UX Polish — v0.7.1

> **[!] Research Intelligence Only. Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] All recommendations are research actions only (REVIEW / RESEARCH / PRACTICE / FIX_DATA / GENERATE_REPORT).**
> **[!] No BUY / SELL / ORDER output.**

---

## Overview

v0.7.1 polishes the Research Intelligence UX introduced in v0.7.0. The goal is to make each
recommendation readable at a glance — **why it matters**, **why act now**, **what happens if ignored**,
and **exactly which command is safe to run**.

---

## New Concepts

### Today Focus

A single one-line summary of the most important thing to do today.

Priority: P0 item → P1 item → first recommendation → default message.

```
Today Focus: P0: Missing daily_k data for 2 symbols — regression will fail
```

### Why Now

Each priority board item and plan entry now shows why the item is time-sensitive.

Examples:
- "Data gap detected today — backtest will use stale data"
- "Rule not reviewed in 90+ days — confidence may have drifted"
- "Replay session has unreviewed mistakes — pattern recurs"

### Risk If Ignored

What happens if you skip this item.

Examples:
- "Regression result unreliable without this data fix"
- "Strategy may execute on outdated rule weights"
- "Replay training quality degrades without mistake review"

### Command Safety Classification

`classify_command_safety(command)` returns one of six labels:

| Label | Meaning |
|-------|---------|
| `SAFE_READ_ONLY` | Reads data only, no side effects |
| `SAFE_REPORT` | Generates a Markdown report |
| `SAFE_REGRESSION` | Runs a regression suite |
| `SAFE_REPLAY` | Starts a replay training session |
| `SAFE_DATA_CHECK` | Checks data coverage or quality |
| `BLOCKED_FOR_TRADING` | Command contains forbidden trading keywords |

Commands containing: `buy`, `sell`, `order`, `execute`, `submit_order`, `auto_trade`, `place_order`, `broker_order`, `real_trade` → always returns `BLOCKED_FOR_TRADING`.

---

## CLI Changes

### `research-intelligence-summary`

```
Overall Status  : OK
Today Focus     : No critical issues — continue optional reports and replay practice
Top P0          : —
Top P1          : —
Total Signals   : 3
Recommendations : 5
Safe Commands   : 5
Blocked Trading : 0  (by design — no real orders)
```

### `research-intelligence-recommendations`

```
Pri  Action                  Safety               Title
---  ----------------------  -------------------  ----------------------------------------
P2   GENERATE_REPORT         SAFE_REPORT          Generate Research Intelligence Report
P2   RUN_REGRESSION          SAFE_REGRESSION      Run Regression Suite — Verify Stable
P3   READ_REPORT             SAFE_READ_ONLY       Read Latest Stable Release Report
```

### `research-intelligence-priority`

```
P2 — 中優先 (1 items):
  • Generate Research Intelligence Report
    Why Now : Signals collected — report not yet generated today
    Command : python main.py research-intelligence-report  [SAFE_REPORT]
```

### `research-intelligence-daily-plan`

```
Daily Research Plan (5/5 items shown):

 1. [P2] Generate Research Intelligence Report
      Command : python main.py research-intelligence-report  [SAFE_REPORT]
      Why Now : Signals collected — report not yet generated today
```

---

## GUI Changes

### Summary Cards

Eight summary cards at the top of the Research Intelligence panel:

| Card | Description |
|------|-------------|
| Today Focus | One-liner most important task (truncated to 60 chars) |
| Total Signals | Total signal count |
| P0 Critical | Number of P0 priority board items |
| P1 High | Number of P1 priority board items |
| Safe Commands | Count of safe (non-BLOCKED) commands |
| Blocked Trading | Always 0 (by design — no real orders) |
| Recommendations | Total recommendation count |
| Overall Status | OK / REVIEW / ATTENTION_NEEDED |

### Priority Board Columns

| Column | Description |
|--------|-------------|
| Priority | P0 / P1 / P2 / P3 (color-coded) |
| Title | Item title |
| Why Now | Time-sensitive reason |
| Risk If Ignored | Consequence of skipping |
| Safe Command | The command to run |
| Safety | Safety label (SAFE_REPORT etc.) |
| Due | When to address (Immediately / This Week / etc.) |

### Plan Table Columns

| Column | Description |
|--------|-------------|
| # | Rank |
| Title | Task title |
| Category | Signal category |
| Command | Suggested command |
| Safety | Command safety label |
| Why Now | Why this is time-sensitive |
| Risk If Ignored | Consequence of skipping |

### Filter Controls

Three dropdown filters appear above the tab content:
- **Priority** — All / P0 / P1 / P2 / P3
- **Category** — All / DATA_GAP / REPORT_GAP / etc. (auto-populated)
- **Source** — All / data_coverage / report_pack / etc. (auto-populated)

Filters apply immediately to the All Signals table. They populate after "Run Intelligence" completes.

### Copy Command

1. Select any row in Priority Board or Plans table
2. The command appears in the "Selected Command" field at the top
3. Click "Copy Command" to copy to clipboard

---

## Report Changes

### New Sections

| Section | Description |
|---------|-------------|
| `一、Today Focus` | Overall status, top P0/P1, safe/blocked counts |
| `六、Signals by Module` | All signals grouped by source module |
| `七、Command Safety` | Safe commands list, blocked trading count=0 |
| `八、What Not To Do` | Static forbidden action table |

### Updated Sections

- `三、Priority Board` — Why Now, Risk If Ignored, Safe Command columns
- `四、Daily Research Plan` — Why Now, Risk If Ignored columns
- `五、Weekly Research Plan` — Why Now, Risk If Ignored columns

---

## Safety Invariants (unchanged)

| Invariant | Value |
|-----------|-------|
| `read_only` | `True` |
| `no_real_orders` | `True` |
| `production_blocked` | `True` |
| `real_order_ready` | `False` |
| Forbidden actions | BUY / SELL / ORDER / EXECUTE / SUBMIT_ORDER / AUTO_TRADE / PLACE_ORDER / BROKER_ORDER / REAL_TRADE |
| blocked_trading_action_count | Always 0 — forbidden action guard ensures this |

---

> [!] Research Intelligence Only. Research Only. No Real Orders. Not investment advice.
> All commands are read-only research actions. No broker connected.
