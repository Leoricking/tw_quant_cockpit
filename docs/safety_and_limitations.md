# TW Quant Cockpit — Safety & Limitations (v0.3.23)

> **[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Not investment advice. REAL_ORDER_READY=False.**

---

## Hard-Coded Safety Invariants

The following constraints are hard-coded and cannot be overridden by configuration, environment variables, or CLI flags.

| Invariant | Value | Notes |
|-----------|-------|-------|
| `PRODUCTION_BLOCKED` | `True` | Always True; never changes |
| `REAL_ORDER_READY` | `False` | Always False; never changes |
| Read-only pipeline | `True` | No data files are modified by research |
| Auto weight application | `Disabled` | Signal quality results are never auto-applied |
| Auto trading | `Not implemented` | No trading engine exists |
| Live broker connection | `Not implemented` | Shioaji / Mega connections do not exist |

These invariants appear in every command's safety banner and in the Data Quality Gate output as a FATAL-severity blocker (`PRODUCTION_BLOCKED`). This blocker is expected and does not prevent research use.

---

## What the System WILL Do

| Capability | Details |
|-----------|---------|
| Read CSV data files | Historical OHLCV, institutional, margin, revenue |
| Fetch public data | Via FinMind API and TWSE public endpoints |
| Calculate signals | Rule-based signal scoring on historical data |
| Simulate portfolios | Backtest-style simulation using historical data only |
| Generate reports | Markdown reports saved to `reports/` directory |
| Display results | GUI cockpit and CLI output |
| Run smoke tests | Validate CLI/GUI output quality |

---

## What the System WILL NEVER Do

| Blocked Action | Reason |
|---------------|--------|
| Place any real order | PRODUCTION_BLOCKED=True; no broker API calls |
| Connect to Shioaji | Not implemented; no code path exists |
| Connect to Mega Securities | Not implemented; no code path exists |
| Auto-apply weight changes | Weights require manual review before adjustment |
| Provide investment advice | Research platform only; not a registered advisor |
| Modify historical data | All data reads are read-only |
| Send orders via any API | No order API, no order data structures |

---

## Read-Only Guarantee

The research pipeline (update-data → run-research → reports) operates as follows:

- **Data files (`data/`)** — read by the research pipeline, never modified
- **Update-data** — writes new data files (fetched from providers); does not modify existing rows
- **Reports (`reports/`)** — written by report builders; these are output artifacts only
- **No in-place modification** — existing data is never overwritten by analysis steps

The `--dry-run` flag on `update-data` disables even the write of new data files.

---

## Backtest Limitations

Backtests in this system are simulations using historical data. They have the following known limitations:

| Limitation | Detail |
|-----------|--------|
| Look-ahead bias | Not fully eliminated; research-grade only |
| Transaction costs | Simplified model; not broker-accurate |
| Liquidity | Not modeled; assumes fills at close price |
| Survivorship bias | Depends on data coverage; partial mitigation only |
| Mock contamination | Backtest Readiness capped at 60 if mock data detected |
| Coverage cap | Backtest Readiness capped at 70 if ticker coverage < 70% |

**Backtest results are for research purposes only.** Past simulated performance does not predict future returns.

---

## Signal Quality Limitations

- Signal quality recommendations (BOOST/KEEP/REDUCE/DISABLE) are computed from historical backtests.
- They represent statistical patterns in past data, not predictions.
- Single-day recommendations should not trigger weight changes.
- Weight changes require multi-period review and manual decision.

---

## Data Quality Limitations

| Data Source | Limitation |
|-------------|-----------|
| FinMind API | Requires token; rate-limited; historical depth varies |
| TWSE public data | Available with delay; format may change |
| XQ exports | Manual export required; stale if not updated |
| Institutional data | Delayed by 1 trading day |
| Monthly revenue | Released by 10th of following month |

---

## Mock Data Warning

Mock mode (`--mode mock`) uses synthetic or cached test data:
- Not representative of real market conditions
- Backtest Readiness Score is capped when mock data is detected
- Do not use mock mode results for any research decisions
- Mock mode is for development and testing only

---

## No Investment Advice

TW Quant Cockpit is a quantitative research tool, not a financial advisor.

- All outputs are research observations, not investment recommendations
- The system does not account for individual financial circumstances
- Past simulated performance does not guarantee future results
- All investment decisions require independent professional advice

---

## Safety Banner

Every CLI command outputs:

```
Read Only         : YES
No Real Orders    : YES
Production Trading: BLOCKED
Real Order Ready  : NO
```

The GUI shows an equivalent banner in every tab that cannot be dismissed.

---

*TW Quant Cockpit v0.3.23 — Research Only — Not Investment Advice*
