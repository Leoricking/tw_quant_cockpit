# Release Notes — v1.2.x: Replay Training Series

> [!] Research Only. No Real Orders. Not Investment Advice.

---

## v1.2.2 — Decision Journal Integration

> [!] Research Only. No Real Orders. Simulation Decision Only. Not Investment Advice.

### Overview

v1.2.2 adds a comprehensive Decision Journal system to the Replay Training module.
Researchers can capture trade theses, risk plans, emotional states, discipline
checklists, and append-only decision revisions — all linked to replay sessions,
scenarios, and checkpoints. No performance metrics, no hindsight data, no real orders.

### What's New

#### Decision Journal Core (`replay/decision_journal_schema.py`, `decision_journal_store.py`, `decision_journal_manager.py`, `decision_journal_query.py`)

- DJR- prefixed journal entries, DREV- prefixed revisions
- Append-only JSONL storage in `data/replay_journal/`
- Corrupted-tail graceful recovery
- Entry lifecycle: DRAFT → RECORDED → REVISED → ARCHIVED → restored
- Archived entries are immutable (revision blocked with ValueError)
- import_entry requires dry_run=False AND allow_write=True

#### Trade Thesis & Risk Plan (`replay/decision_journal_schema.py`)

- TradeThesis: setup_type, time_horizon, key_levels, invalidation, entry_trigger
- RiskPlan: stop_type, target_type, stop_notes, target_notes, position_size_notes, exit_rules

#### Emotional State Capture (`replay/emotional_state.py`)

- Self-reported only — NOT a psychological assessment
- Sliders: confidence_level, anxiety_level, focus_level — each 0-100 (out-of-range raises ValueError)
- 12 primary emotions; self_reported=True invariant

#### Cognitive Bias Registry (`replay/cognitive_bias.py`)

- 17 known biases (FOMO, REVENGE_TRADING, CONFIRMATION_BIAS, etc.)
- Unknown bias names raise ValueError

#### Discipline Checklist (`replay/discipline_checklist.py`)

- 23 standard items across 5 categories: DATA, SETUP, RISK, EMOTION, DISCIPLINE
- Required items tracked; all_required_passed flag

#### Decision Comparator (`replay/decision_comparator.py`)

- Side-by-side entry comparison with forbidden field enforcement
- Forbidden fields raise ValueError; render_markdown output shows NOT_QUALIFIED

#### Summary Builder (`replay/decision_journal_summary.py`)

- Allowed stats: entry_count, status counts, action/setup distributions, confidence buckets, revision_frequency
- Forbidden stats raise ValueError

#### Portability (`replay/decision_journal_portability.py`)

- dry_run=True by default
- import_entries requires dry_run=False AND allow_write=True
- Strips api_key, secret, broker, realized_return, future_return, hindsight_score from export
- validate_import_file rejects forbidden fields before any write

#### Templates (`replay/decision_templates.py`, `replay/journal_templates/*.json`)

- 8 templates: free_form, breakout, pullback, bottom_reversal, no_chase, risk_reduction, exit_review, wait_confirmation
- All have simulation_only=True

#### GUI Panels (`gui/replay_decision_journal_panel.py`, `gui/replay_*`)

- ReplayDecisionJournalPanel with QThread for data loading
- Safety banner: "RESEARCH ONLY | SIMULATION DECISION ONLY — NO ORDER WILL BE SENT"
- 7 buttons: New, View/Edit, Revise, Archive, Export, Import (Dry Run), Refresh
- Headless stubs when PyQt5 unavailable

#### Reports (`reports/replay_decision_journal_report.py`, `reports/replay_decision_journal_summary_report.py`)

- Per-session detail report: Overview, Timeline, Revision History, Safety Declaration
- Period summary report: Status/Action/Setup/Confidence distributions, Revision stats, Completeness

### CLI Commands (25 new)

