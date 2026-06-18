# Partial Bar Protection & Future Data Firewall v1.2.5

> [!] Research Only. No Real Orders. Not Investment Advice.

## Partial Bar Protection

A partial bar is a bar that has not yet closed at the current replay_timestamp.

### Qualification Levels

| State | Qualification | Use |
|-------|--------------|-----|
| Bar closed before replay_timestamp | CONFIRMED | Safe for indicator calculation |
| Bar opened but not yet closed | PARTIAL_OBSERVATION | Display only, not for signals |
| No data available | UNAVAILABLE | Neutral in agreement |

### Key Rules

1. **Partial bar NEVER used for confirmed signals**
2. **Partial bar close is not a confirmed close**: `confirmed_close=False`
3. **Partial bar breakout is not confirmed**: `confirmed_breakout=False`
4. **Indicators are calculated on completed bars only** (`_filter_completed()`)
5. **Partial bar `visible_ohlcv()`** is used for display only

### Partial Bar Aggregation

When aggregating 1m → 5m/20m/60m and the final group is incomplete:
- `is_partial=True`
- `qualification=PARTIAL_OBSERVATION`
- Not included in confirmed signal calculations

## Future Data Firewall

`MultiTimeframeFutureDataFirewall` runs on all bars before display or calculation.

### Checks Performed (in order)

1. **Timestamp check**: `bar.timestamp > replay_timestamp` → BLOCKED
2. **Available-at check**: `bar.available_at > replay_timestamp` → BLOCKED
3. **Incomplete close leak**: Bar marked as complete but has no valid close → BLOCKED
4. **Daily close leak**: Daily bar with `available_at` in future → BLOCKED
5. **Aggregation leak**: Aggregated bar using future source bars → BLOCKED
6. **Indicator leak**: Indicator calculated with future bars → BLOCKED
7. **Strategy leak**: Strategy output containing future fields → BLOCKED

### Forbidden Fields

These fields are stripped from all bars before storage and display:

```
outcome, forward_return, realized_pnl, hindsight_score,
final_session_high, final_session_low, future_high, future_low,
next_day_open, next_day_close, final_result, future_max_gain,
future_max_loss
```

### Per-Snapshot Counters

The firewall tracks per-session:
- `future_rows_blocked`
- `incomplete_bars_blocked`
- `daily_close_leaks_blocked`
- `aggregation_leaks_blocked`
- `indicator_leaks_blocked`
- `strategy_leaks_blocked`

Use `replay-mtf-firewall-check` CLI command to view stats.

## Point-in-Time Verifier

`MultiTimeframePointInTimeVerifier` performs independent verification per timeframe.

### Verification Steps

1. `verify_bar()` — checks timestamp and available_at against replay_timestamp
2. `verify_snapshot()` — per-TF snapshot integrity
3. `verify_multi_snapshot()` — full MTF snapshot
4. `verify_indicator_inputs()` — no future bars used in indicator window
5. `verify_strategy_inputs()` — no forward-return fields in strategy context
6. `verify_source_available_at()` — source data not from future
7. `verify_parent_child_boundary()` — parent TF bar not ahead of child clock
8. `verify_partial_status()` — partial bar correctly marked

### Failure Behavior

- One TF fails verification → that TF is BLOCKED for that snapshot
- Optional TF failure → does not block overall session
- All failures logged with evidence
- No silent suppression

## Safety Flags

All MTF modules carry these module-level constants:

```python
NO_REAL_ORDERS = True
RESEARCH_ONLY = True
NO_BFILL = True  # on alignment engine
NO_CENTERED_ROLLING = True  # on indicator engine
NO_FUTURE_NEAREST = True  # on alignment engine
NO_AUTO_TRADE = True  # on agreement analyzer
NO_AUTO_BLOCK = True  # on conflict analyzer
DEFAULT_PREVIEW_MODE = True  # on batch runner
```
