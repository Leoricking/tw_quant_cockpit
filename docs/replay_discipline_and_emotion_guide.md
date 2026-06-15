# Replay Discipline and Emotional State Guide v1.2.2

> **[!] Research Only. No Real Orders. Simulation Decision Only.**
> **[!] Self-reported only. NOT a psychological assessment.**
> **[!] This guide is for replay simulation training only.**

## Discipline Checklist

The discipline checklist records your decision process across 5 categories.

### Categories and Items

**DATA (4 items)**
- DATA-001: Historical price data loaded and verified [REQUIRED]
- DATA-002: Volume data available
- DATA-003: No forward-looking data present [REQUIRED]
- DATA-004: Correct replay date confirmed [REQUIRED]

**SETUP (4 items)**
- SETUP-001: Setup type clearly identified [REQUIRED]
- SETUP-002: Key support/resistance levels noted
- SETUP-003: Trend direction assessed
- SETUP-004: Market context reviewed

**RISK (5 items)**
- RISK-001: Stop level defined [REQUIRED]
- RISK-002: Target level defined
- RISK-003: Risk/reward ratio considered [REQUIRED]
- RISK-004: Position size noted
- RISK-005: Maximum loss amount noted

**EMOTION (5 items)**
- EMOT-001: Emotional state recorded [REQUIRED]
- EMOT-002: Cognitive bias flags reviewed
- EMOT-003: FOMO check performed
- EMOT-004: Revenge trading check performed
- EMOT-005: Overconfidence check performed

**DISCIPLINE (5 items)**
- DISC-001: Decision rationale written [REQUIRED]
- DISC-002: No chasing moves
- DISC-003: Plan before entry
- DISC-004: No overriding stop plan
- DISC-005: Pre/post notes completed

### Evaluation

- All required items must pass for `all_required_passed=True`.
- Failed required items appear in `blocked_items`.
- The checklist records process only — no trading signals, no auto-execution.

## Emotional State Capture

### Overview

Emotional state is self-reported by the researcher during replay simulation.

**This is not:**
- A psychological assessment
- A clinical evaluation
- A diagnostic tool
- A trading signal

### Sliders (0-100)

| Slider | Description |
|--------|-------------|
| Confidence | How confident are you in this decision? (0=none, 100=very high) |
| Anxiety | How anxious are you feeling? (0=calm, 100=very anxious) |
| Focus | How focused are you right now? (0=very distracted, 100=very focused) |

Values outside 0-100 are rejected with `ValueError`.

### Primary Emotion

Select the emotion that best describes your current state:

`NEUTRAL`, `CALM`, `CONFIDENT`, `UNCERTAIN`, `ANXIOUS`, `FEARFUL`,
`GREEDY`, `FRUSTRATED`, `IMPATIENT`, `EXCITED`, `FATIGUED`, `OTHER`

### Cognitive Bias Flags

Self-report which biases may be present. Only KNOWN_BIASES are accepted.

Known biases (17 total):

| Bias | Description |
|------|-------------|
| FOMO | Fear of missing out on a move |
| REVENGE_TRADING | Trading to recover losses |
| CONFIRMATION_BIAS | Seeking only confirming evidence |
| ANCHORING | Over-reliance on initial price reference |
| OVERCONFIDENCE | Excessive confidence in outcome |
| LOSS_AVERSION | Fear of loss exceeding rational risk assessment |
| RECENCY_BIAS | Over-weighting recent events |
| AVAILABILITY_BIAS | Over-weighting easily recalled events |
| HINDSIGHT_BIAS | Believing outcome was predictable |
| NARRATIVE_FALLACY | Building story around data pattern |
| GAMBLER_FALLACY | Believing past results affect future probability |
| STATUS_QUO_BIAS | Preference for current position |
| SUNK_COST_FALLACY | Holding because of past investment |
| HERD_MENTALITY | Following crowd |
| OPTIMISM_BIAS | Over-estimating positive outcomes |
| PLANNING_FALLACY | Under-estimating time/difficulty |
| DUNNING_KRUGER | Over-estimating own competence |

Unknown bias names raise `ValueError` — this prevents informal naming from
polluting the bias record.

## Self-Reported Risk Detection

The system can detect self-reported risk patterns:

- `SELF_REPORTED_FOMO`: FOMO flag checked + anxiety > 70
- `SELF_REPORTED_REVENGE_RISK`: REVENGE_TRADING flag + frustration emotion
- `SELF_REPORTED_OVERCONFIDENCE`: confidence_level > 90 + OVERCONFIDENCE flag

These are informational flags only. No trading decisions are made from them.

## Important Disclaimers

- All emotional data is research and training only.
- No psychological conclusions should be drawn from this data.
- This is not a substitute for professional support.
- Simulation decisions made here are not real trades.
