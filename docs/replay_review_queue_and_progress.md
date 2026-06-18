# Replay Review Queue and Progress v1.2.6

> [!] Research Only. No Real Orders. Not Investment Advice.

## Review Queue

### Queue Item Types

| Type | Description |
|---|---|
| `OUTCOME_REVEAL_PENDING` | Session awaiting outcome reveal (optional) |
| `MISTAKE_REVIEW_PENDING` | Suggested mistakes awaiting review |
| `STRATEGY_RULE_REVIEW_PENDING` | Strategy rule conflicts awaiting review |
| `TIMEFRAME_CONFLICT_REVIEW` | MTF conflicts awaiting review |
| `LOW_CONFIDENCE_REVIEW` | Low confidence sessions |
| `INSUFFICIENT_DATA_REVIEW` | Insufficient data sessions |
| `POINT_IN_TIME_REVIEW` | PIT integrity issues |
| `REPORT_MISSING` | Missing session reports |
| `SESSION_INCOMPLETE` | Incomplete sessions |
| `OTHER` | Other review items |

### Priority Levels

- **P0** — Critical (data leak, outcome visible before reveal)
- **P1** — High (store corrupted, required module unavailable)
- **P2** — Normal (most review items)
- **P3** — Low (optional items)

### Queue Actions

| Action | Notes |
|---|---|
| `start_review` | Mark as IN_REVIEW |
| `complete` | Mark as COMPLETED — does NOT auto-confirm/auto-reveal |
| `dismiss` | Mark as DISMISSED with reason |
| `block` | Mark as BLOCKED with reason |
| `reopen` | Reopen COMPLETED/DISMISSED/BLOCKED item |

**[!] complete() does NOT auto-confirm mistakes or auto-reveal outcomes.**

## Review Progress

### Required Steps (8)

1. session_completed
2. journal_exists
3. process_score_calculated
4. suggested_mistakes_reviewed
5. strategy_conflicts_reviewed
6. timeframe_conflicts_reviewed
7. point_in_time_verified
8. review_note_added

### Optional Steps (4)

1. outcome_revealed
2. outcome_score_calculated
3. composite_score_calculated
4. final_report_generated

### Status Values

| Status | Meaning |
|---|---|
| `NOT_STARTED` | No required steps completed |
| `IN_PROGRESS` | Some required steps completed |
| `REVIEW_COMPLETE` | All required steps completed |
| `BLOCKED` | A step is blocked |
| `INSUFFICIENT` | Insufficient data to calculate |

**[!] PROCESS_REVIEW_COMPLETE does NOT require Outcome Reveal.**
**[!] outcome_reveal_required = False always.**

## Not Investment Advice