| Command | Description |
|---------|-------------|
| `replay-journal-health` | Health check for decision journal |
| `replay-journal-create` | Create new journal entry (DRAFT) |
| `replay-journal-entry` | Show entry detail |
| `replay-journal-list` | List entries (with optional filters) |
| `replay-journal-search` | Full-text search entries |
| `replay-journal-filter` | Filter by status/action/setup/emotion |
| `replay-journal-thesis` | Add trade thesis to entry |
| `replay-journal-risk` | Add risk plan to entry |
| `replay-journal-emotion` | Record emotional state |
| `replay-journal-checklist` | Run discipline checklist |
| `replay-journal-check-item` | Check individual item |
| `replay-journal-finalize` | Finalize entry (RECORDED) |
| `replay-journal-revise` | Create append-only revision (DREV-) |
| `replay-journal-revisions` | List revisions for entry |
| `replay-journal-compare` | Compare two entries (no perf data) |
| `replay-journal-archive` | Archive entry (immutable) |
| `replay-journal-restore` | Restore archived entry |
| `replay-journal-hide` | Hide entry from view (not deleted) |
| `replay-journal-export` | Export session metadata (no forbidden fields) |
| `replay-journal-export-session` | Export all entries for session |
| `replay-journal-import` | Import (dry-run by default; --execute + --allow-write to write) |
| `replay-journal-summary` | Session summary (no perf stats) |
| `replay-journal-session-summary` | Alias for replay-journal-summary |
| `replay-journal-report` | Generate per-session detail report |
| `replay-journal-summary-report` | Generate period summary report |

### Backward Compatibility

`ReplayDecision` schema updated with new optional fields, all defaulting safely:

- `journal_entry_id: Optional[str] = None`
- `thesis_id: Optional[str] = None`
- `risk_plan_id: Optional[str] = None`
- `emotional_state_id: Optional[str] = None`
- `checklist_ids: List[str] = []`
- `revision_count: int = 0`
- `latest_revision_id: Optional[str] = None`
- `simulation_only: bool = True`

Old v1.2.1 session data loads without error.

### Safety Invariants

- `DECISION_AUTO_SCORING_ENABLED = False`
- `DECISION_AUTO_GENERATION_ENABLED = False`
- `DECISION_AUTO_EXECUTION_ENABLED = False`
- `REPLAY_TRADE_EXECUTION_ENABLED = False`
- Forbidden fields: realized_return, future_return, hindsight_score, final_result
- Forbidden summary stats: win_rate, pnl, alpha, sharpe, accuracy
- Archived entries immutable — revision raises ValueError
- Import requires dry_run=False AND allow_write=True
- Emotional state: self_reported=True invariant; 0-100 range enforced
- Cognitive bias: only KNOWN_BIASES accepted
- No Real Orders. No Broker Connection.

### Regression Tests

- `tests/test_replay_decision_journal_regression.py` — 24 test cases
- `tests/fixtures/replay_journal/` — 24 fixture files

### Documentation

- `docs/replay_decision_journal_v1.2.2.md`
- `docs/replay_decision_journal_templates.md`
- `docs/replay_discipline_and_emotion_guide.md`

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

## v1.2.3 — Replay Scoring & Mistake Taxonomy

> [!] Research Only. No Real Orders. Scoring NEVER triggers paper orders or broker execution.
> [!] Process scores use NO future data, NO outcome, NO PnL. Outcome reveal EXPLICIT ONLY.
> [!] Mistake detection SUGGESTED status only. System cannot auto-confirm mistakes.
> [!] Not Investment Advice.

### Overview

v1.2.3 adds complete process and outcome scoring with strict separation, explicit outcome
reveal, composite classification, explainable mistake taxonomy and review, plan adherence
evaluation, confidence handling, GUI and CLI review workflows, reports, and regression coverage.

### Core Modules

