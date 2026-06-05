# TW Quant Cockpit — Strategy Memory UX v0.8.1

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] ACCEPTED = research accepted, not trading enabled. Not Investment Advice.**

---

## Overview

Strategy Memory UX v0.8.1 is a polish release that adds status lifecycle management, actionable UX fields, safe command labelling, and new CLI/GUI views to the Strategy Research Memory system introduced in v0.7.2.

All changes are backward compatible. No existing functionality removed.

---

## New UX Fields on StrategyMemoryItem

| Field | Type | Description |
|-------|------|-------------|
| `display_title` | str | Formatted title for GUI display (truncated to 80 chars) |
| `needs_action` | bool | True for P0/P1 items requiring immediate attention |
| `validation_ready` | bool | True for items in VALIDATING status |
| `status_hint` | str | Human-readable status label |
| `next_step` | str | Suggested safe CLI command |
| `last_action_at` | str | ISO timestamp of last status change |
| `safe_command_count` | int | Number of safe commands available |
| `blocked_command_count` | int | Always 0 — BUY/SELL/ORDER blocked |
| `accepted_is_research_only` | bool | Always True — ACCEPTED ≠ trading enabled |

---

## Status Lifecycle

```
NEW → REVIEWING → VALIDATING → ACCEPTED
                              → REJECTED
                              → NEEDS_MORE_EVIDENCE
* → ARCHIVED (any status)
```

### ACCEPTED Invariant

`accepted_is_research_only` is always `True`, enforced in `__post_init__` and `from_dict`.
It cannot be set to False, even from a CSV file.

**ACCEPTED means:** research finding accepted as valid for further investigation.
**ACCEPTED does NOT mean:** strategy enabled, trade signal generated, real order placed.

---

## New CLI Commands

| Command | Description |
|---------|-------------|
| `python main.py strategy-memory-validation-queue` | Show VALIDATING-status memories ready for decision |
| `python main.py strategy-memory-active-threads` | Show REVIEWING-status active research threads |
| `python main.py strategy-memory-repeated-patterns` | Show memories seen more than once (seen_count > 1) |

### Enhanced Existing Commands

| Command | New Flags |
|---------|-----------|
| `strategy-memory-list` | `--active-only`, `--needs-action`, `--sort`, `--include-archived` |
| `strategy-memory-search` | `--needs-action`, `--source-module`, `--rule`, `--strategy`, `--include-archived` |
| `strategy-memory-summary` | Displays Today Focus, Active Threads, Validation Queue, Repeated Patterns, Needs Action counts |
| `strategy-memory-show` | Displays status_hint, needs_action, validation_ready, links, research-only warning |
| `strategy-memory-update-status` | Explicit 3-line research-only warning block on every call |

---

## New Query Methods

Added to `StrategyMemoryQuery`:

| Method | Description |
|--------|-------------|
| `search_advanced(**kwargs)` | Full filter set: memory_type, status, priority, source_module, rule, strategy, needs_action, include_archived, sort_by |
| `sort_memories(memories, sort_by)` | Sort by: priority, status, last_seen, seen_count |
| `get_validation_queue()` | Return VALIDATING-status memories (store-backed) |
| `get_active_research_threads()` | Return REVIEWING-status memories (store-backed) |
| `get_repeated_patterns()` | Return memories with seen_count > 1 (store-backed) |

---

## Safe Command Labels

`StrategyMemoryAdapter.load_safe_commands()` returns commands with safety labels.
BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE keywords are blocked (never returned).

| Label | Meaning |
|-------|---------|
| `SAFE_READ_ONLY` | Display/list command |
| `SAFE_REPORT` | Report generation |
| `SAFE_REGRESSION` | Regression suite |
| `SAFE_REPLAY` | Replay training |
| `SAFE_DATA_CHECK` | Data coverage check |

---

## Memory Link Improvements

`StrategyMemoryLink` now carries:

| Field | Description |
|-------|-------------|
| `target_title` | Title of the target memory item |
| `why_linked` | Human-readable explanation of the link |
| `suggested_next_step` | Safe CLI command for the next research step |

Duplicate detection is now conservative: similarity > 80% AND same memory_type AND same source_module (Jaccard word-overlap).

