# Replay Session Checkpoints and Fork Workflow — v1.2.1

> [!] Research Only. No Real Orders. Checkpoints NEVER store future data. Fork NEVER copies future data. Not Investment Advice.

## Overview

Checkpoints and forks are the two main tools for exploring multiple decision paths within a single replay session.

- **Checkpoint**: A point-in-time snapshot of session state. Used to save progress, compare states over time, or as a starting point for a fork.
- **Fork**: Creates a new session branching off from an existing session at its current state (or a specified checkpoint). The fork gets a new session_id.

## Checkpoints

### What is a Checkpoint?

A checkpoint captures:
- Current session state (`status`, `current_date`, `current_index`, `total_steps`, `qualification`)
- Decision count and annotation count at that point
- PIT (point-in-time) verification status
- Warning count
- A researcher note

### What a Checkpoint DOES NOT Store

The following fields are explicitly FORBIDDEN from checkpoints:

```
future_return, outcome, final_label, answer,
realized_pnl, broker, order_token, api_key, secret
```

These are stripped before writing. A checkpoint reflects only what was known at `replay_date`.

### Checkpoint IDs

Checkpoints use the `RCP-` prefix (e.g., `RCP-AABBCCDDEE00`).

### Creating a Checkpoint

```bash
python main.py replay-session-checkpoint \
  --session-id RPL-2454-20250101-ABC123 \
  --note "Before testing breakout entry"
```

### Listing Checkpoints

```bash
python main.py replay-session-checkpoints --session-id RPL-2454-20250101-ABC123
```

### Programmatic

```python
from replay.session_checkpoint import ReplayCheckpointManager
from replay.replay_session_store import ReplaySessionStore

store = ReplaySessionStore(repo_root=".")
cp_mgr = ReplayCheckpointManager(store=store, repo_root=".")

cp = cp_mgr.create_checkpoint("RPL-2454-20250101-ABC123", note="Day 5 state")
print(cp.checkpoint_id)  # RCP-XXXX...

checkpoints = cp_mgr.list_checkpoints("RPL-2454-20250101-ABC123")
```

### Restore

Restore creates a **new state revision** — it does NOT overwrite the append-only history.

```python
cp_mgr.restore_checkpoint(checkpoint_id, session_id)
```

## Forks

### What is a Fork?

A fork creates a **new session** branching from an existing one. This allows you to:
- Test different decision paths from the same starting point
- Compare "what if I had done X instead of Y at day N"
- Study the same scenario with different entry/exit strategies

Forks ALWAYS:
- Create a new `session_id`
- Set status to `CREATED`
- Remove future data fields from the starting state
- Record lineage: `relation_type = FORK` or `FORK_FROM_CHECKPOINT`

### Forking the Current State

```bash
python main.py replay-session-fork \
  --session-id RPL-2454-20250101-ABC123 \
  --name "Alternative entry strategy"
```

### Forking from a Checkpoint

```bash
python main.py replay-session-fork \
  --session-id RPL-2454-20250101-ABC123 \
  --checkpoint-id RCP-AABBCCDDEE00 \
  --name "From checkpoint: try different exit"
```

### What Fork NEVER Copies

- `future_return`
- `realized_pnl`
- `outcome`
- `final_label`

### Programmatic

```python
from replay.session_manager import ReplaySessionManager

mgr = ReplaySessionManager(repo_root=".")
forked = mgr.fork_session(
    "RPL-2454-20250101-ABC123",
    checkpoint_id="RCP-AABBCCDDEE00",
    new_name="Alt path from checkpoint 5"
)
print(forked.session_id)  # new RPL-... ID
```

## Session Lineage

Every forked session is tracked in the lineage system.

```bash
python main.py replay-session-lineage --session-id RPL-2454-FORK-XXXX
```

Output shows:
- Root session
- Parent session
- Relation type (FORK / FORK_FROM_CHECKPOINT / DUPLICATE / IMPORTED)
- Lineage depth
- Children sessions

### Cycle Detection

The lineage manager detects cycles (A → B → A) and returns a WARN status. Cycles do not crash the system.

## Session Comparison

After forking, compare two sessions to analyze decision differences:

```bash
python main.py replay-session-compare \
  --session-id-a RPL-2454-20250101-ABC123 \
  --session-id-b RPL-2454-FORK-XXXX
```

### What Comparison Shows

- Config comparison: same symbol, same scenario, same date range
- Progress comparison: current index, total steps, completion %
- Decision comparison: action distribution, count, confidence
- Annotation comparison: annotation counts by type
- PIT status: point_in_time_verified flag
- Qualification comparison
- Warning count comparison

### What Comparison NEVER Shows

- `realized_return`
- `future_return`
- `hindsight_score`
- `final_result`
- `future_max_gain`
- `future_max_loss`

These are completely forbidden from comparison output.

## Typical Workflow

```
1. Create session from scenario
   python main.py replay-session-create-from-scenario --scenario-id RSC-BUILTIN-PULLBACK-001 --stock 2454

2. Step through replay (using existing v1.2.0 commands)
   python main.py replay-next --session-id SESSION_ID

3. Create checkpoint at key decision point
   python main.py replay-session-checkpoint --session-id SESSION_ID --note "Breakout attempt day 8"

4. Continue stepping and make decision A

5. Fork from the checkpoint to try decision B
   python main.py replay-session-fork --session-id SESSION_ID --checkpoint-id CHECKPOINT_ID --name "Try sell instead"

6. Compare the two paths
   python main.py replay-session-compare --session-id-a SESSION_ID --session-id-b FORK_SESSION_ID

7. View lineage to understand the full session tree
   python main.py replay-session-lineage --session-id SESSION_ID
```

## Safety Notes

- Checkpoints are point-in-time only — no future data
- Forks are research tools only — NOT trading strategies
- Session comparison is for studying decision process only
- No real orders are placed at any step
- All sessions are simulation only
