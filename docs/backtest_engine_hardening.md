# Backtest Engine Hardening — v0.3.26

> **Research Only / Backtest Only / No Real Orders / Not Investment Advice**
>
> All content in this document describes simulation-only components.
> Production trading is BLOCKED. This is not investment advice.

---

## 1. v0.3.26 目標 (Objectives)

v0.3.26 introduces the **Hardened Backtest Engine**, a set of modules that make
backtesting results more realistic and statistically robust. The goals are:

- Eliminate common look-ahead biases (signal_close entry)
- Apply realistic Taiwan transaction costs (commission + sell tax + slippage)
- Filter illiquid names that could not realistically be traded at simulated sizes
- Account for gap risk endemic to Taiwan's ±10% daily price limit market structure
- Validate strategy stability using walk-forward and out-of-sample splits
- Decompose performance by market regime (bull / bear / sideways / high_volatility)
- Assign confidence grades (A/B/C/D) with clear limitations

**No existing backtests are replaced or modified.** All hardened modules
are additive, housed in `backtest/` with the `hardened_` prefix.

---

## 2. Entry Model: signal_close vs next_open

### Why signal_close is biased

When a signal is generated using **today's close price**, using that same close
as the entry price is unrealistic: the signal is not known until the close is
finalized, and filling at that exact price requires executing at the bell.

This creates **look-ahead bias** — the backtest knows the close before placing
the simulated order, overstating returns.

### Why next_open is more realistic

Using the **open price of the next trading day** reflects how a retail trader
would actually execute: they receive the signal after market close, review it
overnight, and submit an order that fills near the next day's open.

```
signal_close  →  unrealistic, inflated returns, look-ahead bias
next_open     →  realistic for end-of-day signal systems (default)
next_close    →  conservative; trades placed at next-day close
vwap_proxy    →  (high+low+close)/3 on next day, proxy only
```

The v0.3.26 default is `entry_model="next_open"`.

---

## 3. Taiwan Transaction Costs

Taiwan has specific transaction costs that significantly affect net returns,
especially for short-term strategies.

### Components

| Cost Item | Rate | Notes |
|-----------|------|-------|
| Commission (buy) | 0.1425% | Statutory maximum |
| Commission discount | 0.6× | Typical 6-fold discount for online brokers |
| **Effective commission** | **0.0855%** | Per buy trade |
| Commission (sell) | 0.1425% × 0.6 = 0.0855% | Same as buy |
| Securities transaction tax | **0.3%** | Sell only; statutory, no discount |
| Slippage | **5 bps** | Base; scales with market impact |
| Min commission | **20 NTD** | Per trade minimum |

### Round-trip cost estimate

For a 100,000 NTD trade (typical retail size):

```
Buy:   100,000 × 0.000855 = 85.5 NTD commission + 50 NTD slippage = 135.5 NTD
Sell:  100,000 × 0.000855 = 85.5 NTD commission
     + 100,000 × 0.003    = 300 NTD sell tax
     + 50 NTD slippage    = 435.5 NTD
Total: ~571 NTD / 100,000 NTD ≈ 0.57% round-trip cost
```

This means a strategy must generate >0.57% gross return per trade just to break even.
Short-term high-frequency strategies are particularly penalized.

### Zero-cost comparison

Running `cost_model="zero"` vs `cost_model="taiwan_realistic"` reveals the true
drag of transaction costs. A strategy with 2% gross return per trade becomes
~1.43% net — a 28% reduction in profitability.

---

## 4. Liquidity Filter

### Why liquidity matters in backtest

A backtest that ignores liquidity will simulate trades in stocks that could
not realistically be filled at the assumed size. Small-cap stocks in Taiwan
with volume of 100–200 shares per day cannot absorb a 100,000 NTD position
without significant market impact.

### Parameters

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `min_daily_volume` | 500 shares | Minimum daily volume to allow entry |
| `min_daily_turnover` | 10,000,000 NTD | Minimum daily turnover (close × volume) |
| `max_participation_rate` | 5% | Max fraction of daily volume the simulated trade represents |

### Liquidity score (0–100)

