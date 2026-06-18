# Replay Review Dashboard v1.2.6

**Version:** 1.2.6
**Release:** Replay Review Dashboard
**Track:** replay_training
**Research Only:** True | **No Real Orders:** True

---

## Safety Declaration

> [!] Replay Review Only. Process/Outcome Separated.
> Outcome Hidden Until Explicit Reveal.
> Suggested Mistakes Are Not Confirmed.
> No Auto Review Completion. No Auto Decision.
> No Auto Execution. No Real Orders. Broker Disabled.
> Not Investment Advice.

---

## Overview

The Replay Review Dashboard provides a unified view integrating:
- Session management and review tracking
- Decision journals
- Process scoring (no future data, no outcome, no PnL)
- Outcome scoring (hidden until explicit reveal)
- Mistake taxonomy (suggested only — not auto-confirmed)
- Strategy Knowledge Replay (training only)
- Multi-Timeframe Replay (D1/M60/M20/M5/M1)
- Review queue (P0/P1/P2/P3)
- Review progress tracking
- Search, filtering, grouping, sorting
- Session comparison
- Batch review operations
- Report generation
- Governance integration

## Key Modules

| Module | Description |
|---|---|
| `replay/review_dashboard_schema.py` | Dataclasses: Snapshot, SessionRow, QueueItem, Progress, Checklist |
| `replay/review_dashboard_adapter.py` | Loads from all sub-modules (graceful UNAVAILABLE) |
| `replay/review_dashboard_engine.py` | Builds global/session/symbol/scenario dashboards |
| `replay/review_dashboard_cards.py` | Card builders for all categories |
| `replay/review_dashboard_tables.py` | Table builders with sort/filter/paginate |
| `replay/review_dashboard_charts.py` | Chart data spec builders |
| `replay/review_queue.py` | Queue manager (append-only history) |
| `replay/review_progress.py` | Progress calculator |
| `replay/review_checklist.py` | Checklist with manual-only actions |
| `replay/review_notes.py` | Append-only note revisions |
| `replay/review_tags.py` | Tags (no score effect) |
| `replay/review_search.py` | Full-text search |
| `replay/review_filters.py` | Filter builders |
| `replay/review_sorting.py` | Multi-column sort |
| `replay/review_grouping.py` | Group by field |
| `replay/review_comparator.py` | Session/symbol/scenario comparison |
| `replay/review_batch.py` | Batch operations (preview by default) |
| `replay/review_store.py` | Append-only JSONL store |
| `replay/review_query.py` | Query engine |
| `replay/review_summary.py` | Summary builders |
| `replay/review_report.py` | Markdown report builder |
| `replay/review_health.py` | Health check |

## Safety Invariants

- `auto_review_complete_enabled = False`
- `auto_outcome_reveal_enabled = False`
- `auto_mistake_confirmation_enabled = False`
- `auto_decision_creation_enabled = False`
- `auto_score_to_trade_enabled = False`
- `replay_trade_execution_enabled = False`
- Outcome score hidden in `ReplayReviewSessionRow.to_dict()` when `outcome_revealed=False`
- Process/Outcome strictly separated in all charts and reports
- Missing modules return UNAVAILABLE, not crash
- Batch runner BLOCKED without `--execute --allow-write`
- Checklist: `auto_complete = False` always
- Queue: `complete()` does NOT auto-confirm mistakes or auto-reveal outcome

## Not Investment Advice