- `replay/scoring_schema.py` — ScoreComponent, ReplayProcessScore, ReplayOutcomeScore, ReplayCompositeScore, MistakeRecord, MistakeReviewRecord, OutcomeRevealRecord
- `replay/process_score_engine.py` — 11-dimension process score; no future data
- `replay/outcome_score_engine.py` — outcome score after explicit reveal
- `replay/composite_score_engine.py` — process+outcome composite; PROCESS_ONLY default
- `replay/score_confidence.py` — DEMO_ONLY / INSUFFICIENT / OBSERVATIONAL / RELIABLE
- `replay/score_explainer.py` — human-readable score explanations
- `replay/outcome_reveal.py` — explicit reveal workflow; default BLOCKED
- `replay/plan_adherence.py` — pre-session plan vs. actual decisions
- `replay/mistake_taxonomy.py` — 31 mistake types across 6 categories
- `replay/mistake_detector.py` — SUGGESTED-only detection; never auto-confirms
- `replay/mistake_review.py` — USER-only confirmation; SYSTEM_REVIEW blocked
- `replay/scoring_store.py` — append-only JSONL store; corrupted line tolerance
- `replay/scoring_query.py` — query by session, symbol, scenario
- `replay/scoring_summary.py` — aggregate scoring summary
- `replay/scoring_health.py` — health check with 13 invariant checks

### Reports

- `reports/replay_scoring_report.py`
- `reports/replay_mistake_taxonomy_report.py`
- `reports/replay_scoring_summary_report.py`

### GUI Panels

- `gui/replay_scoring_panel.py`
- `gui/replay_scoring_adapter.py`
- `gui/replay_process_score_detail_dialog.py`
- `gui/replay_outcome_reveal_dialog.py`
- `gui/replay_outcome_score_dialog.py`
- `gui/replay_composite_score_dialog.py`
- `gui/replay_mistake_review_dialog.py`
- `gui/replay_plan_adherence_dialog.py`

### CLI Commands (23 new commands)

```
replay-scoring-health, replay-score-process, replay-score-process-detail,
replay-outcome-preview, replay-outcome-reveal, replay-score-outcome,
replay-score-composite, replay-mistakes-detect, replay-mistakes,
replay-mistake, replay-mistake-confirm, replay-mistake-dismiss,
replay-mistake-override, replay-mistake-reopen, replay-plan-adherence,
replay-scoring-summary, replay-scoring-session-summary,
replay-scoring-symbol-summary, replay-scoring-scenario-summary,
replay-scoring-report, replay-mistake-report
```

### Safety Invariants

- `SCORING_TRIGGERS_NO_ORDERS = True`
- `AUTO_OUTCOME_REVEAL_ENABLED = False`
- `AUTO_MISTAKE_CONFIRMATION_ENABLED = False`
- `AUTO_SCORE_TO_TRADE_ENABLED = False`
- `REPLAY_TRADE_EXECUTION_ENABLED = False`
- All mistakes start as `SUGGESTED` — system never auto-confirms
- `original_snapshot_unchanged = True` — reveal never modifies session
- Process score forbidden fields enforced: no `realized_pnl`, `future_return`, etc.

### Documentation

- `docs/replay_scoring_mistake_taxonomy_v1.2.3.md`
- `docs/replay_process_vs_outcome_scoring.md`
- `docs/replay_mistake_taxonomy_guide.md`
- `docs/replay_outcome_reveal_and_review.md`

---

## v1.2.6 — Replay Review Dashboard

### Overview

Adds a comprehensive review dashboard for completed replay sessions. Separates process quality
from outcome quality. Outcome is hidden by default and requires explicit user reveal.

### New Files

**replay/ (22 files)**

