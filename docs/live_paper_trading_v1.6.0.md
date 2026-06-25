# Live Paper Trading Foundation — v1.6.0

**Release date:** 2026-06-25
**Stage:** FOUNDATION
**Classification:** PAPER TRADING ONLY · SIMULATION_ONLY · NOT_FOR_PRODUCTION

---

## Safety Invariants

| Flag | Value |
|------|-------|
| `NO_REAL_ORDERS` | `True` |
| `BROKER_EXECUTION_ENABLED` | `False` |
| `PRODUCTION_TRADING_BLOCKED` | `True` |
| `REAL_ORDER_CREATION_ENABLED` | `False` |
| `PAPER_ORDER_CREATION_ENABLED` | `True` |
| `LIVE_PAPER_TRADING_RESEARCH_ONLY` | `True` |

**All paper orders carry `research_only=True`, `executable_on_broker=False`, `real_order_created=False`. These are enforced by `__post_init__` assertions and cannot be changed at runtime.**

---

## Architecture

### Session Lifecycle

```
CREATED → READY → RUNNING ⇄ PAUSED → COMPLETED
                          ↓
                        HALTED → RECOVERED → PAUSED / RUNNING
```

- Recovery default: `auto_resume=False` → always recovers to **PAUSED**
- Kill switch halt: preserves positions, **no auto close-out**, cancels queued orders

### Core Modules (34 total)

| Module | Purpose |
|--------|---------|
| `enums_v160.py` | All enumerations (12 enums) |
| `models_v160.py` | Dataclasses with safety assertions |
| `validation_v160.py` | Input validation helpers |
| `event_v160.py` | `PaperEvent` with hash chain support |
| `idempotency_v160.py` | Duplicate event rejection registry |
| `event_journal_v160.py` | Append-only, hash-chained event log |
| `event_bus_v160.py` | Process-local in-memory event bus |
| `market_session_v160.py` | Taiwan calendar (Asia/Taipei) |
| `data_classification_v160.py` | LIVE/DELAYED/REPLAY/FIXTURE/OFFLINE |
| `order_state_machine_v160.py` | 10-status paper order FSM |
| `latency_model_v160.py` | ZERO_DISCLOSED / FIXED_MS / EVENT_COUNT_DELAY |
| `slippage_model_v160.py` | FIXED_BPS / SPREAD_BASED / PARTICIPATION / VOLATILITY |
| `liquidity_model_v160.py` | Volume participation check |
| `partial_fill_v160.py` | Partial fill split logic |
| `paper_fill_v160.py` | Fill simulation entry point |
| `execution_simulator_v160.py` | Full execution pipeline |
| `paper_cash_v160.py` | Cash reserve / debit / credit |
| `paper_position_v160.py` | Position tracking |
| `paper_ledger_v160.py` | GENESIS-seeded hash-chained ledger |
| `paper_pnl_v160.py` | Realized + unrealized PnL |
| `paper_risk_gate_v160.py` | 16-check risk gate per order |
| `paper_kill_switch_v160.py` | 10-trigger kill switch |
| `snapshot_v160.py` | Session state snapshot |
| `audit_v160.py` | Audit trail |
| `lineage_v160.py` | Data lineage tracking |
| `reproducibility_v160.py` | Reproducibility manifest builder |
| `explain_v160.py` | Decision explanation |
| `store_v160.py` | In-memory session store |
| `session_replay_v160.py` | Event replay |
| `recovery_v160.py` | Snapshot + replay recovery |
| `session_v160.py` | Core session engine |
| `query_v160.py` | Query API (forbidden real-order methods) |
| `health_v160.py` | 40+ health checks |

---

## Slippage Models

| Model | Description |
|-------|-------------|
| `FIXED_BPS` | Fixed basis points (default 10bps), deterministic |
| `SPREAD_BASED` | Half bid-ask spread; warns if spread missing |
| `PARTICIPATION_BASED` | Proportional to volume participation rate |
| `VOLATILITY_ADJUSTED` | Half of volatility bps estimate |

All models are policy-versioned. Same inputs → same output (deterministic).

---

## Kill Switch Triggers (10)

