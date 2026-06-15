# Replay Scenario & Session Manager — v1.2.1

> [!] Research Only. No Real Orders. Scenario templates NEVER contain future answers. Not Investment Advice.

## Overview

v1.2.1 introduces a complete scenario template library and structured session lifecycle manager built on top of the v1.2.0 Replay Training UX Foundation.

Key capabilities:
- 6 builtin scenario templates (pullback, breakout, bottom reversal, no-chase, risk control, free practice)
- Full session lifecycle: create from scenario, search, filter, archive, restore, fork, duplicate
- Session checkpoints (point-in-time snapshots, no future data)
- Session lineage tracking (root/fork/duplicate/imported relations)
- Session comparison (decision process only, NO future performance)
- Batch session creation with preview/dry-run default
- Portable session metadata for cross-machine use

## Architecture

```
replay/
  scenario_schema.py       — ReplayScenarioTemplate, ReplayScenarioInstance, ScenarioValidationResult
  scenario_store.py        — ScenarioTemplateStore (JSONL + JSON atomic)
  scenario_library.py      — ReplayScenarioLibrary (CRUD + builtins + validate + export/import)
  scenario_validator.py    — ReplayScenarioValidator
  scenario_query.py        — ReplayScenarioQuery (filter/search/stats)
  session_manager.py       — ReplaySessionManager (lifecycle)
  session_manager_health.py — ReplayScenarioSessionManagerHealthCheck
  session_checkpoint.py    — ReplayCheckpoint, ReplayCheckpointManager
  session_lineage.py       — ReplaySessionLineage, ReplaySessionLineageManager
  session_comparator.py    — ReplaySessionComparator (process only, no performance)
  session_portability.py   — ReplaySessionPortability (path normalization, export/import)
  session_registry.py      — ReplaySessionRegistry (index)
  batch_session_builder.py — ReplayBatchSessionBuilder (preview/dry-run default)
  templates/               — 6 builtin JSON templates
```

## ID Prefixes

| Type | Prefix | Example |
|------|--------|---------|
| Scenario template | RSC- | RSC-BUILTIN-PULLBACK-001 |
| Scenario instance | RSI- | RSI-A1B2C3D4 |
| Checkpoint | RCP- | RCP-AABBCCDDEE00 |
| Session | RPL- | RPL-2454-20250101120000-AB1234 |

## Builtin Scenario Templates

| ID | Name | Category | Difficulty |
|----|------|----------|------------|
| RSC-BUILTIN-FREE-PRACTICE-001 | Free Practice | FREE_PRACTICE | BEGINNER |
| RSC-BUILTIN-PULLBACK-001 | Pullback Training | PULLBACK | INTERMEDIATE |
| RSC-BUILTIN-BREAKOUT-001 | Breakout Training | BREAKOUT | INTERMEDIATE |
| RSC-BUILTIN-BOTTOM-REVERSAL-001 | Bottom Reversal Training | BOTTOM_REVERSAL | ADVANCED |
| RSC-BUILTIN-NO-CHASE-001 | No Chase Training | NO_CHASE | INTERMEDIATE |
| RSC-BUILTIN-RISK-CONTROL-001 | Risk Control Training | RISK_CONTROL | BEGINNER |

## CLI Quick Reference

```bash
# Health
python main.py replay-scenario-health

# List / search scenarios
python main.py replay-scenarios
python main.py replay-scenario-search --query "pullback"
python main.py replay-scenario-show --scenario-id RSC-BUILTIN-PULLBACK-001
python main.py replay-scenario-validate --scenario-id RSC-BUILTIN-PULLBACK-001

# Create session from scenario
python main.py replay-session-create-from-scenario --scenario-id RSC-BUILTIN-FREE-PRACTICE-001 --stock 2454

# Search sessions
python main.py replay-session-search --query "2454"

# Checkpoint
python main.py replay-session-checkpoint --session-id SESSION_ID --note "before big decision"
python main.py replay-session-checkpoints --session-id SESSION_ID

# Fork
python main.py replay-session-fork --session-id SESSION_ID --name "Alternative path"

# Compare
python main.py replay-session-compare --session-id-a SESSION_A --session-id-b SESSION_B

# Lineage
python main.py replay-session-lineage --session-id SESSION_ID

# Batch
python main.py replay-batch-preview --scenario-id RSC-BUILTIN-FREE-PRACTICE-001 --symbols 2454,2330,2345
python main.py replay-batch-create --scenario-id RSC-BUILTIN-FREE-PRACTICE-001 --symbols 2454,2330 --allow-write
```

## Safety Guards

### Scenario template guards
- `archived=True` → BLOCKED from instantiation. Must `replay-scenario-restore` first.
- Forbidden fields blocked at validation: `future_return`, `outcome`, `final_label`, `answer`, `realized_pnl`, `broker`, `order_token`, `api_key`, `secret`
- `strict_future_firewall=False` → validation error (all templates require this True)
- Duplicate scenario ID on new create: guarded by store

### Checkpoint guards
- Forbidden fields removed from snapshot: `future_return`, `outcome`, `final_label`, `answer`, `realized_pnl`, `broker`, `order_token`, `api_key`, `secret`
- Restore creates new state revision; append-only history NOT overwritten

### Fork guards
- Fork always creates new `session_id`
- Future data fields removed from fork state: `future_return`, `realized_pnl`, `outcome`, `final_label`

### Session comparison guards
- FORBIDDEN in output: `realized_return`, `future_return`, `hindsight_score`, `final_result`, `future_max_gain`, `future_max_loss`
- Comparison covers: config, progress, decision count/actions, confidence, annotations, PIT status, qualification, warning counts

### Batch guards
- `allow_write=False` (default) → BLOCKED — preview only
- Hard limit: 500 sessions
- Default max: 50 sessions

### Session archive guards
- `ARCHIVED` sessions are immutable
- Must call `restore_session()` before resuming

## v1.2.0 Backward Compatibility

- All v1.2.0 sessions (RPL- prefix, JSONL store) are fully readable by v1.2.1
- v1.2.0 sessions without lineage records: lineage read returns None (not an error)
- `portable_metadata_version=1` field added to new sessions; absent from v1.2.0 sessions (treated as version 0)

## Safety Constants

```
REPLAY_TRADE_EXECUTION_ENABLED    = False
REPLAY_AUTO_EXECUTION_ENABLED     = False
REPLAY_AUTO_DECISION_ENABLED      = False
REPLAY_AUTO_SCORING_ENABLED       = False
REPLAY_SCENARIO_LIBRARY_AVAILABLE = True
REPLAY_SESSION_MANAGER_AVAILABLE  = True
REPLAY_CHECKPOINT_AVAILABLE       = True
REPLAY_SESSION_FORK_AVAILABLE     = True
REPLAY_SESSION_COMPARE_AVAILABLE  = True
REPLAY_BATCH_SESSION_CREATION_AVAILABLE = True
NO_REAL_ORDERS                    = True
PRODUCTION_TRADING_BLOCKED        = True
```
