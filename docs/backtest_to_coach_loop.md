# Backtest-to-Coach Loop v0.7.3

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not Investment Advice. All outputs are research and training materials only.**

---

## Overview

v0.7.3 introduces the **Backtest-to-Coach Loop** — a pipeline that converts backtest weaknesses, replay mistakes, journal patterns, rule confidence issues, strategy memories, and data gaps into safe, structured coach training tasks.

The loop bridges quantitative research results (backtests, rule governance, data coverage) with skill-building actions (replay practice, journal review, rule review). It produces daily and weekly training plans with specific, measurable practice goals.

---

## What Is the Backtest-to-Coach Loop?

The Backtest-to-Coach Loop:

1. **Reads** outputs from all Research OS modules (backtest results, replay training, portfolio journal, strategy memory, research intelligence, rule governance, data coverage)
2. **Extracts** weakness signals from these outputs (low win rate, high drawdown, low replay score, repeat mistakes, data gaps, low-confidence rules)
3. **Converts** each signal into a safe coach training task (PRACTICE_REPLAY, REVIEW_RULE, REVIEW_JOURNAL, FIX_DATA, BACKTEST_MORE, READ_REPORT, UPDATE_MEMORY, WAIT)
4. **Ranks** tasks by priority (P0 → P3) and task type priority
5. **Deduplicates** to remove repeated tasks
6. **Produces** a daily training plan (max 7 items, balanced by type) and weekly plan (max 12 items)
7. **Saves** all outputs to CSV and generates a Markdown report

**What it does NOT do:**
- Does NOT place real orders
- Does NOT connect to any broker
- Does NOT modify rule weights or strategy weights
- Does NOT auto-accept memories
- Does NOT auto-trade
- All outputs are labeled: Research Only, No Real Orders, Production Trading BLOCKED

---

## Why Connect Backtest to Training?

| Without Loop | With Loop |
|-------------|-----------|
| Backtest reveals weak win rate — no action | Low win rate → BACKTEST_MORE task with command |
| Replay score 55 — no follow-up | Low score → PRACTICE_REPLAY task with drill command |
| Journal shows repeat stop-loss mistake — forgotten | Repeat mistake → REVIEW_JOURNAL task |
| Rule confidence 0.3 — unnoticed | Low confidence → REVIEW_RULE task |
| Data gap in coverage — isolated | Data gap → FIX_DATA task |

The loop closes the gap between research findings and structured skill-building practice.

---

## Signal Extractor

`BacktestSignalExtractor` extracts `BacktestCoachSignal` objects from:

| Source Module | Signal Examples |
|--------------|----------------|
| `backtest` | low win_rate, high max_drawdown, poor reward/risk, small sample |
| `strategy_memory` | rule candidate needs evidence, replay mistake pattern, data gap |
| `replay_training` | score < 60, fake breakout mistake, stop loss mistake |
| `portfolio_journal` | repeat mistake tags, low process quality |
| `research_intelligence` | P0/P1 data gaps, replay issues, rule reviews |
| `rule_governance` | low confidence rules (< 0.4), candidate rules needing backtest |
| `data_coverage` | missing required items, not generated items |

Thresholds:
- Win rate < 45% → `LOW_WIN_RATE` / P1
- Max drawdown > 15% → `HIGH_DRAWDOWN` / P1
- Avg reward/risk < 1.2 → `POOR_RISK_REWARD` / P1
- Trade count < 30 → `SAMPLE_TOO_SMALL` / P2
- Replay score < 60 → `REPLAY_SCORE_LOW` / P1
- Rule confidence < 0.4 → `RULE_LOW_CONFIDENCE` / P1

---

## Coach Task Builder

`CoachTaskBuilder` converts each signal to a `CoachTrainingTask`.

**Task Types (ONLY these — no trading actions):**

| Task Type | When Used |
|-----------|-----------|
| `PRACTICE_REPLAY` | Fake breakout, stop loss, VWAP, opening range, low replay score |
| `REVIEW_RULE` | High drawdown, poor risk/reward, low confidence rule |
| `REVIEW_JOURNAL` | Repeat journal mistakes, late exit |
| `FIX_DATA` | Data insufficient, missing required data |
| `BACKTEST_MORE` | Low win rate, small sample, rule candidate needs evidence |
| `READ_REPORT` | Data not generated, optional items |
| `UPDATE_MEMORY` | Memory follow-up tasks |
| `WAIT` | Environment-limited items |

