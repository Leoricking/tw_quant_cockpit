# Research Intelligence Stable v0.8.0

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not Investment Advice. REAL_ORDER_READY=False.**

---

## v0.8.0 Goals

v0.8.0 stabilizes the full Research Intelligence layer — combining Research Intelligence (v0.7.0–v0.7.1),
Strategy Research Memory (v0.7.2), and Backtest-to-Coach Loop (v0.7.3) into a validated,
documented, and audited intelligence layer for the TW Quant Cockpit.

Key deliverables:
- Intelligence Stable Schema (29 capabilities, 7-category checklist)
- Capability Matrix with stable_status for all 29 capabilities
- Stable Checklist (import health, CLI health, report health, safety, regression, runtime, stable integration)
- Release Manifest (JSON + Markdown)
- Intelligence Stable Engine + Store
- Intelligence Stable Report (11-section Markdown)
- GUI Panel (IntelligenceStablePanel) with safety banner, summary cards, capability/check tables
- CLI: 6 new commands (intelligence-stable, intelligence-stable-summary, etc.)
- Integration with report pack, regression suites, auto report center, stable release checks

---

## What Research Intelligence Stable Is

Research Intelligence Stable is NOT:
- Investment advice
- A live trading signal system
- A broker or order execution system
- An automatic strategy activator

Research Intelligence Stable IS:
- A validation framework for the v0.7.x Research Intelligence layer
- A structured audit of all research AI capabilities (29 capabilities)
- A safety audit that verifies no forbidden trading actions (BUY/SELL/ORDER) appear in any outputs
- A documentation and reporting layer for the Research OS v0.8.0 milestone

---

## v0.7.x Completion Summary

| Version | Feature | Status |
|---------|---------|--------|
| v0.7.0 | Research Intelligence Upgrade | Done |
| v0.7.1 | Intelligence UX Polish | Done |
| v0.7.2 | Strategy Research Memory | Done |
| v0.7.3 | Backtest-to-Coach Loop | Done |
| v0.8.0 | Research Intelligence Stable | Done |

---

## Intelligence Capability Matrix (29 Capabilities)

### Research Intelligence (8)
1. Research Intelligence Engine — STABLE
2. Signal Aggregator — STABLE
3. Recommendation Engine — STABLE
4. Priority Planner — STABLE
5. Daily Research Plan — STABLE
6. Weekly Research Plan — STABLE
7. Research Intelligence Report — STABLE
8. Safe Command Guard — STABLE

### Strategy Memory (7)
9. Strategy Memory Engine — STABLE
10. Memory Extractor — STABLE
11. Memory Store — STABLE
12. Memory Linker — USABLE
13. Memory Query — STABLE
14. Strategy Memory Report — STABLE
15. Strategy Memory GUI — STABLE

### Backtest Coach (6)
16. Backtest Coach Engine — STABLE
17. Backtest Signal Extractor — USABLE
18. Coach Task Builder — STABLE
19. Coach Training Task Store — STABLE
20. Backtest Coach Report — STABLE
21. Backtest Coach GUI — STABLE

### Supporting (8)
22. Replay Training UI — STABLE
23. Data Coverage Matrix — STABLE
24. Report Pack — STABLE
25. Regression Suite — STABLE
26. Stable Release Checklist — STABLE
27. No Real Orders Safety — STABLE
28. Production Trading BLOCKED — STABLE
29. Intelligence Stable v0.8.0 — STABLE

---

## Stable Checklist (7 Categories)

### A. Import Health
- Research Intelligence Engine import
- Strategy Memory Engine import
- Backtest Coach Engine import
- Intelligence Stable Report import
- Intelligence Stable Adapter import

### B. CLI Health
- research-intelligence-summary
- research-intelligence-recommendations
- strategy-memory-summary
- strategy-memory-list
- backtest-coach-summary
- backtest-coach-tasks

### C. Report Health
- Research Intelligence Report
- Strategy Memory Report
- Backtest Coach Report
- Report Pack Directory

### D. Safety
- Research Intelligence: No forbidden actions
- Strategy Memory: No forbidden actions
- Backtest Coach: No forbidden actions
- Capability Matrix: All capabilities have safety flags
- No broker submit_order in CLI

### E. Regression
- release_gate suite
- quick suite

### F. Runtime
- paper command
- mock-realtime command

### G. Stable Integration
- stable-v060-check
- Report Pack directory
- Data Coverage info

---

## Safety Audit

All 29 capabilities have:
- `no_real_orders = True`
- `production_blocked = True`

