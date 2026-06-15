# Replay Future Data Firewall — v1.2.0

> [!] Research Only. No Real Orders.

## Purpose

The Future Data Firewall prevents any forward-looking data from leaking into a replay training session. In a historical replay, a researcher should only see what was knowable on the replay date — not what happened afterward.

## What the Firewall Blocks

### Forbidden Fields (exact match)
- `forward_return`
- `future_return`
- `future_high`
- `future_low`
- `outcome`
- `final_label`
- `target_label`
- `realized_pnl`
- `next_close`
- `next_open`
- `future_signal`
- `hindsight_score`

### Forbidden Prefixes (prefix match)
- `forward_return_*` — blocks `forward_return_1`, `forward_return_5`, `forward_return_20`, etc.

### Date-Based Blocking

For daily price/volume data: any row with a date **after** the current replay date is excluded.

For fundamental data: quarterly report data is only shown after the announcement date (`announce_date` column). If no announcement date is present, the data is excluded.

## Firewall Implementation

The firewall lives in `replay/future_data_firewall.py` and provides:

| Method | Description |
|--------|-------------|
| `filter_dataframe(df, replay_date)` | Remove rows with date > replay_date |
| `filter_by_announcement_date(df, replay_date)` | Fundamental PIT filter |
| `validate_frame(df)` | Raise ValueError if forbidden columns present |
| `detect_future_rows(df, replay_date)` | Count future rows without removing |
| `sanitize_context(context_dict, replay_date)` | Filter a context dictionary |
| `verify_snapshot(snapshot)` | Verify a ReplayMarketSnapshot is clean |
| `future_field_scan(df)` | Return list of forbidden columns found |
| `build_firewall_report(df, replay_date)` | Generate a firewall status dict |

## CLI Verification

```bash
# Check firewall status for current replay date
python main.py replay-firewall-check --session-id RPL-2330-20230101-XXXX
```

Output shows:
- `Is Clean: True/False`
- `Future Data Blocked: N` (count of blocked fields)
- `PIT Verified: True/False`
- List of any issues found

## Point-In-Time Context Builder

The `PointInTimeReplayContextBuilder` in `replay/point_in_time_context.py` computes all technical indicators using only data available on or before the replay date:

| Indicator | Method |
|-----------|--------|
| MA5, MA10, MA20, MA60 | Rolling mean, min_periods=1 |
| Volume MA5 | Rolling mean on volume |
| KD (K, D) | EWM-based stochastic |
| MACD (macd, signal, histogram) | EWM-based |
| RSI | EWM-based relative strength |
| ATR | EWM-based average true range |
| Rolling High/Low (20-day) | Rolling max/min |

All rolling computations use `center=False` and do not fill forward across gaps.

## Health Check

The firewall is verified during `replay-health`:

```
[PASS] future_firewall: Blocked ['forward_return_5', 'future_high']: 2 forbidden fields
[PASS] date_navigation: previous at first day: changed=False
```

---
[!] Research Only. No Real Orders. Not Investment Advice.
