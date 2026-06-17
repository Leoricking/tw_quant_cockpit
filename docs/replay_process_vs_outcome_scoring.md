# Process vs Outcome Scoring in Replay Training

> **[!] Research Only. No Real Orders. Replay Training Only.**
> **[!] Process scores use NO future data, NO outcome, NO PnL.**
> **[!] Not Investment Advice.**

## Core Principle: Process-Outcome Separation

A core principle of the replay scoring system is the strict separation of process quality
from outcome quality. These are scored independently and combined only when explicitly
requested.

### Why Separate?

Good decisions can have bad outcomes (variance, bad luck). Bad decisions can have good
outcomes (luck, favorable randomness). Learning from outcomes alone teaches the wrong
lessons. The process score evaluates decision quality at the time of the decision.

### Process Score

The **process score** evaluates the quality of decision-making BEFORE knowing the outcome:

- Was the thesis documented?
- Was the risk plan defined?
- Was the checklist completed?
- Was evidence for and against considered?
- Were confirmation/invalidation conditions set?
- Was point-in-time integrity maintained?

**No future data is used.** Process scores can be calculated immediately after a session,
before any outcome data is reviewed.

### Outcome Score

The **outcome score** evaluates what actually happened AFTER the session:

- How did the trade play out vs. the plan?
- Did the invalidation conditions trigger correctly?
- Was the stop loss hit within the window?

**Outcome scores are BLOCKED by default.** They require an explicit `--reveal` AND
`--confirm-review` flag to prevent accidental hindsight contamination.

### Composite Score

The **composite score** combines both:

```
composite = process_weight * process_score + outcome_weight * outcome_score
```

Default weights: `process_weight=0.70`, `outcome_weight=0.30`.

Before outcome is revealed, the composite status is `PROCESS_ONLY` — not `COMPOSITE`.
A warning is shown if `outcome_weight > 0.50`.

## Interpretation

| State | Lesson |
|-------|--------|
| Good Process, Good Outcome | Correct behavior reinforced |
| Good Process, Bad Outcome | Variance — do not change the process |
| Bad Process, Good Outcome | Lucky — do not reinforce this pattern |
| Bad Process, Bad Outcome | Process needs improvement |

The critical insight: **do not change a good process because of a bad outcome.**

## Safety Notes

- The process score engine source code lists all forbidden fields:
  `realized_return`, `future_return`, `final_result`, `realized_pnl`, etc.
- These fields will never be used in process scoring.
- The outcome reveal requires explicit user action and flags.

---
*[!] Research Only. Not Investment Advice. No Real Orders.*
