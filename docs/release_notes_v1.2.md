# Release Notes — v1.2.x: Replay Training Series

> [!] Research Only. No Real Orders. Not Investment Advice.

---

## v1.2.1 — Replay Scenario & Session Manager

> [!] Research Only. No Real Orders. Scenario templates NEVER contain future answers. Not Investment Advice.

### Overview

v1.2.1 builds on v1.2.0 to add a structured scenario template library, full session lifecycle management (search, filter, archive, restore, fork, clone), session checkpoints, session lineage tracking, session comparison (process only — no future performance), batch session creation, and portable session metadata. All guards from v1.2.0 are preserved and extended.

### What's New

#### Scenario Template Library (`replay/scenario_schema.py`, `scenario_store.py`, `scenario_library.py`, `scenario_validator.py`, `scenario_query.py`)

- 6 builtin templates loaded from `replay/templates/`: free_practice, pullback_training, breakout_training, bottom_reversal_training, no_chase_training, risk_control_training
- Scenario IDs use RSC- prefix; instances use RSI- prefix
- `archived=True` scenarios BLOCKED from instantiation (must restore first)
- Template validation blocks: forbidden fields (future_return, outcome, final_label, answer, realized_pnl, broker, order_token, api_key, secret), invalid dates, strict_future_firewall=False
- Duplicate detection by name+category before creation

#### Session Manager (`replay/session_manager.py`, `session_manager_health.py`)

- `create_from_scenario()` — Create session from template; archived scenarios BLOCKED
- `search_sessions()`, `filter_sessions()` — Query by symbol, scenario, status, tag, date range
- `fork_session()` — Always creates new session_id; NEVER copies future data
- `duplicate_session()` — New session_id, CREATED status
- `archive_session()` — Immutable; `restore_session()` to re-enable
- `delete_from_view()` — Sets hidden=True only; does NOT delete audit record

#### Session Checkpoints (`replay/session_checkpoint.py`)

- RCP- prefix for checkpoint IDs
- Checkpoint stores only data at `replay_date` — NO future data
- Forbidden fields blocked: future_return, outcome, final_label, answer, realized_pnl, broker, order_token, api_key, secret
- `restore_checkpoint()` creates new state revision; does NOT overwrite append-only history

#### Session Lineage (`replay/session_lineage.py`)

- Tracks ROOT, DUPLICATE, FORK, FORK_FROM_CHECKPOINT, RESTORED, IMPORTED, ORPHAN_IMPORTED
- Cycle detection — no circular parent chains
- Missing parent: WARN, don't crash
- `root_session_id` is stable across forks

#### Session Comparison (`replay/session_comparator.py`)

- Compares: config, progress, decision process, annotations, PIT status, warning counts, qualification
- FORBIDDEN in output: realized_return, future_return, hindsight_score, final_result, future_max_gain, future_max_loss
- This compares decision process and session state ONLY, NOT performance

#### Batch Session Builder (`replay/batch_session_builder.py`)

- Default: preview/dry-run only
- `allow_write=True` required to create sessions
- Default max 50, hard limit 500
- Does NOT auto-play, auto-decide, auto-score, auto-execute, auto-download

#### Session Portability & Registry (`replay/session_portability.py`, `session_registry.py`)

- `portable_metadata_version=1` field for cross-machine compatibility
- Path normalization for Windows/Unix portability
- Session registry with session_id index

### CLI Commands (19 new)

| Command | Description |
|---------|-------------|
| `replay-scenario-health` | Health check for scenario & session manager |
| `replay-session-manager-health` | Alias for replay-scenario-health |
| `replay-scenarios` | List all active scenario templates |
| `replay-scenario-search` | Search/filter scenario templates |
| `replay-scenario-show` | Show template detail |
| `replay-scenario-validate` | Validate a template |
| `replay-scenario-create` | Create new template |
| `replay-scenario-archive` | Archive template (blocks instantiation) |
| `replay-scenario-restore` | Restore archived template |
| `replay-scenario-duplicate` | Duplicate template with new ID |
| `replay-session-create-from-scenario` | Create session from template |
| `replay-session-search` | Search/filter sessions |
| `replay-session-checkpoint` | Create a checkpoint (no future data) |
| `replay-session-checkpoints` | List checkpoints |
| `replay-session-fork` | Fork session (new ID, no future data) |
| `replay-session-compare` | Compare two sessions (no performance data) |
| `replay-session-lineage` | Show session lineage tree |
| `replay-batch-preview` | Preview batch session creation (dry-run) |
| `replay-batch-create` | Batch create sessions (--allow-write required) |

### Safety Invariants

- `REPLAY_TRADE_EXECUTION_ENABLED = False`
- `REPLAY_AUTO_EXECUTION_ENABLED = False`
- `REPLAY_AUTO_DECISION_ENABLED = False`
- `REPLAY_AUTO_SCORING_ENABLED = False`
- Scenario templates NEVER contain: future answers, realized returns, future labels
- Checkpoints NEVER store: future_return, outcome, final_label, answer, realized_pnl
- Fork NEVER copies future data
- Session comparison NEVER shows: realized_return, future_return, hindsight_score
- Batch execution BLOCKED without explicit --allow-write
- Archived scenario BLOCKED from instantiation until restored
- No Real Orders. No Broker Connection. Production Trading BLOCKED.

---

## v1.2.0 — Replay Training UX Foundation

