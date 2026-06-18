# Replay Challenge Mode v1.2.7

**[!] Challenge Training Only. Simulation Only. No Real Orders. Not Investment Advice.**
**[!] Future data hidden. Outcome hidden until explicit reveal. Answer Key separate.**
**[!] No Public Leaderboard. No Network Submission. Local personal records only.**
**[!] Process weight always >= Outcome weight. No auto-decision. No auto-reveal.**

---

## Overview

v1.2.7 adds the Replay Challenge Mode to the TW Quant Cockpit. This mode wraps the existing replay infrastructure in structured, scored challenge scenarios designed to improve decision-making discipline through deliberate practice.

### Key Safety Invariants

- Research/simulation only — no broker, no real orders
- Challenge actions are SIMULATION DECISION ONLY
- Future data hidden by Future Firewall (all difficulty levels, including EXPERT)
- Outcome hidden until explicit reveal with `--reveal --confirm-review`
- Answer Key stored separately; active challenge cannot query it
- Process weight always >= Outcome weight (Process default 80%, Outcome max 20%)
- Deterministic seed: same seed + data version = same challenge
- No Public Leaderboard; No Network Submission
- Missing modules show UNAVAILABLE; missing data shows BLOCKED; no crash
- All mistakes are SUGGESTED only — never auto-Confirmed
- Timeout only marks status — never executes decision
- Pause time does not count as active elapsed

---

## Architecture

### Core Components (31 modules)
- `replay/challenge_schema.py` — dataclasses
- `replay/challenge_engine.py` — main engine
- `replay/challenge_library.py` — challenge library
- `replay/challenge_template.py` — 12 built-in templates
- `replay/challenge_generator.py` — challenge generation
- `replay/challenge_seed.py` — deterministic seed
- `replay/challenge_difficulty.py` — difficulty settings
- `replay/challenge_rules.py` — rule types
- `replay/challenge_objectives.py` — objective types
- `replay/challenge_constraints.py` — constraints
- `replay/challenge_session.py` — session wrapper
- `replay/challenge_attempt.py` — attempt manager
- `replay/challenge_clock.py` — monotonic clock
- `replay/challenge_hidden_data.py` — hidden data guard
- `replay/challenge_hint.py` — hint manager
- `replay/challenge_action.py` — action log
- `replay/challenge_scoring.py` — scoring engine
- `replay/challenge_result.py` — result builder
- `replay/challenge_review.py` — review manager
- `replay/challenge_progress.py` — progress tracker
- `replay/challenge_streak.py` — streak tracker
- `replay/challenge_badges.py` — badge system
- `replay/challenge_leaderboard.py` — local leaderboard
- `replay/challenge_comparator.py` — attempt comparator
- `replay/challenge_batch.py` — batch runner
- `replay/challenge_store.py` — data store
- `replay/challenge_query.py` — query interface
- `replay/challenge_summary.py` — summary builder
- `replay/challenge_report.py` — report generator
- `replay/challenge_definition.py` — definition manager
- `replay/challenge_health.py` — health check

---

## Built-in Templates (12)

1. Free Decision Practice (BEGINNER)
2. Timed Pullback Decision (INTERMEDIATE)
3. Breakout Confirmation (INTERMEDIATE)
4. No Chase Discipline (INTERMEDIATE)
5. No Panic Sell Discipline (INTERMEDIATE)
6. Do Not Rebuy Yet (ADVANCED)
7. Bottom Reversal Confirmation (ADVANCED)
8. Risk Control Under Pressure (ADVANCED)
9. Strategy Conflict Review (ADVANCED)
10. Multi-Timeframe Conflict (ADVANCED)
11. Point-in-Time Integrity (EXPERT)
12. Journal Discipline (BEGINNER)

---

## Difficulty Levels

| Level | Symbol | Date | Hints | Time | Strategy Warnings | Future Firewall |
|-------|--------|------|-------|------|-------------------|-----------------|
| BEGINNER | Visible | Visible | 5 | 2x | Show | **Active** |
| INTERMEDIATE | Visible | Visible | 2 | 1x | Show | **Active** |
| ADVANCED | Optional hide | Optional hide | 1 | 1x | Hide | **Active** |
| EXPERT | Hidden | Hidden | 0 | 0.8x | Hide | **Active** |
| CUSTOM | Config | Config | Config | Config | Config | **Always Active** |

All difficulty levels keep Future Firewall active. CUSTOM cannot disable it.

---

## Hidden Data Rules

### Always Hidden in Active Payload
- `forward_return`, `realized_pnl`, `outcome_score`, `future_signal`
- `final_high`, `final_low`, `hindsight_score`, `answer_key`, `best_action`, `expected_result`
- `future_bars`, `future_strategy_signals`, `future_timeframe_conflicts`
- `future_review_classification`, `prior_attempt_answer`, `best_attempt_answer`
- `future_journal_revisions`, `MFE`, `MAE`, `final_session_high`, `final_session_low`

Any of these in the active payload → `BLOCKED` status.

---

## Scoring

Default weights:
- Process Quality: 35%
- Discipline: 15%
- Risk Planning: 15%
- Information Usage: 10%
- Strategy Awareness: 10%
- MTF Awareness: 10%
- Timing: 5%

Rules:
- Profit != high score. Loss != low score.
- ENTER does not auto-get high score. WAIT/SKIP not auto-penalized.
- Outcome not included by default (post-review optional, max 20%).
- Process weight always >= Outcome weight.
- Supports: GOOD_PROCESS_BAD_OUTCOME, BAD_PROCESS_GOOD_OUTCOME, PROCESS_ONLY.

---

## CLI SOP

```bash
python main.py replay-challenge-health
python main.py replay-challenge-templates
python main.py replay-challenge-list
python main.py replay-challenge-create --template NO_CHASE --difficulty INTERMEDIATE
python main.py replay-challenge-start --challenge-id <id>
python main.py replay-challenge-action --attempt-id <id> --action WRITE_THESIS --reason "..."
python main.py replay-challenge-submit --attempt-id <id>
python main.py replay-challenge-result --attempt-id <id>
python main.py replay-challenge-review --attempt-id <id>
# Reveal outcome (requires both flags):
python main.py replay-challenge-reveal-outcome --attempt-id <id> --reveal --confirm-review
python main.py replay-challenge-progress
python main.py replay-challenge-leaderboard
```

---

## Safety Declaration

[!] Challenge Training Only. Simulation Only. No Real Orders.
[!] Future data hidden. Outcome hidden until explicit reveal.
[!] Answer Key separate. Process weight >= Outcome weight.
[!] No Public Leaderboard. No Network Submission.
[!] No auto-decision. No auto-reveal. No auto-confirm.
[!] Not Investment Advice.
