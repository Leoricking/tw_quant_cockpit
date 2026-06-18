# Replay Training Capability Matrix v1.2.9

> **[!] Research Only. No Real Orders. Not Investment Advice.**
> **[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.**

---

## Overview

This document describes all 16 capabilities certified in the Replay Training Stable
Rollup (v1.2.9). Every capability carries `safety_qualified=True` and
`research_only=True`. No capability enables real order execution, broker
connectivity, or automated trading decisions.

---

## Capability Matrix

| # | Capability ID | Module | Introduced | Status | CLI Available | GUI Available | Report | Backward Compat |
|---|--------------|--------|-----------|--------|---------------|---------------|--------|-----------------|
| 1 | replay_session_step | replay_foundation | v1.2.0 | STABLE | Yes | Yes | Yes | Yes |
| 2 | scenario_library | scenario_manager | v1.2.1 | STABLE | Yes | Yes | Yes | Yes |
| 3 | session_fork_checkpoint | session_manager | v1.2.1 | STABLE | Yes | Yes | Yes | Yes |
| 4 | decision_journal | decision_journal | v1.2.2 | STABLE | Yes | Yes | Yes | Yes |
| 5 | process_outcome_scoring | scoring_mistake_taxonomy | v1.2.3 | STABLE | Yes | Yes | Yes | Yes |
| 6 | mistake_taxonomy | scoring_mistake_taxonomy | v1.2.3 | STABLE | Yes | Yes | Yes | Yes |
| 7 | strategy_replay | strategy_knowledge | v1.2.4 | STABLE | Yes | Yes | Yes | Yes |
| 8 | multi_timeframe_sync | multi_timeframe | v1.2.5 | STABLE | Yes | Yes | Yes | Yes |
| 9 | review_queue | review_dashboard | v1.2.6 | STABLE | Yes | Yes | Yes | Yes |
| 10 | challenge_mode | challenge_mode | v1.2.7 | STABLE | Yes | Yes | Yes | Yes |
| 11 | challenge_personal_leaderboard | challenge_mode | v1.2.7 | STABLE | Yes | Yes | No | Yes |
| 12 | dataset_registry | dataset_registry | v1.2.8 | STABLE | Yes | Yes | Yes | Yes |
| 13 | session_registry | session_registry | v1.2.8 | STABLE | Yes | Yes | Yes | Yes |
| 14 | stable_health_check | stable_rollup | v1.2.9 | STABLE | Yes | Yes | Yes | N/A |
| 15 | stable_manifest | stable_rollup | v1.2.9 | STABLE | Yes | Yes | Yes | N/A |
| 16 | capability_matrix | stable_rollup | v1.2.9 | STABLE | Yes | Yes | Yes | N/A |

All 16 capabilities: `safety_qualified = True`, `research_only = True`, `no_real_orders = True`.

---

## Capability Details

### 1. replay_session_step

- **Module:** `replay.replay_schema` / `replay.replay_foundation`
- **Introduced:** v1.2.0
- **Description:** Core bar-by-bar step engine for replay sessions. Enforces
  the future data firewall — no future OHLCV or annotations visible to the
  trader during a session.
- **Health Command:** `replay-health`
- **Safety Notes:** Future data firewall is a hard invariant. FAIL if future
  fields are accessible before the current bar.

### 2. scenario_library

- **Module:** `replay.scenario_schema` / `replay.scenario_manager`
- **Introduced:** v1.2.1
- **Description:** Library of named replay scenarios. Supports templates,
  tags, and scenario metadata. Scenarios hold only historical reference data
  (no live prices).
- **Health Command:** `replay-scenario-health`

### 3. session_fork_checkpoint

- **Module:** `replay.session_schema` / `replay.session_manager`
- **Introduced:** v1.2.1
- **Description:** Fork and checkpoint mechanism for replay sessions. Allows
  branching a session at any bar to explore alternative decision paths.
  Checkpoints are immutable once written.
- **Health Command:** `replay-session-health`

### 4. decision_journal

- **Module:** `replay.decision_journal_schema` / `replay.decision_journal`
- **Introduced:** v1.2.2
- **Description:** Append-only decision journal. Records trader rationale,
  emotional state, and decision metadata at each bar step. No auto-write —
  all journal entries require explicit user action.
- **Health Command:** `replay-journal-health`
- **Safety Notes:** Journal is append-only (no delete, no auto-modify).
  `AUTO_REPLAY_DECISION_ENABLED = False` enforced.

### 5. process_outcome_scoring

- **Module:** `replay.scoring_schema`
- **Introduced:** v1.2.3
- **Description:** Two-dimensional scoring: process score (decision quality
  independent of outcome) and outcome score (realized result). Process and
  outcome are stored separately and must never be conflated.
- **Health Command:** `replay-scoring-health`
- **Safety Notes:** Outcome fields (realized_return, future_return,
  realized_pnl) are blocked from process scoring. Separation is a contract
  invariant.

### 6. mistake_taxonomy

- **Module:** `replay.scoring_schema` / `replay.mistake_taxonomy`
- **Introduced:** v1.2.3
- **Description:** 31-type mistake taxonomy for classifying decision errors.
  Used in post-review annotation. No auto-classification — all taxonomy
  labels require explicit user assignment.
- **Health Command:** `replay-scoring-health`
- **Safety Notes:** `AUTO_MISTAKE_CONFIRMATION_ENABLED = False`.

### 7. strategy_replay

- **Module:** `replay.strategy_knowledge_schema`
- **Introduced:** v1.2.4
- **Description:** Point-in-time strategy knowledge replay. Strategy rules
  are replayed as they existed on the session start date — no future strategy
  changes visible. Prevents look-ahead bias in strategy self-assessment.
- **Health Command:** `replay-strategy-health`
- **Safety Notes:** `AUTO_STRATEGY_CHANGE_ENABLED = False`.
  Point-in-time integrity is a hard invariant.

### 8. multi_timeframe_sync

- **Module:** `replay.multi_timeframe_schema`
- **Introduced:** v1.2.5
- **Description:** Synchronized D1/M60/M20/M5/M1 multi-timeframe replay.
  All timeframes advance together — no timeframe can show bars ahead of the
  session current_date. Partial bars are handled correctly.
- **Health Command:** `replay-multitf-health`
- **Safety Notes:** Timeframe future firewall is a hard invariant across all
  5 timeframes.

### 9. review_queue

- **Module:** `replay.review_schema`
- **Introduced:** v1.2.6
- **Description:** Review queue and progress dashboard for completed replay
  sessions. Supports session comparison across multiple replay runs of the
  same scenario.
- **Health Command:** `replay-review-health`

### 10. challenge_mode

- **Module:** `replay.challenge_schema`
- **Introduced:** v1.2.7
- **Description:** Timed challenge mode with hidden outcome. Outcome is
  revealed only after challenge completion — no auto-reveal. Supports
  per-scenario challenge configuration.
- **Health Command:** `replay-challenge-health`
- **Safety Notes:** `AUTO_OUTCOME_REVEAL_ENABLED = False`.
  Hidden outcome integrity is a hard invariant.

### 11. challenge_personal_leaderboard

- **Module:** `replay.challenge_schema`
- **Introduced:** v1.2.7
- **Description:** Personal (local) leaderboard for challenge scores. No
  network submission, no public leaderboard. All scores stored locally only.
- **Health Command:** `replay-challenge-health`
- **Safety Notes:** No network calls from leaderboard code.

### 12. dataset_registry

- **Module:** `replay.dataset_registry_schema`
- **Introduced:** v1.2.8
- **Description:** Dataset versioning with fingerprint and lineage tracking.
  Each dataset version has a SHA-256 fingerprint. Lineage records derivation
  chain. No auto-repair of dataset integrity issues.
- **Health Command:** `replay-dataset-health`
- **Safety Notes:** `AUTO_DATASET_REPAIR_ENABLED = False`.

### 13. session_registry

- **Module:** `replay.session_registry_schema`
- **Introduced:** v1.2.8
- **Description:** Session registry with portable session packages. Sessions
  can be exported to zip packages and imported on another machine. No
  auto-rebind of session paths.
- **Health Command:** `replay-registry-health`
- **Safety Notes:** `AUTO_SESSION_REBIND_ENABLED = False`.

### 14. stable_health_check

- **Module:** `replay.stable_health`
- **Introduced:** v1.2.9
- **Description:** Comprehensive 44+ point health check covering all 12
  replay training modules, safety invariants, data integrity checks,
  auto-action guards, broker/execution guards, and runtime hygiene.
- **Health Command:** `replay-stable-health`
- **Safety Notes:** FAIL count > 0 → exit 1 in CI mode.

### 15. stable_manifest

- **Module:** `replay.stable_manifest`
- **Introduced:** v1.2.9
- **Description:** Release manifest for the complete v1.2 Replay Training
  line. Lists all 12 modules, 16 capabilities, 24 CLI commands, 10 store
  paths, backward compatibility range (v1.2.0–v1.2.8), and safety flags.
- **Health Command:** `replay-stable-manifest`

### 16. capability_matrix

- **Module:** `replay.stable_capability_matrix`
- **Introduced:** v1.2.9
- **Description:** Machine-readable capability matrix for the v1.2 line.
  Used by health checks, release gate, and documentation generation.
  All 16 capabilities have `safety_qualified=True`.
- **Health Command:** `replay-stable-capabilities`

---

## Safety Qualifications

Every capability in this matrix has been validated against the following
safety invariants:

| Invariant | Status |
|-----------|--------|
| NO_REAL_ORDERS = True | ENFORCED |
| REAL_ORDERS_ENABLED = False | ENFORCED |
| BROKER_EXECUTION_ENABLED = False | ENFORCED |
| PRODUCTION_TRADING_BLOCKED = True | ENFORCED |
| AUTO_REPLAY_DECISION_ENABLED = False | ENFORCED |
| AUTO_REPLAY_EXECUTION_ENABLED = False | ENFORCED |
| AUTO_MISTAKE_CONFIRMATION_ENABLED = False | ENFORCED |
| AUTO_OUTCOME_REVEAL_ENABLED = False | ENFORCED |
| AUTO_STRATEGY_CHANGE_ENABLED = False | ENFORCED |
| AUTO_DATASET_REPAIR_ENABLED = False | ENFORCED |
| AUTO_SESSION_REBIND_ENABLED = False | ENFORCED |
| REPLAY_TRADE_EXECUTION_ENABLED = False | ENFORCED |

---

## CLI Quick Reference

```
replay-stable-health          — Full health check (44+ points, FAIL > 0 → exit 1)
replay-stable-summary         — Summary dict
replay-stable-manifest        — Release manifest
replay-stable-capabilities    — Capability matrix (this document in machine form)
replay-stable-contracts       — Cross-module contract checks
replay-stable-compatibility   — Backward compat v1.2.0–v1.2.8
replay-stable-store-audit     — 10 data store audits
replay-stable-runtime-audit   — Runtime isolation checks
replay-stable-cli-audit       — CLI command registration audit
replay-stable-gui-audit       — GUI panel import audit
replay-stable-report-audit    — Report generator audit
replay-stable-safety-audit    — Safety flag and keyword scan
replay-stable-regression-audit — Regression suite audit
replay-stable-report          — Generate stable rollup report
```

---

*[!] Research Only. No Real Orders. Not Investment Advice.*
