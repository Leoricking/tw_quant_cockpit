# Replay Review Workflow v1.2.6

> [!] Research Only. No Real Orders. Not Investment Advice.

## Overview

The replay review workflow separates process quality from outcome quality.
Outcome is hidden by default and requires explicit user reveal.

## Step-by-Step Workflow

### Required Steps (for Process Review Complete)

1. **Session Completed** — Complete the replay session
2. **Journal Exists** — Ensure decision journal entry is present
3. **Process Score Calculated** — Calculate process score (no future data)
4. **Suggested Mistakes Reviewed** — Review suggested mistakes (suggested only)
5. **Strategy Conflicts Reviewed** — Review strategy conflicts (training only)
6. **Timeframe Conflicts Reviewed** — Review MTF conflicts (training only)
7. **Point-in-Time Verified** — Verify no future data leakage
8. **Review Note Added** — Add final review note

### Optional Steps

- **Outcome Reveal** — Explicitly reveal outcome (user action required)
- **Outcome Score Calculated** — Calculate outcome score (after reveal)
- **Composite Score Calculated** — Calculate composite classification
- **Final Report Generated** — Generate session report

## Key Safety Rules

- `PROCESS_REVIEW_COMPLETE` does NOT require Outcome Reveal
- Outcome score is hidden until explicit reveal
- Suggested mistakes are NOT auto-confirmed
- Strategy conflicts are training-only (no auto-trade, no auto-block)
- Batch operations are preview by default
- Missing modules show UNAVAILABLE (no crash)

## CLI Commands

```
python main.py replay-review-health
python main.py replay-review-dashboard --mode real
python main.py replay-review-progress --session-id SES-001
python main.py replay-review-checklist --session-id SES-001
python main.py replay-review-queue
python main.py replay-review-summary
```

## Not Investment Advice