1. `MANUAL_HALT` — explicit operator halt
2. `MAX_SESSION_LOSS` — total loss exceeds limit
3. `MAX_DRAWDOWN` — drawdown % exceeds limit
4. `MAX_REJECTED_ORDERS` — too many rejections
5. `MAX_MALFORMED_EVENTS` — data quality failure
6. `DATA_STALE` — market data age > threshold
7. `DATA_FEED_LOST` — feed connection lost
8. `LEDGER_HASH_MISMATCH` — hash chain broken
9. `RECONCILIATION_FAILURE` — position mismatch
10. `SAFETY_CONTRACT_VIOLATION` — safety flag tampered

**On trigger:** new paper orders blocked, queued orders cancelled, positions preserved, session halted. No automatic position close-out. Human review required.

---

## Data Classification

| Mode | Formal Conclusion | Paper Trading |
|------|------------------|---------------|
| `LIVE` | Yes | Yes (paper only) |
| `DELAYED` | Yes | Yes (disclose delay) |
| `REPLAY` | Yes (historical) | Yes |
| `FIXTURE` | **No** | Yes (labeled TEST) |
| `OFFLINE` | **No** | Yes (no live claims) |

**No real→mock fallback. No silent degradation to FIXTURE.**

---

## Taiwan Market Hours (Asia/Taipei)

| Period | Time |
|--------|------|
| Pre-Open | 08:30 – 09:00 |
| Regular Session | 09:00 – 13:30 |
| Closed | After 13:30 |
| Non-Trading | Weekends + TWSE holidays |

Fill simulation only permitted during OPEN session.

---

## Settlement Disclosure

`SIMPLIFIED_PAPER_SETTLEMENT` — NOT real T+2 Taiwan settlement. Settlement is simulated for paper trading purposes only. Not suitable for compliance or real financial reporting.

---

## CLI Commands (30)

All commands carry `safety_classification=SIMULATION_ONLY` and `group=live_paper_trading`.

Key commands:
- `paper-trading-health` — run health checks
- `paper-session-create` — create paper session
- `paper-session-start` / `paper-session-pause` / `paper-session-resume` / `paper-session-stop`
- `paper-session-status` — query session state
- `paper-order-submit` — submit paper order
- `paper-order-cancel` — cancel paper order
- `paper-order-list` — list orders
- `paper-fill-list` — list fills
- `paper-position-list` — list positions
- `paper-cash-balance` — cash status
- `paper-pnl-summary` — PnL summary
- `paper-risk-gate-check` — run risk gate
- `paper-kill-switch` — manual halt
- `paper-snapshot-create` / `paper-snapshot-list`
- `paper-ledger-verify` — verify hash chain
- `paper-session-replay` — replay events
- `paper-session-recover` — recover from snapshot
- `paper-reproducibility-manifest` — generate manifest
- `paper-session-report` — full session report

---

## Release Gate

`release/live_paper_trading_release_gate_v160.py` — 31 checks:
- 25 functional checks (imports, module structure, lifecycle, simulation)
- 6 safety gates (NO_REAL_ORDERS, BROKER_BLOCKED, PRODUCTION_BLOCKED, PAPER_ONLY_LEDGER, FORBIDDEN_METHODS, SAFETY_CONTRACT)

Safety gate failure sets `blocked: True` on the result.

---

## Reproducibility

Given the same:
- Session config (hash)
- Initial cash
- Policy IDs (slippage, liquidity, risk, sizing)
- Data mode + event sequence
- Python version + dependency versions

The system produces the same ledger hash and snapshot hash. Captured in `PaperSessionReproducibilityManifest`.

---

## Testing

- Test file: `tests/test_live_paper_trading_v160.py` (320+ tests)
- Fixture directory: `tests/fixtures/live_paper_trading/` (34 fixture files)
- All fixtures carry `fixture_type=TEST_FIXTURE`, `paper_only=true`, `not_real_order=true`

---

## Version History

| Version | Description |
|---------|-------------|
| 1.6.0 | Live Paper Trading Foundation — paper-only simulation system |
| 1.5.9.2 | Portfolio Stable Rollup Release Gate Compatibility Hotfix |
| 1.5.9 | Portfolio Stable Rollup |

---

*This document is for research and educational purposes only. Not for production trading, investment decisions, or financial planning.*