---

## Daily Training Plan

The daily plan (max 7 items) is balanced by type:

| Slot | Task Type | Count |
|------|-----------|-------|
| System/Data | FIX_DATA or READ_REPORT | 1 |
| Replay Practice | PRACTICE_REPLAY | 2 |
| Journal Review | REVIEW_JOURNAL | 1 |
| Rule Review | REVIEW_RULE | 1 |
| Backtest | BACKTEST_MORE | 1 |
| Optional | Any remaining P2/P3 | 1 |

---

## Weekly Training Plan

The weekly plan (max 12 items) is the top 12 tasks ranked by priority and task type priority.

---

## Integration

| Module | Integration |
|--------|-------------|
| `strategy_memory` | `extract_from_backtest_coach()` reads BACKTEST_MORE/REVIEW_RULE tasks as FOLLOW_UP_TASK memories |
| `research_intelligence` | Optionally loads backtest_coach_summary as context for system signals |
| `report_pack` | `REPORT_BACKTEST_COACH` in daily, weekly, and full packs (optional) |
| `auto_report_center` | backtest_coach summary in full and daily profiles |
| `auto_report_index` | 4 manifest fields: total_tasks, replay_tasks, backtest_tasks, report_path |
| `regression/suite_registry` | 4 regression tests in research_os suite |
| `stable_release/checklist_v060` | 2 checks: summary_can_run, no_forbidden_actions |
| `stable_release/capability_matrix` | `backtest_to_coach_loop` capability (USABLE) |
| `data_coverage/registry` | 2 coverage items: backtest_coach_tasks, backtest_coach_report |
| `experiments/snapshot_builder` | `build_backtest_coach_snapshot()` |
| `gui/dashboard` | BacktestCoachPanel tab |
| `gui/navigation/tab_registry` | `backtest_coach` tab metadata |

---

## CLI Usage

```bash
# Run full loop (extract signals → build tasks → save → report)
python main.py backtest-coach --mode real --period daily

# Run weekly plan
python main.py backtest-coach --mode real --period weekly

# Show summary only
python main.py backtest-coach-summary

# Show signals
python main.py backtest-coach-signals

# Show all tasks
python main.py backtest-coach-tasks

# Show daily plan
python main.py backtest-coach-daily-plan

# Show weekly plan
python main.py backtest-coach-weekly-plan

# Generate Markdown report only
python main.py backtest-coach-report --mode real
```

---

## GUI Usage

1. Launch: `python main.py cockpit`
2. Find the "Backtest Coach" tab in the Research OS group
3. Click **Run Loop** to extract signals and build tasks
4. Review **Tasks** tab for all coach training tasks with priorities
5. Review **Daily Plan** tab for today's 7-item training plan
6. Click **Copy Selected Command** to copy the `suggested_command` for a task
7. Click **Generate Report** for a Markdown report
8. Use **Signals** tab to see all raw weakness signals

---

## Safety

- All outputs labeled: Research Only, No Real Orders, Production Trading BLOCKED
- `_guard()` function raises `ValueError` if any text contains: BUY, SELL, ORDER, EXECUTE, SUBMIT_ORDER, AUTO_TRADE, REAL_TRADE
- Copy Command button guards against forbidden command keywords
- No broker connection. No order submission. No auto-trading.
- `READ_ONLY = True`, `NO_REAL_ORDERS = True`, `PRODUCTION_BLOCKED = True` in `backtest_coach/__init__.py`

---

## Files

| File | Description |
|------|-------------|
| `backtest_coach/__init__.py` | Package init with safety flags |
| `backtest_coach/backtest_coach_schema.py` | Dataclasses, constants, forbidden keyword guard |
| `backtest_coach/backtest_signal_extractor.py` | Extracts signals from 7 source modules |
| `backtest_coach/coach_task_builder.py` | Converts signals to tasks, ranks, deduplicates, builds plans |
| `backtest_coach/backtest_coach_engine.py` | Master pipeline engine |
| `backtest_coach/backtest_coach_store.py` | CSV persistence (5 output files) |
| `reports/backtest_coach_report.py` | 8-section Markdown report generator |
| `gui/backtest_coach_adapter.py` | GUI ↔ backend bridge |
| `gui/backtest_coach_panel.py` | PySide6 GUI tab |

---

*TW Quant Cockpit v0.7.3 — Backtest-to-Coach Loop — Research Only — Not Investment Advice*
