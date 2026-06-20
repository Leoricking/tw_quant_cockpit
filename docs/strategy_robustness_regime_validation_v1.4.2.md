# Strategy Robustness & Regime Validation — v1.4.2

> **[!] Research Only. No Real Orders. Production Trading: BLOCKED.**
> **[!] Robustness validation does NOT execute trades. Not Investment Advice.**
> **[!] Historical robustness does NOT guarantee future performance.**
> **[!] Formal conclusions require real data. Mock results are DEMO_ONLY.**

---

## Overview

v1.4.2 adds the **Strategy Robustness & Regime Validation** framework. It
consumes existing backtest results (v1.4.0) and A/B/C validation results
(v1.4.1) to answer a single question:

> Is the strategy robust — or does it only appear to work under narrow,
> specific conditions?

A single backtest result cannot answer this. Robustness validation runs
multiple independent stress tests, cross-sectional splits, rolling windows,
bootstrap confidence intervals, and failure-mode classifiers to produce a
multi-dimensional **Robustness Score** (0–100) and a **RobustnessStatus**
that clearly communicates what level of confidence the evidence supports.

---

## Why a Single Backtest Is Not Enough

A backtest can overfit to:

- A single profitable year
- A handful of high-performing symbols
- One industry sector that happened to rally
- Purely bull-market conditions
- A narrow parameter setting that only works at exactly that point
- Easily eroded by realistic costs and slippage

Robustness validation exposes these failure modes *before* they cost real money.

---

## Dimensions

### Time Robustness

Splits results by year, half-year, quarter, and rolling windows (60 / 120 /
250 trading days). Checks whether performance is concentrated in a single
period, whether recent windows are declining, and whether the strategy
direction reverses across windows.

### Cross-Sectional Robustness

Splits results by symbol, universe tier, and liquidity bucket. Detects whether
1–3 stocks drive the entire result, whether removing the best symbol causes
failure, and whether the majority of symbols are actually unprofitable.

### Industry Robustness

Groups results by industry and sector. Detects concentration in a single
supply chain, negative industry drag, and insufficient cross-industry
reproducibility. Missing metadata is tagged `INSUFFICIENT_DATA` — the system
never guesses an industry.

### Regime Robustness

Uses the existing `MarketRegimeClassifier` (v1.4.0) to split results into
BULL / BEAR / SIDEWAYS / HIGH_VOLATILITY / LOW_VOLATILITY / UNKNOWN. A
`RegimeDependencyScore` flags strategies that only work in bull markets or
that break down during sideways/bear regimes. **No future data is used to
classify the current regime.**

### Parameter Sensitivity

Tests a limited, explicit neighborhood around each parameter (±5%, ±10%,
adjacent discrete values). Detects performance cliffs, flat regions, and
single-point validity. Grid search, Bayesian optimization, and AutoML are
explicitly prohibited. **OOS data is never used to select parameters.**

### Cost Sensitivity

Tests the strategy at 1×, 1.25×, 1.5×, and 2× the baseline cost, plus a
conservative high-cost scenario. Outputs the break-even cost and the
cost-sensitivity slope. Flags strategies that fail under realistic brokerage
and tax assumptions.

### Slippage Sensitivity

Tests at 2 bps, 5 bps, 10 bps, and 20 bps slippage, plus a volume-aware
conservative case. Does not assume perfect fills.

### Trade Concentration

Calculates top-1, top-3, top-5, and top-10% trade contributions, plus
HHI-equivalent concentration scores. Runs remove-best-trade stress tests and
winsorized return analysis. If removing a small number of trades causes
strategy failure, status is downgraded to CONCENTRATED or FRAGILE.

### Bootstrap Confidence Intervals

Resamples trade outcomes to produce 90% and 95% confidence intervals for
expectancy, win rate, profit factor, mean return, and median return. Uses a
fixed deterministic seed. **Bootstrap does not guarantee trade independence —
this limitation is explicitly labeled in all outputs.**

### Monte Carlo Trade-Order Simulation

Shuffles trade order to simulate drawdown paths, recovery lengths, and ruin
probability. **Individual trade returns are never modified.** Produces
terminal capital distribution (5th / median / 95th percentile) and worst
simulated drawdown. Monte Carlo results are never presented as formal return
forecasts.

### Rolling Stability

