# Paper & Mock Practice Example

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Overview

This example shows how to use paper trading simulation and mock realtime features.
**Paper trading is simulation only** — no real money, no real positions.
**Mock realtime is simulation only** — not live market data.

---

## Paper Trading Simulation

Paper trading simulates research decisions with no real money or real positions.

```
python main.py paper
```

This runs the paper trading simulation. All positions are simulated.
No real orders are placed. No broker connection is made.

### What Paper Trading Is

- A research simulation tool
- Tracks hypothetical decisions for research purposes
- Helps evaluate strategy ideas in a safe environment

### What Paper Trading Is NOT

- Not real trading
- Not connected to any broker
- Not investment advice

## Mock Realtime Simulation

```
python main.py mock-realtime --duration 10
```

This runs a 10-second mock realtime simulation.
Data is simulated — not live market data.

### What Mock Realtime Is

- A simulation of realtime data flow
- Used for testing system components
- Research tool only

### What Mock Realtime Is NOT

- Not live market data
- Not connected to any data provider in realtime
- Not investment advice

---

## Replay Training Practice

```
python main.py intraday-replay --mode real
```

REVIEW the intraday replay session. Practice reading charts with no real decisions.

```
python main.py replay-training-summary --mode real
```

REVIEW training scores and replay metrics.

---

## Allowed Actions (REVIEW mode)

- REVIEW paper trading simulation results
- READ_REPORT replay training summary
- KEEP_OBSERVING simulation metrics
- WAIT before drawing conclusions from simulated data

## What NOT To Do

- Do NOT treat paper trading results as real performance
- Do NOT use mock realtime data for real decisions
- Do NOT skip safety checks in simulation mode

---

## Safety Declaration

This example is Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. Paper trading is simulation only. Mock realtime is simulation only.
Templates do not enable trading.

---

*TW Quant Cockpit v1.0.6 — Example Workflows & Templates — Research Only — Not Investment Advice*
