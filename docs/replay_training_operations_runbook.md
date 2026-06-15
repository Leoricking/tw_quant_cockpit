# Replay Training Operations Runbook — v1.2.0

> [!] Research Only. No Real Orders. Replay Training Only.

## Health Check

Run before starting any replay session:

```bash
python main.py replay-health
```

Expected: 8/8 checks PASS. Any FAIL should be investigated before proceeding.

## Starting a Session

### Step 1: Choose a symbol and date range

Pick a symbol that has imported daily data, and a historical date range. The longer the range, the more training steps available.

### Step 2: Create the session

```bash
python main.py replay-create --stock 2330 --start 2023-01-01 --end 2023-12-31 --name "2330 Training Jan-Dec 2023"
```

Note the session ID printed (format: `RPL-{symbol}-{date}-{rand4}`).

### Step 3: Verify the session

```bash
python main.py replay-sessions
python main.py replay-session --session-id <YOUR_SESSION_ID>
```

## Navigating the Timeline

### Step forward one day
```bash
python main.py replay-next --session-id <ID>
```

### Step backward one day
```bash
python main.py replay-previous --session-id <ID>
```

### Jump to a specific date
```bash
python main.py replay-jump --session-id <ID> --date 2023-06-01
```
If the date is not a trading day, the firewall normalizes to the nearest previous trading day.

### View current snapshot
```bash
python main.py replay-current --session-id <ID>
```

### Check progress
```bash
python main.py replay-summary --session-id <ID>
```

## Recording Decisions

At each replay step, record what you would do at that point in time:

```bash
python main.py replay-decision --session-id <ID> \
  --action WATCH \
  --confidence 50 \
  --reason "Volume below MA5; waiting for confirmation"
```

Available actions: `WATCH`, `WAIT`, `ENTER`, `ADD`, `HOLD`, `REDUCE`, `EXIT`, `STOP`, `SKIP`

**All decisions are simulation-only.** No order is placed. The decision records your analysis for review.

## Adding Annotations

Annotate observations, support/resistance levels, or learning notes:

```bash
python main.py replay-annotation --session-id <ID> \
  --type SUPPORT \
  --title "Key support zone" \
  --content "240-245 area acted as strong support in previous 3 weeks"
```

Annotation types: `SUPPORT`, `RESISTANCE`, `OBSERVATION`, `SETUP`, `LESSON`

## Pausing and Resuming

```bash
# Pause
python main.py replay-pause --session-id <ID>

# Resume later
python main.py replay-resume --session-id <ID>
```

## Checking Data Integrity

```bash
# Check that no future data has leaked into current snapshot
python main.py replay-firewall-check --session-id <ID>

# Check point-in-time indicator verification
python main.py replay-point-in-time-check --session-id <ID>
```

Both should report `PIT Verified: True` and `Is Clean: True`.

## Generating Reports

```bash
# Full session report (saved to reports/ directory)
python main.py replay-report --session-id <ID>
```

The report includes 9 sections:
1. Session Overview
2. Timeline Progress
3. Market Snapshots
4. Decisions Log
5. Annotations
6. Action Distribution
7. Firewall Status
8. Data Availability Summary
9. Safety Checklist

**Note:** Reports do NOT include realized returns, future max gain/loss, accuracy scores, or hindsight metrics. Research Only.

## Session Lifecycle Operations

### Duplicate a session (for A/B comparison)
```bash
python main.py replay-duplicate --session-id <ID> --name "2330 Training — Alt Approach"
```
Creates a new session with the same config but a new session ID.

### Archive a completed session (immutable)
```bash
python main.py replay-archive --session-id <ID>
```
Archived sessions cannot be modified. Use for completed training records.

## Troubleshooting

### "jump failed" / "next failed"

If timeline navigation returns an error, check:
1. Is the session status PLAYING or PAUSED?
2. Does real data exist for the symbol (run `replay-current` to check availability)?
3. For real mode: verify the data import for the symbol is complete.

For mock mode sessions, navigation should always work (synthetic dates are generated).

### "No real price data" warning

This is informational. The session continues in DEMO_ONLY qualification mode. To train with real data, import daily CSV data for the symbol and create a new session.

### Corrupted session store

If you see JSONL parse errors, the store's corrupted-tail tolerance will skip the bad line and continue. The session state JSON is atomic-written and separate from JSONL logs, so state is not lost.

## Data Storage

All session data is stored under `data/replay_sessions/` (gitignored). This directory is **never committed** to the repository.

Directory structure:
```
data/replay_sessions/
  RPL-2330-20230101-XXXX/
    state.json          (atomic session state)
    decisions.jsonl     (append-only decision log)
    events.jsonl        (append-only event log)
    annotations.jsonl   (append-only annotation log)
```

## Safety Summary

- All decisions: `simulation_decision_only=True`
- No real orders: `no_real_orders=True`  
- No future data: firewall enforced at data layer
- No production stores modified: all writes go to `data/replay_sessions/`
- Mock data: always DEMO_ONLY qualification

---
[!] Research Only. No Real Orders. Not Investment Advice.