Forbidden keywords scanned: `BUY`, `SELL`, `ORDER`, `EXECUTE`, `SUBMIT_ORDER`, `AUTO_TRADE`, `REAL_TRADE`

Forbidden action count in all outputs: **0**

---

## Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│        Research Intelligence Stable v0.8.0              │
│   [!] Research Only | No Real Orders | Not Investment   │
├─────────────────────────────────────────────────────────┤
│  Layer 1: Research Intelligence                         │
│  - Signal aggregation from 8 modules                   │
│  - Recommendations (research tasks only)               │
│  - Priority Board (P0/P1/P2/P3)                        │
│  - Daily plan (7 items) / Weekly plan (12 items)       │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Strategy Memory                               │
│  - 10 memory types (STRATEGY_HYPOTHESIS, etc.)         │
│  - Upsert deduplication                                │
│  - Status/priority tracking                            │
│  - Keyword-heuristic linking                           │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Backtest-to-Coach Loop                        │
│  - Safe coach tasks only (PRACTICE_REPLAY, REVIEW, …) │
│  - No BUY/SELL/ORDER tasks                             │
│  - Daily/weekly training plan                          │
└─────────────────────────────────────────────────────────┘
```

---

## CLI Usage

### v0.8.0 Intelligence Stable Commands

```bash
# Run full intelligence stable validation
python main.py intelligence-stable --mode real

# Show latest summary
python main.py intelligence-stable-summary

# List all capabilities
python main.py intelligence-stable-capabilities

# Show all checks
python main.py intelligence-stable-checks

# Build release manifest
python main.py intelligence-stable-manifest

# Generate report
python main.py intelligence-stable-report --mode real
```

### v0.7.x Commands

```bash
# Research Intelligence
python main.py research-intelligence --mode real
python main.py research-intelligence-summary
python main.py research-intelligence-recommendations
python main.py research-intelligence-priority
python main.py research-intelligence-daily-plan
python main.py research-intelligence-weekly-plan
python main.py research-intelligence-report

# Strategy Memory
python main.py strategy-memory --mode real
python main.py strategy-memory-summary
python main.py strategy-memory-list
python main.py strategy-memory-search --keyword "2330"
python main.py strategy-memory-show --id MEM-001
python main.py strategy-memory-update-status --id MEM-001 --status CONFIRMED
python main.py strategy-memory-archive --id MEM-001
python main.py strategy-memory-report

# Backtest Coach
python main.py backtest-coach --mode real
python main.py backtest-coach-summary
python main.py backtest-coach-signals
python main.py backtest-coach-tasks
python main.py backtest-coach-daily-plan
python main.py backtest-coach-weekly-plan
python main.py backtest-coach-report
```

---

## GUI Usage

The Intelligence Stable tab is registered in the Cockpit GUI under the `research_os` group.

Features:
- Safety banner (always visible)
- Summary cards: Overall Status, Capabilities, Stable count, Checks PASS, Warnings, Forbidden Actions
- Capability Matrix table (29 rows)
- Stable Checklist table
- Safety Audit panel
- Report & Manifest panel
- Actions: Run Stable Validation (async), Generate Report, Build Manifest, Refresh

---

## Report Usage

The intelligence stable report (`reports/intelligence_stable_report_YYYY-MM-DD.md`) contains:
1. Header with version, safety declaration
2. Release Overview
3. Capability Matrix
4. Stable Checklist
5. Safety Audit
6. Research Intelligence Layer
7. Strategy Memory Layer
8. Backtest-to-Coach Layer
9. Regression / Report / Data Coverage
10. Known Limitations
11. Safety Declaration

---

## Known Limitations

1. No investment advice — all outputs are research tasks only
2. No automatic strategy activation
3. No live order execution — production trading is BLOCKED
4. Provider token environment limits may affect some reports
5. Optional reports may be missing if not yet generated
6. Backtest quality depends on data coverage

---

## No Real Orders Declaration

This system **does not** and **cannot** place real trading orders.

- `NO_REAL_ORDERS = True`
- `PRODUCTION_BLOCKED = True`
- `REAL_ORDER_READY = False`
- `read_only = True`

No broker connection. No Shioaji. No Mega. No auto-trading.

---

## Not Investment Advice Declaration

Nothing in TW Quant Cockpit v0.8.0, nor any output of the Research Intelligence Stable system,
constitutes investment advice, financial advice, or trading recommendations of any kind.

All outputs are for research and learning purposes only.
