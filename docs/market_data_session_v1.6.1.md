# Market Data Session Adapter v1.6.1

**TW Quant Cockpit — Research Only. No Real Orders. No Broker. Simulation Only.**

## Overview

v1.6.1 adds a complete market data ingestion, normalization, timing, and quality-governance layer
feeding into the Paper Trading system. All components are research-only with no broker API,
no credential storage, and no real order submission.

## Safety Invariants

| Flag | Value |
|------|-------|
| NO_REAL_ORDERS | True |
| BROKER_EXECUTION_ENABLED | False |
| PRODUCTION_TRADING_BLOCKED | True |
| MARKET_DATA_ONLY | True |
| NO_BROKER_API | True |
| LIVE_TO_FIXTURE_FALLBACK_DISABLED | True |
| LIVE_TO_OFFLINE_FALLBACK_DISABLED | True |
| UNKNOWN_SOURCE_AS_LIVE_DISABLED | True |
| SILENT_FIXTURE_FALLBACK_DISABLED | True |
| FUTURE_DATE_COUNTS_AS_FRESH | False |

## Pipeline Architecture

```
Provider Adapter → Raw Event → Validation → Normalization → Session Clock
    → Freshness/Sequence Gate → Canonical Event → Store → Paper Event Bus
```

## Modules (34 total)

| Module | Purpose |
|--------|---------|
| `__init__.py` | Package safety flags |
| `enums_v161.py` | 7 enum classes (9+11+6+6+6+4+9 values) |
| `models_v161.py` | 6 dataclasses with safety assertions |
| `validation_v161.py` | Raw event validation (bid≤ask, price>0) |
| `adapter_base_v161.py` | Abstract adapter interface |
| `adapter_registry_v161.py` | Registry (duplicate ID=BLOCKED, UNKNOWN=BLOCKED) |
| `public_provider_adapter_v161.py` | TWSE/TPEX/MOPS public adapter |
| `replay_adapter_v161.py` | Historical replay with PIT enforcement |
| `fixture_adapter_v161.py` | Static test fixture adapter |
| `offline_adapter_v161.py` | Local cached data adapter |
| `session_v161.py` | Full session lifecycle (11 states) |
| `session_clock_v161.py` | Injectable clock (no real sleep in tests) |
| `calendar_v161.py` | Taiwan market calendar (TWSE/TPEX windows) |
| `symbol_mapper_v161.py` | Provider→canonical mapping (ambiguous=BLOCKED) |
| `normalizer_v161.py` | Normalization coordinator |
| `quote_normalizer_v161.py` | Quote normalization (bid≤ask enforced) |
| `trade_normalizer_v161.py` | Trade normalization (price>0 enforced) |
| `sequence_v161.py` | Sequence gap/duplicate/out-of-order detection |
| `deduplication_v161.py` | Bounded LRU deduplication |
| `freshness_v161.py` | Freshness classification (future≠FRESH) |
| `delay_v161.py` | Delivery delay measurement (ms) |
| `quality_v161.py` | Quality gate (PASS/WARN/FAIL/BLOCKED) |
| `anomaly_v161.py` | Price spike and volume anomaly detection |
| `feed_monitor_v161.py` | Feed health: heartbeat, gaps, failures |
| `reconnect_v161.py` | Reconnect policy (NO/FIXED/EXPONENTIAL) |
| `failover_v161.py` | Failover (LIVE→FIXTURE/OFFLINE=BLOCKED) |
| `checkpoint_v161.py` | Checkpoint creation and storage |
| `resume_v161.py` | Session resume (always PAUSED, never RUNNING) |
| `lineage_v161.py` | Event lineage tracking through pipeline |
| `reproducibility_v161.py` | Deterministic session hash verification |
| `explain_v161.py` | Human-readable quality decision explanations |
| `store_v161.py` | Bounded in-memory canonical event store |
| `query_v161.py` | Read-only query service (broker methods=BLOCKED) |
| `health_v161.py` | 34-module health check |

