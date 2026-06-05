# TW Quant Cockpit — Strategy Research Memory v0.8.1

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not Investment Advice. REAL_ORDER_READY=False.**

---

## Overview

Strategy Research Memory (v0.7.2) is a queryable, status-tracked memory system for the TW Quant Cockpit Research OS. It stores research hypotheses, rule candidates, replay mistake patterns, journal patterns, data gaps, report gaps, regression risks, and research conclusions extracted from all Research OS module outputs.

All items are research-only. No trading actions, no auto-accept/reject, no real orders.

---

## Memory Types

| Type | Description |
|------|-------------|
| `STRATEGY_HYPOTHESIS` | Research hypothesis about a strategy idea |
| `RULE_CANDIDATE` | Candidate rule for governance review |
| `REPLAY_MISTAKE_PATTERN` | Recurring mistake pattern from replay training |
| `JOURNAL_PATTERN` | Recurring pattern from portfolio journal |
| `DATA_GAP` | Missing data that blocks analysis |
| `REPORT_GAP` | Missing report that creates research blind spot |
| `REGRESSION_RISK` | Risk identified from regression/stability checks |
| `PROVIDER_LIMITATION` | Data provider limitation |
| `RESEARCH_CONCLUSION` | Research conclusion ready for review |
| `FOLLOW_UP_TASK` | Follow-up task identified during research |

---

## Memory Statuses

| Status | Description |
|--------|-------------|
| `NEW` | Just extracted, not yet reviewed |
| `REVIEWING` | Under active review |
| `VALIDATING` | Being validated with data/backtests |
| `ACCEPTED` | Validated and accepted as research finding |
| `REJECTED` | Reviewed and rejected |
| `ARCHIVED` | No longer active, archived for reference |
| `NEEDS_MORE_EVIDENCE` | Interesting but needs more evidence |

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `python main.py strategy-memory` | Run full extraction pipeline |
| `python main.py strategy-memory-summary` | Show latest summary |
| `python main.py strategy-memory-list` | List all memories |
| `python main.py strategy-memory-list --active-only` | List active (non-archived) memories |
| `python main.py strategy-memory-list --needs-action` | List memories needing action |
| `python main.py strategy-memory-list --sort priority` | Sort by priority |
| `python main.py strategy-memory-list --include-archived` | Include archived memories |
| `python main.py strategy-memory-search --keyword replay` | Search by keyword |
| `python main.py strategy-memory-search --needs-action` | Search for action-needed items |
| `python main.py strategy-memory-search --source-module replay_training` | Filter by source module |
| `python main.py strategy-memory-show --memory-id XXXXX` | Show single memory detail |
| `python main.py strategy-memory-update-status --memory-id XXXXX --status REVIEWING` | Update status |
| `python main.py strategy-memory-archive --memory-id XXXXX` | Archive a memory |
| `python main.py strategy-memory-report` | Generate Markdown report |
| `python main.py strategy-memory-validation-queue` | Show memories ready for validation |
| `python main.py strategy-memory-active-threads` | Show active research threads |
| `python main.py strategy-memory-repeated-patterns` | Show repeated pattern memories |

---

## Data Sources

Strategy memory items are extracted from:

- `data/backtest_results/research_intelligence/` — Research Intelligence recommendations
- `data/backtest_results/strategy_knowledge/` — Strategy Knowledge Ingestion
- `data/backtest_results/rule_governance/` — Rule Governance low-confidence rules
- `data/backtest_results/replay_training/` — Replay Training mistake patterns
- `data/backtest_results/portfolio_journal/` — Journal recurring mistakes
- `data/backtest_results/data_coverage/` — Data Coverage gaps
- `data/backtest_results/report_pack/` — Report Pack missing items

---

## Output Files

| File | Description |
|------|-------------|
| `data/backtest_results/strategy_memory/strategy_memories.csv` | All memory items |
| `data/backtest_results/strategy_memory/strategy_memory_links.csv` | Memory links |
| `data/backtest_results/strategy_memory/strategy_memory_summary.csv` | Latest summary |
| `data/backtest_results/strategy_memory/strategy_memory_timeline.csv` | Timeline view |
| `reports/strategy_memory_report_YYYY-MM-DD.md` | Markdown report |

