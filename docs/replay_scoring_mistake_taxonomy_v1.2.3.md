# Replay Scoring & Mistake Taxonomy v1.2.3

> **[!] Research Only. No Real Orders. Replay Training Only.**
> **[!] Scoring NEVER triggers paper orders or broker execution.**
> **[!] Process scores use NO future data, NO outcome, NO PnL.**
> **[!] Outcome reveal is EXPLICIT ONLY — default BLOCKED.**
> **[!] Mistake detection is SUGGESTED status only — never auto-confirmed.**
> **[!] Not Investment Advice. Broker Disabled.**

## Overview

v1.2.3 adds a complete replay scoring and mistake taxonomy system. It provides structured
process and outcome scoring with strict separation, explicit outcome reveal, composite
score classification, explainable mistake taxonomy and review, plan adherence evaluation,
confidence handling, and GUI/CLI review workflows.

Key features:

- **Process Score Engine** — 11 weighted dimensions (total 100), no future data
- **Outcome Score Engine** — only available after explicit outcome reveal
- **Composite Score Engine** — process + optional outcome; PROCESS_ONLY before reveal
- **Mistake Taxonomy** — 31 mistake types across 6 categories
- **Mistake Detector** — SUGGESTED status only, never auto-confirmed
- **Mistake Review** — USER-only confirmation; SYSTEM_REVIEW cannot confirm
- **Outcome Reveal** — default BLOCKED; requires --reveal AND --confirm-review
- **Plan Adherence** — evaluates pre-session plan vs. actual decisions
- **Score Confidence** — DEMO_ONLY / INSUFFICIENT / OBSERVATIONAL / RELIABLE
- **Scoring Store** — append-only JSONL store under data/replay_scoring/
- **CLI Workflows** — 23 replay-scoring-* and replay-mistake-* commands
- **Reports** — session scoring report, mistake taxonomy report, scoring summary

## ID Conventions

| Prefix | Meaning |
|--------|---------|
| `PSC-` | Process Score |
| `OSC-` | Outcome Score |
| `CSC-` | Composite Score |
| `MIS-` | Mistake Record |
| `MRV-` | Mistake Review Record |
| `REV-` | Outcome Reveal Record |

## Scoring Lifecycle

```
Session Completed
      |
      v
[Process Score]  ← BEFORE outcome reveal (no future data)
      |
      v
[Outcome Reveal] ← EXPLICIT: --reveal --confirm-review flags required
      |           (default BLOCKED — never auto-revealed)
      v
[Outcome Score]  ← Only after confirmed reveal
      |
      v
[Composite Score] ← PROCESS_ONLY until outcome revealed
                     COMPOSITE after both available
```

## Process Score Dimensions

| Dimension | Weight |
|-----------|--------|
| Thesis Quality | 15 |
| Risk Planning | 15 |
| Discipline Checklist | 15 |
| Evidence Quality | 10 |
| Confirmation/Invalidation | 10 |
| Point-in-Time Integrity | 10 |
| Emotional Awareness | 5 |
| Revision Quality | 5 |
| Data Sufficiency | 5 |
| Scenario Objective | 5 |
| Session Completion | 5 |
| **Total** | **100** |

## Composite Classifications

| Classification | Meaning |
|----------------|---------|
| `PROCESS_ONLY` | Outcome not yet revealed |
| `GOOD_PROCESS_GOOD_OUTCOME` | Both above threshold |
| `GOOD_PROCESS_BAD_OUTCOME` | Good process, bad outcome (variance, luck) |
| `BAD_PROCESS_GOOD_OUTCOME` | Bad process, good outcome (luck, not skill) |
| `BAD_PROCESS_BAD_OUTCOME` | Both below threshold |

## Safety Invariants

- `SCORING_TRIGGERS_NO_ORDERS = True` — scoring never creates orders
- `AUTO_OUTCOME_REVEAL_ENABLED = False` — outcome never auto-revealed
- `AUTO_MISTAKE_CONFIRMATION_ENABLED = False` — mistakes never auto-confirmed
- `AUTO_SCORE_TO_TRADE_ENABLED = False` — scores never trigger trades
- `REPLAY_TRADE_EXECUTION_ENABLED = False` — no trade execution

## CLI Reference

```
python main.py replay-scoring-health
python main.py replay-score-process --session-id <ID>
python main.py replay-outcome-preview --session-id <ID>
python main.py replay-outcome-reveal --session-id <ID> --reveal --confirm-review
python main.py replay-score-outcome --session-id <ID> --reveal-id <REV-ID>
python main.py replay-score-composite --session-id <ID>
python main.py replay-mistakes-detect --session-id <ID>
python main.py replay-mistakes --session-id <ID>
python main.py replay-mistake-confirm --mistake-id <MIS-ID>
python main.py replay-mistake-dismiss --mistake-id <MIS-ID>
python main.py replay-plan-adherence --session-id <ID>
python main.py replay-scoring-summary
python main.py replay-scoring-report --session-id <ID>
python main.py replay-mistake-report --session-id <ID>
```

---
*[!] Research Only. Not Investment Advice. No Real Orders.*
