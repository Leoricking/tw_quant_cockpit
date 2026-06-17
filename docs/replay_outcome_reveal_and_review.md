# Outcome Reveal and Review Guide

> **[!] Research Only. No Real Orders. Replay Training Only.**
> **[!] Outcome reveal is EXPLICIT ONLY — default BLOCKED.**
> **[!] Reveal does NOT modify the original session snapshot or journal entry.**
> **[!] AUTO_OUTCOME_REVEAL_ENABLED = False (invariant — never changes).**
> **[!] Not Investment Advice.**

## Overview

Outcome reveal is the process of unlocking post-session outcome data for a completed
replay session. This allows users to see what actually happened after their decision
point, compare outcome to process quality, and build composite scores.

## Why Default BLOCKED?

The purpose of replay training is to practice decision-making in a forward-only context.
Seeing outcomes prematurely contaminates the training signal and introduces hindsight bias.

The system defaults to BLOCKED so users must make an explicit, deliberate choice to
reveal outcomes — signaling they have already completed their process review.

## Reveal Requirements

A reveal requires **both** flags simultaneously:

| Flag | Purpose |
|------|---------|
| `--reveal` | Explicit intent to reveal |
| `--confirm-review` | Confirms process review is complete |

With only one flag, the reveal is BLOCKED. This is intentional.

## What Reveal Does

When both flags are provided and the session is eligible:

1. Creates an `OutcomeRevealRecord` in the scoring store
2. Records the reveal window (default: 20 bars after session end)
3. Sets `status = REVEALED`
4. Sets `reveal_confirmed = True`
5. Sets `confirm_review_flag = True`
6. **Does NOT modify** the original session, state, or journal entries

## What Reveal Does NOT Do

- Does NOT modify original session snapshot (`original_snapshot_unchanged = True`)
- Does NOT modify original journal entries (`original_journal_unchanged = True`)
- Does NOT auto-trigger outcome scoring
- Does NOT trigger any trade or paper order
- Does NOT auto-confirm mistakes

## Session Eligibility

A session is eligible for reveal if:

- Session status is `COMPLETED`
- No prior confirmed reveal exists for this session

Preview eligibility without revealing:

```bash
python main.py replay-outcome-preview --session-id <ID> --window 20
```

## Reveal Window

The reveal window (default: 20 bars) controls how many bars after the session end
date are included in the outcome view. A larger window shows more of what happened
after the decision point.

## CLI Workflow

```bash
# Step 1: Complete process scoring first
python main.py replay-score-process --session-id <ID>

# Step 2: Preview reveal eligibility (no actual reveal)
python main.py replay-outcome-preview --session-id <ID>

# Step 3: Reveal outcome (both flags required)
python main.py replay-outcome-reveal --session-id <ID> --reveal --confirm-review

# Step 4: Score outcome (requires reveal ID from step 3)
python main.py replay-score-outcome --session-id <ID> --reveal-id <REV-ID>

# Step 5: Build composite score
python main.py replay-score-composite --session-id <ID>
```

## Composite Score After Reveal

Before reveal: `status = PROCESS_ONLY`, `classification = PROCESS_ONLY`

After reveal: `status = COMPOSITE`, classification is one of:
- `GOOD_PROCESS_GOOD_OUTCOME`
- `GOOD_PROCESS_BAD_OUTCOME`
- `BAD_PROCESS_GOOD_OUTCOME`
- `BAD_PROCESS_BAD_OUTCOME`

## Safety Invariants

The following are enforced in code and cannot be overridden:

```python
AUTO_OUTCOME_REVEAL_ENABLED = False     # Never auto-reveal
original_snapshot_unchanged = True      # Never modify original
original_journal_unchanged = True       # Never modify journal
auto_outcome_reveal_enabled = False     # On every reveal record
```

---
*[!] Research Only. Not Investment Advice. No Real Orders.*
