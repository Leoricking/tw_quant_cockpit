# TW Quant Cockpit Safety Guide v1.0

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Core Safety Declarations

| Declaration | Status |
|-------------|--------|
| Research Only | True — all outputs are research results only |
| No Real Orders | True — no real trading actions possible |
| Production Trading BLOCKED | True — production trading is explicitly blocked |
| Broker Execution Disabled | True — no broker API connection |
| VALIDATED does not enable trading | True — VALIDATED is a research grade only |
| Paper Trading Is Simulation | True — paper trades are simulated, not real |
| Mock Realtime Is Simulation | True — mock realtime is not live market data |
| Not Investment Advice | True — nothing here is investment advice |
| Read Only | True — no auto-modification of strategies or weights |
| No Auto Weight Application | True — rule weights require manual review |
| No Shioaji | True — no Shioaji broker connection |
| No Mega Broker | True — no Mega broker connection |

---

## How the Safety Scanner Works

The `SafetyScanner` in `regression_hardening/safety_scanner.py` scans files for forbidden trading keywords.

### Forbidden Keywords (standalone uppercase)

```
BUY, SELL, ORDER, EXECUTE, SUBMIT_ORDER, AUTO_TRADE, REAL_TRADE, LIVE_TRADE, BROKER_ORDER
```

### Whitelist Phrases

The following phrases containing partial matches to forbidden keywords are explicitly whitelisted:

```
No Real Orders
No broker execution
Broker Execution Disabled
Not an order
```

When a forbidden keyword appears inside a whitelisted phrase, it is NOT flagged. This prevents false positives from safety documentation.

### Scan Results

- **PASS**: No forbidden keywords found (outside whitelist)
- **WARN**: Possible false positive — investigate
- **BLOCKED**: Forbidden keyword found outside whitelist — must be fixed

---

## Safe Actions vs Forbidden Actions

### Safe Research Actions

| Action | Type |
|--------|------|
| REVIEW | Research review |
| READ_REPORT | Read Markdown report |
| BACKTEST_MORE | Run additional backtests |
| PRACTICE_REPLAY | Practice with replay cockpit |
| REVIEW_RISK | Review risk parameters in reports |
| WAIT | Wait for more data |
| KEEP_OBSERVING | Continue observing a strategy |
| DO_NOT_CHASE | Research note — do not chase price |

### Forbidden Actions (Never in This System)

| Action | Why Forbidden |
|--------|--------------|
| Real broker execution | No broker API |
| Live position management | No trading engine |
| Auto rule weight application | Manual review required |
| Investment advice generation | Not a registered advisor |
| Automatic trading | Production trading blocked |

---

## VALIDATED Grade — What It Means

VALIDATED means:
- The strategy has been validated across multiple research evidence sources
- Backtests, replay sessions, coach tasks, evidence graph, and training metrics all support it
- It passes the cross-module confidence scoring threshold

VALIDATED does NOT mean:
- The strategy is ready for real trading
- It can be executed with a broker
- It guarantees positive returns
- It is investment advice

**VALIDATED = Research Validated Only. Production Trading BLOCKED.**

---

## Safety Invariants

These invariants are checked at every release:

```python
REAL_ORDERS_ENABLED = False
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
VALIDATED_DOES_NOT_ENABLE_TRADING = True
NO_REAL_ORDERS = True
read_only = True
production_blocked = True
```

These constants are in `release/version_info.py` and are checked by:
- `research-cockpit-stable` (44-item checklist)
- `stable-v060-check` (multi-category checklist)
- `release-gate-health` (release gate health check)
- `regression-run --suite release_gate` (regression suite)

---

*TW Quant Cockpit v1.0.5 — Documentation & User Guide Polish — Research Only — Not Investment Advice*