- **100**: All checks pass
- **Proportional degradation**: based on how far below thresholds the stock falls
- **0**: No volume data available

Trades failing liquidity checks are marked `status="LIQUIDITY_REJECTED"` and
excluded from performance metrics. This prevents survivorship bias from
illiquid "winners" that could never have been executed.

---

## 5. Gap Risk

### Taiwan context

Taiwan stocks are subject to a **±10% daily price limit**. When a negative
event occurs overnight (earnings miss, geopolitical event), stocks will often
open at the limit-down price with no buyers — making it impossible to exit
at the intended stop-loss price.

This "gap-through" phenomenon means stop-loss orders execute at the open,
not at the intended stop level, causing larger-than-modeled losses.

### Gap classification

| Category | Condition | Action |
|----------|-----------|--------|
| `NO_GAP` | abs(gap) < 3% | Allow entry; no adjustment |
| `GAP_UP_WARNING` | 3% ≤ gap < 6% | Allow but flag; no chase |
| `GAP_UP_BLOCK` | gap ≥ 6% | Block entry (chasing too high) |
| `GAP_DOWN_WARNING` | -6% < gap ≤ -3% | Allow; adjust stop-loss model |
| `GAP_DOWN_STOP` | gap ≤ -6% | Block entry; position dangerous |

### no_chase_gap_pct

Additionally, if abs(gap) ≥ `no_chase_gap_pct` (default 4%), entry is blocked
regardless of direction. This prevents the backtest from assuming fills at
prices that would require chasing a large move.

### Gap stop-loss

When a position is held through a gap-down night, the effective stop-loss
exit is `max(intended_stop, next_open)` — i.e., the position cannot exit
better than the next-day open in a gap scenario.

---

## 6. Walk-forward Validation

### Why better than in-sample only

An **in-sample only** backtest optimizes and evaluates on the same data.
This inflates performance metrics because the strategy has implicitly "seen"
the entire test period during development.

**Walk-forward validation** simulates the real-world process:
1. Train/fit on historical data (training window)
2. Test on unseen future data (test window)
3. Step forward and repeat

This produces multiple test-period samples, each genuinely out-of-sample,
giving a much more honest picture of how the strategy would perform on new data.

### Split methods

| Method | Description | Use case |
|--------|-------------|----------|
| `walk_forward` | Rolling train+test windows stepping by step_days | Primary validation |
| `out_of_sample` | Single train/test split at 70%/30% | Quick OOS check |
| `expanding_window` | Growing training window, fixed test window | Growing dataset scenarios |
| `in_sample_only` | Train = Test = full period | Overfitting risk (labeled) |

### Default parameters

```python
train_window_days = 252  # ~1 trading year
test_window_days = 63    # ~1 trading quarter
step_days = 21           # ~1 trading month
```

---

## 7. Regime Split

### Why regime matters

A strategy that performs well in bull markets may fail in bear markets or
high-volatility regimes. Averaging performance across all regimes masks this
risk and leads to overconfidence.

### Classification rules

Applied in priority order:

1. **high_volatility**: 20-day rolling return std > `volatility_threshold` (0.02 = 2%)
2. **bull**: close > MA60 AND MA20 > MA60 (uptrend confirmed by both price and momentum)
3. **bear**: close < MA60 AND MA20 < MA60
4. **sideways**: else (mixed signals)

### Proxy regime

If no market index data is available, the regime falls back to `"unknown"`.
This is noted with `is_proxy=True` in the regime DataFrame and flagged in the
assumption summary.

---

## 8. Confidence Grade

### Criteria

| Grade | Criteria |
|-------|----------|
| **A** | trades ≥ 100 AND splits ≥ 4 AND each split ≥ 10 trades AND max_drawdown not extreme (>50%) |
| **B** | trades ≥ 50 AND splits ≥ 2 |
| **C** | trades ≥ 20 |
| **D** | else (< 20 trades, insufficient data, too many missing prices) |

### CRITICAL WARNING

