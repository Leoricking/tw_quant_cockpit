# Research Trading Cockpit Stable v1.0.0

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] VALIDATED does not enable trading. Broker Execution Disabled.**
> **[!] Not Investment Advice.**

---

## v1.0.0 目標 (Goals)

TW Quant Cockpit v1.0.0 is the first stable research cockpit release.
It provides a unified research environment for strategy research, validation, evidence tracking,
crash reversal analysis, and training — all research-only, no real trading.

---

## System Modules

| Module | CLI | Status |
|--------|-----|--------|
| Strategy Lab Dashboard | `strategy-lab-dashboard` | STABLE |
| Strategy Validation Score | `strategy-validation` | STABLE |
| Evidence Graph UX | `evidence-graph-ux` | STABLE |
| Crash Reversal Strategy Pack | `crash-reversal` | STABLE |
| Strategy Lab Stable | `strategy-lab` | STABLE |
| Training Metrics | `training-metrics` | STABLE |
| Backtest Coach | `backtest-coach` | STABLE |
| Strategy Memory | `strategy-memory` | STABLE |
| Research Intelligence | `research-intelligence` | STABLE |
| Data Coverage | `data-coverage` | STABLE |
| Report Pack | `report-pack` | STABLE |
| Regression Gate | `regression-run` | STABLE |
| Paper Trading | `paper` | SIMULATION ONLY |
| Mock Realtime | `mock-realtime` | SIMULATION ONLY |

---

## Dashboard Cards

The Strategy Lab Dashboard shows:
- Strategy Lab Status (validation grades)
- Validation Grade Mix (INSUFFICIENT/OBSERVATIONAL/VALIDATING/VALIDATED/CONFLICTED/REJECTED)
- Evidence Health (threads, orphans)
- Crash Reversal Risk (high/extreme warnings)
- Needs Backtest / Needs Replay / Needs Data
- Training Progress (improving/worsening metrics)
- Active Strategy Memories
- Coach Tasks
- Report Pack Health
- No Real Orders Safety
- **v1.0.0 cards:** Release Version, Stable Status, Broker Execution (Disabled), Paper/Mock (Simulation Only)

---

## Validation Board

Validation grades:
```
INSUFFICIENT → OBSERVATIONAL → VALIDATING → VALIDATED
                                          → CONFLICTED
                                          → REJECTED
```

**VALIDATED = Research Validated Only. Does NOT enable trading.**

---

## Evidence Board

Evidence threads with quality labels:
- STRONG_EVIDENCE — multiple consistent supporting nodes
- PARTIAL_EVIDENCE — some support, some missing
- NEEDS_DATA — data gaps blocking validation
- NEEDS_BACKTEST — backtest required
- CONFLICTED — contradictory evidence
- ORPHANED — isolated nodes with no thread

---

## Crash Reversal Board

6-stage crash reversal analysis:
1. Crash Cause Classifier (Fundamental/Financial/Technical/Systemic)
2. Post-Crash Stabilization Checklist (8 conditions)
3. Relative Strength After Crash Score
4. Sakata EPS-backed Dip Buy Filter
5. Moving Average Profit Discipline
6. High-Risk Industry Exposure Guard

Research Only — these checks do NOT trigger any real trading actions.

---

## Action Board

Action items are SAFE_READ_ONLY commands:
- BACKTEST_MORE → run `strategy-validation --mode real`
- PRACTICE_REPLAY → run `replay-training`
- FIX_DATA → run `data-coverage-gaps`
- REVIEW_RISK → run `crash-reversal-summary`
- READ_REPORT → run `strategy-lab-dashboard-report`

No BUY/SELL/ORDER actions. No broker connections.

---

## Module Health

Run: `python main.py research-cockpit-stable-checks`

---

## CLI Usage

```bash
# Version info
python main.py version-info

# Research Cockpit Stable
python main.py research-cockpit-stable --mode real
python main.py research-cockpit-stable-summary
python main.py research-cockpit-stable-checks
python main.py research-cockpit-stable-manifest
python main.py research-cockpit-stable-report --mode real

# Strategy Lab Dashboard
python main.py strategy-lab-dashboard --mode real
python main.py strategy-lab-dashboard-summary
python main.py strategy-lab-dashboard-cards

# Strategy Validation
python main.py strategy-validation --mode real
python main.py strategy-validation-summary

# Evidence Graph
python main.py evidence-graph-ux --mode real
python main.py evidence-graph-summary

# Crash Reversal
python main.py crash-reversal-summary

# Regression
python main.py regression-run --suite release_gate --mode real

# Paper / Mock (simulation only)
python main.py paper
python main.py mock-realtime --duration 10
```

---

## GUI Usage

Launch: `python main.py gui`

Tabs:
- Strategy Lab Dashboard — unified dashboard board
- Strategy Lab Stable — capability matrix, checklist
- Strategy Validation Score — validation grade board
- Evidence Graph — evidence threads and gaps
- Research Intelligence Stable — intelligence stable
- Backtest Coach — coach tasks and signals
- Training Metrics — metric trends
- Strategy Memory — memory items and validation queue

---

## No Real Orders

This system enforces No Real Orders at all times:

```python
REAL_ORDERS_ENABLED               = False
NO_REAL_ORDERS                    = True
PRODUCTION_TRADING_BLOCKED        = True
BROKER_EXECUTION_ENABLED          = False
VALIDATED_DOES_NOT_ENABLE_TRADING = True
PAPER_TRADING_IS_SIMULATION       = True
MOCK_REALTIME_IS_SIMULATION       = True
```

---

## VALIDATED does not enable trading

Even when a strategy reaches VALIDATED grade:
- No broker connection is made
- No real order is placed
- No trading is enabled
- VALIDATED = Research Validated Only

This is enforced at the module level and cannot be bypassed.

---

## Roadmap

| Version | Feature | Priority |
|---------|---------|---------|
| v1.0.x | Maintenance — bug fixes, warning cleanup | P1 |
| v1.1 | Data Quality / Universe Expansion | P2 |
| broker-api-branch | Broker API (only if explicitly requested) | ON_REQUEST |

---

*TW Quant Cockpit v1.0.0 — Research Trading Cockpit Stable — Research Only — Not Investment Advice*
