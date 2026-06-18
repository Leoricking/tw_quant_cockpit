# Timeframe Alignment Rules v1.2.5

> [!] Research Only. No Real Orders. Not Investment Advice.

## Core Rules

### 1. Past-Only Asof Join
All bar lookups use past-only asof join (no bfill, no nearest-future):
- Only bars with `timestamp <= replay_timestamp` are returned
- `available_at <= replay_timestamp` is also enforced
- Result: always the most recent completed bar before the replay timestamp

### 2. No Backfill (NO_BFILL)
- Missing values are left as None/NaN — never filled forward or backward
- `NO_BFILL = True` on `TimeframeAlignmentEngine`

### 3. No Centered Rolling (NO_CENTERED_ROLLING)
- All rolling calculations use `min_periods`, never centered window
- `NO_CENTERED_ROLLING = True` on `MultiTimeframeIndicatorEngine`

### 4. No Future Nearest (NO_FUTURE_NEAREST)
- nearest() lookups never return a bar from after replay_timestamp
- `NO_FUTURE_NEAREST = True` on `TimeframeAlignmentEngine`

## Alignment Engine Methods

### latest_completed_bar(symbol, timeframe, replay_timestamp)
- Returns the most recent bar with `timestamp <= replay_timestamp` AND bar is complete
- Partial bar at replay boundary: returned separately as current_partial_bar
- Returns None if no completed bar available

### current_partial_bar(symbol, timeframe, replay_timestamp)
- Returns the in-progress bar at replay_timestamp (if any)
- Qualification: PARTIAL_OBSERVATION
- Never used for confirmed signals

### detect_lookahead(bars, replay_timestamp)
- Returns list of bars with timestamp > replay_timestamp
- Used by firewall for violation reporting

## Hierarchy Rules

```
D1 (Daily — highest)
  └─ M60 (60-minute)
       └─ M20 (20-minute)
            └─ M5 (5-minute — primary default)
                 └─ M1 (1-minute — trigger default)
```

- Higher TF provides fundamental/sector context
- Lower TF provides trigger/entry timing
- M1 missing → trigger_timeframe falls back to M5 (explicit, logged, no fake M1)

## Taiwan Market Calendar

- Trading hours: 09:00–13:30 Asia/Taipei
- Trading days: Mon–Fri excluding Taiwan public holidays
- Pre-market, after-hours, odd-lots, night session: NOT_SUPPORTED_V1_2_5

## Stale Timeframe Detection

A timeframe is considered stale if its latest completed bar is older than:
- D1: > 1 trading day
- M60: > 2 hours during session
- M20: > 40 minutes during session
- M5: > 10 minutes during session
- M1: > 2 minutes during session

Stale timeframes are marked STALE (not BEARISH) in agreement analysis.
