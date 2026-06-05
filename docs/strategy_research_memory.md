# TW Quant Cockpit — Strategy Research Memory v0.7.2

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
| `python main.py strategy-memory-search --keyword replay` | Search by keyword |
| `python main.py strategy-memory-show --memory-id XXXXX` | Show single memory |
| `python main.py strategy-memory-update-status --memory-id XXXXX --status REVIEWING` | Update status |
| `python main.py strategy-memory-archive --memory-id XXXXX` | Archive a memory |
| `python main.py strategy-memory-report` | Generate Markdown report |

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

---

## GUI Panel

The Strategy Research Memory panel is available in the TW Quant Cockpit GUI under the `research_os` tab group.

Features:
- Safety banner always visible
- Summary cards (Total, Active, New, Reviewing, etc.)
- Filter by keyword, type, status, priority, symbol
- Memory table with color-coded priority and status
- Detail panel with hypothesis, evidence, validation plan, suggested commands
- Links table
- Run extraction, generate report, refresh, update status, archive

---

*[!] Research Only. No Real Orders. Production Trading BLOCKED. Not Investment Advice.*

*TW Quant Cockpit v0.7.2 — Strategy Research Memory.*
