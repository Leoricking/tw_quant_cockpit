# Replay Training UX Foundation — v1.2.0

> [!] Research Only. No Real Orders. Replay Training Only.
> This system is for training and simulation purposes. No orders are placed. No production data is modified.

## Overview

v1.2.0 introduces the **Replay Training UX Foundation** — a complete point-in-time historical replay system for structured training on past market data. The replay engine allows a researcher to step through a historical period day-by-day, record simulation decisions at each step, annotate observations, and build a structured training record — all with a strict future data firewall.

## Core Principles

1. **No Future Data Leakage** — All data shown at each replay step is strictly limited to what was available on that date. Forward returns, future highs, hindsight scores, and outcome labels are blocked at the data layer.
2. **Simulation Decisions Only** — All decisions recorded during replay carry `simulation_decision_only=True` and `no_real_orders=True`. No order is ever placed or queued.
3. **Point-in-Time Accuracy** — Technical indicators (MA, KD, MACD, RSI, ATR) are computed using only data available on or before the replay date.
4. **Append-Only Store** — Session decisions, events, and annotations are stored in append-only JSONL files. Nothing is deleted; hidden annotations set `hidden=True`.
5. **Trading Calendar From Data** — The replay calendar is built from actual trading dates in imported CSV data, not a Mon–Fri heuristic.

## Architecture

```
replay/
  replay_schema.py              # Session, decision, annotation, event dataclasses
  replay_calendar.py            # TradingCalendar from real CSV data
  replay_data_source.py         # PIT data loading with REAL/MOCK mode separation
  future_data_firewall.py       # Blocks all forward-return fields
  point_in_time_context.py      # Computes PIT technical indicators
  replay_timeline.py            # Date navigation (previous/next/jump)
  replay_session_store.py       # Append-only JSONL/JSON store
  replay_training_session.py    # Session lifecycle (create/open/archive/duplicate)
  replay_training_engine.py     # Main engine — orchestrates all sub-components
  replay_decision.py            # Decision capture with SIMULATION invariant
  replay_annotations.py         # Annotation management
  replay_summary.py             # Session summary (no future performance data)
  replay_query.py               # Query sessions, decisions, events, annotations
  replay_health.py              # 8-check health verification

gui/
  replay_session_dialog.py      # PySide6 session creation dialog
  replay_decision_dialog.py     # PySide6 decision recording dialog (with safety banner)
  replay_training_panel.py      # Main replay training GUI panel (v0.6.3+)
  replay_training_adapter.py    # GUI adapter layer

reports/
  replay_training_session_report.py   # 9-section session report builder
```

## Session ID Format

```
RPL-{SYMBOL}-{YYYYMMDD}-{RANDOM4}
Example: RPL-2330-20260615-A1B2
```

## Decision Actions

| Action | Meaning |
|--------|---------|
| WATCH | Observing, no position |
| WAIT | Hold off, conditions not met |
| ENTER | Start a simulated position |
| ADD | Add to existing simulated position |
| HOLD | Maintain current simulated position |
| REDUCE | Reduce simulated position size |
| EXIT | Close simulated position |
| STOP | Emergency stop (simulated) |
| SKIP | Skip this date |

## Future Data Firewall

The firewall blocks the following fields from appearing in any replay context:

**Forbidden Fields:**
- `forward_return`, `future_return`, `future_high`, `future_low`
- `outcome`, `final_label`, `target_label`, `realized_pnl`
- `next_close`, `next_open`, `future_signal`, `hindsight_score`

**Forbidden Prefixes:**
- `forward_return_*` (blocks forward_return_1, forward_return_5, etc.)

The firewall also enforces announcement date filtering for fundamental data (quarterly reports not shown until after the announcement date).

## Session Modes

| Mode | Data Source | Qualification |
|------|-------------|---------------|
| `real` | Actual imported CSV data | OBSERVATIONAL_ONLY (if data verified PIT) |
| `mock` | Synthetic/generated data | DEMO_ONLY |

**Note:** Mock mode sessions are always classified as DEMO_ONLY and cannot be used for formal research conclusions.

## CLI Commands

| Command | Description |
|---------|-------------|
| `replay-health` | Run 8-check health verification |
| `replay-create` | Create a new replay session |
| `replay-sessions` | List all sessions |
| `replay-session` | Show session details |
| `replay-resume` | Resume a paused session |
| `replay-current` | Show current date snapshot |
| `replay-next` | Advance to next trading day |
| `replay-previous` | Go back to previous trading day |
| `replay-jump` | Jump to a specific date |
| `replay-play-step` | Play one step forward |
| `replay-pause` | Pause the current session |
| `replay-decision` | Record a simulation decision |
| `replay-annotation` | Add an annotation |
| `replay-summary` | Show session summary |
| `replay-report` | Generate full session report |
| `replay-duplicate` | Duplicate a session |
| `replay-archive` | Archive a session (immutable) |
| `replay-firewall-check` | Check firewall status at current date |
| `replay-point-in-time-check` | Verify PIT context at current date |

## Quick Start

```bash
# Check the replay system health
python main.py replay-health

# Create a session for 2330 (TSMC) covering 2023
python main.py replay-create --stock 2330 --start 2023-01-01 --end 2023-12-31 --name "2330 Training 2023"

# Note the session ID from output (e.g., RPL-2330-20230101-XXXX)
python main.py replay-sessions

# Step through the session
python main.py replay-next --session-id RPL-2330-20230101-XXXX
python main.py replay-current --session-id RPL-2330-20230101-XXXX

# Record a simulation decision
python main.py replay-decision --session-id RPL-2330-20230101-XXXX --action WATCH --confidence 50 --reason "Waiting for breakout"

# Add an annotation
python main.py replay-annotation --session-id RPL-2330-20230101-XXXX --type SUPPORT --title "Volume spike" --content "Volume 2x above MA5"

# Generate session report
python main.py replay-report --session-id RPL-2330-20230101-XXXX
```

## Safety Invariants

- `NO_REAL_ORDERS = True` (module-level, all replay files)
- `RESEARCH_ONLY = True` (module-level, all replay files)
- `REPLAY_TRAINING_ONLY = True` (engine-level)
- `SIMULATION_DECISION_ONLY = True` (decision manager)
- `NO_FUTURE_PERFORMANCE_EVALUATION = True` (summary builder)
- `REPLAY_TRADE_EXECUTION_ENABLED = False` (version_info.py)
- `REPLAY_AUTO_EXECUTION_ENABLED = False` (version_info.py)

## Version Information

- **Version:** 1.2.0
- **Release Name:** Replay Training UX Foundation
- **Stage:** FOUNDATION
- **Base Release:** 1.1.9 Data Governance Stable Rollup
- **Track:** replay_training

---
[!] Research Only. No Real Orders. Not Investment Advice.
