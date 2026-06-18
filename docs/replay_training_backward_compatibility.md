# Replay Training Backward Compatibility v1.2.9

> **[!] Research Only. No Real Orders. Not Investment Advice.**
> **[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.**

---

## Overview

This document describes the backward compatibility guarantees for the Replay
Training v1.2 line (v1.2.0–v1.2.9). The guarantees apply to:

- JSONL store format compatibility
- Schema class field compatibility
- CLI command availability
- Safety flag availability and values

Compatibility is verified at v1.2.9 freeze by `ReplayStableCompatibilityChecker`
against fixture-based schema checks for each prior version.

---

## Compatibility Range

| From Version | To Version | Status | Verified By |
|--------------|------------|--------|-------------|
| v1.2.0 | v1.2.9 | COMPATIBLE | ReplayStableCompatibilityChecker |
| v1.2.1 | v1.2.9 | COMPATIBLE | ReplayStableCompatibilityChecker |
| v1.2.2 | v1.2.9 | COMPATIBLE | ReplayStableCompatibilityChecker |
| v1.2.3 | v1.2.9 | COMPATIBLE | ReplayStableCompatibilityChecker |
| v1.2.4 | v1.2.9 | COMPATIBLE | ReplayStableCompatibilityChecker |
| v1.2.5 | v1.2.9 | COMPATIBLE | ReplayStableCompatibilityChecker |
| v1.2.6 | v1.2.9 | COMPATIBLE | ReplayStableCompatibilityChecker |
| v1.2.7 | v1.2.9 | COMPATIBLE | ReplayStableCompatibilityChecker |
| v1.2.8 | v1.2.9 | COMPATIBLE | ReplayStableCompatibilityChecker |

All 9 prior versions pass `check_all()` with status PASS.

---

## Per-Version Compatibility Guarantees

### v1.2.0 — Replay Training UX Foundation

**Schema:** `replay.replay_schema`
**Key Types:** `ReplaySession`, `ReplayBar`, `ReplayStep`

**Guarantees at v1.2.9:**
- `ReplaySession` fields `session_id`, `symbol`, `start_date`, `current_date`,
  `mode`, `no_real_orders`, `research_only` are present and unchanged.
- `ReplayBar` fields `date`, `open`, `high`, `low`, `close`, `volume` are
  present and unchanged.
- `ReplayStep` `step_index`, `bar`, `session_id` are present and unchanged.
- Future data firewall invariant (`current_date` fence) is unchanged.
- JSONL session store format from v1.2.0 is readable without migration.

**Breaking Change Risk:** NONE. Schema is frozen.

---

### v1.2.1 — Replay Scenario & Session Manager

**Schemas:** `replay.scenario_schema`, `replay.session_schema`
**Key Types:** `ReplayScenario`, `ScenarioTemplate`, `ReplaySessionFork`,
`ReplayCheckpoint`

**Guarantees at v1.2.9:**
- `ReplayScenario` fields `scenario_id`, `name`, `symbol`, `start_date`,
  `end_date`, `description`, `tags` are present and unchanged.
- `ReplaySessionFork` `fork_id`, `parent_session_id`, `fork_bar_index` are
  present and unchanged.
- `ReplayCheckpoint` `checkpoint_id`, `session_id`, `bar_index`,
  `no_real_orders` are present and unchanged.
- Session JSONL stores from v1.2.1 are readable without migration.

**Breaking Change Risk:** NONE. Schemas are frozen.

---

### v1.2.2 — Decision Journal Integration

**Schema:** `replay.decision_journal_schema`
**Key Types:** `DecisionJournalEntry`, `EmotionalState`

**Guarantees at v1.2.9:**
- `DecisionJournalEntry` fields `entry_id`, `session_id`, `bar_index`,
  `rationale`, `emotional_state`, `no_real_orders`, `research_only` are
  present and unchanged.
- `EmotionalState` enum values are unchanged.
- Journal is append-only — v1.2.2 entries are readable in v1.2.9.
- `AUTO_REPLAY_DECISION_ENABLED = False` invariant unchanged.

**Breaking Change Risk:** NONE. Schema is frozen.

---

### v1.2.3 — Replay Scoring & Mistake Taxonomy

**Schema:** `replay.scoring_schema`
**Key Types:** `ReplayScore`, `ProcessScore`, `OutcomeScore`, `MistakeEntry`

**Guarantees at v1.2.9:**
- `ReplayScore` fields `score_id`, `session_id`, `process_score`,
  `outcome_score`, `no_real_orders`, `research_only` are present and unchanged.
- Process/outcome separation invariant: `realized_return`, `future_return`,
  `realized_pnl` are not present in `ProcessScore` fields — unchanged.
- 31-type mistake taxonomy type codes are unchanged.
- `AUTO_MISTAKE_CONFIRMATION_ENABLED = False` invariant unchanged.

**Breaking Change Risk:** NONE. Schema is frozen.

---

### v1.2.4 — Strategy Knowledge Replay

**Schema:** `replay.strategy_knowledge_schema`
**Key Types:** `StrategyKnowledgeSnapshot`, `PointInTimeStrategyRule`

**Guarantees at v1.2.9:**
- `StrategyKnowledgeSnapshot` fields `snapshot_id`, `session_id`,
  `snapshot_date`, `rules`, `no_real_orders`, `research_only` are present
  and unchanged.
- Point-in-time integrity: `snapshot_date <= current_date` invariant unchanged.
- `AUTO_STRATEGY_CHANGE_ENABLED = False` invariant unchanged.

**Breaking Change Risk:** NONE. Schema is frozen.

---

### v1.2.5 — Multi-Timeframe Replay

**Schema:** `replay.multi_timeframe_schema`
**Key Types:** `MultiTimeframeSession`, `TimeframeBar`

**Guarantees at v1.2.9:**
- `MultiTimeframeSession` fields `session_id`, `timeframes` (D1, M60, M20,
  M5, M1), `current_date`, `no_real_orders`, `research_only` are present and
  unchanged.
- Timeframe future firewall: no timeframe bar with `date > current_date` is
  accessible — invariant unchanged.
- Partial bar handling rules are unchanged.

**Breaking Change Risk:** NONE. Schema is frozen.

---

### v1.2.6 — Replay Review Dashboard

**Schema:** `replay.review_schema`
**Key Types:** `ReviewQueueEntry`, `ReviewProgress`, `SessionComparison`

**Guarantees at v1.2.9:**
- `ReviewQueueEntry` fields `queue_id`, `session_id`, `status`, `priority`,
  `no_real_orders`, `research_only` are present and unchanged.
- Review queue JSONL store from v1.2.6 is readable without migration.
- Session comparison fields are unchanged.

**Breaking Change Risk:** NONE. Schema is frozen.

---

### v1.2.7 — Replay Challenge Mode

**Schema:** `replay.challenge_schema`
**Key Types:** `ChallengeConfig`, `ChallengeSession`, `LeaderboardEntry`

**Guarantees at v1.2.9:**
- `ChallengeConfig` fields `challenge_id`, `scenario_id`, `time_limit_seconds`,
  `hide_outcome`, `no_real_orders`, `research_only` are present and unchanged.
- Hidden outcome invariant: `outcome_revealed = False` until explicit reveal
  action — unchanged.
- Personal leaderboard is local-only. No network submission — unchanged.
- `AUTO_OUTCOME_REVEAL_ENABLED = False` invariant unchanged.

**Breaking Change Risk:** NONE. Schema is frozen.

---

### v1.2.8 — Replay Dataset & Session Registry

**Schemas:** `replay.dataset_registry_schema`, `replay.session_registry_schema`
**Key Types:** `DatasetVersion`, `DatasetLineage`, `SessionRegistryEntry`,
`SessionPackage`

**Guarantees at v1.2.9:**
- `DatasetVersion` fields `version_id`, `dataset_id`, `fingerprint_sha256`,
  `created_at`, `no_real_orders`, `research_only` are present and unchanged.
- `DatasetLineage` fields `parent_version_id`, `derivation_method` are
  present and unchanged.
- `SessionRegistryEntry` fields `registry_id`, `session_id`, `package_path`,
  `no_real_orders`, `research_only` are present and unchanged.
- Session packages exported at v1.2.8 can be listed by v1.2.9 registry.
- `AUTO_DATASET_REPAIR_ENABLED = False` invariant unchanged.
- `AUTO_SESSION_REBIND_ENABLED = False` invariant unchanged.

**Breaking Change Risk:** NONE. Schemas are frozen.

---

## Store Format Guarantees

All 10 JSONL stores use append-only semantics. Format guarantees:

| Store | Path | Format | Compat |
|-------|------|--------|--------|
| replay_sessions | data/replay_sessions/ | JSONL | v1.2.0+ |
| replay_scenarios | data/replay_scenarios/ | JSONL | v1.2.1+ |
| decision_journal | data/decision_journal/ | JSONL | v1.2.2+ |
| replay_scores | data/replay_scores/ | JSONL | v1.2.3+ |
| mistake_entries | data/mistake_entries/ | JSONL | v1.2.3+ |
| strategy_snapshots | data/strategy_snapshots/ | JSONL | v1.2.4+ |
| multi_timeframe_sessions | data/multi_timeframe_sessions/ | JSONL | v1.2.5+ |
| review_queue | data/review_queue/ | JSONL | v1.2.6+ |
| challenge_sessions | data/challenge_sessions/ | JSONL | v1.2.7+ |
| dataset_registry | data/dataset_registry/ | JSONL | v1.2.8+ |

**Append-Only Contract:** Existing JSONL records are never modified or deleted
by normal application operations. Older records are always valid.

**Unknown Field Policy:** If a record contains fields not recognized by the
current code version, those fields are ignored (forward compatibility). If the
current code version expects a field not present in an older record, a default
value is used (backward compatibility).

---

## Safety Flag Backward Compatibility

The following safety flags have been `False` (disabled) since their introduction
and must remain `False` in all future maintenance releases:

| Flag | Introduced | Value | Frozen |
|------|-----------|-------|--------|
| REAL_ORDERS_ENABLED | v1.2.0 | False | YES |
| BROKER_EXECUTION_ENABLED | v1.2.0 | False | YES |
| AUTO_REPLAY_DECISION_ENABLED | v1.2.2 | False | YES |
| AUTO_REPLAY_EXECUTION_ENABLED | v1.2.2 | False | YES |
| AUTO_MISTAKE_CONFIRMATION_ENABLED | v1.2.3 | False | YES |
| AUTO_OUTCOME_REVEAL_ENABLED | v1.2.7 | False | YES |
| AUTO_STRATEGY_CHANGE_ENABLED | v1.2.4 | False | YES |
| AUTO_DATASET_REPAIR_ENABLED | v1.2.8 | False | YES |
| AUTO_SESSION_REBIND_ENABLED | v1.2.8 | False | YES |
| REPLAY_TRADE_EXECUTION_ENABLED | v1.2.0 | False | YES |

Any change to these flags from `False` to `True` requires a new major version
review and explicit safety documentation.

---

## Compatibility Verification

To verify backward compatibility at any time:

```
python main.py replay-stable-compatibility
```

This runs `ReplayStableCompatibilityChecker.check_all()` against all 9 prior
versions. All should return PASS. A WARN indicates an optional schema class
is not importable (acceptable in minimal environments). A FAIL indicates a
hard invariant violation.

---

*[!] Research Only. No Real Orders. Not Investment Advice.*
