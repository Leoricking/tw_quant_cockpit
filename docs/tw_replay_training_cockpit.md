# TW Replay Training Cockpit — v0.5.6

> **[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not investment advice. REAL_ORDER_READY=False.**

---

## Overview

The TW Replay Training Cockpit (v0.5.6) is a Taiwan stock intraday tape reading practice system.
It allows you to step through historical 1min/5min intraday bars bar-by-bar, place training markers,
and receive AI rule-based review and scoring — all without any real order execution.

**Core principle:** Taiwan Time-Machine style replay practice (台股時光機復盤練習).

---

## Features

- **Hidden future data** — `hidden_future_data=True` by default; `get_visible_bars()` NEVER returns future bars
- **1min/5min timeframe** — configurable bar frequency
- **User markers** — annotate ENTRY, EXIT, STOP_LOSS, TAKE_PROFIT, FAKE_BREAKOUT, VWAP_LOSS, OPENING_RANGE_FAIL, and more
- **AI rule-based review** — 7 detection rules, no external LLM API, no network calls
- **Session scoring** — 0-100 score with 6-component breakdown
- **Drill builder** — 8 drill types tailored to detected mistakes
- **Journal integration** — research/replay training entries only (no real trade data)
- **9-section Markdown report** — comprehensive session debrief

---

## CLI Usage

### 1. Create a replay training session
```bash
python main.py replay-training --symbol 2454 --date 2026-06-03 --timeframe 1min --mode real
```

### 2. Load session summary
```bash
python main.py replay-training-summary
```

### 3. Advance one bar
```bash
python main.py replay-training-next --session-id RTRAIN-20260603-120000-ABCDEF
```

### 4. Go back one bar
```bash
python main.py replay-training-prev --session-id RTRAIN-20260603-120000-ABCDEF
```

### 5. Add a marker
```bash
python main.py replay-training-marker --session-id RTRAIN-... --type ENTRY --price 123.5 --note "VWAP reclaim"
```

### 6. Run AI review
```bash
python main.py replay-ai-review --session-id RTRAIN-...
```

### 7. Get session score
```bash
python main.py replay-training-score --session-id RTRAIN-...
```

### 8. Get drill suggestions
```bash
python main.py replay-training-drills --session-id RTRAIN-...
```

### 9. Generate full report
```bash
python main.py replay-training-report --mode real
```

---

## GUI Usage

1. Open the GUI: `python main.py cockpit`
2. Click the **Replay Training** tab
3. Enter symbol, date, timeframe
4. Click **Load Session**
5. Use **Prev / Next** buttons to step through bars
6. Place markers using the marker buttons
7. Click **Run AI Review** to get rule-based feedback
8. Click **Generate Report** for full Markdown debrief

---

## AI Review Rules

The AI reviewer uses 7 rule-based checks (no external LLM):

| Rule | Description |
|------|-------------|
| chase_high | Entry after 3+ consecutive up bars AND price > VWAP * 1.01 |
| ignored_vwap_loss | Entry with no stop added within 3 bars of price losing VWAP |
| ignored_fake_breakout | ENTRY marker on breakout bar that reversed within 3 bars |
| ignored_opening_range_fail | Entry near OR break that failed |
| early_take_profit | EXIT followed by price continuing up 2%+ with no weakness signal |
| late_stop_loss | Price dropped 3%+ below entry before stop/exit marker |
| violated_strategy | strategy_context has WAIT_PULLBACK but user entered on up-bar |

---

## Score Breakdown (0-100)

| Component | Points |
|-----------|--------|
| Entry quality | 25 |
| Exit/stop discipline | 20 |
| Fake breakout avoidance | 15 |
| VWAP/opening range compliance | 15 |
| Strategy adherence | 15 |
| Notes completeness | 10 |

---

## Output Files

All outputs saved to `data/backtest_results/replay_training/`:
- `replay_training_sessions.csv`
- `replay_markers.csv`
- `replay_mistakes.csv`
- `replay_ai_reviews.csv`
- `replay_scores.csv`
- `replay_drills.csv`
- `replay_training_summary.csv`

Reports saved to `reports/replay_training_report_*.md`

---

## Safety Declaration

| Constraint | Status |
|------------|--------|
| Replay Training Only | TRUE |
| Research Only | TRUE |
| No Real Orders | TRUE |
| No Broker Execution | TRUE |
| No Auto Trading | TRUE |
| Production Blocked | TRUE |
| Real Order Ready | FALSE |
| External LLM API | FALSE |
| Network Calls | FALSE |

> [!] This module is for replay training and research simulation only.
> No real orders are placed. No broker is connected.
> Not investment advice.
