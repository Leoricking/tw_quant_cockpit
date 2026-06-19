# Strategy Knowledge Empirical Backtest v1.4.0

**[!] Research Only | No Real Orders | Broker Execution Disabled | Production Trading BLOCKED | Backtest Does Not Guarantee Future Performance**

## Overview

The Strategy Knowledge Empirical Backtest system (v1.4.0) provides a structured framework for empirically testing quantifiable strategy rules using historical data. It is designed for research and learning purposes only.

## Key Components

### Rule Registry (`empirical_backtest/rule_registry_v140.py`)
- 11 built-in strategy rules registered at startup
- 7 backtestable rules (OHLCV-based, quantifiable conditions)
- 4 manual-only rules (require institutional/margin/financial data)
- Rules: ABC Buy Points (A/B/C), Second Wave Momentum, Volume Breakout, MA Bullish Alignment, Institutional Filter, Margin Risk Filter, Fundamental Turnaround, Sakata Quantifiable, High Win Rate Framework V1

### Data Gate (`empirical_backtest/data_gate_v140.py`)
- Blocks mock/demo/fixture data from formal backtests
- Blocks duplicate bars, missing bars (>5%), future timestamps
- Blocks unknown data sources, stale data, source conflicts
- Blocks insufficient history and unknown corporate actions

### Lookahead Bias Guard (`empirical_backtest/lookahead_guard_v140.py`)
- Blocks same-bar close execution
- Blocks future bar access
- Blocks financial data before release date
- Blocks future universe membership
- Blocks survivorship-only universe without flag

### Corporate Action Guard (`empirical_backtest/corporate_action_guard_v140.py`)
- Passes ADJUSTED and NOT_APPLICABLE status
- Blocks UNKNOWN status across corporate events
- Blocks PARTIALLY_ADJUSTED data
- Warns on UNADJUSTED data

### Cost Model (`empirical_backtest/cost_model_v140.py`)
- Taiwan brokerage rate: 0.1425%
- Transaction tax (stock): 0.3%, ETF: 0.1%
- Minimum fee: TWD 20
- Slippage model: CONSERVATIVE_FIXED (10 bps default)

### Signal Engine (`empirical_backtest/signal_engine_v140.py`)
- Evaluates rule conditions against bar data
- Safe condition parsing (no crashes on missing data)
- No future bar access in condition evaluation

### Backtest Engine (`empirical_backtest/backtest_engine_v140.py`)
- 15-step backtest flow
- dry_run=True by default
- Demo mode produces DEMO_ONLY status (not formal)
- Per-symbol error isolation

### Metrics (`empirical_backtest/backtest_engine_v140.py`)
- 30+ performance metrics including Sharpe, Sortino, Calmar
- Zero trades → all metrics "unavailable" (no crash)
- Includes total fees, taxes, slippage

### Period Split (`empirical_backtest/period_split_v140.py`)
- Train/validation/test split with embargo and purge days
- Walk-forward validation with non-overlapping folds
- All folds preserved (no cherry-picking)

### Confidence Evaluator (`empirical_backtest/confidence_v140.py`)
- Score-based: HIGH/MEDIUM/LOW/INSUFFICIENT/BLOCKED
- Blocks formal conclusion for <10 trades, mock data, BLOCKED status

### Store & Query (`empirical_backtest/store_v140.py`)
- Append-only JSON storage (never overwrites by ID)
- Atomic writes (tmp + rename)
- Query by rule, symbol, universe, status

## Safety Constants

```python
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
BACKTEST_MOCK_FORMAL_CONCLUSION_ALLOWED = False
BACKTEST_AUTO_OPTIMIZATION_ENABLED = False
BACKTEST_AUTO_TRADING_ENABLED = False
```

## CLI Commands

```
strategy-rule-list              List all registered strategy rules
strategy-rule-show              Show details of a specific rule (--rule-id)
strategy-rule-health            Run health check for strategy rule system
empirical-backtest-plan         Build a dry run backtest plan
empirical-backtest-run          Run empirical backtest (dry_run=True by default)
empirical-backtest-show         Show a backtest result (--backtest-id)
empirical-backtest-list         List all backtest runs
empirical-backtest-compare      Compare multiple backtest results
empirical-backtest-walk-forward Run walk-forward validation
empirical-backtest-metrics      Show metrics for a backtest
empirical-backtest-blocked      List blocked backtests
empirical-backtest-create-repair Create repair tasks for blocked backtests
empirical-backtest-report       Generate text report for a backtest
empirical-backtest-health       Run full health check (31 checks)
```

## Limitations

- Formal conclusions require real, adjusted, fresh data
- Institutional/margin/fundamental rules are NOT backtestable without verified data
- Past backtest performance does NOT guarantee future results
- Walk-forward results are research only — not trading signals
- Mock/demo data produces DEMO_ONLY status — no formal conclusions

## Health Check

Run `python main.py empirical-backtest-health` to verify all 31 health checks.

---

**[!] Research Only | No Real Orders | Broker Execution Disabled | Production Trading BLOCKED | Backtest Does Not Guarantee Future Performance**