> **Even Grade A does NOT authorize live trading.**
>
> The confidence grade reflects the statistical robustness of the backtest
> simulation. It does NOT account for:
> - Future market regime changes
> - Model overfitting to historical patterns
> - Real-world execution frictions beyond the modeled cost assumptions
> - Regulatory, liquidity, or operational risks
> - Any forward-looking predictive validity
>
> **Production Trading: BLOCKED. Research Only / Backtest Only / No Real Orders.**

---

## 9. CLI Usage Examples

Run the hardened backtest from Python:

```python
from backtest.hardened_backtester import HardenedBacktester

bt = HardenedBacktester(
    mode="real",
    entry_model="next_open",
    exit_model="combined",
    cost_model="taiwan_realistic",
    split_method="walk_forward",
    max_holding_days=20,
    stop_loss_pct=0.08,
    take_profit_pct=0.20,
    use_liquidity_filter=True,
    use_gap_risk=True,
    use_regime_split=True,
)
result = bt.run()
print(result["confidence_grade"])
print(result["net_return"])
```

Generate a report:

```python
from reports.hardened_backtest_report import HardenedBacktestReportBuilder

builder = HardenedBacktestReportBuilder(backtest_result=result, mode="real")
report_path = builder.build()
print(f"Report: {report_path}")
```

Compare zero-cost vs realistic:

```python
# Zero cost baseline
bt_zero = HardenedBacktester(cost_model="taiwan_realistic", zero_cost=True)
zero_result = bt_zero.run()

# Realistic cost
bt_real = HardenedBacktester(cost_model="taiwan_realistic", zero_cost=False)
real_result = bt_real.run()

cost_drag = zero_result["net_return"] - real_result["net_return"]
print(f"Cost drag: {cost_drag:.2%}")
```

---

## 10. GUI Usage

The hardened backtest panel is accessible in the TW Quant Cockpit GUI:

1. Navigate to **Hardened Backtest** tab (or add it via `gui/hardened_backtest_panel.py`)
2. Select parameters in the control bar:
   - Entry Model: `next_open` (default) / `signal_close` / `next_close` / `vwap_proxy`
   - Cost Model: `taiwan_realistic` / `zero`
   - Split Method: `walk_forward` / `out_of_sample` / `in_sample_only` / `expanding_window`
   - Max Holding Days: 1–120 (default 20)
   - Mode: `real` / `mock`
3. Click **Run Hardened Backtest** — runs in background thread
4. Review:
   - Summary cards: Net Return, Sharpe, Max DD, Profit Factor, Win Rate, Trade Count, Grade
   - Assumptions table: all model parameters
   - Cost metrics: gross vs net, cost impact
   - Split metrics: per-window OOS performance
   - Regime metrics: bull/bear/sideways/high_volatility breakdown
   - Warnings: data quality, low sample, cost, regime instability
5. Click **Generate Report** to write `reports/hardened_backtest_report_YYYY-MM-DD.md`

---

## 11. Safety Statement

```
════════════════════════════════════════════════════════════════════
  RESEARCH ONLY / BACKTEST ONLY / NO REAL ORDERS
  NOT INVESTMENT ADVICE
════════════════════════════════════════════════════════════════════

  All components described in this document are for research
  and educational purposes ONLY.

  - read_only         = True
  - no_real_orders    = True
  - production_blocked = True

  No orders, positions, or trades are placed by any component
  in this module suite. All results are simulated backtest
  results and do NOT represent actual trading performance.

  Past simulated performance does NOT guarantee future results.
  Backtests have inherent limitations including (but not limited
  to): survivorship bias, look-ahead bias, overfitting,
  transaction cost assumptions, liquidity assumptions,
  market impact assumptions, and regime instability.

  This software MUST NOT be used to make real investment decisions
  without extensive additional due diligence by a qualified
  financial professional.

  Consult a licensed financial advisor before making any
  investment decisions.

  TW Quant Cockpit v0.3.26 — Production Trading: BLOCKED
════════════════════════════════════════════════════════════════════
```

---

*TW Quant Cockpit v0.3.26 — Backtest Engine Hardening*
*Research Only / Backtest Only / No Real Orders / Not Investment Advice*