- `review_dashboard_schema.py` — Dataclasses with enums and safety invariants
- `review_dashboard_adapter.py` — Module adapter with safe_unavailable() fallback
- `review_dashboard_engine.py` — Engine: build_global_dashboard(), build_session_dashboard()
- `review_dashboard_cards.py` — Score cards; outcome/composite HIDDEN until revealed
- `review_dashboard_tables.py` — Paginated tables with sort/filter
- `review_dashboard_charts.py` — Charts with process_outcome_separated=True
- `review_queue.py` — Queue with complete() that does NOT auto-confirm or auto-reveal
- `review_progress.py` — 8 required + 4 optional steps; OUTCOME_REVEAL_REQUIRED=False
- `review_checklist.py` — Checklist with NO_AUTO_COMPLETE for 4 manual items
- `review_notes.py` — Append-only notes (APPEND_ONLY=True)
- `review_tags.py` — Tags (TAG_AFFECTS_SCORE=False, TAG_AFFECTS_TRADING=False)
- `review_search.py`, `review_filters.py`, `review_sorting.py`, `review_grouping.py`
- `review_comparator.py` — NOT_AVAILABLE sentinel for unrevealed outcomes
- `review_batch.py` — DEFAULT_PREVIEW_MODE=True; BLOCKED without --execute --allow-write
- `review_store.py` — Append-only JSONL; atomic write via .tmp + os.replace()
- `review_query.py`, `review_summary.py`, `review_report.py`
- `review_health.py` — 30+ health checks; run() returns Dict[str, Tuple[str, str]]

**reports/ (3 files)**

- `replay_review_dashboard_report.py`
- `replay_review_summary_report.py`
- `replay_review_queue_report.py`

**gui/ (17 files)**

- `replay_review_dashboard.py` — Main dashboard widget (framework-agnostic)
- 16 panel stub files with RESEARCH_ONLY=True

**tests/ (27 fixtures + 1 regression file)**

- `tests/fixtures/replay_review/` — 25 JSON + 2 JSONL fixtures
- `tests/test_replay_review_dashboard_regression.py`

**docs/ (3 files)**

- `docs/replay_review_dashboard_v1.2.6.md`
- `docs/replay_review_workflow.md`
- `docs/replay_review_queue_and_progress.md`

### CLI Commands (30+)

```
replay-review-health, replay-review-dashboard, replay-review-session,
replay-review-session-detail, replay-review-queue, replay-review-start,
replay-review-complete, replay-review-dismiss, replay-review-reopen,
replay-review-progress, replay-review-checklist, replay-review-note,
replay-review-tag, replay-review-tags, replay-review-search,
replay-review-filter, replay-review-compare-sessions,
replay-review-compare-symbols, replay-review-compare-scenarios,
replay-review-summary, replay-review-symbol-summary,
replay-review-scenario-summary, replay-review-report,
replay-review-summary-report, replay-review-queue-report,
replay-review-batch-preview, replay-review-batch-run
```

### Safety Invariants

- `AUTO_REVIEW_COMPLETE_ENABLED = False`
- `AUTO_OUTCOME_REVEAL_ENABLED = False`
- `AUTO_MISTAKE_CONFIRMATION_ENABLED = False`
- `AUTO_SCORE_TO_TRADE_ENABLED = False`
- `REPLAY_TRADE_EXECUTION_ENABLED = False`
- complete() does NOT auto-confirm mistakes or auto-reveal outcomes
- Outcome hidden in to_dict() when outcome_revealed=False
- Batch default preview mode; execute requires --execute --allow-write
- Missing modules return UNAVAILABLE (no crash)
- Append-only JSONL stores; atomic state write via .tmp + os.replace()
- PROCESS_REVIEW_COMPLETE does NOT require Outcome Reveal
- outcome_reveal_required = False always

### Documentation

- `docs/replay_review_dashboard_v1.2.6.md`
- `docs/replay_review_workflow.md`
- `docs/replay_review_queue_and_progress.md`

---

## v1.2.7 — Replay Challenge Mode

**Challenge Training Only. No Real Orders. Not Investment Advice.**

### Features