Uses 60-day, 120-day, and 250-day rolling windows to compute rolling
expectancy, win rate, drawdown, and profit factor. Reports positive-window
ratio, negative-window ratio, and the longest consecutive negative streak.

### Strategy Decay Detection

Compares early vs. recent performance across multiple splits (train vs.
validation, first half vs. second half, prior folds vs. recent folds). Reports
a `DecayStatus`: NO_DECAY / POSSIBLE_DECAY / SIGNIFICANT_DECAY /
INSUFFICIENT_DATA / UNKNOWN. A short-term recent dip alone does not trigger
SIGNIFICANT_DECAY.

### Stress Scenarios

Runs pre-defined, reproducible stress scenarios: HIGH_COST, HIGH_SLIPPAGE,
LOW_LIQUIDITY, REDUCED_FILL_RATE, DELAYED_EXECUTION, REMOVE_TOP_TRADES,
BEAR_ONLY, SIDEWAYS_ONLY, HIGH_VOLATILITY_ONLY, SMALL_SAMPLE, DATA_GAPS,
CORPORATE_ACTION_UNCERTAIN. Each scenario has explicit parameters,
assumptions, and does not modify the original backtest result.

### Failure Mode Classification

Classifies identified weaknesses into: OVERFIT, REGIME_DEPENDENT,
PARAMETER_CLIFF, COST_EROSION, SLIPPAGE_EROSION, TRADE_CONCENTRATION,
SYMBOL_CONCENTRATION, INDUSTRY_CONCENTRATION, TIME_CONCENTRATION,
SAMPLE_TOO_SMALL, DATA_QUALITY_WEAK, FRESHNESS_WEAK, SURVIVORSHIP_RISK,
CORPORATE_ACTION_RISK, RECENT_DECAY, NO_OOS_SUPPORT,
WALK_FORWARD_INSTABILITY, UNKNOWN. Each failure mode includes severity,
evidence, affected metrics, and a recommended research action. **Recommended
actions are limited to research operations — BUY/SELL/TRADE/ORDER are
explicitly prohibited.**

---

## Robustness Score

A composite score from 0 to 100 across 14 dimensions:

| Range | Status |
|-------|--------|
| 80–100 | ROBUST |
| 65–79 | ACCEPTABLE |
| 45–64 | FRAGILE |
| 25–44 | HIGH_RISK |
| 0–24 | BLOCKED |

Penalties apply for concentration, cliff risk, recent decay, and insufficient
data. A high average return alone cannot produce a ROBUST score.

---

## Formal Conclusion Rules

A formal conclusion (`formal_conclusion_allowed=True`) requires **all** of:

1. Real data (not mock/fixture)
2. Data Quality gate pass
3. Freshness gate pass
4. No lookahead contamination
5. Corporate action pass
6. Sufficient symbols (configurable minimum)
7. Sufficient trades (configurable minimum)
8. Sufficient time span (configurable minimum)
9. At least one OOS period
10. Walk-forward not severely unstable
11. Robustness Score at or above threshold
12. No critical trade concentration
13. No critical parameter cliff

**Mock data produces DEMO_ONLY status. Mock formal conclusions are disabled.**

---

## A/B/C Robustness Comparison

`ABCRobustnessComparison` compares A vs. B vs. C buy point rules across
regime-specific, cost-sensitive, parameter-sensitive, recent vs. early, and
cross-industry splits. All comparisons use the same universe, date range,
execution model, costs, slippage, benchmark, and data quality profile. If
conditions differ, results are labeled as not directly rankable.

---

## Strategy Knowledge Comparison

Beyond A/B/C, the comparison engine supports any backtestable rule from the
Strategy Knowledge Registry (second wave, volume breakout, MA alignment,
institutional filter, margin filter, fundamental turnaround, composite rule).
Manual-only rules retain MANUAL_ONLY / NOT_BACKTESTABLE status and are never
force-converted to numeric rules.

---

## Repair Integration

When a robustness run is blocked by missing industry metadata, stale source
results, insufficient symbol count, or data gaps, the system can create
optional repair candidates via `RobustnessRepairIntegration`.

Rules:

- `create_repair_tasks=False` by default
- No automatic repair execution
- No automatic provider refresh or data download
- No mock fallback
- Uses `CoverageRepairQueue` for deduplication
- Re-running robustness validation is required after repair