> [!] Research Only. No Real Orders. Not Investment Advice.

### Overview

v1.2.0 introduces the **Replay Training UX Foundation**, a complete day-by-day historical replay system for structured training on past TW market data. Researchers can step through a historical period, record simulation decisions at each step, annotate observations, and build a structured training record — all protected by a strict future data firewall.

## What's New

### Replay Training Module (`replay/`)

New files added alongside the existing v0.4.4 intraday replay components:

- **`replay_schema.py`** — 6 dataclasses: `ReplaySessionConfig`, `ReplaySessionState`, `ReplayMarketSnapshot`, `ReplayDecision`, `ReplayEvent`, `ReplayAnnotation`
- **`replay_calendar.py`** — `ReplayTradingCalendar` built from actual imported CSV data
- **`replay_data_source.py`** — Point-in-time data loading with strict real/mock separation
- **`future_data_firewall.py`** — Blocks all forward-return, future_high, hindsight_score fields
- **`point_in_time_context.py`** — Computes MA/KD/MACD/RSI/ATR using only data ≤ replay date
- **`replay_timeline.py`** — Date navigation with edge-case guards (no crash at first/last day)
- **`replay_session_store.py`** — Append-only JSONL + atomic JSON session store
- **`replay_training_session.py`** — Session lifecycle (create/open/archive/duplicate)
- **`replay_training_engine.py`** — Main orchestration engine
- **`replay_decision.py`** — Decision capture with `SIMULATION_DECISION_ONLY=True` invariant
- **`replay_annotations.py`** — Annotation management (hidden=True for audit-safe removal)
- **`replay_summary.py`** — Session summary without future performance data
- **`replay_query.py`** — Query interface for sessions, decisions, annotations
- **`replay_health.py`** — 8-check health verification

### GUI Additions (`gui/`)

- **`replay_session_dialog.py`** — PySide6 dialog for creating replay sessions
- **`replay_decision_dialog.py`** — PySide6 dialog with prominent "SIMULATION DECISION ONLY — NO ORDER WILL BE SENT" safety banner

### Reports (`reports/`)

- **`replay_training_session_report.py`** — 9-section Markdown report builder

### CLI Commands (19 new commands)

```
replay-health, replay-create, replay-sessions, replay-session, replay-resume,
replay-current, replay-next, replay-previous, replay-jump, replay-play-step,
replay-pause, replay-decision, replay-annotation, replay-summary, replay-report,
replay-duplicate, replay-archive, replay-firewall-check, replay-point-in-time-check
```

### Test Fixtures (`tests/fixtures/replay/`)

17 fixture files covering: valid daily data, future-field-contaminated data, chips, fundamentals, non-trading date normalization, session configs, decisions, annotations, store JSONL (including corrupted-tail tolerance test).

### Regression Test Suite

- `tests/test_replay_training_foundation_regression.py` — 9 test classes, fixed clock at 2023-06-15

### Governance & Infrastructure Updates

- **`governance_alerts/alert_policy.py`** — 5 new replay alert types (REPLAY_FUTURE_DATA_LEAK_DETECTED at P0, etc.)
- **`gui/navigation/tab_registry.py`** — "Replay Training" tab registered with all 14 CLI commands
- **`regression/suite_registry.py`** — 3 new regression entries (QUICK, FULL, RELEASE_GATE suites)
- **`.gitignore`** — `data/replay_sessions/` excluded; fixture files exempted

### Version Info (`release/version_info.py`)

- VERSION: `1.1.9` → `1.2.0`
- RELEASE_NAME: "Data Governance Stable Rollup" → "Replay Training UX Foundation"
- RELEASE_STAGE: STABLE → FOUNDATION
- RELEASE_TRACK: research → replay_training
- New flags: `REPLAY_TRAINING_AVAILABLE=True`, `REPLAY_FUTURE_DATA_FIREWALL_AVAILABLE=True`, `REPLAY_TRADE_EXECUTION_ENABLED=False`, `REPLAY_AUTO_EXECUTION_ENABLED=False`, `REPLAY_SIMULATION_DECISION_ONLY=True`, `REPLAY_DECISION_CAPTURE_AVAILABLE=True`, `REPLAY_ANNOTATION_AVAILABLE=True`, `REPLAY_REPORT_AVAILABLE=True`

## Safety Invariants (unchanged and new)

All existing safety flags preserved. New flags:
- `REPLAY_TRADE_EXECUTION_ENABLED = False` — replay cannot trigger trades
- `REPLAY_AUTO_EXECUTION_ENABLED = False` — no auto-stepping or auto-decisions
- `REPLAY_SIMULATION_DECISION_ONLY = True` — all decisions are simulation-only

## Known Limitations

- Real-mode sessions require that daily CSV data be imported for the target symbol. Without data, the timeline is empty and navigation returns errors (expected behavior).
- The replay report does not include forward performance data (by design).
- Mock-mode sessions are always DEMO_ONLY and cannot be used for formal research conclusions.

## Documentation Added

- `docs/replay_training_ux_foundation_v1.2.0.md`
- `docs/replay_future_data_firewall.md`
- `docs/replay_training_operations_runbook.md`
- `docs/release_notes_v1.2.md` (this file)

## Base Release

Builds on v1.1.9 Data Governance Stable Rollup. All 1.1.x governance, alerts, registry, and quality gate functionality remains intact.

---
[!] Research Only. No Real Orders. Not Investment Advice.
