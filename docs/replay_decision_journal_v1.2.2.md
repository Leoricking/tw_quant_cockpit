# Replay Decision Journal v1.2.2

> **[!] Research Only. No Real Orders. Simulation Decision Only.**
> **[!] No performance metrics. No hindsight. No future data.**
> **[!] Not Investment Advice. Broker Disabled.**

## Overview

The Decision Journal is a structured system for capturing, revising, and reviewing
trading decisions made during replay simulation sessions. It is a training tool only.

Key features:

- **Trade Thesis Capture** — setup type, time horizon, key levels, invalidation
- **Risk Plan Capture** — stop type, target type, position sizing notes
- **Emotional State Capture** — self-reported 0-100 sliders, primary emotion, bias flags
- **Discipline Checklists** — 23 standard items across 5 categories
- **Append-Only Revisions** — DREV- prefixed records, original never modified
- **Session/Scenario Linkage** — entries link to replay sessions and checkpoints
- **Export/Import with Dry-Run Guard** — dry_run=True by default
- **Reports** — per-session detail report and period summary report

## ID Conventions

| Prefix | Meaning |
|--------|---------|
| `DJR-` | Decision Journal Entry |
| `DREV-` | Decision Revision Record |

## Entry Lifecycle

```
create_entry → DRAFT
record_entry → RECORDED
revise_entry → creates DREV- + marks REVISED
archive_entry → ARCHIVED (immutable)
restore_entry → RECORDED
hide_entry → hidden=True (not deleted)
```

Archived entries are immutable. No revision is permitted on an ARCHIVED entry.

## Forbidden Fields

These fields are **never stored, exported, compared, or summarized**:

- `realized_return`, `future_return`, `hindsight_score`, `final_result`
- `future_max_gain`, `future_max_loss`
- `win_rate`, `return_rate`, `pnl`, `accuracy`, `alpha`, `sharpe`

Any attempt to include these fields raises `ValueError`.

## Emotional State

- Self-reported only. NOT a psychological assessment.
- Levels: `confidence_level`, `anxiety_level`, `focus_level` — each 0-100.
- Values outside 0-100 raise `ValueError`.
- `self_reported: true` is an invariant.

## Cognitive Bias Flags

- Only flags from `CognitiveBiasRegistry.KNOWN_BIASES` are accepted.
- Unknown bias names raise `ValueError`.
- 17 known biases defined (FOMO, REVENGE_TRADING, CONFIRMATION_BIAS, etc.).

## Discipline Checklist

Standard 23-item checklist:

| Category | Items |
|----------|-------|
| DATA | 4 items |
| SETUP | 4 items |
| RISK | 5 items |
| EMOTION | 5 items |
| DISCIPLINE | 5 items |

Required items must all pass before `all_required_passed=True`.

## Import Guard

Import requires **both** conditions to be true:

- `dry_run=False`
- `allow_write=True`

Default behavior is `dry_run=True`, which returns `status="dry_run"` without writing.

## Storage

Data is stored in `data/replay_journal/`:

- `journal_entries.jsonl` — append-only entry log
- `journal_revisions.jsonl` — append-only revision log
- `journal_links.jsonl` — session/scenario/checkpoint links
- `journal_emotional_states.jsonl` — emotional state records
- `journal_checklists.jsonl` — checklist results
- `journal_index.csv` — deduplicated index (rebuilt on demand)

Corrupted tail lines in JSONL files are skipped gracefully.

## CLI Commands

```bash
python main.py replay-journal-health
python main.py replay-journal-create --action BUY --symbol AAPL --date 2026-06-10
python main.py replay-journal-entry --id DJR-20260610-XXXX
python main.py replay-journal-list --session RPL-SESSION-ID
python main.py replay-journal-finalize --id DJR-20260610-XXXX
python main.py replay-journal-revise --id DJR-20260610-XXXX --reason "..." --field confidence --value 60
python main.py replay-journal-archive --id DJR-20260610-XXXX
python main.py replay-journal-export --session RPL-SESSION-ID
python main.py replay-journal-import --file export.json --execute
python main.py replay-journal-report --session RPL-SESSION-ID
python main.py replay-journal-summary-report --from 2026-06-01 --to 2026-06-16
```

## Safety Flags

```python
NO_REAL_ORDERS = True
RESEARCH_ONLY = True
simulation_only = True  # enforced on every entry
DECISION_AUTO_SCORING_ENABLED = False
DECISION_AUTO_GENERATION_ENABLED = False
DECISION_AUTO_EXECUTION_ENABLED = False
REPLAY_TRADE_EXECUTION_ENABLED = False
```

## Version History

| Version | Description |
|---------|-------------|
| v1.2.2 | Decision Journal Integration (this release) |
| v1.2.1 | Replay Scenario & Session Manager |
| v1.2.0 | Research Run Registry |
