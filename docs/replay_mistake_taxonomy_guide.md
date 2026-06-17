# Replay Mistake Taxonomy Guide

> **[!] Research Only. No Real Orders. Replay Training Only.**
> **[!] Mistake taxonomy is for training pattern recognition, not psychological diagnosis.**
> **[!] WAIT/SKIP with good rationale is NOT a mistake.**
> **[!] Planned stop is NOT PANIC_SELL. Single loss != mistake.**
> **[!] Not Investment Advice.**

## Overview

The mistake taxonomy provides a structured vocabulary for classifying decision errors
during replay training sessions. All mistakes start as SUGGESTED and require USER
confirmation before being treated as confirmed.

## Mistake Categories

### Entry Mistakes
| Type | Description |
|------|-------------|
| `CHASING_BREAKOUT` | Entered after breakout already extended |
| `ENTERING_WITHOUT_CONFIRMATION` | Entered before confirmation conditions met |
| `IGNORING_INVALIDATION_CONDITIONS` | Entered despite invalidation signal |
| `OVERSIZING_ENTRY` | Position size exceeds risk plan |
| `ENTERING_AGAINST_TREND` | Entered against primary trend without documented reason |
| `SKIPPING_VALID_SETUP` | Missed a setup that met all criteria |

### Exit Mistakes
| Type | Description |
|------|-------------|
| `PANIC_SELL` | Exited due to emotion, not plan |
| `EXITED_TOO_EARLY` | Exited before plan target reached |
| `HOLDING_TOO_LONG` | Held past documented exit criteria |
| `IGNORING_STOP_LOSS` | Did not exit at planned stop level |
| `MISSING_TARGET_EXIT` | Did not exit at planned target level |

### Risk Mistakes
| Type | Description |
|------|-------------|
| `NO_STOP_DEFINED` | No stop loss documented in risk plan |
| `RISK_REWARD_IGNORED` | Risk/reward ratio not evaluated |
| `OVERSIZING_POSITION` | Position exceeds documented size limits |
| `ADDING_TO_LOSER` | Added to losing position without plan |
| `CONCENTRATION_RISK_IGNORED` | Portfolio concentration not checked |

### Process Mistakes
| Type | Description |
|------|-------------|
| `SKIPPED_CHECKLIST` | Discipline checklist not completed |
| `NO_THESIS_DOCUMENTED` | No written thesis for the decision |
| `INSUFFICIENT_EVIDENCE` | Insufficient evidence for/against |
| `REVISED_PLAN_MID_TRADE` | Plan changed after entry without documented reason |
| `IGNORED_INVALIDATION_SIGNAL` | Ignored own invalidation conditions |

### Emotional Mistakes (Self-Reported / Rule-Triggered Only)
| Type | Description |
|------|-------------|
| `FOMO_ENTRY` | Entered due to fear of missing out |
| `REVENGE_TRADE` | Entered to recover prior loss |
| `OVERCONFIDENCE` | Oversized due to prior wins |
| `LOSS_AVERSION_HOLD` | Held losing position to avoid realizing loss |
| `ANCHORING_BIAS` | Decision anchored to prior price |

### Data Quality Mistakes
| Type | Description |
|------|-------------|
| `FUTURE_DATA_RISK` | Evidence may contain future-looking data |
| `STALE_DATA_USED` | Decision based on stale/outdated data |

## Critical Exclusions

The following actions are NEVER classified as mistakes by the system:

| Action | Reason |
|--------|--------|
| `WAIT` with documented rationale | Disciplined patience is correct behavior |
| `SKIP` with documented no-trade conditions | Avoiding bad setups is correct |
| `STOP` with risk_plan_id present | Planned stop is NOT PANIC_SELL |
| `REDUCE` with plan documentation | Planned reduce is NOT EXITED_TOO_EARLY |

## Mistake Lifecycle

```
System Detects → SUGGESTED
                      |
           USER Reviews (required)
                 /          \
         CONFIRMED          DISMISSED
              |                 |
           REOPENED         (preserved)
              |
          CONFIRMED
```

- **SUGGESTED**: Initial state. System cannot advance past this automatically.
- **NEEDS_REVIEW**: Flagged for explicit review.
- **CONFIRMED**: USER has confirmed this is a mistake.
- **DISMISSED**: USER has determined this is not a mistake.
- **OVERRIDDEN**: USER has changed the type or severity.
- **REOPENED**: Previously dismissed, now under review again.

## Severity Levels

| Level | Meaning |
|-------|---------|
| `LOW` | Minor process gap, unlikely to affect outcomes |
| `MEDIUM` | Meaningful process gap |
| `HIGH` | Significant deviation from plan |
| `CRITICAL` | Violated core risk rule |

## Using the CLI

```bash
# Detect mistakes (all SUGGESTED)
python main.py replay-mistakes-detect --session-id <ID>

# List mistakes for review
python main.py replay-mistakes --session-id <ID>

# Confirm a mistake (USER only)
python main.py replay-mistake-confirm --mistake-id MIS-XXXXXX

# Dismiss a mistake
python main.py replay-mistake-dismiss --mistake-id MIS-XXXXXX

# Override type/severity
python main.py replay-mistake-override --mistake-id MIS-XXXXXX --type HOLDING_TOO_LONG

# Reopen dismissed mistake
python main.py replay-mistake-reopen --mistake-id MIS-XXXXXX

# Mistake taxonomy report
python main.py replay-mistake-report --session-id <ID>
```

---
*[!] Research Only. Not Investment Advice. No Real Orders.*