---

## Replay Integration

`RobustnessReplayIntegration` exposes read-only evidence (robustness score,
regime dependency, parameter sensitivity, cost sensitivity, decay status,
formal conclusion status) to Replay sessions. It **never** modifies Replay
session scores, challenge questions, or rule parameters. The Replay v1.2.9
stable baseline is preserved unchanged.

---

## CLI

All commands default to dry-run. `--execute` must be explicitly specified for
write operations. No automatic parameter adjustment, repair, or download.

```
robustness-plan --rule-id <id>
robustness-run --rule-id <id> --dry-run
robustness-run --rule-id <id> --execute
robustness-show --robustness-id <id>
robustness-list
robustness-time --robustness-id <id>
robustness-symbols --robustness-id <id>
robustness-industries --robustness-id <id>
robustness-regimes --robustness-id <id>
robustness-parameters --robustness-id <id>
robustness-costs --robustness-id <id>
robustness-slippage --robustness-id <id>
robustness-concentration --robustness-id <id>
robustness-bootstrap --robustness-id <id>
robustness-monte-carlo --robustness-id <id>
robustness-decay --robustness-id <id>
robustness-stress --robustness-id <id>
robustness-failure-modes --robustness-id <id>
robustness-compare --robustness-id <id> --robustness-id <id>
abc-robustness-compare
robustness-create-repair --robustness-id <id>
robustness-report --robustness-id <id>
robustness-health
```

Each output includes:
- Application Version, Rule ID, Rule Version
- Universe, Date Range, Symbols, Industries, Regimes, Trades
- All dimension stability scores
- Bootstrap CI, Monte Carlo Risk
- Decay Status, Failure Modes
- Robustness Score, Robustness Status, Confidence
- Formal Conclusion Allowed
- No Real Orders / Broker Execution Disabled / Production Trading BLOCKED

---

## GUI

**Strategy Robustness Panel** (`gui/strategy_robustness_panel.py`) provides:

- **Safety Banner**: Research Only / No Real Orders / Broker Disabled /
  Production Trading BLOCKED / Historical Robustness Does Not Guarantee Future
  Performance
- **Configuration**: rule, source backtest, source A/B/C validation, universe,
  date range, rolling window, bootstrap/monte carlo iterations, cost/slippage
  multipliers, parameter neighborhood, stress scenarios
- **Summary Cards**: Robustness Score, Status, Time Stability, Symbol
  Stability, Industry Stability, Regime Stability, Parameter Stability, Cost
  Resilience, Decay Status, Formal Conclusion
- **16 Tabs**: Overview / Time / Symbols / Industries / Regimes / Parameters /
  Costs / Slippage / Concentration / Bootstrap / Monte Carlo / Rolling
  Stability / Decay / Stress Scenarios / Failure Modes / Provenance
- **Actions**: Build Dry Run Plan / Run Robustness / Compare Rules / Compare
  A/B/C / Run Stress Tests / Create Repair Tasks / Export Report / Refresh
- Nav tab ID: `strategy_robustness` (group: research, priority: P1)
- Default dry-run; no Buy/Sell/Order; QThread cleaned on close

---

## Safety

| Flag | Value |
|------|-------|
| No Real Orders | True |
| Broker Execution Enabled | False |
| Production Trading BLOCKED | True |
| Formal Conclusion Requires Real Data | True |
| Mock Formal Conclusion Allowed | False |
| Auto Optimization Enabled | False |
| Auto Trading Enabled | False |
| Mock Fallback Enabled | False |
| Replay Score Modification | False |

Robustness results are **never** converted to trading recommendations, order
signals, or broker instructions.

---

## Known Limitations

- Bootstrap assumes trade independence (labeled as a limitation in all outputs)
- Monte Carlo does not model portfolio-level correlation
- Industry metadata may be incomplete for some symbols (tagged INSUFFICIENT_DATA)
- Corporate action adjustments depend on provider accuracy
- Historical robustness does not guarantee future performance
- Formal conclusions require real market data — mock data produces DEMO_ONLY

---

## Next Version

- v1.4.3: Forum Intelligence & Market Sentiment
- v1.5.0: Stock Screening & Precise Price Validation
- v1.5.1: GUI Decision Cockpit Integration
