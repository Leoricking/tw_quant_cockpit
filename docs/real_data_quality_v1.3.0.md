# Real Data Quality Foundation v1.3.0

**Research Only. No Real Orders. No Broker. Not Investment Advice.**

---

## Overview

The Real Data Quality Foundation (v1.3.0) provides a centralized, deterministic data quality
validation system for TW Quant Cockpit. It enforces strict rules about data mode, source
trustworthiness, price validity, freshness, and cross-source consistency.

---

## Status Codes

| Status | Meaning | Action |
|--------|---------|--------|
| `PASS` | Score 85-100, no critical issues | Analysis allowed |
| `DEGRADED` | Score 65-84, non-critical issues | Analysis allowed with limitations |
| `BLOCKED` | Critical issue OR score < 65 | No precise prices, no formal recommendations |
| `UNAVAILABLE` | No data source connected | Real data unavailable — no mock fallback |

---

## Data Modes

| Mode | Label | Description |
|------|-------|-------------|
| `REAL` | `REAL_DATA` | Real market data from identified, non-mock source |
| `MOCK` | `DEMO_ONLY` | Simulated/demo data — always labeled DEMO_ONLY |
| `UNAVAILABLE` | `UNAVAILABLE` | No data source — no fallback |

**MOCK mode always displays DEMO_ONLY label.** It is never substituted for REAL mode.

---

## Why Real Mode Has No Mock Fallback

Real mode (`data_mode=REAL`) never falls back to mock data. This is a hard safety rule:

- Mock data labeled as Real would mislead analysis and potentially trading decisions.
- If a Real source is unavailable, the system returns `UNAVAILABLE` — not mock data.
- This prevents "demo data masquerading as production data."

**Rule:** Real mode + mock/unknown source = `BLOCKED`. Always.

---

## When Precise Prices Are Blocked

Precise price generation is disabled when:

1. Quality status is `BLOCKED` or `UNAVAILABLE`
2. A `CRITICAL` severity issue exists (e.g., OHLC violation, close = 0, mock source in REAL mode)
3. Cross-source price conflict > 5% between sources
4. Quality score < 85 (PASS threshold)

When blocked, the system shows `DATA QUALITY BLOCKED` with specific reasons.

---

## Quality Score (0-100)

The score is **deterministic** — same inputs always produce the same score.

| Category | Weight |
|----------|--------|
| Core price completeness | 25 |
| Data freshness | 20 |
| OHLCV history depth | 15 |
| Technical indicators | 10 |
| Chips / institutional data | 10 |
| Fundamentals | 10 |
| Source trustworthiness | 5 |
| Cross-source consistency | 5 |

**CRITICAL issue cap:** Any `CRITICAL` severity issue caps the score at **49** (forces BLOCKED).

---

## How to Run the CLI

```
# Check data quality for a symbol (returns UNAVAILABLE if no real source)
python main.py data-quality --symbol 2330

# Check with a specific completeness profile
python main.py data-quality --symbol 2330 --profile precise_price

# Output as JSON
python main.py data-quality --symbol 2330 --json

# Run system health check
python main.py real-data-quality-health
```

**Exit codes:**
- `0` — PASS or DEGRADED
- `1` — BLOCKED or UNAVAILABLE
- `2` — Usage error (missing --symbol or --all)

---

## How to Read the Quality Score

```
Quality Score: 72/100
Quality Status: DEGRADED
```

| Score | Status | Interpretation |
|-------|--------|----------------|
| 85-100 | PASS | All required data present and fresh |
| 65-84 | DEGRADED | Non-critical fields missing or slightly stale |
| 1-64 | BLOCKED | Core data issues — do not use for precise analysis |
| 0 | UNAVAILABLE | No data at all |

---

## Completeness Profiles

| Profile | Use Case | Key Requirements |
|---------|----------|------------------|
| `stock_screening` | Screening candidates | symbol, OHLCV, MA5/10/20, volume |
| `precise_price` | Precise entry/exit levels | OHLCV, MA5/10/20/60, real source, timestamp |
| `backtest` | Historical strategy testing | Continuous OHLCV, no duplicate bars |
| `abc_buy_point` | A/B/C buy point analysis | OHLCV, MA5/10/20, KD, institutional direction |

**A/B/C profile note:** Never auto-judges buy point. Returns `insufficient_data` when
data does not meet minimum requirements. Manual review always required.

---

## Safety Rules

- `NO_REAL_ORDERS = True` — no order submission, no broker API
- `MOCK_FALLBACK_ENABLED = False` — never enabled, never changeable
- Real mode with mock source → always `BLOCKED`
- `UNAVAILABLE` → no mock substitution, ever
- NaN indicators → never silently converted to 0 (flagged as issue)
- Missing chips → never assumed to be zero
- Cross-source conflict → never silently pick one; conflict is reported

---

*v1.3.0 — Real Data Quality Foundation. Not Investment Advice.*
