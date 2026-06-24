# Portfolio Walk-forward Backtest v1.5.4

## Version Positioning

TW Quant Cockpit v1.5.4 introduces Portfolio Walk-forward Backtest as a pure research tool.
This version builds on v1.5.3 Drawdown & Risk Controls and adds historical simulation capability.

**Base Release**: v1.5.3 Drawdown & Risk Controls
**Baseline**: PORTFOLIO_WALK_FORWARD_BASELINE = "1.5.4"

## Research-Only Declaration

```
HISTORICAL_SIMULATION_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True
NO_FORMAL_LEDGER_WRITE = True
NO_AUTO_APPLY = True
NO_LIVE_REBALANCE = True
PRODUCTION_TRADING_BLOCKED = True
```

All results are for research and educational purposes only. Past performance is not a
guarantee of future results. This module does not create orders, connect to brokers,
write to formal ledgers, or automatically apply any strategy changes.

## Walk-forward Window Types

### Rolling Windows
- Training window has fixed length (e.g., 252 days)
- Steps forward by `step_length` (e.g., 21 days)
- Standard walk-forward methodology
- Last window marked PARTIAL if insufficient validation data

### Expanding Windows
- Training start is fixed (anchored to start_date)
- Training end grows with each step
- Grows the in-sample period over time
- Useful for studying information accumulation effects

### Anchored Windows
- Training always starts at anchor_date
- Validation period shifts forward by step_length
- Alternative to full expanding window

## Purge and Embargo

### Purge Period
- Buffer between training_end and validation_start
- Prevents label leakage (e.g., forward returns computed at training boundary)
- `purge_length` calendar days (0 = no purge)

### Embargo Period
- Buffer after validation_end before next window's training data is used
- Prevents cross-contamination from stale signals
- `embargo_length` calendar days (0 = no embargo)

## As-of Reconstruction

Historical portfolio reconstruction enforces PIT (Point-in-Time) integrity:

- `available_from <= as_of` enforced for all data inputs
- Future transactions, future prices, future classifications: ALL BLOCKED
- `fetched_at` is NOT accepted as a proxy for `available_from`
- Each window is validated independently

## Decision Replay

Decisions are replayed using current engine logic applied to historical data.

**Disclosure**: `["HISTORICAL_REPLAY", "CURRENT_ENGINE_APPLIED_TO_HISTORICAL_DATA"]`

Steps:
1. Portfolio reconstruction (as-of date)
2. Eligibility check
3. Sizing replay (PIT-safe)
4. Correlation replay (training window data only)
5. Risk control replay (simulation only)
6. Policy application
7. Hypothetical transaction proposal

## Simulation Ledger

All transactions are:
- `SIMULATION_ONLY` — not real orders
- `NOT_REAL_ORDER` — cannot be executed
- `research_only=True`
- `executable=False`
- `real_order_created=False`
- `formal_ledger_persisted=False`

Transaction types: HYPOTHETICAL_BUY, HYPOTHETICAL_SELL, HYPOTHETICAL_HOLD,
CASH_DEPOSIT, CASH_WITHDRAWAL, DIVIDEND, FEE, TAX, CORPORATE_ACTION

## Execution Timing Assumptions

- `SAME_CLOSE`: Decision executed at same day's close (look-ahead risk)
- `NEXT_OPEN`: Decision executed at next trading day's open (recommended)
- `NEXT_CLOSE`: Decision executed at next trading day's close

Default assumption: NEXT_CLOSE. Look-ahead prevention enforced.

## Costs, Tax, Slippage, Liquidity

### Costs
- Taiwan: buy fee 0.1425%, sell fee 0.1425%, transaction tax 0.3% (sell only)
- Minimum fee: TWD 20 per transaction
- Decimal precision enforced (Python Decimal)

### Slippage
- NONE_DISCLOSED: no slippage (optimistic, must be disclosed)
- FIXED_BPS: fixed basis points (e.g., 5 bps)
- VOLUME_PARTICIPATION: market impact from ADV participation
- VOLATILITY_ADJUSTED: volatility-scaled impact
- Missing ADV → BLOCKED
- No negative slippage without explicit price improvement flag

### Liquidity
- Maximum research quantity based on ADV × participation_rate
- Partial fills are hypothetical and simulation_only
- Suspended stocks → BLOCKED
- Missing ADV → BLOCKED

## Partial Fills

Partial fill simulation:
- `partial_fill=True` when quantity > max_research_quantity
- Partial fill quantity = min(requested, ADV × participation_rate)
- Always marked `simulation_only=True`

## Sizing Replay

- ATR_STOP_DISTANCE: primary method
- Uses historical ATR, volatility, price, stop from context
- PIT-safe: only uses data available at decision date

## Correlation Replay

- ROLLING_CORRELATION: 60-day rolling window (training data only)
- Minimum observations check (20 trading days minimum)
- PARTIAL status if insufficient observations

## Risk Control Replay

Simulation-only risk actions:
- FREEZE_NEW_BUYS: block new buy proposals in simulation
- REDUCE_NEW_POSITION_SIZE: scale down new position size proposals
- BLOCK_NEW_SIZING: block all new sizing proposals

Permanently blocked (never executed):
- AUTO_SELL, BROKER_CALL, REAL_ORDER, FORMAL_LEDGER_WRITE, LIVE_REBALANCE

## Valuation

- Missing price → `positions[symbol] = None` (partial status)
- Do NOT substitute 0 or last-known price silently
- `status = "PARTIAL"` when any price missing

## Returns Calculation