- Structured scored challenge scenarios wrapping existing replay infrastructure
- 12 built-in challenge templates (BEGINNER through EXPERT)
- 5 difficulty levels; all difficulty levels keep Future Firewall active
- Process-weighted scoring: 35% Process Quality + 15% Discipline + 15% Risk Planning + 10% Info + 10% Strategy + 10% MTF + 5% Timing
- Outcome weight capped at 20%; process weight always >= outcome weight
- Hidden data guard: 20 forbidden fields blocked from active payload
- Deterministic seed: same seed + source_id + data_version = same challenge
- Outcome reveal requires both --reveal AND --confirm-review; no auto-reveal
- All mistakes SUGGESTED only — never auto-Confirmed
- Timeout marks status only — never executes decision
- Local personal leaderboard only; no public leaderboard; no network submission
- Answer Key stored separately from active payload
- 57 health checks (30 component + 27 safety invariant checks)
- 9 new governance alerts (P0/P1)
- 33 new CLI commands (replay-challenge-*)
- Batch guard: requires --execute AND --allow-write; preview by default
- Missing modules show UNAVAILABLE; no crash

### Safety Invariants

- `REPLAY_CHALLENGE_MODE_AVAILABLE = True`
- `PUBLIC_LEADERBOARD_ENABLED = False`
- `NETWORK_SCORE_SUBMISSION_ENABLED = False`
- `AUTO_CHALLENGE_DECISION_ENABLED = False`
- `AUTO_CHALLENGE_OUTCOME_REVEAL_ENABLED = False`
- `AUTO_CHALLENGE_MISTAKE_CONFIRMATION_ENABLED = False`
- Future firewall active at all difficulty levels
- Answer Key stored separately (ACTIVE_AND_ANSWER_KEY_SEPARATED = True)
- Timeout never executes decision (TIMEOUT_EXECUTES_DECISION = False)

### Documentation

- `docs/replay_challenge_mode_v1.2.7.md`
- `docs/replay_challenge_hidden_data_rules.md`
- `docs/replay_challenge_scoring.md`

---

## v1.2.8 — Replay Dataset & Session Registry

**Research Only. No Real Orders. Dataset Registry Only. No Broker.**

### Features

- Complete Replay Dataset Catalog, Registry, Manifest, Versioning, Fingerprint, Lineage, Qualification, Snapshot, Freeze, Validator, Integrity, Portability, Package, Import/Export, Path Remap, Conflict Detection
- Session Registry with Dataset Bindings, Fingerprint, Lineage
- Deterministic path-independent fingerprints (SHA-256; excludes absolute paths, machine names, timestamps)
- Frozen datasets immutable — hash mismatch after freeze → CORRUPTED
- RELATIVE_ONLY path mode for portable packages
- Dataset qualification levels: VERIFIED_REAL, REAL_UNVERIFIED, MOCK_DEMO_ONLY, INSUFFICIENT, BLOCKED, INCOMPATIBLE
- Session status: ACTIVE, PAUSED, COMPLETED, ARCHIVED, ORPHANED, BLOCKED, INSUFFICIENT
- Append-only JSONL storage with graceful corrupted-tail handling
- Session-Dataset binding locked after session creation; COMPLETED sessions cannot be directly rebound
- Mock datasets can never be VERIFIED_REAL; real datasets with mock contamination → BLOCKED
- Package never contains secrets, .env, API tokens, broker credentials, absolute paths
- Registry Repair: preview by default; execute requires --allow-write
- ~50 registry health checks
- 35 new CLI commands (replay-registry-*, replay-dataset-*, replay-session-*, replay-package-*)
- 17 new GUI panels and dialogs
- 4 new report types
- 27 test fixtures

### Safety Invariants

- `NO_REAL_ORDERS = True` throughout all modules
- `RESEARCH_ONLY = True` throughout all modules
- `AUTO_DATASET_OVERWRITE_ENABLED = False`
- `AUTO_DATASET_REPAIR_ENABLED = False`
- `AUTO_SESSION_REBIND_ENABLED = False`
- `AUTO_PACKAGE_IMPORT_ENABLED = False`
- `AUTO_REGISTRY_CONFLICT_RESOLUTION_ENABLED = False`
- `AUTO_REGISTRY_REPAIR_ENABLED = False`

### Documentation

- `docs/replay_dataset_session_registry_v1.2.8.md`
- `docs/replay_dataset_versioning_and_lineage.md`
- `docs/replay_portable_package_and_path_remap.md`

---
[!] Research Only. No Real Orders. Not Investment Advice.