---

## Memory Store: Protected Statuses

`upsert_memories()` will not overwrite status for items in:
- `REVIEWING`, `VALIDATING`, `ACCEPTED`, `REJECTED`

This prevents accidental reset of in-progress items during re-extraction.

`update_status()` now:
- Sets `last_action_at` timestamp
- Logs the transition
- Forces `accepted_is_research_only=True` when setting ACCEPTED

---

## Report v0.8.1

10-section Markdown report format:
1. Header
2. Today Memory Focus (top memory + suggested command)
3. Memory Status Board (status counts, ACCEPTED note)
4. Active Research Threads
5. Validation Queue
6. Repeated Patterns
7. Memory Links (with why_linked)
8. Suggested Safe Commands
9. What Not To Do
10. Safety Declaration

---

## GUI Panel v0.8.1

New features in `gui/strategy_memory_panel.py`:

- Safety banner: "ACCEPTED means research accepted, not trading enabled"
- Summary cards: Total, Active, Needs Action, Validation Queue, Repeated, P0, P1, Blocked Cmds
- Source module filter dropdown
- Active-only / Needs-action / Include-archived checkboxes
- Memory table: 10 columns including Needs Action and Validation Ready
- Detail panel: 7 tabs (Summary, Hypothesis, Evidence, Validation, Commands, Links, Safety)
- Commands tab: safe command list with safety labels; BUY/SELL/ORDER blocked
- Links tab: Relation, Source, Target, Why Linked, Next Step
- Safety tab: full research-only declaration
- Status action buttons row: REVIEWING, VALIDATING, NEEDS_MORE_EVIDENCE, ACCEPTED, REJECTED, Archive
- `closeEvent`: QThread cleanup (worker.quit() + worker.wait())

---

## Research Integration

### Research Intelligence (recommendation_engine.py)

`build_recommendations(signals, mode, memory_summary=None)`:
- Extracts keywords from existing memory titles
- P3 recommendations with ≥2 keyword overlap get "(seen)" suffix in rationale
- P0/P1 items are never modified

### Backtest Coach (coach_task_builder.py)

`build_tasks(signals, mode, memory_items=None)`:
- Deduplicates tasks by title+task_type, keeping higher priority
- Computes `related_memory_id` by 2-word overlap with memory items

---

## Regression Coverage

New test cases added to `SUITE_RESEARCH_OS`:

- `strategy_memory_ux_import` — StrategyMemoryPanel import check
- `strategy_memory_ux_summary` — strategy-memory-summary
- `strategy_memory_ux_list_active` — strategy-memory-list --active-only
- `strategy_memory_ux_search_needs_action` — strategy-memory-search --needs-action
- `strategy_memory_ux_validation_queue` — strategy-memory-validation-queue
- `strategy_memory_ux_report` — strategy-memory-report --mode real

Release gate smoke tests:
- `release_gate_strategy_memory_ux_import`
- `release_gate_strategy_memory_ux_summary`

---

## Stable Release Checklist

Three new checks in `stable_release_checklist_v060.py`:

- `strategy_memory_ux_import` — StrategyMemoryPanel import
- `strategy_memory_no_forbidden_commands` — load_safe_commands() BUY/SELL/ORDER guard
- `accepted_is_research_only` — accepted_is_research_only always True

Two new checks in `intelligence_stable_checklist.py`:

- `strategy_memory_ux_safe` — accepted_is_research_only invariant
- `accepted_memory_does_not_enable_trading` — ACCEPTED ≠ trading

---

## Safety Invariants

| Property | Value |
|----------|-------|
| Read Only | YES |
| No Real Orders | YES |
| Production Trading | BLOCKED |
| ACCEPTED Enables Trading | NO — always False |
| BUY/SELL/ORDER in Commands | BLOCKED |
| Auto-Accept Memory | NO |
| Auto-Reject Memory | NO |
| Connect to Broker | NO |
| Real Order Ready | NO |

---

*[!] Research Only. No Real Orders. Production Trading BLOCKED. Not Investment Advice.*

*TW Quant Cockpit v0.8.1 — Strategy Memory UX.*