- Minimum 2 observations for returns
- Minimum 3 observations for volatility
- TWR: product of (1 + period_return) - 1
- Sharpe-like ratio: only computed if n >= 12, with assumption disclosure

## Benchmark

- PIT-safe: as_of boundary enforced
- Missing benchmark → BLOCKED
- Fixture demo mode: deterministic pseudo-returns

## Drawdown Calculation

- Peak-to-trough rolling calculation
- Underwater series computed for all dates
- Recovery date tracked separately from trough date

## Turnover

- Turnover rate = (total_buys + total_sells) / 2
- Tracked by window and overall

## Train/Validation Separation

- Training metrics: computed from training window data only
- Validation metrics: computed from out-of-sample validation window
- No data leakage across purge/embargo boundary
- Degradation = out_of_sample_return - in_sample_return (exploratory label only)

## Stability Analysis

Score formula (version="1.5.4"):
```
score = positive_ratio × 40 + (1 - dispersion_normalized) × 30 + (1 - worst_drawdown_normalized) × 30
```

- Missing component → None (not 0)
- Score range: 0-100
- No future performance guarantee

## Parameter Sensitivity

Supported parameters:
- sizing_risk_pct, stop_distance, atr_multiplier, max_position_weight
- max_cluster_weight, drawdown_warning_threshold, cash_reserve, correlation_threshold

Grid: fixed, deterministic
Cliff effect: adjacent values differ by > 50% in return
selection_applied = False ALWAYS

## Regime Segmentation

Decision-time regime (PIT-safe):
- BULLISH: benchmark_return > 5% annualized
- BEARISH: benchmark_return < -5% annualized
- HIGH_VOLATILITY: volatility > 25%
- LOW_VOLATILITY: volatility < 10%
- SIDEWAYS: abs(return) < 2%
- LIQUIDITY_STRESS: explicit flag
- UNKNOWN: else

Ex-post regime is separate from decision-time regime.

## Eligibility Gate

Non-boolean structured output:
- `run_allowed`: bool
- `window_generation_allowed`: bool
- `decision_replay_allowed`: bool
- And 5 more component-level flags

## PIT Validation

- `available_from <= as_of` required for ALL data types
- `fetched_at` rejected as proxy for `available_from`
- Each window validated independently
- Data types: prices, returns, classifications, ETF holdings, benchmark,
  ATR, volatility, correlation, risk_policy, sizing_policy, corporate_actions

## Lineage

Full lineage tracked for:
- Config, windows, decisions, transactions, snapshots
- Price, universe, classification, ETF holdings, benchmark
- Policies, cost model, slippage model, calculation version, code commit

Orphan windows, decisions, transactions → BLOCKED

## Reproducibility

- Config hash, window hashes, decision hashes, dataset hashes, result hashes
- Python version, dependencies, timezone, calendar version
- Fixed seed = 42 for any random operations
- Hash mismatch → BLOCKED

## Explainability

Full explanation covers:
- Configuration, windows summary, purge/embargo, timing assumptions
- Reconstruction method, sizing method, correlation constraints
- Risk controls, costs, slippage, liquidity, window results
- Degradation, stability, sensitivity, regimes, benchmark
- Drawdown, turnover, warnings, blockers, limitations, safety text

## CLI Commands

29 new CLI commands (all research-only):
portfolio-walk-forward-health, walk-forward-configs, walk-forward-config-show,
walk-forward-eligibility, walk-forward-windows, walk-forward-reconstruct,
walk-forward-decision-replay, walk-forward-sizing-replay,
walk-forward-correlation-replay, walk-forward-risk-replay,
walk-forward-transactions, walk-forward-costs, walk-forward-slippage,
walk-forward-liquidity, walk-forward-valuation, walk-forward-returns,
walk-forward-turnover, walk-forward-benchmark, walk-forward-drawdown,
walk-forward-stability, walk-forward-parameter-sensitivity,
walk-forward-regimes, walk-forward-run, walk-forward-show,
walk-forward-list, walk-forward-lineage, walk-forward-reproducibility,
walk-forward-explain, portfolio-walk-forward-report

FORBIDDEN CLI commands (not created):
walk-forward-execute, walk-forward-submit, walk-forward-broker,
walk-forward-live-rebalance, walk-forward-apply-live

## GUI

Research-only panel (headless safe):
- No QApplication import at module level
- All views: HISTORICAL_SIMULATION_ONLY
- No forbidden controls (Execute, Submit, Buy, Sell, etc.)
- PRODUCTION_TRADING_BLOCKED = True

## Safety Boundaries

```
HISTORICAL_SIMULATION_ONLY = True
NOT_AN_ORDER = True
NO_BROKER_CALL = True
NO_FORMAL_LEDGER_WRITE = True
PAST_PERFORMANCE_NOT_FUTURE_GUARANTEE = True
PRODUCTION_TRADING_BLOCKED = True
```

## Known Limitations

1. Fixture data only — not real market data in demo/test mode
2. Decision replay applies current engine to historical data (methodology risk)
3. Slippage and cost models are simplified approximations
4. No corporate action adjustments in fixture mode
5. Calendar uses weekday-only (no specific Taiwan holiday calendar in fixtures)
6. Regime classification based on simple thresholds, not ML models
7. Stability score formula is a research approximation, not a validated metric
8. Parameter sensitivity uses fixed demo grid in fixture mode

## Next Version: v1.5.9

Planned improvements (not yet implemented):
- Real data integration for walk-forward backtests
- Taiwan holiday calendar integration
- ML-based regime classification
- Full corporate action adjustments
- Live broker integration (permanently blocked in v1.5.4)
- Enhanced slippage models with real ADV data