## Key Invariants

### Bid ≤ Ask
All quote events enforce `bid_price <= ask_price`. Violations are dropped at normalization
and blocked at the model level.

### Freshness
- `LIVE_PUBLIC`: FRESH / DELAYED / STALE / EXPIRED / UNKNOWN
- `REPLAY` / `FIXTURE` / `OFFLINE` / `SIMULATION`: NOT_APPLICABLE
- Future timestamps: UNKNOWN (never FRESH)

### Checkpoint Resume
Checkpoint restore always sets `status=PAUSED`. Operator must call `start()` to go ACTIVE.
`RESUME_TO_PAUSED_NOT_RUNNING=True`

### PIT Enforcement (Replay)
`available_from <= paper_session_as_of` — events with future availability dates are excluded.

### Failover Blocks
- LIVE_PUBLIC → FIXTURE: **BLOCKED** (LIVE_TO_FIXTURE_FAILOVER_DISABLED=True)
- LIVE_PUBLIC → OFFLINE: **BLOCKED** (LIVE_TO_OFFLINE_FAILOVER_DISABLED=True)

### Reproducibility
Same raw events + config → same canonical events → same sequence decisions → same
quality results → same checkpoint hash → same session hash.

## Reconnect Policies

| Policy | Behavior |
|--------|---------|
| NO_RECONNECT | No auto-reconnect |
| FIXED_INTERVAL | Reconnect at fixed intervals |
| BOUNDED_EXPONENTIAL_BACKOFF | Exponential backoff with max_interval bound |

All use injectable clock — no real `sleep()` in tests.

## CLI Commands (29 new, all RESEARCH_ONLY)

```
market-data-health                   # Health check
market-data-session-create           # Create session
market-data-session-start            # Start session
market-data-session-pause            # Pause session
market-data-session-resume           # Resume (PAUSED→ACTIVE)
market-data-session-halt             # Halt session
market-data-session-complete         # Complete session
market-data-session-show             # Show session status
market-data-session-list             # List sessions
market-data-adapter-register         # Register adapter
market-data-adapter-list             # List adapters
market-data-event-list               # List events for symbol
market-data-quote-show               # Show latest quote
market-data-trade-show               # Show latest trade
market-data-quality-show             # Quality summary
market-data-freshness-show           # Freshness status
market-data-sequence-show            # Sequence status
market-data-feed-health              # Feed health status
market-data-anomaly-show             # Anomalies
market-data-checkpoint-create        # Create checkpoint
market-data-checkpoint-show          # Show checkpoint
market-data-session-restore          # Restore from checkpoint (→PAUSED)
market-data-lineage-show             # Event lineage
market-data-reproducibility-verify   # Verify reproducibility
market-data-explain                  # Explain quality decisions
market-data-calendar-show            # Taiwan market calendar
market-data-symbol-map               # Symbol mapping registry
market-data-session-report           # Generate research report
market-data-release-gate             # Release gate (34 checks)
```

## Test Coverage

- `tests/test_market_data_session_v161.py`: 360+ tests across 37 groups
- `tests/fixtures/market_data_session/`: 33 fixture files

## Release Gate

`release/market_data_session_release_gate_v161.py`: 34 checks covering:
- Safety invariants (6 checks)
- Version info (1)
- Enums (1)
- Models safety assertions (2)
- Adapter registry (1)
- Failover blocks (2)
- Checkpoint/Resume invariants (2)
- Symbol mapper (1)
- Freshness (2)
- Deduplication (1)
- Sequence (1)
- Reconnect policies (2)
- Reproducibility (1)
- Session E2E pipeline (1)
- CLI registration (2)
- GUI panel (1)
- Report (1)
- Docs (1)
- Fixtures (1)
- No broker API (1)
- Canonical event safety markers (1)
- Health check (1)
- v1.6.0 backward compat (1)

---
*[!] Research Only. No Real Orders. No Broker. Not Investment Advice.*