---

## Deduplication

Memory items are deduplicated by: `normalized(title) + memory_type + source_module`.

If the same item is seen again:
- `seen_count` is incremented
- `last_seen_at` is updated
- Status is preserved (not reset to NEW)
- Title/summary only updated if status is still NEW

---

## Memory Links

Links are built automatically between:
- Items with the same title+type → `DUPLICATES`
- Items sharing symbols → `RELATED_TO`
- Items sharing rules → `RELATED_TO`
- `RULE_CANDIDATE` + `DATA_GAP` → `REQUIRES_DATA`
- `STRATEGY_HYPOTHESIS` → `REQUIRES_BACKTEST`
- `REPLAY_MISTAKE_PATTERN` → `REQUIRES_REPLAY`

---

## v0.8.1 UX Additions

| Feature | Description |
|---------|-------------|
| `needs_action` field | True for P0/P1 items needing immediate attention |
| `validation_ready` field | True for items in VALIDATING status |
| `status_hint` field | Human-readable status label |
| `next_step` field | Suggested safe CLI command for next step |
| `last_action_at` field | ISO timestamp of last status change |
| `display_title` field | Formatted title for GUI display |
| `safe_command_count` field | Number of safe commands available |
| `blocked_command_count` field | Always 0 (BUY/SELL/ORDER commands blocked) |
| `accepted_is_research_only` | Always True — ACCEPTED ≠ trading enabled |

### Status Flow

```
NEW → REVIEWING → VALIDATING → ACCEPTED
                              → REJECTED
                              → NEEDS_MORE_EVIDENCE
* → ARCHIVED (any status)
```

**ACCEPTED means: research finding accepted for further study.**
**ACCEPTED does NOT mean: strategy enabled, trade signal generated, or order placed.**

### Safe Command Labels

| Label | Meaning |
|-------|---------|
| `SAFE_READ_ONLY` | Display/list command, no side effects |
| `SAFE_REPORT` | Report generation command |
| `SAFE_REGRESSION` | Regression suite command |
| `SAFE_REPLAY` | Replay training command |
| `SAFE_DATA_CHECK` | Data coverage command |

---

## Safety Invariants

| Property | Value |
|----------|-------|
| Read Only | YES |
| No Real Orders | YES |
| Production Trading | BLOCKED |
| Auto-Accept Memory | NO |
| Auto-Reject Memory | NO |
| Modify Rule Weights | NO |
| Connect to Broker | NO |
| Real Order Ready | NO |
| ACCEPTED Enables Trading | NO — research-only invariant always enforced |
| BUY/SELL/ORDER in Commands | BLOCKED — load_safe_commands() guards all output |

---

## GUI Panel (v0.8.1)

The Strategy Research Memory panel is available in the TW Quant Cockpit GUI under the `research_os` tab group.

Features:
- Safety banner: "ACCEPTED means research accepted, not trading enabled"
- Summary cards: Total, Active, Needs Action, Validation Queue, Repeated, P0, P1, Blocked Cmds
- Filters: keyword, type, status, priority, symbol, source module, active-only, needs-action, include-archived
- Memory table: Priority, Status, Type, Title, Source, Symbols, Seen, Last Seen, Needs Action, Validation Ready
- Detail panel tabs: Summary, Hypothesis, Evidence, Validation, Commands, Links, Safety
- Commands tab: safe command list with safety labels; BUY/SELL/ORDER keywords blocked
- Links tab: Relation, Source, Target, Why Linked, Next Step columns
- Safety tab: research-only declaration with ACCEPTED note
- Status action buttons: Set REVIEWING, Set VALIDATING, Set NEEDS_MORE_EVIDENCE, Set ACCEPTED, Set REJECTED, Archive
- Run extraction, generate report, refresh

---

*[!] Research Only. No Real Orders. Production Trading BLOCKED. Not Investment Advice.*

*TW Quant Cockpit v0.8.1 — Strategy Research Memory UX.*
