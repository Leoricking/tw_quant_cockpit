# Multi-Timeframe Replay v1.2.5

> [!] Research Only. No Real Orders. Not Investment Advice.
> [!] Agreement/Conflict analysis is Training Only. No Auto-Trade. No Auto-Block.
> [!] Batch default preview mode. BLOCKED without --execute --allow-write.

## Overview

Multi-Timeframe Replay (MTF) enables synchronized replay across D1, M60, M20, M5, and M1 timeframes
with a single authoritative clock, point-in-time verified indicators, and strict future data firewall.

## Key Architecture

- **Single Clock**: `ReplayTimeframeClock` is the only time source. No individual TF clock.
- **Hierarchy**: D1 > M60 > M20 > M5 > M1
- **Session defaults**: primary_timeframe=M5, trigger_timeframe=M1 (fallback M5 if M1 missing, explicit log)
- **Bar aggregation**: 1m → 5m/20m/60m only. Daily is NEVER aggregated from intraday.
- **Past-only asof join**: NO bfill, NO centered rolling, NO nearest-future.

## Future Data Firewall

All bars pass through `MultiTimeframeFutureDataFirewall` before display:

- Block timestamp > replay_timestamp
- Block available_at > replay_timestamp
- Block incomplete bar marked as complete (daily close leak)
- Block aggregation leaks
- Block indicator leaks (forward-looking calculations)
- Strip forbidden fields: forward_return, realized_pnl, hindsight_score, outcome, etc.

## Partial Bar Protection

- Partial bar qualification: `PARTIAL_OBSERVATION` (never `CONFIRMED`)
- Partial bar close: `confirmed_close=False`
- Partial bar breakout: `confirmed_breakout=False`
- Indicators calculated on **completed bars only**
- Partial bar `visible_ohlcv()` used for display only, not for signals

## Agreement Analysis

- States: FULL_BULLISH_ALIGNMENT, FULL_BEARISH_ALIGNMENT, HIGHER_TF_BULLISH_LOWER_TF_PULLBACK,
  HIGHER_TF_BEARISH_LOWER_TF_REBOUND, MIXED_STRUCTURE, INSUFFICIENT
- Unavailable timeframes = neutral (NOT bearish)
- Partial bar = not used for confirmed signal
- `training_only=True`, `no_auto_trade=True`

## Conflict Detection

- 14 conflict types
- All conflicts: auto_block=False, auto_decision=False, auto_trade=False
- Status: NEEDS_REVIEW only

## Bar Aggregation

Source M1 bars → 5m, 20m, 60m buckets:
- open=first, high=max, low=min, close=last, volume=sum, amount=sum
- source="AGGREGATED_FROM_M1"
- Incomplete group → is_partial=True, qualification=PARTIAL_OBSERVATION
- D1 aggregation from intraday: INVALID (raises exception)

## Store Layout

```
data/replay_timeframes/
  timeframe_snapshots.jsonl       # per-TF snapshots
  multi_snapshots.jsonl           # full MTF snapshots
  alignment_results.jsonl         # alignment engine output
  timeframe_agreements.jsonl      # agreement analysis
  timeframe_conflicts.jsonl       # conflict records
  timeline_events.jsonl           # 14 event types
  timeframe_state.json            # atomic state (temp+replace)
  timeframe_index.csv             # session index
  timeframe_audit.jsonl           # audit trail
  exports/                        # export directory
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `replay-timeframe-health` | Run all MTF health checks |
| `replay-timeframes` | List timeframes and hierarchy |
| `replay-mtf-session-create` | Create MTF session |
| `replay-mtf-snapshot` | Show current snapshot |
| `replay-mtf-next` | Advance one bar |
| `replay-mtf-previous` | Step back one bar |
| `replay-mtf-jump` | Jump to timestamp |
| `replay-mtf-agreement` | Show agreement analysis |
| `replay-mtf-conflicts` | Show conflict analysis |
| `replay-mtf-list` | List MTF sessions |
| `replay-mtf-summary` | Show summary |
| `replay-mtf-report` | Generate report |
| `replay-mtf-timeline-report` | Generate timeline report |
| `replay-mtf-batch-preview` | Preview batch (default) |
| `replay-mtf-batch-run` | Run batch (--execute --allow-write required) |
| `replay-mtf-firewall-check` | Check firewall stats |
| `replay-mtf-pit-check` | Check point-in-time integrity |
| `replay-mtf-compare` | Compare sessions (no future reveal) |
| `replay-mtf-store-check` | Validate store integrity |

## Safety Invariants

- `NO_REAL_ORDERS = True` on all MTF modules
- `RESEARCH_ONLY = True` on all MTF modules
- `NO_AUTO_TRADE = True` on agreement module
- `NO_AUTO_BLOCK = True` on conflict module
- `DEFAULT_PREVIEW_MODE = True` on batch runner
- No broker connection, no order submission
